import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import (
    ZayvoraApiHandler, get_db,
    _ensure_reinforcement_tables,
    record_clinician_override,
    get_reinforcement_matrix,
    generate_proactive_pre_consult_brief
)


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestReinforcementAgent(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}
        with get_db() as conn:
            _ensure_reinforcement_tables(conn)
            cur = conn.cursor()
            cur.execute("DELETE FROM clinician_feedback_overrides WHERE mrn LIKE 'PAT-TEST-%'")
            cur.execute("DELETE FROM formulation_preference_matrix WHERE organ_axis = 'Test-Axis'")
            conn.commit()

    def test_record_positive_feedback_reinforces_weight(self):
        """Verifies clinician acceptance boosts formulation confidence weight and tracks usage."""
        with get_db() as conn:
            res1 = record_clinician_override(
                mrn="PAT-TEST-001",
                doctor_id="DOC-IRFAN",
                formulation_name="Majun Suranjan",
                ai_proposed_dose="5g BID",
                doctor_prescribed_dose="5g BID",
                action_type="ACCEPTED",
                clinical_rationale="Effective for Waja-ul-Mafasil flare",
                organ_axis="Test-Axis",
                conn=conn
            )
            self.assertTrue(res1["ok"])
            self.assertEqual(res1["updated_confidence_weight"], 1.0)
            self.assertEqual(res1["acceptance_rate_percent"], 100.0)
            self.assertEqual(res1["safety_validation_status"], "VALIDATED_SAFE")

            # Prescribe a second time accepted
            res2 = record_clinician_override(
                mrn="PAT-TEST-002",
                doctor_id="DOC-IRFAN",
                formulation_name="Majun Suranjan",
                ai_proposed_dose="5g BID",
                doctor_prescribed_dose="5g BID",
                action_type="ACCEPTED",
                clinical_rationale="Concur with AI recommendation",
                organ_axis="Test-Axis",
                conn=conn
            )
            self.assertEqual(res2["updated_confidence_weight"], 1.0)
            self.assertEqual(res2["acceptance_rate_percent"], 100.0)

    def test_record_override_penalizes_weight_and_tracks_delta(self):
        """Verifies clinician modification/override reduces confidence weight and logs rationale."""
        with get_db() as conn:
            # First interaction: dose modified
            res1 = record_clinician_override(
                mrn="PAT-TEST-001",
                doctor_id="DOC-IRFAN",
                formulation_name="Sharbat Zanjabeel",
                ai_proposed_dose="15ml BID",
                doctor_prescribed_dose="10ml OD",
                action_type="DOSE_CHANGE",
                clinical_rationale="Lower dose indicated due to mild gastritis",
                organ_axis="Test-Axis",
                conn=conn
            )
            self.assertTrue(res1["ok"])
            self.assertEqual(res1["updated_confidence_weight"], 0.85)
            self.assertEqual(res1["acceptance_rate_percent"], 0.0)

            # Second interaction: again overridden
            res2 = record_clinician_override(
                mrn="PAT-TEST-002",
                doctor_id="DOC-IRFAN",
                formulation_name="Sharbat Zanjabeel",
                ai_proposed_dose="15ml BID",
                doctor_prescribed_dose="5ml OD",
                action_type="DOSE_CHANGE",
                clinical_rationale="Patient intolerant to high ginger concentration",
                organ_axis="Test-Axis",
                conn=conn
            )
            self.assertEqual(res2["updated_confidence_weight"], 0.8)
            self.assertEqual(res2["acceptance_rate_percent"], 0.0)

    def test_upi_safety_ceiling_and_schedule_e1_fail_closed(self):
        """Verifies safety guardrail flags doses exceeding UPI pharmacopoeia ceiling or Schedule E1."""
        with get_db() as conn:
            # Habbe Shifa has 1000mg maximum ceiling and is Schedule E(1)
            res = record_clinician_override(
                mrn="PAT-TEST-003",
                doctor_id="DOC-IRFAN",
                formulation_name="Habbe Shifa",
                ai_proposed_dose="500mg OD",
                doctor_prescribed_dose="2500mg TDS",
                action_type="DOSE_CHANGE",
                clinical_rationale="Severe acute crisis",
                organ_axis="Test-Axis",
                conn=conn
            )
            self.assertEqual(res["safety_validation_status"], "WARNING_EXCEEDS_UPI_CEILING")
            self.assertIn("Schedule E(1)", res["safety_advisory"])
            self.assertIn("exceeds UPI maximum", res["safety_advisory"])

    def test_preference_matrix_query_and_enrichment(self):
        """Verifies matrix ranking and integration into pre-consultation dossier."""
        with get_db() as conn:
            record_clinician_override(
                mrn="PAT-TEST-004", doctor_id="DOC-IRFAN", formulation_name="Jawarish Kamuni",
                ai_proposed_dose="5g BID", doctor_prescribed_dose="5g BID", action_type="ACCEPTED",
                clinical_rationale="Gold standard for Meda", organ_axis="Meda-Amaa (GI System)", conn=conn
            )

            # Query matrix
            matrix = get_reinforcement_matrix(organ_axis="Meda-Amaa", conn=conn)
            self.assertGreaterEqual(len(matrix), 1)
            kamuni = [m for m in matrix if m["formulation_name"] == "Jawarish Kamuni"][0]
            self.assertEqual(kamuni["formulation_name"], "Jawarish Kamuni")
            self.assertGreaterEqual(kamuni["confidence_weight"], 0.8)

            # Verify proactive pre-consult brief enriches suggested_medicines
            brief = generate_proactive_pre_consult_brief(
                mrn="PAT-TEST-004", chief_complaint="Indigestion and bloating in stomach",
                mizaj="Balghami", conn=conn
            )
            suggested = brief["proposed_regimen"]["suggested_medicines"]
            kamuni_in_brief = [m for m in suggested if m["name"] == "Jawarish Kamuni"][0]
            self.assertIn("clinician_badge", kamuni_in_brief)
            self.assertIn("clinician_preference_weight", kamuni_in_brief)

    def test_http_reinforcement_endpoints(self):
        """Verifies HTTP GET and POST routes for ReinforcementAgent."""
        # 1. POST record-override
        self.handler.path = "/api/v1/clinical/agent/reinforcement/record-override"
        self.handler.rfile = MagicMock()
        payload = json.dumps({
            "mrn": "PAT-TEST-005",
            "doctor_id": "DOC-IRFAN",
            "formulation_name": "Majun Falasfa",
            "ai_proposed_dose": "5g OD",
            "doctor_prescribed_dose": "5g BID",
            "action_type": "DOSE_CHANGE",
            "clinical_rationale": "Elderly patient needing kidney tonification",
            "organ_axis": "Kulyah-Masana"
        }).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload)), "Content-Type": "application/json"}
        self.handler.do_POST()

        resp_post = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_post["ok"])
        self.assertEqual(resp_post["agent_version"], "v1.0-ReinforcementAgent")
        self.assertEqual(resp_post["result"]["formulation_name"], "Majun Falasfa")

        # 2. GET matrix
        self.handler.wfile = MockWFile()
        self.handler.path = "/api/v1/clinical/agent/reinforcement/matrix?axis=Kulyah-Masana"
        self.handler.do_GET()

        resp_get = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_get["ok"])
        self.assertEqual(resp_get["agent_version"], "v1.0-ReinforcementAgent")
        self.assertGreaterEqual(len(resp_get["preferences"]), 1)


if __name__ == "__main__":
    unittest.main()
