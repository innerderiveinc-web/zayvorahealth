"""
Test Suite: ZAYVORA Clinical Intelligence Doctrine & Enterprise Implementation Blueprint
Reference:
  - ZAYVORA Health OS™ Clinical Intelligence Doctrine & Enterprise Implementation Blueprint
  - Version 1.0 - September 2026

Mechanisms Verified:
  1. 9-Layer Clinical Reasoning Stack (Mufradat -> Murakkab -> Nuskha -> Mizaj -> Organ-Axis -> Evidence -> Safety -> Copilot -> Clinician)
  2. E0 to E6 Evidence Hierarchy & Knowledge State Machine (10 Gates)
  3. Ten Invariants: What Must Never Happen (INV-01 to INV-10)
  4. Nuskha Approval State Machine & Hard AI Prescription Blocking
  5. Hakeem Sahab AI Copilot Tool Permission Model (Autonomous Diagnosis != Prescription)
  6. Live REST API Server Governance Endpoints
"""

import unittest
import json
import io
from unittest.mock import MagicMock

from services.knowledge.app.data.clinical_doctrine_spec import (
    CLINICAL_STACK_LAYERS,
    EVIDENCE_TIERS_E0_E6,
    KNOWLEDGE_STATES,
    WHAT_MUST_NEVER_HAPPEN,
    get_clinical_doctrine,
    get_evidence_tier_e,
    validate_knowledge_state_transition
)
from services.therapeutic.app.engines.nuskha_state_machine import NuskhaStateMachine
from services.ai.app.security.copilot_permission_guard import CopilotPermissionGuard
import services.live_api_server as las


class TestClinicalIntelligenceDoctrineSpec(unittest.TestCase):
    """Verifies core 9-layer doctrine, E0-E6 tiers, and knowledge state machine."""

    def test_nine_clinical_stack_layers(self):
        self.assertEqual(len(CLINICAL_STACK_LAYERS), 9)
        expected_keys = [
            "1_MUFRADAT", "2_MURAKKAB", "3_NUSKHA", "4_MIZAJ",
            "5_ORGAN_AXIS", "6_EVIDENCE", "7_SAFETY_FIREWALL",
            "8_HAKEEM_SAHAB", "9_CLINICIAN_APPROVAL"
        ]
        for k in expected_keys:
            self.assertIn(k, CLINICAL_STACK_LAYERS)

        # Check Murakkab formulation classes
        murakkab = CLINICAL_STACK_LAYERS["2_MURAKKAB"]
        self.assertIn("CLASS_A", murakkab["classes"])
        self.assertIn("CLASS_B", murakkab["classes"])
        self.assertIn("CLASS_C", murakkab["classes"])

    def test_evidence_tiers_e0_to_e6(self):
        self.assertEqual(len(EVIDENCE_TIERS_E0_E6), 7)
        for t in ["E0", "E1", "E2", "E3", "E4", "E5", "E6"]:
            tier_info = get_evidence_tier_e(t)
            self.assertIsNotNone(tier_info)
            self.assertEqual(tier_info["tier"], t)
            self.assertTrue("typical_source" in tier_info)
            self.assertTrue("allowed_representation" in tier_info)

        # E0 is historical only
        self.assertIn("strictly not clinical efficacy proof", EVIDENCE_TIERS_E0_E6["E0"]["allowed_representation"])
        # E5 is human RCTs
        self.assertIn("Controlled Clinical Evidence", EVIDENCE_TIERS_E0_E6["E5"]["name"])
        # E6 is meta-analysis
        self.assertIn("High-Confidence Synthesis", EVIDENCE_TIERS_E0_E6["E6"]["name"])

    def test_ten_invariants_what_must_never_happen(self):
        self.assertEqual(len(WHAT_MUST_NEVER_HAPPEN), 10)
        inv_ids = [inv["id"] for inv in WHAT_MUST_NEVER_HAPPEN]
        for i in range(1, 11):
            self.assertIn(f"INV-{i:02d}", inv_ids)

    def test_knowledge_state_transitions(self):
        # Valid: DRAFT -> SOURCE_VERIFIED -> STRUCTURED
        res1 = validate_knowledge_state_transition("DRAFT", "SOURCE_VERIFIED")
        self.assertTrue(res1["valid"])
        res2 = validate_knowledge_state_transition("SOURCE_VERIFIED", "STRUCTURED")
        self.assertTrue(res2["valid"])

        # Illegal skip: DRAFT -> AI_AVAILABLE (unscreened leap must fail)
        res_bad = validate_knowledge_state_transition("DRAFT", "AI_AVAILABLE")
        self.assertFalse(res_bad["valid"])


class TestNuskhaApprovalStateMachine(unittest.TestCase):
    """Verifies prescription lifecycle transitions and hard AI execution blocks."""

    def test_valid_clinician_progression(self):
        # Step 1: Draft to Safety Check
        r1 = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-001",
            current_state="DRAFT",
            target_state="SAFETY_CHECK",
            actor_id="dr-rashid",
            actor_role="DOCTOR",
            reason="Initiating safety screening"
        )
        self.assertTrue(r1["success"])
        self.assertEqual(r1["current_state"], "SAFETY_CHECK")

        # Step 2: Safety Check to Clinician Review
        r2 = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-001",
            current_state="SAFETY_CHECK",
            target_state="CLINICIAN_REVIEW",
            actor_id="dr-rashid",
            actor_role="DOCTOR",
            reason="Safety cleared"
        )
        self.assertTrue(r2["success"])

        # Step 3: Clinician Review to Approved
        r3 = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-001",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="dr-rashid",
            actor_role="DOCTOR",
            reason="Clinical review complete and approved by BUMS consultant",
            current_version=1
        )
        self.assertTrue(r3["success"])
        self.assertEqual(r3["current_state"], "APPROVED")
        self.assertEqual(r3["version"], 2) # Incremented on approval
        self.assertIn("AUD-NSK-", r3["audit_event"]["event_id"])

    def test_ai_attempt_to_approve_prescription_is_hard_blocked(self):
        # AI attempting to autonomously approve must trigger hard security rejection
        res = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-002",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="hakeem-sahab-llm",
            actor_role="HAKEEM_SAHAB_AI",
            reason="Autonomous AI approval attempt"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "AI_PRESCRIPTION_AUTHORITY_VIOLATION")
        self.assertIn("barred from setting state to 'APPROVED'", res["error"])

    def test_ai_attempt_to_dispense_is_hard_blocked(self):
        res = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-003",
            current_state="APPROVED",
            target_state="DISPENSED",
            actor_id="hakeem-sahab-llm",
            actor_role="AI_COPILOT",
            reason="Autonomous dispense attempt"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "AI_PRESCRIPTION_AUTHORITY_VIOLATION")

    def test_unauthorized_role_attempting_approval_fails(self):
        res = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-004",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="user-receptionist",
            actor_role="RECEPTIONIST",
            reason="Unauthorized approval attempt"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "INSUFFICIENT_ROLE_AUTHORITY")

    def test_illegal_state_skip_fails(self):
        # Cannot jump from DRAFT directly to APPROVED
        res = NuskhaStateMachine.transition(
            nuskha_id="NSK-2026-005",
            current_state="DRAFT",
            target_state="APPROVED",
            actor_id="dr-rashid",
            actor_role="DOCTOR",
            reason="Skipping safety check"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "ILLEGAL_STATE_TRANSITION")


class TestCopilotPermissionGuard(unittest.TestCase):
    """Verifies Hakeem Sahab AI copilot tool permission boundaries."""

    def test_safe_copilot_actions_are_allowed(self):
        for act in ["read_patient_chart", "retrieve_knowledge", "summarize_evidence", "flag_safety_issue", "draft_questions"]:
            res = CopilotPermissionGuard.evaluate_permission(act, actor_role="HAKEEM_SAHAB_AI")
            self.assertTrue(res["allowed"])
            self.assertEqual(res["status"], "ALLOWED")

    def test_draft_plan_is_allowed_as_draft_only(self):
        res = CopilotPermissionGuard.evaluate_permission("draft_plan", actor_role="HAKEEM_SAHAB_AI")
        self.assertTrue(res["allowed"])
        self.assertEqual(res["status"], "ALLOWED_DRAFT_ONLY")

    def test_restricted_clinical_actions_are_blocked_for_ai(self):
        blocked_actions = ["finalize_prescription", "dispense_medication", "change_approved_nuskha", "change_safety_rules"]
        for act in blocked_actions:
            res = CopilotPermissionGuard.evaluate_permission(act, actor_role="HAKEEM_SAHAB_AI")
            self.assertFalse(res["allowed"])
            self.assertEqual(res["status"], "BLOCKED")
            self.assertIn("HARD STOP", res["reason"])

    def test_clinician_authority_overrides_tool_gates(self):
        res = CopilotPermissionGuard.evaluate_permission("finalize_prescription", actor_role="DOCTOR")
        self.assertTrue(res["allowed"])
        self.assertEqual(res["status"], "ALLOWED_CLINICIAN_AUTHORITY")


class TestLiveApiDoctrineEndpoints(unittest.TestCase):
    """Verifies REST endpoints for doctrine, state machine, and copilot permissions."""

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"
        self.handler._get_auth_context = lambda: {
            "user_id": "test-practitioner",
            "roles": ["SUPER_ADMIN"],
            "clinic_id": "facility-delhi-01"
        }

    def test_get_doctrine_spec_endpoint(self):
        self.handler.path = "/api/v1/governance/doctrine/spec"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/governance/doctrine/spec HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertIn("stack_layers", body["doctrine"])
        self.assertEqual(len(body["doctrine"]["stack_layers"]), 9)
        self.assertEqual(len(body["doctrine"]["invariants"]), 10)

    def test_get_knowledge_state_machine_endpoint(self):
        self.handler.path = "/api/v1/governance/knowledge/state-machine"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/governance/knowledge/state-machine HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(len(body["states"]), 10)

    def test_get_copilot_permissions_endpoint(self):
        self.handler.path = "/api/v1/ai/copilot/permissions"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/ai/copilot/permissions HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertIn("finalize_prescription", body["copilot_permission_matrix"])

    def test_post_nuskha_transition_endpoint(self):
        payload = json.dumps({
            "nuskha_id": "NSK-API-001",
            "current_state": "CLINICIAN_REVIEW",
            "target_state": "APPROVED",
            "actor_id": "dr-hakeem-irfan",
            "actor_role": "DOCTOR",
            "reason": "Prescription verified and approved with classical Musleh"
        }).encode("utf-8")
        self.handler.path = "/api/v1/therapeutic/nuskha/transition"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/therapeutic/nuskha/transition HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(body["transition_result"]["current_state"], "APPROVED")

    def test_post_ai_forbidden_transition_returns_403(self):
        payload = json.dumps({
            "nuskha_id": "NSK-API-002",
            "current_state": "CLINICIAN_REVIEW",
            "target_state": "APPROVED",
            "actor_id": "hakeem-ai-agent",
            "actor_role": "HAKEEM_SAHAB_AI",
            "reason": "Unauthorized AI approval"
        }).encode("utf-8")
        self.handler.path = "/api/v1/therapeutic/nuskha/transition"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/therapeutic/nuskha/transition HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("403 Forbidden", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertFalse(body["ok"])
        self.assertEqual(body["transition_result"]["code"], "AI_PRESCRIPTION_AUTHORITY_VIOLATION")

    def test_post_evaluate_permission_endpoint(self):
        payload = json.dumps({
            "action": "finalize_prescription",
            "actor_role": "HAKEEM_SAHAB_AI"
        }).encode("utf-8")
        self.handler.path = "/api/v1/ai/copilot/evaluate-permission"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/ai/copilot/evaluate-permission HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertFalse(body["permission_evaluation"]["allowed"])
        self.assertEqual(body["permission_evaluation"]["status"], "BLOCKED")

    def test_get_patient_360_endpoint(self):
        self.handler.path = "/api/v1/patient/360/MRN-2026-TARIQ"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/patient/360/MRN-2026-TARIQ HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        panels = body["patient_360"]["panels"]
        self.assertEqual(len(panels), 10)
        self.assertIn("identity_and_consent", panels)
        self.assertIn("mizaj", panels)
        self.assertIn("care_plan", panels)

    def test_post_canonical_safety_evaluate_endpoint(self):
        payload = json.dumps({
            "patient_id": "P-TEST-01",
            "candidate_interventions": ["SARPAGANDHA", "AMLA"],
            "context": {"current_therapies": ["ANTIHYPERTENSIVE"]}
        }).encode("utf-8")
        self.handler.path = "/api/v1/safety/evaluate"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/safety/evaluate HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(body["safety_evaluation"]["decision"], "CAUTION")

    def test_post_hakeem_case_brief_endpoint(self):
        payload = json.dumps({
            "patient_id": "P-TEST-02",
            "patient_context": {"name": "Zayd", "age": 40, "chief_complaints": ["Lethargy"]}
        }).encode("utf-8")
        self.handler.path = "/api/v1/hakeem/case-brief"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/hakeem/case-brief HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        brief = body["case_brief"]
        self.assertIn("case_summary", brief)
        self.assertIn("evidence_items", brief)
        self.assertEqual(brief["clinician_approval_state"], "NOT_REVIEWED")


if __name__ == "__main__":
    unittest.main()
