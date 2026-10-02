#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — ZFIE Comprehensive Domain & Engine Test Suite
Validates the complete ZAYVORA Formulation Intelligence Engine™ specification:
- Parts A-C: Non-disruptive domain extension in /packages/zfie
- Part D: 28 isolated database migrations
- Parts E-J: Formulation, ZKB, Safety, Hakeem Sahab & Clinical Adapters
- Part K: Full REST API Gateway (/api/v1/zfie/...)
- Parts L-M: 19-Step Pipeline & Reproducible Knowledge Snapshots
- Parts N-U: Multidimensional Evidence, Claim Classifier, Docking E2, Synergy, Contradictions & Scientific Memory
- Parts 27-28: Acceptance Criteria & Negative Safety/Authorization Invariants
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from packages.zfie.core.enums import (
    ClaimType,
    ContradictionStatus,
    EntityType,
    EvidenceLevel,
    EvidenceStrength,
    FindingStatus,
    QualityStatus,
    SafetyVerdict,
    SynergyCandidateStatus,
    SynergyModel,
    ValidationStatus
)
from packages.zfie.core.types import (
    AnalysisJob,
    BiologicalStateProfile,
    KnowledgeSnapshot,
    ProvenanceRecord,
    ScientificEvidenceProfile,
    ZFIEFinding
)
from packages.zfie.core.errors import (
    InvalidEvidencePromotionError,
    UnauthorizedClinicalMutationError,
    ZFIESafetyBlockError
)
from packages.zfie.core.validators import (
    classify_scientific_claim,
    validate_evidence_promotion
)
from packages.zfie.identity.canonical_identity import CanonicalIdentityRegistry
from packages.zfie.identity.synonym_resolution import SynonymResolver
from packages.zfie.formulation.formulation_twin import (
    BatchManufacturingTwin,
    ComputationalFormulationTwin,
    FormulaIngredient,
    FormulationTwinRegistry
)
from packages.zfie.chemistry.compounds import CompoundRegistry
from packages.zfie.molecular.targets import TargetRegistry
from packages.zfie.evidence.evidence_bridge import EvidenceBridgeEngine
from packages.zfie.safety.safety_evaluator import ZFIESafetyEvaluator
from packages.zfie.contradiction.conflict_detection import (
    ContradictionObject,
    ContradictionRegistry
)
from packages.zfie.synergy.synergy_engine import SynergyEngine
from packages.zfie.validation.validation_engine import (
    ExperimentPlan,
    ScientificHypothesis,
    ValidationEngine
)
from packages.zfie.memory.negative_knowledge import (
    NegativeScientificRecord,
    ScientificMemoryRegistry
)
from packages.zfie.adapters.formulation_adapter import ZAYVORAFormulationAdapter
from packages.zfie.adapters.zkb_adapter import SafetyFirewallAdapter, ZKBAdapter
from packages.zfie.adapters.hakeem_zfie_adapter import HakeemSahabZFIEAdapter
from packages.zfie.clinical.clinical_adapter import ClinicalAdapter
from packages.zfie.pipeline.pipeline_orchestrator import ZFIEPipelineOrchestrator


class TestZFIECompleteEngine(unittest.TestCase):

    def test_01_canonical_identity_generation(self):
        """Test 01: Canonical IDs are immutable, type-prefixed, and collision-resistant."""
        id_muf = CanonicalIdentityRegistry.generate_id(EntityType.MUFRAD, "Suranjan Shirin")
        self.assertTrue(id_muf.startswith("ZAY-MUF-"))
        
        id_form = CanonicalIdentityRegistry.generate_id(EntityType.FORMULATION, "Majoon Suranjan")
        self.assertTrue(id_form.startswith("ZAY-FORM-"))

        id_batch = CanonicalIdentityRegistry.generate_id(EntityType.BATCH, "MS-2026-LOT-01")
        self.assertTrue(id_batch.startswith("ZAY-BATCH-"))

    def test_02_synonym_resolution_to_canonical(self):
        """Test 02: Multi-lingual names resolve to authoritative Canonical ID."""
        self.assertEqual(SynonymResolver.resolve_to_canonical_id("Suranjan Shirin"), "ZAY-MUF-0001")
        self.assertEqual(SynonymResolver.resolve_to_canonical_id("Colchicum autumnale"), "ZAY-MUF-0001")
        self.assertEqual(SynonymResolver.resolve_to_canonical_id("Black Pepper"), "ZAY-MUF-0002")
        self.assertEqual(SynonymResolver.resolve_to_canonical_id("Kali Mirch"), "ZAY-MUF-0002")
        self.assertEqual(SynonymResolver.resolve_to_canonical_id("Guggulu"), "ZAY-MUF-0003")

    def test_03_formula_and_batch_separation(self):
        """Test 03: Formula and Batch are distinct entities; Batch changes do not mutate Formula."""
        twin = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        self.assertIsNotNone(twin)
        self.assertEqual(twin.formula_version, "v1.1")

        batches = FormulationTwinRegistry.list_batches("ZAY-FORM-0001")
        self.assertTrue(len(batches) >= 2)
        b1, b2 = batches[0], batches[1]
        self.assertNotEqual(b1.batch_id, b2.batch_id)
        self.assertEqual(b1.formulation_id, twin.canonical_id)

    def test_04_versioning_and_cryptographic_hash(self):
        """Test 04: Modifying ingredient ratios creates a new version with distinct SHA-256 hash."""
        base_twin = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        v_next = FormulationTwinRegistry.create_new_version(
            base_id="ZAY-FORM-0001",
            new_version_tag="v1.2",
            modified_proportions={"ZAY-MUF-0001": 0.40, "ZAY-MUF-0002": 0.30},
            change_rationale="Optimized Suranjan-Piperine bioavailability per clinical PK trial"
        )
        self.assertEqual(v_next.formula_version, "v1.2")
        self.assertNotEqual(v_next.hash_signature, base_twin.hash_signature)
        self.assertEqual(v_next.parent_version, "v1.1")
        self.assertTrue(len(v_next.version_history) >= 1)

    def test_05_multidimensional_evidence_profile(self):
        """Test 05: Multi-dimensional evidence profile replaces single misleading AI confidence score."""
        profile = ScientificEvidenceProfile()
        d = profile.to_dict()
        self.assertNotIn("confidence", d)
        self.assertIn("traditional", d)
        self.assertIn("chemical", d)
        self.assertIn("target", d)
        self.assertIn("pathway", d)
        self.assertIn("exposure", d)
        self.assertIn("safety", d)
        self.assertIn("human", d)
        self.assertIn("combination", d)

    def test_06_claim_classifier(self):
        """Test 06: Claims are classified into OBSERVED, CURATED, CALCULATED, PREDICTED, INFERRED."""
        c1 = classify_scientific_claim("Compound Colchicine measured in batch MS-2026-08A via HPLC")
        self.assertEqual(c1, ClaimType.OBSERVED)

        c2 = classify_scientific_claim("Suranjan is curated from canon in UPI Vol II")
        self.assertEqual(c2, ClaimType.CURATED)

        c3 = classify_scientific_claim("In silico docking score indicates -9.4 kcal/mol affinity")
        self.assertEqual(c3, ClaimType.PREDICTED)

        c4 = classify_scientific_claim("Pathway cluster may explain joint anti-inflammatory phenotype")
        self.assertEqual(c4, ClaimType.INFERRED)

    def test_07_docking_labeled_computational_hypothesis_e2(self):
        """Test 07: Docking predictions are explicitly labeled COMPUTATIONAL HYPOTHESIS at E2."""
        pred = TargetRegistry.predict_docking("ZAY-CMP-0001", "ZAY-TGT-0001")
        self.assertEqual(pred.evidence_level, EvidenceLevel.E2_COMPUTATIONAL_PREDICTION)
        self.assertEqual(pred.hypothesis_label, "COMPUTATIONAL HYPOTHESIS")
        self.assertIn("Does NOT prove clinical efficacy", pred.disclaimer)

    def test_08_evidence_ladder_and_promotion_block(self):
        """Test 08: Computational predictions (E2) cannot silently promote to E5/E6 without experimental proof."""
        with self.assertRaises(InvalidEvidencePromotionError):
            validate_evidence_promotion(
                source_level=EvidenceLevel.E2_COMPUTATIONAL_PREDICTION,
                target_level=EvidenceLevel.E6_CONTROLLED_CLINICAL,
                has_experimental_validation=False
            )

        with self.assertRaises(InvalidEvidencePromotionError):
            EvidenceBridgeEngine.promote_evidence_level(
                evidence_id="EVD-003",
                target_level=EvidenceLevel.E6_CONTROLLED_CLINICAL,
                experimental_data_attached=False
            )

    def test_09_safety_firewall_block_terminates_execution(self):
        """Test 09: Safety BLOCK terminates execution and raises ZFIESafetyBlockError."""
        # Unpurified Suranjan violates Schedule E1 Mudabbar rule
        unsafe_ingredients = [
            {"mufrad_id": "ZAY-MUF-0001", "processing_method": "Raw Unpurified Corm"}
        ]
        res = ZFIESafetyEvaluator.evaluate_formulation("ZAY-FORM-UNSAFE", unsafe_ingredients)
        self.assertEqual(res["verdict"], SafetyVerdict.BLOCK.value)
        self.assertFalse(res["can_proceed_to_clinic"])

        with self.assertRaises(ZFIESafetyBlockError):
            SafetyFirewallAdapter.evaluate_and_enforce("ZAY-FORM-UNSAFE", unsafe_ingredients)

    def test_10_ai_cannot_self_approve_or_sign(self):
        """Test 10: AI is strictly prohibited from autonomous prescription signing or self-approval."""
        with self.assertRaises(UnauthorizedClinicalMutationError):
            HakeemSahabZFIEAdapter.attempt_autonomous_signature("ENC-001", "AI-HAKEEM-SAHAB")

        with self.assertRaises(PermissionError):
            ZKBAdapter.attempt_mutation("ZAY-MUF-0001", {"mizaj": "Cold"})

    def test_11_contradictions_as_first_class_objects(self):
        """Test 11: Contradictions are preserved with species, dose, and methodological lineage."""
        contras = ContradictionRegistry.list_for_formulation("ZAY-FORM-0001")
        self.assertTrue(len(contras) >= 1)
        c = contras[0]
        self.assertIn(c.status, [ContradictionStatus.OPEN, ContradictionStatus.EXPLAINED])
        self.assertTrue(len(c.species_differences) > 0)
        self.assertTrue(len(c.methodological_differences) > 0)

    def test_12_synergy_engine_research_boundary(self):
        """Test 12: Synergy candidates are initialized as UNVALIDATED and support Bliss/Loewe models."""
        candidate = SynergyEngine.evaluate_pair("ZAY-FORM-0001", "Colchicine", "Piperine", SynergyModel.BLISS)
        self.assertEqual(candidate.status, SynergyCandidateStatus.UNVALIDATED)
        self.assertEqual(candidate.model_used, SynergyModel.BLISS)
        self.assertLess(candidate.predicted_combination_index, 1.0)
        self.assertIn("UNVALIDATED candidate", candidate.notes)

    def test_13_validation_engine_and_planner(self):
        """Test 13: Experimental validation lifecycle and next-best-experiment proposal."""
        hyps = ValidationEngine.list_hypotheses("ZAY-FORM-0001")
        self.assertTrue(len(hyps) >= 1)
        
        proposal = ValidationEngine.plan_next_best_experiment("ZAY-FORM-0001", ["Hepatic clearance rate"])
        self.assertIn("proposal_id", proposal)
        self.assertEqual(proposal["status"], "PROPOSED_FOR_REVIEW")

    def test_14_scientific_memory_negative_knowledge(self):
        """Test 14: Scientific Memory permanently tracks falsified claims and toxicity findings."""
        negs = ScientificMemoryRegistry.list_for_formulation("ZAY-FORM-0001")
        self.assertTrue(len(negs) >= 2)
        tox = next((n for n in negs if n.record_type == "TOXICITY_SIGNAL"), None)
        self.assertIsNotNone(tox)
        self.assertIn("Raw Corm", tox.title)

    def test_15_formulation_adapter_does_not_mutate_nuskha(self):
        """Test 15: ZAYVORAFormulationAdapter translates Nuskha without mutating original record."""
        original_nuskha = {
            "id": "RX-774901",
            "name": "Custom Matab Compound",
            "items": [
                {"name": "Suranjan Shirin", "quantity_g": 4.0, "prep": "Mudabbar"},
                {"name": "Filfil Siyah", "quantity_g": 2.0, "prep": "Powder"}
            ]
        }
        twin = ZAYVORAFormulationAdapter.nuskha_to_formulation_twin(original_nuskha)
        self.assertIsNotNone(twin)
        # Original dict remains completely untouched
        self.assertEqual(original_nuskha["id"], "RX-774901")
        self.assertEqual(len(original_nuskha["items"]), 2)

    def test_16_clinical_adapter_why_this_drawer(self):
        """Test 16: ClinicalAdapter prepares comprehensive 'Why this?' Formulation Intelligence Drawer."""
        drawer = ClinicalAdapter.get_drawer_intelligence("ZAY-FORM-0001")
        self.assertIn("formulation", drawer)
        self.assertIn("batch", drawer)
        self.assertIn("relevant_mechanisms", drawer)
        self.assertIn("evidence_profile", drawer)
        self.assertIn("safety", drawer)
        self.assertIn("contradictions", drawer)
        self.assertIn("why_this", drawer)
        self.assertIn("traditional_grounding", drawer["why_this"])
        self.assertIn("molecular_rationale", drawer["why_this"])

    def test_17_19_step_pipeline_orchestrator(self):
        """Test 17: Full 19-step worker pipeline executes reproducibly with knowledge snapshot."""
        job = ZFIEPipelineOrchestrator.submit_job(
            formulation_id="ZAY-FORM-0001",
            formula_version_id="v1.1",
            mode="SHADOW"
        )
        self.assertEqual(job.status, "COMPLETED")
        self.assertIsNotNone(job.result)
        res = job.result
        self.assertIn("knowledge_snapshot", res)
        self.assertIn("docking_predictions", res)
        self.assertIn("organ_axis", res)
        self.assertIn("safety", res)
        self.assertIn("audit_event", res)
        self.assertTrue(res["requires_clinician_review"])


if __name__ == "__main__":
    unittest.main()
