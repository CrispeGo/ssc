#!/usr/bin/env python3
"""GS project: column-aware OCR of all paper PDFs -> one .txt per paper (workspace).
Handles 2-column layouts (2017-2020) via gutter detection; single-col passes through.
Usage: python3 ocr_all.py <pdfdir> <outdir>"""
import os, sys, subprocess, glob, concurrent.futures as cf
from PIL import Image
import numpy as np

def find_gutter(png):
    """Return split-x if page is 2-column else None."""
    im = Image.open(png).convert('L')
    a = np.asarray(im) < 128
    h, w = a.shape
    colprof = a.sum(axis=0)
    lo, hi = int(w*0.30), int(w*0.70)
    best_len, best_c, run = 0, None, 0
    for x in range(lo, hi):
        if colprof[x] <= max(2, int(h*0.002)):
            run += 1
            if run > best_len: best_len, best_c = run, x
        else:
            run = 0
    if best_c is None: return None
    split = int(best_c - best_len/2)
    left_ink = colprof[:lo].sum(); right_ink = colprof[hi:].sum()
    two_col = (best_len >= 12 and abs(split - w/2) < w*0.06
               and left_ink > h*5 and right_ink > h*5
               and colprof[:split-20].sum() > h*8 and colprof[split+20:].sum() > h*8)
    return split if two_col else None

def ocr_page(png):
    """OCR one page image; split columns when gutter detected."""
    split = find_gutter(png)
    if split is None:
        r = subprocess.run(['tesseract', png, 'stdout', '--psm', '6'],
                           capture_output=True, text=True, timeout=180)
        return r.stdout
    im = Image.open(png)
    w, h = im.size
    left = f'/var/tmp/gswork/tmpimg/_l.png'; right = f'/var/tmp/gswork/tmpimg/_r.png'
    im.crop((0, 0, split, h)).save(left)
    im.crop((split, 0, w, h)).save(right)
    out = []
    for part in (left, right):
        r = subprocess.run(['tesseract', part, 'stdout', '--psm', '6'],
                           capture_output=True, text=True, timeout=180)
        out.append(r.stdout)
    return out[0] + '\n~~COL2~~\n' + out[1]

def ocr_pdf(pdf, outdir):
    base = os.path.splitext(os.path.basename(pdf))[0]
    outtxt = os.path.join(outdir, base + '.txt')
    if os.path.exists(outtxt) and os.path.getsize(outtxt) > 5000:
        return (base, 'cached')
    tmpdir = f'/var/tmp/gswork/tmpimg/{base}'
    os.makedirs(tmpdir, exist_ok=True)
    os.makedirs('/var/tmp/gswork/tmpimg', exist_ok=True)
    try:
        subprocess.run(['pdftoppm', '-r', '150', '-gray', '-png', pdf, f'{tmpdir}/pg'],
                       check=True, capture_output=True, timeout=600)
        pages = sorted(glob.glob(f'{tmpdir}/pg-*.png'))
        parts = []
        for p in pages:
            parts.append(f'===PAGE {os.path.basename(p)}===\n' + ocr_page(p))
        with open(outtxt, 'w') as f:
            f.write('\n'.join(parts))
        for p in pages: os.remove(p)
        os.rmdir(tmpdir)
        return (base, f'ok ({len(pages)}pg)')
    except Exception as e:
        return (base, f'FAIL: {e}')

if __name__ == '__main__':
    pdfdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(pdfdir, '*.pdf')))
    print(f'OCR-ing {len(pdfs)} PDFs (column-aware) -> {outdir}', flush=True)
    done = 0
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        for base, status in ex.map(lambda p: ocr_pdf(p, outdir), pdfs):
            done += 1
            if 'FAIL' in status or done % 10 == 0:
                print(f'[{done}/{len(pdfs)}] {base}: {status}', flush=True)
    print('ALL DONE', flush=True)
