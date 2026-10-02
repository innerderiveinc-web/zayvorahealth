"""
ZAYVORA Health OS™ — Next-Gen Platform Enhancements Unit Test Suite
===================================================================
Tests all 4 newly integrated strategic pillars:
  1. AI Copilot (Hakeem Sahab™) Deep RAG Integration (12 Volumes + 38 Treatises)
  2. Interactive Clinical Case Simulator & Medical Competency Grading Engine
  3. Full Offline PWA (Web Manifest & Service Worker caching)
  4. Botanical Visual Atlas & Morphological Identification Keys
  5. Live REST API Endpoints in live_api_server.py
"""

import os
import json
import unittest
from typing import Dict, Any

class TestPlatformEnhancementsSuite(unittest.TestCase):

    # =========================================================================
    # 1. AI COPILOT DEEP RAG INTEGRATION
    # =========================================================================
    def test_01_hakeem_deep_rag_extraction(self):
        from services.ai.app.engines.hakeem_case_brief_engine import HakeemCaseBriefEngine
        rag = HakeemCaseBriefEngine.extract_grand_library_canonical_rag(
            clinical_condition="Waja-ul-Mafasil",
            patient_mizaj="Balgham",
            symptoms=["Joint swelling", "Morning stiffness"]
        )
        self.assertIsInstance(rag, dict)
        self.assertIn("matched_chapters", rag)
        self.assertGreater(len(rag["matched_chapters"]), 0)
        self.assertIn("canonical_treatise_excerpts", rag)
        self.assertGreater(len(rag["canonical_treatise_excerpts"]), 0)
        self.assertIn("classical_citations", rag)
        self.assertGreater(len(rag["classical_citations"]), 0)
        
        # Verify first treatise excerpt contains 4 deep layers
        first_excerpt = rag["canonical_treatise_excerpts"][0]
        self.assertIn("canonical_philosophy", first_excerpt)
        self.assertIn("molecular_pathophysiology", first_excerpt)
        self.assertIn("bedside_semiology", first_excerpt)
        self.assertIn("recipes_mudabbar", first_excerpt)

    def test_02_hakeem_evidence_grounded_copilot_brief_contains_deep_rag(self):
        from services.ai.app.engines.hakeem_case_brief_engine import HakeemCaseBriefEngine
        brief = HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
            patient_id="PAT-TEST-001",
            patient_context={
                "name": "Hamza Tariq",
                "age": 45,
                "chief_complaints": ["Chronic polyarthritis", "Joint pain"],
                "mizaj": "Balgham"
            },
            clinical_condition="Waja-ul-Mafasil"
        )
        self.assertIsInstance(brief, dict)
        self.assertIn("grand_library_canonical_rag", brief)
        rag_data = brief["grand_library_canonical_rag"]
        self.assertGreater(rag_data["total_matches"], 0)
        self.assertIn("clinical_reasoning_summary", brief)
        self.assertIn("draft_nuskha", brief)

    # =========================================================================
    # 2. INTERACTIVE CLINICAL CASE SIMULATOR ENGINE
    # =========================================================================
    def test_03_case_simulator_catalog(self):
        from services.knowledge.app.engines.case_simulator_engine import CaseSimulatorEngine
        cases = CaseSimulatorEngine.get_all_cases()
        self.assertIsInstance(cases, list)
        self.assertGreaterEqual(len(cases), 3)
        for c in cases:
            self.assertIn("id", c)
            self.assertIn("title_en", c)
            self.assertIn("category", c)
            self.assertIn("difficulty", c)
            self.assertIn("total_stages", c)
            self.assertGreaterEqual(c["total_stages"], 4)

    def test_04_case_simulator_sanitization(self):
        from services.knowledge.app.engines.case_simulator_engine import CaseSimulatorEngine
        # Sanitized (for doctor/student taking challenge)
        sanitized = CaseSimulatorEngine.get_case_by_id("sim-case-01", sanitize_answers=True)
        self.assertIsNotNone(sanitized)
        for stage in sanitized["stages"]:
            self.assertNotIn("correct_option_index", stage)
            self.assertNotIn("classical_citation", stage)
            self.assertNotIn("biomedical_rationale", stage)
            self.assertEqual(len(stage["options"]), 4)

        # Unsanitized (for grading engine)
        full = CaseSimulatorEngine.get_case_by_id("sim-case-01", sanitize_answers=False)
        self.assertIsNotNone(full)
        for stage in full["stages"]:
            self.assertIn("correct_option_index", stage)
            self.assertIn("classical_citation", stage)
            self.assertIn("biomedical_rationale", stage)

    def test_05_case_simulator_evaluation_and_grading(self):
        from services.knowledge.app.engines.case_simulator_engine import CaseSimulatorEngine
        # Case 1 correct answers: Stage 1 -> 1, Stage 2 -> 1, Stage 3 -> 1, Stage 4 -> 1
        perfect_answers = {1: 1, 2: 1, 3: 1, 4: 1}
        result = CaseSimulatorEngine.evaluate_case_submission(
            case_id="sim-case-01",
            user_answers=perfect_answers,
            clinician_id="DOC-TEST"
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["score_percentage"], 100.0)
        self.assertEqual(result["correct_stages"], 4)
        self.assertEqual(result["clinical_competency_rank"], "Master Integrative Physician (Tabeeb-e-Haziq)")
        self.assertEqual(len(result["stage_evaluations"]), 4)
        for ev in result["stage_evaluations"]:
            self.assertTrue(ev["is_correct"])
            self.assertTrue(len(ev["classical_citation"]) > 20)
            self.assertTrue(len(ev["biomedical_rationale"]) > 20)

    # =========================================================================
    # 3. FULL OFFLINE PWA (MANIFEST & SERVICE WORKER)
    # =========================================================================
    def test_06_pwa_manifest_validity(self):
        paths = ["manifest.json", "docs/manifest.json", "apps/web/public/manifest.json"]
        for p in paths:
            self.assertTrue(os.path.exists(p), f"Manifest missing at {p}")
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("name", data)
            self.assertIn("short_name", data)
            self.assertEqual(data["theme_color"], "#2D6A4F")
            self.assertEqual(data["display"], "standalone")
            self.assertIn("icons", data)
            self.assertGreater(len(data["icons"]), 0)

    def test_07_service_worker_validity(self):
        paths = ["sw.js", "docs/sw.js", "apps/web/public/sw.js"]
        for p in paths:
            self.assertTrue(os.path.exists(p), f"ServiceWorker missing at {p}")
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("addEventListener('install'", content)
            self.assertIn("addEventListener('fetch'", content)

    # =========================================================================
    # 4. BOTANICAL VISUAL ATLAS & IDENTIFICATION KEYS
    # =========================================================================
    def test_08_botanical_visual_atlas_catalog(self):
        from services.knowledge.app.data.botanical_visual_atlas import get_all_botanical_atlas, get_botanical_by_id
        atlas = get_all_botanical_atlas()
        self.assertEqual(len(atlas), 12)

        for herb in atlas:
            self.assertIn("id", herb)
            self.assertIn("canonical_name", herb)
            self.assertIn("botanical_name", herb)
            self.assertIn("family", herb)
            self.assertIn("vernacular_names", herb)
            self.assertIn("urdu", herb["vernacular_names"])
            self.assertIn("mizaj", herb)
            self.assertIn("macroscopic_diagnostic_keys", herb)
            self.assertIn("organoleptic_profile", herb)
            self.assertIn("microscopic_diagnostic_markers", herb)
            self.assertIn("adulteration_detection_sops", herb)
            self.assertGreater(len(herb["adulteration_detection_sops"]), 0)

    def test_09_botanical_visual_atlas_lookup_and_detox(self):
        from services.knowledge.app.data.botanical_visual_atlas import get_botanical_by_id
        suranjan = get_botanical_by_id("bva-02-suranjan")
        self.assertIsNotNone(suranjan)
        self.assertEqual(suranjan["canonical_name"], "Suranjan Shireen")
        self.assertTrue(suranjan["detoxification_and_safety"]["is_schedule_e1"])
        self.assertTrue(suranjan["detoxification_and_safety"]["mudabbar_required"])
        self.assertIn("cow's milk", suranjan["detoxification_and_safety"]["purification_sop"].lower())

        asgandh = get_botanical_by_id("asgandh")
        self.assertIsNotNone(asgandh)
        self.assertEqual(asgandh["canonical_name"], "Asgandh")

    # =========================================================================
    # 5. LIVE REST API ROUTE INTEGRATION
    # =========================================================================
    def test_10_live_api_routes_available(self):
        import services.live_api_server as las
        # Verify engine loaders
        self.assertIsNotNone(las.CaseSimulatorEngine)
        self.assertIsNotNone(las.get_all_botanical_atlas)
        self.assertIsNotNone(las.HakeemCaseBriefEngine)

        # Direct verification of simulator catalog
        cases = las.CaseSimulatorEngine.get_all_cases()
        self.assertGreaterEqual(len(cases), 3)

        # Direct verification of botanical atlas
        atlas = las.get_all_botanical_atlas()
        self.assertEqual(len(atlas), 12)

        # Direct verification of Deep RAG copilot brief
        brief = las.HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
            patient_id="MRN-TEST-99",
            patient_context={"name": "Rashid Khan", "age": 50, "chief_complaints": ["Gouty arthritis"]},
            clinical_condition="Waja-ul-Mafasil"
        )
        self.assertIn("grand_library_canonical_rag", brief)
        self.assertGreater(len(brief["grand_library_canonical_rag"]["matched_chapters"]), 0)


if __name__ == "__main__":
    unittest.main()
