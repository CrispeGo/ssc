package com.zipmod;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.RandomAccessFile;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.zip.Deflater;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import java.util.zip.ZipOutputStream;

/**
 * Pure (non-Android) core logic of the "Download Year as ZIP" feature.
 * Kept free of android.* imports so it can be unit-tested on a plain JVM.
 *
 * Data model replicated from the original app:
 *  - ChaptersActivity receives intent extras: "name" = JSON array of papers,
 *    "title" = section/year name.
 *  - Each paper object: { "name": title, "series": code, "extra": pdfUrl + "#pdf_data" }
 *  - Only entries whose "extra" contains "pdf_data" are real PDFs
 *    (other markers: "html_data" for HTML notes, "gamezop" for games).
 */
public final class ZipCore {

    private ZipCore() {}

    /** One downloadable PDF paper. */
    public static final class Paper {
        public final String name;    // display name, e.g. "CHSL Tier-I (02 July 2024) Shift- 4"
        public final String series;  // series code, e.g. "A5"
        public final String url;     // raw "extra" value (may end with #pdf_data)

        public Paper(String name, String series, String url) {
            this.name = name == null ? "" : name;
            this.series = series == null ? "" : series;
            this.url = url == null ? "" : url;
        }
    }

    /**
     * Parse the papers JSON exactly as the original ChaptersActivity receives it
     * (intent extra "name"). Keeps only genuine PDF items and de-duplicates
     * identical URLs (same file listed twice), while preserving genuinely
     * separate Hindi/English versions (they have different URLs).
     */
    public static List<Paper> parsePapers(String json) {
        List<Paper> out = new ArrayList<Paper>();
        if (json == null) return out;
        String s = json.trim();
        if (s.isEmpty()) return out;
        JSONArray arr;
        try {
            arr = new JSONArray(s);
        } catch (Exception e) {
            return out;
        }
        Map<String, Paper> byUrl = new LinkedHashMap<String, Paper>();
        for (int i = 0; i < arr.length(); i++) {
            JSONObject o;
            try {
                o = arr.getJSONObject(i);
            } catch (Exception e) {
                continue;
            }
            String name = opt(o, "name");
            String series = opt(o, "series");
            String extra = opt(o, "extra");
            if (extra == null || extra.length() == 0) continue;
            String low = extra.toLowerCase(Locale.ROOT);
            if (!low.contains("pdf_data")) continue;   // not a direct PDF item
            if (!low.startsWith("http://") && !low.startsWith("https://")) continue; // safety
            String bare = stripFragment(extra);
            if (bare.length() == 0) continue;
            if (!byUrl.containsKey(bare)) byUrl.put(bare, new Paper(name, series, extra));
        }
        out.addAll(byUrl.values());
        return out;
    }

    /** Rebuild a single paper as JSON (used for "retry failed" batches). */
    public static String paperJson(Paper p) {
        try {
            JSONObject o = new JSONObject();
            o.put("name", p.name);
            o.put("series", p.series);
            o.put("extra", p.url);
            return o.toString();
        } catch (Exception e) {
            return "{\"name\":\"Paper\",\"series\":\"\",\"extra\":\"\"}";
        }
    }

    private static String opt(JSONObject o, String key) {
        try {
            String v = o.optString(key, "");
            return v == null ? "" : v;
        } catch (Exception e) {
            return "";
        }
    }

    /** Remove "#pdf_data" style fragment from a URL (fragments are never sent to servers). */
    public static String stripFragment(String url) {
        if (url == null) return "";
        int h = url.indexOf('#');
        return h >= 0 ? url.substring(0, h) : url;
    }

    /** Sanitize arbitrary text into a filesystem-safe filename fragment. */
    public static String sanitize(String s) {
        if (s == null) return "";
        s = s.replace('\u2013', '-').replace('\u2014', '-').replace('\u2018', '\'')
             .replace('\u2019', '\'').replace('\u201C', '"').replace('\u201D', '"');
        StringBuilder sb = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isLetterOrDigit(c)) {
                sb.append(c);
            } else if (c == ' ' || c == '-' || c == '(' || c == ')' || c == '_' || c == '.' || c == ',') {
                sb.append(c);
            } else {
                sb.append('_');
            }
        }
        String r = sb.toString().trim();
        StringBuilder sp = new StringBuilder(r.length());
        boolean lastUnderscore = false;
        for (int i = 0; i < r.length(); i++) {
            char c = r.charAt(i);
            if (c == ' ') {
                if (!lastUnderscore) sp.append('_');
                lastUnderscore = true;
            } else if (c == '_') {
                if (!lastUnderscore) sp.append('_');
                lastUnderscore = true;
            } else {
                sp.append(c);
                lastUnderscore = false;
            }
        }
        r = sp.toString();
        while (r.startsWith("_")) r = r.substring(1);
        while (r.endsWith("_")) r = r.substring(0, r.length() - 1);
        return r;
    }

    /** Detect language marker from a paper name; null when not determinable. */
    public static String detectLanguage(String name) {
        if (name == null) return null;
        String low = name.toLowerCase(Locale.ROOT);
        boolean hi = low.contains("hindi");
        boolean en = low.contains("english");
        if (hi && !en) return "Hindi";
        if (en && !hi) return "English";
        return null;
    }

    /**
     * Build a readable, unique ZIP entry name for one paper.
     * Zero-padded index keeps files sorted in file managers:
     *   "01_CHSL_Tier-I_(02_July_2024)_Shift-_4_A5.pdf"
     * Duplicates get "_1", "_2", ... suffixes.
     *
     * @param total total number of papers in the batch (decides padding width)
     */
    public static String buildFileName(String paperName, String series, String section,
                                       int index, int total, Set<String> usedLower) {
        int width = total >= 100 ? 3 : 2;
        String prefix = String.format(Locale.US, "%0" + width + "d_", Integer.valueOf(index + 1));
        String base = sanitize(paperName);
        String sec = sanitize(section);
        if (base.isEmpty()) base = "Paper_" + (index + 1);
        if (!sec.isEmpty()
                && !base.toLowerCase(Locale.ROOT).contains(sec.toLowerCase(Locale.ROOT))) {
            base = sec + "_" + base;
        }
        String sr = sanitize(series);
        if (!sr.isEmpty() && !base.toLowerCase(Locale.ROOT).contains(sr.toLowerCase(Locale.ROOT))) {
            base = base + "_" + sr;
        }
        String lang = detectLanguage(paperName);
        if (lang != null && !base.toLowerCase(Locale.ROOT).contains(lang.toLowerCase(Locale.ROOT))) {
            base = base + "_" + lang;
        }
        if (base.length() > 90) base = base.substring(0, 90);
        String name = prefix + base + ".pdf";
        String candidate = name;
        int n = 1;
        while (usedLower.contains(candidate.toLowerCase(Locale.ROOT))) {
            candidate = prefix + base + "_" + n + ".pdf";
            n++;
        }
        usedLower.add(candidate.toLowerCase(Locale.ROOT));
        return candidate;
    }

    /** ZIP file name for a section: 2024 -> "SSC_CHSL_2024_Papers.zip". */
    public static String zipNameFor(String section) {
        return zipNameFor(section, false);
    }

    /** Retry batches (only previously-failed papers) get an "_Retry" suffix. */
    public static String zipNameFor(String section, boolean retry) {
        String s = sanitize(section);
        if (s.isEmpty()) s = "Papers";
        return "SSC_CHSL_" + s + "_Papers" + (retry ? "_Retry" : "") + ".zip";
    }

    /** Sub-directory inside the public Downloads folder. */
    public static String relativeDirFor(String section) {
        String s = sanitize(section);
        if (s.isEmpty()) s = "Papers";
        return "SSC CHSL Papers/" + s;
    }

    /** A file is a plausible PDF only if it starts with "%PDF-". */
    public static boolean looksLikePdf(File f) {
        if (f == null || !f.exists() || f.length() < 5) return false;
        RandomAccessFile raf = null;
        try {
            raf = new RandomAccessFile(f, "r");
            byte[] b = new byte[5];
            raf.readFully(b);
            return b[0] == '%' && b[1] == 'P' && b[2] == 'D' && b[3] == 'F' && b[4] == '-';
        } catch (Exception e) {
            return false;
        } finally {
            if (raf != null) try { raf.close(); } catch (IOException ignore) {}
        }
    }

    /**
     * Download url into dest with manual redirect handling and timeouts.
     * Throws on HTTP error / network error. Used identically on Android and JVM tests.
     */
    public static void fetchTo(String rawUrl, File dest) throws IOException {
        String u = stripFragment(rawUrl);
        HttpURLConnection conn = null;
        try {
            for (int redirect = 0; redirect < 5; redirect++) {
                URL url = new URL(u);
                conn = (HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(20000);
                conn.setReadTimeout(60000);
                conn.setInstanceFollowRedirects(false);
                conn.setRequestProperty("User-Agent",
                        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36");
                int code = conn.getResponseCode();
                if (code == HttpURLConnection.HTTP_MOVED_PERM
                        || code == HttpURLConnection.HTTP_MOVED_TEMP
                        || code == HttpURLConnection.HTTP_SEE_OTHER
                        || code == 307 || code == 308) {
                    String loc = conn.getHeaderField("Location");
                    conn.disconnect();
                    conn = null;
                    if (loc == null || loc.length() == 0) {
                        throw new IOException("Redirect without Location");
                    }
                    u = loc.startsWith("http") ? loc
                            : new URL(new URL(u), loc).toString(); // relative redirect
                    continue;
                }
                if (code != HttpURLConnection.HTTP_OK) {
                    throw new IOException("HTTP " + code);
                }
                File tmp = new File(dest.getParentFile(), dest.getName() + ".part");
                InputStream in = new BufferedInputStream(conn.getInputStream(), 65536);
                OutputStream out = new BufferedOutputStream(new FileOutputStream(tmp), 65536);
                try {
                    copy(in, out);
                } finally {
                    closeQuietly(in);
                    closeQuietly(out);
                }
                if (dest.exists()) dest.delete();
                if (!tmp.renameTo(dest)) {
                    // fallback if rename fails
                    copyStream(tmp, dest);
                    tmp.delete();
                }
                return;
            }
            throw new IOException("Too many redirects");
        } finally {
            if (conn != null) conn.disconnect();
        }
    }

    public static void copy(InputStream in, OutputStream out) throws IOException {
        byte[] buf = new byte[65536];
        int r;
        while ((r = in.read(buf)) > 0) out.write(buf, 0, r);
        out.flush();
    }

    private static void copyStream(File from, File to) throws IOException {
        InputStream in = new BufferedInputStream(new FileInputStream(from), 65536);
        OutputStream out = new BufferedOutputStream(new FileOutputStream(to), 65536);
        try {
            copy(in, out);
        } finally {
            closeQuietly(in);
            closeQuietly(out);
        }
    }

    public static void closeQuietly(java.io.Closeable c) {
        if (c != null) try { c.close(); } catch (IOException ignore) {}
    }

    /**
     * Create a ZIP archive containing the given files under the given entry names.
     * Streams with 64 KiB buffers — files are never fully loaded into RAM.
     * PDFs barely compress, so BEST_SPEED keeps ZIP creation fast.
     */
    public static int buildZip(List<String> entryNames, List<File> files, File out) throws IOException {
        int n = 0;
        ZipOutputStream zos = null;
        try {
            zos = new ZipOutputStream(new BufferedOutputStream(new FileOutputStream(out), 65536));
            zos.setLevel(Deflater.BEST_SPEED);
            byte[] buf = new byte[65536];
            for (int i = 0; i < files.size(); i++) {
                File f = files.get(i);
                zos.putNextEntry(new ZipEntry(entryNames.get(i)));
                InputStream in = new BufferedInputStream(new FileInputStream(f), 65536);
                try {
                    int r;
                    while ((r = in.read(buf)) > 0) zos.write(buf, 0, r);
                } finally {
                    closeQuietly(in);
                }
                zos.closeEntry();
                n++;
            }
        } finally {
            if (zos != null) try { zos.close(); } catch (IOException ignore) {}
        }
        // sanity check: archive must be readable and contain n entries
        ZipFile zf = null;
        try {
            zf = new ZipFile(out);
            if (zf.size() != n) throw new IOException("ZIP verification failed");
        } finally {
            if (zf != null) try { zf.close(); } catch (IOException ignore) {}
        }
        return n;
    }

    /** Recursively delete a file or directory; never throws. */
    public static void deleteRecursively(File f) {
        if (f == null || !f.exists()) return;
        File[] children = f.listFiles();
        if (children != null) {
            for (File c : children) deleteRecursively(c);
        }
        try { f.delete(); } catch (Exception ignore) {}
    }

    /** 10-block progress meter like "██████░░░░" plus percentage. */
    public static String meter(int done, int total) {
        int pct = total <= 0 ? 0 : (int) Math.round(done * 100.0 / total);
        int filled = (int) Math.round(pct / 10.0);
        if (filled > 10) filled = 10;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10; i++) sb.append(i < filled ? '█' : '░');
        sb.append(' ').append(pct).append('%');
        return sb.toString();
    }
}
