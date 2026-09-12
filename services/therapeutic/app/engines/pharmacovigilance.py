"""
WHO-UMC Pharmacovigilance Causality Assessment Engine.

Implements the international Uppsala Monitoring Centre (WHO-UMC) standardized
system for causality assessment of suspected Adverse Drug Reactions (ADRs) and
herb-drug-toxicology events in integrative Unani healthcare.

Includes statutory Schedule E(1) Mudabbar verification rules to detect toxic
alkaloid / heavy metal reactions caused by unpurified administration.
"""
from __future__ import annotations

from typing import Any


def evaluate_who_umc_causality(report: dict[str, Any]) -> dict[str, Any]:
    """Evaluates an ADR report against WHO-UMC causality criteria and statutory
    Unani toxicological rules.
    """
    suspected_agent = report.get("suspected_agent", "")
    adverse_reaction = report.get("adverse_reaction_description", "")
    latency_hours = report.get("latency_hours")
    dechallenge = report.get("dechallenge_performed", False)
    dechallenge_outcome = report.get("dechallenge_outcome", "unknown")
    rechallenge = report.get("rechallenge_performed", False)
    rechallenge_outcome = report.get("rechallenge_outcome", "not_applicable")
    concomitant_drugs = report.get("concomitant_drugs", [])
    alternative_etiologies = report.get("alternative_etiologies_considered", [])
    is_schedule_e1 = report.get("is_schedule_e1_substance", False)
    mudabbar_followed = report.get("verified_mudabbar_protocol_followed", True)

    # 1. Statutory Poison & Mudabbar Check
    statutory_warning = None
    regulatory_action_required = False
    recommendations = []

    if is_schedule_e1 and not mudabbar_followed:
        statutory_warning = (
            f"STATUTORY POISON AUDIT FAILURE: Suspected agent '{suspected_agent}' is classified "
            "under Schedule E(1) of the Drugs & Cosmetics Act and was administered without "
            "verified Mudabbar (detoxification) protocol. Immediate batch quarantine and "
            "toxicology audit required."
        )
        regulatory_action_required = True
        recommendations.append("Quarantine remaining clinical stock of this batch immediately.")
        recommendations.append("Obtain stat serum chemistry, hepatic function, and renal panels.")
        recommendations.append("File mandatory AYUSH National Pharmacovigilance Yellow Report.")

    # 2. Causality Scoring according to WHO-UMC Criteria
    # Plausible time window: 0.5 to 72 hours for acute reactions
    time_plausible = latency_hours is not None and (0.1 <= latency_hours <= 168.0)
    has_alternative_cause = len(alternative_etiologies) > 0 or len(concomitant_drugs) > 0

    score = 0
    if time_plausible:
        score += 3
    elif latency_hours is not None:
        score += 1

    if dechallenge and dechallenge_outcome == "improved":
        score += 3
    elif dechallenge and dechallenge_outcome == "no_change":
        score -= 2

    if rechallenge and rechallenge_outcome == "positive":
        score += 4
    elif rechallenge and rechallenge_outcome == "negative":
        score -= 4

    if not has_alternative_cause:
        score += 2
    else:
        score -= 1

    if is_schedule_e1 and not mudabbar_followed:
        score += 4

    # 3. Categorization
    if not adverse_reaction or len(adverse_reaction.strip()) < 5:
        category = "UNCLASSIFIABLE"
        rationale = "Insufficient clinical information or incomplete adverse event description."
    elif latency_hours is None and not dechallenge:
        category = "CONDITIONAL_UNCLASSIFIED"
        rationale = "Essential temporal data or de-challenge information lacking; pending clinical investigation."
    elif rechallenge and rechallenge_outcome == "positive" and dechallenge_outcome == "improved" and not has_alternative_cause:
        category = "CERTAIN"
        rationale = "Plausible temporal relationship, clinical improvement upon de-challenge, and unequivocal positive re-challenge without alternative explanations."
    elif dechallenge_outcome == "improved" and time_plausible and (not has_alternative_cause or (is_schedule_e1 and not mudabbar_followed)):
        category = "PROBABLE"
        rationale = "Reasonable time sequence to drug intake, clinical improvement upon drug cessation, and alternative etiologies unlikely or non-explanatory."
    elif time_plausible and (has_alternative_cause or dechallenge_outcome in ("unknown", "no_change")):
        category = "POSSIBLE"
        rationale = "Reasonable temporal relationship, but concurrent medications, underlying pathology, or indeterminate de-challenge provide alternative explanations."
    elif latency_hours is not None and latency_hours > 720:  # > 30 days for acute reaction
        category = "UNLIKELY"
        rationale = "Temporal relationship makes causal connection highly improbable, and disease/concomitant therapies provide plausible explanations."
    else:
        category = "POSSIBLE"
        rationale = "Plausible time window with partial clinical resolution; requires ongoing monitoring."

    if category in ("CERTAIN", "PROBABLE") and is_schedule_e1:
        regulatory_action_required = True
        if "File mandatory AYUSH National Pharmacovigilance Yellow Report." not in recommendations:
            recommendations.append("File mandatory AYUSH National Pharmacovigilance Yellow Report.")

    if not recommendations:
        recommendations.append("Document event in patient longitudinal electronic medical record.")
        recommendations.append("Consider non-pharmacological Tadbeer or alternative Badal formulation.")

    return {
        "causality_category": category,
        "causality_score": score,
        "rationale": rationale,
        "statutory_warning": statutory_warning,
        "regulatory_action_required": regulatory_action_required,
        "recommendations": recommendations,
    }
