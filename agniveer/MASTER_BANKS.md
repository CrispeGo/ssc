# Agniveer Vayu — Master Question Banks (TXT)

Ye 5 compiled question-bank files hain — **har available paper** ka clean, linear transcription,
paper/date/shift/source label ke saath + answer key (jahan source ne di ho). Memory-based papers
ke answers "as printed" hain (errors ho sakte hain — reproduce kiye gaye hain, invent nahi).

| File | Subject | Papers | Questions | Keyed |
|---|---|---|---|---|
| `Master_Math_All_Papers.txt` | Mathematics | 33 | 799 | ✅ (source keys) |
| `Master_Physics_All_Papers.txt` | Physics | 34 | 824 | ✅ |
| `Master_Physics_Notes.txt` | Physics (teaching notes) | — | — | — |
| `Master_English_All_Papers.txt` | English | 65 | 1,240 | 1,113 |
| `Master_RAGA_All_Papers.txt` | Reasoning & General Awareness | 27 | 802 | 802 |

## Format (sab mein same)

```
PAPER 12  |  GROUP Y  |  13 Jul 2021 Shift-1  |  Source: Prepp
==============================================================================
Q1. <question text>
   (A) <option>
   (B) <option>
   (C) <option>
   (D) <option>
   Answer: B
```

Har file mein: **NOTE** (policy) → **INVENTORY** (paper-wise counts) → **MISSING / EXCLUDED** note →
paper sections. Figure-based questions (options sirf diagram) ka stem + key rakha hai,
`(Options are figure-based in the source)` note ke saath.

## Sources covered

- **SelfStudys** — full-solution papers (2020–2025), Group X + Y
- **Prepp / Collegedunia** — 2020–2021 saare day/shift papers (Group X + Y) + subject samples
- **Utkarsh** — 2024–2026 (Group X, Y, XY "Other than Science")
- **PW** — official Group XY Model Papers
- **AllExamPYQs** — Group Y all-shifts (2022, 2023)
- **User-uploaded memory TXTs** — Group XY (no answer key, `Answer: ?`)

## Build scripts

`agniveer/scripts/` mein extraction pipeline hai:
`extract_math.py`, `extract_physics.py`, `extract_english.py`, `extract_raga.py` →
ye 4 script in files ko PDF/TXT sources se generate karte hain (reproducible).
