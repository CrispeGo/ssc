#!/usr/bin/env python3
# PDF लेआउट QA: margins, blank pages, column balance, content height
from PIL import Image
import glob

files = sorted(glob.glob('qa/pg-*.png'))
print(f"pages: {len(files)}")
S = 65/25.4
L, R, T, B = 15*S, 13*S, 15*S, 17*S
TOL = 4

for f in files:
    im = Image.open(f).convert('L')
    w, h = im.size
    px = im.load()
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if px[x, y] < 200:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    issues = []
    if maxx == -1:
        issues.append("BLANK PAGE")
    else:
        if minx < L - TOL: issues.append(f"left-margin: {minx:.0f}<{L:.0f}")
        if maxx > w - R + TOL: issues.append(f"right-margin: {maxx:.0f}>{w-R:.0f}")
        if miny < T - TOL: issues.append(f"top-margin: {miny:.0f}<{T:.0f}")
        if maxy > h - B + TOL: issues.append(f"bottom-margin: {maxy:.0f}>{h-B:.0f}")
    body_h = ((maxy - miny) / (h - T - B) * 100) if maxx > 0 else 0
    if maxx > minx:
        lw = rw = 0
        midx = (minx + maxx) // 2
        for y in range(int(miny), int(maxy), 3):
            for x in range(int(minx), int(midx), 2):
                if px[x, y] < 200: lw += 1
            for x in range(int(midx), int(maxx), 2):
                if px[x, y] < 200: rw += 1
        tot = lw + rw
        bal = f"L{lw*100//max(tot,1)}%/R{rw*100//max(tot,1)}%" if tot > 500 else "sparse"
    else:
        bal = "-"
    print(f"{f.split('/')[-1]}: contentH={body_h:.0f}% {bal} {'⚠ ' + '; '.join(issues) if issues else 'OK'}")
