#!/usr/bin/env python3
"""Post-fix 2023 gs_parsed: extract options glued in qtext; strip mark glyphs;
restore missing qnums from text-layer skeleton (with answers)."""
import os, sys, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ocr_2023_gs import ga_page_range
from parse_text import parse_qn_choosen

MARKS = re.compile(r'^[\s\-*%~#@«✓XxvVlL()\.]{0,6}')
OPTM = re.compile(r'(?:(?<=[\s\-*%~#@])|^)([1-4])\.\s*')

def fix_q(q):
    qt = q.get('qtext', '') or ''
    if not q.get('options'):
        ms = list(OPTM.finditer(qt))
        # find a run covering >= 3 distinct ks
        best = None
        for i in range(len(ms)):
            run = [ms[i]]
            for j in range(i+1, len(ms)):
                if ms[j].group(1) != run[-1].group(1):
                    run.append(ms[j])
                if len({m.group(1) for m in run}) >= 4: break
            ks = {m.group(1) for m in run}
            if len(ks) >= 2:
                best = run; break
        if best:
            opts = {}
            for k, m in enumerate(best):
                end = best[k+1].start() if k+1 < len(best) else len(qt)
                raw = qt[m.end():end]
                raw = MARKS.sub('', raw)
                raw = re.sub(r'[\s\-*%~#@]+$', '', raw)
                opts[m.group(1)] = re.sub(r'\s+', ' ', raw).strip()
            q['options'] = opts
            qt = qt[:best[0].start()]
    qt = MARKS.sub('', qt)
    qt = re.sub(r'^Ans\s*', '', qt)
    q['qtext'] = re.sub(r'\s+', ' ', qt).strip()
    return q

def main(rawdir, parseddir):
    for f in sorted(glob.glob(os.path.join(parseddir, '2023_*.gs.json'))):
        base = os.path.basename(f).replace('.gs.json', '')
        d = json.load(open(f))
        qs = [fix_q(q) for q in d['questions']]
        # skeleton from text layer
        txt = open(os.path.join(rawdir, base + '.txt')).read()
        rng = ga_page_range(txt)
        skel = {}
        if rng:
            lines = ('\f'.join(txt.split('\f')[rng[0]:rng[1]])).split('\n')
            for q in parse_qn_choosen(lines, 0, len(lines)):
                if q.get('qnum') is not None:
                    skel[q['qnum']] = q.get('answer')
        # apply answers, find missing
        have = set()
        for q in qs:
            if q.get('qnum') is not None:
                have.add(q['qnum'])
                if q.get('answer') is None and q['qnum'] in skel:
                    q['answer'] = skel[q['qnum']]
        missing = sorted(set(skel) - have)
        for qn in missing:
            qs.append({'qnum': qn, 'qtext': '[question PDF me image tha — OCR se capture nahi hua]',
                       'options': {}, 'answer': skel.get(qn)})
        qs.sort(key=lambda q: (q.get('qnum') is None, q.get('qnum') or 999))
        with open(f, 'w') as fh:
            json.dump({'mode': 'ocr+skel', 'questions': qs, 'span': d.get('span', [])}, fh, ensure_ascii=False)
        na = sum(1 for q in qs if q.get('answer') is not None)
        print(f'{base}: {len(qs)} Qs, {na} answers, opts-fixed: {sum(1 for q in qs if q["options"])}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
