#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the master physics TXT from _phys_raw.json."""
import json, re

R = json.load(open('/home/user/_phys_raw.json'))

# ---------- tidy helpers ----------
def tidy_opt(s):
    s = s.replace('\u00a0', ' ')
    m = re.search(r'(?:\n\s*[-–]?\d+(?:\.\d+)?\s*){2,}', s)
    if m:
        s = s[:m.start()]
    return re.sub(r'\s+', ' ', s).strip()

def _raw_junk(ln):
    s = ln.strip()
    if not s:
        return False
    if re.match(r'^Page[- ]*\d+$', s, re.I):
        return True
    if s.startswith('http://') or s.startswith('https://'):
        return True
    if re.match(r'^={3,}$', s):
        return True
    if re.match(r'^(PHYSICS|MATHEMATICS|ENGLISH|RAGA|SCIENCE|GENERAL|REASONING|OTHER)[ -–—]*QUESTIONS?', s, re.I):
        return True
    return False

def render_q(q, n):
    """q: dict with q/opts/ans OR raw"""
    if q is None:
        return f"Q{n}. [question not available in this source]\n"
    if 'raw' in q:
        lines = [ln.rstrip() for ln in q['raw'].split('\n')]
        lines = [ln for ln in lines if not _raw_junk(ln)]
        if not lines:
            return f"Q{n}. [no text]\n"
        return f"Q{n}. {lines[0]}\n" + "\n".join(lines[1:]).rstrip() + "\n"
    parts = [f"Q{n}. {q['q']}"]
    for L, o in zip('ABCD', q['opts']):
        o = tidy_opt(o)
        if o:
            parts.append(f"   ({L}) {o}")
    if q.get('ans'):
        parts.append(f"   Answer: {q['ans']}")
    return "\n".join(parts) + "\n"

# ---------- sort: chronological, MODEL last ----------
def sort_key(r):
    k = r['key']
    if k == 'MODEL':
        return (9999, 0, 0, r['grp'], r['src'])
    y, m, d = [int(x) for x in k.split('-')]
    return (y, m, d, r['grp'], r['src'])

R_sorted = sorted(R, key=sort_key)

out = []
out.append("=" * 78)
out.append("AGNIVEER VAYU (AIR FORCE) — MASTER PHYSICS QUESTION BANK")
out.append("All Physics questions from ALL available papers (Group X + Group XY + Model)")
out.append("Compiled: 12 September 2026")
out.append("=" * 78)
out.append("")
out.append("NOTE: Questions are transcribed as printed in the source. Where a source")
out.append("carries an answer key, the answer is shown; user-uploaded TXTs contain no")
out.append("answer key (as provided). Memory-based papers may have minor wording")
out.append("variations and their answer keys may occasionally contain errors — they")
out.append("are reproduced as printed. Some shifts appear from more than one source,")
out.append("and both copies are kept. Hindi paper (07 Nov 2020) is kept in Hindi.")
out.append("")

# ---------- inventory ----------
out.append("-" * 78)
out.append("INVENTORY (papers included in this file)")
out.append("-" * 78)
tot_q = 0
for r in R_sorted:
    qs = r['qs']
    cnt = sum(1 for x in (qs or []) if x is not None)
    tot_q += cnt
    out.append(f"  {r['key']:12s} | {r['grp']:3s} | {r['label']:22s} | {r['src']:12s} | Physics Qs: {cnt}")
out.append(f"  {'':12s} | {'':3s} | {'':22s} | {'':12s} | TOTAL Physics Qs: {tot_q}")
out.append("")
out.append("MISSING PAPER (Physics section not obtainable anywhere free):")
out.append("  - Group X, 18 Mar 2024 (Shift 1) — available only on Testbook (login/paid,")
out.append("    link expired). No free site carries its Physics questions, so nothing")
out.append("    could be harvested. (Group Y 17/18-Mar-2024 and 16-Nov-2024 are also")
out.append("    Testbook-only but Group Y has no Physics section.)")
out.append("")

# ---------- papers ----------
idx = 1
for r in R_sorted:
    qs = r['qs']
    out.append("")
    out.append("=" * 78)
    out.append(f"PAPER {idx}  |  GROUP {r['grp']}  |  {r['label']}  |  Source: {r['src']}")
    out.append("=" * 78)
    idx += 1
    if not qs:
        out.append("  (no content)")
        continue
    for n, q in enumerate(qs, 1):
        out.append(render_q(q, n))

txt = "\n".join(out) + "\n"
path = '/home/user/agniveer/Master_Physics_All_Papers.txt'
open(path, 'w', encoding='utf-8').write(txt)
print("WROTE:", path)
print("Total physics questions:", tot_q)
print("Papers listed:", len(R_sorted))
import os
print("File size:", os.path.getsize(path), "bytes")
