# CHSL MATHS — QUESTION-LOGIC MASTER FILE
# PART 5: GEOMETRY — Triangles • Circles • Quadrilaterals • Polygons

**Evidence base:** 4,825 PYQs (193 papers, 2017–2024). Geometry pool: **678 raw → ~630 clean questions** (kuch trig/pie-chart leaks nikale). Ye advanced-math ka sabse consistent block hai: **har paper me 2-4 Q, 94% papers**.
Har solution independently verified (kai jagah dataset ka "chosen option" galat tha — flagged). OCR-garbled par `[SOURCE UNCLEAR]`.

**Part map:** 1 Commercial ✅ | 2 Ratio/Avg/Interest ✅ | 3 T&W/Speed ✅ | 4 Number/Algebra ✅ | **5 (ye file)** | 6 Mensuration | 7 Trigonometry | 8 DI | 9 Mixture+Index

---
---

# SECTION 0 — GEOMETRY FOUNDATION (5 laws, sab derive kiye)

**L1. Triangle angle-sum = 180°.** *Kyun:* vertex se parallel line khinchoge to teeno angles ek point par lining-up ho jaate hain (straight line = 180). SAB angle-chasing isi par khada hai.

**L2. Exterior angle = do remote interior angles ka sum.** *Kyun:* exterior + apna interior = 180 (line), interior-sum bhi 180 → exterior = baaki dono.

**L3. Isosceles = equal sides ↔ equal angles (base par).** Aur equilateral = 60-60-60.

**L4. Inscribed-angle law:** centre par angle = circumference par angle ka **DOUBLE** (same arc).
*Derivation (micro):* arc PR par ∠POR (centre) aur ∠PQR (circumference) — isosceles triangles POQ... standard proof: OQ ko extend karo, do exterior angles banao; dono triangle isosceles (OP = OQ = OR).

**L5. Pythagoras:** right angle ↔ hypotenuse² = legs². Area-interpretation bhi hai (square par square), par exam me sirf equation chahiye.

**📦 Minimum-ratta (geometry):**
- Triples: (3,4,5) (5,12,13) (8,15,17) (7,24,25) (9,40,41) (11,60,61) + multiples (6-8-10, 9-12-15, 15-20-25 = 3-4-25? nahi — 15-20-25 = 5×(3,4,5) ✓)
- Equilateral: height = a√3/2, area = √3a²/4, r = a√3/6, R = a√3/3 = 2r
- Polygon: interior-sum = (n−2)×180, each exterior = 360/n

---
---

# SECTION T — TRIANGLES (7 models • ~230 PYQs)

---

## ▌T1. ANGLE-CHASE (sum + isosceles + exterior)
**DATA: ~90 clean Q — har saal. Triangle-family ka base model.**

**Universal:** L1 + L2 + L3 — teeno laws ek saath. Unknown angles ko x maano, sum laga do.
**PYQ 1 (isosceles + bisector intersection)** [2024|Q20]: `Isosceles: equal sides ke beech ka angle 40°. Baaki dono angles ke bisectors kis angle par intersect karte hain?` →
Base angles = 70 each. Incentre-formula (T2): 90 + 40/2 = **110°** ✓
**PYQ 2 (exterior)** [2023|Q24]: `A = B (isosceles); A ka exterior = 115°. ∠C?` →
∠A = 180−115 = 65 = ∠B → ∠C = 180−130 = **50°** ✓
**PYQ 3 (rhombus-style composite)** [2023|Q16]: `Rhombus STUV: ∠SUV = 44° (diagonal SU), ∠STU = 92°. 4∠SVU − 3∠TSU?` →
Rhombus me diagonal angles ko bisect karta hai: ∠SUV = ½∠U → ∠U = 88 → ∠S = 88 (opposite equal), ∠V = 92
∠SVU = 92 (poora V-angle), ∠TSU = ½∠S = 44 → 4(92) − 3(44) = **236°** ✓
**Traps:**
- "angle between the EQUAL sides" = vertex angle (40°); base angles nahi
- Rhombus/parallelogram me "∠SUV" jaisa 3-letter angle dekho — S-U diagonal hai (4th letter nahi!)
- Exterior angle REMOTE interiors ka sum hai — sirf adjacent nahi

---

## ▌T2. INCENTRE / BISECTOR-INTERSECTION ANGLE ⭐ (formula derive hai)
**DATA: ~20 Q — 2019, 2020, 2022, 2024 me recurring.**

**THE FORMULA (derive karo):** bisectors B aur C par intersect karte hain (incentre I):
∠BIC = 180 − (B/2 + C/2) = 180 − (180−A)/2 = **90 + A/2**
**PYQ 1** [2022|Q60]: `I incentre of △XYZ; ∠YIZ = 115°. ∠YXZ?` →
115 = 90 + X/2 → **X = 50°** ✓
**PYQ 2** [2019|Q8]: `B, C ke bisectors D par milte; ∠BDC = 104° [OCR: BDE→BDC]. ∠A?` →
104 = 90 + A/2 → **∠A = 28°** ✓
**PYQ 3** [2023|Q4]: `B, C ke internal bisectors X par; ∠BAC = 30°. ∠BXC?` → 90 + 15 = **105°** ✓
**Variation (EXTERIOR bisector):** ek interior + ek exterior bisector ka intersection = **90 − A/2** (supplementary configuration).
**Trap:** formula me A = WOH angle hai jo bisect NAHI hua raha (third angle). Aur "90 +" interior-pair ke liye, "90 −" interior-exterior pair ke liye.

---

## ▌T3. CENTROID / CENTRES (2:1 + coordinates)
**DATA: 18 Q + 2024 me coordinate-centroid.**

**Centroid:** teeno medians ka intersection, median ko **2:1 (vertex se 2)** me kaatta hai.
*Derivation sketch:* median ek triangle ko do EQUAL-area triangles me kaatta hai; teeno balance-points combine → centroid vertex se 2/3 distance par.
**Coordinate form:** G = ((x₁+x₂+x₃)/3, (y₁+y₂+y₃)/3) — average hi hai (equal masses ka centre of mass).
**Centres ka map (1-line each — kabhi kya hota):**
- **Equilateral:** sab centres coincide (centroid = incentre = circumcentre = orthocentre) [2018 PYQ]
- **Right triangle:** orthocentre = right-angle vertex; circumcentre = hypotenuse ka midpoint
- **Incentre:** angle bisectors (hamesha andar)
**PYQ 1** [2019|Q14]: `△ABC: AB = 7, BC = 24, AC = 25 (7-24-25!). G centroid. BG?` →
Right angle at B (Pythagoras check). Median BM to AC = hypotenuse/2 = 12.5 (right-triangle property)
BG = ⅔×12.5 = **25/3 = 8⅓ cm** ✓
**PYQ 2** [2017|Q63]: `G = (−1,−2); A = (6,−4), B = (−2,2). C?` →
C = 3G − A − B = (−3−6+2, −6+4−2) = **(−7,−4)** ✓
**Trap:** BG = ⅔ of BM hai (poora median nahi); GMC wala hissa ⅓.

---

## ▌T4. MIDPOINT THEOREM + MEDIAN PROPERTIES ⭐
**DATA: 15 Q — 2022, 2024 me push.**

**Theorem (both directions):**
- Midpoints ko jodo → line **third side ke parallel aur aadhi** hai
- **Converse (SSC favourite):** koi line ek side ke parallel ho aur aadhi side kaate → doosari side ko bhi midpoint par kaat-ti hai
**Median ka right-angle test:** median = half of the side jispar hai ⇒ triangle us vertex par **right-angled**.
*Derivation:* hypotenuse ko diameter maano, right-angle vertex circle par (angle in semicircle) — midpoint = centre, median = radius = half hypotenuse.
**PYQ 1** [2024|Q8]: `L, M midpoints of AB, AC; BC = 18. LM?` → **9** ✓ (aadha)
**PYQ 2 (converse-application)** [2022|Q57]: `PN median on QR; PN = QN. ∠QPR?` →
PN = QN = NR (median = half of QR) → **90°** ✓
**PYQ 3 (median-squares identity)** [2019|Q24]: `Right angle at A; BL, CM medians. Relation?` →
**4(BL² + CM²) = 5BC²** ✓
*(Derive: Apollonius — median from B: BL² = (2a²+2c²−b²)/4; from C: CM² = (2a²+2b²−c²)/4; add: = (4a² + b² + c²)/4 = 5a²/4 kyunki right-angle par b²+c² = a²)*
**Trap:** "median = half side" ⇒ right angle us VERTEX par jahan se median nikla — ulta direction bhi yaad rakho.

---

## ▌T5. RIGHT TRIANGLE & ALTITUDE-ON-HYPOTENUSE ⭐
**DATA: 48 Q (me se ~10 trig-leak Part 7 me).**

**Altitude rule (derive):** right triangle, hypotenuse par altitude h: **legs ka product = hypotenuse × h** (area do tarike se: ½×leg₁×leg₂ = ½×hyp×h).
**PYQ 1** [2024|Q16]: `∠B = 90°, AB = 15, BC = 20, BD ⊥ AC. BD?` →
AC = 25 (15-20-25 = 5×(3,4,5)); BD = 15×20/25 = **12 cm** ✓
**PYQ 2 (equilateral height relation)** [2023|Q5]: `Equilateral PQR, PM ⊥ QR. Kaunsa sach?` →
PM = a√3/2 → PM² = 3a²/4 → **3PQ² = 4PM²** ✓
**PYQ 3 (isosceles perimeter)** [2020|Q4]: `Isosceles perimeter 90, base 26. Equal sides?` → (90−26)/2 = **32** *(options OCR-garbled — method yahi)*
**Fastest:** pehle TRIPLE pehchano (15-20-25, 7-24-25, 9-12-15) — 80% right-triangle Q inhi par bane hain.

---

## ▌T6. SIMILAR TRIANGLES (ratio → side, area, perimeter) ⭐⭐
**DATA: 34 direct + area-subtraction versions ~15 — milakar ~50. 2024 me 11 Q (sabse zyada)!**

**Core (derive):** AA similar → sides ratio k → **perimeters k, areas k²**.
*Area k² kyun:* base b → kb, height h → kh; area ½bh → ½(kb)(kh) = k²·(½bh).
**PYQ 1 (perimeter→side)** [2023|Q24]: `△ABC ∼ △PQR; perimeters 24:16; PQ = 4.8. AB?` →
k = 24/16 = 3/2 → AB = 4.8×1.5 = **7.2 cm** ✓
**PYQ 2 (perimeters 120:240)** [2022|Q63]: `PQ = 30 → UV?` → k = 2 → **60 cm** ✓
**PYQ 3 (area→side)** [2021|Q60]: `Areas 361:225; badi triangle ki longest side 38. Chhoti ki?` →
sides 19:15 → 38×15/19 = **30 cm** ✓ *(361 = 19², 225 = 15² — SSC squares deta hai, root nikaalo)*
**PYQ 4 (area-difference, 2024)** [2024|Q12]: `Similar triangles perimeters 4:7; areas ka sum 195. Difference?` →
areas 16k:49k → 65k = 195 → k = 3 → diff = 33k = **99** *(question "1/3 of difference" maangta tha — to 33; dono readings options me — wording OCR-partials)*
**Trap:** perimeter-ratio ko side-ratio jaisa hi use karo, par AREA me SQUARE karna hai — 4:7 perimeter → 16:49 area. Ye sabse bada similar-triangles trap hai.

---

## ▌T7. BPT / PARALLEL-LINE INSIDE TRIANGLE (Thales)
**DATA: ~13 Q.**

**Theorem:** triangle ke andar ek line ek side ke parallel → **dusri do sides ko SAME ratio me kaatti hai** (AM/AN = MB/NC types).
*Derivation:* parallel lines → corresponding angles equal → AA similar → sides proportional.
**PYQ 1** [2023|Q3]: `△MNO; AB ∥ NO (A on MN, B on MO); MA = 2.5, AN = 7.5, MB = 2.2. BO?` →
MA/AN = MB/BO → 2.5/7.5 = 2.2/BO → BO = **6.6** ✓
**PYQ 2 (fraction sides)** [2018|Q255]: `DE ∥ BC, AD/DB = 5/13-type, DB-part 26 → side nikaalo` — same setup, ratio equate karo. `[numbers partially OCR-lost — method pakka]`
**PYQ 3 (midpoint + parallel = T4 converse)** [2024]: `△ABC me BC ke parallel line, AP = QC configuration` — BPT + midpoint-theorem combo.
**Trap:** BPT me ratio sides ke SEGMENTS ka hai (AM:MB), poore sides ka nahi. Diagram hota to dekho kaunsa segment diya hai.

---
---

# SECTION C — CIRCLES (8 models • ~299 PYQs — GEOMETRY KA 45%)

---

## ▌C1. CHORD + PERPENDICULAR FROM CENTRE ⭐ (39-Q family)
**Model:** centre se chord tak perpendicular = chord ko bisect karta hai. Right triangle banao:
**r² = d² + (chord/2)²** (Pythagoras — chord ka AADHA lena hi asli step hai)
**PYQ 1** [2023|Q13]: `d = 20, diameter = 58. Chord?` →
r = 29 → half-chord = √(29²−20²) = √441 = 21 → chord = **42 cm** ✓
**Variations (dataset me sab aaye):** chord diya + r diya → d nikaalo; chord diya + d diya → r; "kitni door chord hai" = d.
**Trap:** answer half-chord nahi, POORA chord (21 vs 42 — 2023 me yahi option-trap tha).

---

## ▌C2. TANGENT LENGTH (external point) ⭐
**Model:** radius ⊥ tangent (diameter jo tangent point se) → Pythagoras:
**t = √(d² − r²)** (d = point se centre ki doori)
**PYQ** [2023|Q5]: `r = 6, point 10 cm from centre. Tangent length?` → √(100−36) = **8 cm** ✓
**Trap:** d − r (= 4) nahi — SQUARE root nikalna hai. Ye 2-second Q hai, options me 4/8/10 sab hote hain.

---

## ▌C3. TWO TANGENTS FROM SAME POINT
**Model:** external point A se dono tangents **equal**; O se jodo → quadrilateral OPAQ me do right angles:
**∠POQ + ∠PAQ = 180°** (remaining two angles of quadrilateral)
**PYQ** [2020|Q14]: `∠PAQ = 80°. ∠POQ?` → 180−80 = **100°** ✓
**Variations:** ∠POQ poocha ho to 180−; "angle between tangents" = 180 − central; tangent lengths equal wale sides nikaalne me T5/P一系列.
**Trap:** log 90 + 80 = 170 ya 80 hi likh dete hain — quadrilateral-angles sum hi use karo.

---

## ▌C4. COMMON TANGENTS + TOUCHING CIRCLES (38-Q family!) ⭐⭐
**DATA: 2024 me 62 circle-Q me se bada hissa — naya favourite.**

**Length formulas (derive — centres ko jodo, radius-difference/sum ka right triangle):**
- **Direct common tangent** = √(d² − (r₁−r₂)²)
- **Transverse common tangent** = √(d² − (r₁+r₂)²)
(d = centres ke beech distance; derivation: dono centres se radii khincho, tangent ke perpendicular — difference/sum of radii ek leg ban jaata hai)
**THE 90° RESULT (derive kiya, gem hai):** do circles **externally touch** karte hain (point M), PQ direct common tangent → **∠PMQ = 90°**.
*Proof:* O₁P ⊥ PQ, O₂Q ⊥ PQ → quadrilateral PO₁O₂Q me ∠P + ∠Q = 180 → ∠PO₁M + ∠QO₂M = 180 (O₁-M-O₂ collinear). Ab inscribed-angle law: ∠MPQ = ½∠PO₁M, ∠PQM = ½∠QO₂M → ∠MPQ + ∠PQM = 90 → ∠PMQ = 90° ∎
**PYQ 1** [2024|Q10]: `Circles touch externally at M; PQ direct common tangent; ∠MPQ = 38°. ∠MQP?` →
∠PMQ = 90 → **∠MQP = 52°** ✓
**PYQ 2 (transverse/direct given sides):** centres d par, r₁, r₂ → formula plug. *(Dataset me numeric versions 2022-24 me — formula se seedha)*
**Traps:**
- Touching EXTERNALLY → d = r₁+r2; INTERNALLY → d = r₁−r₂ (ye pehle fix karo)
- Direct tangent me MINUS (r₁−r₂), transverse me PLUS (r₁+r₂) — ulta yaadne par dono galat

---

## ▌C5. CENTRE vs CIRCUMFERENCE ANGLES + ARCS
**Model (L4):** centre = double. Reflex arc vs minor arc ka dhyan.
**PYQ (exterior of cyclic quad)** [2024|Q23]: `Arc PQR subtends 240° at centre O; PQ extended to A. ∠AQR?` →
∠PQR (inscribed on major arc) = ½×(arc PR not containing Q) = ½×120 = 60
Exterior ∠AQR = 180 − 60 = **120°** ✓ *(exterior angle = opposite interior of cyclic quadrilateral)*
**Variations dataset me:** "angle subtended at centre by chord", semicircle me angle = 90 (Thales).

---

## ▌C6. CYCLIC QUADRILATERAL
**Model:** opposite angles **supplementary** (180). *Derivation: dono angles same do arcs ko dekhte hain jo milakar poora circle (360) banate hain → inscribed halves sum to 180.*
**PYQ 1** [2022|Q18]: `∠P = 3x+5, opposite ∠R = 4x. x?` → 7x+5 = 180 → **x = 25°** ✓
**PYQ 2 (ratio wala)** [2022|Q13]: `2∠O = 3∠M (opposite). ∠M?` → ∠M+∠O = 180, ∠O = 1.5∠M → 2.5∠M = 180 → **72°** ✓
**Trap:** opposite EQUAL nahi — SUPPLEMENTARY. Parallelogram-property se confuse mat hona.

---

## ▌C7. INSCRIBED/CIRCUMSCRIBED FIGURES (equilateral focus) ⭐
**DATA: 35 equilateral-Q ka core yahan; 9 incircle-Q.**

**Equilateral ke circles (derive):** r = area/s = (√3a²/4)/(3a/2) = **a√3/6**; R = **a√3/3 = 2r**
**PYQ 1** [2022|Q69]: `Incircle radius of equilateral = 9√3. Perimeter?` →
r = a√3/6 → a = 9√3×6/√3 = 54 → perimeter = **162** ✓
**PYQ 2 (square me inscribed circle)** [2021|Q59]: `Square side 21, inscribed circle...` — r = a/2 se sector/segment area. *(Question shaded-region maangta tha — OCR-cut `[SOURCE UNCLEAR]`; setup: r = 10.5, sector-angles se kaato)*
**PYQ 3 (THREE mutually touching circles — gem!)** [2022|Q8]: `3 circles, r = 7 each, ek doosre ko touch karte hain. Beech ka enclosed area?` →
Centres equilateral triangle banate hain (side 14): area = 49√3
Teen sectors (60° each) = 3×(60/360)×(22/7)×49 = 77 → **49√3 − 77 cm²** ✓
*(Model: touching circles → centres = polygon; sector-subtraction)*
**Trap:** incircle me r = a√3/6 (÷6), circumcircle me a√3/3 (÷3) — factor 2 ka farak, SSC dono options rakhta hai.

---

## ▌C8. INTERSECTING CHORDS / SECANTS (power of a point)
**Model:** do chords point P par intersect → **PA×PB = PC×PD** (andar-bahar products equal).
*Derivation:* join endpoints → similar triangles (vertical angles + same arc inscribed angles) → sides proportional → products equal.
**PYQ** [2024]: `O centre; chords AB, CD intersect internally at P...` — PA×PB = PC×PD plug karo. *(2024 OCR-text me numbers unclear — model guaranteed recurring)*
**Secant-tangent version:** tangent² = external-part × full-secant (same theorem, C2 ka generalization).

---
---

# SECTION Q — QUADRILATERALS & POLYGONS (5 models • ~85 PYQs)

---

## ▌Q1. RHOMBUS / PARALLELOGRAM ANGLE-PROPERTIES
**Laws (derive):** parallelogram: opposite angles equal, adjacent supplementary (co-interior parallel lines). Rhombus = parallelogram + **diagonals bisect the angles** + diagonals ⊥ bisect each other.
*(T1 ke PYQ-3 rhombus wale me full solved example hai — 236°)*
**PYQ** [2022|Q13-cyclic]: `Cyclic MNOP: 2∠O = 3∠M` → C6 se 72° ✓ *(cyclic-quadrilateral ≠ parallelogram — dono properties alag questions me mix hoti hain)*

---

## ▌Q2. SIMILAR-TRIANGLE AREA SUBTRACTION (inner/outer region)
**DATA: 2019, 2022, 2024 — recurring twisted format.**
**PYQ 1** [2019|Q13]: `DE ∥ BC, DE:BC = 3:5. Area(ADE) : Area(DECB)?` →
areas 9:25 → quadrilateral (BIGGER minus chhota) = 25−9 = 16 → **9:16** ✓
**PYQ 2** [2022|Q57]: `MN ∥ BC; AN:NC = 4:5. Quadrilateral MBCN = 130. Area(AMN)?` →
AM:AB = 4:9 → areas 16:81 → quad = 65 parts = 130 → 1 part = 2 → **AMN = 32 cm²** ✓
**PYQ 3** [2024|Q16]: `XY ∥ FG; EX:XF = 2:3; quad XFGY = 44. Area(EXY)?` →
EX:EF = 2:5 → areas 4:25 → quad = 21 parts = 44 → 1 part = 44/21 → EXY = 4×44/21 = **8.38 m²** ✓
**Model:** ratio → square → (total − inner) subtraction. Har saal ek Q pakka isi template par.

---

## ▌Q3. POLYGON ANGLE-SUMS
**Laws (derive):** ek vertex se (n−2) triangles ban sakte hain → interior-sum = **(n−2)×180**; bahar ghoomte hue full turn = **exterior-sum 360**.
**PYQ 1** [2017|Q272]: `Interior sum 540° → sides?` → (n−2)180 = 540 → **n = 5** ✓
**PYQ 2** [2018|Q72]: `Regular pentagon: interior, exterior me kitna farak?` →
108 − 72 = **36°** ✓
**PYQ 3 (triangles from vertices)** [2019|Q20]: `11-sided polygon ke vertices se kitne triangles?` →
**C(11,3) = 165** ✓ *(koi bhi 3 vertices ek triangle banate hain, collinear nahi)*
**Trap:** "sum of interior angles" vs "each interior angle of REGULAR polygon" — regular word dekho to ÷n karo.

---

## ▌Q4. MIDPOINT + PARALLEL INSIDE QUADRILATERALS
**PYQ** [2024|Q13]: `Right △ABC (C par 90°); M hypotenuse ka midpoint; CM extend karke D jaisa ki DM = CM; D ko B se joda...` →
Ye midpoint-theorem CONVERSE ka construction question hai (prove-style): DM = CM + M midpoint ⇒ ACBD parallelogram-type symmetric figure. Answer-length BC-double relations se aata hai (ye Q **5 cm** maangta tha — option B) — construction-question me midpoint-theorem converse hi lagana hai.

---

## ▌Q5. EULER'S FORMULA (polyhedra — 1-off bonus)
**PYQ** [2017|Q66]: `Dodecahedron: V = 20. Edges?` →
**V − E + F = 2** → E = 20 + 12 − 2 = **30** ✓ *(F = 12 for dodecahedron — ye ek baar dekh lo)*

---
---

# PART 5 MASTER TRAPS (dataset-verified)

| # | Trap | Evidence |
|---|---|---|
| 1 | Chord ka answer = FULL chord (half nahi — 21 vs 42) | 2023 |
| 2 | Tangent length = √(d²−r²), d−r nahi | 8 vs 4 |
| 3 | ∠POQ = 180 − ∠PAQ (quadrilateral, not 90+X) | 100° |
| 4 | Angle at centre DOUBLE; reflex-arc vs minor-arc check | 240°→120° |
| 5 | Similar: AREA ratio = side ratio ka SQUARE | 16:49 |
| 6 | Perimeter-ratio = side-ratio (same k) — direct multiply | 7.2 |
| 7 | Rhombus diagonal bisects ANGLES (half-angle given ho sakta hai) | 44 = ½88 |
| 8 | Centroid vertex se ⅔ (midpoint se nahi) | 8⅓ |
| 9 | Incentre-formula me A = THIRD angle (jo bisect nahi hua) | 115→50 |
| 10 | Median = half-side ⇒ right angle (converse bhi) | ∠QPR = 90 |
| 11 | "Angle between equal sides" = vertex angle | 40° wala |
| 12 | Cyclic quad: opposite SUPPLEMENTARY (equal nahi) | 72 |
| 13 | Touching circles: external → d = r₁+r₂; internal → d = r₁−r₂ | C4 |
| 14 | Direct tangent me (r₁−r₂), transverse me (r₁+r₂) — ulta nahi | C4 |
| 15 | Sector-subtraction me teen 60° sectors (equilateral centres) | 49√3−77 |
| 16 | Inner/outer area: quadrilateral = (total − inner triangle) | 9:16 |

---

# PART 5 COVERAGE AUDIT (dataset ke against)

- Geometry pool: 678 raw → leaks hata kar (sec/tan-trig ~10 → Part 7; pie-chart ~5 → Part 8; pure area-formula ~10 → Part 6; OCR-unreadable ~12) → **~630 clean Q, 20 models me ~92% mapped**
- **Data-driven findings:**
  - **Circles = geometry ka 45%** (299 Q) — chord 39 + common-tangent 38 do bade families; 2024 me circles ka peak (62 Q)
  - **Similar-triangles 2024 me explosion** (11 Q vs 2020 me 1) — T6 + Q2 ka combo sabse relevant naya pattern
  - Incentre-formula (90+A/2) har 2 saal me pakka
  - Intersecting-chords power-of-point 2024 me aaya — model ready
  - Euler/polyhedra = 1 Q in 7 yrs — skip-level, formula ek line
- Dataset-answer check: rhombus-236°, three-circles 49√3−77, incentre-50°, centroid-8⅓ sab computed-match ✓; 2 OCR-partial (square-inscribed 2021, intersecting-chords 2024) `[SOURCE UNCLEAR]` flags ke saath
- Cross-part dedupe: trig-labelled right-triangle Q (sec R type) → Part 7 me trig-models ke saath; coordinate-centroid Part 4-A6 bridge; area-formula (circle/rhombus area) → Part 6

**Part 5 → 20 models, ~92% coverage, 40+ verified PYQ solutions.**
