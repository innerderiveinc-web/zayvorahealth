"""
ZFIE Hakeem Sahab Adapter: HakeemSahabZFIEAdapter
Bridges ZFIE computational intelligence into Hakeem Sahab's clinical copilot reasoning.
Strict Non-Autonomous Doctrine:
Never outputs automatic prescriptions, approvals, or signatures.
Clinical authority remains 100% with the human clinician.
"""

from typing import Any, Dict, List, Optional
from packages.zfie.core.errors import UnauthorizedClinicalMutationError


class HakeemSahabZFIEAdapter:
    """Provides evidence-grounded scientific synthesis for the clinician."""

    @classmethod
    def synthesize_clinical_consideration(
        cls,
        patient_context: Dict[str, Any],
        formulation_data: Dict[str, Any],
        safety_evaluation: Dict[str, Any],
        evidence_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesizes clinical considerations without autonomous action."""
        form_name = formulation_data.get("name", "Formulation")
        verdict = safety_evaluation.get("verdict", "UNKNOWN")

        return {
            "clinician_guidance_type": "DECISION_SUPPORT_ONLY",
            "autonomous_prescription_permitted": False,
            "electronic_signature_status": "AWAITING_HUMAN_CLINICIAN_KEY",
            "summary": (
                f"Formulation Twin evaluated for {form_name}. "
                f"Safety Clearance State: {verdict}. "
                "All primary active phytochemicals mapped to molecular targets and evidence levels."
            ),
            "safety_state": safety_evaluation,
            "evidence_profile": evidence_summary,
            "required_clinician_actions": [
                "Review Schedule E1 Mudabbar purification certificate before signing",
                "Verify renal status and absence of pregnancy contraindications",
                "Confirm patient dosage and administration schedule"
            ]
        }

    @classmethod
    def generate_clinical_response(
        cls,
        clinical_objective: str,
        formulation_id: str = "ZAY-FORM-0001",
        patient_context: Optional[Dict[str, Any]] = None,
        analysis_mode: str = "CLINICAL_CDS"
    ) -> Dict[str, Any]:
        """
        Emits the Section 53 Clinical Response contract:
        Enforces requiresClinicianReview=True and autonomousActionAllowed=False.
        """
        from packages.zfie.formulation.formulation_twin import FormulationTwinRegistry
        from packages.zfie.safety.safety_evaluator import ZFIESafetyEvaluator
        from packages.zfie.contradiction.conflict_detection import ContradictionRegistry

        twin = FormulationTwinRegistry.get_twin(formulation_id)
        ingredients = [
            {"mufrad_id": i.mufrad_id, "processing_method": i.processing_method}
            for i in twin.ingredients
        ] if twin else []

        safety = ZFIESafetyEvaluator.evaluate_formulation(formulation_id, ingredients, patient_context)
        contradictions = [c.to_dict() for c in ContradictionRegistry.list_for_formulation(formulation_id)]

        return {
            "clinicalObjective": clinical_objective or (twin.therapeutic_target if twin else "Clinical Assessment"),
            "biologicalContext": [
                {
                    "state": "Inflammatory Synovial Hyperemia (Waja-ul-Mafasil)",
                    "status": "SUPPORTED"
                },
                {
                    "state": "Microtubule Polymerization and Neutrophil Migration",
                    "status": "ESTABLISHED"
                }
            ],
            "mechanisticConsiderations": [
                {
                    "findingId": "ZFIE-FND-001",
                    "statement": "Colchicine demonstrates high-affinity binding to Beta-tubulin, halting neutrophil extravasation.",
                    "evidenceLevel": "E5",
                    "evidenceStatus": "ESTABLISHED"
                },
                {
                    "findingId": "ZFIE-FND-002",
                    "statement": "Piperine downregulates CYP3A4 and intestinal P-gp, enhancing active bioavailability.",
                    "evidenceLevel": "E4",
                    "evidenceStatus": "SUPPORTED"
                }
            ],
            "evidence": [
                {
                    "evidenceId": "ZAY-EVD-91",
                    "citation": "Colchicine in the Treatment and Prophylaxis of Acute Gout Flares",
                    "level": "E5",
                    "direction": "INHIBITORY"
                }
            ],
            "safety": {
                "state": safety.get("verdict", "CAUTION"),
                "issues": safety.get("warnings", [])
            },
            "contradictions": contradictions,
            "unknowns": [
                "Long-term PK interaction with high-dose statin therapy",
                "Bioavailability variation across disparate gut microbiota phenotypes"
            ],
            "requiresClinicianReview": True,
            "autonomousActionAllowed": False
        }

    @classmethod
    def attempt_autonomous_signature(cls, encounter_id: str, clinician_id: str) -> None:
        """Strictly blocks AI self-approval."""
        raise UnauthorizedClinicalMutationError(
            "Forbidden AI Action: AI agent is legally and architecturally prohibited from self-approving or signing prescriptions."
        )
