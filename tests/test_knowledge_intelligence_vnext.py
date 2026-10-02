"""
ZAYVORA Health OS™ — Test Suite #61: Knowledge Intelligence & Clinical Governance vNEXT
=======================================================================================
Verifies the complete 18-Phase source-governed, evidence-linked, safety-controlled
clinical knowledge intelligence pipeline:
- Canonical Drug Registry & Confusable Species Disambiguation
- Source Provenance Completeness (Zero Fabricated Citations)
- Classical Validation Engine (Strict NOT_VERIFIED for unknowns)
- Independent Pharmacopoeial Crosswalk (UPI & NFUM)
- Evidence Engine v2 (Prohibition of in-vitro extrapolation to human efficacy)
- Safety Firewall v2 (5 AI Safety States)
- 12-State Knowledge State Machine (Strict sequential transitions)
- Grounded Hakeem Sahab Copilot Disclosures
- Organ-Axis Review Workflow
- Murakkab Class Separation & Formulation Governance
- Reviewer Workspace 8 Actions & Immutable Audit Logging
- Patient Safety Anti-Leakage Barrier
- Live REST API Endpoints Bridge
"""

import sys
import os
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.engines.knowledge_intelligence_vnext import (
    CanonicalDrugRegistry,
    SourceProvenanceEngine,
    ClassicalValidationEngine,
    PharmacopoeialCrosswalkEngine,
    EvidenceEngineV2,
    SafetyFirewallV2,
    KnowledgeStateMachine,
    GroundedHakeemSahabVNext,
    OrganAxisReviewEngine,
    MurakkabGovernanceEngine,
    ReviewerWorkspaceEngine,
    PatientSafetyBarrier,
    KnowledgeState,
    AISafetyState,
    ReviewerAction,
    MurakkabClass,
    IngredientRole,
    GOLD_BENCHMARK_25_IDS,
)
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
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


def _call_post(path, payload):
    data = json.dumps(payload).encode()
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {"Content-Length": str(len(data))}
    req.request_version = "HTTP/1.1"
    req.rfile = io.BytesIO(data)
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_POST()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


class TestKnowledgeIntelligenceVNext(unittest.TestCase):
    """Full acceptance test suite for vNEXT Knowledge Intelligence & Clinical Governance."""

    # -------------------------------------------------------------------------
    # 1. Canonical Drug Identity & Confusable Disambiguation
    # -------------------------------------------------------------------------
    def test_canonical_drug_identity_reconciliation_mulethi(self):
        """Mulethi must reconcile to ZMF-096 Asl-us-Soos without duplicate creation."""
        res = CanonicalDrugRegistry.reconcile_drug_identity("Mulethi")
        self.assertTrue(res["matched"])
        self.assertEqual(res["canonical_id"], "ZMF-096")
        self.assertEqual(res["canonical_unani_name"], "Asl-us-Soos")
        self.assertEqual(res["botanical_name"], "Glycyrrhiza glabra")
        self.assertFalse(res.get("confusable_alert", False))

    def test_canonical_drug_identity_reconciliation_ashwagandha(self):
        """Ashwagandha must reconcile to ZMF-005 Asgandh."""
        res = CanonicalDrugRegistry.reconcile_drug_identity("Ashwagandha")
        self.assertTrue(res["matched"])
        self.assertEqual(res["canonical_id"], "ZMF-005")
        self.assertEqual(res["canonical_unani_name"], "Asgandh")

    def test_confusable_species_disambiguation_asaroon_vs_tagar(self):
        """Asaroon (ZMF-014) and Tagar (ZMF-015) must trigger confusable alerts."""
        res_asaroon = CanonicalDrugRegistry.reconcile_drug_identity("Asaroon")
        self.assertTrue(res_asaroon["matched"])
        self.assertEqual(res_asaroon["canonical_id"], "ZMF-014")
        self.assertTrue(res_asaroon.get("confusable_alert"))
        self.assertEqual(res_asaroon["differentiating_notes"]["confusable_with"], "ZMF-015 Tagar")

        res_tagar = CanonicalDrugRegistry.reconcile_drug_identity("Tagar")
        self.assertTrue(res_tagar["matched"])
        self.assertEqual(res_tagar["canonical_id"], "ZMF-015")
        self.assertTrue(res_tagar.get("confusable_alert"))
        self.assertEqual(res_tagar["differentiating_notes"]["confusable_with"], "ZMF-014 Asaroon")

    # -------------------------------------------------------------------------
    # 2. Source Provenance Completeness
    # -------------------------------------------------------------------------
    def test_source_provenance_validation_rejects_incomplete_citation(self):
        """Book-title-only citation without pages or volume must fail."""
        incomplete_citation = {
            "source_type": "CLASSICAL",
            "work_title": "Al-Qanun fi al-Tibb",
            "author": "Ibn Sina",
            # missing volume, pages, edition_or_year
        }
        valid, missing = SourceProvenanceEngine.validate_citation_completeness(incomplete_citation)
        self.assertFalse(valid)
        self.assertTrue(any("volume" in m for m in missing))
        self.assertTrue(any("pages" in m for m in missing))
        self.assertTrue(any("edition" in m for m in missing))

    def test_source_provenance_validation_accepts_complete_citation(self):
        """Complete classical citation with all 5 mandatory fields must pass."""
        complete_citation = {
            "source_type": "CLASSICAL",
            "work_title": "Al-Qanun fi al-Tibb",
            "author": "Ibn Sina (Avicenna)",
            "edition_or_year": "1593 Rome Ed. / New Delhi Reprint 1993",
            "volume": "Vol. II",
            "pages": "pp. 120-122",
            "passage_text": "Asl-us-Soos: Muattil-e-Akhlat, Muaddil, Naf-e-Khashunat-e-Sadr."
        }
        valid, missing = SourceProvenanceEngine.validate_citation_completeness(complete_citation)
        self.assertTrue(valid)
        self.assertEqual(len(missing), 0)

    # -------------------------------------------------------------------------
    # 3. Classical Validation Engine
    # -------------------------------------------------------------------------
    def test_classical_validation_missing_parameters_remain_unverified(self):
        """Empty classical parameters must be flagged as NOT_VERIFIED, never hallucinated."""
        sparse_profile = {
            "mizaj_primary": "Hot",
            "daraja": None,
            "afaal": ["Muhafiz-e-Kabid"],
            "muzir": None,
            "musleh": None,
            "badal": None,
            "tadbeer_required": False
        }
        audit = ClassicalValidationEngine.audit_classical_profile(sparse_profile)
        self.assertFalse(audit["is_complete"])
        self.assertEqual(audit["fields_audit"]["daraja"], "NOT_VERIFIED")
        self.assertEqual(audit["fields_audit"]["muzir"], "NOT_VERIFIED")
        self.assertEqual(audit["fields_audit"]["musleh"], "NOT_VERIFIED")
        self.assertEqual(audit["fields_audit"]["badal"], "NOT_VERIFIED")

    # -------------------------------------------------------------------------
    # 4. Pharmacopoeial Crosswalk
    # -------------------------------------------------------------------------
    def test_pharmacopoeial_crosswalk_independent_tracking(self):
        """UPI and NFUM editions must be independently recorded with E1 status."""
        entry = PharmacopoeialCrosswalkEngine.verify_pharmacopoeial_entry(
            upi_part="Part I",
            upi_volume="Vol I",
            upi_monograph_title="Asl-us-Soos (Liquorice Root)",
            nfum_part="Part II",
            nfum_edition="2007",
            nfum_entry="Entry 42",
            is_schedule_e1=False
        )
        self.assertTrue(entry["verified"])
        self.assertEqual(entry["upi"]["monograph_title"], "Asl-us-Soos (Liquorice Root)")
        self.assertEqual(entry["nfum"]["edition"], "2007")
        self.assertFalse(entry["is_schedule_e1"])

    # -------------------------------------------------------------------------
    # 5. Evidence Engine v2 & In-Vitro Guardrail
    # -------------------------------------------------------------------------
    def test_evidence_engine_in_vitro_extrapolation_blocked(self):
        """Extrapolating in-vitro (E1) data to human clinical efficacy must be strictly blocked."""
        illicit_claim = {
            "claim_type": "HUMAN_CLINICAL_EFFICACY",
            "claimed_benefit": "Cures advanced osteoarthritis in humans within 14 days",
            "evidence_tier": "E1",  # In-vitro cell culture only
            "supporting_studies": [{"type": "in_vitro_cell_assay", "source": "Cell Biology Lab 2024"}]
        }
        res = EvidenceEngineV2.evaluate_claim_evidence(illicit_claim)
        self.assertFalse(res["accepted"])
        self.assertIn("IN_VITRO_EXTRAPOLATION_PROHIBITED", res["flags"])
        self.assertEqual(res["assigned_evidence_level"], "E1")

    def test_evidence_engine_valid_clinical_claim(self):
        """RCT human clinical trial (E5) is properly evaluated and accepted."""
        valid_claim = {
            "claim_type": "HUMAN_CLINICAL_EFFICACY",
            "claimed_benefit": "Reduces chronic dry cough symptoms",
            "evidence_tier": "E5",  # Randomized controlled clinical trial
            "supporting_studies": [{"type": "human_double_blind_rct", "sample_size": 120, "p_value": 0.01}]
        }
        res = EvidenceEngineV2.evaluate_claim_evidence(valid_claim)
        self.assertTrue(res["accepted"])
        self.assertEqual(res["assigned_evidence_level"], "E5")

    # -------------------------------------------------------------------------
    # 6. Safety Firewall v2 (5 Explicit AI States)
    # -------------------------------------------------------------------------
    def test_safety_firewall_v2_five_states(self):
        """Firewall must output strictly one of the 5 explicit AISafetyState enum values."""
        # 1. Schedule E1 poison evaluated for PATIENT role -> BLOCKED
        poison_drug = {
            "drug_id": "ZMF-008",
            "is_schedule_e1": True,
            "classical_state": KnowledgeState.CLINICAL_ACTIVE.value,
            "narrow_therapeutic_index": True
        }
        res_patient = SafetyFirewallV2.evaluate_drug_safety_state(poison_drug, user_role="PATIENT")
        self.assertEqual(res_patient["ai_state"], AISafetyState.BLOCKED.value)

        # 2. Schedule E1 poison evaluated for CLINICIAN role -> CLINICIAN_ONLY
        res_clinician = SafetyFirewallV2.evaluate_drug_safety_state(poison_drug, user_role="CLINICIAN")
        self.assertEqual(res_clinician["ai_state"], AISafetyState.CLINICIAN_ONLY.value)

        # 3. Candidate drug in early research -> RESEARCH_RETRIEVAL
        candidate_drug = {
            "drug_id": "ZMF-999",
            "is_schedule_e1": False,
            "classical_state": KnowledgeState.CANDIDATE.value
        }
        res_candidate = SafetyFirewallV2.evaluate_drug_safety_state(candidate_drug, user_role="RESEARCHER")
        self.assertEqual(res_candidate["ai_state"], AISafetyState.RESEARCH_RETRIEVAL.value)

        # 4. Safe approved drug in CLINICAL_ACTIVE -> CLINICAL_COPILOT_ELIGIBLE
        safe_active_drug = {
            "drug_id": "ZMF-096",
            "is_schedule_e1": False,
            "classical_state": KnowledgeState.CLINICAL_ACTIVE.value
        }
        res_copilot = SafetyFirewallV2.evaluate_drug_safety_state(safe_active_drug, user_role="CLINICIAN")
        self.assertEqual(res_copilot["ai_state"], AISafetyState.CLINICAL_COPILOT_ELIGIBLE.value)

    # -------------------------------------------------------------------------
    # 7. 12-State Knowledge State Machine (Strict Transitions)
    # -------------------------------------------------------------------------
    def test_knowledge_state_machine_strict_linear_progression(self):
        """Illegal skipping of intermediate review gates must be rejected."""
        # Valid sequential: CANDIDATE -> IDENTITY_REVIEW
        valid_step, _ = KnowledgeStateMachine.can_transition(KnowledgeState.CANDIDATE, KnowledgeState.IDENTITY_REVIEW)
        self.assertTrue(valid_step)

        # Illegal skip: CANDIDATE -> BOARD_APPROVED
        invalid_skip, reason = KnowledgeStateMachine.can_transition(KnowledgeState.CANDIDATE, KnowledgeState.BOARD_APPROVED)
        self.assertFalse(invalid_skip)
        self.assertIn("INVALID_TRANSITION", reason)

        # Recovery from CONFLICT -> RECONCILIATION_REQUIRED
        conflict_recovery, _ = KnowledgeStateMachine.can_transition(KnowledgeState.CONFLICT, KnowledgeState.RECONCILIATION_REQUIRED)
        self.assertTrue(conflict_recovery)

    # -------------------------------------------------------------------------
    # 8. Grounded Hakeem Sahab Brief (Unverified Disclosures)
    # -------------------------------------------------------------------------
    def test_grounded_hakeem_sahab_brief_disclosures(self):
        """Brief must contain explicit UNVERIFIED / SAFETY REVIEW disclosures."""
        brief = GroundedHakeemSahabVNext.generate_grounded_brief("ZMF-096")
        self.assertIn("brief_markdown", brief)
        self.assertIn("ZAYVORA Grounded Retrieval", brief["brief_markdown"])
        self.assertIn("EVIDENCE NOT VERIFIED", brief["brief_markdown"])

    # -------------------------------------------------------------------------
    # 9. Organ-Axis Review Workflow
    # -------------------------------------------------------------------------
    def test_organ_axis_review_workflow(self):
        """Proposing an axis link creates PROPOSED status, review transitions to APPROVED."""
        link = OrganAxisReviewEngine.propose_axis_link("ZMF-096", "RESPIRATORY_AXIS", "SYS_ALGO")
        self.assertEqual(link["status"], "PROPOSED")
        reviewed = OrganAxisReviewEngine.review_axis_link("ZMF-096:RESPIRATORY_AXIS", "BOARD_REVIEWER_01", approved=True)
        self.assertEqual(reviewed["status"], "APPROVED")

    # -------------------------------------------------------------------------
    # 10. Murakkab Formulation Governance
    # -------------------------------------------------------------------------
    def test_murakkab_governance_classical_vs_rnd(self):
        """Classical formulation requires source; R&D requires rationale."""
        # Classical missing source -> raises ValueError
        with self.assertRaises(ValueError):
            MurakkabGovernanceEngine.create_murakkab_record(
                "Sharbat-e-Aijaz",
                MurakkabClass.CLASSICAL_FORMULATION,
                [{"drug_id": "ZMF-096", "role": IngredientRole.JUZ_E_AZAM.value}],
                authoritative_source=None
            )

        # Valid Classical
        classical_rec = MurakkabGovernanceEngine.create_murakkab_record(
            "Sharbat-e-Aijaz",
            MurakkabClass.CLASSICAL_FORMULATION,
            [{"drug_id": "ZMF-096", "role": IngredientRole.JUZ_E_AZAM.value}],
            authoritative_source="Bayaz-e-Kabir, Vol. II, p. 88"
        )
        self.assertEqual(classical_rec["class"], "CLASSICAL_FORMULATION")

        # Valid R&D
        rnd_rec = MurakkabGovernanceEngine.create_murakkab_record(
            "ZAYVORA HepatoShield RND-1",
            MurakkabClass.ZAYVORA_RND_FORMULATION,
            [{"drug_id": "ZMF-011", "role": IngredientRole.JUZ_E_AZAM.value}],
            rnd_rationale="Synergistic antioxidant protection tested under IRB-2026-04"
        )
        self.assertEqual(rnd_rec["class"], "ZAYVORA_RND_FORMULATION")

    # -------------------------------------------------------------------------
    # 11. Reviewer Workspace 8 Actions & Audit Logging
    # -------------------------------------------------------------------------
    def test_reviewer_workspace_actions_and_audit(self):
        """Executing reviewer actions must update state and append to immutable audit trail."""
        res = ReviewerWorkspaceEngine.execute_reviewer_action(
            "ZMF-096",
            ReviewerAction.APPROVE,
            "CLINICAL_BOARD_CHAIR",
            "Identity verified against Bayaz-e-Kabir and UPI Part I"
        )
        self.assertTrue(res["success"])
        trail = ReviewerWorkspaceEngine.get_audit_trail_for_drug("ZMF-096")
        self.assertTrue(len(trail) >= 1)
        self.assertEqual(trail[-1]["action"], ReviewerAction.APPROVE.value)

    # -------------------------------------------------------------------------
    # 12. Patient Safety Anti-Leakage Barrier
    # -------------------------------------------------------------------------
    def test_patient_safety_anti_leakage(self):
        """Candidate drugs and unsigned Schedule E1 poisons must never leak to patient care."""
        safe, reason = PatientSafetyBarrier.is_safe_for_patient_regimen(
            "ZMF-999", KnowledgeState.CANDIDATE.value, is_schedule_e1=False, clinician_signed=False
        )
        self.assertFalse(safe)
        self.assertIn("LEAKAGE_PREVENTED", reason)

        # Unsigned E1 poison blocked
        safe_e1, reason_e1 = PatientSafetyBarrier.is_safe_for_patient_regimen(
            "ZMF-008", KnowledgeState.CLINICAL_ACTIVE.value, is_schedule_e1=True, clinician_signed=False
        )
        self.assertFalse(safe_e1)
        self.assertIn("Schedule E(1) poison strictly prohibited", reason_e1)

        # Signed safe active drug allowed
        safe_ok, _ = PatientSafetyBarrier.is_safe_for_patient_regimen(
            "ZMF-096", KnowledgeState.CLINICAL_ACTIVE.value, is_schedule_e1=False, clinician_signed=True
        )
        self.assertTrue(safe_ok)

    # -------------------------------------------------------------------------
    # 13. Live REST API Server Endpoints
    # -------------------------------------------------------------------------
    def test_api_reconcile_identity(self):
        """GET /api/v1/governance/knowledge-vnext/reconcile-identity?q=mulethi"""
        res = _call_get("/api/v1/governance/knowledge-vnext/reconcile-identity?q=mulethi")
        self.assertTrue(res.get("ok"))
        self.assertEqual(res["data"]["canonical_id"], "ZMF-096")

    def test_api_benchmarks(self):
        """GET /api/v1/governance/knowledge-vnext/benchmarks"""
        res = _call_get("/api/v1/governance/knowledge-vnext/benchmarks")
        self.assertTrue(res.get("ok"))
        self.assertEqual(len(res["gold_benchmark_ids"]), 25)

    def test_api_safety_evaluate(self):
        """POST /api/v1/governance/knowledge-vnext/safety-evaluate"""
        payload = {
            "drug": {
                "drug_id": "ZMF-008",
                "is_schedule_e1": True,
                "classical_state": "CLINICAL_ACTIVE"
            },
            "user_role": "PATIENT"
        }
        res = _call_post("/api/v1/governance/knowledge-vnext/safety-evaluate", payload)
        self.assertTrue(res.get("ok"))
        self.assertEqual(res["safety_evaluation"]["ai_state"], "BLOCKED")

    def test_api_transition_state(self):
        """POST /api/v1/governance/knowledge-vnext/transition-state"""
        payload = {
            "current_state": "CANDIDATE",
            "target_state": "IDENTITY_REVIEW"
        }
        res = _call_post("/api/v1/governance/knowledge-vnext/transition-state", payload)
        self.assertTrue(res.get("ok"))
        self.assertTrue(res.get("allowed"))

    def test_api_reviewer_action(self):
        """POST /api/v1/governance/knowledge-vnext/reviewer-action"""
        payload = {
            "drug_id": "ZMF-096",
            "action": "APPROVE",
            "actor_id": "BOARD_MEMBER_04",
            "notes": "Classical Mizaj (Hot 1, Dry 1) verified"
        }
        res = _call_post("/api/v1/governance/knowledge-vnext/reviewer-action", payload)
        self.assertTrue(res.get("ok"))
        self.assertTrue(res["action_result"]["success"])

    def test_api_grounded_brief(self):
        """POST /api/v1/governance/knowledge-vnext/grounded-brief"""
        res = _call_post("/api/v1/governance/knowledge-vnext/grounded-brief", {"drug_id": "ZMF-096"})
        self.assertTrue(res.get("ok"))
        self.assertIn("grounded_brief", res)

    def test_api_patient_safety_barrier(self):
        """POST /api/v1/governance/knowledge-vnext/evaluate-patient-safety"""
        payload = {
            "drug_id": "ZMF-008",
            "current_state": "CLINICAL_ACTIVE",
            "is_schedule_e1": True,
            "clinician_signed": False
        }
        res = _call_post("/api/v1/governance/knowledge-vnext/evaluate-patient-safety", payload)
        self.assertTrue(res.get("ok"))
        self.assertFalse(res.get("safe"))


if __name__ == "__main__":
    unittest.main()
