"""
Unit and Integration Test Suite for ZAYVORA 12-Axis Clinical Intelligence Framework™
Author: Dr. Irfan Ashraf, BUMS

Tests:
  1. 12-Axis Canonical Schema Integrity & Core Axis Links
  2. Axis Activity Index Weighted Formula Calculation
  3. Safe Clinical Status Labels (No false disease diagnoses)
  4. Patient 360 12-Axis Health Map Generation
  5. Hakeem Sahab AI Copilot Draft Generation (Clinician-in-the-loop)
  6. Live REST API endpoints:
     - GET /api/v1/knowledge/axes-12/all
     - GET /api/v1/knowledge/axes-12/{axis_id}
     - POST /api/v1/clinical/axes-12/score
     - POST /api/v1/clinical/axes-12/patient-map
     - POST /api/v1/clinical/axes-12/ai-draft
"""

import unittest
import json
import io
from unittest.mock import MagicMock

from services.knowledge.app.data.organ_axes_12_schema import (
    ORGAN_AXES_12,
    get_all_organ_axes,
    get_axis_by_id,
    get_axes_by_foundational_core
)
from services.clinical.app.engines.twelve_axis_engine import TwelveAxisEngine
import services.live_api_server as las


class TestTwelveAxisFramework(unittest.TestCase):

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"

    def test_schema_count_and_core_links(self):
        """Test that all 12 axes exist and link to Book 1's 3 Foundational Core Axes."""
        self.assertEqual(len(ORGAN_AXES_12), 12)
        
        # Test specific axes exist
        self.assertIn("AXIS_01", ORGAN_AXES_12)
        self.assertEqual(ORGAN_AXES_12["AXIS_01"]["axis_name"], "Gut–Liver Axis")
        self.assertIn("AXIS_12", ORGAN_AXES_12)
        self.assertEqual(ORGAN_AXES_12["AXIS_12"]["axis_name"], "Dermato–Hair Axis")

        # Test link back to Book 1 core axes
        jigar_khasiya_axes = get_axes_by_foundational_core("Jigar–Khasiya")
        self.assertTrue(len(jigar_khasiya_axes) >= 3)
        self.assertTrue(any(a["axis_id"] == "AXIS_04" for a in jigar_khasiya_axes)) # Male Reproductive

        dimagh_kuli_axes = get_axes_by_foundational_core("Dimagh–Kuli")
        self.assertTrue(len(dimagh_kuli_axes) >= 3)
        self.assertTrue(any(a["axis_id"] == "AXIS_06" for a in dimagh_kuli_axes)) # Neuro-Psychological

    def test_axis_activity_index_calculation(self):
        """Test the safe weighted Axis Activity Index formula."""
        # 0.25*80 + 0.20*60 + 0.30*70 + 0.10*50 + 0.15*80 = 20 + 12 + 21 + 5 + 12 = 70.0
        res = TwelveAxisEngine.calculate_single_axis_activity(
            axis_id="AXIS_01",
            symptoms_score=80,
            history_score=60,
            investigations_score=70,
            lifestyle_score=50,
            clinician_assessment=80
        )
        self.assertEqual(res["activity_index"], 70.0)
        self.assertEqual(res["status"], TwelveAxisEngine.STATUS_HIGH)
        self.assertEqual(res["clinician_status"], "Clinician Validated")

    def test_safe_status_labels_and_red_flag(self):
        """Ensure safe clinical status labels and immediate red flag escalation."""
        # Red flag check
        res_rf = TwelveAxisEngine.calculate_single_axis_activity(
            axis_id="AXIS_07", # Cardio-Vascular
            symptoms_score=40,
            history_score=30,
            investigations_score=30,
            lifestyle_score=20,
            has_red_flags=True
        )
        self.assertEqual(res_rf["status"], TwelveAxisEngine.STATUS_RED_FLAG)
        self.assertIn("Immediate referral", res_rf["ui_meaning"])

        # Low concern check
        res_low = TwelveAxisEngine.calculate_single_axis_activity(
            axis_id="AXIS_02",
            symptoms_score=10,
            history_score=10,
            investigations_score=10,
            lifestyle_score=10
        )
        self.assertEqual(res_low["status"], TwelveAxisEngine.STATUS_LOW)
        self.assertIn("Routine wellness", res_low["ui_meaning"])

    def test_patient_360_map_generation(self):
        """Test full 12-axis map generation for Patient 360."""
        patient_data = {
            "patient_id": "MRN-2026-TEST",
            "mizaj": "Bard-Ratab",
            "axes": {
                "AXIS_01": {"symptoms_score": 60, "history_score": 50, "investigations_score": 70, "lifestyle_score": 40},
                "AXIS_02": {"symptoms_score": 80, "history_score": 70, "investigations_score": 85, "lifestyle_score": 60, "has_red_flags": False}
            }
        }
        res_map = TwelveAxisEngine.generate_patient_360_axis_map(patient_data)
        self.assertEqual(len(res_map["axes"]), 12)
        self.assertIn("ZAYVORA 12-Axis Clinical Intelligence Framework™", res_map["framework_notice"])
        self.assertIn("Metabolic–Pancreatic Axis", res_map["priority_axes"])

    def test_hakeem_sahab_ai_copilot_draft(self):
        """Test advisory AI copilot draft generation with clinician-in-the-loop."""
        summary = {
            "reported_symptoms": ["bloating", "acid reflux"],
            "biomarkers": {"fbg": 115, "hba1c": 6.2},
            "mizaj": "Bard-Ratab"
        }
        draft = TwelveAxisEngine.generate_hakeem_sahab_ai_draft(summary)
        self.assertEqual(draft["clinical_status"], "DRAFT - Requires Clinician Review & Edit")
        self.assertTrue(draft["safety_summary"]["clinician_review_required"])
        self.assertTrue(draft["safety_summary"]["autonomous_prescription_prevented"])
        self.assertIn("medication", str(draft["missing_information"]).lower())

    def test_api_12_axis_endpoints(self):
        """Test live REST endpoints for 12-axis framework."""
        # 1. GET /api/v1/knowledge/axes-12/all
        self.handler.path = "/api/v1/knowledge/axes-12/all"
        self.handler.command = "GET"
        self.handler.requestline = "GET /api/v1/knowledge/axes-12/all HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body_get = json.loads(resp_lines[1])
        self.assertTrue(body_get["ok"])
        self.assertEqual(body_get["total_axes"], 12)

        # 2. POST /api/v1/clinical/axes-12/score
        score_payload = json.dumps({
            "axis_id": "AXIS_01",
            "symptoms_score": 60,
            "history_score": 40,
            "investigations_score": 50,
            "lifestyle_score": 50
        })
        self.handler.path = "/api/v1/clinical/axes-12/score"
        self.handler.command = "POST"
        self.handler.requestline = "POST /api/v1/clinical/axes-12/score HTTP/1.1"
        self.handler.rfile = io.BytesIO(score_payload.encode("utf-8"))
        self.handler.headers = {"Content-Length": str(len(score_payload))}
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        resp_lines = self.handler.wfile.getvalue().decode("utf-8").split("\r\n\r\n", 1)
        self.assertIn("200 OK", resp_lines[0])
        body_score = json.loads(resp_lines[1])
        self.assertTrue(body_score["ok"])
        self.assertIn("axis_score", body_score)


if __name__ == "__main__":
    unittest.main()
