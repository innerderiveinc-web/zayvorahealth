"""
ZAYVORA Health OS™ — Care Gap & Adherence Intelligence Engine
============================================================
Reference:
  - Book 2: ZAYVORA Clinical Handbook (Continuous Care & Regimen Compliance)
  - Purpose: Proactively detects gaps between expected care continuum and actual patient events:
      1. Missed clinical follow-up windows
      2. Overdue monitoring laboratory investigations
      3. Imminent medication exhaustion & refill gaps
      4. Regimen adherence deficits with root-cause insights
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
import datetime


class CareGapSeverity:
    URGENT = "URGENT"
    WARNING = "WARNING"
    ADVISORY = "ADVISORY"


@dataclass
class CareGapItem:
    gap_id: str
    gap_type: str
    title: str
    severity: str
    description: str
    days_overdue: int
    potential_root_causes: List[str]
    recommended_clinical_action: str
    auto_triggerable_action: str
    detected_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


@dataclass
class PatientCareGapSummary:
    patient_id: str
    patient_name: str
    total_gaps_count: int
    urgent_count: int
    warning_count: int
    advisory_count: int
    overall_adherence_pct: float
    gaps: List[CareGapItem]
    care_continuity_index: float  # 0.0 - 1.0


class CareGapIntelligenceEngine:
    """
    Evaluates patient longitudinal record against protocol milestones
    to detect continuum gaps and formulate clinician intervention strategies.
    """

    @classmethod
    def evaluate_patient_care_gaps(
        cls,
        patient_id: str,
        patient_name: str,
        active_protocol_id: str = "PROT-METABOLIC-RESET-90",
        current_day_in_protocol: int = 24,
        last_consultation_date: Optional[str] = None,
        last_refill_date: Optional[str] = None,
        days_supply_issued: int = 21,
        labs_completed: Optional[List[str]] = None,
        reported_adherence_pct: float = 76.5
    ) -> PatientCareGapSummary:
        labs_completed = labs_completed or []
        gaps: List[CareGapItem] = []

        # 1. Check Missed Follow-up Gap
        # In 90-day protocols, Day 21 is a mandatory interim checkpoint
        if current_day_in_protocol > 21:
            days_past = current_day_in_protocol - 21
            gaps.append(CareGapItem(
                gap_id=f"GAP-FU-{patient_id}-D21",
                gap_type="MISSED_FOLLOW_UP",
                title="Protocol Day 21 Interim Review Overdue",
                severity=CareGapSeverity.WARNING if days_past <= 5 else CareGapSeverity.URGENT,
                description=f"Day 21 therapeutic milestone check-in is overdue by {days_past} days.",
                days_overdue=days_past,
                potential_root_causes=[
                    "Patient perceived symptom improvement and assumed early cessation",
                    "Difficulty attending clinic in person (tele-consult candidate)",
                    "Communication gap regarding protocol milestone significance"
                ],
                recommended_clinical_action="Initiate tele-consultation check-in or send WhatsApp appointment booking link.",
                auto_triggerable_action="SEND_WHATSAPP_FOLLOWUP_REMINDER"
            ))

        # 2. Check Overdue Biomarker / Lab Monitoring
        required_d21_labs = ["hs-CRP", "ESR", "Serum Uric Acid"]
        missing_labs = [lab for lab in required_d21_labs if not any(lab.lower() in l.lower() for l in labs_completed)]
        if missing_labs and current_day_in_protocol >= 21:
            gaps.append(CareGapItem(
                gap_id=f"GAP-LAB-{patient_id}-D21",
                gap_type="OVERDUE_DIAGNOSTICS",
                title=f"Pending Monitoring Labs ({', '.join(missing_labs)})",
                severity=CareGapSeverity.WARNING,
                description=f"Protocol requires Day 21 inflammatory monitoring: {', '.join(missing_labs)} are pending.",
                days_overdue=current_day_in_protocol - 21,
                potential_root_causes=[
                    "Phlebotomy scheduling delay",
                    "Cost sensitivity or uncollected sample",
                    "Patient unaware of fasting requirements"
                ],
                recommended_clinical_action="Dispatch home phlebotomy order or send lab requisition reminder.",
                auto_triggerable_action="DISPATCH_HOME_LAB_REQUISITION"
            ))

        # 3. Check Imminent Medicine Exhaustion / Refill Gap
        days_remaining = days_supply_issued - current_day_in_protocol
        if days_remaining <= 3:
            gaps.append(CareGapItem(
                gap_id=f"GAP-REFILL-{patient_id}-PHARM",
                gap_type="MEDICINE_DEPLETION_RISK",
                title="Active Formulation Supply Imminently Depleted",
                severity=CareGapSeverity.URGENT if days_remaining <= 0 else CareGapSeverity.WARNING,
                description=(
                    f"Prescribed 21-day medication pack exhausted {abs(days_remaining)} days ago."
                    if days_remaining < 0 else
                    f"Only {days_remaining} days of formulation remaining; reorder not yet confirmed."
                ),
                days_overdue=max(0, -days_remaining),
                potential_root_causes=[
                    "Patient forgot to trigger reorder",
                    "Courier transit buffer delay",
                    "Financial constraint or lack of payment confirmation"
                ],
                recommended_clinical_action="Verify pharmacist FEFO stock allocation and prompt patient for seamless reorder.",
                auto_triggerable_action="PROMPT_PHARMACY_REORDER"
            ))

        # 4. Check Adherence Deficit (< 80%)
        if reported_adherence_pct < 80.0:
            gaps.append(CareGapItem(
                gap_id=f"GAP-ADH-{patient_id}-REGIMEN",
                gap_type="ADHERENCE_DEFICIT",
                title=f"Regimen Adherence Below Therapeutic Threshold ({reported_adherence_pct}%)",
                severity=CareGapSeverity.WARNING,
                description=f"Patient adherence is currently {reported_adherence_pct}%, falling short of the 85% target.",
                days_overdue=0,
                potential_root_causes=[
                    "Regimen complexity (multiple doses across morning/evening)",
                    "Taste / palatability of unrefined herbal powder or decoction",
                    "Mild gastric discomfort or digestive heaviness"
                ],
                recommended_clinical_action="Simplify dosing schedule or switch unrefined powder to honey-bound Majun or enteric capsules.",
                auto_triggerable_action="CLINICIAN_DOSING_OPTIMIZATION_ALERT"
            ))

        urgent_c = sum(1 for g in gaps if g.severity == CareGapSeverity.URGENT)
        warning_c = sum(1 for g in gaps if g.severity == CareGapSeverity.WARNING)
        advisory_c = sum(1 for g in gaps if g.severity == CareGapSeverity.ADVISORY)

        # Compute Continuity Index (1.0 = perfect compliance, drops with gaps)
        continuity_penalty = (urgent_c * 0.20) + (warning_c * 0.10) + (advisory_c * 0.05)
        continuity_idx = max(0.20, round(1.0 - continuity_penalty, 2))

        return PatientCareGapSummary(
            patient_id=patient_id,
            patient_name=patient_name,
            total_gaps_count=len(gaps),
            urgent_count=urgent_c,
            warning_count=warning_c,
            advisory_count=advisory_c,
            overall_adherence_pct=reported_adherence_pct,
            gaps=gaps,
            care_continuity_index=continuity_idx
        )
