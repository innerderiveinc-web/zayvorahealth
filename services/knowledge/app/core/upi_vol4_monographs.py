"""
ZAYVORA Health OS™ — Statutory Unani Pharmacopoeia of India (UPI) Part-II, Vol-IV
Official Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H), Ministry of AYUSH.

Includes:
1. 50 Standard Compound Formulations (Murakkabat) with exact compositions, TLC Rf values,
   physico-chemical parameters, dosage, and classical indications.
2. Appendix 6: Statutory Tadbir-e-Adviyah (Detoxification) SOPs for toxic single drugs.
3. Appendix 7: Official Metric Equivalents of Classical Weights & Measures.
4. Canonical Heritage Editions Registry (Ibn Sina Canon Book 4, Akhlaq-e-Jalali, Shifa' al-Abdan).
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

# ============================================================================
# APPENDIX 7: OFFICIAL METRIC EQUIVALENTS OF CLASSICAL WEIGHTS & MEASURES
# (Adopted by the Unani Pharmacopoeia Committee, Ministry of AYUSH)
# ============================================================================
CLASSICAL_WEIGHTS_METRIC_MAP: Dict[str, Dict[str, Any]] = {
    "chawal": {"name": "Chawal", "urdu_name": "چاول", "metric_mg": 15.0, "metric_g": 0.015, "category": "micro"},
    "ratti": {"name": "Ratti", "urdu_name": "رتی", "metric_mg": 125.0, "metric_g": 0.125, "category": "micro"},
    "surkh": {"name": "Surkh", "urdu_name": "سرخ", "metric_mg": 125.0, "metric_g": 0.125, "category": "micro"},
    "qeerat": {"name": "Qeerat", "urdu_name": "قیراط", "metric_mg": 250.0, "metric_g": 0.25, "category": "minor"},
    "dang": {"name": "Dang", "urdu_name": "دانگ", "metric_mg": 500.0, "metric_g": 0.5, "category": "minor"},
    "masha": {"name": "Masha", "urdu_name": "ماشہ", "metric_mg": 1000.0, "metric_g": 1.0, "category": "standard"},
    "dirham": {"name": "Dirham", "urdu_name": "درہم", "metric_mg": 3500.0, "metric_g": 3.5, "category": "standard"},
    "misqal": {"name": "Misqal", "urdu_name": "مثقال", "metric_mg": 4500.0, "metric_g": 4.5, "category": "standard"},
    "tola": {"name": "Tola", "urdu_name": "تولہ", "metric_mg": 12000.0, "metric_g": 12.0, "category": "standard"},
    "dam": {"name": "Dam", "urdu_name": "دام", "metric_mg": 21000.0, "metric_g": 21.0, "category": "macro"},
    "oqia": {"name": "Oqia", "urdu_name": "اوقیہ", "metric_mg": 32000.0, "metric_g": 32.0, "category": "macro"},
    "chhatak": {"name": "Chhatak", "urdu_name": "چھٹانک", "metric_mg": 60000.0, "metric_g": 60.0, "category": "macro"},
    "pao": {"name": "Pao", "urdu_name": "پاؤ", "metric_mg": 240000.0, "metric_g": 240.0, "category": "bulk"},
    "ratal_tibbi": {"name": "Ratal Tibbi", "urdu_name": "رطل طبی", "metric_mg": 420000.0, "metric_g": 420.0, "category": "bulk"},
    "ser": {"name": "Ser", "urdu_name": "سیر", "metric_mg": 960000.0, "metric_g": 960.0, "category": "bulk"},
    "astar": {"name": "Astar", "urdu_name": "استار", "metric_mg": 1000000.0, "metric_g": 1000.0, "category": "bulk"},
    "man_tabrizi": {"name": "Man Tabrizi", "urdu_name": "من تبریزی", "metric_mg": 2900000.0, "metric_g": 2900.0, "category": "bulk"}
}

def convert_classical_weight(quantity: float, unit: str) -> Dict[str, Any]:
    """Converts a classical Unani posology weight into exact metric grams and milligrams."""
    key = unit.strip().lower().replace(" ", "_").replace("-", "_")
    info = CLASSICAL_WEIGHTS_METRIC_MAP.get(key)
    if not info:
        # Fallback to direct metric
        return {"quantity": quantity, "unit": unit, "grams": quantity, "milligrams": quantity * 1000.0, "is_classical": False}
    return {
        "classical_quantity": quantity,
        "classical_unit": info["name"],
        "urdu_name": info["urdu_name"],
        "grams": round(quantity * info["metric_g"], 4),
        "milligrams": round(quantity * info["metric_mg"], 2),
        "is_classical": True,
        "statutory_source": "Unani Pharmacopoeia of India Part-II, Appendix-7"
    }

# ============================================================================
# APPENDIX 6: STATUTORY TADBIR-E-ADVIYAH (DETOXIFICATION) PROTOCOLS
# ============================================================================
TADBIR_E_ADVIYAH_SOP: Dict[str, Dict[str, Any]] = {
    "azaraqi": {
        "canonical_name": "Azaraqi (Kuchla / Nux Vomica)",
        "botanical_name": "Strychnos nux-vomica L.",
        "appendix_ref": "Appendix 6.1.6 (vi)",
        "poison_category": "Schedule E(1) Convulsant Neurotoxin",
        "procedure": (
            "1. Azaraqi seeds are buried in Peeli Matti (yellow clay) and water is poured over it daily for 10 days. "
            "2. Removed and washed; outer seed coat (testa) peeled with knife; cotyledons separated and embryo (pitta) excised. "
            "3. Healthy cotyledons tied in clean cloth bag, immersed in 2 litres of milk, and boiled till milk evaporates. "
            "4. Removed, washed thoroughly with water to yield Azaraqi Mudabbar."
        ),
        "target_alkaloids": ["Strychnine reduction", "Brucine attenuation"],
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "jamalgota": {
        "canonical_name": "Habb-us-Salateen (Jamalgota / Croton)",
        "botanical_name": "Croton tiglium L.",
        "appendix_ref": "Appendix 6.1.6 (iv)",
        "poison_category": "Schedule E(1) Drastic Purgative / Phorbol Ester",
        "procedure": (
            "1. Kernels of Jamalgota tied in cloth bag and boiled in cow's milk until milk becomes dense. "
            "2. When cooled, kernels taken out, and the toxic embryo part (pitta) between cotyledons is completely excised. "
            "3. Yields Jamalgota Mudabbar suitable for micro-posology."
        ),
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "sankhiya": {
        "canonical_name": "Samm-ul-Far (Sankhiya / Arsenic Trioxide)",
        "chemical_name": "Arsenic Trioxide (As2O3)",
        "appendix_ref": "Appendix 6.1.6 (viii)",
        "poison_category": "Schedule E(1) Mineral Poison",
        "procedure": (
            "1. Fine powder of Sankhiya immersed in sufficient fresh Aab-e-Leemu (lemon juice). "
            "2. Ground in mortar of China clay or glass until juice is completely absorbed. "
            "3. Process repeated exactly seven (7) times to obtain Sankhiya Mudabbar."
        ),
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "shingraf": {
        "canonical_name": "Shingraf (Cinnabar / Red Mercuric Sulphide)",
        "chemical_name": "HgS",
        "appendix_ref": "Appendix 6.1.6 (ix)",
        "poison_category": "Schedule E(1) Heavy Metal Compound",
        "procedure": (
            "Ground with fresh Aab-e-Leemu (lemon juice) until completely absorbed and an ultra-fine impalpable powder is obtained. "
            "Repeated three (3) cycles."
        ),
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "seemab": {
        "canonical_name": "Seemab (Purified Mercury)",
        "chemical_name": "Elemental Mercury (Hg)",
        "appendix_ref": "Appendix 6.1.6 (x)",
        "poison_category": "Schedule E(1) Toxic Metal",
        "procedure": (
            "Method A: Ground with half-burnt brick pieces for 12 hours, washed with water, repeated 3 times. "
            "Method B: Squeezed through 4-layer 50-count cloth bag till blackish tinge disappears. "
            "Method C: Ground with pure turmeric powder until color alteration ceases."
        ),
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "beesh": {
        "canonical_name": "Beesh (Meetha Telia / Bachnak / Aconite)",
        "botanical_name": "Aconitum ferox / napellus",
        "appendix_ref": "Appendix 6.1.6 (xii)",
        "poison_category": "Schedule E(1) Cardiotoxin / Neurotoxin",
        "procedure": (
            "Beesh cut into small pieces, tied in fine cloth bag, dipped in vessel of milk without touching bottom, "
            "boiled until milk evaporates, then thoroughly washed in water to obtain Beesh Mudabbar."
        ),
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "bhilawan": {
        "canonical_name": "Bhilawan (Baladur / Marking Nut)",
        "botanical_name": "Semecarpus anacardium L.f.",
        "appendix_ref": "Appendix 6.1.6 (iii)",
        "poison_category": "Schedule E(1) Corrosive Phenolic Resin",
        "procedure": (
            "Thalamus cap removed, corrosive Asal-e-Bhilawan squeezed out with red-hot tongs, "
            "boiled in water three times, then boiled in milk and dried."
        ),
        "safety_gate": "MANDATORY_MUDABBAR_CERTIFICATE_REQUIRED"
    },
    "khabs_ul_hadeed": {
        "canonical_name": "Khabs-ul-Hadeed (Iron Rust / Calx Base)",
        "chemical_name": "Iron Oxide complex",
        "appendix_ref": "Appendix 6.1.6 (xi)",
        "procedure": (
            "Heated red-hot in charcoal fire and quenched in Triphala water or sugarcane vinegar 7 times, "
            "or immersed in vinegar for 14 days and fried in Almond Oil (Roghan-e-Badam)."
        ),
        "safety_gate": "GMP_PURIFICATION_REQUIRED"
    }
}

# ============================================================================
# CANONICAL HERITAGE EDITIONS REGISTRY
# ============================================================================
CANONICAL_LIBRARY_REGISTRY: Dict[str, Dict[str, Any]] = {
    "qanun_book_4_unesco_yale": {
        "book_id": "book-qanun-vol4",
        "title": "Kitab al-Qanun fi al-Tibb: Book Four (Fever, Surgery & Toxicology)",
        "original_title": "كتاب القانون في الطب - الكتاب الرابع",
        "author": "Ibn Sina (Avicenna, 980–1037 CE)",
        "curator_sources": [
            "UNESCO Memory of the World Register",
            "Yale Medical Library (Historic Editio Princeps, Rome: Typographia Medicea, 1593 CE, shelfmark 4770566_1.med.yale.edu)"
        ],
        "key_clinical_domains": [
            "Hummiyat (Fevers: Ephemeral, Humoral-Putrid, and Hectic/Diqq)",
            "Buhran (Crisis Days: Forecasting outcome on Days 4, 7, 11, 14, 21)",
            "Jarahat wa Kusoor (Surgical trauma, bone setting, wound debridement, and cautery)",
            "Zeenah (Aesthetic dermatology: Alopecia/Balkhora, Vitiligo/Bars, Melasma/Kalaf)",
            "Sumoom (Comprehensive Toxicology: Animal venoms, poisonous herbs, mineral toxins)"
        ],
        "governance_status": "GOLD_STANDARD_CANONICAL_ANCHOR"
    },
    "akhlaq_e_jalali_rekhta": {
        "book_id": "book-akhlaq-jalali",
        "title": "Akhlaq-e-Jalali (Lawami' al-Ishraq fi Makarim al-Akhlaq)",
        "original_title": "اخلاق جلالی",
        "author": "Allama Jalal-ud-Deen Muhammad Dawwani (1426–1502 CE)",
        "curator_sources": ["Naval Kishore Press (1897) / Rekhta Classical Digital Archive"],
        "key_clinical_domains": [
            "Ilaj bil Nafsiyat (Unani Psychosomatic Medicine)",
            "Tadbeer-e-Nafsani (Cognitive-behavioral emotional equilibrium)",
            "Quwa Nafsaniyya balance (Aaqila, Ghadabiyya, Shahwiyya)",
            "Clinical intervention for Melancholia (Malikhuliya), Health Anxiety (Miraq), Panic and Grief"
        ],
        "governance_status": "PSYCHOSOMATIC_FOUNDATION_CORPUS"
    },
    "shifa_al_abdan_mcgill": {
        "book_id": "book-shifa-al-abdan",
        "title": "Shifa' al-Abdan",
        "original_title": "شفاء الابدان",
        "author": "Hakim Wajid Ali Khan",
        "curator_sources": ["McGill University Osler Library of the History of Medicine (MS osl_robe_7786_43-20833)"],
        "key_clinical_domains": [
            "Amraz-e-Ras ta Qadam (Organ-by-organ internal medicine)",
            "Indian Subcontinent Clinical Experience & Bedside Case Studies",
            "Synergistic Compound Formulations (Qarabadin) & Indigenous Substitute Botanicals"
        ],
        "governance_status": "CLINICAL_PRACTICE_VALIDATION_CORPUS"
    },
    "ishrah_al_adwiyah_wadud": {
        "book_id": "book-ishrah-adwiyah",
        "title": "Ishrah al-Adwiyah (Kulliyat-e-Adwiyah)",
        "original_title": "اشراح الادویہ (کلیات ادویہ)",
        "author": "Dr. Abdul Wadud, M.D. (Ilmul Advia) AMU Aligarh",
        "curator_sources": ["S.H. Unani Tibbiya College / Academic BUMS & MD Curriculum (Burhanpur 2004)"],
        "key_clinical_domains": [
            "Kulliyat-e-Adwiyah (General Principles of Unani Pharmacology)",
            "Pharmacodynamics & Mechanism of Action (74 Standardized Action Terms)",
            "Taste Science (9 Za'iqat) & Elemental Dynamics",
            "Toxicology & 4th-Degree Drugs vs Absolute Poisons (Paracelsus-Avicenna Law)",
            "8 Statutory Compounding Rationale (Qawanin-e-Tarkeeb)",
            "Drug Antagonism (Pharmacological, Chemical, Physical Incompatibility)",
            "Drug Substitution (Ibdal: Badal-e-Aqrab, Badal-e-Sanawi, Badal-e-Baeed)"
        ],
        "governance_status": "PHARMACOLOGICAL_CURRICULUM_FOUNDATION"
    }
}

# ============================================================================
# 50 OFFICIAL COMPOUND FORMULATIONS (UPI PART-II, VOLUME-IV)
# ============================================================================
UPI_PART2_VOL4_MONOGRAPHS: List[Dict[str, Any]] = [
    {
        "monograph_no": 1,
        "name": "Aksir-e-Riyah",
        "urdu_name": "اکسیر ریاح",
        "nfum_code": "NFUM-VI, 7.2",
        "page_no": 5,
        "form": "Safoof (Powdered preparation)",
        "composition": [
            {"ingredient": "Hilteet Khalis (Ferula foetida Regel)", "part": "Oleo-resin", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Kafoor Khalis (Cinnamomum camphora)", "part": "Crystal", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Zanjabeel (Zingiber officinale Rosc)", "part": "Rhizome", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Ajwayin Khurasani (Hyoscyamus niger L)", "part": "Seed", "quantity_g": 80.0, "is_schedule_e1": True},
            {"ingredient": "Filfil Siyah (Piper nigrum L)", "part": "Fruit", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Gul-e-Aak (Calotropis procera)", "part": "Flower", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Zarambad (Curcuma zedoaria Rosc)", "part": "Rhizome", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Soda Khurdani (Sodium bicarbonate)", "part": "Powder", "quantity_g": 120.0, "is_schedule_e1": False},
            {"ingredient": "Namak Siyah (Black salt)", "part": "Crystal", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Namak-e-Turb (Amal-e-Iqla Lixiviated Raphanus sativus)", "part": "Powder", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Naushadar (Ammonium Chloride)", "part": "Crystal", "quantity_g": 80.0, "is_schedule_e1": False}
        ],
        "actions": ["Kasir-e-Riyah (Carminative)"],
        "therapeutic_uses": ["Qulanj (Colic)", "Nafkh-e-Shikam (Flatulence)", "Waj-ul-Kulya (Renal Colic)"],
        "dose": "500 mg",
        "mode_of_administration": "For oral use along with lukewarm water.",
        "physicochemical_specs": {
            "total_ash_max_pct": 30.0,
            "acid_insoluble_ash_max_pct": 4.0,
            "alcohol_soluble_extractive_min_pct": 13.0,
            "water_soluble_extractive_min_pct": 53.0,
            "ph_range": "5 - 6",
            "loss_on_drying_max_pct": 8.0
        },
        "tlc_fingerprint": {
            "solvent_system": "chloroform: ethyl acetate (5: 1)",
            "spray_reagent": "5% vanillin sulphuric acid reagent (105°C)",
            "rf_values": [0.28, 0.58, 0.76, 0.82],
            "spot_color": "Violet"
        },
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 2,
        "name": "Anoshdaru",
        "urdu_name": "انوشدارو",
        "nfum_code": "NFUM-I, 5.1",
        "page_no": 8,
        "form": "Majoon / Electuary (Semi-solid, 72 Brix)",
        "composition": [
            {"ingredient": "Aamla (Phyllanthus emblica L)", "part": "Fruit", "quantity_g": 700.0, "is_schedule_e1": False},
            {"ingredient": "Gul-e-Surkh (Rosa damascena Mill)", "part": "Flower", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Sad Kufi (Cyperus rotundus L)", "part": "Rhizome", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Qaranful (Syzygium aromaticum)", "part": "Flower bud", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Mastagi (Pistacia lentiscus L)", "part": "Resin", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Sumbul-ut-Teeb (Nardostachys jatamansi)", "part": "Rhizome", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Zafran (Crocus sativus L)", "part": "Stigma & Style", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Qand safaid (Sugar)", "part": "Crystal", "quantity_g": 1000.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Aam (General tonic)", "Mufatteh Sudad (Deobstruent)", "Qabiz (Constipative)"],
        "therapeutic_uses": ["Khafqan (Palpitation)", "Zof-e-Qalb (Cardiac weakness)", "Zof-e-Umoomi (Debility)", "Yarqan-e-Suddi (Obstructive Jaundice)", "Zaheer (Dysentery)"],
        "dose": "5-10 g twice daily",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {
            "total_ash_max_pct": 1.0,
            "acid_insoluble_ash_max_pct": 0.5,
            "alcohol_soluble_extractive_min_pct": 27.0,
            "water_soluble_extractive_min_pct": 38.0,
            "ph_range": "4 - 5",
            "reducing_sugar_min_pct": 26.0,
            "non_reducing_sugar_max_pct": 15.0
        },
        "tlc_fingerprint": {
            "solvent_system": "chloroform: methanol (7.4: 2.6)",
            "rf_values": [0.32, 0.67, 0.76],
            "spot_color": "Greenish black / Brownish black"
        },
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 3,
        "name": "Araq-e-Maul Laham Makoh Kasni Wala",
        "urdu_name": "عرق ماء اللحم مکوہ کاسنی والا",
        "nfum_code": "NFUM-V, 8.7",
        "page_no": 11,
        "form": "Araq / Distillate (Liquid)",
        "composition": [
            {"ingredient": "Barg Gawzaban (Borago officinalis)", "part": "Leaf", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Gilo Sabz (Tinospora cordifolia)", "part": "Stem", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Gosht-e-Buz (Goat's Meat decoction)", "part": "Meat", "quantity_g": 1600.0, "is_schedule_e1": False},
            {"ingredient": "Aab-e-Kasni Sabz (Cichorium intybus)", "part": "Leaf juice", "quantity_g": 800.0, "is_schedule_e1": False},
            {"ingredient": "Aab-e-Mako (Solanum nigrum)", "part": "Whole plant juice", "quantity_g": 800.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Aaza (Tonic for Principal Organs)", "Muqawwi-e-Meda (Stomachic)", "Muqawwi-e-Jigar (Hepatoprotective)"],
        "therapeutic_uses": ["Amraaz-e-Meda (Gastric disease)", "Amraz-e-Jigar (Hepatic dysfunction)", "General organ debility"],
        "dose": "125 ml",
        "mode_of_administration": "For oral use along with Sharbat-e-Kasoos.",
        "physicochemical_specs": {"ph_range": "5 - 6", "specific_gravity": "1.0 - 1.1", "refractive_index": "1.33 - 1.34"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 4,
        "name": "Dawa-e-Atfal",
        "urdu_name": "دواء الاطفال",
        "nfum_code": "NFUM-VI, 7.3",
        "page_no": 13,
        "form": "Safoof (Pediatric Powder)",
        "composition": [
            {"ingredient": "Khaksi (Sisymbrium irio L)", "part": "Seed", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Milk", "part": "Liquid", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Sat-e-Loban (Styrax benzoin Dryand)", "part": "Extract", "quantity_g": 1.0, "is_schedule_e1": False}
        ],
        "actions": ["Daf-e-Tap-e-Atfal (Pediatric Antipyretic)"],
        "therapeutic_uses": ["Diqq-ul-Atfal (Pediatric Tuberculosis / Chronic Low-grade Fever)"],
        "dose": "1 g twice daily",
        "mode_of_administration": "For oral use along with Khamira Marwareed (2g).",
        "physicochemical_specs": {"total_ash_max_pct": 6.0, "acid_insoluble_ash_max_pct": 1.0, "ph_range": "4 - 5"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 5,
        "name": "Dawa-e-Tikore",
        "urdu_name": "دواء ٹکور",
        "nfum_code": "NFUM-VI, 7.5",
        "page_no": 15,
        "form": "Zimad / Poultice (External)",
        "composition": [
            {"ingredient": "Meda Lakri (Litsea chinensis Lam)", "part": "Stem bark", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Anba Haldi (Curcuma amada Roxb)", "part": "Rhizome", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Malkangani (Celastrus paniculatus)", "part": "Seed", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Asgand Nagauri (Withania somnifera)", "part": "Root", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Zanjabeel Khushk (Zingiber officinale)", "part": "Rhizome", "quantity_g": 100.0, "is_schedule_e1": False}
        ],
        "actions": ["Moharrik (Stimulant)", "Muqawwi-e-Asab (Nervine Tonic)"],
        "therapeutic_uses": ["Zof-e-Qazeeb (Penile Atony / Neuromuscular flaccidity)"],
        "dose": "15 g (External application)",
        "mode_of_administration": "Poultice soaked in hot sesame oil applied locally before use of Tila.",
        "physicochemical_specs": {"total_ash_max_pct": 16.0, "ph_range": "6 - 7"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 6,
        "name": "Habb-e-Ayarij",
        "urdu_name": "حب ایارج",
        "nfum_code": "NFUM-V, 1.2",
        "page_no": 18,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Asaroon (Asarum europaeum L)", "part": "Rhizome", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Elwa / Sibr (Aloe vera extract)", "part": "Extract", "quantity_g": 400.0, "is_schedule_e1": False},
            {"ingredient": "Balchar / Sumbul-ut-Tibb", "part": "Rhizome", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Mastagi (Pistacia lentiscus)", "part": "Resin", "quantity_g": 30.0, "is_schedule_e1": False},
            {"ingredient": "Zafran (Crocus sativus L)", "part": "Stigma & Style", "quantity_g": 2.8, "is_schedule_e1": False}
        ],
        "actions": ["Tanqiya-e-Dimagh (Cephalic evacuation / Cleansing of Brain)"],
        "therapeutic_uses": ["Malikhuliya (Melancholia / Depressive disorder)", "Headache of morbid humors"],
        "dose": "250 mg - 1.5 g at night",
        "mode_of_administration": "For oral use along with Araq-e-Gaozaban (120 ml).",
        "physicochemical_specs": {"disintegration_time_max_min": 30, "ph_range": "5 - 6"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 7,
        "name": "Habb-e-Azaraqi",
        "urdu_name": "حب اذراقی",
        "nfum_code": "NFUM-I, 1.5",
        "page_no": 21,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Azaraqi Mudabbar (Strychnos nux-vomica detoxified)", "part": "Seed", "quantity_g": 20.0, "is_schedule_e1": True},
            {"ingredient": "Filfil Siyah (Piper nigrum L)", "part": "Fruit", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Filfil Daraz (Piper longum L)", "part": "Fruit", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Araq-e-Ajwaiyn", "part": "Distillate", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Asab (Nervine tonic)", "Moharrik-e-Asab (Nerve stimulant)"],
        "therapeutic_uses": ["Falij (Paralysis / Hemiplegia)", "Laqwa (Facial Paralysis)", "Khadar (Numbness / Sensory insensibility)"],
        "dose": "250 - 500 mg twice daily",
        "mode_of_administration": "For oral use along with water after meals.",
        "physicochemical_specs": {"total_ash_max_pct": 5.0, "disintegration_time_max_min": 30, "ph_range": "4 - 5"},
        "tlc_fingerprint": {"solvent_system": "toluene: ethyl acetate (7: 3)", "rf_values": [0.18, 0.63], "spot_color": "Violet"},
        "schedule_e1_warning": True,
        "statutory_caution": "SCHEDULE E(1) POISON: Contains Kuchla Mudabbar. Strictly adhere to Appendix 6.1.6(vi) detoxification."
    },
    {
        "monograph_no": 8,
        "name": "Habb-e-Bawaseer Amya",
        "urdu_name": "حب بواسیر اعمیٰ",
        "nfum_code": "NFUM-I, 1.6",
        "page_no": 24,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Halela Kabuli Biryan (Roasted Terminalia chebula)", "part": "Pericarp", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Rasaut (Berberis aristata extract detoxified)", "part": "Extract", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Raughan Zard (Pure Ghee)", "part": "Ghee", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Mulaiyin (Laxative)"],
        "therapeutic_uses": ["Bawaseer Amya (Blind piles)", "Qabz (Chronic Constipation)"],
        "dose": "250 - 500 mg",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 4.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 9,
        "name": "Habb-e-Bawaseer Badi",
        "urdu_name": "حب بواسیر بادی",
        "nfum_code": "NFUM-V, 1.3",
        "page_no": 26,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Rasaut (Berberis aristata extract detoxified)", "part": "Extract", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Maghz Tukhm-e-Bakayin (Melia azedarach)", "part": "Kernel", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Maghz Tukhm-e-Neem (Azadirachta indica)", "part": "Kernel", "quantity_g": 150.0, "is_schedule_e1": False},
            {"ingredient": "Gond Keeker (Acacia nilotica)", "part": "Gum", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Mulaiyin (Laxative)"],
        "therapeutic_uses": ["Bawaseer-e-Badi (Blind piles / Non-bleeding hemorrhoids)", "Qabz (Constipation)"],
        "dose": "Two pills (Each 850 mg)",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 9.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 10,
        "name": "Habb-e-Bawaseer Khooni",
        "urdu_name": "حب بواسیر خونی",
        "nfum_code": "NFUM-V, 1.4",
        "page_no": 29,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Rasaut (Berberis aristata extract)", "part": "Extract", "quantity_g": 140.0, "is_schedule_e1": False},
            {"ingredient": "Sang-e-Jarahat (Magnesium silicate)", "part": "Solid", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Kateera Safaid (Astragalus gummifer)", "part": "Gum", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Geru (Red Earth)", "part": "Solid", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Mazu Sabz (Quercus infectoria)", "part": "Gall", "quantity_g": 20.0, "is_schedule_e1": False}
        ],
        "actions": ["Mulaiyin (Laxative)", "Habis-ud-Dam (Styptic / Hemostatic)"],
        "therapeutic_uses": ["Bawaseer Damya (Bleeding piles)", "Bawaseer-e-Khooni"],
        "dose": "Two pills (725 mg each) twice a day",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 25.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 11,
        "name": "Habb-e-Dabba-e-Atfal",
        "urdu_name": "حب دبہ الاطفال",
        "nfum_code": "NFUM-I, 1.11",
        "page_no": 32,
        "form": "Habb (Pediatric Pill)",
        "composition": [
            {"ingredient": "Habb-us-Salateen Mudabbar (Croton tiglium detoxified)", "part": "Seed", "quantity_g": 10.0, "is_schedule_e1": True},
            {"ingredient": "Sibr (Aloe vera extract)", "part": "Extract", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Kateera (Cochlospermum religiosum)", "part": "Gum", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Aab-e-Barg-e-Kanghi (Abutilon indicum)", "part": "Leaf juice", "quantity_g": 50.0, "is_schedule_e1": False}
        ],
        "actions": ["Mus-hil (Purgative / Broncho-mucolytic)"],
        "therapeutic_uses": ["Dabba-e-Atfal (Infantile Broncho-pneumonia / Stridor)", "Qabz (Constipation)"],
        "dose": "125 - 250 mg",
        "mode_of_administration": "For oral use along with water after meals.",
        "physicochemical_specs": {"total_ash_max_pct": 7.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 12,
        "name": "Habb-e-Sadar",
        "urdu_name": "حب صدر",
        "nfum_code": "NFUM-VI, 1.11",
        "page_no": 35,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Mom Kham (Bee Wax)", "part": "Wax", "quantity_g": 250.0, "is_schedule_e1": False},
            {"ingredient": "Mastagi Roomi (Pistacia lentiscus L)", "part": "Resin", "quantity_g": 250.0, "is_schedule_e1": False}
        ],
        "actions": ["Musakkin (Sedative / Thoracic soothing)"],
        "therapeutic_uses": ["Waj-ul-Sadr (Chest pain / Intercostal neuralgia / Pleuritic distress)"],
        "dose": "400 - 800 mg twice daily",
        "mode_of_administration": "For oral use along with lukewarm water.",
        "physicochemical_specs": {"total_ash_max_pct": 4.0, "ph_range": "7 - 8"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 13,
        "name": "Habb-e-Harsinghar",
        "urdu_name": "حب ہارسنگھار",
        "nfum_code": "NFUM-II, 1.12",
        "page_no": 36,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Maghz-e-Tukhm-e-Harsinghar (Nyctanthes arbor-tristis)", "part": "Kernel", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Filfil Siyah (Piper nigrum L)", "part": "Fruit", "quantity_g": 5.0, "is_schedule_e1": False}
        ],
        "actions": ["Mulaiyin (Laxative / Analgesic)"],
        "therapeutic_uses": ["Bawaseer Damiya (Bleeding piles)", "Bawaseer Amya (Blind piles)", "Sciatica (Irq-un-Nasa)"],
        "dose": "250 - 500 mg twice daily",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 5.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 14,
        "name": "Habb-e-Hilteet",
        "urdu_name": "حب حلتيت",
        "nfum_code": "NFUM-1, 1.17",
        "page_no": 39,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Hilteet (Ferula foetida Regel)", "part": "Resin", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Zanjabeel (Zingiber officinale)", "part": "Rhizome", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Namak-e-Sang (Rock Salt)", "part": "Crystals", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Tankar Biryan (Borax roasted)", "part": "Powder", "quantity_g": 25.0, "is_schedule_e1": False}
        ],
        "actions": ["Kasir-e-Riyah (Carminative)", "Muqawwi-e-Meda (Stomachic)", "Hazim (Digestive)", "Mustahhi (Appetizer)"],
        "therapeutic_uses": ["Nafkh-e-Shikam (Flatulence)", "Zof-e-Ishteha (Anorexia)", "Zof-e-Hazm (Dyspepsia)"],
        "dose": "0.5 - 1 g",
        "mode_of_administration": "For oral use along with water after meals.",
        "physicochemical_specs": {"total_ash_max_pct": 37.0, "ph_range": "9 - 10"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 15,
        "name": "Habb-e-Loban",
        "urdu_name": "حب لوبان",
        "nfum_code": "NFUM-III, 1.31",
        "page_no": 42,
        "form": "Habb / Lozenges",
        "composition": [
            {"ingredient": "Kundur (Boswellia serrata)", "part": "Resin", "quantity_g": 7.0, "is_schedule_e1": False},
            {"ingredient": "Aarad Baqla (Vicia faba)", "part": "Seed", "quantity_g": 7.0, "is_schedule_e1": False},
            {"ingredient": "Rubb-us-Soos (Glycyrrhiza extract)", "part": "Aq. Ext", "quantity_g": 7.0, "is_schedule_e1": False},
            {"ingredient": "Gul-e-Banafsha (Viola odorata)", "part": "Flower", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Maghz-e-Badam Talkh (Bitter Almond)", "part": "Kernel", "quantity_g": 2.0, "is_schedule_e1": False}
        ],
        "actions": ["Musakkin-e-Sual (Cough relieving)", "Munaffis-e-Balgham (Expectorant)", "Mohallil-e-Warm (Anti-inflammatory)"],
        "therapeutic_uses": ["Sual-e-Yabis (Dry cough)", "Zat-ur-Riya (Pneumonia)", "Zat-ul-Janab (Pleurisy)", "Dabba-e-Atfal"],
        "dose": "250 mg (Lozenges)",
        "mode_of_administration": "For oral use (dissolve slowly in mouth).",
        "physicochemical_specs": {"total_ash_max_pct": 6.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 16,
        "name": "Habb-e-Luluvi",
        "urdu_name": "حب لؤلؤی",
        "nfum_code": "NFUM-III, 1.32",
        "page_no": 45,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Zahar Mohra (Bezoar stone / Serpentine)", "part": "Mineral", "quantity_g": 12.0, "is_schedule_e1": False},
            {"ingredient": "Sandal Safaid (Santalum album)", "part": "Heart wood", "quantity_g": 12.0, "is_schedule_e1": False},
            {"ingredient": "Marwareed (Mytilus margaritiferus pearl)", "part": "Pearl", "quantity_g": 12.0, "is_schedule_e1": False},
            {"ingredient": "Araq-e-Keora", "part": "Distillate", "quantity_g": 12.0, "is_schedule_e1": False},
            {"ingredient": "Araq-e-Gulab", "part": "Distillate", "quantity_g": 12.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Qalb (Cardiotonic)", "Habis-ud-Dam (Styptic)", "Muqawwi-e-Aam (General Tonic)"],
        "therapeutic_uses": ["Nazf-ud-Dam (Hemorrhage / Hemoptysis)", "Zof-e-Aam (General debility)", "Khafqan"],
        "dose": "2 g",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 36.0, "ph_range": "7 - 8"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 17,
        "name": "Habb-e-Mamool Qawi",
        "urdu_name": "حب معمول قوی",
        "nfum_code": "NFUM-III, 1.35",
        "page_no": 48,
        "form": "Habb (Pill for External/Local Use)",
        "composition": [
            {"ingredient": "Pakhanbed (Bergenia ciliata)", "part": "Root", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Murdar Sang (Litharge / Monoxide of Lead)", "part": "Mineral", "quantity_g": 5.0, "is_schedule_e1": True},
            {"ingredient": "Rasaut (Berberis aristata)", "part": "Extract", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Sandal surkh (Pterocarpus santalinus)", "part": "Heart wood", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Muqil (Commiphora mukul)", "part": "Gum", "quantity_g": 5.0, "is_schedule_e1": False}
        ],
        "actions": ["Habis-ud-Dam (Styptic / Astringent)"],
        "therapeutic_uses": ["Bawaseer-e-Damiya (Bleeding Piles)", "Bawaseer-e-Umya (Blind Piles)"],
        "dose": "For local application",
        "mode_of_administration": "For external use only (paste in suitable medium).",
        "physicochemical_specs": {"total_ash_max_pct": 24.0, "ph_range": "4 - 5"},
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 18,
        "name": "Habb-e-Mastagi",
        "urdu_name": "حب مصطگی",
        "nfum_code": "NFUM-III, 1.36",
        "page_no": 51,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Namak Hindi (Salt)", "part": "Crystals", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Post Halela Zard (Terminalia chebula)", "part": "Pericarp", "quantity_g": 6.0, "is_schedule_e1": False},
            {"ingredient": "Zanjabeel (Zingiber officinale)", "part": "Rhizome", "quantity_g": 6.0, "is_schedule_e1": False},
            {"ingredient": "Sumbul-ut-Teeb (Nardostachys jatamansi)", "part": "Rhizome", "quantity_g": 6.0, "is_schedule_e1": False},
            {"ingredient": "Mastagi (Pistacia lentiscus)", "part": "Resin", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Halela Siyah (Terminalia chebula)", "part": "Unripe fruit", "quantity_g": 14.0, "is_schedule_e1": False},
            {"ingredient": "Sibr (Aloe vera extract)", "part": "Extract", "quantity_g": 28.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Meda (Stomachic)", "Kasir-e-Riyah (Carminative)"],
        "therapeutic_uses": ["Zof-e-Meda (Gastric weakness)", "Nafkh-e-Shikam (Flatulence)"],
        "dose": "500 - 1000 mg",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 15.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 19,
        "name": "Habb-e-Mulaiyin",
        "urdu_name": "حب ملین",
        "nfum_code": "NFUM-III, 1.37",
        "page_no": 54,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Maghz-e-Habb-ul-Salateen Mudabbar (Croton tiglium detoxified)", "part": "Kernel", "quantity_g": 6.0, "is_schedule_e1": True},
            {"ingredient": "Maghz-e-Badam (Sweet Almond)", "part": "Kernel", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Maghz-e-Tukhm-e-Bedanjeer (Castor seed kernel)", "part": "Kernel", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Qand Safaid (Sugar)", "part": "Crystals", "quantity_g": 20.0, "is_schedule_e1": False}
        ],
        "actions": ["Mulaiyin (Laxative / Mild Purgative)"],
        "therapeutic_uses": ["Qabz (Habitual Constipation)"],
        "dose": "250 mg",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 6.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 20,
        "name": "Habb-e-Surfa",
        "urdu_name": "حب سرفہ",
        "nfum_code": "NFUM-I, 1.59",
        "page_no": 57,
        "form": "Habb (Pill)",
        "composition": [
            {"ingredient": "Asl-us-Soos (Glycyrrhiza glabra)", "part": "Stolon & Root", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Tukhm-e-Khubbazi (Malva sylvestris)", "part": "Seed", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Maghz-e-Tukhm-e-Kaddu Shireen (Pumpkin seed)", "part": "Kernel", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Samagh-e-Arabi Biryan (Acacia roasted)", "part": "Gum", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Zafran (Crocus sativus L)", "part": "Style & Stigma", "quantity_g": 5.0, "is_schedule_e1": False}
        ],
        "actions": ["Musakkin-e-Sual (Cough relaxant)"],
        "therapeutic_uses": ["Sual (Bronchitis / Persistent Cough)"],
        "dose": "125 - 250 mg",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 6.0, "disintegration_time_max_min": 30},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 21,
        "name": "Itrifal Fauladi",
        "urdu_name": "اطریفل فولادی",
        "nfum_code": "NFUM-III, 5.13",
        "page_no": 60,
        "form": "Itrifal (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Kushta-e-Faulad (Calx of Iron)", "part": "Powder", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Halela (Terminalia chebula)", "part": "Pericarp", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Amla (Phyllanthus emblica)", "part": "Fruit", "quantity_g": 120.0, "is_schedule_e1": False},
            {"ingredient": "Satawar (Asparagus racemosus)", "part": "Root", "quantity_g": 45.0, "is_schedule_e1": False},
            {"ingredient": "Asl-us-Soos (Glycyrrhiza glabra)", "part": "Stolon & Root", "quantity_g": 60.0, "is_schedule_e1": False},
            {"ingredient": "Asal (Honey)", "part": "As such", "quantity_g": 335.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Meda (Stomachic)", "Muwallid-e-Dam (Haematogenic / Erythropoietic)", "Muqawwi-e-Ama (Intestinal tonic)"],
        "therapeutic_uses": ["Bawaseer-e-Umya (Hemorrhoids)", "Su-ul-Qinya (Anemia / Microcytic hypochromic)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use along with water or Araq-e-Gaozaban.",
        "physicochemical_specs": {"total_ash_max_pct": 5.0, "reducing_sugar_min_pct": 26.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 22,
        "name": "Itrifal Mundi",
        "urdu_name": "اطریفل منڈی",
        "nfum_code": "NFUM-III, 5.14",
        "page_no": 63,
        "form": "Itrifal (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Gul-e-Mundi (Sphaeranthus indicus)", "part": "Inflorescence", "quantity_g": 26.66, "is_schedule_e1": False},
            {"ingredient": "Post-e-Halela Zard", "part": "Pericarp", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Halela Siyah", "part": "Pericarp", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Barg-e-Shahtara (Fumaria indica)", "part": "Leaf", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Ustukhuddus (Lavandula stoechas)", "part": "Inflorescence", "quantity_g": 40.0, "is_schedule_e1": False}
        ],
        "actions": ["Mussaffi-e-Dam (Blood purifier / Alterative)"],
        "therapeutic_uses": ["Ramad (Conjunctivitis)", "Fasad-e-Dam (Putrefaction of Blood / Dermatitis)", "Jarab-wa-Hikka (Scabies and Pruritus)"],
        "dose": "10 - 20 g",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "reducing_sugar_min_pct": 37.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 23,
        "name": "Itrifal Sana Qawi",
        "urdu_name": "اطریفل سنا قوی",
        "nfum_code": "NFUM-III, 5.15",
        "page_no": 66,
        "form": "Itrifal (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Rewand Chini (Rheum emodi)", "part": "Root", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Balela", "part": "Pericarp", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Aamla (Phyllanthus emblica)", "part": "Fruit", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Halela Zard", "part": "Pericarp", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Sana (Cassia angustifolia)", "part": "Leaf", "quantity_g": 50.0, "is_schedule_e1": False}
        ],
        "actions": ["Mulaiyin (Laxative / Purgative)"],
        "therapeutic_uses": ["Safa (Scalp infection / Seborrhea)", "Qabz (Chronic Constipation)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "water_soluble_extractive_min_pct": 68.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 24,
        "name": "Itrifal Ustukhuddus",
        "urdu_name": "اطریفل اسطخودوس",
        "nfum_code": "NFUM-I, 5.20",
        "page_no": 69,
        "form": "Itrifal (Semi-solid, 77 Brix)",
        "composition": [
            {"ingredient": "Ustukhuddus (Lavandula stoechas)", "part": "Inflorescence", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Halela Zard", "part": "Pericarp", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Halela Kabuli", "part": "Pericarp", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Halela Siyah", "part": "Fruit", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Balela", "part": "Pericarp", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Aamla", "part": "Fruit", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Bisfayej (Polypodium vulgare)", "part": "Rhizome", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Aftimoon (Cuscuta reflexa)", "part": "Whole plant", "quantity_g": 100.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Asab (Nervine tonic)", "Tanqiya-e-Dimagh (Brain detoxifier)"],
        "therapeutic_uses": ["Suda (Headache)", "Falij (Hemiplegia)", "Laqwa (Facial palsy)", "Nazla-e-Muzmin (Chronic Catarrh / Sinusitis)", "Sara (Epilepsy)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use along with lukewarm water.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "reducing_sugar_min_pct": 37.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 25,
        "name": "Itrifal-e-Deedan",
        "urdu_name": "اطریفل دیدان",
        "nfum_code": "NFUM-I, 5.12",
        "page_no": 72,
        "form": "Itrifal (Semi-solid, 76 Brix)",
        "composition": [
            {"ingredient": "Baobarang (Embelia ribes)", "part": "Seed", "quantity_g": 125.0, "is_schedule_e1": False},
            {"ingredient": "Turbud (Operculina turpethum)", "part": "Root", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Habb-ul-Neel (Ipomoea hederacea)", "part": "Seed", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Qimbeel (Mallotus philippinensis)", "part": "Fruit", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Palaspapra (Butea monosperma)", "part": "Seed", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Afsanteen (Artemisia absinthium)", "part": "Aerial part", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Shahm-e-Hanzal (Citrullus colocynthis)", "part": "Fruit pulp", "quantity_g": 15.0, "is_schedule_e1": True}
        ],
        "actions": ["Daf-e-Kirm-e-Ama (Anthelmintic / Vermifuge)"],
        "therapeutic_uses": ["Deedan-e-Ama (Intestinal helminthiasis / Worm infestation)"],
        "dose": "10 - 15 g",
        "mode_of_administration": "For oral use along with water at bed time.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 26,
        "name": "Itrifal-e-Kabir",
        "urdu_name": "اطریفل کبیر",
        "nfum_code": "NFUM-I, 5.14",
        "page_no": 75,
        "form": "Itrifal (Semi-solid, 76 Brix)",
        "composition": [
            {"ingredient": "Halela", "part": "Pericarp", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Balela", "part": "Pericarp", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Amla", "part": "Fruit", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Buzidan (Tanacetum umbelliferum)", "part": "Root", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Sheetraj Hindi (Plumbago zeylanica)", "part": "Root", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Behman Safaid (Centaurea behen)", "part": "Root", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Behman Surkh (Salvia haematodes)", "part": "Root", "quantity_g": 20.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Dimagh (Brain tonic)", "Munaqqi-e-Dimagh (Clear bad humor from brain)"],
        "therapeutic_uses": ["Zof-e-Dimagh (Weakness of brain)", "Nazla Muzmin (Chronic catarrh)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use twice daily after meals.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "reducing_sugar_min_pct": 36.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 27,
        "name": "Khamira Gawzaban Ambari Jadwar Ood Saleeb Wala",
        "urdu_name": "خمیرہ گاؤزبان عنبری جدوار عود صلیب والا",
        "nfum_code": "NFUM-V, 5.19",
        "page_no": 78,
        "form": "Khamira (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Abresham Muqarraz (Bombyx mori silk cocoon)", "part": "Silk cocoon", "quantity_g": 6.25, "is_schedule_e1": False},
            {"ingredient": "Berg Gaozaban (Borago officinalis)", "part": "Leaf", "quantity_g": 37.5, "is_schedule_e1": False},
            {"ingredient": "Ambar Ashhab (Ambra grasea)", "part": "As such", "quantity_g": 0.661, "is_schedule_e1": False},
            {"ingredient": "Warq-e-Nuqra (Silver foil)", "part": "Foils", "quantity_g": 8.25, "is_schedule_e1": False},
            {"ingredient": "Warq-e-Tila (Gold leaf)", "part": "Foils", "quantity_g": 14.0, "is_schedule_e1": False},
            {"ingredient": "Jadwar Saeeda (Delphinium denudatum)", "part": "Root", "quantity_g": 26.5, "is_schedule_e1": False},
            {"ingredient": "Ood Saleeb Saeeda (Paeonia emodi)", "part": "Tuber", "quantity_g": 34.25, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Aza-e-Raeesa (Tonic to Brain, Heart and Liver)"],
        "therapeutic_uses": ["Ummus Sibyan (Infantile epilepsy)", "Ikhtenaqur-Reham (Hysteria)", "Khafqan (Palpitation)"],
        "dose": "5 g",
        "mode_of_administration": "For oral use once a day after breakfast.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "water_soluble_extractive_min_pct": 74.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 28,
        "name": "Khamira-e-Banafsha",
        "urdu_name": "خمیرہ بنفشہ",
        "nfum_code": "NFUM-I, 5.45",
        "page_no": 81,
        "form": "Khamira (Semi-solid, 80 Brix)",
        "composition": [
            {"ingredient": "Gul-e-Banafsha (Viola odorata L)", "part": "Flower", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Qand Safaid (Sugar)", "part": "Crystal", "quantity_g": 1600.0, "is_schedule_e1": False}
        ],
        "actions": ["Munaffis-e-Balgham (Expectorant)", "Mulaiyin (Laxative)"],
        "therapeutic_uses": ["Qabz (Constipation)", "Nazla (Catarrh)", "Sual (Cough)"],
        "dose": "20 - 40 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "water_soluble_extractive_min_pct": 79.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 29,
        "name": "Khamira Gawzaban Ambari",
        "urdu_name": "خمیرہ گاؤزبان عنبری",
        "nfum_code": "NFUM-V, 5.18",
        "page_no": 83,
        "form": "Khamira (Semi-solid, 76 Brix)",
        "composition": [
            {"ingredient": "Abresham Muqarraz (Bombyx mori)", "part": "Silk cocoon", "quantity_g": 8.33, "is_schedule_e1": False},
            {"ingredient": "Barg Gawzaban (Borago officinalis)", "part": "Leaf", "quantity_g": 50.0, "is_schedule_e1": False},
            {"ingredient": "Ambar Ashhab (Ambra grasea)", "part": "Ambergris", "quantity_g": 0.83, "is_schedule_e1": False},
            {"ingredient": "Warq Nuqra (Silver foil)", "part": "Foil", "quantity_g": 9.16, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Qalb wa Dimagh (Cardiac and Brain tonic)"],
        "therapeutic_uses": ["Zof-e-Qalb wa Dimagh (Weakness of heart and brain)", "Khafqan (Palpitation)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use twice a day after meals.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "reducing_sugar_min_pct": 29.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 30,
        "name": "Khamira Murakkab",
        "urdu_name": "خمیرہ مرکب",
        "nfum_code": "NFUM-V, 5.25",
        "page_no": 86,
        "form": "Khamira (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Abresham Muqarraz", "part": "Silk cocoon", "quantity_g": 7.5, "is_schedule_e1": False},
            {"ingredient": "Berg-e-Gaozaban", "part": "Leaf", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Agar hindi (Aquilaria agallocha)", "part": "Heart wood", "quantity_g": 3.75, "is_schedule_e1": False},
            {"ingredient": "Zafran (Crocus sativus L)", "part": "Style & Stigma", "quantity_g": 0.21, "is_schedule_e1": False},
            {"ingredient": "Warq-e-Nuqra", "part": "Foil", "quantity_g": 4.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Qalb wa Dimagh (Tonic for Brain, Heart and Liver)"],
        "therapeutic_uses": ["Um-us-Sibyan (Infantile Epilepsy)", "Ikhtenaq-ur-Rehem (Hysteria)", "Ikhtilaaj (Palpitation)"],
        "dose": "5 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 31,
        "name": "Laooq-e-Falij",
        "urdu_name": "لعوق فالج",
        "nfum_code": "NFUM-III, 5.4",
        "page_no": 89,
        "form": "Laooq / Linctus (Semi-solid, 72 Brix)",
        "composition": [
            {"ingredient": "Zanjabeel (Zingiber officinale)", "part": "Rhizome", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Filfil Siyah (Piper nigrum)", "part": "Fruit", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Filfil Daraz (Piper longum)", "part": "Fruit", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Khulanjan (Alpinia galanga)", "part": "Rhizome", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Waj-e-Turki (Acorus calamus)", "part": "Rhizome", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Aaqarqarha (Anacyclus pyrethrum)", "part": "Root", "quantity_g": 20.0, "is_schedule_e1": False}
        ],
        "actions": ["Munaqqi-e-Dimagh (Clear bad humor from the Brain)", "Muqawwi-e-Asab (Nervine Tonic)"],
        "therapeutic_uses": ["Falij (Hemiplegia / Stroke rehabilitation)", "Laqwa (Facial palsy)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use (licked slowly).",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "water_soluble_extractive_min_pct": 60.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 32,
        "name": "Laooq-e-Motadil",
        "urdu_name": "لعوق معتدل",
        "nfum_code": "NFUM-III, 5.6",
        "page_no": 92,
        "form": "Laooq / Linctus (Semi-solid, 76 Brix)",
        "composition": [
            {"ingredient": "Tukhm-e-Khashkhaash (Papaver somniferum)", "part": "Seed", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Koknar (Papaver somniferum capsule)", "part": "Capsule", "quantity_g": 10.0, "is_schedule_e1": True},
            {"ingredient": "Asl-us-Soos (Glycyrrhiza glabra)", "part": "Stolon & Root", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Parsiaoshan (Adiantum capillus-veneris)", "part": "Whole plant", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Zufa-e-Khushk (Hyssopus officinalis)", "part": "Flower", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Munzij (Concoctive / Maturative of phlegm)", "Munaffis-e-Balgham (Expectorant)", "Musakkin (Sedative)"],
        "therapeutic_uses": ["Sual (Bronchitis / Cough)", "Zeequn-Nafas (Asthma)", "Nazla (Catarrh)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 33,
        "name": "Laooq-e-Petha",
        "urdu_name": "لعوق پیٹھہ",
        "nfum_code": "NFUM-III, 5.7",
        "page_no": 95,
        "form": "Laooq (Semi-solid, 76 Brix)",
        "composition": [
            {"ingredient": "Tukhm-e-Khashkhaash (Papaver somniferum)", "part": "Seed", "quantity_g": 30.0, "is_schedule_e1": False},
            {"ingredient": "Maghz-e-Tukhm-e-Petha (Benincasa hispida)", "part": "Kernel", "quantity_g": 30.0, "is_schedule_e1": False},
            {"ingredient": "Maghz-e-Tukhm-e-Kaddu (Cucurbita moschata)", "part": "Kernel", "quantity_g": 30.0, "is_schedule_e1": False},
            {"ingredient": "Samagh-e-Arabi (Acacia nilotica)", "part": "Gum", "quantity_g": 30.0, "is_schedule_e1": False}
        ],
        "actions": ["Musakkin-e-Sual (Antitussive / Demulcent)"],
        "therapeutic_uses": ["Sual-e-Yabis (Dry irritative cough)", "Hemoptysis prevention"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 34,
        "name": "Laooq-e-Zeeq-un-Nafas Balghami",
        "urdu_name": "لعوق ضیق النفس بلغمی",
        "nfum_code": "NFUM-III, 5.11",
        "page_no": 98,
        "form": "Laooq (Semi-solid, 78 Brix)",
        "composition": [
            {"ingredient": "Asl-us-Soos (Glycyrrhiza glabra)", "part": "Stolon & Root", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Irsa / Sausan (Iris ensata)", "part": "Root", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Zufa-e-Khushk (Hyssopus officinalis)", "part": "Flower", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Unnab (Zizyphus jujuba)", "part": "Fruit", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Anjeer Zard (Ficus carica)", "part": "Fruit", "quantity_g": 25.0, "is_schedule_e1": False},
            {"ingredient": "Maghz-e-Chilghoza (Pinus gerardiana)", "part": "Kernel", "quantity_g": 5.0, "is_schedule_e1": False}
        ],
        "actions": ["Munaffis-e-Balgham (Expectorant)", "Musakkin-e-Sual (Antitussive)"],
        "therapeutic_uses": ["Zeequn-Nafas (Phlegmatic Asthma / COPD)", "Sual Muzmin (Chronic Bronchitis)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 1.0, "water_soluble_extractive_min_pct": 84.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 35,
        "name": "Majoon-e-Gheekawar",
        "urdu_name": "معجون گھیگوار",
        "nfum_code": "NFUM-II, 4.8",
        "page_no": 101,
        "form": "Majoon (Semi-solid, 76 Brix)",
        "composition": [
            {"ingredient": "Maghz-e-Gheekawar (Aloe vera fresh pulp)", "part": "Pulp", "quantity_g": 250.0, "is_schedule_e1": False},
            {"ingredient": "Sheer-e-Gao (Cow milk)", "part": "Liquid", "quantity_g": 1000.0, "is_schedule_e1": False},
            {"ingredient": "Qand Safaid (Sugar)", "part": "Crystal", "quantity_g": 1000.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Asab (Nerve Strengthening)", "Mohallil-e-Waram (Anti-inflammatory)"],
        "therapeutic_uses": ["Waj-ul-Qutn (Lumbago / Lower back pain)", "Waj-ul-Mafasil (Rheumatism)", "Waram-e-Mafasil (Arthritis)"],
        "dose": "10 g",
        "mode_of_administration": "For oral use along with milk.",
        "physicochemical_specs": {"total_ash_max_pct": 3.0, "water_soluble_extractive_min_pct": 83.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 36,
        "name": "Majoon-e-Gul",
        "urdu_name": "معجون گل",
        "nfum_code": "NFUM-II, 4.7",
        "page_no": 103,
        "form": "Majoon (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Gul-e-Surkh (Rosa damascena)", "part": "Flower", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Beekh-e-Sausan (Iris ensata)", "part": "Root", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Luk Maghsool (Coccus lacca washed)", "part": "Secretion", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Rewand chini (Rheum emodi)", "part": "Root", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Zafran (Crocus sativus)", "part": "Style & Stigma", "quantity_g": 3.0, "is_schedule_e1": False}
        ],
        "actions": ["Mohallil-e-Waram (Anti-inflammatory)"],
        "therapeutic_uses": ["Warm-e-Kabid (Hepatitis / Hepatic swelling)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "ph_range": "6 - 7"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 37,
        "name": "Majoon-e-Hafiz-ul-Ajsad",
        "urdu_name": "معجون حافظ الاجساد",
        "nfum_code": "NFUM-II, 4.9",
        "page_no": 106,
        "form": "Majoon (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Asaroon (Asarum europaeum)", "part": "Rhizome", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Majeeth (Rubia cordifolia)", "part": "Root", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Beikh kibar (Capparis spinosa)", "part": "Root bark", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Sumbul-ut-Teeb", "part": "Root", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Zafran", "part": "Style & Stigma", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Mohallil-e-Waram (Anti-inflammatory)", "Mudirr-e-Baul (Diuretic)"],
        "therapeutic_uses": ["Su-ul-Qinya (Anemia)", "Istisqa (Dropsy / Ascites / Edema)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "water_soluble_extractive_min_pct": 71.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 38,
        "name": "Majoon-e-Ibn-e-Sarafiyun",
        "urdu_name": "معجون ابن سراف یون",
        "nfum_code": "NFUM-II, 4.11",
        "page_no": 109,
        "form": "Majoon (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Aqrab Sokhta (Heterometrus charred scorpion)", "part": "Entire body", "quantity_g": 15.0, "is_schedule_e1": False},
            {"ingredient": "Hajr-ul-Yahood (Silicate of lime / Jew's stone)", "part": "Powder", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Kaknaj (Physalis alkekengi)", "part": "Fruit", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Kushta Seesa (Calx of lead / Plumbum)", "part": "Ash", "quantity_g": 5.0, "is_schedule_e1": True},
            {"ingredient": "Khakastar-e-Post-e-Baiza-e-Murgh", "part": "Ash of egg shell", "quantity_g": 5.0, "is_schedule_e1": False}
        ],
        "actions": ["Mufattit-e-Hasat (Lithotriptic / Calculus disintegrator)"],
        "therapeutic_uses": ["Hasat-e-Kulya (Renal calculus / Nephrolithiasis)", "Hasat-e-Masana (Vesical / Bladder calculus)"],
        "dose": "5 g",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": True
    },
    {
        "monograph_no": 39,
        "name": "Majoon-e-Kundur",
        "urdu_name": "معجون کندر",
        "nfum_code": "NFUM-V, 5.47",
        "page_no": 112,
        "form": "Majoon (Semi-solid, 74 Brix)",
        "composition": [
            {"ingredient": "Kundur (Boswellia serrata)", "part": "Gum-Resin", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Juft Baloot (Quercus infectoria gall)", "part": "Gall", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Saad Kufi (Cyperus rotundus)", "part": "Rhizome", "quantity_g": 210.0, "is_schedule_e1": False},
            {"ingredient": "Filfil Siyah (Piper nigrum)", "part": "Seed", "quantity_g": 40.0, "is_schedule_e1": False},
            {"ingredient": "Qust Shireen (Saussurea costus)", "part": "Root", "quantity_g": 100.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Asab (Nervine Tonic)", "Habis (Astringent / Retentive)"],
        "therapeutic_uses": [
            "Zof-e-Gurda wa masana (Weakness of Kidney and Urinary Bladder)",
            "Salas-ul Baul (Urinary Incontinence)",
            "Kasrat-e-Baul (Polyuria)",
            "Baul Fil Farash (Nocturnal Enuresis / Bed wetting in children)"
        ],
        "dose": "5 - 10 g twice daily",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "water_soluble_extractive_min_pct": 68.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 40,
        "name": "Majoon-e-Luluvi",
        "urdu_name": "معجون لؤلؤی",
        "nfum_code": "NFUM-II, 4.13",
        "page_no": 115,
        "form": "Majoon (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Marwareed (Mytilus pearl)", "part": "As such", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Marjan (Corallium rubrum)", "part": "As such", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Behman Safaid (Centaurea behen)", "part": "Root", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Mastagi (Pistacia lentiscus)", "part": "Gum", "quantity_g": 3.0, "is_schedule_e1": False}
        ],
        "actions": ["Moharrik-e-Bah (Sex stimulant)", "Muqawwi-e-Bah (Aphrodisiac)", "Muqawwi-e-Asab (Nerve strengthening)"],
        "therapeutic_uses": ["Zof-e-Bah (Sexual debility)", "Zof-e-Asab (Neurasthenia)"],
        "dose": "5 g",
        "mode_of_administration": "For oral use.",
        "physicochemical_specs": {"total_ash_max_pct": 3.0, "alcohol_soluble_extractive_min_pct": 30.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 41,
        "name": "Majoon-e-Mujarrab",
        "urdu_name": "معجون مجرب",
        "nfum_code": "NFUM-II, 4.17",
        "page_no": 118,
        "form": "Majoon (Semi-solid, 78 Brix)",
        "composition": [
            {"ingredient": "Amla (Phyllanthus emblica)", "part": "Fruit", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Badranjboya (Nepeta hindostana)", "part": "Leaf", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Tabasheer Safaid (Bambusa bambos)", "part": "Siliceous concretion", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Aab-e-Zarishk (Berberis juice)", "part": "Fruit Juice", "quantity_g": 450.0, "is_schedule_e1": False}
        ],
        "actions": ["Munaqqi-e-Dimagh (Brain tonic & purifier)"],
        "therapeutic_uses": ["Malikhuliya (Melancholia)", "Miraq (Psychoneurosis / Hypochondriasis)"],
        "dose": "5 - 10 g",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 3.0, "water_soluble_extractive_min_pct": 55.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 42,
        "name": "Majoon-e-Piyaz",
        "urdu_name": "معجون پیاز",
        "nfum_code": "NFUM-I, 5.101",
        "page_no": 121,
        "form": "Majoon (Semi-solid, 75 Brix)",
        "composition": [
            {"ingredient": "Salab Misri (Orchis latifolia)", "part": "Tuber", "quantity_g": 35.0, "is_schedule_e1": False},
            {"ingredient": "Musli Safaid (Chlorophytum arundinaceum)", "part": "Root", "quantity_g": 35.0, "is_schedule_e1": False},
            {"ingredient": "Musli Siyah (Curculigo orchioides)", "part": "Root", "quantity_g": 35.0, "is_schedule_e1": False},
            {"ingredient": "Talmakhana (Hygrophila auriculata)", "part": "Seed", "quantity_g": 35.0, "is_schedule_e1": False},
            {"ingredient": "Aab-e-Piyaz Safaid (White Onion juice)", "part": "Onion juice", "quantity_g": 1500.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Bah (Aphrodisiac)", "Mumsik (Retentive / Semen viscous agent)"],
        "therapeutic_uses": ["Zof-e-Bah (Sexual debility)", "Jiryan (Spermatorrhoea)", "Surat-e-Inzal (Premature ejaculation)"],
        "dose": "5 - 10 g twice daily",
        "mode_of_administration": "For oral use along with milk or water.",
        "physicochemical_specs": {"total_ash_max_pct": 2.0, "water_soluble_extractive_min_pct": 72.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 43,
        "name": "Namak-e-Ajeeb",
        "urdu_name": "نمک عجیب",
        "nfum_code": "NFUM-VI, 7.6",
        "page_no": 124,
        "form": "Safoof / Compound Salt Powder",
        "composition": [
            {"ingredient": "Namak-e-Toam (Common Salt)", "part": "Crystal", "quantity_g": 80.0, "is_schedule_e1": False},
            {"ingredient": "Naushadar (Ammonium chloride)", "part": "Crystal", "quantity_g": 27.5, "is_schedule_e1": False},
            {"ingredient": "Tukhm-e-Karafs (Apium graveolens)", "part": "Fruit", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Nankhwah (Trachyspermum ammi)", "part": "Fruit", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Sirka Naishakar (Cane Vinegar)", "part": "Liquid", "quantity_g": 60.0, "is_schedule_e1": False}
        ],
        "actions": ["Kasir-e-Riyah (Carminative)", "Hazim (Digestive)"],
        "therapeutic_uses": ["Waj-ul-Meda (Stomach ache)", "Qulanj (Colic)", "Waj-ul-Kulya (Renal Colic)"],
        "dose": "1 g",
        "mode_of_administration": "For oral use along with lukewarm water.",
        "physicochemical_specs": {"total_ash_max_pct": 57.0, "ph_range": "8 - 9"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 44,
        "name": "Namak-e-Sulemani",
        "urdu_name": "نمک سلیمانی",
        "nfum_code": "NFUM-VI, 7.7",
        "page_no": 127,
        "form": "Safoof / Compound Salt Powder",
        "composition": [
            {"ingredient": "Namak-e-Toam (Sodium Chloride)", "part": "Crystal", "quantity_g": 545.0, "is_schedule_e1": False},
            {"ingredient": "Naushadar (Ammonium chloride)", "part": "Crystal", "quantity_g": 65.0, "is_schedule_e1": False},
            {"ingredient": "Soda Khurdani (Sodium bicarbonate)", "part": "Powder", "quantity_g": 47.5, "is_schedule_e1": False},
            {"ingredient": "Hilteet Khalis (Ferula foetida)", "part": "Oleo Resin", "quantity_g": 6.0, "is_schedule_e1": False},
            {"ingredient": "Zeera Siyah (Carum carvi)", "part": "Fruit", "quantity_g": 6.0, "is_schedule_e1": False}
        ],
        "actions": ["Hazim (Digestive)", "Mulaiyin (Laxative)", "Kasir-e-Riyah (Carminative)"],
        "therapeutic_uses": ["Zof-e-Hazm (Weak digestion)", "Waj-ul-Meda (Gastric ache)", "Qabz (Constipation)"],
        "dose": "0.5 - 1 g",
        "mode_of_administration": "For oral use along with water after meals.",
        "physicochemical_specs": {"total_ash_max_pct": 72.0, "ph_range": "8 - 9"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 45,
        "name": "Raughan-e-Zarareeh",
        "urdu_name": "روغن ذراریح",
        "nfum_code": "NFUM-V, 7.8",
        "page_no": 130,
        "form": "Raughan / Medicated Oil (External)",
        "composition": [
            {"ingredient": "Nakchhikni (Centipeda minima)", "part": "Aerial part", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Kharateen Musaffa (Earthworm purified)", "part": "Whole", "quantity_g": 20.0, "is_schedule_e1": False},
            {"ingredient": "Baiza Murgh (Hen's egg solid yolk)", "part": "Egg yolk", "quantity_g": 48.0, "is_schedule_e1": False}
        ],
        "actions": ["Sala (Calvities / Hair follicle stimulant)", "Mumbit-e-Shar"],
        "therapeutic_uses": ["Balkhora (Alopecia areata / Circumscribed baldness)"],
        "dose": "Q.S. for external use",
        "mode_of_administration": "For external use on affected scalp / patch.",
        "physicochemical_specs": {"acid_value_max": 16.0, "refractive_index": "1.470 - 1.472"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 46,
        "name": "Raughan-e-Amla",
        "urdu_name": "روغن آملہ",
        "nfum_code": "NFUM-I, 8.1",
        "page_no": 132,
        "form": "Raughan / Medicated Oil (External)",
        "composition": [
            {"ingredient": "Aab-e-Aamla Taza (Fresh Amla juice)", "part": "Fruit juice", "quantity_g": 1000.0, "is_schedule_e1": False},
            {"ingredient": "Barg-e-Murad (Myrtus communis)", "part": "Leaf", "quantity_g": 125.0, "is_schedule_e1": False},
            {"ingredient": "Barg-e-Hina (Lawsonia inermis)", "part": "Leaf", "quantity_g": 125.0, "is_schedule_e1": False},
            {"ingredient": "Raughan-e-Kunjad (Sesame oil)", "part": "Oil", "quantity_g": 3750.0, "is_schedule_e1": False}
        ],
        "actions": ["Muqawwi-e-Shar (Hair Tonic)", "Musawwid-e-Shar (Natural hair blackening)"],
        "therapeutic_uses": ["Intesar-e-Shar (Falling of hair / Telogen effluvium)"],
        "dose": "Q.S. for external use",
        "mode_of_administration": "For external use on scalp.",
        "physicochemical_specs": {"acid_value_max": 3.0, "refractive_index": "1.465 - 1.475"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 47,
        "name": "Safoof Gesu Daraaz",
        "urdu_name": "سفوف گیسو دراز",
        "nfum_code": "NFUM-VI, 7.9",
        "page_no": 134,
        "form": "Safoof (Hair Wash Powder)",
        "composition": [
            {"ingredient": "Halela Siyah", "part": "Unripe fruit", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Balela", "part": "Fruit", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Aamla Khushk", "part": "Fruit", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Shikakai (Acacia concinna)", "part": "Pod", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Tukhm-e-Hulba (Trigonella foenum-graecum)", "part": "Seed", "quantity_g": 100.0, "is_schedule_e1": False},
            {"ingredient": "Post-e-Ritha (Sapindus mukorossi)", "part": "Rind", "quantity_g": 20.0, "is_schedule_e1": False}
        ],
        "actions": ["Mutawwil-e-Shar (Promotes hair growth)", "Mumbitshar (Hair tonic)"],
        "therapeutic_uses": ["Qillat-e-Num-e-Shar (Diminished hair growth)", "Intesar-e-Shar (Thinning of hair)"],
        "dose": "Q.S. for external use only",
        "mode_of_administration": "For external wash on hair.",
        "physicochemical_specs": {"total_ash_max_pct": 5.0, "ph_range": "4 - 5"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 48,
        "name": "Safoof-e-Deedan",
        "urdu_name": "سفوف دیدان",
        "nfum_code": "NFUM-VI, 7.8",
        "page_no": 137,
        "form": "Safoof (Powder)",
        "composition": [
            {"ingredient": "Afsanteen Roomi (Artemisia absinthium)", "part": "Whole plant", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Baobarang (Embelia ribes)", "part": "Fruit", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Turbud Safaid (Operculina turpethum)", "part": "Root", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Gul-e-Surkh (Rosa damascena)", "part": "Flower", "quantity_g": 200.0, "is_schedule_e1": False},
            {"ingredient": "Sat-e-Ajwayin (Thymol extract)", "part": "Fruit extract", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Qatil wa Mukhrij-e-Deedan-e-Ama (Vermicide & Vermifuge)"],
        "therapeutic_uses": ["Deedan-e-Ama (Intestinal worm infestation)"],
        "dose": "6 g (Adult); 3 g (Children)",
        "mode_of_administration": "For oral use along with warm water at bed time.",
        "physicochemical_specs": {"total_ash_max_pct": 6.0, "ph_range": "5 - 6"},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 49,
        "name": "Tiryaq-e-Meda",
        "urdu_name": "تریاق معدہ",
        "nfum_code": "NFUM-III, 5.19",
        "page_no": 140,
        "form": "Safoof / Fast Gastric Powder",
        "composition": [
            {"ingredient": "Naushadar (Ammonium chloride)", "part": "Crystal", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Filfil Siyah (Piper nigrum)", "part": "Fruits", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Namak-e-Khurdani (Sodium chloride)", "part": "Crystal", "quantity_g": 5.0, "is_schedule_e1": False},
            {"ingredient": "Heel Khurd (Elettaria cardamomum)", "part": "Seeds", "quantity_g": 5.0, "is_schedule_e1": False}
        ],
        "actions": ["Hazim (Digestive)", "Kasir-e-Riyah (Carminative)"],
        "therapeutic_uses": ["Zof-e-Hazm (Indigestion / Acute dyspepsia)", "Nafakh-e-Shikam (Flatulence of stomach)"],
        "dose": "0.5 - 1 g",
        "mode_of_administration": "For oral use along with lukewarm water.",
        "physicochemical_specs": {"total_ash_max_pct": 46.0, "water_soluble_extractive_min_pct": 59.0},
        "schedule_e1_warning": False
    },
    {
        "monograph_no": 50,
        "name": "Tiryaq-e-Pechish",
        "urdu_name": "تریاق پیچش",
        "nfum_code": "NFUM-III, 5.20",
        "page_no": 142,
        "form": "Safoof (Gastrointestinal Powder)",
        "composition": [
            {"ingredient": "Post-e-Halela Zard (Roasted in Desi Ghee)", "part": "Pericarp", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Nankhawah (Trachyspermum ammi)", "part": "Fruit", "quantity_g": 10.0, "is_schedule_e1": False},
            {"ingredient": "Zeera Safaid (Cuminum cyminum)", "part": "Fruit", "quantity_g": 10.0, "is_schedule_e1": False}
        ],
        "actions": ["Mufatteh Sudad (Deobstruent)", "Kasir-e-Riyah (Carminative)", "Habis-e-Ishaal (Antidiarrheal)"],
        "therapeutic_uses": ["Nafakh-e-Shikam (Flatulence)", "Zaheer (Pechish / Dysentery / Tenesmus)"],
        "dose": "3 - 5 g",
        "mode_of_administration": "For oral use along with water.",
        "physicochemical_specs": {"total_ash_max_pct": 6.0, "water_soluble_extractive_min_pct": 30.0},
        "schedule_e1_warning": False
    }
]

def get_upi_vol4_compound_by_name(name_or_query: str) -> Optional[Dict[str, Any]]:
    """Looks up an official compound formulation from UPI Part-II Vol-IV."""
    q = name_or_query.strip().lower()
    for item in UPI_PART2_VOL4_MONOGRAPHS:
        if q == item["name"].lower() or q == item["urdu_name"].lower() or q in item["name"].lower():
            return item
    return None

def get_all_upi_vol4_monographs() -> List[Dict[str, Any]]:
    """Returns the full 50 statutory compound formulations from UPI Vol-IV."""
    return list(UPI_PART2_VOL4_MONOGRAPHS)
