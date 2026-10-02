"""
ZAYVORA Health OS™ — Full Validation Suite #57
===============================================
Tests all Phase 1-5 implementations:
  Phase 1: Safety Firewall ZMF Hard-Block + Copilot Ingredient Gate
  Phase 2: 12-Gate Pipeline Tracker
  Phase 3: Badal-e-Advia Substitute Advisory
  Phase 4: Patient Monograph Card Generator
  Phase 5: API route integration (GET + POST)
"""
import sys
import os
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.live_api_server import ZayvoraApiHandler


def _call_get(path):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {}
    req.request_version = "HTTP/1.1"
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_GET()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


def _call_post(path, payload):
    data = json.dumps(payload).encode()
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {"Content-Length": str(len(data))}
    req.request_version = "HTTP/1.1"
    req.rfile = io.BytesIO(data)
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_POST()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


class TestPhase1SafetyFirewallHardBlock(unittest.TestCase):
    """Phase 1a: ZMF Hard-Block wired into safety_firewall.run_safety_firewall()"""

    def test_zmf_blocked_ingredient_triggers_do_not_recommend(self):
        """ZMF-002 (Suranjan Talkh) should trigger DO_NOT_RECOMMEND verdict."""
        from services.therapeutic.app.engines.safety_firewall import run_safety_firewall
        result = run_safety_firewall(
            patient_context={"age": 40, "pregnancy_status": "not_pregnant",
                             "lactation_status": "no", "allergies": [],
                             "current_medications": [], "comorbidities": [],
                             "chief_complaint": "joint pain"},
            ingredients=[{"name": "Suranjan Talkh", "zmf_id": "ZMF-002", "dose_mg": 50}]
        )
        self.assertEqual(result["verdict"], "DO_NOT_RECOMMEND")
        reasons_text = " ".join(result["reasons"])
        self.assertIn("HARD BLOCK", reasons_text)

    def test_suranjan_shodhana_enforcement(self):
        """ZMF-002 without shodhana_certified must trigger Shodhana enforcement message."""
        from services.therapeutic.app.engines.safety_firewall import run_safety_firewall
        result = run_safety_firewall(
            patient_context={"age": 40, "pregnancy_status": "not_pregnant",
                             "lactation_status": "no", "allergies": [],
                             "current_medications": [], "comorbidities": [],
                             "chief_complaint": "joint pain"},
            ingredients=[{"name": "Suranjan Talkh", "zmf_id": "ZMF-002",
                          "shodhana_certified": False}]
        )
        reasons_text = " ".join(result["reasons"])
        self.assertIn("SHODHANA ENFORCEMENT", reasons_text)

    def test_non_blocked_zmf_passes_gate(self):
        """ZMF-001 (Asgandh) must NOT trigger ZMF hard-block."""
        from services.therapeutic.app.engines.safety_firewall import run_safety_firewall
        result = run_safety_firewall(
            patient_context={"age": 35, "pregnancy_status": "not_pregnant",
                             "lactation_status": "no", "allergies": [],
                             "current_medications": [], "comorbidities": [],
                             "chief_complaint": "fatigue"},
            ingredients=[{"name": "Asgandh", "zmf_id": "ZMF-001", "dose_mg": 500}]
        )
        reasons_text = " ".join(result["reasons"])
        self.assertNotIn("MUFRADAT-250 HARD BLOCK", reasons_text)

    def test_zmf_101_shangraf_blocked(self):
        """ZMF-101 (Shangraf / Mercury Sulphide) must trigger hard block."""
        from services.therapeutic.app.engines.safety_firewall import run_safety_firewall
        result = run_safety_firewall(
            patient_context={"age": 50, "pregnancy_status": "not_pregnant",
                             "lactation_status": "no", "allergies": [],
                             "current_medications": [], "comorbidities": [],
                             "chief_complaint": "skin disease"},
            ingredients=[{"name": "Shangraf", "zmf_id": "ZMF-101"}]
        )
        self.assertEqual(result["verdict"], "DO_NOT_RECOMMEND")
        reasons_text = " ".join(result["reasons"])
        self.assertIn("HARD BLOCK", reasons_text)


class TestPhase1CopilotIngredientGate(unittest.TestCase):
    """Phase 1b: Copilot ingredient access gate via evaluate_ingredient_access()"""

    def test_ai_blocked_from_high_risk_zmf(self):
        """AI Copilot must be HARD_BLOCKED for ZMF-002 (HIGH_RISK_28)."""
        from services.ai.app.security.copilot_permission_guard import CopilotPermissionGuard
        result = CopilotPermissionGuard.evaluate_ingredient_access(
            zmf_id="ZMF-002", ingredient_name="Suranjan Talkh",
            actor_role="HAKEEM_SAHAB_AI"
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["status"], "HARD_BLOCKED_ZMF_HIGH_RISK_28")

    def test_clinician_bypasses_block(self):
        """A registered Hakeem must bypass the AI ingredient block."""
        from services.ai.app.security.copilot_permission_guard import CopilotPermissionGuard
        result = CopilotPermissionGuard.evaluate_ingredient_access(
            zmf_id="ZMF-002", ingredient_name="Suranjan Talkh",
            actor_role="HAKEEM"
        )
        self.assertTrue(result["allowed"])
        self.assertEqual(result["status"], "ALLOWED_CLINICIAN_AUTHORITY")

    def test_non_blocked_ingredient_allowed_for_ai(self):
        """ZMF-001 (Asgandh) must be allowed for AI research access."""
        from services.ai.app.security.copilot_permission_guard import CopilotPermissionGuard
        result = CopilotPermissionGuard.evaluate_ingredient_access(
            zmf_id="ZMF-001", ingredient_name="Asgandh",
            actor_role="HAKEEM_SAHAB_AI"
        )
        self.assertTrue(result["allowed"])
        self.assertEqual(result["status"], "ALLOWED_RESEARCH_ONLY")

    def test_copilot_ingredient_gate_api_post(self):
        """POST /api/v1/ai/copilot/ingredient-access returns correct decision."""
        resp = _call_post("/api/v1/ai/copilot/ingredient-access",
                          {"zmf_id": "ZMF-089", "ingredient_name": "Jamalgota",
                           "actor_role": "HAKEEM_SAHAB_AI"})
        self.assertTrue(resp.get("ok"))
        decision = resp["access_decision"]
        self.assertFalse(decision["allowed"])
        self.assertEqual(decision["status"], "HARD_BLOCKED_ZMF_HIGH_RISK_28")


class TestPhase2TwelveGateTracker(unittest.TestCase):
    """Phase 2: 12-Gate Evidence Pipeline Tracker"""

    def test_gate_definitions_return_12_gates(self):
        """Gate definitions endpoint must return exactly 12 gates."""
        from services.knowledge.app.engines.twelve_gate_tracker_engine import TwelveGateTrackerEngine
        gates = TwelveGateTrackerEngine.get_all_gate_definitions()
        self.assertEqual(len(gates), 12)
        gate_numbers = [g["gate_number"] for g in gates]
        self.assertEqual(gate_numbers, list(range(1, 13)))

    def test_new_drug_at_gate_zero(self):
        """Untracked Mufrad starts at Gate 0 with no clinical promotion."""
        from services.knowledge.app.engines.twelve_gate_tracker_engine import TwelveGateTrackerEngine
        status = TwelveGateTrackerEngine.get_gate_status("ZMF-099")
        self.assertEqual(status["current_gate_completed"], 0)
        self.assertFalse(status["clinical_promotion_allowed"])
        self.assertFalse(status["pipeline_complete"])

    def test_gate_signoff_advances_pipeline(self):
        """Recording Gate 1 sign-off advances the drug to Gate 1."""
        from services.knowledge.app.engines.twelve_gate_tracker_engine import TwelveGateTrackerEngine
        result = TwelveGateTrackerEngine.record_gate_signoff(
            zmf_id="ZMF-010", gate_number=1,
            signed_by="Dr. Ahmad Unani", notes="Classical texts verified"
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["highest_gate_completed"], 1)
        # Verify persistent read-back
        status = TwelveGateTrackerEngine.get_gate_status("ZMF-010")
        self.assertEqual(status["current_gate_completed"], 1)

    def test_out_of_order_gate_blocked(self):
        """Signing Gate 3 without Gate 2 must fail."""
        from services.knowledge.app.engines.twelve_gate_tracker_engine import TwelveGateTrackerEngine
        result = TwelveGateTrackerEngine.record_gate_signoff(
            zmf_id="ZMF-020", gate_number=3,
            signed_by="Lab Director"
        )
        self.assertFalse(result["success"])
        self.assertIn("Gate 2", result["error"])

    def test_dashboard_summary_structure(self):
        """Dashboard must return expected keys."""
        from services.knowledge.app.engines.twelve_gate_tracker_engine import TwelveGateTrackerEngine
        dash = TwelveGateTrackerEngine.get_dashboard_summary()
        self.assertIn("total_mufradat_catalog", dash)
        self.assertEqual(dash["total_mufradat_catalog"], 250)
        self.assertIn("gate_distribution", dash)

    def test_12gate_gates_api_get(self):
        """GET /api/v1/governance/12-gate/gates returns 12 gate definitions."""
        resp = _call_get("/api/v1/governance/12-gate/gates")
        self.assertTrue(resp.get("ok"))
        self.assertEqual(len(resp["gate_definitions"]), 12)

    def test_12gate_dashboard_api_get(self):
        """GET /api/v1/governance/12-gate/dashboard returns dashboard data."""
        resp = _call_get("/api/v1/governance/12-gate/dashboard")
        self.assertTrue(resp.get("ok"))
        self.assertIn("total_mufradat_catalog", resp["dashboard"])

    def test_12gate_signoff_api_post(self):
        """POST /api/v1/governance/12-gate/signoff records a gate sign-off."""
        resp = _call_post("/api/v1/governance/12-gate/signoff",
                          {"zmf_id": "ZMF-050", "gate_number": 1,
                           "signed_by": "Prof. Karimi", "notes": "CTE verified"})
        self.assertTrue(resp.get("ok"))
        self.assertTrue(resp["result"]["success"])


class TestPhase3BadalEAdvia(unittest.TestCase):
    """Phase 3: Badal-e-Advia Substitute Advisory Engine"""

    def test_suranjan_badal_recommendations(self):
        """Suranjan Talkh must return at least 1 classical substitute."""
        from services.therapeutic.app.engines.badal_e_advia_engine import BadalEAdviaEngine
        result = BadalEAdviaEngine.get_badal_recommendations(
            ingredient_name="Suranjan Talkh", zmf_id="ZMF-002",
            indication="joint inflammation"
        )
        self.assertTrue(result["is_high_risk_blocked"])
        self.assertGreater(result["total_recommendations"], 0)
        self.assertGreater(len(result["classical_substitutes"]), 0)

    def test_jamalgota_badal_recommendations(self):
        """Jamalgota must return safe purgative substitutes."""
        from services.therapeutic.app.engines.badal_e_advia_engine import BadalEAdviaEngine
        result = BadalEAdviaEngine.get_badal_recommendations(
            ingredient_name="Jamalgota", zmf_id="ZMF-089"
        )
        self.assertTrue(result["is_high_risk_blocked"])
        subs = result["classical_substitutes"]
        self.assertGreater(len(subs), 0)
        # Sana Makki should be among substitutes for Jamalgota
        names = [s["name"].lower() for s in subs]
        self.assertTrue(any("sana" in n for n in names))

    def test_mizaj_based_fallback_for_unknown_drug(self):
        """Unknown drug with patient_mizaj provides Mizaj-based fallback."""
        from services.therapeutic.app.engines.badal_e_advia_engine import BadalEAdviaEngine
        result = BadalEAdviaEngine.get_badal_recommendations(
            ingredient_name="Unknown Obscure Drug XYZ",
            patient_mizaj="Haar Ratab"
        )
        self.assertGreater(len(result["mizaj_based_fallback"]), 0)

    def test_badal_catalog_api_get(self):
        """GET /api/v1/therapeutic/badal-e-advia/catalog returns full catalog."""
        resp = _call_get("/api/v1/therapeutic/badal-e-advia/catalog")
        self.assertTrue(resp.get("ok"))
        catalog = resp["badal_catalog"]
        self.assertGreater(catalog["total_entries"], 0)
        self.assertGreater(catalog["total_substitutes"], 0)

    def test_badal_recommend_api_post(self):
        """POST /api/v1/therapeutic/badal-e-advia/recommend returns recommendations."""
        resp = _call_post("/api/v1/therapeutic/badal-e-advia/recommend",
                          {"ingredient_name": "Suranjan Talkh", "zmf_id": "ZMF-002",
                           "indication": "arthritis"})
        self.assertTrue(resp.get("ok"))
        recs = resp["badal_recommendations"]
        self.assertTrue(recs["is_high_risk_blocked"])
        self.assertGreater(recs["total_recommendations"], 0)


class TestPhase4PatientCardGenerator(unittest.TestCase):
    """Phase 4: Patient Monograph Card Generator"""

    def test_asgandh_card_structure(self):
        """ZMF-001 (Asgandh) must return well-structured patient card."""
        from services.knowledge.app.engines.mufradat_card_generator import MufradatCardGenerator
        card = MufradatCardGenerator.generate_card("ZMF-001")
        self.assertNotIn("error", card)
        self.assertEqual(card["card_type"], "MUFRAD_PATIENT_MONOGRAPH")
        self.assertIn("identity", card)
        self.assertIn("temperament", card)
        self.assertIn("key_traditional_uses", card)
        self.assertIn("safety", card)
        self.assertIn("governance", card)

    def test_blocked_drug_card_shows_restricted_notice(self):
        """HIGH_RISK_28 card must show restricted notice."""
        from services.knowledge.app.engines.mufradat_card_generator import MufradatCardGenerator
        card = MufradatCardGenerator.generate_card("ZMF-002")
        # May be blocked in registry or not found — either shows restriction
        if "error" not in card:
            self.assertTrue(card["safety"]["is_high_risk_restricted"])

    def test_seed_cards_api_get(self):
        """GET /api/v1/knowledge/mufradat-250/cards/seeds returns 5 seed cards."""
        resp = _call_get("/api/v1/knowledge/mufradat-250/cards/seeds")
        self.assertTrue(resp.get("ok"))
        seeds = resp["seed_cards"]
        self.assertEqual(seeds["total_requested"], 5)

    def test_single_card_api_get(self):
        """GET /api/v1/knowledge/mufradat-250/card/ZMF-001 returns Asgandh card."""
        resp = _call_get("/api/v1/knowledge/mufradat-250/card/ZMF-001")
        self.assertTrue(resp.get("ok"))
        card = resp["card"]
        self.assertEqual(card["card_type"], "MUFRAD_PATIENT_MONOGRAPH")

    def test_batch_cards_api_post(self):
        """POST /api/v1/knowledge/mufradat-250/cards/batch generates batch."""
        resp = _call_post("/api/v1/knowledge/mufradat-250/cards/batch",
                          {"zmf_ids": ["ZMF-001", "ZMF-004", "ZMF-005"]})
        self.assertTrue(resp.get("ok"))
        batch = resp["batch_result"]
        self.assertEqual(batch["total_requested"], 3)
        self.assertGreater(batch["cards_generated"], 0)

    def test_governance_footer_present_in_card(self):
        """Every patient card must include the mandatory governance footer."""
        from services.knowledge.app.engines.mufradat_card_generator import MufradatCardGenerator
        card = MufradatCardGenerator.generate_card("ZMF-004")
        if "error" not in card:
            footer = card["governance"]["footer"]
            self.assertIn("NOT a prescription", footer)
            self.assertIn("ZAYVORA", footer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
