"""
ZAYVORA Health OS™ — CP-AFUM Certification Progression Engine
Source: Dr. Irfan Ashraf — CP-AFUM Course Notes Table C.1
Manages 3 Certification Tiers:
- Level 1: Certified Axis Practitioner (CP-AFUM)
- Level 2: Advanced Clinical Fellow
- Level 3: ZAYVORA Faculty
"""
from typing import Dict, Any, List

CERTIFICATION_LEVELS = {
    "L1": {
        "level": 1,
        "code": "CP-AFUM",
        "title": "Certified Axis Practitioner",
        "requirements": [
            "Complete all 3 semesters (24 weeks)",
            "Minimum 80% attendance across all modules",
            "Submit 20 supervised case studies (all 7 elements)",
            "Pass written examination (70% minimum overall)",
            "Pass clinical viva with Dr. Irfan Ashraf (mandatory clearance)",
            "Pass lab interpretation test clearance"
        ],
        "rights": [
            "Practice under ZAYVORA Clinical Protocols",
            "Use Z-ACIP platform at clinic level",
            "Order ZAYVORA clinical-grade products",
            "Display CP-AFUM designation",
            "List in ZAYVORA Affiliate Clinic Network",
            "Contribute cases to outcome registry"
        ]
    },
    "L2": {
        "level": 2,
        "code": "AFUF-FELLOW",
        "title": "Advanced Clinical Fellow",
        "requirements": [
            "Hold valid Level 1 CP-AFUM certification",
            "Document minimum 50 ZAYVORA patient cases",
            "Complete ZAYVORA Faculty Micro-Training (8 weeks)",
            "Submit 1 clinical case report for publication consideration",
            "Pass Level 2 advanced viva assessment",
            "Founder endorsement (Dr. Irfan Ashraf approval required)"
        ],
        "rights": [
            "Supervise CP-AFUM Practicum students",
            "Conduct ZAYVORA affiliate clinic training",
            "Co-author research publications",
            "Access advanced Z-ACIP analytics",
            "Higher-tier SaaS access",
            "Eligible for ZAYVORA Annual Conference speaker"
        ]
    },
    "L3": {
        "level": 3,
        "code": "ZAYVORA-FACULTY",
        "title": "ZAYVORA Faculty",
        "requirements": [
            "Hold valid Level 2 Advanced Fellow certification",
            "Minimum 1 co-authored peer-reviewed publication",
            "Demonstrate teaching excellence (formal evaluation)",
            "Formal appointment and approval by Founder",
            "Agree to ZAYVORA Faculty Code of Practice",
            "Annual faculty performance review"
        ],
        "rights": [
            "Lead CP-AFUM module delivery",
            "Conduct final viva examinations",
            "Represent ZAYVORA at conferences",
            "Full research platform access",
            "Advisory board membership",
            "Revenue share on Institute programmes delivered"
        ]
    }
}


def evaluate_practitioner_tier(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates practitioner achievements and returns their highest certified tier
    and remaining requirements for next tier progression.
    """
    semesters_done = profile.get("semesters_completed", 0)
    attendance_pct = profile.get("attendance_pct", 0)
    accepted_cases = profile.get("accepted_cases_count", 0)
    written_exam_score = profile.get("written_exam_score", 0)
    viva_cleared = profile.get("viva_cleared", False)
    lab_test_passed = profile.get("lab_test_passed", False)
    months_post_l1 = profile.get("months_post_l1", 0)
    total_patient_cases = profile.get("total_patient_cases", accepted_cases)
    case_report_published = profile.get("case_report_published", False)
    founder_endorsed = profile.get("founder_endorsed", False)
    peer_reviewed_pub = profile.get("peer_reviewed_pub", False)

    l1_eligible = (
        semesters_done >= 3 and
        attendance_pct >= 80.0 and
        accepted_cases >= 20 and
        written_exam_score >= 70.0 and
        viva_cleared and
        lab_test_passed
    )

    l2_eligible = (
        l1_eligible and
        months_post_l1 >= 18 and
        total_patient_cases >= 50 and
        case_report_published and
        founder_endorsed
    )

    l3_eligible = (
        l2_eligible and
        peer_reviewed_pub and
        profile.get("faculty_appointed", False)
    )

    current_tier = "STUDENT"
    if l3_eligible:
        current_tier = "L3"
    elif l2_eligible:
        current_tier = "L2"
    elif l1_eligible:
        current_tier = "L1"

    next_tier_requirements = []
    if current_tier == "STUDENT":
        if semesters_done < 3: next_tier_requirements.append(f"Complete {3 - semesters_done} remaining semesters.")
        if attendance_pct < 80.0: next_tier_requirements.append(f"Raise attendance from {attendance_pct}% to 80%.")
        if accepted_cases < 20: next_tier_requirements.append(f"Submit {20 - accepted_cases} more supervised cases.")
        if written_exam_score < 70.0: next_tier_requirements.append("Achieve ≥70% on written exam.")
        if not lab_test_passed: next_tier_requirements.append("Pass Semester 1 lab interpretation test.")
        if not viva_cleared: next_tier_requirements.append("Clear mandatory 20-minute clinical viva with Dr. Irfan Ashraf.")
    elif current_tier == "L1":
        if total_patient_cases < 50: next_tier_requirements.append(f"Document {50 - total_patient_cases} more patient cases in Z-ACIP.")
        if months_post_l1 < 18: next_tier_requirements.append(f"Requires {18 - months_post_l1} more months clinical experience.")
        if not case_report_published: next_tier_requirements.append("Submit 1 clinical case report for publication.")
        if not founder_endorsed: next_tier_requirements.append("Obtain Founder endorsement (Dr. Irfan Ashraf).")

    return {
        "current_tier": current_tier,
        "tier_details": CERTIFICATION_LEVELS.get(current_tier, {"title": "CP-AFUM Candidate"}),
        "is_certified_practitioner": l1_eligible,
        "can_practice_zayvora": l1_eligible,
        "next_tier_requirements": next_tier_requirements
    }
