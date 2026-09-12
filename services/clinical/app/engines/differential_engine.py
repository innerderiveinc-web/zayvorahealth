"""
ZAYVORA Integrative Differential Considerations & ICD-11 Diagnostic Cross-Mapping Engine.
Maps classical Unani Amraz (diseases) to ICD-11 / SNOMED-CT codes and highlights biomedical Red Flags.
"""
from __future__ import annotations

from typing import Any

UNANI_AMRAZ_ICD11_REGISTRY: list[dict[str, Any]] = [
    {
        "unani_disease": "Niqris (Gout)",
        "urdu_name": "نقرس",
        "icd11_code": "FA25",
        "icd11_title": "Gout and certain crystal arthropathies",
        "snomed_concept_id": "90560007",
        "organ_axis": "mafasil",
        "classical_asbab": "Stasis of morbid Safra and Balgham in peripheral joints, impaired excretion",
        "usool_e_ilaj": "Tanqiya of morbid matter via Mus-hil-e-Balgham/Safra, Taqwiyat-e-Meda and Kulyah",
        "keywords": ["gout", "niqris", "uric acid", "big toe", "podagra", "joint pain", "joint swelling"],
        "red_flags": [
            "Hot, erythematous swollen joint with systemic fever (suspect septic arthritis until proven otherwise)",
            "Renal colic or anuria indicating uric acid nephrolithiasis",
            "Severe tophi ulceration with secondary purulent infection",
        ],
    },
    {
        "unani_disease": "Waja-ul-Mafasil (Osteoarthritis / Arthralgia)",
        "urdu_name": "وجع المفاصل",
        "icd11_code": "FA00",
        "icd11_title": "Osteoarthritis of hip or knee",
        "snomed_concept_id": "396275006",
        "organ_axis": "mafasil",
        "classical_asbab": "Accumulation of cold morbid phlegm (Balgham Kham) or melancholic humors (Sauda)",
        "usool_e_ilaj": "Muhallilat (resolvents), Dalak (medical massage) with Roghan, Taqwiyat-e-Mafasil",
        "keywords": ["arthritis", "waja", "knee pain", "joint stiffness", "crepitus", "back pain", "mafasil"],
        "red_flags": [
            "Morning stiffness lasting > 1 hour (suggesting inflammatory arthritis / Rheumatoid)",
            "Systemic B-symptoms (unexplained weight loss, night sweats, nocturnal bony ache)",
            "Acute monoarthritis with inability to bear weight",
        ],
    },
    {
        "unani_disease": "Falij wa Laqwa (Stroke / Hemiplegia & Facial Palsy)",
        "urdu_name": "فالج و لقوہ",
        "icd11_code": "8B20",
        "icd11_title": "Stroke not known if ischaemic or haemorrhagic",
        "snomed_concept_id": "230690007",
        "organ_axis": "dimagh-aasab",
        "classical_asbab": "Obstruction (Suddah) of motor nerves by thick phlegm (Balgham Ghaleez)",
        "usool_e_ilaj": "Tanqiya-e-Dimagh with Ustukhuddus and Ayarij, followed by Muqawwiyat-e-Aasab",
        "keywords": ["stroke", "paralysis", "facial palsy", "laqwa", "falij", "weakness on one side", "speech difficulty"],
        "red_flags": [
            "EMERGENCY: Sudden onset focal neurological deficit within 4.5 hours — immediate hospital stroke unit transfer required",
            "Loss of consciousness, pupillary asymmetry, or respiratory depression",
            "Severe sudden 'thunderclap' headache with neck stiffness",
        ],
    },
    {
        "unani_disease": "Su-e-Hazm wa Nafakh (Functional Dyspepsia & Meteorism)",
        "urdu_name": "سوء ہضم و نفخ",
        "icd11_code": "MD90",
        "icd11_title": "Dyspepsia",
        "snomed_concept_id": "16331000",
        "organ_axis": "meda-amaa",
        "classical_asbab": "Su-e-Mizaj Meda (cold/moist weakness of gastric faculty or excessive burning Safra)",
        "usool_e_ilaj": "Taqwiyat-e-Meda with Jawarish Kamuni / Zanjabeel, dietary modification (Tadbeer-e-Ghiza)",
        "keywords": ["dyspepsia", "indigestion", "su-e-hazm", "gas", "bloating", "flatulence", "nausea", "stomach fullness"],
        "red_flags": [
            "Progressive dysphagia or odynophagia",
            "Unintentional significant weight loss or anorexia in patient > 55 years",
            "Melena, hematemesis, or unexplained iron deficiency anemia",
            "Persistent vomiting",
        ],
    },
    {
        "unani_disease": "Shafiqah (Migraine / Hemicrania)",
        "urdu_name": "شقیقہ",
        "icd11_code": "8A80",
        "icd11_title": "Migraine",
        "snomed_concept_id": "37796009",
        "organ_axis": "dimagh-aasab",
        "classical_asbab": "Vapors of yellow bile (Bukharaat-e-Safrawi) rising to one side of the cerebrum",
        "usool_e_ilaj": "Taskeen of Safra, Tanqiya with Itrifal Ustukhuddus, Natool with calming decoctions",
        "keywords": ["migraine", "shafiqah", "one-sided headache", "throbbing head", "photophobia", "aura"],
        "red_flags": [
            "New onset headache in patient > 50 years or with history of malignancy",
            "Headache accompanied by fever, neck stiffness, and confusion",
            "Sudden maximal intensity headache ('thunderclap')",
        ],
    },
    {
        "unani_disease": "Ziq-un-Nafs (Bronchial Asthma / Dyspnea)",
        "urdu_name": "ضیق النفس",
        "icd11_code": "CA23",
        "icd11_title": "Asthma",
        "snomed_concept_id": "195967001",
        "organ_axis": "riya-sadr",
        "classical_asbab": "Spasm or obstruction of bronchial conduits by tenacious phlegm (Balgham-e-Lazuq)",
        "usool_e_ilaj": "Talteef and Tanqiya with Munaffis-e-Balgham (Asal-us-Soos, Zoofa, Joshanda)",
        "keywords": ["asthma", "wheezing", "shortness of breath", "ziq-un-nafs", "chest tightness", "cough"],
        "red_flags": [
            "EMERGENCY: Silent chest, central cyanosis, exhaustion, or inability to complete sentences",
            "Peak expiratory flow rate < 33% of predicted/personal best",
            "No relief from rescue bronchodilators",
        ],
    },
]


def match_differential_considerations(
    chief_complaint: str,
    organ_axis: str | None = None,
    dominant_mizaj: str | None = None,
) -> list[dict[str, Any]]:
    """Evaluates symptoms, organ axis, and Mizaj to generate ranked differential considerations."""
    complaint_lower = chief_complaint.lower()
    matched = []

    for entry in UNANI_AMRAZ_ICD11_REGISTRY:
        score = 0
        # Keyword matches
        for kw in entry["keywords"]:
            if kw in complaint_lower:
                score += 3

        # Organ axis alignment
        if organ_axis and entry["organ_axis"] == organ_axis:
            score += 2

        if score > 0:
            matched.append({
                "score": score,
                "unani_disease": entry["unani_disease"],
                "urdu_name": entry["urdu_name"],
                "icd11_code": entry["icd11_code"],
                "icd11_title": entry["icd11_title"],
                "snomed_concept_id": entry["snomed_concept_id"],
                "organ_axis": entry["organ_axis"],
                "classical_asbab": entry["classical_asbab"],
                "usool_e_ilaj": entry["usool_e_ilaj"],
                "red_flags": entry["red_flags"],
            })

    # Sort by match relevance
    return sorted(matched, key=lambda x: x["score"], reverse=True)
