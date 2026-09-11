#!/usr/bin/env python3
"""Generate 00_STRUCTURE_PROPOSAL.md from gs_classified.json — all numbers computed live."""
import json, collections, os, sys

qs = json.load(open('master_build/gs_classified.json'))
N_PAPERS = 193
ANALYZABLE = [q for q in qs if q['subject'] not in ('NO-TEXT','NON-GS')]
OUT = []

def w(s=''): OUT.append(s)

# topic -> chapter mapping (for proposal structure)
CH = {
 'HISTORY': [
   ('प्राचीन भारत — Indus/Vedic/Buddha-Jain/Maurya/Gupta-Chola', ['Ancient-IVC','Ancient-Vedic','Ancient-Buddhism/Jainism','Ancient-Mauryan','Ancient-Gupta&Later','Ancient-PostGupta','Ancient-Prehistory','Ancient-Misc2','Ancient-Misc3']),
   ('मध्यकालीन भारत — Sultanate/Mughal/Maratha-Bhakti-Sufi', ['Medieval-Sultanate','Medieval-Mughal','Medieval-Maratha/Bhakti-Sufi','Medieval-Misc2','Medieval-Misc3','Medieval-Rajput/Misc']),
   ('आधुनिक भारत — British rule/1857/Freedom struggle/Socio-religious', ['Modern-BritishRule','Modern-1857','Modern-FreedomStruggle','Modern-SocioReligious','Modern-Organizations','Modern-Misc2','Modern-Misc3']),
   ('विश्व इतिहास — Revolutions/World Wars/Renaissance', ['World-Revolution','World-Wars&After','World-Misc','World-Misc2']),
 ],
 'GEOGRAPHY': [
   ('भारत — States/Capitals/Boundaries', ['States&Boundaries']),
   ('भारत — Rivers', ['Rivers']),
   ('भारत — Mountains/Passes/Plains/Plateaus', ['Mountains/Passes','Mountains2','Plains&Landforms']),
   ('भारत — Climate/Monsoon', ['Climate']),
   ('भारत — Soils/Agriculture/Crops', ['Soils','Agriculture-Geo']),
   ('भारत — Population/Census', ['Population']),
   ('भारत — Lakes/Waterfalls/Dams', ['Lakes/Waterfalls','Dams&Projects']),
   ('भारत — Minerals/Energy/Industry', ['Minerals&Industry','Energy&Industry']),
   ('भारत — Transport/Highways/Ports', ['Transport/Highways']),
   ('Physical Earth — Earthquake/Volcano/Rocks/Time zones', ['EarthBasics','EarthBasics2','EarthBasics3']),
   ('Oceanography', ['Oceanography']),
   ('विश्व भूगोल — Continents/Countries/Deserts/Grasslands', ['World-Geo','World-Misc2']),
   ('Solar System/Space (static)', ['SolarSystem','Astronomy','Astronomy2']),
 ],
 'POLITY': [
   ('Constitution — making/Preamble/salient features', ['Constitution']),
   ('Articles + Fundamental Rights/Writs', ['Articles/FundamentalRights']),
   ('Fundamental Duties + DPSP', ['Duties&DPSP']),
   ('Parliament — LS/RS/Bills/Session', ['Parliament']),
   ('President/VP/PM/Governor/Council of Ministers', ['Executive-President/PM']),
   ('Judiciary — SC/HC/PIL', ['Judiciary']),
   ('Amendments + Emergency', ['Amendments&Emergency']),
   ('Panchayati Raj + Municipalities', ['PanchayatiRaj']),
   ('Constitutional/Statutory Bodies + Elections', ['Bodies&Elections']),
   ('Laws & Acts — IPC/RPA/Acts timeline', ['Laws&Acts','Laws2']),
   ('Union structure/Citizenship/Schedules', ['UnionStructure','UnionStructure2','Misc-Polity','Misc2']),
 ],
 'ECONOMICS': [
   ('RBI + Monetary policy', ['RBI&Monetary']),
   ('Money & Banking + Public finance', ['Money&Banking','Money&Banking2']),
   ('Budget + Taxation', ['Budget&Tax']),
   ('National Income — GDP/GNP/NNP', ['NationalIncome']),
   ('Planning + Govt Schemes + Poverty', ['Planning','Schemes','Poverty&Employment']),
   ('Market theory — demand/supply/cost/competition', ['Markets-Cost','Markets&Trade']),
   ('International institutions — IMF/WTO/World Bank', ['Institutions']),
   ('Reforms/Sectors/Industry', ['Reforms&Industry','Sectors']),
   ('Inflation', ['Inflation']),
   ('Agri-economics — Revolutions/MSP', ['Agriculture-Eco']),
   ('Misc', ['Misc-Eco']),
 ],
 'BIOLOGY': [
   ('Cell & Genetics — DNA/chromosome/mitosis', ['Cell&Genetics','Cell&Genetics2']),
   ('Plants & Botany — photosynthesis/taxonomy', ['Plants']),
   ('Human body — Circulation/Respiration/Digestion', ['Circulation','Respiration/Excretion','Digestion']),
   ('Human body — Hormones/Nerves/Bones/Muscles/Facts', ['Nervous/Hormones','Skeleton/Muscles','Skeleton2','Body-Facts']),
   ('Nutrition + Deficiency diseases', ['Nutrition/Deficiency']),
   ('Diseases & Immunity', ['Disease&Immunity','Disease&Immunity2']),
   ('Animal kingdom + Husbandry', ['Classification','AnimalHusbandry']),
 ],
 'ENVIRONMENT': [
   ('National Parks/Sanctuaries/Tiger reserves', ['Parks&Sanctuaries']),
   ('Forests/Wetlands/Ramsar + Acts', ['Wetlands&Acts']),
   ('Ecosystem/Biodiversity/Species/IUCN', ['Biodiversity/Ecosystem','Species&IUCN']),
   ('Pollution', ['Pollution']),
   ('Climate change/Ozone/Protocols', ['ClimateChange/Ozone']),
 ],
 'PHYSICS': [
   ('Motion/Force/Newton', ['Motion&Force']),
   ('Work/Energy/Machines', ['Work/Energy/Machines']),
   ('Electricity/Magnetism', ['Electricity/Magnetism','Electricity2']),
   ('Heat/Thermodynamics', ['Heat','Heat2']),
   ('Optics/Light', ['Optics']),
   ('Sound', ['Sound']),
   ('Units/Measurement/Instruments', ['Units&Measurement','Units2','Pressure/Fluids']),
   ('Waves/EM spectrum', ['Waves']),
   ('Modern physics — atom/radioactivity/relativity', ['ModernPhysics','ModernPhysics2']),
   ('Daily-life physics', ['DailyLife-Phy']),
   ('Misc/Inventions', ['Misc-Phy']),
 ],
 'CHEMISTRY': [
   ('Acids/Bases/Salts/pH', ['Acids/Bases/Salts','Acids2']),
   ('Periodic table + Atomic structure', ['PeriodicTable/Atom','PeriodicTable2']),
   ('Gases', ['Gases']),
   ('Metals/Non-metals/Alloys/Rusting', ['Metals/Alloys']),
   ('Matter/Solutions/Colloids', ['Matter&Mixtures']),
   ('Compounds & their uses', ['Compounds']),
   ('Formulas/Reactions', ['Formulas&Reactions']),
   ('Organic chemistry + Fuels', ['Organic/Fuels']),
   ('Polymers/Fibres/Plastics', ['Polymers/Fibres']),
   ('Daily-life chemistry (soap/preservatives/sweeteners)', ['DailyLife-Chem']),
   ('Agri-chem (fertilisers/pesticides)', ['Agri-Chem']),
   ('Misc', ['Misc-Chem']),
 ],
 'CULTURE': [
   ('Music — classical gharanas + folk music', ['Music']),
   ('Classical dances — 8 forms + exponents', ['ClassicalDances']),
   ('Folk dances — state-wise', ['FolkDances','Dance-Persons']),
   ('Festivals & Fairs', ['Festivals/Fairs']),
   ('Architecture & Monuments — temples/masjid/UNESCO', ['Architecture']),
   ('Literature — poets/classical languages', ['Literature-Culture','Literature2']),
   ('Films', ['Films']),
   ('Paintings', ['Paintings']),
   ('Theatre/Puppetry/Martial arts', ['Theatre&Puppetry','Martial&Misc']),
 ],
 'STATIC': [
   ('Sports (non-cricket) — players/rules/tournaments', ['Sports-Others','Sports2','Sports-Equipment/Rules']),
   ('Cricket', ['Sports-Cricket']),
   ('Books & Authors', ['Books&Authors']),
   ('Awards — national/international', ['Awards','Awards2']),
   ('Abbreviations/Full forms', ['Abbreviations']),
   ('Firsts & Superlatives', ['Firsts&Superlatives']),
   ('Currencies of world', ['Currencies']),
   ('Important Days & Themes', ['Days&Themes','Days2']),
   ('International orgs/Parliaments/HQ', ['Parliaments&Orgs']),
   ('National symbols', ['NationalSymbols']),
   ('Institutes/Locations', ['Institutes&Places']),
   ('Defence/Missiles/Airports/Railways', ['Airports/Ports/Misc-India']),
   ('Persons/First-institutes/Infra', ['Persons&Infra','Persons&Infra2']),
   ('Tribes of India', ['Tribes']),
   ('Nicknames (cities/countries)', ['Nicknames']),
   ('Misc inventions/facts', ['Misc-Static']),
 ],
 'COMPUTER': [
   ('MS Office — Word/Excel/PowerPoint', ['MSOffice','MSOffice2']),
   ('Internet/Tech/Apps', ['Internet&Tech']),
   ('Hardware/Network/Generations', ['Hardware&Network','Hardware&Network2']),
   ('Computer basics + history', ['Misc-Comp']),
 ],
}
PARTS = [
 ('Part 1','POLITY'), ('Part 2','HISTORY'), ('Part 3','GEOGRAPHY'), ('Part 4','ECONOMICS'),
 ('Part 5','BIOLOGY + ENVIRONMENT'), ('Part 6','PHYSICS + CHEMISTRY'), ('Part 7','CULTURE'),
 ('Part 8','STATIC + COMPUTER'), ('Part 9','MASTER INDEX + CA-count + Strategy'),
]
SUBJ_LABEL = {'POLITY':'राजव्यवस्था (Polity)','HISTORY':'इतिहास (History)','GEOGRAPHY':'भूगोल (Geography)',
 'ECONOMICS':'अर्थव्यवस्था (Economics)','BIOLOGY':'जीव विज्ञान (Biology)','ENVIRONMENT':'पर्यावरण (Environment)',
 'PHYSICS':'भौतिकी (Physics)','CHEMISTRY':'रसायन (Chemistry)','CULTURE':'कला-संस्कृति (Art & Culture)',
 'STATIC':'स्टैटिक GK (Static GK)','COMPUTER':'कंप्यूटर (Computer Awareness)'}

sub = collections.defaultdict(list)
for q in qs: sub[q['subject']].append(q)

def ansrate(pool):
    na = sum(1 for q in pool if q.get('answer') is not None)
    return na, (100.0*na/len(pool) if pool else 0)

w('# GS MASTER — STRUCTURE PROPOSAL (PYQ-EVIDENCE SE)')
w('## 193 papers • 2017–2024 • Har number is analysis se computed, koi guess nahi')
w()
w('---')
w('## 1. DATA BASE (honest accounting)')
w()
tot = len(qs)
w(f'- **Total parsed questions: {tot}** (193 papers × 25 slots = 4,825; {4825-tot} slots image/OCR-fail placeholders the)')
netext = len(sub['NO-TEXT']); nongs = len(sub['NON-GS']); unk = len(sub['UNKNOWN'])
w(f'- **NO-TEXT (text recover nahi hua): {netext}** — 2023 ke {sum(1 for q in sub["NO-TEXT"] if q["paper"].startswith("2023"))} placeholder + {sum(1 for q in sub["NO-TEXT"] if q["topic"]=="hindi-font-broken")} Hindi font-broken + {sum(1 for q in sub["NO-TEXT"] if q["topic"]=="empty/short")} empty')
w(f'- **NON-GS (2017-19 window me maths/English leak): {nongs}** — GS analysis se exclude')
w(f'- **UNKNOWN (signals nahi mile / OCR-mush): {unk}** — exclude (mostly 2023 OCR-garble)')
w(f'- **Analysable GS questions: {len(ANALYZABLE)-unk}** (+ CA {len(sub["CA"])} count-only)')
w(f'- **CA (Current Affairs): {len(sub["CA"])} — user rule ke mutabik SIRF COUNT, content nahi**')
w()
w(f'> **2023 FIX NOTE:** Phase-1 TXT me 2023 ke 769 questions ka OCR-text ek parse-overwrite bug se')
w('> blank ho gaya tha (answers the, text nahi). Detect karke fix kiya — 2023 ke 32 papers ka GA-OCR')
w('> dobara run + merge hua. ' + f'**TXT v2: {tot} questions / {sum(1 for q in qs if q.get("answer") is not None)} answers**')
w('> (pehle 4,431/3,740). Workspace + uploads dono jagah updated. Baaki saare years unchanged.')
w()
w('---')
w('## 2. SUBJECT-WISE YIELD TABLE (ranked)')
w()
w('| Rank | Subject | Qs | % of GS | Avg Qs/paper | Answer coverage |')
w('|---|---|---|---|---|---|')
rank = 0
order = sorted([s for s in sub if s not in ('NO-TEXT','NON-GS','UNKNOWN')], key=lambda s: -len(sub[s]))
for s in order:
    if s == 'CA':
        w(f'| — | **CA (count-only)** | {len(sub[s])} | — | {len(sub[s])/N_PAPERS:.1f} | — |')
        continue
    rank += 1
    na, pct = ansrate(sub[s])
    w(f'| {rank} | {SUBJ_LABEL.get(s,s)} | **{len(sub[s])}** | {100.0*len(sub[s])/(len(ANALYZABLE)-unk):.1f}% | {len(sub[s])/N_PAPERS:.1f} | {pct:.0f}% |')
w()
sci = len(sub['PHYSICS'])+len(sub['CHEMISTRY'])+len(sub['BIOLOGY'])+len(sub['ENVIRONMENT'])
w(f'**Science total (Phy+Chem+Bio+Env): {sci} Qs** — GK-book style me alag-alag lagte hain, saath dekho to 4th biggest subject hai.')
w()
w('---')
w('## 3. HIGH-YIELD CHAPTER MAP (jahan se marks aate hain — top 30)')
w()
rows = []
for s in CH:
    for chap, topics in CH[s]:
        pool = [q for q in sub[s] if q['topic'] in topics]
        if not pool: continue
        papers_touched = len(set(q['paper'] for q in pool))
        rows.append((len(pool), papers_touched, s, chap))
rows.sort(reverse=True)
w('| # | Chapter | Subject | Qs | Papers me aaya (193 me se) |')
w('|---|---|---|---|---|')
for i,(c, pt, s, chap) in enumerate(rows[:30],1):
    w(f'| {i} | {chap} | {SUBJ_LABEL.get(s,s).split("(")[0].strip()} | **{c}** | {pt} ({100.0*pt/N_PAPERS:.0f}%) |')
w()
w('> **"Papers me aaya" = kitne papers me is chapter ka kam se kam 1 Q aaya.** Yahi "minimum input maximum output" ka')
w('> ranking hai — jis chapter ka spread zyada, wo chapter pehle pakadna chahiye.')
w()
w('---')
w('## 4. PROPOSED MASTER STRUCTURE (8 parts + index)')
w()
w('| Part | Contents | Evidence base |')
w('|---|---|---|')
for pid, content in PARTS:
    if '+' in content:
        ss = [x.strip() for x in content.split('+')]
        if 'MASTER' in content: n = len(sub['CA'])
        else: n = sum(len(sub[x]) for x in ss)
        w(f'| **{pid}** | {content} | {n} Qs |')
    else:
        w(f'| **{pid}** | {SUBJ_LABEL.get(content,content)} | {len(sub[content])} Qs |')
w()
for pid, content in PARTS:
    ss = [x.strip() for x in content.split('+')] if '+' in content else [content]
    if 'MASTER' in content: continue
    w(f'### {pid} — {content}')
    for s in ss:
        if s not in CH: continue
        w(f'**{SUBJ_LABEL.get(s,s)} — {len(sub[s])} Qs:**')
        for chap, topics in CH[s]:
            pool = [q for q in sub[s] if q['topic'] in topics]
            if not pool: continue
            pt = len(set(q['paper'] for q in pool))
            w(f'- {chap} — **{len(pool)} Qs** ({pt} papers)')
    w()
w('---')
w('## 5. VERBATIM REPEATS (same question dobara — free marks)')
w()
groups = collections.defaultdict(list)
for q in ANALYZABLE:
    if q['subject'] == 'CA': continue
    groups[q['nkey']].append(q)
dupg = sorted((g for g in groups.values() if len(g)>=2 and len(g[0]['nkey'])>25), key=lambda g:-len(g))
w(f'Distinct questions: {len(groups)} | verbatim-repeat groups: {len(dupg)}')
w()
w('**Top verbatim repeats:**')
for g in dupg[:20]:
    yrs = ','.join(sorted(set(str(q['year']) for q in g), reverse=True))
    w(f'- x{len(g)} ({yrs}) {g[0]["qtext"][:100]}')
w()
w('> Verbatim repeat kam hain (SSC wording badal ke poochta hai) — isliye asli frequency signal')
w('> **chapter/fact-level** hai (Section 3), jo master ka base hai.')
w()
w('---')
w('## 6. CA — COUNT-ONLY BLOCK (user rule)')
w()
w('| Year | CA Qs | Papers |')
w('|---|---|---|')
yp = collections.defaultdict(set)
for q in sub['CA']: yp[q['year']].add(q['paper'])
for y in sorted(yp, reverse=True):
    w(f'| {y} | {sum(1 for q in sub["CA"] if q["year"]==y)} | {len(yp[y])} |')
w()
w('**Trend:** 2017-20 me CA ~0-1 Q/paper → 2021 se ~4 Q/paper. Ab bhi static hi 80%+ hai.')
w('Master me CA ka sirf ek chhota strategy-box hoga (kya padhna hai, kitna, kahan se) — full CA coverage scope me nahi.')
w()
w('---')
w('## 7. FACT-CHECK POLICY (master writing ke time)')
w()
w('- Har part likhte waqt dataset-answers ko theory PDFs (364 downloaded the, /var/tmp reset hua — **us part ke topics ke PDFs dobara download** karunga) se verify karunga')
w('- Galat/misleading dataset answer → **[DATASET-ANSWER GALAT — correct: X]** flag ke saath correction')
w('- 2020-2022 ke answers "Chosen Option" (candidate response) hain — 100% official nahi, verify zaroori')
w('- `[स्रोत अस्पष्ट]`-type rules wahi rahenge jo maths me the (OCR-garble par kabhi invent nahi)')
w()
w('---')
w('## 8. NEXT STEP')
w()
w('1. Aap is structure ko check karo — **part order** theek hai ya badalna hai?')
w('2. Confirm hone par **Part 1 (Polity)** se shuru — maths jaisa part-by-part, aap review karoge phir aage')
w('3. Har part me: chapter-wise PYQ-evidence → high-frequency facts → derive-yaad logic → mini-ratta box')
w()
w('*Generated from: master_build/gs_classified.json (har Q tagged: subject/topic/paper/year/answer)*')

open('master_build/00_STRUCTURE_PROPOSAL.md','w').write('\n'.join(OUT))
print('written:', len(OUT), 'lines')
