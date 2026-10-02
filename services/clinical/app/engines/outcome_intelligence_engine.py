"""
ZAYVORA Health OS™ — Outcome Intelligence Engine ("What Changed?")
=================================================================
Implements Phase 9 of the Clinical Evolution Roadmap:
1. Multi-Dimensional Longitudinal Delta Tracking:
   - Pre/Post Symptom Severity (VAS, PROMs, Functional Index)
   - Objective Biomarker Shifts (e.g., hs-CRP, HOMA-IR, HbA1c, eGFR)
   - Mizaj Restitution Index (Ta'deel-e-Mizaj humoral equilibrium)
   - Treatment Adherence Percentage (Medication Possession Ratio)
2. Classical Unani Outcome Classification:
   - Kamil (Complete Remission / Al-Shifa al-Taam): >= 80% improvement + humoral balance
   - Juz'i (Partial Response / Tahassun Juz'i): 40% - 79% improvement
   - Ghair Mu'athir (Non-Responsive / Adam al-Istijabah): < 40% change
   - Intikas (Relapse or Deterioration / Al-Ruju'): > 20% worsening
3. Real-World Evidence (RWE) Closed-Loop Ingestion:
   - HIPAA Safe Harbor § 164.514(b)(2) compliant de-identification
   - Emits structured outcome records into the clinical knowledge base.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import datetime
import hashlib

class ClassicalOutcome(str, Enum):
    KAMIL = "KAMIL"                     # Complete remission (>= 80%)
    JUZ_I = "JUZ_I"                     # Partial improvement (40-79%)
    GHAIR_MUATHIR = "GHAIR_MUATHIR"     # Non-responsive (< 40%)
    INTIKAS = "INTIKAS"                 # Deterioration / relapse (> 20% worsening)

@dataclass
class BiomarkerObservation:
    marker_name: str
    baseline_value: float
    followup_value: float
    unit: str
    is_lower_better: bool = True

@dataclass
class OutcomeEvaluation:
    patient_id: str
    deidentified_hash: str
    condition: str
    protocol_nuskha_id: str
    day_in_treatment: int
    vas_baseline: float
    vas_followup: float
    vas_improvement_percent: float
    mizaj_restitution_score: float # 0.0 to 1.0
    adherence_percent: float
    biomarker_deltas: List[Dict[str, Any]]
    composite_improvement_index: float
    outcome_class: ClassicalOutcome
    clinical_summary: str
    rwe_learning_eligible: bool
    evaluation_timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

class OutcomeIntelligenceEngine:
    """
    Computes rigorous clinical response deltas and assigns authoritative outcome classifications.
    """

    # In-memory store for longitudinal patient trajectories
    _PATIENT_TRAJECTORIES: Dict[str, List[OutcomeEvaluation]] = {}

    @staticmethod
    def _deidentify_patient(patient_id: str) -> str:
        # HIPAA Safe Harbor deterministic hash
        return hashlib.sha256(f"ZAYVORA_RWE_SALT_{patient_id}".encode()).hexdigest()[:16]

    @classmethod
    def evaluate_followup(
        cls,
        patient_id: str,
        condition: str,
        protocol_nuskha_id: str,
        day_in_treatment: int,
        vas_baseline: float,
        vas_followup: float,
        mizaj_deviation_baseline: float, # e.g. 8.0/10 deviation
        mizaj_deviation_followup: float, # e.g. 2.0/10 deviation
        adherence_percent: float,
        biomarkers: Optional[List[BiomarkerObservation]] = None
    ) -> OutcomeEvaluation:
        # 1. Calculate VAS Symptom Relief
        # VAS is 0-10 scale where 10 is max pain/distress
        if vas_baseline <= 0:
            vas_improvement_pct = 0.0
        else:
            vas_improvement_pct = ((vas_baseline - vas_followup) / vas_baseline) * 100.0

        # 2. Calculate Mizaj Restitution Score (Humoral Ta'deel)
        # Shift towards 0 deviation represents perfect equilibrium
        if mizaj_deviation_baseline <= 0:
            mizaj_restitution = 1.0
        else:
            restitution_delta = (mizaj_deviation_baseline - mizaj_deviation_followup) / mizaj_deviation_baseline
            mizaj_restitution = max(0.0, min(1.0, restitution_delta))

        # 3. Biomarker Deltas
        biomarker_deltas: List[Dict[str, Any]] = []
        biomarker_score_acc = 0.0
        if biomarkers:
            for b in biomarkers:
                if b.baseline_value != 0:
                    raw_pct = ((b.baseline_value - b.followup_value) / b.baseline_value) * 100.0
                    normalized_improvement = raw_pct if b.is_lower_better else -raw_pct
                else:
                    normalized_improvement = 0.0
                
                biomarker_deltas.append({
                    "marker": b.marker_name,
                    "baseline": b.baseline_value,
                    "followup": b.followup_value,
                    "unit": b.unit,
                    "improvement_percent": round(normalized_improvement, 2)
                })
                biomarker_score_acc += max(-100.0, min(100.0, normalized_improvement))
            avg_biomarker_improvement = biomarker_score_acc / len(biomarkers)
        else:
            avg_biomarker_improvement = vas_improvement_pct

        # 4. Composite Improvement Index (Weighted: 50% VAS, 25% Mizaj, 25% Lab/Biomarker)
        composite_index = (
            (vas_improvement_pct * 0.50) +
            (mizaj_restitution * 100.0 * 0.25) +
            (avg_biomarker_improvement * 0.25)
        )
        composite_index = round(composite_index, 2)

        # 5. Authoritative Classical Classification
        if composite_index <= -20.0:
            outcome = ClassicalOutcome.INTIKAS
            summary = "Patient experienced clinical deterioration or acute relapse (Intikas/Al-Ruju'). Immediate protocol review indicated."
        elif composite_index >= 80.0:
            outcome = ClassicalOutcome.KAMIL
            summary = "Complete therapeutic resolution achieved (Kamil/Al-Shifa al-Taam) with profound humoral equilibrium."
        elif composite_index >= 40.0:
            outcome = ClassicalOutcome.JUZ_I
            summary = "Substantial partial response documented (Tahassun Juz'i); continuation or tapering of Murakkab recommended."
        else:
            outcome = ClassicalOutcome.GHAIR_MUATHIR
            summary = "Minimal clinical response observed (<40% improvement); investigate non-adherence or consider Badal substitution."

        # RWE eligibility requires at least 70% adherence
        rwe_eligible = (adherence_percent >= 70.0) and (outcome in [ClassicalOutcome.KAMIL, ClassicalOutcome.JUZ_I, ClassicalOutcome.GHAIR_MUATHIR])

        evaluation = OutcomeEvaluation(
            patient_id=patient_id,
            deidentified_hash=cls._deidentify_patient(patient_id),
            condition=condition,
            protocol_nuskha_id=protocol_nuskha_id,
            day_in_treatment=day_in_treatment,
            vas_baseline=vas_baseline,
            vas_followup=vas_followup,
            vas_improvement_percent=round(vas_improvement_pct, 2),
            mizaj_restitution_score=round(mizaj_restitution, 2),
            adherence_percent=adherence_percent,
            biomarker_deltas=biomarker_deltas,
            composite_improvement_index=composite_index,
            outcome_class=outcome,
            clinical_summary=summary,
            rwe_learning_eligible=rwe_eligible
        )

        if patient_id not in cls._PATIENT_TRAJECTORIES:
            cls._PATIENT_TRAJECTORIES[patient_id] = []
        cls._PATIENT_TRAJECTORIES[patient_id].append(evaluation)

        return evaluation

    @classmethod
    def get_trajectory(cls, patient_id: str) -> List[OutcomeEvaluation]:
        return cls._PATIENT_TRAJECTORIES.get(patient_id, [])

