#!/usr/bin/env python3
"""Extract chapter-wise PYQ dump for a subject from gs_classified.json (for part-writing).
Usage: python3 extract_part_qs.py <subject> <outfile>   (e.g. POLITY master_build/part1_polity_qs.txt)"""
import json, collections, re, sys, os

CH = {
 'POLITY': {
  'Constitution': 'Constitution-making & Preamble',
  'Articles/FundamentalRights': 'Articles + FR + Writs',
  'Duties&DPSP': 'FD + DPSP',
  'Parliament': 'Parliament',
  'Executive-President/PM': 'Executive',
  'Judiciary': 'Judiciary',
  'Amendments&Emergency': 'Amendments + Emergency',
  'PanchayatiRaj': 'Panchayati Raj',
  'Bodies&Elections': 'Bodies + Elections',
  'Laws&Acts': 'Laws & Acts', 'Laws2': 'Laws & Acts',
  'UnionStructure': 'Union/Citizenship/Schedules', 'UnionStructure2': 'Union/Citizenship/Schedules',
  'Misc-Polity': 'Union/Citizenship/Schedules', 'Misc2': 'Union/Citizenship/Schedules',
 },
 'HISTORY': {
  'Ancient-Prehistory': 'Ancient — प्राचीन: पूर्व-इतिहास',
  'Ancient-IVC': 'Ancient — सिंधु सभ्यता',
  'Ancient-Vedic': 'Ancient — वैदिक काल',
  'Ancient-Buddhism/Jainism': 'Ancient — बौद्ध और जैन धर्म',
  'Ancient-Mauryan': 'Ancient — मौर्य काल',
  'Ancient-Gupta&Later': 'Ancient — गुप्त काल',
  'Ancient-PostGupta': 'Ancient — उत्तर-गुप्त काल',
  'Ancient-Misc2': 'Ancient — विविध', 'Ancient-Misc3': 'Ancient — विविध',
  'Medieval-Sultanate': 'Medieval — दिल्ली सल्तनत',
  'Medieval-Mughal': 'Medieval — मुगल काल',
  'Medieval-Maratha/Bhakti-Sufi': 'Medieval — मराठा/भक्ति-सूफी',
  'Medieval-Misc2': 'Medieval — विविध', 'Medieval-Misc3': 'Medieval — विविध',
  'Modern-BritishRule': 'Modern — ब्रिटिश शासन',
  'Modern-1857': 'Modern — 1857',
  'Modern-SocioReligious': 'Modern — सामाजिक-धार्मिक सुधार',
  'Modern-FreedomStruggle': 'Modern — स्वतंत्रता संग्राम',
  'Modern-Organizations': 'Modern — संगठन',
  'Modern-Misc2': 'Modern — विविध', 'Modern-Misc3': 'Modern — विविध',
  'World-Misc': 'World — विश्व इतिहास', 'World-Revolution': 'World — विश्व इतिहास', 'World-Wars&After': 'World — विश्ह इतिहास',
 },
 'GEOGRAPHY': {
  'EarthBasics': 'भौतिक भूगोल — पृथ्वी', 'EarthBasics2': 'भौतिक भूगोल — पृथ्वी', 'EarthBasics3': 'भौतिक भूगोल — पृथ्वी',
  'SolarSystem': 'सौरमंडल',
  'Astronomy': 'खगोल — तारामंडल', 'Astronomy2': 'खगोल — तारामंडल',
  'Mountains/Passes': 'पर्वत और दर्रे', 'Mountains2': 'पर्वत और दर्रे',
  'Plains&Landforms': 'मैदान और भू-आकृतियाँ',
  'Rivers': 'नदियाँ',
  'Lakes/Waterfalls': 'झीलें और जलप्रपात',
  'Climate': 'जलवायु',
  'Soils': 'मृदा (सॉइल)',
  'Agriculture-Geo': 'कृषि भूगोल',
  'Minerals&Industry': 'खनिज और उद्योग',
  'Energy&Industry': 'ऊर्जा',
  'Transport/Highways': 'परिवहन और राजमार्ग',
  'Dams&Projects': 'बाँध और परियोजनाएँ',
  'Population': 'जनसंख्या',
  'Oceanography': 'महासागर',
  'States&Boundaries': 'राज्य — पहचान और सीमाएँ',
  'World-Geo': 'विश्व भूगोल', 'World-Misc2': 'विश्व भूगोल',
 },
 'SCIENCE': {
  # PHYSICS
  'Motion&Force': 'भौतिक — गति, बल और मशीनें',
  'Work/Energy/Machines': 'भौतिक — गति, बल और मशीनें',
  'Units&Measurement': 'भौतिक — इकाइयाँ और मापन', 'Units2': 'भौतिक — इकाइयाँ और मापन',
  'Pressure/Fluids': 'भौतिक — दाब और तरल',
  'Heat': 'भौतिक — ऊष्मा', 'Heat2': 'भौतिक — ऊष्मा',
  'Optics': 'भौतिक — प्रकाश',
  'Waves': 'भौतिक — तरंगें और ध्वनि', 'Sound': 'भौतिक — तरंगें और ध्वनि',
  'Electricity/Magnetism': 'भौतिक — विद्युत और चुंबकत्व', 'Electricity2': 'भौतिक — विद्युत और चुंबकत्व',
  'ModernPhysics': 'भौतिक — आधुनिक भौतिकी', 'ModernPhysics2': 'भौतिक — आधुनिक भौतिकी',
  'DailyLife-Phy': 'भौतिक — दैनिक जीवन की भौतिकी', 'Misc-Phy': 'भौतिक — दैनिक जीवन की भौतिकी',
  # CHEMISTRY
  'PeriodicTable/Atom': 'रसायन — परमाणु और आवर्त सारणी', 'PeriodicTable2': 'रसायन — परमाणु और आवर्त सारणी',
  'Matter&Mixtures': 'रसायन — पदार्थ, मिश्रण और विलयन',
  'Acids/Bases/Salts': 'रसायन — अम्ल, क्षार और लवण', 'Acids2': 'रसायन — अम्ल, क्षार और लवण',
  'Gases': 'रसायन — गैसें',
  'Metals/Alloys': 'रसायन — धातु, अधातु और मिश्रधातुएँ',
  'Compounds': 'रसायन — महत्वपूर्ण यौगिक',
  'Formulas&Reactions': 'रसायन — सूत्र और अभिक्रियाएँ',
  'Polymers/Fibres': 'रसायन — बहुलक और तंतु',
  'Organic/Fuels': 'रसायन — कार्बन और ईंधन',
  'Agri-Chem': 'रसायन — कृषि-रसायन', 'Misc-Chem': 'रसायन — कृषि-रसायन',
  'DailyLife-Chem': 'रसायन — दैनिक जीवन का रसायन',
  # BIOLOGY
  'Cell&Genetics': 'जीव — कोशिका और आनुवंशिकी', 'Cell&Genetics2': 'जीव — कोशिका और आनुवंशिकी',
  'Plants': 'जीव — पादप जीव विज्ञान',
  'Body-Facts': 'जीव — मानव शरीर: संरचना और वर्गीकरण',
  'Digestion': 'जीव — पाचन तंत्र',
  'Circulation': 'जीव — रक्त और संचारण',
  'Respiration/Excretion': 'जीव — श्वसन और उत्सर्जन',
  'Skeleton/Muscles': 'जीव — कंकाल और मांसपेशियाँ',
  'Nervous/Hormones': 'जीव — तंत्रिका और हार्मोन',
  'Nutrition/Deficiency': 'जीव — पोषण और विटामिन',
  'Disease&Immunity': 'जीव — रोग और प्रतिरक्षा', 'Disease&Immunity2': 'जीव — रोग और प्रतिरक्षा',
  'Classification': 'जीव — जैव वर्गीकरण', 'AnimalHusbandry': 'जीव — जैव वर्गीकरण',
  # ENVIRONMENT
  'Parks&Sanctuaries': 'पर्यावरण — उद्यान और अभयारण्य',
  'Wetlands&Acts': 'पर्यावरण — आर्द्रभूमि और अधिनियम',
  'Biodiversity/Ecosystem': 'पर्यावरण — जैव विविधता और पारितंत्र',
  'Species&IUCN': 'पर्यावरण — प्रजातियाँ और IUCN',
  'ClimateChange/Ozone': 'पर्यावरण — जलवायु परिवर्तन और ओज़ोन',
  'Pollution': 'पर्यावरण — प्रदूषण',
 },
 'ECONOMICS': {
  'RBI&Monetary': 'RBI और मौद्रिक नीति',
  'Markets-Cost': 'बाजार — माँग, पूर्ति, लागत',
  'NationalIncome': 'राष्ट्रीय आय',
  'Planning': 'नियोजन',
  'Markets&Trade': 'बाजार और व्यापार',
  'Money&Banking': 'मुद्रा और बैंकिंग', 'Money&Banking2': 'मुद्रा और बैंकिंग',
  'Budget&Tax': 'बजट और कर',
  'Misc-Eco': 'विविध अर्थ',
  'Poverty&Employment': 'निर्धनता और रोज़गार',
  'Schemes': 'योजनाएँ',
  'Institutions': 'संस्थाएँ',
  'Reforms&Industry': 'सुधार और उद्योग',
  'Agriculture-Eco': 'कृषि अर्थ',
  'Sectors': 'क्षेत्र',
  'Inflation': 'मुद्रा स्फीति',
 },
}

GROUPS = {'SCIENCE': ['BIOLOGY', 'CHEMISTRY', 'PHYSICS', 'ENVIRONMENT']}

def main(subject, outfile):
    qs = json.load(open('master_build/gs_classified.json'))
    chmap = CH[subject]
    subs = GROUPS.get(subject, [subject])
    pol = [q for q in qs if q['subject'] in subs]
    def shift(q):
        m = re.search(r'Shift\s*-\s*(\d+)', q.get('pname') or '')
        return f"S{m.group(1)}" if m else ''
    byc = collections.defaultdict(list)
    for q in pol: byc[chmap.get(q['topic'], q['topic'])].append(q)
    out = [f'{subject} PYQs — {len(pol)} questions, chapter-wise (for part writing)', '='*90]
    for chap in sorted(byc, key=lambda c: -len(byc[c])):
        out.append(''); out.append(f'###### {chap} — {len(byc[chap])} Qs')
        for q in sorted(byc[chap], key=lambda q: (-q['year'], q['paper'])):
            qt = re.sub(r'^\s*Q\s*\.?\s*\d{1,3}[\.\):)_]?\s*', '', (q['qtext'] or '')).strip()
            opts = q.get('options') or {}
            o = ' | '.join(f"{k}){str(v)[:40]}" for k, v in opts.items() if str(v).strip())
            a = q.get('answer'); at = ''
            if a is not None and str(a) in opts and str(opts[str(a)]).strip():
                at = f" => ANS({a}): {str(opts[str(a)])[:60]}"
            elif a is not None:
                at = f" => ANS: ({a})"
            tag = f"[{q['year']}{('-' + shift(q)) if shift(q) else ''}|{q['paper']}]"
            out.append(f"{tag} {qt[:260]}")
            if o: out.append(f"    {o[:320]}{at}")
    open(outfile, 'w').write('\n'.join(out))
    print(f'{outfile}: {len(pol)} Qs, {len(byc)} chapters')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
