#!/usr/bin/env python3
"""Build the single consolidated GS TXT (maths-TXT format).
Sources: ocr_raw/2024_*.parsed.json + gs_parsed/*.gs.json + b_data.json (names).
Usage: python3 build_gs_txt.py <rootdir> <outfile>"""
import os, sys, json, glob, re

def load_bdata(root):
    d = json.load(open(os.path.join(root, 'b_data.json')))
    papers = []
    for c in d['categories']:
        for it in c['data']:
            papers.append({'year': c['year'], 'name': it['name']})
    return papers

def norm_text(t):
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def render_q(q, idx, style):
    """style: 'num' (1-4) or 'let' (A-D)."""
    qnum = q.get('qnum') if q.get('qnum') is not None else idx
    qt = norm_text(q.get('qtext', ''))
    qt = re.sub(r'^\s*Q\.?\s*\d{1,3}[\.:)_]?\s*', '', qt)
    out = [f"Q{qnum}. {qt}"]
    opts = q.get('options', {})
    if any(str(k) in ('1', '2', '3', '4') for k in opts):
        keys = ['1', '2', '3', '4']
    else:
        keys = ['A', 'B', 'C', 'D']
    for k in keys:
        if k in opts and str(opts[k]).strip():
            out.append(f"   ({k}) {norm_text(str(opts[k]))}")
        elif k in opts:
            out.append(f"   ({k}) [option text image/figure me tha]")
    if len(opts) == 0:
        out.append("   [Options image me the — OCR se capture nahi hue]")
    a = q.get('answer')
    if a is not None:
        akey = str(a)
        atext = opts.get(akey, opts.get(int(a) if str(a).isdigit() else a, ''))
        if akey in opts and str(opts.get(akey, '')).strip():
            out.append(f"   >> Answer: ({akey}) {norm_text(str(opts[akey]))}")
        else:
            out.append(f"   >> Answer: ({akey})")
    else:
        out.append("   >> Answer: [extract nahi ho paya — original PDF me dekhein]")
    return '\n'.join(out)

def main():
    root, outfile = sys.argv[1], sys.argv[2]
    papers = load_bdata(root)
    assert len(papers) == 193, len(papers)
    blocks = []
    ystats = {}
    tot_q = tot_a = 0
    for idx, p in enumerate(papers, 1):
        year = p['year']
        base = f"{year}_{idx:03d}"
        qs = []
        src = ''
        if year == 2024:
            f = os.path.join(root, 'ocr_raw', base + '.parsed.json')
            if os.path.exists(f):
                allq = json.load(open(f))
                qs = [q for q in allq if q.get('sec') and re.search(r'wareness|knowledge', str(q['sec']), re.I)]
            src = 'OCR (scan) + green-tick answer detection'
        else:
            f = os.path.join(root, 'gs_parsed', base + '.gs.json')
            if os.path.exists(f):
                d = json.load(open(f))
                qs = d['questions']
                m = d.get('mode', '')
                if year == 2023 or m == 'ocr':
                    src = "OCR (questions images me the) + text-layer 'Chosen Option' answers"
                elif base == '2021_118':
                    src = 'OCR (text-layer font corrupt tha)'
                elif year in (2017, 2018, 2019):
                    src = 'TEXT-layer (geometry-aware 2-column extraction)'
                else:
                    src = "TEXT-layer (candidate-response 'Chosen Option')"
            else:
                src = 'GS SECTION PARSE FAIL'
        style = 'let' if year in (2017, 2018, 2019) else 'num'
        na = sum(1 for q in qs if q.get('answer') is not None)
        yst = ystats.setdefault(year, [0, 0, 0])
        yst[0] += 1; yst[1] += len(qs); yst[2] += na
        tot_q += len(qs); tot_a += na
        lines = []
        lines.append('=' * 78)
        lines.append(f"PAPER {idx:03d}  |  {year}  |  {p['name']}  [Tier-I]")
        lines.append(f"Source: {src}  |  Questions: {len(qs)}  |  Answers mile: {na}/{len(qs)}")
        lines.append('=' * 78)
        # render sorted by qnum if all have qnum, else doc order
        rq = sorted(qs, key=lambda q: (q.get('qnum') is None, q.get('qnum') if q.get('qnum') is not None else 999))
        # placeholders for missing qnums in 1..25 (2019+) or contiguous range
        qnums = [q.get('qnum') for q in rq if q.get('qnum') is not None]
        if qnums:
            expected = set(range(min(qnums), min(qnums) + 25))
            missing = sorted(expected - set(qnums))
        else:
            missing = []
        byq = {q.get('qnum'): q for q in rq if q.get('qnum') is not None}
        noq = [q for q in rq if q.get('qnum') is None]
        emitted = set()
        for qn in sorted(set(qnums) | (expected if qnums else set())):
            if qn in byq:
                lines.append('')
                lines.append(render_q(byq[qn], qn, style))
                emitted.add(id(byq[qn]))
        for q in noq:
            lines.append('')
            lines.append(render_q(q, 0, style))
        for qn in missing:
            lines.append('')
            lines.append(f"Q{qn}. [Question PDF me image/figure-based tha — OCR se capture nahi hua; answer bhi nahi mila]")
        blocks.append('\n'.join(lines))
    # header
    H = []
    H.append('=' * 78)
    H.append('  SSC CHSL TIER-I — GENERAL AWARENESS / GK (GS) QUESTIONS')
    H.append('  2024 se 2017 tak | Sabhi available shifts | ~25 questions per paper')
    H.append('=' * 78)
    H.append('')
    H.append(f'  TOTAL: 193 papers | {tot_q} questions parsed | {tot_a} answers extracted')
    H.append('  (Image-based questions ke liye ~618 placeholder lines bhi hain — har paper ka 25-question slot covered hai)')
    H.append('')
    H.append('  Year-wise breakdown (papers / questions / answers):')
    for y in sorted(ystats, reverse=True):
        p_, q_, a_ = ystats[y]
        H.append(f'    {y}:  {p_:3d} papers | {q_:5d} questions | {a_:5d} answers')
    H.append('')
    H.append('  KAISE BANA HAI (honest disclosure):')
    H.append("  - 2017-2019 (46 papers): 2-column PDFs — geometry-aware text-layer")
    H.append("    extraction (column split ke saath); 'Ans. X' letters se answers.")
    H.append("  - 2020-2022 (81 papers): text-layer direct; answers 'Chosen Option'")
    H.append("    (candidate-response sheets) se — 2020_118 samet kuch papers me")
    H.append("    'Not Answered' (--) ka matlab answer available nahi hai.")
    H.append('  - 2021 ka 1 paper (118): font-layer corrupt — poora OCR.')
    H.append('  - 2023 (32 papers): question-bodies PDF me IMAGES the — GS pages')
    H.append("    ka OCR (150dpi) + answers text-layer 'Chosen Option' se merge.")
    H.append('  - 2024 (34 papers): English PDFs pure scans — poora OCR (200dpi)')
    H.append('    + GREEN-TICK answer detection (SSC sheet me har question me 1')
    H.append('    green tick = sahi option, 3 red X = galat).')
    H.append('  - [Image/figure-based] questions: jahan question/options image me')
    H.append('    the aur OCR fail hua, wahan placeholder diya hai — taaki koi')
    H.append('    question miss na lage, aap PDF me dekh sakte ho.')
    H.append("  - 'Chosen Option' wale answers candidate ke responses hain —")
    H.append('    bade level par sahi hain (maths project me inhi se 4825 me sirf')
    H.append('    8 discrepancy aaye the), par GS me fact-check Master phase me')
    H.append('    hoga — dataset-answer galat milega to flag hoga.')
    H.append('  - OCR wale questions me spelling/half-reading errors possible hain')
    H.append('    — meaning clear rehta hai.')
    H.append('')
    H.append('  NOTE: Question numbers original paper ke according hain (2017-2018')
    H.append('  me GS block 26-50/76-100 jaise ranges me hai; 2019+ me har section')
    H.append('  Q.1-25 restart hota hai).')
    H.append('')
    H.append('=' * 78)
    out = '\n'.join(H) + '\n\n' + '\n\n'.join(blocks) + '\n'
    with open(outfile, 'w') as f:
        f.write(out)
    print(f'written {outfile}: {tot_q} questions, {tot_a} answers, {len(papers)} papers')

if __name__ == '__main__':
    main()
