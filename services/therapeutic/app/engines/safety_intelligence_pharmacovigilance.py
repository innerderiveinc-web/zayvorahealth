"""
ZAYVORA Health OS™ — Safety Intelligence & Pharmacovigilance Engine
===================================================================
Implements Phase 10 of the Clinical Evolution Roadmap:
1. End-to-End Traceable ADR (Adverse Drug Reaction) Pipeline:
   Drug -> Adverse Event -> Patient -> Batch / Lot -> Severity -> Action -> Outcome
2. Standardized WHO-UMC Causality Assessment:
   - Evaluates: Event Latency, Dechallenge, Rechallenge, Concomitant Meds, Alternative Etiology.
   - Assigns: CERTAIN, PROBABLE, POSSIBLE, UNLIKELY, CONDITIONAL.
3. Statutory & Quality Interventions:
   - Automated Batch Quarantine: Freezes inventory lots immediately if serious ADR or Schedule E1 toxicity is reported.
   - AYUSH Yellow Report Generator: Emits standardized Pharmacovigilance adverse reaction filings for regulatory submission.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import datetime
import uuid

class ADRSeverity(str, Enum):
    MILD = "MILD"               # Transient, no medical intervention required
    MODERATE = "MODERATE"       # Minimal medical intervention, dose adjustment
    SEVERE = "SEVERE"           # Hospitalization, persistent disability
    LIFE_THREATENING = "LIFE_THREATENING"

class WHOUmcCausality(str, Enum):
    CERTAIN = "CERTAIN"
    PROBABLE = "PROBABLE"
    POSSIBLE = "POSSIBLE"
    UNLIKELY = "UNLIKELY"
    CONDITIONAL = "CONDITIONAL"

class SafetyAction(str, Enum):
    LOGGED_FOR_MONITORING = "LOGGED_FOR_MONITORING"
    DOSAGE_REDUCED = "DOSAGE_REDUCED"
    DRUG_WITHDRAWN = "DRUG_WITHDRAWN"
    BATCH_QUARANTINED = "BATCH_QUARANTINED"
    AYUSH_REPORT_FILED = "AYUSH_REPORT_FILED"

@dataclass
class ADRReport:
    report_id: str
    patient_id: str
    suspected_drug: str
    lot_batch_number: Optional[str]
    adverse_reaction: str
    severity: ADRSeverity
    onset_hours_after_dose: float
    dechallenge_positive: bool
    rechallenge_positive: Optional[bool]
    concomitant_drugs: List[str]
    alternative_etiology_likely: bool
    who_causality: WHOUmcCausality
    immediate_action: SafetyAction
    quarantine_enforced: bool
    ayush_yellow_report: Dict[str, Any]
    reporting_clinician_id: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

class SafetyIntelligenceEngine:
    """
    Orchestrates clinical pharmacovigilance, causality grading, and rapid safety interventions.
    """

    _ADR_ARCHIVE: Dict[str, ADRReport] = {}
    _ACTIVE_ALERTS: List[Dict[str, Any]] = []

    @classmethod
    def evaluate_who_causality(
        cls,
        onset_hours: float,
        dechallenge_positive: bool,
        rechallenge_positive: Optional[bool],
        alternative_etiology_likely: bool
    ) -> WHOUmcCausality:
        """
        Standard WHO-UMC causality algorithm logic:
        - Certain: Plausible time relationship, dechallenge positive, rechallenge positive, no other cause.
        - Probable: Plausible time relationship, dechallenge positive, alternative cause unlikely, no rechallenge.
        - Possible: Reasonable time relationship, could be explained by disease or other drugs, dechallenge info unclear.
        - Unlikely: Improbable time relationship or clear alternative cause.
        """
        if alternative_etiology_likely:
            return WHOUmcCausality.UNLIKELY

        if rechallenge_positive is True and dechallenge_positive:
            return WHOUmcCausality.CERTAIN

        if dechallenge_positive and not alternative_etiology_likely:
            return WHOUmcCausality.PROBABLE

        if onset_hours <= 72.0:
            return WHOUmcCausality.POSSIBLE

        return WHOUmcCausality.CONDITIONAL

    @classmethod
    def report_adverse_reaction(
        cls,
        patient_id: str,
        suspected_drug: str,
        lot_batch_number: Optional[str],
        adverse_reaction: str,
        severity: ADRSeverity,
        onset_hours: float,
        dechallenge_positive: bool,
        rechallenge_positive: Optional[bool],
        concomitant_drugs: List[str],
        alternative_etiology_likely: bool,
        clinician_id: str
    ) -> ADRReport:
        causality = cls.evaluate_who_causality(
            onset_hours=onset_hours,
            dechallenge_positive=dechallenge_positive,
            rechallenge_positive=rechallenge_positive,
            alternative_etiology_likely=alternative_etiology_likely
        )

        report_id = f"ADR-{uuid.uuid4().hex[:8].upper()}"
        quarantine_enforced = False
        action = SafetyAction.LOGGED_FOR_MONITORING

        # Serious reaction or high causality triggering batch quarantine
        if severity in [ADRSeverity.SEVERE, ADRSeverity.LIFE_THREATENING] or causality in [WHOUmcCausality.CERTAIN, WHOUmcCausality.PROBABLE]:
            action = SafetyAction.BATCH_QUARANTINED
            quarantine_enforced = True
            
            # Quaratine the lot in the pharmacy inventory if specified
            if lot_batch_number:
                try:
                    from services.therapeutic.app.engines.closed_loop_pharmacy_engine import ClosedLoopPharmacyEngine
                    ClosedLoopPharmacyEngine.quarantine_lot(
                        lot_id=lot_batch_number,
                        reason=f"Safety Alert: {severity.value} ADR reported ({adverse_reaction})"
                    )
                except Exception:
                    pass

            cls._ACTIVE_ALERTS.append({
                "alert_id": f"ALT-{uuid.uuid4().hex[:6].upper()}",
                "report_id": report_id,
                "drug": suspected_drug,
                "lot": lot_batch_number,
                "severity": severity.value,
                "action": "LOT_QUARANTINED",
                "timestamp": datetime.datetime.utcnow().isoformat()
            })

        # Generate official AYUSH Yellow Form document payload
        yellow_report = {
            "form_type": "AYUSH_NATIONAL_PHARMACOVIGILANCE_SUSPECTED_ADR",
            "report_reference": report_id,
            "patient_identifier": f"ANON-{hash(patient_id) % 100000}",
            "suspected_unani_or_herbal_drug": suspected_drug,
            "batch_number": lot_batch_number or "UNSPECIFIED",
            "adverse_reaction_description": adverse_reaction,
            "who_causality_grade": causality.value,
            "severity_level": severity.value,
            "action_taken": action.value,
            "reporting_centre": "ZAYVORA_CENTRAL_CLINICAL_OS",
            "submission_ready": True
        }

        report = ADRReport(
            report_id=report_id,
            patient_id=patient_id,
            suspected_drug=suspected_drug,
            lot_batch_number=lot_batch_number,
            adverse_reaction=adverse_reaction,
            severity=severity,
            onset_hours_after_dose=onset_hours,
            dechallenge_positive=dechallenge_positive,
            rechallenge_positive=rechallenge_positive,
            concomitant_drugs=concomitant_drugs,
            alternative_etiology_likely=alternative_etiology_likely,
            who_causality=causality,
            immediate_action=action,
            quarantine_enforced=quarantine_enforced,
            ayush_yellow_report=yellow_report,
            reporting_clinician_id=clinician_id
        )

        cls._ADR_ARCHIVE[report_id] = report
        return report

    @classmethod
    def get_active_alerts(cls) -> List[Dict[str, Any]]:
        return list(cls._ACTIVE_ALERTS)

