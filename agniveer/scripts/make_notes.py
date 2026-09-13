# -*- coding: utf-8 -*-
"""Regenerate Master_Physics_Notes.txt from repaired content.txt."""
import re, textwrap

src = open("/home/user/pdf_build/content.txt", encoding="utf-8").read()
lines = src.split("\n")

CH = {  # chapter number -> title
 "1":"PHYSICAL WORLD, UNITS AND MEASUREMENT",
 "2":"KINEMATICS",
 "3":"LAWS OF MOTION",
 "4":"WORK, ENERGY AND POWER",
 "5":"ROTATIONAL MOTION (SYSTEM OF PARTICLES AND RIGID BODY)",
 "6":"GRAVITATION",
 "7":"PROPERTIES OF BULK MATTER (SOLIDS AND FLUIDS)",
 "8":"THERMODYNAMICS",
 "9":"KINETIC THEORY OF GASES",
 "10":"OSCILLATIONS AND WAVES",
 "11":"ELECTROSTATICS",
 "12":"CURRENT ELECTRICITY",
 "13":"MAGNETIC EFFECTS OF CURRENT AND MAGNETISM",
 "14":"ELECTROMAGNETIC INDUCTION AND ALTERNATING CURRENT",
 "15":"ELECTROMAGNETIC WAVES",
 "16":"OPTICS",
 "17":"DUAL NATURE OF MATTER AND RADIATION",
 "18":"ATOMS AND NUCLEI",
 "19":"ELECTRONIC DEVICES",
 "20":"COMMUNICATION SYSTEMS",
}

R = "=" * 80
out = []
def w(s): out.append(s)

# ---------------- header ----------------
w(R); w("PHYSICS MASTER NOTES"); w("IAF AGNIVEERVAYU (SCIENCE GROUP)")
w("ENGLISH MASTER VERSION"); w(R); w("")
w("HOW THIS BOOK WORKS"); w("")
w("Every chapter teaches one topic concept-first, in a fixed 13-section flow:")
w("INTRODUCTION -> CORE CONCEPTS -> KEY RELATIONS -> FORMULAS -> CONDITIONS /")
w("SPECIAL CASES -> HOW TO RECOGNIZE THE QUESTION -> SOLVING METHODS ->")
w("REAL PYQ EXAMPLES -> 10-SECOND TRICKS -> IMPORTANT FACTS -> COMMON TRAPS ->")
w("GRAPHS / DIAGRAMS -> LAST-MINUTE REVISION.")
w("Real exam questions appear only as worked examples inside this flow,")
w("never as a question dump: learn the concept, then solve any variation.")
w("")
w("WHAT IS COVERED"); w("")
w("All 20 official Agniveervayu Physics topics, built strictly from the real")
w("papers. Every formula, condition, trap and example is something the exam")
w("actually demands - or is directly needed to solve what it demands. Nothing")
w("else has been added.")
w(""); w(R); w("TABLE OF CONTENTS"); w(R)
def toc_case(s):
    s = s.title()
    for small in (" And ", " Of ", " The ", " For "):
        s = s.replace(small, small.lower())
    return s
for n in range(1, 21):
    w(f"{n:>3}. {toc_case(CH[str(n)])}")
w("")
w(" FINAL FORMULA REVISION")
w(" FINAL RELATIONS REVISION")
w(" FINAL TRICKS REVISION")
w(" FINAL TRAPS REVISION")
w(" FINAL FACTS REVISION")
w(R); w("")

# ---------------- body ----------------
cur_ch = None
cur_sec = None
in_tbl = False
in_box = False
skip_until_chapter = False
cur_pyq = {"E":[],"W":[],"x":[],"M":[],"K":[]}

def flush_pyq():
    global cur_pyq
    if any(cur_pyq.values()):
        for part in ["E","W","x","M","K"]:
            if cur_pyq[part]:
                lab = {"E":"Q. ","W":"   Method: ","x":"   Solve: ",
                       "M":"   Faster: ","K":"   Takeaway: "}[part]
                for t in cur_pyq[part]:
                    w(lab + t); lab = "       "
        w("")
    cur_pyq = {"E":[],"W":[],"x":[],"M":[],"K":[]}

def emit_bullet(t):
    t = t.strip()
    if not t: return
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    if len(t) <= 86:
        w("- " + t)
    else:
        w("- " + textwrap.fill(t, 86, subsequent_indent="  ", initial_indent=""))

def emit_prose(t):
    t = t.strip()
    if not t: return
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    for ln in textwrap.wrap(t, 88):
        w(ln)

sec_labels = {
 "INTRODUCTION":"INTRODUCTION",
 "CORE CONCEPTS":"CORE CONCEPTS",
 "KEY RELATIONS":"KEY RELATIONS",
 "FORMULAS":"FORMULAS",
 "CONDITIONS / SPECIAL CASES":"CONDITIONS / SPECIAL CASES",
 "HOW TO RECOGNIZE THE QUESTION":"HOW TO RECOGNIZE THE QUESTION",
 "SOLVING METHODS":"SOLVING METHODS",
 "REAL PYQ EXAMPLES":"REAL PYQ EXAMPLES",
 "10-SECOND TRICKS":"10-SECOND TRICKS",
 "IMPORTANT FACTS":"IMPORTANT FACTS",
 "COMMON TRAPS":"COMMON TRAPS",
 "GRAPHS / DIAGRAMS":"GRAPHS / DIAGRAMS",
 "LAST-MINUTE REVISION":"LAST-MINUTE REVISION",
}
sec_order = ["INTRODUCTION","CORE CONCEPTS","KEY RELATIONS","FORMULAS",
 "CONDITIONS / SPECIAL CASES","HOW TO RECOGNIZE THE QUESTION","SOLVING METHODS",
 "REAL PYQ EXAMPLES","10-SECOND TRICKS","IMPORTANT FACTS","COMMON TRAPS",
 "GRAPHS / DIAGRAMS","LAST-MINUTE REVISION"]

for ln in lines:
    s = ln.strip()
    if not s: continue
    if s.startswith("END OF PHYSICS"): break
    if re.match(r"^={3,}", s): continue
    m = re.match(r"^#(\d+)\|(.*)$", s)
    if m:
        flush_pyq(); in_tbl=False; in_box=False; skip_until_chapter=False
        n, title = m.group(1), m.group(2).strip()
        cur_ch = n; cur_sec = None
        w(R); w(f"CHAPTER {n} - {title}"); w(R); w("")
        continue
    if s == "##CONTENTS":
        skip_until_chapter = True; continue
    if skip_until_chapter:
        continue
    if s.startswith("##FINAL"):
        flush_pyq(); in_tbl=False; in_box=False
        label = s[2:].strip().upper()
        cur_sec = None
        w(R); w(label); w(R)
        continue
    m = re.match(r"^##(\d+)\.\s*(.*)$", s)
    if m:
        flush_pyq(); in_tbl=False; in_box=False
        num, label = int(m.group(1)), m.group(2).strip()
        cur_sec = label
        w(f"{num}. {sec_labels.get(label, label.upper())}"); w("")
        continue
    # in-box / table / pyq markers
    if s in ("TBL",):
        in_tbl=True; continue
    if s in ("ENDTBL",):
        in_tbl=False; w(""); continue
    if in_tbl:
        w("    " + s.replace("|", " | ").strip()); continue
    if s in ("B>",):
        in_box=True; continue
    if s in ("B<",):
        in_box=False; w(""); continue
    if in_box:
        if s.startswith("p>"): emit_bullet(s[2:])
        else: emit_bullet(s)
        continue
    if s.startswith("F>"):
        emit_bullet(s[2:]); continue
    if s.startswith("T>"):
        w("TRAP: " + s[2:]); continue
    if s.startswith("C>"):
        w("FIX:  " + s[2:]); continue
    if s.startswith("E>"):
        flush_pyq()
        cur_pyq["E"].append(re.sub(r"\*\*(.+?)\*\*", r"\1", s[2:]).strip())
        continue
    if s[0:2] in ("W>","x>","M>","K>"):
        cur_pyq[s[:1]].append(re.sub(r"\*\*(.+?)\*\*", r"\1", s[2:]).strip())
        continue
    # plain line
    if cur_sec in ("CORE CONCEPTS","CONDITIONS / SPECIAL CASES",
                   "KEY RELATIONS","SOLVING METHODS","10-SECOND TRICKS",
                   "IMPORTANT FACTS","GRAPHS / DIAGRAMS"):
        if s.startswith("- "): emit_bullet(s[2:])
        else: emit_bullet(s)
    else:
        emit_prose(s)

flush_pyq()
w(""); w(R); w("END OF PHYSICS MASTER NOTES"); w(R)

text = "\n".join(out) + "\n"
open("/home/user/agniveer/Master_Physics_Notes.txt", "w", encoding="utf-8").write(text)
print("wrote notes:", len(out), "lines,", len(text), "bytes")
