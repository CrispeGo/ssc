/**
 * CHSL Previous Year Papers — ZIP Web App (backend)
 *
 * Serves the mobile frontend and a hardened JSON/PDF/ZIP API.
 * Content source + structure verified from the original APK:
 *   Home3 -> BoxActivity -> ChaptersActivity -> PdfViewerActivity
 *   https://bollywoodnewstoday.com/appdata/com.tarun.sscchslpreviousyearpapers/<x>.json
 */
'use strict';

const express = require('express');
const path = require('path');
const fs = require('fs');

const cfg = require('./config');
const content = require('./content');
const jobs = require('./jobs');
const { proxyPdf, DownloadError } = require('./downloader');
const U = require('./util');

const app = express();
app.disable('x-powered-by');
app.use(express.json({ limit: '256kb' }));

// ---- tiny per-IP rate limit for job creation ----
const rate = new Map();
setInterval(() => {
  const cutoff = Date.now() - 60000;
  for (const [k, v] of rate) if (v.t < cutoff) rate.delete(k);
}, 60000).unref();

function rateLimited(ip) {
  const now = Date.now();
  const r = rate.get(ip) || { t: now, n: 0 };
  if (now - r.t > 60000) { r.t = now; r.n = 0; }
  r.n++;
  rate.set(ip, r);
  return r.n > cfg.JOB_CREATE_RATE_PER_MIN;
}

function fail(res, status, message) {
  res.status(status).json({ error: message });
}

// ----------------------------------------------------------------- health
app.get('/api/health', (req, res) => {
  res.json({ ok: true, time: new Date().toISOString() });
});

// ----------------------------------------------------------------- content
app.get('/api/content', async (req, res, next) => {
  try {
    const data = await content.load();
    res.json(data);
  } catch (e) { next(e); }
});

// ------------------------------------------------------------ single PDF
// Same-origin validated proxy: whitelist + %PDF magic bytes + size cap.
// ?dl=1 -> attachment (DOWNLOAD PDF), otherwise inline (OPEN PDF -> Chrome's
// native viewer handles it).
app.get('/api/pdf', async (req, res, next) => {
  try {
    const url = String(req.query.url || '');
    const download = req.query.dl === '1';
    if (download) {
      // best-effort readable filename from the query
      let name = String(req.query.name || '').trim();
      name = U.sanitize(name) || 'paper';
      if (!name.toLowerCase().endsWith('.pdf')) name += '.pdf';
      res.setHeader('Content-Disposition',
        `attachment; filename="${name.replace(/"/g, '')}"; filename*=UTF-8''${encodeURIComponent(name)}`);
    } else {
      res.setHeader('Content-Disposition', 'inline');
    }
    await proxyPdf(url, res);
  } catch (e) {
    if (e instanceof DownloadError) return fail(res, 400, e.reason);
    next(e);
  }
});

// ------------------------------------------------------------------ jobs
app.post('/api/create-job', async (req, res, next) => {
  try {
    if (rateLimited(req.ip)) return fail(res, 429, 'Too many job requests, slow down.');
    await content.load();

    const body = req.body || {};
    const type = body.type;

    if (jobs.runningCount() >= cfg.MAX_RUNNING_JOBS) {
      return fail(res, 409, 'A download job is already running. Wait for it to finish or cancel it.');
    }

    let papers = [];
    let zipName;
    let folderMode = 'flat';

    if (type === 'section') {
      const section = content.findSection(String(body.sectionId || ''));
      if (!section) return fail(res, 404, 'Unknown section');
      papers = section.papers;
      zipName = U.sectionZipName(section.categoryTitle, section.title, section.categoryKey);
    } else if (type === 'selected') {
      const ids = Array.isArray(body.paperIds) ? body.paperIds.map(String) : [];
      if (ids.length === 0) return fail(res, 400, 'No papers selected');
      papers = content.findPapers(ids);
      if (papers.length === 0) return fail(res, 404, 'Papers not found');
      zipName = U.SELECTED_ZIP;
    } else if (type === 'retry') {
      const ids = Array.isArray(body.paperIds) ? body.paperIds.map(String) : [];
      if (ids.length === 0) return fail(res, 400, 'No papers to retry');
      papers = content.findPapers(ids);
      if (papers.length === 0) return fail(res, 404, 'Papers not found');
      const first = papers[0];
      zipName = U.sectionZipName(first.categoryTitle, first.sectionTitle, first.categoryKey)
        .replace(/\.zip$/, '_Retry.zip');
    } else if (type === 'all') {
      papers = content.allPapers();
      if (papers.length === 0) return fail(res, 404, 'No PDF content available');
      zipName = U.ALL_ZIP;
      folderMode = 'tree';
    } else {
      return fail(res, 400, 'Invalid job type');
    }

    if (papers.length > cfg.MAX_FILES) {
      return fail(res, 400, `Too many files (${papers.length} > ${cfg.MAX_FILES})`);
    }

    const job = jobs.create(type, papers, zipName, folderMode);
    res.status(202).json({ jobId: job.id, total: job.total, zipName });
  } catch (e) { next(e); }
});

app.get('/api/job/:id', (req, res) => {
  const job = jobs.get(req.params.id);
  if (!job) return fail(res, 404, 'Unknown job');
  res.json(job.toJSON());
});

app.post('/api/job/:id/cancel', (req, res) => {
  const job = jobs.get(req.params.id);
  if (!job) return fail(res, 404, 'Unknown job');
  const ok = jobs.cancel(req.params.id);
  res.json({ cancelled: ok, state: job.state });
});

app.get('/api/job/:id/zip', (req, res) => {
  const job = jobs.get(req.params.id);
  if (!job) return fail(res, 404, 'Unknown job');
  if (job.state !== 'done' || !job.zipPath || !fs.existsSync(job.zipPath)) {
    return fail(res, job.state === 'expired' ? 410 : 409, `Job not ready (state: ${job.state})`);
  }
  res.setHeader('Content-Length', String(job.zipBytes));
  res.download(job.zipPath, job.zipName);
});

app.get('/api/jobs/recent', (req, res) => {
  res.json({ recent: jobs.recentDone() });
});

// ---------------------------------------------------------------- static
const FRONTEND = path.join(__dirname, '..', '..', 'frontend');
app.use(express.static(FRONTEND, { index: 'index.html', maxAge: '1h' }));

app.use('/api', (req, res) => fail(res, 404, 'Unknown API endpoint'));

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  console.error('[server]', err);
  fail(res, 500, 'Internal error');
});

const server = app.listen(cfg.PORT, cfg.HOST, () => {
  console.log(`CHSL ZIP Web listening on http://${cfg.HOST}:${cfg.PORT}`);
  console.log(`Content base: ${cfg.CONTENT_BASE}`);
  console.log(`Allowed hosts: ${cfg.ALLOWED_HOSTS.join(', ')}`);
});

server.keepAliveTimeout = 75000;
