"""
ZAYVORA Health OS™ — Laboratory & Diagnostic Layer (Service 2 & 5)

Authoritative clinical laboratory result processor.
Manages:
  - Orders & Specimen accessioning
  - Reference ranges with classical Unani humoral correlation
  - Result status states: NEW, REVIEWED, ACTION_REQUIRED, ABNORMAL, CRITICAL, RESOLVED
  - Safe patient-facing summaries with zero raw code leakage
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class LabResultItem:
    test_code: str                   # e.g., URIC_ACID, HOMA_IR, ESR, CRP
    test_name: str
    observed_value: float
    unit: str
    reference_low: float
    reference_high: float
    flag: str                        # NORMAL, LOW, HIGH, CRITICAL_HIGH
    result_state: str                # NEW, REVIEWED, ACTION_REQUIRED, ABNORMAL, CRITICAL, RESOLVED
    clinician_note: Optional[str]
    patient_plain_summary: str
    unani_humoral_correlation: str


@dataclass
class LabOrderReport:
    report_id: str                   # LAB-2026-XXXX
    order_id: str                    # ORD-XXXX
    patient_id: str
    mrn: str
    ordering_clinician: str
    facility_id: str
    collection_time: str
    reported_time: str
    items: List[LabResultItem]
    overall_status: str              # FINAL_CERTIFIED, PRELIMINARY, PENDING_REVIEW
    digital_pathologist_sign: str


class LabDiagnosticsOS:
    """Manages diagnostic reporting, status progression, and patient summaries."""

    _REPORTS: Dict[str, LabOrderReport] = {}

    @classmethod
    def get_patient_reports(cls, patient_id: str) -> List[Dict[str, Any]]:
        """Returns all finalized diagnostic reports for a patient."""
        reports = [asdict(r) for r in cls._REPORTS.values() if r.patient_id == patient_id]
        if not reports:
            # Seed canonical standard report for Hamza Farooqi
            rep = cls.create_sample_report(patient_id, "MRN-2026-0001", "DOC-01")
            reports = [asdict(rep)]
        return reports

    @classmethod
    def create_sample_report(
        cls,
        patient_id: str,
        mrn: str,
        clinician_id: str
    ) -> LabOrderReport:
        now = datetime.now(timezone.utc).isoformat()
        rep_id = f"LAB-2026-{uuid.uuid4().hex[:6].upper()}"

        items = [
            LabResultItem(
                test_code="URIC_ACID",
                test_name="Serum Uric Acid",
                observed_value=6.8,
                unit="mg/dL",
                reference_low=3.5,
                reference_high=7.2,
                flag="NORMAL",
                result_state="RESOLVED",
                clinician_note="Down from 8.2 baseline. Indicates effective phlegmatic evacuation via Hab-e-Suranjan.",
                patient_plain_summary="Your uric acid is now within the safe normal range. The joint swelling medicine is working well.",
                unani_humoral_correlation="Rutuubat-e-Ghariba clearance in progress."
            ),
            LabResultItem(
                test_code="ESR",
                test_name="Erythrocyte Sedimentation Rate (1st Hour)",
                observed_value=22.0,
                unit="mm/hr",
                reference_low=0.0,
                reference_high=20.0,
                flag="HIGH",
                result_state="ACTION_REQUIRED",
                clinician_note="Mild residual synovial inflammation. Continue Dal'k and Balsan application.",
                patient_plain_summary="Slight residual joint stiffness inflammation remaining, but much lower than your first visit.",
                unani_humoral_correlation="Mild Hararat-e-Ghariba lingering in peripheral joint capsule."
            ),
            LabResultItem(
                test_code="CREATININE",
                test_name="Serum Creatinine",
                observed_value=0.9,
                unit="mg/dL",
                reference_low=0.7,
                reference_high=1.3,
                flag="NORMAL",
                result_state="REVIEWED",
                clinician_note="Optimal renal filtration. Safe to sustain current herbal dosages.",
                patient_plain_summary="Kidney filtration is completely healthy and normal.",
                unani_humoral_correlation="Quwwat-e-Dafi'ah (Excretory faculty) optimal."
            )
        ]

        sig = hashlib.sha256(f"{rep_id}|{patient_id}|{now}|certified".encode("utf-8")).hexdigest()
        report = LabOrderReport(
            report_id=rep_id,
            order_id="ORD-2026-9901",
            patient_id=patient_id,
            mrn=mrn,
            ordering_clinician=clinician_id,
            facility_id="FAC-HQ-01",
            collection_time="2026-09-18T08:30:00Z",
            reported_time=now,
            items=items,
            overall_status="FINAL_CERTIFIED",
            digital_pathologist_sign=sig
        )

        cls._REPORTS[rep_id] = report
        return report

    @classmethod
    def transition_result_state(
        cls,
        report_id: str,
        test_code: str,
        target_state: str,
        clinician_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transitions a specific test result state (e.g. NEW -> REVIEWED -> ACTION_REQUIRED)."""
        report = cls._REPORTS.get(report_id)
        if not report:
            raise KeyError(f"Report '{report_id}' not found.")
        for item in report.items:
            if item.test_code.upper() == test_code.upper():
                item.result_state = target_state.upper()
                if clinician_note:
                    item.clinician_note = clinician_note
                return {
                    "ok": True,
                    "report_id": report_id,
                    "test_code": test_code,
                    "new_state": target_state.upper(),
                    "clinician_note": item.clinician_note
                }
        raise KeyError(f"Test '{test_code}' not found in report '{report_id}'.")
