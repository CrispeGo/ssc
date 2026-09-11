# Workspace Backup — GitHub Mirror

- **Remote repo:** https://github.com/CrispeGo/ssc (branch: `main`)
- यह workspace का पूरा backup है: CHSL_GS_Master (Parts 1-5 + tools + raw data), CHSL_Maths_Master, chsl-zip-web (web app), zipmod-project, APK builds, uploads (source txt) आदि।

## दोबारा push करना हो तो (नए session में)
```
cd /home/user
git remote add origin https://github.com/CrispeGo/ssc.git   # यदि remote न हो
git add -A && git commit -m "update"
git push https://<GH_PAT>@github.com/CrispeGo/ssc.git main
```
- PAT token यहाँ file में संग्रहित नहीं है (सुरक्षा) — user के पास रहता है।
- `.git/config` platform-snapshot में persist नहीं होता, इसलिए remote हर नए session में दोबारा add करना पड़ सकता है।
- `node_modules/`, `.npm/`, `.env` git में नहीं जाते (.gitignore)।
