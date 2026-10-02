"""
ZAYVORA Health OS™ — CP-AFUM Practicum Registry Engine
Source: Dr. Irfan Ashraf — CP-AFUM Course Notes Module 6, Table 6.1 & Table 6.2
Tracks:
- 20 Required Supervised Cases across 5 specific clinical tracks
- Verification of all 7 Mandatory Case Documentation Elements
- Strict Rejection Gates (Missing Elements 1, 2, or 4 cause outright rejection)
"""
from typing import Dict, Any, List

REQUIRED_CASES_DISTRIBUTION = {
    "male_infertility": {"target": 5, "name": "Male Infertility", "hero_product": "ManiVital Pro™", "key_marker": "Semen Analysis at 12 weeks"},
    "pcos_female_fertility": {"target": 5, "name": "PCOS / Female Fertility", "hero_product": "OvaSync™", "key_marker": "AMH trend + LH:FSH ratio at 8 weeks"},
    "t2dm_metabolic": {"target": 4, "name": "Type 2 Diabetes / Metabolic", "hero_product": "MetaboCore Elite™", "key_marker": "HbA1c at 12 weeks (target ≥0.5% reduction)"},
    "thyroid": {"target": 3, "name": "Thyroid (Hypo + Subclinical)", "hero_product": "ThyroMet Axis™", "key_marker": "TSH + Free T3 at 8 weeks"},
    "anxiety_stress_ibs": {"target": 3, "name": "Anxiety / Stress / IBS", "hero_product": "NeuroCalmX™", "key_marker": "Cortisol AM/PM at 8 weeks + PRO score"}
}

MANDATORY_DOCUMENTATION_ELEMENTS = [
    {"num": 1, "name": "Mizaj Assessment", "required": True, "fatal": True, "field": "mizaj_assessment", "desc": "Dominant Mizaj + scoring rationale from 8 domains + Mixed Mizaj note."},
    {"num": 2, "name": "Axis Identification", "required": True, "fatal": True, "field": "axis_identification", "desc": "Primary axis + secondary axis with supporting lab values and dates."},
    {"num": 3, "name": "Severity Classification", "required": True, "fatal": False, "deduction": 5, "field": "severity_classification", "desc": "Mild/Moderate/Severe with specific clinical and lab criteria."},
    {"num": 4, "name": "Phase Protocol", "required": True, "fatal": True, "field": "phase_protocol", "desc": "Phase 1 (product+duration+rationale) + Phase 2 (hero+dose) + Phase 3 (taper)."},
    {"num": 5, "name": "Product Stack", "required": True, "fatal": False, "deduction": 10, "field": "product_stack", "desc": "All products per phase with specific Mizaj-adjusted doses."},
    {"num": 6, "name": "Lab Monitoring Plan", "required": True, "fatal": False, "deduction": 5, "field": "lab_monitoring_plan", "desc": "Biomarkers monitored at Week 4, 8, 12 with target values."},
    {"num": 7, "name": "Predicted Outcome", "required": True, "fatal": False, "deduction": 5, "field": "predicted_outcome", "desc": "Expected 12-week clinical and lab outcomes with mechanistic justification."}
]


def validate_practicum_case(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates a submitted clinical case against the 7 mandatory documentation elements.
    Outright rejects if Element 1, 2, or 4 is missing.
    Calculates score out of 100 based on completeness.
    """
    score = 100
    missing_fatal = []
    deductions = []

    for elem in MANDATORY_DOCUMENTATION_ELEMENTS:
        field_val = case_data.get(elem["field"])
        is_empty = field_val is None or (isinstance(field_val, (str, list, dict)) and len(field_val) == 0)

        if is_empty:
            if elem["fatal"]:
                missing_fatal.append(f"Element {elem['num']}: {elem['name']} is MISSING. (FATAL: Case Rejected)")
            else:
                score -= elem.get("deduction", 5)
                deductions.append(f"Missing Element {elem['num']}: {elem['name']} (-{elem.get('deduction', 5)} marks)")

    if missing_fatal:
        return {
            "status": "REJECTED",
            "accepted": False,
            "score": 0,
            "fatal_errors": missing_fatal,
            "deductions": deductions,
            "reason": "Cases missing Element 1 (Mizaj), Element 2 (Axis), or Element 4 (Phase Protocol) are rejected outright per Section 6.5 standards."
        }

    return {
        "status": "ACCEPTED",
        "accepted": True,
        "score": max(score, 0),
        "fatal_errors": [],
        "deductions": deductions,
        "quality_tier": "RESEARCH_GRADE" if score >= 90 else "COMPLIANT" if score >= 70 else "NEEDS_REVISION"
    }


def evaluate_practicum_portfolio(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates a candidate's 20-case practicum portfolio against the track distribution requirements.
    """
    counts = {track: 0 for track in REQUIRED_CASES_DISTRIBUTION}
    valid_cases_count = 0
    total_score = 0

    for c in cases:
        val = validate_practicum_case(c)
        if val["accepted"]:
            valid_cases_count += 1
            total_score += val["score"]
            track = c.get("clinical_track", "").lower().replace("-", "_").replace(" ", "_")
            for req_key in counts:
                if req_key in track or track in req_key:
                    counts[req_key] += 1
                    break

    deficit = {}
    is_distribution_met = True
    for req_key, spec in REQUIRED_CASES_DISTRIBUTION.items():
        if counts[req_key] < spec["target"]:
            is_distribution_met = False
            deficit[spec["name"]] = spec["target"] - counts[req_key]

    is_portfolio_complete = (valid_cases_count >= 20 and is_distribution_met)
    avg_score = round(total_score / valid_cases_count, 1) if valid_cases_count > 0 else 0

    return {
        "total_submitted": len(cases),
        "valid_accepted_cases": valid_cases_count,
        "required_cases": 20,
        "portfolio_complete": is_portfolio_complete,
        "track_distribution_met": is_distribution_met,
        "current_counts": counts,
        "track_deficits": deficit,
        "average_case_score": avg_score,
        "ready_for_final_viva": is_portfolio_complete and avg_score >= 70.0
    }
