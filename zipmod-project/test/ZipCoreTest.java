import com.zipmod.ZipCore;
import com.zipmod.ZipCore.Paper;

import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/** JVM unit tests for ZipCore against the app's REAL live data. */
public class ZipCoreTest {

    static int passed = 0, failed = 0;

    static void check(boolean cond, String name) {
        if (cond) { passed++; System.out.println("  [PASS] " + name); }
        else { failed++; System.out.println("  [FAIL] " + name); }
    }

    public static void main(String[] args) throws Exception {
        // ---------------- 1. parse real PYQ JSON (b_data.json, like the app receives)
        String bData = new String(java.nio.file.Files.readAllBytes(new File(args[0]).toPath()), "UTF-8");
        org.json.JSONObject root = new org.json.JSONObject(bData);
        org.json.JSONArray cats = root.getJSONArray("categories");
        org.json.JSONObject year2024 = null;
        for (int i = 0; i < cats.length(); i++) {
            if ("2024".equals(cats.getJSONObject(i).optString("name"))) year2024 = cats.getJSONObject(i);
        }
        check(year2024 != null, "b_data.json contains year 2024 category");
        // Replicate exactly what CategoriesAdapter$1 passes to ChaptersActivity:
        String papersJson = year2024.getJSONArray("data").toString();
        List<Paper> papers = ZipCore.parsePapers(papersJson);
        check(papers.size() > 0, "parsed papers for 2024: " + papers.size() + " items");
        boolean allPdf = true;
        for (Paper p : papers) if (!p.url.toLowerCase().contains("pdf_data")) allPdf = false;
        check(allPdf, "all parsed items are pdf_data items");
        check(papers.get(0).name.contains("CHSL"), "first paper name: " + papers.get(0).name);
        check(papers.get(0).series.length() > 0, "first paper series: " + papers.get(0).series);

        // ---------------- 2. filter + url-dedup behaviour
        String dupJson = "[{\"name\":\"A\",\"series\":\"A1\",\"extra\":\"https://x/y.pdf#pdf_data\"},"
                + "{\"name\":\"A dup\",\"series\":\"A2\",\"extra\":\"https://x/y.pdf#pdf_data\"},"
                + "{\"name\":\"H\",\"series\":\"A3\",\"extra\":\"https://x/h.html#html_data\"},"
                + "{\"name\":\"G\",\"series\":\"A4\",\"extra\":\"gamezop://x\"},"
                + "{\"name\":\"B\",\"series\":\"A5\",\"extra\":\"https://x/z.pdf#pdf_data\"}]";
        List<Paper> dup = ZipCore.parsePapers(dupJson);
        check(dup.size() == 2, "dedup: exact same URL counted once, html/gamezop filtered (got " + dup.size() + ")");
        String hiEn = "[{\"name\":\"Paper 1 Hindi\",\"series\":\"A1\",\"extra\":\"https://x/h.pdf#pdf_data\"},"
                + "{\"name\":\"Paper 1 English\",\"series\":\"A1\",\"extra\":\"https://x/e.pdf#pdf_data\"}]";
        List<Paper> he = ZipCore.parsePapers(hiEn);
        check(he.size() == 2, "separate Hindi/English URLs preserved");

        // ---------------- 3. filename generation
        Set<String> used = new HashSet<String>();
        String f1 = ZipCore.buildFileName("CHSL Tier-I (02 July 2024) Shift- 4", "A5", "2024", 0, 34, used);
        System.out.println("    -> " + f1);
        check(f1.equals("01_CHSL_Tier-I_(02_July_2024)_Shift-_4_A5.pdf"), "numbered filename from real paper name: " + f1);
        String f2 = ZipCore.buildFileName("CHSL Tier-I (02 July 2024) Shift- 4", "A5", "2024", 1, 34, used);
        check(f2.equals("02_CHSL_Tier-I_(02_July_2024)_Shift-_4_A5.pdf"), "index 2 gets different number: " + f2);
        String f2b = ZipCore.buildFileName("CHSL Tier-I (02 July 2024) Shift- 4", "A5", "2024", 1, 34, used);
        check(f2b.endsWith("_1.pdf"), "true duplicate (same index) gets _1: " + f2b);
        String f3 = ZipCore.buildFileName("Synonyms", "A12", "English", 0, 50, new HashSet<String>());
        System.out.println("    -> " + f3);
        check(f3.equals("01_English_Synonyms_A12.pdf"), "section prefixed when missing: " + f3);
        String f4 = ZipCore.buildFileName("GK Notes Hindi", "A9", "2024", 0, 30, new HashSet<String>());
        check(f4.contains("Hindi"), "language visible in filename: " + f4);
        String f5 = ZipCore.buildFileName("Tricky/Name:With*Bad?Chars<>|", "A1", "2024", 0, 30, new HashSet<String>());
        System.out.println("    -> " + f5);
        check(!f5.matches(".*[/\\\\:*?\"<>|].*"), "illegal filename chars sanitized: " + f5);
        String f6 = ZipCore.buildFileName(null, "", "2024", 3, 30, new HashSet<String>());
        check(f6.equals("04_2024_Paper_4.pdf"), "null name fallback: " + f6);

        // ---------------- 4. zip / folder naming
        check(ZipCore.zipNameFor("2024").equals("SSC_CHSL_2024_Papers.zip"), "zip name: " + ZipCore.zipNameFor("2024"));
        check(ZipCore.zipNameFor("2025").equals("SSC_CHSL_2025_Papers.zip"), "zip name 2025");
        check(ZipCore.relativeDirFor("2024").equals("SSC CHSL Papers/2024"), "rel dir: " + ZipCore.relativeDirFor("2024"));
        check(ZipCore.zipNameFor("Reasoning").equals("SSC_CHSL_Reasoning_Papers.zip"), "non-year section zip name");
        check(ZipCore.zipNameFor("2025", true).equals("SSC_CHSL_2025_Papers_Retry.zip"), "retry zip name: " + ZipCore.zipNameFor("2025", true));
        String fw = ZipCore.buildFileName("Big Batch Paper", "B1", "2025", 5, 120, new HashSet<String>());
        check(fw.startsWith("006_"), "3-digit numbering for 100+ papers: " + fw);
        check(ZipCore.paperJson(new ZipCore.Paper("N", "S", "U#pdf_data")).contains("\"extra\""), "paperJson roundtrip");

        // ---------------- 5. meter
        check(ZipCore.meter(12, 47).equals("███░░░░░░░ 26%"), "meter(12,47): " + ZipCore.meter(12, 47));

        // ---------------- 6. REAL live download of 2 PDFs via the exact code path
        File tmp = new File("ziptest_tmp");
        ZipCore.deleteRecursively(tmp);
        tmp.mkdirs();
        List<File> files = new ArrayList<File>();
        List<String> names = new ArrayList<String>();
        Set<String> used2 = new HashSet<String>();
        int n = Math.min(2, papers.size());
        for (int i = 0; i < n; i++) {
            File out = new File(tmp, "paper_" + i + ".pdf");
            ZipCore.fetchTo(papers.get(i).url, out);   // LIVE network call — same code as on device
            check(ZipCore.looksLikePdf(out), "live download #" + (i + 1) + " is a real PDF (" + out.length() + " bytes)");
            files.add(out);
            names.add(ZipCore.buildFileName(papers.get(i).name, papers.get(i).series, "2024", i, n, used2));
        }

        // ---------------- 7. build zip and verify
        File zip = new File(tmp, "SSC_CHSL_2024_Papers.zip");
        int written = ZipCore.buildZip(names, files, zip);
        check(written == n, "zip written with " + written + " entries");
        check(zip.length() > 1000, "zip file size: " + zip.length() + " bytes");
        ZipFile zf = new ZipFile(zip);
        boolean namesOk = true;
        for (int i = 0; i < names.size(); i++) {
            ZipEntry e = zf.getEntry(names.get(i));
            if (e == null) { namesOk = false; continue; }
            // compare content byte-for-byte
            FileInputStream in = new FileInputStream(files.get(i));
            java.io.InputStream zin = zf.getInputStream(e);
            boolean same = true;
            int a, b;
            do {
                a = in.read(); b = zin.read();
                if (a != b) { same = false; break; }
            } while (a != -1);
            in.close(); zin.close();
            if (!same) namesOk = false;
        }
        zf.close();
        check(namesOk, "zip entries match original files byte-for-byte");
        ZipCore.deleteRecursively(tmp);
        check(!tmp.exists(), "temp dir cleaned after zip");

        System.out.println();
        System.out.println("RESULT: " + passed + " passed, " + failed + " failed");
        if (failed > 0) System.exit(1);
    }
}
