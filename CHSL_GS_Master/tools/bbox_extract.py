#!/usr/bin/env python3
"""Geometry-aware text extraction from text-layer PDFs (handles 2-column pages)."""
import sys, subprocess, re
import xml.etree.ElementTree as ET

def analyze(words, pw):
    # try rank-gap on sorted x-centers (bimodal distribution)
    cw = sorted((w[0]+w[2])/2 for w in words)
    n = len(cw)
    if n >= 16:
        lo, hi = pw*0.28, pw*0.72
        best, bi = 0, None
        for i in range(n-1):
            gap = cw[i+1] - cw[i]
            c = (cw[i]+cw[i+1])/2
            if lo <= c <= hi and gap > best:
                best, bi = gap, i
        if bi is not None and best > pw*0.025:
            split = (cw[bi]+cw[bi+1])/2
            lcount = bi+1; rcount = n-lcount
            if lcount >= 8 and rcount >= 8:
                return split
    # fallback: empty-interval gap
    ivs = sorted((w[0], w[2]) for w in words)
    merged = []
    for s, e in ivs:
        if merged and s <= merged[-1][1] + 0.5:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    lo, hi = pw*0.30, pw*0.70
    best, g0, g1 = 0, None, None
    for i in range(len(merged)-1):
        a, b = merged[i][1], merged[i+1][0]
        c = (a+b)/2
        if lo <= c <= hi and b-a > best:
            best, g0, g1 = b-a, a, b
    if g0 is None or best < pw*0.008:
        return None
    center = (g0+g1)/2
    crossings = sum(1 for w in words if w[0] < center and w[2] > center)
    if crossings > max(8, len(words)*0.02):
        return None
    split = g0 + min(2.5, best*0.3)
    lcount = sum(1 for w in words if (w[0]+w[2])/2 < split)
    if lcount < 8 or len(words)-lcount < 8:
        return None
    return split

def build_lines(col):
    col = sorted(col, key=lambda w: (round(w[1], 1), w[0]))
    lines, cur, cury = [], [], None
    for w in col:
        if cury is None or abs(w[1] - cury) <= 3.5:
            cur.append(w)
            cury = w[1] if cury is None else (cury + w[1]) / 2
        else:
            lines.append(cur); cur, cury = [w], w[1]
    if cur: lines.append(cur)
    out = []
    for ln in lines:
        ln.sort(key=lambda w: w[0])
        out.append(' '.join(w[4] for w in ln))
    return out

def page_lines(words, pw):
    if not words: return []
    W = [(w[0], w[1], w[2], w[3], w[4]) for w in words]
    split = analyze(W, pw)
    if split:
        return build_lines([w for w in W if (w[0]+w[2])/2 < split]) + ['~~COL2~~'] + \
               build_lines([w for w in W if (w[0]+w[2])/2 >= split])
    return build_lines(W)

def extract(pdf):
    xml = subprocess.run(['pdftotext', '-bbox', pdf, '-'], capture_output=True, text=True).stdout
    xml = re.sub(r'xmlns="[^"]+"', '', xml, count=1)
    xml = ''.join(ch for ch in xml if ch == '\n' or ch == '\t' or (ord(ch) >= 32 and ord(ch) != 127))
    root = ET.fromstring(xml)
    out = []
    for pg in root.iter('page'):
        pw = float(pg.get('width'))
        words = [(float(w.get('xMin')), float(w.get('yMin')),
                  float(w.get('xMax')), float(w.get('yMax')), w.text or '')
                 for w in pg.iter('word')]
        out.append('\n'.join(page_lines(words, pw)))
    return '\n\f\n'.join(out)

if __name__ == '__main__':
    for pdf in sys.argv[1:]:
        print(f'===FILE {pdf}===')
        print(extract(pdf))
