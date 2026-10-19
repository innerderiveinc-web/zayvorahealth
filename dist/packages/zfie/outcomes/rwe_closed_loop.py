"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 4B: Real-World Evidence (RWE) & Closed-Loop Outcomes Engine
System: ZAYVORA Health OS™
Doctrine: Formulation x Patient Phenotype x Batch x Biomarker Trajectory x Clinical Outcome = Continual Scientific Learning
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class LongitudinalBiomarkerPoint:
    day_offset: int
    biomarker_name: str
    value: float
    unit: str


@dataclass
class RWEClinicalObservation:
    record_id: str
    patient_mrn: str
    formulation_id: str
    formulation_version: str
    dispensed_batch_id: str
    baseline_diagnosis: str
    patient_phenotype: str          # e.g., "Balghami with Hyperuricemia"
    treatment_duration_days: int
    adherence_pct: float
    biomarker_trajectory: List[LongitudinalBiomarkerPoint]
    clinical_outcome_delta: str     # e.g. "Complete resolution of morning joint erythema and pain (-75%)"
    adverse_events: List[str]
    confounder_score: float         # 0.0 (clean) to 1.0 (high co-medication confounders)
    recorded_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RWEClosedLoopEngine:
    """Manages post-market real-world observational evidence cohorts."""

    _OBSERVATIONS: List[RWEClinicalObservation] = []

    @classmethod
    def record_outcome(
        cls,
        patient_mrn: str,
        formulation_id: str,
        formulation_version: str,
        batch_id: str,
        baseline_diagnosis: str,
        phenotype: str,
        duration_days: int,
        adherence_pct: float,
        biomarker_points: List[Dict[str, Any]],
        outcome_delta: str,
        adverse_events: Optional[List[str]] = None,
        confounder_score: float = 0.1
    ) -> RWEClinicalObservation:
        """Records an authentic patient longitudinal trajectory linked to the exact physical batch dispensed."""
        record_id = f"RWE-{uuid.uuid4().hex[:8].upper()}"
        points = [
            LongitudinalBiomarkerPoint(
                day_offset=p.get("day_offset", 0),
                biomarker_name=p.get("biomarker_name", "Biomarker"),
                value=float(p.get("value", 0.0)),
                unit=p.get("unit", "")
            )
            for p in biomarker_points
        ]

        obs = RWEClinicalObservation(
            record_id=record_id,
            patient_mrn=patient_mrn,
            formulation_id=formulation_id,
            formulation_version=formulation_version,
            dispensed_batch_id=batch_id,
            baseline_diagnosis=baseline_diagnosis,
            patient_phenotype=phenotype,
            treatment_duration_days=duration_days,
            adherence_pct=adherence_pct,
            biomarker_trajectory=points,
            clinical_outcome_delta=outcome_delta,
            adverse_events=adverse_events or [],
            confounder_score=confounder_score
        )

        cls._OBSERVATIONS.append(obs)
        return obs

    @classmethod
    def analyze_batch_cohort(cls, batch_id: str) -> Dict[str, Any]:
        """Aggregates clinical performance and adverse event frequency for a specific manufacturing batch."""
        cohort = [o for o in cls._OBSERVATIONS if o.dispensed_batch_id == batch_id]
        if not cohort:
            return {"batch_id": batch_id, "cohort_size": 0, "status": "NO_LONGITUDINAL_DATA"}

        mean_adherence = sum(o.adherence_pct for o in cohort) / len(cohort)
        total_adverse = sum(len(o.adverse_events) for o in cohort)

        return {
            "batch_id": batch_id,
            "cohort_size": len(cohort),
            "mean_adherence_pct": round(mean_adherence, 2),
            "total_adverse_events": total_adverse,
            "adverse_event_rate_pct": round((total_adverse / len(cohort)) * 100, 2),
            "efficacy_trend": "CONSISTENT_FAVORABLE" if total_adverse == 0 and mean_adherence > 80 else "MODERATE"
        }

    @classmethod
    def list_observations(cls, formulation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if formulation_id:
            return [o.to_dict() for o in cls._OBSERVATIONS if o.formulation_id == formulation_id]
        return [o.to_dict() for o in cls._OBSERVATIONS]


# Pre-seed canonical RWE observation
RWEClosedLoopEngine.record_outcome(
    patient_mrn="MRN-2026-08C65D",
    formulation_id="ZAY-FORM-0001",
    formulation_version="v1.1",
    batch_id="ZAY-BATCH-2026-001",
    baseline_diagnosis="Acute Gouty Arthritis",
    phenotype="Balghami with Synovial Hyperemia",
    duration_days=21,
    adherence_pct=95.0,
    biomarker_points=[
        {"day_offset": 0, "biomarker_name": "Serum Uric Acid", "value": 8.6, "unit": "mg/dL"},
        {"day_offset": 7, "biomarker_name": "Serum Uric Acid", "value": 7.1, "unit": "mg/dL"},
        {"day_offset": 21, "biomarker_name": "Serum Uric Acid", "value": 5.9, "unit": "mg/dL"},
        {"day_offset": 0, "biomarker_name": "hs-CRP", "value": 14.2, "unit": "mg/L"},
        {"day_offset": 21, "biomarker_name": "hs-CRP", "value": 1.8, "unit": "mg/L"}
    ],
    outcome_delta="Complete resolution of acute metatarsophalangeal pain; normalized ambulation.",
    adverse_events=[],
    confounder_score=0.05
)
