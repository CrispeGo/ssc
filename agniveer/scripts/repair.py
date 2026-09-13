# -*- coding: utf-8 -*-
"""Repair content.txt: integrate missing PYQ concept families into their natural chapters."""
import sys
path = "/home/user/pdf_build/content.txt"
text = open(path, encoding="utf-8").read()

EDITS = []  # (anchor, block) — block inserted right after anchor line

def add(anchor, block):
    EDITS.append((anchor, block))

# ================= CH1 UNITS =================
add("- Density unit-conversion: 128 kg/m³ ko aise system mein badlo jahan mass unit 50 g aur length unit 25 cm ho → 128 × (1000/50) × (0.25/1)³ = 40.",
"""- °F ↔ °C: °C = (°F − 32) × 5/9 ; °F = (9/5)°C + 32. 200 °F → (200−32) × 5/9 = 93.3 °C.
- Stefan–Boltzmann constant σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴ (radiated energy ∝ T⁴).
- Pole strength ka unit A·m (magnetic dipole moment ka unit A·m²).
- Mechanical equivalent of heat: 1 cal = 4.18 J.
- CGS unit of electric dipole moment = statC·cm.""")

add("F>1 kWh = 3.6×10⁶ J ; 1 N = 10⁵ dyne ; 1 T = 10⁴ gauss ; 1 pm = 10⁻¹² m = 10⁻⁶ micron",
"""F>°C = (°F − 32) × 5/9 ; °F = (9/5)°C + 32 ; 1 cal = 4.18 J
F>σ (Stefan) = 5.67 × 10⁻⁸ W m⁻² K⁻⁴ ; pole strength unit = A·m""")

add("K>Direct fact. Nit = luminance. Lumen = luminous flux (don't mix).",
"""E>A measured temperature is 200 °F. Its value in Celsius is:
W>°C = (°F − 32) × 5/9.
x>°C = (200 − 32) × 5/9 = 168 × 5/9 = 93.3 °C.
K>Pehle 32 ghato, phir 5/9 se multiply. °C → °F iska ulta (×9/5 + 32).""")

add("- Planck's constant aur angular momentum hamesha twins hain.",
"""- °F → °C: (F − 32) × 5/9 ; 200 °F = 93.3 °C.
- 1 cal = 4.18 J (heat ↔ mechanical work ka bridge).""")

# ================= CH3 LAWS =================
add("**What is impulse?** J = F × Δt = change in momentum (Δp). Same momentum change ke liye: jitna LAMBA time, utna CHOTA force. Isi liye airbag, cushioned bed — stopping time badha kar force kam karte hain.",
"""**What is equilibrium?** Body par net force ZERO (translational) aur net torque ZERO (rotational) ho to body equilibrium mein hai. Zero resultant banane ke liye MINIMUM 2 forces chahiye — equal aur opposite (1 force kabhi zero nahi de sakta, 3-4 zaroori nahi).
**What is a resultant?** Do vectors A aur B ka resultant R = √(A² + B² + 2AB cosθ). Perpendicular (θ = 90°) → R = √(A²+B²); same direction → A+B; opposite → |A−B|.
**What is an Atwood machine?** Pulley par do masses m₁, m₂ (m₂ > m₁) hang ho → acceleration a = (m₂−m₁)g/(m₁+m₂). Massless string hai to tension dono sides par SAME.
**What is apparent weight in a lift?** Lift upar accelerate → R = m(g+a) (feel heavy). Neeche accelerate → R = m(g−a). Free fall (a = g) → R = 0 (weightless).
**Which forces are NOT electromagnetic?** Tension, friction, normal, spring — sab electromagnetic hain (atom-atom charge forces). GRAVITY aur NUCLEAR force electromagnetic NAHI hain.""")

add("- Static friction max: f_max = μₛN ; bina slip ke max acceleration a = μₛg.",
"""- Resultant: R = √(A² + B² + 2AB cosθ) ; ⊥ → √(A²+B²) → 3 kN & 4 kN → 5 kN.
- Atwood: a = (m₂−m₁)g/(m₁+m₂) ; lift: R = m(g ± a).
- Angle between vectors: cosθ = (A·B)/(|A||B|).
- Minimum forces for zero resultant = 2 (equal, opposite).""")

add("F>K = p²/2m → p = √(2mK)",
"""F>R = √(A² + B² + 2AB cosθ) ; cosθ = (A·B)/(|A||B|)
F>a_atwood = (m₂−m₁)g/(m₁+m₂) ; R_lift = m(g ± a)""")

add("- Recoil speed = (chhota mass × uski velocity)/bada mass. Bullet 100 g at 100 m/s, gun 20 kg → v = (0.1×100)/20 = 0.5 m/s.",
"""- 3 kN aur 4 kN ⊥ → resultant 5 kN (3-4-5 triangle).
- Momentum 25% badhao (p → 1.25p) → K = p²/2m → K ×(1.25)² = 1.5625 → 56.25% increment.
- Atwood: heavier side neeche, a = (m₂−m₁)g/(m₁+m₂).
- Lift upar → R = m(g+a); neeche → R = m(g−a).""")

add('- "Max acceleration without slipping" → a = μₛg.',
"""- "Resultant of two forces" → R = √(A²+B²+2AB cosθ).
- "Zero resultant minimum forces" → 2.
- "Pulley / two masses" → Atwood a = (m₂−m₁)g/(m₁+m₂).
- "Weight in a lift" → m(g ± a).""")

add("K>Momentum ∝ velocity (mass constant). KE ∝ v² — dono confuse mat karo.",
"""E>A particle's linear momentum is increased by 25%. The percentage increase in kinetic energy is:
W>K = p²/2m — momentum ka factor square hota hai.
x>p → 1.25p → K ∝ (1.25)² = 1.5625 → 56.25% increase.
K>p ×n → K ×n². 1.25² = 1.5625 (56.25% up).
E>Two forces of 3 kN and 4 kN act perpendicular to each other. Their resultant is:
W>Perpendicular vectors → Pythagoras.
x>R = √(3² + 4²) = 5 kN.
K>3-4-5 right triangle → resultant 5 kN.
E>Two masses m₁ and m₂ (m₂ > m₁) hang from a frictionless pulley. The acceleration is:
W>Atwood machine formula.
x>a = (m₂ − m₁)g/(m₁ + m₂).
K>Net force (m₂−m₁)g ko total mass (m₁+m₂) se divide karo.""")

add("- Recoil speed = (small mass × velocity)/big mass.",
"""- 3 kN ⊥ 4 kN → 5 kN ; p ×1.25 → K ×1.5625.
- Zero resultant ke liye minimum 2 forces (equal-opposite).""")

add("C>Airbag stopping TIME badhata hai → force GHATTI hai (J = FΔt).",
"""T>Zero resultant ke liye 1 ya 3 forces kaafi hain.
C>Minimum 2 forces (equal aur opposite). 1 force kabhi zero resultant nahi deta.
T>Momentum 25% badhao to KE bhi 25% badhti hai.
C>K ∝ p² → (1.25)² = 1.5625 → 56.25% increase.""")

# ================= CH4 WORK =================
add('**Work-energy theorem.** W_total = ΔK — net work = kinetic energy ka change. Ye theorem hi har "force → speed" problem ka shortcut hai.',
"""**What is elastic energy in a wire?** Wire ko stretch karne par stored energy U = (1/2)F × ΔL. Energy density (per volume) = (1/2) × stress × strain = (1/2)Y(strain)² — bilkul spring ke (1/2)kx² jaisa, bas wire ke terms mein.
**Work done pulling a hanging chain.** Uniform chain ka kuch hissa table se latka ho to use upar kheenchne ka work = (hanging mass) × g × (uske centre of mass ki raise). Ek-third length latki ho to W = (m/3) × g × (L/6) = mgL/18.""")

add("- Variable force: W = ∫F dx. F = 3ax² − 3 from 0 to 2 → 8a − 6.",
"""- Wire energy: U = (1/2)FΔL = (1/2)Y × (ΔL/L)² × volume. Energy density = (1/2) × stress × strain.
- Chain (1/3 length L hanging): W = (m/3) × g × (L/6) = mgL/18.""")

add("F>W_spring(x₁→x₂) = (1/2)k(x₂² − x₁²)",
"""F>U_wire = (1/2)FΔL ; energy density = (1/2) × stress × strain = (1/2)Y(strain)²
F>W_chain = (hanging mass) × g × (height of its centre of mass)""")

add("K>Motion oppose karne wala force hamesha negative work karta hai.",
"""E>Energy stored in a stretched wire is (Y = Young's modulus, S = strain):
W>Elastic energy density in a wire.
x>Energy density = (1/2) × stress × strain = (1/2)Y S².
K>Wire energy density = (1/2)Y(strain)² — spring ke (1/2)kx² ka wire version.
E>A uniform chain of length L and mass m lies on a table with one-third of its length hanging. Work to pull it up:
W>Work = mgh for the hanging part's centre of mass.
x>W = (m/3) × g × (L/6) = mgL/18.
K>Hanging part ka CM L/6 neeche hai — sirf hanging mass par mgh lagao.""")

add("- Dot product: (2)(1)+(3)(2)+(1)(−4) = 4 — one line.",
"""- Wire energy density = (1/2) × stress × strain.
- Chain pull-up: W = (hanging mass) × g × (CM height).""")

# ================= CH5 ROTATIONAL =================
add("**Radius of gyration.** k = wo distance jahan saara mass rakhne par same I mile: I = Mk².",
"""**CM of uniform bodies.** Uniform cube/sphere/rod ka CM GEOMETRIC CENTRE par hota hai — cube ka CM body ke centre par (face ya edge par nahi).
**CM formula.** x_cm = Σ(mx)/Σm ; V_cm = Σ(mv)/Σm. Do bodies ka system: V_cm = (m₁v₁ + m₂v₂)/(m₁+m₂).
**KE of centre of mass.** System ki CM motion ki KE = (1/2)(m₁+m₂)V_cm². (Total KE = CM ki KE + relative motion ki KE.)
**Angular acceleration in UCM.** Uniform circular motion mein ω CONSTANT → angular acceleration α = 0.""")

add("- Disc diameter = I → ⊥ axis through rim = 6I (I = MR²/4 ⇒ MR² = 4I; rim = 2I + 4I).",
"""- CM: x_cm = Σ(mx)/Σm ; V_cm = Σ(mv)/Σm ; KE_cm = (1/2)(Σm)V_cm².
- τ = r × F (cross product); magnitude rF sinθ; direction right-hand rule se.
- UCM: ω constant → α = 0.""")

add("K>Mutual attraction = internal force → V_cm nahi badalta.",
"""E>The centre of mass of a uniform cube is at:
W>Uniform body → geometric centre.
x>Cube ka CM uske geometrical centre par hota hai (face/edge/diagonal par nahi).
K>Uniform (symmetric) body ka CM = geometric centre.
E>A ball of mass M (2 m/s) hits a 1 kg ball (1 m/s). KE of centre of mass is 4/3 J. Find M:
W>KE_cm = (1/2)(M+1)V_cm² ; V_cm = (2M + 1×1)/(M+1).
x>(1/2)(M+1)[(2M+1)/(M+1)]² = 4/3 → (2M+1)² = (8/3)(M+1).
x>3(4M²+4M+1) = 8M+8 → 12M²+4M−5 = 0 → M = 0.5 kg.
K>KE_cm = (1/2)(Σm)V_cm² — pehle V_cm nikalo, phir KE.""")

add("- Kepler equal areas = angular momentum conservation.",
"""- Uniform body → CM at geometric centre.
- UCM mein α = 0 (ω constant).""")

# ================= CH6 GRAVITATION =================
add("- g = GM/R² ; g' at height h (h << R): g' = g(1 − 2h/R).",
"""- g at depth d: g' = g(1 − d/R) — Earth ke centre par zero.
- g = (4/3)πGρR (density form): same radius → g ∝ ρ; same density → g ∝ R.""")

add("- Satellite: PE = 2 × total energy. Total energy E₀ → PE = 2E₀, KE = −E₀.",
"""- Radii 1:4, densities 1:2 → g ratio = (ρ₁R₁)/(ρ₂R₂) = (1×1)/(2×4) = 1:8.
- Height par g 1/4 rah jaye → (1−2h/R) = 1/4 → h = 3R/8.""")

# ================= CH7 BULK =================
add("Bernoulli = energy conservation; continuity = mass conservation.",
"""**What is calorimetry?** Heat transfer Q = mcΔT. m = mass, c = specific heat, ΔT = temperature change. Mixture: heat gained = heat lost. Water ki specific heat sabse zyada: 1 cal/g°C = 4186 J/kg°C.
**What is thermal expansion?** Garam karne par solid expand hota hai. Linear ΔL = αLΔT ; area ΔA = βAΔT (β = 2α) ; volume ΔV = γVΔT (γ = 3α). Isliye α : β : γ = 1 : 2 : 3. Thermometer isi expansion par chalta hai.
**Why does hot glass crack on sudden cooling?** Bahar ki layer pehle sikud jaati hai, andar nahi → thermal STRESS → crack (glass heat ka poor conductor hai).
**What is capillary rise?** Patli tube mein liquid upar chadhta hai: h = 2T cosθ/(rρg). Tube patli (r chhota) → rise zyada. Water-glass θ = 0° → h = 2T/(rρg).
**Float fraction.** Floating body ka submerged fraction = ρ_body/ρ_liquid. Cube density 800 kg/m³, water 1000 → 80% andar, 20% bahar.
**Breaking stress.** Wo maximum stress jis par material toot jaata hai (strength). Steel ki elasticity sabse zyada (steel > copper > rubber).
**Moduli.** Bulk modulus K = −ΔP/(ΔV/V) (compress karne ka resistance); modulus of rigidity G = shear stress/shear strain.""")

add("- Work to stretch wire = (1/2)F × ΔL (elastic PE).",
"""- Q = mcΔT ; heat lost = heat gained.
- α : β : γ = 1 : 2 : 3 ; ΔL = αLΔT ; ΔV = γVΔT.
- Capillary: h = 2T cosθ/(rρg).
- Float: submerged fraction = ρ_body/ρ_liq ; n drops combine → radius ×n^(1/3).
- K = −ΔP/(ΔV/V) ; G = shear stress/shear strain.""")

add("F>Gauge pressure = P − Pₐ ; P = ρgh",
"""F>Q = mcΔT ; ΔL = αLΔT ; ΔA = 2αAΔT ; ΔV = 3αVΔT
F>h = 2T cosθ/(rρg) ; submerged fraction = ρ_body/ρ_liq
F>Bulk modulus K = −ΔP/(ΔV/V) ; rigidity G = shear stress/shear strain""")

add("- Water drops diameter 1 cm & 1.5 cm → radii 1:1.5 → ΔP ratio = 1.5:1 = 3:2.",
"""- 8 equal drops combine → R = n^(1/3) r = 2r → ΔP becomes 1/2 (ΔP ∝ 1/r).
- Water drop 27 droplets mein toota → r' = r/3 → ΔP' = 3ΔP.
- Capillary d = 2 mm, rise 15 mm, θ = 0°, SG 0.8 → T = rρgh/2 = (1×10⁻³)(800)(9.8)(0.015)/2 = 0.0588 N/m.
- Gas at constant T: PV = constant (Boyle's law).""")

add('- "Meniscus/contact angle" → convex = mercury (140°).',
"""- "Heat / temperature change / specific heat" → Q = mcΔT.
- "Length/volume on heating" → αLΔT / γVΔT.
- "Capillary rise" → h = 2T cosθ/(rρg).
- "Fraction floating" → ρ_body/ρ_liq.""")

add("K>Linear region ka slope hi Y hai.",
"""E>A gas of 240 ml is heated from 27 °C to 227 °C at constant pressure. New volume:
W>Charles' law — V ∝ T (kelvin mein).
x>V₂ = V₁ × T₂/T₁ = 240 × 500/300 = 400 ml.
K>V ∝ T (kelvin): 300 → 500 K, to 240 → 400 ml.
E>A capillary of diameter 2 mm is dipped in liquid (specific gravity 0.8). Rise 15 mm, contact angle 0°. Surface tension:
W>h = 2T cosθ/(rρg) → T = rρgh/2.
x>T = (1×10⁻³)(800)(9.8)(15×10⁻³)/2 = 0.0588 N/m.
K>T = rρgh/2 — r metre mein, ρ = 800 kg/m³, h metre mein.
E>A metal ball just passes through a ring. Only the ball is heated. It will:
W>Thermal expansion of the ball.
x>Ball expand hota hai → ab ring mein pass nahi karega.
K>Heat ball → expand → won't pass through the ring.
E>A water drop is divided into 27 equal droplets. Pressure difference inside each droplet becomes:
W>r' = r/3 → ΔP ∝ 1/r.
x>ΔP' = 3ΔP (radius ek-third → pressure 3×).
K>27 = 3³ → radius ÷3 → ΔP ×3.
E>A cube floats in water with some part outside. The fraction submerged depends on:
W>Float condition: submerged fraction = ρ_body/ρ_liq.
x>Density ratio decide karta hai kitna hissa andar hai.
K>Submerged fraction = ρ_body/ρ_water.""")

add("- Stress-strain slope = Young's modulus.",
"""- Q = mcΔT (heat = mass × c × ΔT).
- α:β:γ = 1:2:3 ; radius ÷n → ΔP ×n (drops).
- Capillary: h = 2T cosθ/(rρg).""")

add("- Venturi-meter flow speed; manometer pressure difference; Pascal = pressure; Archimedes = buoyancy.",
"""- Water: c = 1 cal/g°C = 4186 J/kg°C (highest); 1 cal = 4.18 J.
- Steel sabse elastic; thermometer thermal expansion par chalta hai.
- Liquid ka η temperature ke saath GHATTA hai; gas ka η BADHTA hai.""")

add("C>Slope = Young's modulus.",
"""T>Heat dene par body ka temperature hamesha badhta hai.
C>Phase change (ice → water) mein temperature CONSTANT rehta hai (latent heat).
T>Area expansion coefficient = 3α.
C>β = 2α (area), γ = 3α (volume) — 1:2:3 ka order.
T>Ice melts in brim-full cup → water overflows.
C>Level SAME rehta hai (displaced water = ice ka weight).""")

# ================= CH8 THERMO =================
add("**Carnot engine.** Do temperatures ke beech maximum efficiency wala ideal engine: η = 1 − T₂/T₁ (temperatures KELVIN mein!).",
"""**Isochoric (constant volume).** V constant → koi expansion nahi → work W = 0. Tab ΔQ = ΔU (saari heat internal energy ban jaati hai).
**Isobaric (constant pressure).** W = PΔV (pressure × volume change).
**Refrigerator.** Heat engine ka ULTA — sink se heat nikal kar source ko deta hai. Coefficient of performance COP = Q₂/W = T₂/(T₁−T₂) (kelvin mein). Ye engine ki efficiency ka reciprocal NAHI hai.
**Polytropic process PVⁿ = constant.** n = 1 → isothermal, n = γ → adiabatic. Work done W = (P₁V₁ − P₂V₂)/(n − 1).""")

add("- 200 J work ON gas (adiabatic) → ΔU = +200 J.",
"""- Isochoric: W = 0, ΔQ = ΔU ; Isobaric: W = PΔV.
- Refrigerator COP = T₂/(T₁ − T₂). 0 °C–100 °C → 273/100 = 2.73.
- PV² = constant → W = (P₁V₁ − P₂V₂)/(2 − 1).""")

add("F>T(K) = t(°C) + 273",
"""F>Isochoric: W = 0 ; Isobaric: W = PΔV ; COP_ref = T₂/(T₁−T₂)
F>PVⁿ = const → W = (P₁V₁ − P₂V₂)/(n−1)""")

add("- Source temperature badhao → Carnot efficiency badhti hai.",
"""- Isochoric (V constant) → W = 0 → ΔQ = ΔU.
- Refrigerator 0 °C & 100 °C → COP = 273/(373−273) = 2.73.
- Gas law names: PV = constant (Boyle, T const); V ∝ T (Charles, P const); P ∝ T (Gay-Lussac, V const).""")

add("K>W = η × Q₁ — efficiency ko heat se multiply karo.",
"""E>Work done by a gas in an isochoric process is:
W>Isochoric = constant volume.
x>ΔV = 0 → W = PΔV = 0.
K>Volume constant → koi work nahi (W = 0).
E>A Carnot refrigerator operates between 0 °C and 100 °C. Its coefficient of performance is:
W>COP = T₂/(T₁−T₂).
x>COP = 273/(373−273) = 273/100 = 2.73.
K>COP = T_cold/(T_hot − T_cold) — kelvin mein.
E>A gas expands with PV² = constant from P₁ = 320 kPa, V₁ = 0.04 m³ to P₂ = 80 kPa. Work done:
W>Polytropic work formula (n = 2).
x>V₂ = V₁√(P₁/P₂) = 0.04 × 2 = 0.08 m³.
x>W = (P₁V₁ − P₂V₂)/(n−1) = (12800 − 6400)/1 = 6400 J = 6.4 kJ.
K>W = (P₁V₁ − P₂V₂)/(n−1); pehle V₂ nikalo (PVⁿ = const se).""")

add("- η = 1 − T_cold/T_hot (hamesha kelvin).",
"""- Isochoric → W = 0 (instant).
- Refrigerator COP = T_cold/(T_hot − T_cold).""")

add("C>Second law ENTROPY define karta hai.",
"""T>Refrigerator ka COP = engine ki efficiency.
C>COP = T₂/(T₁−T₂) — engine η = 1 − T₂/T₁ se bilkul alag.
T>Isochoric mein gas kaam karti hai.
C>V constant → W = PΔV = 0.""")

# ================= CH9 KINETIC =================
add("**What is sound speed in a gas?** v = √(γP/ρ). Constant temperature par pressure double karo to density bhi double → v UNCHANGED.",
"""**What is rms speed?** Molecules ki speeds ka root-mean-square: v_rms = √(3RT/M) = √(3P/ρ) = √(3k_BT/m). Matlab: v_rms ∝ √T (temperature ka square root) aur v_rms ∝ 1/√M (molar mass ka ulta square root). Constant temperature par pressure se INDEPENDENT hai.
**Gas law names.** Boyle: PV = constant (T const). Charles: V ∝ T (P const). Gay-Lussac: P ∝ T (V const). Teeno milkar ideal gas law PV = nRT banate hain.""")

add("- van der Waals: (P + a/V²)(V − b) = RT ; a ka dimension [ML⁵T⁻²].",
"""- v_rms = √(3RT/M) = √(3P/ρ). O₂ (M = 32) at 300 K → 483 m/s; at 1200 K → 483 × 2 = 966 m/s.
- Pressure double + T half → v_rms ×(1/√2) (P se independent, sirf √T se).
- Boyle: PV const; Charles: V ∝ T; Gay-Lussac: P ∝ T.""")

add("F>v = √(γP/ρ) ; van der Waals 'a' : [ML⁵T⁻²]",
"""F>v_rms = √(3RT/M) = √(3P/ρ) ; v_rms ∝ √T, ∝ 1/√M
F>Boyle: PV = const ; Charles: V ∝ T ; Gay-Lussac: P ∝ T""")

add("K>a/V² pressure jaisa → a ka dimension [ML⁵T⁻²].",
"""E>The rms speed of oxygen molecules at 300 K is about 483 m/s. The rms speed at 1200 K is:
W>v_rms ∝ √T.
x>v₂ = v₁ × √(1200/300) = 483 × 2 = 966 m/s.
K>Temperature 4× → rms speed 2× (√4).
E>The rms speed of a gas is v. If pressure is doubled and temperature is halved, the new rms speed is:
W>v_rms ∝ √T (constant T par pressure se independent).
x>v' = v × √(1/2) = v/√2.
K>rms speed sirf √T aur 1/√M par depend — pressure nahi.
E>PV = constant at constant temperature is which law?
W>Gas law names.
x>Boyle's law (T constant → PV constant).
K>Boyle = PV; Charles = V/T; Gay-Lussac = P/T.""")

add("- van der Waals 'a' → [ML⁵T⁻²].",
"""- rms speed: T 4× → v 2× ; M 4× → v half.
- Boyle PV, Charles V/T, Gay-Lussac P/T.""")

# ================= CH10 WAVES =================
add("**Sound.** Mechanical wave; speed solids > liquids > gases. Bats ultrasonic waves (reflection) se obstacles detect karte hain.",
"""**What is a wave number?** k = 2π/λ — 2π length mein kitni waves (propagation constant bhi kehte hain). y = A sin(ωt − kx) mein x ka coefficient hi k hai.
**What is a stationary wave?** Do SAME waves opposite directions mein milti hain to stationary wave banti hai. Isme ENERGY TRANSFER NAHI hota (energy nodes ke beech trapped). Nodes = zero displacement, antinodes = maximum.
**What is intensity of a wave?** Intensity ∝ (amplitude)² — amplitude double → intensity 4×.
**SHM phase relations.** x = A sin ωt. Velocity v = dx/dt leads x by 90°; acceleration a = −ω²x is 180° out of phase with x (a leads v by 90°). Mean par v max; extreme par a max.
**Phase difference of two waves.** y = A sin(ωt + φ₁) aur y = A sin(ωt + φ₂) → phase difference = |φ₁ − φ₂|.""")

add("- SHM energy E ∝ A² (A double → KE ×4).",
"""- k = 2π/λ ; v = ω/k ; particle velocity in wave: v_max = Aω.
- I ∝ A² ; stationary wave → energy transfer ZERO.
- SHM: v leads x by 90°; a leads v by 90° (a = −ω²x).
- Two waves: Δφ = |φ₁ − φ₂| (π/3 − π/4 = π/12).""")

add("F>vmax = ωA ; amax = ω²A ; v = ω√(A²−x²) ; E = (1/2)mω²A²",
"""F>k = 2π/λ ; v = ω/k ; I ∝ A²
F>Particle velocity in wave: v_max = Aω""")

add("K>Energy ∝ A² — amplitude double → energy ×4.",
"""E>In y = a sin(ωt + kx), the quantity k is called:
W>Wave parameters.
x>k = wave number / propagation constant = 2π/λ.
K>k = 2π/λ — x ka coefficient.
E>In which type of wave is energy not transferred?
W>Stationary wave property.
x>Stationary wave (standing wave) — energy nodes ke beech trapped.
K>Stationary = no energy transfer; progressive = energy travels.
E>The phase difference between velocity and acceleration in SHM is:
W>SHM phase relations.
x>v leads x by 90°; a = −ω²x (180° from x) → v aur a mein 90°.
K>SHM: v leads x by 90°; a leads v by 90°.
E>Two waves y₁ = 20 sin(4πt + π/4) and y₂ = 20 sin(4πt + π/3). Phase difference:
W>Δφ = |φ₁ − φ₂|.
x>Δφ = π/3 − π/4 = π/12.
K>Same ω → phase difference = phases ka antar.
E>Intensity of light depends on:
W>I ∝ A².
x>Intensity ∝ (amplitude)² — frequency/wavelength se nahi.
K>Amplitude double → intensity 4×.""")

add("- x = A/2 → (√3/2)vmax ; A double → energy ×4.",
"""- k = 2π/λ ; stationary → no energy transfer.
- Intensity ∝ A² ; v leads x by 90°, a leads v by 90°.""")

# ================= CH11 ELECTROSTATICS =================
add("**What is a capacitor?** Charge store karne wala device. C = Q/V = ε₀A/d. Energy U = (1/2)CV² = Q²/2C.",
"""**What is potential difference from work?** V = W/q — charge q ko move karne mein jo work W karna pade, wo potential difference se aata hai. Equipotential surface (same V) par move karne mein work = 0.
**What is surface charge density?** σ = Q/A — charge per area. Spherical shell: σ = Q/(4πR²). Thin shell ke just bahar E = σ/ε₀.
**What is charge quantisation?** Charge discrete hota hai: q = ne (n = integer, e = 1.6×10⁻¹⁹ C). e ka koi fraction possible nahi.
**How does a dipole's field vary with r?** Axial aur equatorial dono par E ∝ 1/r³; potential V ∝ 1/r². (Point charge ke E ∝ 1/r² se zyada jaldi girta hai.)
**PE of a charge system.** Do charges ki PE = kq₁q₂/r. Teen charges equilateral triangle (side x) par system ki U = 3kQ²/x — aur yehi work hai system arrange karne mein.""")

add("- Gauss: ∮E·dA = q/ε₀ (electricity) ; ∮B·dA = 0 (magnetism).",
"""- V = W/q ; equipotential par W = 0.
- σ = Q/A = Q/4πR² (shell) ; E(shell outside) = σ/ε₀.
- q = ne (quantisation); e = 1.6×10⁻¹⁹ C.
- Dipole: E ∝ 1/r³, V ∝ 1/r². System PE: U = kq₁q₂/r.""")

add("F>C = Q/V = ε₀A/d ; U = (1/2)CV² = Q²/2C",
"""F>V = W/q ; σ = Q/A ; E = σ/ε₀ (just outside conductor)
F>U_system = k q₁q₂/r ; dipole: E ∝ 1/r³, V ∝ 1/r²""")

add("- Distance badhao (charge constant) → C ghate, U = Q²/2C badhe. d double → C half (10 μF → 5 μF).",
"""- −5 C ko 100 J mein move karo → V = W/q = 100/5 = 20 V.
- Equipotential (5 V) par 10 C move → W = qΔV = 10 × 0 = 0.
- Shell σ = 88.54 C/m², 12 mm bahar → E = σ/ε₀ = 88.54/8.85×10⁻¹² ≈ 10¹³ N/C.
- 3 charges +Q triangle side x → U = 3kQ²/x.""")

add('- "Field inside conductor" → 0.',
"""- "Work to move charge" → V = W/q.
- "Surface charge density / shell" → σ = Q/A.
- "Dipole field vs distance" → ∝ 1/r³.""")

add("K>Rest charge → E only; moving charge → E + B.",
"""E>The work done on moving a charge of −5 C in an electric field is 100 J. The potential difference is:
W>V = W/q.
x>V = 100/5 = 20 V (magnitude — sign sirf direction batata hai).
K>V = W/q — work ko charge se divide.
E>The work done in moving a charge of 10 C between two points on a 5 V equipotential surface is:
W>Equipotential → same V → ΔV = 0.
x>W = qΔV = 10 × 0 = 0.
K>Equipotential surface par move → work ZERO.
E>Three charges +Q are at the vertices of an equilateral triangle of side x. Work to assemble them:
W>System PE = sum of pair energies.
x>U = 3 × kQ²/x (teen pair, har pair ki energy kQ²/x).
K>Triangle: 3 pair → 3kQ²/x.
E>The electric field strength and potential due to a dipole vary with distance r as:
W>Dipole distance dependence.
x>E ∝ 1/r³ ; V ∝ 1/r².
K>Dipole E ∝ r⁻³ (point charge ke r⁻² se tez girta hai).""")

add("- E inside conductor = 0 (hamesha).",
"""- Equipotential move → W = 0.
- Dipole: E ∝ 1/r³, V ∝ 1/r².""")

# ================= CH12 CURRENT =================
add("**What is power?** P = VI = I²R = V²/R. AC mein Pavg = Vrms Irms cosφ.",
"""**What is internal resistance?** Battery ke andar ki khud ki resistance r. Circuit mein current I = E/(R + r). Terminal voltage V = E − Ir (current draw karne par EMF se kam).
**What is drift velocity?** Electrons ka average slow net motion (electric field ke against): I = neAv_d. n = electrons/m³, e = charge, A = area, v_d = drift velocity. I aur A dono double → v_d SAME (2/2 = 1).
**What is conductance?** Resistance ka reciprocal: G = 1/R, unit siemens (S).
**What is a temperature coefficient?** R = R₀(1 + αΔT). Metals ka α positive (R badhta hai), semiconductors ka α NEGATIVE (R ghatta hai).""")

add("- p(t) = v(t)·i(t) ; w(t) = ∫p(t)dt.",
"""- I = E/(R+r) ; V_terminal = E − Ir. (E = 4 V, r = 2 Ω, R = 7 Ω → I = 4/9 A.)
- I = neAv_d → v_d ∝ I/A. I aur A dono double → v_d unchanged.
- EMF cell ke ELECTRODES/electrolyte par depend karta hai — circuit (R, I) par nahi.
- R aur V se length: R = ρL/A, V = AL → L = √(RV/ρ).""")

add("F>P = VI = I²R = V²/R ; Pavg = Vrms Irms cosφ",
"""F>I = E/(R+r) ; V = E − Ir ; G = 1/R
F>I = neAv_d ; R = R₀(1 + αΔT)""")

add("- Resistivity material property hai; resistance shape par depend karta hai.",
"""- Battery 4 V, r = 2 Ω, R = 7 Ω → I = 4/(7+2) = 4/9 A.
- I aur A dono double → v_d SAME (I/A ratio constant).
- Heater wire: nichrome (high resistivity + high melting point).
- n cells parallel (har cell r) → total internal resistance r/n.""")

add('- "Same battery, two currents" → E equate karo.',
"""- "Battery + internal resistance" → I = E/(R+r).
- "Drift velocity vs I, A" → I = neAv_d.""")

add("K>Same shape → R ∝ ρ directly.",
"""E>A battery of EMF 4 V and internal resistance 2 Ω is connected to a 7 Ω resistor. The current is:
W>I = E/(R+r).
x>I = 4/(7+2) = 4/9 A.
K>Total resistance = R + r (battery ka r bhi series mein).
E>The drift velocity of electrons is v for current I and area A. If I and A both double, new drift velocity is:
W>I = neAv_d → v_d = I/(neA).
x>v_d' = (2I)/(ne·2A) = v_d → same.
K>I aur A dono ×2 → ratio same → v_d unchanged.
E>Which equation shows the relation between current i and drift velocity v_d?
W>I = neAv_d.
x>i = neAv_d (n = free electrons/m³, e = charge, A = area).
K>i = neAv_d — drift velocity ka defining relation.
E>On increasing temperature, the resistance of semiconductors:
W>Semiconductor temperature behaviour.
x>Semiconductor: R GHATTA hai (negative temperature coefficient).
K>Metals R ↑, semiconductors R ↓ with temperature.""")

add("- KCL = charge, KVL = energy.",
"""- I = E/(R+r) ; V = E − Ir.
- I aur A dono double → drift velocity same.""")

add("C>2/2 = 1 → R unchanged.",
"""T>Terminal voltage hamesha EMF ke barabar hoti hai.
C>V = E − Ir — current draw karne par EMF se kam.
T>Drift velocity electrons ki itni hi hoti hai jitni current.
C>Drift velocity bahut slow (~mm/s); electric field tez travel karta hai.""")

# ================= CH13 MAGNETISM =================
add("**What does the hysteresis loop area give?** Energy loss per magnetisation cycle.",
"""**What is the field of a circular coil?** Centre par B = μ₀I/2R (N turns → ×N). Axis par distance x par B = μ₀IR²/2(R²+x²)^(3/2). (Solenoid ka B = μ₀nI ALAG hai.)
**What is Biot–Savart law?** Current element Idl ka field dB = (μ₀/4π) Idl sinθ/r². Wire aur coil ke B formulas isi se aate hain.
**What is a cyclotron?** Charged particle ko circular paths mein accelerate karta hai. Frequency f = qB/2πm (velocity se independent — sirf q, B, m).
**Force between parallel currents.** Same direction → ATTRACTION; opposite → repulsion. F/L = μ₀I₁I₂/2πd.
**Magnetic torque.** Field mein magnet/loop par τ = MB sinθ (M = magnetic moment, B = field). Maximum θ = 90° par.
**What is susceptibility?** χ = μᵣ − 1, jahan μᵣ = μ/μ₀ relative permeability. Diamagnetic χ negative (temperature se independent); paramagnetic χ ∝ 1/T.
**Ferromagnetic examples.** Iron, nickel, cobalt (aluminium paramagnetic, copper diamagnetic). Freely suspended magnet N–S align karta hai.""")

add("- Solenoid 50 cm, 100 turns, 2.5 A → B = 4π×10⁻⁷ × (100/0.5) × 2.5 = 6.28×10⁻⁴ T.",
"""- B(coil centre) = μ₀I/2R ; axis (x = R): B/√8.
- Radius half (current same) → B ×2 (B ∝ 1/R).
- Cyclotron: f = qB/2πm ; F/L = μ₀I₁I₂/2πd ; τ = MB sinθ.
- χ = μᵣ − 1 ; μ = μ₀μᵣ.""")

add("F>r = mv/qB ; T = 2πm/qB ; m = NIA ; χ = μᵣ − 1",
"""F>B(coil) = μ₀I/2R ; B_axis = μ₀IR²/2(R²+x²)^(3/2)
F>dB = (μ₀/4π) Idl sinθ/r² ; f_cyclotron = qB/2πm
F>F/L = μ₀I₁I₂/2πd ; τ = MB sinθ ; μ = μ₀μᵣ""")

add("- 1 T = 10⁴ gauss. Angle of dip: poles 90°, equator 0°.",
"""- Coil radius half (I same) → centre B ×2.
- Coil axis x = R → B_axis = B_centre/(2√2) = B/√8.
- Parallel currents same direction → attract.
- Diamagnetic: temperature se independent; paramagnetic: χ ∝ 1/T.""")

add('- "Moment direction" → right-hand rule.',
"""- "Coil ke centre ka field" → μ₀I/2R (×N turns).
- "Cyclotron frequency" → qB/2πm.
- "Parallel wires" → μ₀I₁I₂/2πd (same → attract).""")

add("K>Hysteresis area = energy loss per cycle.",
"""E>Magnetic field at the centre of a circular coil of radius R carrying current I is B. The field on the axis at distance R is:
W>B_axis = μ₀IR²/2(R²+x²)^(3/2) at x = R.
x>B_axis = μ₀IR²/2(2R²)^(3/2) = B/(2√2) = B/√8.
K>Axis x = R → B/√8 (centre ka 1/(2√2)).
E>If the radius of a current-carrying coil is halved keeping current same, field at centre:
W>B = μ₀I/2R → B ∝ 1/R.
x>R/2 → B ×2.
K>Coil centre B ∝ 1/R (radius half → field double).
E>The angular frequency of a charged particle in a cyclotron is:
W>Cyclotron frequency.
x>ω = qB/m (f = qB/2πm) — velocity se independent.
K>Cyclotron f = qB/2πm (sirf q, B, m).
E>For two parallel wires carrying currents Iₐ and I_b, force per length is:
W>Force between parallel currents.
x>F/L = μ₀IₐI_b/2πd (same direction → attract).
K>Parallel wires: μ₀I₁I₂/2πd — attraction for same direction.
E>The relationship between magnetic susceptibility χ and permeability μ is:
W>χ = μᵣ − 1, μ = μ₀μᵣ.
x>χ = (μ/μ₀) − 1 → μ = μ₀(1 + χ).
K>μᵣ = 1 + χ ; μ = μ₀μᵣ.""")

add("- Hysteresis area = energy loss/cycle.",
"""- Coil: radius half → B ×2 ; axis x = R → B/√8.
- Cyclotron f = qB/2πm (no v) ; same-direction wires attract.""")

add("- Curie temperature ke upar ferromagnetic → paramagnetic.",
"""- Ferromagnetic: Fe, Ni, Co. Al paramagnetic, Cu diamagnetic.
- Freely suspended magnet: N–S align (earth ka field).""")

add("C>Helical path tab banta hai jab velocity ka ∥ component bhi ho.",
"""T>Cyclotron frequency velocity par depend karti hai.
C>f = qB/2πm — velocity par independent.
T>Parallel wires same direction mein repel karti hain.
C>Same direction → ATTRACT; opposite → repel.""")

# ================= CH14 EMI/AC =================
add("**What is a transformer?** Voltage badalne wala device: Vp/Vs = Np/Ns.",
"""**What is LCR resonance?** Series LCR mein jab X_L = X_C hota hai, circuit pure resistive ban jaata hai: Z = R, current MAX, cosφ = 1. Resonant frequency f₀ = 1/(2π√LC) — R par depend NAHI karti (R badle to f₀ same).
**What is half-cycle average of AC?** i = I₀ sin ωt ka half-cycle average Ī = 2I₀/π (full-cycle average = 0).
**What is mutual inductance emf?** ε = −M dI/dt (M = coefficient of mutual induction, henry). Current jitni tez badle, emf utna bada.
**What are eddy currents?** Bulk conductor mein CHANGING magnetic flux se bante hain — circular induced currents (isliye transformer core laminated hota hai).
**Energy in an inductor.** U = (1/2)LI². 50 mH, 4 A → 0.5 × 0.05 × 16 = 0.4 J.""")

add("- Magnet fast → coil ki taraf → LARGER emf (ε ∝ speed).",
"""- f₀ = 1/(2π√LC) ; Ī_half = 2I₀/π.
- ε = M dI/dt : M = 0.5 H, ΔI = 4 A in 0.5 s → ε = 0.5 × 8 = 4 V.
- U_inductor = (1/2)LI² ; eddy currents = changing flux in bulk conductor.""")

add("F>Pavg = Vrms Irms cosφ ; η_transformer = VsIs/VpIp",
"""F>f₀ = 1/(2π√LC) ; Ī_half = 2I₀/π ; ε = M dI/dt
F>U = (1/2)LI² ; ideal transformer: P_in = P_out""")

add("- Pure inductive circuit: V aur I mein 90° phase difference.",
"""- Resonance: X_L = X_C → Z = R → cosφ = 1 (current max).
- R decrease karo → f₀ SAME (sirf L, C decide karte hain).
- i = 50 sin100t → Ī_half = 2×50/π = 100/π A.
- Ideal step-down transformer mein POWER constant rehti hai.""")

add('- "AC power / resonance" → cosφ = 1.',
"""- "Resonant frequency" → f₀ = 1/(2π√LC).
- "Half-cycle average" → 2I₀/π.
- "Mutual inductance emf" → ε = M dI/dt.""")

add("K>Generator = EMI (flux change → emf).",
"""E>The mathematical form of the resonant frequency of an LCR circuit is:
W>Resonance condition.
x>f₀ = 1/(2π√LC).
K>f₀ = 1/(2π√LC) — R ka koi role nahi.
E>In a series RLC circuit (R = 1000 Ω, L = 4 H, C = 10⁻⁶ F), R is decreased by 20 Ω. Resonant frequency:
W>f₀ sirf L, C par depend.
x>R badle to f₀ unchanged.
K>Resonant frequency R se independent.
E>An AC current i = 50 sin 100t A. Its half-cycle average is:
W>Ī = 2I₀/π.
x>Ī = 2 × 50/π = 100/π A.
K>Half-cycle average = 2I₀/π; full-cycle = 0.
E>Mutual inductance is 0.5 H. Current changes from +2 A to −2 A in 0.5 s. Induced emf:
W>ε = M dI/dt.
x>ε = 0.5 × (4/0.5) = 4 V.
K>ΔI = 4 A (sign ka dhyan: +2 → −2).
E>The energy stored in a 50 mH inductor carrying 4 A is:
W>U = (1/2)LI².
x>U = 0.5 × 50×10⁻³ × 16 = 0.4 J.
K>Inductor energy = (1/2)LI² — capacitor ke (1/2)CV² jaisa.""")

add("- Resonance → cosφ = 1.",
"""- f₀ = 1/(2π√LC) ; Ī_half = 2I₀/π.
- ε = M dI/dt ; U = (1/2)LI².""")

add("C>Generator = electromagnetic induction.",
"""T>R badhane se resonant frequency badhti hai.
C>f₀ = 1/(2π√LC) — sirf L aur C; R se independent.
T>Full-cycle average = 2I₀/π.
C>Full-cycle average = 0; HALF-cycle = 2I₀/π.""")

# ================= CH15 EM WAVES =================
add("- Max frequency = gamma; max wavelength = radio; UV/X/micro/gamma mein micro ki wavelength sabse badi.",
"""- Wavelength ranges: microwave ≈ 1 mm–1 m ; visible 400–800 nm ; UV < 400 nm ; IR > 800 nm.
- Point source se distance r par intensity I = P/4πr² (P = power). 100 W, 10% → 10 W; r = 5 m → I = 10/(4π×25) ≈ 0.032 W/m².
- Galaxies ke beech distance BADHTI ja rahi hai (redshift → expanding universe, Hubble).""")

add("K>EM waves fields se deflect nahi hoti.",
"""E>The wavelength range of microwaves is:
W>Spectrum ranges.
x>Microwave ≈ 1 mm to 1 m (radio se chhota, IR se bada).
K>Microwave 1 mm–1 m ; visible 400–800 nm.
E>A 100 W bulb converts 10% power to visible radiation. Average intensity 5 m away is:
W>I = P/4πr².
x>I = 10/(4π × 25) ≈ 0.032 W/m².
K>I = P/4πr² — radius ka square neeche.""")

# ================= CH16 OPTICS =================
add("**What does the eye see?** Retina par image REAL, INVERTED, DIMINISHED.",
"""**What is dispersion?** White light prism se guzarti hai to alag-alag colours mein toot jaati hai (alag λ → alag μ → alag deviation). VIOLET sabse zyada deviate hota hai (μ sabse zyada), RED sabse kam. Isliye glass ka refractive index violet ke liye MAXIMUM.
**What is a rainbow?** Barish ki boondo mein refraction + TIR + dispersion — teeno milkar rainbow banate hain (red bahar, violet andar).
**What is lens power?** P = 1/f (f metre mein), unit DIOPTRE (D). Convex lens f +ve → P +ve; concave → P −ve. +2.5 D → f = 1/2.5 = 0.4 m = 40 cm convex.
**What is the lens-maker formula?** 1/f = (μ−1)(1/R₁ − 1/R₂). Sign convention: convex surface R +ve, concave R −ve. Lens ko liquid (μ_l) mein duba do → μ → μ_g/μ_l.
**Mirrors inclined.** Do plane mirrors θ angle par → number of images N = 360/θ − 1 (jab 360/θ even integer ho).
**Deviation at a mirror.** Plane mirror par light i angle par gire to deviation δ = 180° − 2i (i = 30° → δ = 120°).
**What is Huygens' principle?** Wavefront ka HAR point naya secondary wavelet banata hai; unka envelope agla wavefront hai. Isse reflection AUR refraction dono explain hote hain.
**What is polarisation?** Sirf TRANSVERSE waves polarise hoti hain (light haan, sound nahi). Reflection se light partially polarise hoti hai; Brewster angle par puri: tan θ_B = μ.
**Diffraction condition.** Jab slit/obstacle ka size wavelength ke barabar ho tab diffraction clearly dikhta hai (corona around moon = diffraction).
**Colour of objects.** Object apna colour usi wavelength ko reflect karke dikhata hai. Red paper yellow light mein → BLACK (yellow absorb ho jaata hai, kuch reflect nahi hota).""")

add("- Simple microscope (D = 25 cm): M = 1 + D/f ; f = 4 cm → 7.25.",
"""- Dispersion order (deviation): violet > indigo > ... > red; μ_violet sabse bada.
- P = 1/f (m) ; +2.5 D → 40 cm convex.
- 1/f = (μ−1)(1/R₁ − 1/R₂) ; N(mirrors) = 360/θ − 1.
- Plane mirror deviation δ = 180° − 2i ; Brewster: tan θ_B = μ.
- Telescope: M = f₀/fₑ ; YDSE amplitude ratio = √(I₁/I₂) = √(1/4) = 1:2.
- Destructive interference: path difference = (2n+1)λ/2 (phase 180°).
- v = c/μ → v₁/v₂ = μ₂/μ₁ (glass 3/2, water 4/3 → v_w/v_g = 9/8).
- λ in medium = λ₀/μ (6000 Å in glass μ = 1.5 → 4000 Å).""")

add("F>sin C = μ_rarer/μ_denser ; M = 1 + D/f ; resolving power ∝ 1/λ",
"""F>P = 1/f (dioptre) ; 1/f = (μ−1)(1/R₁ − 1/R₂)
F>N = 360/θ − 1 ; δ(mirror) = 180° − 2i ; tan θ_B = μ
F>v = c/μ ; λ_medium = λ₀/μ ; M_telescope = f₀/fₑ""")

add("- Glass (μ = √3), i = 60° → r = 30° → angle between refracted and reflected = 90°.",
"""- 30° mirrors asymmetric → N = 360/30 − 1 = 11.
- Plane mirror i = 30° → δ = 180 − 60 = 120°.
- Double convex lens f = 25 cm, μ = 1.5, R₁ = 2R₂ → 1/25 = 0.5(1/R₁ + 1/R₂) → R₁ = 37.5 cm, R₂ = 18.75 cm.
- Concave lens μ_g = 1.5 in liquid μ_l = 2 → relative μ = 0.75 < 1 → lens CONVEX ban jaati hai (f = 80 cm).
- Red paper in yellow light → black.""")

add('- "Microscope" → M = 1 + D/f.',
"""- "Power of lens (dioptre)" → P = 1/f.
- "Two mirrors / number of images" → 360/θ − 1.
- "White light / colours / rainbow" → dispersion.
- "Polarisation / Brewster" → transverse + tan θ_B = μ.
- "Frequency in medium / λ change" → λ/μ, v = c/μ.""")

add("K>Simple microscope (D = 25 cm): M = 1 + D/f.",
"""E>The power of a lens is +2.5 D. The lens is:
W>P = 1/f.
x>f = 1/2.5 = 0.4 m = 40 cm; P positive → convex.
K>P = 1/f (metre) — +ve = convex, −ve = concave.
E>Two plane mirrors are at 30°. Number of images (object placed asymmetrically):
W>N = 360/θ − 1.
x>N = 360/30 − 1 = 12 − 1 = 11.
K>N = 360/θ − 1 (θ se divide karke 1 ghatao).
E>The angle of incidence on a plane mirror is 30°. Angle of deviation is:
W>δ = 180° − 2i.
x>δ = 180° − 60° = 120°.
K>Mirror deviation = 180° − 2i.
E>A double convex lens has f = 25 cm, μ = 1.5, one radius double the other. The radii are:
W>Lens-maker: 1/f = (μ−1)(1/R₁ + 1/R₂), R₁ = 2R₂.
x>1/25 = 0.5(1/R₁ + 1/R₂) → R₂ = 18.75 cm, R₁ = 37.5 cm.
K>Biconvex: 1/f = (μ−1)(1/R₁ + 1/R₂) — signs dhyan se.
E>Which law can be explained by Huygens' principle?
W>Huygens secondary wavelets.
x>Reflection AND refraction dono.
K>Huygens → reflection + refraction dono.
E>Refractive index of glass is 1.5 for light of wavelength 6000 Å in vacuum. Wavelength in glass:
W>λ_medium = λ₀/μ.
x>λ = 6000/1.5 = 4000 Å.
K>Medium mein wavelength GHTATI hai: λ/μ.
E>In YDSE the slit-width ratio is 1 : 4. The amplitude ratio is:
W>Intensity ∝ width, amplitude ∝ √I.
x>I₁:I₂ = 1:4 → A₁:A₂ = √1:√4 = 1:2.
K>Amplitude ratio = √(intensity ratio).""")

add("- Plane mirror: v = u.",
"""- P = 1/f ; N = 360/θ − 1 ; δ = 180° − 2i.
- Violet sabse zyada deviate; μ_violet maximum.
- λ in medium = λ₀/μ (ghat-ta hai); frequency same.""")

add("- Visible light: 400–800 nm. Near point ≈ 25 cm.",
"""- Dispersion: VIBGYOR (violet sabse zyada deviate).
- Rainbow: refraction + TIR + dispersion.
- Telescope: M = f₀/fₑ (f₀ >> fₑ).""")

add("C>Inside focus → image VIRTUAL, mirror ke peeche (v negative).",
"""T>Convex lens ki power negative hoti hai.
C>Convex = +ve power (converging); concave = −ve.
T>N mirrors = 360/θ.
C>N = 360/θ − 1 (jab 360/θ even integer ho).
T>Medium change par frequency badalti hai.
C>Frequency constant; λ = λ₀/μ ghat-ta hai.""")

# ================= CH18 ATOMS =================
add("**What is fission?** Bhaari nucleus do parts mein tootta hai.",
"""**Spectral series names.** Hydrogen lines: Lyman (n = 1, UV), Balmer (n = 2, visible), Paschen (n = 3, IR). Balmer hi visible series hai. Formula: 1/λ = R(1/n₁² − 1/n₂²).
**Nuclear reactions balance.** Har nuclear reaction mein mass number (A) aur charge (Z) dono CONSERVE hote hain — unknown particle nikalne ke liye A aur Z ka sum match karo.""")

add("K>Fusion → extreme temperature needed for coulomb barrier.",
"""E>Lyman and Balmer are the names of:
W>Spectral series.
x>Hydrogen spectral series (Lyman UV n = 1, Balmer visible n = 2).
K>Balmer = visible (n = 2); Lyman = UV (n = 1).
E>In a nuclear reaction, balancing is done using:
W>Conservation in reactions.
x>Mass number (A) aur charge (Z) dono conserve.
K>Nuclear reactions: A aur Z dono conserve karo.""")

add("- α = helium nucleus, β = electron.",
"""- Lyman UV, Balmer visible, Paschen IR.""")

# ================= CH19 ELECTRONICS =================
add("**What is rectification?** AC → DC. Chain: Rectifier → Filter (smooth) → Regulator (constant).",
"""**What are logic gates?** Digital circuits ke basic blocks. AND (output 1 sirf jab dono inputs 1), OR (koi ek 1 to output 1), NOT (invert), NAND (AND ka ulta), NOR (OR ka ulta), XOR (inputs alag to 1). Truth table se koi bhi combination nikal jaata hai.
**What are energy bands?** Conduction band = wo band jisme electrons freely conduct karte hain. Valence band = atoms se bandhe electrons. Conductor mein dono overlap; insulator mein bada gap.
**Ge at 0 K.** Absolute zero par germanium INSULATOR jaisa behave karta hai (koi free electron nahi).
**Emitter.** Transistor ka emitter HEAVILY doped aur THIN hota hai (zyada carriers inject karne ke liye).""")

add("- npn > pnp (electron mobility).",
"""- AND: Y = A·B ; OR: Y = A+B ; NOT: Y = Ā ; NAND = AND + NOT ; NOR = OR + NOT.
- AND + NOT ka combination = NAND gate.
- Conduction band electrons hi conduction mein hissa lete hain.
- Ge at 0 K = insulator; emitter heavily doped + thin.""")

add("F>β (current gain) = Ic/Ib (common emitter)",
"""F>AND: Y = A·B ; OR: Y = A+B ; NOT: Y = Ā ; NAND = NOT(A·B) ; NOR = NOT(A+B)""")

add("K>npn > pnp — electrons faster.",
"""E>Which logic gate gives output Y = 1 only when both inputs are 1?
W>AND gate definition.
x>AND gate (Y = A·B).
K>AND = dono 1 tab 1; OR = koi ek 1 tab 1.
E>AND gate followed by NOT gate gives:
W>Gate combination.
x>AND + NOT = NAND gate.
K>AND + NOT = NAND; OR + NOT = NOR.
E>Which band in a solid has electrons that participate in conduction?
W>Energy bands.
x>Conduction band (valence band ke electrons bandhe hote hain).
K>Conduction = conduction band electrons.
E>Pure germanium at absolute zero behaves as:
W>Semiconductor at 0 K.
x>Insulator (koi free electron nahi).
K>0 K par semiconductor = insulator.""")

add("- Zener = reverse-biased regulator.",
"""- AND+NOT = NAND ; OR+NOT = NOR.
- Conduction band → current; Ge at 0 K → insulator.""")

add("- Si diode knee ~0.7 V; Ge ~0.3 V.",
"""- Emitter: heavily doped + thin; collector: largest area.""")

# ================= FINAL BLOCKS =================
add("- ΔQ = ΔU + W ; η = 1 − T₂/T₁ ; PV = nRT ; E = (3/2)Nk_BT ; γ = 1 + 2/f",
"""- Q = mcΔT ; ΔL = αLΔT ; α:β:γ = 1:2:3 ; h = 2T cosθ/(rρg)
- v_rms = √(3RT/M) ; f₀ = 1/(2π√LC) ; Ī_half = 2I₀/π ; ε = M dI/dt ; U = (1/2)LI²
- I = E/(R+r) ; I = neAv_d ; V = W/q ; σ = Q/A ; E = σ/ε₀
- B = μ₀I/2R ; B_axis = μ₀IR²/2(R²+x²)^(3/2) ; f_cyc = qB/2πm ; F/L = μ₀I₁I₂/2πd ; τ = MB sinθ
- P = 1/f ; 1/f = (μ−1)(1/R₁ − 1/R₂) ; N = 360/θ − 1 ; δ = 180° − 2i ; tan θ_B = μ
- k = 2π/λ ; I ∝ A² ; R = √(A²+B²+2AB cosθ) ; COP = T₂/(T₁−T₂)""")

add("- Photoelectric = frequency ; lines = (n−m)(n−m+1)/2 ; T½ = 0.693τ",
"""- p ×1.25 → K ×1.5625 ; resultant 3-4-5 ; min zero-resultant = 2 forces
- Isochoric W = 0 ; COP ≠ engine η ; rms sirf √T (pressure nahi)
- f₀ R se independent ; full-cycle average = 0 (half = 2I₀/π)
- Violet sabse zyada deviate ; μ_violet max ; N = 360/θ − 1
- Convex = +ve power ; Ge at 0 K = insulator ; reverse bias widens depletion""")

add("- 27 °C = 27 K ; henry = inductance ; weber = flux ; Zener = regulator",
"""- Water c = 1 cal/g°C ; 1 cal = 4.18 J ; σ_Stefan = 5.67×10⁻⁸
- Ferromagnetic: Fe, Ni, Co ; microwave 1 mm–1 m ; visible 400–800 nm
- Lyman UV / Balmer visible ; emitter heavily doped + thin ; galaxies recede (Hubble)""")

# ---------------- apply ----------------
missing = []
for anchor, block in EDITS:
    n = text.count(anchor)
    if n != 1:
        missing.append((anchor[:70], n))
if missing:
    print("ANCHOR PROBLEMS:")
    for a, n in missing:
        print(f"  count={n} : {a}")
    sys.exit(1)

for anchor, block in EDITS:
    text = text.replace(anchor, anchor + "\n" + block, 1)

open(path, "w", encoding="utf-8").write(text)
print(f"Applied {len(EDITS)} insertions OK. New length: {len(text.splitlines())} lines")
