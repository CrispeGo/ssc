p = "agniveer/Master_Physics_Notes.txt"
s = open(p, encoding="utf-8").read()
miss = []

def rep(old, new):
    global s
    if old not in s:
        miss.append(old[:80].replace("\n","\\n"))
    s = s.replace(old, new)

# ---------- PREFACE ----------
rep("""This book is built strictly from the real Agniveervayu Physics papers.
It teaches the exact knowledge needed to solve them — concept first,
formula, conditions, quick methods, traps, and selected exam examples.
""",
"""HOW THIS BOOK WORKS

Every chapter teaches one topic concept-first, in a fixed flow:
CORE CONCEPTS -> key relations -> formula bank -> conditions/special cases
-> how questions are solved -> 10-second tricks -> facts -> traps -> graphs
-> last-minute revision. Real exam questions appear only as worked examples,
never as a question dump: learn the concept, then solve any variation.

WHAT IS COVERED

All 20 official Agniveervayu Physics topics, built strictly from the real
papers. Every formula, condition, trap and example is something the exam
actually demands — or is directly needed to solve what it demands. Nothing
else has been added.
""")

# ---------- CH1 ----------
rep("- Error analysis (absolute, relative, least count) is in the syllabus.\n", "")
rep("""9. STANDARD GRAPHS/DIAGRAM KNOWLEDGE
   - Dimension table in the FORMULA BANK is the key memorisation sheet.
   - Vernier calipers: least count = 1 MSD - 1 VSD (standard 0.01 cm).
   - Screw gauge: least count = pitch / number of circular divisions.""",
"""9. STANDARD GRAPHS/DIAGRAM KNOWLEDGE
   - Dimension table in the FORMULA BANK is the memorisation sheet here.
   - Conversion ladder: 1 kWh = 3.6 x 10^6 J ; 1 N = 10^5 dyne ;
     1 T = 10^4 gauss ; 1 pm = 10-6 micron (1 micron = 10-6 m).""")

# ---------- CH6 ----------
rep("- Satellite orbital velocity v = √(GM/r)",
    "- Satellite: v = √(GM/r) ; T = 2π√(r3/GM) ; E = -GMm/2r ; PE = 2E ; KE = -E")
rep("- Astronaut in satellite → free fall (weightless), gravity still present.",
    """- Astronaut in satellite → free fall (weightless), gravity still present.
- Satellite in circular orbit: PE = 2 x total energy, KE = -total energy
  (Example: total energy E0 → PE = 2E0).
- Satellite time period depends on central mass M and orbit radius r, NOT
  on the satellite's own mass.
- Escape velocity: planet with 2M and R/2 → ve doubles (11.2 → 22.4 km/s).""")
rep('''- Escape velocity equal for A and B → MA/RA = MB/RB (M ∝ R). Statement 2
  "M1R1 = M2R2" is WRONG — it must be M1/R1 = M2/R2.''',
    '''- Escape velocity equal for A and B → MA/RA = MB/RB (M ∝ R), NOT
  M1R1 = M2R2 (that option is wrong).
- Example: satellite total energy E0 → PE = 2E0, KE = -E0.''')
rep("""TRAP: g from poles to equator DECREASES.""",
    """TRAP: g from poles to equator DECREASES.

TRAP: Satellite time period depends on the CENTRAL body's mass and orbit
radius — NOT on the satellite's own mass.""")
rep("""- F = GMm/r2 ; g = GM/R2 ; ve = √(2gR) ; T2 ∝ r3
- 4M & R/2 → 16g ; 1% smaller R → g up ~2%
- Escape velocity equal ⇒ M/R equal""",
    """- F = GMm/r2 ; g = GM/R2 ; ve = √(2gR) ; T2 ∝ r3
- 4M & R/2 → 16g ; 1% smaller R → g up ~2% ; 2M & R/2 → ve x2
- Satellite: PE = 2E_total ; T = 2π√(r3/GM) (independent of satellite mass)""")

# ---------- CH7 ----------
rep("- Capillarity: contact angle decides meniscus shape.",
    """- Capillarity: contact angle decides meniscus shape.
- Pascal's law: pressure applied to an enclosed fluid is transmitted
  equally in all directions (hydraulic lift/brakes).
- Archimedes: buoyant force = weight of fluid displaced (loss of weight =
  weight of fluid displaced).""")
rep("- Work done in stretching wire W = (1/2) F x (elastic PE).",
    """- Work done in stretching wire W = (1/2) F x (elastic PE).
- Poisson ratio σ = lateral strain / longitudinal strain (unitless).""")
rep("""- Temperature rises → surface tension falls (minimum near 75°C among given
  options).""",
    """- Temperature rises → surface tension falls (minimum near 75°C among given
  options).
- Floating ice melts in a brim-full cup → water level UNCHANGED (the
  displaced water weighs the same as the ice).""")
rep("- Venturi-meter: flow speed. Manometer: pressure difference.",
    """- Venturi-meter: flow speed. Manometer: pressure difference.
- Poisson ratio = lateral/longitudinal strain; Pascal = pressure
  transmission; Archimedes = buoyancy.""")

# ---------- CH9 ----------
rep("""- Real-gas corrections: 'a' accounts for intermolecular attraction,
  'b' for molecular volume.""",
    """- Real-gas corrections: 'a' accounts for intermolecular attraction,
  'b' for molecular volume.
- A temperature rise of 27 °C = a rise of 27 K (1 °C interval = 1 K).""")
rep("""9. STANDARD GRAPHS/DIAGRAM KNOWLEDGE
   - Maxwell speed distribution: most-probable < average < rms speed.
   - P-V diagram: isothermal hyperbola vs steeper adiabatic curve.""",
    """9. STANDARD GRAPHS/DIAGRAM KNOWLEDGE
   - KE vs T: straight line through the origin (E ∝ T).
   - Sound speed vs pressure (constant T): flat line — v does not change.
   - P-V diagram: isothermal hyperbola vs steeper adiabatic curve.""")

# ---------- CH10 ----------
rep("- Dipole SHM: ω = √(2qE/md) for an electric dipole.\n", "")
rep("- Acceleration in SHM: a = -ω2x.",
    """- Acceleration in SHM: a = -ω2x.
- Ratio (max acceleration)/(max velocity) = ω = 2πf.
  Example: A = 0.01 m, f = 50 Hz → ratio = 100π.""")

# ---------- CH11 ----------
rep("""- Distance between plates increased (charge constant) → C decreases
  (C = ε0A/d), U = Q2/2C increases.""",
    """- Distance between plates increased (charge constant) → C decreases
  (C = ε0A/d), U = Q2/2C increases. d doubled → C halves (10 μF → 5 μF).""")

# ---------- CH13 ----------
rep('''- Coil moment ∝ square of wire length: m = NI(πr2) with fixed wire length
  → m ∝ L2. (Option: "directly proportional to the square of the length
  of wire.")''',
    '''- Coil moment with fixed wire length L: m = NI(πr2) and L = 2πrN ⇒
  m ∝ L2 (directly proportional to the square of the wire length).''')
rep("""- Angle of dip = 90° at magnetic poles, 0° at magnetic equator.
- μ0 = 4π x 10-7 T m/A.""",
    """- Angle of dip = 90° at magnetic poles, 0° at magnetic equator.
- Ferromagnetic above the Curie temperature → becomes PARAMAGNETIC.
- 1 tesla = 10^4 gauss ; μ0 = 4π x 10-7 T m/A.""")

# ---------- CH14 ----------
rep("""- ε = -dΦ/dt = -A dB/dt (area A fixed):
  A = 2 m2, B: 4 → 8 Wb/m2 in 2 s → ε = 2 x (4/2) = 4 V.""",
    """- ε = -dΦ/dt = -A dB/dt (area A fixed):
  A = 2 m2, B: 4 → 8 Wb/m2 in 2 s → ε = 2 x (4/2) = 4 V.
- Φ(t) given → differentiate. Example: Φ = 6t2 + 3t + 2 (weber) →
  ε = dΦ/dt = 12t + 3 ; at t = 3 s → 39 V.""")
rep("- Higher impedance circuit carries LESS current (same source).",
    """- Higher impedance circuit carries LESS current (same source).
- Magnet moved faster toward a coil → larger induced emf (ε ∝ rate of
  flux change ∝ speed).""")
rep("- Filter gives smooth DC output from a rectifier.",
    """- Filter gives smooth DC output from a rectifier.
- Weber = unit of magnetic flux; henry = unit of inductance.""")

# ---------- CH15 ----------
rep("- EM waves are transverse; they propagate in vacuum.",
    """- EM waves are transverse; they propagate in vacuum.
- EM waves carry ENERGY (not charge or mass).
- Highest frequency = gamma rays; longest wavelength = radio; among
  UV/X-ray/microwave/gamma, microwave has the longest wavelength.""")

# ---------- CH16 ----------
rep("""- YDSE: fringe width β = λD/d ; position of nth bright fringe
  yn = n λ D / d.""",
    """- YDSE: fringe width β = λD/d ; position of nth bright fringe
  yn = n λ D / d.
- Critical angle (relative): sin C = μrarer / μdenser.
  Water 4/3, glass 5/3 (glass→water) → C = sin-1(4/5).
- Simple microscope (image at D = 25 cm): M = 1 + D/f.
  Example: f = 4 cm → M = 1 + 25/4 = 7.25.""")

# ---------- CH17 ----------
rep("- Einstein equation: hν = φ + Kmax (Kmax = eV0).",
    """- Einstein equation: hν = φ + Kmax (Kmax = eV0).
- Matter waves: a moving particle has a de Broglie wavelength λ = h/p.""")
rep("- Threshold is about FREQUENCY (min), not intensity or power.",
    """- Threshold is about FREQUENCY (min), not intensity or power.
- de Broglie: λ = h/p = h/√(2mK). Example: λ = 0.2 Å →
  p = h/λ = 3.3 x 10-23 kg m/s.
- Same KE: λ ∝ 1/√m → λproton/λelectron = √(me/mp) ≈ 1/43.""")
rep("- E = hν = hc/λ ; λ = h/p (de Broglie)",
    "- E = hν = hc/λ ; de Broglie λ = h/p = h/√(2mK)")
rep("- Photon has energy and momentum but zero rest mass.",
    "- Photon: E = hν. Matter wave: λ = h/p.")
rep("""- E = hν = hc/λ ; E(eV) = 12400/λ(Å)
- φ = hc/λ0 ; hν = φ + Kmax
- λ0 = 5000 Å → φ ≈ 4x10-19 J ; 6000 Å → 2.06 eV""",
    """- E = hν = hc/λ ; E(eV) = 12400/λ(Å) ; λ = h/p = h/√(2mK)
- φ = hc/λ0 ; hν = φ + Kmax ; same KE → λ ∝ 1/√m
- λ0 = 5000 Å → φ ≈ 4x10-19 J ; 6000 Å → 2.06 eV ; 0.2 Å → 3.3x10-23 kg m/s""")

# ---------- CH18 ----------
rep("""- N = N0 e^(-λt) ; T1/2 = 0.693/λ ; τ(mean life) = 1/λ
- Spectral lines from n to m: (n-m)(n-m+1)/2
- Binding energy: E = Δm c2""",
    """- N = N0 e^(-λt) ; T1/2 = 0.693/λ = 0.693 x τ ; mean life τ = 1/λ
- Spectral lines from n to m: (n-m)(n-m+1)/2""")
rep("- λ = 0.00231/day → 300 days half-life.",
    """- λ = 0.00231/day → 300 days half-life.
- Mean life τ = 50 days → T1/2 = 0.693 x 50 = 34.65 days.""")
rep("""   - Energy-level diagram: Lyman (to n=1, UV) and Balmer (to n=2, visible) transitions.
   - Binding-energy-per-nucleon curve: peaks near Fe-56 (most stable).
   - Decay curve: N vs t is exponential decay; half-life constant.""",
    """   - Energy-level diagram: Lyman (to n=1, UV) and Balmer (to n=2, visible) transitions.
   - Decay curve: N vs t is exponential decay; half-life constant.""")
rep("- α, β, γ: γ has no mass/charge (pure energy), highest penetration.",
    "- α, β, γ (penetrating power): γ > β > α ; γ has no mass/charge (pure energy).")

# ---------- CH19 ----------
rep("- Full-wave rectifier uses 2 diodes (bridge uses 4).",
    """- Zener diode: HEAVILY doped, connected in REVERSE bias, used as a
  VOLTAGE REGULATOR.""")
rep("""- Diode: conducts in forward bias only.
- Transistor current: Ie = Ib + Ic ; gain β = Ic/Ib.""",
    "- Diode: conducts in forward bias only; Zener conducts in reverse breakdown.")
rep("- Zener diode: used as voltage regulator (reverse breakdown).",
    "- Zener diode: heavily doped, reverse biased → voltage regulator.")
rep("""- Pentavalent → N-type ; trivalent → P-type
- Reverse bias widens depletion region
- Rectifier → filter → regulator ; npn > pnp (electron mobility)""",
    """- Pentavalent → N-type ; trivalent → P-type
- Reverse bias widens depletion region ; Zener = heavily doped, reverse, regulator
- Rectifier → filter → regulator ; npn > pnp (electron mobility)""")

# ---------- CH20 ----------
rep("""- A signal carries information; modulation superimposes it on a carrier.
- Propagation modes: ground wave, sky wave (ionosphere reflection), and
  space wave — radio waves use ALL THREE.
- Modulation: AM (amplitude), FM (frequency).
- Antenna height ∝ 1/frequency for transmission.""",
    """- A signal carries information; MODULATION superimposes the low-frequency
  baseband signal onto a high-frequency carrier (necessary for effective
  transmission).
- DEMODULATION = recovering the original signal at the receiver (the
  reverse of modulation).
- Propagation modes: ground wave, sky wave (ionosphere reflection) and
  space wave — radio waves use ALL THREE.""")
rep("""- c = νλ (carrier and signal both EM).
- Modulation index (AM) μ = Am/Ac.""",
    "- c = νλ (carrier and signal both EM) ; modulation index μ = Am/Ac.")
rep("- Space wave: line-of-sight for TV/microwave.",
    """- Space wave: line-of-sight for TV/microwave.
- Voice sounding high-pitched (man → woman) after transmission = wrong
  bandwidth selection of the amplifiers.""")
rep("- Ionosphere reflects sky waves; satellites use space wave.",
    """- Ionosphere reflects sky waves; satellites use space wave.
- Modulation is necessary for transmission; demodulation is its reverse.""")
rep("""- Propagation: ground, sky (ionosphere), space (LOS)
- AM/FM are modulation types""",
    """- Modulation (baseband on carrier) → transmit → demodulation at receiver
- Propagation: ground, sky (ionosphere), space (LOS)""")

# ---------- FINAL FORMULA ----------
rep("- F = GMm/r2 ; g = GM/R2 ; ve = √(2gR) ; T2 ∝ r3 ; 4M&R/2 → 16g",
    "- F = GMm/r2 ; g = GM/R2 ; ve = √(2gR) ; T2 ∝ r3 ; 4M&R/2 → 16g ; satellite PE = 2E_total")
rep("- SHM: v = ω√(A2-x2) ; vmax = ωA ; amax = ω2A ; x = A/2 → (√3/2)vmax",
    "- SHM: v = ω√(A2-x2) ; vmax = ωA ; amax = ω2A ; amax/vmax = 2πf ; x = A/2 → (√3/2)vmax")
rep("- ε = -dΦ/dt = -A dB/dt ; transformer Vp/Vs = Np/Ns ; η = VsIs/VpIp",
    "- ε = -dΦ/dt = -A dB/dt ; ε = dΦ/dt from Φ(t) ; transformer Vp/Vs = Np/Ns ; η = VsIs/VpIp")
rep("- c = νλ = 1/√(μ0ε0) ; E0 = cB0 ; E = hν = hc/λ ; E(eV) = 12400/λ(Å)",
    "- c = νλ = 1/√(μ0ε0) ; E0 = cB0 ; E = hν = hc/λ ; λ = h/p ; E(eV) = 12400/λ(Å)")
rep("- δ = (μ-1)A ; β = λD/d ; yn = nλD/d",
    "- δ = (μ-1)A ; β = λD/d ; yn = nλD/d ; sin C = μr/μd ; M = 1 + D/f")
rep("- T1/2 = 0.693/λ ; N = N0 e^(-λt) ; lines n→m = (n-m)(n-m+1)/2",
    "- T1/2 = 0.693/λ = 0.693τ ; N = N0 e^(-λt) ; lines n→m = (n-m)(n-m+1)/2")

# ---------- FINAL TRICKS ----------
rep("- 4x mass & half radius → 16g ; equal escape velocity → equal M/R.",
    """- 4x mass & half radius → 16g ; equal escape velocity → equal M/R.
- Satellite: PE = 2 x total energy ; T independent of satellite mass.""")
rep("- Mean position → v max ; A doubled → energy x4 ; x = A/2 → (√3/2)v.",
    """- Mean position → v max ; A doubled → energy x4 ; x = A/2 → (√3/2)v.
- amax/vmax = 2πf ; same-KE de Broglie → λ ∝ 1/√m.""")
rep("- E0/B0 = c ; E(eV) = 12400/λ(Å) ; T1/2 = 0.693/λ.",
    """- E0/B0 = c ; E(eV) = 12400/λ(Å) ; T1/2 = 0.693/λ.
- Zener = reverse-biased regulator ; ferromagnetic → paramagnetic above Curie T.""")

# ---------- FINAL TRAPS ----------
rep("- Concave mirror sign convention: f, R positive; u negative.",
    "- Concave mirror: object inside focus → virtual image behind mirror.")
rep("- Spectral lines n→m = (n-m)(n-m+1)/2, not n(n-1)/2.",
    """- Spectral lines n→m = (n-m)(n-m+1)/2, not n(n-1)/2.
- Mean life vs half-life: T1/2 = 0.693τ (not τ).""")

# ---------- FINAL FACTS ----------
rep("- Angle of dip: poles 90°, equator 0°.",
    "- Angle of dip: poles 90°, equator 0° ; 1 T = 10^4 gauss.")
rep("- Galaxies are receding (distance increasing).",
    """- Galaxies are receding (distance increasing).
- EM waves carry energy; Poisson ratio = lateral/longitudinal strain.
- 27 °C rise = 27 K ; henry = inductance ; weber = flux ; Zener = regulator.""")

open(p, "w", encoding="utf-8").write(s)
print("MISSED:", len(miss))
for m in miss:
    print("  -", m)
