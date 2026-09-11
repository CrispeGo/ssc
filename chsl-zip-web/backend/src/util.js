/**
 * Filename utilities — web port of the same rules used across this project
 * (sanitization, dedup with _1/_2, language tags, zero-padded numbering).
 */
'use strict';

function sanitize(s) {
  if (!s) return '';
  s = String(s)
    .replace(/\u2013/g, '-').replace(/\u2014/g, '-')
    .replace(/\u2018/g, "'").replace(/\u2019/g, "'")
    .replace(/\u201C/g, '"').replace(/\u201D/g, '"');
  let r = '';
  for (const ch of s) {
    if (/[A-Za-z0-9]/.test(ch)) r += ch;
    else if (ch === ' ' || ch === '-' || ch === '(' || ch === ')' || ch === '_' || ch === '.' || ch === ',') r += ch;
    else r += '_';
  }
  r = r.trim().replace(/[_ ]+/g, '_');
  while (r.startsWith('_')) r = r.slice(1);
  while (r.endsWith('_')) r = r.slice(0, -1);
  return r;
}

function detectLanguage(name) {
  if (!name) return null;
  const low = String(name).toLowerCase();
  const hi = low.includes('hindi');
  const en = low.includes('english');
  if (hi && !en) return 'Hindi';
  if (en && !hi) return 'English';
  return null;
}

/**
 * Build a readable, unique entry name for one paper.
 * "01_CHSL_Tier-I_(02_July_2024)_Shift-_4_A5.pdf"
 */
function buildEntryName(paperName, series, index, total, used) {
  const width = total >= 100 ? 3 : 2;
  const prefix = String(index + 1).padStart(width, '0') + '_';
  let base = sanitize(paperName);
  if (!base) base = 'Paper_' + (index + 1);
  const sr = sanitize(series);
  if (sr && !base.toLowerCase().includes(sr.toLowerCase())) base += '_' + sr;
  const lang = detectLanguage(paperName);
  if (lang && !base.toLowerCase().includes(lang.toLowerCase())) base += '_' + lang;
  if (base.length > 90) base = base.slice(0, 90);
  let name = prefix + base + '.pdf';
  let candidate = name;
  let n = 1;
  while (used.has(candidate.toLowerCase())) {
    candidate = prefix + base + '_' + n + '.pdf';
    n++;
  }
  used.add(candidate.toLowerCase());
  return candidate;
}

function isYear(s) {
  return !!s && /^\d{4}$/.test(String(s).trim());
}

/** "SSC_CHSL_2025_Papers.zip" / "SSC_CHSL_Tier-I_PYQs_(Hindi)_2024_Papers.zip" */
function sectionZipName(categoryTitle, sectionTitle, categoryKey) {
  const sec = sanitize(sectionTitle) || 'Papers';
  // The primary English PYQ years keep the clean classic name the user expects.
  if (categoryKey === 'pyq-en' && isYear(sectionTitle)) {
    return 'SSC_CHSL_' + sec + '_Papers.zip';
  }
  const cat = sanitize(categoryTitle);
  if (!cat) return 'SSC_CHSL_' + sec + '_Papers.zip';
  return 'SSC_CHSL_' + cat + '_' + sec + '_Papers.zip';
}

const SELECTED_ZIP = 'SSC_CHSL_Selected_Papers.zip';
const ALL_ZIP = 'SSC_CHSL_ALL_PAPERS.zip';

module.exports = {
  sanitize,
  detectLanguage,
  buildEntryName,
  isYear,
  sectionZipName,
  SELECTED_ZIP,
  ALL_ZIP,
};
