import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import ZayvoraApiHandler, get_db, generate_canonical_evidence_dossier


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestCanonResearchAgent(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}

    def test_direct_dossier_generation_waja_ul_mafasil(self):
        """Verifies multi-step canonical compilation for joint pain."""
        with get_db() as conn:
            dossier = generate_canonical_evidence_dossier("Waja-ul-Mafasil", depth="comprehensive", conn=conn)

        self.assertIn("dossier_id", dossier)
        self.assertTrue(dossier["dossier_id"].startswith("DOS-CANON-2026-"))
        self.assertEqual(dossier["query"], "Waja-ul-Mafasil")
        self.assertGreater(len(dossier["matched_treatises"]), 0)
        self.assertGreater(len(dossier["validated_monographs"]), 0)
        self.assertGreater(len(dossier["phytochemical_crosswalk"]), 0)
        self.assertIn("markdown_content", dossier)
        self.assertIn("Al-Qanun", dossier["markdown_content"])
        self.assertLess(dossier["execution_time_ms"], 100.0)

    def test_direct_dossier_generation_product_sku_zay001(self):
        """Verifies master product SKU resolution and ingredient expansion."""
        with get_db() as conn:
            dossier = generate_canonical_evidence_dossier("ZAY-001", depth="comprehensive", conn=conn)

        self.assertIsNotNone(dossier["matched_product"])
        self.assertEqual(dossier["matched_product"]["sku"], "ZAY-001")
        self.assertEqual(dossier["matched_product"]["organ_axis"], "CEREBROVASCULAR")
        self.assertIn("markdown_content", dossier)

    def test_get_canonical_dossier_endpoint(self):
        """Verifies GET /api/v1/research/agent/canonical-dossier."""
        self.handler.path = "/api/v1/research/agent/canonical-dossier?query=Suranjan"
        self.handler.do_GET()

        resp = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp.get("agent_version"), "v1.0-CanonResearchAgent")
        dossier = resp.get("dossier", {})
        self.assertEqual(dossier.get("query"), "Suranjan")
        self.assertTrue(dossier.get("statutory_safety", {}).get("mudabbar_required"))

    def test_post_canonical_dossier_endpoint(self):
        """Verifies POST /api/v1/research/agent/canonical-dossier."""
        self.handler.path = "/api/v1/research/agent/canonical-dossier"
        self.handler.rfile = MagicMock()
        payload = json.dumps({"query": "Asthma", "depth": "comprehensive"}).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload))}
        self.handler.do_POST()

        resp = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp.get("ok"))
        dossier = resp.get("dossier", {})
        self.assertEqual(dossier.get("query"), "Asthma")
        self.assertGreater(len(dossier.get("phytochemical_crosswalk", [])), 0)


if __name__ == "__main__":
    unittest.main()
