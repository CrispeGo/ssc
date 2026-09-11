/**
 * Central configuration — everything overridable via environment variables.
 * Defaults reflect the VERIFIED architecture of the original APK:
 *   Home3 -> BoxActivity -> ChaptersActivity -> PdfViewerActivity
 *   content base: https://bollywoodnewstoday.com/appdata/<package>/
 *   JSONs: b_data.json, handwritten.json, mcq.json, questionbank.json, revision.json, c_data.json
 */
require('dotenv').config();

function num(v, d) {
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : d;
}

const CONTENT_BASE =
  process.env.CONTENT_BASE ||
  'https://bollywoodnewstoday.com/appdata/com.tarun.sscchslpreviousyearpapers';

const ALLOWED_HOSTS = (process.env.ALLOWED_HOSTS ||
  'bollywoodnewstoday.com,www.bollywoodnewstoday.com')
  .split(',')
  .map((h) => h.trim().toLowerCase())
  .filter(Boolean);

// PDFs must live under this path prefix on the allowed hosts.
const ALLOWED_PATH_PREFIX = process.env.ALLOWED_PATH_PREFIX || '/appdata/';

module.exports = {
  PORT: num(process.env.PORT, 3000),
  HOST: process.env.HOST || '0.0.0.0',

  CONTENT_BASE,
  ALLOWED_HOSTS,
  ALLOWED_PATH_PREFIX,

  // Content JSON cache (ms) — new server content appears automatically after this.
  CONTENT_TTL_MS: num(process.env.CONTENT_TTL_MS, 5 * 60 * 1000),

  // Download hardening.
  CONCURRENCY: num(process.env.CONCURRENCY, 5),
  MAX_FILE_MB: num(process.env.MAX_FILE_MB, 150),
  MAX_FILES: num(process.env.MAX_FILES, 1500),
  FILE_TIMEOUT_MS: num(process.env.FILE_TIMEOUT_MS, 180000), // per attempt
  MAX_REDIRECTS: 5,

  // Job management.
  MAX_RUNNING_JOBS: num(process.env.MAX_RUNNING_JOBS, 2),
  JOB_CREATE_RATE_PER_MIN: num(process.env.JOB_CREATE_RATE_PER_MIN, 20),

  // Finished ZIPs are deleted from the server after this (minutes).
  ZIP_TTL_MIN: num(process.env.ZIP_TTL_MIN, 180),
};
