"""
Test Suite: ZAYVORA Master Clinical Architecture & Decision Support System
References:
  - Book 1: The Organ-Axis Based Functional Unani System
  - Book 2: ZAYVORA Clinical Handbook (Precision Protocols for the Modern Hakim)
  - Master Clinical System: Complete Protocol Architecture & Business Model
  - Patient & Family Guide: Understanding Your Health Through Unani Medicine
Author: Dr. Irfan Ashraf, BUMS.
"""

import unittest
import json
import io
from unittest.mock import MagicMock

from services.knowledge.app.data.dual_tier_product_catalog import (
    DUAL_TIER_CATALOG,
    get_dual_tier_product,
    get_all_dual_tier_products,
    validate_80_20_compliance
)
from services.knowledge.app.data.program_packages_pricing import (
    PROGRAM_TIER_SPECS,
    PROGRAM_SPECIFIC_PRICING,
    get_program_pricing,
    calculate_clinic_revenue_projection
)
from services.knowledge.app.data.matab_compounding_formulas import (
    MATAB_FORMULAS,
    get_matab_formula,
    get_all_matab_formulas
)
from services.knowledge.app.data.patient_education_modules import (
    PATIENT_EDUCATION_CHAPTERS,
    get_patient_education_module,
    get_all_patient_education_modules
)
from services.clinical.app.engines.clinical_decision_support_ext import ClinicalDecisionSupportExt
from services.clinical.app.engines.emergency_red_flag_guard import EmergencyRedFlagGuard
import services.live_api_server as las


class TestDualTierProductCatalog(unittest.TestCase):
    """Verifies dual-tier product architecture and 80/20 formulation rules."""

    def test_catalog_structure_and_tiers(self):
        prods = get_all_dual_tier_products()
        self.assertGreaterEqual(len(prods), 3)

        p1 = get_dual_tier_product("ZAY-PROD-01")
        self.assertIsNotNone(p1)
        self.assertEqual(p1["core_line"]["capsule_fill_mg"], 500)
        self.assertEqual(p1["elite_line"]["capsule_fill_mg"], 700)
        self.assertIn("twice daily", p1["core_line"]["dosing"])
        self.assertIn("1 capsule twice daily", p1["elite_line"]["dosing"])

    def test_80_20_compliance_validator(self):
        # Valid formula: 85% Unani herbs, 15% Precision
        valid_formula = [
            {"name": "Shatavari Extract", "amount_mg": 200, "category": "80% Core"},
            {"name": "Ashoka Extract", "amount_mg": 150, "category": "80% Core"},
            {"name": "Lodhra Extract", "amount_mg": 100, "category": "80% Core"},
            {"name": "Zinc Bisglycinate", "amount_mg": 15, "category": "20% Precision"},
            {"name": "Piperine", "amount_mg": 5, "category": "20% Precision"}
        ]
        res_valid = validate_80_20_compliance(valid_formula)
        self.assertTrue(res_valid["compliant"])
        self.assertGreaterEqual(res_valid["unani_core_percentage"], 70.0)

        # Invalid formula: Modern nutraceutical dominates as hero ingredient
        invalid_formula = [
            {"name": "Myo-Inositol", "amount_mg": 500, "category": "20% Precision"},
            {"name": "Shatavari Extract", "amount_mg": 50, "category": "80% Core"}
        ]
        res_invalid = validate_80_20_compliance(invalid_formula)
        self.assertFalse(res_invalid["compliant"])
        self.assertIn("Modern ingredient dominates", res_invalid["violation"])


class TestProgramPackagesAndPricing(unittest.TestCase):
    """Verifies 90-day program tiers, deliverables, and revenue projections."""

    def test_tier_specs(self):
        self.assertIn("BASIC", PROGRAM_TIER_SPECS)
        self.assertIn("ADVANCED", PROGRAM_TIER_SPECS)
        self.assertIn("SIGNATURE_ELITE", PROGRAM_TIER_SPECS)

        elite = PROGRAM_TIER_SPECS["SIGNATURE_ELITE"]
        self.assertIn("Clinical Elite Line", elite["product_line"])
        self.assertIn("Biomarker 360", elite["lab_support"])

    def test_program_pricing_calculation(self):
        fert_basic = get_program_pricing("FEMALE_FERTILITY", "BASIC")
        self.assertEqual(fert_basic["price_inr"], 12000)
        self.assertEqual(fert_basic["biological_duration_days"], 90)

        fert_elite = get_program_pricing("FEMALE_FERTILITY", "SIGNATURE_ELITE")
        self.assertEqual(fert_elite["price_inr"], 42000)

    def test_clinic_revenue_model(self):
        # 20 Basic @ ₹10k, 15 Advanced @ ₹22k, 5 Signature @ ₹40k = ₹7,30,000 monthly
        rev = calculate_clinic_revenue_projection(20, 15, 5)
        self.assertEqual(rev["monthly_breakdown"]["total_monthly_revenue_inr"], 730000)
        self.assertEqual(rev["single_clinic_annual_inr"], 8760000)


class TestMatabFormulasAndEducation(unittest.TestCase):
    """Verifies internal dispensary formulations and patient education chapters."""

    def test_matab_formulas(self):
        all_matab = get_all_matab_formulas()
        self.assertGreaterEqual(len(all_matab), 8)

        m1 = get_matab_formula("MATAB-01")
        self.assertIsNotNone(m1)
        self.assertIn("phase_1", m1["phases"])
        self.assertIn("phase_2", m1["phases"])
        self.assertIn("phase_3", m1["phases"])

    def test_patient_education_modules(self):
        mods = get_all_patient_education_modules()
        self.assertGreaterEqual(len(mods), 4)

        tsh = get_patient_education_module("tsh-vs-free-t3")
        self.assertIsNotNone(tsh)
        self.assertIn("60% of all T4-to-T3 conversion occurs in the LIVER", tsh["pathophysiology"]["the_liver_connection"])


class TestClinicalDecisionSupportAndRedFlags(unittest.TestCase):
    """Verifies plateau management, mixed mizaj resolution, and emergency referral guard."""

    def test_plateau_evaluation_engine(self):
        # Patient at 4 weeks with stagnant progress
        res_plateau = ClinicalDecisionSupportExt.evaluate_treatment_plateau(
            weeks_on_protocol=4,
            reported_compliance_pct=90.0,
            subjective_improvement_pct=5.0,
            lab_markers_stagnant=True,
            patient_frustration=True,
            current_herbs=["Asgandh", "Guggul"]
        )
        self.assertTrue(res_plateau["plateau_detected"])
        self.assertEqual(len(res_plateau["modification_protocol"]), 6)
        self.assertGreaterEqual(len(res_plateau["suggested_rotations"]), 2)

        # On track patient
        res_ok = ClinicalDecisionSupportExt.evaluate_treatment_plateau(
            weeks_on_protocol=4,
            reported_compliance_pct=95.0,
            subjective_improvement_pct=40.0,
            lab_markers_stagnant=False,
            patient_frustration=False
        )
        self.assertFalse(res_ok["plateau_detected"])

    def test_mixed_mizaj_resolver(self):
        # Hot Liver + Cold Kidneys
        res = ClinicalDecisionSupportExt.resolve_mixed_mizaj_conflict(
            "Liver", "Hot", "Kidney", "Cold", "Elevated ALT and low libido"
        )
        self.assertIn("Hot Liver / Cold Kidneys", res["clinical_pattern"])
        self.assertEqual(len(res["sequenced_solution"]), 3)
        self.assertIn("Cool and Clear the Liver First", res["sequenced_solution"][0]["stage"])

    def test_emergency_red_flag_guard(self):
        # Safe patient
        safe_eval = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["mild fatigue", "occasional bloating"],
            labs={"alt": 28, "creatinine": 0.9, "fbs": 92}
        )
        self.assertTrue(safe_eval["is_safe_for_unani_care"])

        # Cardiac chest pain emergency
        cardiac_eval = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["acute chest pain", "shortness of breath radiating to left arm"]
        )
        self.assertFalse(cardiac_eval["is_safe_for_unani_care"])
        self.assertIn("EMERGENCY HARD STOP", cardiac_eval["decision"])

        # Objective Hepatic ALT > 300 U/L
        hepatic_eval = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["nausea"],
            labs={"alt": 340}
        )
        self.assertFalse(hepatic_eval["is_safe_for_unani_care"])
        self.assertTrue(any(f["system"] == "Hepatic" for f in hepatic_eval["detected_red_flags"]))

        # Objective Renal Creatinine > 2.0 mg/dL
        renal_eval = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["swollen ankles"],
            labs={"creatinine": 2.6}
        )
        self.assertFalse(renal_eval["is_safe_for_unani_care"])
        self.assertTrue(any(f["system"] == "Renal" for f in renal_eval["detected_red_flags"]))


class TestMasterSystemLiveApiEndpoints(unittest.TestCase):
    """Verifies live HTTP endpoints in live_api_server.py."""

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"

    def test_get_dual_tier_catalog_endpoint(self):
        self.handler.path = "/api/v1/knowledge/catalog/dual-tier"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/catalog/dual-tier HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertGreaterEqual(body["total_products"], 3)

    def test_get_program_packages_endpoint(self):
        self.handler.path = "/api/v1/knowledge/programs/packages"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/programs/packages HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertIn("SIGNATURE_ELITE", body["tier_specs"])

    def test_post_validate_80_20_endpoint(self):
        payload = json.dumps({
            "formula_items": [
                {"name": "Shatavari", "amount_mg": 200, "category": "80% Core"},
                {"name": "Lodhra", "amount_mg": 100, "category": "80% Core"},
                {"name": "Zinc", "amount_mg": 10, "category": "20% Precision"}
            ]
        }).encode("utf-8")
        self.handler.path = "/api/v1/therapeutic/formula/validate-80-20"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/therapeutic/formula/validate-80-20 HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertTrue(body["evaluation"]["compliant"])

    def test_post_triage_red_flags_endpoint(self):
        payload = json.dumps({
            "symptoms": ["chest pain", "shortness of breath"],
            "labs": {}
        }).encode("utf-8")
        self.handler.path = "/api/v1/clinical/triage/red-flags"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/clinical/triage/red-flags HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertFalse(body["triage_evaluation"]["is_safe_for_unani_care"])


if __name__ == "__main__":
    unittest.main()
