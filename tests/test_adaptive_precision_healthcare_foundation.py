"""
ZAYVORA Health OS™ — Test Suite #66
===================================
Adaptive Precision Healthcare OS & Phenotype Intelligence Foundation
- WHO SMART Guidelines Level 4 Executable Knowledge Rules
- Precision Patient Longitudinal Model (Phase 18 Foundation)
- Sub-Phenotypic Stratification Engine (Phase 19 Foundation)
- 5-Tier Response Intelligence Classification (Phase 20 Foundation)
- Adherent Non-Responder Failure Detection & Protocol Escalation
- Orchestrator Continuum Stages 13 & 14 Integration
- Live REST Endpoints for Adaptive Precision & Knowledge Compiler
"""

import datetime
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.clinical.app.engines.precision_patient_model import (
    PrecisionPatientModel,
    SymptomObservation,
    FunctionalBiomarkerDelta,
    MizajDynamicRecord,
    OrganAxisRecord,
    PrescribedNuskhaRecord,
    PosologyAdherenceRecord,
    LifestyleDynamicsRecord,
)
from services.clinical.app.engines.phenotype_and_response_engine import (
    PhenotypeAndResponseEngine,
    ResponseClassificationTier,
    ClinicalPhenotypeProfile,
    ResponseEvaluation,
)
from services.knowledge.app.core.knowledge_compiler import (
    KnowledgeCompiler,
    KnowledgeCompilerError,
    ReviewerSignoff,
    ExecutableKnowledgeRule,
)
from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
    ClinicalIntelligenceCoreOrchestrator,
    ClinicalContinuumRequest,
)


class TestAdaptivePrecisionHealthcareFoundation(unittest.TestCase):
    """Suite #66: Adaptive Precision Healthcare Foundation Verification"""

    def test_precision_patient_model_creation_and_trajectory(self):
        """Validates that PrecisionPatientModel synthesizes the 5 core longitudinal questions."""
        ppm = PrecisionPatientModel(
            patient_id="P-PRECISION-001",
            age=52,
            gender="MALE",
            baseline_vitals={"pulse": 78, "bp": "130/85"},
            primary_condition="Waja-ul-Mafasil"
        )
        ppm.add_symptom("Bilateral Knee Pain & Morning Stiffness", 8.5, 90, "2026-01-01")
        ppm.add_biomarker_delta("ESR", 48.0, 22.0, "mm/hr", is_lower_better=True)
        ppm.add_biomarker_delta("hs-CRP", 6.8, 1.9, "mg/L", is_lower_better=True)
        ppm.add_mizaj_record("Balghami Ghaleez", 0.3, 0.85, 0.75, 0.25, 0.65)
        ppm.add_organ_axis_score("Musculoskeletal & Articular (Mafasil)", 0.82, is_compromised=True)
        ppm.add_nuskha_record("NSK-SURANJAN-01", ["Majun Suranjan", "Habb-e-Asgandh"], "2026-01-10", "DOC-HAKEEM-01")
        ppm.add_posology_adherence(30, 60, 56)  # 93.3% adherence
        ppm.add_lifestyle_record("Winter", "Barid Ratab Diet", "Gentle Takmeed", 0.80)
        ppm.add_outcome_record("KAMIL", 78.5, "Shifa-e-Kamil (Complete Clinical Resolution)")

        summary = ppm.synthesize_longitudinal_summary()

        self.assertEqual(summary["patient_id"], "P-PRECISION-001")
        self.assertEqual(summary["primary_condition"], "Waja-ul-Mafasil")
        # Verify the 5 core clinical questions are answered
        answers = summary["longitudinal_trajectory_answers"]
        self.assertIn("Majun Suranjan", answers["what_was_tried"]["prescribed_drugs"])
        self.assertGreater(answers["what_was_tried"]["adherence_rate_pct"], 90.0)
        self.assertEqual(len(answers["what_changed"]["improved_biomarkers"]), 2)
        self.assertTrue(answers["what_changed"]["symptom_relief_achieved"])
        self.assertEqual(len(answers["what_caused_adverse_effects"]), 0)
        self.assertEqual(answers["what_worked_for_phenotype"]["effective_for_mizaj"], "Balghami Ghaleez")

    def test_biomarker_delta_computation(self):
        """Verifies calculation of percentage change and direction-aware improvement."""
        esr_delta = FunctionalBiomarkerDelta("ESR", 50.0, 25.0, "mm/hr", is_lower_better=True)
        self.assertEqual(esr_delta.percentage_change, -50.0)
        self.assertTrue(esr_delta.is_improved)

        hdl_delta = FunctionalBiomarkerDelta("HDL", 35.0, 48.0, "mg/dL", is_lower_better=False)
        self.assertGreater(hdl_delta.percentage_change, 30.0)
        self.assertTrue(hdl_delta.is_improved)

    def test_phenotype_stratification_joint_pain(self):
        """Tests sub-phenotyping of Waja-ul-Mafasil across 4 canonical humors."""
        engine = PhenotypeAndResponseEngine()

        # Balghami Sub-phenotype
        balgham = engine.classify_phenotype("Waja-ul-Mafasil", "Balghami (Cold & Wet)")
        self.assertEqual(balgham.phenotype_code, "PHENO-ARTH-BALGHAM")
        self.assertIn("Balghami Ghaleez", balgham.phenotype_name)
        self.assertIn("Munzij & Mushil", balgham.suggested_line_of_treatment)

        # Safrawi Sub-phenotype
        safra = engine.classify_phenotype("Waja-ul-Mafasil", "Safrawi (Hot & Dry)")
        self.assertEqual(safra.phenotype_code, "PHENO-ARTH-SAFRA")
        self.assertIn("Bilious-Inflammatory", safra.phenotype_name)
        self.assertIn("Tabreed", safra.suggested_line_of_treatment)

        # Sawdawi Sub-phenotype
        sawda = engine.classify_phenotype("Waja-ul-Mafasil", "Sawdawi (Cold & Dry)")
        self.assertEqual(sawda.phenotype_code, "PHENO-ARTH-SAWDA")
        self.assertIn("Melancholic-Desiccated", sawda.phenotype_name)

        # Damawi Sub-phenotype
        dam = engine.classify_phenotype("Waja-ul-Mafasil", "Damawi (Hot & Wet)")
        self.assertEqual(dam.phenotype_code, "PHENO-ARTH-DAM")
        self.assertIn("Sanguine-Plethoric", dam.phenotype_name)

    def test_phenotype_stratification_diabetes(self):
        """Tests metabolic condition sub-phenotyping."""
        engine = PhenotypeAndResponseEngine()
        dm_haar = engine.classify_phenotype("Ziyabetus", "Haar Yabis")
        self.assertEqual(dm_haar.phenotype_code, "PHENO-DM-HAAR")
        self.assertIn("Metabolic Burn", dm_haar.phenotype_name)

        dm_barid = engine.classify_phenotype("Ziyabetus", "Barid Ratab")
        self.assertEqual(dm_barid.phenotype_code, "PHENO-DM-BARID")
        self.assertIn("Sluggish Metabolism", dm_barid.phenotype_name)

    def test_response_intelligence_responder_tier(self):
        """Tests Responder classification when VAS improves by >=75%."""
        engine = PhenotypeAndResponseEngine()
        res = engine.evaluate_response(
            patient_id="P-101",
            vas_baseline=8.0,
            vas_followup=1.5,
            adherence_pct=92.0,
            adverse_events=[]
        )
        self.assertEqual(res.tier, ResponseClassificationTier.RESPONDER)
        self.assertGreaterEqual(res.vas_improvement_pct, 75.0)
        self.assertFalse(res.protocol_switch_recommended)
        self.assertIn("EXCELLENT RESPONSE", res.clinical_recommendation)

    def test_response_intelligence_partial_and_non_responder(self):
        """Tests Partial Responder and Non-Responder with low adherence."""
        engine = PhenotypeAndResponseEngine()
        partial = engine.evaluate_response(
            patient_id="P-102",
            vas_baseline=8.0,
            vas_followup=4.0,
            adherence_pct=85.0
        )
        self.assertEqual(partial.tier, ResponseClassificationTier.PARTIAL_RESPONDER)
        self.assertEqual(partial.vas_improvement_pct, 50.0)

        non_resp = engine.evaluate_response(
            patient_id="P-103",
            vas_baseline=8.0,
            vas_followup=6.5,
            adherence_pct=45.0  # Poor adherence
        )
        self.assertEqual(non_resp.tier, ResponseClassificationTier.NON_RESPONDER)
        self.assertIn("SUB-OPTIMAL ADHERENCE", non_resp.clinical_recommendation)

    def test_response_intelligence_adherent_non_responder_safety_flag(self):
        """CRITICAL: Tests that Adherent Non-Responders automatically trigger escalation."""
        engine = PhenotypeAndResponseEngine()
        res = engine.evaluate_response(
            patient_id="P-104",
            vas_baseline=8.0,
            vas_followup=7.5,   # Only 6.25% relief
            adherence_pct=88.0, # High compliance!
            adverse_events=[]
        )
        self.assertEqual(res.tier, ResponseClassificationTier.ADHERENT_NON_RESPONDER)
        self.assertTrue(res.protocol_switch_recommended)
        self.assertIn("FLAG: ADHERENT NON-RESPONDER", res.clinical_recommendation)
        self.assertIn("second-line review", res.clinical_recommendation.lower())

    def test_response_intelligence_intolerant(self):
        """Tests Intolerant classification when adverse reaction occurs."""
        engine = PhenotypeAndResponseEngine()
        res = engine.evaluate_response(
            patient_id="P-105",
            vas_baseline=8.0,
            vas_followup=6.0,
            adherence_pct=80.0,
            adverse_events=[{"event": "Severe gastralgia and skin rash", "severity": "SEVERE"}]
        )
        self.assertEqual(res.tier, ResponseClassificationTier.INTOLERANT)
        self.assertTrue(res.protocol_switch_recommended)
        self.assertIn("DISCONTINUE CURRENT PROTOCOL", res.clinical_recommendation)

    def test_who_smart_l4_knowledge_compiler_compilation_and_validation(self):
        """Tests compilation, SemVer checking, reviewer gate, and self-testing in KnowledgeCompiler."""
        compiler = KnowledgeCompiler()

        # Valid Rule Compilation
        signoff = ReviewerSignoff.create("Hakim Z. Ahmad", "CHIEF_CLINICIAN", "ZAYVORA-TEST-001", "1.0.0")
        valid_rule_dict = {
            "rule_id": "ZAYVORA-TEST-001",
            "title": "Test Herbal Safety Rule",
            "version": "1.0.0",
            "source_evidence": {"evidence_level": "E2_PHARMACOPOEIA"},
            "inputs": ["esr"],
            "logic_expression": {"field": "esr", "gte": 30.0},
            "outputs": {"action": "RECOMMEND_TAKMEED"},
            "contraindications": ["Skin ulceration"],
            "safety_confidence": 0.95,
            "reviewer_approval": {
                "signed_by": signoff.signed_by,
                "reviewer_role": signoff.reviewer_role,
                "approval_timestamp": signoff.approval_timestamp,
                "signature_hash": signoff.signature_hash
            },
            "test_cases": [
                {"name": "High ESR matches", "inputs": {"esr": 35.0}, "expected_matches": True, "expected_action": "RECOMMEND_TAKMEED"},
                {"name": "Low ESR does not match", "inputs": {"esr": 15.0}, "expected_matches": False}
            ]
        }
        rule = compiler.compile_rule(valid_rule_dict)
        self.assertEqual(rule.rule_id, "ZAYVORA-TEST-001")
        self.assertEqual(rule.version, "1.0.0")

        # Fails if missing reviewer approval
        no_rev = dict(valid_rule_dict)
        no_rev["rule_id"] = "ZAYVORA-FAIL-001"
        no_rev["reviewer_approval"] = None
        with self.assertRaises(KnowledgeCompilerError):
            compiler.compile_rule(no_rev)

        # Fails if test case doesn't pass
        bad_test = dict(valid_rule_dict)
        bad_test["rule_id"] = "ZAYVORA-FAIL-002"
        bad_test["test_cases"] = [
            {"name": "Bad expectation", "inputs": {"esr": 35.0}, "expected_matches": False}
        ]
        with self.assertRaises(KnowledgeCompilerError):
            compiler.compile_rule(bad_test)

    def test_who_smart_l4_knowledge_compiler_execution_and_contraindication(self):
        """Tests deterministic rule execution and contraindication blocking."""
        compiler = KnowledgeCompiler()

        # Seeded Rule: Suranjan Joint Pain Rule
        # Eligible patient
        res = compiler.evaluate_rule(
            "ZAYVORA-WHO-L4-SURANJAN-001",
            {"condition": "waja_ul_mafasil", "serum_creatinine": 1.1}
        )
        self.assertTrue(res["matched"])
        self.assertFalse(res["blocked_by_contraindication"])
        self.assertEqual(res["outputs"]["action"], "AUTHORIZE_SURANJAN_PROTOCOL")

        # Contraindicated patient (Pregnancy)
        res_contra = compiler.evaluate_rule(
            "ZAYVORA-WHO-L4-SURANJAN-001",
            {"condition": "waja_ul_mafasil", "serum_creatinine": 1.1, "is_pregnant": "Pregnancy"}
        )
        self.assertFalse(res_contra["matched"])
        self.assertTrue(res_contra["blocked_by_contraindication"])
        self.assertIn("Pregnancy", res_contra["triggered_contraindications"])

    def test_clinical_orchestrator_stage_13_and_14_integration(self):
        """Tests end-to-end execution of continuum with Stage 13 & Stage 14 generation."""
        req = ClinicalContinuumRequest(
            patient_id="PAT-CONTINUUM-001",
            patient_name="Mohammad Tariq",
            age=48,
            gender="MALE",
            chief_complaints=["Severe bilateral knee arthralgia", "Morning joint stiffness"],
            presenting_condition="Waja-ul-Mafasil",
            symptom_duration_days=45,
            baseline_pain_vas=8.5,
            constitutional_signs={"nabz": "Bateea (Slow)", "baul": "Abyad (Pale)", "mizaj": "Balghami"},
            targeted_axes=["mafasil", "meda-amaa"],
            candidate_drugs=["Suranjan Talkh", "Asgandh", "Zanjabeel"],
            clinician_id="DOC-999",
            clinician_role="CHIEF_PHYSICIAN",
            followup_proms_day=14,
            followup_symptom_vas=2.0,  # Huge improvement
            followup_adverse_events=[]
        )

        resp = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)

        self.assertIsNotNone(resp.stage_13_precision_patient_model)
        self.assertEqual(resp.stage_13_precision_patient_model["patient_id"], "PAT-CONTINUUM-001")
        self.assertIn("longitudinal_trajectory_answers", resp.stage_13_precision_patient_model)

        self.assertIsNotNone(resp.stage_14_phenotype_and_response)
        pheno = resp.stage_14_phenotype_and_response["phenotype_profile"]
        self.assertIn("PHENO-ARTH-BALGHAM", pheno["phenotype_code"])

        resp_eval = resp.stage_14_phenotype_and_response["response_evaluation"]
        self.assertEqual(resp_eval["tier"], "RESPONDER")
        self.assertGreaterEqual(resp_eval["vas_improvement_pct"], 75.0)

    def test_live_api_server_precision_endpoints(self):
        """Tests that live API server imports and registers all precision and compiler handlers."""
        import services.live_api_server as server
        self.assertIsNotNone(server.PrecisionPatientModel)
        self.assertIsNotNone(server.PhenotypeAndResponseEngine)
        self.assertIsNotNone(server.KnowledgeCompiler)
        self.assertIsNotNone(server.global_knowledge_compiler)

        rules = server.global_knowledge_compiler.list_rules()
        self.assertGreaterEqual(len(rules), 2)
        self.assertTrue(any(r["rule_id"] == "ZAYVORA-WHO-L4-SURANJAN-001" for r in rules))


if __name__ == "__main__":
    unittest.main()
