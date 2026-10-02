"""
ZAYVORA Health OS™ — CP-AFUM Academic Curriculum Engine
Source: Dr. Irfan Ashraf — CP-AFUM Complete Course Notes (24 Weeks, 96 Lectures, 6 Modules)
"""
from typing import Dict, Any, List

CP_AFUM_PROGRAMME_SPEC = {
    "title": "Certified Practitioner in Axis-Based Functional Unani Medicine (CP-AFUM)",
    "institution": "ZAYVORA Institute of Axis-Based Functional Unani Medicine",
    "academic_director": "Hakeem Dr. Irfan Ashraf, BUMS (Aligarh Muslim University, Batch 2002, Passed 2007), Integrative Medicine Practitioner",
    "duration_weeks": 24,
    "total_lectures": 96,
    "modules_count": 6,
    "semesters_count": 3,
    "supervised_cases_required": 20,
    "pass_requirement_overall_pct": 70.0,
    "case_analysis_min_pass_pct": 60.0,
    "viva_mandatory": True,
    "minimum_attendance_pct": 80.0
}

SEMESTERS = [
    {
        "semester": 1,
        "name": "Foundations",
        "weeks": "Weeks 1–6",
        "lectures_count": 36,
        "modules": [
            {
                "module_number": 1,
                "title": "Mizaj & Temperament Science",
                "weeks": "Weeks 1–2",
                "lectures": "L01–L12",
                "key_focus": "Four humours (Dam, Balgham, Safra, Sauda), 4 primary qualities (Hot, Cold, Wet, Dry), 8-domain Mizaj Assessment Form, Dose Adjustment Matrix, Thermal herb pairing."
            },
            {
                "module_number": 2,
                "title": "Organ-Axis Systems Biology",
                "weeks": "Weeks 3–4",
                "lectures": "L13–L24",
                "key_focus": "6 Organ Axes (Gut-Liver, Liver-Pancreas, Gut-Ovarian, Liver-Testicular, Thyroid-Neuro, HPA), cascade failures, 5 Axis Priority Rules."
            },
            {
                "module_number": 3,
                "title": "Clinical Diagnostics & Lab Integration",
                "weeks": "Weeks 5–6",
                "lectures": "L25–L36",
                "key_focus": "Functional vs standard lab interpretation, 5 Non-Negotiable Lab Trigger Rules, HOMA-IR, TG/HDL, Semen analysis WHO 6th ed vs ZAYVORA optimal."
            }
        ]
    },
    {
        "semester": 2,
        "name": "Therapeutic Architecture",
        "weeks": "Weeks 7–16",
        "lectures_count": 40,
        "modules": [
            {
                "module_number": 4,
                "title": "Phase-Based Therapeutic Model",
                "weeks": "Weeks 7–8",
                "lectures": "L37–L44",
                "key_focus": "3-Phase Model (Stabilization, Axis Correction, Consolidation), 8 Complete Phase Trigger Rules (R1–R8), Phase 1/2/3 exit criteria."
            },
            {
                "module_number": 5,
                "title": "Therapeutic Formulation Science",
                "weeks": "Weeks 9–10",
                "lectures": "L45–L52",
                "key_focus": "Classical pharmacodynamics (Kaifiyat & Khawas), 4 key standardization targets (Withanolides >=5%, Silymarin 70-80%, Berberine >=95%, Valerenic acid 0.8%), 6 hero products, herb-drug interactions."
            }
        ]
    },
    {
        "semester": 3,
        "name": "Clinical Practicum & Case Mastery",
        "weeks": "Weeks 17–24",
        "lectures_count": 20,
        "modules": [
            {
                "module_number": 6,
                "title": "Clinical Practicum & Case Mastery",
                "weeks": "Weeks 11–24",
                "lectures": "L53–L90+",
                "key_focus": "20 Supervised Clinical Cases, 7 mandatory case elements, 8 red flag referral criteria, Z-ACIP platform EMR use, research documentation, final clinical viva."
            }
        ]
    }
]

ASSESSMENT_FRAMEWORK = {
    "Part A (MCQ)": {"weight_pct": 30, "format": "30 multiple-choice questions (Mizaj, Axis, Labs, Phase, Formulation)"},
    "Part B (Short Answer)": {"weight_pct": 20, "format": "10 structured questions on phase trigger logic and dose modification"},
    "Part C (Case Analysis)": {"weight_pct": 30, "format": "2 complex clinical cases with full ZAYVORA analysis (Mandatory 60% separate pass)"},
    "Part D (Viva Voce)": {"weight_pct": 20, "format": "20-minute oral examination with Dr. Irfan Ashraf (Mandatory clearance — cannot be waived)"}
}


def get_curriculum_summary() -> Dict[str, Any]:
    """Returns complete CP-AFUM curriculum architecture."""
    return {
        "spec": CP_AFUM_PROGRAMME_SPEC,
        "semesters": SEMESTERS,
        "assessment": ASSESSMENT_FRAMEWORK
    }
