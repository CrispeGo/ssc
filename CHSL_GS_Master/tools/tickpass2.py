#!/usr/bin/env python3
"""Pass-2 answer detection for 2024 scans: re-render pages, find green ticks,
map to nearest option-number token and question. Overwrites .answers.json files.
Usage: python3 tickpass2.py <pdfdir> <rawdir>"""
import os, sys, subprocess, glob, json, re
import numpy as np
from PIL import Image
import concurrent.futures as cf

QRE = re.compile(r'^Q\.?\s*(\d{1,3})[\.:)]?$')
OPTRE = re.compile(r'^([1-4])[\.\)]$')

def clusters(mask):
    ys, xs = np.nonzero(mask)
    pts = sorted(zip(ys.tolist(), xs.tolist()))
    cl = []
    for y, x in pts:
        placed = False
        for c in cl:
            if abs(y - c['cy']) < 22 and abs(x - c['cx']) < 60:
                c['ys'].append(y); c['xs'].append(x)
                c['cy'] = sum(c['ys'])/len(c['ys']); c['cx'] = sum(c['xs'])/len(c['xs'])
                placed = True; break
        if not placed:
            cl.append({'ys':[y],'xs':[x],'cy':y,'cx':x})
    return [c for c in cl if len(c['ys']) >= 8]

def tsv_tokens(png):
    r = subprocess.run(['tesseract', png, 'stdout', '--psm', '6', 'tsv'],
                       capture_output=True, text=True, timeout=240)
    toks = []
    for line in r.stdout.split('\n')[1:]:
        p = line.split('\t')
        if len(p) == 12 and p[11].strip():
            toks.append({'text': p[11].strip(), 'left': int(p[6]), 'top': int(p[7]),
                         'w': int(p[8]), 'h': int(p[9])})
    return toks

def page_tokens_marks(png):
    im = Image.open(png).convert('RGB')
    a = np.asarray(im).astype(int)
    r, g, b = a[...,0], a[...,1], a[...,2]
    green = (g > 90) & (g - r > 35) & (g - b > 35)
    marks = clusters(green)
    toks = tsv_tokens(png)
    return toks, marks

def page_events(png):
    """Return ordered events: ('Q', qnum, y, x) and ('M', markidx, y, x) for green marks."""
    toks, marks = page_tokens_marks(png)
    events = []
    for t in toks:
        m = QRE.match(t['text'])
        if m:
            events.append(('Q', int(m.group(1)), t['top'] + t['h']/2, t['left']))
    for i, c in enumerate(marks):
        events.append(('M', i, c['cy'], c['cx']))
    # option tokens indexed for lookup
    optmap = [(t, OPTRE.match(t['text'])) for t in toks]
    opttoks = [(t, int(om.group(1))) for t, om in optmap if om and len(t['text']) <= 12]
    return events, opttoks, marks

def do_pdf(pdf, rawdir):
    base = os.path.splitext(os.path.basename(pdf))[0]
    jout = os.path.join(rawdir, base + '.answers.json')
    tmpdir = f'/var/tmp/gswork/tp2/{base}'
    os.makedirs(tmpdir, exist_ok=True)
    try:
        subprocess.run(['pdftoppm', '-r', '200', '-png', pdf, f'{tmpdir}/pg'],
                       check=True, capture_output=True, timeout=900)
        pages = sorted(glob.glob(f'{tmpdir}/pg-*.png'))
        qorder, ans = [], {}   # qorder: list of qnums in doc order; ans: {instance_idx: option}
        for p in pages:
            events, opttoks, marks = page_events(p)
            events.sort(key=lambda e: e[2])
            for ev in events:
                if ev[0] == 'Q':
                    qorder.append(ev[1])
                else:
                    mi, my, mx = ev[1], ev[2], ev[3]
                    best = None
                    for t, onum in opttoks:
                        if abs((t['top'] + t['h']/2) - my) < 14 and t['left'] - 70 < mx < t['left'] + 90:
                            if best is None or abs(t['left'] - mx) < abs(best[1] - mx):
                                best = (onum, t['left'])
                    if best is not None and qorder:
                        idx = len(qorder) - 1
                        if idx not in ans: ans[idx] = best[0]
        with open(jout, 'w') as f:
            json.dump({'qorder': qorder, 'answers': ans}, f)
        for p in pages: os.remove(p)
        os.rmdir(tmpdir)
        return (base, f'{len(qorder)} Qs, {len(ans)} answers')
    except Exception as e:
        return (base, f'FAIL: {e}')

if __name__ == '__main__':
    pdfdir, rawdir = sys.argv[1], sys.argv[2]
    pdfs = sorted(glob.glob(os.path.join(pdfdir, '2024_*.pdf')))
    print(f'tickpass2: {len(pdfs)} papers', flush=True)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        for base, status in ex.map(lambda p: do_pdf(p, rawdir), pdfs):
            print(f'  {base}: {status}', flush=True)
    print('DONE', flush=True)
