"""
ZAYVORA Health OS™ — Master Organ-Axis Diagnostic Matrix
Source: ZAYVORA Master Clinical System (Dr. Irfan Ashraf)
Section 1: 12 Canonical Organ Axes, Governing Powers, Disease Mapping, and Scoring System.
"""
from typing import Dict, Any, List, Tuple, Optional

ORGAN_AXES_CATALOG: Dict[str, Dict[str, Any]] = {
    "Qalb-Uroq": {
        "id": "Qalb-Uroq",
        "arabic_name": "قلب و عروق",
        "body_system": "Cardio-Vascular",
        "governing_power": "Quwwat-e-Haiwaniyah (Vital Faculty)",
        "key_diseases": ["Hypertension", "Ischaemic Heart Disease (IHD)", "Palpitations", "Arrhythmia"],
        "primary_products": ["HyperCalm", "CardioGuard", "LipidClear"],
        "regulatory_track": "AYUSH preferred",
        "description": "Cardiovascular and vascular network governing circulation, blood pressure, and arterial elasticity."
    },
    "Jigar-Banas": {
        "id": "Jigar-Banas",
        "arabic_name": "جگر و بنقراس",
        "body_system": "Hepato-Metabolic",
        "governing_power": "Quwwat-e-Tabi'iyah (Natural/Metabolic Faculty)",
        "key_diseases": ["Diabetes Type 2", "NAFLD", "Fatty Liver", "Metabolic Syndrome", "Insulin Resistance"],
        "primary_products": ["DiabEase", "HepaClear", "LipidClear", "MetaboBurn-M"],
        "regulatory_track": "FSSAI/AYUSH",
        "description": "Hepatic and pancreatic metabolic axis regulating glucose homeostasis, glycogen storage, and intermediate metabolism."
    },
    "Dimagh-Qalb": {
        "id": "Dimagh-Qalb",
        "arabic_name": "دماغ و قلب",
        "body_system": "Neuro-Cardiac",
        "governing_power": "Quwwat-e-Nafsaniyah wa Haiwaniyah (Neuro-Vital Faculty)",
        "key_diseases": ["Anxiety", "Depression", "Insomnia", "Stress", "Burnout", "Cardioneurosis"],
        "primary_products": ["MindBalance", "Sleep+Stress"],
        "regulatory_track": "FSSAI/AYUSH",
        "description": "Central nervous system, HPA axis, and cardiac autonomic interface governing emotional and sleep regulation."
    },
    "Riya-Sadr": {
        "id": "Riya-Sadr",
        "arabic_name": "ریہ و صدر",
        "body_system": "Respiratory",
        "governing_power": "Quwwat-e-Tanaffusiyah (Respiratory Faculty)",
        "key_diseases": ["Asthma", "COPD", "Allergic Rhinitis", "Bronchitis", "Mucosal Congestion"],
        "primary_products": ["LungEase", "Immunity"],
        "regulatory_track": "FSSAI",
        "description": "Bronchopulmonary network and thoracic mucosal barrier providing oxygenation and phlegm clearance."
    },
    "Mafasil-Dam": {
        "id": "Mafasil-Dam",
        "arabic_name": "مفاصل و دم",
        "body_system": "Musculo-Skeletal",
        "governing_power": "Quwwat-e-Masika wa Muharrika (Holding & Locomotor Faculty)",
        "key_diseases": ["Osteoarthritis (OA)", "Rheumatoid Arthritis (RA)", "Gout", "Joint Inflammation"],
        "primary_products": ["JointFree"],
        "regulatory_track": "FSSAI",
        "description": "Joints, cartilage matrix, synovial fluid, and circulating inflammatory mediators."
    },
    "Khusyatain-Dam": {
        "id": "Khusyatain-Dam",
        "arabic_name": "خصیتین و دم",
        "body_system": "Male Reproductive",
        "governing_power": "Quwwat-e-Tawalludiyah (Generative Faculty)",
        "key_diseases": ["Erectile Dysfunction (ED)", "Oligospermia", "Low Testosterone", "Male Infertility", "DNA Fragmentation"],
        "primary_products": ["VigorX-ED", "TestoVital Classic", "Fertility PRO", "FertiMax-M"],
        "regulatory_track": "AYUSH/FSSAI",
        "description": "Testicular Leydig and Sertoli cell network, spermatogenesis, and androgenic hormone cascade."
    },
    "Reham-Mabaysim": {
        "id": "Reham-Mabaysim",
        "arabic_name": "رحم و مبایض",
        "body_system": "Female Reproductive",
        "governing_power": "Quwwat-e-Tanasuliyya Niswaniyah (Female Generative Faculty)",
        "key_diseases": ["PCOS", "Leucorrhoea", "Menstrual Disorders (Dysmenorrhoea/Menorrhagia)", "Menopause"],
        "primary_products": ["CycloCare-PCOS", "FertiliWomen", "LeucoClear", "MenoPease"],
        "regulatory_track": "FSSAI/AYUSH",
        "description": "Uterine-ovarian axis governing folliculogenesis, endometrial integrity, and menstrual cycle synchrony."
    },
    "Meda-Amaa": {
        "id": "Meda-Amaa",
        "arabic_name": "معدہ و امعاء",
        "body_system": "GI System",
        "governing_power": "Quwwat-e-Hazima wa Dafia (Digestive & Expulsive Faculty)",
        "key_diseases": ["IBS", "Chronic Constipation", "Bloating", "Gut Dysbiosis", "Leaky Gut", "SIBO"],
        "primary_products": ["GutEase-IBS", "HepaClear"],
        "regulatory_track": "FSSAI",
        "description": "Gastrointestinal tract, enteric nervous system, mucosal barrier, and gut microbiome."
    },
    "Ghudad-Hazm": {
        "id": "Ghudad-Hazm",
        "arabic_name": "غدد و ہضم",
        "body_system": "Endocrine / Thyroid",
        "governing_power": "Quwwat-e-Mughayyira (Transformative Metabolic Faculty)",
        "key_diseases": ["Hypothyroidism", "Subclinical Hypothyroidism", "Low T3 Syndrome", "Metabolic Dysregulation"],
        "primary_products": ["ThyroMet-W", "MindBalance"],
        "regulatory_track": "FSSAI",
        "description": "Thyroid gland and hepatic deiodinase enzymatic axis regulating cellular metabolic rate."
    },
    "Ghudda-Mithana": {
        "id": "Ghudda-Mithana",
        "arabic_name": "غدہ و مثانہ",
        "body_system": "Prostate-Urinary",
        "governing_power": "Quwwat-e-Dafia (Urinary Excretory Faculty)",
        "key_diseases": ["BPH", "LUTS (Lower Urinary Tract Symptoms)", "Urinary Stones (Hisat-e-Kulya)", "UTI"],
        "primary_products": ["ProstaGuard", "UroClear"],
        "regulatory_track": "FSSAI",
        "description": "Prostate gland, renal pelvis, ureters, and urinary bladder."
    },
    "Shaar-Jigar": {
        "id": "Shaar-Jigar",
        "arabic_name": "شعر و جگر",
        "body_system": "Hair-Systemic",
        "governing_power": "Quwwat-e-Ghazia (Nutritive Hair Follicle Faculty)",
        "key_diseases": ["Androgenic Alopecia (Male/Female)", "Telogen Effluvium", "DHT Excess", "Stress Hair Loss"],
        "primary_products": ["HairRoot-X"],
        "regulatory_track": "FSSAI",
        "description": "Dermal hair follicles, scalp microcirculation, and hepatic nutrient-androgen regulatory balance."
    },
    "Tabiyat": {
        "id": "Tabiyat",
        "arabic_name": "طبیعت و مناعت",
        "body_system": "Immune System",
        "governing_power": "Quwwat-e-Mudabbira-e-Badan (Innate Healing Intelligence)",
        "key_diseases": ["Recurrent Infections", "Post-Viral Fatigue", "Immunodeficiency", "Inflammatory Diathesis"],
        "primary_products": ["Immunity"],
        "regulatory_track": "FSSAI",
        "description": "Innate and adaptive immune network, macrophage phagocytosis, T-cell regulation, and biological resilience."
    }
}

def score_organ_axes(scores: Dict[str, int]) -> Dict[str, Any]:
    """
    Evaluates 12-axis symptom scores (0-5 scale per axis) and applies clinical rules:
    0 = No symptoms in this axis
    1-2 = Mild/occasional symptoms
    3 = Moderate symptoms present regularly
    4 = Significant impairment in this axis
    5 = Severe / primary complaint in this axis

    CLINICAL RULE:
    - Highest score = PRIMARY AXIS (Treated in Phase 1)
    - Second highest score (>= 3) = SECONDARY AXIS (Added in Phase 2)
    - Phase 3 Maintenance covers both axes.
    """
    valid_scores = {k: max(0, min(5, scores.get(k, 0))) for k in ORGAN_AXES_CATALOG.keys()}
    sorted_axes = sorted(valid_scores.items(), key=lambda x: x[1], reverse=True)
    
    primary_axis = sorted_axes[0][0] if sorted_axes[0][1] > 0 else None
    primary_score = sorted_axes[0][1] if primary_axis else 0
    
    secondary_axis = None
    secondary_score = 0
    if len(sorted_axes) > 1 and sorted_axes[1][1] >= 3:
        secondary_axis = sorted_axes[1][0]
        secondary_score = sorted_axes[1][1]

    recommendations = []
    if primary_axis:
        rec_data = ORGAN_AXES_CATALOG[primary_axis]
        recommendations.append({
            "role": "PRIMARY",
            "axis": primary_axis,
            "score": primary_score,
            "products": rec_data["primary_products"],
            "phase": "Phase 1 Reset / Foundation"
        })
    if secondary_axis:
        sec_data = ORGAN_AXES_CATALOG[secondary_axis]
        recommendations.append({
            "role": "SECONDARY",
            "axis": secondary_axis,
            "score": secondary_score,
            "products": sec_data["primary_products"],
            "phase": "Phase 2 Target Addition"
        })

    return {
        "scores": valid_scores,
        "primary_axis": primary_axis,
        "primary_score": primary_score,
        "secondary_axis": secondary_axis,
        "secondary_score": secondary_score,
        "clinical_strategy": "Treat Primary Axis first in Phase 1 (30 days); introduce Secondary Axis in Phase 2 (60-90 days); maintain both in Phase 3.",
        "recommendations": recommendations
    }

# Convenience aliases and accessor functions
MASTER_ORGAN_AXES = ORGAN_AXES_CATALOG

def get_all_axes() -> List[Dict[str, Any]]:
    """Returns list of all 12 organ axes."""
    return list(ORGAN_AXES_CATALOG.values())

def get_axis_by_id(axis_id: str) -> Optional[Dict[str, Any]]:
    """Returns organ axis by ID or key."""
    for k, v in ORGAN_AXES_CATALOG.items():
        if k.lower() == axis_id.lower() or v.get("id", "").lower() == axis_id.lower():
            return v
    return None
