"""
ZAYVORA Pharmacopoeia & Classical Unani Drug Register.

Sources:
- Unani Pharmacopoeia of India (UPI), Parts I & II, Ministry of AYUSH, Govt of India.
- National Formulary of Unani Medicine (NFUM), Parts I-VI, CCRUM.
- Schedule E(1) of the Drugs and Cosmetics Rules, 1945 (Ayurvedic, Siddha and Unani Poisons).
- Classical Texts: Al-Qanoon fit-Tibb (Avicenna), Kitab al-Hawi (Rhazes), Makhzan-ul-Adwiya.
"""
from __future__ import annotations

from typing import Any

# ============================================================================
# 1. SCHEDULE E(1) STATUTORY POISONS REGISTER (DRUGS & COSMETICS RULES 1945)
# ============================================================================
SCHEDULE_E1_POISONS: dict[str, dict[str, Any]] = {
    "suranjan_talkh": {
        "id": "se1-suranjan-talkh",
        "canonical_name": "Suranjan Talkh",
        "urdu_name": "سورنجان تلخ",
        "botanical_name": "Colchicum luteum Baker / Colchicum autumnale L.",
        "family": "Colchicaceae",
        "part_used": "Dried corm",
        "synonyms": ["Bitter Meadow Saffron", "Colchicum", "Suranjan-e-Talkh"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 3, "wd_degree": 3},
        "toxic_alkaloids": ["Colchicine", "Demecolcine"],
        "poison_class": "Mitotic Inhibitor / Tubulin Binder / Cytotoxic Alkaloid",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": (
            "Boiled in cow's milk (Sheer-e-Gao) for 3 hours, outer membranous skin peeled, "
            "embryonic shoot excised, dried in shade, and lightly fried with Almond Oil (Roghan-e-Badam)."
        ),
        "musleh": "Roghan-e-Badam (Almond Oil), Kateera (Tragacanth), Zafran (Saffron)",
        "badal": "Suranjan Shireen, Bozidana",
        "max_single_dose_mg": 250.0,
        "max_daily_dose_mg": 750.0,
        "therapeutic_window": "Narrow (colchicine toxicity produces cholera-like gastrointestinal catastrophe)",
        "antidote": "Demulcents, Tannic acid solution, Gastric lavage with 0.1% potassium permanganate, Atropine for colic",
        "statutory_warning": "SCHEDULE E(1) POISON: Caution: To be taken under medical supervision only. Must be Mudabbar (detoxified).",
    },
    "kuchla": {
        "id": "se1-kuchla",
        "canonical_name": "Kuchla",
        "urdu_name": "کچلہ / اذراقی",
        "botanical_name": "Strychnos nux-vomica L.",
        "family": "Loganiaceae",
        "part_used": "Dried ripe seeds",
        "synonyms": ["Azaraqi", "Nux Vomica", "Poison Nut"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 3, "wd_degree": 3},
        "toxic_alkaloids": ["Strychnine", "Brucine"],
        "poison_class": "Glycine Receptor Antagonist / Spinal Neurotoxin / Convulsant",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": (
            "Soaked in cow's milk or Triphala decoction for 7 days with daily liquid change; "
            "outer seed coat (testa) and cotyledonary embryo excised; endosperm fried in Cow's Ghee (Roghan-e-Zard) until yellowish-brown."
        ),
        "musleh": "Roghan-e-Zard (Ghee), Milk (Sheer-e-Taza), Anisoon (Aniseed)",
        "badal": "Jadwar, Asgandh",
        "max_single_dose_mg": 65.0,
        "max_daily_dose_mg": 125.0,
        "therapeutic_window": "Extremely Narrow (strychnine causes violent tetanic convulsions and asphyxia)",
        "antidote": "Diazepam/Barbiturates for seizures, Charcoal hemoperfusion, Tannin wash, absolute quiet",
        "statutory_warning": "SCHEDULE E(1) POISON: Toxic spinal stimulant. Strictly contraindicated without Mudabbar processing.",
    },
    "bhilawa": {
        "id": "se1-bhilawa",
        "canonical_name": "Bhilawa",
        "urdu_name": "بھیلاواں / حب الفہم",
        "botanical_name": "Semecarpus anacardium L.f.",
        "family": "Anacardiaceae",
        "part_used": "Mature fruit pericarp",
        "synonyms": ["Hab-ul-Fahm", "Marking Nut", "Bhallataka"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 4, "wd_degree": 3},
        "toxic_alkaloids": ["Bhilawanol", "Anacardic acid", "Carbophenol"],
        "poison_class": "Severe Contact Vesicant / Alkylresorcinol / Nephrotoxin",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": (
            "Thalamus removed; fruits cut into pieces and rubbed vigorously with coarse brick powder (Surkhi) "
            "in an earthen pot for 7 days to absorb corrosive phenolic resins, then thoroughly washed in warm water and boiled in milk."
        ),
        "musleh": "Gond Babool (Acacia arabica), Roghan-e-Kunjad (Sesame oil), Butter, Coconut water",
        "badal": "Balela, Kundur",
        "max_single_dose_mg": 125.0,
        "max_daily_dose_mg": 250.0,
        "therapeutic_window": "Narrow (causes severe blister formation, contact dermatitis, hematuria, renal failure)",
        "antidote": "Cold milk, Sesame oil application externally, demulcents, systemic corticosteroids",
        "statutory_warning": "SCHEDULE E(1) POISON: Potent vesicant. Requires certification of Shodhana/Mudabbar with brick powder.",
    },
    "afeem": {
        "id": "se1-afeem",
        "canonical_name": "Afeem",
        "urdu_name": "افیون / تریاق",
        "botanical_name": "Papaver somniferum L.",
        "family": "Papaveraceae",
        "part_used": "Dried milky exudate (latex) from unripe capsules",
        "synonyms": ["Afyoon", "Opium", "Taryaaq"],
        "mizaj": {"temperament": "Saudawi", "quality": "Cold & Dry", "hc_degree": 4, "wd_degree": 4},
        "toxic_alkaloids": ["Morphine", "Codeine", "Thebaine", "Noscapine", "Papaverine"],
        "poison_class": "Opioid Receptor Agonist / Narcotic Analgesic / Respiratory Depressant",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Dissolved in fresh Arq-e-Gulab (Rose water) and filtered 7 times, evaporated slowly under gentle shade/mild water bath.",
        "musleh": "Jund-e-Bedastar, Zafran (Saffron), Filfil Siyah (Black pepper)",
        "badal": "Bazrulbanj (Hyoscyamus), Post-e-Khashkhash",
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 65.0,
        "therapeutic_window": "Extremely Narrow (causes pinpoint pupils, respiratory arrest, coma)",
        "antidote": "Naloxone (IV 0.4mg-2mg repeated), assisted mechanical ventilation, activated charcoal",
        "statutory_warning": "SCHEDULE E(1) / NDPS NARCOTIC: Controlled substance. Requires statutory license and Mudabbar certificate.",
    },
    "bhang": {
        "id": "se1-bhang",
        "canonical_name": "Bhang",
        "urdu_name": "بھنگ / قنب",
        "botanical_name": "Cannabis sativa L.",
        "family": "Cannabaceae",
        "part_used": "Dried mature leaves and flowering tops",
        "synonyms": ["Qinnab", "Vijaya", "Indian Hemp"],
        "mizaj": {"temperament": "Saudawi", "quality": "Cold & Dry", "hc_degree": 3, "wd_degree": 3},
        "toxic_alkaloids": ["Delta-9-Tetrahydrocannabinol (THC)", "Cannabidiol (CBD)"],
        "poison_class": "Cannabinoid Receptor Agonist / Psychotropic Hallucinogen",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Washed with cold water 21 times in cloth strainer, dried, and lightly roasted in Cow's Ghee.",
        "musleh": "Roghan-e-Zard (Ghee), Roghan-e-Pista, Honey, Milk",
        "badal": "Post-e-Khashkhash, Kishneez Khushk",
        "max_single_dose_mg": 250.0,
        "max_daily_dose_mg": 500.0,
        "therapeutic_window": "Moderate (causes dysphoria, psychosis, tachycardia, postural hypotension)",
        "antidote": "Acidic fluids (Lemon juice/Sirka), cold shower, supportive psychiatric monitoring",
        "statutory_warning": "SCHEDULE E(1) POISON: Sedative psychotropic botanical. Use only Mudabbar processed leaves.",
    },
    "dhatura": {
        "id": "se1-dhatura",
        "canonical_name": "Dhatura",
        "urdu_name": "دھتورہ / جوز ماثل",
        "botanical_name": "Datura metel L. / Datura stramonium L.",
        "family": "Solanaceae",
        "part_used": "Dried seeds and leaves",
        "synonyms": ["Jauz-e-Masir", "Thorn Apple", "Stramonium"],
        "mizaj": {"temperament": "Saudawi", "quality": "Cold & Dry", "hc_degree": 4, "wd_degree": 4},
        "toxic_alkaloids": ["Hyoscine (Scopolamine)", "Hyoscyamine", "Atropine"],
        "poison_class": "Muscarinic Acetylcholine Receptor Antagonist / Anticholinergic",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Seeds steeped in cow's milk for 12 hours, heated gently until boiled, seed coat peeled, and dried.",
        "musleh": "Roghan-e-Badam, Sheer-e-Taza, Honey, Vinegar",
        "badal": "Bazrulbanj, Afyoon",
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 60.0,
        "therapeutic_window": "Extremely Narrow (causes 'blind as a bat, mad as a hatter, red as a beet, hot as a hare, dry as a bone')",
        "antidote": "Physostigmine salicylate (1-2mg IV slowly), cold sponging, pilocarpine drops",
        "statutory_warning": "SCHEDULE E(1) POISON: High-potency anticholinergic deliriant.",
    },
    "jamalgota": {
        "id": "se1-jamalgota",
        "canonical_name": "Jamalgota",
        "urdu_name": "جمال گوٹہ / حب السلاطین",
        "botanical_name": "Croton tiglium L.",
        "family": "Euphorbiaceae",
        "part_used": "Seeds",
        "synonyms": ["Habb-us-Salateen", "Croton Seeds", "Jayapala"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 4, "wd_degree": 4},
        "toxic_alkaloids": ["Croton oil", "Crotin (toxalbumin)", "Phorbol esters"],
        "poison_class": "Drastic Hydragogue Cathartic / Protein Synthesis Inhibitor",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Outer husk removed; cotyledonary germ/embryo meticulously excised; boiled in cow's milk for 3 hours between cloth bundle (Dola Yantra).",
        "musleh": "Kishneez Khushk, Lemon juice, Buttermilk, Roghan-e-Badam",
        "badal": "Turbud, Saqmooniya",
        "max_single_dose_mg": 30.0,
        "max_daily_dose_mg": 60.0,
        "therapeutic_window": "Extremely Narrow (causes violent hypercatharsis, dehydration, mucosal sloughing, circulatory collapse)",
        "antidote": "Lemon juice, cold rice gruel (Kanjika), IV fluid replacement, oral demulcents",
        "statutory_warning": "SCHEDULE E(1) POISON: Drastic purgative. Untreated seeds cause lethal dehydration.",
    },
    "bish": {
        "id": "se1-bish",
        "canonical_name": "Bish",
        "urdu_name": "بیش / میٹھا تیلیا",
        "botanical_name": "Aconitum ferox Wall. / Aconitum chasmanthum Stapf",
        "family": "Ranunculaceae",
        "part_used": "Dried tuberous root",
        "synonyms": ["Meetha Teeliya", "Monkshood", "Wolfsbane", "Vatsanabha"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 4, "wd_degree": 4},
        "toxic_alkaloids": ["Aconitine", "Mesoaconitine", "Hypaconitine"],
        "poison_class": "Voltage-Gated Sodium Channel Activator / Cardiotoxin / Neurotoxin",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Root submerged in Cow's urine (Gau Mutra) for 3 days in sunlight, washed, then boiled in Cow's milk for 3 hours until soft.",
        "musleh": "Sheer-e-Taza, Roghan-e-Zard, Borax (Tankar), Harad",
        "badal": "Jadwar Khatai",
        "max_single_dose_mg": 15.0,
        "max_daily_dose_mg": 30.0,
        "therapeutic_window": "Extremely Narrow (fatal dose of raw aconitine is 1-2 mg; causes intractable ventricular arrhythmias)",
        "antidote": "Atropine for bradycardia, Flecainide/Amiodarone for ventricular tachycardia, gastric lavage",
        "statutory_warning": "SCHEDULE E(1) POISON: Fatal cardiotoxin. Raw root prescription is strictly prohibited.",
    },
    "samm_ul_far": {
        "id": "se1-samm-ul-far",
        "canonical_name": "Samm-ul-Far",
        "urdu_name": "سم الفار / سنکھیا",
        "botanical_name": "Arsenic trioxide (As2O3)",
        "family": "Mineral origin",
        "part_used": "Refined mineral sublimate",
        "synonyms": ["White Arsenic", "Sankhiya", "Shukla Pashana"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 4, "wd_degree": 4},
        "toxic_alkaloids": ["Arsenic (trivalent As3+)"],
        "poison_class": "Sulfhydryl Group Inhibitor / Heavy Metal Cellular Poison",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Purified as Kushta-e-Samm-ul-Far through repeated calcinations (Taqteer / Putapaka) with plant juices (Calotropis/Aak) until micro-particulate oxide form is achieved.",
        "musleh": "Tamarind pulp, Butter, Fresh cow milk",
        "badal": "Ras-Kapur Mudabbar",
        "max_single_dose_mg": 2.0,
        "max_daily_dose_mg": 5.0,
        "therapeutic_window": "Extremely Narrow (causes multi-organ failure, gastrointestinal hemorrhage, garlic breath)",
        "antidote": "Dimercaprol (BAL), Succimer (DMSA), aggressive fluid resuscitation",
        "statutory_warning": "SCHEDULE E(1) POISON: Heavy metal mineral. Must be standard Kushta complying with UPI standards.",
    },
    "seemab": {
        "id": "se1-seemab",
        "canonical_name": "Seemab",
        "urdu_name": "سیماب / پارہ",
        "botanical_name": "Hydrargyrum / Elemental Mercury (Hg)",
        "family": "Mineral origin",
        "part_used": "Purified elemental metal",
        "synonyms": ["Para", "Mercury", "Quicksilver", "Rasendra"],
        "mizaj": {"temperament": "Saudawi", "quality": "Cold & Dry", "hc_degree": 4, "wd_degree": 4},
        "toxic_alkaloids": ["Elemental and inorganic mercury salts"],
        "poison_class": "Heavy Metal / Nephrotoxin / Neurotoxin",
        "mandatory_mudabbar": True,
        "mudabbar_protocol": "Triturated with Sulphur (Gandhak) for 72 continuous hours to form black non-metallic sulphide (Kajjali / Kajli) passing tests of Rekhapurna and Varitara.",
        "musleh": "Gandhak (Sulphur), Zeera Siyah, Lemon juice",
        "badal": "Kushta-e-Marwareed",
        "max_single_dose_mg": 15.0,
        "max_daily_dose_mg": 30.0,
        "therapeutic_window": "Extremely Narrow. Raw elemental mercury is NEVER administered internally.",
        "antidote": "DMSA, Dimercaprol (BAL), Penicillamine",
        "statutory_warning": "SCHEDULE E(1) POISON: Mercury. Strictly prohibited except in chemically stabilized Kajli/Kushta formulation.",
    },
}

# ============================================================================
# 2. UPI AUTHENTIC CLASSICAL SINGLE DRUGS (MUFRADAT) REGISTER
# ============================================================================
UPI_MUFRADAT_REGISTRY: list[dict[str, Any]] = [
    {
        "id": "upi-suranjan-talkh",
        "name": "Suranjan Talkh",
        "botanical_name": "Colchicum luteum Baker",
        "part_used": "Corm",
        "synonyms": ["Bitter Colchicum", "Hermodactyl Bitter", "Suranjan-e-Talkh"],
        "afal": ["Mus-hil-e-Balgham (Phlegm purgative)", "Muhallil-e-Awraam (Anti-inflammatory)", "Musakkin-e-Alam (Analgesic)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 3, "wd_degree": 3},
        "organ_axes": ["mafasil", "meda-amaa"],
        "traditional_uses": "Standard classical single drug for Waja-ul-Mafasil (arthralgia), Niqris (gout), and Irqun-Nasa (sciatica).",
        "contraindications": "Pregnancy, renal impairment, active peptic ulcer, ulcerative colitis.",
        "musleh": "Roghan-e-Badam, Kateera",
        "badal": "Suranjan Shireen, Bozidana",
        "dose": "250 mg - 500 mg (Mudabbar)",
        "is_schedule_e1": True,
        "modern_pharmacology": "Contains colchicine which binds unpolymerized tubulin, inhibiting microtubule dynamics and neutrophil extravasation.",
    },
    {
        "id": "upi-kuchla",
        "name": "Kuchla",
        "botanical_name": "Strychnos nux-vomica L.",
        "part_used": "Seeds",
        "synonyms": ["Azaraqi", "Nux Vomica", "Kupilu"],
        "afal": ["Muqawwi-e-Aasab (Nervine tonic)", "Muqawwi-e-Meda (Stomachic)", "Muharrik-e-Qalb (Cardiac stimulant)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 3, "wd_degree": 3},
        "organ_axes": ["dimagh-aasab", "meda-amaa", "qalb-uroq"],
        "traditional_uses": "Used in Falij (hemiplegia), Laqwa (facial paralysis), Rasha (tremors), and Zofe-Aasab (neurasthenia).",
        "contraindications": "Hypertension, cardiac arrhythmias, epilepsy, pregnancy, active nephritis.",
        "musleh": "Roghan-e-Zard (Ghee), Fresh cow milk",
        "badal": "Jadwar Khatai",
        "dose": "30 mg - 65 mg (Mudabbar)",
        "is_schedule_e1": True,
        "modern_pharmacology": "Strychnine is an antagonist at glycine receptors on motor neurons in spinal cord, enhancing neuronal excitability.",
    },
    {
        "id": "upi-asgandh",
        "name": "Asgandh",
        "botanical_name": "Withania somnifera (L.) Dunal",
        "part_used": "Root",
        "synonyms": ["Ashwagandha", "Winter Cherry", "Asgandh Nagori"],
        "afal": ["Muqawwi-e-Aam (General tonic)", "Muqawwi-e-Bah (Aphrodisiac)", "Musakkin-e-Aasab (Sedative/Nervine)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 2, "wd_degree": 2},
        "organ_axes": ["dimagh-aasab", "tabiyat", "khusyatain"],
        "traditional_uses": "Used for Zofe-Badan (general debility), Kla (fatigue), Zofe-Aasab, and insomnia.",
        "contraindications": "Hyperthyroidism, autoimmune flare-ups.",
        "musleh": "Gond Kateera, Shakkar (Raw sugar)",
        "badal": "Bahman Surkh, Salab Misri",
        "dose": "3 g - 5 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Withanolides (withaferin A, withanolide D) display GABA-mimetic, adaptogenic, and immunomodulatory activity.",
    },
    {
        "id": "upi-zanjabeel",
        "name": "Zanjabeel",
        "botanical_name": "Zingiber officinale Roscoe",
        "part_used": "Dried rhizome",
        "synonyms": ["Ginger", "Sonth", "Adrak"],
        "afal": ["Hazim (Digestive)", "Kasir-e-Riyah (Carminative)", "Muqawwi-e-Hafiza (Memory booster)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 3, "wd_degree": 2},
        "organ_axes": ["meda-amaa", "dimagh-aasab"],
        "traditional_uses": "Indicated in Su-e-Hazm (dyspepsia), Nafakh-e-Shikam (flatulence), and Balghami cough.",
        "contraindications": "Active gastric bleeding, cholelithiasis, concurrently with high-dose anticoagulants.",
        "musleh": "Roghan-e-Badam, Honey",
        "badal": "Darfulful (Piper retrofractum)",
        "dose": "1 g - 2 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Gingerols and shogaols inhibit COX-2 and 5-LOX, suppress NF-kappaB, and accelerate gastric emptying.",
    },
    {
        "id": "upi-filfil-siyah",
        "name": "Filfil Siyah",
        "botanical_name": "Piper nigrum L.",
        "part_used": "Dried unripe fruit",
        "synonyms": ["Black Pepper", "Kali Mirch", "Gol Mirch"],
        "afal": ["Jali (Detergent)", "Hazim (Digestive)", "Muqawwi-e-Meda (Stomachic)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 3, "wd_degree": 3},
        "organ_axes": ["meda-amaa", "riya-sadr"],
        "traditional_uses": "Used for respiratory congestion, cold phlegmatic dyscrasias, and sluggish digestion.",
        "contraindications": "Severe gastritis, peptic ulceration, hyperacidity.",
        "musleh": "Roghan-e-Zaitoon (Olive oil), Fresh milk",
        "badal": "Zanjabeel, Peepal (Piper longum)",
        "dose": "500 mg - 1 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Piperine enhances hepatic and intestinal drug bioavailability by inhibiting CYP3A4 and P-glycoprotein.",
    },
    {
        "id": "upi-asal-us-soos",
        "name": "Asal-us-Soos",
        "botanical_name": "Glycyrrhiza glabra L.",
        "part_used": "Stolon and root",
        "synonyms": ["Licorice", "Mulethi", "Irq-us-Soos"],
        "afal": ["Mulaqqin-e-Halaq (Throat demulcent)", "Munaffis-e-Balgham (Expectorant)", "Muhallil (Resolvent)"],
        "mizaj": {"temperament": "Damwi", "quality": "Hot & Wet (Near Motadil)", "hc_degree": 1, "wd_degree": 1},
        "organ_axes": ["riya-sadr", "meda-amaa"],
        "traditional_uses": "Cough, hoarseness of voice (Baha-us-Sawt), gastric ulcers, and pharyngitis.",
        "contraindications": "Hypertension, chronic kidney disease, hypokalemia, congestive heart failure.",
        "musleh": "Gul-e-Surkh (Rose petals), Kateera",
        "badal": "Katheera, Samagh-e-Arabi",
        "dose": "3 g - 5 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Glycyrrhizin inhibits 11-beta-hydroxysteroid dehydrogenase type 2, resulting in mineralocorticoid excess and potassium loss.",
    },
    {
        "id": "upi-sana-makki",
        "name": "Sana Makki",
        "botanical_name": "Cassia angustifolia M.Vahl",
        "part_used": "Dried leaflets",
        "synonyms": ["Senna", "Barg-e-Sana", "Sanay"],
        "afal": ["Mus-hil-e-Safra wa Balgham (Purgative of yellow bile and phlegm)", "Tanqia-e-Meda (Gastric cleanser)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 1, "wd_degree": 2},
        "organ_axes": ["meda-amaa"],
        "traditional_uses": "Relieves chronic Qabz (constipation) and cleanses morbid humors.",
        "contraindications": "Intestinal obstruction, acute inflammatory bowel diseases, appendicitis, pregnancy.",
        "musleh": "Anisoon (Pimpinella anisum), Gulqand, Roghan-e-Badam",
        "badal": "Turbud Safed",
        "dose": "3 g - 7 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Sennosides A and B are converted by colonic bacteria into rheinanthrone, which stimulates colonic peristalsis.",
    },
    {
        "id": "upi-ustukhuddus",
        "name": "Ustukhuddus",
        "botanical_name": "Lavandula stoechas L.",
        "part_used": "Dried inflorescence",
        "synonyms": ["Arabian Lavender", "Jarub-e-Dimagh (Broom of the Brain)"],
        "afal": ["Tanqia-e-Dimagh (Brain purifier)", "Mufattih-e-Sudad (Deobstruent)", "Muqawwi-e-Aasab (Nervine)"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 1, "wd_degree": 2},
        "organ_axes": ["dimagh-aasab"],
        "traditional_uses": "Premier classical cephalic medicine for Suda-e-Barid (cold headache), Shafiqah (migraine), and chronic sinusitis.",
        "contraindications": "Bleeding disorders, concurrent CNS depressant sedative use.",
        "musleh": "Kateera, Lemon juice",
        "badal": "Aftimoon (Cuscuta reflexa)",
        "dose": "3 g - 7 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Linalool, camphor, and 1,8-cineole modulate GABA-A receptors, exerting neuroprotective and anxiolytic actions.",
    },
    {
        "id": "upi-kalonji",
        "name": "Kalonji",
        "botanical_name": "Nigella sativa L.",
        "part_used": "Seeds",
        "synonyms": ["Black Seed", "Habbat-ul-Barakah", "Black Cumin"],
        "afal": ["Mudir-e-Baul wa Tams (Diuretic and emmenagogue)", "Qatil-e-Kirm-e-Shikam (Anthelmintic)", "Kasir-e-Riyah"],
        "mizaj": {"temperament": "Safrawi", "quality": "Hot & Dry", "hc_degree": 2, "wd_degree": 2},
        "organ_axes": ["tabiyat", "riya-sadr", "meda-amaa"],
        "traditional_uses": "Used for respiratory infections, digestive weakness, immune debility, and skin disorders.",
        "contraindications": "Large therapeutic doses during pregnancy.",
        "musleh": "Sirka (Vinegar), Roghan-e-Kunjad",
        "badal": "Zeera Siyah",
        "dose": "1 g - 3 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Thymoquinone exhibits antioxidant, anti-inflammatory, histone deacetylase inhibitory, and bronchodilator activity.",
    },
    {
        "id": "upi-gokhru",
        "name": "Gokhru",
        "botanical_name": "Tribulus terrestris L.",
        "part_used": "Dried spiny fruit",
        "synonyms": ["Khar-e-Khasak", "Puncture Vine", "Gokshura"],
        "afal": ["Mudir-e-Baul (Diuretic)", "Mufattit-e-Hasat (Lithotriptic)", "Muqawwi-e-Bah (Aphrodisiac)"],
        "mizaj": {"temperament": "Damwi", "quality": "Hot & Wet (Moderate)", "hc_degree": 1, "wd_degree": 1},
        "organ_axes": ["meda-amaa", "khusyatain"],
        "traditional_uses": "Indicated in Hasat-e-Kulyah wa Masana (renal/vesical calculi), Usr-ul-Baul (dysuria), and burning micturition.",
        "contraindications": "Prostatic hypertrophy with acute retention.",
        "musleh": "Roghan-e-Badam, Honey",
        "badal": "Kaknaj, Beikh-e-Kasni",
        "dose": "5 g - 10 g",
        "is_schedule_e1": False,
        "modern_pharmacology": "Protodioscin and furostanol saponins promote nitric oxide release, increase glomerular filtration, and inhibit calcium oxalate crystallization.",
    },
]

# ============================================================================
# 3. NFUM CLASSICAL COMPOUND FORMULATIONS (MURAKKABAT) REGISTER
# ============================================================================
NFUM_COMPOUND_REGISTRY: list[dict[str, Any]] = [
    {
        "id": "nfum-majun-suranjan",
        "name": "Majun Suranjan",
        "urdu_name": "معجون سورنجان",
        "category": "Majun (Confection)",
        "classical_indication": "Waja-ul-Mafasil (Joint pain), Niqris (Gout), Irqun-Nasa (Sciatica)",
        "key_ingredients": [
            {"name": "Suranjan Talkh Mudabbar", "is_schedule_e1": True},
            {"name": "Zanjabeel", "is_schedule_e1": False},
            {"name": "Filfil Siyah", "is_schedule_e1": False},
            {"name": "Turbud Safed", "is_schedule_e1": False},
            {"name": "Post-e-Halela Zard", "is_schedule_e1": False},
            {"name": "Asal / Qand Safed", "is_schedule_e1": False},
        ],
        "dose": "5 g to 10 g with warm water at bedtime",
        "schedule_e1_warning": True,
        "precautions": "Contains Schedule E(1) Suranjan Talkh. Avoid during pregnancy, renal failure, or active colitis.",
    },
    {
        "id": "nfum-habb-e-suranjan",
        "name": "Habb-e-Suranjan",
        "urdu_name": "حب سورنجان",
        "category": "Habb (Pill/Tablet)",
        "classical_indication": "Acute arthritis, gout flare-up, backache, inflammatory rheumatic conditions",
        "key_ingredients": [
            {"name": "Suranjan Talkh Mudabbar", "is_schedule_e1": True},
            {"name": "Elwa (Aloe vera extract)", "is_schedule_e1": False},
            {"name": "Jalapa", "is_schedule_e1": False},
        ],
        "dose": "1 to 2 pills (250mg each) twice daily",
        "schedule_e1_warning": True,
        "precautions": "Strictly Mudabbar Suranjan. Monitor for loose stools and abdominal cramping.",
    },
    {
        "id": "nfum-habb-e-asab",
        "name": "Habb-e-Asab",
        "urdu_name": "حب اعصاب",
        "category": "Habb (Pill/Tablet)",
        "classical_indication": "Falij (Hemiplegia), Laqwa (Facial Palsy), Zofe-Aasab (Nervine weakness), Neurasthenia",
        "key_ingredients": [
            {"name": "Kuchla Mudabbar", "is_schedule_e1": True},
            {"name": "Filfil Siyah", "is_schedule_e1": False},
            {"name": "Zanjabeel", "is_schedule_e1": False},
        ],
        "dose": "1 pill (65mg) once daily after meals with milk",
        "schedule_e1_warning": True,
        "precautions": "SCHEDULE E(1) POISON: Contains Kuchla Mudabbar. Do not exceed 1 pill daily. Never give to patients with hypertension or epilepsy.",
    },
    {
        "id": "nfum-itrifal-kishneezi",
        "name": "Itrifal Kishneezi",
        "urdu_name": "اطریفل کشنیزی",
        "category": "Itrifal",
        "classical_indication": "Suda (Headache), Nazla wa Zukam (Chronic catarrh), weakness of stomach, flatulence",
        "key_ingredients": [
            {"name": "Post-e-Halela Zard", "is_schedule_e1": False},
            {"name": "Post-e-Halela Siyah", "is_schedule_e1": False},
            {"name": "Post-e-Balela", "is_schedule_e1": False},
            {"name": "Amla", "is_schedule_e1": False},
            {"name": "Kishneez Khushk (Coriander seeds)", "is_schedule_e1": False},
            {"name": "Roghan-e-Badam", "is_schedule_e1": False},
            {"name": "Shahad (Honey)", "is_schedule_e1": False},
        ],
        "dose": "5 g to 10 g at bedtime with warm water or milk",
        "schedule_e1_warning": False,
        "precautions": "Gentle, non-toxic formulation. Safe for long-term use.",
    },
    {
        "id": "nfum-itrifal-ustukhuddus",
        "name": "Itrifal Ustukhuddus",
        "urdu_name": "اطریفل اسطخودوس",
        "category": "Itrifal",
        "classical_indication": "Tanqia-e-Dimagh (Purification of the brain from phlegm and melancholia), migraine, chronic sinusitis",
        "key_ingredients": [
            {"name": "Ustukhuddus", "is_schedule_e1": False},
            {"name": "Halela Siyah", "is_schedule_e1": False},
            {"name": "Post-e-Halela Zard", "is_schedule_e1": False},
            {"name": "Post-e-Balela", "is_schedule_e1": False},
            {"name": "Amla", "is_schedule_e1": False},
            {"name": "Aftimoon", "is_schedule_e1": False},
        ],
        "dose": "5 g to 10 g at bedtime",
        "schedule_e1_warning": False,
        "precautions": "Mild laxative effect due to Halela and Balela.",
    },
    {
        "id": "nfum-jawarish-kamuni",
        "name": "Jawarish Kamuni",
        "urdu_name": "جوارش کمونی",
        "category": "Jawarish",
        "classical_indication": "Nafakh-e-Shikam (Meteorism/flatulence), Qulanj (Colic), Su-e-Hazm (Dyspepsia)",
        "key_ingredients": [
            {"name": "Zeera Siyah Mudabbar (Carum carvi)", "is_schedule_e1": False},
            {"name": "Filfil Siyah", "is_schedule_e1": False},
            {"name": "Zanjabeel", "is_schedule_e1": False},
            {"name": "Barg-e-Sudab", "is_schedule_e1": False},
            {"name": "Darchini", "is_schedule_e1": False},
        ],
        "dose": "5 g after meals twice daily",
        "schedule_e1_warning": False,
        "precautions": "Contains carminative spices; exercise caution in severe active peptic ulcers.",
    },
    {
        "id": "nfum-sharbat-bazoori-motadil",
        "name": "Sharbat Bazoori Motadil",
        "urdu_name": "شربت بزوری معتدل",
        "category": "Sharbat (Syrup)",
        "classical_indication": "Usr-ul-Baul (Dysuria), burning micturition, fever, liver and kidney clearance",
        "key_ingredients": [
            {"name": "Tukhm-e-Khyarain (Cucumber seeds)", "is_schedule_e1": False},
            {"name": "Tukhm-e-Kharbuza (Melon seeds)", "is_schedule_e1": False},
            {"name": "Tukhm-e-Kasni (Chicory seeds)", "is_schedule_e1": False},
            {"name": "Beikh-e-Kasni (Chicory root)", "is_schedule_e1": False},
            {"name": "Beikh-e-Badiyan (Fennel root)", "is_schedule_e1": False},
        ],
        "dose": "25 ml to 50 ml mixed with warm water twice daily",
        "schedule_e1_warning": False,
        "precautions": "Contains sugar syrup; diabetics require sugar-free decoction alternative (Joshanda Bazoori).",
    },
    {
        "id": "nfum-khamira-abresham-hakim-arshad-wala",
        "name": "Khamira Abresham Hakim Arshad Wala",
        "urdu_name": "خمیرہ ابریشم حکیم ارشد والا",
        "category": "Khamira",
        "classical_indication": "Khafqan (Palpitations), Zofe-Qalb (Cardiac weakness), Melancholia, Convalescence",
        "key_ingredients": [
            {"name": "Abresham Muqarraz (Raw silk)", "is_schedule_e1": False},
            {"name": "Zafran (Saffron)", "is_schedule_e1": False},
            {"name": "Kushta-e-Marwareed (Pearl calx)", "is_schedule_e1": False},
            {"name": "Kushta-e-Yaqoot (Ruby calx)", "is_schedule_e1": False},
            {"name": "Ambar", "is_schedule_e1": False},
            {"name": "Ood Gharqi (Agarwood)", "is_schedule_e1": False},
        ],
        "dose": "3 g to 5 g morning on empty stomach with milk",
        "schedule_e1_warning": False,
        "precautions": "Premier cardio-cerebral tonic. Safe when prepared according to standard GMP.",
    },
    {
        "id": "nfum-majun-falasifa",
        "name": "Majun Falasifa",
        "urdu_name": "معجون فلاسفہ",
        "category": "Majun",
        "canonical_reference": "Ibn Sina, Al-Qanun fi al-Tibb, Vol. 5; Qarabadin-e-Azam",
        "classical_indication": "Zof-e-Kulliya wa Masana (Renal and vesical debility), incontinence, Zof-e-Bah, Zof-e-Asab, geriatric tonification",
        "organ_axes": ["kulliya-masana", "dimagh-asab", "jinsi-tawallud"],
        "key_ingredients": [
            {"name": "Zanjabeel (Ginger)", "is_schedule_e1": False},
            {"name": "Filfil Siyah (Black Pepper)", "is_schedule_e1": False},
            {"name": "Filfil Daraz (Long Pepper)", "is_schedule_e1": False},
            {"name": "Darchini (Cinnamon)", "is_schedule_e1": False},
            {"name": "Baboona (Chamomile)", "is_schedule_e1": False},
            {"name": "Zarawand Mudaharraj", "is_schedule_e1": False},
            {"name": "Salab Misri (Orchis mascula)", "is_schedule_e1": False},
            {"name": "Maghz-e-Chilgoza (Pine nut)", "is_schedule_e1": False},
            {"name": "Maghz-e-Narjeel (Coconut kernel)", "is_schedule_e1": False},
            {"name": "Post-e-Bekh-e-Babool", "is_schedule_e1": False},
        ],
        "dose": "5 g to 10 g once daily in the morning with 250 ml milk",
        "schedule_e1_warning": False,
        "precautions": "Warm-natured polyherbal compound; use with caution in extreme Safrawi (choleric) temperaments.",
        "modernization_tags": {
            "diabetic_friendly_alternative": "Sugar-free standardized dry extract capsule (500mg BD)",
            "stability_profile": "Standard electuary in honey base, 24 months shelf life at room temperature",
        },
    },
    {
        "id": "nfum-safoof-mohazzil",
        "name": "Safoof Mohazzil",
        "urdu_name": "سفوف مہزل",
        "category": "Safoof (Powder)",
        "canonical_reference": "Kabiruddin, Biaz-e-Kabir, Vol. 2; NFUM Vol. I",
        "classical_indication": "Siman-e-Mufrit (Obesity/Metabolic Syndrome), excess Balgham stasis, hypercholesterolemia",
        "organ_axes": ["kabid-tihal", "meda-amaa", "mizaj-am"],
        "key_ingredients": [
            {"name": "Burada-e-Lakh (Purified Lac)", "is_schedule_e1": False},
            {"name": "Marzanjoosh (Majorana)", "is_schedule_e1": False},
            {"name": "Badiyan (Fennel seed)", "is_schedule_e1": False},
            {"name": "Zeera Siyah (Black Caraway)", "is_schedule_e1": False},
            {"name": "Barg-e-Sudab (Rue leaf)", "is_schedule_e1": False},
            {"name": "Tukhm-e-Kasoos (Dodder seed)", "is_schedule_e1": False},
        ],
        "dose": "3 g to 5 g twice daily after meals with Arq-e-Zeera or warm water",
        "schedule_e1_warning": False,
        "precautions": "Contraindicated in pregnancy due to Sudab emmenagogue properties. Ensure adequate hydration.",
        "modernization_tags": {
            "diabetic_friendly_alternative": "Naturally sugar-free formulation",
            "standardized_extract_equivalent": "Safoof Mohazzil film-coated tablets (500mg BD)",
        },
    },
    {
        "id": "nfum-tiryaq-e-arbaa",
        "name": "Tiryaq-e-Arba'a",
        "urdu_name": "تریاق اربعہ",
        "category": "Tiryaq (Theriac / Electuary)",
        "canonical_reference": "Galen, De Antidotis; Ibn Sina, Al-Qanun fi al-Tibb, Vol. 5",
        "classical_indication": "Ancient four-ingredient antidote, apoplexy prophylaxis, Falij (Hemiplegia), Laqwa, bite of venomous animals",
        "organ_axes": ["dimagh-asab", "qalb", "mizaj-am"],
        "key_ingredients": [
            {"name": "Hab-ul-Ghar (Laurel berry / Laurus nobilis)", "is_schedule_e1": False},
            {"name": "Habb-ul-Balsan (Balsamodendron fruit)", "is_schedule_e1": False},
            {"name": "Zarawand Taweel (Aristolochia longa)", "is_schedule_e1": False},
            {"name": "Murr Makki (Myrrh / Commiphora myrrha)", "is_schedule_e1": False},
        ],
        "dose": "2 g to 4 g with warm water or Joshanda Badiyan",
        "schedule_e1_warning": False,
        "precautions": "Contains potent resinous bitters; avoid in severe renal parenchymal disease.",
        "modernization_tags": {
            "stability_profile": "Extremely stable classical theriac; historical potency maintained over decades",
        },
    },
    {
        "id": "nfum-khamira-gaozaban-ambari",
        "name": "Khamira Gaozaban Ambari Jadwar Ood Saleeb Wala",
        "urdu_name": "خمیرہ گاؤزباں عنبری جدوار عود صلیب والا",
        "category": "Khamira",
        "canonical_reference": "Azam Khan, Qarabadin-e-Azam; NFUM Vol. I",
        "classical_indication": "Sara (Epilepsy), Ikhtenaq-ur-Rahm (Hysteria/Psychogenic Seizures), Khafqan (Palpitations), neurosis, convalescence",
        "organ_axes": ["dimagh-asab", "qalb"],
        "key_ingredients": [
            {"name": "Gaozaban (Borago officinalis)", "is_schedule_e1": False},
            {"name": "Gul-e-Gaozaban (Borage flowers)", "is_schedule_e1": False},
            {"name": "Kishneez Khushk (Coriander)", "is_schedule_e1": False},
            {"name": "Abresham (Silk cocoon)", "is_schedule_e1": False},
            {"name": "Jadwar Khatai (Delphinium denudatum)", "is_schedule_e1": False},
            {"name": "Ood Saleeb (Paeonia emodi root)", "is_schedule_e1": False},
            {"name": "Ambar Ash-hab (Ambergris)", "is_schedule_e1": False},
            {"name": "Marwareed (Pearl)", "is_schedule_e1": False},
        ],
        "dose": "3 g to 5 g morning on empty stomach with Arq-e-Gaozaban or milk",
        "schedule_e1_warning": False,
        "precautions": "Premier neuro-cerebral restorative. Safe and non-sedating neuroprotective formulation.",
        "modernization_tags": {
            "diabetic_friendly_alternative": "Khamira Gaozaban sugar-free suspension with sorbitol base",
        },
    },
    {
        "id": "nfum-sharbat-zoofa-murakkab",
        "name": "Sharbat Zoofa Murakkab",
        "urdu_name": "شربت زوفا مرکب",
        "category": "Sharbat (Syrup)",
        "canonical_reference": "Ibn Sina, Al-Qanun fi al-Tibb, Vol. 5; Biaz-e-Kabir",
        "classical_indication": "Diq-un-Nafas (Bronchial Asthma), Sual-e-Balghami (Productive phlegmatic cough), Tanqia-e-Riya (Pulmonary clearance)",
        "organ_axes": ["tanaffus", "qalb"],
        "key_ingredients": [
            {"name": "Zoofa Khushk (Hyssopus officinalis)", "is_schedule_e1": False},
            {"name": "Asl-us-Soos (Glycyrrhiza glabra)", "is_schedule_e1": False},
            {"name": "Anjeer Zard (Dry Ficus carica)", "is_schedule_e1": False},
            {"name": "Tukhm-e-Khatmi (Althaea officinalis seeds)", "is_schedule_e1": False},
            {"name": "Bekh-e-Khatmi (Althaea officinalis root)", "is_schedule_e1": False},
        ],
        "dose": "20 ml to 40 ml diluted in warm water twice daily",
        "schedule_e1_warning": False,
        "precautions": "Contains Glycyrrhiza; monitor blood pressure in chronic severe hypertensive patients.",
        "modernization_tags": {
            "diabetic_friendly_alternative": "Joshanda Zoofa (sugar-free decoction brew)",
        },
    },
    {
        "id": "nfum-habb-e-shifa",
        "name": "Habb-e-Shifa",
        "urdu_name": "حب شفاء",
        "category": "Habb (Pill/Tablet)",
        "canonical_reference": "Qarabadin-e-Azam; NFUM Vol. I",
        "classical_indication": "Humma-e-Ajamiya (Malaria / Periodic fevers), Suda (Headache), acute inflammatory pain",
        "organ_axes": ["dimagh-asab", "mizaj-am", "kabid-tihal"],
        "key_ingredients": [
            {"name": "Tukhm-e-Dhatura Mudabbar (Datura fastuosa seed, purified)", "is_schedule_e1": True},
            {"name": "Rewand Chini (Rheum emodi root)", "is_schedule_e1": False},
            {"name": "Zanjabeel (Zingiber officinale)", "is_schedule_e1": False},
            {"name": "Samagh-e-Arabi (Acacia gum binder)", "is_schedule_e1": False},
        ],
        "dose": "1 pill (125 mg) once daily with water; never exceed 1 pill",
        "schedule_e1_warning": True,
        "precautions": "SCHEDULE E(1) POISON: Contains Dhatura Mudabbar (tropane alkaloids). Strictly contraindicated in glaucoma, prostatic hypertrophy, tachyarrhythmias, and pregnancy.",
        "modernization_tags": {
            "stability_profile": "Blister packed tablets, store in dry cool place protected from light",
            "standardized_extract_equivalent": "Strictly limited to certified GMP Mudabbar batch with validated atropine/scopolamine assay",
        },
    },
]

# ============================================================================
# 4. LOOKUP & QUERY API HELPERS
# ============================================================================
def get_schedule_e1_poisons() -> dict[str, dict[str, Any]]:
    return SCHEDULE_E1_POISONS


def match_schedule_e1_substance(name: str) -> dict[str, Any] | None:
    target = name.strip().lower()
    for key, data in SCHEDULE_E1_POISONS.items():
        if target == key or target == data["canonical_name"].lower():
            return data
        if any(syn.lower() in target or target in syn.lower() for syn in data["synonyms"]):
            return data
        if data["botanical_name"].lower().split()[0] in target:
            return data
    return None


_EXPANDED_MUFRADAT_CACHE: list[dict[str, Any]] | None = None


def _build_expanded_mufradat_catalog() -> list[dict[str, Any]]:
    global _EXPANDED_MUFRADAT_CACHE
    if _EXPANDED_MUFRADAT_CACHE is not None:
        return _EXPANDED_MUFRADAT_CACHE

    items = list(UPI_MUFRADAT_REGISTRY)
    existing_ids = {m["id"].lower() for m in items}
    existing_names = {m["name"].lower() for m in items}

    try:
        from services.knowledge.app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
    except ImportError:
        try:
            from app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
        except ImportError:
            GOLD_BENCHMARK_25_MONOGRAPHS = {}

    for zid, mono in GOLD_BENCHMARK_25_MONOGRAPHS.items():
        c_ident = mono.get("canonical_identity", {})
        c_prof = mono.get("classical_profile", {})
        s_fire = mono.get("safety_firewall", {})
        m_evid = mono.get("modern_evidence", {})

        canonical_name = c_ident.get("canonical_unani_name", zid)
        if zid.lower() in existing_ids or canonical_name.lower() in existing_names:
            continue

        # Parse temperament & quality
        mizaj_raw = c_prof.get("mizaj", "Muaddil")
        daraja_raw = str(c_prof.get("daraja", "1"))
        m_lower = mizaj_raw.lower()
        if "garm" in m_lower or "hot" in m_lower:
            if "khushk" in m_lower or "dry" in m_lower:
                temp, qual = "Safrawi", "Hot & Dry"
            else:
                temp, qual = "Damwi", "Hot & Wet"
        elif "sard" in m_lower or "cold" in m_lower:
            if "khushk" in m_lower or "dry" in m_lower:
                temp, qual = "Saudawi", "Cold & Dry"
            else:
                temp, qual = "Balghami", "Cold & Wet"
        else:
            temp, qual = "Damwi", "Moderate (Muaddil)"

        deg = 1
        for char in daraja_raw:
            if char.isdigit():
                deg = int(char)
                break

        axes = []
        for aff in mono.get("organ_axis_affinity", []):
            aff_l = aff.lower()
            if "jigar" in aff_l or "hepato" in aff_l:
                axes.append("jigar-banas")
            elif "dimagh" in aff_l or "neuro" in aff_l:
                axes.append("dimagh-aasab")
            elif "qalb" in aff_l or "cardio" in aff_l:
                axes.append("qalb-uroq")
            elif "riya" in aff_l or "pulmonary" in aff_l or "broncho" in aff_l:
                axes.append("riya-sadr")
            elif "meda" in aff_l or "gastro" in aff_l:
                axes.append("meda-amaa")
            elif "kulyatain" in aff_l or "nephro" in aff_l:
                axes.append("ghudad-hazm")
            elif "khusyatain" in aff_l or "male" in aff_l:
                axes.append("khusyatain")
            elif "reham" in aff_l or "female" in aff_l:
                axes.append("reham-mabaysim")
            elif "mafasil" in aff_l or "joint" in aff_l or "musculo" in aff_l:
                axes.append("mafasil")
            elif "jild" in aff_l or "dermato" in aff_l or "skin" in aff_l:
                axes.append("shaar-jigar")
            elif "tihal" in aff_l or "spleno" in aff_l or "thyroid" in aff_l:
                axes.append("ghudda-mithana")
            elif "vital" in aff_l or "longevity" in aff_l or "tabiyat" in aff_l:
                axes.append("tabiyat")
        if not axes:
            axes.append("tabiyat")

        musleh_val = c_prof.get("musleh", "")
        musleh_str = ", ".join(musleh_val) if isinstance(musleh_val, list) else str(musleh_val or "")
        badal_val = c_prof.get("badal", "")
        badal_str = ", ".join(badal_val) if isinstance(badal_val, list) else str(badal_val or "")

        contra_val = s_fire.get("contraindications", [])
        contra_str = "; ".join(contra_val) if isinstance(contra_val, list) else str(contra_val or "None listed")

        synonyms = list(c_ident.get("synonyms", []))
        if c_ident.get("urdu_name") and c_ident.get("urdu_name") not in synonyms:
            synonyms.append(c_ident.get("urdu_name"))
        if c_ident.get("arabic_name") and c_ident.get("arabic_name") not in synonyms:
            synonyms.append(c_ident.get("arabic_name"))

        items.append({
            "id": zid,
            "name": canonical_name,
            "botanical_name": c_ident.get("botanical_name", ""),
            "part_used": c_ident.get("part_used", ""),
            "synonyms": synonyms,
            "afal": c_prof.get("afaal", []),
            "mizaj": {
                "temperament": temp,
                "quality": qual,
                "hc_degree": deg,
                "wd_degree": deg,
            },
            "organ_axes": axes,
            "traditional_uses": f"Classical indication: {', '.join(c_prof.get('afaal', [])[:4])}.",
            "contraindications": contra_str,
            "musleh": musleh_str,
            "badal": badal_str,
            "dose": c_prof.get("dosage_context", "3g to 5g daily"),
            "is_schedule_e1": s_fire.get("is_schedule_e1", False),
            "modern_pharmacology": f"Constituents: {', '.join(m_evid.get('primary_constituents', [])[:3])}. Evidence: {m_evid.get('evidence_grade', 'MODERATE')}.",
        })
        existing_ids.add(zid.lower())
        existing_names.add(canonical_name.lower())

    _EXPANDED_MUFRADAT_CACHE = items
    return _EXPANDED_MUFRADAT_CACHE


def get_upi_mufradat() -> list[dict[str, Any]]:
    return _build_expanded_mufradat_catalog()


def get_mufrad_by_name(name: str) -> dict[str, Any] | None:
    catalog = _build_expanded_mufradat_catalog()
    target = name.strip().lower()
    for item in catalog:
        if item["name"].lower() == target or item["id"].lower() == target:
            return item
        if any(s.lower() == target for s in item.get("synonyms", [])):
            return item
        if target in item["name"].lower() or item["name"].lower() in target:
            return item
    return None


try:
    try:
        from services.knowledge.app.core.upi_vol4_monographs import (
            UPI_PART2_VOL4_MONOGRAPHS,
            CLASSICAL_WEIGHTS_METRIC_MAP,
            convert_classical_weight,
            TADBIR_E_ADVIYAH_SOP,
            CANONICAL_LIBRARY_REGISTRY,
            get_upi_vol4_compound_by_name,
            get_all_upi_vol4_monographs,
        )
    except ImportError:
        from app.core.upi_vol4_monographs import (
            UPI_PART2_VOL4_MONOGRAPHS,
            CLASSICAL_WEIGHTS_METRIC_MAP,
            convert_classical_weight,
            TADBIR_E_ADVIYAH_SOP,
            CANONICAL_LIBRARY_REGISTRY,
            get_upi_vol4_compound_by_name,
            get_all_upi_vol4_monographs,
        )
except Exception:
    UPI_PART2_VOL4_MONOGRAPHS = []
    CLASSICAL_WEIGHTS_METRIC_MAP = {}
    convert_classical_weight = lambda q, u: {"quantity": q, "unit": u}
    TADBIR_E_ADVIYAH_SOP = {}
    CANONICAL_LIBRARY_REGISTRY = {}
    get_upi_vol4_compound_by_name = lambda x: None
    get_all_upi_vol4_monographs = lambda: []


def get_compound_formulations() -> list[dict[str, Any]]:
    compounds_map = {comp["id"]: comp for comp in NFUM_COMPOUND_REGISTRY}
    try:
        try:
            from services.knowledge.app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
        except ImportError:
            from app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
        for comp in CLASSICAL_MURAKKABAT_50:
            if comp["id"] not in compounds_map:
                compounds_map[comp["id"]] = comp
    except Exception:
        pass

    # Merge UPI Part-II, Vol-IV Statutory Compound Formulations (Ministry of AYUSH)
    try:
        for item in UPI_PART2_VOL4_MONOGRAPHS:
            clean_name = item["name"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace("'", "")
            cid = f"upi-v4-{clean_name}"
            if cid not in compounds_map:
                compounds_map[cid] = {
                    "id": cid,
                    "name": item["name"],
                    "urdu_name": item["urdu_name"],
                    "category": item["form"],
                    "classical_indication": ", ".join(item["therapeutic_uses"]),
                    "canonical_reference": f"Unani Pharmacopoeia of India Part-II, Vol-IV; {item.get('nfum_code', '')}",
                    "key_ingredients": [{"name": ing["ingredient"], "is_schedule_e1": ing.get("is_schedule_e1", False)} for ing in item.get("composition", [])],
                    "dose": item.get("dose", "") + " (" + item.get("mode_of_administration", "") + ")",
                    "schedule_e1_warning": item.get("schedule_e1_warning", False),
                    "precautions": f"UPI Part-II Vol-IV statutory standard. Physicochemical total ash max {item.get('physicochemical_specs', {}).get('total_ash_max_pct', 8)}%.",
                    "analytical_release_specs": {
                        "heavy_metals_ppm": {"lead_max": 10.0, "arsenic_max": 3.0, "cadmium_max": 0.3, "mercury_max": 1.0},
                        "total_ash_max_pct": item.get("physicochemical_specs", {}).get("total_ash_max_pct", 8.0),
                        "acid_insoluble_ash_max_pct": item.get("physicochemical_specs", {}).get("acid_insoluble_ash_max_pct", 2.0),
                        "tlc_rf_values": item.get("tlc_fingerprint", {}).get("rf_values", []),
                        "tlc_solvent_system": item.get("tlc_fingerprint", {}).get("solvent_system", ""),
                        "qc_specification_standard": "Unani Pharmacopoeia of India (UPI) Part-II, Vol-IV",
                    }
                }
    except Exception:
        pass

    return list(compounds_map.values())


def get_compound_by_name(name: str) -> dict[str, Any] | None:
    target = name.strip().lower()
    all_compounds = get_compound_formulations()
    for comp in all_compounds:
        if comp["name"].lower() == target or comp["id"] == target:
            return comp
        if target in comp["name"].lower() or comp["name"].lower() in target:
            return comp
    return None


WFO_POWO_TAXONOMY_MAP: dict[str, dict[str, str]] = {
    "upi-suranjan-talkh": {
        "wfo_id": "wfo-0000613248",
        "powo_id": "urn:lsid:ipni.org:names:533162-1",
        "family": "Colchicaceae",
        "accepted_name": "Colchicum luteum Baker",
    },
    "upi-kuchla": {
        "wfo_id": "wfo-0000494488",
        "powo_id": "urn:lsid:ipni.org:names:547285-1",
        "family": "Loganiaceae",
        "accepted_name": "Strychnos nux-vomica L.",
    },
    "upi-asgandh": {
        "wfo_id": "wfo-0001031317",
        "powo_id": "urn:lsid:ipni.org:names:821360-1",
        "family": "Solanaceae",
        "accepted_name": "Withania somnifera (L.) Dunal",
    },
    "upi-zanjabeel": {
        "wfo_id": "wfo-0000499632",
        "powo_id": "urn:lsid:ipni.org:names:798411-1",
        "family": "Zingiberaceae",
        "accepted_name": "Zingiber officinale Roscoe",
    },
    "upi-filfil-siyah": {
        "wfo_id": "wfo-0000486022",
        "powo_id": "urn:lsid:ipni.org:names:682498-1",
        "family": "Piperaceae",
        "accepted_name": "Piper nigrum L.",
    },
    "upi-asal-us-soos": {
        "wfo_id": "wfo-0000204781",
        "powo_id": "urn:lsid:ipni.org:names:496929-1",
        "family": "Fabaceae",
        "accepted_name": "Glycyrrhiza glabra L.",
    },
    "upi-sana-makki": {
        "wfo_id": "wfo-0000192837",
        "powo_id": "urn:lsid:ipni.org:names:484672-1",
        "family": "Fabaceae",
        "accepted_name": "Senna alexandrina Mill.",
    },
    "upi-ustukhuddus": {
        "wfo_id": "wfo-0000224192",
        "powo_id": "urn:lsid:ipni.org:names:449082-1",
        "family": "Lamiaceae",
        "accepted_name": "Lavandula stoechas L.",
    },
    "upi-haleela-zard": {
        "wfo_id": "wfo-0000321589",
        "powo_id": "urn:lsid:ipni.org:names:171092-1",
        "family": "Combretaceae",
        "accepted_name": "Terminalia chebula Retz.",
    },
    "upi-kishneez": {
        "wfo_id": "wfo-0000620831",
        "powo_id": "urn:lsid:ipni.org:names:840742-1",
        "family": "Apiaceae",
        "accepted_name": "Coriandrum sativum L.",
    },
    "upi-bhang": {
        "wfo_id": "wfo-0000584441",
        "powo_id": "urn:lsid:ipni.org:names:306087-2",
        "family": "Cannabaceae",
        "accepted_name": "Cannabis sativa L.",
    },
    "upi-bhilawa": {
        "wfo_id": "wfo-0000713401",
        "powo_id": "urn:lsid:ipni.org:names:70685-1",
        "family": "Anacardiaceae",
        "accepted_name": "Semecarpus anacardium L.f.",
    },
}

DEFAULT_ANALYTICAL_SPECS: dict[str, Any] = {
    "heavy_metals_ppm": {"lead_max": 10.0, "arsenic_max": 3.0, "cadmium_max": 0.3, "mercury_max": 1.0},
    "total_ash_max_pct": 8.0,
    "acid_insoluble_ash_max_pct": 2.0,
    "water_soluble_extractive_min_pct": 18.0,
    "alcohol_soluble_extractive_min_pct": 12.0,
    "microbial_limits": {"total_aerobic_count_max": 10000, "yeast_mold_max": 100, "e_coli": "absent", "salmonella": "absent"},
    "qc_specification_standard": "Unani Pharmacopoeia of India (UPI) / WHO Guidelines for Quality Control of Herbal Materials",
}

# Auto-enrich registries with WFO taxonomy and analytical release specs
for item in UPI_MUFRADAT_REGISTRY:
    tax = WFO_POWO_TAXONOMY_MAP.get(item["id"])
    if tax:
        item["wfo_id"] = tax["wfo_id"]
        item["powo_id"] = tax["powo_id"]
        item["family"] = tax["family"]
    else:
        item["wfo_id"] = ""
        item["powo_id"] = ""
        item["family"] = ""

for comp in NFUM_COMPOUND_REGISTRY:
    if "analytical_release_specs" not in comp:
        comp["analytical_release_specs"] = dict(DEFAULT_ANALYTICAL_SPECS)


def get_mufrad_by_wfo_id(wfo_id: str) -> dict[str, Any] | None:
    """Looks up a single drug by World Flora Online (WFO) identifier."""
    target = wfo_id.strip().lower()
    for item in UPI_MUFRADAT_REGISTRY:
        if item.get("wfo_id", "").lower() == target:
            return item
    return None


def get_compound_analytical_specs(name_or_id: str) -> dict[str, Any] | None:
    """Returns analytical quality control and release specifications for a Murakkab formulation."""
    comp = get_compound_by_name(name_or_id)
    if comp:
        return comp.get("analytical_release_specs")
    return None

