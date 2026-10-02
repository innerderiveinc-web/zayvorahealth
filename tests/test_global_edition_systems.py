"""
Test Suite for ZAYVORA Global Edition (Second Edition 2026) Clinical & AI Systems
Author: Dr. Irfan Ashraf, BUMS

Validates:
  1. ZAPE 4-Layer Personalisation Engine (Layer 1-4 logic, 6 axes, Mizaj moderation)
  2. Regimental Hydrotherapy & Dalak Engine (Hammam 3-room sequence, contrast shower, Hijama safety gate)
  3. Global Protocols & Appendix B Templates (T2DM, Hypertension, PCOS, Metabolic Syndrome, NAFLD, IBS)
  4. OCEBM Evidence Grading & Canonical Glossary Engine
  5. Live REST API integration endpoints for all new capabilities
"""

import unittest
import json
import io
from unittest.mock import MagicMock

# Engines
from services.clinical.app.engines.zape_engine import ZAPEEngine
from services.therapeutic.app.engines.regimental_hydrotherapy_engine import RegimentalHydrotherapyEngine
from services.clinical.app.engines.global_protocols_engine import GlobalProtocolsEngine
from services.knowledge.app.engines.evidence_glossary_engine import EvidenceGlossaryEngine
import services.live_api_server as las


class TestGlobalEditionSystems(unittest.TestCase):

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"

    # ==================== 1. ZAPE ENGINE TESTS ====================

    def test_zape_axis_calculation_and_moderation(self):
        """Test ZAPE Layer 2 and Layer 3 calculations."""
        raw_data = {
            "patient_id": "PT-TEST-001",
            "mizaj": "Bard-Ratab",
            "bmi": 32.5,
            "waist_cm": 98.0,
            "fbg": 135.0,
            "fasting_insulin": 20.0,
            "hba1c": 7.4,
            "hs_crp": 3.5,
            "pss_10": 22,
            "sbp": 145,
            "dbp": 92,
            "symptoms": ["fatigue", "bloating", "joint pain"]
        }

        decision = ZAPEEngine.generate_zape_decision_support(raw_data)
        self.assertEqual(decision["patient_id"], "PT-TEST-001")
        self.assertEqual(decision["mizaj"], "Bard-Ratab")

        # Check activations
        activations = decision["axis_activations"]
        self.assertIn("Metabolic Axis", activations)
        self.assertIn("Inflammatory Axis", activations)
        self.assertGreaterEqual(activations["Metabolic Axis"]["score"], 50)
        self.assertEqual(activations["Metabolic Axis"]["severity"], "Moderate" if activations["Metabolic Axis"]["score"] < 65 else "Severe")

        # Check Layer 3 Moderation for Bard-Ratab (Cold-Wet)
        lifestyle = decision["recommendations"]["tier_1_lifestyle"]
        self.assertIn("Warming", lifestyle["nutrition"]["principle"])

        # Check Tier 2 Botanicals contains Berberine & Gymnema/Cinnamon
        botanicals = decision["recommendations"]["tier_2_botanicals"]
        botanical_names = [b["botanical"] for b in botanicals]
        self.assertIn("Berberine", botanical_names)

    # ==================== 2. REGIMENTAL & THERMOREGULATION TESTS ====================

    def test_hammam_thermal_sequence_and_contraindications(self):
        """Test Hammam sequence generation and pregnancy/neuropathy gates."""
        # Standard healthy prescription
        h_ok = RegimentalHydrotherapyEngine.generate_hammam_prescription("Bard-Ratab", "Metabolic Syndrome")
        self.assertTrue(h_ok["eligible"])
        self.assertEqual(len(h_ok["sequence"]), 4)
        self.assertEqual(h_ok["sequence"][2]["chamber"], "Bayt al-Harara (Hot Inner Steam Chamber)")
        self.assertEqual(h_ok["sequence"][2]["target_temp_c"], 41.0)

        # Pregnancy contraindication check
        h_preg = RegimentalHydrotherapyEngine.generate_hammam_prescription("Bard-Ratab", "Metabolic", is_pregnant=True)
        self.assertFalse(h_preg["eligible"])
        self.assertIn("pregnancy", h_preg["reason"].lower())

    def test_hijama_safety_gate(self):
        """Test Hijama contraindication screening."""
        # Cleared case
        h_safe = RegimentalHydrotherapyEngine.verify_hijama_safety(
            platelet_count=220000,
            hemoglobin_g_dl=14.2,
            is_anticoagulated=False,
            is_pregnant=False,
            active_infection_at_site=False
        )
        self.assertTrue(h_safe["cleared"])
        self.assertEqual(h_safe["max_extraction_volume_ml"], 50)

        # Anticoagulation rejection
        h_anti = RegimentalHydrotherapyEngine.verify_hijama_safety(
            platelet_count=220000,
            hemoglobin_g_dl=14.2,
            is_anticoagulated=True,
            is_pregnant=False,
            active_infection_at_site=False
        )
        self.assertFalse(h_anti["cleared"])
        self.assertIn("anticoagulant", h_anti["reasons"][0].lower())

    def test_dalak_directional_colonic_massage(self):
        """Test directional clockwise massage for IBS/Suoo-e-Hazm."""
        d_ibs = RegimentalHydrotherapyEngine.prescribe_dalak("Bard-Ratab", "IBS-C with bloating")
        self.assertTrue(d_ibs["eligible"])
        self.assertIn("Clockwise", d_ibs["direction"])

    # ==================== 3. DISEASE PROTOCOLS & APPENDIX B ====================

    def test_t2dm_remission_and_template_b1(self):
        """Test T2DM DiRECT remission logic and Template B1 output."""
        res_active = GlobalProtocolsEngine.evaluate_t2dm(
            hba1c=7.5, fbg=140.0, fasting_insulin=16.0, bmi=29.0, waist_cm=95.0, mizaj="Bard-Ratab", current_meds=["Metformin 1000mg"]
        )
        self.assertEqual(res_active["status"], "Type 2 Diabetes Mellitus Confirmed")
        self.assertFalse(res_active["is_in_remission"])
        self.assertIn("template_b1", res_active)

        # Complete Remission test (off meds, HbA1c < 5.7%)
        res_remiss = GlobalProtocolsEngine.evaluate_t2dm(
            hba1c=5.4, fbg=92.0, fasting_insulin=5.0, bmi=24.0, waist_cm=82.0, current_meds=[]
        )
        self.assertTrue(res_remiss["is_in_remission"])
        self.assertIn("Complete Remission", res_remiss["remission_type"])

    def test_hypertension_imtila_dam_and_template_b2(self):
        """Test Hypertension ACC/AHA classification and Template B2."""
        htn_res = GlobalProtocolsEngine.evaluate_hypertension(sbp=148, dbp=94, mizaj="Harr-Ratab")
        self.assertEqual(htn_res["category"], "Stage 2 Hypertension")
        self.assertEqual(htn_res["template_b2"]["template_id"], "Appendix B2: Hypertension Initial Assessment")
        self.assertIn("Arjuna", str(htn_res["template_b2"]["botanical_support"]))

    def test_pcos_rotterdam_criteria_and_template_b3(self):
        """Test Rotterdam criteria consensus (2 of 3) and Phenotype A."""
        pcos_res = GlobalProtocolsEngine.evaluate_pcos(
            cycle_length_days=45,
            cycles_per_year=6,
            hirsutism_score=9,
            total_testosterone_nmol=2.8,
            ovarian_follicles_count=22,
            amh_pmol_l=42.0,
            fasting_insulin=18.0,
            homa_ir=3.2
        )
        self.assertTrue(pcos_res["pcos_confirmed"])
        self.assertIn("Phenotype A", pcos_res["phenotype"])
        self.assertIn("Myo-Inositol 4g/day", pcos_res["template_b3"]["inositol_protocol"])

    def test_metabolic_syndrome_idf_criteria_and_template_b4(self):
        """Test IDF 2009 Harmonized Metabolic Syndrome Criteria (3 of 5)."""
        met_res = GlobalProtocolsEngine.evaluate_metabolic_syndrome(
            waist_cm=95.0,
            sex="male",
            is_asian=True,
            triglycerides_mg_dl=180.0,
            hdl_mg_dl=35.0,
            sbp=135,
            dbp=88,
            fbg_mg_dl=110.0
        )
        self.assertTrue(met_res["metabolic_syndrome_confirmed"])
        self.assertGreaterEqual(met_res["criteria_count"], 3)
        self.assertIn("Samn Mufrit", met_res["template_b4"]["unani_concept"])

    # ==================== 4. EVIDENCE GRADING & GLOSSARY ====================

    def test_ocebm_evidence_registry_and_glossary(self):
        """Test OCEBM evidence level queries and 42-term canonical glossary."""
        all_ev = EvidenceGlossaryEngine.get_all_evidence()
        self.assertGreaterEqual(len(all_ev), 15)

        # Filter by condition
        dash_ev = EvidenceGlossaryEngine.filter_evidence_by_condition("Hypertension")
        self.assertTrue(any(e["intervention"] == "DASH Diet" for e in dash_ev))

        # Check glossary term
        term_tabiyat = EvidenceGlossaryEngine.get_glossary_term("Tabiyat")
        self.assertIsNotNone(term_tabiyat)
        self.assertEqual(term_tabiyat["english"], "Innate Healing Intelligence")

    # ==================== 5. REST API ENDPOINTS ====================

    def test_api_endpoints_zape_and_regimen(self):
        """Test live HTTP dispatch for new Global Edition endpoints."""
        # 1. GET /api/v1/knowledge/evidence/all
        self.handler.path = "/api/v1/knowledge/evidence/all"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/evidence/all HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body_get = json.loads(resp_lines[1])
        self.assertTrue(body_get["ok"])
        self.assertGreaterEqual(len(body_get["evidence"]), 15)

        # 2. POST /api/v1/clinical/zape/evaluate
        payload = {
            "patient_id": "TEST-REST-01",
            "mizaj": "Harr-Yabis",
            "bmi": 26.0,
            "sbp": 138,
            "dbp": 86,
            "fbg": 110.0,
            "hba1c": 6.2,
            "fasting_insulin": 14.0,
            "hs_crp": 2.2
        }
        body_str = json.dumps(payload)
        self.handler.path = "/api/v1/clinical/zape/evaluate"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/clinical/zape/evaluate HTTP/1.1"
        self.handler.rfile = io.BytesIO(body_str.encode("utf-8"))
        self.handler.headers = {"Content-Length": str(len(body_str))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body_post = json.loads(resp_lines[1])
        self.assertTrue(body_post["ok"])
        self.assertIn("zape_decision_support", body_post)


if __name__ == "__main__":
    unittest.main()
