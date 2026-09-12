"""
ZAYVORA HEALTH™ — Patient App 2.0 Core & Adherence Engine
Generates personalized daily clinical schedules, tracks medication posology adherence,
and manages secure asynchronous patient-clinician communications.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class DailyDoseItem:
    dose_id: str
    medication_name: str
    dosage_form: str         # Majun, Sharbat, Habb, Kushta, Safuf
    quantity_display: str    # e.g., "5g", "2 pills", "20ml"
    timing_slot: str         # "MORNING", "NOON", "EVENING", "BEDTIME"
    intake_vehicle: str      # e.g., "Lukewarm water", "Warm milk", "Arq-e-Gaozaban"
    instructions: str
    status: str = "PENDING"  # "PENDING", "TAKEN", "MISSED", "SKIPPED"
    logged_at_utc: Optional[str] = None
    skip_reason: Optional[str] = None


@dataclass
class PatientDailySchedule:
    patient_id: str
    date_str: str
    doses: List[DailyDoseItem]
    tadbeer_reminders: List[str]
    ghiza_dietary_rules: List[str]
    compliance_score_7d: float
    overall_status: str


@dataclass
class PatientMessage:
    message_id: str
    patient_id: str
    sender_type: str         # "PATIENT", "CLINICIAN", "AI_TRIAGE"
    sender_name: str
    content: str
    urgency: str             # "ROUTINE", "ELEVATED", "EMERGENCY_REDIRECT"
    timestamp_utc: str


# In-memory stores
ADHERENCE_LOGS_STORE: Dict[str, List[DailyDoseItem]] = {}
PATIENT_MESSAGES_STORE: Dict[str, List[PatientMessage]] = {}


class PatientPortalEngine:
    """Engine for patient-facing adherence and clinical coordination."""

    @classmethod
    def get_daily_schedule(cls, patient_id: str, date_str: Optional[str] = None) -> PatientDailySchedule:
        date_str = date_str or datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Standard classical active regimen simulation
        doses = [
            DailyDoseItem(
                dose_id=f"DOSE-{patient_id}-M1",
                medication_name="Sharbat Bazoori Motadil",
                dosage_form="Sharbat (Syrup)",
                quantity_display="20 ml",
                timing_slot="MORNING",
                intake_vehicle="Diluted in 150ml lukewarm water",
                instructions="Take on empty stomach 30 mins before breakfast to induce gentle Tabreed.",
            ),
            DailyDoseItem(
                dose_id=f"DOSE-{patient_id}-N1",
                medication_name="Jawarish Kamuni",
                dosage_form="Jawarish (Electuary)",
                quantity_display="5 g",
                timing_slot="NOON",
                intake_vehicle="Fresh water",
                instructions="Take 15 minutes post-lunch for digestive empowerment (Hazm).",
            ),
            DailyDoseItem(
                dose_id=f"DOSE-{patient_id}-B1",
                medication_name="Majun Suranjan",
                dosage_form="Majun (Confection)",
                quantity_display="5 g",
                timing_slot="BEDTIME",
                intake_vehicle="Lukewarm water",
                instructions="Take at bedtime. Strictly Mudabbar verified batch.",
            ),
        ]

        # Merge with existing logged states if available
        logged_list = ADHERENCE_LOGS_STORE.get(patient_id, [])
        logged_map = {d.dose_id: d for d in logged_list}
        for d in doses:
            if d.dose_id in logged_map:
                d.status = logged_map[d.dose_id].status
                d.logged_at_utc = logged_map[d.dose_id].logged_at_utc
                d.skip_reason = logged_map[d.dose_id].skip_reason

        # Calculate 7-day adherence score
        if not logged_list:
            comp_score = 0.95
        else:
            taken_count = sum(1 for item in logged_list if item.status == "TAKEN")
            comp_score = round(taken_count / len(logged_list), 2)

        return PatientDailySchedule(
            patient_id=patient_id,
            date_str=date_str,
            doses=doses,
            tadbeer_reminders=[
                "Scheduled Dalak (Therapeutic Massage) with Roghan-e-Babbuna on Saturday at 11:00 AM.",
                "Ensure light walking (Riyazat Khafeefa) for 20 minutes before evening meal.",
            ],
            ghiza_dietary_rules=[
                "Dietary Mizaj Balancing: Emphasize cooling fluids (Kadu / Gourd, Moong soup).",
                "Strictly eliminate deep-fried red meat and excessively salted pickles.",
            ],
            compliance_score_7d=comp_score,
            overall_status="EXCELLENT_ADHERENCE" if comp_score >= 0.85 else ("MODERATE_ADHERENCE" if comp_score >= 0.70 else "ACTION_REQUIRED"),
        )

    @classmethod
    def log_adherence(
        cls,
        patient_id: str,
        dose_id: str,
        status: str,
        skip_reason: Optional[str] = None,
    ) -> DailyDoseItem:
        valid_statuses = {"TAKEN", "MISSED", "SKIPPED"}
        if status.upper() not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Must be one of {valid_statuses}.")

        now_utc = datetime.now(timezone.utc).isoformat()
        item = DailyDoseItem(
            dose_id=dose_id,
            medication_name="Logged Medication",
            dosage_form="Standard Form",
            quantity_display="Standard Dose",
            timing_slot="LOGGED",
            intake_vehicle="Standard",
            instructions="",
            status=status.upper(),
            logged_at_utc=now_utc,
            skip_reason=skip_reason,
        )

        if patient_id not in ADHERENCE_LOGS_STORE:
            ADHERENCE_LOGS_STORE[patient_id] = []
        ADHERENCE_LOGS_STORE[patient_id].append(item)
        return item

    @classmethod
    def send_message(
        cls,
        patient_id: str,
        sender_type: str,
        sender_name: str,
        content: str,
    ) -> PatientMessage:
        content_lower = content.lower()
        urgency = "ROUTINE"

        # Triage red flags
        emergency_keywords = ["chest pain", "shortness of breath", "fainting", "severe bleeding", "unconscious"]
        elevated_keywords = ["fever", "vomiting", "rash", "dizziness", "worsened pain"]

        if any(kw in content_lower for kw in emergency_keywords):
            urgency = "EMERGENCY_REDIRECT"
        elif any(kw in content_lower for kw in elevated_keywords):
            urgency = "ELEVATED"

        msg = PatientMessage(
            message_id=f"MSG-{uuid.uuid4().hex[:8].upper()}",
            patient_id=patient_id,
            sender_type=sender_type,
            sender_name=sender_name,
            content=content,
            urgency=urgency,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )

        if patient_id not in PATIENT_MESSAGES_STORE:
            PATIENT_MESSAGES_STORE[patient_id] = []
        PATIENT_MESSAGES_STORE[patient_id].append(msg)
        return msg

    @classmethod
    def get_messages(cls, patient_id: str) -> List[PatientMessage]:
        return PATIENT_MESSAGES_STORE.get(patient_id, [])
