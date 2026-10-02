"""
ZAYVORA Health OS™ — Ilaj Hierarchy & Regimental Therapy Engine
Source: Dr. Irfan Ashraf — The Organ-Axis Clinical System (Chapters 13, 14, 15)
Encodes:
- Classical 5-tier Ilaj hierarchy:
  1. Ilaj bil Tadbeer (Regimental Therapy: 16 modalities)
  2. Ilaj bil Ghiza (Dietary Therapy & Therapeutic Fasting / Sawm)
  3. Ilaj bil Nafsiyat (Psychological Medicine: Mukhataba, Tafarruj, Nafsani Dawakhana)
  4. Ilaj bil Dawa (Pharmacotherapy: Nuskha / GMP)
  5. Ilaj bil Yad (Surgical / Procedural Referral)
- The Hierarchy Rule: Drugs never lead without Asbab-e-Sitta foundation
"""
from typing import Dict, Any, List, Optional

TADBEER_MODALITIES = {
    "Riyazat": {
        "name": "Exercise / Physical Exertion",
        "evidence_grade": "A (RCT)",
        "applications": "Metabolic syndrome, insulin resistance, depression, cardiovascular endurance",
        "mizaj_guidelines": {
            "Damvi": "Tolerates high-intensity well; strength training beneficial.",
            "Balghami": "Vigorous cardiovascular exercise non-negotiable — requires sustained thermogenic stimulation.",
            "Safravi": "Moderate-intensity, non-competitive; cooling environments (swimming); avoid heat exhaustion.",
            "Saudavi": "Gentle, warming restorative movement (walking, yoga); NEVER to exhaustion (spares cortisol)."
        }
    },
    "Dalak": {
        "name": "Therapeutic Massage",
        "evidence_grade": "A (meta-analysis)",
        "applications": "Musculoskeletal pain, lymphatic drainage, anxiety, sleep onset improvement",
        "guidelines": "Dalak-e-Sulb (firm) for muscle tone, Dalak-e-Layyin (gentle) for sedative anxiolysis."
    },
    "Hijama": {
        "name": "Cupping Therapy (Wet / Dry)",
        "evidence_grade": "B (systematic review)",
        "applications": "Musculoskeletal pain (45-70% reduction), hypertension, localized inflammatory congestion",
        "contraindications": ["Active local infection", "Anticoagulant therapy", "Pregnancy (abdominal sites)", "Bleeding diathesis", "Severe anemia (Hb <9)"]
    },
    "Hammam": {
        "name": "Hydrotherapy / Medicinal Bath",
        "evidence_grade": "A (RCT)",
        "applications": "Rheumatoid arthritis, fibromyalgia, chronic fatigue, muscle relaxation"
    },
    "Takmeed": {
        "name": "Fomentation / Warm Packs",
        "evidence_grade": "A (RCT)",
        "applications": "Castor oil pack for pelvic circulation in PCOS; warm local compress for joint stiffness"
    },
    "Tareeq": {
        "name": "Diaphoresis (Therapeutic Sweating)",
        "evidence_grade": "B",
        "applications": "Skin channel clearance, metabolic flush, fever resolution"
    },
    "Huqna": {
        "name": "Enema",
        "evidence_grade": "B",
        "applications": "Severe constipation, IBS-C, lower-bowel pre-Tanqiya preparation"
    },
    "Inkebab": {
        "name": "Inhalation / Steam",
        "evidence_grade": "B",
        "applications": "Respiratory congestion, Balgham-Riya axis, allergic rhinitis, sinusitis"
    }
}


def evaluate_ilaj_hierarchy_compliance(
    prescribed_dawa: List[Dict[str, Any]],
    tadbeer_prescriptions: List[str],
    ghiza_parhez_prescribed: bool,
    nafsiyat_addressed: bool
) -> Dict[str, Any]:
    """
    Validates that a prescription respects the classical Unani Ilaj hierarchy:
    Tadbeer -> Ghiza -> Nafsiyat -> Dawa.
    Flags any 'drugs-alone' violation where lifestyle/diet is omitted.
    """
    violations = []
    recommendations = []

    if prescribed_dawa and not ghiza_parhez_prescribed:
        violations.append("VIOLATION OF THE HIERARCHY RULE: Pharmacotherapy (Ilaj bil Dawa) prescribed without dietary medicine (Ilaj bil Ghiza). Food is primary medicine; herbs cannot compensate for uncontrolled diet.")

    if prescribed_dawa and not tadbeer_prescriptions:
        violations.append("HIERARCHY GAP: No Regimental Therapy (Ilaj bil Tadbeer — e.g. Riyazat, Dalak, Takmeed) specified. Physical modalities carry Grade A clinical evidence.")

    if not nafsiyat_addressed:
        recommendations.append(
            "Nafsiyat Consideration: Screen for stress/anxiety (Mukhataba or Tafarruj sensory therapy). "
            "The mind-body axis directly influences humoral balance (Ref: Dr. Irfan Ashraf, 'Ilaj bil Nafsiyat' 2026)."
        )

    compliant = len(violations) == 0

    return {
        "is_hierarchy_compliant": compliant,
        "violations": violations,
        "recommendations": recommendations,
        "nafsiyat_status": "ADDRESSED" if nafsiyat_addressed else "NEEDS_EVALUATION",
        "clinical_law": "Drugs never lead. A practitioner who prescribes herbs without first addressing Asbab-e-Sitta has handed the patient the weakest medicine available and left the strongest untouched."
    }

