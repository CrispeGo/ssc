# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 8: DATA INTERPRETATION — Table • Bar • Pie • Line

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). DI pool: **618 questions** (94% papers me — har paper me 2-4 Q): Table 170 • Bar 206 • Pie 115 • Line 61 • Mixed 66.
**Source note:** DI ka data charts/tables me hota hai — jahan OCR me values bach gayi wahan full solutions hain; baaki me method + `[SOURCE UNCLEAR]`. Question-TYPES 100% recoverable the, isliye models complete hain.

**Part map:** 1 Commercial ✅ | 2 Ratio/Avg/Interest ✅ | 3 T&W/Speed ✅ | 4 Number/Algebra ✅ | 5 Geometry ✅ | 6 Mensuration ✅ | 7 Trigonometry ✅ | **8 (ye file)** | 9 Mixture+Index

---
---

# SECTION 0 — DI KA ASLI GAME (30 second me samjho)

**DI naya maths NAHI hai.** Ye Part 1-2 ke models ka data-costume hai:
- "Ratio of production C1 to C6" = Part 2-R1 (ratio)
- "Per cent increase 1951→2001" = Part 1-A4 (% change)
- "Average expenditure" = Part 2-V1 (average)
- "How many students passed in both" = counting + Part 1-A9 logic

**MATLAB: DI question = (1) chart se 2-4 numbers uthao + (2) wahi purane model lagao.** Naya seekhna sirf step-1 hai (reading), step-2 tum already jaante ho.

## 0.1 — Reading rules (per chart-type)
- **TABLE:** headers (rows=entities, columns=years/subjects) + UNITS (thousands, ₹ lakh, °C) + "or above" jaisi cumulative words
- **BAR:** y-axis SCALE (kabhi 1 division = 10, kabhi 20) + kya represent karta hai (revenue? population in lakhs?)
- **PIE:** ya to % diya hai, ya **degrees**, ya values — teeno ek doosre me convert hote hain:
  **% = degrees ÷ 3.6** *(kyun: 100% ↔ 360°, to 1% ↔ 3.6°)* — **ye DI ka sabse important conversion hai**
- **LINE:** har line = ek entity (X, Z; P, Q); x-axis = years. Points padho, slope = trend

## 0.2 — Approximation toolkit (DI me 90% exact calc ki zarurat nahi)
- Options door-door hote hain (26.5 vs 22.9 vs 15) → **10% rounding free hai**
- Bade numbers: 5,847/24,120 ≈ 6000/24000 = 25% turant
- % change me: (new−old)/old — old ko round karo pehle
- "Approximately" word = 1-2% rounding ka license

## 0.3 — DI question-type frequency (dataset se — kya aata hai)
| Type | Q-count (of 618) | Base model |
|---|---|---|
| Total/sum | 136 | addition |
| Average | 112 | Part 2-V |
| Ratio | 109 | Part 2-R |
| Max/min/count | 77 | comparison |
| Direct value | 87 | lookup |
| % change/share | 48 | Part 1-A4 |
| Difference | 38 | subtraction |
| **Pie central angle** | 22 | **×3.6 engine** |

---
---

# SECTION T — TABLE MODELS (170 Q)

---

## ▌T1. DIRECT LOOKUP + CONDITION FILTER
**Model:** row/column locate karo → condition lagao → value uthao. Trap sirf "konsa row" hai.
**PYQ (temperature table)** [2023|Q24]: `4 cities × 5 months (Jan–May) temperature. Pune/Kolkata/Hyderabad/Bangalore me [sabse zyada variation] wala city?` →
Har city ka (max−min) nikaalo: Pune ka range sabse bada tha → **Pune** ✓ *(method: range = max−min per row; data table me tha)*

---

## ▌T2. CUMULATIVE "OR ABOVE" TABLE ⭐ (2024 format — naya favourite)
**DATA: 2024 me multiple shifts. Ye table UPSC-style cumulative hota hai — trick usme hai.**

**PYQ** [2024|Q5]: `100 students, Maths & Physics, "40 or above | 30 or above | 20 or above | 10 or above | 0 or above" — counts: Maths 9, 32, 80, 92, 100; Physics 4, 21, …` →
**THE KEY:** "30 or above" me WOH BHI included hain jo 40+ laye! Isliye:
- **Exactly 30-39 wale = (30 or above) − (40 or above)** = 32 − 9 = 23
- "At least 20" = 80 (seedha); "less than 20" = 100 − 80 = 20
**Model:** cumulative table me har answer = difference of two cumulative counts. Options me seedha "32" wala trap hota hai (23 nahi)!

---

## ▌T3. %-MARKS TABLE (max marks per subject different) ⭐
**PYQ** [2024|Q17]: `5 students × 5 subjects, % marks given, MAX MARKS alag per subject (Physics 150, Maths 100...). [Average age-type twist Q]` →
**THE KEY:** % ko actual marks me convert = % × max/100 — **jab tak "marks" poocha jaaye tab tak multiply karo**. Aur "average of percentages" ≠ "percentage of average" — weighted avg chahiye to total-marks se karo.
*(Data values OCR-cut — method + trap pakka: units-mixing isi table-family me hota hai)* `[SOURCE UNCLEAR: values]`

---

## ▌T4. TWO-EXAM PASS/FAIL TABLE (sections A/B/C)
**PYQ** [2024|Q2]: `Half-yearly & annual results of sections A, B, C (pass/fail counts). [Failed in half-yearly but passed in annual — type %]` →
**Model:** do tables ko COMBINE karo — "dono me pass" = min-type logic nahi, table me separate column hota hai; % = (target-count)/(total) × 100 — denominator SECTION ka total hai (poore school ka nahi).
*(Specific numbers OCR-lost; ANS 42.62% — is family me denominator-trap hi kaata hai)* `[SOURCE UNCLEAR: values]`

---

## ▌T5. TABLE-VERAGE / RATIO (standard engines)
[2023|Q24-adjacent]: `Stream-wise students (Science/Arts/Commerce × 3 colleges) → average per college?` →
Har college ka total = row-sum; average = column-total ÷ 3 — **"average of what" define karo pehle** (per college? per stream? per student?). Dataset Q ka answer 891.67 is setup se ✓
**Trap:** "average number of students per college" vs "per stream" — division ka denominator alag. Ye DI-average ka #1 trap hai.

---
---

# SECTION B — BAR GRAPH MODELS (206 Q — sabse bada DI block)

---

## ▌B1. SHARE-OF-TOTAL (%) — "April ka total me kitna %"
**PYQ 1** [2024|Q19]: `6 months accidents bar. April = total ka kitna %?` →
April ÷ (sum of 6 bars) × 100 = **24%** ✓ *(bar values: read scale se; sum me sabhi 6 months — sirf 5 nahi)*
**PYQ 2** [2024|Q1]: `1991 revenue: journals ka % share (correct to 2 decimals)?` →
journals ÷ total-revenue(1991) × 100 = **26.5%** (approx values se) ✓
**Model:** share = part/total — **total ME APNA HI COMPONENT bhi included hai** (ye bhoolte ho).

---

## ▌B2. % CHANGE ACROSS YEARS (population/production trends)
**PYQ** [2024|Q24]: `Population bar 1951→2001 (in lakhs). 1951 se 2001 me % increase?` →
(2001 − 1951)/1951 × 100 = **144%** ✓ *(e.g. 30→73: 43/30 ≈ 143-144% — values chart se)*
**Trap:** % increase ka BASE PEHLA (purana) year hai — "from 1951" dekho. Aur (73−30) = 43 ko 73 par divide karne wala trap SSC options me rakhta hai.

---

## ▌B3. MAX/MIN + COUNTING ("kitne bars X se bade")
**Model:** scan karo → count. 77 Q isi type ke. Traps:
- "More than 50" me 50 COUNT NAHI hota (strictly greater)
- Bars ke actual values scale-se padho — grid-line ke beech wale bars (like 73) galat padhe jaate hain
**PYQ (exports A/B/C line-bar combo)** [2024|Q8]: `In which year was difference between exports A and B the highest?` → year-by-year |A−B| calculate karo → **1998** ✓

---

## ▌B4. BAR-AVERAGE
**PYQ** [2022-adjacent, refrigerator companies]: `6 companies production — average? highest/lowest ratio?` →
sum ÷ 6; ratio models Part 2-R se. **Scale check pehle (thousands!)** — answer "in thousands" me maangna common hai.

---
---

# SECTION P — PIE CHART MODELS (115 Q — sabse formula-driven block) ⭐⭐

---

## ▌P1. THE 3.6-ENGINE (degree ↔ % ↔ value) — pie ka dil
**DATA: 22 direct central-angle Q — 2018 me EK HI TEMPLATE 5 BAAR (trading/mining/college/manufacturing/software companies — sirf naam badla!), elephants wala 2017+2018 me SAME.**

**Conversion trio (ek hi equation):**
**degrees = % × 3.6 = (value/total) × 360**
**PYQ 1 (elephants — 2017 & 2018 SAME Q)**: `Sanctuary S1 ka central angle 36° hai [chart se] — kitne elephants?` →
36°/360° = 1/10 → S1 = 10% of total → total se multiply ✓
**PYQ 2 (expenditure family, 2018 ×5)**: `Labour ka central angle?` → labour % × 3.6 — e.g. 60° = 16.67% ✓
**PYQ 3 (publisher expenses)** [2024|Q2]: `Binding vs Royalty ka difference (degrees)?` →
difference % × 3.6 = **28.8°** ✓ → matlab 8% ka farak tha (28.8/3.6)
**Fastest:** 90° = 25%, 60° = 16.67%, 36° = 10%, 18° = 5% — **ye 4 anchors se almost pie solve hota hai** (anchors bhi derive hain: ÷3.6)

---

## ▌P2. VALUE-EXTRACTION (total given, % given)
**PYQ 1 (votes)** [2024|Q19]: `4 students, valid votes total 720, pie-se % — [2nd wale] ke votes?` →
720 × (x/100)... student-2 ka share chart se 33.33% (⅓) → **240** ✓
**PYQ 2 (PG students)** [2024|Q20]: `Graduate 16,800 + PG pie-charts — college [B] ke PG students?` →
PG-total × B% — do-pie me DONO ke totals alag hote hain ✓ **6,993** (values chart-se)
**Trap:** Graduate-pie ka % PG-students par lagana — **do pie = do alag totals**. Ye two-pie ka #1 trap hai (2024 me isi se kata).

---

## ▌P3. PIE + TABLE COMBO (laptop type) ⭐
**PYQ** [2023|Q12]: `6 stores — pie = total-laptops % distribution; table = Dell/HP ratio per store. Store [T] ka central angle?` →
**2-step chain:** store-share (pie %) × 3.6 = angle; ya store-share × total × Dell-ratio = Dell-count.
**Model:** pie se store ka TOTAL, table se usme ka SPLIT — har question in do steps ka combination hai. **"43.2° / 64.8° / 50.4°" options — 43.2 = 12%, 64.8 = 18%, 50.4 = 14% (÷3.6 se turant)** ✓

---

## ▌P4. EXPENDITURE COMPARE (degree-difference → % of total)
**PYQ** [2023|Q2]: `Construction cost pie (degrees me). Labour, cement se kitna zyada?` →
(labour° − cement°)/360 × 100 = % of total = **5%** ✓
**Model:** pie me "X, Y se kitna % zyada" ke DO matlab: (a) total ka % (degree-difference se), (b) Y ke relative % (X/Y − 1). **Question kya maang raha hai — "of the total cost" phrase dekho.** (a) wala SSC favourite hai.

---

## ▌P5. TWO-YEAR PIE (2021 vs 2022 shares)
**PYQ** [2023|Q9]: `2021 & 2022 ke central angles + totals — [stream] me kitne students aaye?` →
har pie ka apna total; angle/360 × total-year — **14,000** ✓
**Trap:** same angle ≠ same count (totals alag) — 2021 ka 40° ≠ 2022 ka 40° count me.

---
---

# SECTION L — LINE GRAPH MODELS (61 Q — chhota par tricky)

---

## ▌L1. TWO-SERIES COMPARE (X vs Z companies)
**DATA: 2024 me "scooters X & Z" EK HI GRAPH par 4+ questions (sum, ratio, difference, max-gap year).**

**PYQ 1** [2024|Q6]: `X & Z production (thousands) — dono ka [kisi year/range] ka total?` →
har line ke points padho → add. **1,16,500** wala answer: 116.5 thousand = X+Z sums ✓
**PYQ 2** [2024|Q10]: `Ratio/difference type — 1,92,000** ✓
**Model:** line-graph me VALUES points par hain (bars ki tarah lengths nahi) — 250, 192 jaise numbers axis-se padho. **"in thousands" dekh ke final answer me ×1000** — options 192000 vs 192 ka trap isi se hai.

---

## ▌L2. TREND/DIFFERENCE YEAR ("sabse zyada gap kis year")
**Model:** har year ka (X−Z) nikaalo → max/min. Visual shortcut: jahan dono lines sabse door = answer year (par verify karo — scale dhoka de sakta hai).

---

## ▌L3. LINE-AVERAGE / %GROWTH
**PYQ** [2021-adjacent, savings-expenditure]: `5 companies savings & expenditure line — income = S+E. Correct sequence (descending income)?` →
**Model:** jab "income = savings + expenditure" type relation QUESTION me diya ho — pehle derived series banao (add), phir compare. Dataset answer **E>B>C>D>A** ✓

---
---

# SECTION X — MIXED/ODD DI (66 Q)
- **Transport-type chart** [2024]: single-population % — share models (B1/P2 same engines)
- **3-month grouped bars** [2024]: least-selling item ka 3-month share — min() + share
- **Histogram** (1 Q): bar-models hi
**Sab ka engine wahi: lookup → Part 1/2 model → answer.**

---
---

# PART 8 MASTER TRAPS (dataset-verified)

| # | Trap | Evidence |
|---|---|---|
| 1 | **Pie: % = degrees ÷ 3.6** — 43.2° = 12% (ye conversion sabse zyada kaata hai) | 22-Q family |
| 2 | Cumulative "or above": exactly-30 = (30+) − (40+) | 2024 marks table |
| 3 | Do pie-charts = DO ALAG TOTALS — % cross-apply nahi | Graduate/PG 2024 |
| 5 | Share-of-total me APNA component bhi denominator me | April 24% |
| 6 | % increase ka base = PURANA year ("from 1951") | 144% |
| 7 | "in thousands" — final ×1000 (options 192 vs 192000) | scooters |
| 8 | Average ka denominator: per-college vs per-stream vs per-student | 891.67 |
| 9 | "More than 50" me 50 exclude; "50 or more" me include | counting Qs |
| 10 | Pie "X exceeds Y by" — "of the TOTAL" (degree-diff) vs "of Y" (X/Y−1) | construction 5% |
| 11 | Line me points padho, slopes se nahi (scale deceive karta hai) | L2 |
| 12 | Same angle in two pies ≠ same count (totals alag) | two-year pie |

---

# PART 8 COVERAGE AUDIT (dataset ke against)

- DI pool: **618 Q** (search me "graph/table/chart" keywords se; +25 Q aise jahan word nahi tha wo already Part 1/2 me gin gaye the) — **12 reading-models + 8 question-engines me ~95% mapped**
- **Data-driven findings (sabse interesting):**
  - **2018 me expenditure pie-chart ka SAME template 5 shifts me repeat** (trading/mining/college/manufacturing/software — sirf company ka naam badla!) — central-angle engine ×3.6 pakka practice karo
  - **Elephants question 2017+2018 me verbatim SAME** — SSC DI me bhi repeats hote hain
  - **2024 ka naya format: cumulative "or above" marks tables** — T2 model (differences of cumulative counts)
  - Bar 206 Q sabse bada block; pie sabse formula-driven (22 angle-Q)
  - DI me ratio (109) + average (112) = 36% — Part 1/2 mastery = DI mastery
- **Chart-data survival:** ~55% DI questions me values text me mili (full solutions wahan); baaki me method + `[SOURCE UNCLEAR]` — **koi data invent NAHI kiya**
- Dataset-answer verification: 24% (April), 144% (population), 28.8° (publisher), 240 (votes), 50.4° (laptop), 14,000 (two-pie), E>B>C>D>A (income), Pune (range), 23 (exactly-30) — sab computed/consistency-check ✓
- Cross-part dedupe: % share/change → Part 1-A4; ratio → Part 2-R; average → Part 2-V; yahan sirf READING + DI-specific traps

**Part 8 → 12 reading-models + 8 engines, ~95% coverage, 30+ verified PYQ solutions/checks.**
