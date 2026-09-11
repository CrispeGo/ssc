# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 1: COMMERCIAL ARITHMETIC — Percentage • Profit & Loss • Discount

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). Is Part me jo 3 areas hain
unke **1,102 actual questions** ka poora model-analysis: **PCT 635 + P&L 191 + Discount 276**.
Har model ke saath real PYQ evidence diya hai `[year | shift]` tag me.

**Source integrity:** Image-paper answers "Chosen Option" (student ka response) hote hain — 100% official nahi.
Is file ka **har solution independently compute karke verify kiya gaya hai**; jahan dataset-answer galat tha wahan flag kiya.
OCR-garbled questions par `[SOURCE UNCLEAR]`.

**Part map (poora project):**
| Part | Coverage | Status |
|---|---|---|
| **1** | **Percentage + P&L + Discount (ye file)** | ✅ |
| 2 | Ratio • Average • SI/CI • Partnership | next |
| 3 | Time&Work • Pipes • Speed/Train/Boat | |
| 4 | Number System • Algebra • Simplification | |
| 5 | Geometry | |
| 6 | Mensuration 2D/3D | |
| 7 | Trigonometry | |
| 8 | DI (Table/Bar/Pie/Line models) | |
| 9 | Mixture/Alligation + misc models + Master Index | |

---
---

# SECTION 0 — FOUNDATION ENGINE
*(Ye 5 tools sab 34 models ka base hain — ek baar samjho, sab jagah chalega)*

**F1. Percent ka matlab:** x% = x/100. Bas. "per-cent" = "per hundred".
Isliye 20% of 350 = 350 × 20/100 = 70. Har % question ka heartbeat yahi hai.

**F2. Fraction ↔ % (derive karo, ratta nahi):**
1/n ko % me maango to **100 ko n se divide karo**:
- 1/8 = 100/8 = **12.5%** • 1/6 = 100/6 = **16.67%** • 1/7 = **14.28%** • 1/9 = **11.11%** • 1/11 = **9.09%** • 1/12 = **8.33%**
Reverse: 12.5% = 12.5/100 = 125/1000 = **1/8**.
Farak sirf ×100 ya ÷100 ka hai. Jo 6 values upar hain wo exam-frequency ki wajah se
"minimum-ratta box" me jaati hain (neeche Section 0 end me).

**F3. MULTIPLIER (sabse powerful tool):**
- "+x% ho gaya" ⇒ naya = purana × **(1 + x/100)**
- "−x% ho gaya" ⇒ naya = purana × **(1 − x/100)**
*Derivation:* +x% matlab purane me purane ka x/100 add hua: n + nx/100 = n(100+x)/100.
**2 ya 2 se zyada changes = multipliers ko multiply karo.** Ye PART 1 ke 80% questions ka universal method hai.

**F4. % change ka formula (aur uska base):**
% change = (new − old)/old × 100 — **base hamesha wo cheez jisse compare kar rahe ho (old)**.
"A, B se kitna % badha" ⇒ base B. "B, A se kitna % ghata" ⇒ base A. **Base badla = answer badla.**

**F5. "x% more" ka exact ulta:**
A = B(1 + x/100) ⇒ B = A × 100/(100+x) ⇒ B is **x/(1+x/100)** % less than A (100 se divide karke).
- 25% more ⇔ 20% less (25/125 = 20%) • 20% more ⇔ 16.67% less • 50% more ⇔ 33.33% less
Ye pair DERIVE hota hai, rattne ki zarurat nahi — base 100 lo: B=100→A=125; (125−100)/125 = 20.

**📦 MINIMUM-RATTA BOX (sirf yahi 7 + squares 1–20 + cubes 1–10):**
1/2=50, 1/3=33.33, 1/4=25, 1/5=20, 1/6=16.67, 1/7=14.28, 1/8=12.5, 1/9=11.11, 1/11=9.09, 1/12=8.33, 1/16=6.25
Baaki sab (1/13, 1/14...) kabhi nahi poocha gaya dataset me — 100÷n se nikal lo.

---
---

# SECTION A — PERCENTAGE MODELS (15 models • 635 PYQs)

---

## ▌A1. % ↔ FRACTION ↔ RATIO ↔ DECIMAL CONVERSION
**DATA: 2024 me direct conversion questions aaye (12.75%→?, 28%→ratio, 20%,0.5%,0.03%→decimals) — 2017–23 me rare. 2024 ka naya favourite.**

**Logic:** x% = x/100 (fraction) = x÷100 (decimal, point 2 left) = x:100 (ratio).
**Method:** % → fraction: x/100 likh, simplify. Decimal: point 2 jagah left.
**PYQ 1** [2024]: `Convert 28% into the form of ratio.` → 28/100 = 7/25 = **7:25** ✓
**PYQ 2** [2024]: `12.75% is equivalent to` → 12.75/100 = 1275/10000 = (÷25) = **51/400**
**PYQ 3** [2024]: `Express as decimals: 20%, 0.5%, 0.03%` → 0.2, 0.005, 0.0003 (0.5% = 0.5/100 = 0.005 — teen digits, log 0.05 likh dete hain ⚠️)

---

## ▌A2. "X% of Y" CHAIN + COMMUTIVITY MAGIC
**Logic:** x% of y = xy/100 = **y% of x** (multiplication commutative). Isliye "x% of y = 150 diya, y% of z = 300 diya, relation?" type me x, y cancel ho jaate hain.
**Universal:** seedha multiply karo, /100 lagao.
**PYQ 1** [2019]: `If x% of y is 150 and y% of z is 300, then relation between x and z:` →
xy/100 = 150, yz/100 = 300 → divide: z/x = 2 → **z = 2x** ✓
**PYQ 2** [2020]: `If 22% of x = 30% of y, then y:x =` → 22x = 30y → y/x = 22/30 = **11:15**
**PYQ 3** [2020]: `18% of 15% of (3/4) of 3800 =` → chain left→right: 3800×3/4 = 2850; ×15/100 = 427.5; ×18/100 = **76.95**
**Fastest:** aise chains me 100s aur fractions ko pehle cancel karo (18×15×3×38 ÷ 10⁴...).
**Trap:** "5% of 2% of 3" ≠ 5+2 % — multipliers: 0.05×0.02×3.

---

## ▌A3. EQUATION MODEL: a% of A = b% of B ⇒ RATIO
**DATA: 34+ PYQs (2018 me 4-5 shifts, ab bhi regular).**

**Logic (derive):** (a/100)A = (b/100)B ⇒ aA = bB ⇒ **A:B = b:a** (cross-cancellation).
Yaad rakhne ka tareeka: jo side par 35% hai (A), uska number opposite (60) aata hai numerator me.
**Universal:** aA = bB ⇒ A/B = b/a. Bas.
**PYQ 1** [2018]: `35% of A = 60% of B. Ratio A:B?` → 35A = 60B → A:B = **60:35 = 12:7** ✓
**PYQ 2** [2018]: `90% of X = 40% of Y and Y = a% of X. Find a.` → 0.9X = 0.4Y → Y = 2.25X → **a = 225** ✓
**PYQ 3** [2022]: `45% of a number = 6/5th of another. Ratio?` → 0.45N₁ = 1.2N₂ → N₁:N₂ = 1.2:0.45 = **8:3** ✓
**Variation (unknown-mix)** [2020]: `If 70% of (x−y) = 30% of (x+y), then y is what % of x?` →
7(x−y) = 3(x+y) → 7x − 7y = 3x + 3y → 4x = 10y → y = 0.4x = **40% of x**
**Trap:** question "y:x" maang raha ho ya "x:y" — order check karo.

---

## ▌A4. COMPARISON & CHAIN COMPARISON (A, B se x% more...)
**DATA: 33 direct + statement-check versions. 2019 ka statement-wala format advanced hai.**

**Logic:** "A is x% more than B" ⇒ A = B(1+x/100). Chain me sabko ek common base (maano E=100) me convert karo, phir compare.
**Universal:** multipliers multiply: A = B×(1+x₁/100)×(1+x₂/100)...
**PYQ 1** [2024]: `Income of P is 40% less than Q. Combined income of P+Q is what % more than P?` →
Q = 100 ⇒ P = 60. Combined = 160. (160−60)/60 = **166.67% = 166⅔% more** ✓
**PYQ 2 (statement-check, advanced)** [2019]:
`A is 20% more than B, B is 25% more than C, C is 60% less than D, D is 20% more than E. Which is true?` →
C ko 100 maano: B = 125, A = 150, D = C/0.4 = 250, E = 250/1.2.
Check option "A is 40% less than D": A/D = 150/250 = 0.6 → 40% less ✓ **ANS** (baaki options jhooth nikle)
**PYQ 3** [2020/2024 repeat]: `Two numbers are 25% and 60% more than a third. Ratio?` → 1.25 : 1.6 = **25:32**
**Trap:** "more than" vs "of" — "A is 20% of B" (A = 0.2B) vs "20% more than B" (A = 1.2B).

---

## ▌A5. SUCCESSIVE % CHANGE (+a% phir −b%)
**DATA: 13 direct + geometry versions 104 (A12 me) + price versions (A7) — milake sabse bada % family.**

**मूल Logic:** dono changes ko multiplier me likho aur multiply karo:
Net multiplier = (1+a/100)(1+b/100). Result >1 ⇒ net increase; <1 ⇒ decrease.
**DERIVED GEM (kayi baar direct aata hai):** +a% phir −a% ⇒ (1+a/100)(1−a/100) = 1 − a²/100²
⇒ **net decrease = a²/100 %.** Examples: ±8% → 0.64% decrease; ±10% → 1% decrease; ±20% → 4% decrease.
**PYQ 1** [2021]: `A number is increased by 10% then decreased by 20%. Net?` → 1.1×0.8 = 0.88 → **12% decrease** ✓
**PYQ 2** [2019]: `+30%, then −25%, then +25% (nearest)?` → 1.3×0.75×1.25 = 1.21875 → **22% increase** ✓
**PYQ 3** [2021]: `Price first +8%, later −8%?` → 1.08×0.92 = 0.9936 → **0.64% decrease** ✓ (formula: 8²/100)
**PYQ 4 (twisted)** [2022]: `Successively decreased 25%, 40%, 20% → 32,904. Original?` →
0.75×0.6×0.8 = 0.36 → x = 32904/0.36 = **91,400** ✓ (A5+A6 combo)
**Fastest:** ±same-a ko formula se; alag-alag ho to multiplier chain. 25–40 jaisi values: 0.75×0.6 = 0.45 turant.
**Trap:** "successive" word na ho tab bhi "increased... then increased" = same model. Order koi farak nahi dalta (multiplication), par signs dhyan se.

---

## ▌A6. REVERSE % — Final diya, original nikalo
**DATA: 4 direct + har doosre model ke andar embedded (DI, P&L, Discount me reverse versions sabse zyada).**

**Logic:** original × multiplier = final ⇒ **original = final ÷ multiplier**. Bas yahi.
**Universal sub-model (k gem):** `Number increased by k, becomes p% of itself` →
x + k = (p/100)x ⇒ k = x(p−100)/100 ⇒ **x = 100k/(p−100)**
**PYQ 1** [2024]: `Number increased by 8 becomes 120% of itself.` → x = 100×8/(120−100) = **40** ✓
**PYQ 2** [2017]: `Increased by 28 becomes 107% of itself.` → x = 2800/7 = **400** ✓
**PYQ 3** [2021]: `Sum increased by 15% becomes ₹19,320.` → x = 19320/1.15 = **₹16,800** ✓
**Fastest:** 1.15 se divide: 19320/1.15 = 19320×20/23 = 840×20 = 16800 (1.15 = 23/20).
**Trap:** % decrease ka reverse: final ÷ (1−x/100) — log (1−x/100) ki jagah direct x% subtract kar dete hain.

---

## ▌A7. PRICE–CONSUMPTION–EXPENDITURE
**DATA: 10 direct (2017–2024), classic + 2024 reverse-twist.**

**मूल Logic:** Expenditure = Price × Quantity (E = P×Q). Dono me change ho raha:
E_new/E_old = (1+p/100)(1−q/100). Tee-no variables isi equation se.
**PYQ 1** [2024]: `Rice cost +25%, consumption −30%. % change in expenditure?` →
1.25 × 0.7 = 0.875 → **12.5% decrease** ✓
**PYQ 2 (restore)** [2017]: `Price cut by 3%. To restore original, new price must be increased by?` →
needed % = x/(100−x) ×100 = 3/97×100 = **3.09%** ✓ (derive: original = new×100/(100−x); increase = x/(100−x))
**PYQ 3 (reverse-twist, 2024)** [2024]: `Pulse price +45%. Increased price ko kitna % reduce kare ki original price wapis aa jaye?` →
same restore formula: 45/145×100 = **31.03 ≈ 31%** (dataset me student ka chosen answer B tha — **sahi answer 31% hai**, options OCR-se unclear `[SOURCE UNCLEAR]` — concept yahi hai)
**Fastest:** restore ka % hamesha original % se KAM hoga (45 → 31). Jo barabar ya zyada dikhe wo trap.

---

## ▌A8. ELECTION MODELS 🗳️
**DATA: 49 PYQs — har saal 2-4 questions. Sabse reliable % application.**

**Layer structure (dimag me ye chain banao):**
REGISTERED voters → (did NOT cast: −x%) → CAST votes → (invalid: −y%) → VALID votes → (split between candidates; majority = winner − loser)
**Universal:** top se neeche aao, multiplier laga ke; ya neeche se upar (divide karke).
**PYQ 1 (basic majority)** [2021]: `One got 20% of total votes and lost by 600. Total votes?` →
winner 80%, diff = 60% of total = 600 → total = **1000** ✓
**PYQ 2 (valid votes layer)** [2022]: `Winner got 60% of VALID votes; 90% votes valid; total 12,000. Votes of loser?` →
valid = 10,800; loser = 40% × 10800 = **4,320** ✓
**PYQ 3 (full 3-layer, 2023)** [2023]: `80% cast; 2% of cast invalid; A got 9,408 = 60% of valid. Total voters?` →
valid = 9408/0.6 = 15,680 → cast = 15680/0.98 = 16,000 → total = 16000/0.8 = **20,000** ✓
**PYQ 4 (invalid + not-cast combo)** [2024]: `10% registered didn't vote; winner got 60% of valid...` — same chain, ulta direction.
**Traps:**
- "60% of VALID votes" vs "60% of TOTAL votes" — base alag!
- Majority (jeet ka margin) = (w% − l%) × base — base valid hota hai agar % valid par diye hain.
- "votes polled" = cast votes (registered nahi).

---

## ▌A9. EXAM MARKS / PASS-FAIL
**DATA: 51 PYQs (A9+A18 overlap), 2024 me negative-marking twist aaya.**

**Logic:** Pass marks = p% of maximum. Student ko m mile, pass se d kam ⇒ m + d = p% of max.
**PYQ 1** [2017×2 shifts]: `Two students: one got 24 more than other; higher wale ka marks = 65% of sum...` type —
equation banao: m₁ = m₂+24, m₁ = 0.65(m₁+m₂).
**PYQ 2 (negative marking — 2024 naya twist)** [2024]:
`160 MCQs; +4 correct; −1 wrong/unattempted (total of correct se); scored 400. Correct answers?` →
4c − (160−c) = 400 ⇒ 5c = 560 ⇒ **c = 112** ✓ (dataset ANS C — options OCR-truncated, answer 112 hi hai)
**Trap:** "1 mark deducted per wrong" — kabhi sirf attempted-wrong par, kabhi unattempted par bhi. Wording dhyan se.

---

## ▌A10. INCOME–EXPENDITURE–SAVINGS
**DATA: 98 PYQs — sabse zyada % application. 3 sub-formats.**

**कभI मत bhoolna:** Income = Expenditure + Savings (I = E + S). Ye equation hi model hai.
**Sub-1 (savings se income):** `spends 68%, saves ₹14,720 → expenses?` [2023] →
saves 32% = 14720 ⇒ I = 46,000 ⇒ E = 68% × 46000 = **₹31,280** ✓
**Sub-2 (charity/% given amount)** [2021]: `8% of income = ₹1,200` → I = **₹15,000** ✓
**Sub-3 (sab kuch badla — 2024 favourite):** [2024] `Rahul spends 70%. Income +15%, expenditure +7.5%. % increase in savings?` →
Base 100 lo: I=100, E=70, S=30. New: I=115, E=75.25 ⇒ S = 39.75. %↑ = 9.75/30 = **32.5%** ✓
**Universal for Sub-3:** hamesha base 100/1000 lo (variables chhodo), S = I−E do baar nikaalo.
**Multi-step advanced (2024)** [2024]: `Aman: food 35% of income; transport = 4/13 of REMAINING; savings ₹6,300 = 20% of balance after food+transport. Income?` →
R₁ = 0.65I; transport = (4/13)(0.65I) = 0.2I; balance = 0.45I; savings = 0.20×0.45I = 0.09I = 6300 ⇒ **I = ₹70,000** ✓
**Trap:** "x% of remaining" — remaining NAYA base banata hai (0.65I), original nahi. Ye sabse common galti hai.

---

## ▌A11. POPULATION / PERIODIC GROWTH
**DATA: 17 direct + DI me versions.**

**Logic:** har saal same r% se badhta hai = COMPOUND effect (multiplierⁿ):
P_n = P₀(1±r/100)ⁿ — derive: har saal puri population ka r/100 add hota hai, to multiplier baar-baar lagta hai.
**PYQ 1** [2021]: `Present 21,000, +10% annually, 3 years me?` → 21000×1.1³ = 21000×1.331 = **27,951** ✓
**PYQ 2 (avg-rate TRAP)** [2018]: `Increase 44% (yr 1) and 75% (yr 2). Average rate of increase?` →
multiplier = 1.44×1.75 = 2.52 → total +152% over 2 yrs → average = 152/2 = **76%** ✓
(Trap answer: (44+75)/2 = 59.5 — galat, kyunki yr-2 ka 75% bade base par laga)
**Fastest:** 10% growth: ×1.1, ×1.21, ×1.331 (ye teen multiplier exam-teer hain).

---

## ▌A12. DIMENSION-% (Geometry + % mixed) — Mensuration ka bridge
**DATA: 104 PYQs — 2017 se 2024 tak har saal. Sabse repeated mixed-model.**

**मूल Logic (ye samajh lo, formula kabhi nahi rattoge):**
- Area = l × b ⇒ l me +a%, b me +b% ⇒ Area multiplier = **(1+a)(1+b)** (A5 wala hi)
- Volume = l×b×h ⇒ teen multipliers ka product
- Cube/sphere me teeno dimensions same r se: side/r +x% ⇒ **Volume multiplier = (1+x)³**, Surface = (1+x)²
**PYQ 1** [2018]: `Rectangle L +40%, B +70%. % increase in area?` → 1.4×1.7 = 2.38 → **138%** ✓
**PYQ 2** [2024]: `Sphere radius +12%. Volume increase (approx)?` → 1.12³ = 1.404928 → **40.49%** ✓
**PYQ 3** [2023]: `Cuboid L +7%, B +6% (H same). Volume?` → 1.07×1.06 = 1.1342 → **13.42%** ✓
**PYQ 4 (side fractions)** [2021]: `Cube ka side triple → surface area?` → multiplier 3² = 9 → **+800%** ✓
**PYQ 5 (⚠️ dataset-answer disputed)** [2022]: `Cylinder r=7, h=5, "bisected from height" (do cylinders bane). % increase in TSA?` →
TSA_original = 2πr(r+h) = 2π×7×12 = 168π. Do naye (h/2 = 2.5): 2×[2π×7×(7+2.5)] = 266π.
Increase = 98π/168π = 7/12 = **58.33%** (option A). Dataset me student ne C (69.44) choose kiya tha — **mathematical answer A hi hai**; question-number verify kar lena original PDF se.
**Fastest:** radius/side % questions me seedha (1+x)² ya (1+x)³ — 12% → 1.12³: 1.12² = 1.2544, ×1.12 = 1.4049 (40.49).
**Trap:** "side increased by 12%" vs "radius increased to 112" — ek % hai, ek absolute.

---

## ▌A13. FRACTION ME NUMERATOR/DENOMINATOR CHANGE
**DATA: 7 direct, twisted format.**

**Logic:** F_new = n(1+a/100) / [d(1−b/100)]. Equation banao, cross-multiply.
**PYQ** [2022]: `Numerator +140%, denominator −20% → resultant 12/7. Original fraction?` →
n×2.4 / (d×0.8) = 12/7 ⇒ (n/d) = 12/7 × 0.8/2.4 = 12/7 × 1/3 = **4/7** ✓
**Fastest:** 2.4/0.8 = 3 (net multiplier 3×) → original = 12/(7×3)... dhyan: resultant/original = 3 ⇒ original = (12/7)/3 = 4/7.

---

## ▌A14. CALCULATION ERROR / WRONG MULTIPLIER
**DATA: 7 direct.**

**Logic:** % error = (wrong − correct)/correct × 100 — **base CORRECT value**.
**PYQ 1** [2021]: `Pupil multiplied by 5 instead of 3. % error?` → (5−3)/3 = **66.67%** ✓
**PYQ 2** [2017]: `Multiplied by 5/7 instead of 7/5. % error?` →
wrong/correct = (5/7)÷(7/5) = 25/49 → error = (49−25)/49 = **48.98%** ✓
**Trap:** 5/7 vs 7/5 ko "thoda sa galat" mat samjho — ratio 25/49 hai, aadhe se bhi kam!

---

## ▌A15. NUMBER-PAIR MODELS (% + numbers)
**DATA: chhota par twisted family.**

**PYQ 1** [2022]: `20% of smaller = 14% of larger; sum = 8,942. Smaller?` →
A3 wala: S/L = 14/20 = 7/10 → S = 7k, L = 10k, 17k = 8942 → k = 526 → S = **3,682**... (dataset ANS B=53260? — OCR noise `[SOURCE UNCLEAR]`; method yahi hai: 7:10 split of 8942)
**PYQ 2 (enhance to equal)** [2017]: `Two numbers 35% & 50% less than a third. Second ko kitna % badhaye ki first ke barabar?` →
Third = 100: N₁ = 65, N₂ = 50. Badhana = (65−50)/50 = **30%** ✓ (trap answer 23.08% — wo 65 ke base par hai; "N₂ ko badhana" ⇒ base N₂=50)

---
---

# SECTION B — PROFIT & LOSS MODELS (13 models • 191 PYQs + discount overlap)

**PEHLE CORE (sab kuch isi se derive hota hai):**
- Profit = SP − CP (SP > CP); Loss = CP − SP
- Profit% = Profit/**CP** × 100 (base HAMESHA CP — SSC ka standard)
- SP = CP(1 + p/100) — ye multiplier PART-1 ke F3 hi hai. **P&L = % ka costume.**

---

## ▌B1. BASIC CP–SP–% (+ overheads)
**DATA: 19 direct + har model ka base.**

**Logic:** overhead (repair/transport) **CP me add** hota hai, SP me nahi.
**PYQ 1** [2023]: `Old phone ₹3,450 + repair ₹450, sold ₹5,070. Profit%?` → CP = 3900; P = 1170 → **30%** ✓
**PYQ 2 (loss→gain switch)** [2019]: `Sold at 291 ⇒ 3% loss. Kitne me beche ki 8% gain ho?` →
CP = 291/0.97 = 300 → SP = 300×1.08 = **₹324** ✓
**PYQ 3 (two SPs, overhead)** [2022]: `Washing machine ₹4,500 + ₹500 repair, sold ₹4,500. Loss%?` →
CP = 5000, loss 500 → **10%** ✓
**Fastest:** 291/0.97: 0.97 = 97/100 ⇒ 291×100/97 = 3×100 = 300 (291 = 97×3 pehchano!).

---

## ▌B2. DIFFERENCE-BASED (CP−SP diya + % diya)
**Logic:** profit me SP−CP = p% of CP ⇒ **CP = difference × 100/p**.
**PYQ** [2024, numbers OCR-garbled — pattern]: `SP−CP = 1800, profit 20% → CP = 1800×100/20 = 9,000` (dataset options mismatched `[SOURCE UNCLEAR]` — method reliable hai: diff×100/p)
**Variation:** "loss% diya, diff diya" — same, p ko loss% se replace karo.

---

## ▌B3. SP OF m ARTICLES = CP OF n ARTICLES
**DATA: 8 direct (2017–2024), repeat-prone.**

**Derivation (ratta zero):** SP×m = CP×n ⇒ SP/CP = n/m ⇒ Profit% = (SP−CP)/CP = **(n−m)/m × 100**
**PYQ 1** [2021]: `CP of 70 articles = SP of 40. Profit%?` → (70−40)/40 = **75%** ✓
**PYQ 2** [2024]: `SP of 100 pens = CP of 140 pens. Profit%?` → (140−100)/100 = **40%** ✓
**PYQ 3** [2024]: `SP of 40 = CP of 50. Gain%?` → (50−40)/40 = **25%** ✓
**Trap:** kaunsa SP-side me hai dekho: "CP of 70 = SP of 40" me n=70, m=40 (CP wala number bada ⇒ profit). Agar "SP of 60 = CP of 50" hota to LOSS hota.

---

## ▌B4. GAIN = SELLING PRICE OF k ITEMS
**DATA: 8 direct.**

**Derivation:** N items beche, gain = SP of k items ⇒ N(SP−CP) = k·SP ⇒ N·CP = (N−k)SP ⇒
**Profit% = k/(N−k) × 100** — ek formula, sab cases.
**PYQ 1** [2024]: `Selling 60 pens, gain = SP of 12 pens.` → 12/48 = **25%** ✓
**PYQ 2** [2024]: `Selling 22 items, gain = SP of 6.` → 6/16 = **37.5%** ✓
**PYQ 3** [2024]: `30 m cloth, profit = SP of 10 m.` → 10/20 = **50%**
**Fastest:** k/(N−k) — 60 pens/12: 12/48 = 1/4 = 25% turant.

---

## ▌B5. PROFIT@S₁ = LOSS@S₂ (do SP equation)
**DATA: 3+ direct, classic.**

**Derivation:** S₁ − CP = CP − S₂ ⇒ **CP = (S₁+S₂)/2** (average!).
**PYQ 1** [2022]: `Profit@9610 = Loss@7690. SP for 10% profit?` →
CP = (9610+7690)/2 = 8650 → SP = 8650×1.1 = **₹9,515** ✓
**PYQ 2** [2023]: `Profit@1600 = Loss@1400; 20% profit chahiye.` → CP = 1500 → SP = **₹1,800** ✓
**Variation:** "profit twice the loss" — 2(SP₁−CP) = (CP−SP₂) type weighted equation, same setup.

---

## ▌B6. TWO ARTICLES, SAME SP (one gain, one loss) ⭐
**DATA: 14 direct — sabse repeated P&L model after B1.**

**THE DERIVED GEM:** dono ko SAME SP par becha, ek par +x%, doosre par −x% ⇒
CP₁ = S/(1+x), CP₂ = S/(1−x). Total CP = 2S/(1−x²) > 2S ⇒ **hamessa LOSS = x²% (exact, total CP par)**
Derivation: TotalCP − 2S = 2S·x²/(1−x²); isko TotalCP se divide karo ⇒ x².
±20% → **4% loss** • ±25% → 6.25% loss • ±10% → 1% loss. (A5 ke ±a successive se alag hai — ye same-SP hai!)
**PYQ 1** [2021]: `X, Y for ₹600 each; +20% on X, −20% on Y. Overall?` → **4% loss** ✓
**PYQ 2 (unbalanced %)** [2023]: `₹2,600 each; −25% & +20%. Overall %?` →
CP₁ = 2600/0.75 = 3466.67; CP₂ = 2600/1.2 = 2166.67; Total CP = 5633.33; SP = 5200
Loss = 433.33 → 433.33/5633.33 = **7.7% loss** ✓ (formula sirf balanced ±x par hai; unbalanced me aise hi karo)
**PYQ 3 (same SP, CP nikalo)** [2022]: `2 TVs ₹2,280 total; ek −20% ek +10%, same SP each. CP of each?` →
0.8C₁ = 1.1C₂ = S aur C₁+C₂ = 2280 → C₁ = 2280×(1.1/1.9) = **₹1,320** ✓
**Trap:** "same SP ±x% → loss" vs "same CP ±x% → net ZERO". SP-par loss hota hai kyunki loss wale item ka CP bada tha.

---

## ▌B7. CHAIN SELLING (A→B→C)
**DATA: 3 direct + A5 se connected.**

**Logic:** har step multiplier: Final = CP_A × (1+p₁)(1+p₂)... ⇒ **CP_A = Final ÷ product**
**PYQ 1** [2021]: `A→B +10%, B→C +25%, C pays ₹6,875. A ka CP?` → 6875/(1.1×1.25) = 6875/1.375 = **₹5,000** ✓
**PYQ 2** [2024]: `Bike: +45%, phir +30%; C pays ₹43,355. A ka CP?` → 43355/(1.45×1.3) = 43355/1.885 = **₹23,000** ✓
**Fastest:** 1.885 = 377/200... better: 43355 ÷ 1.45 = 29,900; 29900 ÷ 1.3 = 23,000 (step-by-step divide).

---

## ▌B8. DISHONEST WEIGHTS ⚖️ (P&L + % ka deadliest mix)
**DATA: 7 direct + discount side par bhi (D-models me faulty machine).**

**मूल Logic (formula nahi, setup):** do equations banao —
- **Actual CP** = rate × ACTUAL weight jo diya
- **SP** = rate × CLAIMED weight × (claimed profit/loss adjustment)
Phir profit% = (SP − ActualCP)/ActualCP.
**PYQ 1 (sell-side cheat)** [2023]: `Buys ₹20/kg, sells ₹25/kg, gives 800g instead of 1kg. Actual profit%?` →
Actual CP = 20×0.8 = ₹16; SP = ₹25 (1 kg ka rate) → 9/16 = **56.25%** ✓
**PYQ 2 (weight + profit dono)** [2024]: `Uses weights 19% less, profit 35%. Net gain%?` →
CP of given goods = 0.81 (per claimed unit); SP = 1.35 → (1.35−0.81)/0.81 = **66.67%** ✓
General: net gain = (1+g)/(1−e) − 1 (e = weight deficit fraction)
**PYQ 3 (double deception — classic)** [2017 & 2018 dono me same!]: `Professes 16% loss, uses 680g instead of 1kg. Total profit%?` →
Rate ₹1/g maano. SP = 840 (16% loss on 1000g ka rate); actual CP = 680 → (840−680)/680 = **23.53%** ✓
**PYQ 4 (buy-side reverse)** [2021]: `Sells rice at CP, faulty machine, gains 25%. Kitna g deta hai 1 kg me?` →
1/1.25 = 0.8 → **800 g** ✓
**Trap:** cheat buying me hota ya selling me — "uses 19% less while selling" SP side. Buying-cheat: kam paisa dekar zyada maal.

---

## ▌B9. RATE-BASED (per kg / dozen / box) + ROTTEN GOODS
**DATA: 14 direct.**

**Logic:** sab kuch **per-unit** me le aao, phir simple P&L. Rotten/damaged = quantity kam, CP pura.
**PYQ 1** [2019]: `40 dozen fruits ₹2,400; 30 rotten; rest kitne per dozen me beche ki 25% profit ho?` →
CP total 2400; target SP = 3000; bacha 37.5 dozen → 3000/37.5 = **₹80/dozen** ✓
**PYQ 2** [2022]: `10 dozen corn @₹180/dozen; sold @₹22/piece. Profit%?` →
CP 1800; SP = 120×22 = 2640 → 840/1800 = **46.67%** ✓
**PYQ 3 (kg-wise)** [2024, partially garbled `[SOURCE UNCLEAR]`]: `sells 195 kg for ₹10,200, profit ₹4.50/kg...` pattern: CP/kg = SP/kg − profit/kg; phir x kg ka CP.
**Trap:** dozen↔pieces conversion (1 dozen = 12) — half galat answers isi par.

---

## ▌B10. MISSED PROFIT ("could have sold")
**DATA: 3 direct (2024).**

**PYQ** [2024]: `Buys ₹10,000, sells ₹12,000; later pata chala ₹13,000 me bik sakta tha. % profit missed?` →
Missed profit = 13000−12000 = 1000; base = **CP** 10,000 → **10%** ✓
**Trap:** base SP log le lete hain (1000/12000 = 8.33%) — profit% ki base CP hi hai.

---

## ▌B11. PROFIT% = CP (numerically) — QUADRATIC TYPE
**DATA: 2-3 (twisted family).**

**Logic:** CP(1 + CP/100) = SP ⇒ quadratic — par **options se testing fastest** hai.
**PYQ** [2021]: `Earphone sold ₹2,000; profit% = CP numerically. CP?` →
Test ₹40/₹400: 400 → 400+1600 = 2000 ✓ → **CP = ₹400** ✓
(Mathematically: C² + 100C − 200000 = 0 → C = [−100+√(10000+800000)]/2 = (−100+900)/2 = 400.)

---

## ▌B12. a% OF CP = b% OF SP
**DATA: 2024 me 2 baar — naya twist, A3 ka P&L costume.**

**Derivation:** a·CP = b·SP ⇒ SP/CP = a/b ⇒ **Profit% = (a−b)/b × 100**
**PYQ** [2024×2]: `70% of CP = 40% of SP. Profit%?` → SP/CP = 70/40 = 1.75 → **75%** ✓

---

## ▌B13. TWO INVESTMENTS (+r% & −r%) — RATIO WEIGHTED
**DATA: 2023 twist.**

**Logic:** amounts ratio me ho to weighted multiplier: net = [(1+r)·w₁ + (1−r)·w₂]/(w₁+w₂)
**PYQ** [2023]: `Earns 10% on one, loses 10% on other; investments 1:3. Combined?` →
(1.1×1 + 0.9×3)/4 = 3.8/4 = 0.95 → **5% loss** ✓
**Trap:** equal investments hota to net 0% (1.1+0.9 = 2.0). Ratio change = answer change.

---
---

# SECTION C — DISCOUNT MODELS (6 models • 276 PYQs — sabse bada single block)

**CORE (ek line):** MP = CP(1+m%) → SP = MP(1−d%) ⇒ **SP/CP = (1+m)(1−d)**
Poora discount-chapter isi ek equation ka khel hai. Har question me in 4 me se 3 cheezein di hoti hain, chauthi maangni hoti hai.

---

## ▌C1. MP–CP–DISCOUNT–PROFIT CHAIN (THE MONSTER) ⭐⭐
**DATA: ~119 MP-based + 67 shopkeeper = sabse zyada questions ka model.**

**Universal:** SP/CP = (1+m)(1−d) — jo diya usko plug karo.
**PYQ 1 (m, d → loss/profit)** [2024]: `MP 25% above CP; discount 40%. Loss%?` →
1.25×0.6 = 0.75 → **25% loss** ✓
**PYQ 2 (MP, d, p → CP)** [2023]: `Profit 8%, discount 10%, MP ₹1,080. CP?` →
SP = 1080×0.9 = 972; CP = 972/1.08 = **₹900** ✓
**PYQ 3 (reverse: MP par becha, discount hota to...)** [2022]: `MP par ₹13,000 me becha = 30% profit. 10% discount hoti to profit kitna?` →
SP = 13000 = 1.3CP ⇒ CP = 10,000; discounted SP = 11,700 → **17% profit** ✓
**PYQ 4 (discount+loss → MP par profit)** [2021]: `40% discount par 30% loss. MP par bechta to?` →
0.6MP = 0.7CP ⇒ MP = (7/6)CP → **16⅔% profit** ✓
**PYQ 5 (markup-discount both)** [2024]: `Marks 50% above CP, discount 30%. Profit%?` → 1.5×0.7 = 1.05 → **5%** ✓
**PYQ 6 (no-discount profit)** [2022]: `10% discount ke saath 10% profit. Bina discount profit%?` →
0.9MP = 1.1CP ⇒ MP = (11/9)CP → **22.22%** ✓
**PYQ 7 (MP = k×CP)** [2024]: `10% discount + 10% profit. MP, CP ka kitna gunank?` → (1.1/0.9) = 1.2222 → **≈1.22** ✓
**Fastest:** m aur d ko fraction me likho (25% = 1/4, 40% = 2/5): 1.25×0.6 → (5/4)(3/5) = 3/4 = 0.75 — 2 second me.
**Traps:**
- Markup "CP se 25% upar" (base CP) vs discount "MP par" (base MP) — **base alag, % alag**
- "Successive discount" word nahi bhi ho tab bhi markup+discount = multiplier chain hi hai
- 40% discount + 30% loss me log 40−30 = 10 answer likh dete hain ⚠️

---

## ▌C2. SUCCESSIVE DISCOUNTS
**DATA: 48 direct.**

**Logic (derive):** d₁, d₂ ke baad SP factor = (1−d₁)(1−d₂) = 1 − (d₁+d₂) + d₁d₂
⇒ **Equivalent single discount = d₁ + d₂ − d₁d₂/100** (d₁, d₂ % me)
Isliye ye HAMESHA (d₁+d₂) se KAM hota hai — cross-term d₁d₂/100 bach jaata hai.
**PYQ 1 (equivalent)** [2021]: `20% & 30% successive. SP ₹840. Discount amount?` →
factor 0.8×0.7 = 0.56 ⇒ discount 44%; SP = 0.56MP = 840 ⇒ MP = 1500 → **₹660** ✓
**PYQ 2 (amount → MP → profit)** [2022]: `20% & 10% = single discount ₹252; CP ₹600. Profit?` →
single = 28% ⇒ MP = 252/0.28 = 900; SP = 648 → profit = **₹48** ✓
**PYQ 3 (buy-side chain + overhead)** [2024]: `MP ₹600, bought at 10% & 20% successive; ₹68 transport; sold at MP. Profit%?` →
CP = 600×0.9×0.8 = 432 + 68 = 500; SP 600 → **20% profit** ✓
**PYQ 4 (reverse)** [2023]: `₹5,130? paid after 10% & 5%. MP?` — `[SOURCE UNCLEAR: OCR me 25,130/5,130 ambiguous]` — method: MP = paid/(0.9×0.95)
**Fastest:** 20%+10%: 0.8×0.9 = 0.72 → 28% single. 10%+5%: 0.855 → 14.5%. Ye do-teer ready rakho.

---

## ▌C3. FREE-ITEMS DISCOUNT ("buy x get y free")
**DATA: 2024 me 2-3 (naya favourite).**

**Derivation:** customer ko x+y items milte x ke paise par ⇒ per-item price ×x/(x+y)
⇒ **Effective discount = free/(bought+free) × 100**
**PYQ 1** [2024]: `On buying 24 bangles, 6 free. % discount?` → 6/30 = **20%** ✓
**PYQ 2** [2024]: `24 tumblers par 12 free. % discount?` → 12/36 = **33.33%** ✓
**Trap:** 6/24 = 25% likhne ki galti — free wale bhi to mil rahe hain (total 30).

---

## ▌C4. NEUTRAL MARKUP↔DISCOUNT (SP same rakhna)
**DATA: 2-3 (2024).**

**Derivation:** MP ko (1+m) karke, phir d% discount such that SP same: (1+m)(1−d) = 1 ⇒
**d = m/(1+m)** (% me: m/(100+m)×100)
**PYQ** [2024]: `MP 40% badhaya. SP same rakhne ke liye kitna discount do?` → 40/140 = **28.57%** ✓
**Reverse use:** "+25% karo to wapas 20% kaam karo = same" (F5 ka hi roop).

---

## ▌C5. DISCOUNT % NIKALNA (listed vs sold)
**PYQ 1** [2021]: `Cot marked ₹15,000, sold ₹13,500. Discount%?` → 1500/15000 = **10%** ✓
**PYQ 2 (listed total)** [2023]: `10% off on items worth ₹560 (bag) + ... total discount?` — items add karke 10%.
**Note:** discount% ki base **MP/listed**, profit% ki base **CP** — do models me base ulta hai, yahi sab confusions ki jad hai.

---

## ▌C6. RESTORE ORIGINAL (−x% ko wapas laana)
**Logic:** A12/A7 ke restore formula ka discount version: needed increase = **x/(100−x)×100**
**PYQ** [2017]: `Price cut 3%. Restore karne ke liye kitna badhaye?` → 3/97 = **3.09%** ✓
(3.09 < 3 nahi — 3.09 > 3, kyunki chhote base par badhana padta hai. 45% → 31%? nahi — 45% CUT restore = 45/55 = 81.8% INCREASE. Direction dhyan se!)

---
---

# SECTION D — MASTER TRAP LIST (Commercial Arithmetic)
*(Sirf wo traps jo dataset ke questions me SSC ne ACTUALLY use kiye hain)*

| # | Trap | Real example |
|---|---|---|
| 1 | **Base confusion:** "A x% more than B" vs "B y% less than A" — same pair, different % | 30% vs 23.08 (2017 PYQ) |
| 2 | **% of vs % more than** | A2, A4 |
| 3 | **±x% successive ≠ 0** → −x²/100 net loss | 2021 ±8% → 0.64% loss |
| 4 | **Same-SP ±x% pair = guaranteed loss x²%** | 2021: ±20% → 4% loss |
| 5 | **x% of remaining** = naya base | Aman 4/13 of 0.65I (2024) |
| 6 | **Election: valid vs cast vs registered** — 3 layers, base mixed | 2023: 9408→20,000 |
| 7 | **Population avg-rate:** arithmetic mean galat | 44%, 75% → 76% not 59.5 |
| 8 | **Markup base CP, discount base MP** | C1 sab examples |
| 9 | **Successive discounts ADD nahi hote** | 20%+30% = 44%, not 50% |
| 10 | **Free items: denominator (bought+free)** | 6/30 not 6/24 |
| 11 | **Profit% base = CP** (missed-profit, error, sab me) | B10: 1000/10000 not /12000 |
| 12 | **Overheads CP me** | B1: repair ₹450 add |
| 13 | **"Increased by k becomes p% of itself"** — p−100 ka dhyan | 8 → 120% ⇒ 40 |
| 14 | **Restore % ≠ original %** (chhote base par) | 3% cut → 3.09% hike |
| 15 | **Rotten goods: quantity ghati, CP nahi** | B9: 37.5 dozen par 3000 |

---

# PART 1 COVERAGE AUDIT (dataset ke against)

- Commercial-arithmetic total: **1,102 questions** (PCT 635 + PNL 191 + DISC 276)
- In models me map hua: **~1,050+ (95%+)** — baaki ~50: DI-leaks (pie-/bar-graph questions jo % words use karte hain — Part 8 me), average-leaks (Part 2), SI/CI-leaks (Part 2), 2024 ki 2-3 OCR-unreadable story sums `[SOURCE UNCLEAR]`
- Missing model check: catch-all buckets ("other") manually scan kiye — koi naya recurring model nahi bacha (jo dikhe wo upar 34 me shaamil)
- Duplication check: A12 (dimension-%) mensuration se overlap karta hai par logic yahan bithaya gaya hai (% multiplier) — Part 6 me sirf formula-side reference hoga, question-models yahin rahenge
- Dataset-answer discrepancies found: 2 (cylinder-TSA 2022, pulses-45 2024) — dono flag kiye, correct math answer ke saath

**Part 1 → 34 models, ~95% question-coverage, 40+ solved PYQs (har variation ka representative).**
