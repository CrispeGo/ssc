# -*- coding: utf-8 -*-
"""Extract ALL English questions from every Agniveer Vayu paper source (v4 final).
   Builds Master_English_All_Papers.txt (mirrors Master_Math_All_Papers.txt)."""
import pymupdf, re, os, json

ROOT = "/home/user/agniveer"
OUT = os.path.join(ROOT, "Master_English_All_Papers.txt")
DBG = "/home/user/pdf_build/english_raw.json"

def pdf_text(path):
    d = pymupdf.open(path)
    return "\n".join(p.get_text() for p in d).replace("\xa0", " ")

def clean(s):
    s = s.replace("\u200b", "").replace("\ufeff", "").replace("\u200c", "").replace("\u200d", "")
    return re.sub(r"\s+", " ", s).strip()

ENGLISH_KW = ["synonym","antonym","spell","spelt","voice","direct speech","indirect",
              "noun form","adjective form","verb form","adverb form","preposition",
              "one word","substitute","passage","idiom","phrase","opposite","similar",
              "segment","error","fill in the","collective noun","jumbled","narration",
              "misspelled","article","opposite in meaning"]

def is_english(q):
    ql = q.lower()
    return any(k in ql for k in ENGLISH_KW)

# ============================================================ SELFSTUDYS
def parse_selfstudys(path, group):
    full = pdf_text(path)
    i = full.find("English")
    if i < 0:
        return []
    seg = full[i:]
    qs = []
    parts = re.split(r"Question\s+(\d+)\s*\n", seg)
    for k in range(1, len(parts), 2):
        num = int(parts[k]); blk = parts[k+1] if k+1 < len(parts) else ""
        m = re.search(r"Options:\s*\n", blk)
        if not m:
            continue
        qtext = clean(blk[:m.start()])
        rest = blk[m.end():]
        om = re.search(r"A\.\s*(.*?)\nB\.\s*(.*?)\nC\.\s*(.*?)\nD\.\s*(.*?)\n", rest, re.S)
        if not om:
            continue
        opts = [clean(om.group(i)) for i in (1,2,3,4)]
        am = re.search(r"Answer:\s*([A-Da-d])", rest)
        qs.append((num, qtext, opts, am.group(1).upper() if am else "?"))
    if group == "Y":
        qs = [x for x in qs if x[0] <= 20]
    else:
        hi = [x for x in qs if x[0] >= 51]
        if hi:
            qs = hi
    return [(q, o, a) for (n, q, o, a) in qs]

# ============================================================ UTKARSH
def _utkarsh_blocks(seg):
    out = []
    parts = re.split(r"\n(\d+)\.?\s*\n", "\n"+seg)
    for k in range(1, len(parts), 2):
        n = int(parts[k]); blk = parts[k+1] if k+1 < len(parts) else ""
        om = re.match(r"\s*(.*?)\n\s*\(a\)\s*(.*?)\n\s*\(b\)\s*(.*?)\n\s*\(c\)\s*(.*?)\n\s*\(d\)\s*(.*?)\s*\[([a-d])\]", blk, re.S)
        if not om:
            continue
        q = clean(om.group(1)); opts = [clean(om.group(i)) for i in (2,3,4,5)]
        out.append((n, q, opts, om.group(6).upper()))
    return out

def parse_utkarsh(path):
    full = pdf_text(path)
    qs = _utkarsh_blocks(full)
    if any(x[0] >= 51 for x in qs):
        # Group X: English is the last section (Q51-70)
        qs = [x for x in qs if x[0] >= 51]
    else:
        # Group Y: English is the first section (Q1-20); stop once GA begins
        res = []
        for x in qs:
            if x[0] > 20:
                break
            res.append(x)
        qs = res
    return [(q, o, a) for (n, q, o, a) in qs]

def parse_utkarsh_section(path):
    full = pdf_text(path)
    secs = [(m.start(), m.group(1).strip()) for m in re.finditer(r"Section\s*:\s*([^\n]+)", full)]
    names = [s[1].lower() for s in secs]
    if "english" not in names:
        return []
    idx = names.index("english")
    start = secs[idx][0]
    end = secs[idx+1][0] if idx+1 < len(secs) else len(full)
    seg = full[start:end]
    out = []
    parts = re.split(r"\n(\d+)\.\s{1,}", "\n"+seg)
    for k in range(1, len(parts), 2):
        blk = parts[k+1] if k+1 < len(parts) else ""
        om = re.match(r"\s*(.*?)\n\s*\(a\)\s*(.*?)\n\s*\(b\)\s*(.*?)\n\s*\(c\)\s*(.*?)\n\s*\(d\)\s*(.*?)\s*\[([a-d])\]", blk, re.S)
        if not om:
            continue
        out.append((clean(om.group(1)), [clean(om.group(i)) for i in (2,3,4,5)], om.group(6).upper()))
    return out

# ============================================================ PW MODELS (questions + separate Answer Key table)
def _pw_key(full):
    key = {}
    km = re.search(r"Answer\s*Key", full)
    if km:
        kseg = full[km.end():km.end()+4000]
        for m in re.finditer(r"Q(\d+)\s*\n\s*\(?([A-D])\)?", kseg):
            key[int(m.group(1))] = m.group(2).upper()
        for m in re.finditer(r"Q(\d+)\s+\(([A-D])\)", kseg):
            key[int(m.group(1))] = m.group(2).upper()
    return key

def parse_pw_model(path, limit=20):
    full = pdf_text(path)
    key = _pw_key(full)
    out = []
    parts = re.split(r"\nQ\s*(\d+)\s*\n", "\n"+full)
    for k in range(1, len(parts), 2):
        num = int(parts[k]); blk = parts[k+1] if k+1 < len(parts) else ""
        if num > limit:
            continue
        om = re.match(r"\s*(.*?)\n\(A\)\s*(.*?)\n\(B\)\s*(.*?)\n\(C\)\s*(.*?)\n\(D\)\s*(.*?)(?:\n|$)", blk, re.S)
        if not om:
            continue
        q = clean(om.group(1)); opts = [clean(om.group(i)) for i in (2,3,4,5)]
        out.append((num, q, opts, key.get(num, "?")))
    seen = set(); res = []
    for n, q, o, a in out:
        kk = (q, tuple(o))
        if kk in seen:
            continue
        seen.add(kk)
        res.append((q, o, a))
    return res

# ============================================================ PREPP
def _prepp_que_blocks(text):
    out = []
    for m in re.finditer(r"Que\.\s*(\d+)\s*\n", text):
        n = int(m.group(1)); s = m.end()
        nxt = re.search(r"Que\.\s*\d+\s*\n", text[s:])
        body = (text[s : s + nxt.start()] if nxt else text[s:]).split("\n")
        # drop "Solution" labels and solution-answer lines
        body = [ln for ln in body if not ln.strip().startswith("Solution")]
        inline = None
        for i, ln in enumerate(body):
            mm = re.match(r"^\s*Correct Option\s*-\s*(\d+)\s*$", ln)
            if mm:
                inline = int(mm.group(1)); body[i] = ""
        try:
            i1 = body.index("1.")
        except ValueError:
            continue
        if i1+3 < len(body) and body[i1+1].strip() == "2." and body[i1+2].strip() == "3." and body[i1+3].strip() == "4.":
            # layout B: option texts listed first, then 1.-4. markers
            opts = [clean(body[i1-4]), clean(body[i1-3]), clean(body[i1-2]), clean(body[i1-1])]
            qlines = [x for x in body[:i1-4] if x.strip()]
        else:
            # layout A: option text on the line above its number marker
            i2 = body.index("2.", i1+1); i3 = body.index("3.", i2+1); i4 = body.index("4.", i3+1)
            opts = [clean(body[i1-1]), clean(body[i2-1]), clean(body[i3-1]), clean(body[i4-1])]
            try:
                i5 = body.index("5.", i4+1)
                opts.append(clean(body[i5-1]))
            except ValueError:
                pass
            qlines = [x for x in body[:i1-1] if x.strip()]
        qtext = clean(" ".join(qlines))
        out.append((n, qtext, opts, inline))
    return out

def _prepp_key(text):
    key = {}
    # style A (2020): trailing "Que. N / Correct Option - M" table
    for m in re.finditer(r"Que\.\s*(\d+)\s*\n\s*Correct Option\s*-\s*(\d+)", text):
        key[int(m.group(1))] = "ABCD"[int(m.group(2))-1]
    if key:
        return key
    # style B: "Solution Correct Option - M" lines (dense papers print them in
    # question order; sparse papers print them inline after their own question)
    sols = re.findall(r"Solution Correct Option\s*-\s*(\d+)", text)
    ques = [int(x) for x in re.findall(r"Que\.\s*(\d+)\s*\n", text)]
    if len(sols) == len(ques) and sols:
        for i, s in enumerate(sols):
            key[ques[i]] = "ABCD"[int(s)-1]
    else:
        cur = None
        for m in re.finditer(r"Que\.\s*(\d+)\s*\n|Solution Correct Option\s*-\s*(\d+)", text):
            if m.group(1) is not None:
                cur = int(m.group(1))
            elif cur is not None:
                key[cur] = "ABCD"[int(m.group(2))-1]
    return key

def parse_prepp(path, group):
    text = pdf_text(ROOT+"/prepp/"+path)
    blocks = _prepp_que_blocks(text)
    key = _prepp_key(text)
    def score(rng):
        return sum(1 for n, q, o, inc in blocks if rng[0] <= n <= rng[1] and is_english(q))
    if group == "Y":
        rng = (1, 20)
        if score(rng) < 8:
            return []
    else:
        s1 = score((1, 20)); s2 = score((51, 70))
        if max(s1, s2) < 8:
            return []
        rng = (1, 20) if s1 >= s2 else (51, 70)
    out = []
    for n, q, o, inc in blocks:
        if rng[0] <= n <= rng[1]:
            ans = "ABCDE"[inc-1] if inc else key.get(n, "?")
            out.append((q, o, ans))
    return out

# ============================================================ SAMPLE X ENGLISH
def parse_sample(path):
    t = pdf_text(path)
    segs = re.split(r"Ans\s*:\s*([A-Da-d])", t)
    out = []
    for k in range(1, len(segs), 2):
        seg = segs[k-1]; ans = segs[k].upper()
        m = re.search(r"Q\.(\d+)\.", seg)
        if not m:
            continue
        num = int(m.group(1))
        pre = seg[:m.start()].strip()
        post = seg[m.end():]
        stem_pre = ""
        if num > 1 and pre:
            stem_pre = " ".join(x.strip() for x in pre.split("\n") if x.strip())
        om = re.match(r"\s*(.*?)\s*\(A\)\s*(.*?)\s*\(B\)\s*(.*?)\s*\(C\)\s*(.*?)\s*\(D\)\s*(.*?)\Z", post, re.S)
        if not om:
            # error-spotting style (Q16-18): sentence + inline A-D labels, no option letters
            q = clean((stem_pre + " " + clean(post)).strip())
            out.append((q, [], ans))
            continue
        q = clean((stem_pre + " " + clean(om.group(1))).strip())
        opts = [clean(om.group(i)) for i in (2,3,4,5)]
        out.append((q, opts, ans))
    return out

# ============================================================ ALLEXAMPYQS (Que. N blocks, inline "Correct Option - M", English = first 20)
def parse_alx(path):
    text = pdf_text(ROOT+"/allexampyqs/"+path)
    out = []
    for m in re.finditer(r"Que\.\s*(\d+)\s*\n", text):
        n = int(m.group(1)); s = m.end()
        if not (1 <= n <= 20):
            continue
        nxt = re.search(r"Que\.\s*\d+\s*\n", text[s:])
        blk = text[s : s + nxt.start()] if nxt else text[s:]
        cos = list(re.finditer(r"Correct Option\s*-\s*(\d+)", blk))
        if not cos:
            continue
        if len(cos) == 1:
            lines = [ln for ln in blk.split("\n") if not ln.strip().startswith("Correct Option")]
            try:
                i1 = lines.index("1."); i2 = lines.index("2.", i1+1); i3 = lines.index("3.", i2+1); i4 = lines.index("4.", i3+1)
            except ValueError:
                continue
            opts = [clean(lines[i1-1]), clean(lines[i2-1]), clean(lines[i3-1]), clean(lines[i4-1])]
            q = clean(" ".join(x.strip() for x in lines[:i1-1] if x.strip()))
            out.append((q, opts, "ABCD"[int(cos[0].group(1))-1]))
        else:
            for ci, co in enumerate(cos):
                sub_end = cos[ci+1].start() if ci+1 < len(cos) else len(blk)
                sub = [ln for ln in blk[co.end():sub_end].split("\n") if not ln.strip().startswith("Correct Option")]
                try:
                    i1 = sub.index("1."); i2 = sub.index("2.", i1+1); i3 = sub.index("3.", i2+1); i4 = sub.index("4.", i3+1)
                except ValueError:
                    continue
                opts = [clean(sub[i1-1]), clean(sub[i2-1]), clean(sub[i3-1]), clean(sub[i4-1])]
                if ci == 0:
                    stem = blk[:co.start()]
                else:
                    prev_sub = [ln for ln in blk[cos[ci-1].end():co.start()].split("\n") if not ln.strip().startswith("Correct Option")]
                    try:
                        p4 = prev_sub.index("4.")
                    except ValueError:
                        p4 = -1
                    stem = "\n".join(prev_sub[p4+1:])
                q = clean(stem + " " + " ".join(x.strip() for x in sub[:i1-1] if x.strip()))
                out.append((q, opts, "ABCD"[int(co.group(1))-1]))
    return out

# ============================================================ USER TXT
def parse_text_english(text, qmin, qmax):
    lines = text.replace("\xa0", " ").split("\n")
    marks = []
    for idx, ln in enumerate(lines):
        m = re.match(r"^Q\.?\s*(\d+)\s*[\.\s]?\s*(.*)$", ln)
        if m:
            num = int(m.group(1))
            if qmin <= num <= qmax:
                marks.append((num, idx, m.group(2).strip()))
    out = []
    for k in range(len(marks)):
        num, i, rest = marks[k]
        jend = marks[k+1][1] if k+1 < len(marks) else len(lines)
        body = lines[i+1:jend]
        opts = None; qtext = None
        for b, ln in enumerate(body):
            s = ln.strip()
            if re.match(r"^1\.\s*\S", s):
                if b+3 < len(body) and all(re.match(r"^%d\.\s*\S" % w, body[b+o].strip()) for o, w in enumerate([2,3,4], 1)):
                    opts = [clean(re.sub(r"^%d\.\s*" % w, "", body[b+o].strip())) for o, w in enumerate([1,2,3,4])]
                    qtext = clean(rest + " " + " ".join(x.strip() for x in body[:b] if x.strip()))
                break
            if s in ("1.","2.","3.","4."):
                try:
                    i1 = body.index("1."); i2 = body.index("2.", i1+1); i3 = body.index("3.", i2+1); i4 = body.index("4.", i3+1)
                    opts = [clean(body[i1-1]), clean(body[i2-1]), clean(body[i3-1]), clean(body[i4-1])]
                    qtext = clean(rest + " " + " ".join(x.strip() for x in body[:i1-1] if x.strip()))
                except ValueError:
                    opts = None
                break
        if opts and len(opts) == 4 and qtext:
            out.append((qtext, opts, "?"))
    return out

# ============================================================ build
papers = []
def add(group, sortkey, date, source, qs):
    papers.append({"group": group, "sk": sortkey, "date": date, "source": source, "qs": qs})

fx = [("Group_X_2020_04-Nov.pdf","2020-11-04","04 Nov 2020"),
      ("Group_X_2021_18-Jul.pdf","2021-07-18","18 Jul 2021"),
      ("Group_X_2022_25-Jul.pdf","2022-07-25","25 Jul 2022"),
      ("Group_X_2023_18-Jan.pdf","2023-01-18","18 Jan 2023"),
      ("Group_X_2023_19-Jan.pdf","2023-01-19","19 Jan 2023"),
      ("Group_X_2023_13-Oct_Shift-1.pdf","2023-10-13","13 Oct 2023 Shift-1"),
      ("Group_X_2023_14-Oct_Shift-1.pdf","2023-10-14","14 Oct 2023 Shift-1"),
      ("Group_X_2024_16-Nov.pdf","2024-11-16","16 Nov 2024"),
      ("Group_X_2025_22-Mar.pdf","2025-03-22","22 Mar 2025")]
fy = [("Group_Y_2021_13-Jul.pdf","2021-07-13","13 Jul 2021"),
      ("Group_Y_2022_24-Jul.pdf","2022-07-24","24 Jul 2022"),
      ("Group_Y_2022_25-Jul.pdf","2022-07-25","25 Jul 2022"),
      ("Group_Y_2022_27-Jul.pdf","2022-07-27","27 Jul 2022"),
      ("Group_Y_2023_18-Jan.pdf","2023-01-18","18 Jan 2023"),
      ("Group_Y_2023_19-Jan.pdf","2023-01-19","19 Jan 2023"),
      ("Group_Y_2023_20-Jan.pdf","2023-01-20","20 Jan 2023"),
      ("Group_Y_2023_13-Oct_Shift-1.pdf","2023-10-13","13 Oct 2023 Shift-1"),
      ("Group_Y_2023_13-Oct_Shift-2.pdf","2023-10-13","13 Oct 2023 Shift-2"),
      ("Group_Y_2023_14-Oct.pdf","2023-10-14","14 Oct 2023"),
      ("Group_Y_2025_22-Mar.pdf","2025-03-22","22 Mar 2025")]
for f, sk, d in fx:
    add("X", sk, d, "SelfStudys", parse_selfstudys(ROOT+"/"+f, "X"))
for f, sk, d in fy:
    add("Y", sk, d, "SelfStudys", parse_selfstudys(ROOT+"/"+f, "Y"))

utk = [("utkarsh/Group_X_2024_17-Mar_Shift-1.pdf","X","2024-03-17","17 Mar 2024 Shift-1", None),
       ("utkarsh/Group_X_2025_25-Sep_Shift-A.pdf","X","2025-09-25","25 Sep 2025 Shift-A", None),
       ("utkarsh/Group_X_2025_27-Sep.pdf","X","2025-09-27","27 Sep 2025", None),
       ("utkarsh/Group_Y_2025_28-Sep.pdf","Y","2025-09-28","28 Sep 2025", None),
       ("utkarsh/Group_Y_2026_31-Mar_Shift-1.pdf","Y","2026-03-31","31 Mar 2026 Shift-1", None),
       ("utkarsh/Group_Y_2026_31-Mar_Shift-2.pdf","Y","2026-03-31","31 Mar 2026 Shift-2", None),
       ("utkarsh/Group_XY_2026_30-Mar_OtherThanScience.pdf","XY","2026-03-30","30 Mar 2026 (Other than Science)", parse_utkarsh_section)]
for f, g, sk, d, custom in utk:
    qs = custom(ROOT+"/"+f) if custom else parse_utkarsh(ROOT+"/"+f)
    add(g, sk, d, "Utkarsh", qs)

add("XY", "MODEL-1", "Official Model Paper 1 (English)", "PW Model",
    parse_pw_model(ROOT+"/model_papers/PW_GroupXY_Official_Model_Paper_1.pdf", 25))
add("Y", "2022-07-24", "24 Jul 2022", "PW Model",
    parse_pw_model(ROOT+"/model_papers/PW_GroupY_24Jul2022.pdf", 20))

utxt = [("user_txt/Agniveer_Vayu_Group_XY_16_Nov_2024_Fresh_Verified.txt","2024-11-16","16 Nov 2024"),
        ("user_txt/Agniveer_Vayu_Group_XY_22_Mar_2025_All_Questions.txt","2025-03-22","22 Mar 2025"),
        ("user_txt/Agniveer_Vayu_Group_XY_25_Sep_2025_Fresh_Verified.txt","2025-09-25","25 Sep 2025"),
        ("user_txt/Agniveer_Vayu_Group_XY_26_Sep_2025_Fresh_Verified.txt","2025-09-26","26 Sep 2025"),
        ("user_txt/Agniveer_Vayu_Group_XY_27_Sep_2025_Fresh_Verified.txt","2025-09-27","27 Sep 2025"),
        ("user_txt/Agniveer_Vayu_Group_XY_28_Sep_2025_Fresh_Verified.txt","2025-09-28","28 Sep 2025")]
for f, sk, d in utxt:
    t = open(ROOT+"/"+f, encoding="utf-8").read()
    add("XY", sk, d, "User TXT", parse_text_english(t, 51, 70))

fxp = [("Group_X_2020_04-Nov.pdf","2020-11-04","04 Nov 2020"),
       ("Group_X_2020_05-Nov.pdf","2020-11-05","05 Nov 2020"),
       ("Group_X_2020_06-Nov.pdf","2020-11-06","06 Nov 2020"),
       ("Group_X_2020_07-Nov.pdf","2020-11-07","07 Nov 2020"),
       ("Group_X_2021_12-Jul_S2.pdf","2021-07-12","12 Jul 2021 Shift-2"),
       ("Group_X_2021_13-Jul_S1.pdf","2021-07-13","13 Jul 2021 Shift-1"),
       ("Group_X_2021_13-Jul_S2.pdf","2021-07-13","13 Jul 2021 Shift-2"),
       ("Group_X_2021_14-Jul_S1.pdf","2021-07-14","14 Jul 2021 Shift-1"),
       ("Group_X_2021_14-Jul_S3.pdf","2021-07-14","14 Jul 2021 Shift-3"),
       ("Group_X_2021_15-Jul_S1.pdf","2021-07-15","15 Jul 2021 Shift-1"),
       ("Group_X_2021_15-Jul_S3.pdf","2021-07-15","15 Jul 2021 Shift-3"),
       ("Group_X_2021_18-Jul_S1.pdf","2021-07-18","18 Jul 2021 Shift-1"),
       ("Group_X_2021_18-Jul_S3.pdf","2021-07-18","18 Jul 2021 Shift-3")]
fyp = [("Group_Y_2020_04-Nov.pdf","2020-11-04","04 Nov 2020"),
       ("Group_Y_2020_05-Nov.pdf","2020-11-05","05 Nov 2020"),
       ("Group_Y_2020_06-Nov.pdf","2020-11-06","06 Nov 2020"),
       ("Group_Y_2020_07-Nov.pdf","2020-11-07","07 Nov 2020"),
       ("Group_Y_2021_12-Jul_S1.pdf","2021-07-12","12 Jul 2021 Shift-1"),
       ("Group_Y_2021_12-Jul_S2.pdf","2021-07-12","12 Jul 2021 Shift-2"),
       ("Group_Y_2021_13-Jul_S1.pdf","2021-07-13","13 Jul 2021 Shift-1"),
       ("Group_Y_2021_14-Jul_S3.pdf","2021-07-14","14 Jul 2021 Shift-3"),
       ("Group_Y_2021_15-Jul_S1.pdf","2021-07-15","15 Jul 2021 Shift-1"),
       ("Group_Y_2021_15-Jul_S2.pdf","2021-07-15","15 Jul 2021 Shift-2"),
       ("Group_Y_2021_15-Jul_S3.pdf","2021-07-15","15 Jul 2021 Shift-3"),
       ("Group_Y_2021_16-Jul_S2.pdf","2021-07-16","16 Jul 2021 Shift-2")]
for f, sk, d in fxp:
    add("X", sk, d, "Prepp", parse_prepp(f, "X"))
for f, sk, d in fyp:
    add("Y", sk, d, "Prepp", parse_prepp(f, "Y"))

add("X", "SAMPLE", "Sample English Paper", "Prepp Sample",
    parse_sample(ROOT+"/prepp/Sample_X_English.pdf"))

alx = [("Group_Y_2022_24-Jul_All-Shifts.pdf","2022-07-24","24 Jul 2022 (All Shifts)"),
       ("Group_Y_2022_25-Jul_All-Shifts.pdf","2022-07-25","25 Jul 2022 (All Shifts)"),
       ("Group_Y_2023_18-Jan_MB.pdf","2023-01-18","18 Jan 2023 (MB)"),
       ("Group_Y_2023_20-Jan_MB.pdf","2023-01-20","20 Jan 2023 (MB)")]
for f, sk, d in alx:
    add("Y", sk, d, "AllExamPYQs", parse_alx(f))

order = {"SelfStudys":0,"Prepp":1,"Utkarsh":2,"User TXT":3,"PW Model":4,"AllExamPYQs":5,"Prepp Sample":6}
papers.sort(key=lambda p: (p["sk"], order.get(p["source"], 9), p["group"]))

# ============================================================ write
R = "=" * 78
out = []
def w(s): out.append(s)
w(R)
w("AGNIVEER VAYU (AIR FORCE) — MASTER ENGLISH QUESTION BANK")
w("All English questions from ALL available papers (Group X + Group Y + Group XY + Model)")
w("Compiled: 13 September 2026")
w(R); w("")
w("NOTE: Questions are transcribed as printed in the source. Where a source")
w("carries an answer key, the answer is shown; user-uploaded TXTs contain no")
w("answer key (as provided). Memory-based papers may have minor wording")
w("variations and their answer keys may occasionally contain errors — they are")
w("reproduced as printed. The English section is common to Group X and Group Y,")
w("so papers of BOTH groups (plus Group XY and model papers) are included here.")
w("A few Prepp 2021 questions carry 'Answer: ?' where the source itself omits")
w("its 'Correct Option' annotation.")
w(""); w("-"*78); w("INVENTORY (papers included in this file)"); w("-"*78)
tot = keyed = 0
for p in papers:
    n = len(p["qs"]); k = sum(1 for q in p["qs"] if q[2] != "?")
    tot += n; keyed += k
    w("  {:<12s} | {:<3s} | {:<26s} | {:<12s} | English Qs: {}".format(
        p["sk"], p["group"], p["date"], p["source"], n))
w("  {:<12s} | {:<3s} | {:<26s} | {:<12s} | TOTAL English Qs: {} (keyed {})".format("", "", "", "", tot, keyed))
w("")
w("MISSING / EXCLUDED:")
w("  - PW_GroupXY_Official_Model_Paper_Eng.pdf — scanned image (no text layer).")
w("  - sscstudy/AirForce_Group_X_Y_PYQ_Book_263pg.pdf — scanned (no text layer).")
w("  - Prepp 07 Nov 2020 (X and Y) — question bodies are empty placeholders")
w("    in the source (answer-key only / Hindi-only content).")
w("  - Testbook-paid papers (e.g. X 18 Mar 2024) — not obtainable anywhere free.")
w(""); w(R)
pid = 0
for p in papers:
    pid += 1
    w(""); w("PAPER {}  |  GROUP {}  |  {}  |  Source: {}".format(pid, p["group"], p["date"], p["source"])); w(R)
    for qi, (q, opts, ans) in enumerate(p["qs"], 1):
        w("Q{}. {}".format(qi, q))
        for oi, o in enumerate(opts):
            w("   ({}) {}".format("ABCDE"[oi], o))
        w("   Answer: {}".format(ans))
        w("")
w(R); w("END OF ENGLISH QUESTION BANK"); w(R)
text = "\n".join(out) + "\n"
open(OUT, "w", encoding="utf-8").write(text)

json.dump([{"group":p["group"],"date":p["date"],"source":p["source"],
            "qs":[{"q":q,"opts":o,"ans":a} for q,o,a in p["qs"]]} for p in papers],
          open(DBG,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print("papers: {} | total Qs: {} | keyed: {}".format(len(papers), tot, keyed))
for p in papers:
    k = sum(1 for q in p["qs"] if q[2] != "?")
    print("  {:<3s} {:<26s} {:<12s} -> {} Qs (keyed {})".format(p["group"], p["date"], p["source"], len(p["qs"]), k))
