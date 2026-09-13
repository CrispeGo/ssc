import re

path = "agniveer/Master_Physics_Notes.txt"
s = open(path, encoding="utf-8").read()

# ---------- targeted text fixes ----------
fixes = [
    # 1. typo in Ch17 heading
    ("4. IMPORTANT CONDITIONS / SPECIAL CASIES",
     "4. IMPORTANT CONDITIONS / SPECIAL CASES"),
    # 2. remove misplaced gravitation trap from Ch3
    ('TRAP: "1% change in radius" for g — g = GM/R2, so Δg/g = -2 ΔR/R.\n  Radius reduced 1% → g increases (by ~2%).\n', ''),
    # 3. correct Carnot max-efficiency note in Ch8
    ("- Carnot maximum efficiency when source-sink DIFFERENCE is largest:\n  40 K/20 K gives η = 50% (largest among 40/20, 60/40, 80/60, 100/80 —\n  all give 0.5, but 40 K/20 K has highest relative ratio → answer A).",
     "- Same 20 K gap each: the LOWEST cold/hot ratio wins. 40 K/20 K →\n  η = 50% (60/40 → 33.3%, 80/60 → 25%, 100/80 → 20%) → answer A."),
    # 4. clean up Ch19 10-second trick
    ('- Pentavalent → N (P-N both start with "n"? No: Penta → N-type, Tri →\n  P-type).',
     "- Pentavalent → N-type ; trivalent → P-type (periodic group V vs III)."),
    # 5. Ch16 mirror example 1 -> magnitude formula
    ("- Concave mirror f = 20 cm, u = 30 cm → 1/v = 1/20 - 1/30 = 1/60 → v = 60 cm.",
     "- Concave mirror quick form: v = uf/(u-f). f = 20 cm, u = 30 cm →\n  v = 600/10 = 60 cm."),
    # 6. Ch16 mirror example 2
    ("- Concave mirror R = 25 (f = 12.5), u = 10 → 1/v = 1/12.5 - 1/10 = -0.02\n  → v = 50 cm (real side; option 50).",
     "- Concave mirror R = 25 cm (f = 12.5 cm), u = 10 cm: uf/(u-f) =\n  125/(-2.5) = -50 cm → virtual image, 50 cm behind the mirror."),
    # 7. Ch16 trap wording to match magnitude method
    ("TRAP: Concave mirror signs: f and R positive, u negative (real object).\nUse 1/v = 1/f - 1/u carefully.",
     "TRAP: Concave mirror, object inside focus → image is virtual, forms\nbehind the mirror (v comes out negative; give its magnitude)."),
]
for old, new in fixes:
    if old not in s:
        print("WARN not found:", old[:60].replace("\n", "\\n"))
    s = s.replace(old, new)

# ---------- graphs content per chapter ----------
graphs = {
1: ["- Dimension table in the FORMULA BANK is the key memorisation sheet.",
    "- Vernier calipers: least count = 1 MSD - 1 VSD (standard 0.01 cm).",
    "- Screw gauge: least count = pitch / number of circular divisions."],
2: ["- x-t graph: slope = velocity; straight line = uniform velocity.",
    "- v-t graph: slope = acceleration; AREA under v-t = displacement.",
    "- a-t graph: area = change in velocity.",
    "- Projectile path is a parabola; range is maximum at 45°."],
3: ["- Free-body diagram: draw weight, normal, friction, applied force first.",
    "- Force-time graph: area = impulse = change in momentum.",
    "- Momentum conserved with changing mass → v ∝ 1/m (rectangular hyperbola).",
    "- Friction vs applied force: static friction rises to μsN, then drops to μkN."],
4: ["- Force-displacement graph: AREA = work done.",
    "- Spring F vs x: straight line through origin; area = (1/2)kx².",
    "- Power-time graph: area = energy."],
5: ["- MI axes (draw each): ring, disc, sphere, rod — centre / diameter / tangent / end.",
    "- ω-t graph for constant angular acceleration: straight line (slope = α)."],
6: ["- g vs r: inside Earth g ∝ r (linear rise); outside g ∝ 1/r² (falls).",
    "- g vs depth: decreases linearly to zero at the centre.",
    "- Orbit diagram: orbital velocity keeps it circling; escape velocity leaves forever."],
7: ["- Stress-strain curve: linear region slope = Young's modulus, then yield point, fracture.",
    "- Meniscus: concave for contact angle < 90° (water, alcohol); convex for > 90° (mercury).",
    "- Soap bubble has TWO surfaces, drop has ONE → 4T/r vs 2T/r."],
8: ["- P-V diagram: isotherm = hyperbola (PV = const); adiabat is STEEPER (PV^γ = const).",
    "- Carnot cycle: two isotherms + two adiabats; enclosed area = net work per cycle."],
9: ["- Maxwell speed distribution: most-probable < average < rms speed.",
    "- P-V diagram: isothermal hyperbola vs steeper adiabatic curve."],
10:["- SHM: x-t is sinusoidal; v leads x by 90°; a leads x by 180°.",
    "- Energy vs position: PE is a parabola (∝ x²), total energy a horizontal line.",
    "- Transverse wave (crest-trough) vs longitudinal wave (compression-rarefaction)."],
11:["- Field lines: start on +, end on -; never cross; E inside a conductor = 0.",
    "- E vs r for a point charge: E ∝ 1/r² curve.",
    "- Parallel-plate capacitor: uniform field E = V/d between plates.",
    "- Equipotential surfaces are perpendicular to field lines."],
12:["- Ohm's law: V-I graph is a straight line through origin; slope = R.",
    "- Non-ohmic devices (diode, filament) give curved V-I graphs.",
    "- Circuit symbols: cell, resistor, ammeter (series), voltmeter (parallel)."],
13:["- Hysteresis (B-H) loop: area = energy loss per cycle; loop gives retentivity & coercivity.",
    "- Right-hand rule: straight wire → concentric field circles; solenoid → uniform field inside.",
    "- Earth's field: dip = 90° at poles, 0° at equator."],
14:["- AC waveforms: V and I are sine waves; phase angle φ decides the power factor.",
    "- Phasor diagram: VL and VC opposite; at resonance they cancel (cosφ = 1).",
    "- Transformer: two coils on a laminated core; Vp/Vs = Np/Ns."],
15:["- EM spectrum by increasing frequency: radio < micro < IR < visible < UV < X < gamma.",
    "- E and B are perpendicular sinusoids travelling together along the propagation axis."],
16:["- Ray diagrams: concave mirror & convex lens form real inverted images; convex mirror & concave lens always virtual erect.",
    "- YDSE: alternate bright/dark fringes; fringe width β = λD/d.",
    "- Prism: deviation δ = (μ-1)A for a thin prism."],
17:["- Kmax vs frequency ν: straight line; slope = h; x-intercept = threshold frequency ν0.",
    "- Stopping potential vs frequency: straight line with the same intercept."],
18:["- Energy-level diagram: Lyman (to n=1, UV) and Balmer (to n=2, visible) transitions.",
    "- Binding-energy-per-nucleon curve: peaks near Fe-56 (most stable).",
    "- Decay curve: N vs t is exponential decay; half-life constant."],
19:["- Diode V-I: conducts in forward bias, blocks in reverse (knee ~0.7 V Si, 0.3 V Ge).",
    "- Logic symbols: AND, OR, NOT, NAND, NOR (bubble = inversion).",
    "- Transistor symbols: npn (arrow out), pnp (arrow in)."],
20:["- Communication block diagram: transmitter → channel → receiver.",
    "- Propagation: ground wave (follows surface), sky wave (ionosphere reflection), space wave (line-of-sight)."],
}

lines = s.split("\n")
out = []
cur = None
for ln in lines:
    m = re.match(r"^CHAPTER (\d+) —", ln)
    if m:
        cur = int(m.group(1))
    if ln.strip() == "9. LAST-MINUTE REVISION":
        g = graphs.get(cur, [])
        out.append("")
        out.append("9. STANDARD GRAPHS/DIAGRAM KNOWLEDGE")
        for bullet in g:
            out.append("   " + bullet)
        out.append("")
        out.append("10. LAST-MINUTE REVISION")
    else:
        out.append(ln)

open(path, "w", encoding="utf-8").write("\n".join(out))
print("done")
