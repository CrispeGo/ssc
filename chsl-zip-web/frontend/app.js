/**
 * CHSL ZIP Web — frontend
 * Navigation mirrors the original app: HOME -> CATEGORY -> YEAR/SECTION -> PAPERS -> PDF
 * plus: search, selective download, ZIP jobs with real progress, recent downloads.
 */
'use strict';

(() => {
  const $view = document.getElementById('view');
  const $title = document.getElementById('title');
  const $back = document.getElementById('backBtn');
  const $toast = document.getElementById('toast');

  const state = {
    content: null,        // {categories, totals}
    route: { view: 'home' },
    selections: {},       // sectionId -> Set(paperId)
    activeJobId: localStorage.getItem('chsl_active_job') || null,
  };

  // ------------------------------------------------------------ helpers
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function toast(msg, ms = 2600) {
    $toast.textContent = msg;
    $toast.hidden = false;
    clearTimeout(toast._t);
    toast._t = setTimeout(() => { $toast.hidden = true; }, ms);
  }

  async function api(path, opts) {
    const r = await fetch(path, opts);
    if (!r.ok) {
      let msg = `HTTP ${r.status}`;
      try { const j = await r.json(); if (j.error) msg = j.error; } catch (_) {}
      throw new Error(msg);
    }
    return r.json();
  }

  const fmtBytes = (b) => {
    if (!b && b !== 0) return '';
    if (b > 1024 * 1024 * 1024) return (b / 1073741824).toFixed(2) + ' GB';
    if (b > 1024 * 1024) return (b / 1048576).toFixed(1) + ' MB';
    if (b > 1024) return (b / 1024).toFixed(0) + ' KB';
    return b + ' B';
  };

  const CAT_EMOJI = { 'pyq-en': '📄', 'pyq-hi': '📜', mcq: '🧩', notes: '📚', 'pyq2': '🗂️' };

  // ------------------------------------------------------------ router
  function go(route, push = true) {
    state.route = route;
    if (push) history.pushState({ route }, '');
    render();
  }
  window.addEventListener('popstate', () => {
    const r = history.state && history.state.route;
    state.route = r || { view: 'home' };
    render();
  });
  $back.addEventListener('click', () => history.back());

  function setTitle(t) { $title.textContent = t; }
  function showBack(b) { $back.hidden = !b; }

  async function render() {
    const r = state.route;
    removeActionbar();
    if (r.view === 'home') return renderHome();
    if (r.view === 'category') return renderCategory(r.categoryKey);
    if (r.view === 'section') return renderSection(r.sectionId);
    if (r.view === 'search') return renderSearch(r.q);
    if (r.view === 'job') return renderJob(r.jobId);
    renderHome();
  }

  // ------------------------------------------------------------ loading
  function loadingHtml(msg = 'Loading…') {
    return `<div class="loading"><div class="spinner"></div>${esc(msg)}</div>`;
  }

  async function ensureContent() {
    if (state.content) return state.content;
    try {
      state.content = await api('/api/content');
    } catch (e) {
      $view.innerHTML = `<div class="empty">⚠️ Couldn't load content.<br>${esc(e.message)}<br><br>
        <button class="btn btn-primary" style="max-width:220px" onclick="location.reload()">Retry</button></div>`;
      throw e;
    }
    return state.content;
  }

  // ------------------------------------------------------------ HOME
  async function renderHome() {
    setTitle('SSC CHSL Previous Year Papers');
    showBack(false);
    $view.innerHTML = loadingHtml();
    const c = await ensureContent();

    const recentsHtml = await recentsBlock();

    const cards = c.categories
      .filter((cat) => cat.paperCount > 0)
      .map((cat) => `
        <div class="card" data-cat="${esc(cat.key)}">
          <div class="emoji">${CAT_EMOJI[cat.key] || '📁'}</div>
          <div class="card-title">${esc(cat.title)}</div>
          <div class="card-count">${cat.sections.length} section${cat.sections.length !== 1 ? 's' : ''} · ${cat.paperCount} PDFs</div>
        </div>`).join('');

    $view.innerHTML = `
      <div class="search-wrap">
        <svg viewBox="0 0 24 24" width="19" height="19"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14"/></svg>
        <input id="search" type="search" placeholder="Search papers, years, subjects…" autocomplete="off">
      </div>

      <div class="hero">
        <h2>📦 Download Everything</h2>
        <p>${c.totals.categories} categories · ${c.totals.sections} sections · ${c.totals.papers} PDFs — one master ZIP with organised folders.</p>
        <button class="btn btn-primary" id="btn-all">📦 DOWNLOAD EVERYTHING</button>
      </div>

      <div class="grid">${cards}</div>
      ${recentsHtml}
      <p class="hint">Same content &amp; structure as the CHSL app · new papers appear automatically when the source updates.</p>
    `;

    document.getElementById('search').addEventListener('input', (e) => {
      const q = e.target.value.trim();
      if (q.length >= 2) go({ view: 'search', q }, true);
      else if (state.route.view === 'search') history.back();
    });

    document.getElementById('btn-all').addEventListener('click', () => {
      confirmModal(
        'Download Everything?',
        `Categories: ${c.totals.categories}\nPDFs: ${c.totals.papers}\n\nThe server will download every PDF and build SSC_CHSL_ALL_PAPERS.zip. Keep this page open — you can also leave and come back.`,
        () => startJob({ type: 'all' })
      );
    });

    $view.querySelectorAll('.card[data-cat]').forEach((el) =>
      el.addEventListener('click', () => go({ view: 'category', categoryKey: el.dataset.cat })));
  }

  async function recentsBlock() {
    let recent = [];
    try { recent = (await api('/api/jobs/recent')).recent; } catch (_) {}
    if (!recent.length) return '';
    const items = recent.map((j) => `
      <div class="recent-item">
        <div class="r-main">
          <div class="r-name">${esc(j.zipName)}</div>
          <div class="r-sub">${j.ok}/${j.total} PDFs · ${fmtBytes(j.zipBytes)} · ${new Date(j.finishedAt).toLocaleString()}</div>
        </div>
        <a class="sm-btn sm-dl" style="flex:0 0 auto;padding:0 14px;text-decoration:none" href="/api/job/${esc(j.id)}/zip">⬇ Save</a>
      </div>`).join('');
    return `<div class="recent"><h3>Recent Downloads</h3>${items}
      <p class="hint">ZIPs are removed from the server automatically after a few hours.</p></div>`;
  }

  // ------------------------------------------------------------ CATEGORY
  async function renderCategory(categoryKey) {
    const c = await ensureContent();
    const cat = c.categories.find((x) => x.key === categoryKey);
    if (!cat) return go({ view: 'home' }, false);
    setTitle(cat.title);
    showBack(true);
    $view.innerHTML = loadingHtml();

    const cards = cat.sections.map((s) => `
      <div class="card" data-sec="${esc(s.id)}">
        <div class="emoji">${/^\d{4}$/.test(s.title) ? '📅' : '📘'}</div>
        <div class="card-title">${esc(s.title)}</div>
        <div class="card-count">${s.papers.length} paper${s.papers.length !== 1 ? 's' : ''}</div>
        <button class="mini-zip" data-zip="${esc(s.id)}">📦 ZIP</button>
      </div>`).join('');

    $view.innerHTML = `
      <div class="section-head"><h2>${esc(cat.title)}</h2></div>
      <p class="page-sub">Tap a section to see papers — or grab the whole section as ZIP.</p>
      <div class="grid">${cards}</div>`;

    $view.querySelectorAll('.card[data-sec]').forEach((el) =>
      el.addEventListener('click', () => go({ view: 'section', sectionId: el.dataset.sec })));
    $view.querySelectorAll('.mini-zip').forEach((el) => {
      el.addEventListener('click', (ev) => {
        ev.stopPropagation();
        const s = cat.sections.find((x) => x.id === el.dataset.zip);
        confirmModal(`Download ${s.title} as ZIP?`, `${s.papers.length} PDFs will be downloaded and zipped.`, () =>
          startJob({ type: 'section', sectionId: s.id }));
      });
    });
  }

  // ------------------------------------------------------------ SECTION (papers)
  async function renderSection(sectionId) {
    const c = await ensureContent();
    let section = null, cat = null;
    for (const cc of c.categories) for (const s of cc.sections)
      if (s.id === sectionId) { section = s; cat = cc; }
    if (!section) return go({ view: 'home' }, false);

    setTitle(section.title);
    showBack(true);
    $view.innerHTML = loadingHtml();

    const sel = state.selections[sectionId] || new Set();

    const rows = section.papers.map((p) => `
      <div class="paper-row ${sel.has(p.id) ? 'checked' : ''}" data-pid="${esc(p.id)}">
        <input type="checkbox" class="cb" ${sel.has(p.id) ? 'checked' : ''}>
        <div class="p-main">
          <div class="p-name">${esc(p.name)}</div>
          <div class="p-meta">${esc(cat.title)} · ${esc(section.title)}${p.series ? ' · Set ' + esc(p.series) : ''}</div>
          <div class="p-actions">
            <button class="sm-btn sm-open" data-open="${esc(p.id)}">📖 Open PDF</button>
            <button class="sm-btn sm-dl" data-dl="${esc(p.id)}">⬇ Download</button>
          </div>
        </div>
      </div>`).join('');

    $view.innerHTML = `
      <div class="breadcrumb"><span class="crumb-link" data-nav="cat">Home</span> › ${esc(cat.title)}</div>
      <div class="section-head"><h2>${esc(section.title)}</h2>
        <span class="count">${section.papers.length} Papers</span></div>
      <button class="btn btn-dark" id="btn-zip-all" style="margin-bottom:12px">📦 DOWNLOAD ALL AS ZIP</button>
      <div class="toolbar-row">
        <button class="btn btn-ghost" id="btn-selall">Select All</button>
        <button class="btn btn-ghost" id="btn-desel">Clear</button>
      </div>
      <div id="paper-list">${rows}</div>
      <div style="height:70px"></div>`;

    $view.querySelector('.crumb-link[data-nav="cat"]')
      .addEventListener('click', () => go({ view: 'category', categoryKey: cat.key }));

    $view.querySelector('#btn-zip-all').addEventListener('click', () => {
      confirmModal(`Download ${section.title} as ZIP?`, `${section.papers.length} PDFs will be downloaded and zipped.`, () =>
        startJob({ type: 'section', sectionId }));
    });

    const paperById = new Map(section.papers.map((p) => [p.id, p]));
    const updateBar = () => {
      const n = (state.selections[sectionId] || new Set()).size;
      const el = document.getElementById('sel-count');
      if (el) el.textContent = n;
      const btn = document.getElementById('btn-zip-sel');
      if (btn) btn.disabled = n === 0;
    };

    $view.querySelector('#btn-selall').addEventListener('click', () => {
      state.selections[sectionId] = new Set(section.papers.map((p) => p.id));
      $view.querySelectorAll('.paper-row').forEach((r) => {
        r.classList.add('checked');
        r.querySelector('.cb').checked = true;
      });
      updateBar();
    });
    $view.querySelector('#btn-desel').addEventListener('click', () => {
      state.selections[sectionId] = new Set();
      $view.querySelectorAll('.paper-row').forEach((r) => {
        r.classList.remove('checked');
        r.querySelector('.cb').checked = false;
      });
      updateBar();
    });

    $view.querySelectorAll('.paper-row').forEach((row) => {
      row.addEventListener('click', (ev) => {
        if (ev.target.closest('button')) return;
        const cb = row.querySelector('.cb');
        cb.checked = !cb.checked;
        cb.dispatchEvent(new Event('change'));
      });
      row.querySelector('.cb').addEventListener('change', (ev) => {
        const pid = row.dataset.pid;
        if (!state.selections[sectionId]) state.selections[sectionId] = new Set();
        if (ev.target.checked) state.selections[sectionId].add(pid);
        else state.selections[sectionId].delete(pid);
        row.classList.toggle('checked', ev.target.checked);
        updateBar();
      });
    });

    $view.querySelectorAll('[data-open]').forEach((b) => b.addEventListener('click', () => {
      const p = paperById.get(b.dataset.open);
      if (p) openPdf(p);
    }));
    $view.querySelectorAll('[data-dl]').forEach((b) => b.addEventListener('click', () => {
      const p = paperById.get(b.dataset.dl);
      if (p) downloadPdf(p);
    }));

    mountActionbar(`
      <button class="btn btn-primary" id="btn-zip-sel" disabled>📦 Download Selected (<span id="sel-count">0</span>)</button>`);
    document.getElementById('btn-zip-sel').addEventListener('click', () => {
      const ids = [...(state.selections[sectionId] || new Set())];
      if (!ids.length) return toast('Select at least one paper');
      confirmModal('Download selected papers as ZIP?', `${ids.length} PDFs will be downloaded and zipped.`, () =>
        startJob({ type: 'selected', paperIds: ids }));
    });
    updateBar();
  }

  function removeActionbar() {
    const old = document.getElementById('actionbar');
    if (old) old.remove();
  }
  function mountActionbar(html) {
    removeActionbar();
    const bar = document.createElement('div');
    bar.id = 'actionbar';
    bar.innerHTML = html;
    document.body.appendChild(bar);
  }

  // ------------------------------------------------------------ PDF open/download
  function openPdf(p) {
    const u = `/api/pdf?url=${encodeURIComponent(p.url)}`;
    location.href = u; // Chrome's native PDF viewer; Android Back returns here
  }
  function downloadPdf(p) {
    const u = `/api/pdf?url=${encodeURIComponent(p.url)}&dl=1&name=${encodeURIComponent(p.name.slice(0, 90))}`;
    toast('Starting PDF download…');
    const a = document.createElement('a');
    a.href = u;
    a.download = '';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  // ------------------------------------------------------------ SEARCH
  async function renderSearch(q) {
    setTitle('Search');
    showBack(true);
    const c = await ensureContent();
    const needle = q.toLowerCase();
    const hits = [];
    for (const cat of c.categories)
      for (const s of cat.sections)
        for (const p of s.papers) {
          const hay = `${p.name} ${s.title} ${cat.title}`.toLowerCase();
          if (hay.includes(needle)) hits.push({ p, s, cat });
        }
    const rows = hits.slice(0, 120).map(({ p, s, cat }) => `
      <div class="paper-row">
        <div class="p-main">
          <div class="p-name">${esc(p.name)}</div>
          <div class="p-meta">${esc(cat.title)} · ${esc(s.title)}</div>
          <div class="p-actions">
            <button class="sm-btn sm-open" data-open="${esc(p.id)}">📖 Open</button>
            <button class="sm-btn sm-dl" data-dl="${esc(p.id)}">⬇ Download</button>
          </div>
        </div>
      </div>`).join('');

    $view.innerHTML = `
      <div class="breadcrumb">Results for “${esc(q)}” — ${hits.length} match${hits.length !== 1 ? 'es' : ''}${hits.length > 120 ? ' (showing 120)' : ''}</div>
      ${rows || '<div class="empty">No papers found.</div>'}`;

    const byId = new Map(hits.map((h) => [h.p.id, h.p]));
    $view.querySelectorAll('[data-open]').forEach((b) =>
      b.addEventListener('click', () => openPdf(byId.get(b.dataset.open))));
    $view.querySelectorAll('[data-dl]').forEach((b) =>
      b.addEventListener('click', () => downloadPdf(byId.get(b.dataset.dl))));
  }

  // ------------------------------------------------------------ JOBS
  async function startJob(payload) {
    try {
      const r = await api('/api/create-job', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      state.activeJobId = r.jobId;
      localStorage.setItem('chsl_active_job', r.jobId);
      go({ view: 'job', jobId: r.jobId });
    } catch (e) {
      toast(e.message, 4000);
    }
  }

  let jobTimer = null;

  async function renderJob(jobId) {
    setTitle('Download');
    showBack(false);
    if (jobTimer) { clearTimeout(jobTimer); jobTimer = null; }

    const draw = (job) => {
      const pct = job.total ? Math.round((job.done / job.total) * 100) : 0;
      const blocks = '█'.repeat(Math.round(pct / 10)) + '░'.repeat(10 - Math.round(pct / 10));

      let body = '';
      if (job.state === 'queued' || job.state === 'downloading') {
        body = `
          <div class="job-sub">Downloading papers…</div>
          <div class="job-num">${job.done} / ${job.total}</div>
          <div class="meter">${blocks} ${pct}%</div>
          <div class="pbar"><div style="width:${pct}%"></div></div>
          <div class="current-file">${job.current && job.current.length ? esc(job.current[0]) : ''}</div>
          <p class="hint">You can leave this screen — the server keeps downloading. Come back anytime.</p>
          <button class="btn btn-danger" id="btn-cancel" style="margin-top:14px">✕ Cancel download</button>`;
      } else if (job.state === 'zipping') {
        body = `
          <div class="job-sub">Creating ZIP…</div>
          <div class="job-num">🗜️ ${job.ok} PDFs</div>
          <div class="meter">██████████ 100%</div>
          <div class="pbar"><div style="width:100%"></div></div>`;
      } else if (job.state === 'done') {
        const failedHtml = job.failed.length ? `
          <div class="failed-box">
            <h4>Failed (${job.failed.length}):</h4>
            <ul>${job.failed.map((f) => `<li>${esc(f.name)} — ${esc(f.reason)}</li>`).join('')}</ul>
          </div>` : '';
        body = `
          <div class="job-title">✅ ZIP Ready</div>
          <div class="job-sub">${esc(job.zipName)} · ${fmtBytes(job.zipBytes)}</div>
          <div class="job-num"><span class="ok-badge">${job.ok}</span> / ${job.total} PDFs included</div>
          ${failedHtml}
          <div style="display:flex;flex-direction:column;gap:10px;margin-top:16px">
            <a class="btn btn-primary" id="btn-save" href="/api/job/${esc(job.id)}/zip" style="text-decoration:none">⬇ DOWNLOAD ZIP</a>
            ${job.failed.length ? `<button class="btn btn-ghost" id="btn-retry">↻ Retry Failed (${job.failed.length})</button>` : ''}
            <button class="btn btn-ghost" id="btn-home">← Home</button>
          </div>`;
      } else if (job.state === 'cancelled') {
        body = `
          <div class="job-title">✕ Cancelled</div>
          <div class="job-sub">Temporary files were cleaned up.</div>
          <button class="btn btn-ghost" id="btn-home" style="margin-top:12px">← Home</button>`;
      } else if (job.state === 'expired') {
        body = `
          <div class="job-title">⌛ ZIP expired</div>
          <div class="job-sub">Server ZIPs are deleted after a few hours. Start the download again.</div>
          <button class="btn btn-ghost" id="btn-home" style="margin-top:12px">← Home</button>`;
      } else {
        body = `
          <div class="job-title">⚠️ Failed</div>
          <div class="job-sub">${esc(job.error || 'Unknown error')}</div>
          <button class="btn btn-ghost" id="btn-home" style="margin-top:12px">← Home</button>`;
      }

      $view.innerHTML = `<div class="job-card">${body}</div>`;

      const onCancel = () => api(`/api/job/${job.id}/cancel`, { method: 'POST' }).catch(() => {});
      const onHome = () => go({ view: 'home' });
      const btnC = document.getElementById('btn-cancel');
      const btnH = document.getElementById('btn-home');
      const btnR = document.getElementById('btn-retry');
      if (btnC) btnC.addEventListener('click', onCancel);
      if (btnH) btnH.addEventListener('click', onHome);
      if (btnR) btnR.addEventListener('click', () => {
        const ids = job.failed.map((f) => f.id);
        startJob({ type: 'retry', paperIds: ids });
      });
      if (job.state === 'done') {
        state.activeJobId = null;
        localStorage.removeItem('chsl_active_job');
      }
    };

    const poll = async () => {
      let job = null;
      try { job = await api(`/api/job/${jobId}`); }
      catch (e) {
        $view.innerHTML = `<div class="job-card"><div class="job-title">⚠️ Job not found</div>
          <div class="job-sub">${esc(e.message)}</div>
          <button class="btn btn-ghost" id="btn-home" style="margin-top:12px">← Home</button></div>`;
        document.getElementById('btn-home').addEventListener('click', () => go({ view: 'home' }));
        return;
      }
      draw(job);
      if (['queued', 'downloading', 'zipping'].includes(job.state)) {
        jobTimer = setTimeout(poll, 1200);
      }
    };
    poll();
  }

  // ------------------------------------------------------------ modal
  function confirmModal(title, text, onYes) {
    const back = document.createElement('div');
    back.className = 'modal-back';
    back.innerHTML = `
      <div class="modal">
        <h3>${esc(title)}</h3>
        <p>${esc(text)}</p>
        <div class="row">
          <button class="btn btn-ghost" data-no>Cancel</button>
          <button class="btn btn-primary" data-yes>Start</button>
        </div>
      </div>`;
    document.body.appendChild(back);
    back.querySelector('[data-no]').addEventListener('click', () => back.remove());
    back.querySelector('[data-yes]').addEventListener('click', () => { back.remove(); onYes(); });
    back.addEventListener('click', (e) => { if (e.target === back) back.remove(); });
  }

  // ------------------------------------------------------------ boot
  render();
  // resume an in-flight job after page reload / re-entry
  if (state.activeJobId) {
    api(`/api/job/${state.activeJobId}`).then((j) => {
      if (['queued', 'downloading', 'zipping'].includes(j.state)) {
        go({ view: 'job', jobId: state.activeJobId });
      } else if (j.state === 'done') {
        state.activeJobId = null;
        localStorage.removeItem('chsl_active_job');
      }
    }).catch(() => {
      state.activeJobId = null;
      localStorage.removeItem('chsl_active_job');
    });
  }
})();
