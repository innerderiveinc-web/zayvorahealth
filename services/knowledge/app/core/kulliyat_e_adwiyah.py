"""
ZAYVORA Health OS™ — Kulliyat-e-Adwiyah (Fundamentals of Unani Pharmacology)
=============================================================================
Authoritative Codification of 'Ishrah al-Adwiyah' (Kulliyat-e-Adwiyah)
By Dr. Abdul Wadud, M.D. (Ilmul Advia) AMU Aligarh;
Reader, Dept of Ilmul Advia, S.H. Unani Tibbiya College, Burhanpur (M.P.).
First Edition, 2004.

Definitive Epistemological Bridge between Classical Unani Pharmacology
(Ibn Sina, Al-Razi, Ibn al-Baitar, Qarshi) and Modern Pharmacological Science
(Stereochemistry, Receptor Binding, Pharmacokinetics, Biotransformation,
Pharmacodynamics, Drug Antagonism, and Standardized Terminology).
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import hashlib

# =============================================================================
# 1. CANONICAL WORK METADATA
# =============================================================================

ISHRAH_AL_ADWIYAH_METADATA: Dict[str, Any] = {
    "source_id": "SRC-WADUD-ISHRAH-ADWIYAH-2004",
    "title": "Ishrah al-Adwiyah (Kulliyat-e-Adwiyah)",
    "title_urdu": "اشراح الادویہ (کلیات ادویہ)",
    "author": "Dr. Abdul Wadud",
    "author_qualification": "M.D. (Ilmul Advia) AMU Aligarh",
    "author_designation": "Reader, Department of Ilmul Advia, S.H. Unani Tibbiya College, Burhanpur (M.P.)",
    "publisher": "Yasir Faraz / Mumtaz Screen Printers, Burhanpur",
    "edition": "First Edition, 2004",
    "total_pages": 176,
    "language": "Urdu with English Pharmacological Equivalence",
    "discipline": "Kulliyat-e-Adwiyah (General Principles of Unani Pharmacology & Pharmacognosy)",
    "digital_sha256": hashlib.sha256(b"ISHRAH-AL-ADWIYAH-DR-ABDUL-WADUD-2004-AMU").hexdigest(),
    "scholarly_importance": (
        "Core reference work for BUMS and MD (Ilmul Advia) across Indian Unani Medical Colleges. "
        "Provides precise 1:1 harmonization between classical Unani pharmacology terms "
        "and modern pharmacodynamics, mechanism of action, biotransformation, and drug antagonism."
    )
}

# =============================================================================
# 2. THE 9 TASTES (ZA'IQAH) & PHARMACODYNAMICS (pp. 41-43)
# =============================================================================

TASTE_PHARMACODYNAMICS: Dict[str, Dict[str, Any]] = {
    "huraif": {
        "taste_id": "huraif",
        "name_urdu": "حریف (تیز / چرپرا)",
        "name_english": "Pungent / Acrid",
        "elemental_mizaj": "Hot & Dry (Har-Yabis)",
        "representative_drugs": ["Filfil Siyah (Black Pepper)", "Rai (Mustard)", "Zanjabeel (Ginger)", "Aaqarqarha"],
        "primary_actions": [
            "Mufattih-e-Urooq (Vasodilator)",
            "Musakhkhin (Calorific / Heating)",
            "Mulattif (Attenuant / Demulcent)",
            "Muraqqiq (Liquefying)",
            "Muhallil (Resolvent / Anti-inflammatory)",
            "Mani-e-Ufoonat (Antiseptic)"
        ],
        "mechanism": "Stimulates local heat and blood flow; disperses accumulated phlegm and cold morbid humours."
    },
    "murr": {
        "taste_id": "murr",
        "name_urdu": "مر (تلخ / کڑوا)",
        "name_english": "Harsh-Bitter",
        "elemental_mizaj": "Hot & Dry (Har-Yabis)",
        "representative_drugs": ["Chiraita", "Shahtara", "Afsanteen", "Neem"],
        "primary_actions": [
            "Mufattih-e-Urooq (Deobstruent)",
            "Musakhkhin (Mild Heating)",
            "Mulattif (Attenuant)",
            "Muhallil (Resolvent)",
            "Mani-e-Ufoonat (Antiseptic / Antibacterial)",
            "Musaffi-e-Dam (Blood Purifier)"
        ],
        "mechanism": "Purges visceral obstructions, combats sepsis and fermentation, tones gastrointestinal lining."
    },
    "maleh": {
        "taste_id": "maleh",
        "name_urdu": "مالح (نمکین)",
        "name_english": "Salty",
        "elemental_mizaj": "Hot & Dry (Har-Yabis)",
        "representative_drugs": ["Namak Ta'am (Rock/Table Salt)", "Shura Qalmi", "Jawakhar"],
        "primary_actions": [
            "Mufattih-e-Urooq (Deobstruent)",
            "Musakhkhin (Calorific)",
            "Mulattif (Attenuant)",
            "Muraqqiq (Liquefying)",
            "Muhallil (Resolvent)",
            "Mani-e-Ufoonat (Antiseptic)",
            "Qati-e-Mawad (Matter-cleaving)",
            "Jaazib (Absorbent)"
        ],
        "mechanism": "Dissolves viscous humoral coagulates through osmotic draw and drying action."
    },
    "hamez": {
        "taste_id": "hamez",
        "name_urdu": "حامض (کھٹا / ترش)",
        "name_english": "Acidic / Sour",
        "elemental_mizaj": "Cold & Dry (Barid-Yabis)",
        "representative_drugs": ["Aab-e-Lemu (Lemon)", "Aloo Bukhara", "Imli (Tamarind)", "Sirka (Vinegar)"],
        "primary_actions": [
            "Mufattih-e-Urooq (Deobstruent)",
            "Mulattif (Attenuant)",
            "Muraqqiq (Liquefying)",
            "Qati-e-Mawad (Matter-cleaving)",
            "Dafi-e-Atash (Thirst-quenching)",
            "Mubarrid (Refrigerant)",
            "Mudirr-e-Baul (Mild Diuretic)"
        ],
        "mechanism": "Suppresses bilious inflammation and metabolic heat; promotes diuresis and cuts phlegm."
    },
    "afas": {
        "taste_id": "afas",
        "name_urdu": "عفص (کسیلا)",
        "name_english": "Astringent-Bitter / Tannic",
        "elemental_mizaj": "Cold & Dry (Barid-Yabis)",
        "representative_drugs": ["Phitkari (Alum)", "Mazoo (Oak Gall)", "Post-e-Anar (Pomegranate Rind)"],
        "primary_actions": [
            "Raadi' (Repellent / Deflector)",
            "Aasir (Compressor / Tissue-constricting)",
            "Musallib (Hardener / Sclerotic)",
            "Mukaththif (Condenser / Viscositive)",
            "Habis-e-Dam (Haemostatic / Styptic)",
            "Qabiz (Astringent)"
        ],
        "mechanism": "Precipitates mucous membrane proteins (tannin effect), contracts relaxed tissue and arrests bleeding."
    },
    "qabiz": {
        "taste_id": "qabiz",
        "name_urdu": "قابض (پھیکا سکڑاؤ دار)",
        "name_english": "Pure Astringent",
        "elemental_mizaj": "Cold & Dry (Barid-Yabis)",
        "representative_drugs": ["Chhalia (Areca Nut)", "Hab-ul-Aas (Myrtle)", "Katha"],
        "primary_actions": [
            "Raadi' (Repellent)",
            "Aasir (Squeezer)",
            "Qabiz (Astringent)",
            "Habis (Arresting secretions)",
            "Mukaththif (Condenser)",
            "Mubarrid (Cooling)"
        ],
        "mechanism": "Reduces secretory leakage from capillaries and mucus glands by constricting cellular pore diameter."
    },
    "dasm": {
        "taste_id": "dasm",
        "name_urdu": "دسم (پھیکا چکنا / چرب)",
        "name_english": "Bland / Fatty / Unctuous",
        "elemental_mizaj": "Warm & Moist (Moderate)",
        "representative_drugs": ["Ghee", "Roghan Zaitoon (Olive Oil)", "Roghan Badam (Almond Oil)"],
        "primary_actions": [
            "Murattib (Moisturizing / Hydrating)",
            "Muraqqiq (Emollient)",
            "Murkhi (Relaxant / Antispasmodic)",
            "Mulayyin (Laxative / Aperient)",
            "Munzij (Concoctive)"
        ],
        "mechanism": "Soothes irritated mucous lining, softens hard humoral matter, and relieves muscular tension."
    },
    "hilw": {
        "taste_id": "hilw",
        "name_urdu": "حلو (شیریں / میٹھا)",
        "name_english": "Sweet",
        "elemental_mizaj": "Warm & Moist (Har-Rattab)",
        "representative_drugs": ["Shahd (Honey)", "Qand (Cane Sugar)", "Munaqqa", "Injeer (Fig)"],
        "primary_actions": [
            "Jali (Detergent / Cleansing)",
            "Mulayyin (Mild Laxative)",
            "Muraqqiq (Diluent)",
            "Murkhi (Relaxant)",
            "Musakhkhin (Calorific / Nourishing)",
            "Muqawwi-e-Aaza (Vital Organ Tonic)"
        ],
        "mechanism": "Rapid systemic assimilation; provides substrate for innate heat (Hararat Ghariziyyah) and cleanses ulcers."
    },
    "tafi": {
        "taste_id": "tafi",
        "name_urdu": "تفہ / تفسیخہ (بے مزا / پھیکا)",
        "name_english": "Tasteless / Insipid",
        "elemental_mizaj": "Cold & Moist / Neutral",
        "representative_drugs": ["Aab-e-Muqattar (Distilled Water)", "Nishashta (Starch)", "Lu'ab-e-Aspaghol"],
        "primary_actions": [
            "Murattib (Moisturizing)",
            "Musakkin (Demulcent / Soothing)",
            "Mubarrid (Cooling)"
        ],
        "mechanism": "Passive hydration, buffering harsh medicinal substances, and demulcent mucosal protection."
    }
}

# =============================================================================
# 3. THE 4 DEGREES OF TEMPERAMENT & POISON THRESHOLD (pp. 23-26)
# =============================================================================

TEMPERAMENT_DEGREES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "darjah_1": {
        "degree": 1,
        "name_urdu": "درجہ اول",
        "name_english": "First Degree",
        "clinical_definition": (
            "Drugs that induce a mild physiological shift in the body's temperament, "
            "which is imperceptible upon a single standard therapeutic dose, but becomes "
            "observable and clinically active upon repeated administration."
        ),
        "safety_margin": "Extremely safe; minimal risk of systemic disturbance.",
        "examples": ["Gaozaban", "Banafsha", "Behidana", "Khashkhash"]
    },
    "darjah_2": {
        "degree": 2,
        "name_urdu": "درجہ دوم",
        "name_english": "Second Degree",
        "clinical_definition": (
            "Drugs whose temperamental action is distinctly perceptible by the body upon "
            "a single therapeutic dose, but which do not cause functional disruption, injury, "
            "or organ impairment in standard therapeutic dosage."
        ),
        "safety_margin": "Safe for standard clinical prescription; monitor duration.",
        "examples": ["Zanjabeel", "Asgandh", "Kishneez Khushk", "Babchi"]
    },
    "darjah_3": {
        "degree": 3,
        "name_urdu": "درجہ سوم",
        "name_english": "Third Degree",
        "clinical_definition": (
            "Drugs whose action strongly affects normal physiological equilibrium, producing "
            "marked functional changes (intense diuresis, diaphoresis, sedation, or gastrointestinal evacuation). "
            "Excessive dosage or prolonged unmonitored use causes clinical toxicity."
        ),
        "safety_margin": "Narrow therapeutic index; requires strict posology and corrective adjuvants (Muslehat).",
        "examples": ["Suranjan Shirin", "Turbud", "Saqmonia", "Afeeyun (Low Dose)"]
    },
    "darjah_4": {
        "degree": 4,
        "name_urdu": "درجہ چہارم (ادویہ سمیہ)",
        "name_english": "Fourth Degree (Toxic / Poisonous Drugs)",
        "clinical_definition": (
            "Drugs possessing such extreme elemental heat, cold, or dryness that they can "
            "corrupt vital physiological functions, cause tissue destruction, and prove fatal "
            "if administered in raw state without precise posology and mandatory purification."
        ),
        "paracelsus_avicenna_invariant": (
            "It is the dose which distinguishes the drug from a poison (Dawa-e-Sammi vs Summ-e-Mutlaq). "
            "While an Absolute Poison (Summ-e-Mutlaq, e.g. Potassium Cyanide) possesses zero therapeutic window, "
            "a 4th-degree drug is a potent therapeutic agent when properly processed (Mudabbar) and micro-dosed."
        ),
        "mandatory_controls": [
            "Mandatory Schedule E(1) Mudabbar Detoxification SOP verification",
            "Double-signoff clinical authorization",
            "Microgram/milligram posology calibration"
        ],
        "examples": ["Kuchla (Strychnos nux-vomica)", "Bhang (Cannabis sativa)", "Sankhiya (Arsenic)", "Afeeyun (Opium)"]
    }
}

# =============================================================================
# 4. THE 8 STATUTORY RULES OF COMPOUNDING (QAWANIN-E-TARKEEB, pp. 91-94)
# =============================================================================

COMPOUNDING_RULES: List[Dict[str, Any]] = [
    {
        "rule_number": 1,
        "rationale_code": "ISLAH",
        "name_urdu": "دوا کی اصلاح (Correction of Drug)",
        "name_english": "Correction / Toxicity Mitigation",
        "principle": (
            "Adding a corrective adjuvant (Musleh) to mitigate the adverse side effects, "
            "irritation, or harshness of the primary therapeutic drug (e.g., adding Roghan Badam "
            "to Jalapa/Turbud to prevent violent intestinal griping and dehydration)."
        )
    },
    {
        "rule_number": 2,
        "rationale_code": "IDHAFAH_QUWWAT",
        "name_urdu": "اضافت قوت (Increase Potency / Synergism)",
        "name_english": "Synergistic Potentiation",
        "principle": (
            "Combining two or more substances with complementary actions to amplify therapeutic "
            "efficacy without needing to escalate single-drug dosage into the toxic threshold "
            "(e.g., combining Paracetamol with Ibuprofen in modern pharmacology, or Asgandh with Suranjan in Unani)."
        )
    },
    {
        "rule_number": 3,
        "rationale_code": "TAZEEF_AMAL",
        "name_urdu": "تضعیف عمل (Decrease Action / Attenuation)",
        "name_english": "Action Attenuation / Moderation",
        "principle": (
            "Tempering an overly violent or drastic action when patient constitution or "
            "disease severity warrants gentler evacuation (e.g., combining an astringent with a harsh purgative)."
        )
    },
    {
        "rule_number": 4,
        "rationale_code": "SURAT_NUFOOZ",
        "name_urdu": "سرعت نفوذ (Increase Rate of Absorption)",
        "name_english": "Absorption Acceleration & Organ Targeting",
        "principle": (
            "Adding a rapidly penetrative carrier (Badraqa) to speed up absorption and deliver the drug "
            "swiftly to target tissues (e.g., using Sharab/Araq or Zafaran to speed delivery to cardiac/brain tissue)."
        )
    },
    {
        "rule_number": 5,
        "rationale_code": "IBTA_NUFOOZ",
        "name_urdu": "ابطاء نفوذ (Decrease Rate of Absorption / Sustained Release)",
        "name_english": "Absorption Retardation / Sustained Local Action",
        "principle": (
            "Adding an oily, viscous, or demulcent vehicle to retard drug transit and absorption, "
            "ensuring prolonged contact with gastrointestinal mucosa for local therapeutic action "
            "(e.g., mixing Kuchla with ghee or butter to delay absorption)."
        )
    },
    {
        "rule_number": 6,
        "rationale_code": "AMRAZ_MURAKKABAH",
        "name_urdu": "امراض مرکبہ کا علاج (Treatment of Compound Diseases)",
        "name_english": "Multi-Morbidity / Compound Pathology Targeting",
        "principle": (
            "Addressing concurrent multi-organ pathology or opposing disease states in a single patient "
            "(e.g., combining a febrifuge with an expectorant in acute febrile bronchitis)."
        )
    },
    {
        "rule_number": 7,
        "rationale_code": "MIQDAR_VOLUME",
        "name_urdu": "مقدار میں اضافہ (Increase Volume / Bulking)",
        "name_english": "Volume Expansion & Palatability Bulking",
        "principle": (
            "Expanding the volume of potent, minute-dose drugs with safe bulking media (syrup, honey, seed mucilage) "
            "to facilitate accurate oral dosing, swallowability, and patient compliance."
        )
    },
    {
        "rule_number": 8,
        "rationale_code": "TAHAFFUZ_PRESERVATION",
        "name_urdu": "تحفظ ادویہ (Preservation of Drugs)",
        "name_english": "Preservation & Shelf-Life Stabilization",
        "principle": (
            "Incorporating natural preservative matrices (such as high-Brix honey, cane sugar syrup, vinegar, or alcohol) "
            "to prevent microbial growth, oxidative degradation, and fermentation over multi-year storage."
        )
    }
]

# =============================================================================
# 5. DRUG ANTAGONISM (TANAQUZ-E-ADWIYAH, pp. 96-97)
# =============================================================================

ANTAGONISM_TYPES: Dict[str, Dict[str, Any]] = {
    "pharmacological": {
        "term_urdu": "تناقض فعلی",
        "term_english": "Pharmacological Antagonism",
        "definition": (
            "Occurs when two drugs exert opposing physiological actions on the same organ system or receptor "
            "(e.g., co-administering a strong purgative like Saqmonia with an intestinal astringent like Mazoo, "
            "or a stimulant like Kuchla with a heavy sedative like Afeeyun)."
        ),
        "clinical_management": "Avoid simultaneous administration; separate timing by at least 4 to 6 hours."
    },
    "chemical": {
        "term_urdu": "تناقض صوری (کیمیائی)",
        "term_english": "Chemical Antagonism",
        "definition": (
            "Occurs when two co-administered chemical substances react chemically in the stomach or bloodstream, "
            "forming an insoluble precipitate, neutral salt, or gas that completely destroys therapeutic potency "
            "(e.g., strongly acidic substances neutralizing alkaline compounds in gastric juice)."
        ),
        "clinical_management": "Contraindicated in same formulation; separate gastric phases."
    },
    "physical": {
        "term_urdu": "تناقض کیفی (طبیعی)",
        "term_english": "Physical Antagonism",
        "definition": (
            "Occurs when physical properties prevent action or absorption, such as an oily film blocking "
            "water-soluble drug contact, or a demulcent mucilage mechanically coating and entrapping active toxins."
        ),
        "clinical_management": "Utilized therapeutically in toxicology as demulcent antidotes."
    }
}

# =============================================================================
# 6. STANDARDIZED 74+ PHARMACOLOGICAL ACTION DICTIONARY (pp. 150-176)
# =============================================================================

KULLIYAT_PHARMACOLOGICAL_ACTIONS: List[Dict[str, Any]] = [
    {
        "term_id": "ACT-01",
        "term_urdu": "اکال",
        "term_english": "Corrosive / Caustic",
        "definition_urdu": "ایسی دوائیں جو بافتوں میں تیزی سے نفوذ کر کے انہیں تباہ کر دیتی ہیں۔",
        "definition_english": "An agent that causes corrosion and destruction of living tissue.",
        "examples": ["Tezab (Mineral Acids)", "Neela Thotha (Copper Sulphate)", "Chuna (Quicklime)"],
        "target_system": "Tissue / Dermatological",
        "mode": "Destructive / Surgical"
    },
    {
        "term_id": "ACT-02",
        "term_urdu": "جاذب",
        "term_english": "Siccative / Absorbent",
        "definition_urdu": "ایسی دوائیں جن میں رطوبت کو جذب کرنے کی خصوصی قوت ہوتی ہے۔",
        "definition_english": "An agent that absorbs moisture and fluid exudates from tissues.",
        "examples": ["Phaoa", "Ghareeqoon", "Jund Bedastar", "Sartan"],
        "target_system": "Tissue / Exudate Management",
        "mode": "Siccative"
    },
    {
        "term_id": "ACT-03",
        "term_urdu": "جالی",
        "term_english": "Detergent / Detersive",
        "definition_urdu": "ایسی دوائیں جو اعضاء کی سطح اور مسامات سے میل، رطوبات اور کثافتوں کو صاف کر دیں۔",
        "definition_english": "A cleansing agent that through surface activity exerts cleansing, oil-dissolving, and antibacterial effect.",
        "examples": ["Shura", "Shahd", "Sirka", "Namak", "Reetha", "Lehsan"],
        "target_system": "Integumentary / Mucosal",
        "mode": "Cleansing"
    },
    {
        "term_id": "ACT-04",
        "term_urdu": "حابس دم",
        "term_english": "Haemostatic / Styptic",
        "definition_urdu": "ایسی دوائیں جو اپنی قوت قابضہ کی وجہ سے عروق کو سکیڑ کر خون کے بہاؤ کو روکتی ہیں۔",
        "definition_english": "An astringent haemostatic agent used topically or systemically to arrest bleeding.",
        "examples": ["Mazoo", "Geru", "Dam-ul-Akhwain", "Shab-e-Yamani (Alum)"],
        "target_system": "Vascular / Hematological",
        "mode": "Vascular Constriction"
    },
    {
        "term_id": "ACT-05",
        "term_urdu": "حالق",
        "term_english": "Depilatory",
        "definition_urdu": "ایسی گرم اور تیز دوائیں جو بالوں کی جڑوں میں نفوذ کر کے بالوں کو گرا دیں۔",
        "definition_english": "An agent that causes falling out of hairs from follicles.",
        "examples": ["Noora (Lime Depilatory)", "Hartal (Arsenic trisulphide)"],
        "target_system": "Integumentary",
        "mode": "Hair Removal"
    },
    {
        "term_id": "ACT-06",
        "term_urdu": "حکاک",
        "term_english": "Pruritic / Irritant",
        "definition_urdu": "ایسی دوائیں جو تیزی اور حرارت کی وجہ سے جلد میں خارش اور سوزش پیدا کریں۔",
        "definition_english": "An agent that causes pruritus or itching and local sensory nerve irritation.",
        "examples": ["Bhilawa", "Rai", "Kunch Beej"],
        "target_system": "Integumentary / Sensory Nerve",
        "mode": "Irritant"
    },
    {
        "term_id": "ACT-07",
        "term_urdu": "خاتم",
        "term_english": "Cicatrizant",
        "definition_urdu": "ایسی دوائیں جو زخموں کی رطوبت خشک کر کے کھرنڈ بنا دیں اور اندمال زخم میں مدد دیں۔",
        "definition_english": "An agent causing or favouring cicatrization and scar formation in wound healing.",
        "examples": ["Anzaroot", "Sang-e-Jarahat", "Sadaf Sokhta", "Neela Thotha"],
        "target_system": "Wound Care / Regeneration",
        "mode": "Wound Healing"
    },
    {
        "term_id": "ACT-08",
        "term_urdu": "دابق",
        "term_english": "Emplastic / Adhesive",
        "definition_urdu": "ایسی دوائیں جو اپنی لزوجت اور چپکنے کی صفت کی وجہ سے جلد سے چپک جاتی ہیں۔",
        "definition_english": "Any material that adheres to surface tissues or causes adherence between surfaces.",
        "examples": ["Ral Safaid", "Samgh-e-Arabi", "Gond Kundur"],
        "target_system": "Topical Formulations",
        "mode": "Mechanical Adhesive"
    },
    {
        "term_id": "ACT-09",
        "term_urdu": "دافع تشنج",
        "term_english": "Antispasmodic / Anticonvulsive",
        "definition_urdu": "ایسی دوائیں جو اعصابی اور عضلاتی اینٹھن اور اینٹھن پیدا کرنے والے اسباب کو دور کریں۔",
        "definition_english": "An agent that quiets spasm or prevents seizures and muscular contractions.",
        "examples": ["Asrol", "Afeeyun", "Bhang", "Hing", "Dhatura", "Jund Bedastar"],
        "target_system": "Neuromuscular",
        "mode": "Antispasmodic"
    },
    {
        "term_id": "ACT-10",
        "term_urdu": "دافع عفونت",
        "term_english": "Antiseptic",
        "definition_urdu": "ایسی دوائیں جو سڑاند اور جراثیمی تعفن پیدا کرنے والے اسباب کو ختم کریں۔",
        "definition_english": "An agent that possesses the capability of destroying pathogenic microorganisms or inhibiting their growth.",
        "examples": ["Afsanteen", "Kabab Chini", "Sandal", "Neem", "Kafoor", "Darchini"],
        "target_system": "Microbiological / Anti-infective",
        "mode": "Antiseptic"
    },
    {
        "term_id": "ACT-11",
        "term_urdu": "دافع حمی",
        "term_english": "Antipyretic / Antifebrile",
        "definition_urdu": "ایسی دوائیں جو جسم کے غیر طبعی بڑھے ہوئے درجہ حرارت کو اعتدال پر لائیں۔",
        "definition_english": "An agent that reduces fever and brings abnormal body temperature toward normal.",
        "examples": ["Khas", "Karanjwa", "Afsanteen", "Chiraita", "Gilo"],
        "target_system": "Thermoregulatory / Systemic",
        "mode": "Antipyretic"
    },
    {
        "term_id": "ACT-12",
        "term_urdu": "رادع",
        "term_english": "Repellent",
        "definition_urdu": "ایسی دوائیں جو برودت اور قبض کی وجہ سے کسی عضو کی طرف گرنے والے فاسد مواد کو لوٹا دیں۔",
        "definition_english": "An agent that derives off or repels morbid fluids from an inflamed organ by astringency and cooling.",
        "examples": ["Sandal Surkh", "Geru", "Sang-e-Jarahat", "Gil-e-Armani"],
        "target_system": "Inflammatory / Vascular Flux",
        "mode": "Repellent"
    },
    {
        "term_id": "ACT-13",
        "term_urdu": "عاصر",
        "term_english": "Squeezer / Tissue Constrictor",
        "definition_urdu": "ایسی دوائیں جو اپنی قوت قابضہ سے عضو کو سکیڑ کر فاسد رطوبات نچوڑ دیں۔",
        "definition_english": "An agent that constricts tissues and empties morbid accumulated fluid from them.",
        "examples": ["Halela", "Aamla", "Behroza", "Tukhm-e-Jamun"],
        "target_system": "Cellular / Tissue Fluid",
        "mode": "Constriction"
    },
    {
        "term_id": "ACT-14",
        "term_urdu": "غسال",
        "term_english": "Irrigator / Lavage",
        "definition_urdu": "ایسی سیال دوائیں جو رطوبت اور قوت جلاء سے بافتوں کو دھو کر صاف کر دیں۔",
        "definition_english": "An agent that washes out and purges cavities or ulcer surfaces.",
        "examples": ["Shahd ka Paani", "Namak ka Paani", "Jau ka Paani"],
        "target_system": "Cavity / Wound",
        "mode": "Irrigation"
    },
    {
        "term_id": "ACT-15",
        "term_urdu": "قابض",
        "term_english": "Astringent",
        "definition_urdu": "ایسی دوائیں جو برودت اور یبوست کی وجہ سے اعضاء کے منافذ میں تنگی پیدا کر کے اخراج رطوبات کو روکیں۔",
        "definition_english": "An agent causing contraction of tissues, arresting secretions and checking discharge.",
        "examples": ["Dam-ul-Akhwain", "Hab-ul-Aas", "Babul", "Supari", "Katha"],
        "target_system": "Mucosal / Secretory",
        "mode": "Astringent"
    },
    {
        "term_id": "ACT-16",
        "term_urdu": "قابض امعاء",
        "term_english": "Intestinal Astringent",
        "definition_urdu": "ایسی دوائیں جو آنتوں کی حرکات کو سست کر کے یا رطوبات کو سکھا کر دستوں کو روکیں۔",
        "definition_english": "An agent that checks diarrhoea and intestinal discharge by constricting bowel mucosa.",
        "examples": ["Afeeyun", "Ajwain Khurasani", "Bel Giri"],
        "target_system": "Gastrointestinal",
        "mode": "Antidiarrhoeal"
    },
    {
        "term_id": "ACT-17",
        "term_urdu": "قاشر",
        "term_english": "Sloughing / Desquamative",
        "definition_urdu": "ایسی دوائیں جو مردہ بافتوں یا جلد کے چھلکوں کو کھرچ کر الگ کر دیں۔",
        "definition_english": "An agent that separates and sheds necrosed tissue from living biological structures.",
        "examples": ["Zarawand", "Qust", "Kunjad Siyah"],
        "target_system": "Dermatological / Wound",
        "mode": "Desquamation"
    },
    {
        "term_id": "ACT-18",
        "term_urdu": "قاتل و مخرج دیدان",
        "term_english": "Vermicide & Vermifuge / Anthelmintic",
        "definition_urdu": "ایسی دوائیں جو پیٹ کے کیڑوں کو ہلاک کریں یا انہیں جسم سے خارج کر دیں۔",
        "definition_english": "An agent that destroys (vermicide) or expels (vermifuge) intestinal worms.",
        "examples": ["Baobrang", "Kamila", "Palas Papra", "Qust"],
        "target_system": "Gastrointestinal / Parasitic",
        "mode": "Anthelmintic"
    },
    {
        "term_id": "ACT-19",
        "term_urdu": "قاطع باہ",
        "term_english": "Anaphrodisiac",
        "definition_urdu": "ایسی دوائیں جو جنسی قوت یا خواہش کو کم یا زائل کر دیں۔",
        "definition_english": "An agent that lessens or abolishes sexual desire and spermatogenesis.",
        "examples": ["Kafoor", "Afeeyun", "Kishneez Khushk", "Aab-e-Lemu"],
        "target_system": "Endocrine / Reproductive",
        "mode": "Suppressive"
    },
    {
        "term_id": "ACT-20",
        "term_urdu": "کاسر ریاح",
        "term_english": "Carminative",
        "definition_urdu": "ایسی دوائیں جو اپنی حرارت اور لطافت سے پیٹ کی گیس کو تحلیل یا خارج کر دیں۔",
        "definition_english": "An agent that prevents the formation or causes expulsion of flatus from the digestive tract.",
        "examples": ["Zira Safaid", "Badiyan", "Ajwain Desi", "Zanjabeel", "Sonth"],
        "target_system": "Gastrointestinal",
        "mode": "Carminative"
    },
    {
        "term_id": "ACT-21",
        "term_urdu": "کاوی",
        "term_english": "Escharotic / Caustic",
        "definition_urdu": "ایسی دوائیں جو شدید حرارت اور خشکی کی وجہ سے مسام کو جلا کر داغ ڈال دیں۔",
        "definition_english": "An agent that destroys living tissue and produces an eschar or slough.",
        "examples": ["Tezab", "Chuna", "Neela Thotha"],
        "target_system": "Tissue / Caustic",
        "mode": "Escharotic"
    },
    {
        "term_id": "ACT-22",
        "term_urdu": "لاذع",
        "term_english": "Irritant",
        "definition_urdu": "ایسی دوائیں جو اپنی حدت کی وجہ سے سطح جلد پر سوزش اور جلن پیدا کریں۔",
        "definition_english": "An agent that causes local inflammatory reaction, burning sensation, and erythema.",
        "examples": ["Rai", "Sirka", "Lehsan", "Piyaz"],
        "target_system": "Integumentary",
        "mode": "Irritant"
    },
    {
        "term_id": "ACT-23",
        "term_urdu": "مانع عرق",
        "term_english": "Anadiaphoretic",
        "definition_urdu": "ایسی دوائیں جو پسینے کی پیدائش یا اخراج کو کم کریں۔",
        "definition_english": "An agent that lessens sweat secretion by depressing sweat gland innervation or closing pores.",
        "examples": ["Dhatura", "Ajwain Khurasani", "Luffah"],
        "target_system": "Integumentary / Autonomic",
        "mode": "Antisecretory"
    },
    {
        "term_id": "ACT-24",
        "term_urdu": "مانع نوبت",
        "term_english": "Antiperiodic",
        "definition_urdu": "ایسی دوائیں جو بخار کی باری کو روکیں اور دوروں کے تواتر کو توڑیں۔",
        "definition_english": "An agent that prevents regular recurrence of a disease symptom or paroxysm (e.g. malaria).",
        "examples": ["Karanjwa", "Chiraita", "Afsanteen", "Karanj"],
        "target_system": "Hematological / Infectious",
        "mode": "Antiperiodic"
    },
    {
        "term_id": "ACT-25",
        "term_urdu": "مبرّد",
        "term_english": "Refrigerant / Frigorific",
        "definition_urdu": "ایسی دوائیں جو جسم میں ٹھنڈک پیدا کریں اور گرمی کی شدت کو گھٹائیں۔",
        "definition_english": "An agent that decreases body heat production and imparts a sensation of coolness.",
        "examples": ["Kafoor", "Sandal", "Khurfa", "Kaddu"],
        "target_system": "Thermoregulatory",
        "mode": "Cooling"
    },
    {
        "term_id": "ACT-26",
        "term_urdu": "منفط",
        "term_english": "Vesicant",
        "definition_urdu": "ایسی دوائیں جو جلد پر چھالے یا آبلے پیدا کر دیں۔",
        "definition_english": "An agent that produces blisters (vesicles) on the cutaneous surface.",
        "examples": ["Rai", "Roghan Jamalgota", "Bhilawan"],
        "target_system": "Integumentary",
        "mode": "Blistering"
    },
    {
        "term_id": "ACT-27",
        "term_urdu": "مجفف",
        "term_english": "Desiccative",
        "definition_urdu": "ایسی دوائیں جو اپنی یبوست سے رطوبتوں کو کم کر کے خشکی پیدا کریں۔",
        "definition_english": "An agent that removes moisture and dries up exudative secretions.",
        "examples": ["Phitkari", "Murdar Sang", "Sang-e-Jarahat"],
        "target_system": "Mucosal / Cutaneous",
        "mode": "Drying"
    },
    {
        "term_id": "ACT-28",
        "term_urdu": "مجشئ",
        "term_english": "Flatulent",
        "definition_urdu": "ایسی دوائیں یا غذائیں جو عمل ہضم میں بگاڑ سے معدہ اور آنتوں میں ریاح پیدا کریں۔",
        "definition_english": "An agent that produces excessive flatus and gas in the gastrointestinal tract.",
        "examples": ["Arvi", "Aloo"],
        "target_system": "Gastrointestinal",
        "mode": "Gas-producing"
    },
    {
        "term_id": "ACT-29",
        "term_urdu": "مہیج / مقوی باہ",
        "term_english": "Aphrodisiac",
        "definition_urdu": "ایسی دوائیں جو جنسی خواہش اور قوت کو بڑھائیں۔",
        "definition_english": "An agent that arouses or increases sexual desire, erectile power, and spermatogenesis.",
        "examples": ["Zafaran", "Amber", "Mushk", "Malkangni", "Kunch Beej", "Salab Misri"],
        "target_system": "Endocrine / Reproductive",
        "mode": "Aphrodisiac"
    },
    {
        "term_id": "ACT-30",
        "term_urdu": "مجمد",
        "term_english": "Coagulant",
        "definition_urdu": "ایسی دوائیں جو برودت اور یبوست سے رطوبتوں کو جما دیں۔",
        "definition_english": "An agent that causes coagulation and thickening of biological fluids.",
        "examples": ["Phitkari", "Geru", "Sang-e-Jarahat", "Kahruba"],
        "target_system": "Hematological",
        "mode": "Coagulant"
    },
    {
        "term_id": "ACT-31",
        "term_urdu": "محرک اعصاب",
        "term_english": "Nerve Stimulant",
        "definition_urdu": "ایسی دوائیں جو اعصاب میں تحریک پیدا کر کے ان کے افعال کو تیز کریں۔",
        "definition_english": "An agent that increases functional activity and conduction velocity of peripheral and central nerves.",
        "examples": ["Kuchla", "Bhang", "Sunbul-ut-Teeb"],
        "target_system": "Nervous System",
        "mode": "Stimulant"
    },
    {
        "term_id": "ACT-32",
        "term_urdu": "محرک دماغ",
        "term_english": "Brain Stimulant / Nootropic",
        "definition_urdu": "ایسی دوائیں جو دماغ کے افعال میں تحریک پیدا کر کے بیداری اور چستی لائیں۔",
        "definition_english": "An agent that increases cerebral activity, cognitive alertness, and mental alertness.",
        "examples": ["Jund Bedastar", "Amber", "Chai", "Qahwa"],
        "target_system": "Central Nervous System",
        "mode": "Stimulant"
    },
    {
        "term_id": "ACT-33",
        "term_urdu": "محلل",
        "term_english": "Resolvent / Anti-inflammatory",
        "definition_urdu": "ایسی دوائیں جو حرارت اور تحلیلی قوت کی بنا پر ورم کے مادے کو پگھلا کر خارج کر دیں۔",
        "definition_english": "An agent that arrests inflammatory processes and resolves pathological swellings (Awraam).",
        "examples": ["Amba Haldi", "Darhald", "Asaroon", "Alsi", "Mako", "Zarawand"],
        "target_system": "Immune / Connective Tissue",
        "mode": "Anti-inflammatory"
    },
    {
        "term_id": "ACT-34",
        "term_urdu": "محمر",
        "term_english": "Rubefacient",
        "definition_urdu": "ایسی دوائیں جو جلدی عروق کو پھیلا کر مقامی دوران خون کو بڑھائیں اور سرخی پیدا کریں۔",
        "definition_english": "A counter-irritant that produces cutaneous hyperemia and erythema when applied to skin.",
        "examples": ["Rai", "Lehsan", "Roghan Jamalgota", "Kabab Chini"],
        "target_system": "Integumentary / Vascular",
        "mode": "Rubefacient"
    },
    {
        "term_id": "ACT-35",
        "term_urdu": "مخدر",
        "term_english": "Anaesthetic / Narcotic",
        "definition_urdu": "ایسی دوائیں جو اعصابی حس کو وقتی طور پر ختم کر کے درد اور تکلیف کا احساس زائل کریں۔",
        "definition_english": "An agent that produces reversible loss of pain sensation and consciousness or local anaesthesia.",
        "examples": ["Afeeyun", "Ajwain Khurasani", "Dhatura", "Kahu", "Khashkhash", "Shukran"],
        "target_system": "Central & Peripheral Nervous System",
        "mode": "Sensory Blockade"
    },
    {
        "term_id": "ACT-36",
        "term_urdu": "منوم",
        "term_english": "Hypnotic / Soporific",
        "definition_urdu": "ایسی دوائیں جو دماغ میں ضعف اور سکون پیدا کر کے نیند لائیں۔",
        "definition_english": "An agent that induces and promotes sleep resembling physiological natural sleep.",
        "examples": ["Afeeyun", "Khashkhash", "Kahu"],
        "target_system": "Central Nervous System",
        "mode": "Hypnotic"
    },
    {
        "term_id": "ACT-37",
        "term_urdu": "مخرج جنین و مشیمہ",
        "term_english": "Abortifacient / Ecbolic",
        "definition_urdu": "ایسی دوائیں جو رحم کے عضلات میں شدید اینٹھن پیدا کر کے جنین یا مشیمہ کو باہر خارج کر دیں۔",
        "definition_english": "An agent that stimulates uterine contraction and expels the fetus or retained placenta.",
        "examples": ["Abhal", "Post-e-Amaltas", "Barg-e-Baans"],
        "target_system": "Uterine / Obstetric",
        "mode": "Uterine Evacuation"
    },
    {
        "term_id": "ACT-38",
        "term_urdu": "مخشن",
        "term_english": "Roughening Agent",
        "definition_urdu": "ایسی دوائیں جو اپنی خشکی اور حدت سے جلد کی سطح پر کھردرابن پیدا کریں۔",
        "definition_english": "An agent that roughens and hardens the cutaneous surface through dehydration.",
        "examples": ["Rai", "Bhilawa", "Filfil Siyah"],
        "target_system": "Integumentary",
        "mode": "Roughening"
    },
    {
        "term_id": "ACT-39",
        "term_urdu": "مدر بول",
        "term_english": "Diuretic",
        "definition_urdu": "ایسی دوائیں جو گردوں کی فعالیت کو تیز کر کے پیشاب کے اخراج کو بڑھائیں۔",
        "definition_english": "An agent that causes a net loss of sodium and water in urine, thereby increasing urinary volume.",
        "examples": ["Khar-e-Khasak (Gokhru)", "Shura Qalmi", "Jawakhar", "Tukhm-e-Khiyar"],
        "target_system": "Renal / Urinary",
        "mode": "Diuretic"
    },
    {
        "term_id": "ACT-40",
        "term_urdu": "مدر حیض",
        "term_english": "Emmenagogue",
        "definition_urdu": "ایسی دوائیں جو رحم میں خون کی آمد کو بڑھا کر یا خون کو پگھلا کر بند حیض کو جاری کریں۔",
        "definition_english": "An agent that stimulates or increases menstrual flow and relieves amenorrhoea.",
        "examples": ["Abhal", "Post-e-Amaltas", "Khar-e-Khasak", "Mushktaramshi"],
        "target_system": "Reproductive / Gynecological",
        "mode": "Emmenagogue"
    },
    {
        "term_id": "ACT-41",
        "term_urdu": "مدر لعاب دہن",
        "term_english": "Sialogogue",
        "definition_urdu": "ایسی دوائیں جو غدد لعابیہ میں تحریک پیدا کر کے تھوک کے اخراج کو بڑھائیں۔",
        "definition_english": "An agent that stimulates salivary gland secretion and flow of saliva.",
        "examples": ["Aaqarqarha", "Filfil Siyah", "Rai", "Tambaku"],
        "target_system": "Salivary / Oral",
        "mode": "Sialogogue"
    },
    {
        "term_id": "ACT-42",
        "term_urdu": "مدمل",
        "term_english": "Cicatrizant / Vulnerary",
        "definition_urdu": "ایسی دوائیں جو زخموں کی رطوبت خشک کر کے نئے خلیات بننے اور زخم بھرنے میں مدد دیں۔",
        "definition_english": "An agent that promotes wound granulation, re-epithelialization, and scar maturation.",
        "examples": ["Sang-e-Jarahat", "Dam-ul-Akhwain", "Gil-e-Multani", "Anzaroot"],
        "target_system": "Wound Care",
        "mode": "Regenerative"
    },
    {
        "term_id": "ACT-43",
        "term_urdu": "مرخی",
        "term_english": "Relaxant / Emollient",
        "definition_urdu": "ایسی دوائیں جو حرارت اور رطوبت کی وجہ سے اعضاء یا جلد کو ڈھیلا اور نرم کریں۔",
        "definition_english": "An agent that relaxes muscular spasm and softens tissue surfaces.",
        "examples": ["Alsi", "Roghniyat", "Mom (Beeswax)"],
        "target_system": "Muscular / Cutaneous",
        "mode": "Relaxant"
    },
    {
        "term_id": "ACT-44",
        "term_urdu": "مسخن",
        "term_english": "Calorific / Thermogenic",
        "definition_urdu": "ایسی دوائیں جو اندرونی یا بیرونی استعمال سے جسمانی اعضاء میں طبعی حرارت پیدا کریں۔",
        "definition_english": "An agent that increases generation and retention of heat in the organism.",
        "examples": ["Mushk", "Amber", "Khulanjaan", "Aaqarqarha", "Zafaran"],
        "target_system": "Metabolic / Vital Heat",
        "mode": "Thermogenic"
    },
    {
        "term_id": "ACT-45",
        "term_urdu": "مسکن",
        "term_english": "Sedative / Calming",
        "definition_urdu": "ایسی دوائیں جو اعصابی ہیجان اور بے چینی کو دور کر کے سکون بخشیں۔",
        "definition_english": "An agent that allays nervous excitement, irritability, and functional hyperactivity.",
        "examples": ["Gaozaban", "Banafsha", "Ustukhuddus"],
        "target_system": "Nervous System",
        "mode": "Sedative"
    },
    {
        "term_id": "ACT-46",
        "term_urdu": "مسکن الم",
        "term_english": "Analgesic",
        "definition_urdu": "ایسی دوائیں جو اعصاب پر اثر انداز ہو کر درد کے احساس کو دور کریں۔",
        "definition_english": "An agent that selectively relieves pain without causing loss of consciousness.",
        "examples": ["Afeeyun", "Ajwain Khurasani", "Bhang"],
        "target_system": "Pain Pathways",
        "mode": "Analgesic"
    },
    {
        "term_id": "ACT-47",
        "term_urdu": "مسکن قلب",
        "term_english": "Cardiac Sedative",
        "definition_urdu": "ایسی دوائیں جو دل کے بڑھے ہوئے افعال، اضطراب اور خفقان کو پرسکون کریں۔",
        "definition_english": "An agent that decreases excessive cardiac rate and calms cardiac palpitations (Khafqan).",
        "examples": ["Bhring", "Afeeyun", "Shukran"],
        "target_system": "Cardiovascular",
        "mode": "Cardiac Sedative"
    },
    {
        "term_id": "ACT-48",
        "term_urdu": "مسکن تنفس",
        "term_english": "Respiratory Sedative",
        "definition_urdu": "ایسی دوائیں جو تنفسی آلات کی بے چینی اور شدید کھانسی کو پرسکون کریں۔",
        "definition_english": "An agent that reduces cough reflex irritability and calms respiratory tract spasm.",
        "examples": ["Afeeyun", "Khashkhash", "Dhatura"],
        "target_system": "Respiratory",
        "mode": "Antitussive / Sedative"
    },
    {
        "term_id": "ACT-49",
        "term_urdu": "مسکن معدہ",
        "term_english": "Gastric Sedative",
        "definition_urdu": "ایسی دوائیں جو معدے کے اضطراب، متلی اور بے چینی کو سکون دیں۔",
        "definition_english": "An agent that allays gastric hypermotility and relieves vomiting reflexes.",
        "examples": ["Ajwain Khurasani", "Dhatura", "Luffah"],
        "target_system": "Gastrointestinal",
        "mode": "Antiemetic / Sedative"
    },
    {
        "term_id": "ACT-50",
        "term_urdu": "مسکن حرارت",
        "term_english": "Febrifuge",
        "definition_urdu": "ایسی دوائیں جو جسم کی غیر طبعی حرارت کو کم کر کے ٹھنڈک پہنچائیں۔",
        "definition_english": "An agent that reduces feverish states and abates internal burning.",
        "examples": ["Aab-e-Barg-e-Kasni", "Aab-e-Anar Tursh", "Sheera-e-Tukhm-e-Kahu"],
        "target_system": "Thermoregulatory",
        "mode": "Cooling / Febrifuge"
    },
    {
        "term_id": "ACT-51",
        "term_urdu": "مسیل / مسہل",
        "term_english": "Purgative / Cathartic",
        "definition_urdu": "ایسی دوائیں جو آنتوں کی قوت دافعہ کو بڑھا کر اور رطوبات کو کھینچ کر دست لائیں۔",
        "definition_english": "An agent that produces copious evacuation of watery or fecal matter from the intestines.",
        "examples": ["Turbud", "Saqmonia", "Jamalgota", "Jalapa"],
        "target_system": "Gastrointestinal / Evacuation",
        "mode": "Purgative"
    },
    {
        "term_id": "ACT-52",
        "term_urdu": "مسہل صفراء",
        "term_english": "Cholagogue Purgative",
        "definition_urdu": "ایسی دوائیں جو خاص طور پر صفراء کو آنتوں کی راہ سے خارج کریں۔",
        "definition_english": "An agent that specifically purges yellow bile (Khilt-e-Safra) from the liver and gallbladder.",
        "examples": ["Saqmonia", "Usara-e-Rewand", "Sibr Zard"],
        "target_system": "Hepatobiliary / Intestinal",
        "mode": "Cholagogue"
    },
    {
        "term_id": "ACT-53",
        "term_urdu": "مسہل بلغم",
        "term_english": "Phlegmagogue Purgative",
        "definition_urdu": "ایسی دوائیں جو خاص طور پر بلغم کے فاسد مادے کو آنتوں کے ذریعے نکالیں۔",
        "definition_english": "An agent that specifically purges phlegmatic humour (Khilt-e-Balgham) through bowel evacuation.",
        "examples": ["Turbud", "Jalapa", "Shahm-e-Hanzal", "Ghariqoon"],
        "target_system": "Gastrointestinal",
        "mode": "Phlegmagogue"
    },
    {
        "term_id": "ACT-54",
        "term_urdu": "مسہل سوداء",
        "term_english": "Melanagogue Purgative",
        "definition_urdu": "ایسی دوائیں جو خاص طور پر سوداوی فاسد مادے کو خارج کریں۔",
        "definition_english": "An agent that specifically purges black bile (Khilt-e-Sawda) from the system.",
        "examples": ["Aftimoon", "Kharbaq Siyah", "Turbud"],
        "target_system": "Gastrointestinal / Systemic",
        "mode": "Melanagogue"
    },
    {
        "term_id": "ACT-55",
        "term_urdu": "معدل",
        "term_english": "Humoral Moderator",
        "definition_urdu": "ایسی دوائیں جو اخلاط و رطوبات کی حدت و برودت کو طبعی اعتدال پر لائیں۔",
        "definition_english": "An agent that normalizes morbid humoral qualities and restores temperamental balance.",
        "examples": ["Banafsha", "Ushba", "Sandal", "Unnab"],
        "target_system": "Humoral / Systemic",
        "mode": "Harmonizing"
    },
    {
        "term_id": "ACT-56",
        "term_urdu": "منضج",
        "term_english": "Concoctive / Maturing Agent",
        "definition_urdu": "ایسی دوائیں جو خام اور غیر طبعی اخلاط کو پکا کر اخراج کے قابل بنائیں۔",
        "definition_english": "An agent that cooks, ripens, and prepares raw, crude humours for safe evacuation (Tanqiya).",
        "examples": ["Barg-e-Kasni", "Badiyan", "Asl-us-Soos", "Gaozaban", "Aftimoon"],
        "target_system": "Humoral Processing",
        "mode": "Concoctive"
    },
    {
        "term_id": "ACT-57",
        "term_urdu": "مقوی",
        "term_english": "Tonic",
        "definition_urdu": "ایسی دوائیں جو کمزور عضو کی قوت کو بحال کر کے اس کے افعال کو اعتدال پر لائیں۔",
        "definition_english": "An agent that restores enfeebled organ function and promotes tone, vigor, and wellbeing.",
        "examples": ["Zafaran", "Amber", "Marwareed", "Darchini"],
        "target_system": "Systemic / Vital Organs",
        "mode": "Tonic"
    },
    {
        "term_id": "ACT-58",
        "term_urdu": "مقوی قلب",
        "term_english": "Cardiotonic",
        "definition_urdu": "ایسی دوائیں جو عضلات قلب کو تقویت دے کر اس کے انقباض و انبساط کو منظم کریں۔",
        "definition_english": "An agent that tones cardiac muscle and strengthens contractility and rhythm.",
        "examples": ["Khamira Abresham", "Marwareed", "Zafaran", "Bahar-e-Naranj"],
        "target_system": "Cardiovascular",
        "mode": "Cardiotonic"
    },
    {
        "term_id": "ACT-59",
        "term_urdu": "مقوی اعصاب",
        "term_english": "Nervine Tonic",
        "definition_urdu": "ایسی دوائیں جو اعصابی نظام کو قوت بخشیں اور اعصابی تھکن دور کریں۔",
        "definition_english": "An agent that strengthens nerves, improves conduction, and overcomes chronic nervous exhaustion.",
        "examples": ["Kuchla Mudabbar", "Jund Bedastar", "Bozidan"],
        "target_system": "Nervous System",
        "mode": "Nervine Tonic"
    },
    {
        "term_id": "ACT-60",
        "term_urdu": "مقوی جگر",
        "term_english": "Hepatotonic / Hepatoprotective",
        "definition_urdu": "ایسی دوائیں جو جگر کے استحالہ اور صفراء کی پیدائش کو درست کریں۔",
        "definition_english": "An agent that supports liver function, enhances hepatic metabolism, and protects hepatocytes.",
        "examples": ["Kasni", "Mako", "Afsanteen", "Rewand Chini"],
        "target_system": "Hepatobiliary",
        "mode": "Hepatoprotective"
    },
    {
        "term_id": "ACT-61",
        "term_urdu": "مقوی گردہ",
        "term_english": "Nephrotonic",
        "definition_urdu": "ایسی دوائیں جو گردوں کی چھاننے کی قوت کو تقویت پہنچائیں۔",
        "definition_english": "An agent that restores glomerular filtration efficacy and tones renal parenchyma.",
        "examples": ["Mastagi", "Khar-e-Khasak", "Kaknaj"],
        "target_system": "Renal",
        "mode": "Nephrotonic"
    },
    {
        "term_id": "ACT-62",
        "term_urdu": "مصفی دم",
        "term_english": "Blood Purifier",
        "definition_urdu": "ایسی دوائیں جو خون میں سے فاسد مادوں اور عفونت کو اخراجی راستوں کے ذریعے صاف کریں۔",
        "definition_english": "An agent that removes metabolic waste and toxic endotoxins from circulation.",
        "examples": ["Chiraita", "Mundi", "Unnab", "Shahtara", "Neem", "Ushba"],
        "target_system": "Hematological",
        "mode": "Blood Purifier"
    },
    {
        "term_id": "ACT-63",
        "term_urdu": "معرّق",
        "term_english": "Diaphoretic / Sudorific",
        "definition_urdu": "ایسی دوائیں جو غدد عرقیہ میں تحریک پیدا کر کے پسینہ لائیں۔",
        "definition_english": "An agent that stimulates sweat glands and promotes cutaneous perspiration.",
        "examples": ["Kasni", "Chai", "Lehsan", "Ushba"],
        "target_system": "Integumentary",
        "mode": "Diaphoretic"
    },
    {
        "term_id": "ACT-64",
        "term_urdu": "معطس",
        "term_english": "Errhine / Ptarmic",
        "definition_urdu": "ایسی دوائیں جو ناک کی مخاطی جھلی میں تحریک پیدا کر کے چھینک لائیں۔",
        "definition_english": "An agent that induces sneezing and nasal secretion clearance.",
        "examples": ["Kundush", "Tambaku", "Naushadar"],
        "target_system": "Nasal / Respiratory",
        "mode": "Errhine"
    },
    {
        "term_id": "ACT-65",
        "term_urdu": "مغذی",
        "term_english": "Nutrient / Nutritive",
        "definition_urdu": "ایسی دوائیں جن میں غذائی مادے کثیر ہوں اور جو بدن کی بافتوں کو غذا پہنچائیں۔",
        "definition_english": "An agent that supplies essential nutritional substrate for tissue repair and vitality.",
        "examples": ["Maghz Badam", "Roghan Zaitoon", "Injeer", "Baiza Murgh"],
        "target_system": "Metabolic",
        "mode": "Nutritive"
    },
    {
        "term_id": "ACT-66",
        "term_urdu": "مغلظ منی",
        "term_english": "Semen Concentrative / Inspissant",
        "definition_urdu": "ایسی دوائیں جو قوت قابضہ سے منی کے قوام کو گاڑھا کریں۔",
        "definition_english": "An agent that increases semen viscosity and corrects seminal thinning.",
        "examples": ["Salab Misri", "Satawar", "Musli Safaid", "Samgh-e-Dhak"],
        "target_system": "Reproductive",
        "mode": "Inspissant"
    },
    {
        "term_id": "ACT-67",
        "term_urdu": "مفتت حصاة",
        "term_english": "Lithotriptic",
        "definition_urdu": "ایسی دوائیں جو گردے اور مثانے کی پتھریوں کو ریزہ ریزہ کر کے خارج کریں۔",
        "definition_english": "An agent that effects the dissolution or fragmentation of urinary and renal calculi.",
        "examples": ["Sang-e-Sar-e-Mahi", "Hab-ul-Qillat", "Hajar-ul-Yahood", "Kulthi"],
        "target_system": "Urinary / Calculi",
        "mode": "Lithotriptic"
    },
    {
        "term_id": "ACT-68",
        "term_urdu": "مفتح",
        "term_english": "Deobstruent",
        "definition_urdu": "ایسی دوائیں جو اپنی حرارت، لطافت اور تحلیل کی قوت سے رگوں اور اعضاء کے سدوں کو کھولیں۔",
        "definition_english": "An agent that removes obstructions and clears pathways in blood vessels, bile ducts, and viscera.",
        "examples": ["Afsanteen", "Kabab Chini", "Badiyan", "Aniseed"],
        "target_system": "Vascular / Visceral Ducts",
        "mode": "Deobstruent"
    },
    {
        "term_id": "ACT-69",
        "term_urdu": "ملین",
        "term_english": "Laxative / Aperient",
        "definition_urdu": "ایسی دوائیں جو آنتوں کی رطوبت میں اضافہ کر کے اجابت کو نرم کریں۔",
        "definition_english": "A mild cathartic that promotes bowel evacuation without causing griping pain or violent purgation.",
        "examples": ["Taranjabeen", "Maveez Munaqqa", "Gulqand", "Aspaghol"],
        "target_system": "Gastrointestinal",
        "mode": "Laxative"
    },
    {
        "term_id": "ACT-70",
        "term_urdu": "ممسک منی",
        "term_english": "Semen Retentive",
        "definition_urdu": "ایسی دوائیں جو قوت مخدرہ یا قابضہ سے سرعت انزال کو روکیں۔",
        "definition_english": "An agent that prolongs coital duration and prevents premature ejaculation.",
        "examples": ["Dhatura", "Bhang", "Afeeyun", "Ajwain Khurasani"],
        "target_system": "Reproductive",
        "mode": "Retentive"
    },
    {
        "term_id": "ACT-71",
        "term_urdu": "ملطف",
        "term_english": "Attenuant / Demulcent",
        "definition_urdu": "ایسی دوائیں جو غلیظ خلط کو چھوٹے چھوٹے اجزاء میں تقسیم کر کے رقیق اور نرم بنا دیں۔",
        "definition_english": "An agent dividing viscous or dense matter into smaller, thinner particles for safe dispersion.",
        "examples": ["Baboona", "Khatmi", "Khabazi", "Chob Chini"],
        "target_system": "Humoral",
        "mode": "Attenuant"
    },
    {
        "term_id": "ACT-72",
        "term_urdu": "منفث بلغم",
        "term_english": "Mucolytic / Expectorant",
        "definition_urdu": "ایسی دوائیں جو پھیپھڑوں میں جمے ہوئے بلغم کو پتلا کر کے کھانسی کے ذریعے باہر نکالیں۔",
        "definition_english": "An agent that liquefies bronchial secretions and facilitates their expectoration.",
        "examples": ["Asl-us-Soos (Mulethi)", "Naushadar", "Piyaz Dashti", "Sapistan"],
        "target_system": "Respiratory",
        "mode": "Mucolytic"
    },
    {
        "term_id": "ACT-73",
        "term_urdu": "ہاضم",
        "term_english": "Digestive / Digestant",
        "definition_urdu": "ایسی دوائیں جو معدے کے ہاضم رسوں کے اخراج کو بڑھا کر غذا کو جلد ہضم کرائیں۔",
        "definition_english": "An agent that promotes digestion by stimulating the secretion of digestive enzymes and gastric juices.",
        "examples": ["Papita", "Namak Siyah", "Zanjabeel", "Ajwain Desi"],
        "target_system": "Gastrointestinal",
        "mode": "Digestive"
    },
    {
        "term_id": "ACT-74",
        "term_urdu": "تریاق",
        "term_english": "Antidote",
        "definition_urdu": "ایسی مخصوص دوائیں جو زہروں کے مضر اثرات کو اپنے افعال یا کیمیائی ردعمل سے باطل کر دیں۔",
        "definition_english": "An agent that counteracts the effects of a poison physically, chemically, or pharmacologically.",
        "examples": ["Tiryaq-e-Farooq", "Hab-e-Jadwar", "Zahar Mohra"],
        "target_system": "Toxicology / Systemic",
        "mode": "Antidote"
    }
]

# Quick index for lookup
_ACTIONS_BY_TERM: Dict[str, Dict[str, Any]] = {}
for act in KULLIYAT_PHARMACOLOGICAL_ACTIONS:
    _ACTIONS_BY_TERM[act["term_id"].upper()] = act
    _ACTIONS_BY_TERM[act["term_urdu"]] = act
    _ACTIONS_BY_TERM[act["term_english"].upper()] = act


# =============================================================================
# 7. PUBLIC ENGINE API FUNCTIONS
# =============================================================================

def get_kulliyat_metadata() -> Dict[str, Any]:
    """Returns canonical bibliographic metadata for Ishrah al-Adwiyah."""
    return ISHRAH_AL_ADWIYAH_METADATA

def get_all_pharmacological_actions() -> List[Dict[str, Any]]:
    """Returns the complete list of 74 standardized Unani pharmacological actions."""
    return KULLIYAT_PHARMACOLOGICAL_ACTIONS

def get_action_by_id_or_name(query: str) -> Optional[Dict[str, Any]]:
    """Looks up a specific pharmacological action by term ID, Urdu name, or English name."""
    q = query.strip().upper()
    if q in _ACTIONS_BY_TERM:
        return _ACTIONS_BY_TERM[q]
    for act in KULLIYAT_PHARMACOLOGICAL_ACTIONS:
        if q in act["term_english"].upper() or query.strip() in act["term_urdu"]:
            return act
    return None

def search_actions(query: str) -> List[Dict[str, Any]]:
    """Searches actions across Urdu name, English name, definition, or examples."""
    q = query.strip().lower()
    if not q:
        return KULLIYAT_PHARMACOLOGICAL_ACTIONS
    results = []
    for act in KULLIYAT_PHARMACOLOGICAL_ACTIONS:
        text = f"{act['term_id']} {act['term_urdu']} {act['term_english']} {act['definition_urdu']} {act['definition_english']} {' '.join(act['examples'])} {act['target_system']}".lower()
        if q in text:
            results.append(act)
    return results

def get_taste_pharmacodynamics(taste_id: Optional[str] = None) -> Any:
    """Returns pharmacodynamics for a specific taste (Za'iqah) or all 9 tastes."""
    if taste_id:
        return TASTE_PHARMACODYNAMICS.get(taste_id.lower().strip())
    return TASTE_PHARMACODYNAMICS

def get_temperament_degree(degree: int) -> Optional[Dict[str, Any]]:
    """Returns clinical definitions and poison thresholds for degrees 1 to 4."""
    key = f"darjah_{degree}"
    return TEMPERAMENT_DEGREES_REGISTRY.get(key)

def get_all_compounding_rules() -> List[Dict[str, Any]]:
    """Returns the 8 statutory rules of compounding (Qawanin-e-Tarkeeb)."""
    return COMPOUNDING_RULES

def get_antagonism_mechanisms() -> Dict[str, Dict[str, Any]]:
    """Returns the 3 classes of drug antagonism."""
    return ANTAGONISM_TYPES
