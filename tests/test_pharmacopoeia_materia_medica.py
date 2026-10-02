"""
Test Suite: ZAYVORA Pharmacopoeia (Single Drugs Reference & Scientific Validation)
Reference: Parts 1 & 2 by Dr. Irfan Ashraf, BUMS.
Verifies:
  1. Monographs integrity (Classical Mizaj 1-4, Afaal, Modern Pharmacodynamics, ZAYVORA products).
  2. Thermal Balance & Net Mizaj Calculator.
  3. Mandatory Musleh Corrective Enforcement (Aqarqarha & Tabasheer/Sandal, Guggul & Amla).
  4. Tadbir (Purification/Shuddhi) Certification Gate (Sang-e-Yahud, Shilajit).
  5. Pharmacological Synergy Detection (Mitochondrial Triad, 2000% Bioavailability cascade).
"""

import unittest
import json
import io
from services.knowledge.app.data.pharmacopoeia_monographs import (
    MONOGRAPHS,
    get_all_monographs,
    get_monograph,
    get_monograph_by_key,
    search_monographs
)
from services.therapeutic.app.engines.formula_safety_checker import FormulaSafetyChecker


class TestPharmacopoeiaMonographs(unittest.TestCase):
    """Verifies atomic botanical, mineral, and bioactive single drug monographs."""

    def test_monograph_count_and_categories(self):
        self.assertGreaterEqual(len(MONOGRAPHS), 40)
        all_drugs = get_all_monographs()
        self.assertEqual(len(all_drugs), len(MONOGRAPHS))

    def test_key_botanicals_part_1(self):
        # Aqarqarha (Hot 4, Dry 3) - most potent thermal agent
        aq = get_monograph("AQARQARHA")
        self.assertIsNotNone(aq)
        self.assertEqual(aq["mizaj"]["heat"], 4)
        self.assertEqual(aq["mizaj"]["dryness"], 3)
        self.assertIn("Tabasheer", aq["why_essential"])

        # Asgandh
        asg = get_monograph("ASGANDH")
        self.assertIsNotNone(asg)
        self.assertIn("Withania somnifera", asg["botanical_name"])
        self.assertTrue(any("Muqawwi" in a for a in asg["afaal"]))

        # Amla
        amla = get_monograph("AMLA")
        self.assertIsNotNone(amla)
        self.assertEqual(amla["mizaj"]["cold"], 1)
        self.assertEqual(amla["mizaj"]["dryness"], 2)

    def test_key_botanicals_and_minerals_part_2(self):
        # Sang-e-Yahud (Fossil Stone)
        sy = get_monograph("SANG_E_YAHUD")
        self.assertIsNotNone(sy)
        self.assertIn("Kulthi", sy["tadbir"])

        # Shilajit
        sh = get_monograph("SHILAJIT")
        self.assertIsNotNone(sh)
        self.assertIn("fulvic", sh["pharmacodynamics"].lower())

        # Saffron / Zafran
        zf = get_monograph("ZAFRAN")
        self.assertIsNotNone(zf)
        self.assertEqual(zf["mizaj"]["heat"], 2)
        self.assertEqual(zf["mizaj"]["dryness"], 1)

    def test_modern_bioactive_nutraceuticals(self):
        coq10 = get_monograph("COQ10")
        self.assertIsNotNone(coq10)
        self.assertIn("ATP", coq10["pharmacodynamics"])

        cit = get_monograph("L_CITRULLINE")
        self.assertIsNotNone(cit)
        self.assertIn("nitric oxide", cit["pharmacodynamics"].lower())

        zn = get_monograph("ZINC_BISGLYCINATE")
        self.assertIsNotNone(zn)
        self.assertIn("sperm", zn["why_essential"].lower())

    def test_search_monographs(self):
        results = search_monographs("curcumin")
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any(r["key"] == "HALDI" for r in results))

        results_af = search_monographs("aphrodisiac")
        self.assertGreaterEqual(len(results_af), 2)


class TestFormulaThermalAndSafetyEngine(unittest.TestCase):
    """Verifies thermal balance, Musleh enforcement, and Tadbir quality gates."""

    def test_net_mizaj_thermal_calculator(self):
        # Highly heating formula: Aqarqarha (4H) + Filfil Siyah (3H)
        hot_formula = [
            {"key": "AQARQARHA", "weight_g": 1.0},
            {"key": "FILFIL_SIYAH", "weight_g": 1.0}
        ]
        res_hot = FormulaSafetyChecker.calculate_net_formula_mizaj(hot_formula)
        self.assertGreater(res_hot["net_thermal_index"], 2.0)
        self.assertIn("Hot Dominant", res_hot["classified_formula_mizaj"])

        # Thermally counter-balanced formula: Aqarqarha + Tabasheer (Cold 2) + Sandal Safaid (Cold 3)
        balanced_formula = [
            {"key": "AQARQARHA", "weight_g": 1.0},
            {"key": "TABASHEER", "weight_g": 1.0},
            {"key": "SANDAL_SAFAID", "weight_g": 1.0},
            {"key": "AMLA", "weight_g": 1.0}
        ]
        res_bal = FormulaSafetyChecker.calculate_net_formula_mizaj(balanced_formula)
        self.assertLess(res_bal["net_thermal_index"], 1.5)

    def test_aqarqarha_musleh_enforcement_rule(self):
        # Missing Tabasheer & Sandal must fail
        unprotected_formula = [
            {"key": "AQARQARHA", "weight_g": 1.0},
            {"key": "ASGANDH", "weight_g": 2.0}
        ]
        audit_unprotected = FormulaSafetyChecker.audit_formula_safety_and_musleh(unprotected_formula)
        self.assertFalse(audit_unprotected["formula_cleared"])
        self.assertEqual(audit_unprotected["decision"], "FORMULA REJECTED - SAFETY INTERACTION")
        self.assertTrue(any("Tabasheer" in v for v in audit_unprotected["violations"]))

        # Protected formula must pass
        protected_formula = [
            {"key": "AQARQARHA", "weight_g": 1.0},
            {"key": "TABASHEER", "weight_g": 1.0},
            {"key": "SANDAL_SAFAID", "weight_g": 1.0}
        ]
        audit_protected = FormulaSafetyChecker.audit_formula_safety_and_musleh(protected_formula)
        self.assertTrue(audit_protected["formula_cleared"])
        self.assertEqual(audit_protected["decision"], "FORMULA APPROVED FOR COMPOUNDING")

    def test_curcumin_piperine_synergy_and_caution(self):
        # Haldi without Piperine gives caution
        haldi_alone = [{"key": "HALDI", "weight_g": 1.0}]
        audit_haldi = FormulaSafetyChecker.audit_formula_safety_and_musleh(haldi_alone)
        self.assertTrue(any("Piperine" in c for c in audit_haldi["cautions"]))

        # Haldi + Filfil Siyah (contains piperine) activates 2,000% cascade
        haldi_piperine = [
            {"key": "HALDI", "weight_g": 1.0},
            {"key": "FILFIL_SIYAH", "weight_g": 0.05}
        ]
        audit_synergy = FormulaSafetyChecker.audit_formula_safety_and_musleh(haldi_piperine)
        self.assertTrue(any("2,000% Bioavailability" in s for s in audit_synergy["synergies_detected"]))

    def test_mitochondrial_triad_synergy(self):
        mito_formula = [
            {"key": "COQ10", "weight_g": 0.1},
            {"key": "SHILAJIT", "weight_g": 0.25},
            {"key": "L_CARNITINE", "weight_g": 0.5}
        ]
        audit_mito = FormulaSafetyChecker.audit_formula_safety_and_musleh(mito_formula)
        self.assertTrue(any("Mitochondrial Power Triad" in s for s in audit_mito["synergies_detected"]))

    def test_tadbir_purification_verification(self):
        # Sang-e-Yahud insufficient oxidation (<40 days)
        bad_sy = FormulaSafetyChecker.verify_tadbir_compliance(
            "SANG_E_YAHUD",
            {"oxidation_days": 15, "finely_triturated": True}
        )
        self.assertFalse(bad_sy["passed"])
        self.assertIn("Sang-e-Yahud requires full 40-day oxidation", bad_sy["reason"])

        # Sang-e-Yahud compliant
        good_sy = FormulaSafetyChecker.verify_tadbir_compliance(
            "SANG_E_YAHUD",
            {"oxidation_days": 42, "finely_triturated": True}
        )
        self.assertTrue(good_sy["passed"])
        self.assertIn("Tadbir-e-Sang-e-Yahud Certified", good_sy["certification"])

        # Shilajit heavy metals violation (>3 ppm)
        bad_shilajit = FormulaSafetyChecker.verify_tadbir_compliance(
            "SHILAJIT",
            {"lead_ppm": 8.5, "fulvic_acid_percent": 55.0}
        )
        self.assertFalse(bad_shilajit["passed"])
        self.assertIn("Lead 8.5 ppm exceeds", bad_shilajit["reason"])

        # Shilajit compliant
        good_shilajit = FormulaSafetyChecker.verify_tadbir_compliance(
            "SHILAJIT",
            {"lead_ppm": 1.2, "fulvic_acid_percent": 58.0}
        )
        self.assertTrue(good_shilajit["passed"])
        self.assertIn("Shodhana Certified", good_shilajit["certification"])


if __name__ == "__main__":
    unittest.main()


class TestPharmacopoeiaLiveApiEndpoints(unittest.TestCase):
    """Tests live HTTP GET & POST routes in live_api_server.py for Pharmacopoeia."""

    def setUp(self):
        import services.live_api_server as las
        import io
        from unittest.mock import MagicMock
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"

    def test_get_all_monographs_endpoint(self):
        import io
        self.handler.path = "/api/v1/knowledge/materia-medica/all"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/materia-medica/all HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertGreaterEqual(body["total_monographs"], 40)

    def test_get_single_monograph_endpoint(self):
        import io
        self.handler.path = "/api/v1/knowledge/materia-medica/AQARQARHA"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/materia-medica/AQARQARHA HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertEqual(body["monograph"]["key"], "AQARQARHA")

    def test_post_audit_safety_endpoint(self):
        import io
        payload = json.dumps({
            "ingredients": [
                {"key": "AQARQARHA", "weight_g": 1.0},
                {"key": "TABASHEER", "weight_g": 1.0},
                {"key": "SANDAL_SAFAID", "weight_g": 1.0}
            ]
        }).encode("utf-8")
        self.handler.path = "/api/v1/therapeutic/formula/audit-safety"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/therapeutic/formula/audit-safety HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertTrue(body["audit"]["formula_cleared"])

    def test_post_tadbir_verify_endpoint(self):
        import io
        payload = json.dumps({
            "drug_name": "SANG_E_YAHUD",
            "tadbir_report": {
                "oxidation_days": 45,
                "finely_triturated": True
            }
        }).encode("utf-8")
        self.handler.path = "/api/v1/therapeutic/formula/tadbir-verify"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/therapeutic/formula/tadbir-verify HTTP/1.1"
        self.handler.rfile = io.BytesIO(payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body = json.loads(resp_lines[1])
        self.assertTrue(body["ok"])
        self.assertTrue(body["tadbir_verification"]["passed"])
