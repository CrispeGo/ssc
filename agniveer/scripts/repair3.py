# -*- coding: utf-8 -*-
"""Third (final) repair pass: concise one-liners for remaining singleton facts."""
import sys
path = "/home/user/pdf_build/content.txt"
text = open(path, encoding="utf-8").read()

EDITS = [
("1 kWh = 3.6 × 10⁶ J (kilo-watt-hour → joules).",
 "- [potential] = [M¹L²T⁻³A⁻¹] ; [magnetic field B] = [M¹T⁻²A⁻¹] (F = qvB se).\n- Coefficient of viscosity η ka SI unit Pa·s (poiseuille), CGS unit poise."),
("Time (second) hi ek aisi quantity hai jiska unit CGS aur SI dono mein SAME hai.",
 "- km/h → m/s: ×5/18 (54 km/h = 15 m/s)."),
("- s = xt² − yt + z (polynomial in t): a = d²s/dt² = 2x — CONSTANT, isliye t = 4 s par bhi 2x hi hoga.",
 "- Average speed (distance segments): v_avg = total distance / total time. 1/3 distance at 60 km/h, 2/3 at 30 km/h → v_avg = 36 km/h.\n- Escalator/moving walkway: combined time t = t₁t₂/(t₁+t₂) (walk speed + walkway speed).\n- Coefficient of restitution e = separation speed / approach speed; bounce ke baad height = e²h (perfectly elastic e = 1)."),
("- Temperature badhao → surface tension ghatta hai.",
 "- Elasticity = wo ability jisse body permanent change ko RESIST karti hai (stress hatane par original shape wapas aa jaati hai)."),
("- Echo sunne ke liye minimum distance ≈ 17 m (sound 340 m/s, 0.1 s ka gap).",
 "- SHM examples: pendulum (chhota angle), spring-block. NOT SHM: uniform circular motion, earth ka rotation."),
("- q = ne (quantisation); e = 1.6×10⁻¹⁹ C.",
 "- Conductor ka saara charge OUTER surface par rehta hai (E inside = 0) — external field mein bhi redistribution surface par hi hoti hai."),
("- Mirror/image velocity: tum plane mirror ki taraf speed u se bhaago → image tumhari taraf 2u se aati hai (object ke relative image ki speed = 2u).",
 "- Vehicle ka rear-view mirror CONVEX hota hai: wide field of view + hamesha erect, diminished image."),
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
