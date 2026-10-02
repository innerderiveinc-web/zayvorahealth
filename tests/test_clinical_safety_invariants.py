#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Permanent Clinical Safety Invariants Test Suite
====================================================================
Validates all 10 non-negotiable clinical safety invariants (SAFETY-001 through SAFETY-010):

SAFETY-001: Autonomous AI copilot prescription approval is strictly blocked.
SAFETY-002: IT / System Administrator (SUPER_ADMIN) prescribing is strictly barred.
SAFETY-003: Unverified / unregistered clinician prescription sign-off fails closed.
SAFETY-004: Safety BLOCK status hard-blocks clinical prescription approval.
SAFETY-005: Safety UNKNOWN status fails closed (no fail-open permitted).
SAFETY-006: Safety CAUTION requires mandatory signed clinician acknowledgement rationale.
SAFETY-007: Schedule E(1) statutory poisons require mandatory Mudabbar & dosage ceilings.
SAFETY-008: Confusable species detection (Asaroon vs Tagar) enforces adulteration barriers.
SAFETY-009: Pre-clinical E1/E2 evidence cannot assert human clinical efficacy.
SAFETY-010: Closed-loop learning proposals remain staged and cannot alter runtime rules without board ratification.
"""

from __future__ import annotations

import os
import sys
import unittest
from typing import Any, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.therapeutic.app.engines.nuskha_state_machine import (
    NuskhaStateMachine,
    UnverifiedClinicianException,
    SafetyBlockException,
    SafetyIncompleteException,
    MissingClinicianRationaleException,
    AdministrativePrescriptionForbiddenException
)
from services.identity.app.core.clinician_registry_service import ClinicianRegistryService
from services.knowledge.app.core.canonical_substance_identity import CanonicalSubstanceIdentityService
from services.knowledge.app.engines.evidence_claim_grounding_engine import (
    EvidenceClaimGroundingEngine,
    EvidenceTier
)
from services.clinical.app.engines.closed_loop_learning_engine import (
    ClosedLoopLearningEngine,
    CandidateKnowledgeUpdate
)
from services.clinical.app.engines.outcome_intelligence_engine import (
    OutcomeEvaluation,
    ClassicalOutcome
)
from services.therapeutic.app.engines.nuskha_compiler import compile_nuskha


class TestClinicalSafetyInvariants(unittest.TestCase):
    """Permanent Hardened Regression Suite for ZAYVORA Clinical Safety Invariants."""

    # -------------------------------------------------------------------------
    # SAFETY-001: AI Prescription Approval Blocked
    # -------------------------------------------------------------------------
    def test_safety_001_ai_prescription_approval_blocked(self):
        """Invariant: Autonomous AI must never transition a prescription to APPROVED."""
        for ai_role in ["AI", "AI_COPILOT", "HAKEEM_SAHAB_AI", "BOT"]:
            res = NuskhaStateMachine.transition(
                nuskha_id="NSK-SAFE-001",
                current_state="CLINICIAN_REVIEW",
                target_state="APPROVED",
                actor_id="ai-agent-01",
                actor_role=ai_role,
                reason="Attempted autonomous AI prescribing"
            )
            self.assertFalse(res["success"], f"AI role {ai_role} must be blocked from APPROVED")
            self.assertEqual(res["code"], "AI_PRESCRIPTION_AUTHORITY_VIOLATION")
            self.assertIn("barred from setting state to 'APPROVED'", res["error"])

    # -------------------------------------------------------------------------
    # SAFETY-002: Administrative Prescribing Barred
    # -------------------------------------------------------------------------
    def test_safety_002_admin_prescribing_barred(self):
        """Invariant: Administrative roles (SUPER_ADMIN, ADMIN) cannot prescribe or approve medications."""
        for admin_role in ["SUPER_ADMIN", "ADMIN"]:
            res = NuskhaStateMachine.transition(
                nuskha_id="NSK-SAFE-002",
                current_state="CLINICIAN_REVIEW",
                target_state="APPROVED",
                actor_id="sysadmin-user-01",
                actor_role=admin_role,
                reason="Administrative override prescription attempt"
            )
            self.assertFalse(res["success"], f"Admin role {admin_role} must be barred from APPROVED")
            self.assertEqual(res["code"], "INSUFFICIENT_ROLE_AUTHORITY")

            # Verify exception is raised when raise_on_error is requested
            with self.assertRaises(AdministrativePrescriptionForbiddenException):
                NuskhaStateMachine.transition(
                    nuskha_id="NSK-SAFE-002",
                    current_state="CLINICIAN_REVIEW",
                    target_state="APPROVED",
                    actor_id="sysadmin-user-01",
                    actor_role=admin_role,
                    reason="Administrative override attempt",
                    raise_on_error=True
                )

    # -------------------------------------------------------------------------
    # SAFETY-003: Unverified Clinician Prescription Approval Blocked
    # -------------------------------------------------------------------------
    def test_safety_003_unverified_clinician_fails_closed(self):
        """Invariant: Clinician not active/verified in statutory registry cannot approve prescriptions."""
        unverified_ids = ["unverified_dr_jones", "imposter_clinician_99", "fake-doctor-01"]
        for unverified_id in unverified_ids:
            res = NuskhaStateMachine.transition(
                nuskha_id="NSK-SAFE-003",
                current_state="CLINICIAN_REVIEW",
                target_state="APPROVED",
                actor_id=unverified_id,
                actor_role="DOCTOR",
                reason="Unverified clinician sign-off attempt"
            )
            self.assertFalse(res["success"])
            self.assertIn(res["code"], ["CLINICIAN_NOT_REGISTERED", "CLINICIAN_NOT_VERIFIED"])

            with self.assertRaises(UnverifiedClinicianException):
                NuskhaStateMachine.transition(
                    nuskha_id="NSK-SAFE-003",
                    current_state="CLINICIAN_REVIEW",
                    target_state="APPROVED",
                    actor_id=unverified_id,
                    actor_role="DOCTOR",
                    reason="Unverified sign-off",
                    raise_on_error=True
                )

    # -------------------------------------------------------------------------
    # SAFETY-004: Safety BLOCK Status Hard-Blocks Approval
    # -------------------------------------------------------------------------
    def test_safety_004_safety_block_prohibits_approval(self):
        """Invariant: Prescription with safety status BLOCK cannot be approved under any circumstances."""
        res = NuskhaStateMachine.transition(
            nuskha_id="NSK-SAFE-004",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="CLN-IRFAN-01",
            actor_role="DOCTOR",
            reason="Attempting approval despite critical toxicity flag",
            safety_status="BLOCK"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "SAFETY_BLOCK_CONTRAINDICATION")
        self.assertIn("prohibited", res["error"].lower())

        with self.assertRaises(SafetyBlockException):
            NuskhaStateMachine.transition(
                nuskha_id="NSK-SAFE-004",
                current_state="CLINICIAN_REVIEW",
                target_state="APPROVED",
                actor_id="CLN-IRFAN-01",
                actor_role="DOCTOR",
                reason="Toxicity override",
                safety_status="BLOCK",
                raise_on_error=True
            )

    # -------------------------------------------------------------------------
    # SAFETY-005: Safety UNKNOWN Status Fails Closed
    # -------------------------------------------------------------------------
    def test_safety_005_safety_unknown_fails_closed(self):
        """Invariant: Prescription with UNKNOWN safety evaluation must fail closed."""
        res = NuskhaStateMachine.transition(
            nuskha_id="NSK-SAFE-005",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="CLN-IRFAN-01",
            actor_role="DOCTOR",
            reason="Approving without completed safety check",
            safety_status="UNKNOWN"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["code"], "SAFETY_EVALUATION_INCOMPLETE")

        with self.assertRaises(SafetyIncompleteException):
            NuskhaStateMachine.transition(
                nuskha_id="NSK-SAFE-005",
                current_state="CLINICIAN_REVIEW",
                target_state="APPROVED",
                actor_id="CLN-IRFAN-01",
                actor_role="DOCTOR",
                reason="Incomplete check override",
                safety_status="UNKNOWN",
                raise_on_error=True
            )

    # -------------------------------------------------------------------------
    # SAFETY-006: Safety CAUTION Requires Signed Clinician Rationale
    # -------------------------------------------------------------------------
    def test_safety_006_safety_caution_requires_rationale(self):
        """Invariant: CAUTION safety status requires explicit signed clinician justification rationale."""
        # 1. Missing rationale -> FAILS
        res_missing = NuskhaStateMachine.transition(
            nuskha_id="NSK-SAFE-006",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="CLN-IRFAN-01",
            actor_role="DOCTOR",
            reason="Approving caution prescription",
            safety_status="CAUTION",
            clinician_acknowledgement_rationale=""
        )
        self.assertFalse(res_missing["success"])
        self.assertEqual(res_missing["code"], "MISSING_CLINICIAN_RATIONALE")

        with self.assertRaises(MissingClinicianRationaleException):
            NuskhaStateMachine.transition(
                nuskha_id="NSK-SAFE-006",
                current_state="CLINICIAN_REVIEW",
                target_state="APPROVED",
                actor_id="CLN-IRFAN-01",
                actor_role="DOCTOR",
                reason="Approving caution prescription",
                safety_status="CAUTION",
                clinician_acknowledgement_rationale=None,
                raise_on_error=True
            )

        # 2. Provided rationale -> SUCCEEDS with cryptographic signature
        res_valid = NuskhaStateMachine.transition(
            nuskha_id="NSK-SAFE-006",
            current_state="CLINICIAN_REVIEW",
            target_state="APPROVED",
            actor_id="CLN-IRFAN-01",
            actor_role="DOCTOR",
            reason="Approving with explicit Musleh rationale",
            safety_status="CAUTION",
            clinician_acknowledgement_rationale="Patient monitored weekly; Roghan-e-Badam Musleh prescribed to mitigate GI warmth."
        )
        self.assertTrue(res_valid["success"])
        self.assertEqual(res_valid["current_state"], "APPROVED")
        self.assertTrue(res_valid.get("digital_signature"))

    # -------------------------------------------------------------------------
    # SAFETY-007: Schedule E(1) Poison Gating & Mudabbar Enforced
    # -------------------------------------------------------------------------
    def test_safety_007_schedule_e1_poison_mudabbar_enforced(self):
        """Invariant: Schedule E1 poisons (Kuchla, Suranjan Talkh) require Mudabbar and carry statutory warnings."""
        for poison_query in ["Suranjan Talkh", "Kuchla", "Bhilawa", "Jamalgota"]:
            sub = CanonicalSubstanceIdentityService.resolve_substance(poison_query)
            self.assertTrue(sub["matched"])
            self.assertTrue(sub["is_schedule_e1"])
            self.assertTrue(sub["mandatory_mudabbar"])
            self.assertIsNotNone(sub["mudabbar_protocol"])
            self.assertGreater(len(sub["toxic_alkaloids"]), 0)

        # In formulation compiler:
        compiled = compile_nuskha(
            target_organ_axes=["mafasil"],
            therapeutic_objective="Anti-arthritic",
            ingredients=[{"name": "Suranjan Talkh", "dose_mg": 200}],
            patient_context={"age": 45}
        )
        ing = compiled["compiled_ingredients"][0]
        self.assertEqual(ing["canonical_id"], "ZMF-002")
        self.assertTrue(ing["is_schedule_e1"])
        self.assertTrue(ing["is_mudabbar"])

    # -------------------------------------------------------------------------
    # SAFETY-008: Confusable Species Disambiguation & Adulteration Barrier
    # -------------------------------------------------------------------------
    def test_safety_008_confusable_species_disambiguation(self):
        """Invariant: Confusable commercial species (Asaroon vs Tagar, Chiraita vs Kalmegh) must be flagged."""
        # Pair 1: Asaroon vs Tagar
        is_conf, notes = CanonicalSubstanceIdentityService.is_confusable("Asaroon", "Tagar")
        self.assertTrue(is_conf)
        self.assertIn("Aristolochiaceae", notes)

        # Pair 2: Chiraita vs Kalmegh
        is_conf2, notes2 = CanonicalSubstanceIdentityService.is_confusable("Chiraita", "Kalmegh")
        self.assertTrue(is_conf2)

        # Resolution resolves to different botanical identities
        asaroon = CanonicalSubstanceIdentityService.resolve_substance("Asaroon")
        tagar = CanonicalSubstanceIdentityService.resolve_substance("Tagar")
        self.assertEqual(asaroon["canonical_id"], "ZMF-014")
        self.assertEqual(tagar["canonical_id"], "ZMF-015")
        self.assertNotEqual(asaroon["family"], tagar["family"])

    # -------------------------------------------------------------------------
    # SAFETY-009: Pre-Clinical E1/E2 Extrapolation Prohibition
    # -------------------------------------------------------------------------
    def test_safety_009_preclinical_extrapolation_prohibition(self):
        """Invariant: In-vitro (E1) or animal (E2) evidence cannot assert proven human clinical efficacy."""
        # Claim with pre-clinical E1 asserting human efficacy -> FAILS
        extrapolation_claim = {
            "source_id": "SRC-UPI-VOL1",
            "page_number": 5,
            "passage_text": "In-vitro assay showed 92% COX-2 down-regulation.",
            "evidence_tier": "E1",
            "asserts_human_efficacy": True,
            "confidence_score": 0.90
        }
        val = EvidenceClaimGroundingEngine.validate_claim(extrapolation_claim)
        self.assertFalse(val["is_valid"])
        self.assertIn("Extrapolation Violation", val["errors"][0])

        # Claim with proper pre-clinical disclaimer without asserting human efficacy -> PASSES with warning
        proper_claim = {
            "source_id": "SRC-UPI-VOL1",
            "page_number": 5,
            "passage_text": "In-vitro assay showed 92% COX-2 down-regulation in cellular models.",
            "evidence_tier": "E1",
            "asserts_human_efficacy": False,
            "confidence_score": 0.90
        }
        val_proper = EvidenceClaimGroundingEngine.validate_claim(proper_claim)
        self.assertTrue(val_proper["is_valid"])
        self.assertIsNotNone(val_proper["preclinical_warning"])

    # -------------------------------------------------------------------------
    # SAFETY-010: Research Learning Firewall (Zero Bleed into Runtime)
    # -------------------------------------------------------------------------
    def test_safety_010_research_learning_firewall(self):
        """Invariant: Closed-loop learning proposals remain staged and cannot alter runtime rules without board ratification."""
        ClosedLoopLearningEngine.clear_registry()

        eval1 = OutcomeEvaluation(
            patient_id="P-TEST-001",
            deidentified_hash="hash-abc-001",
            condition="Waja-ul-Mafasil",
            protocol_nuskha_id="NSK-TEST-01",
            day_in_treatment=14,
            vas_baseline=8.0,
            vas_followup=2.0,
            vas_improvement_percent=75.0,
            mizaj_restitution_score=85.0,
            adherence_percent=95.0,
            biomarker_deltas=[],
            composite_improvement_index=80.0,
            outcome_class=ClassicalOutcome.KAMIL,
            clinical_summary="High efficacy observed in patient cohort.",
            rwe_learning_eligible=True
        )
        ClosedLoopLearningEngine.ingest_outcome_evaluation(eval1)
        cku = ClosedLoopLearningEngine.evaluate_cohort_for_knowledge_update("Waja-ul-Mafasil", min_cohort_threshold=1)

        self.assertIsNotNone(cku)
        self.assertEqual(cku.governance_status, "PENDING_CLINICAL_BOARD_REVIEW")
        self.assertFalse(cku.is_promoted_to_production)
        self.assertEqual(cku.staging_partition, "RESEARCH_STAGING_ISOLATED")

        # Invariant: Unpromoted proposal is NOT active in production runtime
        self.assertFalse(ClosedLoopLearningEngine.is_rule_active_in_production(cku.update_id))

        # Attempt to promote without board resolution fails
        res_no_res = ClosedLoopLearningEngine.promote_proposal_to_production(
            proposal_id=cku.update_id,
            board_resolution_id="",
            signed_by_clinician_id="CLN-IRFAN-01"
        )
        self.assertFalse(res_no_res["promoted"])

        # Formal promotion with valid resolution succeeds
        res_prom = ClosedLoopLearningEngine.promote_proposal_to_production(
            proposal_id=cku.update_id,
            board_resolution_id="RES-GOV-2026-09-001",
            signed_by_clinician_id="CLN-IRFAN-01"
        )
        self.assertTrue(res_prom["promoted"])
        self.assertTrue(ClosedLoopLearningEngine.is_rule_active_in_production(cku.update_id))


if __name__ == "__main__":
    unittest.main()
