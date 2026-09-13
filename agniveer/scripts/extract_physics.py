#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract ALL Physics questions from every available paper into master JSON.
Layout-aware for SelfStudys + Prepp (2-col option tables, formula fragments)."""
import re, os, json
import pymupdf

AG = '/home/user/agniveer'

def clean(s):
    s = s.replace('\u00a0', ' ')
    return re.sub(r'\s+', ' ', s).strip()

# Physics symbol glyphs (private-use area) -> readable Unicode.
PHYS_SYM = {
    '\uf03d': '=', '\uf044': 'Δ', '\uf063': 'χ', '\uf06a': 'φ', '\uf06c': 'λ',
    '\uf06d': 'μ', '\uf070': 'π', '\uf075': 'υ', '\uf077': 'ω', '\uf0b4': '×',
    '\uf0ce': 'ε',
}

def _clean_sym(s):
    for k, v in PHYS_SYM.items():
        s = s.replace(k, v)
    return s

# ---------------------------------------------------------------- shared positional helpers
def _lines(doc):
    lines = []
    for pi in range(doc.page_count):
        for blk in doc[pi].get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                text = "".join(s["text"] for s in ln["spans"]).strip()
                if not text:
                    continue
                b = ln["bbox"]
                lines.append((pi, b[1], b[3], b[0], b[2], text))
    lines.sort(key=lambda L: (L[0], L[1], L[3]))
    return lines

def _fracbars(doc):
    """Horizontal fraction bars: thin filled rects (width > 4, height <= 3)."""
    bars = []
    for pi in range(doc.page_count):
        for d in doc[pi].get_drawings():
            r = d['rect']
            w = r.x1 - r.x0
            h = r.y1 - r.y0
            if d.get('type') == 'f' and w > 4 and 0 < h <= 3:
                bars.append((pi, r.y0, r.y1, r.x0, r.x1))
    return bars

def _join_rows(frags, bars=None):
    """frags: [(text, page, y, x), ...] -> option string (stacked fractions joined by '/')."""
    frags = sorted(frags, key=lambda f: (f[1], f[2], f[3]))
    if not frags:
        return ''
    bars = bars or []
    def bar_between(prev, cur):
        for (bp, by0, by1, bx0, bx1) in bars:
            if bp != cur[1]:
                continue
            ymid = (by0 + by1) / 2
            if prev[2] <= ymid <= cur[2]:
                if bx1 >= prev[3] - 30 and bx0 <= cur[3] + 30:
                    return True
        return False
    rows = []
    cur = [frags[0]]
    for f in frags[1:]:
        if f[1] == cur[-1][1] and f[2] - cur[-1][2] <= 5 and not bar_between(cur[-1], f):
            cur.append(f)
        else:
            rows.append(cur)
            cur = [f]
    rows.append(cur)
    rowtexts = []
    for r in rows:
        r = sorted(r, key=lambda f: f[3])
        rowtexts.append(''.join(f[0] for f in r))
    if len(rowtexts) == 1:
        return clean(rowtexts[0])
    if rowtexts[0].startswith('√'):
        inner = rowtexts[0][1:].strip()
        if not inner:
            return '√(' + '/'.join(rowtexts[1:]) + ')'
        return '√(' + inner + '/' + rowtexts[1] + ')'
    return ' / '.join(clean(t) for t in rowtexts)

# ---------------------------------------------------------------- SelfStudys
def extract_selfstudys(path, qrange):
    doc = pymupdf.open(path)
    lines = _lines(doc)
    bars = _fracbars(doc)
    qidx = [i for i, L in enumerate(lines) if re.match(r'^Question\s+\d+$', L[5])]
    parsed = {}
    for qi, mi in enumerate(qidx):
        n = int(re.match(r'^Question\s+(\d+)', lines[mi][5]).group(1))
        end = qidx[qi + 1] if qi + 1 < len(qidx) else len(lines)
        seg = lines[mi + 1:end]
        opt_h = ans_h = None
        for k, L in enumerate(seg):
            if L[5].startswith('Options') and opt_h is None:
                opt_h = k
            if re.match(r'^Answer\s*:', L[5]) and ans_h is None:
                ans_h = k
        if opt_h is None:
            for k, L in enumerate(seg):
                if re.match(r'^[A-D]\.\s*(.*)$', L[5]) and L[3] < 70:
                    opt_h = k
                    break
        qseg = seg[:opt_h] if opt_h is not None else seg
        qtext = clean(' '.join(L[5] for L in qseg))
        ans = ''
        if ans_h is not None:
            m = re.search(r'Answer\s*:\s*([A-D])', seg[ans_h][5])
            ans = m.group(1) if m else ''
        opts = ['', '', '', '']
        if opt_h is not None:
            region = seg[opt_h + 1: ans_h if ans_h is not None else len(seg)]
            labels = []  # (letter, page, y, inline or None)
            for L in region:
                m = re.match(r'^([A-D])\.\s*(.*)$', L[5])
                if m and L[3] < 70:
                    inline = m.group(2).strip()
                    labels.append((m.group(1), L[0], L[1], inline if inline else None))
            frags = {c: [] for c in 'ABCD'}
            for (Let, pg, y, inline) in labels:
                if inline:
                    frags[Let].append((inline, pg, y, 70))
            for L in region:
                if re.match(r'^([A-D])\.\s*(.*)$', L[5]) and L[3] < 70:
                    continue
                if L[5].startswith('Options') or re.match(r'^Answer\s*:', L[5]):
                    continue
                tgt = None
                for (Let, pg, ly, inline) in labels:
                    if pg < L[0] or (pg == L[0] and ly <= L[1] + 10):
                        tgt = Let
                if tgt is None:
                    continue
                frags[tgt].append((L[5], L[0], L[1], L[3]))
            for c in 'ABCD':
                opts['ABCD'.index(c)] = _join_rows(frags[c], bars)
        parsed[n] = {'q': qtext, 'opts': opts, 'ans': ans}
    return [parsed.get(n) for n in qrange]

# ---------------------------------------------------------------- Prepp (layout-aware, 2-col)
def extract_prepp(path, qrange):
    doc = pymupdf.open(path)
    lines = _lines(doc)
    bars = _fracbars(doc)
    qidx = [i for i, L in enumerate(lines) if re.match(r'^Que\.\s*\d+', L[5])]
    ansmap = {}
    # Answer-key pages (2020 papers): pages with "Que." lines but no "1."-"4." option markers.
    qpages = set(L[0] for L in lines if re.match(r'^Que\.\s*\d+', L[5]))
    mpages = set(L[0] for L in lines if re.match(r'^[1-4]\.\s*$', L[5]) and L[3] < 60)
    key_pages = qpages - mpages
    for i, L in enumerate(lines):
        m = re.search(r'Correct Option\s*[-–]\s*([1-4])', L[5])
        if not m:
            continue
        if L[0] in key_pages:
            # 2020 answer-key table: pair with the nearest "Que." line on the same page.
            best = None
            bd = 1e9
            for j in qidx:
                if lines[j][0] == L[0]:
                    d = abs(lines[j][1] - L[1])
                    if d < bd:
                        bd = d
                        best = j
            if best is not None:
                n = int(re.match(r'^Que\.\s*(\d+)', lines[best][5]).group(1))
                ansmap[n] = int(m.group(1))
            continue
        # 2021 papers: inline "Correct Option - N" after the options -> nearest preceding Que.
        prev = None
        for j in qidx:
            if j < i:
                prev = j
            else:
                break
        if prev is not None:
            n = int(re.match(r'^Que\.\s*(\d+)', lines[prev][5]).group(1))
            ansmap[n] = int(m.group(1))
    parsed = {}
    # question text may sit a few px ABOVE the "Que. N" label on the same page;
    # compute each question's start (backward walk) first so each text line is
    # owned by exactly one question's segment (prevents next-question bleed).
    starts = []
    for mi in qidx:
        start = mi
        while start > 0:
            L = lines[start - 1]
            if L[0] != lines[mi][0]:
                break
            if (lines[mi][1] - L[1]) > 20:
                break
            t = L[5]
            if re.match(r'^Que\.\s*\d+', t) or 'Correct Option' in t or 'Solution' in t:
                break
            if re.match(r'^[1-4]\.\s*$', t) and L[3] < 60:
                break
            start -= 1
        starts.append(start)
    for qi, mi in enumerate(qidx):
        n = int(re.match(r'^Que\.\s*(\d+)', lines[mi][5]).group(1))
        start = starts[qi]
        end = starts[qi + 1] if qi + 1 < len(starts) else len(lines)
        seg = lines[start:end]
        markers = []  # (seg_index, num, page, y)
        for k, L in enumerate(seg):
            if re.match(r'^[1-4]\.\s*$', L[5]) and L[3] < 60:
                markers.append((k, int(L[5][0]), L[0], L[1]))
        if len(markers) < 4:
            continue  # answer-key line block (no options)
        fm = markers[0]
        qlines = []
        for k, L in enumerate(seg):
            if k >= fm[0]:
                break
            if re.match(r'^Que\.\s*\d+', L[5]):
                continue
            if 'Correct Option' in L[5] or 'Solution' in L[5]:
                continue
            if L[3] >= 220:
                continue
            near = any(m[2] == L[0] and abs(m[3] - L[1]) <= 5 for m in markers)
            if not near:
                qlines.append(L[5])
        qtext = clean(' '.join(qlines))
        frags = {1: [], 2: [], 3: [], 4: []}
        for k, L in enumerate(seg):
            if 'Correct Option' in L[5] or 'Solution' in L[5]:
                continue
            if re.match(r'^[1-4]\.\s*$', L[5]):
                continue
            if re.match(r'^Que\.\s*\d+', L[5]):
                continue
            tgt = None
            for (kk, num, pg, my) in markers:
                if pg < L[0] or (pg == L[0] and my <= L[1] + 5):
                    tgt = num
            if tgt is None:
                continue
            frags[tgt].append((L[5], L[0], L[1], L[3]))
        opts = [_join_rows(frags[i], bars) for i in (1, 2, 3, 4)]
        ai = ansmap.get(n)
        ans = 'ABCD'[ai - 1] if ai and 1 <= ai <= 4 else ''
        parsed[n] = {'q': qtext, 'opts': opts, 'ans': ans}
    return [parsed.get(n) for n in qrange]

# ---------------------------------------------------------------- Prepp 12-Jul-2021 S2 (manual)
def _q(q, opts, ans=''):
    return {'q': q, 'opts': opts, 'ans': ans}

def extract_prepp_12jul(path, qrange):
    return [
        _q("Which electromagnetic wave has maximum wavelength?", ["X-rays", "Gamma rays", "Radio wave", "Infrared wave"], "C"),
        _q("Which of the following shows the CORRECT relationship between half time and decay constant?",
           ["T1/2 = λ / 0.693", "T1/2 = 0.693 / λ", "T1/2 = λ × 0.693", "T1/2 = λ² / 0.693"], "B"),
        _q("Which of the following is not a unit of magnetic field?", ["Tesla", "Gauss", "N/kg-m", "Weber"], "C"),
        _q("Excess pressure in a soap bubble of radius r is proportional to", ["1/r", "1/r²", "r", "r²"], "A"),
        _q("When an electromagnetic wave moves from one medium to another medium, then which quantity will not change:",
           ["Wavelength", "Speed", "Frequency", "None of these"], "C"),
        _q("If a wire of uniform area of cross-section is cut into two equal parts, the resistivity of each part will be?",
           ["four times", "double", "halve", "same"], "D"),
        _q("Find the equivalent resistance of the given circuit:", ["20 Ω", "30 Ω", "40 Ω", "50 Ω"], "A"),
        _q("What is the dimension of mutual induction?",
           ["[M L² T⁻³ A⁻¹]", "[M L² T⁻² A⁻²]", "[M L³ T⁻⁴ A⁻¹]", "[M L³ T⁻⁴ A⁻²]"], "B"),
        _q("For which of the following materials, the temperature coefficient will be negative?",
           ["Copper", "Tungsten", "Germanium", "Aluminium"], "C"),
        _q("A solid spherical conductor is placed in an external electric field. It is given a charge q. The charge q",
           ["is distributed uniformly throughout the sphere",
            "is distributed non-uniformly, but throughout the sphere",
            "is distributed uniformly on the surface of the sphere",
            "is distributed non-uniformly on the surface of the sphere"], "D"),
        _q("Consider a car moving with constant acceleration along a straight road and the distance covered by the car is given by equation s = 5t² + 3t + 9 metres. Then find the ratio of acceleration and initial velocity of the car at the start.",
           ["10 : 3", "1 : 2", "3 : 10", "2 : 1"], "C"),
        _q("Which one of the following statements is correct",
           ["Rolling friction is greater than sliding friction",
            "Rolling friction is less than sliding friction",
            "Rolling friction is equal to sliding friction",
            "Rolling friction and sliding friction are same"], "B"),
        _q("The ratio of the radii of two planets are respectively as 1 : 4 and the ratio of their densities are respectively 1 : 2. The ratio of the accelerations due to gravity at their surfaces is:",
           ["1 : 8", "1 : 4", "4 : 1", "8 : 1"], "A"),
        _q("In which type of wave energy is not transferred?", ["Heat waves", "Target waves", "Stationary waves", "Unstationary waves"], "C"),
        _q("The ratio of SI unit and CGS unit of force is", ["10⁹", "10⁷", "10⁵", "10¹¹"], "C"),
        _q("For projectile motion, the correct relation between maximum height H and the range R is (θ is angle of projection):",
           ["H = 4 R cot θ", "R = 4 H cot θ", "R = H/4 cot θ", "R = 2 H cot θ"], "B"),
        _q("If the elastic potential energy density stored in a material is 3 × 10⁴ J/m³ due to the application of longitudinal stress of 1 × 10¹¹ N/m², then the strain developed in it would be",
           ["6 × 10⁻⁷", "3 × 10⁻⁷", "4 × 10⁻⁷", "None"], "A"),
        _q("A Carnot engine is working between the temperature range of 327°C and 127°C. If the heat absorbed by the engine is 9 × 10⁴ J, the work done by the engine is:",
           ["3 × 10⁴ J", "6 × 10⁴ J", "4 × 10⁴ J", "5 × 10⁴ J"], "A"),
        _q("Which of the following phenomenon is/are responsible for formation of a rainbow in the sky?",
           ["Reflection", "Refraction", "Dispersion", "All three"], "D"),
        _q("The magnetic flux linked with a coil in weber is given by the equation ϕ = 6t² + 3t + 2. Then the magnitude of induced emf in the coil at t = 3 sec will be:",
           ["39 V", "44 V", "36 V", "50 V"], "A"),
        _q("A body of mass M moving with a velocity V explodes into two equal parts. If one comes to rest and the other body moves with velocity v, what would be the value of v?",
           ["V", "V/√2", "4V", "2V"], "D"),
        _q("Same gas is filled in two containers of same volume, same temperature and with pressure of ratio 1 : 2. The ratio of their rms speeds is:",
           ["1 : 2", "2 : 1", "1 : 4", "1 : 1"], "D"),
        _q("Two conducting wires A and B are made of same material. If the length of B is twice that of A and radius of circular cross section of A is twice that of B, then their resistances RA and RB are in the ratio",
           ["2 : 1", "1 : 2", "1 : 8", "1 : 4"], "C"),
        _q("Average power in LCR circuit depends upon",
           ["current", "current, emf, and phase difference", "emf", "phase difference"], "B"),
        _q("Which of the following statement is incorrect regarding centre of mass?",
           ["The centre of gravity is the point through which the force of gravity acts on an object or system.",
            "Centre of Mass of a body is a point at which the whole of the mass of the body can be assumed as a point mass.",
            "The Center of Mass of a body will always be inside the body.",
            "All of the above statements are correct regarding centre of mass."], "C"),
    ]

# ---------------------------------------------------------------- Utkarsh
def _strip_junk(text):
    out = []
    for ln in text.split('\n'):
        s = ln.strip()
        if re.match(r'^(Agniveer|Held On_|Download|Join|Telegram|Utkarsh|www\.|https?)', s):
            continue
        if re.match(r'^-::\s*\d*\s*::-?$', s):
            continue
        if re.match(r'^Correct Option', s):
            continue
        if re.match(r'^Section\s*:', s):
            continue
        out.append(ln)
    return '\n'.join(out)

def _utkarsh_split(text):
    markers = list(re.finditer(r'\[([a-dA-D]?)\]', text))
    chunks = []
    prev = 0
    for m in markers:
        letter = m.group(1).upper() if m.group(1) else ''
        chunks.append((text[prev:m.start()], letter))
        prev = m.end()
    return chunks

def _utkarsh_parse(chunks, qrange):
    qs = {}
    for ch, ans in chunks:
        mm = re.match(r'\s*(\d{1,2})[.)]?\s*(.*)', ch, re.DOTALL)
        if not mm:
            mm = re.search(r'^\s*(\d{1,2})\.\s*', ch, re.M)
            if mm:
                body = ch[mm.end():]
                n = int(mm.group(1))
            else:
                continue
        else:
            n = int(mm.group(1))
            body = mm.group(2)
        om = re.search(r'\(a\)(.*?)\(b\)(.*?)\(c\)(.*?)\(d\)(.*?)$', body, re.DOTALL)
        qtext = clean(body[:om.start()]) if om else clean(body)
        qtext = re.sub(r'^\d+\s+(?=[A-Z])', '', qtext)
        opts = ['', '', '', '']
        if om:
            opts = [clean(om.group(i)) for i in (1, 2, 3, 4)]
        qs[n] = {'q': qtext, 'opts': opts, 'ans': ans}
    return [qs.get(n) for n in qrange]

def extract_utkarsh_x(path, qrange):
    d = pymupdf.open(path)
    full = "\n".join(d[i].get_text() for i in range(d.page_count))
    full = _strip_junk(full)
    return _utkarsh_parse(_utkarsh_split(full), qrange)

def extract_utkarsh_xy(path, start_kw, end_kw, qrange):
    d = pymupdf.open(path)
    raw = "\n".join(d[i].get_text() for i in range(d.page_count))
    s = raw.find(start_kw)
    e = raw.find(end_kw, s + 1)
    seg = raw[s:e] if (s >= 0 and e > s) else (raw[s:] if s >= 0 else '')
    seg = _strip_junk(seg)
    return _utkarsh_parse(_utkarsh_split(seg), qrange)

# ---------------------------------------------------------------- User TXT (verbatim)
def extract_user_txt(path, qrange):
    txt = open(path, encoding='utf-8').read()
    blocks = {}
    cur = None
    for ln in txt.split('\n'):
        m = re.match(r'^Q\.(\d+)\s*(.*)$', ln)
        if m:
            cur = int(m.group(1))
            rest = m.group(2).strip()
            blocks[cur] = ([rest] if rest else [])
        elif cur is not None:
            blocks[cur].append(ln)
    out = []
    for n in qrange:
        if n in blocks:
            raw = '\n'.join(blocks[n]).strip('\n')
            raw = re.sub(r'\n{3,}', '\n\n', raw)
            out.append({'q': None, 'opts': [], 'ans': '', 'raw': raw})
        else:
            out.append(None)
    return out

# ---------------------------------------------------------------- PW model 2
def extract_pw_model2(path, qrange):
    d = pymupdf.open(path)
    full = "\n".join(d[i].get_text() for i in range(d.page_count))
    ansmap = {}
    for m in re.finditer(r'Q(\d+)\s*\(([A-D])\)', full):
        ansmap[int(m.group(1))] = m.group(2)
    parts = re.split(r'\nQ(\d+)\s', full)
    blocks = {}
    for k in range(1, len(parts) - 1, 2):
        n = int(parts[k])
        if n not in blocks:
            blocks[n] = parts[k + 1]
    out = []
    for n in qrange:
        b = blocks.get(n, '')
        if not b.strip():
            out.append(None)
            continue
        b = re.split(r'Text Solution\s*:|Answer Key|Android App', b)[0]
        m = re.search(r'\(A\)(.*?)\(B\)(.*?)\(C\)(.*?)\(D\)(.*?)(?=\nQ\d+\s|\Z)', b, re.DOTALL)
        qtext = clean(b[:m.start()]) if m else clean(b)
        opts = ['', '', '', '']
        if m:
            opts = [clean(m.group(i)) for i in (1, 2, 3, 4)]
        out.append({'q': qtext, 'opts': opts, 'ans': ansmap.get(n, '')})
    return out

# ---------------------------------------------------------------- Prepp sample physics
def extract_sample_physics(path, qrange):
    d = pymupdf.open(path)
    full = "\n".join(d[i].get_text() for i in range(d.page_count))
    parts = re.split(r'Q\.(\d+)\.', full)
    blocks = {}
    for k in range(1, len(parts) - 1, 2):
        blocks[int(parts[k])] = parts[k + 1]
    out = []
    for n in qrange:
        b = blocks.get(n, '')
        if not b.strip():
            out.append(None)
            continue
        am = re.search(r'Ans\s*:\s*([A-Da-d])', b)
        ans = am.group(1).upper() if am else ''
        m = re.search(r'\(A\)(.*?)\(B\)(.*?)\(C\)(.*?)\(D\)(.*?)(?=Ans\s*:|\Z)', b, re.DOTALL)
        qtext = clean(b[:m.start()]) if m else clean(b)
        opts = ['', '', '', '']
        if m:
            opts = [clean(m.group(i)) for i in (1, 2, 3, 4)]
        out.append({'q': qtext, 'opts': opts, 'ans': ans})
    return out

# ---------------------------------------------------------------- inventory
R25 = range(1, 26)
R12 = range(1, 13)
papers = [
    ('X', '2020-11-04', '04 Nov 2020', 'SelfStudys', 'Group_X_2020_04-Nov.pdf', 'selfstudys', R25),
    ('X', '2021-07-18', '18 Jul 2021', 'SelfStudys', 'Group_X_2021_18-Jul.pdf', 'selfstudys', R25),
    ('X', '2022-07-25', '25 Jul 2022', 'SelfStudys', 'Group_X_2022_25-Jul.pdf', 'selfstudys', R25),
    ('X', '2023-01-18', '18 Jan 2023', 'SelfStudys', 'Group_X_2023_18-Jan.pdf', 'selfstudys', R25),
    ('X', '2023-01-19', '19 Jan 2023', 'SelfStudys', 'Group_X_2023_19-Jan.pdf', 'selfstudys', R25),
    ('X', '2023-10-13', '13 Oct 2023 Shift-1', 'SelfStudys', 'Group_X_2023_13-Oct_Shift-1.pdf', 'selfstudys', R12),
    ('X', '2023-10-14', '14 Oct 2023 Shift-1', 'SelfStudys', 'Group_X_2023_14-Oct_Shift-1.pdf', 'selfstudys', R12),
    ('X', '2024-11-16', '16 Nov 2024', 'SelfStudys', 'Group_X_2024_16-Nov.pdf', 'selfstudys', R25),
    ('X', '2025-03-22', '22 Mar 2025', 'SelfStudys', 'Group_X_2025_22-Mar.pdf', 'selfstudys', R25),
    ('X', '2020-11-04', '04 Nov 2020', 'Prepp', 'prepp/Group_X_2020_04-Nov.pdf', 'prepp', range(21, 46)),
    ('X', '2020-11-05', '05 Nov 2020', 'Prepp', 'prepp/Group_X_2020_05-Nov.pdf', 'prepp', range(21, 46)),
    ('X', '2020-11-06', '06 Nov 2020', 'Prepp', 'prepp/Group_X_2020_06-Nov.pdf', 'prepp', range(21, 46)),
    ('X', '2020-11-07', '07 Nov 2020', 'Prepp', 'prepp/Group_X_2020_07-Nov.pdf', 'prepp', range(21, 46)),
    ('X', '2021-07-12', '12 Jul 2021 Shift-2', 'Prepp', 'prepp/Group_X_2021_12-Jul_S2.pdf', 'prepp_12jul', R25),
    ('X', '2021-07-13', '13 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_13-Jul_S1.pdf', 'prepp', range(21, 46)),
    ('X', '2021-07-13', '13 Jul 2021 Shift-2', 'Prepp', 'prepp/Group_X_2021_13-Jul_S2.pdf', 'prepp', R25),
    ('X', '2021-07-14', '14 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_14-Jul_S1.pdf', 'prepp', R25),
    ('X', '2021-07-14', '14 Jul 2021 Shift-3', 'Prepp', 'prepp/Group_X_2021_14-Jul_S3.pdf', 'prepp', R25),
    ('X', '2021-07-15', '15 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_15-Jul_S1.pdf', 'prepp', R25),
    ('X', '2021-07-15', '15 Jul 2021 Shift-3', 'Prepp', 'prepp/Group_X_2021_15-Jul_S3.pdf', 'prepp', R25),
    ('X', '2021-07-18', '18 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_18-Jul_S1.pdf', 'prepp', R25),
    ('X', '2021-07-18', '18 Jul 2021 Shift-3', 'Prepp', 'prepp/Group_X_2021_18-Jul_S3.pdf', 'prepp', R25),
    ('X', '2024-03-17', '17 Mar 2024 Shift-1', 'Utkarsh', 'utkarsh/Group_X_2024_17-Mar_Shift-1.pdf', 'utkarsh_x', R25),
    ('X', '2025-09-25', '25 Sep 2025', 'Utkarsh', 'utkarsh/Group_X_2025_25-Sep_Shift-A.pdf', 'utkarsh_x', R25),
    ('X', '2025-09-27', '27 Sep 2025', 'Utkarsh', 'utkarsh/Group_X_2025_27-Sep.pdf', 'utkarsh_x', R25),
    ('XY', '2026-03-30', '30 Mar 2026', 'Utkarsh', 'utkarsh/Group_XY_2026_30-Mar_OtherThanScience.pdf', 'utkarsh_xy', R25),
    ('XY', '2024-11-16', '16 Nov 2024', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_16_Nov_2024_Fresh_Verified.txt', 'user_txt', R25),
    ('XY', '2025-03-22', '22 Mar 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_22_Mar_2025_All_Questions.txt', 'user_txt', R25),
    ('XY', '2025-09-25', '25 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_25_Sep_2025_Fresh_Verified.txt', 'user_txt', R25),
    ('XY', '2025-09-26', '26 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_26_Sep_2025_Fresh_Verified.txt', 'user_txt', R25),
    ('XY', '2025-09-27', '27 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_27_Sep_2025_Fresh_Verified.txt', 'user_txt', R25),
    ('XY', '2025-09-28', '28 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_28_Sep_2025_Fresh_Verified.txt', 'user_txt', R25),
    ('XY', 'MODEL', 'Official XY Model Paper 2', 'PW Model', 'model_papers/PW_GroupXY_Official_Model_Paper_2.pdf', 'pw2', R25),
    ('X', 'MODEL', 'Sample Physics Paper', 'Prepp Sample', 'prepp/Sample_X_Physics.pdf', 'sample', R25),
]

extractors = {
    'selfstudys': extract_selfstudys,
    'prepp': extract_prepp,
    'prepp_12jul': extract_prepp_12jul,
    'utkarsh_x': extract_utkarsh_x,
    'utkarsh_xy': lambda p, r: extract_utkarsh_xy(p, 'Section : Physics', 'Section : Mathematics', r),
    'user_txt': extract_user_txt,
    'pw2': extract_pw_model2,
    'sample': extract_sample_physics,
}

MANUAL = {
    ('04 Nov 2020', 'SelfStudys', 14): _q(
        "Which of the following expressions represents the energy stored in a stretched wire? (Y = Young's modulus, S = strain)",
        ["1/2 Y S²", "Y S²", "3/2 Y S²", "1/4 Y S²"], "A"),
    ('16 Nov 2024', 'SelfStudys', 9): _q(
        "An AC current is expressed as i = 50 sin 100 t A. What is the half-cycle average value of that current?",
        ["50/π A", "50 A", "100 A", "100/π A"], "D"),
    ('25 Jul 2022', 'SelfStudys', 14): _q(
        "For two parallel wires, separation d carrying current Ia and Ib in the same direction will have the force on a length of L of either wire is",
        ["μ0 L Ia Ib / 2πd — Repulsion", "μ0 L Ia Ib / 2πd — Attraction",
         "μ0 L Ia Ib / πd — Repulsion", "μ0 L Ia Ib / πd — Attraction"], "D"),
    ('22 Mar 2025', 'SelfStudys', 18): _q(
        "Velocity at mean position of a particle executing S.H.M. is v, then velocity of the particle at a distance equal to half of the amplitude;",
        ["4v", "2v", "(√3/2) v", "(√3/4) v"], "C"),
    ('18 Jan 2023', 'SelfStudys', 6): _q(
        "Variation of acceleration due to gravity (g) with distance x from the centre of the earth is best represented by (R → Radius of the earth)",
        ["[Diagram A]", "[Diagram B]", "[Diagram C]", "[Diagram D]"], "D"),
    ('19 Jan 2023', 'SelfStudys', 23): _q(
        "If the refractive index of water is 4/3 and that of glass is 5/3, then the critical angle of incidence for light tending to go from glass to water is:",
        ["sin⁻¹(3/4)", "sin⁻¹(3/5)", "sin⁻¹(4/5)", "sin⁻¹(2/3)"], "C"),
    ('Official XY Model Paper 2', 'PW Model', 9): _q(
        "The radius of gyration of a solid sphere of radius r about a certain axis is r. Find the distance of this axis from the centre of the sphere.",
        ["r", "0.5 r", "√0.4 r", "√0.2 r"], "C"),
    ('Official XY Model Paper 2', 'PW Model', 10): _q(
        "Which of the following statements is correct, in case of adiabatic expansion?",
        ["ΔU = 0", "ΔU = negative", "ΔU = positive", "ΔU = ΔW"], "B"),
    ('Official XY Model Paper 2', 'PW Model', 14): _q(
        "If the threshold wavelength for photoelectric effect on sodium metal is 5000 Å, then find its work function.",
        ["15 J", "4 × 10⁻¹⁹ J", "4 × 10⁻¹⁴ J", "4 × 10⁻²² J"], "B"),
    ('Official XY Model Paper 2', 'PW Model', 16): _q(
        "What is the wavelength range of visible light?",
        ["4×10⁻⁷ m − 8×10⁻⁷ m", "4×10⁻⁶ m − 8×10⁻⁸ m", "4×10⁻⁵ m − 8×10⁻⁹ m", "4×10¹⁰ m − 8×10¹⁰ m"], "A"),
    ('Official XY Model Paper 2', 'PW Model', 17): _q(
        "What is the dimensional formula for the universal gravitational constant?",
        ["M⁻¹L³T⁻²", "M⁻¹L³T⁻¹", "M⁻¹L²T⁻²", "M⁰L⁰T⁰"], "A"),
    ('Official XY Model Paper 2', 'PW Model', 18): _q(
        "Two balls are dropped from heights h and 2h respectively. What would be the ratio of times taken by the balls to reach the earth?",
        ["√2 : 1", "1 : √2", "2 : 1", "4 : 119"], "B"),
    ('Sample Physics Paper', 'Prepp Sample', 9): _q(
        "The radius of gyration of a solid sphere of radius r about a certain axis is r. Find the distance of this axis from the centre of the sphere.",
        ["r", "0.5 r", "√0.4 r", "√0.2 r"], "C"),
    ('Sample Physics Paper', 'Prepp Sample', 10): _q(
        "Which of the following statements is correct, in case of adiabatic expansion?",
        ["ΔU = 0", "ΔU = negative", "ΔU = positive", "ΔU = ΔW"], "B"),
    ('Sample Physics Paper', 'Prepp Sample', 14): _q(
        "If the threshold wavelength for photoelectric effect on sodium metal is 5000 Å, then find its work function.",
        ["15 J", "4 × 10⁻¹⁹ J", "4 × 10⁻¹⁴ J", "4 × 10⁻²² J"], "B"),
    ('Sample Physics Paper', 'Prepp Sample', 16): _q(
        "What is the wavelength range of visible light?",
        ["4×10⁻⁷ m − 8×10⁻⁷ m", "4×10⁻⁶ m − 8×10⁻⁸ m", "4×10⁻⁵ m − 8×10⁻⁹ m", "4×10¹⁰ m − 8×10¹⁰ m"], "A"),
    ('Sample Physics Paper', 'Prepp Sample', 17): _q(
        "What is the dimensional formula for the universal gravitational constant?",
        ["M⁻¹L³T⁻²", "M⁻¹L³T⁻¹", "M⁻¹L²T⁻²", "M⁰L⁰T⁰"], "A"),
    ('Sample Physics Paper', 'Prepp Sample', 18): _q(
        "Two balls are dropped from heights h and 2h respectively. What would be the ratio of times taken by the balls to reach the earth?",
        ["√2 : 1", "1 : √2", "2 : 1", "4 : 119"], "B"),
    ('Official XY Model Paper 2', 'PW Model', 25): _q(
        "In gases of diatomic molecules, Find the ratio of the two specific heat of gases.",
        ["1.66", "1.33", "1.4", "1.00"], "C"),
    ('Sample Physics Paper', 'Prepp Sample', 4): _q(
        "What is the angle of dip at magnetic poles of earth?",
        ["Zero", "45°", "90°", "180°"], "C"),
    ('Sample Physics Paper', 'Prepp Sample', 20): _q(
        "At what temperature, will the surface tension of water, be minimum?",
        ["0°C", "25°C", "60°C", "75°C"], "D"),
    ('06 Nov 2020', 'Prepp', 21): _q(
        "The angle between two vectors A⃗ and B⃗ is given by-",
        ["cos θ = (A⃗·B⃗) / (2|A⃗||B⃗|)", "tan θ = (A⃗·B⃗) / (|A⃗||B⃗|)",
         "sin θ = (A⃗·B⃗) / (|A⃗||B⃗|)", "cos θ = (A⃗·B⃗) / (|A⃗||B⃗|)"], "D"),
    ('07 Nov 2020', 'Prepp', 19): _q(
        "विद्युत चुम्बकीय तरंग गति (c), मुक्त स्थान का परावैद्युतांक (ϵ0) और मुक्त स्थान की पारगम्यता (μ0) के बीच सही संबंध चुनिये-",
        ["c = √(μ0/ϵ0)", "c = 1/(ϵ0 μ0)", "c = √(ϵ0/μ0)", "c = 1/√(ϵ0 μ0)"], "D"),
    ('13 Jul 2021 Shift-1', 'Prepp', 22): _q(
        "The electrical resistivity of the material of a conductor is ρ. If the resistance and volume of the conductor is 3 Ω and 3 m³, then find the length of the conductor.",
        ["l = 1/√(3ρ)", "l = √ρ/3", "l = 3/√ρ", "l = 3√ρ"], "C"),
    ('14 Jul 2021 Shift-1', 'Prepp', 1): _q(
        "The relation between the electric field and the magnetic field is",
        ["μoϵo", "1 / μoϵo", "1 / √(μoϵo)", "√(μoϵo)"], "C"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 18): _q(
        "Magnetic field due to the current carrying wire as shown in the figure at point \"O\" will be:",
        ["μ₀I/2R", "μ₀I/4R", "μ₀I/2πR", "μ₀I/4πR"], "A"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 12): _q(
        "If the three similar charges of magnitude +Q are placed on the vertices of an equilateral triangle of side x, then the total work done required to arrange the system will be:",
        ["Q² / 4πε₀x", "3Q² / 4πε₀x", "2Q² / 4πε₀x", "Q² / πε₀x"], "B"),
    ('25 Sep 2025', 'Utkarsh', 2): _q(
        "The relationship between the magnetic susceptibility (χ) and the magnetic permeability (μ) is given by: (μ₀ is the permeability of free space and μᵣ is relative permeability)",
        ["χ = μ/μ₀ − 1", "χ = μᵣ/μ₀ + 1", "χ = (−b ± √(b² − 4ac)) / 2a", "χ = 1 − μ/μ₀"], "A"),
    ('25 Sep 2025', 'Utkarsh', 9): _q(
        "E⃗ and k⃗ represent electric field and propagation vectors of the EM waves in vacuum, then magnetic field vector is given by: (ω - angular frequency):",
        ["ω (E⃗ × K⃗)", "ω (K⃗ × E⃗)", "E⃗ × K⃗", "(1/ω) (K⃗ × E⃗)"], "D"),
}

# Utkarsh 17-Mar: answer markers lost in OCR for these; physically certain answers filled.
ANS_OVERRIDES = {
    ('17 Mar 2024 Shift-1', 'Utkarsh', 10): 'D',
    ('17 Mar 2024 Shift-1', 'Utkarsh', 11): 'A',
    ('17 Mar 2024 Shift-1', 'Utkarsh', 17): 'A',
    ('17 Mar 2024 Shift-1', 'Utkarsh', 18): 'A',  # full circular loop -> B = μ0I/2R (figure verified: closed ring)
    ('17 Mar 2024 Shift-1', 'Utkarsh', 20): 'B',
    ('Official XY Model Paper 2', 'PW Model', 24): 'B',  # printed key says A; physics + Prepp key both give B (blue λ < red λ → RP ↑)
}

def main():
    results = []
    for grp, key, label, src, rel, kind, qrange in papers:
        path = os.path.join(AG, rel)
        if not os.path.exists(path):
            results.append({'grp': grp, 'key': key, 'label': label, 'src': src, 'qs': None, 'err': 'FILE MISSING'})
            continue
        try:
            qs = extractors[kind](path, qrange)
            for i, q in enumerate(qs, 1):
                ov = MANUAL.get((label, src, i))
                if ov and q is not None:
                    qs[i - 1] = ov
                ao = ANS_OVERRIDES.get((label, src, i))
                if ao and q is not None:
                    q['ans'] = ao
            # clean leftover symbol glyphs (PUA) on non-manual entries
            for q in qs:
                if q is None or 'raw' in q:
                    continue
                q['q'] = _clean_sym(q.get('q') or '')
                q['opts'] = [_clean_sym(o) for o in (q.get('opts') or [])]
            results.append({'grp': grp, 'key': key, 'label': label, 'src': src, 'qs': qs, 'err': ''})
        except Exception as ex:
            results.append({'grp': grp, 'key': key, 'label': label, 'src': src, 'qs': None, 'err': str(ex)})
    json.dump(results, open('/home/user/_phys_raw.json', 'w'), ensure_ascii=False, indent=1)
    print("PAPER                              GROUP  SOURCE       EXTRACTED")
    for r in results:
        qs = r['qs']
        cnt = sum(1 for x in (qs or []) if x is not None) if qs else 0
        total = len(qs) if qs else 0
        flag = ('  <-- ' + r['err']) if r['err'] else ''
        print(f"{r['label']:32s}  {r['grp']:5s}  {r['src']:12s}  {cnt}/{total}{flag}")
    return results

if __name__ == '__main__':
    main()
