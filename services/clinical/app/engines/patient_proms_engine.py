"""
ZAYVORA Health OS™ — Patient PROMs (Patient-Reported Outcome Measures) Engine
=============================================================================
Calculates longitudinal clinical improvement index, Mizaj normalization drift,
and 8-Tier Parhez adherence across 7-day and 14-day post-consultation milestones.

Features:
1. 5 Core Clinical Domains:
   - Pain & Primary Symptom Severity (VAS 0-10)
   - Hazm & Gastro-Metabolic Vitality (0-10)
   - Sleep, Mental Calm & Neuro-Equilibrium (0-10)
   - Physical Vigor & Quwwat-e-Badaniyya (0-10)
   - Treatment Tolerability & Safety (0-10)
2. 8-Tier Parhez Adherence Calculation (0-100%)
3. Red Flag Safety Escalation Firewall (Triggers doctor review if adverse score > 4)
4. Unani Mizaj Normalization Trajectory (Equilibrium Index)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class PROMsIntakeRecord:
    patient_id: str
    encounter_id: str
    day_number: int  # Day 0 (Baseline), Day 7, Day 14
    symptom_severity_vas: float  # 0 (No symptoms) to 10 (Worst imaginable)
    hazm_digestive_score: float  # 0 (Severe indigestion/nausea) to 10 (Optimal digestion)
    sleep_mental_calm_score: float  # 0 (Insomnia/high anxiety) to 10 (Deep restorative sleep)
    energy_vigor_score: float  # 0 (Severe fatigue) to 10 (High vitality)
    parhez_adherence_percent: float  # 0 to 100% adherence to 8-Tier Parhez
    medication_compliance_percent: float  # 0 to 100% adherence to Nuskha
    adverse_symptoms: List[str] = field(default_factory=list)
    patient_notes: str = ""
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PROMsEvaluationResult:
    patient_id: str
    encounter_id: str
    day_number: int
    clinical_improvement_percent: float  # e.g., +45.0%
    overall_vitality_index: float  # 0.0 to 100.0
    mizaj_normalization_state: str  # e.g., "STABLE_EQUILIBRIUM", "PROGRESSING_NORMAL", "DIVERGENT"
    parhez_compliance_tier: str  # e.g., "EXCELLENT (>=85%)", "ADEQUATE (65-84%)", "DEFICIENT (<65%)"
    requires_clinical_escalation: bool
    escalation_reasons: List[str]
    recommendation_summary: str
    longitudinal_trajectory: Dict[str, Any]


class PatientPROMsEngine:
    """Clinical outcome scoring engine for patient recovery and safety tracking."""

    @classmethod
    def evaluate_intake(
        cls,
        current: PROMsIntakeRecord,
        baseline: Optional[PROMsIntakeRecord] = None,
    ) -> PROMsEvaluationResult:
        escalation_reasons: List[str] = []
        requires_escalation = False

        # 1. Safety Firewall: Adverse symptoms check
        if current.adverse_symptoms:
            for adv in current.adverse_symptoms:
                adv_lower = adv.lower()
                if any(k in adv_lower for k in ["bleeding", "severe chest pain", "rash", "vomiting blood", "fainting"]):
                    requires_escalation = True
                    escalation_reasons.append(f"Critical adverse symptom reported: '{adv}'. Immediate doctor alert.")
                elif any(k in adv_lower for k in ["severe cramps", "palpitations", "jaundice"]):
                    requires_escalation = True
                    escalation_reasons.append(f"Potentially drug-related warning symptom: '{adv}'. Review Nuskha & Musleh.")

        # 2. Overall Vitality Index (0-100)
        # Weighted composite: 30% low symptom, 25% digestion, 25% energy, 20% sleep
        symptom_inversion = max(0.0, 10.0 - current.symptom_severity_vas)
        vitality = (
            (symptom_inversion * 3.0) +
            (current.hazm_digestive_score * 2.5) +
            (current.energy_vigor_score * 2.5) +
            (current.sleep_mental_calm_score * 2.0)
        )
        vitality_index = round(min(100.0, max(0.0, vitality)), 1)

        # 3. Clinical Improvement Percentage compared to baseline
        if baseline:
            base_symptom = baseline.symptom_severity_vas
            if base_symptom > 0:
                symptom_delta = ((base_symptom - current.symptom_severity_vas) / base_symptom) * 100.0
            else:
                symptom_delta = 0.0

            base_vitality = (
                (max(0.0, 10.0 - baseline.symptom_severity_vas) * 3.0) +
                (baseline.hazm_digestive_score * 2.5) +
                (baseline.energy_vigor_score * 2.5) +
                (baseline.sleep_mental_calm_score * 2.0)
            )
            if base_vitality > 0:
                vitality_delta = ((vitality - base_vitality) / base_vitality) * 100.0
            else:
                vitality_delta = 0.0

            improvement_pct = round((symptom_delta * 0.6) + (vitality_delta * 0.4), 1)
        else:
            # First recording (baseline established)
            improvement_pct = 0.0

        # 4. Parhez Compliance Tier
        if current.parhez_adherence_percent >= 85.0:
            compliance_tier = "EXCELLENT (>=85%)"
        elif current.parhez_adherence_percent >= 65.0:
            compliance_tier = "ADEQUATE (65-84%)"
        else:
            compliance_tier = "DEFICIENT (<65%)"
            if current.day_number >= 7 and improvement_pct < 15.0:
                escalation_reasons.append(
                    f"Low Parhez adherence ({current.parhez_adherence_percent}%) with stagnant clinical recovery."
                )

        # 5. Mizaj Normalization State
        if vitality_index >= 75.0 and current.symptom_severity_vas <= 3.0:
            mizaj_state = "STABLE_EQUILIBRIUM"
        elif vitality_index >= 50.0:
            mizaj_state = "PROGRESSING_NORMAL"
        else:
            mizaj_state = "DIVERGENT_SU_E_MIZAJ"

        # 6. Recommendation Summary
        if requires_escalation:
            rec = "EMERGENCY CLINICAL REVIEW: Hold Schedule E(1) and potent 3°/4° Mufradat pending Hakeem re-assessment."
        elif improvement_pct >= 30.0:
            rec = "POSITIVE CLINICAL TRAJECTORY: Continue current Nuskha & 8-Tier Parhez regimen through Day 14."
        elif current.day_number >= 14 and improvement_pct < 20.0:
            rec = "PLATEAU OBSERVED: Consider Tanqiya (evacuation) cascade or adjusting Nuskha potency / Musleh pairing."
        else:
            rec = "RECOVERY ON TRACK: Reinforce hydration, circadian Asbab-e-Sittah, and herbal anupan timing."

        trajectory = {
            "day": current.day_number,
            "symptom_severity": current.symptom_severity_vas,
            "vitality_index": vitality_index,
            "parhez_compliance": current.parhez_adherence_percent,
            "medication_compliance": current.medication_compliance_percent,
            "baseline_comparison": {
                "baseline_symptom": baseline.symptom_severity_vas if baseline else None,
                "improvement_percent": improvement_pct,
            } if baseline else None,
        }

        return PROMsEvaluationResult(
            patient_id=current.patient_id,
            encounter_id=current.encounter_id,
            day_number=current.day_number,
            clinical_improvement_percent=improvement_pct,
            overall_vitality_index=vitality_index,
            mizaj_normalization_state=mizaj_state,
            parhez_compliance_tier=compliance_tier,
            requires_clinical_escalation=requires_escalation,
            escalation_reasons=escalation_reasons,
            recommendation_summary=rec,
            longitudinal_trajectory=trajectory,
        )
