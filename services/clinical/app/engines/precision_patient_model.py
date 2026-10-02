"""
ZAYVORA Health OS™ — Precision Patient Model Engine (Phase 18)
=============================================================
Represents the patient as an integrated, longitudinal clinical model
rather than a static EMR row:

Patient 360:
├── Demographics & Baseline Vitals
├── Longitudinal Symptom Trajectory
├── Functional Lab Biomarkers
├── 10-Ajnas Mizaj Dynamic State
├── 12 Organ-Axis Multi-Dimensional Scoring
├── Prescribed Nuskha & Pharmacotherapy History
├── Posology Adherence Rate (MPR)
├── Asbab-e-Sittah Lifestyle Dynamics
├── Standardized Classical Outcomes (Kamil, Juz'i, Ghair Mu'athir, Intikas)
├── Pharmacovigilance Adverse Reaction Logs
├── Clinical Phenotype Signature
└── Early Risk Signals & Wearable Integration

Synthesizes the core clinical intelligence question:
"What was tried → What changed → What did not change → What caused adverse effects → What worked for which phenotype"
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class SymptomObservation:
    symptom_name: str
    severity_vas: float  # 0.0 - 10.0
    duration_days: int
    onset_date: str
    notes: Optional[str] = None


@dataclass
class FunctionalBiomarkerDelta:
    marker_name: str
    baseline_value: float
    current_value: float
    unit: str
    is_lower_better: bool = True
    last_tested_date: str = ""

    @property
    def percentage_change(self) -> float:
        if self.baseline_value == 0:
            return 0.0
        return round(((self.current_value - self.baseline_value) / self.baseline_value) * 100.0, 2)

    @property
    def is_improved(self) -> bool:
        if self.is_lower_better:
            return self.current_value < self.baseline_value
        return self.current_value > self.baseline_value


@dataclass
class MizajStateRecord:
    timestamp: str
    dominant_mizaj: str  # e.g., "Barid-Ratab"
    heat_degree: int = 2     # 1-4
    cold_degree: int = 2     # 1-4
    dry_degree: int = 2      # 1-4
    moist_degree: int = 2    # 1-4
    dyscrasia: Optional[str] = None


# Compatibility aliases
MizajDynamicRecord = MizajStateRecord
OrganAxisRecord = Dict[str, Any]
PrescribedNuskhaRecord = Dict[str, Any]
PosologyAdherenceRecord = Dict[str, Any]
LifestyleDynamicsRecord = Dict[str, Any]


@dataclass
class RiskSignal:
    signal_id: str
    signal_type: str  # "ADR_RISK", "ADHERENCE_DROP", "VAS_REBOUND", "THERMAL_POLARIZATION"
    severity: str     # "LOW", "MODERATE", "ELEVATED", "CRITICAL"
    trigger_detail: str
    detected_at: str
    requires_clinician_review: bool = True


@dataclass
class PrecisionPatientModel:
    """Master longitudinal precision model for an individual patient in ZAYVORA OS."""
    patient_id: str
    demographics: Dict[str, Any] = field(default_factory=dict)
    presenting_condition: str = "General"
    age: Optional[int] = None
    gender: Optional[str] = None
    baseline_vitals: Dict[str, Any] = field(default_factory=dict)
    primary_condition: Optional[str] = None
    medical_history: List[str] = field(default_factory=list)
    symptoms: List[SymptomObservation] = field(default_factory=list)
    biomarkers: List[FunctionalBiomarkerDelta] = field(default_factory=list)
    mizaj_history: List[MizajStateRecord] = field(default_factory=list)
    organ_axis_scores: Dict[str, float] = field(default_factory=dict)
    nuskha_history: List[Dict[str, Any]] = field(default_factory=list)
    adherence_percentage: float = 100.0
    lifestyle_parameters: Dict[str, Any] = field(default_factory=dict)
    outcome_trajectory: List[Dict[str, Any]] = field(default_factory=list)
    adverse_events: List[Dict[str, Any]] = field(default_factory=list)
    phenotype_signature: Optional[str] = None
    response_classification: str = "UNKNOWN"
    early_risk_signals: List[RiskSignal] = field(default_factory=list)
    last_updated: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def __post_init__(self):
        if self.primary_condition and not self.presenting_condition:
            self.presenting_condition = self.primary_condition
        elif self.presenting_condition and not self.primary_condition:
            self.primary_condition = self.presenting_condition

        if self.age or self.gender or self.baseline_vitals:
            if not self.demographics:
                self.demographics = {
                    "age": self.age,
                    "gender": self.gender,
                    "vitals": self.baseline_vitals
                }

    def add_symptom(
        self,
        symptom_name: str,
        severity_vas: float,
        duration_days: int = 1,
        onset_date: str = "",
        notes: Optional[str] = None
    ) -> None:
        if not onset_date:
            onset_date = datetime.date.today().isoformat()
        self.symptoms.append(
            SymptomObservation(
                symptom_name=symptom_name,
                severity_vas=severity_vas,
                duration_days=duration_days,
                onset_date=onset_date,
                notes=notes
            )
        )

    def add_biomarker_delta(
        self,
        marker_name: str,
        baseline_value: float,
        current_value: float,
        unit: str,
        is_lower_better: bool = True
    ) -> None:
        self.biomarkers.append(
            FunctionalBiomarkerDelta(
                marker_name=marker_name,
                baseline_value=baseline_value,
                current_value=current_value,
                unit=unit,
                is_lower_better=is_lower_better,
                last_tested_date=datetime.date.today().isoformat()
            )
        )

    def add_mizaj_record(
        self,
        dominant_mizaj: str,
        hot_score: float = 0.5,
        cold_score: float = 0.5,
        wet_score: float = 0.5,
        dry_score: float = 0.5,
        mizaj_divergence_index: float = 0.0
    ) -> None:
        self.mizaj_history.append(
            MizajStateRecord(
                timestamp=datetime.datetime.utcnow().isoformat() + "Z",
                dominant_mizaj=dominant_mizaj,
                heat_degree=int(hot_score * 4) or 2,
                cold_degree=int(cold_score * 4) or 2,
                dry_degree=int(dry_score * 4) or 2,
                moist_degree=int(wet_score * 4) or 2,
                dyscrasia=f"Divergence: {mizaj_divergence_index}"
            )
        )

    def add_organ_axis_score(self, axis_name: str, pathology_score: float, is_compromised: bool = True) -> None:
        self.organ_axis_scores[axis_name] = pathology_score

    def add_nuskha_record(
        self,
        nuskha_id: str,
        drugs: List[str],
        start_date: Optional[str] = None,
        clinician_approved_by: Optional[str] = None
    ) -> None:
        comp = [{"drug": d, "posology": "Standard therapeutic dose"} for d in drugs]
        self.nuskha_history.append({
            "nuskha_id": nuskha_id,
            "composition": comp,
            "start_date": start_date or datetime.date.today().isoformat(),
            "clinician_approved_by": clinician_approved_by,
        })

    def add_posology_adherence(self, period_days: int, doses_prescribed: int, doses_taken: int) -> None:
        if doses_prescribed > 0:
            rate = round((doses_taken / doses_prescribed) * 100.0, 1)
        else:
            rate = 100.0
        self.update_adherence(rate)

    def add_lifestyle_record(self, season: str, diet_category: str, regimen: str, adherence: float = 0.8) -> None:
        self.lifestyle_parameters = {
            "season": season,
            "diet": diet_category,
            "regimen": regimen,
            "lifestyle_adherence": adherence
        }

    def add_outcome_record(
        self,
        outcome_type: str,
        improvement_percent: float,
        classical_term: Optional[str] = None
    ) -> None:
        self.outcome_trajectory.append({
            "outcome_type": outcome_type,
            "vas_improvement_percent": improvement_percent,
            "classical_term": classical_term or outcome_type,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        })
        if outcome_type in ("KAMIL", "Shifa-e-Kamil") or improvement_percent >= 70.0:
            self.response_classification = "RESPONDER"

    def add_adverse_event(self, suspected_drug: str, reaction: str, severity: str = "MILD") -> None:
        self.adverse_events.append({
            "suspected_drug": suspected_drug,
            "reaction": reaction,
            "severity": severity,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        })
        if severity in ("SEVERE", "LIFE_THREATENING"):
            self.response_classification = "INTOLERANT"

    def update_adherence(self, rate: float) -> None:
        """Updates posology adherence and generates risk signals if adherence drops."""
        self.adherence_percentage = max(0.0, min(100.0, rate))
        if self.adherence_percentage < 60.0:
            self.early_risk_signals.append(
                RiskSignal(
                    signal_id=f"SIG-ADH-{len(self.early_risk_signals)+1:03d}",
                    signal_type="ADHERENCE_DROP",
                    severity="ELEVATED",
                    trigger_detail=f"Medication possession ratio fell to {self.adherence_percentage}%. Risk of treatment non-responsiveness.",
                    detected_at=datetime.datetime.utcnow().isoformat() + "Z",
                    requires_clinician_review=True,
                )
            )

    def synthesize_longitudinal_summary(self) -> Dict[str, Any]:
        """
        Synthesizes the 5 core precision health vectors:
        1. What was tried
        2. What changed
        3. What did not change
        4. What caused adverse effects
        5. What worked for which phenotype
        """
        # 1. What was tried
        tried_drugs = set()
        for n in self.nuskha_history:
            for item in n.get("composition", []):
                d = item.get("drug") or item.get("name")
                if d:
                    tried_drugs.add(d)

        # 2. What changed
        improved_symptoms = []
        improved_markers = []
        for b in self.biomarkers:
            if b.is_improved:
                improved_markers.append(f"{b.marker_name} ({b.baseline_value} -> {b.current_value} {b.unit}, {b.percentage_change}%)")

        for o in self.outcome_trajectory:
            if o.get("vas_improvement_percent", 0.0) >= 30.0:
                improved_symptoms.append(f"Pain VAS improved by {o.get('vas_improvement_percent')}%")

        # 3. What did not change
        unchanged_markers = [
            f"{b.marker_name} (still at {b.current_value} {b.unit})"
            for b in self.biomarkers if not b.is_improved and abs(b.percentage_change) < 5.0
        ]

        # 4. What caused adverse effects
        adverse_drugs = [
            f"{ae.get('suspected_drug')} causing {ae.get('reaction')} (Severity: {ae.get('severity')})"
            for ae in self.adverse_events
        ]

        # 5. What worked for which phenotype
        successful_interventions = []
        eff_mizaj = self.mizaj_history[-1].dominant_mizaj if self.mizaj_history else "Undetermined"
        if self.response_classification in ("RESPONDER", "KAMIL") or any(o.get("vas_improvement_percent", 0.0) >= 70.0 for o in self.outcome_trajectory):
            for n in self.nuskha_history:
                drugs = [i.get("drug") for i in n.get("composition", []) if i.get("drug")]
                successful_interventions.append(f"Protocol [{', '.join(drugs)}] for Phenotype [{self.phenotype_signature or eff_mizaj}]")

        longitudinal_answers = {
            "what_was_tried": {
                "prescribed_drugs": list(tried_drugs),
                "adherence_rate_pct": self.adherence_percentage,
                "nuskha_count": len(self.nuskha_history),
            },
            "what_changed": {
                "improved_biomarkers": improved_markers,
                "symptom_relief_achieved": len(improved_symptoms) > 0 or any(o.get("vas_improvement_percent", 0.0) >= 30.0 for o in self.outcome_trajectory),
                "details": improved_symptoms + improved_markers,
            },
            "what_did_not_change": unchanged_markers,
            "what_caused_adverse_effects": adverse_drugs,
            "what_worked_for_phenotype": {
                "effective_for_mizaj": eff_mizaj,
                "phenotype_signature": self.phenotype_signature,
                "successful_interventions": successful_interventions,
            },
        }

        return {
            "patient_id": self.patient_id,
            "primary_condition": self.primary_condition or self.presenting_condition,
            "phenotype": self.phenotype_signature or "UNCLASSIFIED_PHENOTYPE",
            "current_response": self.response_classification,
            "adherence_rate": f"{self.adherence_percentage}%",
            "what_was_tried": list(tried_drugs),
            "what_changed": improved_symptoms + improved_markers,
            "what_did_not_change": unchanged_markers,
            "what_caused_adverse_effects": adverse_drugs,
            "what_worked_for_phenotype": successful_interventions,
            "active_risk_signals": [asdict(s) for s in self.early_risk_signals],
            "longitudinal_trajectory_answers": longitudinal_answers,
        }


class PrecisionPatientModelEngine:
    """Coordinator engine managing patient precision profiles."""

    _PATIENT_MODELS: Dict[str, PrecisionPatientModel] = {}

    @classmethod
    def get_or_create_model(
        cls,
        patient_id: str,
        demographics: Optional[Dict[str, Any]] = None,
        condition: str = "General Malaise",
    ) -> PrecisionPatientModel:
        if patient_id not in cls._PATIENT_MODELS:
            cls._PATIENT_MODELS[patient_id] = PrecisionPatientModel(
                patient_id=patient_id,
                demographics=demographics or {"name": "Patient", "age": 45, "gender": "UNKNOWN"},
                presenting_condition=condition,
            )
        return cls._PATIENT_MODELS[patient_id]

    @classmethod
    def reset_registry(cls) -> None:
        cls._PATIENT_MODELS.clear()
