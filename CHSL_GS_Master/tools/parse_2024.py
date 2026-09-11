#!/usr/bin/env python3
"""2024 scans v3: Q-line-anchored blocks. Handles single-line and multi-line
option groups; green-tick answer via line + x-token matching."""
import os, sys, subprocess, glob, json, re
import numpy as np
from PIL import Image
import concurrent.futures as cf

SEC = re.compile(r'Section\s*:\s*(.+)', re.I)
QSTART = re.compile(r'^Q\.?\s*\d{1,3}(?!\d)')
ANSISH = re.compile(r"^Ans?\b|^Ans[)\].:,]")
NUMTOK = re.compile(r'^(\d?)([1-4])[\.\),]\S{0,10}$')

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

def page_data(png):
    im = Image.open(png).convert('RGB')
    a = np.asarray(im).astype(int)
    r, g, b = a[...,0], a[...,1], a[...,2]
    green = (g > 90) & (g - r > 35) & (g - b > 35)
    marks = clusters(green)
    tsv = subprocess.run(['tesseract', png, 'stdout', '--psm', '6', 'tsv'],
                         capture_output=True, text=True, timeout=240).stdout
    words = []
    for line in tsv.split('\n')[1:]:
        p = line.split('\t')
        if len(p) == 12 and p[11].strip():
            words.append({'t': p[11].strip(), 'x': int(p[6]), 'y': int(p[7]),
                          'w': int(p[8]), 'h': int(p[9])})
    words.sort(key=lambda w: (w['y'], w['x']))
    lines, cur, cury = [], [], None
    for w in words:
        yc = w['y'] + w['h']/2
        if cury is None or abs(yc - cury) <= 12:
            cur.append(w); cury = yc if cury is None else (cury + yc)/2
        else:
            lines.append(cur); cur, cury = [w], yc
    if cur: lines.append(cur)
    out_lines = []
    for ln in lines:
        ln.sort(key=lambda w: w['x'])
        out_lines.append({'text': ' '.join(w['t'] for w in ln),
                          'words': ln, 'yc': sum(w['y']+w['h']/2 for w in ln)/len(ln)})
    return out_lines, marks

def line_opt_groups(text):
    """All option-number groups on a line, in order: [(k, after_text)]."""
    groups = []
    for m in re.finditer(r'(?:^|\s)([1-4])[\.\),]\s*', text):
        k = int(m.group(1))
        nxt = text[m.end():].strip()
        groups.append((k, nxt))
    return groups

def do_pdf(pdf, outdir):
    base = os.path.splitext(os.path.basename(pdf))[0]
    jout = os.path.join(outdir, base + '.parsed.json')
    if os.path.exists(jout): return (base, 'cached')
    tmpdir = f'/var/tmp/gswork/p24/{base}'
    os.makedirs(tmpdir, exist_ok=True)
    try:
        subprocess.run(['pdftoppm', '-r', '200', '-png', pdf, f'{tmpdir}/pg'],
                       check=True, capture_output=True, timeout=900)
        pages = sorted(glob.glob(f'{tmpdir}/pg-*.png'))
        all_lines, all_marks = [], []
        for p in pages:
            lines, marks = page_data(p)
            all_lines.extend(lines)
            all_marks.extend(marks)
        # green marks -> line index
        marks_by_line = {}
        for m in all_marks:
            best, bd = None, 1e9
            for li, ln in enumerate(all_lines):
                d = abs(ln['yc'] - m['cy'])
                if d < 16 and d < bd: best, bd = li, d
            if best is not None:
                marks_by_line.setdefault(best, []).append(m)
        texts = [ln['text'] for ln in all_lines]
        # section map
        sec = None; secmap = {}
        for i, t in enumerate(texts):
            ms = SEC.search(t)
            if ms: sec = ms.group(1).strip()
            secmap[i] = sec
        # Q-line anchored blocks
        qidx = [i for i, t in enumerate(texts) if QSTART.match(t.strip())]
        questions = []
        for qi, qstart in enumerate(qidx):
            qend = qidx[qi+1] if qi+1 < len(qidx) else len(texts)
            # ans line: first Ans-ish line in range
            ans_line = None
            for i in range(qstart, min(qend, qstart+30)):
                if ANSISH.match(texts[i].strip()): ans_line = i; break
            if ans_line is None: continue
            # options: groups from ans_line onward (max 8 lines)
            opts = {}
            optlines = {}   # k -> line index
            for i in range(ans_line, min(qend, ans_line+8)):
                for k, rest in line_opt_groups(texts[i]):
                    if k not in opts:
                        opts[k] = rest
                        optlines[k] = i
                if len(opts) >= 4: break
            if len(opts) < 3: continue
            # qnum
            qnum = None
            mm = re.search(r'\bQ\.?\s*(\d{1,3})(?!\d)', texts[qstart])
            if mm: qnum = int(mm.group(1))
            qtext = ' '.join(texts[qstart:ans_line])
            # answer: green marks on option lines; x-match when multiple options on a line
            answer = None
            for k, li in sorted(optlines.items()):
                if li in marks_by_line:
                    ms = marks_by_line[li]
                    groups_on_line = line_opt_groups(texts[li])
                    if len(groups_on_line) >= 2:
                        # x-match: number token positions
                        ntoks = [(w['x'], w) for w in all_lines[li]['words'] if NUMTOK.match(w['t'])]
                        for m in ms:
                            best, bd = None, 1e9
                            for tx, w in ntoks:
                                d = abs(tx - m['cx'])
                                if d < bd: best, bd = (w, d)
                            if best and bd < 120:
                                nm = NUMTOK.match(best['t'])
                                kk = int(nm.group(2))
                                if kk in opts: answer = kk; break
                    else:
                        answer = k
                    if answer is not None: break
            questions.append({'sec': secmap.get(ans_line), 'qnum': qnum,
                              'qtext': qtext, 'options': opts, 'answer': answer})
        with open(jout, 'w') as f:
            json.dump(questions, f, ensure_ascii=False)
        with open(os.path.join(outdir, base + '.txt'), 'w') as f:
            f.write('\n'.join(texts))
        for p in pages: os.remove(p)
        os.rmdir(tmpdir)
        nans = sum(1 for q in questions if q['answer'] is not None)
        return (base, f'{len(questions)} blocks, {nans} answers')
    except Exception as e:
        return (base, f'FAIL: {e}')

if __name__ == '__main__':
    pdfdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(pdfdir, '2024_*.pdf')))
    print(f'parse_2024: {len(pdfs)} papers', flush=True)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        for base, status in ex.map(lambda p: do_pdf(p, outdir), pdfs):
            print(f'  {base}: {status}', flush=True)
    print('DONE', flush=True)
