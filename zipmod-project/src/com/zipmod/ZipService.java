package com.zipmod;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.ClipData;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.media.MediaScannerConnection;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.os.IBinder;
import android.os.PowerManager;
import android.provider.MediaStore;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Foreground service that downloads every PDF of a section/year, packs the
 * successful ones into "SSC_CHSL_<section>_Papers.zip" and saves it to the
 * public Downloads folder (MediaStore on Android 10+, legacy path below).
 * Failed files are reported; they never abort the batch.
 *
 * Runs only for the duration of the active download/ZIP task and stops itself
 * afterwards — no permanent background service. A bounded partial wake lock is
 * held only while the worker is actively transferring/zipping so that screen
 * lock / realme UI battery management do not interrupt mid-download.
 */
public class ZipService extends Service {

    public static final String EXTRA_SECTION = "zip_section";
    public static final String EXTRA_PAPERS_JSON = "zip_papers_json";
    public static final String EXTRA_IS_RETRY = "zip_is_retry";
    private static final String ACTION_CANCEL = "com.zipmod.CANCEL";
    private static final String CHANNEL_ID = "chsl_zip_download";
    private static final int NOTIF_ID = 48213;

    private static volatile ZipService instance;
    private volatile boolean cancelled = false;
    private volatile String sectionForNotif = "";
    private Thread worker;

    @Override
    public IBinder onBind(Intent intent) { return null; }

    @Override
    public void onCreate() {
        super.onCreate();
        instance = this;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && ACTION_CANCEL.equals(intent.getAction())) {
            cancelled = true;
            return START_NOT_STICKY;
        }
        createChannel();
        startFg(buildProgressNotification("Preparing download…", 0, 0, true));

        final String section = intent == null ? "" : safe(intent.getStringExtra(EXTRA_SECTION));
        final String json = intent == null ? "" : safe(intent.getStringExtra(EXTRA_PAPERS_JSON));
        final boolean retry = intent != null && intent.getBooleanExtra(EXTRA_IS_RETRY, false);
        final List<ZipCore.Paper> papers = ZipCore.parsePapers(json);

        if (papers.isEmpty()) {
            ZipHelper.dispatchError("No downloadable PDFs found in this section.");
            notifyFinal(buildErrorNotification("No downloadable PDFs found in this section."));
            finish();
            return START_NOT_STICKY;
        }

        worker = new Thread(new Runnable() {
            public void run() { doWork(section, papers, retry); }
        }, "ZipDownloadWorker");
        worker.start();
        return START_NOT_STICKY;
    }

    @Override
    public void onDestroy() {
        instance = null;
        super.onDestroy();
    }

    /** Android 15: dataSync foreground services time out after 6 hours — stop gracefully. */
    @Override
    public void onTimeout(int startId) {
        cancelled = true;
    }

    static void requestCancel() {
        ZipService s = instance;
        if (s != null) s.cancelled = true;
    }

    // ------------------------------------------------------------------ work

    private void doWork(String section, List<ZipCore.Paper> papers, boolean retry) {
        sectionForNotif = section == null ? "" : section;
        int total = papers.size();

        // Bounded partial wake lock: held only while work is actually running,
        // released in finally — the service stops right after the task ends.
        PowerManager.WakeLock wl = null;
        try {
            try {
                PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
                if (pm != null) {
                    wl = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "CHSLZip:download");
                    wl.acquire(6 * 60 * 60 * 1000L); // hard cap: 6 hours
                }
            } catch (Throwable ignore) {}

            File tempDir = new File(getCacheDir(), "zip_dl_tmp");
            ZipCore.deleteRecursively(tempDir);
            //noinspection ResultOfMethodCallIgnored
            tempDir.mkdirs();

            List<File> okFiles = new ArrayList<File>();
            List<String> okNames = new ArrayList<String>();
            List<String> failedNames = new ArrayList<String>();
            List<String> failedJsons = new ArrayList<String>();
            Set<String> used = new HashSet<String>();

            for (int i = 0; i < papers.size(); i++) {
                if (cancelled) break;
                ZipCore.Paper p = papers.get(i);
                postProgress(i, total, p.name);

                File out = new File(tempDir, "paper_" + i + ".pdf");
                boolean ok = false;
                IOException last = null;
                for (int attempt = 1; attempt <= 2 && !ok && !cancelled; attempt++) {
                    try {
                        ZipCore.fetchTo(p.url, out);
                        ok = true;
                    } catch (IOException e) {
                        last = e;
                    }
                }
                if (ok && ZipCore.looksLikePdf(out)) {
                    String fname = ZipCore.buildFileName(p.name, p.series, section, i, total, used);
                    okFiles.add(out);
                    okNames.add(fname);
                } else {
                    if (out.exists()) out.delete();
                    String display = p.name == null || p.name.trim().length() == 0
                            ? ("Paper " + (i + 1)) : p.name.trim();
                    failedNames.add(display + (ok ? " (invalid file)" : " (" + errText(last) + ")"));
                    failedJsons.add(ZipCore.paperJson(p));
                }
            }

            if (cancelled) {
                ZipCore.deleteRecursively(tempDir);
                notifyFinal(buildErrorNotification("Download cancelled."));
                ZipHelper.dispatchCancelled();
                finish();
                return;
            }

            if (okFiles.isEmpty()) {
                ZipCore.deleteRecursively(tempDir);
                String msg = "All " + total + " downloads failed. Check your internet connection and try again.";
                notifyFinal(buildErrorNotification(msg));
                ZipHelper.dispatchError(msg);
                finish();
                return;
            }

            postProgress(total, total, null);
            ZipHelper.dispatchZipPhase(okFiles.size());
            updateNotification("Creating ZIP… (" + okFiles.size() + " PDFs)");

            String zipName = ZipCore.zipNameFor(section, retry);
            File zipFile = new File(tempDir, zipName);
            ZipCore.buildZip(okNames, okFiles, zipFile);

            SavedZip saved = saveToDownloads(zipFile, zipName, ZipCore.relativeDirFor(section));

            // Temp files are no longer needed; the user's own saved PDFs are never touched.
            ZipCore.deleteRecursively(tempDir);

            int failed = failedNames.size();
            String summary = "ZIP Ready — " + okFiles.size() + "/" + total + " PDFs"
                    + (failed > 0 ? " (" + failed + " failed)" : ".");
            notifyFinal(buildDoneNotification(summary, saved.location, saved.uri));
            ZipHelper.dispatchComplete(okFiles.size(), failed, failedNames, failedJsons,
                    saved.uri, saved.location);
        } catch (Throwable t) {
            File tempDir = new File(getCacheDir(), "zip_dl_tmp");
            ZipCore.deleteRecursively(tempDir);
            String msg = "ZIP creation failed: " + safe(t.getMessage());
            notifyFinal(buildErrorNotification(msg));
            ZipHelper.dispatchError(msg);
            finish();
            return;
        } finally {
            if (wl != null && wl.isHeld()) {
                try { wl.release(); } catch (Throwable ignore) {}
            }
        }
        finish();
    }

    private static String errText(IOException e) {
        if (e == null) return "download failed";
        String m = e.getMessage();
        return m == null || m.length() == 0 ? e.getClass().getSimpleName() : m;
    }

    private static final class SavedZip {
        final Uri uri;
        final String location;
        SavedZip(Uri uri, String location) { this.uri = uri; this.location = location; }
    }

    // -------------------------------------------------------------- storage

    private SavedZip saveToDownloads(File zipFile, String zipName, String relDir) throws IOException {
        Uri uri = savePublicFile(this, zipFile, zipName, relDir, "application/zip");
        return new SavedZip(uri, "Downloads/" + relDir + "/" + zipName);
    }

    /**
     * Saves a file into the public Downloads folder.
     * Android 10+: MediaStore Downloads collection (scoped storage, no permission).
     * Android 6-9: legacy public directory (caller must hold WRITE_EXTERNAL_STORAGE).
     * Static so ZipHelper.exportIndividualPdf can reuse it for single PDFs.
     */
    public static Uri savePublicFile(Context ctx, File src, String displayName,
                                     String relDir, String mime) throws IOException {
        if (Build.VERSION.SDK_INT >= 29) {
            ContentValues cv = new ContentValues();
            cv.put(MediaStore.MediaColumns.DISPLAY_NAME, displayName);
            cv.put(MediaStore.MediaColumns.MIME_TYPE, mime);
            cv.put(MediaStore.MediaColumns.RELATIVE_PATH,
                    Environment.DIRECTORY_DOWNLOADS + "/" + relDir);
            cv.put(MediaStore.MediaColumns.IS_PENDING, 1);
            Uri uri = ctx.getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, cv);
            if (uri == null) throw new IOException("Could not create file in Downloads");
            try {
                OutputStream out = ctx.getContentResolver().openOutputStream(uri);
                if (out == null) throw new IOException("Could not open output stream");
                InputStream in = new FileInputStream(src);
                try {
                    ZipCore.copy(in, out);
                } finally {
                    ZipCore.closeQuietly(in);
                    ZipCore.closeQuietly(out);
                }
                ContentValues done = new ContentValues();
                done.put(MediaStore.MediaColumns.IS_PENDING, 0);
                ctx.getContentResolver().update(uri, done, null, null);
            } catch (Exception e) {
                try { ctx.getContentResolver().delete(uri, null, null); } catch (Exception ignore) {}
                throw new IOException(safe(e.getMessage()), e);
            }
            return uri;
        } else {
            File base = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            File dir = new File(base, relDir);
            if (!dir.exists() && !dir.mkdirs()) throw new IOException("Could not create " + dir);
            File dest = new File(dir, displayName);
            int n = 1;
            String baseName = displayName.endsWith(".zip") || displayName.endsWith(".pdf")
                    ? displayName.substring(0, displayName.length() - 4) : displayName;
            String ext = displayName.endsWith(".zip") || displayName.endsWith(".pdf")
                    ? displayName.substring(displayName.length() - 4) : "";
            while (dest.exists()) {
                dest = new File(dir, baseName + "_" + n + ext);
                n++;
            }
            InputStream in = new FileInputStream(src);
            OutputStream out = new FileOutputStream(dest);
            try {
                ZipCore.copy(in, out);
            } finally {
                ZipCore.closeQuietly(in);
                ZipCore.closeQuietly(out);
            }
            try {
                MediaScannerConnection.scanFile(ctx, new String[]{dest.getAbsolutePath()},
                        new String[]{mime}, null);
            } catch (Throwable ignore) {}
            return Uri.fromFile(dest);
        }
    }

    static void shareZip(Context ctx, Uri uri) {
        if (ctx == null || uri == null) return;
        try {
            Intent share = new Intent(Intent.ACTION_SEND);
            share.setType("application/zip");
            share.putExtra(Intent.EXTRA_STREAM, uri);
            share.setClipData(ClipData.newRawUri("zip", uri));
            share.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            Intent chooser = Intent.createChooser(share, "Share ZIP");
            chooser.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            if (Build.VERSION.SDK_INT >= 29) {
                // grant to all targets of the chooser
                chooser.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            }
            ctx.startActivity(chooser);
        } catch (Throwable ignore) {}
    }

    // --------------------------------------------------------- notifications

    private void createChannel() {
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            if (nm == null) return;
            NotificationChannel ch = new NotificationChannel(CHANNEL_ID,
                    "ZIP Downloads", NotificationManager.IMPORTANCE_LOW);
            ch.setDescription("Progress of year ZIP downloads");
            nm.createNotificationChannel(ch);
        }
    }

    private void startFg(Notification n) {
        try {
            if (Build.VERSION.SDK_INT >= 29) {
                startForeground(NOTIF_ID, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC);
            } else {
                startForeground(NOTIF_ID, n);
            }
        } catch (Throwable t) {
            try { startForeground(NOTIF_ID, n); } catch (Throwable ignore) {}
        }
    }

    private Notification.Builder base() {
        if (Build.VERSION.SDK_INT >= 26) return new Notification.Builder(this, CHANNEL_ID);
        return new Notification.Builder(this);
    }

    private PendingIntent piCancel() {
        Intent i = new Intent(this, ZipService.class);
        i.setAction(ACTION_CANCEL);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getService(this, 3, i, flags);
    }

    /** Notification tap opens the app (launcher intent) — no background activity tricks. */
    private PendingIntent piLaunchApp() {
        try {
            Intent i = getPackageManager().getLaunchIntentForPackage(getPackageName());
            if (i == null) i = new Intent();
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
            return PendingIntent.getActivity(this, 6, i, flags);
        } catch (Throwable t) {
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
            return PendingIntent.getActivity(this, 6, new Intent(), flags);
        }
    }

    private PendingIntent piOpenDownloads() {
        Intent i = new Intent(android.app.DownloadManager.ACTION_VIEW_DOWNLOADS);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getActivity(this, 4, i, flags);
    }

    private PendingIntent piShare(Uri uri) {
        Intent share = new Intent(Intent.ACTION_SEND);
        share.setType("application/zip");
        share.putExtra(Intent.EXTRA_STREAM, uri);
        share.setClipData(ClipData.newRawUri("zip", uri));
        share.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        Intent chooser = Intent.createChooser(share, "Share ZIP");
        chooser.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getActivity(this, 5, chooser, flags);
    }

    /** "Downloading CHSL 2025" / "18 / 47 papers" + progress bar + Cancel. */
    private Notification buildProgressNotification(String text, int done, int total,
                                                   boolean indeterminate) {
        Notification.Builder b = base();
        String sec = sectionForNotif == null || sectionForNotif.length() == 0
                ? "Papers" : sectionForNotif;
        int pct = total <= 0 ? 0 : (int) Math.round(done * 100.0 / total);
        b.setContentTitle("Downloading CHSL " + sec);
        if (indeterminate) {
            b.setContentText(text);
        } else {
            b.setContentText(done + " / " + total + " papers (" + pct + "%)");
        }
        b.setSmallIcon(android.R.drawable.stat_sys_download);
        b.setOngoing(true);
        b.setOnlyAlertOnce(true);
        b.setProgress(total, done, indeterminate);
        b.setContentIntent(piLaunchApp());
        b.addAction(0, "Cancel download", piCancel());
        return b.build();
    }

    /** "✅ ZIP Ready — 43/47 PDFs" + file name and location + Share/Open actions. */
    private Notification buildDoneNotification(String summary, String location, Uri uri) {
        Notification.Builder b = base();
        b.setContentTitle("✅ " + summary);
        b.setContentText(location);
        b.setStyle(new Notification.BigTextStyle().bigText(summary + "\n" + location));
        b.setSmallIcon(android.R.drawable.stat_sys_download_done);
        b.setAutoCancel(true);
        b.setContentIntent(piLaunchApp());
        if (uri != null) b.addAction(0, "Share ZIP", piShare(uri));
        b.addAction(0, "Open Downloads", piOpenDownloads());
        return b.build();
    }

    private Notification buildErrorNotification(String text) {
        Notification.Builder b = base();
        b.setContentTitle("ZIP download failed");
        b.setContentText(text);
        b.setStyle(new Notification.BigTextStyle().bigText(text));
        b.setSmallIcon(android.R.drawable.stat_notify_error);
        b.setAutoCancel(true);
        b.setContentIntent(piLaunchApp());
        return b.build();
    }

    private void postProgress(int done, int total, String current) {
        ZipHelper.dispatchProgress(done, total, current);
        Notification n = buildProgressNotification(null, total, done, false);
        notifyProgress(n);
    }

    private void updateNotification(String text) {
        Notification n = buildProgressNotification(text, 0, 0, true);
        notifyProgress(n);
    }

    private void notifyProgress(Notification n) {
        try {
            NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            if (nm != null) nm.notify(NOTIF_ID, n);
        } catch (Throwable ignore) {}
    }

    private void notifyFinal(Notification n) {
        try {
            NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            if (nm != null) nm.notify(NOTIF_ID + 1, n);
            nmIdCancel();
        } catch (Throwable ignore) {}
    }

    private void nmIdCancel() {
        try {
            NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            if (nm != null) nm.cancel(NOTIF_ID);
        } catch (Throwable ignore) {}
    }

    private void finish() {
        try { stopForeground(true); } catch (Throwable ignore) {}
        stopSelf();
    }

    private static String safe(String s) { return s == null ? "" : s; }
}
