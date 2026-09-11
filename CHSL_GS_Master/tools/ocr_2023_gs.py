#!/usr/bin/env python3
"""2023 papers: GS question-bodies are images. OCR the GA pages; merge answers
from text-layer skeleton (gs_parsed/*.gs.json). Also OCR 2021_118 (broken font).
Usage: python3 ocr_2023_gs.py <pdfdir> <rawdir> <parseddir>"""
import os, sys, glob, json, re, subprocess
import concurrent.futures as cf

GA = re.compile(r'section\s*:\s*general\s*awareness', re.I)
ANY = re.compile(r'section\s*:\s*\w', re.I)

def ga_page_range(txt):
    """Return (start_page, end_page_exclusive) for GA section (0-based)."""
    chunks = txt.split('\f')
    start = end = None
    for i, c in enumerate(chunks):
        if start is None and GA.search(c):
            start = i
        elif start is not None and ANY.search(c) and not GA.search(c):
            end = i
            break
    if start is None: return None
    if end is None: end = len(chunks)
    return (start, end)

def ocr_pdf_pages(pdf, p0, p1, tag):
    tmpdir = f'/var/tmp/gswork/g23/{tag}'
    os.makedirs(tmpdir, exist_ok=True)
    subprocess.run(['pdftoppm', '-r', '150', '-gray', '-png', '-f', str(p0+1), '-l', str(p1),
                    pdf, f'{tmpdir}/pg'], check=True, capture_output=True, timeout=600)
    pages = sorted(glob.glob(f'{tmpdir}/pg-*.png'))
    parts = []
    for p in pages:
        r = subprocess.run(['tesseract', p, 'stdout', '--psm', '6'],
                           capture_output=True, text=True, timeout=240)
        parts.append(r.stdout)
        os.remove(p)
    try: os.rmdir(tmpdir)
    except OSError: pass
    return '\n'.join(parts)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_text import parse_qn_choosen

def do_2023(pdf, rawdir, parseddir):
    base = os.path.splitext(os.path.basename(pdf))[0]
    txt_path = os.path.join(rawdir, base + '.txt')
    skel_path = os.path.join(parseddir, base + '.gs.json')
    out_path = skel_path
    if os.path.exists(txt_path + '.done'): return (base, 'cached')
    txt = open(txt_path).read()
    rng = ga_page_range(txt)
    if rng is None: return (base, 'no-GA-header')
    p0, p1 = rng
    ocr_txt = ocr_pdf_pages(pdf, p0, p1, base)
    # trim before GA header on the first OCR page (previous section's tail)
    m = GA.search(ocr_txt)
    if m and ocr_txt[:m.start()].count('Section') >= 0:
        ocr_txt = ocr_txt[m.start():]
    lines = ocr_txt.split('\n')
    qs = parse_qn_choosen(lines, 0, len(lines))
    # answers from skeleton (text layer)
    skel = {}
    if os.path.exists(skel_path):
        for q in json.load(open(skel_path))['questions']:
            if q.get('qnum') is not None and q.get('answer') is not None:
                skel[q['qnum']] = q['answer']
    for q in qs:
        if q.get('qnum') in skel:
            q['answer'] = skel[q['qnum']]
    with open(out_path, 'w') as f:
        json.dump({'mode': 'ocr', 'questions': qs, 'span': [p0, p1]}, f, ensure_ascii=False)
    open(txt_path + '.done', 'w').write('ok')
    na = sum(1 for q in qs if q['answer'] is not None)
    return (base, f'{len(qs)} Qs, {na} answers')

def do_118(pdfdir, rawdir):
    pdf = os.path.join(pdfdir, '2021_118.pdf')
    if not os.path.exists(pdf): return ('2021_118', 'no pdf')
    out = os.path.join(rawdir, '2021_118.txt')
    if os.path.exists(out) and os.path.getsize(out) > 5000: return ('2021_118', 'cached')
    txt = ocr_pdf_pages(pdf, 0, 99, 'y2021_118')
    with open(out, 'w') as f: f.write(txt)
    return ('2021_118', f'{len(txt)} chars')

if __name__ == '__main__':
    pdfdir, rawdir, parseddir = sys.argv[1], sys.argv[2], sys.argv[3]
    r = do_118(pdfdir, rawdir)
    print(r[1], flush=True)
    pdfs = sorted(glob.glob(os.path.join(pdfdir, '2023_*.pdf')))
    print(f'2023 GS OCR: {len(pdfs)} papers', flush=True)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        for base, status in ex.map(lambda p: do_2023(p, rawdir, parseddir), pdfs):
            print(f'  {base}: {status}', flush=True)
    print('DONE', flush=True)
