"""
ZAYVORA Health OS™ — Test Suite #64: Clinical Intelligence Core vNext & Learning Healthcare OS
=============================================================================================
Verifies the end-to-end 12-stage clinical reasoning loop, WHO SMART Guidelines Level 3 DAK,
and Closed-Loop Learning Healthcare System:

1. WHO SMART Guidelines Level 3 Computable DAK (CDD, DSL, SHA-256 integrity, SemVer 2.0.0).
2. Complete 12-Stage Clinical Intelligence Continuum runtime execution.
3. Strict Safety Invariants:
   - Autonomous AI sign-off Hard-Block (AI cannot approve prescriptions).
   - Statutory Schedule E(1) poison hard-block detection.
   - Special population contraindication hard-blocks (e.g., Pregnancy).
4. Outcome Intelligence & Closed-Loop Learning (HIPAA § 164.514(b)(2) de-identification,
   cohort statistical deltas, and Candidate Knowledge Updates requiring Clinical Governance Board).
5. Live REST API Endpoints Integration.
"""

import sys
import os
import io
import json
import unittest
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.core.who_smart_dak_engine import (
    WHOSmartDAKEngine,
    SMARTKnowledgeArtifact,
    ComputableDecisionRule,
    WHOCoreDataElement,
)
from services.clinical.app.engines.closed_loop_learning_engine import (
    ClosedLoopLearningEngine,
    CandidateKnowledgeUpdate,
)
from services.clinical.app.engines.outcome_intelligence_engine import (
    OutcomeEvaluation,
    ClassicalOutcome,
)
from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
    ClinicalIntelligenceCoreOrchestrator,
    ClinicalContinuumRequest,
    ClinicalContinuumResponse,
)
from services.therapeutic.app.engines.nuskha_state_machine import NuskhaStateMachine
from services.live_api_server import ZayvoraApiHandler


def _call_get(path):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {}
    req.request_version = "HTTP/1.1"
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_GET()
    raw = req.wfile.getvalue().decode()
    header, _, body = raw.partition("\r\n\r\n")
    return json.loads(body) if body.strip() else {}


def _call_post(path, data):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    body_bytes = json.dumps(data).encode("utf-8")
    req.headers = {"Content-Length": str(len(body_bytes)), "Content-Type": "application/json"}
    req.request_version = "HTTP/1.1"
    req.rfile = io.BytesIO(body_bytes)
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_POST()
    raw = req.wfile.getvalue().decode()
    header, _, body = raw.partition("\r\n\r\n")
    return json.loads(body) if body.strip() else {}


class TestClinicalIntelligenceCoreVNext(unittest.TestCase):

    def setUp(self):
        ClosedLoopLearningEngine.clear_registry()

    # -------------------------------------------------------------------------
    # PART 1: WHO SMART Guidelines Level 3 Computable DAK Tests
    # -------------------------------------------------------------------------
    def test_01_who_smart_dak_transformation_and_cdd(self):
        """WHO SMART Guidelines Level 3 computable transformation & CDD codes."""
        sample_mufrad = {
            "name": "Suranjan Shirin",
            "botanical_name": "Colchicum autumnale L.",
            "mizaj": "Haar 2, Yabis 2",
            "is_schedule_e1": False,
            "requires_tadbeer": True,
            "tadbeer_method": "Soaking in almond oil (Tadbeer-e-Roghani)",
            "primary_organ_axis": "MAFASIL",
            "therapeutic_actions": ["Mudammil-e-Mafasil", "Musakkin-e-Waja"],
            "standard_dose": "1 - 3 grams",
            "musleh": "Kateera, Roghan-e-Badam",
            "badal": "Asgandh",
            "contraindications": ["Severe Renal Impairment", "Pregnancy"]
        }

        art = WHOSmartDAKEngine.transform_mufrad_to_smart_artifact(sample_mufrad, version="2.0.0")
        self.assertIsInstance(art, SMARTKnowledgeArtifact)
        self.assertEqual(art.version, "2.0.0")
        self.assertTrue(art.sha256_hash)
        self.assertEqual(len(art.sha256_hash), 64)

        # Validate validation method
        val = WHOSmartDAKEngine.validate_computable_artifact(art)
        self.assertTrue(val["is_valid"])
        self.assertTrue(val["sha256_verified"])
        self.assertEqual(val["governance_status"], "RATIFIED_COMPUTABLE")

        # Validate Core Data Dictionary elements
        cdd = WHOSmartDAKEngine.CORE_DATA_DICTIONARY
        self.assertIn("MIZAJ_HOT_DEGREE", cdd)
        self.assertIn("SCHEDULE_E1_POISON_STATUS", cdd)
        self.assertIn("TADBEER_STATUS", cdd)
        self.assertIn("ORGAN_AXIS_TARGET", cdd)

        # Validate Decision Support Rules
        self.assertGreaterEqual(len(art.decision_rules), 1)
        self.assertEqual(art.decision_rules[0].action_type, "MANDATE_MUSLEH")

    def test_02_who_smart_dak_cryptographic_integrity(self):
        """Cryptographic SHA-256 integrity verification of Level 3 DAK artifact."""
        sample_mufrad = {
            "name": "Asgandh",
            "botanical_name": "Withania somnifera (L.) Dunal",
            "mizaj": "Haar 1, Yabis 2",
            "is_schedule_e1": False,
            "primary_organ_axis": "DIMAGH-ASAB",
            "therapeutic_actions": ["Muqawwi-e-Aam", "Musakkin-e-Asab"],
            "standard_dose": "3 - 5 grams",
        }
        art = WHOSmartDAKEngine.transform_mufrad_to_smart_artifact(sample_mufrad)
        val = WHOSmartDAKEngine.validate_computable_artifact(art)
        self.assertTrue(val["sha256_verified"])

        # Tampering detection
        art.computable_payload["botanical_name"] = "Tampered Scientific Name"
        tampered_val = WHOSmartDAKEngine.validate_computable_artifact(art)
        self.assertFalse(tampered_val["sha256_verified"])
        self.assertFalse(tampered_val["is_valid"])
        self.assertEqual(tampered_val["governance_status"], "REJECTED_VALIDATION")

    # -------------------------------------------------------------------------
    # PART 2: 12-Stage Clinical Intelligence Continuum Tests
    # -------------------------------------------------------------------------
    def test_03_full_twelve_stage_continuum_execution(self):
        """Execute full 12-stage clinical loop on benchmark Waja-ul-Mafasil case."""
        req = ClinicalContinuumRequest(
            patient_id="P-HAMZA-101",
            patient_name="Hamza Farooqi",
            age=54,
            gender="MALE",
            chief_complaints=["Chronic bilateral knee pain", "Morning stiffness > 45 mins", "Aggravated in cold"],
            presenting_condition="Waja-ul-Mafasil",
            symptom_duration_days=180,
            baseline_pain_vas=8.0,
            constitutional_signs={"dominant_humor": "Balgham", "cold_degree": 3, "moist_degree": 2},
            targeted_axes=["mafasil", "meda-amaa"],
            candidate_drugs=["Suranjan Shirin", "Zanjabeel", "Asgand"],
            clinician_id="HAK-0042",
            clinician_role="HAKEEM",
            is_pregnant=False,
            has_renal_impairment=False,
            followup_proms_day=14,
            followup_symptom_vas=2.0,
            followup_adverse_events=[]
        )

        res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
        self.assertIsInstance(res, ClinicalContinuumResponse)
        self.assertTrue(res.transaction_id.startswith("TX-ZAYVORA-"))

        # Stage 1: Patient Profile
        self.assertEqual(res.stage_1_patient_profile["patient_id"], "P-HAMZA-101")
        self.assertEqual(res.stage_1_patient_profile["condition"], "Waja-ul-Mafasil")

        # Stage 2: Assessment & Triage
        self.assertTrue(res.stage_2_triage_assessment.get("is_safe_for_unani_care"))
        self.assertIn("decision", res.stage_2_triage_assessment)

        # Stage 3: Mizaj
        self.assertEqual(res.stage_3_mizaj_quantification["dominant_mizaj"], "Balgham")

        # Stage 4: 12-Axis Targeting
        self.assertIn("axes", res.stage_4_organ_axis_targeting)

        # Stage 5: Knowledge Retrieval
        self.assertGreaterEqual(res.stage_5_knowledge_retrieval["count"], 1)

        # Stage 6: Evidence Hierarchy
        self.assertGreaterEqual(len(res.stage_6_evidence_hierarchy["records"]), 1)

        # Stage 7: Safety Firewall
        self.assertEqual(res.stage_7_safety_firewall["decision"], "PASS")

        # Stage 8: Hakeem Sahab Case Brief
        self.assertIn("clinical_reasoning_summary", res.stage_8_hakeem_sahab_brief)
        self.assertIn("draft_nuskha", res.stage_8_hakeem_sahab_brief)
        self.assertEqual(res.stage_8_hakeem_sahab_brief["draft_nuskha"]["status"], "NON_BINDING_CLINICAL_DRAFT")

        # Stage 9: Clinician Approval
        self.assertEqual(res.stage_9_clinician_approval["nuskha_state"], "APPROVED")
        self.assertTrue(res.stage_9_clinician_approval["is_ratified"])
        self.assertEqual(len(res.stage_9_clinician_approval["state_audit_trail"]), 3)

        # Stage 10: Nuskha & 8-Tier Parhez
        self.assertIn("parhez_8_tier", res.stage_10_nuskha_and_parhez)
        self.assertEqual(len(res.stage_10_nuskha_and_parhez["parhez_8_tier"]), 8)

        # Stage 11: PROMs Follow-up
        self.assertIsNotNone(res.stage_11_proms_followup)
        self.assertGreaterEqual(res.stage_11_proms_followup["clinical_improvement_percent"], 70.0)

        # Stage 12: Outcome & Closed-Loop Learning
        self.assertIsNotNone(res.stage_12_outcome_and_learning)
        self.assertEqual(res.stage_12_outcome_and_learning["outcome_classification"], ClassicalOutcome.KAMIL.value)
        self.assertTrue(res.stage_12_outcome_and_learning["rwe_learning_eligible"])
        self.assertIsNotNone(res.stage_12_outcome_and_learning["candidate_knowledge_update"])

        # Compliance Summary
        self.assertTrue(res.compliance_summary["who_smart_dak_conformance"])
        self.assertTrue(res.compliance_summary["licensed_clinician_final_signoff"])

    # -------------------------------------------------------------------------
    # PART 3: Safety Firewall Invariants & Autonomous Hard-Blocks
    # -------------------------------------------------------------------------
    def test_04_safety_invariant_ai_signoff_hard_block(self):
        """Invariant: AI Copilot role can NEVER approve prescriptions or transition to APPROVED."""
        req_ai = ClinicalContinuumRequest(
            patient_id="P-AI-001",
            patient_name="Autonomous Attempt",
            age=35,
            gender="MALE",
            chief_complaints=["Knee tenderness"],
            presenting_condition="Waja-ul-Mafasil",
            symptom_duration_days=7,
            baseline_pain_vas=5.0,
            constitutional_signs={"dominant_humor": "Dam"},
            targeted_axes=["mafasil"],
            candidate_drugs=["Asgand"],
            clinician_id="BOT-AGY-AI",
            clinician_role="AI_COPILOT",
        )
        res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req_ai)
        self.assertFalse(res.stage_9_clinician_approval["is_ratified"])
        self.assertNotEqual(res.stage_9_clinician_approval["nuskha_state"], "APPROVED")
        self.assertIn("Security Violation", res.stage_9_clinician_approval["status_message"])

    def test_05_safety_invariant_pregnancy_contraindication_block(self):
        """Invariant: Teratogenic / abortifacient botanicals in pregnancy must be BLOCKED."""
        req_preg = ClinicalContinuumRequest(
            patient_id="P-PREG-002",
            patient_name="Fatima Zahra",
            age=27,
            gender="FEMALE",
            chief_complaints=["Joint inflammation"],
            presenting_condition="Waja-ul-Mafasil",
            symptom_duration_days=14,
            baseline_pain_vas=7.0,
            constitutional_signs={"dominant_humor": "Safra"},
            targeted_axes=["mafasil"],
            candidate_drugs=["Suranjan Shirin"],  # Colchicum contains colchicine -> contraindicated in pregnancy
            clinician_id="HAK-0042",
            clinician_role="HAKEEM",
            is_pregnant=True,
        )
        res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req_preg)
        self.assertEqual(res.stage_7_safety_firewall["decision"], "BLOCK")
        blocked_items = [item["id"] for item in res.stage_7_safety_firewall["items"] if item["status"] == "BLOCK"]
        self.assertIn("Suranjan Shirin", blocked_items)

    def test_06_safety_invariant_schedule_e1_poison_hard_block(self):
        """Invariant: Schedule E(1) statutory poison triggers autonomous hard-block flag."""
        req_e1 = ClinicalContinuumRequest(
            patient_id="P-TOX-003",
            patient_name="Tariq Mansoor",
            age=50,
            gender="MALE",
            chief_complaints=["Severe radiculopathy"],
            presenting_condition="Irq-un-Nasa",
            symptom_duration_days=45,
            baseline_pain_vas=9.0,
            constitutional_signs={"dominant_humor": "Sauda"},
            targeted_axes=["dimagh-asab"],
            candidate_drugs=["Kuchla", "Zanjabeel"],  # Kuchla is Strychnos nux-vomica (Schedule E1 poison)
            clinician_id="HAK-0042",
            clinician_role="HAKEEM",
        )
        res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req_e1)
        self.assertTrue(res.compliance_summary["schedule_e1_autonomous_hard_block_active"])

    # -------------------------------------------------------------------------
    # PART 4: Outcome Intelligence & Closed-Loop Learning Tests
    # -------------------------------------------------------------------------
    def test_07_closed_loop_learning_hipaa_safe_harbor(self):
        """HIPAA § 164.514(b)(2) irreversible salted hashing for RWE outcomes."""
        pid = "PATIENT-SECRET-MRN-994"
        h1 = ClosedLoopLearningEngine.deidentify_patient_id(pid)
        h2 = ClosedLoopLearningEngine.deidentify_patient_id(pid)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 16)
        self.assertNotIn("PATIENT", h1)
        self.assertNotIn("994", h1)

    def test_08_closed_loop_learning_cohort_metrics_and_cku(self):
        """Closed-loop statistical trajectory updates & Candidate Knowledge Update (CKU) generation."""
        # Feed 3 real-world patient outcomes into ClosedLoopLearningEngine
        for i, (vas_b, vas_f, out_cls) in enumerate([(8.0, 1.0, ClassicalOutcome.KAMIL),
                                                     (7.5, 2.0, ClassicalOutcome.KAMIL),
                                                     (8.0, 3.5, ClassicalOutcome.JUZ_I)]):
            eval_rec = OutcomeEvaluation(
                patient_id=f"P-LHS-{i+1}",
                deidentified_hash=ClosedLoopLearningEngine.deidentify_patient_id(f"P-LHS-{i+1}"),
                condition="Waja-ul-Mafasil",
                protocol_nuskha_id="NSK-MAFASIL-STD",
                day_in_treatment=14,
                vas_baseline=vas_b,
                vas_followup=vas_f,
                vas_improvement_percent=round(((vas_b - vas_f) / vas_b) * 100.0, 1),
                mizaj_restitution_score=0.85,
                adherence_percent=95.0,
                biomarker_deltas=[],
                composite_improvement_index=85.0 if out_cls == ClassicalOutcome.KAMIL else 55.0,
                outcome_class=out_cls,
                clinical_summary="Followup assessment",
                rwe_learning_eligible=True,
            )
            ClosedLoopLearningEngine.ingest_outcome_evaluation(eval_rec)

        summary = ClosedLoopLearningEngine.get_registry_summary()
        self.assertEqual(summary["total_patient_evaluations"], 3)
        self.assertIn("waja-ul-mafasil", summary["conditions"])

        # Generate Candidate Knowledge Update
        cku = ClosedLoopLearningEngine.evaluate_cohort_for_knowledge_update(
            condition="Waja-ul-Mafasil",
            protocol_nuskha_name="Waja-ul-Mafasil Standard Protocol",
            min_cohort_threshold=3,
        )
        self.assertIsNotNone(cku)
        self.assertIsInstance(cku, CandidateKnowledgeUpdate)
        self.assertEqual(cku.target_condition, "Waja-ul-Mafasil")
        self.assertEqual(cku.cohort_sample_size, 3)
        self.assertEqual(cku.governance_decision, "PENDING_PANEL_REVIEW")
        self.assertAlmostEqual(cku.remission_rate_kamil_percent, 66.7, places=1)
        self.assertEqual(cku.adverse_event_rate_percent, 0.0)
        self.assertIn("Meets WHO SMART Guidelines criteria", cku.clinical_rationale)

    # -------------------------------------------------------------------------
    # PART 5: Live API Endpoints Integration Tests
    # -------------------------------------------------------------------------
    def test_09_api_execute_continuum_endpoint(self):
        """Test POST /api/v1/clinical/continuum/execute via live API router."""
        payload = {
            "patient_id": "P-API-TEST",
            "patient_name": "Bilal Ahmad",
            "age": 48,
            "gender": "MALE",
            "chief_complaints": ["Knee pain", "Weather sensitivity"],
            "presenting_condition": "Waja-ul-Mafasil",
            "symptom_duration_days": 90,
            "baseline_pain_vas": 7.0,
            "constitutional_signs": {"dominant_humor": "Balgham"},
            "targeted_axes": ["mafasil"],
            "candidate_drugs": ["Suranjan Shirin", "Zanjabeel"],
            "clinician_id": "HAK-0042",
            "clinician_role": "HAKEEM",
            "is_pregnant": False,
            "has_renal_impairment": False,
            "followup_proms_day": 14,
            "followup_symptom_vas": 2.0,
            "followup_adverse_events": []
        }
        res = _call_post("/api/v1/clinical/continuum/execute", payload)
        self.assertTrue(res.get("ok"))
        self.assertIn("continuum_response", res)
        c_res = res["continuum_response"]
        self.assertEqual(c_res["patient_id"], "P-API-TEST")
        self.assertEqual(c_res["stage_9_clinician_approval"]["nuskha_state"], "APPROVED")
        self.assertTrue(c_res["stage_9_clinician_approval"]["is_ratified"])

    def test_10_api_who_smart_dak_endpoint(self):
        """Test GET /api/v1/clinical/continuum/who-smart-dak/mufrad/{name}."""
        res = _call_get("/api/v1/clinical/continuum/who-smart-dak/mufrad/Suranjan")
        self.assertTrue(res.get("ok"))
        self.assertIn("artifact", res)
        art = res["artifact"]
        self.assertEqual(art["version"], "1.0.0")
        self.assertTrue(len(art["sha256_hash"]) == 64)

    def test_11_api_learning_health_system_summary_endpoint(self):
        """Test GET /api/v1/clinical/continuum/learning-health-system/summary."""
        res = _call_get("/api/v1/clinical/continuum/learning-health-system/summary")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res.get("status"), "OPERATIONAL")
        self.assertIn("registry", res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
