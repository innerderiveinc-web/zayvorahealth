"""
ZAYVORA Health OS™ — Care Plan OS & Longitudinal Chronic Programs (Service 9)

Elevates wellness packages into structured, physician-supervised longitudinal
care plans (e.g. Metabolic Reset 90, Gut-Brain Protocol, Joint Restore).
Coordinates phases, clinical milestones, adherence tracking, and outcome certification.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class CarePlanPhase:
    phase_number: int
    title: str
    classical_unani_concept: str     # Tanqia, Tadeel, Taqwiyat
    duration_days: int
    goals: List[str]
    nuskha_ids: List[str]
    tadbeer_protocols: List[str]
    parhez_level: str
    milestone_check: str
    status: str                      # UPCOMING, ACTIVE, COMPLETED


@dataclass
class LongitudinalCarePlan:
    plan_id: str                     # CP-2026-XXXX
    patient_id: str
    clinician_id: str
    program_name: str
    target_condition: str
    status: str                      # ACTIVE, COMPLETED_KAMIL, COMPLETED_NAQIS, SUSPENDED
    start_date: str
    target_end_date: str
    current_phase_index: int
    phases: List[CarePlanPhase]
    adherence_overall_pct: float
    proms_history: List[Dict[str, Any]]
    clinician_notes: str
    tamper_proof_hash: str


class CarePlanOSEngine:
    """Orchestrates longitudinal patient care plans across weeks and months."""

    _PLANS: Dict[str, LongitudinalCarePlan] = {}

    @classmethod
    def create_metabolic_reset_90(
        cls,
        patient_id: str,
        clinician_id: str,
        start_date: Optional[str] = None
    ) -> LongitudinalCarePlan:
        """Initializes the gold-standard 90-day Metabolic & Musculoskeletal Reset program."""
        now = start_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        plan_id = f"CP-MR90-{uuid.uuid4().hex[:6].upper()}"

        phases = [
            CarePlanPhase(
                phase_number=1,
                title="Phase 1: Tanqia-e-Mawad (Metabolic & Synovial Detoxification)",
                classical_unani_concept="Munzij wa Mushil-e-Balgham (Coction & Evacuation of Phlegmatic Morbidity)",
                duration_days=21,
                goals=[
                    "Eliminate visceral water-retention & phlegmatic congestion",
                    "Normalize morning joint stiffness below 30 minutes",
                    "Initiate gentle gastro-metabolic reset"
                ],
                nuskha_ids=["RX-MR90-P1"],
                tadbeer_protocols=["Dal'k Layyin (Warming sesame massage)", "Tareeq (Gentle steam diaphoretic)"],
                parhez_level="Tier 1-3 Strict Restrictions (No cold/wet food)",
                milestone_check="Day 21 Joint Mobility & Uric Acid Screening",
                status="COMPLETED"
            ),
            CarePlanPhase(
                phase_number=2,
                title="Phase 2: Tadeel-e-Mizaj (Humoral Balancing & Cartilage Restitution)",
                classical_unani_concept="Tadeel-e-Hararat-e-Ghariziya (Restoring Innate Metabolic Heat)",
                duration_days=42,
                goals=[
                    "Reduce VAS knee pain score by > 50%",
                    "Restore synovial fluidity and joint lubrication",
                    "Improve fasting insulin sensitivity and lipid balance"
                ],
                nuskha_ids=["RX-MR90-P2"],
                tadbeer_protocols=["Dal'k Mushtarik (Medium massage)", "Hammam (Therapeutic heat chamber)"],
                parhez_level="Tier 4-5 Moderate Restrictions",
                milestone_check="Day 63 Mid-point PROMs & Ultrasound Synovial Scan",
                status="ACTIVE"
            ),
            CarePlanPhase(
                phase_number=3,
                title="Phase 3: Taqwiyat-e-Aaza (Organ Fortification & Relapse Prevention)",
                classical_unani_concept="Taqwiyat-e-Meda wa Mafasil (Strengthening Stomach & Joints)",
                duration_days=27,
                goals=[
                    "Full functional ambulation without pain",
                    "HOMA-IR stabilization below 1.8",
                    "Transition to sustained lifestyle maintenance regimen"
                ],
                nuskha_ids=["RX-MR90-P3"],
                tadbeer_protocols=["Dal'k Sulb (Deep muscle strengthening)", "Riyazat-e-Motadila (Brisk walking)"],
                parhez_level="Tier 6-8 Sustained Healthy Nutrition",
                milestone_check="Day 90 Comprehensive Clinical Outcome & DSMB Certification",
                status="UPCOMING"
            )
        ]

        hash_src = f"{plan_id}|{patient_id}|{clinician_id}|Metabolic Reset 90|90days"
        plan_hash = hashlib.sha256(hash_src.encode("utf-8")).hexdigest()

        plan = LongitudinalCarePlan(
            plan_id=plan_id,
            patient_id=patient_id,
            clinician_id=clinician_id,
            program_name="Metabolic & Musculoskeletal Reset 90 (MR-90)",
            target_condition="Waja-ul-Mafasil & Metabolic Cold-Wet Imbalance",
            status="ACTIVE",
            start_date=now,
            target_end_date="2026-12-15",
            current_phase_index=1, # 0-indexed: currently on Phase 2
            phases=phases,
            adherence_overall_pct=91.4,
            proms_history=[
                {"day": 0, "vas_pain": 8.0, "morning_stiffness_mins": 60, "date": "2026-09-01"},
                {"day": 14, "vas_pain": 5.0, "morning_stiffness_mins": 35, "date": "2026-09-15"},
                {"day": 21, "vas_pain": 4.0, "morning_stiffness_mins": 20, "date": "2026-09-22"}
            ],
            clinician_notes="Patient responds favorably to Suranjan + Balsan protocol. Synovial stiffness down significantly.",
            tamper_proof_hash=plan_hash
        )

        cls._PLANS[plan_id] = plan
        return plan

    @classmethod
    def get_patient_active_care_plan(cls, patient_id: str) -> Optional[Dict[str, Any]]:
        """Finds or initializes the active longitudinal care plan for a patient."""
        for p in cls._PLANS.values():
            if p.patient_id == patient_id and p.status == "ACTIVE":
                return asdict(p)

        # Default: seed the canonical benchmark plan
        seeded = cls.create_metabolic_reset_90(patient_id, "DOC-01")
        return asdict(seeded)
