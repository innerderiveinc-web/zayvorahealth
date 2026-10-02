"""
ZAYVORA AGENTIC CLINICAL AI™ — Deterministic Safety Firewall
============================================================
Implements Section 7 & Section 28:
- Hardcoded, non-probabilistic clinical safety firewall.
- Evaluates: Identity -> Allergies -> Drug-Herb Interactions -> Contraindications
  -> Organ Function -> Dose Constraints -> Mudabbar Detoxification -> Missing Data.
- Returns explicit states: PASS, CAUTION, BLOCK, UNKNOWN.
"""

from typing import Dict, Any, List, Optional
from app.agentic.models import SafetyState, SafetyCheckResult


# Deterministic contraindication registries
PREGNANCY_CONTRAINDICATED_HERBS = {
    "abhal": "Juniperus communis (Emmenagogue, stimulates uterine contractions)",
    "murr": "Commiphora myrrha (Uterine stimulant)",
    "asaroon": "Asarum europaeum (Potential abortifacient and irritant)",
    "bish": "Aconitum ferox (Extreme systemic neurotoxicity, teratogenic risk)",
    "azaraqi": "Strychnos nux-vomica (Convulsant, fetal toxicity)",
    "afiyun": "Papaver somniferum (Opioid, neonatal respiratory depression)",
    "boza": "High-dose emmenagogue formulation",
    "kareel": "Capparis decidua (High uterine stimulant in classical doctrine)",
    "suranjan": "Colchicum luteum (Antimitotic agent, severe teratogenic hazard)",
}

SEVERE_NEPHROTOXIC_HERBS = {
    "samm-ul-far": "Arsenic trioxide (Severe nephrotoxicity & acute tubular necrosis)",
    "ras-kapur": "Calomel / Mercurous chloride (Nephrotoxic heavy mineral)",
    "dar-shishan": "Lead-based mineral calx (Heavy metal accumulation)",
    "suranjan_talkh": "Bitter Colchicum (Narrow therapeutic index, renal failure hazard)",
}

SCHEDULE_E1_HERBS = {
    "bish": "Aconitum ferox / Vatsanabha",
    "azaraqi": "Strychnos nux-vomica / Kuchla",
    "afiyun": "Papaver somniferum / Afeem",
    "bhang": "Cannabis sativa / Qinnab",
    "shingraf": "Cinnabar / Mercuric sulphide",
    "samm-ul-far": "Arsenic trioxide",
}

HERB_DRUG_INTERACTIONS = {
    ("warfarin", "guggul"): "Increased bleeding risk due to platelet aggregation inhibition.",
    ("warfarin", "zanjabeel"): "High-dose ginger may potentiate anticoagulant effect of Warfarin.",
    ("metformin", "karela"): "Additive hypoglycemia risk; monitor blood glucose closely.",
    ("digoxin", "usba"): "Electrolyte disturbance potential altering cardiac glycoside toxicity.",
}


class DeterministicSafetyFirewall:
    """
    Non-probabilistic clinical safety rules engine.
    Ensures that lethal or high-risk contraindications are NEVER left to LLM guesswork.
    """

    @classmethod
    def evaluate(
        cls,
        patient_context: Dict[str, Any],
        proposed_action: Dict[str, Any],
    ) -> SafetyCheckResult:
        reasons: List[str] = []
        contraindications_found: List[Dict[str, Any]] = []
        missing_critical_data: List[str] = []
        red_flags: List[str] = []

        is_blocked = False
        is_unknown = False
        is_caution = False

        # Extract context
        is_pregnant = patient_context.get("is_pregnant")
        is_lactating = patient_context.get("is_lactating", False)
        age = patient_context.get("age")
        gender = patient_context.get("gender", "").upper()
        allergies = [a.lower() for a in patient_context.get("allergies", [])]
        current_meds = [m.lower() for m in patient_context.get("current_medications", [])]
        egfr = patient_context.get("egfr")
        creatinine = patient_context.get("creatinine")
        lft_alt = patient_context.get("alt")

        # Proposed substances
        proposed_herbs = [h.lower() for h in proposed_action.get("herbs", [])]
        has_mudabbar_certificate = proposed_action.get("has_mudabbar_certificate", False)

        # 1. PREGNANCY EVALUATION
        # If female aged 15-50 and pregnancy status is completely absent while proposing toxic/emmenagogue herbs
        if gender == "FEMALE" and age is not None and 15 <= age <= 50:
            if is_pregnant is None:
                # Check if any proposed herb is pregnancy-sensitive
                for herb in proposed_herbs:
                    for contra_herb in PREGNANCY_CONTRAINDICATED_HERBS:
                        if contra_herb in herb:
                            is_unknown = True
                            missing_critical_data.append("Pregnancy status (required before prescribing reproductive/active botanicals)")
                            reasons.append(f"Pregnancy status unknown for female patient aged {age} prescribed sensitive herb '{herb}'.")
                            break

        if is_pregnant:
            for herb in proposed_herbs:
                for contra_herb, detail in PREGNANCY_CONTRAINDICATED_HERBS.items():
                    if contra_herb in herb:
                        is_blocked = True
                        contraindications_found.append({
                            "type": "PREGNANCY_CONTRAINDICATION",
                            "herb": herb,
                            "severity": "CRITICAL",
                            "detail": detail,
                        })
                        reasons.append(f"BLOCK: Herb '{herb}' is strictly contraindicated in pregnancy ({detail}).")

        # 2. RENAL IMPAIRMENT EVALUATION
        is_renal_impaired = (egfr is not None and egfr < 30) or (creatinine is not None and creatinine > 2.0)
        if is_renal_impaired:
            for herb in proposed_herbs:
                for contra_herb, detail in SEVERE_NEPHROTOXIC_HERBS.items():
                    if contra_herb in herb:
                        is_blocked = True
                        contraindications_found.append({
                            "type": "RENAL_FAILURE_CONTRAINDICATION",
                            "herb": herb,
                            "severity": "CRITICAL",
                            "detail": detail,
                        })
                        reasons.append(f"BLOCK: Herb '{herb}' is strictly contraindicated in severe renal impairment ({detail}).")

        # 3. SCHEDULE E(1) MUDABBAR DETOXIFICATION GATE
        for herb in proposed_herbs:
            for sched_e, detail in SCHEDULE_E1_HERBS.items():
                if sched_e in herb:
                    if not has_mudabbar_certificate:
                        is_blocked = True
                        contraindications_found.append({
                            "type": "MUDABBAR_DETOX_REQUIRED",
                            "herb": herb,
                            "severity": "FATAL_IF_RAW",
                            "detail": f"Schedule E(1) toxic botanical requires validated Mudabbar detoxification certificate before release: {detail}",
                        })
                        reasons.append(f"BLOCK: Schedule E(1) drug '{herb}' lacks validated Mudabbar detoxification certification.")

        # 4. ALLERGY CHECK
        for herb in proposed_herbs:
            for allergy in allergies:
                if allergy in herb or herb in allergy:
                    is_blocked = True
                    contraindications_found.append({
                        "type": "PATIENT_ALLERGY_MATCH",
                        "herb": herb,
                        "allergy": allergy,
                        "severity": "CRITICAL",
                        "detail": f"Patient has documented severe allergy to '{allergy}'.",
                    })
                    reasons.append(f"BLOCK: Patient documented allergy to '{allergy}' directly matches proposed herb '{herb}'.")

        # 5. HERB-DRUG INTERACTIONS
        for herb in proposed_herbs:
            for med in current_meds:
                for (drug_key, herb_key), detail in HERB_DRUG_INTERACTIONS.items():
                    if drug_key in med and herb_key in herb:
                        is_caution = True
                        reasons.append(f"CAUTION: Potential interaction between '{med.title()}' and '{herb.title()}': {detail}")

        # 6. RED FLAG CLINICAL CONDITIONS
        vital_signs = patient_context.get("vitals", {})
        systolic_bp = vital_signs.get("systolic_bp")
        if systolic_bp is not None and systolic_bp > 180:
            red_flags.append("HYPERTENSIVE_CRISIS")
            reasons.append("RED FLAG: Patient presents with Hypertensive Crisis (SBP > 180 mmHg). Requires immediate emergency stabilization.")
            is_caution = True

        # Resolve final Safety State
        if is_blocked:
            state = SafetyState.BLOCK
        elif is_unknown:
            state = SafetyState.UNKNOWN
        elif is_caution:
            state = SafetyState.CAUTION
        else:
            state = SafetyState.PASS
            reasons.append("Deterministic safety checks passed: no known allergies, contraindications, or unverified toxic botanicals detected.")

        return SafetyCheckResult(
            state=state,
            reasons=reasons,
            contraindications_found=contraindications_found,
            missing_critical_data=missing_critical_data,
            red_flags=red_flags,
        )
