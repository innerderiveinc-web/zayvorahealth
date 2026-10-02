#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — ZFIE Horizontal Layers Comprehensive Test Suite
Validates the 5 foundational horizontal layers:
1. Scientific Data Factory (ETL & Ingestion)
2. Scientific Benchmarking, Uncertainty & MLOps
3. Unani <-> Biomedical Semantic Bridge
4. Manufacturing QC Spectral Intelligence & RWE Closed-Loop
5. Formulation Compiler, Scientific Review Board & Experiment Recommender
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from packages.zfie.factory.ingestion import (
    ScientificDataFactory, IngestionSourceType, LicenseMetadata, ReviewStatus
)
from packages.zfie.benchmark.benchmarks import (
    ScientificBenchmarkingSuite, UncertaintyCalibrationEngine, ModelLifecycleStage
)
from packages.zfie.bridge.semantic_bridge import (
    UnaniBiomedicalBridgeRegistry, SemanticEvidenceStatus
)
from packages.zfie.manufacturing.batch_qc_intelligence import (
    BatchQCIntelligenceEngine, BatchReleaseStatus
)
from packages.zfie.outcomes.rwe_closed_loop import (
    RWEClosedLoopEngine
)
from packages.zfie.compiler.formulation_compiler import (
    FormulationCompiler
)
from packages.zfie.governance.scientific_review_board import (
    ScientificReviewBoard, ProposalDomain, GovernanceStage
)
from packages.zfie.governance.knowledge_decay import (
    KnowledgeFreshnessEngine, KnowledgeFreshnessState
)
from packages.zfie.validation.experiment_recommender import (
    ExperimentRecommendationEngine
)
from tests.test_live_api_integration import DirectTestClient


class TestZFIEHorizontalLayers(unittest.TestCase):

    def setUp(self):
        self.client = DirectTestClient()

    # ── Layer 1: Scientific Data Factory ─────────────────────────────────────
    def test_layer1_ingestion_and_review_board(self):
        """Test scientific ingestion, normalization, and review board staging."""
        payload = {
            "name": "Colchicine",
            "smiles": "CC(=O)NC1CCC2=CC(=O)C(=C(C2=C3C1=CC(=C(C3=O)OC)OC)OC)OC",
            "pubchem_cid": 6167,
            "chembl_id": "CHEMBL84",
            "uniprot_id": "P07437"
        }
        lic = LicenseMetadata(
            source_name="PubChem",
            license_type="Public Domain",
            commercial_use_allowed=True,
            attribution_required=True,
            redistribution_allowed=True,
            source_uri="https://pubchem.ncbi.nlm.nih.gov"
        )
        record = ScientificDataFactory.ingest_payload(
            source_type=IngestionSourceType.PUBLIC_REPOSITORY,
            source_name="PubChem",
            source_version="2026.09",
            payload=payload,
            license_meta=lic
        )
        self.assertIsNotNone(record.staging_id)
        self.assertEqual(record.review_status, ReviewStatus.STAGED)
        self.assertEqual(record.normalized_entity["identifiers"]["chembl_id"], "CHEMBL84")

        # Review board approval
        approved = ScientificDataFactory.review_record(
            staging_id=record.staging_id,
            approved=True,
            reviewer_id="DR-PHARMA-01",
            notes="Compound identity verified against crystallographic standard."
        )
        self.assertEqual(approved.review_status, ReviewStatus.APPROVED)

    # ── Layer 2: Scientific Benchmarking & Uncertainty ──────────────────────
    def test_layer2_benchmarking_and_uncertainty_calibration(self):
        """Test standard benchmarks and epistemic uncertainty calibration."""
        report = ScientificBenchmarkingSuite.evaluate_model("ZFIE-DOCK-MECH", "v1.0")
        self.assertTrue(report.overall_pass)
        self.assertEqual(len(report.metrics), 6)
        self.assertLessEqual(report.brier_score, 0.20)

        # Epistemic interval check
        ci = UncertaintyCalibrationEngine.calculate_epistemic_interval(0.88, sample_variance=0.04, sample_size=16)
        self.assertEqual(ci["prediction"], 0.88)
        self.assertLess(ci["ci_lower_95"], 0.88)
        self.assertGreater(ci["ci_upper_95"], 0.88)

    # ── Layer 3: Unani <-> Biomedical Semantic Bridge ───────────────────────
    def test_layer3_semantic_bridge_and_epistemic_guard(self):
        """Test controlled 6-step semantic bridge and non-reductionist caution."""
        mapping = UnaniBiomedicalBridgeRegistry.map_classical_concept("Waja-ul-Mafasil")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping["concept_id"], "SEM-BRG-001")
        self.assertIn("Synovial MSU Crystals", str(mapping["biomarker_associations"]))
        # Non-reductionist caution check
        self.assertIn("does NOT alone prove", mapping["epistemic_caution"])

    # ── Layer 4: Manufacturing QC & RWE Closed-Loop ─────────────────────────
    def test_layer4_batch_qc_spectral_similarity(self):
        """Test HPLC peak cosine similarity and outlier detection."""
        # Golden reference aligned batch
        dossier = BatchQCIntelligenceEngine.register_and_evaluate_batch(
            batch_id="BATCH-TEST-PASS",
            batch_number="MS-2026-T1",
            formulation_id="ZAY-FORM-0001",
            formulation_version="v1.1",
            raw_material_lots=["LOT-SUR-2026-01"],
            supplier_name="Kashmir Certified Botanicals",
            solvent="Hydro-ethanolic (70:30)",
            temp_c=65.0,
            duration_h=4.0,
            mfg_date="2026-09-01",
            exp_date="2028-09-01",
            measured_peaks=[
                {"compound": "Colchicine", "rt": 4.12, "abundance": 28.5},
                {"compound": "Piperine", "rt": 7.45, "abundance": 34.2},
                {"compound": "Guggulsterone_E", "rt": 11.20, "abundance": 18.0}
            ]
        )
        self.assertEqual(dossier.status, BatchReleaseStatus.QC_PASSED)
        self.assertFalse(dossier.outlier_flag)
        self.assertGreaterEqual(dossier.similarity_to_golden_standard, 0.99)

        # Severely contaminated / outlier batch
        outlier_dossier = BatchQCIntelligenceEngine.register_and_evaluate_batch(
            batch_id="BATCH-TEST-FAIL",
            batch_number="MS-2026-T2",
            formulation_id="ZAY-FORM-0001",
            formulation_version="v1.1",
            raw_material_lots=["LOT-UNKNOWN"],
            supplier_name="Uncertified",
            solvent="Water",
            temp_c=25.0,
            duration_h=1.0,
            mfg_date="2026-09-01",
            exp_date="2028-09-01",
            measured_peaks=[
                {"compound": "Colchicine", "rt": 4.12, "abundance": 2.0},  # Severely deficient
                {"compound": "Piperine", "rt": 7.45, "abundance": 1.0},
                {"compound": "Guggulsterone_E", "rt": 11.20, "abundance": 0.5}
            ]
        )
        self.assertEqual(outlier_dossier.status, BatchReleaseStatus.QC_REJECTED)
        self.assertTrue(outlier_dossier.outlier_flag)

    def test_layer4_rwe_closed_loop_tracking(self):
        """Test longitudinal real-world evidence and batch cohort aggregation."""
        obs = RWEClosedLoopEngine.record_outcome(
            patient_mrn="MRN-TEST-100",
            formulation_id="ZAY-FORM-0001",
            formulation_version="v1.1",
            batch_id="ZAY-BATCH-2026-001",
            baseline_diagnosis="Acute Gouty Arthritis",
            phenotype="Balghami Synovial Hyperemia",
            duration_days=30,
            adherence_pct=92.0,
            biomarker_points=[
                {"day_offset": 0, "biomarker_name": "Serum Uric Acid", "value": 8.9, "unit": "mg/dL"},
                {"day_offset": 30, "biomarker_name": "Serum Uric Acid", "value": 6.1, "unit": "mg/dL"}
            ],
            outcome_delta="Significant reduction in inflammatory flares and pain index.",
            adverse_events=[]
        )
        self.assertIsNotNone(obs.record_id)
        cohort = RWEClosedLoopEngine.analyze_batch_cohort("ZAY-BATCH-2026-001")
        self.assertGreaterEqual(cohort["cohort_size"], 1)
        self.assertEqual(cohort["total_adverse_events"], 0)

    # ── Layer 5: Compiler, Governance, Freshness & Recommendations ───────────
    def test_layer5_formulation_compiler_research_candidate_only(self):
        """Test formulation compiler creates candidate with strict non-autonomous caveat."""
        arch = FormulationCompiler.compile_candidate_formulation(
            clinical_objective="Chronic Gouty Arthritis & Joint Stiffness",
            biological_state="Crystal Synovitis & Impaired Humoral Clearance"
        )
        self.assertTrue(arch.candidate_id.startswith("ZAY-CAND-"))
        self.assertEqual(len(arch.ingredients), 3)
        self.assertIn("RESEARCH CANDIDATE ONLY", arch.statutory_warning)

    def test_layer5_governance_multi_stage_workflow(self):
        """Test scientific review board multi-stage advancement."""
        prop = ScientificReviewBoard.submit_proposal(
            domain=ProposalDomain.MOLECULAR_MECHANISM,
            title="Piperine Mediated CYP3A4 Downregulation in Conjunction with Colchicine",
            proposed_by="AGENT-RESEARCH",
            summary="Mechanistic pathway synergy.",
            evidence_ids=["ZAY-EVD-91"]
        )
        self.assertEqual(prop.current_stage, GovernanceStage.PROPOSAL)

        # Advance to SCIENTIFIC_REVIEW
        ScientificReviewBoard.advance_stage(
            prop.proposal_id, reviewer_id="DR-01", reviewer_role="CHIEF_PHARMACOLOGIST", approved=True
        )
        self.assertEqual(prop.current_stage, GovernanceStage.SCIENTIFIC_REVIEW)

    def test_layer5_knowledge_decay_freshness_invalidation(self):
        """Test knowledge freshness engine invalidates dependent analysis runs."""
        edge = KnowledgeFreshnessEngine.register_analysis_dependency(
            analysis_id="AN-TEST-001",
            subject_id="ZAY-FORM-0001",
            evidence_ids=["EVD-REF-101", "EVD-REF-102"]
        )
        self.assertEqual(edge.freshness_state, KnowledgeFreshnessState.CURRENT)

        # Trigger evidence update notification
        affected = KnowledgeFreshnessEngine.notify_evidence_updated(
            evidence_id="EVD-REF-101",
            reason="Phase III clinical trial failed to replicate in-vitro synergy"
        )
        self.assertIn("AN-TEST-001", affected)
        check = KnowledgeFreshnessEngine.check_freshness("AN-TEST-001")
        self.assertEqual(check["freshness_state"], KnowledgeFreshnessState.STALE.value)
        self.assertIn("Phase III", check["invalidation_reason"])

    def test_layer5_next_best_experiment_recommender(self):
        """Test ranking and scoring of next best empirical experiments."""
        recs = ExperimentRecommendationEngine.get_top_recommendations_for_formulation("ZAY-FORM-0001")
        self.assertEqual(len(recs), 3)
        self.assertTrue(recs[0]["composite_priority_score"] >= recs[1]["composite_priority_score"])
        self.assertIn("Beta-tubulin", recs[0]["target_protein_or_cell_line"])

    # ── REST API Integration Tests ──────────────────────────────────────────
    def test_rest_api_horizontal_layers(self):
        """Verify all new horizontal endpoints respond with 200/201 over REST."""
        # 1. Benchmark summary
        st, body = self.client.request("GET", "/api/v1/zfie/benchmark/summary")
        self.assertEqual(st, 200)
        self.assertTrue(body["benchmark_summary"]["overall_pass"])

        # 2. Bridge mappings
        st, body = self.client.request("GET", "/api/v1/zfie/bridge/mappings")
        self.assertEqual(st, 200)
        self.assertGreaterEqual(len(body["mappings"]), 2)

        # 3. Governance proposals
        st, body = self.client.request("GET", "/api/v1/zfie/governance/proposals")
        self.assertEqual(st, 200)
        self.assertGreaterEqual(len(body["proposals"]), 1)

        # 4. Next-best experiment
        st, body = self.client.request("GET", "/api/v1/zfie/experiments/next-best")
        self.assertEqual(st, 200)
        self.assertEqual(len(body["recommendations"]), 3)

        # 5. Compiler compile endpoint
        st, body = self.client.request(
            "POST",
            "/api/v1/zfie/compiler/compile",
            {"clinical_objective": "Acute Gout Joint Flare", "biological_state": "Synovial Hyperemia"}
        )
        self.assertEqual(st, 200)
        self.assertIn("RESEARCH CANDIDATE ONLY", body["candidate_architecture"]["statutory_warning"])

        # 6. Governance Submit & 21 CFR Part 11 Sign-off
        st, body = self.client.request(
            "POST",
            "/api/v1/zfie/governance/proposals",
            {
                "domain": "FORMULATION_DESIGN",
                "title": "Neuro-Cognitive Cephalalgia Formulation v1.2",
                "proposed_by": "DR-AZIZ-RESEARCH",
                "summary": "Standardization of Itrifal Kishneezi with linalool fraction.",
                "supporting_evidence_ids": ["ZAY-EVD-0110"]
            }
        )
        self.assertEqual(st, 201)
        prop_id = body["proposal"]["proposal_id"]

        st_sign, body_sign = self.client.request(
            "POST",
            "/api/v1/zfie/governance/sign-off",
            {
                "proposal_id": prop_id,
                "reviewer_id": "DR-FAROOQI",
                "reviewer_role": "CHIEF_PHARMACOLOGIST",
                "approved": True,
                "comments": "Reviewed botanical evidence and safety bounds. Approved for stage advance."
            }
        )
        self.assertEqual(st_sign, 200)
        self.assertTrue(body_sign["qms_cfr_part_11_verified"])
        self.assertIsNotNone(body_sign["audit_leaf_hash"])
        self.assertEqual(body_sign["proposal"]["current_stage"], "SCIENTIFIC_REVIEW")



if __name__ == "__main__":
    unittest.main()
