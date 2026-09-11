/**
 * Content service — mirrors EXACTLY what the original app does:
 *
 *  Home3 (fragment) builds 6 category cards from string resources:
 *    "Tier-I PYQs (English)"  -> /b_data.json
 *    "Tier-I PYQs (Hindi)"    -> /handwritten.json
 *    "Solved Subjectwise PYQs"-> /mcq.json
 *    "All Subject Notes"      -> /questionbank.json
 *    "Tier-II PYQs"           -> /revision.json
 *    "Educational Games"      -> /c_data.json   (gamezop links — no PDFs)
 *  URL = CONTENT_BASE + <json path>
 *  BoxActivity fetches the JSON (categories[] {name, data[]}),
 *  ChaptersActivity shows data[] items {name, series, extra}
 *  where extra = "<pdf-url>#pdf_data" (or #html_data / gamezop).
 *
 * This module discovers everything dynamically from those same endpoints —
 * new years/categories appear on the website automatically.
 */
'use strict';

const crypto = require('crypto');
const cfg = require('./config');

// The category map below is the ONLY thing taken from the APK's static
// resources (titles + json file names). The content itself is 100% dynamic.
const CATEGORY_DEFS = [
  { key: 'pyq-en', title: 'Tier-I PYQs (English)', json: '/b_data.json' },
  { key: 'pyq-hi', title: 'Tier-I PYQs (Hindi)', json: '/handwritten.json' },
  { key: 'mcq', title: 'Solved Subjectwise PYQs', json: '/mcq.json' },
  { key: 'notes', title: 'All Subject Notes', json: '/questionbank.json' },
  { key: 'pyq2', title: 'Tier-II PYQs', json: '/revision.json' },
  { key: 'games', title: 'Educational Games', json: '/c_data.json' },
];

function paperId(url) {
  return crypto.createHash('sha1').update(url).digest('hex').slice(0, 12);
}

function stripFragment(u) {
  if (!u) return '';
  const h = u.indexOf('#');
  return h >= 0 ? u.slice(0, h) : u;
}

class ContentService {
  constructor() {
    this.cache = null;          // {at, data}
    this.fetching = null;       // promise de-dup
  }

  async fetchJson(url) {
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Linux; Android 13) CHSL-Zip-Web/1.0' },
      signal: AbortSignal.timeout(30000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
    return res.json();
  }

  async load(force = false) {
    if (!force && this.cache && Date.now() - this.cache.at < cfg.CONTENT_TTL_MS) {
      return this.cache.data;
    }
    if (!force && this.fetching) return this.fetching;

    this.fetching = (async () => {
      const categories = [];
      const paperIndex = new Map(); // id -> paper (flat, for jobs/search)

      const results = await Promise.allSettled(
        CATEGORY_DEFS.map((def) => this.fetchJson(cfg.CONTENT_BASE + def.json))
      );

      results.forEach((r, i) => {
        const def = CATEGORY_DEFS[i];
        if (r.status !== 'fulfilled' || !r.value || !Array.isArray(r.value.categories)) {
          // A missing/broken JSON must never take the whole site down.
          console.warn(`[content] ${def.json} unavailable:`,
            r.status === 'rejected' ? String(r.reason).slice(0, 120) : 'bad shape');
          return;
        }
        const sections = [];
        const seenUrlsInSection = new Set();
        for (const cat of r.value.categories) {
          const sectionTitle = String(cat && cat.name != null ? cat.name : '').trim() || 'Papers';
          const rawItems = Array.isArray(cat && cat.data) ? cat.data : [];
          const papers = [];
          for (const it of rawItems) {
            const extra = String((it && it.extra) || '');
            if (!extra.toLowerCase().includes('pdf_data')) continue; // html_data/gamezop filtered
            const url = stripFragment(extra.trim());
            if (!/^https?:\/\//i.test(url)) continue;
            if (seenUrlsInSection.has(url)) continue; // exact dup within section
            seenUrlsInSection.add(url);
            papers.push({
              id: paperId(url),
              name: String((it && it.name) || `Paper ${papers.length + 1}`),
              series: String((it && it.series) || ''),
              url,
            });
          }
          if (papers.length > 0) {
            const sectionId = `${def.key}--${sections.length}`;
            for (const p of papers) p.sectionId = sectionId;
            sections.push({ id: sectionId, title: sectionTitle, papers });
          }
        }
        if (sections.length > 0) {
          const category = {
            key: def.key,
            title: def.title,
            sections,
            paperCount: sections.reduce((a, s) => a + s.papers.length, 0),
          };
          for (const s of sections) {
            s.categoryKey = def.key;
            s.categoryTitle = def.title;
            for (const p of s.papers) {
              p.categoryKey = def.key;
              p.categoryTitle = def.title;
              p.sectionTitle = s.title;
              if (!paperIndex.has(p.id)) paperIndex.set(p.id, p);
            }
          }
          categories.push(category);
        }
      });

      const totalPapers = categories.reduce(
        (a, c) => a + c.paperCount, 0);
      const data = {
        categories,
        totals: {
          categories: categories.length,
          sections: categories.reduce((a, c) => a + c.sections.length, 0),
          papers: totalPapers,
        },
        generatedAt: new Date().toISOString(),
      };
      this.cache = { at: Date.now(), data };
      return data;
    })();

    try {
      return await this.fetching;
    } finally {
      this.fetching = null;
    }
  }

  findSection(sectionId) {
    for (const c of this.cache ? this.cache.data.categories : []) {
      for (const s of c.sections) if (s.id === sectionId) return s;
    }
    return null;
  }

  findPapers(ids) {
    const out = [];
    if (!this.cache) return out;
    const index = new Map();
    for (const c of this.cache.data.categories)
      for (const s of c.sections) for (const p of s.papers) index.set(p.id, p);
    for (const id of ids) {
      const p = index.get(id);
      if (p) out.push(p);
    }
    return out;
  }

  allPapers() {
    const out = [];
    if (!this.cache) return out;
    for (const c of this.cache.data.categories)
      for (const s of c.sections) for (const p of s.papers) out.push(p);
    return out;
  }
}

module.exports = new ContentService();
