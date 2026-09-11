/**
 * Hardened PDF downloader.
 *
 * Security rules (this is NOT an open proxy):
 *  - only https
 *  - only whitelisted hosts (config.ALLOWED_HOSTS)
 *  - only under the /appdata/ path prefix
 *  - redirects followed manually, EVERY hop re-validated
 *  - content-type sanity (text/html -> reject)
 *  - first bytes must be %PDF-
 *  - streaming with size cap + timeout
 */
'use strict';

const fs = require('fs');
const fsp = require('fs/promises');
const path = require('path');
const cfg = require('./config');

class DownloadError extends Error {
  constructor(reason) {
    super(reason);
    this.reason = reason;
  }
}

function validateUrl(raw) {
  let u;
  try {
    u = new URL(raw);
  } catch {
    throw new DownloadError('invalid URL');
  }
  if (u.protocol !== 'https:') throw new DownloadError('only https is allowed');
  if (!cfg.ALLOWED_HOSTS.includes(u.hostname.toLowerCase())) {
    throw new DownloadError(`host not allowed: ${u.hostname}`);
  }
  if (!u.pathname.startsWith(cfg.ALLOWED_PATH_PREFIX)) {
    throw new DownloadError('path not allowed');
  }
  return u;
}

/**
 * Fetch a PDF into destPath. Validates everything; throws DownloadError on
 * any rule violation. Returns { bytes }.
 */
async function downloadPdf(rawUrl, destPath) {
  let url = validateUrl(rawUrl).toString();
  const maxBytes = cfg.MAX_FILE_MB * 1024 * 1024;

  for (let hop = 0; hop <= cfg.MAX_REDIRECTS; hop++) {
    const res = await fetch(url, {
      redirect: 'manual',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13) CHSL-Zip-Web/1.0',
        Accept: 'application/pdf,*/*',
      },
      signal: AbortSignal.timeout(cfg.FILE_TIMEOUT_MS),
    }).catch((e) => {
      throw new DownloadError(`network: ${String(e && e.cause ? e.cause.code || e.message : e.message).slice(0, 80)}`);
    });

    if ([301, 302, 303, 307, 308].includes(res.status)) {
      const loc = res.headers.get('location');
      try { res.body && res.body.cancel(); } catch (_) {}
      if (!loc) throw new DownloadError('redirect without location');
      // resolve + re-validate every hop
      url = validateUrl(new URL(loc, url).toString()).toString();
      continue;
    }

    if (!res.ok) throw new DownloadError(`HTTP ${res.status}`);

    const ct = (res.headers.get('content-type') || '').toLowerCase();
    if (ct.includes('text/html')) throw new DownloadError('not a PDF (html response)');

    // Stream to disk, validating the magic bytes from the first chunk and
    // enforcing the size cap — never loads the file into RAM.
    const tmp = destPath + '.part';
    const out = fs.createWriteStream(tmp);
    let bytes = 0;
    let checked = false;
    try {
      const reader = res.body.getReader();
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        if (!checked) {
          const head = Buffer.from(value.buffer, value.byteOffset, Math.min(5, value.byteLength));
          if (head.length < 5 || head[0] !== 0x25 || head[1] !== 0x50 || head[2] !== 0x44 || head[3] !== 0x46 || head[4] !== 0x2d) {
            throw new DownloadError('not a PDF (magic bytes)');
          }
          checked = true;
        }
        bytes += value.byteLength;
        if (bytes > maxBytes) throw new DownloadError(`file exceeds ${cfg.MAX_FILE_MB} MB`);
        if (!out.write(value)) await new Promise((r) => out.once('drain', r));
      }
      if (!checked) throw new DownloadError('empty response');
      await new Promise((r) => out.end(r));
    } catch (e) {
      out.destroy();
      try { await fsp.unlink(tmp); } catch (_) {}
      if (e instanceof DownloadError) throw e;
      throw new DownloadError(`stream: ${String(e.message || e).slice(0, 80)}`);
    }

    try { await fsp.rename(tmp, destPath); } catch (_) {
      // rename can fail across some setups — copy fallback
      await fsp.copyFile(tmp, destPath);
      try { await fsp.unlink(tmp); } catch (_) {}
    }
    return { bytes };
  }
  throw new DownloadError('too many redirects');
}

/** Streaming proxy body for single-PDF view/download (same validation rules). */
async function proxyPdf(rawUrl, res) {
  let url = validateUrl(rawUrl).toString();
  for (let hop = 0; hop <= cfg.MAX_REDIRECTS; hop++) {
    const upstream = await fetch(url, {
      redirect: 'manual',
      headers: { 'User-Agent': 'Mozilla/5.0 (Linux; Android 13) CHSL-Zip-Web/1.0' },
      signal: AbortSignal.timeout(cfg.FILE_TIMEOUT_MS),
    }).catch((e) => {
      throw new DownloadError(`network: ${String(e && e.message || e).slice(0, 80)}`);
    });

    if ([301, 302, 303, 307, 308].includes(upstream.status)) {
      const loc = upstream.headers.get('location');
      try { upstream.body && upstream.body.cancel(); } catch (_) {}
      if (!loc) throw new DownloadError('redirect without location');
      url = validateUrl(new URL(loc, url).toString()).toString();
      continue;
    }
    if (!upstream.ok) throw new DownloadError(`HTTP ${upstream.status}`);
    const ct = (upstream.headers.get('content-type') || '').toLowerCase();
    if (ct.includes('text/html')) throw new DownloadError('not a PDF (html response)');

    // buffer first chunk to validate magic bytes before sending anything
    const reader = upstream.body.getReader();
    const first = await reader.read();
    if (first.done) throw new DownloadError('empty response');
    const head = Buffer.from(first.value.buffer, first.value.byteOffset, Math.min(5, first.value.byteLength));
    if (head.length < 5 || head[0] !== 0x25 || head[1] !== 0x50 || head[2] !== 0x44 || head[3] !== 0x46 || head[4] !== 0x2d) {
      try { reader.cancel(); } catch (_) {}
      throw new DownloadError('not a PDF (magic bytes)');
    }

    const len = parseInt(upstream.headers.get('content-length') || '0', 10);
    res.status(200);
    res.setHeader('Content-Type', 'application/pdf');
    if (len > 0) res.setHeader('Content-Length', String(len));
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.write(first.value);
    const out = res;
    let bytes = first.value.byteLength;
    try {
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        bytes += value.byteLength;
        if (bytes > cfg.MAX_FILE_MB * 1024 * 1024) {
          try { reader.cancel(); } catch (_) {}
          out.destroy();
          return;
        }
        if (!out.write(value)) await new Promise((r) => out.once('drain', r));
      }
    } catch (e) {
      // client disconnect etc.
    }
    out.end();
    return;
  }
  throw new DownloadError('too many redirects');
}

module.exports = { downloadPdf, proxyPdf, validateUrl, DownloadError };
