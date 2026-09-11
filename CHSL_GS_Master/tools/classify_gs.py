#!/usr/bin/env python3
"""Phase-2: Classify all GS PYQs (193 papers) into subject/topic + frequency analysis.
Purpose: derive the GS Master structure purely from PYQ evidence (user rule).
Input: root dir containing gs_parsed/, ocr_raw/, b_data.json
Output: <outroot>/gs_classified.json + <outroot>/classification_report.txt
"""
import os, sys, json, re, collections, random

# ---------------- normalization ----------------
SUBJ_ORDER = ['HISTORY','POLITY','ECONOMICS','GEOGRAPHY','ENVIRONMENT','BIOLOGY','CHEMISTRY','PHYSICS','CULTURE','STATIC','COMPUTER']

def norm(t):
    if not t: return ''
    t = str(t).lower()
    t = t.replace("'", '').replace('\u2019', '').replace('\u2013',' ').replace('\u2014',' ').replace('-',' ').replace('/',' ')
    t = re.sub(r'[^\w\s]', ' ', t)          # drop punctuation (keep word chars)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def strip_qnum(t):
    return re.sub(r'^\s*q\s*\d{1,3}\s*', '', t).strip()

# ---------------- signal tables ----------------
SIG = []

def add(subject, topic, phrases, w):
    for ph in phrases:
        ph = ph.strip().lower().replace('-', ' ')
        if not ph: continue
        rx = re.compile(r'(?<![a-z])' + re.escape(ph) + r'(?:s|es|ed|d|ing|ly)?(?![a-z])')
        SIG.append((subject, topic, rx, w))
        if len(ph) > 3 and ph.endswith('y') and ph[-2] not in 'aeiou':
            rx2 = re.compile(r'(?<![a-z])' + re.escape(ph[:-1]) + r'(?:y|ies)(?:s|es|ed|d|ing|ly)?(?![a-z])')
            SIG.append((subject, topic, rx2, w))

# ================= HISTORY =================
add('HISTORY','Ancient-IVC',['harappan','mohenjodaro','mohenjo daro','lothal','dholavira','kalibangan','chanhudaro','indus valley civilisation','indus valley civilization'],7)
add('HISTORY','Ancient-Vedic',['vedic period','vedic age','rig veda','samaveda','yajurveda','atharvaveda','upanishad','brahmana book','aryan'],6)
add('HISTORY','Ancient-Buddhism/Jainism',['buddha','buddhism','mahavira','jainism','nirvana','tripitaka','tirthankara',' bodh gaya','sarnath','kusinara','lumbini','four noble truth','eightfold path','ahimsa jain','monastery'],7)
add('HISTORY','Ancient-Mauryan',['maurya','ashoka','chandragupta maurya','bindusara','kalinga war','dhamma','edict','megasthenes','indika','arthashastra','kautilya','chanakya'],7)
add('HISTORY','Ancient-Gupta&Later',['gupta','samudragupta','chandragupta ii','skandagupta','fa hien','hiuen tsang','harshavardhana','harsha','banabhatta','harshacharita','nalanda','taxila','vikramshila','kanishka','kushan','satavahana','sangam age','sangam literature','pallava','chola empire','rajaraja','rajendra chola','golden age'],6)
add('HISTORY','Ancient-PostGupta',['pala','palas','pratihara','rashtrakuta','tripartite struggle','kannauj','chauhan','tomara','chahamana','gahadavala','sen dynasty','sena dynasty','pandya','chera','inscription','chola emperor'],6)
add('HISTORY','Medieval-Rajput/Misc',['bijolia','chittor fort','mewar','paramara','chandela','gehlot'],5)
add('HISTORY','Medieval-Sultanate',['delhi sultanate','iltutmish','razia sultana','razia','qutub ud din','qutb ud din','balban','alauddin khilji','khilji','jalal ud din','tughlaq','muhammad bin tughlaq','firoz shah tughlaq','firoz tughlaq','lodhi dynasty','sayyid dynasty','sayyid ruler','khizr khan','muhammad ghori','prithviraj chauhan','battle of tarain','tarain'],7)
add('HISTORY','Medieval-Mughal',['mughal','babur','humayun','akbar','jahangir','shah jahan','aurangzeb','sher shah','sur dynasty','battle of panipat','panipat','battle of khanwa','khanwa','battle of chausa','chausa','rana pratap','maharana pratap','haldighati','mansabdari','jagirdari','din i ilahi','sulh i kul','ibadat khana','tansen','todar mal','baburnama','akbarnama','tuzuk i jahangiri','jizya','guru tegh bahadur','guru nanak','gobind singh','khalsa'],7)
add('HISTORY','Medieval-Maratha/Bhakti-Sufi',['maratha','shivaji','sambhaji','peshwa','bajirao','vijayanagara','vijayanagar','krishnadevaraya','bahmani','hampi','bhakti movement','sufi','sufism','kabir','meera bai','chaitanya','namdev','surdas','tulsidas','dadu dayal'],7)
add('HISTORY','Modern-BritishRule',['battle of plassey','plassey','battle of buxar','buxar','robert clive','east india company','anglo mysore','tipu sultan','tipu','anglo maratha','anglo sikh','subsidiary alliance','doctrine of lapse','permanent settlement','ryotwari','mahalwari','cornwallis','wellesley','bentinck','dalhousie','ripon','curzon','regulating act','pitts india act','charter act','act of 1919','act of 1935','minto morley','morley minto'],7)
add('HISTORY','Modern-1857',['revolt of 1857','mutiny','sepoy','first war of independence','mangal pandey','nana saheb','tantia tope','lakshmi bai','kunwar singh','begum hazrat mahal','jhansi'],7)
add('HISTORY','Modern-FreedomStruggle',['indian national congress','congress session','a o hume','dadabhai','gandhi','gandhian','mahatma','champaran','kheda','non cooperation','chauri chaura','civil disobedience','dandi','salt march','salt satyagraha','poona pact','round table','gandhi irwin','quit india','august kranti','jallianwala','rowlatt','simon commission','nehru report','purna swaraj','lahore session','karachi session','haripura','tripuri','cripps mission','cabinet mission','wavel plan','mountbatten','indian independence act','interim government','swadeshi','partition of bengal','surat split','lucknow pact','home rule','annie besant','bal gangadhar','tilak','gokhale','naoroji','khilafat','revolutionary','bhagat singh','chandrashekhar azad','rajguru','sukhdev','kakori','hsra','ashfaqullah','subhas chandra bose','netaji','forward bloc',' azad hind','sarojini naidu','swaraj party'],7)
add('HISTORY','Modern-Organizations',['ghadar party','bombay presidency association','servants of india','rss founded','jamiat','muslim league founded'],7)
add('HISTORY','Modern-SocioReligious',['swami vivekananda','ramakrishna','aryasamaj','arya samaj','dayanand','brahmo samaj','rammohan roy','ram mohan roy','prarthana samaj','satyashodhak','jyotiba phule','savitribai','theosophical society','aligarh movement','sir syed ahmed','deoband'],7)
add('HISTORY','World-Revolution',['french revolution','napoleon','bastille','voltaire','rousseau','montesquieu','louis xvi','reign of terror','robespierre','russian revolution','lenin','bolshevik','karl marx','stalin','trotsky','october revolution','february revolution'],7)
add('HISTORY','World-Wars&After',['world war','first world war','second world war','wwi','wwii','allied powers','axis powers','hitler','nazi','mussolini','pearl harbour','pearl harbor','hiroshima','nagasaki','league of nations','cold war','great depression','new deal','roosevelt','united nations organisation'],7)
add('HISTORY','World-Misc',['renaissance','reformation','martin luther','printing press','gutenberg','industrial revolution','american revolution','boston tea','george washington','abraham lincoln','cleopatra','julius caesar','roman empire','ancient greek','athens','sparta','crusade','byzantine','ottoman empire','constantinople','discovered america','discovered the sea route',' discovered sea route'],7)
add('HISTORY','Medieval-Misc2',['parrot of india','mahmud','ghazni','ghaznavi','jayapal','battle of peshawar'],7)
add('HISTORY','Ancient-Misc2',['kalinga'],6)
add('HISTORY','Modern-Misc2',['bardoli','depressed classes','communal award','reserved seats in the legislative','legislative council','conversion to christianity','religious conversion'],6)

# ================= POLITY =================
add('POLITY','Constitution',['constitution of india','constitution drafting','constituent assembly','drafting committee','ambedkar','preamble','sovereign socialist','republic of india'],7)
add('POLITY','Articles/FundamentalRights',['which article','what article','under article','under the article','of article','of the article','article of the constitution','article in the constitution','articles of the constitution','article 1','article 2','article 3','article 4','fundamental rights','right to equality','right to freedom','right against exploitation','right to constitutional remedies','cultural and educational rights','writ','habeas corpus','mandamus','certiorari','quo warranto','article 21','article 14','article 32','article 19','article 368','article 356','article 370'],6)
add('POLITY','Duties&DPSP',['fundamental duties','directive principles','directive principle'],7)
add('POLITY','Executive-President/PM',['president of india','vice president of india','prime minister of india','council of ministers','cabinet','ordinance','impeachment','pardon','mercy petition','veto','pocket veto','attorney general of india','governor of state','chief minister of a state','chief minister of state','state legislature'],6)
add('POLITY','Parliament',['lok sabha','rajya sabha','parliament','speaker of lok sabha','money bill','joint sitting','quorum','question hour','zero hour','no confidence motion','session of parliament','union legislature','budget session'],6)
add('POLITY','Judiciary',['supreme court','high court','chief justice','judicial review','public interest litigation','integrated judiciary','single integrated judiciary','writ jurisdiction'],6)
add('POLITY','Bodies&Elections',['election commission','universal adult franchise','voter','election commissioner','finance commission','comptroller and auditor','cag','public service commission','upsc','statutory body','constitutional body','national commission','delimitation'],6)
add('POLITY','PanchayatiRaj',['panchayati raj','panchayat','municipality','73rd amendment','74th amendment','local self government','local government','zila parishad','gram sabha','gram panchayat'],7)
add('POLITY','Amendments&Emergency',['amendment','42nd amendment','44th amendment','61st amendment','24th amendment','kesavananda','basic structure','emergency','president rule','presidents rule','financial emergency'],6)
add('POLITY','UnionStructure',['concurrent list','state list','union list','seventh schedule','residuary power','centre and state','federal structure','union of states','citizenship','single citizenship','official language','eighth schedule','scheduled caste','scheduled tribe','reservation'],5)
add('POLITY','Laws&Acts',['indian penal code','ipc','crpc','criminal procedure','representation of the people','rpa act','section of the indian penal','national human rights commission','nhrc','human rights commission','law commission','statute','act of parliament','act was passed by the parliament','act came into force','bill was passed','uidai','aadhaar','meity','special marriage act','marriage act','electoral bond','act was enacted','assembly','vidhan sabha','legislative assembly'],5)
add('POLITY','UnionStructure2',['citizen of india','qualifications for','eligibility for the office','should be a citizen'],4)
add('POLITY','Misc-Polity',['constitution','republic','democracy','parliamentary system','presidential system','unitary'],4)

# ================= ECONOMICS =================
add('ECONOMICS','NationalIncome',['gdp','gnp','ndp','national income','per capita income','gdp deflator','real gdp','nominal gdp','base year'],7)
add('ECONOMICS','Inflation',['inflation','deflation','cpi','wpi','price index','dear money','cheap money','purchasing power','index number'],6)
add('ECONOMICS','RBI&Monetary',['repo rate','reverse repo','bank rate','cash reserve ratio','crr','statutory liquidity','slr','marginal standing facility','monetary policy','mpc','open market operation','reserve bank','rbi','governor of rbi'],7)
add('ECONOMICS','Budget&Tax',['budget','union budget','annual financial statement','fiscal deficit','revenue deficit','primary deficit','direct tax','indirect tax','gst','customs duty','excise duty','service tax','progressive tax','regressive tax','fiscal policy','finance minister'],6)
add('ECONOMICS','Planning',['five year plan','five yearly plan','planning commission','niti aayog','plan holiday'],7)
add('ECONOMICS','Poverty&Employment',['poverty line','below poverty','bpl','poverty estimation','tendulkar committee','mgnrega','unemployment','employment scheme','jobless growth'],6)
add('ECONOMICS','Institutions',['imf','international monetary fund','world bank','wto','gatt','sebi','nabard','sidbi','asian development bank','new development bank','aiib'],7)
add('ECONOMICS','Money&Banking',['money supply','fiat money','legal tender','demonetisation','demonetization','narrow money','broad money','demand deposit','commercial bank','public sector bank','nationalisation of bank','nationalization of bank','cheque','mutual fund','stock exchange','ipo','securities','bond market','insurance','irda','lending rate','banking'],5)
add('ECONOMICS','Agriculture-Eco',['green revolution','white revolution','blue revolution','yellow revolution','golden revolution','minimum support price','msp','food corporation','public distribution system','buffer stock','subsidy'],6)
add('ECONOMICS','Markets&Trade',['quantity demanded','point elasticity','elasticity of demand','law of demand','opportunity cost','production possibility','marginal utility','consumer surplus','perfect competition','monopoly','oligopoly','demand and supply','supply curve','export','import','trade deficit','balance of payment','foreign direct investment','fdi','special economic zone','sez','world trade'],5)
add('ECONOMICS','Reforms&Industry',['liberalisation','liberalization','privatisation','privatization','globalisation','globalization','economic reform','disinvestment','small scale industry','cottage industry','msme','industrial policy'],6)
add('ECONOMICS','Schemes',['antyodaya','deendayal','ayushman','ujjwala','jan dhan','mudra','stand up india','startup india','make in india','skill india','swachh bharat','amrut scheme','atal pension','jeevan jyoti','suraksha bima','krishi sinchayi','fasal bima','saubhagya','pmay','gramin yojana','yojana','scheme was launched','scheme of the government','programme was started','pm poshan','poshan abhiyan','beti bachao'],6)
add('ECONOMICS','Markets-Cost',['market equilibrium','excess supply','excess demand','cost theory','fixed cost','variable cost','average cost','marginal cost','total revenue','public goods','proportional tax','price ceiling','price floor','giffen good','inferior good','normal good','substitute good','complementary good','microfinance','micro finance','microfinance founder','grameen bank','financial year','refinance agency','competitive market structure','nationalisation of air transport','air transport','inventories','demand curve','aggregate demand','aggregate supply','ex ante','ex post','production function','labour and capital','private income','treasury bill','bankruptcy','insolvent','pay off debts','perfectly competitive','savings and credit','rotating savings','employment generation programme','pmegp','one stop centre'],5)
add('ECONOMICS','Misc-Eco',['economy','economics','microeconomics','macroeconomics','barter','capitalism','socialist economy','mixed economy','gdp growth'],4)

# ================= GEOGRAPHY =================
add('GEOGRAPHY','Rivers',['river','ganga','ganges','godavari','kaveri','krishna river','narmada','tapi','tapti','mahanadi','damodar','sutlej','beas','chenab','jhelum','indus','yamuna','ghaghara','gandak','kosi','teesta','luni','sabarmati','mahi','tungabhadra','periyar','subarnarekha','brahmaputra','confluence','tributary','distributary','bank of the river','riverbank','longest river','delta'],5)
add('GEOGRAPHY','Mountains/Passes',['mountain','himalaya','himadri','shiwalik','shivalik','karakoram','aravalli','vindhya','satpura','nilgiri','cardamom hills','purvanchal','ghat','pass in','zoji la','shipki la','nathu la','palghat','thal ghat','bhor ghat','kanchenjunga','peak','summit of mount','mount everest'],5)
add('GEOGRAPHY','Climate',['monsoon','cyclone','rainfall','climate','drought','el nino','la nina','jet stream','bay of bengal','arabian sea','indian ocean','mawsynram','cherrapunji','stratosphere','troposphere','atmospheric layer','layer of the atmosphere'],6)
add('GEOGRAPHY','Soils',['soil','alluvial','black soil','red soil','laterite','regur','loamy'],6)
add('GEOGRAPHY','Lakes/Waterfalls',['lake','wular','dal lake','chilika','pulicat','sambhar lake','lonar','vembanad','waterfall','jog falls','kunchikal','dudhsagar','niagara'],5)
add('GEOGRAPHY','States&Boundaries',['indian state','states of india','capital of','coastline','border of india','shares boundary','neighbouring country','international boundary','line of control','radcliffe line','durand line','mcmahon line','northernmost','southernmost','easternmost','westernmost','statehood','language of the state','sino indian','extent of india','jharkhand','chhattisgarh','madhya pradesh','uttar pradesh','himachal','rajasthan','gujarat','maharashtra','karnataka','kerala','tamil nadu','andhra pradesh','arunachal','assam','odisha','west bengal','punjab','haryana','bihar','uttarakhand','sikkim','meghalaya','manipur','mizoram','nagaland','tripura','goa state','delhi','jammu','border'],3)
add('GEOGRAPHY','Transport/Highways',['national highway','golden quadrilateral','expressway','railway','north east frontier','port'],5)
add('GEOGRAPHY','Dams&Projects',['dam','bhakra','hirakud','sardar sarovar','tehri','nagarjuna sagar','multipurpose project','river valley project','hydel','irrigation canal'],5)
add('GEOGRAPHY','Minerals&Industry',['mineral','coal field','iron ore','bauxite','mica','petroleum reserve','mining','cotton textile','sugar industry','steel plant'],5)
add('GEOGRAPHY','Agriculture-Geo',['crop','kharif','rabi','zaid','leading producer','largest producer of rice','largest producer of wheat','largest producer of cotton','tea producing','coffee producing','jute','cultivation','cropping season','agriculture','farming'],5)
add('GEOGRAPHY','EarthBasics',['earthquake','seismic','richter','volcano','volcanic','tsunami','ring of fire','plate tectonic','continental drift','igneous','sedimentary','metamorphic','weathering','erosion landform','landform','longitude','latitude','equator','international date line','greenwich','ist','coriolis','equinox','solstice','tropic of cancer','tropic of capricorn'],5)
add('GEOGRAPHY','Oceanography',['ocean current','gulf stream','tide','spring tide','neap tide','salinity','mariana trench','deepest ocean','largest ocean','smallest ocean','ocean floor','sea mount','abyssal'],6)
add('GEOGRAPHY','World-Geo',['continent','africa','europe','south america','antarctica','north america','australia','island','peninsula','strait','isthmus','gulf of','sea is the','country','capital city','desert','sahara','gobi','grassland','savanna','steppe','prairie','pampas','veld','downs grassland','tundra','taiga'],4)
add('GEOGRAPHY','SolarSystem',['solar system','planet','mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto','asteroid','meteor','comet','galaxy','milky way','eclipse','solar eclipse','lunar eclipse','moon','sunlight reach','light from the sun','nearest star','closest planet','largest planet','smallest planet','aryabhata','sputnik','satellite launch','isro','pslv','gslv'],5)
add('GEOGRAPHY','Population',['census','population of india','literacy rate','sex ratio','density of population','most populous','demographic','population growth','death rate','birth rate','life expectancy'],5)
add('GEOGRAPHY','EarthBasics2',['time zone','deposits','groundnut','hills','purvachal'],4)
add('GEOGRAPHY','Plains&Landforms',['northern plains','coastal plain','coastal plains','peninsular plateau','geoid','bhabar','terai','bhangar','khadar','doab','canal system','canal','deccan trap','thar desert','indian desert','physical division of india','islands of india','andaman','nicobar','lakshadweep'],5)
add('GEOGRAPHY','Energy&Industry',['nuclear power plant','thermal power','power plant','refinery','oil refinery','steel plant','cotton textile industry','sugar industry','iron and steel industry','textile industry','photovoltaic','oil india'],5)
add('GEOGRAPHY','Astronomy',['constellation','asterism','big dipper','northern sky','southern sky','apogee','perigee','orbit of','orbiting the earth','orbiting the sun','pole star','andromeda','orion','cassiopeia','cygnus','star formation','light year away','nearest galaxy','artificial satellite','space mission','spacecraft','space station'],5)

# ================= ENVIRONMENT =================
add('ENVIRONMENT','Parks&Sanctuaries',['national park','wildlife sanctuary','bird sanctuary','tiger reserve','biosphere reserve','conservation reserve','kaziranga','ranthambore','kanha','bandipur','jim corbett','sundarban','manas national','keoladeo','dachigam','hemis','silent valley','valley of flowers','khangchendzonga','nilgiri biosphere','simlipal','bhitarkanika','gir forest','gir national','periyar sanctuary'],7)
add('ENVIRONMENT','Species&IUCN',['endangered','endemic','vulnerable species','iucn','red data book','red list','critically endangered','extinct species','wildlife protection act','project tiger','project elephant','tiger census','vulture','snow leopard','one horned','great indian bustard'],6)
add('ENVIRONMENT','Biodiversity/Ecosystem',['biodiversity','biodiversity hotspot','megadiverse','ecosystem','ecology','food chain','food web','trophic','decomposer','ecological pyramid','biotic','abiotic','biomagnification','bioaccumulation','symbiosis','mutualism','parasitism','commensalism'],6)
add('ENVIRONMENT','Pollution',['pollution','pollutant','smog','acid rain','eutrophication','algal bloom','oil spill','plastic waste','e waste','biomedical waste','noise pollution','water pollution','air quality','aqi','bharat stage','catalytic converter','effluent'],6)
add('ENVIRONMENT','ClimateChange/Ozone',['global warming','greenhouse effect','greenhouse gas','climate change','ozone layer','ozone depletion','cfc','montreal protocol','kyoto protocol','paris agreement','unfccc','ipcc','carbon footprint','carbon credit','net zero'],7)
add('ENVIRONMENT','Wetlands&Acts',['ramsar','wetland','national green tribunal','ngt','central pollution control','forest conservation act','environment protection act','forest policy','mangrove','coral reef','coral bleaching','forest','potable water','water treatment','purification of water'],5)

# ================= BIOLOGY =================
add('BIOLOGY','Circulation',['heart','cardiac','blood','plasma','platelet','haemoglobin','hemoglobin','wbc','rbc','blood group','blood pressure','artery','vein','capillary','pulse rate','circulation of blood'],6)
add('BIOLOGY','Respiration/Excretion',['lung','pulmonary','respiration','breathing','alveoli','trachea','diaphragm breathing','kidney','nephron','urine','excretion','dialysis','liver','bile','jaundice'],6)
add('BIOLOGY','Digestion',['digestion','digestive','enzyme','saliva','gastric','intestine','villi','peristalsis','appendix'],6)
add('BIOLOGY','Nervous/Hormones',['brain','cerebrum','cerebellum','medulla','nervous system','neuron','nerve','spinal cord','reflex action','hormone','endocrine','insulin','thyroid','thyroxine','adrenal','pituitary','testosterone','oestrogen','estrogen','adrenaline','diabetes'],6)
add('BIOLOGY','Skeleton/Muscles',['bone','skeleton','skull','vertebra','rib cage','bone marrow','cartilage','muscle','tendon','ligament','largest bone','smallest bone','stapes','femur'],6)
add('BIOLOGY','Cell&Genetics',['cell','cell membrane','cell wall','nucleus','mitochondria','ribosome','lysosome','golgi','endoplasmic','organelle','prokaryotic','eukaryotic','mitosis','meiosis','cell division','chromosome','dna','rna','gene','genetic','heredity','mendel','dna fingerprinting','double helix','watson and crick','largest organelle','powerhouse of the cell'],6)
add('BIOLOGY','Plants',['photosynthesis','chlorophyll','chloroplast','stomata','transpiration','xylem','phloem','pollination','germination','gymnosperm','angiosperm','monocot','dicot','plant hormone','auxin','plant tissue','bryophyte','pteridophyte','algae','fungi','bacteria','virus','protozoa','microorganism','yeast','mushroom','lichen','botany','root','stem','leaf','flower','seed','fruit','plant','plants kingdom','guttation','loss of water from leaves','honey bee','bees','insect','entomology','moss','liverwort','hornwort'],5)
add('BIOLOGY','Nutrition/Deficiency',['vitamin','protein','carbohydrate','fat nutrient','mineral nutrient','nutrient','deficiency disease','scurvy','rickets','beriberi','night blindness','goitre','goiter','kwashiorkor','marasmus','anaemia','anemia','balanced diet','roughage','iodised salt','deficiency of'],6)
add('BIOLOGY','Disease&Immunity',['disease','malaria','dengue','chikungunya','tuberculosis','cholera','typhoid','plague','hepatitis','cancer','aids','hiv','ebola','vaccine','vaccination','antibiotic','penicillin','pathogen','immunity','immunisation','immunization','serum','antigen','antibody','blood circulation discovered','william harvey'],6)
add('BIOLOGY','Classification',['taxonomy','binomial nomenclature','linnaeus','five kingdom','whittaker','monera','protista','plantae','animalia','mammal','reptile','amphibian','aves','pisces','invertebrate','arthropod','mollusc','echinoderm','annelid','nematode','platyhelminthes','porifera','coelenterata','warm blooded','cold blooded','egg laying mammal','marsupial','flightless bird','migratory bird','zoology'],6)
add('BIOLOGY','AnimalHusbandry',['animal husbandry','poultry','dairy','fisheries','apiculture','sericulture','pisciculture','hybridisation of crop','hybridization of crop','biofertilizer','bio fertiliser','bio fertiliser'],6)
add('BIOLOGY','Body-Facts',['largest gland','smallest gland','largest organ','smallest organ','human body','body fluid','saliva produced','taste bud','human eye','ear drum','skin','spinal column','animals','animal','phylum','annelida','bmi','body mass index'],5)

# ================= CHEMISTRY =================
add('CHEMISTRY','Acids/Bases/Salts',['acid','ph value','ph scale','litmus','alkali','base','neutralisation','neutralization','common salt','sodium chloride','baking soda','sodium bicarbonate','washing soda','bleaching powder','plaster of paris','quicklime','quick lime','slaked lime','lime water','caustic soda','sodium carbonate'],6)
add('CHEMISTRY','Formulas&Reactions',['chemical formula','chemical name','chemical reaction','chemical equation','chemical change','chemical property','catalyst','catalytic','oxidation','reduction','redox','combustion','electrolysis','exothermic','endothermic','chemical equilibrium'],6)
add('CHEMISTRY','Gases',['oxygen','nitrogen','hydrogen','carbon dioxide','carbon monoxide','helium','neon','argon','chlorine','inert gas','noble gas','laughing gas','tear gas','mustard gas','producer gas','water gas','marsh gas','gas'],4)
add('CHEMISTRY','Metals/Alloys',['metal','alloy','brass','bronze','steel','stainless','solder','duralumin','german silver','rusting','rust of iron','galvanis','galvaniz','electroplating','anodising','anodizing','non metal'],6)
add('CHEMISTRY','PeriodicTable/Atom',['periodic table','mendeleev','moseley','atomic number','atomic mass','atomic weight','lanthanide','actinide','halogen','electron','proton','neutron','nucleus of atom','cathode ray','jj thomson','rutherford','millikan','isotope','isotopes of','deuterium','tritium','heavy water','uranium','thorium','plutonium','radioactive'],5)
add('CHEMISTRY','Organic/Fuels',['hydrocarbon','alkane','alkene','alkyne','benzene','petroleum refining','fractional distillation','coal gas','coke','coal tar','liquified petroleum','lpg','cng','compressed natural','natural gas','petrol','diesel','kerosene','fuel'],5)
add('CHEMISTRY','Polymers/Fibres',['polymer','plastic','polythene','bakelite','nylon','teflon','synthetic fibre','rayon','dacron','orlon','natural rubber','vulcanis','vulcaniz'],6)
add('CHEMISTRY','DailyLife-Chem',['soap','detergent','hard water','soft water','temporary hardness','preservative','sodium benzoate','vinegar','antioxidant','artificial sweetener','saccharin','aspartame','food colour','food additive','matchstick','phosphorus stick','firework','explosive','dynamite','gun powder','tnt'],5)
add('CHEMISTRY','Agri-Chem',['fertiliser','fertilizer','urea','npk','ammonium nitrate','insecticide','pesticide','weedicide'],6)
add('CHEMISTRY','Matter&Mixtures',['colloid','colloidal','suspension','milk of magnesia','olfactory indicator','tyndall','brownian','zigzag movement','matter','mixture','distillation','sublimation','homogeneous','heterogeneous','solution of'],5)
add('CHEMISTRY','Misc-Chem',['chemistry','chemist','alchemist','nobel prize in chemistry','copper sulphate','copper sulfate','iron nail','atom'],4)
add('CHEMISTRY','Compounds',['chemical compound','compound','louis pasteur','chirality'],6)

# ================= PHYSICS =================
add('PHYSICS','Units&Measurement',['si unit','unit of','measured in','derived unit','fundamental unit','dimensional formula','vernier','screw gauge','least count','dimension of'],6)
add('PHYSICS','Optics',['mirror','lens','concave','convex','spectrum','prism','rainbow','total internal reflection','myopia','hypermetropia','presbyopia','astigmatism','telescope','microscope','periscope','kaleidoscope','light year','law of reflection','law of refraction','refraction','reflection of light','speed of light'],6)
add('PHYSICS','Sound',['sound','decibel','sonar','ultrasonic','infrasound','echo','reverberation','doppler','pitch of','loudness','audible','mach number','shock wave','resonance of sound'],6)
add('PHYSICS','Electricity/Magnetism',['ohm','electric current','voltage','resistance','resistivity','fuse','transformer','generator','dynamo','electric motor','ammeter','voltmeter','galvanometer','semiconductor','diode','transistor','superconductor','magnet','magnetic field','compass needle','north pole of magnet'],6)
add('PHYSICS','Motion&Force',['newton','force','velocity','acceleration','momentum','inertia','friction','gravitation','gravity','free fall','projectile','centripetal','centrifugal','relative velocity','displacement','uniform motion','law of motion','kepler law','escape velocity','weightlessness','banking of road'],6)
add('PHYSICS','Work/Energy/Machines',['work done','kinetic energy','potential energy','conservation of energy','joule','watt','horsepower','horse power','simple machine','lever','pulley','inclined plane','efficiency of machine'],6)
add('PHYSICS','Heat',['temperature','thermometer','kelvin','celsius','fahrenheit','calorimeter','specific heat','latent heat','conduction','convection','radiation of heat','thermal expansion','absolute zero','heat engine','carnot'],6)
add('PHYSICS','Waves',['wavelength','frequency','hertz','time period of wave','amplitude','transverse wave','longitudinal wave','electromagnetic wave','gamma ray','x ray','infrared','ultraviolet','microwave','radio wave'],6)
add('PHYSICS','ModernPhysics',['radioactivity','nuclear fission','nuclear fusion','alpha particle','beta particle','gamma radiation','half life','photoelectric','quantum theory','planck'],6)
add('PHYSICS','Pressure/Fluids',['pressure cooker','barometer','manometer','anemometer','hygrometer','pyrometer','seismograph','odometer','lactometer','hydrometer','altimeter','tachometer','sphygmomanometer','archimedes','buoyant','buoyancy','density','relative density','capillary','surface tension','viscosity','pascal law','bernoulli'],6)
add('PHYSICS','DailyLife-Phy',['why ice','why sky','blue colour of the sky','why stars','floats on water','melting point','boiling point','evaporat','condens','steam engine','internal combustion','petrol engine','diesel engine','microwave oven','refrigerator','air conditioner','washing machine'],5)
add('PHYSICS','ModernPhysics2',['theory of relativity','relativity','einstein'],6)
add('PHYSICS','Misc-Phy',['physics','physicist','nobel prize in physics','invented the telephone','invented television','invented radio','invented steam engine','invented the telegraph','charged particle','cyclotron','heating of the air'],4)

# ================= CULTURE =================
add('CULTURE','ClassicalDances',['bharatanatyam','kathakali','kuchipudi','odissi','manipuri dance','kathak dance','mohiniyattam','sattriya','classical dance'],7)
add('CULTURE','FolkDances',['folk dance','ghoomar','kalbelia','bhavai','garba','dandiya','bihu dance','bhangra','giddha','lavani','rouf dance','karma dance','chhau','gaur dance','dumhal','kachhi ghodi','terah talli','dollu kunitha','yakshagana','kummi','kolannalu','fugdi'],7)
add('CULTURE','Music',['hindustani music','carnatic music','raga','ragam','tala music','thumri','khayal','dhrupad','ghazal','qawwali','tabla','sitar','sarod','flute','veena','shehnai','harmonium','sarangi','santoor','gharana','vocalist','instrumentalist','bismillah khan','ravi shankar','zakir hussain','bhimsen joshi','subbulakshmi','musician','melodic instrument','music','folk music','singer','singing','sangeet','bhatkhande','classical music','musical lineage','composed the music','music composer','lyricist','sankirtan','kirtan','annamacharya','song','beatles','maa tujhe salaam','ar rahman'],5)
add('CULTURE','Dance-Persons',['choreographer','dancer','father of modern dance','classical dancer','dance form','dance of','dance is popular','dance belongs'],5)
add('CULTURE','Festivals/Fairs',['festival','pongal','onam','baisakhi','lohri','makar sankranti','navratri','durga puja','chhath','karva chauth','gangaur','teej festival','hornbill festival','pushkar fair','kumbh mela','kumbh','surajkund','hemis festival','bikaner camel','fairs and festival'],6)
add('CULTURE','Paintings',['painting','madhubani','pattachitra','warli','pichwai','phad painting','kalamkari','miniature','mughal painting','rajput painting','basohli','kangra school','company painting','ragamala','fresco','mural'],7)
add('CULTURE','Architecture',['stupa','chaitya','vihara','gopuram','vimana temple','shikhara','mandapa','garbhagriha','amalaka','nagara style','dravida style','vesara','khajuraho','konark','sun temple','brihadeshwara','meenakshi temple','somnath temple','dilwara','rock cut','ajanta','ellora','sanchi','bharhut','amravati stupa','gandhara school','mathura school','temple architecture','temple of','taj mahal','qutub minar','red fort','fatehpur sikri','agra fort','charminar','gol gumbaz','buland darwaza','unesco world heritage','world heritage site','hawa mahal','monument','palace','tomb of','dargah','gurudwara','mosque','temple'],5)
add('CULTURE','Theatre&Puppetry',['theatre','theater','koodiyattam','ramlila','jatra','tamasha','nautanki','swang','bhand pather','ankia naat','mudiyettu','puppet','puppetry','kathputli','string puppet','shadow puppet'],6)
add('CULTURE','Martial&Misc',['martial art','kalaripayattu','silambam','thang ta','gatka','mallakhamb','circus art'],6)
add('CULTURE','Literature-Culture',['sanskrit literature','tamil literature','sanskrit poet','kalidasa','meghaduta','abhijnana','panini','bharata muni','natyashastra','classical language','sahitya akademi award','jnanpith award','gitanjali','playwright','folklore','handicraft','handloom','chikankari','pashmina','banarasi silk','kanjivaram','bidri work','blue pottery','terracotta','wood craft','geographical indication','gi tag','language','lingua franca','costume','cultural costume','lace work','lacework','craft','embroidery','zardozi','phulkari','weaving'],5)
add('CULTURE','Films',['movie','film industry','bollywood','cinema','actor','actress','film director','directed the film','filmfare award','national film award ceremony','feature film'],5)

# ================= STATIC =================
add('STATIC','Awards',['bharat ratna','padma vibhushan','padma bhushan','padma shri','padma award','nobel prize','oscar','academy award','dadasaheb phalke','booker prize','ramon magsaysay','jnanpith','gnanpith','sahitya akademi','fields medal','abel prize','gallantry award','param vir chakra','ashoka chakra','vir chakra','kirti chakra','shaurya chakra','arjuna award','khel ratna','dronacharya award','dhyan chand award','laureus award','grammy','emmy award','cannes','filmfare','national film award','indira gandhi peace','right livelihood','nobel laureate','first indian to win nobel','bharat ratna award'],6)
add('STATIC','Sports-Cricket',['cricket','one day international','test match','t20','ipl','ranji trophy','duleep trophy','deodhar trophy','irani trophy','ashes series','border gavaskar','world cup cricket','icc','batsman','bowler','wicket','run out','lbw','powerplay','third umpire','drs'],6)
add('STATIC','Sports-Others',['olympic','olympics','commonwealth games','asian games','saf games','fifa','football','hockey','badminton','tennis','us open','wimbledon','french open','australian open','grand slam','kabaddi','pro kabaddi','wrestling','boxing','archery','shooting sport','athletics','golf','table tennis','chess','formula one','motogp','tour de france','marathon','trophy','tournament','stadium','sports person','sportsperson','sport of','game is played','game is associated','game played between','players in a team','number of players','olympic game','ancient olympic','captain of','wimbledon title'],5)
add('STATIC','Books&Authors',['book','novel','autobiography','biography','written by','authored by','author of','memoir','my experiments with truth','train to pakistan','midnight children','white tiger novel','interpreter of maladies','guide novel','godan'],5)
add('STATIC','Days&Themes',['day is celebrated','day is observed','international day','national day of','world environment day','world health day','international yoga day','teachers day','earth day','world water day','world wetlands day','wildlife week','national sports day','constitution day','army day','navy day','air force day','gandhi jayanti','celebrated on','observed on','observed every','celebrated every'],6)
add('STATIC','Abbreviations',['full form','fullform','stands for','expanded form','abbreviation','acronym'],7)
add('STATIC','Firsts&Superlatives',['first indian','first woman','first person','first country','first in the world','first to reach','first president of india','first prime minister','first indian woman','tallest','longest railway','highest railway','longest bridge','largest museum','biggest','smallest country','largest country','largest desert','longest wall','seven wonders','wonder of the world','largest planetarium','largest library','longest river in the world','largest stadium','first university'],5)
add('STATIC','Currencies',['currency','rupee','dollar','euro','yen','pound sterling','dirham','rial','taka'],6)
add('STATIC','Parliaments&Orgs',['parliament of','diet of japan','duma','knesset','majlis','national assembly','senate of','headquarters','world health organisation','world health organization','unicef','unesco','fao','ilo','united nations','security council','general assembly','secretary general of un','red cross','amnesty international','greenpeace','nato','asean','saarc','opec','commonwealth nations','non aligned movement','international court','international labour'],5)
add('STATIC','NationalSymbols',['national flag','national anthem','national song','national bird','national animal','national flower','national tree','national aquatic animal','national heritage animal','state animal','state bird','state flower','national emblem','lion capital','ashoka pillar','tricolour','saffron colour in the flag','national symbols','national calendar'],6)
add('STATIC','Airports/Ports/Misc-India',['airport','international airport','sea port','sea harbour','harbour','indian railways','first railway','railway zone','first postage stamp','pin code','first newspaper','standard time of india','missile','agni missile','prithvi missile','brahmos','akash missile','nirbhay','indian army','indian navy','indian air force','bsf','crpf','itbp','cisf','assam rifles','nsg commando','paramilitary','coast guard','galwan','siachen glacier army'],5)
add('STATIC','Tribes',['tribe','tribal','raika','baiga','santhal','gond','bhil','munda','toda','bodo','khasi','aboriginal'],5)
add('STATIC','Institutes&Places',['institute','located at','located in','academy of','research academy','national institute','college of physical education','mountaineering institute','centre of excellence','headquarters of the institute'],4)
add('STATIC','Sports-Equipment/Rules',['standard weight','weight of the hammer','size of basketball','basketball','volleyball','handball','fencing','equestrian','kho kho','hammer throw','javelin','high jump','long jump','triple jump','pole vault','shot put','discus','relay race','badminton court','swimming','gymnastics','rugby','baseball','snooker','billiards','squash','rowing','canoeing','weightlifting','taekwondo','judo','karate','wushu','buddh international','racing circuit','velodrome','penalty stroke','penalty corner','penalty kick','position in the','stroke in','freestyle','butterfly stroke','kabaddi','khelo india','trophy is associated','cup is associated'],5)
add('STATIC','Nicknames',['manchester of','venice of','pink city','city of joy','silicon valley of','queen of the hills','land of the rising sun','land of the midnight sun','pearl of the antilles','gift of the nile','playground of europe','city of seven hills','eternal city','pearl of the orient','sorrow of bengal','sorrow of bihar','referred to as the','known as the gateway','city is known as','state is known as','country is known as'],5)
add('STATIC','Persons&Infra',['founder of','business tycoon','reliance industries','tata group','industrialist','missionary','tunnel','atal tunnel','border roads organisation','corporatized port'],4)
add('STATIC','Misc-Static',['brand','company tagline','invented','invention of','discovered the','discovery of','discoverer','polio vaccine','penicillin discovered','supercomputer','first supercomputer','search engine','radio broadcasting','broadcasting started','first radio'],4)

# ================= COMPUTER =================
add('COMPUTER','MSOffice',['ms word','ms excel','ms powerpoint','powerpoint','ms access','ms office','word document','excel','spreadsheet','workbook','worksheet','slide in','slides in','slide show','cell in excel','row in ms','column in ms','merge cells','auto sum','drop down menu of','clipboard','toolbar','menu bar','icon below','formatting from selected text','header and footer','page margin','page layout'],7)
add('COMPUTER','Internet&Tech',['internet','website','web page','web browser','browser','search engine','e mail','email','gmail','instant messaging','emoticon','digital signature','public key','two factor authentication','authentication','password','bluetooth','usb','wifi','iot','cloud computing','artificial intelligence','machine learning','blockchain','cryptocurrency','e land record','digitise','digitize','technology is used','lan','wan','html','http','ip address','bandwidth','server','database','operating system','software','hardware','computer memory','ram','rom','cpu','printer','scanner','file extension','keyboard shortcut','shortcut key','ctrl key','folder','icon on the desktop'],5)
add('COMPUTER','MSOffice2',['microsoft word','microsoft excel','microsoft powerpoint','mail merge','spell check','spell check in','help window in microsoft','save button','in word','in ppt','in ms word','in ms excel'],6)
add('COMPUTER','Hardware&Network',['secondary memory','primary memory','magnetic disk','hard disk','floppy','cd rom','dvd','network','nodes','gateway','router','data transmission','full duplex','half duplex','simplex','generation of computer','second generation','modes of data','lan wan','topology'],5)
add('COMPUTER','Misc-Comp',['computer','computing','storage device','input device','output device','peripheral'],4)

# ---- v3 additions (unknown-bucket QA se) ----
add('HISTORY','Ancient-Prehistory',['neolithic','palaeolithic','paleolithic','mesolithic','chalcolithic','stone age','burzahom','mehrgarh','microlith'],6)
add('HISTORY','Ancient-Misc3',['sulaiman','arab traveller'],6)
add('HISTORY','Medieval-Misc3',['qutbuddin','aybak','battle of karnal','nadir shah','jaimal'],7)
add('HISTORY','Modern-Misc3',['rohilla','nawab of awadh','awadh','indian association','surendranath','sarvajanik','ganesh utsav','literary society','muhammedan'],6)
add('HISTORY','World-Misc2',['great wall of china'],6)
add('POLITY','Laws2',['board of revenue','arms act','dowry prohibition act','regional rural banks act','act in india promulgated','act was passed in india'],5)
add('POLITY','Misc2',['federalism','level of government','tier of government','three tier'],4)
add('ECONOMICS','Sectors',['primary sector','secondary sector','tertiary sector','sectors of the economy','industrial sector'],6)
add('ECONOMICS','Money&Banking2',['non tax revenue','capital expenditure','capital receipt','revenue expenditure','revenue of the government','dividends received','escheat','without a legal heir','physical quality of life','pqli','quality of life index','demand for money','liquidity preference','keynes','repayment rate','sahaj bijli','uday','literacy programme','new india literacy'],5)
add('GEOGRAPHY','Mountains2',['plateau','plains','ambala','east coast','west coast','coromandel','malabar coast','northern circars'],4)
add('GEOGRAPHY','EarthBasics3',['sea floor spreading','seafloor spreading','harry hammond hess','hydrolysis of','orthoclase'],5)
add('GEOGRAPHY','Astronomy2',['universe','cosmos'],5)
add('GEOGRAPHY','World-Misc2',['midnight sun'],5)
add('BIOLOGY','Disease&Immunity2',['bacterium','toxin'],6)
add('BIOLOGY','Cell&Genetics2',['clone','cloned','cloning','scientific name','solanum','lycopersicum','binomial name'],5)
add('BIOLOGY','Skeleton2',['pivot joint','synovial','joint between','joints in the human'],6)
add('CHEMISTRY','PeriodicTable2',['electronegativity','pauling','diagonal relationship','molecular formula','acetylene','hydride of'],6)
add('CHEMISTRY','Acids2',['ph of'],6)
add('PHYSICS','Electricity2',['emf','induced','faraday','lenz law','electromagnetic induction','battery'],6)
add('PHYSICS','Units2',['significant figures','instrument for measuring','measuring blueness'],6)
add('PHYSICS','Heat2',['warm air','cold air','air expands'],4)
add('CULTURE','Literature2',['poet','ramcharita','bhavabhuti','ardhakathanak','half story','tat vadya','vadya'],5)
add('STATIC','Sports2',['running events','athletics','track event','hurdles','power lifting','powerlifting','issf','world cup','fencing','equestrian'],5)
add('STATIC','Awards2',['saraswati samman'],6)
add('STATIC','Days2',['menstrual hygiene day','hygiene day'],6)
add('STATIC','Persons&Infra2',['vice chancellor','coined the term','drdo','defence research','ministry of defence','academy','situated in','is situated'],4)
add('COMPUTER','Hardware&Network2',['group of 4 bits','nibble','programming','programming language','fortran','cobol'],5)

# ---------------- CA hard rule ----------------
CA_YEAR = re.compile(r'(?<![0-9])(2021|2022|2023|2024|2025)(?![0-9])')
CA_PHRASES_RAW = [
 'appointed as','appointment of','takes charge','took charge','sworn in','passed away','demise of',
 'joint military exercise','military exercise','naval exercise','air exercise','bilateral exercise',
 'g20','brics','sco summit','g7 summit','quad leaders','climate summit',
 'launched by','launched in','launched on','launched under','scheme launched','portal launched',
 'app launched','mission launched','campaign launched','yojana launched','flagged off',
 'recently','inaugurated','conferred the','conferred with','title winner','won the title',
 'runner up','brand ambassador','ambassador for','miss universe','miss world',
 'time magazine','forbes','chandrayaan 3','aditya l1','gaganyaan','covid','coronavirus','pandemic',
 'lockdown','5g','in news','new chief minister','new governor','new president','new prime minister',
 'was appointed','launched the app','launched the scheme','launched the mission','launched the portal',
 'launched a new','launched a','policy was released','was released in','released by the ministry','theme of',
 'current president','current chief minister','current governor','current prime minister',
 'current chairman','current ceo','current chief justice','present president','present chief minister',
 'union budget 2','economic survey 2','resigned','assumed office','summit was held','hosted the',
 'women world cup','world cup was','asia cup','global hunger index','human development index',
 'ease of doing business','guinness book','world record of','final of the','championship was',
]
CA_PHRASES = [re.compile(r'(?<![a-z])' + re.escape(p.replace('-',' ')) + r'(?![a-z])') for p in CA_PHRASES_RAW]

def is_ca(t):
    if CA_YEAR.search(t): return True
    return any(rx.search(t) for rx in CA_PHRASES)

# ---------------- NON-GS leakage detector (2017-19 window drift: maths/English/GI Qs) ----------------
NONGS_RAW = [
 'correct to','decimal places','average of','value of x','two places of decimal','the value of',
 'sin ','cos ','tan ','cot ','sec of','cosec','triangle','hypotenuse','perimeter','area of a',
 'compound interest','simple interest','marked price','cost price','selling price','profit percent',
 'loss percent','discount of','mixture of two','alloy of two','upstream','downstream','km h',
 'men can do a work','days to complete','efficiency of','ratio of the','sum of the two numbers',
 'product of two','square root','cube root','equation','x and y','inequality','algebraic',
 'average of the','per cent of','percentage of the','simplest form','nearest integer',
 'select the correctly spelt','correctly spelt','synonym of','antonym of','idiom','one word substitution',
 'improve the underlined','most appropriate word','fill in the blank with the correct','cloze test',
 'para jumbled','jumbled sentences','given passage','narration change','active voice','passive voice',
 'mirror image','water image','paper folding','paper cutting','dice ','coding decoding','blood relation',
 'direction sense','syllogism','statement and conclusion','venn diagram','select the odd','odd one out',
 'analogy','series is','missing term','wrong number in the series','logical venn','matrix of',
 'select the option that will improve','select the most suitable','arrange the following',
]
NONGS = [re.compile(r'(?<![a-z])' + re.escape(p.strip().replace('-',' ')) + r'(?![a-z])') for p in NONGS_RAW]

NONGS_STRONG_RAW = [
 'cost price','selling price','marked price','compound interest','simple interest','profit percent',
 'loss percent','two places of decimal','correct to the nearest','correct to two','hypotenuse',
 'triangle abc','perimeter of','cosec','square root of','cube root of','ratio and proportion',
 'men can do a work','women can do a work','working together they can','upstream and downstream',
 'correctly spelt','synonym of','antonym of','one word substitution','cloze test','para jumbled',
 'coding decoding','blood relation','mirror image','water image','paper folding','punched',
 'missing number in the series','wrong number in the series','select the odd one','odd one out','price of an article','an article is bought','article is sold','sold at a loss','gain percent on the whole',
]
NONGS_STRONG = [re.compile(r'(?<![a-z])' + re.escape(p) + r'(?![a-z])') for p in NONGS_STRONG_RAW]

def is_nongs(t):
    if any(rx.search(t) for rx in NONGS_STRONG): return True
    hits = sum(1 for rx in NONGS if rx.search(t))
    return hits >= 2

# ---------------- loading ----------------
def load_all(root):
    bd = json.load(open(os.path.join(root, 'b_data.json')))
    papers = []
    for c in bd['categories']:
        for it in c['data']:
            papers.append({'year': c['year'], 'name': it['name']})
    assert len(papers) == 193, len(papers)
    out = []
    for idx, p in enumerate(papers, 1):
        year = p['year']; base = f"{year}_{idx:03d}"
        qs = []
        if year == 2024:
            f = os.path.join(root, 'ocr_raw', base + '.parsed.json')
            if os.path.exists(f):
                allq = json.load(open(f))
                qs = [q for q in allq if q.get('sec') and re.search(r'wareness|knowledge', str(q['sec']), re.I)]
        else:
            f = os.path.join(root, 'gs_parsed', base + '.gs.json')
            if os.path.exists(f):
                qs = json.load(open(f))['questions']
        for q in qs:
            out.append({'paper': base, 'year': year, 'pname': p['name'],
                        'qnum': q.get('qnum'), 'qtext': (q.get('qtext') or '').strip(),
                        'options': q.get('options') or {}, 'answer': q.get('answer')})
    return out

def classify(q):
    t = norm(strip_qnum(q['qtext']))
    if len(t) < 5:
        return ('NO-TEXT', 'empty/short')
    if t.startswith('question pdf') or 'image tha' in t or 'ocr se capture nahi' in t:
        return ('NO-TEXT', 'placeholder')
    if any('\u0900' <= ch <= '\u097f' for ch in t):
        return ('NO-TEXT', 'hindi-font-broken')
    if is_nongs(t):
        return ('NON-GS', 'window-drift-leak')
    if is_ca(t):
        return ('CA', 'current-affairs')
    opt = norm(' | '.join(str(v) for v in q['options'].values() if v))
    subj_scores = collections.defaultdict(float)
    topic_scores = collections.defaultdict(float)
    for subj, topic, rx, w in SIG:
        if rx.search(t):
            subj_scores[subj] += w; topic_scores[(subj, topic)] += w
        elif opt and rx.search(opt):
            subj_scores[subj] += w * 0.5; topic_scores[(subj, topic)] += w * 0.5
    if not subj_scores or max(subj_scores.values()) < 2:
        return ('UNKNOWN', 'no-signal')
    subj = max(subj_scores.items(), key=lambda kv: (kv[1], -SUBJ_ORDER.index(kv[0])))[0]
    ts = {k[1]: v for k, v in topic_scores.items() if k[0] == subj and v > 0}
    topic = max(ts.items(), key=lambda kv: kv[1])[0] if ts else 'general'
    return (subj, topic)

def nkey(q):
    return norm(strip_qnum(q['qtext']))[:220]

def ans_text(q):
    a = q.get('answer')
    if a is None: return None
    opts = q.get('options') or {}
    key = str(a)
    for cand in (key, key.upper(), key.lower()):
        if cand in opts and str(opts[cand]).strip():
            return norm(str(opts[cand]))[:100]
    return None

def main():
    root = sys.argv[1]
    outroot = sys.argv[2]
    os.makedirs(outroot, exist_ok=True)
    qs = load_all(root)
    for q in qs:
        s, t = classify(q)
        q['subject'] = s; q['topic'] = t; q['nkey'] = nkey(q)
    json.dump(qs, open(os.path.join(outroot, 'gs_classified.json'), 'w'), ensure_ascii=False)

    R = []
    def w(line=''): R.append(line)
    w('=' * 78); w('GS PYQ CLASSIFICATION REPORT'); w('=' * 78)
    w(f'Total parsed questions: {len(qs)}  (slots 4825; placeholders/image-Q = {4825-len(qs)})')
    subj_tot = collections.Counter(q['subject'] for q in qs)
    w(''); w('--- SUBJECT TOTALS ---')
    for s, c in subj_tot.most_common():
        ans = sum(1 for q in qs if q['subject'] == s and q['answer'] is not None)
        w(f'{s:12s} {c:5d}  ({c*100.0/len(qs):4.1f}%)   answers: {ans}/{c} = {ans*100.0/c if c else 0:.0f}%')
    w(''); w('--- YEAR x SUBJECT MATRIX ---')
    ys = collections.defaultdict(collections.Counter)
    for q in qs: ys[q['year']][q['subject']] += 1
    subjects = [s for s in ['HISTORY','GEOGRAPHY','POLITY','ECONOMICS','PHYSICS','CHEMISTRY','BIOLOGY','ENVIRONMENT','CULTURE','STATIC','COMPUTER','CA','NO-TEXT','UNKNOWN'] if s in subj_tot]
    w(f"{'year':6s}" + ''.join(f'{s[:7]:>9s}' for s in subjects) + f"{'total':>8s}")
    for y in sorted(ys, reverse=True):
        row = ''.join(f'{ys[y][s]:9d}' for s in subjects)
        w(f'{y:<6d}' + row + f'{sum(ys[y].values()):8d}')
    w(''); w('--- TOPIC TABLES PER SUBJECT ---')
    for s in subjects:
        if s in ('UNKNOWN',): continue
        st = collections.Counter(q['topic'] for q in qs if q['subject'] == s)
        w(f''); w(f'### {s}  (total {subj_tot[s]})')
        for t, c in st.most_common():
            ex = next(q for q in qs if q['subject'] == s and q['topic'] == t)
            w(f'  {c:4d}  {t:28s} e.g. {ex["qtext"][:88]}')
    # duplicates
    groups = collections.defaultdict(list)
    for q in qs:
        if q['subject'] != 'UNKNOWN':
            groups[q['nkey']].append(q)
    dupg = sorted((g for g in groups.values() if len(g) >= 2), key=lambda g: -len(g))
    w(''); w('--- DUPLICATE / REPEAT ANALYSIS ---')
    w(f'distinct question-keys: {len(groups)}; groups repeated >=2 times: {len(dupg)}')
    w(f'repeated-question volume (sum of group sizes): {sum(len(g) for g in dupg)}')
    w(''); w('TOP 80 REPEATED QUESTIONS (count | subject | question | answers-consistency):')
    for g in dupg[:80]:
        ats = set(ans_text(q) for q in g if ans_text(q))
        conf = 'NO-ANSWER' if not ats else ('CONSISTENT' if len(ats) == 1 else 'CHECK-OPTIONS-ORDER')
        years = ','.join(str(q['year']) for q in sorted(g, key=lambda x: -x['year']))
        w(f'  x{len(g)} [{g[0]["subject"][:7]}] ({years}) {g[0]["qtext"][:95]}  <<{conf}>>')
    # CA detail
    w(''); w('--- CA (count-only bucket) YEAR-WISE ---')
    for y in sorted(ys, reverse=True):
        w(f'  {y}: {ys[y]["CA"]:4d}')
    ca_q = [q for q in qs if q['subject'] == 'CA']
    cag = collections.defaultdict(list)
    for q in ca_q: cag[q['nkey']].append(q)
    cadup = sorted((g for g in cag.values() if len(g) >= 2), key=lambda g: -len(g))
    w(''); w('CA repeated questions (top 25):')
    for g in cadup[:25]:
        w(f'  x{len(g)} ({",".join(str(q["year"]) for q in g)}) {g[0]["qtext"][:95]}')
    # unknown dump
    unk = [q for q in qs if q['subject'] == 'UNKNOWN']
    w(''); w(f'--- UNKNOWN BUCKET: {len(unk)} (all listed) ---')
    for q in unk[:400]:
        w(f'  [{q["paper"]}] {strip_qnum(q["qtext"])[:110]}')
    # samples for QA
    rnd = random.Random(42)
    w(''); w('--- RANDOM SAMPLES PER SUBJECT (10 each, for QA) ---')
    for s in subjects:
        if s == 'UNKNOWN': continue
        pool = [q for q in qs if q['subject'] == s]
        for q in rnd.sample(pool, min(10, len(pool))):
            w(f'  [{s[:7]}/{q["topic"][:22]}] {strip_qnum(q["qtext"])[:100]}')
    open(os.path.join(outroot, 'classification_report.txt'), 'w').write('\n'.join(R))
    print('classified:', len(qs))
    print('subject totals:', dict(subj_tot))
    print('report: ', os.path.join(outroot, 'classification_report.txt'))

if __name__ == '__main__':
    main()
