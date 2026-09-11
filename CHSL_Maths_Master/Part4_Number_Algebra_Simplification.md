# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 4: NUMBER SYSTEM • ALGEBRA • SIMPLIFICATION

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). Is Part ke areas ke **~640 actual questions**: Number System 139 • Algebra ~440 clean (515 raw me se ~75 geometry-leaks nikale) • Simplification 61.
Har solution independently verified. OCR-garbled PYQs par `[SOURCE UNCLEAR]`.

**Part map:** 1 Commercial ✅ | 2 Ratio/Avg/Interest ✅ | 3 T&W/Speed ✅ | **4 (ye file)** | 5 Geometry | 6 Mensuration | 7 Trigonometry | 8 DI | 9 Mixture+Index

---
---

# SECTION 0 — FOUNDATION: THE IDENTITY ENGINE
*(Algebra ke 90% questions in 6 identities se bante hain — sab yahan DERIVE hain, ratta zero)*

**I1. (a±b)² = a² ± 2ab + b²** — derive: (a+b)² = (a+b)(a+b) = a²+ab+ba+b² = a²+2ab+b² (distributive law bas).
**I2. a² − b² = (a+b)(a−b)** — derive: (a+b)(a−b) = a²−ab+ab−b². Middle terms cancel.
**I3. (a±b)³ = a³ ± b³ ± 3ab(a±b)** — derive: (a+b)³ = (a+b)²(a+b) = (a²+2ab+b²)(a+b) expand karo.
**I4. a³ ± b³ = (a±b)(a² ∓ ab + b²)** — derive: I3 ko rearrange karo: a³+b³ = (a+b)³ − 3ab(a+b) = (a+b)[(a+b)²−3ab] = (a+b)(a²−ab+b²).
**I5. a³+b³+c³−3abc = (a+b+c)(a²+b²+c²−ab−bc−ca)** — aur iska COROLLARY (SSC ka favourite):
**a+b+c = 0 ⇒ a³+b³+c³ = 3abc**
**I6. (a+b+c)² = a²+b²+c²+2(ab+bc+ca)** — I1 ka 3-variable version.

**Surd rationalization (derive):** 1/(√a+√b) × (√a−√b)/(√a−√b) = **(√a−√b)/(a−b)** — I2 ka use.

**📦 Minimum-ratta:** squares 1–30 • cubes 1–12 • x±1/x cascade (neeche A3 me derive hai, phir ratta) • unit-digit cycles (N4 me derive).

---
---

# SECTION N — NUMBER SYSTEM (11 models • 139 PYQs)

---

## ▌N1. DIVISIBILITY TESTS (with derivations)
**DATA: 84 Q — sabse bada NS model. Har saal 3-5 Q.**

**Rules (derive karke samjho, ratto nahi):**
- **2/5/10:** last digit par hi depend (10 ke factors) — place value: sab positions 10 se divide, sirf units bacha
- **4/8:** last 2/3 digits (100 = 4×25, 1000 = 8×125 — higher powers 8 se divide ho jaati hain)
- **3/9:** digit-sum (kyunki 10 ≡ 1 mod 3 ya 9 — har 10 ki power ≡ 1, to sab digits ka sum bachta hai)
- **11:** alternating sum (10 ≡ −1 mod 11 → odd positions +, even positions −)
- **Composite = co-prime split:** 22 = 2×11, 24 = 8×3, 75 = 3×25, 88 = 8×11, 15 = 3×5 — dono tests pass hone chahiye
**PYQ 1** [2024|Q9]: `Divisible by 22?` → 2×11: 893002 even ✓; alt-sum (8+3+0)−(9+0+2) = 0 ✓ → **893002** ✓
**PYQ 2 (NOT wala)** [2023|Q16]: `NOT divisible by 24 (8×3)?` → 35751 odd hai → 8 par hi fail → **35751** ✓
**PYQ 3 (NOT, 75 = 3×25)** [2021|Q55]: `NOT divisible by 75?` → 163750: ÷25 ✓ (50 se end) par digit-sum 22 → ÷3 fail → **163750** ✓
**Trap:** "NOT divisible" me EK test fail karna kaafi hai — poora divide karke mat baitho. Odd number dekho to 8/4/2 wala test turant karo.

---

## ▌N2. MASKED-DIGIT DIVISIBILITY (x, y digits) ⭐⭐ — SSC ka repeat-favourite
**DATA: 9+ Q (88 wale 2019 me 3 shifts, 2022, 2023 me 2-2; 9/11 combos 2022) — 2024 me bhi.**

**Universal:** dono co-prime factors ke liye x, y ki constraints likho, phir combine karo.
**PYQ 1 (A+B nikalo)** [2022|Q7]: `73A215 ÷ 11 aur 56B26 ÷ 9 → A+B?` →
11: alt-sum (7+A+1)−(3+2+5) = A−2 ≡ 0 → **A = 2**; 9: digit-sum 19+B ≡ 0 → **B = 8** → **A+B = 10** ✓
**PYQ 2 (least x+y, 88)** [2023|Q2]: `780x533y24 ÷ 88 (8×11) → least x+y?` →
÷8: last-3 = 3y24: 324+10y ≡ 0 (mod 8) → 4+2y ≡ 0 → y ∈ {2, 6}
÷11: alt-sum (right se) = x+y−2 ≡ 0 → x+y ∈ {2, 13}
Least: y = 2, x = 0 → **x+y = 2** ✓
**PYQ 3 (2019 classic, 3 shifts me same)** `1230x558y2 ÷ 88 → 5x−5y?` →
÷8: 8y2 = 802+10y ≡ 0 → y ∈ {3, 7}; ÷11: 8−x−y ≡ 0 → x+y = 8 → (x,y) = (5,3) → 5(5)−5(3) = **10**; (1,7) → −30 — positive wala SSC answer hota hai
**PYQ 4 (⚠️ dual-solution)** [2022|Q11]: `2x64y ÷ 88 → 6x−5y?` →
÷8: 640+y ≡ 0 → y ∈ {0, 8}; ÷11: 4+y−x ≡ 0 → x = y+4 → (4,0) → 24 YA (12,8) invalid... (x=1,y=8): 21648 = 88×246 ✓ bhi divide hota hai → **−34** (dataset) ya 24 — dono mathematically valid; SSC ne −34 liya. *[DUAL SOLUTION — method hi kaam hai, options dekho]*
**Trap:** "least value" / "greatest value" / "x²+y²" — combine karke JITNE valid pairs bante hain sab check karo, sirf pehla nahi.

---

## ▌N3. REMAINDER BASICS
**DATA: 27 Q.**

**PYQ 1 (chhota divisor)** [2024|Q11]: `N ÷ 512 → remainder 67. N ÷ 32?` →
512 = 32×16 → N ≡ 67 (mod 32) → 67 − 64 = **3** ✓
**PYQ 2 (last-digits se)** [2021|Q62]: `8127 ÷ 8?` → 8 ke liye last 3 digits: 127 = 8×15+7 → **7** ✓
**PYQ 3 (algebraic)** [2019|Q19]: `(6n+3)² ÷ 9?` → 36n²+36n+9 = 9(4n²+4n+1) → **0** ✓
**PYQ 4 (division-sum relation)** [2023|Q5]: `Divisor = 11×quotient = 5×remainder; remainder = 44 → dividend?` →
d = 5×44 = 220; q = 220/11 = 20; D = dq+r = 220×20+44 = **4,444** ✓
**Logic:** N = dq + r hamesha. Chhote divisor ke liye: r ko usi se phir se divide karo.

---

## ▌N4. UNIT DIGIT (power cycles) — derive, phir 5-second
**DATA: 2 direct (194^102 type) par guaranteed 1 Q har naye paper me.**

**Cycles (khud check karke dekho — pattern hi hai):**
- 0,1,5,6 → **constant**
- 4,9 → cycle 2 (4,6,4,6… / 9,1,9,1…)
- 2,3,7,8 → cycle 4 (2: 2,4,8,6…)
**Rule:** power ko 4 se divide karo — bacha (remainder) hi position batata hai; remainder 0 → cycle ka 4th (last) element.
**PYQ** [2018|Q51]: `Unit digit of 194¹⁰² + 294¹⁰³?` →
4-cycle: even power → 6; odd → 4 → 194¹⁰² → **6**, 294¹⁰³ → **4** → 6+4 = 10 → unit **0** ✓
**Trap:** 4 ki odd power = 4, even = 6 — ulta yaad mat karo (4¹ = 4 se yaad rakho).

---

## ▌N5. PRIMES (range counting)
**DATA: 7 Q — "primes between a and b" har 2-3 saal me.**

**PYQ 1** [2022|Q72]: `Primes between 100 and 120?` → 101, 103, 107, 109, 113 → **5** ✓
**PYQ 2** [2017|Q62]: `Sum of primes between 30 and 42?` → 31+37+41 = **109** ✓
**Fastest:** range me even/5/3 ke multiples kaato — bacha kucha hi check karo. 100–120: 101, 103 (skip 105, 109 ✓, 111 = 3×37, 113 ✓, 117 = 9×13, 119 = 7×17).

---

## ▌N6. LCM/HCF — sirf 2 Q (honest data finding)
**DATA: 2 Q in 7 years — deep theory SKIP karo, bas ye 2 concepts:**
- **HCF × LCM = product** (do numbers ke liye; derive: HCF common part, LCM full part, common part ek hi baar gin lo)
- Polynomial LCM = factor karke har factor ki highest power
**PYQ 1** [2017|Q254]: `HCF = 11, LCM = 825, ek number 275 → doosra?` → 11×825/275 = **33** ✓
**PYQ 2** [2021|Q58]: `LCM of (x³−8)(x+1) and (x³+1)(x−2)?` →
x³−8 = (x−2)(x²+2x+4); x³+1 = (x+1)(x²−x+1) → LCM = **(x+1)(x−2)(x²+2x+4)(x²−x+1)** ✓
*(I4 identity ka direct use — algebra-bridge)*

---

## ▌N7. TWO-DIGIT NUMBER PROBLEMS (digit reversal)
**DATA: 11 Q.**

**मूल Logic:** number = 10a+b (place value). Reversed = 10b+a.
- **Difference (reversed − original) = 9(b−a)** — derive: 10b+a−10a−b = 9(b−a)
- **Sum = 11(a+b)**
**PYQ 1** [2024|Q20]: `Digit-sum 9; reversed exceeds by 45 → original?` →
9(b−a) = 45 → b−a = 5; a+b = 9 → b = 7, a = 2 → **27** ✓
**PYQ 2 (form banana)** [2017|Q169]: `Unit digit y, tens 5 → number?` → **50+y** ✓
**Fastest:** 9(b−a) = difference — 45/9 = 5 turant. (Reverse me POSITIVE difference = reversed bada.)

---

## ▌N8. CONSECUTIVE NUMBERS / AP-sums (number side)
**PYQ 1** [2022|Q6]: `3 consecutive even, sum 126 → smallest×largest?` → middle = 42 → 40, 44 → **1,760** ✓
**PYQ 2** [2022|Q51]: `Sum of ALL two-digit odd numbers?` → 11+13+…+99: 45 terms → (11+99)×45/2 = **2,475** ✓
**PYQ 3** [2021|Q72]: `Two-digit numbers ÷ 6 kitne?` → 12 to 96: (96−12)/6+1 = **15** ✓
*(Counting = AP: (last−first)/step + 1 — ye formula bhi derive hai: kitne steps fit hue)*

---

## ▌N9. SURD/NUMBER COMPARISON (largest among mixed)
**PYQ** [2018|Q252]: `Largest among 2, 3√3, 4, 3√5 type?` →
**Method: sab ko square karo** (positive numbers me order preserve hota hai): 4, 27, 16, 45 → largest nikal lo.
3√3 vs 3√5 wale me coefficient same — seedha andar wali value compare.

---

## ▌N10. DIGITS REQUIRED FOR PAGE-NUMBERING
**PYQ** [2024]: `428 pages ki numbering me kitne digits?` →
1–9: 9 digits; 10–99: 90×2 = 180; 100–428: 329×3 = 987 → total **1,176** ✓
*(Place-value segments — formula nahi, segments gin lo)*

---

## ▌N11. PATTERN-SERIES SIMPLIFICATION
**DATA: 3-4 clean Q — 2022 me 2.**

**PYQ 1 (alternating)** [2022|Q67]: `1−7+2−8+3−9+… 100 terms?` →
50 pairs, har pair (k − (k+6)) = −6 → **−300** ✓
**PYQ 2 (square-difference chain)** [2022|Q4]: `98²−97²+96²−95²+…+12²−11²?` →
Har pair: a²−(a−1)² = 2a−1 (I2 se: (a+a−1)(a−a+1)) → 195, 191, 187, … (44 terms, d = −4)
Sum = 44/2 × (195+13) = 22×208... check last: 12²−11² = 23... wait series 195, 191, …, 23: n = (195−23)/4+1 = 44 → sum = 44×(195+23)/2 = **4,796** ✓
**Model:** series me PAIR banao → har pair ek value → wahi AP ban gaya.

---
---

# SECTION A — ALGEBRA (13 models • ~440 clean PYQs + SIMP 61)

---

## ▌A1. IDENTITY SUBSTITUTION (seedha plug-in)
**DATA: A4-family ~156 (me se clean ~120) — sabse bada algebra model.**

**PYQ 1** [2023|Q17]: `(a²+b²−c²)² − (a²−b²+c²)² ÷ (b²−c²)?` →
I2: x²−y² = (x+y)(x−y); x+y = 2a², x−y = 2(b²−c²) → 4a²(b²−c²)/(b²−c²) = **4a²** ✓
*(Pehchana: dono squares ka difference = I2 ka costume)*
**PYQ 2** [2017|Q66]: `Coefficient of x in (x+9)(8−5x)?` → 8x−45x = **−37** ✓
**PEHCHAN-TRIGGER:** "x²−y² dikhe → (x+y)(x−y) likho TEEN second me. Squares ka ± → I2/I1. Cubes → I3/I4."

---

## ▌A2. IDENTITY-FRACTION (a³±b³)/(a²∓ab+b²) ⭐ — 2023 ka favourite
**DATA: 15 Q decimal-version me (2023 me hi multiple shifts), fraction-versions alag.**

**मूल Logic:** I4 ulta padho: (a³−b³)/(a²+ab+b²) = **a−b**; (a³+b³)/(a²−ab+b²) = **a+b**.
Decimal numbers dikhen to unhe a, b banao (0.24, 0.2 wale) — koi cube nikaalna nahi padta!
**PYQ 1** [2023|Q6]: `(0.24×0.24×0.24 − 0.008)/(0.24×0.24 + 0.048 + 0.04)?` →
a = 0.24, b = 0.2 (0.008 = 0.2³, 0.048 = 0.24×0.2) → answer = a−b = **0.04** ✓
**PYQ 2 (same family)** [2023|Q12]: `(4.2)³ − 0.008 … / (4.2)² + 0.84 + 0.04` → a = 4.2, b = 0.2 → **4** ✓
**Pehchana:** denominator me +ab wala pattern aur numerator me cube-difference — bas a−b likh do. **Ye 2023 me 4+ shifts me aaya — guaranteed repeat.**

---

## ▌A3. x ± 1/x CASCADE ⭐⭐ — evergreen (31+ Q, kabhi nahi rukta)
**DATA: 2017 se 2024 tak har saal. 2019 me 3 shifts me same questions.**

**Derive (ek baar, phir table 2-second):**
x + 1/x = k → x² + 1/x² = **k² − 2** (square karo, cross-term 2)
→ x⁴ + 1/x⁴ = (k²−2)² − 2 → x³ + 1/x³ = **k³ − 3k** (cube karo: x³+1/x³ + 3(x+1/x) = k³)
x − 1/x = m → x²+1/x² = m²+2 (sign flip!), x³−1/x³ = m³+3m
**PYQ 1** [2022|Q74]: `x² + 1/x² = 14 → x³ + 1/x³?` → x+1/x = √16 = 4 → 64−12 = **52** ✓
**PYQ 2 (deep cascade)** [2021|Q59]: `x⁴ + 1/x⁴ = 2207 → x⁵ + 1/x⁵?` →
x²+1/x² = √2209 = 47 → x+1/x = √49 = 7 → x³+1/x³ = 322
x⁵+1/x⁵ = (x²+1/x²)(x³+1/x³) − (x+1/x) = 47×322 − 7 = **15,127** ✓
*(x⁵ rule derive: x⁵+1/x⁵ = x²(x³)+… multiply karke x⁵+x⁻⁵ + x+x⁻¹ = (x²+x⁻²)(x³+x⁻³))*
**PYQ 3 (surds se entry)** [2019, 3 shifts]: `x = 2+√3 → x³+1/x³?` →
1/x = 2−√3 (rationalize) → x+1/x = 4 → 64−12 = **52** ✓
**PYQ 4 (K-version, twisted)** [2022|Q69]: `x + 1/x = K/2 → x⁴ + 1/x⁴?` →
x²+1/x² = (K²−8)/4 → x⁴+1/x⁴ = [(K²−8)²/16] − 2 = **(K⁴−16K²+32)/16** ✓
**Trap:** 2207-type me √(2207+2) = √2209 = 47 — **+2 andar** (k²−2 ulta), aur perfect square hona chahiye (2209 = 47², 49 = 7² — SSC jaan-boojh kar perfect squares deta hai).

---

## ▌A4. a+b+c / SUM-PRODUCT FAMILY
**DATA: 67 raw (~50 clean) — 2 sub-models:**

**Sub-1 (a+b+c given):** I6 ulta: a²+b²+c² = (a+b+c)² − 2(ab+bc+ca)
[2022|Q56]: `(a+b+c) = 7, ab+bc+ca = 12 → a²+b²+c²?` → 49−24 = **25** ✓
Aur **I5-corollary**: a+b+c = 0 → a³+b³+c³ = 3abc
[2019|Q4]: `(3x−7)³+(3x−8)³+(3x+6)³ = 3(3x−7)(3x−8)(3x+6) → x?` →
a³+b³+c³ = 3abc ka matlab: **a+b+c = 0** (ya a=b=c) → 9x−9 = 0 → **x = 1** ✓
*(Pehchan-trigger: teen cubes + 3abc dikhe = a+b+c = 0 likho, 5 second me answer)*

**Sub-2 (sum & product given, expression nikaalo):** expression ko identities me kholo:
[2023|Q10]: `a+5b = 13, ab = 9 → a²+25b²?` → (a+5b)² − 10ab = 169−90 = **79** ✓
[2021|Q69]: `a+b = 8, a−b = 6 → ab?` → ((a+b)²−(a−b)²)/4 = 28/4 = **7** ✓
[2022|Q8]: `p+q = 5, pq = 18 → p³+q³?` → 125−270 = **−145** *(dataset me 145 — magnitude; p,q is case me complex hote hain, sign SSC ne ignore kiya. Method wahi: (p+q)³−3pq(p+q))* `[SIGN — SOURCE AMBIGUOUS]`

---

## ▌A5. LINEAR SYSTEMS (2-3 equations)
**PYQ** [2024|Q20]: `x+y+z = 15, 2x−y+z = 12, x−y−z = −1?` →
Eq1+Eq3: 2x = 14 → x = 7 → y+z = 8; Eq2: 14−y+z = 12 → z−y = −2 → **(7, 5, 3)** ✓
**Method:** elimination cascade — koi bhi do equations add karo jo ek variable kaatein. Options hai to values test karna bhi 10-second ka kaam hai.

---

## ▌A6. COORDINATE LINES (mini-model, 5 Q)
**DATA: 2024 me 3 (naya push), 2020 me 2.**

**PYQ 1 (intercepts)** [2024|Q7]: `5x+12y = 60, axes ke beech ka intercepted length?` →
x-int (y=0): 12; y-int: 5 → length = √(144+25) = **13** *(5-12-13 triple!)* ✓
**PYQ 2 (intersection on line)** [2024|Q11]: `x+y = 2, 2x−y = 1 ka intersection y = Kx+5 par → K?` →
3x = 3 → (1,1) → 1 = K+5 → **K = −4** ✓
**PYQ 3 (infinite solutions)** [2024|Q17]: `kx+3y−(k−3) = 0, 12x+ky−k = 0 infinite solutions → k?` →
ratios equal: k/12 = 3/k = (k−3)/k → k² = 36 → k = 6 (check: 6/12 = 3/6 = 3/6 ✓) → **k = 6**
**PYQ 4 (point-slope)** [2020|Q13]: `(3,−5) se slope 2?` → y+5 = 2(x−3) → **2x−y−11 = 0** ✓
*(Line ke saare models ek hi cheez hain: y = mx+c aur I2-Pythagoras)*

---

## ▌A7. SURDS RATIONALIZATION (combined) ⭐
**PYQ** [2018|Q164]: `x = 1/(√5+√3), y = 1/(√7+√5), z = 1/(√7+√3) → x+y+z?` →
x = (√5−√3)/2, y = (√7−√5)/2, z = (√7−√3)/4
x+y = (√7−√3)/2 → +z = (√7−√3)(1/2+1/4) = **(3/4)(√7−√3)** ✓
**Model:** 1/(√a+√b) ko rationalize karo, phir SAME surd wale terms group ho jaate hain — chains cancel.

---

## ▌A8. STATEMENT TRUE/FALSE (surd inequalities)
**PYQ** [2018|Q64]: `I. 4√3 > 3√4 II. 8√2 > 2√8?` →
4√3 = 6.93 > 6 ✓; 8√2 = 11.31 > 5.66 ✓ → **Both true** ✓
**Method:** approximate values ratta-box se (√2≈1.414, √3≈1.732, √5≈2.236) — 5 second me dono check.

---

## ▌A9. BODMAS / "OF" PRECEDENCE
**DATA: 52 Q SIMP-family ka core.**

**Rule:** **B-O-DM-AS** — "of" = brackets ke turant baad (multiplication hi hai par pehle).
**PYQ 1** [2022|Q62]: `15 − 3 of 12 ÷ 2 + 3 of 2 ÷ 2?` →
(3 of 12)÷2 = 18; (3 of 2)÷2 = 3 → 15−18+3 = **0** ✓
**PYQ 2** [2021|Q53]: `11.5 − [5 + 0.5×(9−3×2)]?` →
inner: 9−6 = 3 → 0.5×3 = 1.5 → 5+1.5 = 6.5 → **5** ✓
**Trap:** "÷" aur "of" ka order — of pehle. Aur minus ke baad brackets: 15−18+3 me log 15−21 kar dete hain (sign spread).

---

## ▌A10. PERFECT-SQUARE DETECTION (decimal chains)
**PYQ** [2018|Q64]: `√(3⁴ + 12²)?` → 81+144 = 225 → **15** ✓
**Model:** a²+b² ko dekho — agar (hypotenuse)² ban raha hai (3-4-5 family: 9-12-15) to seedha root nikalo. Decimals me bhi yahi (5.4−0.4 type pairs — `(a−b)² = a²−2ab+b²` recognize karo).
**Ratta-box:** Pythagorean triples (3,4,5) (5,12,13) (8,15,17) (7,24,25) (9,40,41) — SSC inhi se banata hai.

---

## ▌A11. POLYNOMIAL EXPANSION (about a point)
**PYQ** [2021|Q53]: `x²+2x+3 ko x = −2 ke around expand karo?` →
u = x+2 (x = u−2): (u−2)²+2(u−2)+3 = u²−2u+3 → **(x+2)² − 2(x+2) + 3** ✓
*(Computed answer option-B pattern hai; dataset copy me option-order OCR-shuffled `[SOURCE UNCLEAR: option order]` — method pakka hai: substitute karo, wapas karo)*

---

## ▌A12. EXPONENT LAWS in expressions
Powers ko dekh ke base same karo: 9 = 3², 8 = 2³, 0.25 = (0.5)² — phir add karo (multiplication me powers ADD, power-of-power me MULTIPLY).
*(2024 me exponents wale 2-3 Q OCR-hit the — model basic hai: same base = add exponents.)*

---

## ▌A13. %-SIMPLIFICATION & mixed BODMAS
[2022|Q61-type]: `60% of 870 − √1444 + 18×19` → % ko fraction banao (60% = 3/5), phir BODMAS.
*(Is family ke several 2022-24 Q OCR-garbled — pattern: % → fraction, root → value, phir left-to-right DM-AS.)*

---
---

# PART 4 MASTER TRAPS (dataset-verified)

| # | Trap | Evidence |
|---|---|---|
| 1 | **NOT divisible me ek test fail = kaafi** (odd → 8 fail) | 35751 |
| 2 | Masked digits: **saare valid (x,y) pairs** check karo — "least/greatest" | 780x533y24 → 2 |
| 3 | 88 = 8×11 — co-prime SPLIT zaroori (88 ka direct rule nahi) | N2 sab |
| 4 | Remainder chhote divisor par: 67 mod 32 = 3 (64 nikaal ke) | 2024 |
| 5 | Unit digit 4⁰⁰⁺: even→6, odd→4 (4¹ = 4 se yaad) | 194^102 |
| 6 | x²+1/x² = k → √(k+2) ANDAR (+2), perfect square hona chahiye | 2207→47→7 |
| 7 | x−1/x cascade me SIGN flip (+2/+3m) | A3 |
| 8 | a³+b³+c³ = 3abc ⇔ a+b+c = 0 — teen cubes dikhe to seedha yehi | x = 1 |
| 9 | (a³−b³)/(a²+ab+b²) = a−b — cube calculate karne hi nahi hain | 0.24 |
| 10 | "of" BODMAS me ÷ se PEHLE | 15−18+3 = 0 |
| 11 | 2-digit reversal: diff = 9(b−a), sum = 11(a+b) | 27 |
| 12 | Coefficient ke signs: (x+9)(8−5x) → 8−45 = −37 | 2017 |
| 13 | Intercept-length = √(x-int²+y-int²) — triple pehchano (5-12-13) | 13 |
| 14 | Infinite solutions: teeno ratios equal (sirf do nahi) | k = 6 |

---

# PART 4 COVERAGE AUDIT (dataset ke against)

- Part-4 areas: NUM 139 + ALG 515 raw (~75 △-geometry leaks excluded → ~440) + SIMP 61 → **~640 questions, 24 models me ~92% mapped**
- **Data-driven findings:**
  - **Divisibility = NS ka 60%** (84 Q) — aur 88 wale masked-digit 9 Q ka repeat family (2019 me 3 shifts me SAME question)
  - **Identity-fraction (a³−b³)/(a²+ab+b²) = 2023 ka discovery** — 4+ shifts me decimal costume me aaya
  - **x±1/x cascade 31 Q** — 7 saal me kabhi skip nahi hua; 2019 me 3 shifts same
  - **LCM/HCF sirf 2 Q** — theory skip, 2 concepts kaafi (honest finding)
  - **Recurring-decimal conversions = ~0 clean Q** — skip
  - Unit digit sirf 2 direct Q — par 1 formula-cycle kaafi
  - Coordinate lines 2024 me aaye (3 Q) — naya push, 4 mini-models ready
- Baaki bache: 2024 ke ~12 heavy-OCR expression questions (options unreadable) `[SOURCE UNCLEAR]` — models unke equivalent hain, sirf numbers nahi the
- Dataset-answer discrepancies: 3 flagged (p³+q³ sign-145; polynomial-expansion option-order; 2x64y dual-solution ±24/−34) — sab verified-compute ke saath
- Cross-part dedupe: 70% of (x−y) type equations Part-1 A3 me; geometry-leaks (△ABC wale ~75 Q) Part 5 me jayenge; √-based mensuration Part 6

**Part 4 → 24 models, ~92% coverage, 45+ verified PYQ solutions.**
