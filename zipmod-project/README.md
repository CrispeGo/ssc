# CHSL Previous Year Papers — ZIP Mod (v2: Install-Fixed + Standalone Build)

## 📦 Final deliverables

| File | Package | Kya hai |
|---|---|---|
| **`CHSL_Previous_Year_Papers_ZIP_Standalone.apk`** ⭐ | `com.tarun.sscchslpreviousyearpapers.zipmod` | **RECOMMENDED** — original ke saath co-exist karti hai, uninstall ki zarurat NAHI |
| `CHSL_Previous_Year_Papers_ZIP_Mod.apk` | `com.tarun.sscchslpreviousyearpapers` (same as original) | Replacement build — pehle original uninstall karo |
| `CHSL_Previous_Year_Papers_ZIP_Standalone_Debug.apk` | same as Standalone | Debug-signed variant (optional) |

Teeno release/debug signed: **v1+v2+v3 schemes**, zipaligned (4-byte), installable.

---

## 1. 🔧 INSTALLATION FIX — root cause kya tha

Pichhli APK install kyun nahi hui, uska **confirmed** diagnosis (evidence-based, `aapt dump xmltree` se):

### Root cause #1 (primary) — `isSplitRequired`
Original APK Play Store se device se extract ki gayi thi (manifest me
`com.android.vending.derived.apk.id` meta-data + **Google Play App Signing** certificate).
Uske manifest me tha:

```
android:requiredSplitTypes="base__abi,base__density"
```

Rebuild ke time aapt2 ne isse **`android:isSplitRequired=true`** bana diya
(shipped APK me verify kiya gaya tha). **Is attribute wali APK standalone install
HI nahi ho sakti** — Android usse split-APK bundle maan kar reject karta hai
(`INSTALL_FAILED_MISSING_SPLIT` / "App not installed").

**Fix:** manifest se `requiredSplitTypes` + `splitTypes` + `derived.apk.id`
remove kiya. Ab dono builds me ye attributes **zero** hain (verified) →
standalone installable.

### Root cause #2 — signature mismatch (Build A only)
Original Play app installed hai; uska signing key developer ke paas hai.
Modified APK usse **update ke roop me install nahi ho sakti** — Android ka rule.
Isliye Build A ke liye original uninstall karna padta hai, ya **Build B use karo**
(alag package → parallel install, koi uninstall nahi).

### Root cause #3 (user-side, APK me fix nahi hota)
- realme UI: "Install unknown apps" permission us app ko do jisse APK khol rahe ho (File Manager/Chrome)
- Play Protect scan prompt aaye to "More details" → "Install anyway"

### Sab kuch check kiya gaya (dono builds me)
✅ Signature (v1+v2+v3 verify) • ✅ zipalign • ✅ minSdk 23 / targetSdk 35 (Android 13 compatible)
✅ versionCode 11 / versionName 10.0.1-zipmod • ✅ manifest valid • ✅ koi split requirement nahi
✅ 5 DEX files, d8-generated min-api 23 • ✅ providers ki authorities unique (Build B me renamed)
✅ custom permission renamed (Build B) — original ke saath duplicate permission conflict nahi

## 2. Build B — Standalone package rename (kya-kya badla)

Package: `com.tarun.sscchslpreviousyearpapers` → `com.tarun.sscchslpreviousyearpapers.zipmod`

Sirf manifest package nahi badla — properly update kiya:
- **manifest `package`** (applicationId)
- **custom permission** define + uses: `…zipmod.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`
  (WorkManager runtime par `getPackageName()+…` se yahi compute karta hai — match confirmed)
- **provider authorities**: `…zipmod.mobileadsinitprovider`, `…zipmod.androidx-startup`
- **launcher label**: "CHSL Papers ZIP Mod" (original se alag dikhne ke liye)
- **Jo jaan-boojh ke NAHI badla**: `R.string.Package_name` = `com.tarun.sscchslpreviousyearpapers`
  — yehi content server URL banata hai (`bollywoodnewstoday.com/appdata/<package>/b_data.json`),
  isliye standalone app bilkul wahi content load karta hai. Activity/service FQCNs bhi same
  (smali classes apni puruni jagah par hain — R classes included, IDs unchanged).
- Verified safe: app code me koi `getIdentifier`, koi FileProvider authority string,
  koi raw package const-string nahi (sirf "Rate us" Play-link `getPackageName()` use hota hai —
  benign, original ki listing khulti hai)

## 3. Year-ZIP feature (target: realme Narzo 30 5G, Android 13 / realme UI 4.0)

**Flow:** Year select → 📦 Download All as ZIP → confirmation ("Download all 2025 papers as ZIP?" / "47 PDFs") → [Download] → background foreground-service:

- **Normal notification:** "Downloading CHSL 2025" / "18 / 47 papers (38%)" + progress bar + **Cancel download** action; tap → app khulti hai
- **Screen lock/background me continue** — foreground service + bounded partial wake lock (sirf active download ke दौरान, 6h cap, end par release)
- Har PDF: 2 attempts, 20s connect / 60s read timeout, redirect handling, `%PDF` header validation
- Ek fail ho to batch continue → **"✅ ZIP Ready — 43/47 PDFs"** + failed list + **Retry Failed (4)** button → sirf failed papers dobara → `SSC_CHSL_2025_Papers_Retry.zip`
- **Save:** `Downloads/SSC CHSL Papers/2025/SSC_CHSL_2025_Papers.zip` — Android 10+ MediaStore (koi permission nahi), 6–9 legacy path
- **Filenames:** `01_CHSL_Tier-I_(02_July_2024)_Shift-_4_A5.pdf` — numbered (sorted), title+date+shift+series+language se, sanitized, dedup `_1`
- **RAM-friendly:** pure streaming (64 KiB buffers), Kabhi poora PDF RAM me nahi
- **Temp cleanup** ZIP ke baad/hogi fail par; user ki saved PDFs untouched
- **Dynamic:** years 2019–2025 + future + non-year sections (Reasoning etc.) — sab content JSON se automatic
- Hindi/English alag PDFs preserve; naam me language already ho to duplicate tag nahi

**Individual PDF download bhi improve** (additive): built-in viewer ka app-private download
jaise ka waisa (cache logic untouched), lekin complete hone par ek copy
`Downloads/SSC CHSL Papers/Individual/` me bhi export hoti hai (toast se bataya jata hai).

## 4. Verification — honest report

### ✅ Verified (is environment me, evidence ke saath)
1. **28/28 JVM unit tests** — real server data: 2024 ke 34 papers parse, 2 live PDF downloads
   exact device code-path se, real ZIP byte-for-byte verify, retry naming, 3-digit numbering
2. **Signature:** apksigner verify pass (v1+v2+v3) — teeno APKs
3. **zipalign:** pass
4. **aapt badging + xmltree:** package/version/label/permissions/authorities sab sahi;
   `isSplitRequired`/`requiredSplitTypes` = 0 (yehi pichhli baar install rok raha tha)
5. **Round-trip decode** dono builds: button, `onZipButtonClick`, `startZip` descriptor-exact match,
   `exportIndividualPdf` hook, ZipService+3 permissions manifest me, 24 nayi classes (classes5.dex)
6. **Preservation:** original vs shipped Build A — poore smali tree me sirf 2 app files
   me intended additions (ChaptersActivity +1 method, PdfViewerActivity$2 +1 hook);
   baaki ~25 library files me sirf benign round-trip diffs (field initializers/line numbers,
   zero semantic change)

### ❌ Physically test NAHI hua
- Is sandbox me Android device/emulator nahi hai — **fresh install, launch, button tap,
  notification, MediaStore save, screen-lock continuation kuch bhi device pe run nahi kiya gaya.**
- Ye sab static verification + JVM-tested core logic par based hai. Standard Android APIs
  (MediaStore/Notification/ForegroundService) use kiye hain, lekin device-testing ka claim nahi.
- Pehla use: chhota section try karo (e.g. MCQ → chhota topic) → phir bada year.

## 5. Install kaise kare (realme Narzo 30 5G)

**Standalone (recommended — original app delete karne ki zarurat nahi):**
1. `CHSL_Previous_Year_Papers_ZIP_Standalone.apk` phone me copy karo
2. File Manager se kholo → "Install unknown apps" allow (us app ke liye) → Install
3. Play Protect warning aaye: More details → Install anyway
4. Launcher me **"CHSL Papers ZIP Mod"** naam se aayegi (original "CHSL Previous Year Papers" alag se rahegi)

**Replacement (same package):** pehle original uninstall, phir `CHSL_Previous_Year_Papers_ZIP_Mod.apk` install.

**adb:** `adb install -r CHSL_Previous_Year_Papers_ZIP_Standalone.apk`

Agar install phir bhi fail ho: exact error message bhejo (`adb shell pm install -r <apk>` ka output
ya Settings → install ka error) — usse exact reason pata chalega.

## 6. Notes
- Server abhi live hai (content JSON + PDFs 200 OK) — future me developer content hataye to
  dono apps me list hi nahi banegi (same dependency as original)
- 47 PDFs ≈ 90–150MB download — WiFi recommended
- Battery: service sirf task ke दौरान chalti hai, end par khud stop; wake lock bounded;
  realme aggressive battery mode me bhi foreground-notification wali apps generally spared rehti hain
- Signing: `zipmod-release.keystore` (alias `chslzipmod`, pass `chslzipmod123`) — future update ke liye rakh lo
- Original app Tarun Production ki hai; ye mod personal use ke liye
