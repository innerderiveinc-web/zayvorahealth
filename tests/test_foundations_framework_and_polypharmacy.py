"""
Test Suite: ZAYVORA Foundations, Framework & Polypharmacy Architecture
Reference:
  - ZAYVORA (Part One: Foundations, Framework & Pharmacopoeia)
  - Dr. Irfan Ashraf, BUMS (ISBN: 978-81-960123-4-5)

Mechanisms Verified:
  1. Z-MAI 6-Domain Quantitative Scoring Matrix (0-3 scale, max 18 per humor) & Dosage Form Selector
  2. 4-Tier Polypharmacy Architecture Audit (20-30% / 50-60% / 15-25% / 5-10%)
  3. Behman Dual-Color Balance Law & Aqarqarha Micro-Dose Ceiling (200mg/day max)
  4. 4-Tier Evidence Hierarchy & AYUSH Claims Discipline Matrix
  5. Closed-Loop Biomarker Confirmation Algorithm (Balgham, Safra, Sauda)
  6. Live REST API Server Endpoints
"""

import unittest
import json
import io
from unittest.mock import MagicMock

from services.knowledge.app.data.zmai_scoring_tool import (
    calculate_mizaj_2_matrix,
    MIZAJ_2_DOMAINS
)
from services.therapeutic.app.engines.formula_safety_checker import FormulaSafetyChecker
from services.knowledge.app.data.evidence_grading_matrix import (
    EVIDENCE_TIERS,
    get_all_evidence_tiers,
    get_evidence_tier_details,
    validate_product_claim
)
from services.clinical.app.engines.functional_lab_engine import verify_humoral_biomarker_correlation
import services.live_api_server as las


class TestZMAI6DomainMatrix(unittest.TestCase):
    """Verifies Z-MAI 6-domain quantitative scoring matrix and dosage form rules (Part One Ch 9)."""

    def test_domains_list(self):
        self.assertEqual(len(MIZAJ_2_DOMAINS), 6)
        expected = [
            "body_build_weight", "skin_complexion", "psychological_profile",
            "digestion_appetite", "sleep_quality", "tongue_pulse"
        ]
        self.assertEqual(MIZAJ_2_DOMAINS, expected)

    def test_balgham_dominance_and_safoof_rule(self):
        domain_scores = {
            "body_build_weight": {"balgham": 3, "safra": 0, "sauda": 0, "dam": 1},
            "skin_complexion": {"balgham": 3, "safra": 0, "sauda": 0, "dam": 0},
            "psychological_profile": {"balgham": 2, "safra": 1, "sauda": 0, "dam": 1},
            "digestion_appetite": {"balgham": 3, "safra": 0, "sauda": 1, "dam": 0},
            "sleep_quality": {"balgham": 3, "safra": 0, "sauda": 0, "dam": 1},
            "tongue_pulse": {"balgham": 2, "safra": 0, "sauda": 1, "dam": 0},
        }
        res = calculate_mizaj_2_matrix(domain_scores)
        self.assertEqual(res["primary_dominant_humor"], "balgham")
        self.assertEqual(res["primary_score"], 16)
        self.assertEqual(res["primary_category"], "SIGNIFICANT_DOMINANCE")
        logic = res["clinical_adjustment_logic"]
        # Phlegm dominance strictly forbids moist Majoon and mandates Safoof
        self.assertIn("Safoof", logic["recommended_dosage_form"])
        self.assertIn("Majoon", logic["contraindicated_dosage_form"])
        self.assertIn("Mujaffif", logic["pharmacological_strategy"])

    def test_safra_dominance_and_joshanda_rule(self):
        domain_scores = {
            "body_build_weight": {"safra": 3},
            "skin_complexion": {"safra": 3},
            "psychological_profile": {"safra": 3},
            "digestion_appetite": {"safra": 2},
            "sleep_quality": {"safra": 2},
            "tongue_pulse": {"safra": 2},
        }
        res = calculate_mizaj_2_matrix(domain_scores)
        self.assertEqual(res["primary_dominant_humor"], "safra")
        self.assertEqual(res["primary_score"], 15)
        self.assertEqual(res["primary_category"], "SIGNIFICANT_DOMINANCE")
        logic = res["clinical_adjustment_logic"]
        self.assertIn("Joshanda", logic["recommended_dosage_form"])

    def test_sauda_dominance_and_arq_sharbat_rule(self):
        domain_scores = {
            "body_build_weight": {"sauda": 2},
            "skin_complexion": {"sauda": 3},
            "psychological_profile": {"sauda": 3},
            "digestion_appetite": {"sauda": 2},
            "sleep_quality": {"sauda": 2},
            "tongue_pulse": {"sauda": 2},
        }
        res = calculate_mizaj_2_matrix(domain_scores)
        self.assertEqual(res["primary_dominant_humor"], "sauda")
        self.assertEqual(res["primary_score"], 14)
        logic = res["clinical_adjustment_logic"]
        self.assertTrue("Arq" in logic["recommended_dosage_form"] or "Sharbat" in logic["recommended_dosage_form"])

    def test_clamping_behavior(self):
        # Val over 3 should clamp to 3
        domain_scores = {"body_build_weight": {"balgham": 10}}
        res = calculate_mizaj_2_matrix(domain_scores)
        self.assertEqual(res["mizaj_scores"]["balgham"], 3)


class TestFourTierPolypharmacyArchitecture(unittest.TestCase):
    """Verifies symphonic 4-tier formula architecture audit (Part One Ch 15)."""

    def test_symphonic_polypharmacy_pass(self):
        components = [
            {"tier": 1, "weight_g": 25.0}, # 25% (Target: 20-30%)
            {"tier": 2, "weight_g": 55.0}, # 55% (Target: 50-60%)
            {"tier": 3, "weight_g": 15.0}, # 15% (Target: 15-25%)
            {"tier": 4, "weight_g": 5.0},  # 5%  (Target: 5-10%)
        ]
        res = FormulaSafetyChecker.audit_four_tier_polypharmacy(components)
        self.assertTrue(res["is_symphonic_polypharmacy"])
        self.assertEqual(len(res["warnings"]), 0)
        self.assertEqual(res["status"], "SYMPHONIC POLYPHARMACY APPROVED")
        self.assertEqual(res["tier_percentages"]["tier_1_foundation"], 25.0)
        self.assertEqual(res["tier_percentages"]["tier_2_core"], 55.0)

    def test_polypharmacy_ratio_deviation_warnings(self):
        # Core is 85%, Foundation is 5%
        components = [
            {"tier": 1, "weight_g": 5.0},
            {"tier": 2, "weight_g": 85.0},
            {"tier": 3, "weight_g": 5.0},
            {"tier": 4, "weight_g": 5.0},
        ]
        res = FormulaSafetyChecker.audit_four_tier_polypharmacy(components)
        self.assertFalse(res["is_symphonic_polypharmacy"])
        self.assertGreater(len(res["warnings"]), 0)
        self.assertIn("POLYPHARMACY RATIO DEVIATION", res["status"])


class TestBehmanDualColorAndAqarqarhaRules(unittest.TestCase):
    """Verifies Behman dual-color balance, Aqarqarha ceiling, and Tabasheer specs (Ch 15)."""

    def test_behman_surkh_without_safaid_triggers_violation(self):
        ingredients = [
            {"key": "BEHMAN_SURKH", "weight_g": 5.0, "mizaj": "Hot 2 / Dry 2"}
        ]
        res = FormulaSafetyChecker.audit_formula_safety_and_musleh(ingredients)
        self.assertFalse(res["formula_cleared"])
        self.assertTrue(any("THERMAL BALANCE VIOLATION" in v for v in res["violations"]))

    def test_behman_surkh_with_safaid_passes_and_detects_synergy(self):
        ingredients = [
            {"key": "BEHMAN_SURKH", "weight_g": 5.0, "mizaj": "Hot 2 / Dry 2"},
            {"key": "BEHMAN_SAFAID", "weight_g": 5.0, "mizaj": "Cold 1 / Moist 2"}
        ]
        res = FormulaSafetyChecker.audit_formula_safety_and_musleh(ingredients)
        self.assertTrue(res["formula_cleared"])
        self.assertTrue(any("Behman Dual-Color Balance Active" in s for s in res["synergies_detected"]))

    def test_aqarqarha_dose_ceiling_violation(self):
        ingredients = [
            {"key": "AQARQARHA", "daily_dose_mg": 350.0, "mizaj": "Hot 3 / Dry 3"},
            {"key": "TABASHEER", "weight_g": 5.0},
            {"key": "SANDAL_SAFAID", "weight_g": 5.0}
        ]
        res = FormulaSafetyChecker.audit_formula_safety_and_musleh(ingredients)
        self.assertFalse(res["formula_cleared"])
        self.assertTrue(any("OVERDOSE VIOLATION" in v for v in res["violations"]))

    def test_aqarqarha_safe_dose_passes(self):
        ingredients = [
            {"key": "AQARQARHA", "daily_dose_mg": 180.0, "mizaj": "Hot 3 / Dry 3"},
            {"key": "TABASHEER", "weight_g": 5.0},
            {"key": "SANDAL_SAFAID", "weight_g": 5.0}
        ]
        res = FormulaSafetyChecker.audit_formula_safety_and_musleh(ingredients)
        self.assertTrue(res["formula_cleared"])

    def test_tabasheer_tadbir_standards(self):
        # Valid Tabasheer (>=85% silica, Lead <1 ppm, As <0.5 ppm)
        report_ok = {"silica_percent": 88.5, "lead_ppm": 0.4, "arsenic_ppm": 0.15}
        res_ok = FormulaSafetyChecker.verify_tadbir_compliance("TABASHEER", report_ok)
        self.assertTrue(res_ok["passed"])
        self.assertIn("DNA Heat Shield Certified", res_ok["certification"])

        # Subpotent / high heavy metal
        report_bad = {"silica_percent": 72.0, "lead_ppm": 1.8, "arsenic_ppm": 0.8}
        res_bad = FormulaSafetyChecker.verify_tadbir_compliance("TABASHEER", report_bad)
        self.assertFalse(res_bad["passed"])


class TestEvidenceHierarchyAndClaimsDiscipline(unittest.TestCase):
    """Verifies 4-tier evidence hierarchy and claims validator (Part One Ch 17)."""

    def test_evidence_tiers_structure(self):
        tiers = get_all_evidence_tiers()
        self.assertEqual(len(tiers), 4)
        t1 = get_evidence_tier_details("TIER_1")
        self.assertEqual(t1["symbol"], "✅")
        self.assertIn("Double-blind", t1["definition"])

    def test_prohibited_claims_caught(self):
        claim = "This herbal extract treats diabetes and cures infertility completely."
        res = validate_product_claim(claim, "TIER_3")
        self.assertFalse(res["claim_compliant"])
        self.assertGreaterEqual(len(res["violations"]), 2)
        self.assertEqual(res["recommended_action"], "REVISE CLAIM PER AYUSH CLAIMS DISCIPLINE MATRIX")

    def test_illegal_comparisons_and_unsupported_rct_assertions(self):
        claim = "It is natural viagra that beats sildenafil with no side effects and is clinically proven."
        res = validate_product_claim(claim, "TIER_3")
        self.assertFalse(res["claim_compliant"])
        self.assertTrue(any("natural viagra" in v for v in res["violations"]))
        self.assertTrue(any("beats sildenafil" in v for v in res["violations"]))
        self.assertTrue(any("no side effects" in v for v in res["violations"]))
        self.assertTrue(any("Tier 1 clinical trial proof" in v for v in res["violations"]))

    def test_compliant_claim_passes(self):
        claim = "Supports healthy blood glucose levels and glucose metabolism as part of a balanced diet."
        res = validate_product_claim(claim, "TIER_2")
        self.assertTrue(res["claim_compliant"])
        self.assertEqual(len(res["violations"]), 0)


class TestHumoralBiomarkerClosedLoop(unittest.TestCase):
    """Verifies objective mapping between Unani humors and functional lab panels (Part One Ch 8)."""

    def test_balgham_closed_loop_confirmation(self):
        labs = {
            "fasting_insulin": 16.0,
            "tsh": 3.4,
            "homa_ir": 2.8,
            "ldl": 130,
            "bmi": 28.0
        }
        res = verify_humoral_biomarker_correlation("BALGHAM", labs)
        self.assertTrue(res["is_biomarker_confirmed"])
        self.assertEqual(len(res["confirmations"]), 5)
        self.assertIn("HOMA-IR", res["confirmations"][3])

    def test_safra_closed_loop_confirmation(self):
        labs = {
            "hs_crp": 4.2,
            "alt": 62,
            "ast": 50,
            "bilirubin": 1.5
        }
        res = verify_humoral_biomarker_correlation("SAFRA", labs)
        self.assertTrue(res["is_biomarker_confirmed"])
        self.assertEqual(len(res["confirmations"]), 4)
        self.assertTrue(any("hsCRP" in c for c in res["confirmations"]))

    def test_sauda_closed_loop_confirmation(self):
        labs = {
            "cortisol": 23.5,
            "homocysteine": 15.2,
            "mda": 3.2
        }
        res = verify_humoral_biomarker_correlation("SAUDA", labs)
        self.assertTrue(res["is_biomarker_confirmed"])
        self.assertEqual(len(res["confirmations"]), 3)


class TestLiveApiServerPartOneEndpoints(unittest.TestCase):
    """Verifies live REST API server routing for Part One endpoints."""

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

    def test_get_evidence_grading_matrix(self):
        self.handler.path = "/api/v1/knowledge/evidence/grading-matrix"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/evidence/grading-matrix HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(len(body["tiers"]), 4)

    def test_get_zmai_matrix_domains(self):
        self.handler.path = "/api/v1/clinical/zmai/matrix/domains"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/clinical/zmai/matrix/domains HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(len(body["matrix_domains"]), 6)

    def test_post_zmai_score_matrix(self):
        payload = json.dumps({
            "domain_scores": {
                "body_build_weight": {"balgham": 3},
                "skin_complexion": {"balgham": 3},
                "psychological_profile": {"balgham": 3},
                "digestion_appetite": {"balgham": 2},
                "sleep_quality": {"balgham": 2},
                "tongue_pulse": {"balgham": 2}
            }
        }).encode("utf-8")
        self.handler.path = "/api/v1/clinical/zmai/score-matrix"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/clinical/zmai/score-matrix HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(body["evaluation"]["primary_dominant_humor"], "balgham")
        self.assertIn("Safoof", body["evaluation"]["clinical_adjustment_logic"]["recommended_dosage_form"])

    def test_post_audit_4tier_polypharmacy(self):
        payload = json.dumps({
            "components": [
                {"tier": 1, "weight_g": 25.0},
                {"tier": 2, "weight_g": 55.0},
                {"tier": 3, "weight_g": 15.0},
                {"tier": 4, "weight_g": 5.0}
            ]
        }).encode("utf-8")
        self.handler.path = "/api/v1/therapeutic/formula/audit-4tier"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/therapeutic/formula/audit-4tier HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertTrue(body["polypharmacy_audit"]["is_symphonic_polypharmacy"])

    def test_post_biomarker_closed_loop(self):
        payload = json.dumps({
            "suspected_humor": "SAFRA",
            "labs": {"hs_crp": 4.5, "alt": 60}
        }).encode("utf-8")
        self.handler.path = "/api/v1/clinical/labs/biomarker-closed-loop"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/clinical/labs/biomarker-closed-loop HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertTrue(body["biomarker_correlation"]["is_biomarker_confirmed"])

    def test_post_validate_claim(self):
        payload = json.dumps({
            "claim_text": "Clinically proven to cure infertility and treat diabetes completely",
            "evidence_tier": "TIER_3"
        }).encode("utf-8")
        self.handler.path = "/api/v1/knowledge/claims/validate"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/knowledge/claims/validate HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertFalse(body["claims_evaluation"]["claim_compliant"])


if __name__ == "__main__":
    unittest.main()
