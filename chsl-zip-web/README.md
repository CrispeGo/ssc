# SSC CHSL Previous Year Papers — ZIP Web App

A mobile-first web app that mirrors the **CHSL Previous Year Papers** Android app
(same content source, same navigation: **Home → Category → Year/Section → Papers → PDF**)
and adds a powerful download system on top:

- 📖 **Open PDF** — any paper in Chrome's native viewer (validated server-side)
- ⬇ **Download PDF** — single paper straight to your Downloads
- 📦 **Download All as ZIP** — any year/section (e.g. `SSC_CHSL_2024_Papers.zip`)
- ☑️ **Download Selected as ZIP** — checkbox selection
- 📦 **DOWNLOAD EVERYTHING** — one master ZIP (`SSC_CHSL_ALL_PAPERS.zip`) with
  `Category/Section/` folders, built from **all** PDF content on the source
- ↻ **Retry Failed** — only the papers that failed
- 🔍 **Search** across paper names, years, categories
- 🕘 **Recent Downloads**
- Real progress (`12 / 47`, `███░░░░░░░ 26%`) driven by the **actual backend state**
- Downloads keep running on the server if you switch apps / lock the screen

Everything is **100% dynamic** — new years (2026…), new categories, new papers appear
automatically as soon as the content source updates (5-minute cache).

---

## 1. Install

Requirements: **Node.js 18+**

```bash
cd chsl-zip-web
npm run setup        # installs backend deps (express, archiver, dotenv)
```

## 2. Configure (optional)

Defaults work out of the box. To change anything:

```bash
cp backend/.env.example backend/.env
# edit backend/.env
```

Key settings (all documented in `.env.example`):

| Variable | Default | Meaning |
|---|---|---|
| `PORT` | `3000` | listen port |
| `CONTENT_BASE` | `https://bollywoodnewstoday.com/appdata/com.tarun.sscchslpreviousyearpapers` | content source (verified from the APK) |
| `ALLOWED_HOSTS` | `bollywoodnewstoday.com,www.bollywoodnewstoday.com` | the ONLY hosts the backend will fetch PDFs from |
| `CONCURRENCY` | `5` | parallel downloads |
| `MAX_FILE_MB` | `150` | per-file size cap |
| `ZIP_TTL_MIN` | `180` | finished ZIPs auto-delete after this |

## 3. Run locally

```bash
npm start            # serves frontend + API on http://localhost:3000
```

Open `http://<your-machine-ip>:3000` in Chrome on your phone (same Wi-Fi).

## 4. Deploy

Any Node 18+ host works (single service serves both frontend and API):

- **Render / Railway / Fly.io**: create a Node service, root dir `backend/`
  (or repo root with `npm start`), start command `npm start`, expose the port.
- **VPS (Ubuntu)**:
  ```bash
  git clone <your-repo> && cd chsl-zip-web && npm run setup
  sudo apt install -y nginx certbot python3-certbot-nginx
  # proxy your domain -> 127.0.0.1:3000, then:
  npm start            # or use pm2: pm2 start backend/src/server.js --name chsl
  ```
- HTTPS is recommended (the PDF proxy is same-origin, so no CORS issues either way).

## 5. Change the data source

The content architecture was extracted from the original APK:

```
Home3 → BoxActivity → ChaptersActivity → PdfViewerActivity
GET {CONTENT_BASE}{jsonPath}          # categories[] → {name, data[]}
data[] item: {name, series, extra}    # extra = "<pdf-url>#pdf_data"
```

The six category→JSON mappings live in `backend/src/content.js` (`CATEGORY_DEFS`).
If the app's server moves or adds categories:

1. Update `CONTENT_BASE` and `ALLOWED_HOSTS` in `backend/.env`
2. If the JSON set changes, edit `CATEGORY_DEFS` the same way

No other code changes needed — years, sections and papers are discovered dynamically.

---

## Security design (not an open proxy)

- Only `https` + **whitelisted hosts** + `/appdata/` path prefix
- Redirects followed manually, **every hop re-validated**
- `text/html` responses rejected; **magic bytes must be `%PDF-`**
- Streaming with per-file timeout and size cap — nothing large sits in RAM
- Job rate-limiting + max running jobs + max files per job
- Finished ZIPs auto-delete (default 3 h) — server storage stays clean

## Project layout

```
chsl-zip-web/
├── package.json          # root scripts (setup/start)
├── README.md
├── frontend/             # no build step — plain HTML/CSS/JS
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── backend/
    ├── package.json
    ├── .env.example
    └── src/
        ├── server.js     # Express app + API routes
        ├── config.js     # env-driven configuration
        ├── content.js    # dynamic content discovery (mirrors the APK)
        ├── downloader.js # hardened PDF fetch/proxy
        ├── jobs.js       # background ZIP jobs (concurrency, retry, cancel)
        └── util.js       # filename sanitisation / naming rules
```

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/content` | full dynamic content tree (categories → sections → papers) |
| GET | `/api/pdf?url=…&dl=0\|1&name=…` | validated single-PDF proxy (view / download) |
| POST | `/api/create-job` | `{type:"section",sectionId}` · `{type:"selected",paperIds[]}` · `{type:"retry",paperIds[]}` · `{type:"all"}` |
| GET | `/api/job/:id` | real-time job status/progress |
| POST | `/api/job/:id/cancel` | cancel a running job |
| GET | `/api/job/:id/zip` | download the finished ZIP |
| GET | `/api/jobs/recent` | recent finished ZIPs |

---

*This is an independent web tool for personal study use. It is not affiliated with
the original app's developer, SSC, or any government body. All content is served
by the original app's own public content server.*
