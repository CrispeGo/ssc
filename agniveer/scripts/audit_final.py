# -*- coding: utf-8 -*-
"""Final audit aggregation (v6, post-repair). Uses audit_classify v5 + manual overrides
   + family-status upgrades for families now covered by the repaired book."""
import importlib, io, contextlib, collections, re
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    ac = importlib.import_module('audit_classify')
res, un = ac.classify()

# ---- overrides for unmatched + correctness spot-fixes (paper,qid) -> (ch,fam,st) ----
OV = {
 # Hindi paper P5 (Devanagari) — translated, book judged on English content
 ('P5','Q1'):('Ch1 Units','Unitless quantity','A'),
 ('P5','Q2'):('Ch1 Units','Vector quantity','A'),
 ('P5','Q4'):('Ch4 WorkEnergy','P=FV','A'),
 ('P5','Q5'):('Ch6 Gravitation','g depends on M','A'),
 ('P5','Q6'):('Ch6 Gravitation','Escape velocity value','A'),
 ('P5','Q7'):('Ch19 Electronics','AND+NOT = NAND','A'),
 ('P5','Q8'):('Ch16 Optics','Plane mirror image','A'),
 ('P5','Q9'):('Ch10 Osc/Waves','Polarization','A'),
 ('P5','Q11'):('Ch12 Current','Triangle resistance','A'),
 ('P5','Q12'):('Ch11 Electrostatics','Capacitor distance double','A'),
 ('P5','Q14'):('Ch12 Current','Cells parallel internal r','A'),
 ('P5','Q15'):('Ch5 Rotational','CM depends on','A'),
 ('P5','Q16'):('Ch8 Thermo','Carnot source temp','A'),
 ('P5','Q17'):('Ch8 Thermo','First law 2 mol','A'),
 ('P5','Q18'):('Ch17 Dual Nature','Threshold double -> phi','A'),
 ('P5','Q20'):('Ch1 Units','Unit but no dimension','A'),
 ('P5','Q21'):('Ch8 Thermo','Isothermal dU=0','A'),
 ('P5','Q22'):('Ch7 Bulk','Viscosity stops liquid','A'),
 ('P5','Q23'):('Ch14 EMI/AC','Inductive 90°','A'),
 ('P5','Q24'):('Ch13 Magnetism','Electron KE in B','A'),
 ('P5','Q25'):('Ch14 EMI/AC','Eddy currents','A'),
 # ambiguous "choose correct statement" (options lost in TXT)
 ('P6','Q12'):('Ch16 Optics','Ambiguous statement','D'),
 ('P11','Q9'):('Ch3 Laws','Ambiguous statement','D'),
 ('P14','Q21'):('Ch16 Optics','Ambiguous statement','D'),
 ('P15','Q21'):('Ch16 Optics','Ambiguous statement','D'),
 # diagram/graph-dependent (figure not in TXT)
 ('P19','Q9'):('Ch11 Electrostatics','Flux via figure','D'),
 # mangled transcription (P28 has no keyed twin)
 ('P28','Q15'):('Ch13 Magnetism','Mangled options only','D'),
 ('P28','Q22'):('Ch3 Laws','Mangled','D'),
 ('P4','Q11'):('Ch3 Laws','F=dp/dt','A'),
 ('P12','Q13'):('Ch13 Magnetism','Curie temperature','A'),
 ('P17','Q5'):('Ch15 EM Waves','E0/B0=c','A'),
 ('P19','Q12'):('Ch4 WorkEnergy','W=Fs from x(t)','A'),
 ('P14','Q6'):('Ch16 Optics','Mirror diagram','D'),
 ('P7','Q11'):('Ch16 Optics','Rear-view convex mirror','B'),
 ('P15','Q6'):('Ch16 Optics','Mirror diagram','D'),
 ('P21','Q7'):('Ch13 Magnetism','Para vs dia with T','A'),
 ('P21','Q16'):('Ch16 Optics','Snell i=r -> μ=1','A'),
 ('P21','Q24'):('Ch8 Thermo','Polytropic PV2 work','A'),
 ('P22','Q7'):('Ch13 Magnetism','B coil axis','A'),
 ('P23','Q7'):('Ch13 Magnetism','B coil axis','A'),
 ('P22','Q12'):('Ch13 Magnetism','F=BIl sinθ','A'),
 ('P23','Q12'):('Ch13 Magnetism','F=BIl sinθ','A'),
 ('P22','Q22'):('Ch5 Rotational','KE of CM','A'),
 ('P23','Q22'):('Ch5 Rotational','KE of CM','A'),
 ('P22','Q24'):('Ch16 Optics','Images two mirrors','A'),
 ('P23','Q24'):('Ch16 Optics','Images two mirrors','A'),
 # recoverable from keyed twin paper (text lost in User-TXT copy)
 ('P27','Q9'):('Ch15 EM Waves','E,B,k representation','A'),
 ('P27','Q16'):('Ch12 Current','Parallel product/sum','A'),
 ('P27','Q19'):('Ch16 Optics','Mirror formula numeric','A'),
 ('P30','Q7'):('Ch8 Thermo','First law cal','A'),
 ('P30','Q18'):('Ch6 Gravitation','g pole/equator','A'),
 ('P30','Q23'):('Ch17 Dual Nature','Threshold = frequency','A'),
 # chapter-label corrections (substring rule collisions; status unchanged)
 ('P31','Q18'):('Ch13 Magnetism','T=2πm/qB','A'),
 ('P33','Q5'):('Ch13 Magnetism','T=2πm/qB','A'),
 ('P34','Q5'):('Ch13 Magnetism','T=2πm/qB','A'),
 ('P9','Q6'):('Ch14 EMI/AC','Inductor energy','A'),
 ('P31','Q14'):('Ch11 Electrostatics','Capacitor','A'),
 ('P19','Q10'):('Ch10 Osc/Waves','Interference phase','A'),
 ('P21','Q25'):('Ch10 Osc/Waves','Echo','A'),
 ('P10','Q6'):('Ch15 EM Waves','E/B same phase','A'),
 ('P29','Q11'):('Ch7 Bulk','Terminal velocity','A'),
 ('P30','Q11'):('Ch7 Bulk','Terminal velocity','A'),
 ('P5','Q3'):('Ch3 Laws','F=ma force','A'),
 ('P33','Q8'):('Ch5 Rotational','CM velocity','A'),
}

# ---- family-status upgrades: families now covered by the repaired book ----
# key = classifier/OV family name -> new status (chapter inferred by row)
FAM_STATUS = {
 'F<->C conversion':'A','Stefan-Boltzmann value':'A','Mechanical equiv heat':'A',
 'Pole strength unit':'A','Dipole moment CGS':'A','Dimension ratio h/I':'A',
 'Vector addition':'A','Min forces':'A','Equilibrium conditions':'A','Atwood pulley':'A',
 'Lift apparent weight':'A','Force not electromagnetic':'A','Angle between vectors':'A',
 'Wire energy ½YS²':'A','Energy density ½σε':'A','Chain on table':'A',
 'CM uniform body':'A','CM position':'A','CM statements':'A','α in UCM':'A',
 'Torque cross product':'A',
 'g vs height exact':'A','g∝ρR':'A',
 'Breaking stress':'A','Max elasticity':'A','Modulus rigidity':'A','Drops volume->r':'A',
 'Float fraction':'A','Thermal expansion':'A','Thermal expansion αβγ':'A',
 'Thermometer expansion':'A','Thermal stress glass':'A','Calorimetry':'A',
 'Capillary rise':'A','Viscosity depends':'A',
 'Isochoric W=0':'A','Isobaric':'A','Refrigerator COP':'A','Path function':'A',
 'rms ∝√T':'A',
 't for x=a/2':'A','v-a phase':'A','Phase diff waves':'A','Stationary wave':'A',
 'Wave number k':'A','Echo':'A','Intensity vs amplitude':'A','Wave relations':'A',
 'Polarization':'A',
 'V=W/q':'A','Dipole E,V vs r':'A','PE of charge system':'A','Shell σ':'A',
 'Charge quantization':'A','Conductor between charges':'A','Equipotential':'A',
 'Internal resistance':'A','Drift velocity':'A','Temperature coefficient':'A',
 'L from R,ρ,V':'A','EMF depends':'A','Cells internal r':'A',
 'Heater wire material':'A','Reciprocal of resistance':'A',
 'B coil centre':'A','Cyclotron':'A','Torque MB sinθ':'A','χ=μr-1':'A',
 'Ferromagnetic materials':'A','Magnet NS':'A','Parallel wires force':'A',
 'Biot-Savart':'A','KE constant ⊥B':'A','Electron KE in B':'A',
 'Mutual emf':'A','Resonant freq formula':'A','Eddy currents':'A','Inductor energy':'A',
 'Transformer const':'A','Half-cycle average 2I0/pi':'A','Half-wave Vdc':'A','N dΦ/dt':'A',
 'Wavelength range':'A','Intensity I=P/4pir2':'A',
 'Images two mirrors':'A','Lens power P=1/f':'A','Lens maker':'A','Lens maker liquid':'A',
 'Deviation mirror':'A','λ/μ':'A','μ=c/fλ':'A','Dispersion':'A','Rainbow':'A',
 'Violet deviates':'A','YDSE amplitude':'A','Interference phase':'A','Huygens':'A',
 'Diffraction condition':'A','Telescope':'A','Colour absorption':'A',
 'Brewster polarization':'A','Velocity ratio v=c/mu':'A','Erect -> convex mirror':'A',
 'Image velocity':'A',
 'eV→J':'A',
 'Decay balancing':'A','Series name':'A',
 'Logic gates':'A','Ge at 0K':'A','Emitter doping':'A','Conduction band':'A',
 'AND+NOT = NAND':'A',
 'Galaxies receding':'A',
 # concise singleton facts (final pass)
 'Boyle name':'A','Viscosity unit':'A','Potential dimension':'A','B field dimension':'A',
 'Elasticity definition':'A','SHM examples':'A','Rear-view convex mirror':'A',
 'Charge on conductor':'A','km/h conversion':'A','Avg speed segments':'A',
 'Escalator':'A','Restitution':'A',
}

res, un = ac.classify()
final=[]
for r in res:  # r = (p,qid,q,a,ch,fam,st)
    key=(r[0],r[1])
    if key in OV: final.append(r[:4]+OV[key])
    else: final.append(r)
for r in un:
    key=(r[0],r[1])
    if key in OV: final.append(r[:4]+OV[key])
    else: print("STILL UNMATCHED:", r[0], r[1], r[2][:90])

# apply FAM_STATUS upgrades
hits=collections.Counter()
final2=[]
for r in final:
    p,qid,q,a,ch,fam,st = r
    if fam in FAM_STATUS:
        st = FAM_STATUS[fam]; hits[fam]+=1
    final2.append((p,qid,q,a,ch,fam,st))
final=final2
missed=[f for f in FAM_STATUS if hits[f]==0]
if missed: print("FAM_STATUS keys never matched:", missed)

tot=len(final)
c=collections.Counter(r[6] for r in final)
A,B,Cc,D = c['A'],c['B'],c['C'],c['D']
print("TOTAL",tot," A",A,"B",B,"C",Cc,"D",D)
den=tot-D
print("FULL %  = A/(tot-D)         =", round(A/den*100,2))
print("EFF50 % = (A+0.5B)/(tot-D)  =", round((A+0.5*B)/den*100,2))
print("OPTB %  = (A+B)/(tot-D)     =", round((A+B)/den*100,2))

# per-chapter
by=collections.defaultdict(list)
for r in final: by[r[4]].append(r)
def uniq(rows):
    s=set()
    for r in rows:
        k=re.sub(r'\d+','N',re.sub(r'[^a-z ]',' ',r[2].lower())); k=re.sub(r'\s+',' ',k).strip()
        if k: s.add(k)
    return len(s)
order=sorted(by.keys(), key=lambda x:(x!='Misc',x))
print("\nCHAPTER\tTOTAL\tUNIQ\tA\tB\tC\tD\tFULL%")
for ch in order:
    rows=by[ch]; cc=collections.Counter(r[6] for r in rows)
    u=uniq(rows); f=round(cc['A']/max(1,len(rows)-cc['D'])*100,1)
    print(f"{ch}\t{len(rows)}\t{u}\t{cc['A']}\t{cc['B']}\t{cc['C']}\t{cc['D']}\t{f}")

fam=collections.defaultdict(list)
for r in final: fam[(r[4],r[5],r[6])].append(r)
print("\n== C FAMILIES (by count) ==")
for k,v in sorted(fam.items(), key=lambda x:-len(x[1])):
    if k[2]=='C': print(f"  {k[0]:18s} {k[1][:40]:40s} x{len(v)}")
print("\n== B FAMILIES ==")
for k,v in sorted(fam.items(), key=lambda x:-len(x[1])):
    if k[2]=='B': print(f"  {k[0]:18s} {k[1][:40]:40s} x{len(v)}")

with open('audit_results.tsv','w') as f:
    f.write("paper\tqid\tans\tstatus\tchapter\tfamily\tq\n")
    for r in final:
        f.write(f"{r[0]}\t{r[1]}\t{r[3]}\t{r[6]}\t{r[4]}\t{r[5]}\t{r[2]}\n")
print("\ndumped audit_results.tsv")
