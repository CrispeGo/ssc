#!/bin/bash
BASE="https://www.selfstudys.com"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
OUT="/home/user/agniveer"
mkdir -p "$OUT"

# group:year:slug -> we derive folder and filename from slug
papers=(
"group-x:2020:agniveer-vayu-science-group-x-4-nov-2020"
"group-x:2021:agniveer-vayu-science-group-x-18-july-2021"
"group-x:2022:agniveer-vayu-science-group-x-25-july-2022"
"group-x:2023:agniveer-vayu-science-group-x-18-jan-2023"
"group-x:2023:agniveer-vayu-science-group-x-19-jan-2023"
"group-x:2023:agniveer-vayu-science-group-x-13-oct-2023-shift-1"
"group-x:2023:agniveer-vayu-science-group-x-14-oct-2023-shift-1"
"group-x:2024:agniveer-vayu-science-group-x-16-nov-2024"
"group-x:2025:agniveer-vayu-science-group-x-22-march-2025"
"group-y:2021:agniveer-vayu-other-than-science-group-y-13-july-2021"
"group-y:2022:agniveer-vayu-other-than-science-group-y-24-july-2022"
"group-y:2022:agniveer-vayu-other-than-science-group-y-25-july-2022"
"group-y:2022:agniveer-vayu-other-than-science-group-y-27-july-2022"
"group-y:2023:agniveer-vayu-other-than-science-group-y-18-jan-2023"
"group-y:2023:agniveer-vayu-other-than-science-group-y-19-jan-2023"
"group-y:2023:agniveer-vayu-other-than-science-group-y-20-jan-2023"
"group-y:2023:agniveer-vayu-other-than-science-group-y-13-oct-2023-shift-1"
"group-y:2023:agniveer-vayu-other-than-science-group-y-13-oct-2023-shift-2"
"group-y:2023:agniveer-vayu-other-than-science-group-y-14-oct-2023"
"group-y:2025:agniveer-vayu-other-than-science-group-y-22-march-2025"
)

for p in "${papers[@]}"; do
  IFS=':' read -r grp yr slug <<< "$p"
  page="$BASE/nda/agniveer-vayu/$grp/pyqs/$yr/$slug"
  html=$(curl -sL "$page" -H "User-Agent: $UA")
  pdfid=$(echo "$html" | grep -oE 'https://www\.selfstudys\.com/sitepdfs/[A-Za-z0-9]+' | head -1)
  if [ -z "$pdfid" ]; then
    echo "NO-PDF-ID :: $grp $yr $slug"
    continue
  fi
  fname="$OUT/$(echo "$grp" | tr '-' '_')_${yr}_${slug}.pdf"
  code=$(curl -sL "$pdfid" -H "User-Agent: $UA" -H "Referer: $page" -o "$fname" -w "%{http_code}")
  sz=$(wc -c < "$fname")
  ftype=$(file -b "$fname" | cut -d, -f1)
  echo "$code $sz $ftype :: $fname"
  sleep 1
done
