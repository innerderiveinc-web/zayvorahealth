import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import (
    ZayvoraApiHandler, get_db,
    _ensure_voice_scribe_table,
    parse_and_structure_voice_consultation,
    get_voice_consultation_history
)


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestVoiceAgenticScribe(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}
        with get_db() as conn:
            _ensure_voice_scribe_table(conn)
            cur = conn.cursor()
            cur.execute("DELETE FROM voice_consultation_sessions WHERE mrn LIKE 'PAT-TEST-%'")
            conn.commit()

    def test_voice_scribe_waja_ul_mafasil_extraction(self):
        """Verifies vernacular Roman Urdu parsing for joint pain and Suranjan posology."""
        transcript = "Mareez ko joron me shadeed dard hai, subah jakdan rehti hai. Balghami mizaj hai. Majun Suranjan 5g subah shaam neem garam doodh se aur Roghan Suranjan local application likhein."
        with get_db() as conn:
            res = parse_and_structure_voice_consultation(transcript=transcript, mrn="PAT-TEST-001", conn=conn)

        self.assertTrue(res["ok"])
        self.assertEqual(res["agent_version"], "v1.0-VoiceAgenticScribe")
        sdata = res["structured_data"]
        self.assertIn("Waja-ul-Mafasil", sdata["chief_complaint"])
        self.assertEqual(sdata["predominant_humor"], "Balgham")
        self.assertEqual(sdata["organ_axis"], "Mafasil-Dam (Musculo-Skeletal)")

        med_names = [m["name"] for m in sdata["extracted_medicines"]]
        self.assertIn("Majun Suranjan Mudabbar", med_names)
        self.assertIn("Roghan Suranjan", med_names)

        suranjan = [m for m in sdata["extracted_medicines"] if m["name"] == "Majun Suranjan Mudabbar"][0]
        self.assertEqual(suranjan["frequency"], "BID")
        self.assertIn("doodh", suranjan["anupan"])

    def test_voice_scribe_zeeq_un_nafs_extraction(self):
        """Verifies vernacular Hindi/Urdu speech parsing for asthma and Banafsha / Sapistan."""
        transcript = "Mareez ko khansi aur saans phoolne ki takleef hai, zeeq-un-nafs balghami hai. Sharbat Banafsha aur Lauq Sapistan lijiye."
        with get_db() as conn:
            res = parse_and_structure_voice_consultation(transcript=transcript, mrn="PAT-TEST-002", conn=conn)

        self.assertTrue(res["ok"])
        sdata = res["structured_data"]
        self.assertIn("Zeeq-un-Nafs", sdata["chief_complaint"])
        self.assertEqual(sdata["organ_axis"], "Riya-Sadr (Respiratory)")

        med_names = [m["name"] for m in sdata["extracted_medicines"]]
        self.assertIn("Sharbat Banafsha", med_names)
        self.assertIn("Lauq Sapistan", med_names)

    def test_http_voice_scribe_endpoints(self):
        """Verifies HTTP POST /api/v1/clinical/agent/voice/transcribe-structure and GET history."""
        # 1. POST transcribe-structure
        self.handler.path = "/api/v1/clinical/agent/voice/transcribe-structure"
        self.handler.rfile = MagicMock()
        payload = json.dumps({
            "mrn": "PAT-TEST-003",
            "transcript": "Pet me gas aur hazme ki kharabi hai, Jawarish Kamuni khana khane ke baad paani se lijiye."
        }).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload)), "Content-Type": "application/json"}
        self.handler.do_POST()

        resp_post = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_post["ok"])
        self.assertEqual(resp_post["agent_version"], "v1.0-VoiceAgenticScribe")
        self.assertIn("Kamuni", resp_post["structured_data"]["extracted_medicines"][0]["name"])

        # 2. GET history
        self.handler.wfile = MockWFile()
        self.handler.path = "/api/v1/clinical/agent/voice/history?mrn=PAT-TEST-003"
        self.handler.do_GET()

        resp_get = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_get["ok"])
        self.assertGreaterEqual(len(resp_get["history"]), 1)


if __name__ == "__main__":
    unittest.main()
