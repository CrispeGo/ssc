#!/usr/bin/env python3
"""Extract all text-layer papers. Per paper: try default pdftotext; if Q-sequence
jumbled, use geometry-aware (anchor-cluster column split). Output text_raw/"""
import sys, os, glob, subprocess, re
import xml.etree.ElementTree as ET

ANCH = re.compile(r'^(\d{1,3}\.|Ans\.?|Q\.?\d+[\.\)]?)$')

def words_of(pdf):
    xml = subprocess.run(['pdftotext', '-bbox', pdf, '-'], capture_output=True, text=True).stdout
    xml = re.sub(r'xmlns="[^"]+"', '', xml, count=1)
    xml = ''.join(ch for ch in xml if ch == '\n' or ch == '\t' or (32 <= ord(ch) and ord(ch) != 127))
    root = ET.fromstring(xml)
    pages, pw = [], 595
    for pg in root.iter('page'):
        pw = float(pg.get('width'))
        pages.append([(float(w.get('xMin')), float(w.get('yMin')),
                       float(w.get('xMax')), float(w.get('yMax')), w.text or '')
                      for w in pg.iter('word')])
    return pw, pages

def build_lines(col):
    col = sorted(col, key=lambda w: (round(w[1], 1), w[0]))
    lines, cur, cury = [], [], None
    for w in col:
        if cury is None or abs(w[1] - cury) <= 3.5:
            cur.append(w); cury = w[1] if cury is None else (cury + w[1]) / 2
        else:
            lines.append(cur); cur, cury = [w], w[1]
    if cur: lines.append(cur)
    return [' '.join(w[4] for w in sorted(ln, key=lambda w: w[0])) for ln in lines]

def anchor_split(pages, pw):
    anchors = sorted(w[0] for words in pages for w in words if ANCH.match(w[4]))
    if len(anchors) < 20: return None
    best, bi = 0, None
    for i in range(len(anchors) - 1):
        gap = anchors[i+1] - anchors[i]
        if pw*0.05 <= (anchors[i]+anchors[i+1])/2 <= pw*0.75 and gap > best:
            best, bi = gap, i
    if bi is None or best < pw*0.06: return None
    if (bi+1) < 10 or (len(anchors)-bi-1) < 10: return None
    return anchors[bi+1] - 2.0

def geom_text(pdf):
    pw, pages = words_of(pdf)
    split = anchor_split(pages, pw)
    out = []
    for words in pages:
        if split:
            out.append('\n'.join(build_lines([w for w in words if (w[0]+w[2])/2 < split])))
            out.append('\n'.join(build_lines([w for w in words if (w[0]+w[2])/2 >= split])))
        else:
            out.append('\n'.join(build_lines(words)))
    return '\n'.join(out)

def q_seq(text):
    qa = [int(m) for m in re.findall(r'^Q\.?\s*(\d{1,3})[\.:)]?\s', text, re.M)]
    qb = [int(m) for m in re.findall(r'^(\d{1,3})\.(?:\s|$)', text, re.M)]
    if len(qa) >= 15: return qa
    if len(qb) >= 15: return qb
    return qa or qb

def descents(qs):
    return sum(1 for a, b in zip(qs, qs[1:]) if b < a)

def extract(pdf):
    base = os.path.basename(pdf)
    default = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    if base[:4] in ('2017', '2018', '2019'):
        geo = geom_text(pdf)
        if len(q_seq(geo)) >= 15:
            return geo, 'geom'
        return default, 'geom-failed-default'
    qs = q_seq(default)
    if len(qs) >= 20 and descents(qs) <= 6:
        return default, 'default'
    geo = geom_text(pdf)
    qg = q_seq(geo)
    if descents(qg) < descents(qs):
        return geo, 'geom'
    return default, 'default-jumbled'

if __name__ == '__main__':
    pdfdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    from collections import Counter
    modes = Counter()
    for pdf in sorted(glob.glob(os.path.join(pdfdir, '*.pdf'))):
        base = os.path.splitext(os.path.basename(pdf))[0]
        if base.startswith('2024'): continue
        out = os.path.join(outdir, base + '.txt')
        meta = os.path.join(outdir, base + '.mode')
        if os.path.exists(out): continue
        try:
            txt, mode = extract(pdf)
            open(out, 'w').write(txt)
            open(meta, 'w').write(mode)
            modes[mode] += 1
        except Exception as e:
            print(f'FAIL {base}: {e}', flush=True)
            modes['FAIL'] += 1
    print('modes:', dict(modes), flush=True)
