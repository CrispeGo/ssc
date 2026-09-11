#!/usr/bin/env python3
"""2024 scan papers: color render -> tesseract text + green-tick answer detection.
Per paper: <base>.txt (OCR text) + <base>.answers.json ({qnum: chosen_option})"""
import os, sys, subprocess, glob, json, re
import numpy as np
from PIL import Image

def green_marks(png):
    im = Image.open(png).convert('RGB')
    a = np.asarray(im).astype(int)
    r, g, b = a[...,0], a[...,1], a[...,2]
    mask = (g > 90) & (g - r > 35) & (g - b > 35)
    ys, xs = np.nonzero(mask)
    if len(ys) == 0: return []
    pts = sorted(zip(ys.tolist(), xs.tolist()))
    clusters = []
    for y, x in pts:
        placed = False
        for c in clusters:
            if abs(y - c['cy']) < 22 and abs(x - c['cx']) < 60:
                c['ys'].append(y); c['xs'].append(x)
                c['cy'] = sum(c['ys'])/len(c['ys']); c['cx'] = sum(c['xs'])/len(c['xs'])
                placed = True; break
        if not placed:
            clusters.append({'ys':[y],'xs':[x],'cy':y,'cx':x})
    # keep clusters with enough pixels (real marks)
    return [(c['cy'], c['cx'], len(c['ys'])) for c in clusters if len(c['ys']) >= 8]

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

QRE = re.compile(r'^Q\.?\s*(\d{1,3})[\.\):]?$|^Q\.?(\d{1,3})$')
OPTRE = re.compile(r'^([1-4])[\.\)]$')

def page_answers(png):
    marks = green_marks(png)
    if not marks: return {}, []
    toks = tsv_tokens(png)
    # question-start tokens: 'Q.5' possibly split as 'Q.5' single or 'Q' '.5'
    qtoks = []
    for i, t in enumerate(toks):
        m = QRE.match(t['text'])
        if m:
            qn = m.group(1) or m.group(2)
            qtoks.append((int(qn), t['top'], t['left']))
    answers = {}
    for my, mx, npix in marks:
        # find option token on same line, right of mark
        best = None
        for t in toks:
            om = OPTRE.match(t['text'])
            if om and abs((t['top'] + t['h']/2) - my) < 14 and 0 < t['left'] - mx < 120:
                if best is None or t['left'] < best[1]: best = (int(om.group(1)), t['left'])
        if best is None: continue
        opt = best[0]
        # nearest question above (same column: mark x within [qleft-50, qleft+600])
        qabove = None
        for qn, qtop, qleft in qtoks:
            if qtop <= my + 5 and qleft < mx + 100 and qleft > mx - 400:
                if qabove is None or qtop > qabove[1]: qabove = (qn, qtop)
        if qabove: answers[str(qabove[0])] = opt
    return answers, qtoks and [q[0] for q in qtoks] or []

def do_pdf(pdf, outdir):
    base = os.path.splitext(os.path.basename(pdf))[0]
    txtout = os.path.join(outdir, base + '.txt')
    jout = os.path.join(outdir, base + '.answers.json')
    if os.path.exists(txtout) and os.path.exists(jout): return (base, 'cached')
    tmpdir = f'/var/tmp/gswork/tmp24/{base}'
    os.makedirs(tmpdir, exist_ok=True)
    try:
        subprocess.run(['pdftoppm', '-r', '200', '-png', pdf, f'{tmpdir}/pg'],
                       check=True, capture_output=True, timeout=900)
        pages = sorted(glob.glob(f'{tmpdir}/pg-*.png'))
        parts, allans = [], {}
        for p in pages:
            r = subprocess.run(['tesseract', p, 'stdout', '--psm', '6'],
                               capture_output=True, text=True, timeout=240)
            parts.append(f'===PAGE {os.path.basename(p)}===\n' + r.stdout)
            ans, _ = page_answers(p)
            for k, v in ans.items():
                allans.setdefault(k, v)
        with open(txtout, 'w') as f: f.write('\n'.join(parts))
        with open(jout, 'w') as f: json.dump(allans, f)
        for p in pages: os.remove(p)
        os.rmdir(tmpdir)
        return (base, f'ok ({len(pages)}pg, {len(allans)} answers)')
    except Exception as e:
        return (base, f'FAIL: {e}')

if __name__ == '__main__':
    pdfdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(pdfdir, '2024_*.pdf')))
    print(f'2024 OCR+ticks: {len(pdfs)} papers', flush=True)
    import concurrent.futures as cf
    done = 0
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        for base, status in ex.map(lambda p: do_pdf(p, outdir), pdfs):
            done += 1
            print(f'[{done}/{len(pdfs)}] {base}: {status}', flush=True)
    print('ALL DONE', flush=True)
