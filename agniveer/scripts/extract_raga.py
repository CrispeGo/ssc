# -*- coding: utf-8 -*-
"""Extract ALL RAGA (Reasoning & General Awareness) questions from every
   Agniveer Vayu paper source that carries a RAGA section.
   Builds Master_RAGA_All_Papers.txt (mirrors Master_English_All_Papers.txt).

   RAGA appears only in Group Y (non-science) and Group XY papers:
     - SelfStudys Group Y (root PDFs)  : RAGA = Question 21-50  (keyed, Options: A-D)
     - Prepp Group Y 2020 (04/05/06 Nov): RAGA = Que. 21-50      (keyed via trailing table)
     - Prepp Group Y 2021 (12-16 Jul)    : RAGA = Que. 21-50      (keyed inline)
     - Utkarsh Group Y                    : RAGA = 21-50          (keyed [a]-[d])
     - Utkarsh Group XY (Other than Science): RAGA section 1-30  (keyed [a]-[d])
     - Prepp Sample_X_RAGA               : 30 Qs, keyed "Ans: X" (bilingual; Hindi stripped)
"""
import pymupdf, re, os, json

ROOT = "/home/user/agniveer"
OUT = os.path.join(ROOT, "Master_RAGA_All_Papers.txt")
DBG = "/home/user/pdf_build/raga_raw.json"

def pdf_text(path):
    d = pymupdf.open(path)
    return "\n".join(p.get_text() for p in d).replace("\xa0", " ")

GLYPH = {"\uf0b8": "÷", "\uf0b4": "×", "\uf02b": "+", "\uf03d": "=", "\uf070": "π",
         "\uf0b1": "±", "\uf0a3": "≤", "\uf0b3": "≥", "\uf0d7": "×", "\uf0d6": "√"}
BRACKET_GLYPH = set("\uf0e9\uf0f9\uf0ea\uf0fa\uf0eb\uf0fb\uf0ec\uf0fc\uf0ed\uf0fd\uf0ee\uf0fe\uf0e6\uf0f6\uf0e7\uf0f7\uf0e8\uf0f8")

def clean(s):
    s = s.replace("\u200b", "").replace("\ufeff", "").replace("\u200c", "").replace("\u200d", "")
    for g, r in GLYPH.items():
        s = s.replace(g, r)
    s = "".join(ch for ch in s if ch not in BRACKET_GLYPH)
    s = s.replace("`", "₹")
    return re.sub(r"\s+", " ", s).strip()

# ============================================================ SELFSTUDYS (Group Y, RAGA = Q21-50)
def parse_selfstudys_raga(path):
    full = pdf_text(path)
    qs = []
    parts = re.split(r"Question\s+(\d+)\s*\n", full)
    for k in range(1, len(parts), 2):
        num = int(parts[k]); blk = parts[k+1] if k+1 < len(parts) else ""
        if not (21 <= num <= 50):
            continue
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
        ans = am.group(1).upper() if am else "?"
        fig = all(not o for o in opts)
        if fig:
            opts = []
        qs.append({"q": qtext, "opts": opts, "ans": ans, "fig": fig})
    return qs

# ============================================================ PREPP (Group Y, RAGA = Que. 21-50)
def _prepp_que_blocks(text, rng):
    out = []
    for m in re.finditer(r"Que\.\s*(\d+)\s*\n", text):
        n = int(m.group(1)); s = m.end()
        if not (rng[0] <= n <= rng[1]):
            continue
        nxt = re.search(r"Que\.\s*\d+\s*\n", text[s:])
        body = (text[s : s + nxt.start()] if nxt else text[s:]).split("\n")
        # capture inline key from both "Correct Option - N" and "Solution Correct Option - N"
        inline = None
        for i, ln in enumerate(body):
            mm = re.match(r"^\s*(?:Solution\s+)?Correct Option\s*-\s*(\d+)\s*$", ln)
            if mm:
                inline = int(mm.group(1)); body[i] = ""
        body = [ln for ln in body if not ln.strip().startswith("Solution")]
        # skip key-table rows / junk without any option marker
        if not any(ln.strip() in ("1.", "2.", "3.", "4.") for ln in body):
            continue
        # letter-prefixed option layout (shuffled options + letter map)
        pref = {}
        first_pref = None
        for i, ln in enumerate(body):
            m2 = re.match(r"^\s*([A-D])\.\s*(.+)$", ln)
            if m2 and m2.group(1) not in pref:
                pref[m2.group(1)] = m2.group(2).strip()
                if first_pref is None:
                    first_pref = i
        if len(pref) == 4:
            letters = [ln.strip() for ln in body if re.fullmatch(r"[A-D]", ln.strip())]
            shuf = letters[inline-1] if inline and 1 <= inline <= len(letters) else None
            stem_lines = [ln.strip() for ln in body[:first_pref] if ln.strip()]
            out.append({"n": n, "q": clean(" ".join(stem_lines)),
                        "opts": [pref["A"], pref["B"], pref["C"], pref["D"]],
                        "inline": inline, "fig": False, "shuf": shuf})
            continue
        has5 = any(ln.strip() == "5." for ln in body)
        body = ["" if ln.strip() in ("1.", "2.", "3.", "4.", "5.") else ln for ln in body]
        kept = [ln.strip() for ln in body if ln.strip()]
        K = 5 if has5 else 4
        if len(kept) <= K:
            qtext = clean(" ".join(kept))
            out.append({"n": n, "q": qtext, "opts": [], "inline": inline, "fig": True, "shuf": None})
            continue
        opt_texts = kept[-K:]
        stem_text = kept[:-K]
        if all(o in "ABCD" and len(o) == 1 for o in opt_texts):
            out.append({"n": n, "q": clean(" ".join(stem_text)), "opts": [],
                        "inline": inline, "fig": True, "shuf": None})
            continue
        out.append({"n": n, "q": clean(" ".join(stem_text)),
                    "opts": [clean(o) for o in opt_texts],
                    "inline": inline, "fig": False, "shuf": None})
    return out

def _prepp_key(text):
    key = {}
    for m in re.finditer(r"Que\.\s*(\d+)\s*\n\s*Correct Option\s*-\s*(\d+)", text):
        key[int(m.group(1))] = "ABCD"[(int(m.group(2))-1) % 4]
    if key:
        return key
    sols = re.findall(r"Solution Correct Option\s*-\s*(\d+)", text)
    ques = [int(x) for x in re.findall(r"Que\.\s*(\d+)\s*\n", text)]
    if len(sols) == len(ques) and sols:
        for i, s in enumerate(sols):
            key[ques[i]] = "ABCD"[(int(s)-1) % 4]
    else:
        cur = None
        for m in re.finditer(r"Que\.\s*(\d+)\s*\n|Solution Correct Option\s*-\s*(\d+)", text):
            if m.group(1) is not None:
                cur = int(m.group(1))
            elif cur is not None:
                key[cur] = "ABCD"[(int(m.group(2))-1) % 4]
    return key

def parse_prepp_raga(path):
    text = pdf_text(ROOT+"/prepp/"+path)
    blocks = _prepp_que_blocks(text, (21, 50))
    key = _prepp_key(text)
    out = []
    for d in blocks:
        if d["shuf"]:
            ans = d["shuf"]
        elif d["inline"]:
            ans = "ABCDE"[(d["inline"]-1) % 5]
        else:
            ans = key.get(d["n"], "?")
        if d["fig"] and not d["q"]:
            continue  # pure-figure question with no text at all
        out.append({"q": d["q"], "opts": d["opts"], "ans": ans, "fig": d["fig"]})
    return out

# ============================================================ UTKARSH (Group Y, RAGA = 21-50)
def _utkarsh_blocks(seg):
    # Line-by-line parser: question markers are number-only lines whose NEXT
    # non-empty line is real text (>=3 letters). Bare numbers inside maths
    # expressions / figure grids must not be mistaken for markers.
    lines = seg.split("\n")
    out = []
    i = 0
    nlines = len(lines)
    while i < nlines:
        m = re.fullmatch(r"(\d{1,2})[\.\s]{0,3}", lines[i])
        if m:
            num = int(m.group(1))
            j = i + 1
            while j < nlines and not lines[j].strip():
                j += 1
            if j < nlines and len(re.findall(r"[A-Za-z]", lines[j])) >= 3:
                e = i + 1
                key = None
                while e < nlines and e < i + 60:
                    km = re.search(r"\[([a-d])\]", lines[e])
                    if km:
                        key = km.group(1).upper(); break
                    e += 1
                if key:
                    blk = re.sub(r"\s*\[[a-d]\]\s*$", "", "\n".join(lines[i+1:e+1])).rstrip()
                    om = re.match(r"\s*(.*?)\n\s*\(a\)\s*(.*?)\n\s*\(b\)\s*(.*?)\n\s*\(c\)\s*(.*?)\n\s*\(d\)\s*(.*)\Z", blk, re.S)
                    if om:
                        q = clean(om.group(1))
                        opts = [clean(om.group(x)) for x in (2,3,4,5)]
                        fig = all(not o for o in opts)
                        out.append((num, q, [] if fig else opts, key, fig))
                    i = e + 1
                    continue
        i += 1
    return out

def parse_utkarsh_raga(path):
    full = pdf_text(ROOT+"/"+path)
    qs = _utkarsh_blocks(full)
    out = []
    for n, q, o, a, fig in qs:
        if 21 <= n <= 50:
            out.append({"q": q, "opts": o, "ans": a, "fig": fig})
    return out

def parse_utkarsh_section_raga(path):
    full = pdf_text(ROOT+"/"+path)
    secs = [(m.start(), m.group(1).strip()) for m in re.finditer(r"Section\s*:\s*([^\n]+)", full)]
    names = [s[1].lower() for s in secs]
    if "raga" not in names:
        return []
    idx = names.index("raga")
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
        q = clean(om.group(1)); opts = [clean(om.group(i)) for i in (2,3,4,5)]
        fig = all(not o for o in opts)
        out.append({"q": q, "opts": [] if fig else opts, "ans": om.group(6).upper(), "fig": fig})
    return out

# ============================================================ PREPP SAMPLE RAGA (bilingual, strip Hindi)
COMMON = set("""a an the of to in on for and or but nor if is are was were be been being am
do does did done have has had can could will would shall should may might must not no yes
it its this that these those he she they we you i your his her their our my me him them us
from with by at as than then so too very just now also only even still again here there
when where which who whom whose what how why all each every some any both few more most
many much such own same other another one two three four five between through during
before after against into onto out up down off away because while although though until
unless since about into over under above below find found value number total average sum
mean ratio difference between persons men days work complete select choose the following
given below answer option correct which following first second third next wrong odd one
out series code language means each other another who what when where how many much
capital currency known called also first president prime minister chief state national
india indian world largest smallest highest longest country countries water river sea
ocean mountain island city town village flag ratio length height width area perimeter
volume speed time distance train km kmph hour hours minute minutes day days year years
month months mark marks score scores exam examination student students answer answers
question questions increase decreases spend saves income expenditure saving savings per
cent percentage interest compound simple rate annum sum find evaluate solve direction
read information below follows sitting facing centre center position row left right
middle north south east west sits second immediate neighbour adjacent opposite place
places away between among relation related father mother brother sister daughter son
wife husband family pointing says she he his her my married age born died death year
money rs rupees kg litre meter cm km g grams kgs etc ie eg aproximately approx roughly
among executed controlled organisation motto famous folk dance terrorist searched killed
special task forces exclusive power grant pardon sentence case stations covers journey
returns whole observations later wrongly taken three numbers ratio finish remaining join
now take sum years smallest divided leaves remainder man spends income increases
expenditure increase savings missing table persons playing cards partners north whose
face towards south choose best alternative danger always involves evaluate venn diagrams
depicts relation doctors lawyers professionals waves used radar detecting presence
aircraft type complete odd language code execution guru sikh gurus was
""".split())
STARTERS = set("""which who what when where how why if the a an in on at by of for to
find evaluate solve complete select choose read study point direction danger distance
four three two five six seven eight nine ten a man in the total average sum ratio
difference identify statement statements given below in which of the who among""".split())

KRUTI = set("""maoM sao kao ka kI ko hO hOM qaa yaid tao AaOr va iksa iksaI ikna Wara
kUT BaaYaa Aqa krao kIijae maana jaata inamna dUrI caala ikmaI GaNTa AaOsat
BaUima ikyaa hotu kroM pUNa caar taSa Kola rho dixaNa haogaa ivaklp kaOna saa
hmaoSaa haota AadmaI ApnaI Aaya Kca vaRiw bacat prIxaa sahI galat AMk p`aPt
Kaoyaa p`Sna hla ikyao sambanQa dSaa vaona AaroK inado Savaao cayana kaya bala
jaga idna kama krnao baad hO iksaka jaananao trMgaaoM p`yaaoga p`doSa laaokna
EaRMKlaa saM#yaa lauPt saarNaI""".split())

def _is_english_line(ln):
    s = ln.strip()
    if not s:
        return False
    if re.search(r"[~^@$\\#\[\]<>|\u0930-\u097F]", s):
        return False
    if re.search(r"&\S", s):
        return False  # Kruti '&at' style glued ampersand
    toks = re.findall(r"[A-Za-z]+", s)
    if not toks:
        return False
    for w in toks:
        if w in KRUTI or w.lower() in KRUTI:
            return False
    if len(toks) == 1:
        if len(toks[0]) == 1:
            return False  # single letter = figure residue
        w = toks[0].lower()
        return (w in COMMON) or (w in STARTERS) or (toks[0][0].isupper() and len(w) >= 4)
    common_hits = sum(1 for w in toks if w.lower() in COMMON or w.lower() in STARTERS)
    return common_hits >= 2

def _strip_hindi_stem(raw):
    lines = []
    for ln in raw.split("\n"):
        if _is_english_line(ln):
            lines.append(ln.strip())
    return clean(" ".join(lines))

def _strip_hindi_opt(opt):
    if "/" in opt:
        opt = opt.split("/")[-1]
    return clean(opt)

SAMPLE_STEM_FIX = {
    8: "Find the value of a and b, if [the equation is shown as a fraction figure in the source].",
}

def parse_sample_raga(path):
    t = pdf_text(ROOT+"/prepp/"+path)
    segs = re.split(r"Ans\s*:\s*([A-Da-d])", t)
    out = []
    for k in range(1, len(segs), 2):
        seg = segs[k-1]; ans = segs[k].upper()
        m = re.search(r"Q\.(\d+)\.", seg)
        if not m:
            continue
        num = int(m.group(1))
        post = seg[m.end():]
        om = re.match(r"\s*(.*?)\s*\(A\)\s*(.*?)\s*\(B\)\s*(.*?)\s*\(C\)\s*(.*?)\s*\(D\)\s*(.*?)\Z", post, re.S)
        if not om:
            # no (A)-(D) option letters: figure question with text stem (e.g. Q25 Venn)
            stem = _strip_hindi_stem(post)
            if not stem:
                continue  # fully figure-based (Q26-30), nothing to transcribe
            out.append({"q": stem, "opts": [], "ans": ans, "fig": True})
            continue
        stem = _strip_hindi_stem(om.group(1))
        if num in SAMPLE_STEM_FIX:
            stem = SAMPLE_STEM_FIX[num]
        opts = [_strip_hindi_opt(om.group(i)) for i in (2,3,4,5)]
        fig = all(not o for o in opts)
        if fig:
            opts = []
        if not stem and not opts:
            continue
        out.append({"q": stem, "opts": opts, "ans": ans, "fig": fig})
    return out

# ============================================================ build
papers = []
def add(group, sortkey, date, source, qs):
    papers.append({"group": group, "sk": sortkey, "date": date, "source": source, "qs": qs})

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
for f, sk, d in fy:
    add("Y", sk, d, "SelfStudys", parse_selfstudys_raga(ROOT+"/"+f))

fyp20 = [("Group_Y_2020_04-Nov.pdf","2020-11-04","04 Nov 2020"),
         ("Group_Y_2020_05-Nov.pdf","2020-11-05","05 Nov 2020"),
         ("Group_Y_2020_06-Nov.pdf","2020-11-06","06 Nov 2020")]
for f, sk, d in fyp20:
    add("Y", sk, d, "Prepp", parse_prepp_raga(f))

fyp21 = [("Group_Y_2021_12-Jul_S1.pdf","2021-07-12","12 Jul 2021 Shift-1"),
         ("Group_Y_2021_12-Jul_S2.pdf","2021-07-12","12 Jul 2021 Shift-2"),
         ("Group_Y_2021_13-Jul_S1.pdf","2021-07-13","13 Jul 2021 Shift-1"),
         ("Group_Y_2021_14-Jul_S3.pdf","2021-07-14","14 Jul 2021 Shift-3"),
         ("Group_Y_2021_15-Jul_S1.pdf","2021-07-15","15 Jul 2021 Shift-1"),
         ("Group_Y_2021_15-Jul_S2.pdf","2021-07-15","15 Jul 2021 Shift-2"),
         ("Group_Y_2021_15-Jul_S3.pdf","2021-07-15","15 Jul 2021 Shift-3"),
         ("Group_Y_2021_16-Jul_S2.pdf","2021-07-16","16 Jul 2021 Shift-2")]
for f, sk, d in fyp21:
    add("Y", sk, d, "Prepp", parse_prepp_raga(f))

uy = [("utkarsh/Group_Y_2025_28-Sep.pdf","2025-09-28","28 Sep 2025"),
      ("utkarsh/Group_Y_2026_31-Mar_Shift-1.pdf","2026-03-31","31 Mar 2026 Shift-1"),
      ("utkarsh/Group_Y_2026_31-Mar_Shift-2.pdf","2026-03-31","31 Mar 2026 Shift-2")]
for f, sk, d in uy:
    add("Y", sk, d, "Utkarsh", parse_utkarsh_raga(f))

add("XY", "2026-03-30", "30 Mar 2026 (Other than Science)", "Utkarsh",
    parse_utkarsh_section_raga("utkarsh/Group_XY_2026_30-Mar_OtherThanScience.pdf"))

add("X", "SAMPLE", "Sample RAGA Paper", "Prepp Sample",
    parse_sample_raga("Sample_X_RAGA.pdf"))

order = {"SelfStudys":0,"Prepp":1,"Utkarsh":2,"Prepp Sample":3}
papers.sort(key=lambda p: (p["sk"], order.get(p["source"], 9), p["group"]))

# ============================================================ write
R = "=" * 78
out = []
def w(s): out.append(s)
w(R)
w("AGNIVEER VAYU (AIR FORCE) — MASTER RAGA QUESTION BANK")
w("All Reasoning & General Awareness (RAGA) questions from ALL available papers")
w("(Group Y + Group XY + Sample RAGA paper)")
w("Compiled: 13 September 2026")
w(R); w("")
w("NOTE: Questions are transcribed as printed in the source. Where a source")
w("carries an answer key, the answer is shown. Memory-based papers may have")
w("minor wording variations and their answer keys may occasionally contain")
w("errors — they are reproduced as printed. RAGA is the non-science section")
w("(30 questions in Group Y), so it appears only in Group Y and Group XY")
w("papers; Group X (science) papers have no RAGA section.")
w("")
w("FIGURE-BASED QUESTIONS: where a question's options are printed only as")
w("figures/diagrams (no text), the stem and its key are kept and a note")
w("'(Options are figure-based in the source)' is shown; the figures cannot be")
w("reproduced in a text file.")
w(""); w("-"*78); w("INVENTORY (papers included in this file)"); w("-"*78)
tot = keyed = figq = 0
for p in papers:
    n = len(p["qs"]); k = sum(1 for q in p["qs"] if q["ans"] != "?"); f = sum(1 for q in p["qs"] if q["fig"])
    tot += n; keyed += k; figq += f
    w("  {:<12s} | {:<3s} | {:<26s} | {:<12s} | RAGA Qs: {} (keyed {}, figure-based {})".format(
        p["sk"], p["group"], p["date"], p["source"], n, k, f))
w("  {:<12s} | {:<3s} | {:<26s} | {:<12s} | TOTAL RAGA Qs: {} (keyed {})".format("", "", "", "", tot, keyed))
w("")
w("MISSING / EXCLUDED:")
w("  - Prepp Group Y 07 Nov 2020 — Hindi-language version + empty")
w("    'Question doesnt exist' placeholders; excluded.")
w("  - Prepp Sample RAGA Q26-Q30 — pure figure-series questions with no text")
w("    at all in the source; excluded.")
w("  - Prepp 16 Jul 2021 Shift-2 Q43 — printed entirely as a figure (no text")
w("    in the source); excluded.")
w("  - Utkarsh 31 Mar 2026 Shift-2 Q22 & Q28 — printed in Hindi only (no")
w("    English text in the source); excluded to keep the bank English-only.")
w("  - PW model papers and user-uploaded TXTs carry no RAGA section.")
w("  - sscstudy/AirForce_Group_X_Y_PYQ_Book_263pg.pdf — scanned (no text layer).")
w("  - Testbook-paid papers — not obtainable anywhere free.")
w(""); w(R)
pid = 0
for p in papers:
    pid += 1
    w(""); w("PAPER {}  |  GROUP {}  |  {}  |  Source: {}".format(pid, p["group"], p["date"], p["source"])); w(R)
    for qi, q in enumerate(p["qs"], 1):
        w("Q{}. {}".format(qi, q["q"]))
        if q["fig"]:
            w("   (Options are figure-based in the source)")
        else:
            for oi, o in enumerate(q["opts"]):
                w("   ({}) {}".format("ABCDE"[oi], o))
        w("   Answer: {}".format(q["ans"]))
        w("")
w(R); w("END OF RAGA QUESTION BANK"); w(R)
text = "\n".join(out) + "\n"
open(OUT, "w", encoding="utf-8").write(text)

json.dump([{"group":p["group"],"date":p["date"],"source":p["source"],
            "qs":[{"q":q["q"],"opts":q["opts"],"ans":q["ans"],"fig":q["fig"]} for q in p["qs"]]} for p in papers],
          open(DBG,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print("papers: {} | total Qs: {} | keyed: {} | figure-based: {}".format(len(papers), tot, keyed, figq))
for p in papers:
    k = sum(1 for q in p["qs"] if q["ans"] != "?")
    print("  {:<3s} {:<26s} {:<12s} -> {} Qs (keyed {})".format(p["group"], p["date"], p["source"], len(p["qs"]), k))
