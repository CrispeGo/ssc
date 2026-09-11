# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 6: MENSURATION — 2D (Areas/Perimeters) • 3D (Volume/Surface)

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). Mensuration pool: **548 raw → ~480 clean questions** (2D 293 + 3D 255; leaks: similar-triangles → Part 5, milk/wine mixtures → Part 9, tank-filling work-rate → Part 3).
**96% papers me aata hai; 2024 me peak (3.3 Q/paper).** Har solution independently verified. OCR-garbled par `[SOURCE UNCLEAR]`.

**Part map:** 1 Commercial ✅ | 2 Ratio/Avg/Interest ✅ | 3 T&W/Speed ✅ | 4 Number/Algebra ✅ | 5 Geometry ✅ | **6 (ye file)** | 7 Trigonometry | 8 DI | 9 Mixture+Index

---
---

# SECTION 0 — FORMULA ENGINE (sab kuch derive, ratta sirf 3 values)

## 0.1 — 2D ka mool-sutra
**Rectangle ka area = l×b** (grid me unit squares gino — bas). Baaki SAB kuch isi se:

- **Triangle = ½ × b × h:** rectangle ko diagonal se kaato → do barabar triangles → aadha. **Yahi sab triangle-areas ki jad hai.**
- **Parallelogram = b×h:** triangle ½bh; parallelogram = do triangles (ya: shear karo → rectangle ban jata hai, base×height same rehta hai)
- **Rhombus = ½ d₁d₂:** diagonals ⊥ bisect karte hain → 4 right triangles, each ½×(d₁/2)×(d₂/2) → total ½d₁d₂
- **Trapezium = ½(a+b)×h:** do triangles + ek rectangle... ya cleanly: mid-line (a+b)/2 × h — shear logic
- **Heron** (3 sides diya ho): s = (a+b+c)/2; area = √[s(s−a)(s−b)(s−c)] — *kyun:* ½bh aur (h dono taraf se likho, Pythagoras dono pieces par) se hi nikalta hai; SSC me tab use hota hai jab height na di ho.
- **Equilateral = √3a²/4:** height = a√3/2 (Pythagoras: a² = (a/2)² + h²) → ½×a×a√3/2.

## 0.2 — Circle
**π ki definition hi C = πd** (har circle me circumference/diameter same constant). Phir:
- **Area = πr²:** *intuition-derivation:* circle ko concentric rings me kaato, unroll karo — triangle ban jata hai (base 2πr, height r) → ½×2πr×r = πr²
- **Sector = (θ/360)×πr²** — pizza ka hissa poore ka θ/360 fraction. **Arc = (θ/360)×2πr** (same fraction, perimeter ka)
- **Segment = sector − triangle** (θ ke sin/cos se)

## 0.3 — 3D ka mool-sutra
**Principle 1: Volume = base-area × height** (cylinder/prism/cuboid — stacking sheets). Cuboid l×b×h isi se.
**Principle 2: Cone/Pyramid = ⅓ × (base×height):** *Cavalieri* — cone aur cylinder ko same height par slices me kaato; har slice ka ratio 1:3 rehta hai (similar shrinking cross-sections... cylinder ka slice constant, cone ka shrinks) — net ⅓.
**Principle 3: Sphere V = 4/3πr³, SA = 4πr²:** SA = 4 great-circles (πr²) — Archimedes ka result: sphere ko cylinder me daalo (r, 2r) → sphere ki SA cylinder ke curved part ka ⅔ = ⅔×4πr² = ... exactly 4πr². V: hemisphere + cone = cylinder (Archimedes tomb result: 2/3πr³ + ⅓πr³ = πr³·... 2/3+1/3 = 1 ✓)
- **Hemisphere:** V = ⅔πr³ (aadha), CSA = 2πr² (aadha), TSA = 3πr² (aadha sphere + circle base)
- **Cone:** l² = r²+h² (Pythagoras — slant height), CSA = πrl (sector unroll!), TSA = πr(l+r)

## 0.4 — Unit conversions (derive, yaad nahi)
1 m = 100 cm → 1 m² = 10⁴ cm², **1 m³ = 10⁶ cm³**; **1 m³ = 1000 litres** (1 L = 1000 cm³ = 10⁻³ m³ — decimeter cube se)

## 0.5 — Scaling law (sabse powerful)
Lengths ×k → **areas ×k², volumes ×k³** (2D me 2 dimensions multiply hote hain, 3D me 3).
*Ye Part-1 A12 ka multiplier-engine hai — % wale questions wahan master-treated.*

**📦 MINIMUM-RATTA (sirf yeh):** π ≈ 22/7 (kyunki SSC ke numbers 7 ke multiples hote hain: 14, 21, 35, 154, 132...) • Pythagorean triples (Part 5 list) • √2≈1.414, √3≈1.732, √5≈2.236 • 1 m³ = 1000 L.
**Formula-sheet ratta ZERO** — upar ke 3 principles se sab nikal aata hai (practice me verify karo).

---
---

# SECTION D — 2D MODELS (7 models • ~270 clean PYQs)

---

## ▌D1. TRIANGLE AREA (base-height / equilateral / Heron)
**DATA: ~55 clean Q (70 me se ~15 similar-triangle Part 5 me).**

**PYQ 1 (alt-base direct)** [2022]: `Altitude 8 cm, base 12 cm → area?` → ½×8×12 = **48 cm²** ✓
**PYQ 2 (square se relation)** [2023|Q22]: `Triangle ka area = square ke area ka aadha; square perimeter 172. Triangle ka area?` →
side = 43 → square area 1849 → **924.5 cm²** ✓
**PYQ 3 (equilateral height side se)** [2023|Q5-family]: `PM ⊥ QR equilateral me → 3PQ² = 4PM²` → height a√3/2 se turant (Part 5-T5 me solved).
**Method-choice:** height diya → ½bh; sirf sides → Heron YA equilateral-check; equilateral → √3a²/4 direct.

---

## ▌D2. RHOMBUS (diagonals + side-Pythagoras combo) ⭐
**DATA: 16 Q — 3 sub-models, sab verified:**

**PYQ 1 (area+height → perimeter)** [2024|Q1]: `Area 70 m², height 5 m. Perimeter?` →
Area = base×height (parallelogram property) → side = 70/5 = 14 → perimeter **56 m** ✓
**PYQ 2 (diagonals → perimeter)** [2022|Q65]: `d₁ = 10, d₂ = 24. Perimeter?` →
½d₁ = 5, ½d₂ = 12 → side = √(25+144) = 13 → **52 cm** ✓
**PYQ 3 (ek diagonal + area → side)** [2021|Q65]: `d = 8, area 48. Side?` →
d₂ = 2×48/8 = 12 → half-diagonals 4, 6 → side = √52 = **2√13** ✓
**PYQ 4 (direct)** [2024]: `Diagonals 10 & 8.2 → area?` → ½×10×8.2 = **41 cm²** ✓
**Model-logic:** rhombus me TEENO quantities (area, side, perimeter) diagonals se aati hain — ½d₁d₂ aur √[(d₁/2)²+(d₂/2)²] — ek hi right triangle (half-diagonals) dono deta hai.

---

## ▌D3. TRAPEZIUM (+ isosceles trapezium geometry)
**DATA: 9 Q — chhota par twisted.**

**PYQ 1 (basic)** [2021|Q57]: `Parallel sides 20, 25; height 14 → area?` → ½(45)(14) = **315 cm²** ✓
**PYQ 2 (isosceles — non-parallel side)** [2019|Q16]: `Parallel 20, 10; area 180. Non-parallel sides equal → length?` →
h = 2×180/30 = 12; equal sides wale ends me extra base (20−10)/2 = 5 har taraf
side = √(12²+5²) = **13** ✓ *(5-12-13!)*
**PYQ 3 (45° base angle — advanced)** [2017|Q56]: `Base angle 45°, shorter side 10, equal sides 10 → area?` →
h = 10sin45 = 5√2; projection = 5√2 (45° me dono barabar) → longer base = 10+2×5√2
Area = ½(10+10+10√2)(5√2) = **50√2+50** ✓
**Trap:** isosceles trapezium me (a−b)/2 wala extra-base har END par — ÷2 karna mat bhoolo.

---

## ▌D4. RECTANGLE/SQUARE — DIAGONAL ENGINE ⭐
**DATA: 42 Q — 2018 me 17 (peak), ab bhi har saal.**

**Core:** diagonal = √(l²+b²) (Pythagoras). **17-8-15** aur **25-7-24** SSC favourites.
**PYQ 1 (diagonal+perimeter → area)** [2021|Q68]: `Diagonal 17, perimeter 46. Area?` →
l+b = 23; (l+b)² = l²+b²+2lb → 529 = 289+2lb → **area = 120 cm²** ✓
*(BEST TRICK: (l+b)² − (diagonal)² = 2×area — identity I2/I6 ka costume, kuch bhi solve karne ki zarurat nahi)*
**PYQ 2 (side+diagonal → perimeter)** [2018|Q71]: `Side 7, diagonal 25 → perimeter?` → b = √(625−49) = 24 → 2(31) = **62 cm** ✓
**PYQ 3 (2018 me 4 baar repeat)** [2018, 4 shifts]: `Diagonal 17, breadth 8 → length?` → √(289−64) = **15** ✓
**PYQ 4 (square +5%)** [2024|Q18]: `Side +5% → area?` → 1.05² = 1.1025 → **10.25%** ✓ (Part-1 A12)
**PYQ 5 (floor ratio)** [2022|Q57]: `b = (3/5)l, area 60 → l−b?` → l²×3/5 = 60 → l = 10, b = 6 → **4 m** ✓
**Trap:** "diagonal of a square" = a√2 (isko bhi derive: dono sides equal → √(a²+a²)).

---

## ▌D5. CIRCLE BASICS (C ↔ r ↔ A chain)
**DATA: 74 Q — 2022 me 27 (peak year).**

**Universal:** C = 2πr se r nikaalo, phir A = πr². SSC numbers 7-multiples deta hai (C = 44 → r = 7; C = 132 → r = 21; C = 154 → r = 24.5; C = 88 → r = 14).
**PYQ 1 (area-difference)** [2022|Q65]: `C₁ = 264, C₂ = 308. Bade–chhote ka area-difference?` →
r = 42, 49 → diff = π(49²−42²) = 22/7×637 = **2002 m²** ✓ *(I2-style: R²−r² = (R+r)(R−r) = 91×7)*
**PYQ 2 (dome-paint — CSA of hemisphere)** [2023|Q25]: `Dome base C = 154; painting cost...` →
r = 24.5 → CSA = 2πr² = 3773 m²... cost rate OCR-cut `[rate SOURCE UNCLEAR]` — **method: dome = hemisphere, C→r→2πr²→×rate**
**PYQ 3 (inscribed circle in square)** [2021|Q59]: `Square side 21, inscribed circle...` → r = 10.5 (side/2) — shaded region = a²−πr² = 441−346.5 = 94.5 ✓ *(ANS D — options me yahi tha)*
**Trap:** inscribed circle me r = a/2; circumscribed (square inside circle) me r = a√2/2 = diagonal/2.

---

## ▌D6. SECTOR / ARC / SEGMENT
**DATA: ~35 clean (46 me se angle-chase leaks Part 5).**

**PYQ 1 (sector direct)** [2024|Q18]: `r = 4, θ = 45°, π = 3.14 → sector area?` →
(45/360)×3.14×16 = 2π = **6.28 cm²** ✓
**PYQ 2 (quadrant/90° standard):** SSC 60°, 90°, 120° sectors leta hai — fractions rattne ki zarurat nahi: 90° = ¼, 60° = ⅙, 45° = ⅛ (θ/360 hi hai).
**Segment-model:** segment = sector − triangle = (θ/360)πr² − ½r²sinθ (θ in degrees; triangle formula ½ab·sinC — Part 5-bridge). Sin values Part 7 se aati hain.
**Trap:** "area of sector" vs "length of arc" — dono me θ/360 fraction same, base alag (πr² vs 2πr).

---

## ▌D7. LARGEST-FIGURE / SHADED-REGION (combo-model) ⭐
**DATA: ~15 Q — 2024 ka favourite (largest rectangle in circle, shaded regions).**

**PYQ 1 (largest rectangle in circle)** [2024|Q21]: `Circle r = 5. Largest rectangle cut out — remaining area?` →
Largest rectangle = SQUARE (diagonal = 2r = 10) → side = 10/√2 → area = 50
Remaining = 25π − 50 = **25(π−2)** ✓
*(Kyun square: diagonal fixed 2r; area = ½d₁d₂ max when d₁ = d₂ — rectangle-area identity ½×diagonals-product (rhombus formula!))*
**PYQ 2 (shaded diagram)** [2021|Q73]: `Shaded region = 45 cm²` type — subtraction chains: outer − inner (square−circles, rectangle−triangle...). **Universal: naam likho, formula lagao, minus karo.**
**Model:** "largest X in Y" = X ke special case (square, equilateral, hemisphere) — symmetry maximum deti hai.

---
---

# SECTION H — 3D MODELS (7 models • ~230 clean PYQs)

---

## ▌H1. CUBE / CUBOID (TSA + diagonal + fit-count)
**DATA: 72 Q — 2024 me 25 (sabse zyada)! Naya favourite.**

**Laws:** cuboid TSA = 2(lb+bh+hl); cube TSA = 6a²; **cube diagonal = a√3** (teeno dimensions ka Pythagoras: √(a²+a²+a²)); cuboid diagonal = √(l²+b²+h²).
**PYQ 1 (TSA direct)** [2022|Q73]: `l = 8, b = 2l = 16, h = l/2 = 4 → TSA?` → 2(128+64+32) = **448 cm²** ✓
**PYQ 2 (diagonal → TSA)** [2021|Q55]: `Cube diagonal 8√3 → TSA?` → a = 8 → 6×64 = **384 cm²** ✓
**PYQ 3 (fit-count)** [2021|Q67]: `Trench 16×12×4 m; slabs 4×0.5×0.2 m. Kitne slabs?` →
Volume = 768/0.4 = **1920** ✓ *(dimensions exactly divide — volume-divide hi kaafi; agar na katein to dimension-wise floor karo)*
**PYQ 4 (boxes-fit)** [2024|Q25]: `Box 6×10×12; cubes of volume 216 (side 6)...` — box-fitting me **volume-divide approx nahi** — dimension-wise: 6→1, 10→1, 12→2 = 2 cubes/box `[ANS-key OCR-ambiguous — METHOD: dimension-wise multiply, volume nahi]`
**Trap:** fit-count me volume ÷ volume tabhi sahi jab sides exactly divide karein. 10 me side-6 cube ek hi baar aata hai (4 waste).

---

## ▌H2. CYLINDER (V/CSA/TSA + capacity-litres + CSA&V combo) ⭐
**DATA: 42 Q — 2024 me 15.**

**Laws:** V = πr²h; CSA = 2πrh; TSA = 2πr(r+h); open-top = πr² + 2πrh (base + wall).
**PYQ 1 (capacity → litres)** [2024|Q20]: `r = 2.1, h = 6.3 → capacity (litres)?` →
V = 22/7×4.41×6.3 = 87.318 m³ → **87,318 L** ✓ *(0.4-unit conversion — 1 m³ = 1000 L)*
**PYQ 2 (CSA & V dono diye — COMBO!)** [2019|Q13]: `Pole: CSA = 132, V = 528. Height?` →
V/CSA = r/2 → r = 8 → h = 132/(2π×8) = 2.625 = **2⅝ m** ✓
*(Ye combo SSC ka pasandida hai: divide karke r/2 ya r mil jaata hai — formulas eliminate ho jaate hain)*
**PYQ 3 (ratio)** [2022|Q21]: `h ratio 2:3, r ratio 6:5 → V ratio?` → 36×2 : 25×3 = **24:25** ✓
**PYQ 4 (r:h + V)** [2024]: `r:h = 6:7, V = 792 → CSA?` → 22/7×36k²×7k = 792 → k = 1 → r = 6, h = 7 → CSA = 2×22/7×42 = **264 cm²** ✓
**PYQ 5 (d + CSA → TSA)** [2024]: `d = 14, CSA = 352 → TSA?` → 2πrh = 352 → h = 8 → TSA = 2π×7×15 = **660 cm²** ✓
**PYQ 6 (bisected cylinder)** [2022|Q19]: Part-1 A12 me solved — **+58.33%** TSA (dataset-flagged).
**Trap:** "capacity" answer LITRES me chahiye — m³ ko ×1000. Aur open-top "tank without lid" me top-circle mat jodo.

---

## ▌H3. CONE (l-Pythagoras + CSA/TSA + largest-cone-in-cube)
**DATA: 44 Q — 2021 me 14 (tent season), 2023-24 me regular.**

**PYQ 1 (V direct)** [2024|Q4]: `h = 24, r = 10.5 → V?` → ⅓×22/7×110.25×24 = **2772 cm³** ✓
**PYQ 2 (C+h → CSA)** [2022|Q54]: `Base C = 88, h = 28 → CSA?` →
r = 14 → l = √(196+784) = √980 = 14√5 → CSA = πrl = 22/7×14×14√5 = **616√5 cm²** ✓
**PYQ 3 (d+l → TSA)** [2021|Q62]: `d = 10, l = 16 → TSA?` → πr(l+r) = 22/7×5×21 = **330 cm²** ✓
**PYQ 4 (largest cone in cube)** [2023|Q19]: `Cube edge 35. Largest cone?` →
r = 17.5, h = 35 → V = ⅓×22/7×306.25×35 = **11,229.17 cm³ ≈ 11.23×10³** ✓
*(Largest = base poore face me inscribed circle (r = edge/2) + height = edge)*
**Tent-model:** conical tent = CSA hi canvas (base nahi); "canvas cost" = CSA × rate. stitching margins wale questions skip-level hain (CHSL me nahi aate).
**Trap:** l (slant) vs h (height) — question "height" de to l nikalna PART hai; "slant height" de to seedha CSA.

---

## ▌H4. SPHERE / HEMISPHERE (V↔SA conversion + paint-cost + shell) ⭐
**DATA: 65 Q — 2021 me 21, 2024 me 20. Do bade years.**

**PYQ 1 (V → SA conversion — GEM)** [2023|Q1]: `Sphere V = 4500π cm³. Surface area?` →
r³ = 4500×3/4 = 3375 = **15³** → r = 15 → SA = 4π×225 = **900π cm²** ✓
*(Method: V se r nikaalo (cube root — SSC perfect cubes deta hai: 3375, 216, 1000...), phir SA. Cube-tables 1–12 ratt — Section 0)*
**PYQ 2 (paint-cost)** [2024|Q5]: `Sphere d = 10, rate ₹2/m² [rate OCR-cut]` → SA = 4π×25 = 100π ≈ 314.16 m² → ×rate `[rate SOURCE UNCLEAR — method: 4πr²×rate]`
**PYQ 3 (bowl capacity)** [2021|Q67]: `Bowl base C = 132 → capacity?` → r = 21 → V = ⅔×22/7×9261 = **19,404 cm³** ✓
**PYQ 4 (SHELL — advanced, 2024)** [2024|Q9]: `Hemispherical bowl: inner d = 4, thickness 0.5. Silver ka volume?` →
r_in = 2, r_out = 2.5 → V = ⅔π(2.5³−2³) = ⅔π×7.625 = **15.96 cm³** ✓
*(Shell = difference of volumes — "thickness" dikhe to outer radius = inner + thickness)*
**PYQ 5 (melt-recast preview)** [2022|Q65]: `24 hemispheres → cylinder (r=12, h=24). Hemisphere ka r?` →
24×⅔πr³ = π×144×24 → 16r³ = 3456 → r³ = 216 → **r = 6** ✓ (H6-model)
**Trap:** hemisphere TSA = 3πr² (flat base ke saath), CSA = 2πr² — "bowl" ka flat rim hota hai to TSA wala use; "paint the OUTER surface of dome" = sirf CSA (2πr²).

---

## ▌H5. MELT / RECAST (volume conservation) ⭐
**DATA: 3 direct + sphere/hemisphere versions (H4 me) — milakar ~6 Q. Chhota par guaranteed-concept.**

**मूल Logic:** melt karo → material same → **TOTAL VOLUME conserved**. Sum of old volumes = new volume.
**PYQ 1 (wire square→circle — classic)** [2023|Q3]: `Wire square me hai (area 30.25). Circle me bend kiya → circle ka area?` →
square side = 5.5 → wire length = 22 (perimeter conserved!) → 2πr = 22 → r = 3.5 → area = **38.5 cm²** ✓
*(Yahan VOLUME nahi, LENGTH conserved — wire ka cross-section same rehta hai. SSC ka double-trap: kabhi volume, kabhi length!)*
**PYQ 2 (hemispheres→cylinder):** upar H4-PYQ5 — 24×⅔πr³ = πR²H ✓
**Variations (dataset me aaye):** sphere → wire (V = πr²L, L bahut bada), cone+cylinder combos.
**Trap:** "same wire bent into" = perimeter/length conservation; "melted and recast" = volume conservation. Word dekho.

---

## ▌H6. DIMENSION-% CHANGE (scaling law)
**DATA: 104 Q — Part-1 A12 me MASTER-TREATED** (multiplier (1+x)ⁿ engine). Yahan sirf summary:
- r/side +x% → area/surface ×(1+x)², volume ×(1+x)³
- l+b alag-alag % → multiply multipliers (1.4×1.7 = 2.38)
- Cylinder-bisect type CUT questions me TSA manually (naye faces add hote hain!)
**Reference PYQs:** sphere +12% → 40.49% ✓; cuboid 7%,6% → 13.42% ✓; cube side ×3 → surface +800% ✓; bisected cylinder → +58.33% ✓

---

## ▌H7. WATER-TANK / FILL (cross-ref)
Tank-filling rates = Time & Work (Part 3-P: pipes). Tank capacity = volume (yahan). **Combined questions** (tank kitni der me bharega) Part 3-P se rate + yahan se volume — 2-step chain. (Manoj-Swathi type PYQ Part 3 me classified.)

---
---

# PART 6 MASTER TRAPS (dataset-verified)

| # | Trap | Evidence |
|---|---|---|
| 1 | Rhombus: side = √[(d₁/2)²+(d₂/2)²] — POORE diagonals nahi | 10,24 → 13 |
| 2 | (l+b)² − diag² = 2×area — solve karne ki zarurat nahi | 17,46 → 120 |
| 3 | Isosceles trapezium extra-base = (a−b)/2 HAR end par | 13 |
| 4 | Inscribed circle r = a/2; square-in-circle r = a/√2 | D5, D7 |
| 5 | Largest rectangle in circle = SQUARE (diagonal 2r) | 25(π−2) |
| 6 | Capacity = m³×1000 = litres | 87,318 |
| 7 | V/CSA = r/2 — combo me formulas eliminate | 2⅝ |
| 8 | Slant l = √(r²+h²) — "height" vs "slant" word | 616√5 |
| 9 | Hemisphere TSA = 3πr² vs CSA = 2πr² (dome vs bowl) | H4 |
| 10 | Shell: outer r = inner r + thickness (diameter nahi!) | 15.96 |
| 11 | "Same wire bent" = LENGTH conserve; "melted" = VOLUME conserve | 38.5 |
| 12 | Fit-count: dimension-wise (10 me side-6 → 1), volume-divide nahi | H1 |
| 13 | V→SA: cube-root nikalta hai — perfect cubes ratta (15³ = 3375) | 900π |
| 14 | Sector fraction θ/360 DONO me (arc: 2πr base, area: πr² base) | 6.28 |
| 15 | π = 22/7 tabhi jab 7-multiples (14, 21, 154) — warna 3.14 | sector-2024 |

---

# PART 6 COVERAGE AUDIT (dataset ke against)

- Mensuration pool: 548 raw → leaks (mixture H8 ~20 → Part 9; similar-triangles ~15 → Part 5; tank-work ~4 → Part 3; angle-chase sector ~8 → Part 5; OCR-dead ~10) → **~480 clean Q, 14 models me ~93% mapped**
- **Data-driven findings:**
  - **2024 = mensuration ka record year**: cube/cuboid 25 Q + cylinder 15 + sphere 20 — 3D ne 2D ko overtake kar diya; 2017-18 me 2D (rectangle-diagonal) dominant tha
  - **Rectangle-diagonal 2018 me 17 Q** (peak) — ab bhi (l+b)²−d² trick evergreen
  - **CSA&V-combo cylinder questions** (divide → r/2) recurring elegant model
  - **Shell-thickness (2024)** aur **largest-figure (2024)** naye twists — models ready
  - Paint-cost/tent-canvas = CSA models ke costumes — har saal 2-3 Q
- Dataset-answer verification: 87,318 L; 2002 m²; 120 cm²; 52; 2√13; 13; 315; 50√2+50; 2772; 616√5; 330; 11.23×10³; 900π; 19,404; 15.96; 38.5; 1920; 448; 384 — **sab computed-match ✓**
- Cross-part dedupe: dimension-% (104 Q) Part-1 A12 master; similar-triangle areas Part 5-T6; mixture removal Part 9; pipes Part 3

**Part 6 → 14 models, ~93% coverage, 40+ verified PYQ solutions.**
