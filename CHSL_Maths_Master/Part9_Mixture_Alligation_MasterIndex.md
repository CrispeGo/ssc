# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 9 (FINAL): MIXTURE & ALLIGATION + LEFTOVER MODELS + MASTER INDEX

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). Mixture pool: **69 raw → ~58 clean** (2018 me 16, 2023 me 20 — spikes). Leftover audit: poore 4,558 usable questions ka final cross-check.
Har solution independently verified. OCR-garbled par `[SOURCE UNCLEAR]`.

**Part map:** 1 Commercial ✅ | 2 Ratio/Avg/Interest ✅ | 3 T&W/Speed ✅ | 4 Number/Algebra ✅ | 5 Geometry ✅ | 6 Mensuration ✅ | 7 Trigonometry ✅ | 8 DI ✅ | **9 (ye file)**

---
---

# SECTION M — MIXTURE & ALLIGATION (5 models • ~58 PYQs)

**मूल Logic (alligation ka mool):** do cheezei mix karo → final concentration/price HAMESHA dono ke beech rehta hai, aur **distances ka ratio = quantities ka ULTA ratio**:
cheap qty : dear qty = (dear − mean) : (mean − cheap)
*Derivation:* cheap C₁ (c/kg × x) + dear C₂ (d/kg × y) = mean m: cx + dy = m(x+y) → x(d−m) = y(m−c) → x/y = (m−c)/(d−m). Cross-line diagram isi equation ka chitra hai — koi jadu nahi.

---

## ▌M1. MILK-WATER % ADJUSTMENT (add karke ratio fix)
**PYQ** [2022|Q16]: `150 L mixture, 30% milk. Kitna milk add kare ki water 40% ho jaye?` →
Water = 105 L (70%) → water naya 40% hona chahiye: 105/(150+x) = 0.4 → x = **112.5 L** ✓
**Model:** jise ADD kar rahe ho wo CONSTANT quantity (water) ka % change karta hai — constant wali quantity ko equation banao. (Part 1-A10 "x% of remaining" ka mixture-cousin.)

---

## ▌M2. REPLACEMENT (ek step me kya nikala, kya dala) ⭐
**DATA: 16 Q — 2023-24 ka favourite.**

**PYQ 1** [2024|Q12]: `Milk:water = 7:5. 9 L milk nikal ke water dala → 7:9. Original milk?` →
12u total; milk 7u−9, water 5u+9 → (7u−9)/(5u+9) = 7/9 → 63u−81 = 35u+63 → u = 36/7 → milk = 7u = **36 L** ✓
**PYQ 2** [2023|Q18]: `Chemical:water = 15:9. 48 L mixture nikal ke water dala → 11:13. Baad me water?` →
48 L me se X = 30, water = 18 gaya. X: 15u−30; water: 9u−18+48 = 9u+30
(15u−30)/(9u+30) = 11/13 → 195u−390 = 99u+330 → u = 7.5 → water = **97.5 L** ✓
**Model:** jo nikala usme dono components apne RATIO me hote hain (30:18 = 15:9!) — ye hi "removed mixture is proportional" logic hai. Equation: components me se (fraction × removed) minus karo.

---

## ▌M3. REPEATED REPLACEMENT — cask formula ⭐
**PYQ** [2023|Q21]: `64 L milk; HAR baAR 8 L nikal ke water — 3 baar. Final milk:water?` →
**FORMULA (derive):** har operation ke baad milk × (1 − 8/64) = × 7/8
3 baar: 64×(7/8)³ = 64×343/512 = 343×(64/512) → milk = 343k, k = 64/512 = 1/8 → milk = 42.875
Total 512k−space: milk:water = **343:169** ✓ *(512 = 8³ — SSC powers deta hai!)*
*Derivation:* milk fraction after 1 op = (T−x)/T; har op isi fraction se multiply (kyunki nikali mixture me milk current ratio me thi). Geometric chain = compound decay — CI ka (1−r) cousin (Part 2-I).
**PYQ (2-step cask)** [2023|Q6]: `75 L draw+replace, phir 60 L draw+replace → wine:water [ratio OCR-cut]` →
Method: wine left = T(1−75/T)(1−60/T); ratio se T solve. `[final-ratio SOURCE UNCLEAR — ANS 375 dataset]`
**Trap:** formula (1 − x/T)ⁿ me x = HAR baar nikala amount (same), T = total (constant — bharte jaate ho).

---

## ▌M4. ALLIGATION PRICE-MIX (mean price) ⭐ — sabse common (15 Q)
**PYQ 1 (basic)** [2021|Q69]: `Pulses ₹15 & ₹20 → mixture ₹18. Ratio?` →
(20−18):(18−15) = **2:3** ✓ *(cheap:dear — distances ulta!)*
**PYQ 2** [2021|Q62]: `₹75 & ₹90 → ₹80?` → (90−80):(80−75) = **2:1** ✓
**PYQ 3 (PROFIT twist — SSC ka pasand)** [2023|Q19]: `Tea ₹26 & ₹32/kg; mixture ₹30 me bech ke 10% gain chahiye. Ratio?` →
**Pehle SP ko cost me convert karo:** mixture-cost = 30/1.1 = 300/11 ≈ 27.27
Alligation: (32−27.27):(27.27−26) = 52:14 = **26:7** ✓
**PYQ 4 (gain 25%)** [2023|Q25]: `Wheat ₹23 & ₹14 [OCR: 223/214]; sell ₹20 @25% profit. Ratio?` →
cost = 20/1.25 = 16 → (16−14):(23−16) = **2:7** ✓
**Model:** "selling at X with profit p%" = mean price X/(1+p/100) — **ye conversion hi asli step hai**, baaki standard cross.
**Trap:** SP ko seedha mean maan lena — 30 nahi, 27.27 use hoga. Part 1 (P&L) + Part 2 (alligation) ka joint.

---

## ▌M5. WATER-PROFIT MIXES (fraud + cost mixes)
**PYQ 1** [2023|Q15]: `Milk ₹40/L; water mila ke mixture ₹30/L me becha (no gain). Water:milk?` →
₹30/L = milk fraction 30/40 = 3/4 → water:milk = **1:3** ✓
**PYQ 2 (cost-mix profit)** [2021|Q52]: `26 kg @₹20 + 30 kg @₹36; mixture ₹30/kg me becha. Profit%?` →
Cost = 520+1080 = 1600; SP = 56×30 = 1680 → **5%** ✓
**PYQ 3 (rice gain 10%)** [2023|Q2]: `₹52/kg wala kitna kg + 35 kg @₹45 → 10% gain @ [rate OCR-cut]` → mean-cost = rate/1.1, cross se x. `[rate SOURCE UNCLEAR — method pakka; ANS 87.5 kg]`
**Model:** cost-total vs SP-total — profit% ki base COST (Part 1-B1 yaad karo).

---
---

# SECTION X — LEFTOVER MODELS (final audit se nikale — 4 chhote models)

## ▌X1. FRACTION COMPARISON / ORDERING
**DATA: 2018 me arrange-type, 2022 me largest+smallest — har 2-3 saal me.**
**Model:** denominators ka LCM karke numerators compare — YA cross-multiply pairs me.
**PYQ** [2022|Q72]: `6/11, 4/15, 5/7, 5/13 — largest + smallest ka sum?` →
≈ 0.545, 0.267, 0.714, 0.385 → largest 5/7 + smallest 4/15 = 75/105 + 28/105 = **103/105** ✓
**Fastest:** decimal conversion (~2 digits) — options door-door hote hain.

## ▌X2. COORDINATE EXTRAS (Part 4-A6 ka extension)
**PYQ 1 (distance origin→line)** [2024|Q17]: `Origin se line 6x+8y−48 = 0 tak perpendicular distance?` →
|0+0−48|/√(36+64) = 48/10 = **4.8** ✓ *(formula derive: similar triangles/area — standard result, 1 baar dekh lo)*
**PYQ 2 (reflection)** [2017|Q151]: `(2,−7) ka y-axis me reflection?` → **(−2,−7)** ✓ *(y-axis mirror: x ka sign flip; x-axis: y flip)*

## ▌X3. EQUAL-MULTIPLE SHARE CHAINS
**PYQ** [2022|Q75]: `₹13,000 in X,Y,Z such that 2X = 3Y = 4Z. Z ka share?` →
2X = 3Y = 4Z = 12k (LCM) → X = 6k, Y = 4k, Z = 3k (ratio **6:4:3**) → Z = 13000×3/13 = **₹3,000** ✓
**Model:** "aX = bY = cZ" → LCM se k maano → turant ratio. (Part 2-R1 ka disguised version.)

## ▌X4. UNITARY / FRACTION STORY-PROBLEMS
**PYQ** [2018|Q52]: `25 eggs me 1 rotten; rotten me se 5/8 unusable; total 10 unusable. Crate me kitne eggs?` →
unusable = (1/25)×(5/8) = 1/40 of total → total = 10×40 = **400** ✓
**Model:** fraction-chain ko multiply karke "per unit" nikaalo, phir ulta. (Part 1-A2 chain ka story-roop.)

---
---

# 🎯 MASTER INDEX — POORA QUESTION-MODEL SYSTEM (9 Parts • 170 model-entries + ~25 sub-model variants)

## Total coverage audit (final, dataset ke against)
| | Count |
|---|---|
| Source dataset | **4,825 Q** (193 papers × 25) |
| Image-placeholders (OCR-impossible) | 267 |
| Usable questions analysed | **4,558** |
| Directly bucketed in Parts 1–9 | ~4,160 (91%) |
| Leftover-395 audit: GA-leaks (math hi nahi — urine/dance/planets 😄) | ~40 |
| Leftover: OCR-dead graphs/tables (Part 8 models, text nahi bacha) | ~50 |
| Leftover: same-model different-wording (midpoint/BPT/efficiency/ratio — Parts 3/5/2 me covered) | ~250 |
| Leftover: naye models → **Part 9-X me add** (X1–X4) | ~35 |
| **Effective model-coverage** | **~96% of usable maths** |

## Part-map (model count + core engine)
| Part | Area | Models | Kaunsa ENGINE |
|---|---|---|---|
| 1 | Percentage • P&L • Discount | 34 | MULTIPLIER (1±x/100) — sab kuch isi se |
| 2 | Ratio • Average • SI/CI • Partnership | 25+5sub | equal-distribution + (1+r)ⁿ compound |
| 3 | Time&Work • Pipes • Speed/Train/Boat | 17+4sub | LCM-units + relative speed (±) |
| 4 | Number System • Algebra • Simplification | 24 | 6 identities (I1–I6) + divisibility place-value |
| 5 | Geometry (T/C/Q) | 20 | angle-sum 180 + inscribed-law (centre = 2×) |
| 6 | Mensuration 2D/3D | 14 | ½bh se sab areas; base×h/⅓; ×k²,×k³ |
| 7 | Trigonometry | 10 | DO triangles (45/30-60) + sin²+cos²=1 |
| 8 | Data Interpretation | 17 (12 reading + engines) | reading + Part 1/2 engines; ×3.6 pie |
| 9 | Mixture + Leftovers (ye file) | 9 | alligation cross + (1−x/T)ⁿ |

## Consolidated MINIMUM-RATTA (poore system ke liye — bas yeh, baaki sab derive)
1. **Fraction↔%:** 1/6=16.67, 1/7=14.28, 1/8=12.5, 1/9=11.11, 1/11=9.09, 1/12=8.33 (baaki 100÷n se)
2. **Squares 1–30, cubes 1–12** (+ 15³=3375, 25⁴=390625 type SSC-favourites)
3. **Triples:** (3,4,5)(5,12,13)(8,15,17)(7,24,25)(9,40,41) + 8-15-17/5-12-13 ke multiples
4. **√2≈1.414, √3≈1.732, √5≈2.236** • **π=22/7** (7-multiples par) ya 3.14
5. **x±1/x cascade:** x²+1/x² = k²∓2; x³+1/x³ = k³∓3k (sign flip yaad)
6. **1.1ⁿ (1.21, 1.331), 1.05², 1.04ⁿ** — CI anchors
7. **km/h→m/s ×5/18** ke common: 36→10, 54→15, 63→17.5, 72→20, 90→25
8. **Pie: % = degrees ÷ 3.6** (90°=25%, 36°=10%)
9. **Unit:** 1 m³ = 1000 L; equilateral r = a√3/6, R = a√3/3
10. **Trig:** sirf DO triangles ka diagram (45-45-90, 30-60-90) — table isi se

## TOP-15 TRAPS (poore system ke — sabse zyada repeat hone wale)
1. ±x% successive ≠ 0 → net **−x²/100** (Part 1-A5)
2. Same-SP ±x% pair → guaranteed **loss x²%** (Part 1-B6)
3. Successive discounts ADD nahi hote — **d₁d₂/100** bachta (Part 1-C2)
4. "x% of REMAINING" = naya base (Part 1-A10)
5. Election ki 3 layers: registered→cast→valid (Part 1-A8)
6. **n times = (n−1)×P** ka SI (Part 2-I2)
7. Half-yearly CI: **rate ÷2, periods ×2** (Part 2-I8)
8. Equal-distance avg speed = **harmonic** (Part 2-V6)
9. Efficiency x% more ⇒ days **×100/(100+x)** (Part 3-W3)
10. Overtake: speeds SUBTRACT, lengths ADD (Part 3-S8)
11. Masked digits: co-prime split (88 = 8×11), saare pairs check (Part 4-N2)
12. a³+b³+c³ = 3abc ⇔ a+b+c = 0 (Part 4-I5)
13. Similar triangles: area-ratio = side-ratio ka **SQUARE** (Part 5-T6)
14. "Same wire bent" = LENGTH conserve; "melted" = VOLUME conserve (Part 6-H5)
15. Pie "X exceeds Y" — **"of the total"** (degree-diff) vs "of Y" (Part 8-P4)

## DATA-DRIVEN SKIP-LIST (7 saal, 193 papers me YE NAHI AAYA — padha to time waste)
- Wages distribution & grazing (Part 3) — **0 Q**
- Height-distance trig tables (Part 7) — 6 Q, wo bhi similar-triangles se
- LCM/HCF deep theory (Part 4) — 2 Q
- Recurring decimals (Part 4) — ~0 Q
- Euler/polyhedra — 1 Q (formula 1 line)
- Installments — 5 Q (basic 2-step hi)

## Dataset-integrity summary (poore project ka)
- ~150+ PYQ solutions independently **compute-verified**
- 8 dataset-answer discrepancies flagged (student-chosen-options galat the — sab correct math ke saath)
- ~35 questions `[SOURCE UNCLEAR]` (OCR-unrecoverable) — **kuch bhi invent NAHI kiya**
- GA-contamination identified & excluded (~40 questions jo math-file me leak the)

---
**PROJECT COMPLETE: 193 papers • 4,825 PYQs • 170 model-entries (+~25 sub-models ≈ 195 total) • ~96% usable-coverage • zero-filler**
