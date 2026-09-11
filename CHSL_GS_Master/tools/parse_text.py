#!/usr/bin/env python3
"""Parse GS questions from text-layer papers (2017-2023) -> structured JSON.
Formats:
  2017/2018: 'N.' qnums, A.-D. options, 'Ans. X' / lone letter; NO section headers -> content window
  2019:      sections restart 1-25, 'Ans: X'
  2020/2022: 'Q.N', options 1.-4., 'Chosen Option : N', 'Section : X'
  2021:      continuous 1-100, bare-letter options (A\\n text), 'Answer: X'
  2023:      skeleton only (image questions) -> answers only; questions via OCR (separate)
"""
import os, sys, glob, json, re

GA_HDR = re.compile(r'(section\s*:\s*)?general\s*awareness', re.I)
ANY_HDR = re.compile(r'^(section\s*:\s*)?(general\s*(intelligence|awareness|knowledge)|quantitative\s*aptitude|english\s*language|general\s*reasoning)', re.I)
CHOSEN = re.compile(r'Chosen\s*Option\s*:\s*(\d|--)', re.I)
QID = re.compile(r'Question ID')

GS_CUES = ['who', 'which', 'whom', 'whose', 'where', 'when', 'first', 'capital', 'state', 'river',
    'governor', 'constitution', 'amendment', 'article', 'festival', 'dance', 'dynasty', 'king',
    'emperor', 'battle', 'treaty', 'planet', 'satellite', 'vitamin', 'hormone', 'acid', 'organ',
    'cell', 'national park', 'sanctuary', 'census', 'gdp', 'rbi', 'currency', 'olympic', 'award',
    'nobel', 'author', 'painter', 'musician', 'temple', 'architecture', 'mughal', 'maurya', 'gupta',
    'revolt', 'congress', 'movement', 'election', 'lok sabha', 'rajya sabha', 'supreme court',
    'soil', 'crop', 'monsoon', 'mountain', 'plateau', 'glacier', 'ocean', 'desert', 'coal',
    'mineral', 'iron', 'magnet', 'unit of', 'invention', 'invented', 'discover', 'scientist',
    'president', 'prime minister', 'parliament', 'language', 'tribe', 'species', 'bird', 'animal',
    'disease', 'blood', 'bone', 'brain', 'heart', 'gas', 'metal', 'non-metal', 'salt', 'water',
    'india', 'indian', 'world', 'country', 'city', 'birth', 'died', 'founder', 'established',
    'tiger', 'lion', 'forest', 'wildlife', 'biosphere', 'heritage', 'stupa', 'cave', 'painting',
    'singer', 'player', 'sport', 'trophy', 'rank', 'index', 'scheme', 'policy', 'commission',
    'committee', 'act', 'law', 'court', 'judge', 'currency', 'bank', 'budget', 'tax', 'trade']
OTH_CUES = {'series': -2, 'analogy': -2, 'code language': -3, 'mirror image': -3, 'dice': -3,
    'venn': -3, 'odd': -1, 'conclusion': -2, 'statements': -1, 'arrange': -1, 'matrix': -2,
    'blood relation': -3, 'figure': -1, 'diagram': -1, 'synonym': -4, 'antonym': -4, 'idiom': -4,
    'spelt': -4, 'narration': -4, 'voice': -2, 'blank': -2, 'passage': -2, 'sentence': -2,
    'grammar': -4, 'ratio': -3, 'average': -3, 'percent': -3, 'profit': -3, 'loss': -3,
    'interest': -3, 'km/h': -3, 'train': -2, 'pipe': -2, 'days': -1, 'angle': -2, 'triangle': -2,
    'circle': -2, 'area': -2, 'volume': -3, 'simplify': -3, 'equation': -2, 'x2': -2}

def score_text(t):
    tl = t.lower()
    s = sum(2 for c in GS_CUES if c in tl)
    for c, w in OTH_CUES.items():
        if c in tl: s += w
    return s

def clean(t):
    return re.sub(r'\s+', ' ', t).strip()

def window_gs(questions):
    """2017/2018: pick the best GS block. Primary: qnum-aligned 25-blocks
    (1-25, 26-50, ...); fallback: sliding window by score."""
    n = len(questions)
    W = 25
    if n <= W: return (0, n)
    scores = [score_text(q['qtext'] + ' ' + ' '.join(str(v) for v in q['options'].values()))
              for q in questions]
    # aligned blocks by qnum
    blocks = {}
    for i, q in enumerate(questions):
        qn = q.get('qnum')
        if qn is None: continue
        b = (qn - 1) // 25
        blocks.setdefault(b, []).append(i)
    best, bsel = -1e9, None
    for b, idxs in sorted(blocks.items()):
        if len(idxs) < 12: continue
        s = sum(scores[i] for i in idxs)
        if s > best:
            best, bsel = s, idxs
    if bsel is not None:
        return sorted(bsel)
    # fallback: sliding
    best, bi = -1e9, 0
    cur = sum(scores[:W])
    for i in range(0, n - W + 1):
        if i > 0: cur += scores[i+W-1] - scores[i-1]
        if cur > best: best, bi = cur, i
    return (bi, bi + W)

def split_opts(line):
    ms = list(re.finditer(r'(?:^|\s)([A-D])\.\s*', line))
    out = {}
    for j, m in enumerate(ms):
        end = ms[j+1].start() if j+1 < len(ms) else len(line)
        out[m.group(1)] = clean(line[m.end():end])
    return out

def parse_lettered(lines, i0, i1):
    """2017/2018/2019: 'N.' qnum, A.-D. options (may share lines), 'Ans. X'/'Ans: X'/lone letter."""
    questions = []
    cur = None
    def close():
        nonlocal cur
        if cur and cur['options']:
            questions.append(cur)
        cur = None
    for i in range(i0, i1):
        t = lines[i].strip()
        if not t: continue
        mq = re.match(r'^(\d{1,3})\.(?:\s|$)', t)
        opts_here = split_opts(t)
        if mq and cur is not None and int(mq.group(1)) == cur.get('qnum'):
            # duplicated qnum line (geom artifact): append text
            cur['qtext'] += ' ' + t[mq.end():]
            continue
        if mq and not opts_here:
            close()
            cur = {'qnum': int(mq.group(1)), 'qtext': t[mq.end():], 'options': {}, 'answer': None}
        elif mq and opts_here:
            close()
            qi = t.find('A.')
            if qi < 0 or qi < mq.end():
                qi = mq.end()
            cur = {'qnum': int(mq.group(1)), 'qtext': clean(t[mq.end():qi]),
                   'options': opts_here, 'answer': None}
        elif cur is not None:
            m1 = re.match(r'^Ans[\.:]?\s*([A-D])(?![A-Za-z0-9])', t)
            if m1:
                cur['answer'] = m1.group(1)
                close()
            elif re.match(r'^Ans\.?\s*$', t):
                cur['_ans_pending'] = True
            elif cur.get('_ans_pending') and re.match(r'^[A-D](?:\s|\.|$)', t):
                cur['answer'] = t[0]
                cur.pop('_ans_pending', None)
                close()
            elif opts_here and not re.match(r'^Ans', t):
                for k, v in opts_here.items():
                    cur['options'].setdefault(k, v)
            else:
                if len(cur['options']) == 0:
                    cur['qtext'] += ' ' + t
                else:
                    lastk = max(cur['options'])
                    cur['options'][lastk] = clean(cur['options'][lastk] + ' ' + t)
    close()
    for q in questions:
        q['qtext'] = clean(q.get('qtext', ''))
    return questions

def parse_qn_choosen(lines, i0, i1):
    """2020/2022: 'Q.N ...', 'Ans', options '1. x', 'Chosen Option : k'."""
    questions = []
    cur = None
    for i in range(i0, i1):
        t = lines[i].strip()
        if not t: continue
        mq = re.match(r'^Q\.?\s*(\d{1,3})(?!\d)\s*(.*)', t)
        mc = CHOSEN.search(t)
        if mq:
            if cur: questions.append(cur)
            cur = {'qnum': int(mq.group(1)), 'qtext': clean(mq.group(2)), 'options': {}, 'answer': None}
        elif mc and cur is not None:
            v = mc.group(1)
            cur['answer'] = int(v) if v.isdigit() else None
            questions.append(cur); cur = None
        elif cur is not None:
            mo = re.match(r'^([1-4])\.\s*(.*)', t)
            if mo and len(cur['options']) < 4:
                cur['options'][int(mo.group(1))] = clean(mo.group(2))
            elif re.match(r'^(Ans|Question ID|Status)', t):
                continue
            elif not cur['options']:
                cur['qtext'] = clean(cur['qtext'] + ' ' + t)
    if cur: questions.append(cur)
    return questions

def parse_2021(lines, i0, i1):
    """2021: 'N.' qnum, bare-letter options (A on own line), 'Answer: X'."""
    questions = []
    cur = None
    for i in range(i0, i1):
        t = lines[i].strip()
        if not t: continue
        mq = re.match(r'^(\d{1,3})\.(?:\s|$)', t)
        ma = re.match(r'^Answer\s*:\s*([A-D])\b', t, re.I)
        if mq:
            if cur: questions.append(cur)
            cur = {'qnum': int(mq.group(1)), 'qtext': t[mq.end():], 'options': {}, 'answer': None, '_opt': None}
        elif ma and cur is not None:
            cur['answer'] = ma.group(1)
            questions.append(cur); cur = None
        elif cur is not None:
            if re.match(r'^[A-D]$', t):
                cur['_opt'] = t
                cur['options'][t] = ''
            elif cur.get('_opt'):
                cur['options'][cur['_opt']] = clean(cur['options'][cur['_opt']] + ' ' + t)
            else:
                cur['qtext'] += ' ' + t
    if cur: questions.append(cur)
    for q in questions:
        q.pop('_opt', None)
        q['qtext'] = clean(q['qtext'])
    return questions

def find_sections(lines):
    """Return list of (line_idx, header_text)."""
    out = []
    for i, t in enumerate(lines):
        if ANY_HDR.match(t.strip()) or GA_HDR.match(t.strip()):
            out.append((i, t.strip()))
    return out

def parse_paper(base, text):
    year = int(base[:4])
    lines = text.split('\n')
    secs = find_sections(lines)
    ga_span = None
    for j, (i, h) in enumerate(secs):
        if GA_HDR.match(h):
            end = len(lines)
            for k in range(j+1, len(secs)):
                if not GA_HDR.match(secs[k][1]):
                    end = secs[k][0]
                    break
            ga_span = (i+1, end)
            break
    if year in (2017, 2018):
        qs = parse_lettered(lines, 0, len(lines))
        if not qs: return None
        sel = window_gs(qs)
        if isinstance(sel, list):
            return {'mode': 'window', 'questions': [qs[i] for i in sel], 'all_n': len(qs), 'span': [min(sel), max(sel)+1]}
        s, e = sel
        return {'mode': 'window', 'questions': qs[s:e], 'all_n': len(qs), 'span': [s, e]}
    if ga_span is None: return None
    # format auto-detection within the GA span
    seg = '\n'.join(lines[ga_span[0]:ga_span[1]])
    n_qn = len(re.findall(r'^Q\.?\s*\d{1,3}(?!\d)', seg, re.M))
    n_chosen = len(re.findall(r'Chosen\s*Option', seg, re.I))
    n_answer = len(re.findall(r'^Answer\s*:', seg, re.M | re.I))
    n_anscolon = len(re.findall(r'^Ans[\.:]', seg, re.M))
    if n_qn >= 10 and n_chosen >= 10:
        mode = 'qchosen'
    elif n_qn >= 10 and n_answer >= 10:
        mode = 'qanswer'
    elif n_answer >= 10:
        mode = 'y2021'
    else:
        mode = 'lettered'
    if mode == 'qchosen':
        qs = parse_qn_choosen(lines, *ga_span)
    elif mode == 'y2021':
        qs = parse_2021(lines, *ga_span)
    elif mode == 'qanswer':
        # Q.N qnums but 'Answer: X' style: strip Q. prefix then lettered-parse
        qs = parse_qn_choosen(lines, *ga_span)
    else:
        qs = parse_lettered(lines, *ga_span)
    # dedupe by qnum (keep first), keep doc order
    seen, out = set(), []
    for q in qs:
        k = q.get('qnum')
        if k is not None and k in seen: continue
        if k is not None: seen.add(k)
        out.append(q)
    return {'mode': mode, 'questions': out, 'span': list(ga_span)}

if __name__ == '__main__':
    rawdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    import collections
    stats = collections.defaultdict(lambda: [0, 0, 0])  # papers, qsum, asum
    for f in sorted(glob.glob(os.path.join(rawdir, '*.txt'))):
        base = os.path.splitext(os.path.basename(f))[0]
        year = base[:4]
        if year == '2024': continue
        r = parse_paper(base, open(f).read())
        if r is None:
            print(f'  {base}: NO GS SECTION FOUND', flush=True)
            continue
        with open(os.path.join(outdir, base + '.gs.json'), 'w') as fh:
            json.dump(r, fh, ensure_ascii=False)
        st = stats[year]
        st[0] += 1; st[1] += len(r['questions']); st[2] += sum(1 for q in r['questions'] if q['answer'])
    for y in sorted(stats):
        p, q, a = stats[y]
        print(f'{y}: {p} papers | GS-Qs: {q} (avg {q/max(p,1):.1f}) | answers: {a} ({100*a/max(q,1):.0f}%)')
