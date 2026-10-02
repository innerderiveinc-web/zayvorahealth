"""
ZAYVORA Health OS™ — Test Suite #58: 25-Drug Gold Benchmark Validation
========================================================================
Verifies the 10-Phase Canonical & Evidence Architecture across the
25-drug curated gold benchmark batch.
"""
import sys
import os
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.data.mufradat_gold_batch_monographs import (
    GoldBenchmarkRegistry,
    GOLD_BENCHMARK_25_MONOGRAPHS,
    ValidationState,
    AIPermission,
)
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


class TestMufradatGoldBenchmark(unittest.TestCase):
    """Verifies the 25-Drug Gold Benchmark Dataset and Governance Engine."""

    def test_total_gold_monographs_count(self):
        """Must load all 350 curated core matab monographs (100% complete catalog)."""
        self.assertGreaterEqual(len(GOLD_BENCHMARK_25_MONOGRAPHS), 60)
        self.assertEqual(len(GOLD_BENCHMARK_25_MONOGRAPHS), 350)
        drugs = GoldBenchmarkRegistry.list_gold_drugs()
        self.assertEqual(len(drugs), 350)


    def test_monograph_ten_phase_schema_completeness(self):
        """Every monograph in the 25 batch must contain all 10 architectural layers."""
        required_keys = [
            "zmf_id",
            "category",
            "canonical_identity",
            "primary_unani_citations",
            "classical_profile",
            "pharmacopoeial_crosswalk",
            "pharmacognosy_qc",
            "modern_evidence",
            "safety_firewall",
            "organ_axis_affinity",
            "murakkab_roles",
            "governance",
        ]
        for zmf_id, mono in GOLD_BENCHMARK_25_MONOGRAPHS.items():
            for key in required_keys:
                self.assertIn(key, mono, f"Missing key '{key}' in monograph {zmf_id}")

    def test_primary_unani_citations_structure(self):
        """Every drug must have at least one primary source citation with volume and page."""
        for zmf_id, mono in GOLD_BENCHMARK_25_MONOGRAPHS.items():
            citations = mono["primary_unani_citations"]
            self.assertGreater(len(citations), 0, f"No citations for {zmf_id}")
            for cit in citations:
                self.assertIn("source", cit)
                self.assertIn("volume", cit)
                self.assertIn("page", cit)
                self.assertIn("original_text_snippet", cit)
                self.assertEqual(cit["status"], "VERIFIED")

    def test_schedule_e1_poisons_hard_blocked(self):
        """Suranjan Talkh, Jamalgota, Kuchla, Bhilawa, Afeem, Bhang, Seemab, Hartal Warqi must be hard-blocked."""
        e1_ids = ["ZMF-002", "ZMF-089", "ZMF-090", "ZMF-130", "ZMF-191", "ZMF-192", "ZMF-103", "ZMF-102"]
        for zmf_id in e1_ids:
            res = GoldBenchmarkRegistry.evaluate_ai_safety_gate(zmf_id)
            self.assertFalse(res["ai_permitted"], f"{zmf_id} should NOT be AI permitted")
            self.assertEqual(res["status"], "HARD_BLOCKED_SCHEDULE_E1")

    def test_approved_drugs_cleared_for_ai(self):
        """Non-toxic approved drugs like Asgandh, Haldi, Amla, Mulethi must be AI-cleared."""
        approved_ids = ["ZMF-001", "ZMF-057", "ZMF-091", "ZMF-096", "ZMF-013"]
        for zmf_id in approved_ids:
            res = GoldBenchmarkRegistry.evaluate_ai_safety_gate(zmf_id)
            self.assertTrue(res["ai_permitted"], f"{zmf_id} should be AI permitted")
            self.assertEqual(res["status"], "APPROVED_CLINICAL_KNOWLEDGE")

    def test_synonym_disambiguation_asaroon_vs_tagar(self):
        """Asaroon (ZMF-014) and Tagar (ZMF-015) must be recognized as distinct botanical entities."""
        asaroon = GoldBenchmarkRegistry.get_monograph("ZMF-014")
        tagar = GoldBenchmarkRegistry.get_monograph("ZMF-015")
        self.assertIsNotNone(asaroon)
        self.assertIsNotNone(tagar)
        self.assertIn("Asarum europaeum", asaroon["canonical_identity"]["botanical_name"])
        self.assertIn("Valeriana jatamansi", tagar["canonical_identity"]["botanical_name"])
        self.assertNotEqual(asaroon["canonical_identity"]["family"], tagar["canonical_identity"]["family"])

    def test_synonym_disambiguation_filfil_siyah_vs_daraz(self):
        """Filfil Siyah (ZMF-005) and Filfil Daraz (ZMF-027) must be separate species."""
        siyah = GoldBenchmarkRegistry.get_monograph("ZMF-005")
        daraz = GoldBenchmarkRegistry.get_monograph("ZMF-027")
        self.assertIn("Piper nigrum", siyah["canonical_identity"]["botanical_name"])
        self.assertIn("Piper longum", daraz["canonical_identity"]["botanical_name"])

    def test_api_get_all_gold_drugs(self):
        """GET /api/v1/knowledge/mufradat-gold/all must return all validated gold drugs (350)."""
        resp = _call_get("/api/v1/knowledge/mufradat-gold/all")
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp["total_gold_drugs"], 350)
        self.assertEqual(len(resp["drugs"]), 350)




    def test_api_get_single_gold_monograph(self):
        """GET /api/v1/knowledge/mufradat-gold/ZMF-001 must return full Asgandh monograph."""
        resp = _call_get("/api/v1/knowledge/mufradat-gold/ZMF-001")
        self.assertTrue(resp.get("ok"))
        mono = resp["monograph"]
        self.assertEqual(mono["zmf_id"], "ZMF-001")
        self.assertIn("canonical_identity", mono)
        self.assertEqual(mono["canonical_identity"]["canonical_unani_name"], "Asgandh")

    def test_api_post_safety_gate_evaluation(self):
        """POST /api/v1/governance/mufradat-gold/ai-safety-gate evaluates safety gate."""
        # Test 1: Poison blocked
        resp_poison = _call_post("/api/v1/governance/mufradat-gold/ai-safety-gate", {"zmf_id": "ZMF-089"})
        self.assertTrue(resp_poison.get("ok"))
        self.assertFalse(resp_poison["safety_gate_evaluation"]["ai_permitted"])
        self.assertEqual(resp_poison["safety_gate_evaluation"]["status"], "HARD_BLOCKED_SCHEDULE_E1")

        # Test 2: Safe drug passed
        resp_safe = _call_post("/api/v1/governance/mufradat-gold/ai-safety-gate", {"zmf_id": "ZMF-001"})
        self.assertTrue(resp_safe.get("ok"))
        self.assertTrue(resp_safe["safety_gate_evaluation"]["ai_permitted"])
        self.assertEqual(resp_safe["safety_gate_evaluation"]["status"], "APPROVED_CLINICAL_KNOWLEDGE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
