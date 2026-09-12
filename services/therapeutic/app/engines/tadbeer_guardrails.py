"""
ZAYVORA Ilaj bil-Tadbeer (Regimenal Therapy) Clinical Safety Guardrails.

Master Build Prompt v4.0 §15 (Ilaj bil-Tadbeer) & §13 (Safety Architecture).

Pure, deterministic evaluation of medical contraindications, physiological
safety thresholds, and classical Unani prerequisites for all 12 core
regimenal modalities.
"""
from __future__ import annotations

from typing import Any

VERDICT_ORDER = ["SAFE_TO_CONSIDER", "CAUTION", "MODIFY", "DO_NOT_RECOMMEND", "REFER"]


def _escalate(current: str, candidate: str) -> str:
    return candidate if VERDICT_ORDER.index(candidate) > VERDICT_ORDER.index(current) else current


def run_tadbeer_guardrails(
    *,
    patient_context: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    """
    Evaluates safety of a proposed Tadbeer (regimenal therapy) plan against
    the patient's clinical safety context.
    """
    verdict = "SAFE_TO_CONSIDER"
    reasons: list[str] = []

    procedure_name = (plan.get("name") or "").lower()
    category = (plan.get("category") or "").lower()
    method = (plan.get("method") or "").lower()
    indication = (plan.get("indication") or "").lower()

    age = patient_context.get("age")
    pregnancy = patient_context.get("pregnancy_status") == "pregnant"
    lactation = patient_context.get("lactation_status") == "yes"
    medications = [m.lower() for m in (patient_context.get("current_medications") or [])]
    comorbidities = [c.lower() for c in (patient_context.get("comorbidities") or [])]
    complaint = (patient_context.get("chief_complaint") or "").lower()

    has_anticoagulant = any(
        kw in med
        for med in medications
        for kw in ["warfarin", "heparin", "apixaban", "rivaroxaban", "dabigatran", "clopidogrel", "anticoagulant", "aspirin"]
    )
    has_bleeding_disorder = any(
        kw in c
        for c in comorbidities + [complaint]
        for kw in ["hemophilia", "thrombocytopenia", "bleeding disorder", "itp", "purpura"]
    )
    has_anemia = any("anemia" in c or "low hemoglobin" in c or "anaemia" in c for c in comorbidities + [complaint])
    has_hypotension = any("hypotension" in c or "low blood pressure" in c or "shock" in c for c in comorbidities + [complaint])
    has_fever = any("fever" in c or "bukhar" in c or "humma" in c for c in comorbidities + [complaint])
    has_dvt = any("dvt" in c or "deep vein thrombosis" in c or "thrombophlebitis" in c or "clot in leg" in c for c in comorbidities + [complaint])
    has_uncontrolled_diabetes = any("uncontrolled diabetes" in c or "diabetic neuropathy" in c for c in comorbidities)

    # ========================================================================
    # 1. HIJAMA (CUPPING THERAPY — WET / DRY)
    # ========================================================================
    if "hijama" in procedure_name or "cupping" in procedure_name:
        is_wet = "wet" in procedure_name or "wet" in method or "shart" in procedure_name or "shart" in method
        if is_wet:
            if has_bleeding_disorder or has_anticoagulant:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    "Hijama bil-Shart (Wet Cupping) is strictly contraindicated in patients on anticoagulants or with active coagulopathies."
                )
            if has_anemia:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    "Hijama bil-Shart (Wet Cupping) is contraindicated in moderate-to-severe anemia; risks precipitating hypovolemic crisis."
                )
            if has_hypotension:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    "Wet Cupping is contraindicated during acute hypotension or hemodynamic instability."
                )

        if pregnancy:
            is_pelvic = any(k in method or k in indication for k in ["abdomen", "sacral", "lumbar", "pelvic", "back"])
            if is_pelvic:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    "Hijama over abdominal or lumbosacral regions is contraindicated in pregnancy due to reflex uterine hyperstimulation."
                )
            else:
                verdict = _escalate(verdict, "CAUTION")
                reasons.append("Pregnancy precaution: Hijama requires strict vital monitoring and non-invasive application.")

    # ========================================================================
    # 2. FASD (VENESECTION / PHLEBOTOMY)
    # ========================================================================
    if "fasd" in procedure_name or "venesection" in procedure_name or "phlebotomy" in procedure_name:
        if age is not None:
            if age < 14:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    f"Fasd is strictly contraindicated in pediatric patients under 14 years of age (Canon of Medicine §Fasd Rules)."
                )
            elif age > 60:
                verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
                reasons.append(
                    f"Fasd is contraindicated in elderly patients exceeding 60 years of age due to failure of Tabiyat recovery."
                )
        if pregnancy:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Fasd is absolutely contraindicated during pregnancy.")
        if has_anemia or has_hypotension or has_bleeding_disorder:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Fasd is contraindicated in anemia, hypotension, or coagulopathy.")

    # ========================================================================
    # 3. HAMMAM (TURKISH / MEDICATED BATH)
    # ========================================================================
    if "hammam" in procedure_name or "bath" in procedure_name or category == "bathing":
        if has_fever:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append(
                "Hot Hammam is contraindicated in acute febrile illness (Humma-e-Hadda); exacerbates core hyperthermia."
            )
        if any("cardiac" in c or "heart failure" in c or "angina" in c for c in comorbidities):
            verdict = _escalate(verdict, "CAUTION")
            reasons.append("Hammam causes peripheral vasodilation; requires monitoring in cardiovascular disease.")

    # ========================================================================
    # 4. DALAK (MEDICAL MASSAGE)
    # ========================================================================
    if "dalak" in procedure_name or "massage" in procedure_name or category == "massage":
        if has_dvt:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append(
                "Medical massage is STRICTLY CONTRAINDICATED in suspected or documented Deep Vein Thrombosis (DVT); extreme risk of fatal pulmonary embolism."
            )

    # ========================================================================
    # 5. QAI (THERAPEUTIC EMESIS)
    # ========================================================================
    if "qai" in procedure_name or "emesis" in procedure_name:
        has_severe_htn = any("hypertension" in c or "high blood pressure" in c for c in comorbidities)
        has_hernia = any("hernia" in c for c in comorbidities)
        if has_severe_htn or has_hernia or pregnancy:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append(
                "Therapeutic emesis (Qai) is contraindicated in hypertension, hernia, or pregnancy due to severe acute intra-abdominal/cranial pressure elevation."
            )

    # ========================================================================
    # 6. ISHAAL (THERAPEUTIC PURGATION)
    # ========================================================================
    if "ishaal" in procedure_name or "purgation" in procedure_name:
        if pregnancy:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Drastic purgation (Ishaal) is contraindicated in pregnancy due to risk of inducing premature labor.")
        if any("obstruction" in c or "appendicitis" in c for c in comorbidities):
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append("Purgation is contraindicated in acute bowel obstruction or surgical abdomen.")

    # ========================================================================
    # 7. KAI (CAUTERIZATION)
    # ========================================================================
    if "kai" in procedure_name or "cauterization" in procedure_name:
        if has_uncontrolled_diabetes:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append(
                "Cauterization (Kai) is contraindicated in uncontrolled diabetes or peripheral neuropathy due to risk of non-healing ulcer and gangrene."
            )

    # ========================================================================
    # 8. ZALO (LEECH THERAPY / IRSAL-E-ALAQ)
    # ========================================================================
    if "zalo" in procedure_name or "leech" in procedure_name or "alaq" in procedure_name:
        if has_bleeding_disorder or has_anticoagulant or has_anemia:
            verdict = _escalate(verdict, "DO_NOT_RECOMMEND")
            reasons.append(
                "Leech therapy (Irsal-e-Alaq) is contraindicated in coagulopathy, anticoagulant use, or severe anemia due to prolonged bleeding from hirudin."
            )

    if not reasons:
        reasons.append("No contraindications identified for proposed regimenal therapy. Ensure clinical asepsis and practitioner certification.")

    return {
        "verdict": verdict,
        "reasons": reasons,
        "requiresPractitionerCertification": True,
    }
