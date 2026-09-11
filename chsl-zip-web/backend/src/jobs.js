/**
 * Background ZIP job manager.
 *
 * Job types:
 *   section  — all PDFs of one year/section      -> SSC_CHSL_<section>_Papers.zip
 *   selected — explicitly chosen papers          -> SSC_CHSL_Selected_Papers.zip
 *   retry    — previously failed papers          -> ..._Retry.zip
 *   all      — every PDF on the content source   -> SSC_CHSL_ALL_PAPERS.zip (folders per category/section)
 *
 * Downloads run with bounded concurrency, streamed to temp files (never RAM),
 * failures are collected and never abort the batch. Service is stateless
 * between jobs: temp files are removed immediately, finished ZIPs expire
 * after config.ZIP_TTL_MIN.
 */
'use strict';

const fs = require('fs');
const fsp = require('fs/promises');
const path = require('path');
const crypto = require('crypto');
const archiver = require('archiver');

const cfg = require('./config');
const { downloadPdf } = require('./downloader');
const U = require('./util');

const TMP_ROOT = path.join(__dirname, '..', 'tmp');
const ZIP_ROOT = path.join(__dirname, '..', 'zips');
fs.mkdirSync(TMP_ROOT, { recursive: true });
fs.mkdirSync(ZIP_ROOT, { recursive: true });

class Job {
  constructor(id, type, papers, zipName, folderMode) {
    this.id = id;
    this.type = type;
    this.papers = papers;          // [{id,name,series,url,sectionTitle,categoryTitle,categoryKey,sectionId}]
    this.zipName = zipName;
    this.folderMode = folderMode;  // 'flat' | 'tree'
    this.state = 'queued';        // queued|downloading|zipping|done|error|cancelled
    this.total = papers.length;
    this.done = 0;
    this.ok = 0;
    this.failed = [];              // {id,name,reason}
    this.current = [];
    this.zipPath = null;
    this.zipBytes = 0;
    this.error = null;
    this.createdAt = Date.now();
    this.finishedAt = null;
    this.cancelled = false;
  }

  toJSON() {
    return {
      id: this.id,
      type: this.type,
      state: this.state,
      total: this.total,
      done: this.done,
      ok: this.ok,
      failed: this.failed,
      current: this.current,
      zipName: this.state === 'done' ? this.zipName : undefined,
      zipBytes: this.zipBytes || undefined,
      zipUrl: this.state === 'done' ? `/api/job/${this.id}/zip` : undefined,
      error: this.error,
      createdAt: this.createdAt,
      finishedAt: this.finishedAt,
    };
  }
}

class JobManager {
  constructor() {
    this.jobs = new Map();
    this.running = 0;
    setInterval(() => this.cleanup(), 10 * 60 * 1000).unref();
  }

  create(type, papers, zipName, folderMode) {
    const id = crypto.randomBytes(8).toString('hex');
    const job = new Job(id, type, papers, zipName, folderMode);
    this.jobs.set(id, job);
    this.run(job);
    return job;
  }

  runningCount() {
    let n = 0;
    for (const j of this.jobs.values())
      if (j.state === 'queued' || j.state === 'downloading' || j.state === 'zipping') n++;
    return n;
  }

  get(id) { return this.jobs.get(id); }

  async run(job) {
    try {
      job.state = 'downloading';

      const tmpDir = path.join(TMP_ROOT, job.id);
      await fsp.mkdir(tmpDir, { recursive: true });
      const files = [];   // {file, entry}
      const used = new Set();

      // build entry names up-front (numbering over the whole batch)
      const entries = job.papers.map((p, i) =>
        U.buildEntryName(p.name, p.series, i, job.total, used));

      // ---- bounded-concurrency download pool (streaming to disk) ----
      let cursor = 0;
      const worker = async () => {
        for (;;) {
          if (job.cancelled) return;
          const i = cursor++;
          if (i >= job.papers.length) return;
          const p = job.papers[i];
          job.current.push(p.name);
          const dest = path.join(tmpDir, `p${i}.pdf`);
          try {
            await downloadPdf(p.url, dest);
            files.push({ file: dest, entry: entries[i], paper: p, idx: i });
            job.ok++;
          } catch (e) {
            job.failed.push({
              id: p.id,
              name: p.name,
              reason: (e && e.reason) || String(e && e.message || e).slice(0, 120),
            });
          }
          job.done++;
          job.current = job.current.filter((n) => n !== p.name);
        }
      };
      await Promise.all(
        Array.from({ length: Math.min(cfg.CONCURRENCY, job.total) }, worker));

      if (job.cancelled) {
        await fsp.rm(tmpDir, { recursive: true, force: true });
        job.state = 'cancelled';
        job.finishedAt = Date.now();
        return;
      }

      // ---- zip phase (streamed, low RAM) ----
      if (files.length === 0) {
        await fsp.rm(tmpDir, { recursive: true, force: true });
        job.state = 'error';
        job.error = 'All downloads failed';
        job.finishedAt = Date.now();
        return;
      }

      job.state = 'zipping';
      files.sort((a, b) => a.idx - b.idx);

      const zipPath = path.join(ZIP_ROOT, `${job.id}.zip`);
      await new Promise((resolve, reject) => {
        const out = fs.createWriteStream(zipPath);
        const zip = archiver('zip', { zlib: { level: 1 } });
        out.on('close', resolve);
        out.on('error', reject);
        zip.on('error', reject);
        zip.pipe(out);
        for (const f of files) {
          let entryName = f.entry;
          if (job.folderMode === 'tree') {
            const cat = U.sanitize(f.paper.categoryTitle) || 'Papers';
            const sec = U.sanitize(f.paper.sectionTitle) || 'Papers';
            entryName = `${cat}/${sec}/${f.entry}`;
          }
          zip.file(f.file, { name: entryName });
        }
        zip.finalize();
      });

      const st = await fsp.stat(zipPath);
      job.zipPath = zipPath;
      job.zipBytes = st.size;
      job.state = 'done';
      job.finishedAt = Date.now();

      // temp files no longer needed — remove immediately
      await fsp.rm(tmpDir, { recursive: true, force: true });
    } catch (e) {
      job.state = 'error';
      job.error = String((e && e.message) || e).slice(0, 200);
      job.finishedAt = Date.now();
      try {
        await fsp.rm(path.join(TMP_ROOT, job.id), { recursive: true, force: true });
      } catch (_) {}
    }
  }

  cancel(id) {
    const j = this.jobs.get(id);
    if (!j) return false;
    if (j.state === 'queued' || j.state === 'downloading' || j.state === 'zipping') {
      j.cancelled = true;
      return true;
    }
    return false;
  }

  recentDone(limit = 8) {
    return [...this.jobs.values()]
      .filter((j) => j.state === 'done')
      .sort((a, b) => b.finishedAt - a.finishedAt)
      .slice(0, limit)
      .map((j) => ({
        id: j.id,
        zipName: j.zipName,
        ok: j.ok,
        total: j.total,
        zipBytes: j.zipBytes,
        finishedAt: j.finishedAt,
      }));
  }

  /** Delete expired ZIPs (default 3h) — nothing is kept on the server forever. */
  async cleanup() {
    const cutoff = Date.now() - cfg.ZIP_TTL_MIN * 60 * 1000;
    let n = 0;
    for (const j of this.jobs.values()) {
      if (j.state === 'done' && j.finishedAt < cutoff && j.zipPath) {
        try { await fsp.unlink(j.zipPath); } catch (_) {}
        j.zipPath = null;
        j.state = 'expired';
        n++;
      }
    }
    // orphan tmp dirs
    try {
      const dirs = await fsp.readdir(TMP_ROOT);
      for (const d of dirs) {
        const p = path.join(TMP_ROOT, d);
        const st = await fsp.stat(p);
        if (st.mtimeMs < cutoff) await fsp.rm(p, { recursive: true, force: true });
      }
    } catch (_) {}
    if (n) console.log(`[jobs] cleaned ${n} expired zip(s)`);
  }
}

module.exports = new JobManager();
