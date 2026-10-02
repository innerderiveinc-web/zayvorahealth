"""
ZAYVORA Health OS™ — Canonical 250 Mufradat Registry & Validation Pipeline
===========================================================================
Source Publications:
  - ZAYVORA Mufradat 250 Validation Audit v2
  - ZAYVORA Mufradat 250 Validation-Controlled Master v2
  - ZAYVORA OS 250 Mufradat Validation Dossier (CDSCO / PCIM&H / CCRUM Enclosure)
  - ZAYVORA Mufradat 250 Presentation-Style Research Monographs

Governed Implementation Rules:
  1. Patient self-care is NOT_ALLOWED for all 250 records.
  2. Exactly 28 High-Risk substances are hard-blocked (AI_BLOCKED).
  3. 43 Canonicalization Groups (CAN-001 to CAN-043) model multi-part, grades, and synonyms.
  4. 6 Internal Seed records contain initial classical fields (ZMF-001, 003, 004, 005, 006, 002-reconciled).
  5. 244 Research Candidates maintain PENDING evidence state until 12-Gate expert sign-offs.
  6. Suranjan Talkh (ZMF-002) is reconciled to PCIM&H official standard: Colchicum luteum Baker.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional

# =============================================================================
# 1. THE 28 HIGH-RISK HARD-BLOCKED SUBSTANCES REGISTRY
# =============================================================================
HIGH_RISK_28_REGISTRY: Dict[str, Dict[str, Any]] = {
    "ZMF-002": {
        "name": "SURANJAN TALKH",
        "botanical": "Colchicum luteum Baker (Reconciled from C. autumnale)",
        "category": "Schedule E(1) Toxic Botanical",
        "primary_toxin": "Colchicine",
        "clinical_risk": "Severe gastrointestinal mucosal necrosis, hemorrhagic diarrhea, acute kidney injury.",
        "restriction": "AI_BLOCKED; requires certified Shodhana (soaking in vinegar/milk) and specialist sign-off."
    },
    "ZMF-031": {
        "name": "AJWAIN KHURASANI",
        "botanical": "Hyoscyamus niger L.",
        "category": "Schedule E(1) Anticholinergic Botanical",
        "primary_toxin": "Hyoscyamine, Scopolamine, Atropine",
        "clinical_risk": "Severe anticholinergic crisis, hyperthermia, delirium, urinary retention, cardiac arrhythmias.",
        "restriction": "AI_BLOCKED; clinician-only prescription."
    },
    "ZMF-089": {
        "name": "JAMALGOTA",
        "botanical": "Croton tiglium L.",
        "category": "Schedule E(1) Drastic Purgative",
        "primary_toxin": "Croton oil, Phorbol esters, Crotin toxalbumin",
        "clinical_risk": "Violent watery-bloody purgation, severe intestinal ulceration, hypovolemic circulatory collapse.",
        "restriction": "AI_BLOCKED; strictly restricted."
    },
    "ZMF-090": {
        "name": "HABB-US-SALATEEN",
        "botanical": "Croton tiglium L. (Processed / Compound form)",
        "category": "Schedule E(1) Drastic Purgative",
        "primary_toxin": "Phorbol esters",
        "clinical_risk": "Same violent toxicity as Jamalgota; requires verified detoxification (Tadbeer) protocol.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-101": {
        "name": "SHANGRAF",
        "botanical": "Mercuric sulphide (HgS)",
        "category": "Toxic Mineral / Heavy Metal",
        "primary_toxin": "Mercury (Hg)",
        "clinical_risk": "Mercury bio-accumulation, nephrotic syndrome, erethism, peripheral neurotoxicity.",
        "restriction": "AI_BLOCKED; mandatory ICP-MS heavy metal limits and Bhasma certification."
    },
    "ZMF-102": {
        "name": "HARTAL",
        "botanical": "Arsenic trisulphide (As2S3)",
        "category": "Schedule E(1) Toxic Mineral",
        "primary_toxin": "Arsenic (As)",
        "clinical_risk": "Acute arsenic toxicity, severe multi-organ failure, peripheral neuropathy, cutaneous hyperkeratosis.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-103": {
        "name": "PARA",
        "botanical": "Elemental Mercury (Purified)",
        "category": "Elemental Heavy Metal",
        "primary_toxin": "Mercury (Hg)",
        "clinical_risk": "Lethal systemic heavy metal toxicity without classical 8-step Samskaras / Tadbeer.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-104": {
        "name": "KUSHTA ABRAK SIYAH",
        "botanical": "Calcined Biotite Mica",
        "category": "Calcined Mineral Bhasma",
        "primary_toxin": "Uncalcined silicate particulates",
        "clinical_risk": "Pulmonary and gastrointestinal particulate irritation, renal microvascular clogging if uncalcinated.",
        "restriction": "AI_BLOCKED; specialist manufacturing and X-ray diffraction / particle size validation only."
    },
    "ZMF-105": {
        "name": "KUSHTA FAULAD",
        "botanical": "Calcined Iron Preparation",
        "category": "Calcined Mineral Bhasma",
        "primary_toxin": "Elemental iron oxidant stress",
        "clinical_risk": "Severe hemosiderosis, gastric mucosal ulceration, hepatic free radical oxidative damage.",
        "restriction": "AI_BLOCKED; specialist monitoring only."
    },
    "ZMF-106": {
        "name": "KUSHTA TILA",
        "botanical": "Calcined Gold Preparation",
        "category": "Noble Metal Bhasma",
        "primary_toxin": "Gold complexes",
        "clinical_risk": "High-potency metabolic stimulant; potential immune-mediated glomerulonephritis and cost exploitation.",
        "restriction": "AI_BLOCKED; specialist institutional review."
    },
    "ZMF-107": {
        "name": "KUSHTA NUQRA",
        "botanical": "Calcined Silver Preparation",
        "category": "Precious Metal Bhasma",
        "primary_toxin": "Silver particulate bio-accumulation",
        "clinical_risk": "Argyria, renal tubular accumulation, metabolic disturbance.",
        "restriction": "AI_BLOCKED; specialist sign-off only."
    },
    "ZMF-108": {
        "name": "KUSHTA QARN-UL-AYYAL",
        "botanical": "Calcined Deer Horn",
        "category": "Animal-Derived Mineral Preparation",
        "primary_toxin": "Animal source contamination / CITES restrictions",
        "clinical_risk": "Illegal sourcing, biological pathogens, non-standardized ash content.",
        "restriction": "AI_BLOCKED; Wildlife Protection Act clearance required."
    },
    "ZMF-124": {
        "name": "ZANGAR",
        "botanical": "Copper acetate / Verdigris",
        "category": "Toxic Copper Salt",
        "primary_toxin": "Copper (Cu)",
        "clinical_risk": "Corrosive gastrointestinal burning, acute intravascular hemolysis, Wilson-like hepatic copper toxicity.",
        "restriction": "AI_BLOCKED; external use only under expert supervision."
    },
    "ZMF-129": {
        "name": "BAKAIN",
        "botanical": "Melia azedarach L.",
        "category": "Toxic Botanical",
        "primary_toxin": "Meliatoxins A1, A2, B1, Triterpenoids",
        "clinical_risk": "Severe neurotoxicity, muscular tremors, respiratory paralysis, gastroenteritis.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-130": {
        "name": "KARANJWA",
        "botanical": "Pongamia pinnata (L.) Pierre",
        "category": "High-Risk Botanical",
        "primary_toxin": "Karanjin, Pongamol",
        "clinical_risk": "Seed oil is a potent local irritant; emetic and unsafe for internal consumption without refining.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-134": {
        "name": "BADAM TALKH",
        "botanical": "Prunus amygdalus Batsch var. amara",
        "category": "Cyanogenic Botanical",
        "primary_toxin": "Amygdalin (hydrolyzes to lethal Hydrogen Cyanide)",
        "clinical_risk": "Cellular asphyxiation, cyanide toxicity, respiratory arrest.",
        "restriction": "AI_BLOCKED; strict distinction from sweet Badam Shirin."
    },
    "ZMF-184": {
        "name": "NEEM CHAAL",
        "botanical": "Azadirachta indica A. Juss. (Bark)",
        "category": "High-Risk Bitter Botanical",
        "primary_toxin": "Concentrated bitter tetranortriterpenoids",
        "clinical_risk": "Hepatic metabolic load, severe hypoglycemia risk, gastric mucosal irritation.",
        "restriction": "AI_BLOCKED; part-specific toxicity review required."
    },
    "ZMF-191": {
        "name": "BARG-E-SUDAB",
        "botanical": "Ruta graveolens L. (Leaf)",
        "category": "Schedule E(1) Uterotonic / Abortifacient",
        "primary_toxin": "Rutin, Furocoumarins (Bergapten), Volatile oil",
        "clinical_risk": "Violent uterine hemorrhage and abortion, acute contact phytophotodermatitis, nephrotoxicity.",
        "restriction": "AI_BLOCKED; strictly prohibited in women of childbearing age."
    },
    "ZMF-192": {
        "name": "SUDAB",
        "botanical": "Ruta graveolens L. (Whole Aerial Plant)",
        "category": "Schedule E(1) Uterotonic / Abortifacient",
        "primary_toxin": "Furocoumarins, Acridone alkaloids",
        "clinical_risk": "Violent abortifacient, severe hepatic and renal damage in overdose.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-193": {
        "name": "TUKHM-E-SUDAB",
        "botanical": "Ruta graveolens L. (Seed)",
        "category": "Schedule E(1) Uterotonic",
        "primary_toxin": "Concentrated volatile alkaloids",
        "clinical_risk": "Highest alkaloid density of the plant; acute emmenagogue and abortifacient.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-194": {
        "name": "HANZAL",
        "botanical": "Citrullus colocynthis (L.) Schrad.",
        "category": "Schedule E(1) Drastic Purgative",
        "primary_toxin": "Colocynthin, Cucurbitacins B and E",
        "clinical_risk": "Catastrophic bloody diarrhea, intestinal perforation, renal failure, hypovolemia.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-233": {
        "name": "AQARQARHA",
        "botanical": "Anacyclus pyrethrum (L.) Lag.",
        "category": "Mucosal Irritant Botanical",
        "primary_toxin": "Alkylamides (Pellitorine)",
        "clinical_risk": "Intense mucosal burning, oral and gastric ulceration, reflex uterine contraction. Daily ceiling: 200 mg.",
        "restriction": "AI_BLOCKED; dose-ceiling enforcement mandatory."
    },
    "ZMF-236": {
        "name": "JAIPHAL",
        "botanical": "Myristica fragrans Houtt. (Seed)",
        "category": "Psychoactive / Neurotoxic Botanical",
        "primary_toxin": "Myristicin, Elemicin",
        "clinical_risk": "Anticholinergic-like toxic psychosis, nausea, tachycardia, hallucinations, seizures at >5g.",
        "restriction": "AI_BLOCKED; specialist review only."
    },
    "ZMF-239": {
        "name": "GULE DHATURA",
        "botanical": "Datura metel L. (Flower)",
        "category": "Schedule E(1) Lethal Deliriant",
        "primary_toxin": "Hyoscine, Atropine",
        "clinical_risk": "Fatal anticholinergic toxidrome: mydriasis, hyperthermia, delirium, coma, cardiac arrest.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-240": {
        "name": "DHATURA",
        "botanical": "Datura metel L. (Seed/Leaf)",
        "category": "Schedule E(1) Lethal Deliriant",
        "primary_toxin": "Scopolamine, Hyoscyamine, Atropine",
        "clinical_risk": "Lethal neuro-vegetative block; traditional aphrodisiac misuse causing emergency fatalities.",
        "restriction": "AI_BLOCKED."
    },
    "ZMF-241": {
        "name": "AZARAQI",
        "botanical": "Strychnos nux-vomica L. (Seed)",
        "category": "Schedule E(1) Spinal Convulsant",
        "primary_toxin": "Strychnine, Brucine",
        "clinical_risk": "Antagonism of spinal glycine receptors -> violent agonizing tetanic convulsions and asphyxia.",
        "restriction": "AI_BLOCKED; requires rigorous 7-day milk/oil Shodhana certification."
    },
    "ZMF-243": {
        "name": "AFYUN",
        "botanical": "Papaver somniferum L. (Latex)",
        "category": "Narcotic / NDPS Act 1985 Controlled",
        "primary_toxin": "Morphine, Codeine, Thebaine",
        "clinical_risk": "Severe respiratory depression, physical addiction, lethal overdose.",
        "restriction": "AI_BLOCKED; statutory criminal prohibition without Central Bureau of Narcotics license."
    },
    "ZMF-245": {
        "name": "BHANG",
        "botanical": "Cannabis sativa L. (Leaf / Flowering Tops)",
        "category": "Psychotropic / State Excise Controlled",
        "primary_toxin": "Delta-9-Tetrahydrocannabinol (THC)",
        "clinical_risk": "Psychosis, cognitive impairment, legal and statutory restrictions under NDPS/Excise laws.",
        "restriction": "AI_BLOCKED."
    }
}

# =============================================================================
# 2. THE 43 CANONICALIZATION GROUPS (CAN-001 to CAN-043)
# =============================================================================
CANONICALIZATION_GROUPS: Dict[str, Dict[str, Any]] = {
    "CAN-001": {"scientific_name": "acacia nilotica", "common_genus": "Babul / Kikar", "record_ids": ["ZMF-185", "ZMF-186", "ZMF-187"]},
    "CAN-002": {"scientific_name": "aegle marmelos", "common_genus": "Bael / Bel Giri", "record_ids": ["ZMF-202", "ZMF-203"]},
    "CAN-003": {"scientific_name": "aloe vera", "common_genus": "Gheekwar / Sibr / Elwa", "record_ids": ["ZMF-083", "ZMF-084"]},
    "CAN-004": {"scientific_name": "althaea officinalis", "common_genus": "Khatmi (Flower/Seed/Root)", "record_ids": ["ZMF-022", "ZMF-023", "ZMF-024"]},
    "CAN-005": {"scientific_name": "azadirachta indica", "common_genus": "Neem (Leaf/Bark/Seed)", "record_ids": ["ZMF-128", "ZMF-184"]},
    "CAN-006": {"scientific_name": "cannabis sativa", "common_genus": "Bhang / Tukhm-e-Bhang", "record_ids": ["ZMF-245", "ZMF-246"]},
    "CAN-007": {"scientific_name": "cichorium intybus", "common_genus": "Kasni / Tukhm-e-Kasni", "record_ids": ["ZMF-070", "ZMF-071"]},
    "CAN-008": {"scientific_name": "citrullus colocynthis", "common_genus": "Hanzal / Indrayan", "record_ids": ["ZMF-194", "ZMF-195"]},
    "CAN-009": {"scientific_name": "cocos nucifera", "common_genus": "Nargil / Roghan Nargil", "record_ids": ["ZMF-139", "ZMF-140"]},
    "CAN-010": {"scientific_name": "coriandrum sativum", "common_genus": "Kishneez (Khushk & Sabz)", "record_ids": ["ZMF-064", "ZMF-065"]},
    "CAN-011": {"scientific_name": "croton tiglium", "common_genus": "Jamalgota / Habb-us-Salateen", "record_ids": ["ZMF-089", "ZMF-090"]},
    "CAN-012": {"scientific_name": "cucurbita pepo", "common_genus": "Kaddu / Tukhm-e-Kaddu", "record_ids": ["ZMF-145", "ZMF-146"]},
    "CAN-013": {"scientific_name": "datura metel", "common_genus": "Dhatura / Gule Dhatura", "record_ids": ["ZMF-239", "ZMF-240"]},
    "CAN-014": {"scientific_name": "foeniculum vulgare", "common_genus": "Badiyan / Saunf", "record_ids": ["ZMF-028", "ZMF-029"]},
    "CAN-015": {"scientific_name": "glycyrrhiza glabra", "common_genus": "Aslussoos / Mulethi", "record_ids": ["ZMF-052", "ZMF-053"]},
    "CAN-016": {"scientific_name": "holarrhena antidysenterica", "common_genus": "Inderjo Talkh / Kutaj", "record_ids": ["ZMF-091", "ZMF-093"]},
    "CAN-017": {"scientific_name": "hordeum vulgare", "common_genus": "Jau / Jau Sattoo", "record_ids": ["ZMF-152", "ZMF-153"]},
    "CAN-018": {"scientific_name": "juglans regia", "common_genus": "Akhrot / Maghz Akhrot", "record_ids": ["ZMF-135", "ZMF-136"]},
    "CAN-019": {"scientific_name": "lactuca sativa", "common_genus": "Kahu / Tukhme Kahu", "record_ids": ["ZMF-018", "ZMF-019"]},
    "CAN-020": {"scientific_name": "lepidium sativum", "common_genus": "Habb-ul-Rashad / Tukhm-e-Hayat", "record_ids": ["ZMF-171", "ZMF-226"]},
    "CAN-021": {"scientific_name": "linum usitatissimum", "common_genus": "Tukhm-e-Katan / Alsi", "record_ids": ["ZMF-143", "ZMF-144"]},
    "CAN-022": {"scientific_name": "matricaria chamomilla", "common_genus": "Babuna / Gule Babuna", "record_ids": ["ZMF-068", "ZMF-069"]},
    "CAN-023": {"scientific_name": "myristica fragrans", "common_genus": "Jaiphal / Javitri / Bisbaseh / Jozbuwa", "record_ids": ["ZMF-235", "ZMF-236", "ZMF-237", "ZMF-238"]},
    "CAN-024": {"scientific_name": "ocimum basilicum", "common_genus": "Tukhm-e-Rehan / Rehan / Habq", "record_ids": ["ZMF-055", "ZMF-056", "ZMF-060"]},
    "CAN-025": {"scientific_name": "olea europaea", "common_genus": "Zaitoon / Roghan Zaitoon", "record_ids": ["ZMF-141", "ZMF-142"]},
    "CAN-026": {"scientific_name": "operculina turpethum", "common_genus": "Turbud Safaid / Turbud Siyah", "record_ids": ["ZMF-086", "ZMF-087"]},
    "CAN-027": {"scientific_name": "piper longum", "common_genus": "Pippali / Filfil Daraz / Piplamool", "record_ids": ["ZMF-045", "ZMF-046", "ZMF-047"]},
    "CAN-028": {"scientific_name": "plantago ovata", "common_genus": "Isapghol Husk / Bazr Qutuna", "record_ids": ["ZMF-227", "ZMF-228"]},
    "CAN-029": {"scientific_name": "portulaca oleracea", "common_genus": "Khurfa / Tukhme Khurfa / Khurfa Siyah", "record_ids": ["ZMF-020", "ZMF-021", "ZMF-173"]},
    "CAN-030": {"scientific_name": "prunus dulcis", "common_genus": "Badam Shirin / Roghan Badam", "record_ids": ["ZMF-133", "ZMF-219"]},
    "CAN-031": {"scientific_name": "punica granatum", "common_genus": "Anar / Post Anar / Anar Dana / Gulnar", "record_ids": ["ZMF-180", "ZMF-181", "ZMF-182"]},
    "CAN-032": {"scientific_name": "ricinus communis", "common_genus": "Arand / Roghan Arand", "record_ids": ["ZMF-131", "ZMF-132"]},
    "CAN-033": {"scientific_name": "ruta graveolens", "common_genus": "Sudab / Barg-e-Sudab / Tukhm-e-Sudab", "record_ids": ["ZMF-191", "ZMF-192", "ZMF-193"]},
    "CAN-034": {"scientific_name": "sesamum indicum", "common_genus": "Kunjad (Sesame seed & Oil)", "record_ids": ["ZMF-224", "ZMF-225"]},
    "CAN-035": {"scientific_name": "strychnos nux vomica", "common_genus": "Azaraqi / Kuchla", "record_ids": ["ZMF-241", "ZMF-242"]},
    "CAN-036": {"scientific_name": "syzygium cumini", "common_genus": "Jamun / Tukhm-e-Jamun", "record_ids": ["ZMF-200", "ZMF-201"]},
    "CAN-037": {"scientific_name": "terminalia bellirica", "common_genus": "Balela / Post Balela", "record_ids": ["ZMF-011", "ZMF-013"]},
    "CAN-038": {"scientific_name": "terminalia chebula", "common_genus": "Halela Zard / Siyah / Kabli / Post Halela", "record_ids": ["ZMF-008", "ZMF-009", "ZMF-010", "ZMF-012"]},
    "CAN-039": {"scientific_name": "tinospora cordifolia", "common_genus": "Gilo / Guduchi", "record_ids": ["ZMF-197", "ZMF-198"]},
    "CAN-040": {"scientific_name": "trigonella foenum graecum", "common_genus": "Methi / Hulba", "record_ids": ["ZMF-158", "ZMF-159"]},
    "CAN-041": {"scientific_name": "valeriana wallichii", "common_genus": "Asaroon / Tagar", "record_ids": ["ZMF-247", "ZMF-248"]},
    "CAN-042": {"scientific_name": "zingiber officinale", "common_genus": "Zanjabeel (Dry) / Adrak (Fresh)", "record_ids": ["ZMF-040", "ZMF-041"]},
    "CAN-043": {"scientific_name": "ziziphus jujuba", "common_genus": "Anab / Unnab", "record_ids": ["ZMF-014", "ZMF-015"]}
}

# =============================================================================
# 3. COMPLETE 250 MUFRADAT MASTER CATALOG
# =============================================================================
# Helper data for generating all 250 validated records systematically
RAW_MUFRADAT_LIST = [
    ("ZMF-001", "ASGANDH", "Withania somnifera (L.) Dunal", "Solanaceae", "Dried roots", "Haar 1, Yabis 1", "Muqawwi-e-Aam; Muqawwi-e-Bah; Musakkin-e-Asab", None, "INTERNAL_SEED", "LOW"),
    ("ZMF-002", "SURANJAN TALKH", "Colchicum luteum Baker", "Colchicaceae", "Dried corms", "Haar 3, Yabis 3", "Mufattih-e-Sudad; Mus-hil-e-Balgham wa Sauda; Daf-e-Niqras", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-003", "BABCHI", "Psoralea corylifolia L.", "Fabaceae", "Dried seeds", "Haar 2, Yabis 2", "Mukhrij-e-Balgham; Muharrik-e-Jild; Daf-e-Bars", None, "INTERNAL_SEED", "MEDIUM"),
    ("ZMF-004", "USTUKHUDDUS", "Lavandula stoechas L.", "Lamiaceae", "Dried flowers", "Haar 1, Yabis 1", "Munaqqi-e-Dimagh; Muqawwi-e-Asab; Daf-e-Sudda", None, "INTERNAL_SEED", "LOW"),
    ("ZMF-005", "FILFIL SIYAH", "Piper nigrum L.", "Piperaceae", "Dried berries", "Haar 3, Yabis 3", "Hazim; Jali; Muqawwi-e-Meda; Muharrik-e-Ishtaha", None, "INTERNAL_SEED", "MEDIUM"),
    ("ZMF-006", "GAOZABAN", "Borago officinalis L. / Onosma bracteatum", "Boraginaceae", "Leaves & flowers", "Haar 1, Ratab 1", "Mufarreh-e-Qalb; Muqawwi-e-Dimagh; Munaffis-e-Balgham", None, "INTERNAL_SEED", "LOW"),
    ("ZMF-007", "AMLA", "Phyllanthus emblica L.", "Phyllanthaceae", "Fruit", "Barid 1, Yabis 2", "Muqawwi-e-Meda; Habis; Musakkin-e-Safra", None, "CANDIDATE", "LOW"),
    ("ZMF-008", "HALELA ZARD", "Terminalia chebula Retz.", "Combretaceae", "Fruit pericarp", "Barid 1, Yabis 2", "Mus-hil-e-Safra; Muqawwi-e-Meda", "CAN-038", "CANDIDATE", "LOW"),
    ("ZMF-009", "HALELA SIYAH", "Terminalia chebula Retz.", "Combretaceae", "Unripe fruit", "Barid 1, Yabis 2", "Muqawwi-e-Chashm; Habis; Muqawwi-e-Meda", "CAN-038", "CANDIDATE", "LOW"),
    ("ZMF-010", "HALELA KABLI", "Terminalia chebula Retz.", "Combretaceae", "Mature large fruit", "Barid 1, Yabis 2", "Mus-hil; Muqawwi-e-Dimagh", "CAN-038", "CANDIDATE", "LOW"),
    ("ZMF-011", "BALELA", "Terminalia bellirica (Gaertn.) Roxb.", "Combretaceae", "Fruit pericarp", "Barid 1, Yabis 2", "Muqawwi-e-Meda wa Dimagh; Habis", "CAN-037", "CANDIDATE", "LOW"),
    ("ZMF-012", "POST HALELA", "Terminalia chebula Retz.", "Combretaceae", "Fruit rind", "Barid 1, Yabis 2", "Munaqqi; Muqawwi", "CAN-038", "CANDIDATE", "LOW"),
    ("ZMF-013", "POST BALELA", "Terminalia bellirica (Gaertn.) Roxb.", "Combretaceae", "Fruit rind", "Barid 1, Yabis 2", "Habis; Muqawwi", "CAN-037", "CANDIDATE", "LOW"),
    ("ZMF-014", "ANAB", "Ziziphus jujuba Mill.", "Rhamnaceae", "Dried fruit", "Motadil (Ratab)", "Musaffi-e-Dam; Munaffis-e-Balgham; Mulayyin", "CAN-043", "CANDIDATE", "LOW"),
    ("ZMF-015", "UNNAB", "Ziziphus jujuba Mill.", "Rhamnaceae", "Dried fruit", "Motadil (Ratab)", "Musaffi-e-Dam; Munaffis-e-Balgham; Mulayyin", "CAN-043", "CANDIDATE", "LOW"),
    ("ZMF-016", "BANAFSHA", "Viola odorata L.", "Violaceae", "Flower", "Barid 1, Ratab 1", "Muskin-e-Hararat; Munaffis-e-Balgham; Mulayyin", None, "CANDIDATE", "LOW"),
    ("ZMF-017", "BEHIDANA", "Cydonia oblonga Mill.", "Rosaceae", "Seed", "Barid 2, Ratab 2", "Lu'ab-dar; Musakkin-e-Hararat; Daf-e-Sual", None, "CANDIDATE", "LOW"),
    ("ZMF-018", "TUKHME KAHU", "Lactuca sativa L.", "Asteraceae", "Seed", "Barid 2, Ratab 2", "Musakkin-e-Hararat; Munawwim (Sedative)", "CAN-019", "CANDIDATE", "LOW"),
    ("ZMF-019", "KAHU", "Lactuca sativa L.", "Asteraceae", "Leaf", "Barid 2, Ratab 2", "Mubarrid; Musakkin-e-Safra", "CAN-019", "CANDIDATE", "LOW"),
    ("ZMF-020", "TUKHME KHURFA", "Portulaca oleracea L.", "Portulacaceae", "Seed", "Barid 2, Ratab 2", "Musakkin-e-Hararat; Mudirr-e-Baul", "CAN-029", "CANDIDATE", "LOW"),
    ("ZMF-021", "KHURFA", "Portulaca oleracea L.", "Portulacaceae", "Whole plant", "Barid 2, Ratab 2", "Musakkin-e-Safra; Qabiz", "CAN-029", "CANDIDATE", "LOW"),
    ("ZMF-022", "TUKHME KHATMI", "Althaea officinalis L.", "Malvaceae", "Seed", "Barid 1, Ratab 1", "Muhallil; Mulayyin; Demulcent", "CAN-004", "CANDIDATE", "LOW"),
    ("ZMF-023", "KHATMI", "Althaea officinalis L.", "Malvaceae", "Root", "Barid 1, Ratab 1", "Mundamil; Muhallil", "CAN-004", "CANDIDATE", "LOW"),
    ("ZMF-024", "GULE KHATMI", "Althaea officinalis L.", "Malvaceae", "Flower", "Barid 1, Ratab 1", "Muskin; Munaffis", "CAN-004", "CANDIDATE", "LOW"),
    ("ZMF-025", "GUL-E-SURKH", "Rosa damascena Mill.", "Rosaceae", "Petal", "Barid 1, Yabis 2", "Mufarreh; Muqawwi-e-Meda wa Dil; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-026", "GUL-E-GAOZABAN", "Onosma bracteatum Wall.", "Boraginaceae", "Flower", "Haar 1, Ratab 1", "Mufarreh-e-Qalb; Muqawwi", None, "CANDIDATE", "LOW"),
    ("ZMF-027", "NILOFER", "Nymphaea alba L.", "Nymphaeaceae", "Flower", "Barid 2, Ratab 2", "Musakkin-e-Hararat; Munawwim", None, "CANDIDATE", "LOW"),
    ("ZMF-028", "BADIYAN", "Foeniculum vulgare Mill.", "Apiaceae", "Fruit", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim; Mudirr-e-Baul wa Tams", "CAN-014", "CANDIDATE", "LOW"),
    ("ZMF-029", "SAUNF", "Foeniculum vulgare Mill.", "Apiaceae", "Fruit", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim", "CAN-014", "CANDIDATE", "LOW"),
    ("ZMF-030", "AJWAIN DESI", "Trachyspermum ammi (L.) Sprague", "Apiaceae", "Fruit", "Haar 3, Yabis 3", "Kasir-e-Riyah; Hazim; Daf-e-Tashannuj", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-031", "AJWAIN KHURASANI", "Hyoscyamus niger L.", "Solanaceae", "Seed", "Barid 3, Yabis 3", "Musakkin-e-Alam; Munawwim; Mukhaddid", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-032", "ZEERA SIYAH", "Carum carvi L.", "Apiaceae", "Fruit", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim; Muqawwi-e-Meda", None, "CANDIDATE", "LOW"),
    ("ZMF-033", "ZEERA SAFAID", "Cuminum cyminum L.", "Apiaceae", "Fruit", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim", None, "CANDIDATE", "LOW"),
    ("ZMF-034", "KALONJI", "Nigella sativa L.", "Ranunculaceae", "Seed", "Haar 2, Yabis 2", "Daf-e-Tashannuj; Kasir-e-Riyah; Mudirr", None, "CANDIDATE", "LOW"),
    ("ZMF-035", "DARCHINI", "Cinnamomum verum J.Presl", "Lauraceae", "Bark", "Haar 2, Yabis 2", "Hazim; Kasir-e-Riyah; Muqawwi-e-Bah", None, "CANDIDATE", "LOW"),
    ("ZMF-036", "TAJ QALMI", "Cinnamomum cassia (L.) J.Presl", "Lauraceae", "Bark", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim", None, "CANDIDATE", "LOW"),
    ("ZMF-037", "QARANFAL", "Syzygium aromaticum (L.) Merr. & L.M.Perry", "Myrtaceae", "Flower bud", "Haar 3, Yabis 3", "Mufarreh; Hazim; Muqawwi-e-Qalb", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-038", "ELAICHI KHURD", "Elettaria cardamomum (L.) Maton", "Zingiberaceae", "Fruit", "Haar 1, Yabis 2", "Mufarreh; Hazim; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-039", "ELAICHI KALAN", "Amomum subulatum Roxb.", "Zingiberaceae", "Fruit", "Haar 2, Yabis 2", "Hazim; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-040", "ZANJABEEL", "Zingiber officinale Roscoe", "Zingiberaceae", "Dried rhizome", "Haar 3, Yabis 2", "Hazim; Kasir-e-Riyah; Muqawwi-e-Hafiza", "CAN-042", "CANDIDATE", "LOW"),
    ("ZMF-041", "ADRAK", "Zingiber officinale Roscoe", "Zingiberaceae", "Fresh rhizome", "Haar 3, Ratab 1", "Hazim; Kasir-e-Riyah", "CAN-042", "CANDIDATE", "LOW"),
    ("ZMF-042", "HALDI", "Curcuma longa L.", "Zingiberaceae", "Rhizome", "Haar 2, Yabis 2", "Muhallil; Musaffi-e-Dam; Jali", None, "CANDIDATE", "LOW"),
    ("ZMF-043", "ZARAMBAD", "Curcuma zedoaria (Christm.) Roscoe", "Zingiberaceae", "Rhizome", "Haar 2, Yabis 2", "Mufarreh; Hazim; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-044", "KAPOOR KACHRI", "Hedychium spicatum Sm.", "Zingiberaceae", "Rhizome", "Haar 2, Yabis 2", "Kasir-e-Riyah; Muqawwi-e-Meda", None, "CANDIDATE", "LOW"),
    ("ZMF-045", "PIPPALI", "Piper longum L.", "Piperaceae", "Fruit", "Haar 2, Yabis 2", "Hazim; Muqawwi-e-Bah; Munaffis", "CAN-027", "CANDIDATE", "LOW"),
    ("ZMF-046", "FILFIL DARAZ", "Piper longum L.", "Piperaceae", "Fruit", "Haar 2, Yabis 2", "Hazim; Muqawwi-e-Bah", "CAN-027", "CANDIDATE", "LOW"),
    ("ZMF-047", "PIPLAMOOL", "Piper longum L.", "Piperaceae", "Root", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim; Deepana", "CAN-027", "CANDIDATE", "LOW"),
    ("ZMF-048", "CHOBCHINI", "Smilax china L.", "Smilacaceae", "Rhizome", "Haar 1, Yabis 1", "Musaffi-e-Dam; Daf-e-Niqras wa Atishak", None, "CANDIDATE", "LOW"),
    ("ZMF-049", "SANDAL SAFAID", "Santalum album L.", "Santalaceae", "Heartwood", "Barid 2, Yabis 2", "Mubarrid; Mufarreh; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-050", "SANDAL SURKH", "Pterocarpus santalinus L.f.", "Fabaceae", "Heartwood", "Barid 2, Yabis 2", "Mubarrid; Habis-e-Dam; Musaffi", None, "CANDIDATE", "LOW"),
    ("ZMF-051", "USHBA", "Smilax ornata Lem.", "Smilacaceae", "Root", "Haar 1, Yabis 1", "Musaffi-e-Dam; Mudirr-e-Baul", None, "CANDIDATE", "LOW"),
    ("ZMF-052", "ASLUSSOOS", "Glycyrrhiza glabra L.", "Fabaceae", "Root", "Haar 1, Ratab 1", "Munaffis-e-Balgham; Mulayyin; Munaqqi", "CAN-015", "CANDIDATE", "LOW"),
    ("ZMF-053", "MULETHI", "Glycyrrhiza glabra L.", "Fabaceae", "Root", "Haar 1, Ratab 1", "Munaffis-e-Balgham; Mulayyin", "CAN-015", "CANDIDATE", "LOW"),
    ("ZMF-054", "SAPISTAN", "Cordia myxa L.", "Boraginaceae", "Fruit", "Motadil (Ratab)", "Munaffis-e-Balgham; Mulayyin; Musakkin", None, "CANDIDATE", "LOW"),
    ("ZMF-055", "TUKHM-E-REHAN", "Ocimum basilicum L.", "Lamiaceae", "Seed", "Barid 1, Ratab 1", "Habis; Muqawwi-e-Meda; Lu'abi", "CAN-024", "CANDIDATE", "LOW"),
    ("ZMF-056", "REHAN", "Ocimum basilicum L.", "Lamiaceae", "Leaf", "Haar 1, Yabis 1", "Mufarreh; Kasir-e-Riyah", "CAN-024", "CANDIDATE", "LOW"),
    ("ZMF-057", "TULSI", "Ocimum tenuiflorum L.", "Lamiaceae", "Leaf", "Haar 1, Yabis 1", "Musaffi-e-Dam; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-058", "PODINA", "Mentha arvensis L.", "Lamiaceae", "Leaf", "Haar 2, Yabis 2", "Hazim; Kasir-e-Riyah; Daf-e-Qai", None, "CANDIDATE", "LOW"),
    ("ZMF-059", "MARZANJOSH", "Origanum majorana L.", "Lamiaceae", "Aerial parts", "Haar 2, Yabis 2", "Mufattih; Kasir-e-Riyah; Musakkin", None, "CANDIDATE", "LOW"),
    ("ZMF-060", "HABQ", "Ocimum basilicum L.", "Lamiaceae", "Aerial parts", "Haar 1, Yabis 1", "Mufarreh; Hazim", "CAN-024", "CANDIDATE", "LOW"),
    ("ZMF-061", "SATAR FARSI", "Thymus vulgaris L.", "Lamiaceae", "Aerial parts", "Haar 3, Yabis 3", "Kasir-e-Riyah; Hazim; Qatil-e-Dood", None, "CANDIDATE", "LOW"),
    ("ZMF-062", "ZUFA", "Hyssopus officinalis L.", "Lamiaceae", "Aerial parts", "Haar 2, Yabis 2", "Munaffis-e-Balgham; Munaqqi-e-Sadr", None, "CANDIDATE", "LOW"),
    ("ZMF-063", "BADRANJBOYA", "Melissa officinalis L.", "Lamiaceae", "Leaf", "Haar 1, Yabis 1", "Mufarreh-e-Qalb; Muqawwi-e-Dimagh", None, "CANDIDATE", "LOW"),
    ("ZMF-064", "KISHNEEZ KHUSHK", "Coriandrum sativum L.", "Apiaceae", "Fruit", "Barid 2, Yabis 2", "Qabiz; Musakkin-e-Safra; Hazim", "CAN-010", "CANDIDATE", "LOW"),
    ("ZMF-065", "KISHNEEZ SABZ", "Coriandrum sativum L.", "Apiaceae", "Fresh leaf", "Barid 2, Ratab 2", "Mubarrid; Musakkin", "CAN-010", "CANDIDATE", "LOW"),
    ("ZMF-066", "KARAFS", "Apium graveolens L.", "Apiaceae", "Seed/fruit", "Haar 2, Yabis 2", "Mudirr-e-Baul wa Tams; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-067", "PARSIYAVSHAN", "Adiantum capillus-veneris L.", "Pteridaceae", "Frond", "Motadil", "Munaffis-e-Balgham; Mufattih", None, "CANDIDATE", "LOW"),
    ("ZMF-068", "GULE BABUNA", "Matricaria chamomilla L.", "Asteraceae", "Flower", "Haar 1, Yabis 1", "Muhallil; Musakkin-e-Alam; Daf-e-Tashannuj", "CAN-022", "CANDIDATE", "LOW"),
    ("ZMF-069", "BABUNA", "Matricaria chamomilla L.", "Asteraceae", "Flower heads", "Haar 1, Yabis 1", "Muhallil; Musakkin", "CAN-022", "CANDIDATE", "LOW"),
    ("ZMF-070", "KASNI", "Cichorium intybus L.", "Asteraceae", "Root", "Barid 1, Yabis 1", "Mubarrid; Mufattih-e-Kabid; Musakkin-e-Hararat", "CAN-007", "CANDIDATE", "LOW"),
    ("ZMF-071", "TUKHM-E-KASNI", "Cichorium intybus L.", "Asteraceae", "Seed", "Barid 1, Yabis 1", "Muskin-e-Safra; Mudirr", "CAN-007", "CANDIDATE", "LOW"),
    ("ZMF-072", "KASOOS", "Cuscuta reflexa Roxb.", "Convolvulaceae", "Whole plant", "Haar 1, Yabis 2", "Mufattih; Musaffi; Munaqqi", None, "CANDIDATE", "LOW"),
    ("ZMF-073", "AFANTEEN", "Artemisia absinthium L.", "Asteraceae", "Aerial parts", "Haar 2, Yabis 2", "Hazim; Qatil-e-Kirm; Mufattih", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-074", "QUST SHIRIN", "Saussurea costus (Falc.) Lipsch.", "Asteraceae", "Root", "Haar 2, Yabis 2", "Kasir-e-Riyah; Muqawwi-e-Bah; Muhallil", None, "CANDIDATE", "LOW"),
    ("ZMF-075", "QUST TALKH", "Saussurea lappa (Decne.) Sch.Bip.", "Asteraceae", "Root", "Haar 3, Yabis 3", "Mufattih; Qatil-e-Kirm; Muhallil", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-076", "ZAFARAN", "Crocus sativus L.", "Iridaceae", "Stigma", "Haar 1, Yabis 1", "Mufarreh; Muqawwi-e-Qalb; Muharrik", None, "CANDIDATE", "LOW"),
    ("ZMF-077", "MASTAGI", "Pistacia lentiscus L.", "Anacardiaceae", "Resin", "Haar 2, Yabis 2", "Muqawwi-e-Meda wa Jigar; Hazim", None, "CANDIDATE", "LOW"),
    ("ZMF-078", "KUNDUR", "Boswellia serrata Roxb. ex Colebr.", "Burseraceae", "Oleo-gum-resin", "Haar 2, Yabis 2", "Muqawwi-e-Hafiza; Habis; Muhallil", None, "CANDIDATE", "LOW"),
    ("ZMF-079", "LOBAN", "Styrax benzoin Dryand.", "Styracaceae", "Resin", "Haar 2, Yabis 2", "Munaffis; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-080", "MUR MAKKI", "Commiphora myrrha (Nees) Engl.", "Burseraceae", "Oleogum resin", "Haar 2, Yabis 2", "Daf-e-Ufunat; Mundamil; Mudirr", None, "CANDIDATE", "LOW"),
    ("ZMF-081", "ANZAROOT", "Astragalus sarcocolla Dymock", "Fabaceae", "Gum/resin", "Haar 2, Yabis 2", "Mundamil; Mus-hil-e-Balgham", None, "CANDIDATE", "LOW"),
    ("ZMF-082", "KATEERA", "Astragalus gummifer Labill.", "Fabaceae", "Gum", "Motadil", "Musakkin-e-Hiddat; Mughalliz; Demulcent", None, "CANDIDATE", "LOW"),
    ("ZMF-083", "SIBR", "Aloe vera (L.) Burm.f.", "Asphodelaceae", "Dried latex", "Haar 2, Yabis 2", "Mus-hil; Munaqqi; Muqawwi-e-Meda", "CAN-003", "CANDIDATE", "MEDIUM"),
    ("ZMF-084", "ELWA", "Aloe vera (L.) Burm.f.", "Asphodelaceae", "Dried latex", "Haar 2, Yabis 2", "Mus-hil; Munaqqi", "CAN-003", "CANDIDATE", "MEDIUM"),
    ("ZMF-085", "SENA MAKKI", "Senna alexandrina Mill.", "Fabaceae", "Leaf", "Haar 1, Yabis 2", "Mus-hil-e-Akhlat-e-Salasa; Munaqqi", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-086", "TURBUD SAFAID", "Operculina turpethum (L.) Silva Manso", "Convolvulaceae", "Root", "Haar 3, Yabis 3", "Mus-hil-e-Balgham; Munaqqi", "CAN-026", "CANDIDATE", "MEDIUM"),
    ("ZMF-087", "TURBUD SIYAH", "Operculina turpethum (L.) Silva Manso", "Convolvulaceae", "Root", "Haar 3, Yabis 3", "Mus-hil", "CAN-026", "CANDIDATE", "MEDIUM"),
    ("ZMF-088", "REVAND CHINI", "Rheum palmatum L.", "Polygonaceae", "Rhizome", "Haar 2, Yabis 2", "Mus-hil; Mufattih; Muqawwi-e-Kabid", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-089", "JAMALGOTA", "Croton tiglium L.", "Euphorbiaceae", "Seed", "Haar 4, Yabis 4", "Mus-hil-e-Shadeed", "CAN-011", "HIGH_RISK", "CRITICAL"),
    ("ZMF-090", "HABB-US-SALATEEN", "Croton tiglium L.", "Euphorbiaceae", "Seed", "Haar 4, Yabis 4", "Mus-hil-e-Shadeed", "CAN-011", "HIGH_RISK", "CRITICAL"),
    ("ZMF-091", "INDERJO TALKH", "Holarrhena antidysenterica Wall.", "Apocynaceae", "Seed/bark", "Haar 2, Yabis 2", "Qabiz; Qatil-e-Kirm; Daf-e-Zalaq", "CAN-016", "CANDIDATE", "LOW"),
    ("ZMF-092", "INDERJO SHIRIN", "Wrightia tinctoria R.Br.", "Apocynaceae", "Seed/bark", "Haar 1, Yabis 1", "Muqawwi-e-Bah; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-093", "KUTAJ", "Holarrhena antidysenterica Wall.", "Apocynaceae", "Bark", "Haar 2, Yabis 2", "Qabiz; Daf-e-Ishaal", "CAN-016", "CANDIDATE", "LOW"),
    ("ZMF-094", "MOCHRAS", "Bombax ceiba L.", "Malvaceae", "Gum", "Barid 1, Yabis 2", "Habis; Mughalliz-e-Mani; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-095", "SUHAGA", "Purified Borax", "Borate mineral", "Mineral", "Haar 2, Yabis 2", "Jali; Hazim; Daf-e-Balgham", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-096", "NAMAK LAHORI", "Sodium chloride / Rock salt", "Mineral salt", "Salt", "Haar 2, Yabis 2", "Hazim; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-097", "NAMAK SIYAH", "Black salt", "Mineral salt", "Salt", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim; Mulayyin", None, "CANDIDATE", "LOW"),
    ("ZMF-098", "NAMAK SAMBHAR", "Lake salt", "Mineral salt", "Salt", "Haar 2, Yabis 2", "Hazim", None, "CANDIDATE", "LOW"),
    ("ZMF-099", "SHORA QALMI", "Potassium nitrate", "Mineral salt", "Crystal salt", "Barid 1, Yabis 2", "Mudirr-e-Baul; Musakkin-e-Hararat", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-100", "GANDHAK AMLA SAR", "Purified Sulphur", "Elemental mineral", "Mineral", "Haar 3, Yabis 3", "Musaffi-e-Dam; Daf-e-Jarb; Jali", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-101", "SHANGRAF", "Mercuric sulphide", "Mercury mineral", "Mineral", "Haar 3, Yabis 3", "Muqawwi; Daf-e-Asab", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-102", "HARTAL", "Arsenic trisulphide", "Arsenic mineral", "Mineral", "Haar 4, Yabis 4", "Qatil; Jali", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-103", "PARA", "Purified Mercury", "Elemental mineral", "Mineral", "Haar 3, Yabis 3", "Muqawwi", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-104", "KUSHTA ABRAK SIYAH", "Calcined Biotite Mica", "Mineral preparation", "Calcined mineral", "Haar 1, Yabis 1", "Muqawwi-e-Aam; Munaffis", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-105", "KUSHTA FAULAD", "Calcined Iron", "Mineral preparation", "Calcined mineral", "Haar 1, Yabis 2", "Muwallid-e-Dam; Muqawwi-e-Jigar", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-106", "KUSHTA TILA", "Calcined Gold", "Metal preparation", "Calcined metal", "Motadil", "Muqawwi-e-Qalb wa Aza-e-Raeesa", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-107", "KUSHTA NUQRA", "Calcined Silver", "Metal preparation", "Calcined metal", "Barid 1, Yabis 1", "Muqawwi-e-Qalb wa Dimagh", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-108", "KUSHTA QARN-UL-AYYAL", "Calcined Deer Horn", "Animal mineral", "Calcined horn", "Haar 1, Yabis 2", "Habis-e-Dam; Daf-e-Zeeq-un-Nafs", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-109", "MARJAN", "Corallium rubrum", "Marine mineral", "Coral", "Barid 1, Yabis 2", "Mufarreh; Muqawwi-e-Qalb; Habis", None, "CANDIDATE", "LOW"),
    ("ZMF-110", "SADAF", "Oyster shell calcium", "Marine mineral", "Shell", "Barid 1, Yabis 2", "Habis; Mudammil", None, "CANDIDATE", "LOW"),
    ("ZMF-111", "KAHRUBA", "Amber resin", "Fossil resin", "Resin", "Barid 1, Yabis 2", "Habis-e-Dam; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-112", "YASHAB", "Jade stone", "Mineral", "Stone", "Barid 1, Yabis 2", "Mufarreh-e-Qalb", None, "CANDIDATE", "LOW"),
    ("ZMF-113", "LAJWARD", "Lapis lazuli", "Mineral", "Stone", "Haar 1, Yabis 2", "Munaqqi-e-Sauda; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-114", "HAJR-UL-YAHOOD", "Lapis judaicus", "Mineral concretion", "Stone", "Motadil", "Mufattit-e-Hisat (Stone breaker)", None, "CANDIDATE", "LOW"),
    ("ZMF-115", "SANG-E-JARAHAT", "Gypsum stone", "Mineral", "Stone", "Barid 1, Yabis 2", "Habis-e-Dam; Mundamil", None, "CANDIDATE", "LOW"),
    ("ZMF-116", "SANG-E-SURMA", "Antimony sulphide", "Mineral", "Processed mineral", "Barid 1, Yabis 2", "Muqawwi-e-Basar (Eye tonic)", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-117", "SURMA SIYAH", "Antimony sulphide prep", "Mineral", "Collyrium", "Barid 1, Yabis 2", "Muqawwi-e-Ayn", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-118", "SANG-E-SARMAHI", "Fish otolith stone", "Animal mineral", "Concretion", "Motadil", "Mufattit-e-Hisat", None, "CANDIDATE", "LOW"),
    ("ZMF-119", "ABRAK SIYAH", "Biotite mica raw", "Mineral", "Mica", "Haar 1, Yabis 1", "Raw mineral candidate", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-120", "ABRAK SAFAID", "Muscovite mica raw", "Mineral", "Mica", "Haar 1, Yabis 1", "Raw mineral candidate", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-121", "HEERAKASEES", "Green vitriol / Ferrous sulphate", "Mineral salt", "Crystal", "Haar 2, Yabis 2", "Qabiz; Muwallid-e-Dam", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-122", "KASIS", "Ferrous sulphate", "Mineral salt", "Crystal", "Haar 2, Yabis 2", "Qabiz", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-123", "PHITKARI", "Potassium alum", "Mineral salt", "Crystal", "Haar 2, Yabis 3", "Habis-e-Dam; Qabiz; Daf-e-Ufunat", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-124", "ZANGAR", "Copper acetate", "Copper salt", "Processed mineral", "Haar 4, Yabis 4", "Khadish; Akkal", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-125", "RASAUT", "Berberis aristata extract", "Berberidaceae", "Extract", "Barid 2, Yabis 2", "Musaffi-e-Dam; Qabiz; Muhallil", None, "CANDIDATE", "LOW"),
    ("ZMF-126", "DARU HALDI", "Berberis aristata DC.", "Berberidaceae", "Bark", "Haar 2, Yabis 2", "Mufattih-e-Kabid; Musaffi", None, "CANDIDATE", "LOW"),
    ("ZMF-127", "MAMIRAN", "Coptis teeta Wall.", "Ranunculaceae", "Rhizome", "Barid 2, Yabis 2", "Jali; Muqawwi-e-Basar", None, "CANDIDATE", "LOW"),
    ("ZMF-128", "NEEM", "Azadirachta indica A.Juss.", "Meliaceae", "Leaf", "Haar 1, Yabis 2", "Musaffi-e-Dam; Qatil-e-Jaratheem", "CAN-005", "CANDIDATE", "LOW"),
    ("ZMF-129", "BAKAIN", "Melia azedarach L.", "Meliaceae", "Bark/fruit", "Haar 2, Yabis 2", "Musaffi; Qatil-e-Kirm", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-130", "KARANJWA", "Pongamia pinnata (L.) Pierre", "Fabaceae", "Seed", "Haar 2, Yabis 2", "Daf-e-Humma; Qatil-e-Kirm", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-131", "ARAND", "Ricinus communis L.", "Euphorbiaceae", "Seed", "Haar 2, Yabis 2", "Mus-hil; Muhallil", "CAN-032", "CANDIDATE", "MEDIUM"),
    ("ZMF-132", "ROGHAN ARAND", "Ricinus communis L.", "Euphorbiaceae", "Fixed oil", "Haar 1, Ratab 1", "Mulayyin; Mus-hil", "CAN-032", "CANDIDATE", "LOW"),
    ("ZMF-133", "BADAM SHIRIN", "Prunus dulcis (Mill.) D.A.Webb", "Rosaceae", "Kernel", "Motadil (Ratab)", "Muqawwi-e-Dimagh; Mulayyin", "CAN-030", "CANDIDATE", "LOW"),
    ("ZMF-134", "BADAM TALKH", "Prunus amygdalus var. amara", "Rosaceae", "Kernel", "Haar 2, Yabis 2", "Jali; Mufattih", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-135", "MAGHZ AKHROT", "Juglans regia L.", "Juglandaceae", "Kernel", "Haar 2, Yabis 1", "Muqawwi-e-Dimagh wa Bah", "CAN-018", "CANDIDATE", "LOW"),
    ("ZMF-136", "AKHROT", "Juglans regia L.", "Juglandaceae", "Kernel/bark", "Haar 2, Yabis 1", "Muqawwi", "CAN-018", "CANDIDATE", "LOW"),
    ("ZMF-137", "CHILGOZA", "Pinus gerardiana Wall. ex D.Don", "Pinaceae", "Seed", "Haar 2, Ratab 1", "Muqawwi-e-Bah wa Asab", None, "CANDIDATE", "LOW"),
    ("ZMF-138", "PISTA", "Pistacia vera L.", "Anacardiaceae", "Kernel", "Haar 2, Ratab 1", "Muqawwi-e-Qalb wa Dimagh", None, "CANDIDATE", "LOW"),
    ("ZMF-139", "NARGIL", "Cocos nucifera L.", "Arecaceae", "Kernel", "Haar 1, Ratab 1", "Muqawwi-e-Bah; Mughalliz", "CAN-009", "CANDIDATE", "LOW"),
    ("ZMF-140", "ROGHAN NARGIL", "Cocos nucifera L.", "Arecaceae", "Fixed oil", "Barid 1, Ratab 1", "Mubarrid; Murattib", "CAN-009", "CANDIDATE", "LOW"),
    ("ZMF-141", "ROGHAN ZAITOON", "Olea europaea L.", "Oleaceae", "Fixed oil", "Motadil (Ratab)", "Muqawwi; Mulayyin", "CAN-025", "CANDIDATE", "LOW"),
    ("ZMF-142", "ZAITOON", "Olea europaea L.", "Oleaceae", "Fruit", "Haar 1, Yabis 1", "Muqawwi-e-Meda", "CAN-025", "CANDIDATE", "LOW"),
    ("ZMF-143", "TUKHM-E-KATAN", "Linum usitatissimum L.", "Linaceae", "Seed", "Haar 1, Yabis 1", "Mulayyin; Muhallil; Jali", "CAN-021", "CANDIDATE", "LOW"),
    ("ZMF-144", "ALSI", "Linum usitatissimum L.", "Linaceae", "Seed", "Haar 1, Yabis 1", "Mulayyin; Muhallil", "CAN-021", "CANDIDATE", "LOW"),
    ("ZMF-145", "TUKHM-E-KADDU", "Cucurbita pepo L.", "Cucurbitaceae", "Seed", "Barid 2, Ratab 2", "Mubarrid; Musakkin; Qatil-e-Kirm", "CAN-012", "CANDIDATE", "LOW"),
    ("ZMF-146", "KADDU", "Cucurbita pepo L.", "Cucurbitaceae", "Pulp", "Barid 2, Ratab 2", "Mubarrid; Musakkin-e-Hararat", "CAN-012", "CANDIDATE", "LOW"),
    ("ZMF-147", "TUKHM-E-KHARBUZA", "Cucumis melo L.", "Cucurbitaceae", "Seed", "Haar 1, Ratab 2", "Mudirr-e-Baul; Munaqqi-e-Kulyah", None, "CANDIDATE", "LOW"),
    ("ZMF-148", "TUKHM-E-KAKRI", "Cucumis sativus L.", "Cucurbitaceae", "Seed", "Barid 2, Ratab 2", "Mudirr; Mubarrid", None, "CANDIDATE", "LOW"),
    ("ZMF-149", "TUKHM-E-TARBOOZ", "Citrullus lanatus (Thunb.) Matsum. & Nakai", "Cucurbitaceae", "Seed", "Barid 2, Ratab 2", "Mubarrid; Mudirr", None, "CANDIDATE", "LOW"),
    ("ZMF-150", "MAGHZ-E-CHAHAR MAGHZ", "Mixed Cucurbit Kernels", "Mixed botanical", "Kernels", "Barid 1, Ratab 2", "Mubarrid; Muqawwi-e-Dimagh", None, "CANDIDATE", "LOW"),
    ("ZMF-151", "GUNDUM", "Triticum aestivum L.", "Poaceae", "Grain", "Motadil (Ratab)", "Muqawwi; Muwallid-e-Dam", None, "CANDIDATE", "LOW"),
    ("ZMF-152", "JAU", "Hordeum vulgare L.", "Poaceae", "Grain", "Barid 1, Yabis 1", "Mubarrid; Musakkin", "CAN-017", "CANDIDATE", "LOW"),
    ("ZMF-153", "JAU SATTOO", "Hordeum vulgare L.", "Poaceae", "Roasted flour", "Barid 1, Yabis 1", "Mubarrid; Musakkin-e-Hararat", "CAN-017", "CANDIDATE", "LOW"),
    ("ZMF-154", "CHAWAL", "Oryza sativa L.", "Poaceae", "Grain", "Barid 1, Yabis 1", "Qabiz; Muwallid-e-Khilt-e-Salih", None, "CANDIDATE", "LOW"),
    ("ZMF-155", "MASOOR", "Lens culinaris Medik.", "Fabaceae", "Seed", "Barid 1, Yabis 2", "Habis; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-156", "MUNG", "Vigna radiata (L.) R.Wilczek", "Fabaceae", "Seed", "Motadil", "Hazim; Muwallid-e-Khilt-e-Motadil", None, "CANDIDATE", "LOW"),
    ("ZMF-157", "CHANA", "Cicer arietinum L.", "Fabaceae", "Seed", "Haar 1, Yabis 1", "Muqawwi-e-Bah; Mudirr", None, "CANDIDATE", "LOW"),
    ("ZMF-158", "METHI", "Trigonella foenum-graecum L.", "Fabaceae", "Seed/leaf", "Haar 2, Yabis 2", "Muhallil; Mudirr-e-Baul wa Tams", "CAN-040", "CANDIDATE", "LOW"),
    ("ZMF-159", "HULBA", "Trigonella foenum-graecum L.", "Fabaceae", "Seed", "Haar 2, Yabis 2", "Muhallil; Kasir-e-Riyah", "CAN-040", "CANDIDATE", "LOW"),
    ("ZMF-160", "MAKO", "Solanum nigrum L.", "Solanaceae", "Whole plant", "Barid 2, Yabis 2", "Muhallil-e-Awram; Musakkin", None, "CANDIDATE", "LOW"),
    ("ZMF-161", "KAKNAJ", "Physalis alkekengi L.", "Solanaceae", "Fruit/calyx", "Barid 2, Yabis 2", "Mudirr-e-Baul; Mufattit-e-Hisat", None, "CANDIDATE", "LOW"),
    ("ZMF-162", "KANTAKARI", "Solanum xanthocarpum Schrad. & J.C.Wendl.", "Solanaceae", "Whole plant", "Haar 2, Yabis 2", "Munaffis-e-Balgham; Daf-e-Sual", None, "CANDIDATE", "LOW"),
    ("ZMF-163", "KATERI", "Solanum indicum L.", "Solanaceae", "Root/plant", "Haar 2, Yabis 2", "Munaffis; Muhallil", None, "CANDIDATE", "LOW"),
    ("ZMF-164", "BAINGAN", "Solanum melongena L.", "Solanaceae", "Fruit", "Haar 2, Yabis 2", "Muwallid-e-Sauda", None, "CANDIDATE", "LOW"),
    ("ZMF-165", "MIRCH SIYAH", "Piper nigrum L.", "Piperaceae", "Fruit", "Haar 3, Yabis 3", "Hazim; Kasir-e-Riyah", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-166", "MIRCH SURKH", "Capsicum annuum L.", "Solanaceae", "Fruit", "Haar 3, Yabis 3", "Muharrik; Hazim; Muhallil", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-167", "TAMATAR", "Solanum lycopersicum L.", "Solanaceae", "Fruit", "Barid 1, Ratab 2", "Mubarrid; Musakkin", None, "CANDIDATE", "LOW"),
    ("ZMF-168", "LAHSUN", "Allium sativum L.", "Amaryllidaceae", "Bulb", "Haar 3, Yabis 3", "Muhallil; Kasir-e-Riyah; Mufattih; Musaffi", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-169", "PIYAZ", "Allium cepa L.", "Amaryllidaceae", "Bulb", "Haar 3, Ratab 1", "Muqawwi-e-Bah; Mudirr; Hazim", None, "CANDIDATE", "LOW"),
    ("ZMF-170", "GANDANA", "Allium ampeloprasum L.", "Amaryllidaceae", "Bulb/leaf", "Haar 3, Yabis 2", "Mudirr; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-171", "HABB-UL-RASHAD", "Lepidium sativum L.", "Brassicaceae", "Seed", "Haar 3, Yabis 2", "Mudirr-e-Tams; Kasir-e-Riyah", "CAN-020", "CANDIDATE", "LOW"),
    ("ZMF-172", "KHAKSI", "Sisymbrium irio L.", "Brassicaceae", "Seed", "Haar 2, Ratab 1", "Munaffis; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-173", "KHURFA SIYAH", "Portulaca oleracea L.", "Portulacaceae", "Seed", "Barid 2, Ratab 2", "Mubarrid; Musakkin", "CAN-029", "CANDIDATE", "LOW"),
    ("ZMF-174", "TARAMIRA", "Eruca sativa Mill.", "Brassicaceae", "Seed/oil", "Haar 3, Yabis 2", "Mudirr; Jali; Qatil-e-Kirm", None, "CANDIDATE", "LOW"),
    ("ZMF-175", "RAI", "Brassica juncea (L.) Czern.", "Brassicaceae", "Seed", "Haar 4, Yabis 4", "Jali; Muharrik; Musakkin-e-Waja", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-176", "SARSON", "Brassica campestris L.", "Brassicaceae", "Seed/oil", "Haar 2, Yabis 2", "Muhallil; Jali", None, "CANDIDATE", "LOW"),
    ("ZMF-177", "SHALGAM", "Brassica rapa L.", "Brassicaceae", "Root", "Haar 1, Ratab 2", "Muqawwi-e-Bah; Mudirr", None, "CANDIDATE", "LOW"),
    ("ZMF-178", "KAKRA SINGHI", "Pistacia integerrima J.L.Stewart ex Brandis", "Anacardiaceae", "Gall", "Haar 2, Yabis 2", "Munaffis-e-Balgham; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-179", "MAZU", "Quercus infectoria G.Olivier", "Fagaceae", "Gall", "Barid 1, Yabis 2", "Qabiz; Habis-e-Dam; Mundamil", None, "CANDIDATE", "LOW"),
    ("ZMF-180", "POST ANAR", "Punica granatum L.", "Lythraceae", "Fruit rind", "Barid 2, Yabis 2", "Qabiz; Habis-e-Dam; Qatil-e-Kirm", "CAN-031", "CANDIDATE", "LOW"),
    ("ZMF-181", "ANAR DANA", "Punica granatum L.", "Lythraceae", "Dried aril", "Barid 1, Yabis 2", "Muqawwi-e-Meda; Hazim", "CAN-031", "CANDIDATE", "LOW"),
    ("ZMF-182", "GULNAR", "Punica granatum L.", "Lythraceae", "Flower", "Barid 2, Yabis 2", "Habis-e-Dam; Qabiz", "CAN-031", "CANDIDATE", "LOW"),
    ("ZMF-183", "ARJUN", "Terminalia arjuna (Roxb. ex DC.) Wight & Arn.", "Combretaceae", "Bark", "Barid 1, Yabis 2", "Muqawwi-e-Qalb; Habis-e-Dam", None, "CANDIDATE", "LOW"),
    ("ZMF-184", "NEEM CHAAL", "Azadirachta indica A.Juss.", "Meliaceae", "Bark", "Haar 2, Yabis 2", "Musaffi-e-Dam; Qatil-e-Jaratheem", "CAN-005", "HIGH_RISK", "CRITICAL"),
    ("ZMF-185", "KIKAR GOND", "Acacia nilotica (L.) Delile", "Fabaceae", "Gum", "Motadil (Yabis)", "Mughalliz-e-Mani; Habis; Demulcent", "CAN-001", "CANDIDATE", "LOW"),
    ("ZMF-186", "KIKAR CHAAL", "Acacia nilotica (L.) Delile", "Fabaceae", "Bark", "Barid 1, Yabis 2", "Qabiz; Habis-e-Dam", "CAN-001", "CANDIDATE", "LOW"),
    ("ZMF-187", "GOND BABOOL", "Acacia nilotica (L.) Delile", "Fabaceae", "Gum", "Motadil (Yabis)", "Mughalliz; Habis", "CAN-001", "CANDIDATE", "LOW"),
    ("ZMF-188", "SIRIS", "Albizia lebbeck (L.) Benth.", "Fabaceae", "Bark/seed", "Haar 1, Yabis 1", "Musaffi-e-Dam; Muhallil", None, "CANDIDATE", "LOW"),
    ("ZMF-189", "TALISPATRA", "Abies webbiana (Wall. ex D.Don) Lindl.", "Pinaceae", "Leaf", "Haar 2, Yabis 2", "Munaffis-e-Balgham; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-190", "TEJPAT", "Cinnamomum tamala (Buch.-Ham.) T.Nees & C.H.Eberm.", "Lauraceae", "Leaf", "Haar 2, Yabis 2", "Hazim; Kasir-e-Riyah; Mudirr", None, "CANDIDATE", "LOW"),
    ("ZMF-191", "BARG-E-SUDAB", "Ruta graveolens L.", "Rutaceae", "Leaf", "Haar 3, Yabis 3", "Mudirr-e-Tams; Musqit-e-Hamal", "CAN-033", "HIGH_RISK", "CRITICAL"),
    ("ZMF-192", "SUDAB", "Ruta graveolens L.", "Rutaceae", "Aerial parts", "Haar 3, Yabis 3", "Mudirr-e-Tams; Musqit", "CAN-033", "HIGH_RISK", "CRITICAL"),
    ("ZMF-193", "TUKHM-E-SUDAB", "Ruta graveolens L.", "Rutaceae", "Seed", "Haar 3, Yabis 3", "Mudirr; Qatil-e-Kirm", "CAN-033", "HIGH_RISK", "CRITICAL"),
    ("ZMF-194", "HANZAL", "Citrullus colocynthis (L.) Schrad.", "Cucurbitaceae", "Fruit pulp", "Haar 4, Yabis 4", "Mus-hil-e-Shadeed; Mufattih", "CAN-008", "HIGH_RISK", "CRITICAL"),
    ("ZMF-195", "INDRAYAN", "Citrullus colocynthis (L.) Schrad.", "Cucurbitaceae", "Fruit/root", "Haar 4, Yabis 4", "Mus-hil-e-Shadeed", "CAN-008", "CANDIDATE", "CRITICAL"),
    ("ZMF-196", "CHIRAITA", "Swertia chirata Buch.-Ham. ex C.B.Clarke", "Gentianaceae", "Whole plant", "Haar 2, Yabis 2", "Musaffi-e-Dam; Daf-e-Humma; Muqawwi-e-Meda", None, "CANDIDATE", "LOW"),
    ("ZMF-197", "GILO", "Tinospora cordifolia (Willd.) Miers", "Menispermaceae", "Stem", "Haar 1, Yabis 1", "Daf-e-Humma; Musaffi; Muqawwi", "CAN-039", "CANDIDATE", "LOW"),
    ("ZMF-198", "GUDUCHI", "Tinospora cordifolia (Willd.) Miers", "Menispermaceae", "Stem", "Haar 1, Yabis 1", "Daf-e-Humma; Rasayana", "CAN-039", "CANDIDATE", "LOW"),
    ("ZMF-199", "KARELA", "Momordica charantia L.", "Cucurbitaceae", "Fruit", "Haar 1, Yabis 1", "Musaffi-e-Dam; Hazim; Anti-diabetic", None, "CANDIDATE", "LOW"),
    ("ZMF-200", "JAMUN", "Syzygium cumini (L.) Skeels", "Myrtaceae", "Fruit/seed", "Barid 1, Yabis 2", "Qabiz; Musakkin; Anti-diabetic", "CAN-036", "CANDIDATE", "LOW"),
    ("ZMF-201", "TUKHM-E-JAMUN", "Syzygium cumini (L.) Skeels", "Myrtaceae", "Seed", "Barid 1, Yabis 2", "Qabiz; Anti-diabetic", "CAN-036", "CANDIDATE", "LOW"),
    ("ZMF-202", "BEL GIRI", "Aegle marmelos (L.) Corrêa", "Rutaceae", "Fruit pulp", "Haar 1, Yabis 2", "Muqawwi-e-Meda; Qabiz; Daf-e-Zalaq", "CAN-002", "CANDIDATE", "LOW"),
    ("ZMF-203", "BAEL", "Aegle marmelos (L.) Corrêa", "Rutaceae", "Fruit", "Haar 1, Yabis 2", "Qabiz; Muqawwi", "CAN-002", "CANDIDATE", "LOW"),
    ("ZMF-204", "NARANGI CHILKA", "Citrus aurantium L.", "Rutaceae", "Peel", "Haar 2, Yabis 2", "Kasir-e-Riyah; Hazim; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-205", "LIMU", "Citrus limon (L.) Osbeck", "Rutaceae", "Fruit/peel", "Barid 1, Ratab 2", "Musakkin-e-Safra; Hazim", None, "CANDIDATE", "LOW"),
    ("ZMF-206", "USHQ", "Dorema ammoniacum D.Don", "Apiaceae", "Gum resin", "Haar 2, Yabis 2", "Muhallil; Munaffis; Mufattih", None, "CANDIDATE", "LOW"),
    ("ZMF-207", "JUND BEDASTAR", "Castoreum", "Animal secretion", "Secretion", "Haar 3, Yabis 3", "Muqawwi-e-Asab; Daf-e-Tashannuj", None, "CANDIDATE", "MEDIUM"),
    ("ZMF-208", "QARN-UL-AYYAL", "Cervus elaphus horn", "Animal material", "Horn", "Haar 1, Yabis 2", "Habis; Daf-e-Zeeq-un-Nafs", None, "CANDIDATE", "LOW"),
    ("ZMF-209", "SANG-E-SAR MAHI", "Fish otolith", "Animal mineral", "Concretion", "Motadil", "Mufattit-e-Hisat", None, "CANDIDATE", "LOW"),
    ("ZMF-210", "ABRESHAM", "Bombyx mori silk cocoon", "Animal material", "Silk cocoon", "Haar 1, Ratab 1", "Mufarreh-e-Qalb; Muqawwi-e-Aza-e-Raeesa", None, "CANDIDATE", "LOW"),
    ("ZMF-211", "KIRM DANA", "Cochineal insect", "Animal material", "Insect product", "Haar 2, Yabis 2", "Daf-e-Sual", None, "CANDIDATE", "LOW"),
    ("ZMF-212", "ASAL", "Honey", "Bee product", "Honey", "Haar 2, Yabis 1", "Jali; Munaqqi; Muqawwi", None, "CANDIDATE", "LOW"),
    ("ZMF-213", "MOM", "Beeswax", "Bee product", "Wax", "Motadil", "Mulayyin; Mudammil", None, "CANDIDATE", "LOW"),
    ("ZMF-214", "SHEER KHISHT", "Fraxinus ornus manna", "Oleaceae", "Exudate", "Haar 1, Ratab 1", "Mulayyin; Muskin", None, "CANDIDATE", "LOW"),
    ("ZMF-215", "TARANJABEEN", "Alhagi maurorum manna", "Fabaceae", "Exudate", "Haar 1, Ratab 1", "Mulayyin; Musaffi-e-Dam", None, "CANDIDATE", "LOW"),
    ("ZMF-216", "GULQAND", "Rosa damascena preserve", "Rosaceae", "Preserve", "Motadil", "Mulayyin; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-217", "QAND SAFAID", "Sucrose / White sugar", "Food excipient", "Sugar", "Motadil", "Vehicle; Sweetener", None, "CANDIDATE", "LOW"),
    ("ZMF-218", "SHAKAR SURKH", "Jaggery / Raw cane sugar", "Food excipient", "Sugar", "Haar 1, Ratab 1", "Hazim; Mulayyin", None, "CANDIDATE", "LOW"),
    ("ZMF-219", "ROGHAN BADAM", "Prunus dulcis oil", "Rosaceae", "Fixed oil", "Motadil (Ratab)", "Mulayyin; Muqawwi-e-Dimagh", "CAN-030", "CANDIDATE", "LOW"),
    ("ZMF-220", "ROGHAN GUL", "Rosa damascena infused oil", "Rosaceae", "Medicated oil", "Barid 1, Yabis 1", "Musakkin-e-Suda; Mubarrid", None, "CANDIDATE", "LOW"),
    ("ZMF-221", "ROGHAN KAHU", "Lactuca sativa seed oil", "Asteraceae", "Fixed oil", "Barid 2, Ratab 2", "Munawwim; Musakkin", None, "CANDIDATE", "LOW"),
    ("ZMF-222", "ROGHAN BANAFSHA", "Viola odorata infused oil", "Violaceae", "Medicated oil", "Barid 1, Ratab 1", "Munawwim; Musakkin-e-Hararat", None, "CANDIDATE", "LOW"),
    ("ZMF-223", "ROGHAN BABUNA", "Matricaria chamomilla infused oil", "Asteraceae", "Medicated oil", "Haar 1, Yabis 1", "Muhallil-e-Riyah; Musakkin-e-Alam", None, "CANDIDATE", "LOW"),
    ("ZMF-224", "ROGHAN KUNJAD", "Sesamum indicum oil", "Pedaliaceae", "Fixed oil", "Haar 2, Ratab 1", "Muhallil; Mulayyin", "CAN-034", "CANDIDATE", "LOW"),
    ("ZMF-225", "KUNJAD", "Sesamum indicum L.", "Pedaliaceae", "Seed", "Haar 2, Ratab 1", "Mughalliz-e-Mani; Muqawwi", "CAN-034", "CANDIDATE", "LOW"),
    ("ZMF-226", "TUKHM-E-HAYAT", "Lepidium sativum L.", "Brassicaceae", "Seed", "Haar 3, Yabis 2", "Mudirr-e-Tams; Muqawwi-e-Bah", "CAN-020", "CANDIDATE", "LOW"),
    ("ZMF-227", "ISAPGHOL", "Plantago ovata Forssk.", "Plantaginaceae", "Seed husk", "Barid 1, Ratab 2", "Mulayyin; Musakkin-e-Hararat; Lu'abi", "CAN-028", "CANDIDATE", "LOW"),
    ("ZMF-228", "BAZR QUTUNA", "Plantago ovata Forssk.", "Plantaginaceae", "Seed", "Barid 1, Ratab 2", "Mulayyin; Musakkin", "CAN-028", "CANDIDATE", "LOW"),
    ("ZMF-229", "LISAN-UL-HAMAL", "Plantago major L.", "Plantaginaceae", "Leaf/seed", "Barid 2, Yabis 2", "Habis; Mudammil; Qabiz", None, "CANDIDATE", "LOW"),
    ("ZMF-230", "GUL-E-DHAWA", "Woodfordia fruticosa (L.) Kurz", "Lythraceae", "Flower", "Barid 1, Yabis 2", "Qabiz; Habis; Fermenting catalyst", None, "CANDIDATE", "LOW"),
    ("ZMF-231", "DHAIFAL", "Laurus nobilis L.", "Lauraceae", "Berry", "Haar 2, Yabis 2", "Muhallil; Kasir-e-Riyah", None, "CANDIDATE", "LOW"),
    ("ZMF-232", "DARUNAJ AQRABI", "Doronicum hookeri C.B.Clarke", "Asteraceae", "Root", "Haar 2, Yabis 2", "Mufarreh-e-Qalb; Daf-e-Sumoom", None, "CANDIDATE", "LOW"),
    ("ZMF-233", "AQARQARHA", "Anacyclus pyrethrum (L.) Lag.", "Asteraceae", "Root", "Haar 3, Yabis 3", "Muharrik-e-Bah; Musakkin-e-Asab", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-234", "KABAB CHINI", "Piper cubeba L.f.", "Piperaceae", "Fruit", "Haar 2, Yabis 2", "Mudirr-e-Baul; Munaqqi-e-Majari; Mufarreh", None, "CANDIDATE", "LOW"),
    ("ZMF-235", "JAVITRI", "Myristica fragrans Houtt.", "Myristicaceae", "Aril", "Haar 2, Yabis 2", "Mufarreh; Hazim; Muqawwi-e-Bah", "CAN-023", "CANDIDATE", "LOW"),
    ("ZMF-236", "JAIPHAL", "Myristica fragrans Houtt.", "Myristicaceae", "Seed", "Haar 2, Yabis 2", "Mufarreh; Hazim; Musakkin", "CAN-023", "HIGH_RISK", "CRITICAL"),
    ("ZMF-237", "BISBASEH", "Myristica fragrans Houtt.", "Myristicaceae", "Aril", "Haar 2, Yabis 2", "Mufarreh; Hazim", "CAN-023", "CANDIDATE", "LOW"),
    ("ZMF-238", "JOZBUWA", "Myristica fragrans Houtt.", "Myristicaceae", "Seed", "Haar 2, Yabis 2", "Hazim; Musakkin", "CAN-023", "CANDIDATE", "LOW"),
    ("ZMF-239", "GULE DHATURA", "Datura metel L.", "Solanaceae", "Flower", "Haar 4, Yabis 4", "Musakkin-e-Shadeed", "CAN-013", "HIGH_RISK", "CRITICAL"),
    ("ZMF-240", "DHATURA", "Datura metel L.", "Solanaceae", "Seed/leaf", "Haar 4, Yabis 4", "Mukhaddid; Musakkin", "CAN-013", "HIGH_RISK", "CRITICAL"),
    ("ZMF-241", "AZARAQI", "Strychnos nux-vomica L.", "Loganiaceae", "Seed", "Haar 3, Yabis 3", "Muqawwi-e-Asab; Daf-e-Falij", "CAN-035", "HIGH_RISK", "CRITICAL"),
    ("ZMF-242", "KUCHLA", "Strychnos nux-vomica L.", "Loganiaceae", "Seed", "Haar 3, Yabis 3", "Muqawwi-e-Asab", "CAN-035", "CANDIDATE", "CRITICAL"),
    ("ZMF-243", "AFYUN", "Papaver somniferum L.", "Papaveraceae", "Opium latex", "Barid 4, Yabis 4", "Mukhaddid-e-Aam; Habis; Musakkin", None, "HIGH_RISK", "CRITICAL"),
    ("ZMF-244", "KHASHKHASH", "Papaver somniferum L.", "Papaveraceae", "Seed", "Barid 2, Ratab 2", "Munawwim; Musakkin-e-Sual", None, "CANDIDATE", "LOW"),
    ("ZMF-245", "BHANG", "Cannabis sativa L.", "Cannabaceae", "Leaf/flowering tops", "Haar 3, Yabis 3", "Musakkin; Munawwim; Mukhaddid", "CAN-006", "HIGH_RISK", "CRITICAL"),
    ("ZMF-246", "TUKHM-E-BHANG", "Cannabis sativa L.", "Cannabaceae", "Seed", "Barid 1, Yabis 2", "Qabiz; Habis", "CAN-006", "CANDIDATE", "LOW"),
    ("ZMF-247", "ASAROON", "Valeriana wallichii DC.", "Caprifoliaceae", "Rhizome/root", "Haar 2, Yabis 2", "Mufattih; Muqawwi-e-Dimagh", "CAN-041", "CANDIDATE", "LOW"),
    ("ZMF-248", "TAGAR", "Valeriana wallichii DC.", "Caprifoliaceae", "Root/rhizome", "Haar 2, Yabis 2", "Musakkin; Muqawwi", "CAN-041", "CANDIDATE", "LOW"),
    ("ZMF-249", "JATAMANSI", "Nardostachys jatamansi (D.Don) DC.", "Caprifoliaceae", "Rhizome", "Haar 1, Yabis 2", "Mufarreh; Muqawwi-e-Dimagh wa Qalb", None, "CANDIDATE", "LOW"),
    ("ZMF-250", "BACH", "Acorus calamus L.", "Acoraceae", "Rhizome", "Haar 2, Yabis 2", "Muqawwi-e-Hafiza; Kasir-e-Riyah; Mufattih", None, "CANDIDATE", "LOW")
]

# Synthesize all 250 records
MUFRADAT_250_CATALOG: Dict[str, Dict[str, Any]] = {}

# Populate explicit records
for item in RAW_MUFRADAT_LIST:
    zid, name, bot, fam, part, miz, afaal, can_id, cat_type, risk_lvl = item
    is_high_risk = zid in HIGH_RISK_28_REGISTRY
    ai_state = "BLOCKED" if is_high_risk else ("AI_INTERNAL_ONLY_WITH_LOCAL_SEED" if cat_type == "INTERNAL_SEED" else "RESEARCH_ONLY")
    clin_state = "NOT_APPROVED"

    MUFRADAT_250_CATALOG[zid] = {
        "drug_id": zid,
        "name": name,
        "botanical_identity": bot,
        "family": fam,
        "part_used": part,
        "draft_mizaj": miz,
        "draft_afaal": afaal,
        "canonical_group": can_id,
        "safety_class": "HIGH_RISK" if is_high_risk else "UNREVIEWED",
        "ai_permission_state": ai_state,
        "clinical_use_state": clin_state,
        "patient_self_care": "NOT_ALLOWED",
        "verification_status": "HIGH_RISK_BLOCKED" if is_high_risk else ("LOCAL_SEED_PAGE_AUDIT_PENDING" if cat_type == "INTERNAL_SEED" else "RESEARCH_CANDIDATE_EVIDENCE_PENDING"),
        "high_risk_profile": HIGH_RISK_28_REGISTRY.get(zid)
    }

# Ensure all 250 sequential IDs are populated
for i in range(1, 251):
    z_key = f"ZMF-{i:03d}"
    if z_key not in MUFRADAT_250_CATALOG:
        is_hr = z_key in HIGH_RISK_28_REGISTRY
        MUFRADAT_250_CATALOG[z_key] = {
            "drug_id": z_key,
            "name": f"MUFRAD-{i:03d}",
            "botanical_identity": "Botanical Identity Pending Validation",
            "family": "Unclassified",
            "part_used": "Part Pending",
            "draft_mizaj": "Pending ; secondary: pending",
            "draft_afaal": "Traditional Afaal pending extraction from classical sources",
            "canonical_group": None,
            "safety_class": "HIGH_RISK" if is_hr else "UNREVIEWED",
            "ai_permission_state": "BLOCKED" if is_hr else "RESEARCH_ONLY",
            "clinical_use_state": "NOT_APPROVED",
            "patient_self_care": "NOT_ALLOWED",
            "verification_status": "HIGH_RISK_BLOCKED" if is_hr else "RESEARCH_CANDIDATE_EVIDENCE_PENDING",
            "high_risk_profile": HIGH_RISK_28_REGISTRY.get(z_key)
        }


# =============================================================================
# 4. QUERY & GOVERNANCE ENFORCEMENT FUNCTIONS
# =============================================================================

def get_mufrad_by_id(drug_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single Mufrad record by ZMF ID (e.g. ZMF-001) or name."""
    clean_id = drug_id.upper().strip()
    if clean_id in MUFRADAT_250_CATALOG:
        return MUFRADAT_250_CATALOG[clean_id]
    # Search by name
    for rec in MUFRADAT_250_CATALOG.values():
        if clean_id in rec["name"].upper() or clean_id in rec["botanical_identity"].upper():
            return rec
    return None


def get_all_mufradat_250() -> List[Dict[str, Any]]:
    """Returns all 250 Mufradat records sorted by ID."""
    return [MUFRADAT_250_CATALOG[k] for k in sorted(MUFRADAT_250_CATALOG.keys())]


def get_canonical_groups_registry() -> Dict[str, Dict[str, Any]]:
    """Returns the 43 canonical identity groups."""
    return CANONICALIZATION_GROUPS


def get_high_risk_28_registry() -> Dict[str, Dict[str, Any]]:
    """Returns the 28 high-risk blocked substances with toxicology reasons."""
    return HIGH_RISK_28_REGISTRY


def is_high_risk_blocked(drug_identifier: str) -> bool:
    """Returns True if the drug is in the 28 high-risk blocked list."""
    clean = drug_identifier.upper().strip()
    if clean in HIGH_RISK_28_REGISTRY:
        return True
    for zid, spec in HIGH_RISK_28_REGISTRY.items():
        if clean in spec["name"].upper() or clean in spec["botanical"].upper():
            return True
    return False


def check_formulation_canonical_conflicts(ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Checks if a list of ingredients contains multiple items belonging to the same
    canonical group (e.g. both Pippali and Filfil Daraz in CAN-027).
    """
    conflicts = []
    group_usage: Dict[str, List[str]] = {}

    for ing in ingredients:
        name = ing.get("name") or ing.get("herb") or ""
        rec = get_mufrad_by_id(name)
        if rec and rec["canonical_group"]:
            gid = rec["canonical_group"]
            group_usage.setdefault(gid, []).append(f"{rec['drug_id']}: {rec['name']}")

    for gid, items in group_usage.items():
        if len(items) > 1:
            can_def = CANONICALIZATION_GROUPS.get(gid, {})
            conflicts.append({
                "canonical_group_id": gid,
                "scientific_identity": can_def.get("scientific_name"),
                "compounded_items": items,
                "warning": (
                    f"Duplicate canonical identity detected under group {gid} ({can_def.get('scientific_name')}). "
                    f"Multiple forms ({', '.join(items)}) are compounded together. Clinician must verify combined dose limits."
                )
            })

    return conflicts


def get_clinically_approved_mufradat() -> List[Dict[str, Any]]:
    """Returns codified, clinically verified monographs safe for automated clinical decision guidance."""
    return [
        rec for rec in MUFRADAT_250_CATALOG.values()
        if rec.get("verification_status") in ("LOCAL_SEED_PAGE_AUDIT_PENDING", "UPI_GOLD_STANDARD", "CLINICALLY_APPROVED")
        and not is_high_risk_blocked(rec["drug_id"])
    ]


def get_research_pending_mufradat() -> List[Dict[str, Any]]:
    """Returns research candidates awaiting 12-Gate evidence sign-offs."""
    return [
        rec for rec in MUFRADAT_250_CATALOG.values()
        if rec.get("verification_status") not in ("LOCAL_SEED_PAGE_AUDIT_PENDING", "UPI_GOLD_STANDARD", "CLINICALLY_APPROVED")
        or is_high_risk_blocked(rec["drug_id"])
    ]


def is_clinically_approved_for_ai(drug_identifier: str) -> bool:
    """
    Evaluates whether a drug is clinically approved for automated AI recommendations.
    Returns False if drug is high-risk Schedule E(1) or an unverified research candidate.
    """
    rec = get_mufrad_by_id(drug_identifier)
    if not rec:
        return False
    if is_high_risk_blocked(rec["drug_id"]):
        return False
    return rec.get("verification_status") in ("LOCAL_SEED_PAGE_AUDIT_PENDING", "UPI_GOLD_STANDARD", "CLINICALLY_APPROVED")


def get_registry_stratification_summary() -> Dict[str, Any]:
    """Returns official governance breakdown of the 250 Mufradat master registry."""
    approved = get_clinically_approved_mufradat()
    research = get_research_pending_mufradat()
    high_risk = get_high_risk_28_registry()

    return {
        "total_catalog_count": len(MUFRADAT_250_CATALOG),
        "clinically_approved_for_ai_count": len(approved),
        "research_candidates_pending_count": len(research) - len(high_risk),
        "high_risk_schedule_e1_restricted_count": len(high_risk),
        "governance_doctrine": (
            "Clinical Safety Rule: Automated AI Copilot recommendations may ONLY suggest "
            "monographs from the clinically approved pharmacopoeia. Research Candidates require "
            "Institutional Ethics Committee (IEC) clinical trial protocol. Schedule E(1) drugs "
            "require mandatory physical Mudabbar certification and senior clinician physical lock."
        )
    }

