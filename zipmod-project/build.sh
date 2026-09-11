#!/bin/bash
# =====================================================================
# Rebuild script — CHSL ZIP Mod v2 (Build A replacement + Build B standalone)
#   decompile -> patch -> build -> inject dex -> zipalign -> sign
# Requirements: JDK 17+, apktool 3.x, Android build-tools 35, platform 35
# =====================================================================
set -e

ORIGINAL_APK=${1:-/home/user/chsl_app.apk}
BT=${BT:-/opt/android-sdk/build-tools/35.0.0}
AJ=${AJ:-/opt/android-sdk/platforms/android-35/android.jar}
APKTOOL=${APKTOOL:-/opt/tools/apktool.jar}
WORK=/opt/work
OUT=/home/user

cd "$WORK"

# 1. Decompile original (skip if patched projects already exist)
[ -d chsl_mod ] || java -jar "$APKTOOL" d -f -o chsl_mod "$ORIGINAL_APK"
# Build B = copy of patched Build A project + package rename
if [ ! -d chsl_std ]; then
    cp -a chsl_mod chsl_std
    python3 - << 'PYEOF'
OLD = 'com.tarun.sscchslpreviousyearpapers'
NEW = 'com.tarun.sscchslpreviousyearpapers.zipmod'
m = open('chsl_std/AndroidManifest.xml').read()
m = m.replace(f'package="{OLD}"', f'package="{NEW}"')
m = m.replace(f'android:name="{OLD}.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION"',
              f'android:name="{NEW}.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION"')
m = m.replace(f'android:authorities="{OLD}.mobileadsinitprovider"',
              f'android:authorities="{NEW}.mobileadsinitprovider"')
m = m.replace(f'android:authorities="{OLD}.androidx-startup"',
              f'android:authorities="{NEW}.androidx-startup"')
m = m.replace('android:label="@string/app_name"', 'android:label="@string/app_name_standalone"')
open('chsl_std/AndroidManifest.xml','w').write(m)
s = open('chsl_std/res/values/strings.xml').read()
s = s.replace('<string name="app_name">CHSL Previous Year Papers</string>',
    '<string name="app_name">CHSL Previous Year Papers</string>\n    <string name="app_name_standalone">CHSL Papers ZIP Mod</string>')
open('chsl_std/res/values/strings.xml','w').write(s)
PYEOF
fi

# (Patches already applied inside chsl_mod / chsl_std — see patches/ folder:
#    AndroidManifest.xml   : split-attrs removed (install fix), +3 permissions, +ZipService
#    res/layout/activity_chapters.xml : + "Download All as ZIP" button
#    smali/.../ChaptersActivity.smali : + onZipButtonClick(View)
#    smali/.../PdfViewerActivity$2.smali : + individual PDF export hook
#    apktool.yml           : versionCode 11, versionName 10.0.1-zipmod )

# 2. Compile the ZIP feature (Java -> class -> dex)
rm -rf zipclasses zipdex && mkdir -p zipclasses zipdex
javac --release 8 -nowarn -classpath "$AJ" -d zipclasses zipsrc/com/zipmod/*.java
"$BT/d8" --release --lib "$AJ" --min-api 23 --output zipdex zipclasses/com/zipmod/*.class
cp zipdex/classes.dex classes5.dex

# 3. Build both APKs
java -jar "$APKTOOL" b chsl_mod -o buildA_unsigned.apk
java -jar "$APKTOOL" b chsl_std -o buildB_unsigned.apk

# 4. Inject the new dex + zipalign + sign
for V in A B; do
    zip -0 -X build${V}_unsigned.apk classes5.dex
    "$BT/zipalign" -f -p 4 build${V}_unsigned.apk build${V}_aligned.apk
done

"$BT/apksigner" sign --ks zipmod-release.keystore --ks-key-alias chslzipmod \
    --ks-pass pass:chslzipmod123 --key-pass pass:chslzipmod123 \
    --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
    --out "$OUT/CHSL_Previous_Year_Papers_ZIP_Mod.apk" buildA_aligned.apk
"$BT/apksigner" sign --ks zipmod-release.keystore --ks-key-alias chslzipmod \
    --ks-pass pass:chslzipmod123 --key-pass pass:chslzipmod123 \
    --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
    --out "$OUT/CHSL_Previous_Year_Papers_ZIP_Standalone.apk" buildB_aligned.apk
"$BT/apksigner" sign --ks zipmod-debug.keystore --ks-key-alias androiddebugkey \
    --ks-pass pass:android --key-pass pass:android \
    --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
    --out "$OUT/CHSL_Previous_Year_Papers_ZIP_Standalone_Debug.apk" buildB_aligned.apk

# 5. Verify
for APK in "$OUT"/CHSL_*.apk; do
    echo "### $APK"
    "$BT/apksigner" verify "$APK" 2>/dev/null && echo "  sig OK"
    "$BT/zipalign" -c -p 4 "$APK" && echo "  align OK"
    N=$("$BT/aapt" dump xmltree "$APK" AndroidManifest.xml 2>/dev/null | grep -cE "isSplitRequired|requiredSplitTypes")
    echo "  split-attrs: $N (0 = standalone installable)"
done
echo DONE
