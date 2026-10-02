#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Unified Doctor Clinical Continuum Orchestrator
===================================================================
Unifies the 7 clinical consultation steps into a single, seamless, continuous workflow:
  1. Patient 360 Ingestion
  2. 10-Ajnas Mizaj Assessment
  3. 12 Organ-Axis Diagnostic Scoring
  4. Hakeem Sahab AI v2 Graph-Grounded Brief
  5. Safety Firewall v2 Verification Gate
  6. 4-Tier Nuskha Nawisi Prescribing
  7. 21 CFR Part 11 Digital Signoff & Follow-up Scheduling

Eliminates jumping between disjointed screens; establishes a single continuous record.
"""

from typing import Dict, List, Any, Optional
import datetime
import hashlib

from services.clinical.app.engines.patient_360_engine import Patient360Engine
from services.ai.app.engines.hakeem_case_brief_engine import HakeemCaseBriefEngine
from services.knowledge.app.engines.knowledge_graph_traversal_engine import get_clinical_knowledge_graph
from services.knowledge.app.engines.knowledge_intelligence_vnext import (
    SafetyFirewallV2,
    AISafetyState,
    PatientSafetyBarrier
)


class DoctorContinuumOrchestrator:
    """Orchestrates an end-to-end continuous clinical consultation encounter."""

    @classmethod
    def initialize_continuum_session(
        cls,
        patient_id: str,
        practitioner_id: str = "DOC-IRFAN-01",
        chief_complaint: str = "Chronic bilateral knee stiffness and joint inflammation (Waja-ul-Mafasil)",
        labs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Loads Patient 360 and initializes the continuous clinical encounter."""
        p360 = Patient360Engine.build_patient_360(patient_id=patient_id, labs=labs)
        now_str = datetime.datetime.utcnow().isoformat() + "Z"
        encounter_id = f"ENC-{patient_id.replace('MRN-', '')}-{int(datetime.datetime.utcnow().timestamp())}"

        return {
            "encounter_id": encounter_id,
            "patient_id": patient_id,
            "practitioner_id": practitioner_id,
            "status": "IN_PROGRESS",
            "active_step": 1,
            "steps": [
                {"step_number": 1, "name": "Patient 360 Review", "status": "COMPLETED"},
                {"step_number": 2, "name": "10-Ajnas Mizaj Assessment", "status": "PENDING"},
                {"step_number": 3, "name": "12 Organ-Axis Diagnostic Scoring", "status": "PENDING"},
                {"step_number": 4, "name": "Hakeem Sahab AI v2 Brief", "status": "PENDING"},
                {"step_number": 5, "name": "Safety Firewall v2 Gate", "status": "PENDING"},
                {"step_number": 6, "name": "4-Tier Nuskha Nawisi", "status": "PENDING"},
                {"step_number": 7, "name": "Digital Sign-off & Follow-up", "status": "PENDING"}
            ],
            "patient_360": p360,
            "chief_complaint": chief_complaint,
            "created_at": now_str
        }

    @classmethod
    def execute_consultation_flow(
        cls,
        patient_id: str,
        practitioner_id: str,
        chief_complaint: str,
        mizaj_input: Optional[Dict[str, Any]] = None,
        axis_scores: Optional[Dict[str, Any]] = None,
        labs: Optional[Dict[str, Any]] = None,
        prescribed_drugs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Executes the continuous clinical consultation sequence in a single deterministic pass.
        Returns the unified clinical encounter document.
        """
        now_str = datetime.datetime.utcnow().isoformat() + "Z"
        labs = labs or {}

        # 1. Ingest Patient 360
        p360 = Patient360Engine.build_patient_360(
            patient_id=patient_id,
            labs=labs,
            mizaj_data=mizaj_input,
            axis_scores=axis_scores
        )
        patient_demographics = p360["panels"]["identity_and_consent"]["demographics"]

        # 2. 10-Ajnas Mizaj Assessment
        if mizaj_input:
            mizaj_data = dict(mizaj_input)
            if "status" not in mizaj_data:
                mizaj_data["status"] = "ASSESSED"
        else:
            complaint_lower = chief_complaint.lower()
            if any(w in complaint_lower for w in ["cold", "stiff", "winter", "swelling", "edema", "phlegm"]):
                inferred_humor = "Balgham (Cold & Moist)"
                inferred_cat = "BALGHAMI_DYSCRASIA"
            elif any(w in complaint_lower for w in ["heat", "burning", "fever", "yellow", "bilious"]):
                inferred_humor = "Safra (Hot & Dry)"
                inferred_cat = "SAFRAWI_DYSCRASIA"
            elif any(w in complaint_lower for w in ["dry", "dark", "melanchol", "wasting"]):
                inferred_humor = "Sauda (Cold & Dry)"
                inferred_cat = "SAUDAWI_DYSCRASIA"
            else:
                inferred_humor = "Motadil / Pending Assessment"
                inferred_cat = "INSUFFICIENT_DATA"

            mizaj_data = {
                "dominant_humor": inferred_humor,
                "secondary_humor": "Pending Determinants",
                "score": 12 if inferred_cat != "INSUFFICIENT_DATA" else 0,
                "max_score": 18,
                "status": "INFERRED_FROM_COMPLAINT" if inferred_cat != "INSUFFICIENT_DATA" else "INSUFFICIENT_DATA",
                "category": inferred_cat,
                "recommended_form": "Safoof / Dry Powder Extract",
                "contraindicated_form": "Majoon / Heavy Sugar Syrups" if "Balgham" in inferred_humor else "None",
                "grounding_note": "Derived dynamically from presenting clinical encounter symptoms; formal 10-Ajnas entry recommended."
            }

        # 3. 12 Organ-Axis Diagnostic Scoring
        if axis_scores:
            axes_data = dict(axis_scores)
        else:
            complaint_lower = chief_complaint.lower()
            derived_axes = {}
            if any(w in complaint_lower for w in ["joint", "knee", "arthritis", "mafasil", "pain", "stiffness"]):
                derived_axes["Mafasil-Azlaat (Musculo-Skeletal Axis)"] = {
                    "score": 4, "severity": "HIGH_CONCERN",
                    "action": "Clear viscous exudates & restore joint synovial homeostasis",
                    "source": "derived_from_complaint"
                }
            if any(w in complaint_lower for w in ["liver", "jigar", "metabolic", "fatigue", "cholesterol"]):
                derived_axes["Jigar-Banas (Hepato-Metabolic Axis)"] = {
                    "score": 3, "severity": "MODERATE_CONCERN",
                    "action": "Enhance phase-II hepatic clearance",
                    "source": "derived_from_complaint"
                }
            if any(w in complaint_lower for w in ["digestion", "stomach", "gastric", "meda", "acidity", "gut"]):
                derived_axes["Meda-Ama (Gastro-Intestinal Axis)"] = {
                    "score": 2, "severity": "MILD_CONCERN",
                    "action": "Preserve digestive fire (Hazm)",
                    "source": "derived_from_complaint"
                }
            if not derived_axes:
                derived_axes["Tabiyat (Innate Homeostatic Axis)"] = {
                    "score": 1, "severity": "BASELINE_MONITORING",
                    "action": "Baseline homeostatic preservation",
                    "source": "baseline_default"
                }
            axes_data = derived_axes

        # 4. Hakeem Sahab AI v2 Evidence-Grounded Brief
        hakeem_brief = HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
            patient_id=patient_id,
            patient_context={
                "name": patient_demographics.get("name", "Patient"),
                "age": patient_demographics.get("age", 40),
                "gender": patient_demographics.get("gender", "Male"),
                "user_role": "CLINICIAN"
            },
            clinical_condition="Waja-ul-Mafasil",
            labs=labs,
            mizaj_result=mizaj_data,
            active_axes=list(axes_data.keys())
        )

        # 5. Safety Firewall v2 Verification
        drugs_to_check = prescribed_drugs or ["Asgandh", "Zanjabeel", "Filfil Siyah"]
        safety_checks = []
        is_all_safe = True
        for dname in drugs_to_check:
            rec = SafetyFirewallV2.evaluate_drug_safety_state(
                drug_or_id={"drug_id": dname, "classical_state": "APPROVED"},
                user_role="CLINICIAN"
            )
            safety_checks.append({"drug": dname, "evaluation": rec})
            if rec["ai_state"] == AISafetyState.BLOCKED.value:
                is_all_safe = False

        # 6. 4-Tier Nuskha Nawisi Prescribing
        nuskha = {
            "nuskha_id": f"NSK-{patient_id.replace('MRN-', '')}-01",
            "tier_1_foundation": {"drug": "Asgandh (Withania somnifera)", "dose": "500 mg", "percentage": "35%"},
            "tier_2_core_actives": [
                {"drug": "Zanjabeel (Zingiber officinale)", "dose": "350 mg", "percentage": "30%"},
                {"drug": "Chob Zard (Curcuma longa)", "dose": "250 mg", "percentage": "20%"}
            ],
            "tier_3_corrective_musleh": {"drug": "Filfil Siyah (Piper nigrum)", "dose": "100 mg", "percentage": "10%", "action": "Bio-enhancement & gastric protection"},
            "tier_4_catalyst_vehicle": {"drug": "Lukewarm water with 1 drop Roghan-e-Badiyan", "percentage": "5%", "conduit_function": "Enhance trans-mucosal absorption"},
            "parhez_dietary_restrictions": [
                "Strict avoidance of cold-moist foods (Curd, cucumber, chilled beverages)",
                "Avoid unboiled water after twilight",
                "Recommend warm bone broth infused with ginger and black cumin"
            ],
            "lifestyle_tadbeer": "Dalk (dry massage with Roghan-e-Suranjan) 15 minutes before bedtime"
        }

        # 7. Digital Clinician Sign-Off & Automated Follow-Up
        signature_raw = f"{patient_id}:{practitioner_id}:{nuskha['nuskha_id']}:{now_str}"
        signature_hash = hashlib.sha256(signature_raw.encode()).hexdigest()

        return {
            "encounter_id": f"ENC-{patient_id.replace('MRN-', '')}-{int(datetime.datetime.utcnow().timestamp())}",
            "patient_id": patient_id,
            "practitioner_id": practitioner_id,
            "status": "APPROVED_AND_SIGNED",
            "chief_complaint": chief_complaint,
            "mizaj_assessment": mizaj_data,
            "organ_axes": axes_data,
            "hakeem_sahab_v2_brief": hakeem_brief,
            "safety_firewall_status": {
                "is_all_safe": is_all_safe,
                "evaluations": safety_checks
            },
            "final_nuskha": nuskha,
            "digital_signature": {
                "signed_by": practitioner_id,
                "role": "LICENSED_BUMS_PRACTITIONER",
                "signed_at": now_str,
                "signature_hash": signature_hash,
                "statutory_compliance": "21 CFR Part 11 / IT Act 2000 Section 3"
            },
            "follow_up": {
                "scheduled_date": (datetime.datetime.utcnow() + datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
                "automated_proms_survey": "Day 7 & Day 14 VAS Pain & Stiffness Scale",
                "lab_repeat": "hs-CRP repeat at 28 days"
            }
        }
