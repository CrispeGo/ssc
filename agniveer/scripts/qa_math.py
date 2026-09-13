#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re
R = json.load(open('/home/user/_math_raw.json'))

# allowlist of questions whose answer is genuinely lost in source
KNOWN_BLANK = {
    ('17 Mar 2024 Shift-1', 'Utkarsh', 15),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 25),
}

JUNK = re.compile(r'(Correct Option|Answer\s*:|Android|Held On|Telegram|Defence|Solution\s*:|^\s*\(\s*\)\s*$)', re.I)

def flag_opt(o):
    if not o or len(o) < 1:
        return 'BLANK'
    if JUNK.search(o):
        return 'JUNK:' + o[:60]
    return ''

def flag_q(q):
    if not q or len(q) < 5:
        return 'SHORT/EMPTY'
    if JUNK.search(q):
        return 'JUNKQ:' + q[:60]
    return ''

total_defects = 0
for r in R:
    qs = r['qs']
    if qs is None:
        print(f"[{r['label']} | {r['src']}]  ERROR: {r['err']}")
        total_defects += 1
        continue
    probs = []
    for i, q in enumerate(qs, 1):
        if q is None:
            probs.append(f"Q{i}: MISSING")
            continue
        if 'raw' in q:  # user txt verbatim
            continue
        fq = flag_q(q.get('q'))
        if fq:
            probs.append(f"Q{i}: question {fq}")
        opts = q.get('opts') or []
        if len(opts) != 4:
            probs.append(f"Q{i}: {len(opts)} options")
        for oi, o in enumerate(opts):
            fo = flag_opt(o)
            if fo:
                probs.append(f"Q{i} opt {'ABCD'[oi]}: {fo}")
        ans = q.get('ans') or ''
        if ans == '' and (r['label'], r['src'], i) not in KNOWN_BLANK:
            probs.append(f"Q{i}: no answer")
        elif ans and ans not in 'ABCD':
            probs.append(f"Q{i}: bad answer {ans!r}")
    if probs:
        print(f"[{r['label']} | {r['src']}]  {len(probs)} defect(s)")
        for p in probs:
            print('    ' + p)
        total_defects += len(probs)

print()
print("TOTAL DEFECTS:", total_defects)
