# -*- coding: utf-8 -*-
p = "agniveer/Master_Physics_Notes.txt"
s = open(p, encoding="utf-8").read()

# ---------- 1. Rename headings to the 12-section structure ----------
renames = [
 ("3. FORMULA BANK (dimensions to memorise)", "3. FORMULA BANK"),
 ("3. FORMULA BANK (standard moments of inertia)", "3. FORMULA BANK"),
 ("2. MUST-KNOW RELATIONS", "2. KEY RELATIONS"),
 ("4. IMPORTANT CONDITIONS / SPECIAL CASES", "4. CONDITIONS / SPECIAL CASES"),
 ("5. FAST SOLVING METHODS", "6. SOLVING METHODS"),
 ("6. 10-SECOND TRICKS", "8. 10-SECOND TRICKS"),
 ("7. IMPORTANT FACTS", "9. IMPORTANT FACTS"),
 ("8. COMMON TRAPS", "10. COMMON TRAPS"),
 ("9. STANDARD GRAPHS/DIAGRAM KNOWLEDGE", "11. GRAPHS / DIAGRAM KNOWLEDGE"),
 ("10. LAST-MINUTE REVISION", "12. LAST-MINUTE REVISION"),
]
for a, b in renames:
    assert a in s, a
    s = s.replace(a, b)

# ---------- 2. Preface flow update ----------
old_flow = """Every chapter teaches one topic concept-first, in a fixed flow:
CORE CONCEPTS -> key relations -> formula bank -> conditions/special cases
-> how questions are solved -> 10-second tricks -> facts -> traps -> graphs
-> last-minute revision. Real exam questions appear only as worked examples,
never as a question dump: learn the concept, then solve any variation."""
new_flow = """Every chapter teaches one topic concept-first, in a fixed flow:
CORE CONCEPTS -> KEY RELATIONS -> FORMULA BANK -> CONDITIONS / SPECIAL CASES
-> QUESTION RECOGNITION -> SOLVING METHODS -> SELECTED PYQ EXAMPLES
-> 10-SECOND TRICKS -> IMPORTANT FACTS -> COMMON TRAPS
-> GRAPHS / DIAGRAM KNOWLEDGE -> LAST-MINUTE REVISION.
Real exam questions appear only as worked examples inside this flow,
never as a question dump: learn the concept, then solve any variation."""
assert old_flow in s
s = s.replace(old_flow, new_flow)

# ---------- 3. Question recognition content per chapter ----------
rec = {
1: ["'Find the dimension of X' -> take a defining formula, substitute dimensions.",
    "'Which pair has the same dimension?' -> write both as formulas, compare.",
    "'Dimensionless / unitless?' -> strain, refractive index, specific gravity, angle.",
    "Unit conversion (kWh->J, N->dyne, T->gauss, pm->micron) -> conversion ladder.",
    "'Fundamental vs derived quantity' -> check against the 7 base SI units."],
2: ["'Distance in the nth second / per-second ratio' -> Sn = u + (a/2)(2n-1); odd ratio 1:3:5:7.",
    "'Slope / area of a motion graph' -> slope of x-t = v, slope of v-t = a, area of v-t = s.",
    "'Projectile range / height / time' -> H = u2sin2θ/2g, R = u2sin2θ/g, T = 2u sinθ/g.",
    "'Uniform circular motion acceleration' -> a = v2/r = ω2r.",
    "'s = polynomial in t -> acceleration' -> differentiate twice (a = d2s/dt2)."],
3: ["'Mass from F and a' (or F from m, a) -> F = ma.",
    "'Momentum / double the velocity' -> p = mv.",
    "'Recoil of a gun' -> momentum before = momentum after = 0.",
    "'Impulse / impact force' -> J = FΔt = Δp (longer time -> smaller force).",
    "'Max acceleration without slipping / friction' -> a = μs g."],
4: ["'Work by a force over a displacement (vectors)' -> dot product W = F·s.",
    "'Work by a retarding force' -> negative.",
    "'Spring energy / work between two stretches' -> W = (1/2)k(x2² - x1²).",
    "'Variable force F(x)' -> integrate F dx.",
    "'Power / kinetic-energy estimate' -> P = W/t, K = (1/2)mv2."],
5: ["'Moment of inertia about a given axis' -> table + parallel/perpendicular-axis theorem.",
    "'What does torque depend on?' -> force x moment arm.",
    "'Angular momentum conserved (I changes)' -> L = Iω.",
    "'Centre-of-mass velocity of two bodies' -> no external force -> Vcm constant."],
6: ["'g of a planet (M, R given)' -> g = GM/R2.",
    "'Escape velocity' -> ve = √(2GM/R).",
    "'Satellite energy / time period' -> PE = 2E_total ; T = 2π√(r3/GM).",
    "'Kepler's laws' -> equal areas = angular-momentum conservation."],
7: ["'Young's modulus / slope of stress-strain' -> Y = stress/strain.",
    "'Excess pressure in drop/bubble' -> 2T/r or 4T/r ; ratio = inverse of radii.",
    "'Terminal velocity vs radius' -> vt ∝ r2.",
    "'Gauge vs absolute pressure' -> gauge = P - Pa.",
    "'Meniscus / contact angle' -> convex = mercury (140°).",
    "'Poisson ratio' -> lateral strain / longitudinal strain."],
8: ["'ΔQ, ΔU, W relation' -> first law ΔQ = ΔU + W.",
    "'Isothermal / adiabatic' -> ΔU = 0 / Q = 0.",
    "'Carnot efficiency' -> η = 1 - T2/T1 (kelvin!).",
    "'Work from efficiency' -> W = η Q.",
    "'∮(δQ - δW)' -> 0 (state function)."],
9: ["'Translational KE vs temperature' -> E = (3/2)NkBT.",
    "'γ of a gas' -> diatomic 1.4, monatomic 1.66.",
    "'Sound speed vs pressure' -> unchanged at constant T.",
    "'van der Waals constant dimension' -> a: [ML5T-2]."],
10:["'Velocity at x = A/2' -> (√3/2) vmax.",
    "'Ratio amax/vmax' -> ω = 2πf.",
    "'ω from given a and x' -> ω = √(a/x).",
    "'Sound vs EM wave / medium' -> sound is mechanical."],
11:["'Field ratio E2:E1 (different q, r)' -> (q2/q1)·(r1/r2)2.",
    "'Force in a dielectric' -> F/K.",
    "'Field inside a conductor' -> 0.",
    "'Capacitor combinations / stored energy' -> series/parallel ; U = Q2/2C.",
    "'Dipole oscillation' -> ω = √(2qE/md)."],
12:["'R = ρL/A with L, A changed' -> ratio method.",
    "'Series / parallel equivalent' -> product/sum for two.",
    "'KCL vs KVL conservation' -> charge vs energy.",
    "'AC power / power factor' -> Vrms Irms cosφ.",
    "'Same battery, two currents' -> equate E = I1R1 = I2R2."],
13:["'Field of a wire / solenoid' -> μ0I/2πr ; μ0nI.",
    "'Radius vs B' -> r = mv/qB (∝ 1/B).",
    "'Time period of circular motion' -> 2πm/qB (independent of v).",
    "'Magnetic moment direction' -> right-hand rule.",
    "'Curie temperature' -> ferromagnetic -> paramagnetic."],
14:["'Induced emf from flux / Φ(t)' -> ε = -dΦ/dt.",
    "'Transformer ratio / efficiency' -> Vp/Vs = Np/Ns ; η = VsIs/VpIp.",
    "'AC power at resonance' -> cosφ = 1.",
    "'Generator principle' -> electromagnetic induction."],
15:["'Not an EM wave' -> sound.",
    "'E0 and B0 relation' -> E0/B0 = c.",
    "'Spectrum order' -> radio < micro < IR < visible < UV < X < gamma.",
    "'What EM waves carry' -> energy."],
16:["'Mirror / lens image position' -> v = uf/(u-f) ; m = v/u.",
    "'Prism refractive index' -> μ = 1 + δ/A.",
    "'YDSE fringe' -> β = λD/d.",
    "'Critical angle' -> sin C = μr/μd.",
    "'Microscope magnification' -> M = 1 + D/f."],
17:["'Photon energy from λ' -> E(eV) = 12400/λ(Å).",
    "'Work function from λ0' -> φ = hc/λ0.",
    "'Threshold condition' -> frequency (not intensity).",
    "'de Broglie wavelength' -> λ = h/p = h/√(2mK)."],
18:["'Neutrons in a nucleus' -> A - Z.",
    "'Spectral lines n -> m' -> (n-m)(n-m+1)/2.",
    "'Half-life from λ or mean life' -> T1/2 = 0.693/λ = 0.693τ.",
    "'Fusion condition' -> very high temperature."],
19:["'N-type vs P-type doping' -> pentavalent vs trivalent.",
    "'Zener diode' -> heavily doped, reverse bias, regulator.",
    "'Depletion width' -> widens in reverse bias.",
    "'AC→DC chain' -> rectifier -> filter -> regulator."],
20:["'Propagation modes of radio waves' -> ground + sky + space.",
    "'Modulation / demodulation' -> baseband on carrier / its reverse.",
    "'Pitch change after transmission' -> wrong bandwidth selection."],
}

# ---------- 4. Selected PYQ examples per chapter ----------
ex = {
1: ["• Q: Dimensional formula of energy?",
    "  Concept: E = F·s.  Solve: [F][s] = MLT-2 · L = ML2T-2.",
    "  Answer: [M1L2T-2].  Remember: energy = work = torque.",
    "• Q: Dimension of specific gravity?",
    "  Concept: ratio of two densities — everything cancels.",
    "  Answer: [M0L0T0].  Remember: any pure ratio is dimensionless."],
2: ["• Q: Ratio of distances fallen in the 1st, 2nd, 3rd, 4th second?",
    "  Concept: Sn = u + (a/2)(2n-1) with u = 0 → Sn ∝ (2n-1).",
    "  Answer: 1:3:5:7.  Remember: odd numbers.",
    "• Q: Car from rest to 20 m/s in 10 s — distance covered?",
    "  Concept: u = 0, v = 20, t = 10 → s = (u+v)/2 × t.",
    "  Answer: 100 m.  Remember: average-velocity method."],
3: ["• Q: Bullet 100 g at 100 m/s fired from a 20 kg gun — recoil?",
    "  Concept: momentum conservation, 0 = (0.1)(100) + 20 v.",
    "  Answer: v = 0.5 m/s.  Remember: recoil = (m v)/M.",
    "• Q: A force of 90 N produces a = 15 m/s2 — mass?",
    "  Concept: F = ma → m = F/a.",
    "  Answer: 6 kg.  Remember: m = F/a."],
4: ["• Q: F = 2i+3j+k, displacement s = i+2j-4k — work done?",
    "  Concept: dot product W = F·s = 2+6-4.",
    "  Answer: 4 J.  Remember: multiply matching components.",
    "• Q: Spring k = 1000 N/m stretched 10 cm → 20 cm — work?",
    "  Concept: W = (1/2)k(x2² - x1²) = 0.5×1000×(0.04-0.01).",
    "  Answer: 15 J.  Remember: difference of squares, not (Δx)2."],
5: ["• Q: Moment of inertia of a ring about a tangent?",
    "  Concept: parallel axis, I = MR2 + MR2/2.",
    "  Answer: 3MR2/2.  Remember: ring tangent = 3/2 MR2.",
    "• Q: Disc MI about a diameter = I → MI about ⊥ axis through the rim?",
    "  Concept: I⊥centre = 2I ; rim = 2I + MR2 = 2I + 4I.",
    "  Answer: 6I.  Remember: for a disc MR2 = 4I."],
6: ["• Q: Planet of mass 4M and radius R/2 — its g?",
    "  Concept: g ∝ M/R2 → 4/(1/2)2 = 16.",
    "  Answer: 16g.  Remember: square the radius factor.",
    "• Q: Satellite total energy E0 — its potential energy?",
    "  Concept: PE = 2 × total energy.",
    "  Answer: 2E0.  Remember: KE = -E0."],
7: ["• Q: Bubble radii in ratio 5:3 — excess-pressure ratio?",
    "  Concept: ΔP ∝ 1/r.",
    "  Answer: 3:5.  Remember: invert the radius ratio.",
    "• Q: Radius of a body falling in a liquid doubled — terminal velocity?",
    "  Concept: vt ∝ r2.",
    "  Answer: 4 times.  Remember: square the factor."],
8: ["• Q: Carnot engine between 127 °C and 327 °C — efficiency?",
    "  Concept: η = 1 - T2/T1 in kelvin → 1 - 400/600.",
    "  Answer: 33.3%.  Remember: add 273 first.",
    "• Q: Adiabatic process, 200 J of work done ON the gas — ΔU?",
    "  Concept: Q = 0 → ΔU = -W = +200 J.",
    "  Answer: +200 J.  Remember: work on → ΔU rises."],
9: ["• Q: Ratio Cp/Cv for a diatomic gas?",
    "  Concept: γ = 1 + 2/f with f = 5.",
    "  Answer: 1.4.  Remember: monatomic = 1.66.",
    "• Q: Pressure doubled at constant T — speed of sound?",
    "  Concept: v = √(γP/ρ); ρ also doubles, ratio unchanged.",
    "  Answer: unchanged (332 m/s).  Remember: independent of pressure."],
10:["• Q: Velocity of an SHM particle at x = A/2?",
    "  Concept: v = vmax √(1 - x2/A2) = vmax √(3/4).",
    "  Answer: (√3/2) vmax.  Remember: memorize this standard value.",
    "• Q: A = 0.01 m, f = 50 Hz — ratio amax/vmax?",
    "  Concept: amax/vmax = ω = 2πf.",
    "  Answer: 100π.  Remember: that ratio is just ω."],
11:["• Q: 2 μC at r (E1) vs 8 μC at 2r (E2) — E2:E1?",
    "  Concept: E ∝ q/r2 → (8/2)(1/2)2 = 1.",
    "  Answer: 1:1.  Remember: square the distance ratio.",
    "• Q: Plates at -10 V and +30 V, d = 2 cm — field?",
    "  Concept: E = ΔV/d = 40/0.02.",
    "  Answer: 2000 V/m.  Remember: use the total ΔV."],
12:["• Q: 10 kΩ and 30 kΩ in parallel — equivalent resistance?",
    "  Concept: product/sum = 300/40.",
    "  Answer: 7.5 kΩ.  Remember: two-resistor shortcut.",
    "• Q: Current 5 A drops to 4 A when 2 Ω is added — original R?",
    "  Concept: same emf → 5R = 4(R+2).",
    "  Answer: 8 Ω.  Remember: equate E = IR."],
13:["• Q: Solenoid 50 cm, 100 turns, 2.5 A — field at centre?",
    "  Concept: B = μ0nI = 4π×10-7 × (100/0.5) × 2.5.",
    "  Answer: 6.28×10-4 T.  Remember: n = N/L.",
    "• Q: Magnetic field increased — radius of the circular path?",
    "  Concept: r = mv/qB.",
    "  Answer: radius decreases.  Remember: r ∝ 1/B."],
14:["• Q: Φ = 6t2 + 3t + 2 — induced emf at t = 3 s?",
    "  Concept: ε = dΦ/dt = 12t + 3.",
    "  Answer: 39 V.  Remember: differentiate, then substitute.",
    "• Q: Transformer 220 V→11 V, primary 5 A, secondary 90 A — efficiency?",
    "  Concept: η = VsIs / VpIp = (11×90)/(220×5).",
    "  Answer: 90%.  Remember: power ratio, not voltage ratio."],
15:["• Q: Which is NOT an electromagnetic wave?",
    "  Concept: EM waves are transverse and need no medium.",
    "  Answer: Sound.  Remember: sound is a mechanical wave.",
    "• Q: Relation between E0 and B0 in an EM wave?",
    "  Concept: E0/B0 = c.",
    "  Answer: c.  Remember: E0/B0 = c, not c2."],
16:["• Q: Concave mirror f = 20 cm, object at 30 cm — image distance?",
    "  Concept: v = uf/(u-f) = 600/10.",
    "  Answer: 60 cm.  Remember: v = uf/(u-f).",
    "• Q: Thin prism A = 8°, deviation 2° — refractive index?",
    "  Concept: δ = (μ-1)A → μ = 1 + 2/8.",
    "  Answer: 1.25.  Remember: μ = 1 + δ/A."],
17:["• Q: Wavelength 6000 Å — photon energy?",
    "  Concept: E(eV) = 12400/λ(Å) = 12400/6000.",
    "  Answer: 2.06 eV.  Remember: the 12400 shortcut.",
    "• Q: Electron and proton with same KE — λp : λe?",
    "  Concept: λ ∝ 1/√m → √(me/mp).",
    "  Answer: ≈ 1 : 43.  Remember: lighter particle → longer λ."],
18:["• Q: Electrons from the 8th to the 2nd shell — spectral lines?",
    "  Concept: (n-m)(n-m+1)/2 = 6×7/2.",
    "  Answer: 21.  Remember: use (n-m), not n.",
    "• Q: Mean life 50 days — half-life?",
    "  Concept: T1/2 = 0.693τ = 0.693 × 50.",
    "  Answer: 34.65 days.  Remember: T1/2 = 0.693τ."],
19:["• Q: Germanium doped with gallium — type?",
    "  Concept: trivalent impurity → p-type.",
    "  Answer: p-type.  Remember: group III = p-type.",
    "• Q: Zener diode is used as?",
    "  Concept: heavily doped, reverse biased.",
    "  Answer: voltage regulator.  Remember: Zener = regulator."],
20:["• Q: Radio waves travel from one place to another by?",
    "  Concept: ground + sky + space wave propagation.",
    "  Answer: all of the above.  Remember: radio = all three modes.",
    "• Q: Modulation is?",
    "  Concept: superimposing baseband signal on a carrier.",
    "  Answer: necessary for effective transmission.  Remember: demodulation is the reverse."],
}

# ---------- 5. Insert the two new sections ----------
lines = s.split("\n")
out = []
cur = None
import re
for ln in lines:
    m = re.match(r"^CHAPTER (\d+) —", ln)
    if m:
        cur = int(m.group(1))
    if ln == "6. SOLVING METHODS":
        out.append("5. QUESTION RECOGNITION")
        for b in rec.get(cur, []):
            out.append("   - " + b)
        out.append("")
        out.append(ln)
        continue
    if ln == "8. 10-SECOND TRICKS":
        out.append("7. SELECTED PYQ EXAMPLES")
        for b in ex.get(cur, []):
            out.append(b)
        out.append("")
        out.append(ln)
        continue
    out.append(ln)
s = "\n".join(out)

# ---------- 6. Add FINAL RELATIONS REVISION ----------
anchor = "================================================================================\nFINAL TRICKS REVISION"
rel_block = """================================================================================
FINAL RELATIONS REVISION
================================================================================
- v = u + at ; v2 = u2 + 2as ; Sn = u + (a/2)(2n-1) ; a = v2/r = ω2r
- F = ma = dp/dt ; J = FΔt = Δp ; K = p2/2m ; fmax = μsN ; a = μsg
- W = Fs cosθ ; U = (1/2)kx2 ; P = Fv ; τ = Iα ; L = Iω ; I = Icm + Md2
- F = GMm/r2 ; g = GM/R2 ; ve = √(2gR) ; T2 ∝ r3 ; PE(satellite) = 2E_total
- Y = FL/(AΔL) ; ΔP = 2T/r (drop), 4T/r (bubble) ; vt ∝ r2 ; P = ρgh
- ΔQ = ΔU + W ; η = 1 - T2/T1 ; PV = nRT ; E = (3/2)NkBT ; γ = 1 + 2/f
- v = ω√(A2-x2) ; vmax = ωA ; amax = ω2A ; amax/vmax = 2πf
- F = kq1q2/r2 ; E = kq/r2 = V/d ; C = ε0A/d ; U = Q2/2C ; τ = pE sinθ
- R = ρL/A ; P = VI = I2R = V2/R ; Pavg = Vrms Irms cosφ
- B = μ0I/2πr = μ0nI ; r = mv/qB ; T = 2πm/qB ; m = NIA ; χ = μr - 1
- ε = -dΦ/dt ; Vp/Vs = Np/Ns ; η = VsIs/VpIp ; E0/B0 = c ; E = hc/λ ; λ = h/p
- 1/f = 1/v + 1/u ; m = v/u ; δ = (μ-1)A ; β = λD/d ; sin C = μr/μd ; M = 1 + D/f
- T1/2 = 0.693/λ = 0.693τ ; spectral lines n→m = (n-m)(n-m+1)/2

"""
assert anchor in s
s = s.replace(anchor, rel_block + anchor)

import re as _re
s = _re.sub(r"\n{3,}", "\n\n", s)
open(p, "w", encoding="utf-8").write(s)
print("done")
