package com.zipmod;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Typeface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Entry point invoked (via a tiny smali patch) from ChaptersActivity's new
 * "Download All as ZIP" button. Reads nothing from the activity except the
 * intent extras "title" (section/year) and "name" (papers JSON) that the
 * original app already passes to ChaptersActivity — so the ZIP downloader
 * uses exactly the same PDF URLs as the existing viewer/downloader.
 */
public final class ZipHelper {

    /** Events forwarded by ZipService to the in-app progress dialog. */
    interface Listener {
        void onProgress(int done, int total, String currentPaper);
        void onZipPhase(int fileCount);
        void onComplete(int okCount, int failedCount, List<String> failedNames,
                        List<String> failedJsons, Uri zipUri, String location);
        void onError(String message);
        void onCancelled();
    }

    private static final Handler MAIN = new Handler(Looper.getMainLooper());
    /**
     * Strong reference on purpose: the listener updates the progress dialog.
     * It is cleared on every terminal event (complete/error/cancelled), so the
     * reference — and with it the dialog — never outlives the download.
     */
    private static Listener listener = null;
    static final AtomicBoolean running = new AtomicBoolean(false);

    private ZipHelper() {}

    /**
     * Called from ChaptersActivity.zipButtonClick(View) — shows a confirmation
     * dialog first ("Download all 2025 papers as ZIP?" / "47 PDFs").
     * @param act        the ChaptersActivity
     * @param section    intent extra "title" — year ("2024") or section ("Reasoning")
     * @param papersJson intent extra "name" — JSON array of papers
     */
    public static void startZip(final Activity act, final String section, final String papersJson) {
        if (act == null || act.isFinishing()) return;

        // Validate data first — never crash, whatever happens.
        List<ZipCore.Paper> papers;
        try {
            papers = ZipCore.parsePapers(papersJson);
        } catch (Throwable t) {
            papers = null;
        }
        if (papers == null || papers.isEmpty()) {
            toast(act, "No downloadable PDFs found in this section.");
            return;
        }

        // Confirmation dialog before starting the background job.
        try {
            new AlertDialog.Builder(act)
                    .setTitle("Download All as ZIP")
                    .setMessage("Download all " + (section == null || section.length() == 0
                            ? "papers" : section + " papers") + " as ZIP?\n\n"
                            + papers.size() + " PDFs will be downloaded.")
                    .setPositiveButton("Download", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface d, int w) {
                            startZipInternal(act, section, papersJson, false);
                        }
                    })
                    .setNegativeButton("Cancel", null)
                    .show();
        } catch (Throwable ignore) {}
    }

    /**
     * Starts (or restarts) the background ZIP download without a confirmation
     * dialog — used by the confirmation itself, by "Retry" buttons and by the
     * retry-failed batch. @param retry true when this batch only contains
     * previously-failed papers (ZIP gets an "_Retry" suffix).
     */
    static void startZipInternal(final Activity act, final String section,
                                 final String papersJson, final boolean retry) {
        if (act == null || act.isFinishing()) return;

        if (!hasNetwork(act)) {
            showNoNetwork(act, section, papersJson, retry);
            return;
        }

        // Android 13+: ask (once) for notification permission; feature works without it too.
        if (Build.VERSION.SDK_INT >= 33
                && act.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)
                        != PackageManager.PERMISSION_GRANTED) {
            try {
                act.requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, 48201);
            } catch (Throwable ignore) {}
        }

        // Android 6-9 need WRITE_EXTERNAL_STORAGE for the legacy public Downloads folder.
        if (Build.VERSION.SDK_INT < 29
                && act.checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                        != PackageManager.PERMISSION_GRANTED) {
            try {
                act.requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 48202);
            } catch (Throwable ignore) {}
            toast(act, "Grant storage permission, then tap \"Download All as ZIP\" again.");
            return;
        }

        if (running.get()) {
            toast(act, "A ZIP download is already in progress.");
            return;
        }

        List<ZipCore.Paper> papers;
        try {
            papers = ZipCore.parsePapers(papersJson);
        } catch (Throwable t) {
            papers = null;
        }
        if (papers == null || papers.isEmpty()) {
            toast(act, "No downloadable PDFs found in this section.");
            return;
        }

        showProgressDialog(act, section, papersJson, papers.size(), retry);
        running.set(true);

        Intent svc = new Intent(act, ZipService.class);
        svc.putExtra(ZipService.EXTRA_SECTION, section == null ? "" : section);
        svc.putExtra(ZipService.EXTRA_PAPERS_JSON, papersJson == null ? "" : papersJson);
        svc.putExtra(ZipService.EXTRA_IS_RETRY, retry);
        try {
            if (Build.VERSION.SDK_INT >= 26) act.startForegroundService(svc);
            else act.startService(svc);
        } catch (Throwable t) {
            running.set(false);
            showError(act, section, papersJson, retry,
                    "Could not start download: " + t.getMessage());
        }
    }

    /**
     * Additive improvement for the ORIGINAL individual PDF download: after the
     * app-private copy (which the built-in viewer keeps using) is complete,
     * also export a user-accessible copy to Downloads/SSC CHSL Papers/Individual
     * via MediaStore (Android 10+) or the legacy path when permitted.
     * Never throws, never blocks the caller.
     */
    public static void exportIndividualPdf(final Context ctx, final File file) {
        if (ctx == null || file == null) return;
        if (!file.exists() || file.length() < 1024) return;
        if (!ZipCore.looksLikePdf(file)) return;
        Thread t = new Thread(new Runnable() {
            public void run() {
                try {
                    String name = file.getName();
                    if (name == null || name.trim().length() == 0) name = "paper.pdf";
                    name = name.trim();
                    if (!name.toLowerCase(Locale.ROOT).endsWith(".pdf")) name = name + ".pdf";
                    Uri uri = ZipService.savePublicFile(ctx, file, name,
                            "SSC CHSL Papers/Individual", "application/pdf");
                    if (uri != null) {
                        toast(ctx, "Also saved to Downloads/SSC CHSL Papers/Individual/" + name);
                    }
                } catch (Throwable ignore) {}
            }
        }, "PdfExport");
        t.setDaemon(true);
        t.start();
    }

    // ------------------------------------------------------------------ UI

    private static void showNoNetwork(final Activity act, final String section,
                                      final String json, final boolean retry) {
        try {
            new AlertDialog.Builder(act)
                    .setTitle("No Internet")
                    .setMessage("Internet connection required to download papers.")
                    .setPositiveButton("Retry", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface d, int w) {
                            startZipInternal(act, section, json, retry);
                        }
                    })
                    .setNegativeButton("Cancel", null)
                    .show();
        } catch (Throwable ignore) {}
    }

    private static void showError(final Activity act, final String section, final String json,
                                  final boolean retry, String msg) {
        try {
            new AlertDialog.Builder(act)
                    .setTitle("Download Failed")
                    .setMessage(msg)
                    .setPositiveButton("Retry", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface d, int w) {
                            startZipInternal(act, section, json, retry);
                        }
                    })
                    .setNegativeButton("Close", null)
                    .show();
        } catch (Throwable ignore) {}
    }

    private static int dp(Activity a, int v) {
        return Math.round(v * a.getResources().getDisplayMetrics().density);
    }

    private static void showProgressDialog(final Activity act, final String section,
                                           final String papersJson, final int total,
                                           final boolean retry) {
        LinearLayout root = new LinearLayout(act);
        root.setOrientation(LinearLayout.VERTICAL);
        int pad = dp(act, 20);
        root.setPadding(pad, dp(act, 10), pad, dp(act, 4));

        final ProgressBar bar = new ProgressBar(act, null, android.R.attr.progressBarStyleHorizontal);
        bar.setMax(total);
        bar.setProgress(0);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        root.addView(bar, lp);

        final TextView status = new TextView(act);
        status.setPadding(0, dp(act, 10), 0, 0);
        status.setText("Downloading: Paper 0 of " + total);
        root.addView(status);

        final TextView meterView = new TextView(act);
        meterView.setTypeface(Typeface.MONOSPACE);
        meterView.setPadding(0, dp(act, 4), 0, 0);
        meterView.setText(ZipCore.meter(0, total));
        root.addView(meterView);

        final TextView current = new TextView(act);
        current.setPadding(0, dp(act, 6), 0, dp(act, 8));
        current.setSingleLine(true);
        current.setText("");
        root.addView(current);

        final Listener listenerImpl = new Listener() {
            @Override public void onProgress(int done, int total2, String name) {
                bar.setMax(total2);
                bar.setProgress(done);
                status.setText("Downloading: Paper " + done + " of " + total2);
                meterView.setText(ZipCore.meter(done, total2));
                if (name != null) current.setText(name);
            }
            @Override public void onZipPhase(int fileCount) {
                status.setText("Creating ZIP... (" + fileCount + " PDFs)");
                meterView.setText(ZipCore.meter(10, 10));
                current.setText("Compressing files");
            }
            @Override public void onComplete(int ok, int failed, List<String> failedNames,
                                             List<String> failedJsons, Uri uri, String location) {
                showCompleteDialog(act, section, papersJson, ok, failed, failedNames,
                        failedJsons, uri, location);
            }
            @Override public void onError(String message) {
                showError(act, section, papersJson, retry, message);
            }
            @Override public void onCancelled() {
                toast(act, "ZIP download cancelled.");
            }
        };
        listener = listenerImpl;

        try {
            new AlertDialog.Builder(act)
                    .setTitle("📦 " + (section == null || section.length() == 0
                            ? "Papers" : section) + (retry ? " (retry)" : ""))
                    .setView(root)
                    .setPositiveButton("Hide", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface d, int w) { d.dismiss(); }
                    })
                    .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface d, int w) {
                            ZipService.requestCancel();
                            d.dismiss();
                        }
                    })
                    .setOnCancelListener(new DialogInterface.OnCancelListener() {
                        public void onCancel(DialogInterface d) { /* dialog closed, download continues */ }
                    })
                    .show();
        } catch (Throwable ignore) {}
    }

    private static void showCompleteDialog(final Activity act, final String section,
                                           final String papersJson, int okCount, int failedCount,
                                           List<String> failedNames, List<String> failedJsons,
                                           final Uri uri, String location) {
        try {
            StringBuilder msg = new StringBuilder();
            msg.append(okCount).append(okCount == 1 ? " PDF" : " PDFs")
               .append(" successfully saved.");
            if (failedCount > 0) {
                msg.append("\n\n").append(failedCount).append(" download")
                   .append(failedCount == 1 ? "" : "s").append(" failed:");
                for (int i = 0; i < failedNames.size() && i < 30; i++) {
                    msg.append("\n• ").append(failedNames.get(i));
                }
                if (failedNames.size() > 30) msg.append("\n• …");
            }
            msg.append("\n\nSaved to:\n").append(location);

            ScrollView scroll = new ScrollView(act);
            TextView text = new TextView(act);
            int pad = dp(act, 20);
            text.setPadding(pad, dp(act, 10), pad, dp(act, 10));
            text.setText(msg);
            scroll.addView(text);

            AlertDialog.Builder b = new AlertDialog.Builder(act)
                    .setTitle(failedCount > 0 ? "📦 ZIP Saved — " + okCount + "/" + (okCount + failedCount)
                            : "📦 ZIP Saved")
                    .setView(scroll)
                    .setNegativeButton("Close", null);

            if (failedCount > 0 && failedJsons != null && !failedJsons.isEmpty()) {
                b.setPositiveButton("Retry Failed (" + failedCount + ")",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface d, int w) {
                                StringBuilder sb = new StringBuilder("[");
                                for (int i = 0; i < failedJsons.size(); i++) {
                                    if (i > 0) sb.append(',');
                                    sb.append(failedJsons.get(i));
                                }
                                sb.append(']');
                                startZipInternal(act, section, sb.toString(), true);
                            }
                        });
                b.setNeutralButton("Share ZIP", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface d, int w) { ZipService.shareZip(act, uri); }
                });
            } else {
                b.setPositiveButton("Share ZIP", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface d, int w) { ZipService.shareZip(act, uri); }
                });
                b.setNeutralButton("Open Downloads", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface d, int w) {
                        try {
                            act.startActivity(new Intent(
                                    android.app.DownloadManager.ACTION_VIEW_DOWNLOADS));
                        } catch (Throwable ignore) {}
                    }
                });
            }
            b.show();
        } catch (Throwable ignore) {}
    }

    static void toast(Context c, String s) {
        try {
            Toast.makeText(c, s, Toast.LENGTH_LONG).show();
        } catch (Throwable ignore) {}
    }

    // ------------------------------------------------- events from service

    static void dispatchProgress(final int done, final int total, final String name) {
        final Listener l = listener;
        if (l == null) return;
        MAIN.post(new Runnable() {
            public void run() {
                try { l.onProgress(done, total, name); } catch (Throwable ignore) {}
            }
        });
    }

    static void dispatchZipPhase(final int fileCount) {
        final Listener l = listener;
        if (l == null) return;
        MAIN.post(new Runnable() {
            public void run() {
                try { l.onZipPhase(fileCount); } catch (Throwable ignore) {}
            }
        });
    }

    static void dispatchComplete(final int ok, final int failed, final List<String> failedNames,
                                 final List<String> failedJsons, final Uri uri, final String location) {
        running.set(false);
        final Listener l = listener;
        listener = null;
        if (l == null) return;
        MAIN.post(new Runnable() {
            public void run() {
                try { l.onComplete(ok, failed, failedNames, failedJsons, uri, location); } catch (Throwable ignore) {}
            }
        });
    }

    static void dispatchError(final String message) {
        running.set(false);
        final Listener l = listener;
        listener = null;
        if (l == null) return;
        MAIN.post(new Runnable() {
            public void run() {
                try { l.onError(message); } catch (Throwable ignore) {}
            }
        });
    }

    static void dispatchCancelled() {
        running.set(false);
        final Listener l = listener;
        listener = null;
        if (l == null) return;
        MAIN.post(new Runnable() {
            public void run() {
                try { l.onCancelled(); } catch (Throwable ignore) {}
            }
        });
    }

    static boolean hasNetwork(Context c) {
        try {
            ConnectivityManager cm = (ConnectivityManager) c.getSystemService(Context.CONNECTIVITY_SERVICE);
            if (cm == null) return false;
            NetworkInfo ni = cm.getActiveNetworkInfo();
            return ni != null && ni.isConnected();
        } catch (Throwable t) {
            return false;
        }
    }
}
