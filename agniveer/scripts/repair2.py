# -*- coding: utf-8 -*-
"""Second repair pass: small but real PYQ families not yet fully covered."""
import sys
path = "/home/user/pdf_build/content.txt"
text = open(path, encoding="utf-8").read()

EDITS = [
# Ch8 path function
("- Source temperature badhao → Carnot efficiency badhti hai.",
 "- Heat aur work PATH functions hain (process par depend karte hain); internal energy STATE function hai (process par nahi).\n- P-V diagram: area under curve = work; adiabat isotherm se STEEPER (PV^γ)."),
# Ch10 SHM time to x
("- SHM: v leads x by 90°; a leads v by 90° (a = −ω²x).",
 "- Time to reach x from mean: t = (T/2π) × sin⁻¹(x/A). Mean → A/2: t = T/12 (fixed value)."),
# Ch10 echo
("- Ultrasonic > 20 kHz; sound speed in air ≈ 332 m/s.",
 "- Echo sunne ke liye minimum distance ≈ 17 m (sound 340 m/s, 0.1 s ka gap)."),
# Ch11 conductor between charges
("- q = ne (quantisation); e = 1.6×10⁻¹⁹ C.",
 "- Do charges ke beech CONDUCTOR plate rakho → net force ZERO ho jaata hai (conductor ke andar E = 0)."),
# Ch13 magnetic force does no work
("- Cyclotron: f = qB/2πm ; F/L = μ₀I₁I₂/2πd ; τ = MB sinθ.",
 "- Magnetic force hamesha velocity ke ⊥ hoti hai → koi WORK nahi karti → particle ki KE CONSTANT rehti hai (sirf direction badalti hai)."),
# Ch14 half-wave Vdc + N turns
("- ε = M dI/dt : M = 0.5 H, ΔI = 4 A in 0.5 s → ε = 0.5 × 8 = 4 V.",
 "- N-turn coil: ε = N dΦ/dt. Half-wave rectifier ka DC output = V₀/π (full sine ka half-cycle average 2V₀/π)."),
# Ch16 mirror image velocity
("- Plane mirror: v = u.",
 "- Mirror/image velocity: tum plane mirror ki taraf speed u se bhaago → image tumhari taraf 2u se aati hai (object ke relative image ki speed = 2u)."),
# Ch17 eV to joule
("- E = hc/λ ; E(eV) = 12400/λ(Å) = 1240/λ(nm).",
 "- 1 eV = 1.6×10⁻¹⁹ J (joules mein convert karne ke liye eV ko 1.6×10⁻¹⁹ se multiply karo)."),
]

missing = []
for anchor, block in EDITS:
    n = text.count(anchor)
    if n != 1:
        missing.append((anchor[:60], n))
if missing:
    print("ANCHOR PROBLEMS:")
    for a, n in missing:
        print(f"  count={n} : {a}")
    sys.exit(1)

for anchor, block in EDITS:
    text = text.replace(anchor, anchor + "\n" + block, 1)

open(path, "w", encoding="utf-8").write(text)
print(f"Applied {len(EDITS)} insertions OK. Lines: {len(text.splitlines())}")
