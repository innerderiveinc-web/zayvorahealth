"""
Controlled vocabulary seeded at service startup. Taken verbatim from
ZAYVORA Clinical Architecture Specification v4.0 §9 (Organ-Axis) and §8/classical Unani (Mizaj
temperaments) — not invented here, not sourced from an AI guess. If this
list is ever wrong, the fix is to correct it against the classical source
the framework is built on, not to silently adjust it in code.
"""

ORGAN_AXES = [
    {"code": "qalb-uroq", "name": "Qalb–Uroq", "translation": "Heart–Vessels"},
    {"code": "jigar-banas", "name": "Jigar–Banas", "translation": "Liver–Biliary"},
    {"code": "dimagh-aasab", "name": "Dimagh–Aasab", "translation": "Brain–Nerves"},
    {"code": "riya-sadr", "name": "Riya–Sadr", "translation": "Lungs–Chest"},
    {"code": "mafasil", "name": "Mafasil", "translation": "Joints"},
    {"code": "khusyatain", "name": "Khusyatain", "translation": "Testes/Male reproductive"},
    {"code": "reham-mabaysim", "name": "Reham–Mabaysim", "translation": "Uterus–Female reproductive"},
    {"code": "meda-amaa", "name": "Meda–Amaa", "translation": "Stomach–Intestines"},
    {"code": "ghudad-hazm", "name": "Ghudad–Hazm", "translation": "Digestive Glands"},
    {"code": "ghudda-mithana", "name": "Ghudda–Mithana", "translation": "Thyroid–Metabolism"},
    {"code": "shaar-jigar", "name": "Shaar–Jigar", "translation": "Skin/Hair–Liver axis"},
    {"code": "tabiyat", "name": "Tabiyat", "translation": "Constitution/Vital force"},
]

MIZAJ_TEMPERAMENTS = [
    {"temperament": "Damwi", "translation": "Sanguine", "quality": "Hot & Wet"},
    {"temperament": "Safrawi", "translation": "Choleric", "quality": "Hot & Dry"},
    {"temperament": "Saudawi", "translation": "Melancholic", "quality": "Cold & Dry"},
    {"temperament": "Balghami", "translation": "Phlegmatic", "quality": "Cold & Wet"},
]

EVIDENCE_LEVELS = {
    "E0": "Traditional/Classical",
    "E1": "Preclinical",
    "E2": "Observational Human",
    "E3": "Controlled Clinical",
    "E4": "Systematic Review/Meta-analysis",
    "E5": "ZAYVORA Clinical Evidence",
    "E6": "Independently Replicated Evidence",
}

KNOWLEDGE_WORLDS = {
    "A": "Classical Unani",
    "B": "Biomedical",
    "C": "Clinical (ZAYVORA governed outcomes)",
    "D": "Proprietary (ZAYVORA frameworks/algorithms)",
}
