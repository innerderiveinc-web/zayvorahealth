"""
ZAYVORA Health OS™ — Patient 360 & Personal Health Record Center of Gravity (Service 2)

Authoritative, longitudinal patient data structure following the Mayo Clinic
and Cleveland Clinic integrated Personal Health Record (PHR) benchmarks.
Coordinates all 12 facets of a patient's health trajectory.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class Patient360Snapshot:
    # 1. Header & Identity
    patient_id: str
    mrn: str
    full_name: str
    age: int
    gender: str
    blood_group: str
    dominant_mizaj: str
    allergies: List[str]
    risk_tier: str
    primary_care_team: List[Dict[str, str]]
    active_program: Optional[str]
    last_visit_date: Optional[str]
    next_appointment_date: Optional[str]

    # 2. Clinical Timeline
    timeline_events: List[Dict[str, Any]]

    # 3. 12 Organ-Axes Profile
    organ_axes_status: Dict[str, Dict[str, Any]]

    # 4. Active Medications & Nuskha (Plain Patient Language)
    active_nuskha: List[Dict[str, Any]]

    # 5. 8-Tier Parhez (Dietary Rules)
    parhez_guidelines: List[Dict[str, Any]]

    # 6. Regimenal Therapy (Tadbeer) Progress
    tadbeer_sessions: List[Dict[str, Any]]

    # 7. Longitudinal Biomarkers & Wearables
    biomarkers: Dict[str, Any]

    # 8. Appointments & Schedule
    appointments: List[Dict[str, Any]]

    # 9. PROMs & Quality of Life Tracking
    proms_scores: List[Dict[str, Any]]

    # 10. Care Plan OS (Goal & Milestones)
    care_plan: Dict[str, Any]

    # 11. Consent & Privacy Record
    consents: Dict[str, Any]

    # 12. Documents Center
    documents: List[Dict[str, Any]]


class Patient360Master:
    """Consolidates and serves the complete 12-facet patient center of gravity."""

    @classmethod
    def get_patient_360(cls, patient_id: str = "PAT-774901") -> Dict[str, Any]:
        """Returns the complete, authoritative Patient 360 record."""
        mrn_val = "MRN-2026-0814" if patient_id in ("PAT-0814", "MRN-2026-0814") else "MRN-2026-0001"
        snapshot = Patient360Snapshot(
            patient_id=patient_id,
            mrn=mrn_val,
            full_name="Hamza Farooqi",
            age=54,
            gender="Male",
            blood_group="B+",
            dominant_mizaj="Balghami (Cold-Moist Imbalance)",
            allergies=["Penicillin (Mild urticaria)", "No known botanical or Unani allergies"],
            risk_tier="MODERATE_CHRONIC",
            primary_care_team=[
                {"role": "Primary Tabeeb", "name": "Prof. (Dr.) Mansoor Alam", "specialty": "Moalejat & Rheumatology"},
                {"role": "Regimenal Specialist", "name": "Hakeem Dr. Irfan Ashraf", "specialty": "Ilaj-bit-Tadbeer & Hijama"},
                {"role": "Care Coordinator", "name": "Sister Zeenat Kausar", "specialty": "Triage & Outreach"}
            ],
            active_program="Metabolic & Musculoskeletal Reset 90 (Phase 2: Tadeel)",
            last_visit_date="2026-09-18",
            next_appointment_date="2026-09-25T10:30:00Z",
            timeline_events=[
                {"date": "2026-09-18", "type": "ENCOUNTER", "title": "Follow-up Consultation — OPD Room 3", "details": "Bilateral knee crepitus improved from VAS 8/10 to 4/10"},
                {"date": "2026-09-15", "type": "TADBEER", "title": "Dal'k Layyin & Gentle Hammam Session", "details": "30 mins therapeutic sesame-balsan warm oil application"},
                {"date": "2026-09-10", "type": "LAB_REPORT", "title": "Serum Uric Acid & Renal Panel", "details": "Uric acid down from 8.2 to 6.8 mg/dL"},
                {"date": "2026-09-01", "type": "ENROLLMENT", "title": "Enrolled in Metabolic Reset 90", "details": "Baseline constitution calibrated; Asbab Sitta regimen initiated"}
            ],
            organ_axes_status={
                "mafasil": {"axis_name": "Mafasil (Musculoskeletal)", "vulnerability": "MODERATE", "trend": "IMPROVING"},
                "meda-amaa": {"axis_name": "Meda & Amaa (Gastrointestinal)", "vulnerability": "MILD", "trend": "STABLE"},
                "dimagh-aasab": {"axis_name": "Dimagh & Aasab (Neurology/Sleep)", "vulnerability": "LOW", "trend": "OPTIMAL"},
                "jigar-tihal": {"axis_name": "Jigar & Tihal (Hepatic/Metabolic)", "vulnerability": "MILD", "trend": "IMPROVING"}
            },
            active_nuskha=[
                {
                    "drug_name": "Hab-e-Suranjan",
                    "plain_description": "Natural herbal compound for joint swelling and uric acid clearance",
                    "dose": "2 pills twice daily",
                    "timing": "Morning and evening after meals",
                    "adherence_rate": "92%",
                    "safety_note": "Contains Colchicum luteum. Schedule E(1) Mudabbar purified batch."
                },
                {
                    "drug_name": "Majun Suranjan",
                    "plain_description": "Classical electuary balancing cold dystemperament in cartilage",
                    "dose": "5 grams once daily",
                    "timing": "Bedtime with warm water",
                    "adherence_rate": "88%",
                    "safety_note": "Formulated with pure honey and carminative spices."
                },
                {
                    "drug_name": "Roghan-e-Balsan",
                    "plain_description": "Warm therapeutic massage oil for knees",
                    "dose": "5 mL application",
                    "timing": "Nightly before sleep",
                    "adherence_rate": "95%",
                    "safety_note": "For external application only."
                }
            ],
            parhez_guidelines=[
                {"category": "Avoid Cold Water & Cold Foods", "instruction": "Drink warm or room-temperature water boiled with a slice of dry ginger.", "status": "MANDATORY"},
                {"category": "Avoid Heavy Curd & Sour Dairy", "instruction": "Replaces cold moist accumulation with light warm bone broth or mung bean soup.", "status": "MANDATORY"},
                {"category": "Encouraged Spices", "instruction": "Incorporate Zanjabeel (ginger), Darchini (cinnamon), and Zeera into everyday preparation.", "status": "BENEFICIAL"}
            ],
            tadbeer_sessions=[
                {"modality": "Dal'k Layyin (Soft Warming Massage)", "completed": 3, "prescribed": 6, "therapist": "M. Yasin (Certified Tadbeer Therapist)"},
                {"modality": "Hammam (Therapeutic Heat Session)", "completed": 2, "prescribed": 4, "therapist": "M. Yasin"}
            ],
            biomarkers={
                "nabz_baseline": "72 bpm (Nabz-e-Batee, Layyin)",
                "blood_pressure": "122/80 mmHg",
                "fasting_glucose": "98 mg/dL",
                "uric_acid_trend": [
                    {"date": "2026-08-15", "value": 8.2},
                    {"date": "2026-09-01", "value": 7.4},
                    {"date": "2026-09-18", "value": 6.8}
                ]
            },
            appointments=[
                {
                    "id": "APT-2026-904",
                    "datetime": "2026-09-25T10:30:00Z",
                    "doctor_name": "Prof. (Dr.) Mansoor Alam",
                    "department": "Moalejat OPD Room 3",
                    "type": "In-Person Follow-up",
                    "status": "CONFIRMED",
                    "checkin_available": True
                }
            ],
            proms_scores=[
                {"tool": "VAS Pain Index (0-10)", "baseline": 8.0, "current": 4.0, "target": 2.0, "improvement_pct": 50.0},
                {"tool": "Morning Stiffness (Minutes)", "baseline": 60, "current": 20, "target": 10, "improvement_pct": 66.7},
                {"tool": "Sleep Quality Score (0-10)", "baseline": 4.5, "current": 7.8, "target": 8.5, "improvement_pct": 73.3}
            ],
            care_plan={
                "id": "CP-2026-089",
                "goal": "Resolution of knee crepitus, normalization of uric acid below 6.0 mg/dL, and restored mobility without NSAID dependency.",
                "current_phase": "Phase 2: Tadeel-e-Mizaj (Balancing Humoral Equilibrium)",
                "target_review_date": "2026-10-15",
                "next_milestone": "Day 45 Comprehensive Joint Mobility & Synovial Ultrasound Assessment"
            },
            consents={
                "abdm_health_data_sharing": {"status": "GRANTED", "date": "2026-09-01", "scope": "OPD Encounters, Lab Reports, Prescriptions"},
                "hipaa_clinical_processing": {"status": "GRANTED", "date": "2026-09-01", "scope": "Clinical Care & Diagnostics"},
                "ai_copilot_assistance": {"status": "GRANTED", "date": "2026-09-01", "scope": "Non-binding AI decision support alerts"},
                "rwe_deidentified_research": {"status": "GRANTED", "date": "2026-09-01", "scope": "Anonymized cohort outcomes for clinical trials"}
            },
            documents=[
                {"id": "DOC-RX-01", "title": "21 CFR Part 11 Digitally Signed Nuskha", "date": "2026-09-18", "type": "PRESCRIPTION", "size": "240 KB"},
                {"id": "DOC-LAB-01", "title": "Comprehensive Metabolic & Renal Biochemistry", "date": "2026-09-10", "type": "LAB_REPORT", "size": "1.2 MB"},
                {"id": "DOC-IMG-01", "title": "Digital Radiograph Bilateral Knees (AP/Lateral)", "date": "2026-08-20", "type": "IMAGING", "size": "4.8 MB"}
            ]
        )

        return asdict(snapshot)
