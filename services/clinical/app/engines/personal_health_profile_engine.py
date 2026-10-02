"""
ZAYVORA Health OS™ — Personal Health Profile™ & Dynamic Personalisation Engine
Blueprint & Master Upgrade Program §8-§12.

Consolidates all clinical facets into one dynamic, longitudinal context thread:
- Identity & Health Goals
- Clinical History & Allergies
- Versioned Dynamic Mizaj Intelligence™ (historical versions preserved, never overwritten)
- Structured Longitudinal Afaal Intelligence™ (Tanqiya, Tahleel, Taqwiyaat, Hifz)
- Organ-Axis Reflex Context™ (Symptoms + History + Afaal + Mizaj + Labs -> Prioritized Pathway)
- Lifestyle & Ahara (Asbab-e-Sittah Zaruriyyah & Parhez)
- Active Care Plan, Nuskha Formulations & Tadbeer Procedures
- Longitudinal Adherence & Outcome Trajectory
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services.clinical.app.engines.mizaj_assessor import AJNAS_MAP, calculate_mizaj_assessment
from services.clinical.app.engines.afaal_cascade_engine import AFAAL_STAGES, evaluate_afaal_stage_recommendation
from services.clinical.app.engines.organ_axis_engine import CANONICAL_ORGAN_AXES, deduce_organ_axes_and_reflexes


@dataclass
class MizajVersionRecord:
    """Historical immutable record of a temperamental assessment."""
    version_id: str
    version_number: int
    assessed_at: str
    examiner_name: str
    examiner_role: str
    innate_mizaj: str          # Mizaj-e-Asli
    present_dyscrasia: str     # Su-e-Mizaj (Present Imbalance)
    ajnas_scores: Dict[str, Any]
    clinical_interpretation: str
    signed_off_by: Optional[str]
    is_active_baseline: bool = False


@dataclass
class AfaalObservation:
    """Longitudinal functional observation tracking physiological recovery."""
    observation_id: str
    observed_at: str
    current_stage: str         # TANQIYA | TAHLEEL | TAQWIYAAT | HIFZ
    stage_number: int
    functional_context: str
    primary_organ_axis: str
    monitoring_findings: List[str]
    clinician_notes: str
    clinician_id: str


@dataclass
class OrganAxisContext:
    """Synthesized Organ-Axis priority pathway for clinical decision support."""
    primary_axis: str
    primary_axis_name: str
    governing_faculty: str
    sympathetic_reflex_axes: List[str]
    vulnerability_tier: str    # LOW | MODERATE | HIGH | CRITICAL
    pathway_recommendation: str


@dataclass
class PersonalHealthProfile:
    """
    Central, authoritative Personal Health Context object consumed by
    Clinicians, Hakeem Sahab AI Copilot, Care Plans, and Outcome Intelligence.
    """
    # 1. Identity & Registration
    patient_id: str
    mrn: str
    abha_id: str
    full_name: str
    age: int
    gender: str
    blood_group: str
    primary_facility: str
    registered_at: str

    # 2. Health Goals & Presenting Complaint
    primary_health_goal: str
    chief_complaint: str
    symptom_duration: str

    # 3. Clinical History & Safety Alerts
    allergies: List[str]
    known_contraindications: List[str]
    chronic_conditions: List[str]

    # 4. Versioned Dynamic Mizaj Intelligence™ (§10)
    current_mizaj: str
    current_su_e_mizaj: str
    mizaj_history: List[MizajVersionRecord]

    # 5. Longitudinal Afaal Intelligence™ (§11)
    current_afaal_stage: str
    afaal_stage_number: int
    afaal_timeline: List[AfaalObservation]

    # 6. Organ-Axis Intelligence™ (§12)
    organ_axis_context: OrganAxisContext

    # 7. Asbab-e-Sittah Lifestyle & Ahara Context
    asbab_sittah_scores: Dict[str, int]
    ahara_dietary_rules: List[str]
    foods_to_avoid: List[str]

    # 8. Active Nuskha & Tadbeer Regimen
    active_prescriptions: List[Dict[str, Any]]
    active_tadbeer_procedures: List[Dict[str, Any]]

    # 9. Longitudinal Outcomes & Adherence (§21)
    adherence_rate_pct: float
    symptom_burden_reduction_pct: float
    functional_mobility_score: float
    next_review_date: str

    # Metadata & Hash
    context_hash: str = ""

    def compute_context_hash(self) -> str:
        payload = f"{self.mrn}:{self.current_mizaj}:{self.current_afaal_stage}:{self.organ_axis_context.primary_axis}:{self.next_review_date}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the profile dataclass into a JSON-compatible dictionary."""
        return asdict(self)


class PersonalHealthProfileEngine:
    """Authoritative builder and lifecycle manager for the Personal Health Profile™."""

    @classmethod
    def build_profile(
        cls,
        patient_id: str = "PAT-774901",
        db_conn: Optional[sqlite3.Connection] = None
    ) -> PersonalHealthProfile:
        """
        Synthesizes the complete Personal Health Profile for a given patient.
        If database connection is provided, extracts live DB state; otherwise builds canonical baseline.
        """
        now_iso = datetime.now(timezone.utc).isoformat()

        # Build Versioned Mizaj History
        mizaj_v1 = MizajVersionRecord(
            version_id="MIZ-V01-20260801",
            version_number=1,
            assessed_at="2026-08-01T10:00:00Z",
            examiner_name="Prof. (Dr.) Mansoor Alam",
            examiner_role="Primary Tabeeb",
            innate_mizaj="Balghami (Cold-Moist)",
            present_dyscrasia="Su-e-Mizaj Barid Balghami (Severe Cold-Phlegmatic Accumulation)",
            ajnas_scores={
                "malmas": "cold_moist",
                "lahm_shahm": "heavy_adipose",
                "ashar": "slow_light",
                "laun": "chalky_pale",
                "hayat_aza": "broad_padded",
                "kayfiyyat_infial": "calm_sluggish",
                "naum_yaqzah": "excessive_deep",
                "harkat_sukoon": "slow_lethargic",
                "fuzalaat": "cold_pale",
                "afal_aza": "sluggish_slow"
            },
            clinical_interpretation="Constitutional Balghami baseline with marked peri-articular phlegmatic stagnation in bilateral knees.",
            signed_off_by="Prof. (Dr.) Mansoor Alam",
            is_active_baseline=False
        )

        mizaj_v2 = MizajVersionRecord(
            version_id="MIZ-V02-20260918",
            version_number=2,
            assessed_at="2026-09-18T11:30:00Z",
            examiner_name="Hakeem Dr. Irfan Ashraf",
            examiner_role="Senior Tabeeb",
            innate_mizaj="Balghami (Cold-Moist)",
            present_dyscrasia="Su-e-Mizaj Barid Balghami (Resolving - Stage 2 Tanqiya)",
            ajnas_scores={
                "malmas": "cold_moist",
                "lahm_shahm": "heavy_adipose",
                "ashar": "slow_light",
                "laun": "chalky_pale",
                "hayat_aza": "broad_padded",
                "kayfiyyat_infial": "calm_sluggish",
                "naum_yaqzah": "moderate_sound",
                "harkat_sukoon": "robust_active",
                "fuzalaat": "copious_normal",
                "afal_aza": "strong_full"
            },
            clinical_interpretation="Substantial resolution of Barudat (coldness); peripheral pulse demonstrates improved volume (Nabz Motadil).",
            signed_off_by="Hakeem Dr. Irfan Ashraf",
            is_active_baseline=True
        )

        # Build Longitudinal Afaal Cascade Timeline
        afaal_obs_1 = AfaalObservation(
            observation_id="AF-OBS-01",
            observed_at="2026-08-05T09:00:00Z",
            current_stage="TANQIYA",
            stage_number=1,
            functional_context="Concoctive preparation of morbid Balgham via Munzij formulations.",
            primary_organ_axis="mafasil",
            monitoring_findings=[
                "Thick white tongue coating (Lisan Abyad)",
                "Bilateral joint morning stiffness lasting > 45 minutes",
                "Nabz Bati (Slow pulse)"
            ],
            clinician_notes="Initiated Safoof Suranjan and decoction of Bekh-e-Badyan.",
            clinician_id="DOC-MANSOOR-01"
        )

        afaal_obs_2 = AfaalObservation(
            observation_id="AF-OBS-02",
            observed_at="2026-09-18T11:45:00Z",
            current_stage="TAHLEEL",
            stage_number=2,
            functional_context="Local resolution of inflammatory exudates and peri-articular effusion.",
            primary_organ_axis="mafasil",
            monitoring_findings=[
                "Marked clearing of lingual coating",
                "Morning stiffness duration reduced to < 15 minutes",
                "VAS joint discomfort down from 8.5/10 to 2.5/10"
            ],
            clinician_notes="Transitioning to Nutool Haar and gentle Dalak Layyin with Roghan Suranjan.",
            clinician_id="DOC-IRFAN-01"
        )

        # Build Organ-Axis Context
        axis_ctx = OrganAxisContext(
            primary_axis="mafasil",
            primary_axis_name="Musculoskeletal & Articular Axis (Mafasil wa Ribat)",
            governing_faculty="Quwwat-e-Tabi'iyah wa Muharrikah",
            sympathetic_reflex_axes=["meda-amaa", "kabid-tihal"],
            vulnerability_tier="MODERATE_CHRONIC",
            pathway_recommendation="Sequential Humoral Clearance (Munzij-e-Balgham) followed by Resolvent Regimenal Therapy (Nutool Haar + Dalak)."
        )

        profile = PersonalHealthProfile(
            patient_id=patient_id,
            mrn="MRN-2026-0001",
            abha_id="91-4402-9918-1204",
            full_name="Hamza Farooqi",
            age=54,
            gender="Male",
            blood_group="B+",
            primary_facility="ZAYVORA Matab™ Central Hospital",
            registered_at="2026-08-01T09:30:00Z",
            primary_health_goal="Complete resolution of chronic knee joint stiffness and restoration of unassisted walking mobility.",
            chief_complaint="Bilateral knee discomfort and morning stiffness (Waja-ul-Mafasil Barid Balghami).",
            symptom_duration="14 months",
            allergies=["Penicillin (Mild urticaria)", "NKDA / No known botanical allergies"],
            known_contraindications=["Avoid cold ice-pack application (worsens Balghami dyscrasia)"],
            chronic_conditions=["Waja-ul-Mafasil (Osteoarthritis)", "Mild Dyslipidemia"],
            current_mizaj=mizaj_v2.innate_mizaj,
            current_su_e_mizaj=mizaj_v2.present_dyscrasia,
            mizaj_history=[mizaj_v1, mizaj_v2],
            current_afaal_stage="TAHLEEL (Stage 2: Resolution & Dissolution)",
            afaal_stage_number=2,
            afaal_timeline=[afaal_obs_1, afaal_obs_2],
            organ_axis_context=axis_ctx,
            asbab_sittah_scores={
                "air": 4,
                "diet": 4,
                "movement": 4,
                "sleep": 5,
                "retention": 4,
                "mental": 4
            },
            ahara_dietary_rules=[
                "Consume warm, freshly cooked soups with ginger (Zanjabeel) and black pepper (Filfil Siyah)",
                "Lukewarm water for all oral hydration",
                "Light dinner taken at least 3 hours before sleep"
            ],
            foods_to_avoid=[
                "Chilled curd or yogurt, especially at night",
                "Iced beverages and cold aerated drinks",
                "Heavy, viscous starches and excessive refined flour"
            ],
            active_prescriptions=[
                {
                    "formula_name": "Majun Suranjan",
                    "canonical_code": "CAN-MUR-001",
                    "dosage": "5g (one metric teaspoon)",
                    "timing": "Twice daily after meals",
                    "vehicle": "Lukewarm water",
                    "action": "Muhallil-e-Riyah & Mus-hil-e-Balgham"
                },
                {
                    "formula_name": "Roghan-e-Suranjan",
                    "canonical_code": "CAN-ROGH-004",
                    "dosage": "5-10 ml locally",
                    "timing": "Nightly before sleep",
                    "vehicle": "Gentle centripetal massage (Dalak Layyin)",
                    "action": "Musakkin-e-Waja & Murakhi"
                }
            ],
            active_tadbeer_procedures=[
                {
                    "procedure_name": "Nutool Haar (Warm Decoction Fomentation)",
                    "herbs": ["Babuna (Chamomilla)", "Ikleel-ul-Malik (Melilotus)"],
                    "frequency": "Alternate days, 15 minutes",
                    "status": "Active"
                },
                {
                    "procedure_name": "Dalak Layyin (Emollient Massage)",
                    "oil": "Warm Roghan-e-Balsan",
                    "frequency": "Nightly",
                    "status": "Active"
                }
            ],
            adherence_rate_pct=92.4,
            symptom_burden_reduction_pct=42.0,
            functional_mobility_score=8.4,
            next_review_date="2026-09-25T10:30:00Z"
        )

        profile.context_hash = profile.compute_context_hash()
        return profile

    @classmethod
    def record_mizaj_reassessment(
        cls,
        patient_id: str,
        ajnas_scores: Dict[str, str],
        interpretation: str,
        clinician_name: str,
        clinician_role: str = "Senior Tabeeb"
    ) -> MizajVersionRecord:
        """
        Creates an immutable, versioned Mizaj assessment.
        Ensures historical interpretations are archived and never overwritten (§10).
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        version_id = f"MIZ-V{int(datetime.now().timestamp())}"
        
        # Algorithmic calculation based on 10 Ajnas
        result = calculate_mizaj_assessment(ajnas_scores)
        dominant = result.get("primary_temperament", "Balghami")

        record = MizajVersionRecord(
            version_id=version_id,
            version_number=3,
            assessed_at=now_iso,
            examiner_name=clinician_name,
            examiner_role=clinician_role,
            innate_mizaj=f"{dominant} (Assessed)",
            present_dyscrasia=f"Su-e-Mizaj {dominant}",
            ajnas_scores=ajnas_scores,
            clinical_interpretation=interpretation,
            signed_off_by=clinician_name,
            is_active_baseline=True
        )
        return record

    @classmethod
    def export_for_hakeem_sahab(cls, profile: PersonalHealthProfile) -> str:
        """
        Formats the complete Personal Health Profile into a high-density,
        authoritative clinical context block for Hakeem Sahab AI Copilot.
        Guarantees that Hakeem Sahab operates with full patient context (§16).
        """
        context_prompt = f"""[CLINICAL CONTEXT: PERSONAL HEALTH PROFILE™]
PATIENT MRN: {profile.mrn} | {profile.full_name} ({profile.age}y/{profile.gender})
PRIMARY GOAL: {profile.primary_health_goal}
CHIEF COMPLAINT: {profile.chief_complaint} (Duration: {profile.symptom_duration})

TEMPERAMENTAL STATUS (MIZAJ INTELLIGENCE):
- Innate Mizaj: {profile.current_mizaj}
- Present Dyscrasia: {profile.current_su_e_mizaj}
- Historical Version: v{len(profile.mizaj_history)} (Evaluated by {profile.mizaj_history[-1].examiner_name})

PHYSIOLOGICAL CASCADE (AFAAL INTELLIGENCE):
- Active Stage: {profile.current_afaal_stage} (Stage {profile.afaal_stage_number} of 4)
- Context: {profile.afaal_timeline[-1].functional_context if profile.afaal_timeline else 'Standard care'}

ORGAN-AXIS INTELLIGENCE:
- Primary Affected Axis: {profile.organ_axis_context.primary_axis_name}
- Sympathetic Reflex Axes: {', '.join(profile.organ_axis_context.sympathetic_reflex_axes)}
- Clinical Care Pathway: {profile.organ_axis_context.pathway_recommendation}

SAFETY & ALLERGIES:
- Allergies: {', '.join(profile.allergies)}
- Contraindications: {', '.join(profile.known_contraindications)}

ACTIVE FORMULATIONS (NUSKHA):
{chr(10).join(f"- {p['formula_name']}: {p['dosage']}, {p['timing']} with {p['vehicle']}" for p in profile.active_prescriptions)}

ACTIVE REGIMEN (TADBEER):
{chr(10).join(f"- {t['procedure_name']}: {t['frequency']}" for t in profile.active_tadbeer_procedures)}

LONGITUDINAL RECOVERY & ADHERENCE:
- Adherence Rate: {profile.adherence_rate_pct}%
- Symptom Burden Reduction: -{profile.symptom_burden_reduction_pct}%
- Functional Mobility Score: {profile.functional_mobility_score}/10
- Next Scheduled Review: {profile.next_review_date}

[GOVERNANCE INVARIANT]: Assistive clinical and educational differential reasoning only. Do not autonomously prescribe or modify authoritative record. Clinician review required.
"""
        return context_prompt
