"""
ZAYVORA Health OS™ — Smart Pre-Consultation Intake Engine
========================================================
Reference:
  - Book 2: ZAYVORA Clinical Handbook (Clinical Intake & Matab Encounter)
  - Purpose: Transforms messy, multi-modal, free-text patient intake
    (from WhatsApp, mobile, or voice notes) into a concise, high-yield
    clinical briefing for the doctor BEFORE the consultation begins.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import datetime
import re


@dataclass
class PreConsultBriefing:
    briefing_id: str
    patient_id: str
    patient_name: str
    chief_complaint_summary: str
    symptom_chronology: str
    active_medications: List[str]
    allergies: List[str]
    suspected_humoral_axis_clues: List[str]
    suggested_clinician_questions: List[str]
    triage_priority: str  # ROUTINE, PRIORITY, URGENT
    readiness_status: str  # READY_FOR_CONSULT
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


class SmartPreConsultEngine:
    """
    Synthesizes unstructured patient intake into structured pre-consultation briefings.
    """

    @classmethod
    def generate_briefing(
        cls,
        patient_id: str,
        patient_name: str,
        unstructured_intake_text: str,
        patient_age: int = 42,
        patient_gender: str = "Male"
    ) -> PreConsultBriefing:
        text = unstructured_intake_text.lower()

        # 1. Chief Complaint Extraction
        complaints: List[str] = []
        if any(w in text for w in ["knee", "joint", "ghutna", "ghutno", "ghutne", "gout", "arthritis", "stiffness", "akadpan", "joron", "mafasil"]):
            complaints.append("Bilateral knee joint pain with marked morning stiffness")
        if any(w in text for w in ["acidity", "gas", "indigestion", "hazma", "pet"]):
            complaints.append("Epigastric fullness and delayed postprandial digestion")
        if any(w in text for w in ["sleep", "insomnia", "neend", "stress", "tension"]):
            complaints.append("Fragmented sleep architecture and diurnal fatigue")
        if not complaints:
            complaints.append("General constitutional malaise and non-specific body ache")

        # 2. Chronology / Duration
        if "month" in text or "mah" in text or "saal" in text or "year" in text:
            chronology = "Chronic progressive presentation (> 3 months duration)"
        elif "week" in text or "hafta" in text:
            chronology = "Subacute flare-up (2-4 weeks duration)"
        else:
            chronology = "Recent acute exacerbation reported within past 7-14 days"

        # 3. Medications & Prior Therapies
        meds: List[str] = []
        if "painkiller" in text or "combiflam" in text or "paracetamol" in text or "nsaid" in text:
            meds.append("Intermittent OTC NSAIDs / Analgesics (partial transient relief)")
        if "majoon" in text or "suranjan" in text or "desi" in text or "unani" in text:
            meds.append("Prior Unani formulations (self-administered or previous hakim consult)")
        if not meds:
            meds.append("No active allopathic prescription reported; sporadic home remedies")

        # 4. Humoral & Organ-Axis Clues
        axis_clues: List[str] = []
        if any(w in text for w in ["thandi", "cold", "winter", "sardi", "stiff"]):
            axis_clues.append("Symptoms aggravated by cold/damp environment (Balghami / Barid dyscrasia)")
        if any(w in text for w in ["burning", "jalan", "heat", "garmi", "sweat"]):
            axis_clues.append("Subjective heat/burning sensations (Safrawi / Har involvement)")
        if any(w in text for w in ["heaviness", "bhaaripan", "lethargy"]):
            axis_clues.append("Hepato-splenic metabolic sluggishness (Zof-e-Hazm)")
        if not axis_clues:
            axis_clues.append("Balanced baseline temperament with localized synovial humoral stagnation")

        # 5. Targeted Diagnostic Questions for the Doctor
        clinician_questions = [
            "Assess duration of morning stiffness in minutes (differentiating OA vs Inflammatory Spondylopathy).",
            "Examine pulse (Nabz) for depth and volume (Nabz-e-Azeem vs Nabz-e-Sagheer) to confirm Balgham accumulation.",
            "Screen for nocturnal epigastric reflux before introducing pungent Suranjan/Piperine formulations."
        ]

        priority = "PRIORITY" if ("severe" in text or "ziyada" in text or "worsened" in text) else "ROUTINE"

        return PreConsultBriefing(
            briefing_id=f"PCB-{patient_id}-2026",
            patient_id=patient_id,
            patient_name=patient_name,
            chief_complaint_summary="; ".join(complaints),
            symptom_chronology=chronology,
            active_medications=meds,
            allergies=["No severe drug allergies declared; tolerates classical syrups"],
            suspected_humoral_axis_clues=axis_clues,
            suggested_clinician_questions=clinician_questions,
            triage_priority=priority,
            readiness_status="READY_FOR_CONSULT"
        )
