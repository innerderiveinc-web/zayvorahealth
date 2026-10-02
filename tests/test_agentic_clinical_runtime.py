#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — Agentic Clinical AI Verification Suite
===========================================================
Verifies the complete ZAYVORA Agentic Clinical AI™ Production Architecture:
- 10-State Universal Agent Workflow State Machine (§20)
- Deterministic Safety Firewall (PASS, CAUTION, BLOCK, UNKNOWN) (§7, §28)
- Controlled Tool Registry & R0-R5 Risk Level boundaries (§17, §18)
- Sensing Quality Pre-Gate (Nabz & Lisan signal validation) (§12-14)
- Verification Loop & Provenance Envelopes (§21, §24)
- 21 CFR Part 11 SHA-256 HMAC Digital Signing at Human Approval Gate (§19)
"""

import unittest
import sys
import os

# Ensure AI service path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../services/ai")))

from app.agentic.models import (
    AgentState,
    RiskLevel,
    SafetyState,
    ClinicianDecision,
)
from app.agentic.tool_registry import ToolRegistry, ToolSecurityViolation
from app.agentic.safety_firewall import DeterministicSafetyFirewall
from app.agentic.agents import (
    ClinicalAgent,
    KnowledgeAgent,
    EvidenceAgent,
    SensingAgent,
    OperationsAgent,
    PharmacyAgent,
    PatientAgent,
    ResearchAgent,
)
from app.agentic.orchestrator import HakeemSahabOrchestrator


class TestAgenticClinicalRuntime(unittest.TestCase):

    def setUp(self):
        self.patient_valid = {
            "patient_id": "PAT-9011-VALID",
            "name": "Zayd Farooqi",
            "age": 42,
            "gender": "MALE",
            "allergies": [],
            "current_medications": [],
            "egfr": 95,
            "creatinine": 0.9,
            "vitals": {"bp": "120/80", "pulse": 72, "systolic_bp": 120},
        }
        self.encounter_valid = {
            "encounter_id": "ENC-2026-001",
            "chief_complaint": "Chronic joint stiffness and cold sensation in extremities",
            "vitals": {"bp": "120/80", "pulse": 72},
            "mizaj_assessment": {"dominant_humour": "Balghami", "temperament_type": "Cold & Moist"},
        }
        self.action_valid = {
            "herbs": ["Suranjan Shirin", "Zanjabeel", "Aslussoos"],
            "has_mudabbar_certificate": True,
        }

    # ── Test 1: State Machine Happy Path ─────────────────────────────────────
    def test_01_state_machine_happy_path(self):
        """Validates CREATED -> PLANNING -> RETRIEVING -> ANALYZING -> SAFETY_REVIEW -> AWAITING_APPROVAL -> APPROVED -> EXECUTING -> VERIFYING -> COMPLETED."""
        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=self.patient_valid,
            encounter_context=self.encounter_valid,
            proposed_action=self.action_valid,
            actor_id="DOC-01",
            role="DOCTOR",
        )

        # Must halt at Human Approval Gate
        self.assertEqual(run.state, AgentState.AWAITING_APPROVAL)
        self.assertEqual(run.safety_result.state, SafetyState.PASS)
        self.assertIsNotNone(run.output_payload)
        self.assertTrue(run.output_payload["requires_clinician_decision"])

        # Human Clinician Approves
        completed_run = HakeemSahabOrchestrator.clinician_submit_decision(
            run_id=run.run_id,
            decision=ClinicianDecision.ACCEPT,
            clinician_id="DOC-01",
            clinician_role="DOCTOR",
            clinician_notes="Approved classical concoction for Balghami dyscrasia.",
        )

        # Progression to completed with 21 CFR Part 11 digital signature
        self.assertEqual(completed_run.state, AgentState.COMPLETED)
        self.assertIsNotNone(completed_run.clinician_signature)
        self.assertEqual(len(completed_run.clinician_signature), 64)  # SHA-256 hex string
        self.assertEqual(completed_run.verification_status, "CRYPTOGRAPHICALLY_VERIFIED_SHA256_HMAC")
        self.assertIn("Prescription.signAndLock", completed_run.tools_invoked)

    # ── Test 2: Clinician Decision: MODIFY ───────────────────────────────────
    def test_02_clinician_modify_decision(self):
        """Clinician modifies proposed herbs before signing."""
        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=self.patient_valid,
            encounter_context=self.encounter_valid,
            proposed_action=self.action_valid,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.AWAITING_APPROVAL)

        custom_rx = {"herbs": ["Suranjan Shirin", "Filfil Siyah"], "tier1_munzij": "Custom Decoction"}
        modified_run = HakeemSahabOrchestrator.clinician_submit_decision(
            run_id=run.run_id,
            decision=ClinicianDecision.MODIFY,
            clinician_id="DOC-01",
            clinician_role="DOCTOR",
            clinician_notes="Reduced Aslussoos, added Filfil Siyah for gastric absorption.",
            modified_prescription=custom_rx,
        )
        self.assertEqual(modified_run.state, AgentState.COMPLETED)
        self.assertEqual(modified_run.output_payload["final_prescription"], custom_rx)

    # ── Test 3: Clinician Decision: REJECT ───────────────────────────────────
    def test_03_clinician_reject_decision(self):
        """Clinician rejects draft proposal; workflow cancels cleanly."""
        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=self.patient_valid,
            encounter_context=self.encounter_valid,
            proposed_action=self.action_valid,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.AWAITING_APPROVAL)

        rejected_run = HakeemSahabOrchestrator.clinician_submit_decision(
            run_id=run.run_id,
            decision=ClinicianDecision.REJECT,
            clinician_id="DOC-01",
            clinician_role="DOCTOR",
            clinician_notes="Patient requires immediate MRI before initiating any herbal therapy.",
        )
        self.assertEqual(rejected_run.state, AgentState.CANCELLED)
        self.assertIn("Clinician rejected AI proposal", rejected_run.error_message)

    # ── Test 4: Clinician Decision: DEFER ───────────────────────────────────
    def test_04_clinician_defer_decision(self):
        """Clinician defers action pending further tests; transitions to REQUIRES_CLINICIAN."""
        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=self.patient_valid,
            encounter_context=self.encounter_valid,
            proposed_action=self.action_valid,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.AWAITING_APPROVAL)

        deferred_run = HakeemSahabOrchestrator.clinician_submit_decision(
            run_id=run.run_id,
            decision=ClinicianDecision.DEFER,
            clinician_id="DOC-01",
            clinician_role="DOCTOR",
            clinician_notes="Awaiting fasting blood sugar report tomorrow morning.",
        )
        self.assertEqual(deferred_run.state, AgentState.REQUIRES_CLINICIAN)

    # ── Test 5: Deterministic Safety Firewall - Pregnancy Block ──────────────
    def test_05_safety_firewall_pregnancy_block(self):
        """Pregnant patient prescribed uterine stimulant (Abhal / Bish) must be HARD BLOCKED."""
        pregnant_patient = {
            "patient_id": "PAT-PREG-01",
            "age": 27,
            "gender": "FEMALE",
            "is_pregnant": True,
            "allergies": [],
            "current_medications": [],
        }
        toxic_action = {"herbs": ["Abhal", "Suranjan"], "has_mudabbar_certificate": True}

        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=pregnant_patient,
            encounter_context=self.encounter_valid,
            proposed_action=toxic_action,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.BLOCKED)
        self.assertEqual(run.safety_result.state, SafetyState.BLOCK)
        self.assertTrue(any("PREGNANCY_CONTRAINDICATION" in c["type"] for c in run.safety_result.contraindications_found))

    # ── Test 6: Deterministic Safety Firewall - Unknown Missing Data ─────────
    def test_06_safety_firewall_missing_pregnancy_status(self):
        """Female aged 15-50 with pregnancy status UNKNOWN prescribed active herbs transitions to REQUIRES_INPUT."""
        unknown_preg_patient = {
            "patient_id": "PAT-UNKNOWN-01",
            "age": 29,
            "gender": "FEMALE",
            "is_pregnant": None,  # Unknown!
            "allergies": [],
            "current_medications": [],
        }
        active_action = {"herbs": ["Abhal", "Zanjabeel"], "has_mudabbar_certificate": True}

        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=unknown_preg_patient,
            encounter_context=self.encounter_valid,
            proposed_action=active_action,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.REQUIRES_INPUT)
        self.assertEqual(run.safety_result.state, SafetyState.UNKNOWN)
        self.assertIn("Pregnancy status (required before prescribing reproductive/active botanicals)", run.safety_result.missing_critical_data)

    # ── Test 7: Deterministic Safety Firewall - Renal Failure Block ──────────
    def test_07_safety_firewall_renal_failure_block(self):
        """Nephrotoxic herbs prescribed to renal failure patient (eGFR < 30) must be BLOCKED."""
        renal_patient = {
            "patient_id": "PAT-RENAL-01",
            "age": 65,
            "gender": "MALE",
            "egfr": 22,  # Severe CKD
            "creatinine": 3.4,
            "allergies": [],
            "current_medications": [],
        }
        toxic_renal_action = {"herbs": ["Samm-ul-Far", "Suranjan"], "has_mudabbar_certificate": True}

        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=renal_patient,
            encounter_context=self.encounter_valid,
            proposed_action=toxic_renal_action,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.BLOCKED)
        self.assertEqual(run.safety_result.state, SafetyState.BLOCK)
        self.assertTrue(any("RENAL_FAILURE_CONTRAINDICATION" in c["type"] for c in run.safety_result.contraindications_found))

    # ── Test 8: Deterministic Safety Firewall - Schedule E(1) Mudabbar Gate ──
    def test_08_safety_firewall_schedule_e1_detox_gate(self):
        """Schedule E(1) toxic herbs (Azaraqi / Strychnos) without Mudabbar detox certificate must be BLOCKED."""
        unpurified_action = {
            "herbs": ["Azaraqi", "Suranjan Shirin"],
            "has_mudabbar_certificate": False,  # Missing detox certificate!
        }
        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=self.patient_valid,
            encounter_context=self.encounter_valid,
            proposed_action=unpurified_action,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.BLOCKED)
        self.assertEqual(run.safety_result.state, SafetyState.BLOCK)
        self.assertTrue(any("MUDABBAR_DETOX_REQUIRED" in c["type"] for c in run.safety_result.contraindications_found))

    # ── Test 9: Deterministic Safety Firewall - Patient Allergy Match ────────
    def test_09_safety_firewall_patient_allergy(self):
        """Prescribing an herb that matches patient allergy record must be BLOCKED."""
        allergic_patient = {
            **self.patient_valid,
            "allergies": ["Zanjabeel", "Ginger"],
        }
        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=allergic_patient,
            encounter_context=self.encounter_valid,
            proposed_action=self.action_valid,  # Contains Zanjabeel
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.BLOCKED)
        self.assertEqual(run.safety_result.state, SafetyState.BLOCK)
        self.assertTrue(any("PATIENT_ALLERGY_MATCH" in c["type"] for c in run.safety_result.contraindications_found))

    # ── Test 10: Deterministic Safety Firewall - Herb-Drug Caution ───────────
    def test_10_safety_firewall_herb_drug_caution(self):
        """Warfarin + Guggul interaction triggers CAUTION (proceeds to doctor with notice)."""
        cardiac_patient = {
            **self.patient_valid,
            "current_medications": ["Warfarin 5mg daily"],
        }
        guggul_action = {"herbs": ["Guggul", "Aslussoos"], "has_mudabbar_certificate": True}

        run = HakeemSahabOrchestrator.start_clinical_encounter_workflow(
            patient_context=cardiac_patient,
            encounter_context=self.encounter_valid,
            proposed_action=guggul_action,
            actor_id="DOC-01",
            role="DOCTOR",
        )
        self.assertEqual(run.state, AgentState.AWAITING_APPROVAL)
        self.assertEqual(run.safety_result.state, SafetyState.CAUTION)
        self.assertTrue(any("Warfarin" in r and "Guggul" in r for r in run.safety_result.reasons))

    # ── Test 11: Tool Registry Risk Level & Autonomous Privilege Escalation ──
    def test_11_tool_registry_risk_escalation_defense(self):
        """Autonomous AI can NEVER execute R4 (Prescription.signAndLock) or R5 (Governance) tools."""
        # AI attempting R4
        with self.assertRaises(ToolSecurityViolation):
            ToolRegistry.authorize_execution(
                tool_id="Prescription.signAndLock",
                actor_role="AI_AGENT",
                is_autonomous_ai=True,
                is_clinician_approved=False,
            )

        # AI attempting R5
        with self.assertRaises(ToolSecurityViolation):
            ToolRegistry.authorize_execution(
                tool_id="Governance.updateSafetyPolicy",
                actor_role="AI_AGENT",
                is_autonomous_ai=True,
                is_clinician_approved=False,
            )

        # Authorized doctor executing R4 with approval
        tool = ToolRegistry.authorize_execution(
            tool_id="Prescription.signAndLock",
            actor_role="DOCTOR",
            is_autonomous_ai=False,
            is_clinician_approved=True,
        )
        self.assertEqual(tool.risk_level, RiskLevel.R4_HIGH_IMPACT_CLINICAL)

    # ── Test 12: Sensing Quality Pre-Gate (Nabz Flow) ────────────────────────
    def test_12_sensing_pre_gate_nabz(self):
        """Sections 12-13: 'Is this measurement usable?' before 'What might this mean?'"""
        # Poor signal: excessive motion
        bad_nabz = {"signal_to_noise_ratio": 12.0, "motion_artifacts": True, "contact_pressure_kpa": 5.0}
        val_bad = SensingAgent.validate_nabz_signal(bad_nabz)
        self.assertFalse(val_bad.is_usable)
        self.assertIn("EXCESSIVE_PATIENT_MOTION", val_bad.quality_flags)
        self.assertIsNotNone(val_bad.rejection_reason)

        # Good signal
        good_nabz = {"signal_to_noise_ratio": 26.5, "motion_artifacts": False, "contact_pressure_kpa": 18.0}
        val_good = SensingAgent.validate_nabz_signal(good_nabz)
        self.assertTrue(val_good.is_usable)
        self.assertGreaterEqual(val_good.quality_score, 0.8)

    # ── Test 13: Sensing Quality Pre-Gate (Lisan Flow) ───────────────────────
    def test_13_sensing_pre_gate_lisan(self):
        """Section 14: Lisan tongue image quality and lighting check."""
        # Poor lighting (<300 lux) and blurry
        dim_image = {"ambient_lux": 150, "color_card_detected": False, "focus_sharpness": 0.40}
        val_dim = SensingAgent.validate_lisan_image(dim_image)
        self.assertFalse(val_dim.is_usable)
        self.assertIn("INSUFFICIENT_LIGHTING (<300 lux)", val_dim.quality_flags)

        # Crisp, bright lighting
        bright_image = {"ambient_lux": 750, "color_card_detected": True, "focus_sharpness": 0.92}
        val_bright = SensingAgent.validate_lisan_image(bright_image)
        self.assertTrue(val_bright.is_usable)

    # ── Test 14: Pharmacy FEFO Allocation Invariant ──────────────────────────
    def test_14_pharmacy_fefo_allocation(self):
        """Section 10: Pharmacy Agent allocates earliest expiring batch first (FEFO)."""
        batches = [
            {"batch_number": "LOT-2027-C", "expiry_date": "2027-12-31", "quantity": 100},
            {"batch_number": "LOT-2026-A", "expiry_date": "2026-10-15", "quantity": 40},  # Earliest!
            {"batch_number": "LOT-2027-B", "expiry_date": "2027-05-20", "quantity": 80},
        ]
        res = PharmacyAgent.allocate_fefo_batch("Majun Suranjan", batches)
        self.assertEqual(res["status"], "BATCH_ALLOCATED")
        self.assertEqual(res["allocated_batch"], "LOT-2026-A")
        self.assertEqual(res["expiry_date"], "2026-10-15")

    # ── Test 15: Research Agent Isolation Invariant ──────────────────────────
    def test_15_research_agent_isolation(self):
        """Section 11: RESEARCH != CLINICAL CARE. Query output explicitly warns against clinical use."""
        query = ResearchAgent.query_deidentified_cohort({"condition": "Type 2 Diabetes", "mizaj": "Damawi"})
        self.assertEqual(query["query_type"], "DEIDENTIFIED_RWE_COHORT")
        self.assertIn("RESEARCH DATA ONLY", query["clinical_isolation_notice"])

    # ── Test 16: Provenance Record Envelope ──────────────────────────────────
    def test_16_provenance_envelope(self):
        """Section 24: Knowledge retrievals must carry full provenance envelope."""
        res = KnowledgeAgent.retrieve("Aslussoos")
        prov = res["provenance"]
        self.assertIn("source_id", prov)
        self.assertIn("knowledge_version", prov)
        self.assertEqual(prov["review_status"], "GOVERNANCE_VERIFIED")
        self.assertIn("Ibn Sina", prov["citations"][0])

    # ── Test 17: Audit Trail Observability ───────────────────────────────────
    def test_17_audit_trail_observability(self):
        """Section 23: All significant agent events are recorded in immutable audit ledger."""
        logs = HakeemSahabOrchestrator.get_audit_logs(limit=10)
        self.assertGreater(len(logs), 0)
        latest = logs[-1]
        self.assertIn("event_id", latest)
        self.assertIn("run_id", latest)
        self.assertIn("event_type", latest)


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgenticClinicalRuntime)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == "__main__":
    unittest.main()
