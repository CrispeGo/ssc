#!/usr/bin/env python3
"""SSC CHSL GS project — download all paper PDFs from app dataset.
Usage: python3 download_pdfs.py <b_data.json> <outdir>"""
import json, sys, os, urllib.request, concurrent.futures as cf

def dl(args):
    idx, url, year, name, outdir = args
    fn = os.path.join(outdir, f"{year}_{idx:03d}.pdf")
    if os.path.exists(fn) and os.path.getsize(fn) > 10000:
        return (idx, year, name, fn, 'cached')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as r, open(fn, 'wb') as f:
            f.write(r.read())
        return (idx, year, name, fn, 'ok')
    except Exception as e:
        return (idx, year, name, fn, f'FAIL: {e}')

def main():
    jsonfile, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    d = json.load(open(jsonfile))
    tasks = []
    idx = 0
    for c in d['categories']:
        for item in c['data']:
            idx += 1
            url = item['extra'].split('#')[0]
            tasks.append((idx, url, c['year'], item['name'], outdir))
    print(f"downloading {len(tasks)} PDFs...")
    ok = fail = 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(dl, tasks):
            if r[4] in ('ok', 'cached'): ok += 1
            else:
                fail += 1
                print("  ", r[0], r[1], r[2], r[4])
    print(f"DONE: {ok} ok, {fail} failed")

if __name__ == '__main__':
    main()
