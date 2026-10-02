"""
ZAYVORA Health OS™ — CP-AFUM & Organ-Axis Clinical System Master Test Suite
Source: Dr. Irfan Ashraf — CP-AFUM Textbook, Course Notes & Organ-Axis System
Verifies:
1. UDC Engine (Generation, Parsing, Clinical Constraints)
2. Mizaj Dose Adjustment Personalisation Engine (Table 1.3 Matrix & Thermal Balance)
3. Functional Diagnostics & 5 Non-Negotiable Lab Trigger Rules
4. 3-Phase Therapeutic Engine (R1-R8 Rules & Exit Gates)
5. 5 Non-Negotiable Axis Priority Rules & 6 Organ Axes
6. Dual-Track Delivery & Ilaj Hierarchy Engines
7. CP-AFUM Safety Screen & Red Flag Referrals
8. CP-AFUM Practicum Registry (7 Mandatory Elements) & Certification Engine
9. Live REST API Endpoints in services/live_api_server.py
"""
import unittest
import json
import io

from services.clinical.app.engines.udc_engine import (
    generate_udc, parse_udc, PROTOCOL_MAP
)
from services.clinical.app.engines.mizaj_dose_engine import (
    calculate_mizaj_dose_adjustments, get_herb_thermal_class
)
from services.clinical.app.engines.functional_lab_engine import (
    calculate_homa_ir, calculate_tg_hdl_ratio, evaluate_semen_analysis,
    evaluate_five_non_negotiable_lab_trigger_rules, FUNCTIONAL_LAB_RANGES
)
from services.clinical.app.engines.phase_therapeutic_engine import (
    evaluate_phase_trigger_rules, verify_phase_1_exit, verify_phase_2_exit
)
from services.clinical.app.engines.organ_axis_engine import (
    CP_AFUM_6_AXES, evaluate_five_axis_priority_rules
)
from services.therapeutic.app.engines.dual_track_engine import (
    evaluate_clinical_delivery_track, GMP_PRODUCTS_MASTER
)
from services.therapeutic.app.engines.ilaj_hierarchy_engine import (
    evaluate_ilaj_hierarchy_compliance, TADBEER_MODALITIES
)
from services.therapeutic.app.engines.safety_firewall import (
    evaluate_cp_afum_clinical_safety, CP_AFUM_RED_FLAGS, AFUF_HERB_DRUG_RULES, FORBIDDEN_FORMULATION_LIST
)
from services.clinical.app.engines.cp_afum_curriculum import (
    get_curriculum_summary, CP_AFUM_PROGRAMME_SPEC, SEMESTERS
)
from services.clinical.app.engines.practicum_registry import (
    validate_practicum_case, evaluate_practicum_portfolio, REQUIRED_CASES_DISTRIBUTION
)
from services.clinical.app.engines.certification_engine import (
    evaluate_practitioner_tier, CERTIFICATION_LEVELS
)
from services.live_api_server import ZayvoraApiHandler


class DummyRequest:
    def __init__(self, data: bytes):
        self.rfile = io.BytesIO(data)
        self.wfile = io.BytesIO()

    def makefile(self, *args, **kwargs):
        return self.rfile


class TestUdcEngine(unittest.TestCase):
    def test_udc_generation_and_parsing(self):
        udc = generate_udc("Balghami-Sawdawi", "Balgham Ghalib", "Jigar-Kulya", "Phase 1 (Tanqiya)")
        self.assertEqual(udc, "Balghami-Sawdawi — Balgham Ghalib — Jigar-Kulya — Phase 1 (Tanqiya)")
        
        parsed = parse_udc(udc)
        self.assertTrue(parsed["valid"])
        self.assertEqual(parsed["mizaj"], "Balghami-Sawdawi")
        self.assertEqual(parsed["dominant_khilt"], "Balgham Ghalib")
        self.assertEqual(parsed["primary_axis"], "Jigar-Kulya")
        self.assertEqual(parsed["phase_category"], "Tanqiya")
        self.assertEqual(parsed["recommended_protocol"], "WM-01")
        # Check Phase 1 constraint (no heavy tonics)
        self.assertTrue(any("Muqawwi" in c for c in parsed["clinical_constraints"]))

    def test_udc_taqwiyat_phase_constraints(self):
        udc = generate_udc("Safravi", "Safra Ghalib", "Gut-Ovarian", "Phase 3 (Taqwiyaat)")
        parsed = parse_udc(udc)
        self.assertTrue(parsed["valid"])
        self.assertEqual(parsed["phase_category"], "Taqwiyaat")
        self.assertEqual(parsed["recommended_protocol"], "PC-01")
        self.assertTrue(any("rebuilding" in c.lower() for c in parsed["clinical_constraints"]))


class TestMizajDoseEngine(unittest.TestCase):
    def test_safravi_dose_reduction(self):
        ingredients = [
            {"name": "Ashwagandha (5% withanolides)", "dose_mg": 1000},
            {"name": "Guggul (2.5% guggulsterones)", "dose_mg": 500},
            {"name": "Shatavari (cooling)", "dose_mg": 400},
            {"name": "Berberine (neutral)", "dose_mg": 1000}
        ]
        res = calculate_mizaj_dose_adjustments("Safravi", ingredients)
        # Safravi heating herbs must be reduced 25-30%
        ashwa = next(i for i in res["adjusted_ingredients"] if "Ashwagandha" in i["name"])
        self.assertLessEqual(ashwa["adjusted_dose"], 750.0)
        self.assertGreaterEqual(ashwa["adjusted_dose"], 700.0)
        # Cooling herbs increased +15%
        shata = next(i for i in res["adjusted_ingredients"] if "Shatavari" in i["name"])
        self.assertEqual(shata["adjusted_dose"], 460.0)
        # Neutral unchanged
        berb = next(i for i in res["adjusted_ingredients"] if "Berberine" in i["name"])
        self.assertEqual(berb["adjusted_dose"], 1000.0)
        # Check mandatory clinical flags for Safravi
        self.assertTrue(any("25-30%" in f for f in res["clinical_flags"]))
        self.assertTrue(any("SGPT" in f for f in res["clinical_flags"]))

    def test_thermal_balance_warning(self):
        # Formula with only hot herbs and no cooling
        hot_only = [
            {"name": "Ashwagandha", "dose_mg": 500},
            {"name": "Guggul", "dose_mg": 500}
        ]
        res = calculate_mizaj_dose_adjustments("Balghami", hot_only)
        self.assertFalse(res["is_thermally_balanced"])
        self.assertTrue(any("VIOLATION" in b for b in res["balance_notes"]))


class TestFunctionalLabEngine(unittest.TestCase):
    def test_homa_ir_and_tg_hdl_calculation(self):
        # Normal fasting glucose 95, elevated insulin 15 -> early IR
        homa = calculate_homa_ir(95.0, 15.0)
        self.assertAlmostEqual(homa["homa_ir"], 3.52, places=1)
        self.assertEqual(homa["status"], "MODERATE_RESISTANCE")
        
        # TG 180, HDL 35 -> ratio 5.14
        tg_hdl = calculate_tg_hdl_ratio(180.0, 35.0)
        self.assertAlmostEqual(tg_hdl["tg_hdl_ratio"], 5.14, places=1)
        self.assertEqual(tg_hdl["status"], "INSULIN_RESISTANCE")

    def test_five_lab_trigger_rules(self):
        # Test Rule 1: SGPT > 45
        eval1 = evaluate_five_non_negotiable_lab_trigger_rules({"sgpt": 52.0})
        self.assertTrue(eval1["phase_1_mandatory"])
        self.assertTrue(any("Rule 1" in t["rule"] for t in eval1["triggered_rules"]))

        # Test Rule 3: TSH > 2.5 with symptoms
        eval3 = evaluate_five_non_negotiable_lab_trigger_rules({"tsh": 3.8}, symptoms=["fatigue", "cold intolerance"])
        self.assertTrue(any("Rule 3" in t["rule"] for t in eval3["triggered_rules"]))

        # Test Rule 4: Fasting Insulin > 10
        eval4 = evaluate_five_non_negotiable_lab_trigger_rules({"fasting_insulin": 14.0})
        self.assertTrue(any("Rule 4" in t["rule"] for t in eval4["triggered_rules"]))

        # Test Rule 5: Specialist Referral (Anti-TPO > 300)
        eval5 = evaluate_five_non_negotiable_lab_trigger_rules({"anti_tpo": 350.0})
        self.assertTrue(eval5["requires_referral"])
        self.assertTrue(any("Endocrinology" in r for r in eval5["specialist_referrals"]))

    def test_semen_analysis_evaluation(self):
        params = {
            "volume_ml": 2.2,
            "total_motility_pct": 28.0,  # asthenospermia (<42)
            "concentration_million_ml": 8.0,  # oligospermia (<16)
            "morphology_kruger_pct": 2.0,  # teratospermia (<4)
            "dfi_pct": 38.0  # high DFI (>25)
        }
        sa = evaluate_semen_analysis(params)
        self.assertTrue(any("Asthenozoospermia" in f for f in sa["findings"]))
        self.assertTrue(any("Oligozoospermia" in f for f in sa["findings"]))
        self.assertTrue(any("Teratozoospermia" in f for f in sa["findings"]))
        self.assertTrue(any("DNA Fragmentation" in f for f in sa["findings"]))


class TestPhaseTherapeuticEngine(unittest.TestCase):
    def test_phase_trigger_rules_r1_to_r8(self):
        profile = {
            "sgpt": 62.0,
            "chronicity_months": 36,
            "mizaj": "Safravi",
            "severe_axes_count": 2,
            "hpa_compromised": True,
            "on_insulin_or_hypoglycemics": True
        }
        res = evaluate_phase_trigger_rules(profile)
        self.assertTrue(res["phase_1_mandatory"])  # R1
        self.assertEqual(res["recommended_phase_1_weeks"], 4)  # R2
        self.assertEqual(res["recommended_phase_2_weeks"], 16)  # R4
        applied_rules_codes = [r["rule"] for r in res["applied_rules"]]
        for r_code in ["R1", "R2", "R3", "R4", "R6", "R8"]:
            self.assertIn(r_code, applied_rules_codes)

    def test_phase_exit_gates(self):
        # Phase 1 exit: baseline SGPT 60, current 42 (30% drop) + hs-CRP down
        p1 = verify_phase_1_exit(60.0, 42.0, hs_crp_trending_down=True)
        self.assertTrue(p1["can_exit_phase_1"])

        # Phase 1 failure: baseline 60, current 55 (only 8.3% drop)
        p1_fail = verify_phase_1_exit(60.0, 55.0, hs_crp_trending_down=True)
        self.assertFalse(p1_fail["can_exit_phase_1"])

        # Phase 2 exit: baseline HbA1c 8.0, current 4.5 (43.7% drop) + 80% symptoms resolved
        p2 = verify_phase_2_exit(8.0, 4.5, symptom_resolution_pct=80.0)
        self.assertTrue(p2["can_exit_phase_2"])


class TestOrganAxisPriorityRules(unittest.TestCase):
    def test_five_axis_priority_rules(self):
        eval_res = evaluate_five_axis_priority_rules(
            sgpt=52.0,
            hs_crp=4.1,
            has_hpa_dysregulation=True,
            has_thyroid_dysfunction=True,
            active_axes=["Gut-Ovarian", "Liver-Pancreas", "Thyroid-Neuro", "HPA Axis"]
        )
        self.assertTrue(eval_res["gut_liver_mandatory"])  # Rule 1
        self.assertTrue(eval_res["hpa_stabilization_first"])  # Rule 2 & 3
        # Rule 4 Two-Axis Limit
        self.assertEqual(len(eval_res["priority_axes_phase_2"]), 2)
        self.assertEqual(len(eval_res["deferred_axes"]), 2)

    def test_6_axes_catalog_completeness(self):
        self.assertEqual(len(CP_AFUM_6_AXES), 6)
        expected = ["gut-liver", "liver-pancreas", "gut-ovarian", "liver-testicular", "thyroid-neuro", "hpa-axis"]
        for k in expected:
            self.assertIn(k, CP_AFUM_6_AXES)


class TestDualTrackAndHierarchy(unittest.TestCase):
    def test_dual_track_decision(self):
        # Grade 3 critical depletion -> Track 1 mandatory
        t1 = evaluate_clinical_delivery_track(is_remote=False, active_axes_count=1, quwwat_grade=3, patient_prefers_convenience=False)
        self.assertTrue(t1["mandatory"])
        self.assertIn("TRACK 1", t1["recommended_track"])

        # Remote patient with mild single axis -> Track 2
        t2 = evaluate_clinical_delivery_track(is_remote=True, active_axes_count=1, quwwat_grade=1, patient_prefers_convenience=True)
        self.assertIn("TRACK 2", t2["recommended_track"])

    def test_gmp_products_catalog(self):
        self.assertEqual(len(GMP_PRODUCTS_MASTER), 6)
        for prod in ["LiverPrime Core", "MetaboCore Elite", "OvaSync", "ManiVital Pro", "ThyroMet Axis", "NeuroCalmX"]:
            self.assertIn(prod, GMP_PRODUCTS_MASTER)

    def test_ilaj_hierarchy_rule(self):
        # Dawa prescribed without Ghiza/Parhez -> Violation
        check = evaluate_ilaj_hierarchy_compliance(
            prescribed_dawa=[{"name": "MetaboCore"}],
            tadbeer_prescriptions=["Riyazat 30 min daily"],
            ghiza_parhez_prescribed=False,
            nafsiyat_addressed=True
        )
        self.assertFalse(check["is_hierarchy_compliant"])
        self.assertTrue(any("HIERARCHY RULE" in v for v in check["violations"]))


class TestSafetyFirewallCpAfum(unittest.TestCase):
    def test_red_flag_referral_thresholds(self):
        patient_data = {
            "sgpt": 115.0,  # >100 U/L
            "anti_tpo": 380.0,  # >300 IU/mL
            "suicidal_ideation": True
        }
        res = evaluate_cp_afum_clinical_safety(patient_data, ingredients=["LiverPrime Core"], current_medications=[])
        self.assertTrue(res["requires_specialist_referral"])
        self.assertFalse(res["is_safe"])
        self.assertEqual(len(res["red_flag_referrals"]), 3)

    def test_forbidden_list_detection(self):
        res = evaluate_cp_afum_clinical_safety(
            patient_data={},
            ingredients=["Ashwagandha", "DHEA precursor", "Aristolochia"],
            current_medications=[]
        )
        self.assertFalse(res["is_safe"])
        self.assertEqual(len(res["forbidden_ingredients"]), 2)

    def test_herb_drug_interactions(self):
        res = evaluate_cp_afum_clinical_safety(
            patient_data={},
            ingredients=["Berberine", "Valerian", "Silymarin"],
            current_medications=["Metformin", "Zolpidem", "Cyclosporine"]
        )
        self.assertFalse(res["is_safe"])
        severities = [i["severity"] for i in res["herb_drug_interactions"]]
        self.assertIn("CONTRAINDICATED", severities)


class TestPracticumRegistryAndCertification(unittest.TestCase):
    def test_validate_practicum_case_rejection(self):
        # Missing Element 1 (Mizaj) -> Outright REJECTED
        bad_case = {
            "axis_identification": "Gut-Ovarian",
            "phase_protocol": "Phase 1 LiverPrime"
        }
        res = validate_practicum_case(bad_case)
        self.assertFalse(res["accepted"])
        self.assertEqual(res["status"], "REJECTED")

    def test_validate_practicum_case_accepted(self):
        complete_case = {
            "mizaj_assessment": "Balghami-Sawdawi dominant",
            "axis_identification": "Liver-Testicular + Gut-Liver",
            "severity_classification": "Grade 2 Moderate",
            "phase_protocol": "Phase 1 (4 wks) -> Phase 2 ManiVital Pro (12 wks) -> Phase 3 Taper",
            "product_stack": "LiverPrime Core, ManiVital Pro, CoQ10 300mg",
            "lab_monitoring_plan": "SA at baseline and 12 weeks, SGPT at 4 weeks",
            "predicted_outcome": "+30-50% sperm motility and +20% concentration at 12 weeks"
        }
        res = validate_practicum_case(complete_case)
        self.assertTrue(res["accepted"])
        self.assertEqual(res["status"], "ACCEPTED")
        self.assertEqual(res["score"], 100)

    def test_certification_progression(self):
        student_profile = {
            "semesters_completed": 3,
            "attendance_pct": 85.0,
            "accepted_cases_count": 20,
            "written_exam_score": 78.0,
            "viva_cleared": True,
            "lab_test_passed": True
        }
        cert = evaluate_practitioner_tier(student_profile)
        self.assertTrue(cert["is_certified_practitioner"])
        self.assertEqual(cert["current_tier"], "L1")
        self.assertEqual(cert["tier_details"]["code"], "CP-AFUM")


class TestLiveApiServerCpAfumEndpoints(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)

    def _call_post(self, path: str, payload: dict) -> dict:
        from unittest.mock import MagicMock
        raw_body = json.dumps(payload).encode("utf-8")
        req = DummyRequest(raw_body)
        self.handler.path = path
        self.handler.requestline = f"POST {path} HTTP/1.1"
        self.handler.command = "POST"
        self.handler.request_version = "HTTP/1.1"
        self.handler.client_address = ("127.0.0.1", 12345)
        self.handler.server = MagicMock()
        self.handler.close_connection = False
        self.handler.headers = {
            "Content-Length": str(len(raw_body)),
            "Content-Type": "application/json"
        }
        self.handler.rfile = req.rfile
        self.handler.wfile = req.wfile
        self.handler.do_POST()
        
        output_bytes = req.wfile.getvalue()
        header_end = output_bytes.find(b"\r\n\r\n")
        body_bytes = output_bytes[header_end + 4:]
        return json.loads(body_bytes.decode("utf-8"))

    def _call_get(self, path: str) -> dict:
        from unittest.mock import MagicMock
        req = DummyRequest(b"")
        self.handler.path = path
        self.handler.requestline = f"GET {path} HTTP/1.1"
        self.handler.command = "GET"
        self.handler.request_version = "HTTP/1.1"
        self.handler.client_address = ("127.0.0.1", 12345)
        self.handler.server = MagicMock()
        self.handler.close_connection = False
        self.handler.headers = {}
        self.handler.rfile = req.rfile
        self.handler.wfile = req.wfile
        self.handler.do_GET()

        output_bytes = req.wfile.getvalue()
        header_end = output_bytes.find(b"\r\n\r\n")
        body_bytes = output_bytes[header_end + 4:]
        return json.loads(body_bytes.decode("utf-8"))

    def test_api_curriculum_get(self):
        res = self._call_get("/api/v1/academic/curriculum")
        self.assertTrue(res["ok"])
        self.assertEqual(res["curriculum"]["spec"]["total_lectures"], 96)

    def test_api_udc_generate_post(self):
        res = self._call_post("/api/v1/clinical/udc/generate", {
            "mizaj": "Safravi",
            "dominant_khilt": "Safra Ghalib",
            "primary_axis": "Gut-Ovarian",
            "afaal_phase": "Phase 2 (Tahleel)"
        })
        self.assertTrue(res["ok"])
        self.assertIn("Safravi — Safra Ghalib — Gut-Ovarian — Phase 2 (Tahleel)", res["udc_code"])

    def test_api_mizaj_dose_post(self):
        res = self._call_post("/api/v1/clinical/mizaj/adjust-dose", {
            "mizaj": "Safravi",
            "ingredients": [{"name": "Ashwagandha", "dose_mg": 1000}]
        })
        self.assertTrue(res["ok"])
        adj = res["adjustment"]["adjusted_ingredients"][0]
        self.assertEqual(adj["adjusted_dose"], 720.0)

    def test_api_functional_labs_post(self):
        res = self._call_post("/api/v1/clinical/labs/analyze-functional", {
            "labs": {"sgpt": 54.0, "fasting_glucose": 100, "fasting_insulin": 14.0},
            "symptoms": ["fatigue"]
        })
        self.assertTrue(res["ok"])
        self.assertTrue(res["triggers"]["phase_1_mandatory"])
        self.assertIsNotNone(res["homa_ir"])

    def test_api_practicum_case_validation_post(self):
        res = self._call_post("/api/v1/academic/practicum/validate-case", {
            "case_data": {
                "mizaj_assessment": "Damvi dominant",
                "axis_identification": "Gut-Liver",
                "severity_classification": "Grade 1 Mild",
                "phase_protocol": "Phase 1 LiverPrime",
                "product_stack": "LiverPrime Core",
                "lab_monitoring_plan": "SGPT 4-weekly",
                "predicted_outcome": "SGPT normal at 4 weeks"
            }
        })
        self.assertTrue(res["ok"])
        self.assertTrue(res["validation"]["accepted"])


if __name__ == "__main__":
    unittest.main()
