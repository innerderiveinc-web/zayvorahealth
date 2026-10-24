import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import (
    ZayvoraApiHandler, get_db,
    get_care_continuity_status,
    evaluate_care_continuity_nujz,
    transition_care_continuity_stage
)


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestCareContinuityAgent(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM care_continuity_plans WHERE mrn LIKE 'PAT-TEST-%'")
            conn.commit()

    def test_direct_plan_status_and_defaults(self):
        """Verifies initial plan status generation and schema."""
        with get_db() as conn:
            plan = get_care_continuity_status("PAT-TEST-001", conn=conn)

        self.assertTrue(plan["ok"])
        self.assertEqual(plan["mrn"], "PAT-TEST-001")
        self.assertEqual(plan["current_phase"], "PHASE_1_MUNZIJ")
        self.assertEqual(plan["target_munzij_days"], 7)
        self.assertIn("nujz_index_percent", plan)
        self.assertFalse(plan["doctor_action_required"])

    def test_evaluate_nujz_progression_and_threshold(self):
        """Verifies Alamat-e-Nujz concoction evaluation and threshold trigger."""
        with get_db() as conn:
            # 1. Day 2: Incomplete concoction (Raw humor)
            res_day2 = evaluate_care_continuity_nujz(
                mrn="PAT-TEST-001", day=2, adherence_confirmed=True,
                qaroorah_sediment="clear_watery", bowel_regular=False,
                pulse_quality="batee", stiffness_resolved_pct=15,
                tongue_clearing=False, conn=conn
            )
            self.assertTrue(res_day2["ok"])
            self.assertFalse(res_day2["nujz_reached"])
            self.assertEqual(res_day2["clinical_action"], "CONTINUE_PHASE_1_MUNZIJ")
            self.assertFalse(res_day2["doctor_task_created"])

            # 2. Day 6: Complete concoction (Rasub-e-Mahmood + Matched Pulse)
            res_day6 = evaluate_care_continuity_nujz(
                mrn="PAT-TEST-001", day=6, adherence_confirmed=True,
                qaroorah_sediment="rasub_mahmood", bowel_regular=True,
                pulse_quality="mutadil", stiffness_resolved_pct=85,
                tongue_clearing=True, conn=conn
            )
            self.assertTrue(res_day6["ok"])
            self.assertTrue(res_day6["nujz_reached"])
            self.assertGreaterEqual(res_day6["nujz_index_percent"], 80.0)
            self.assertEqual(res_day6["clinical_action"], "AUTHORIZE_PHASE_2_MUSHIL")

    def test_transition_stage(self):
        """Verifies clinician 21 CFR Part 11 sign-off for phase transition."""
        with get_db() as conn:
            trans = transition_care_continuity_stage(
                mrn="PAT-TEST-001", target_phase="PHASE_2_TANQIYA",
                doctor_id="DOC-IRFAN", notes="Authorized Tanqiya after verified Nujz.", conn=conn
            )
            self.assertTrue(trans["ok"])
            self.assertEqual(trans["transitioned_phase"], "PHASE_2_TANQIYA")
            self.assertEqual(trans["authorized_by"], "DOC-IRFAN")

            status = get_care_continuity_status("PAT-TEST-001", conn=conn)
            self.assertEqual(status["current_phase"], "PHASE_2_TANQIYA")
            self.assertFalse(status["doctor_action_required"])

    def test_http_care_continuity_endpoints(self):
        """Verifies GET and POST HTTP endpoints for CareContinuityAgent."""
        # 1. GET status
        self.handler.path = "/api/v1/clinical/agent/care-continuity/status?mrn=PAT-TEST-001"
        self.handler.do_GET()
        resp_get = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_get["ok"])
        self.assertEqual(resp_get["agent_version"], "v1.0-CareContinuityAgent")

        # 2. POST evaluate
        self.handler.wfile = MockWFile()
        self.handler.path = "/api/v1/clinical/agent/care-continuity/evaluate-nujz"
        self.handler.rfile = MagicMock()
        payload = json.dumps({
            "mrn": "PAT-TEST-001",
            "day": 6,
            "qaroorah_sediment": "rasub_mahmood",
            "bowel_regular": True,
            "pulse_quality": "mutadil",
            "stiffness_resolved_pct": 80,
            "tongue_clearing": True
        }).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.do_POST()
        resp_post = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_post["ok"])
        self.assertTrue(resp_post["evaluation"]["nujz_reached"])


if __name__ == "__main__":
    unittest.main()
