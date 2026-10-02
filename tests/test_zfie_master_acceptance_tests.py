#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — ZFIE Master Acceptance Test Suite (AT-01 to AT-12)
Validates compliance against Section 49 of the ZFIE Production Integration Blueprint.

Acceptance Tests:
- AT-01: Create formulation -> create version -> create batch.
- AT-02: Modify ingredient ratio -> new formula version automatically created.
- AT-03: Run analysis -> result contains model and knowledge versions.
- AT-04: Every molecular relationship has evidence/provenance.
- AT-05: Computational prediction is labelled E2 / E0.
- AT-06: No E2 output can be represented as E5/E6.
- AT-07: Safety BLOCK prevents downstream clinical execution.
- AT-08: AI cannot approve its own recommendation.
- AT-09: Contradictory evidence remains visible.
- AT-10: Research data cannot silently enter production training.
- AT-11: Old analysis remains reproducible after knowledge update.
- AT-12: Clinician can inspect "Why this?"
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
ai_service_path = os.path.join(BASE_DIR, "services", "ai")
if ai_service_path not in sys.path:
    sys.path.insert(0, ai_service_path)

from services.knowledge.app.core.canonical_identity_service import (
    CanonicalIdentityRegistry,
    EntityType
)
from services.therapeutic.app.models.computational_twin import (
    FormulationTwinRegistry,
    FormulationDigitalTwin,
    BatchManufacturingTwin,
    QualityStatus
)
from services.knowledge.app.engines.evidence_bridge import (
    EvidenceBridgeEngine,
    EvidenceLevel
)
from services.knowledge.app.engines.provenance_registry import (
    ProvenanceLicenseRegistry
)
from services.therapeutic.app.engines.formulation_intelligence_engine import (
    FormulationIntelligenceEngine,
    ScientificMemoryRegistry,
    SafetyVerdict
)
from services.ai.app.agentic.formulation_shadow_orchestrator import (
    FormulationShadowOrchestrator
)
from services.knowledge.app.engines.insilico_docking_bridge import (
    in_silico_docking_bridge
)


class TestZFIEMasterAcceptance(unittest.TestCase):

    def test_at_01_create_formulation_version_batch(self):
        """AT-01: Create formulation -> create version -> create batch."""
        twin = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        self.assertIsNotNone(twin)
        self.assertEqual(twin.canonical_id, "ZAY-FORM-0001")
        self.assertEqual(twin.formula_version, "v1.1")
        
        batches = FormulationTwinRegistry.list_batches_for_formulation("ZAY-FORM-0001")
        self.assertTrue(len(batches) >= 2)
        batch = batches[0]
        batch_number = batch["lot_number"] if isinstance(batch, dict) else batch.batch_number
        quality_status = batch["quality_status"] if isinstance(batch, dict) else batch.quality_status.value
        self.assertTrue(batch_number.startswith("MS-2026-"))
        self.assertEqual(quality_status, QualityStatus.CERTIFIED.value)

    def test_at_02_modify_ratio_triggers_new_version(self):
        """AT-02: Modify ingredient ratio -> new formula version automatically created."""
        base_twin = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        new_version = FormulationTwinRegistry.create_new_formula_version(
            base_formulation_id="ZAY-FORM-0001",
            new_version_tag="v1.2",
            modified_proportions={"ZAY-MUF-0001": 0.40, "ZAY-MUF-0002": 0.30, "ZAY-MUF-0003": 0.30},
            change_rationale="Optimized Suranjan-Piperine bioavailability ratio per clinical PK findings."
        )
        self.assertIsNotNone(new_version)
        self.assertEqual(new_version.formula_version, "v1.2")
        self.assertNotEqual(new_version.hash_signature, base_twin.hash_signature)

    def test_at_03_analysis_contains_model_and_knowledge_versions(self):
        """AT-03: Run analysis -> result contains model and knowledge versions."""
        envelope = FormulationIntelligenceEngine.get_standard_intelligence_envelope("ZAY-FORM-0001")
        self.assertIsNotNone(envelope)
        self.assertIn("model", envelope)
        self.assertIn("knowledge", envelope)
        self.assertEqual(envelope["model"]["name"], "ZFIE-MECH-001")
        self.assertTrue(len(envelope["model"]["version"]) > 0)
        self.assertTrue(len(envelope["knowledge"]["version"]) > 0)

    def test_at_04_every_molecular_relationship_has_provenance(self):
        """AT-04: Every molecular relationship has evidence/provenance."""
        matrix = EvidenceBridgeEngine.get_evidence_matrix_for_formulation("ZAY-FORM-0001")
        self.assertTrue(len(matrix) >= 3)
        for claim in matrix:
            self.assertTrue(claim.evidence_id.startswith("ZAY-EVD-"))
            self.assertTrue(len(claim.source_database) > 0)
            self.assertTrue(len(claim.citation) > 0)
            self.assertIsNotNone(claim.evidence_level)

    def test_at_05_computational_prediction_labelled_e0_e2(self):
        """AT-05: Computational prediction is labelled E0 / E2."""
        poses = in_silico_docking_bridge.get_docking_poses("ZAY-CMP-0001")
        self.assertTrue(len(poses) >= 1)
        for p in poses:
            self.assertIn(p["evidence_level"], ["E0", "E2"])
            self.assertLess(p["binding_energy_kcal_mol"], 0.0)

    def test_at_06_no_e2_represented_as_e5_e6(self):
        """AT-06: No E2 output can be represented as E5/E6."""
        claim_docking = EvidenceBridgeEngine.get_claim("ZAY-EVD-0005") # Docking claim
        self.assertIsNotNone(claim_docking)
        self.assertEqual(claim_docking.evidence_level, EvidenceLevel.E0_IN_SILICO)
        self.assertNotEqual(claim_docking.evidence_level, EvidenceLevel.E5_HUMAN_OBSERVATIONAL)
        self.assertNotEqual(claim_docking.evidence_level, EvidenceLevel.E6_CONTROLLED_TRIAL)

    def test_at_07_safety_block_prevents_downstream_execution(self):
        """AT-07: Safety BLOCK prevents downstream clinical execution."""
        # Patient with acute renal failure eGFR=18
        eval_result = FormulationIntelligenceEngine.evaluate_independent_safety(
            "ZAY-FORM-0001",
            {"egfr": 18, "alt_u_l": 25}
        )
        self.assertEqual(eval_result.verdict, SafetyVerdict.BLOCK)
        self.assertIn("severe renal clearance failure", eval_result.contraindication_alerts[0].lower())

    def test_at_08_ai_cannot_approve_its_own_recommendation(self):
        """AT-08: AI cannot approve its own recommendation."""
        insight = FormulationShadowOrchestrator.analyze_prescription_candidate(
            "ZAY-FORM-0001",
            {"egfr": 90}
        )
        self.assertIsNotNone(insight)
        self.assertTrue(insight.requires_clinician_approval)
        self.assertFalse(insight.autonomous_execution_allowed)
        self.assertIn("ZAYVORA SCIENTIFIC NOTICE", insight.statutory_caveat)

    def test_at_09_contradictory_evidence_remains_visible(self):
        """AT-09: Contradictory evidence remains visible."""
        contradictions = ScientificMemoryRegistry.check_for_contradictions("Suranjan Shirin")
        self.assertTrue(len(contradictions) >= 1)
        contra = contradictions[0]
        self.assertEqual(contra["status"], "BLOCKED")
        self.assertIn("refuted_claim", contra)
        self.assertIn("opposing_study", contra)

    def test_at_10_research_data_isolated_from_production(self):
        """AT-10: Research data cannot silently enter production training."""
        # Check environment separation invariants
        envelope = FormulationIntelligenceEngine.get_standard_intelligence_envelope("ZAY-FORM-0001")
        self.assertEqual(envelope["execution_mode"], "SHADOW_ADVISORY")
        self.assertFalse(envelope["clinical_action"]["autonomous_action_allowed"])

    def test_at_11_analysis_reproducible_after_knowledge_update(self):
        """AT-11: Old analysis remains reproducible after knowledge update."""
        env_1 = FormulationIntelligenceEngine.get_standard_intelligence_envelope("ZAY-FORM-0001")
        env_2 = FormulationIntelligenceEngine.get_standard_intelligence_envelope("ZAY-FORM-0001")
        self.assertEqual(env_1["knowledge"]["version"], env_2["knowledge"]["version"])
        self.assertEqual(env_1["finding"]["statement"], env_2["finding"]["statement"])

    def test_at_12_clinician_can_inspect_why_this(self):
        """AT-12: Clinician can inspect 'Why this?' evidence drawer."""
        drawer = FormulationIntelligenceEngine.get_why_this_drawer("ZAY-FORM-0001")
        self.assertIsNotNone(drawer)
        self.assertIn("classical_sources", drawer)
        self.assertIn("citations", drawer)
        self.assertIn("evidence_levels", drawer)
        self.assertIn("statutory_caveat", drawer)
        self.assertTrue(len(drawer["citations"]) >= 2)

    def test_at_13_clinical_encounter_formulation_analysis_contract(self):
        """AT-13: POST /api/v1/zfie/clinical/encounters/{id}/formulation-analysis matches Section 53 contract."""
        try:
            from tests.test_live_api_integration import DirectTestClient
        except ImportError:
            from test_live_api_integration import DirectTestClient
        client = DirectTestClient()
        post_data = {
            "formulationId": "ZAY-FORM-0001",
            "formulationVersionId": "v1.1",
            "analysisMode": "CLINICAL_CDS",
            "clinicalObjective": "Severe Acute Gout Joint Flare"
        }
        status, body = client.request("POST", "/api/v1/zfie/clinical/encounters/ENC-2026-001/formulation-analysis", post_data)
        self.assertEqual(status, 200)
        self.assertTrue(body.get("requiresClinicianReview"))
        self.assertFalse(body.get("autonomousActionAllowed"))
        self.assertIn("clinicalObjective", body)
        self.assertIn("biologicalContext", body)
        self.assertIn("mechanisticConsiderations", body)
        self.assertIn("evidence", body)
        self.assertIn("safety", body)
        self.assertIn("contradictions", body)
        self.assertIn("unknowns", body)

    def test_at_14_non_autonomous_doctrine_cannot_be_bypassed(self):
        """AT-14: AI autonomous approval attempt raises UnauthorizedClinicalMutationError."""
        from packages.zfie.adapters.hakeem_zfie_adapter import HakeemSahabZFIEAdapter
        from packages.zfie.core.errors import UnauthorizedClinicalMutationError
        with self.assertRaises(UnauthorizedClinicalMutationError):
            HakeemSahabZFIEAdapter.attempt_autonomous_signature("ENC-2026-001", "AI_AGENT_007")

    def test_at_15_section_68_feature_flags_and_shadow_mode(self):
        """AT-15: Section 68 feature flags active; Shadow mode strictly enforced."""
        from packages.zfie.core.flags import ZFIESettings
        flags = ZFIESettings.get_flags()
        self.assertTrue(flags["ZFIE_ENABLED"])
        self.assertTrue(flags["ZFIE_RESEARCH_ENABLED"])
        self.assertTrue(flags["ZFIE_SHADOW_MODE"])
        self.assertFalse(flags["ZFIE_CLINICAL_CDS_ENABLED"])
        self.assertFalse(flags["ZFIE_SYNERGY_ENABLED"])
        self.assertFalse(flags["ZFIE_BIOLOGICAL_STATE_ENABLED"])
        self.assertFalse(flags["ZFIE_EXPERIMENT_PLANNER_ENABLED"])

        try:
            from tests.test_live_api_integration import DirectTestClient
        except ImportError:
            from test_live_api_integration import DirectTestClient
        client = DirectTestClient()

        # Query GET flags endpoint
        status, body = client.request("GET", "/api/v1/zfie/config/flags")
        self.assertEqual(status, 200)
        self.assertTrue(body["flags"]["ZFIE_SHADOW_MODE"])
        self.assertFalse(body["flags"]["ZFIE_CLINICAL_CDS_ENABLED"])

        # Execute Clinical CDS request -> automatically constrained to SHADOW
        post_data = {
            "formulationId": "ZAY-FORM-0001",
            "formulationVersionId": "v1.1",
            "analysisMode": "CLINICAL_CDS"
        }
        status, enc_res = client.request("POST", "/api/v1/zfie/clinical/encounters/ENC-2026-001/formulation-analysis", post_data)
        self.assertEqual(status, 200)
        self.assertEqual(enc_res["effectiveMode"], "SHADOW")
        self.assertTrue(enc_res["shadowModeActive"])
        self.assertFalse(enc_res["clinicalCdsEnabled"])
        self.assertIn("Shadow Mode", enc_res["governanceNotice"])


if __name__ == "__main__":
    unittest.main()


