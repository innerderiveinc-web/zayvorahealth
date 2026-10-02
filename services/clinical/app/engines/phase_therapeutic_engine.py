"""
ZAYVORA Health OS™ — Phase-Based Therapeutic Engine
Source: Dr. Irfan Ashraf — CP-AFUM Textbook Chapter 4 & Table 4.1
Encodes:
- The 3-Phase Therapeutic Model (Stabilization -> Axis Correction -> Consolidation)
- The 8 Complete Phase Trigger Rules (R1 to R8)
- Phase Duration Calculations
- Rigorous Phase Exit Gates
"""
from typing import Dict, Any, List, Optional


def evaluate_phase_trigger_rules(patient_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates all 8 Phase Trigger Rules (R1-R8) based on patient clinical parameters.
    """
    applied_rules = []
    
    sgpt = patient_profile.get("sgpt", 0)
    hs_crp = patient_profile.get("hs_crp", 0)
    chronicity_months = patient_profile.get("chronicity_months", 0)
    mizaj = patient_profile.get("mizaj", "").lower()
    severe_axes_count = patient_profile.get("severe_axes_count", 1)
    phase_1_sgpt_improvement_pct = patient_profile.get("phase_1_sgpt_improvement_pct")
    hpa_compromised = patient_profile.get("hpa_compromised", False)
    phase_3_rebound = patient_profile.get("phase_3_rebound", False)
    on_insulin_or_hypoglycemics = patient_profile.get("on_insulin_or_hypoglycemics", False)

    # R1: SGPT >45 OR hs-CRP >3
    phase_1_mandatory = False
    if sgpt > 45 or hs_crp > 3:
        phase_1_mandatory = True
        applied_rules.append({
            "rule": "R1",
            "trigger": "SGPT >45 U/L OR hs-CRP >3 mg/L",
            "action": "Phase 1 (LiverPrime Core) mandatory — no exception for any Mizaj, condition, or severity.",
            "rationale": "Inflamed liver cannot efficiently metabolise Phase 2 actives."
        })

    # R2: Disease chronicity >24 months
    phase_1_duration_weeks = 2
    if chronicity_months > 24:
        phase_1_duration_weeks = 4
        applied_rules.append({
            "rule": "R2",
            "trigger": f"Disease chronicity = {chronicity_months} months (>24 months)",
            "action": "Extend Phase 1 minimum duration from 2 to 4 weeks.",
            "rationale": "Deeply entrenched metabolic stagnation requires extended priming."
        })

    # R3: Safravi Mizaj
    if "safra" in mizaj:
        applied_rules.append({
            "rule": "R3",
            "trigger": "Safravi Mizaj identified",
            "action": "Reduce ALL heating herbs 25-30% throughout ALL three phases.",
            "rationale": "Prevents hepatotoxic heat flares, rising SGPT, and biliary irritation."
        })
        if phase_1_duration_weeks < 4:
            phase_1_duration_weeks = 4

    # R4: Two severe primary axes
    phase_2_duration_weeks = 12
    if severe_axes_count >= 2:
        phase_2_duration_weeks = 16
        applied_rules.append({
            "rule": "R4",
            "trigger": f"{severe_axes_count} severe primary axes identified",
            "action": "Extend Phase 2 to minimum 16 weeks before Phase 3 transition (standard 8-12 weeks).",
            "rationale": "Allows adequate time for both axes to demonstrate measurable correction."
        })

    # R5: Phase 1 improvement <20% in SGPT
    can_proceed_to_phase_2 = True
    if phase_1_sgpt_improvement_pct is not None:
        if phase_1_sgpt_improvement_pct < 20.0:
            can_proceed_to_phase_2 = False
            applied_rules.append({
                "rule": "R5",
                "trigger": f"Phase 1 SGPT improvement = {phase_1_sgpt_improvement_pct}% (<20%)",
                "action": "Do NOT proceed to Phase 2 — extend Phase 1 or investigate compliance failure.",
                "rationale": "Unprimed liver will fail to bioactivate Phase 2 therapeutic compounds."
            })

    # R6: HPA compromised
    if hpa_compromised or "sauda" in mizaj:
        applied_rules.append({
            "rule": "R6",
            "trigger": "HPA compromised (cortisol dysregulation, anxiety, insomnia)",
            "action": "Add NeuroCalmX™ to Phase 1 — stabilize HPA before gonadal/metabolic/thyroid axis correction.",
            "rationale": "Cortisol suppresses LH/FSH and TSH while driving insulin resistance."
        })

    # R7: Phase 3 exit lab rebound
    phase_3_approved = True
    if phase_3_rebound:
        phase_3_approved = False
        applied_rules.append({
            "rule": "R7",
            "trigger": "Phase 3 exit lab shows biomarker rebound",
            "action": "Return to Phase 2 therapeutic dose — do not exit protocol without confirmed stability.",
            "rationale": "Premature exit leads to immediate disease recurrence."
        })

    # R8: Patient on insulin or oral hypoglycaemics
    if on_insulin_or_hypoglycemics:
        applied_rules.append({
            "rule": "R8",
            "trigger": "Patient on insulin or oral hypoglycaemics",
            "action": "Berberine caution (MetaboCore) — monitor blood glucose weekly; coordinate dose with physician.",
            "rationale": "Additive AMPK activation can trigger cumulative hypoglycemia."
        })

    return {
        "phase_1_mandatory": phase_1_mandatory,
        "recommended_phase_1_weeks": phase_1_duration_weeks,
        "recommended_phase_2_weeks": phase_2_duration_weeks,
        "recommended_phase_3_weeks": 4,
        "can_proceed_to_phase_2": can_proceed_to_phase_2,
        "phase_3_stable": phase_3_approved,
        "applied_rules": applied_rules
    }


def verify_phase_1_exit(baseline_sgpt: float, current_sgpt: float, hs_crp_trending_down: bool) -> Dict[str, Any]:
    """
    Phase 1 Exit Criterion: SGPT must have improved by >=20% from baseline AND hs-CRP trending down.
    """
    if baseline_sgpt <= 0:
        return {"can_exit": False, "reason": "Invalid baseline SGPT"}
    
    pct_improvement = ((baseline_sgpt - current_sgpt) / baseline_sgpt) * 100.0
    sgpt_passed = pct_improvement >= 20.0 or current_sgpt <= 25.0  # Optimal threshold
    can_exit = sgpt_passed and hs_crp_trending_down

    reasons = []
    if not sgpt_passed:
        reasons.append(f"SGPT improvement {pct_improvement:.1f}% is below the mandatory 20% threshold.")
    if not hs_crp_trending_down:
        reasons.append("hs-CRP is not trending downward (active systemic inflammation remains).")

    return {
        "can_exit_phase_1": can_exit,
        "sgpt_improvement_percentage": round(pct_improvement, 1),
        "sgpt_passed": sgpt_passed,
        "crp_passed": hs_crp_trending_down,
        "next_step": "Proceed to Phase 2 Axis Correction" if can_exit else "Extend Phase 1 by 2 weeks"
    }


def verify_phase_2_exit(baseline_biomarker: float, current_biomarker: float, symptom_resolution_pct: float) -> Dict[str, Any]:
    """
    Phase 2 Exit Criteria: Primary axis biomarker improved >=40% AND symptom resolution >=70%.
    """
    pct_improvement = ((baseline_biomarker - current_biomarker) / baseline_biomarker) * 100.0 if baseline_biomarker > 0 else 0
    lab_passed = pct_improvement >= 40.0
    symptom_passed = symptom_resolution_pct >= 70.0
    can_exit = lab_passed and symptom_passed

    return {
        "can_exit_phase_2": can_exit,
        "lab_improvement_pct": round(pct_improvement, 1),
        "symptom_resolution_pct": round(symptom_resolution_pct, 1),
        "next_step": "Transition to Phase 3 Consolidation (reduce hero product by 40-50%)" if can_exit else "Continue Phase 2 for 4 additional weeks"
    }
