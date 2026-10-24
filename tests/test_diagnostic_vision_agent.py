import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import (
    ZayvoraApiHandler, get_db,
    _ensure_diagnostic_vision_table,
    analyze_diagnostic_media,
    get_diagnostic_vision_analyses,
    generate_proactive_pre_consult_brief
)


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestDiagnosticVisionAgent(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}
        with get_db() as conn:
            _ensure_diagnostic_vision_table(conn)
            cur = conn.cursor()
            cur.execute("DELETE FROM diagnostic_vision_analyses WHERE mrn LIKE 'PAT-TEST-%'")
            conn.commit()

    def test_tongue_vision_analysis(self):
        """Verifies tongue photo inspection, chromatic coating, and humoral inference."""
        with get_db() as conn:
            res = analyze_diagnostic_media(
                mrn="PAT-TEST-001", modality="TONGUE", raw_filename="tongue_coating.png", conn=conn
            )

        self.assertTrue(res["ok"])
        self.assertEqual(res["agent_version"], "v1.0-DiagnosticVisionAgent")
        self.assertEqual(res["modality"], "TONGUE")
        self.assertIn("chromatic_analysis", res)
        self.assertIn("humoral_markers", res)
        self.assertEqual(res["humoral_markers"]["predominant_humor"], "Balgham")
        self.assertTrue(res["humoral_markers"]["teeth_marks_present"])
        self.assertGreaterEqual(res["confidence_score"], 0.9)

    def test_qaroorah_urine_vision_analysis(self):
        """Verifies urine vial inspection, Rasub-e-Mahmood concoction sediment layer."""
        with get_db() as conn:
            res = analyze_diagnostic_media(
                mrn="PAT-TEST-002", modality="QAROORAH_URINE", raw_filename="urine_sample_day6.png", conn=conn
            )

        self.assertTrue(res["ok"])
        self.assertEqual(res["modality"], "QAROORAH_URINE")
        self.assertIn("Rasub-e-Mahmood", res["humoral_markers"]["sediment_type"])
        self.assertEqual(res["humoral_markers"]["concoction_status"], "NUJZ_ACHIEVED")
        self.assertGreaterEqual(res["humoral_markers"]["nujz_index_contribution"], 80.0)

    def test_lab_report_ocr_vision_analysis(self):
        """Verifies lab pathology report OCR, uric acid and ESR extraction."""
        with get_db() as conn:
            res = analyze_diagnostic_media(
                mrn="PAT-TEST-003", modality="LAB_REPORT", raw_filename="cbc_kft_report.pdf", conn=conn
            )

        self.assertTrue(res["ok"])
        self.assertEqual(res["modality"], "LAB_REPORT")
        biomarkers = res["extracted_biomarkers"]
        self.assertIn("serum_uric_acid", biomarkers)
        self.assertEqual(biomarkers["serum_uric_acid"]["value"], 7.8)
        self.assertEqual(biomarkers["serum_uric_acid"]["status"], "ELEVATED")
        self.assertEqual(biomarkers["erythrocyte_sedimentation_rate_esr"]["status"], "HIGH")

    def test_pre_consult_brief_vision_enrichment(self):
        """Verifies proactive pre-consult brief attaches vision diagnostic findings."""
        with get_db() as conn:
            analyze_diagnostic_media(
                mrn="PAT-TEST-004", modality="TONGUE", raw_filename="lisan_photo.png", conn=conn
            )
            brief = generate_proactive_pre_consult_brief(
                mrn="PAT-TEST-004", chief_complaint="Knee joint pain and stiffness",
                mizaj="Balghami", conn=conn
            )

        self.assertIn("vision_diagnostics", brief)
        self.assertGreaterEqual(len(brief["vision_diagnostics"]), 1)
        self.assertEqual(brief["vision_diagnostics"][0]["modality"], "TONGUE")
        self.assertIn("impression", brief["vision_diagnostics"][0])

    def test_http_vision_agent_endpoints(self):
        """Verifies HTTP POST /api/v1/clinical/agent/vision/analyze and GET history."""
        # 1. POST analyze
        self.handler.path = "/api/v1/clinical/agent/vision/analyze"
        self.handler.rfile = MagicMock()
        payload = json.dumps({
            "mrn": "PAT-TEST-005",
            "modality": "TONGUE",
            "file_name": "clinical_lisan.png"
        }).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload)), "Content-Type": "application/json"}
        self.handler.do_POST()

        resp_post = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_post["ok"])
        self.assertEqual(resp_post["agent_version"], "v1.0-DiagnosticVisionAgent")
        self.assertEqual(resp_post["modality"], "TONGUE")

        # 2. GET history
        self.handler.wfile = MockWFile()
        self.handler.path = "/api/v1/clinical/agent/vision/analyses?mrn=PAT-TEST-005"
        self.handler.do_GET()

        resp_get = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_get["ok"])
        self.assertGreaterEqual(len(resp_get["analyses"]), 1)


if __name__ == "__main__":
    unittest.main()
