# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 3: TIME & WORK • PIPES/CISTERN • SPEED-TIME-DISTANCE • TRAINS • BOATS

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). Is Part ke areas ke **~430 actual questions**: T&W ~180 (clean) • Pipes ~16 • TSD/Trains/Boats ~235.
Har solution independently verified. OCR-garbled PYQs par `[SOURCE UNCLEAR]`.

**Part map:** 1 Commercial ✅ | 2 Ratio/Avg/Interest ✅ | **3 (ye file)** | 4 Number/Algebra/Simplification | 5 Geometry | 6 Mensuration | 7 Trigonometry | 8 DI | 9 Mixture+Index

---
---

# SECTION 0 — PART-3 FOUNDATION

**T1. Work = Rate × Time, LCM-units method:**
"Work" ko LCM of given days maan lo (A 12d, B 15d → work = 60 units). Phir A = 5 units/day, B = 4 units/day.
Aage har question = units ka add-subtract. Fractions (1/12 + 1/15) kabhi mat likho — LCM me sab integers milte hain.

**T2. MDH chain:** M₁D₁H₁ = M₂D₂H₂ (total man-hours constant). Derivation: work = (men × days × hours/day) × per-man-rate — work same hai to product same.

**T3. Speed triangle:** D = S×T. **km/h → m/s: ×5/18** (1 km/h = 1000 m/3600 s = 5/18 — reduce karke aata hai, ratta nahi). m/s → km/h: ×18/5.

**T4. Relative speed (movement ka super-tool):**
- Same direction: **v₁ − v₂** (catch-up/overtake) — "kitni der me pakdega" ka answer is se
- Opposite direction: **v₁ + v₂** (closing speed) — "kitni der me milenge" ka answer is se
- Derivation: har second me distance kitni ghat/badh rahi hai — bas.

**T5. Boat frame (2 equations):** downstream d = b+s, upstream u = b−s (stream neeche/dhaar me help/kabhi rok).
Add: **b = (d+u)/2**; subtract: **s = (d−u)/2**. Ye dono nikaalne wale questions 2-second ke hain.

**📦 Minimum-ratta:** ×5/18 conversions ke common answers: 36→10, 54→15, 63→17.5, 72→20, 90→25 m/s. Squares 21–30.

---
---

# SECTION W — TIME & WORK (7 models • ~180 clean PYQs)

**DATA ALERT: Wages-distribution questions = 0 in 193 papers. Graze/eat questions ≈ 0. Dono classic "coaching topics" CHSL Tier-I me pooche hi nahi gaye — skip them.**

---

## ▌W1. BASIC: A in a days, B in b days → together/alone
**DATA: ~124 Q — sabse bada T&W model. Har saal 4-6 Q.**

**Universal (LCM):** work = LCM(a,b); rates add karo; answer = total ÷ combined rate.
**PYQ 1** [2023|Q7]: `A+B = 15 days, B alone = 21. A alone?` →
Work 105: A+B = 7, B = 5 → A = 2/day → **52.5 days** ✓
**PYQ 2 (with-C)** [2024|Q11]: `A = 20d, B = 10d, A+B+C together = 5d. C alone?` →
Work 20: A=1, B=2; together = 4 → C = 1 → **20 days** *(dataset options/ANS OCR-inconsistent — computed value 20; method yahi)*
**Fastest:** "together t, B alone b → A = tb/(b−t)": 15×21/6 = 52.5 (derive: 1/A = 1/t − 1/b = (b−t)/tb).

---

## ▌W2. PAIRWISE SUMS (A+B, B+C, C&A given) ⭐
**DATA: 2024 me repeat — SSC ka pasand.**

**Logic:** teen equations add karo: 2(A+B+C) = sum of rates → sab mil jaate hain.
**PYQ** [2024|Q5]: `A+B = 12d, B+C = 15d, C+A = 10d. A alone?` →
Work 60: A+B = 5, B+C = 4, C+A = 6 → sum 15 = 2(A+B+C) → A+B+C = 7.5
A = (A+B+C) − (B+C) = 7.5 − 4 = 3.5/day → 60/3.5 = **17 1/7 days** ✓
**Trap:** 2 se divide bhoolna (log 15 ko hi A+B+C maan lete hain). Aur "A nikalna hai to (B+C) wali equation MINUS karo".

---

## ▌W3. EFFICIENCY-% / RATIO (x% more efficient) ⭐
**DATA: 9+ Q — 2024 me 2 (Joey/Tim wala Part-1 % bucket se leak hua tha — asli me T&W hai).**

**मूल Logic:** "B is x% more efficient than A" ⇒ **rate_B = (1+x/100)×rate_A** ⇒ days_B = days_A × 100/(100+x).
Efficiency aur days ULTA proportional hain — efficiency ×  = days ÷.
**PYQ 1** [2024|Q20]: `Joey 15 days; Tim 25% more efficient. Tim?` → 15×100/125 = **12 days** ✓
**PYQ 2** [2022|Q24]: `A = 9 days; B 80% more efficient. Together?` →
B rate = 1.8×A; combined = 2.8×A → time = 9/2.8 = **45/14 days** ✓
**PYQ 3 (efficiency ratio)** [2018|Q65]: `S+T+U together 30 days; eff S:T:U = 20:15:12. U alone?` →
U = 12/47 of total rate → U alone = 30×47/12 = **117.5 = 235/2 days** ✓
**PYQ 4 (half-work trick — twisted)** [2022|Q23]: `S does half the work of T in 1/8 of T's time. Together 60 days. S alone?` →
S ka rate = (1/2 work)/(1/8 time) = 4× T's rate. Together = 5×T rate = 1/60 → T = 300 → S = 300/4 = **75 days** ✓
**Trap:** "80% more efficient" me A ke 9 days se 9×1.8 = 16.2 days NahiN — ulta hota hai (9/1.8 = 5).

---

## ▌W4. MULTI-TYPE WORKFORCE (men & women equations)
**DATA: 4-5 Q, sab twisted-level.**

**Logic:** 2 linear equations in m, w (per-day rates). LCM units me clean integers.
**PYQ 1** [2022|Q70]: `4m+7w = 8 days; 7m+4w = 5 days. 8 women?` →
Work 40: 4m+7w = 5/day; 7m+4w = 8/day.
Add: 11m+11w = 13 → m+w = 13/11. Subtract: 3m−3w = 3 → m−w = 1.
→ m = 12/11, w = 1/11 per day → 8w = 8/11 → 40×11/8 = **55 days** ✓
**PYQ 2** [2022]: `12 men = 8 days; 4 boys = 40 days. 9 boys + 3 men?` →
Work 96: m = 1/96×12 = 1/8 per man... units: 12m = 12/day(96/8), 4b = 2.4/day → m = 1, b = 0.6.
3m+9b = 3+5.4 = 8.4/day → 96/8.4 = **80/7 = 11 3/7 days** ✓
**Fastest:** add/subtract karke (m+w) aur (m−w) nikaalo — direct m, w solve karne se fast.

---

## ▌W5. JOIN / LEAVE MID-WORK (man-days accounting)
**DATA: ~4 Q + MDH mixes.**

**Logic:** **man-days consumed** gin lo: jo log kitne din kaam kare. Remaining work ÷ naya roster.
**PYQ 1** [2021]: `40 men, 18 days ka work. 9 days baad 5 men join. Remaining work?` →
Total = 720 man-days. Used = 40×9 = 360. Remaining 360 ÷ 45 = **8 days** ✓
**PYQ 2** [2019|Q6]: `A does 40% in 6 days; B does 30% in 3 days. Dono ne 2 din saath kaam kiya, B chala gaya. Total?` →
A = 1/15/day, B = 1/10/day. 2 din = 2×(1/6) = 1/3. Remaining 2/3 ÷ A = 10 days → total = **12 days** ✓
**Trap:** "how many MORE days" vs "total days" — 2019 wale me 12 total tha (2+10); agar "more" poocha hota to 10.

---

## ▌W6. MDH (men-days-hours)
**PYQ** [2023|Q19]: `7 people, 4 h/day, 14 days → 12 people, 5 h/day me kitne days?` →
7×4×14 = 392 = 12×5×d → d = 392/60 = **98/15 = 6 8/15 days** ✓
**Fastest:** ratio chain: days scale by (7/12)×(4/5)×14 — inverse proportions lagao.

---

## ▌W7. FRACTION-OF-WORK (direct)
**PYQ** [2022|Q72]: `A alone 40 days. 20% work kitne din me?` → 0.20×40 = **8 days** ✓
(LCM ki zarurat nahi — linear scaling. Ye 2022+ me "easy mark" question hai.)

---
---

# SECTION P — PIPES & CISTERN (4 models • ~16 PYQs — chhota par pakka family)

**Frame: pipes bhi "workers" hain** — fill-pipe = positive rate, drain/leak = negative rate. LCM-units T1 hi.

**▌P1. MULTI-TAP FILL**
[2022|Q68]: `15 taps → 36 min. 60 min me kitne taps?` → Work = 540 tap-min → 540/60 = **9 taps** ✓
*(Inverse proportion — taps × time constant)*

**▌P2. FILL + DRAIN (net rate)** ⭐
[2020|Q22]: `A fills 6h, B fills 8h, C empties 4h. Teeno open?` →
LCM 24: A = +4, B = +3, C = −6 → net +1/hr → **24 hours** ✓
[2023|Q14]: `Inlet 51h, outlet 76.5h. Dono open — tank bharne me?` →
Net = 1/51 − 1/76.5 = 25.5/3901.5 = 1/153 → **153 hours** ✓
*(⚠️ dataset me chosen answer 102 dikha — **153 hi sahi hai**; 102 tab hota jab outlet 102h hota.)*

**▌P3. LEAK MODEL**
[2021|Q66]: `Pipe fills 15h; leak ke saath 20h. Tank FULL hai, pipe band — leak khali karega kitne me?` →
Leak rate = 1/15 − 1/20 = 1/60 → **60 hours** ✓
**Trap:** "kitne me khali karega" = 1/leak-rate (full tank). Log 20−15 = 5 ya 60−20 = 40 bol dete hain.

**▌P4. ALTERNATE HOURS**
[2018|Q65]: `X fills 20h, Y fills 35h; alternate hours, Y pehle. Total?` →
LCM 140: X = 7, Y = 4. Har 2 hrs = 11 units. 12 pairs (24h) = 132. Bacha 8:
hr-25 (Y) = 4 → 4 bache → hr-26 (X) me 4/7 hr. Total = 25 + 4/7 = **179/7 hours** ✓
**Trap:** "Y opened FIRST" — order matters; last incomplete hour me kaunsa pipe khula, wahi fraction deta hai.

---
---

# SECTION S — SPEED-TIME-DISTANCE (10 models • ~235 PYQs)

---

## ▌S1. BASIC D = S×T (direct/return)
**DATA: ~105 (catch-all) — har saal.**

**PYQ 1 (return +1h longer)** [2022|Q68]: `Going 60, return 30, return me 1 ghanta zyada. Distance?` →
d/30 − d/60 = 1 → d/60 = 1 → **60 km** ✓
**PYQ 2 (circular park)** [2022|Q21]: `Diameter 420 m, 9 km/h. Ek round me?` →
πd = 1320 m; 9 km/h = 150 m/min → **8.8 min** ✓
**Fastest:** "speeds ratio 2:1 → times ratio 1:2; difference = 1 part = 1h → slower time 2h, d = 60×1 = 60".

---

## ▌S2. PARTIAL JOURNEY + REQUIRED SPEED
**PYQ** [2022|Q75]: `250 km in 6h chahiye. 3/5 distance 3.5h me cover ki. Baaki ka speed?` →
Done 150 in 3.5h → 100 km, 2.5h bache → **40 km/h** ✓
**Trap:** "3/5th OF DISTANCE" (150 km) — time ka 3/5 (3.6h) nahi.

---

## ▌S3. SPEED FRACTION → LATE (usual time)
**DATA: 7 Q. 2024 wale me fraction OCR-lost — model pakka.**

**Derivation:** speed f×usual → time = (1/f)×usual → **extra = usual×(1/f − 1)**.
f = 3/4 → extra = t/3; f = 5/6 → extra = t/5; f = 2/3 → extra = t/2.
**PYQ** [2024|Q2]: `Usual speed ke [fraction] par 20 min late. Usual time?` `[fraction OCR-lost]` →
Model answer: f = 6/7 → t/6 = 20 → t = 120 min = 2 h ✓ (dataset ANS B — fraction 6/7 tha)
**Universal:** fraction p/q diya ho → usual time = extra × q/(q−p).

---

## ▌S4. STOPPAGE MODEL
**PYQ** [2022|Q3]: `With stoppages 75 km/h, without 90 km/h. Per hour kitna rukta hai?` →
1 ghante me train 75 km chali (90 ki jagah) → running time = 75/90 = 5/6 h → **stoppage = 10 min/h** ✓
**Formula (derive kiya upar):** stoppage min/hr = (1 − v_with/v_without)×60. Trap: 90−75 = 15 min GALAT.

---

## ▌S5. MEETING (opposite/circular) — closing speed
**PYQ 1** [2021|Q55]: `Circular 2500 m, opposite directions, 37 & 35 km/h. Meet after?` →
Closing = 72 km/h = 20 m/s → 2500/20 = 125 s = **2 min 5 s** ✓
**PYQ 2 (staggered start)** [2023|Q3]: `P→Q @30, 8:30 se; Q→P 8:54 se. 181 km. Meet time?` `[Q-man ka speed OCR-lost = 35]` →
8:54 tak P ne 12 km chal liya. Bacha 169; closing 65 → 2.6h → **11:30 AM** ✓
**Logic:** jo late start karta hai uska "handicap" pehle minus karo, phir closing speed.

---

## ▌S6. CHASE / CATCH-UP (same direction relative)
**DATA: 2024 me 2 (policeman-thief).**

**PYQ** [2024|Q21]: `Thief 500 m aage @18; police @36. Kitne time me pakdega?` →
Relative = 18 km/h = 5 m/s → 500/5 = **100 sec** ✓
**Fastest:** gap ÷ relative speed. km/h → m/s conversion hi asli kaam hai.

---

## ▌S7. TRAIN CROSSING POLE / PLATFORM (length = distance)
**मूल Logic:** pole/man → distance = TRAIN ki length. Platform/bridge/tunnel → distance = train + platform.
**PYQ 1** [2021|Q66]: `63 km/h, pole in 24 s. Length?` → 63×5/18 = 17.5 m/s → 17.5×24 = **420 m** ✓
**PYQ 2** [2018|Q166]: `800 m train @90 km/h, bridge in 50 s. Bridge?` →
25 m/s × 50 = 1250 = 800 + bridge → **450 m** ✓
**Trap:** "crosses a bridge" me train ki length ADD hoti hai; "crosses a pole" me nahi. "A girl crossing a bridge" me sirf bridge (girl point-mass).

---

## ▌S8. TRAIN vs TRAIN (relative, lengths add)
**PYQ 1 (same dir, equal length)** [2023|Q10]: `46 & 36 km/h same dir; quicker overtakes in 36 s. Length of each?` →
Relative = 10 km/h = 25/9 m/s → 25/9×36 = 100 = L+L → **50 m** ✓
**PYQ 2 (opposite, length ratio)** [2019|Q19]: `84 & 52 opposite, cross in 12 s; y = (2/3)x. Length x?` →
Closing = 136 km/h = 340/9 m/s → x+y = 340/9×12 = 1360/3; x(1+2/3) = 5x/3 = 1360/3 → **x = 272 m** ✓
**Trap:** "overtakes" (same dir, SUBTRACT) vs "crosses each other" (opposite, ADD). Lengths dono cases me ADD hoti hain.

---

## ▌S9. BOAT & STREAM ⭐ (5 verified PYQs — frame T5 sab solves)
**PYQ 1 (b from d,u)** [2022|Q65]: `36 km upstream 9h, same 36 downstream 3h. Still-water speed?` →
u = 4, d = 12 → b = **8 km/h** ✓
**PYQ 2 (b from d,s)** [2023|Q11]: `Downstream 18, upstream 16. Still water?` → (18+16)/2 = **17** ✓
**PYQ 3 (round trip)** [2024|Q4]: `b = 12, s = 3; 45 km jana + wapas. Total time?` →
d = 15, u = 9 → 45/15 + 45/9 = 3+5 = **8 hours** ✓
**PYQ 4 (two legs)** [2022|Q55]: `s = 4, b = 11; 21 km up + 45 km down?` →
7 + 3 = **6 hours** ✓
**PYQ 5 (d & b given, upstream time)** [2024|Q6]: `60 km down in 4h; b = 13. 30 km up in?` →
d = 15 → s = 2 → u = 11 → 30/11 = **2 8/11 h** ✓
**PYQ 6 (b from u & s direct)** [2023|Q14]: `10 km up in 50 min, s = 3 → b?` →
u = 12 → b = 15. *(Dataset ANS 45 — question-text OCR-corrupt; correct model answer 15)* `[SOURCE UNCLEAR]`
**Trap:** "speed of boat 12 km/h" = still water; "downstream speed" = b+s. Word "downstream/upstream speed" dekho to b±s mat likhna.

---

## ▌S10. GOODS-TRAIN CATCH-UP (2017 classic, do baar repeat)
**PYQ** [2017|Q57 & Q158 — same template, numbers alag]: `X hrs after goods train passed a station, passenger train @ v follows; [catches it t hrs after passing]. Goods train ki speed?` →
Catch-up: dono station se catch-point tak: **v×t = g×(t + X)** (goods ka head-start = X hrs)
→ g = vt/(t+X). `[catch-time t OCR me truncated — 2017 Q57: t=9, v=70, X=5 → g = 630/14 = 45 ✓ dataset ANS]`
**Model:** head-start wala chase — gap = v×X (station se), phir S6 wala relative-speed chase.

---
---

# PART 3 MASTER TRAPS (dataset-verified)

| # | Trap | Evidence |
|---|---|---|
| 1 | Efficiency x% more ⇒ days ×100/(100+x), NOT minus | Joey 15→12 |
| 2 | Pairwise sums me 2(A+B+C) — 2 se divide | 2024: 17 1/7 |
| 3 | km/h→m/s ×5/18 — 63→17.5, 90→25 (ye do repeatedly aaye) | S7 |
| 4 | Pole crossing = train length; platform = train+platform | 420 vs 450 |
| 5 | Overtake: relative SUBTRACT + lengths ADD | 50 m |
| 6 | "More days" vs "total days" (mid-work join) | 12 vs 10 |
| 7 | Leak-empty time = 1/(leak rate) full tank | 60h not 5 |
| 8 | Net pipe rate negative ho sakta (drain > fill) | P2 |
| 9 | Stoppage = (1 − v₁/v₂)×60, not v₂−v₁ | 10 min not 15 |
| 10 | Speed fraction p/q late → usual = extra×q/(q−p) | S3 |
| 11 | Boat: "downstream speed" ≠ "boat speed" — b±s check | S9 |
| 12 | Late-starter ka handicap pehle ghatna (meeting) | 181 km |
| 13 | Wages/grazing = 0 Q — padha to time waste | data finding |
| 14 | Alternate pipes: kaunsa LAST khula (fraction hour) | 179/7 |

---

# PART 3 COVERAGE AUDIT

- Part-3 areas: T&W 267 raw (66 "wheat/eat" false-positives hata kar ~180 clean+leaks), Pipes 20 raw (~16), TRAIN 88, TSD 145, BOAT 28 → **~430 clean questions, 21 models me ~92%+ mapped**
- **Data-driven findings:**
  - **Wages = 0 Q, Grazing = 0 Q** in 193 papers — ye "famous" topics CHSL Tier-I me nahi aate (skip!)
  - Pipes chhota family hai (~16 Q) — 4 models kaafi
  - Trains me pole/platform + relative crossing hi 90% hai
  - 2024 me policeman-chase 2 Q — S6 model naya favourite
  - Goods-train catch-up 2017 me 2 shifts me SAME template — repeat-proof model
- Baaki bache: bus-interval model (2 Q, dono OCR-garbled `[SOURCE UNCLEAR]`), 2024 ki ~6 story-sums fraction-loss (18-men, Sunita, Mohit-bus) — models unke equivalent hain, sirf numbers nahi the
- Dataset-answer discrepancies: 2 flagged (inlet/outlet 153 vs chosen-102; boat-2023 b=15 vs chosen-45) — computed answers verified
- Cross-part dedupe: efficiency-Joey Part-1 % bucket me tha — yahan W3 me master-treatment; avg-speed Part-2 V6 → yahan sirf reference

**Part 3 → 17 model-entries (+pipes 4 sub-models), ~92% coverage, 35+ verified PYQ solutions.**
