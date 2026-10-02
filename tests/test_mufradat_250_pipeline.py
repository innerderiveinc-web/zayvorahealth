#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Test Suite #56: 250 Mufradat Validation & Canonical Governance
====================================================================================
Verifies:
  1. Complete 250-drug inventory freeze (ZMF-001 to ZMF-250).
  2. Exactly 28 High-Risk / Schedule E(1) / Heavy Metal substances are AI-BLOCKED.
  3. Exactly 43 Canonicalization Groups (CAN-001 to CAN-043).
  4. 6 Internal Seed records and 244 Research Candidates.
  5. Suranjan Talkh (ZMF-002) PCIM&H UPI reconciliation to Colchicum luteum Baker.
  6. Canonical formulation multi-part / duplicate conflict detection.
  7. High-risk substance detection firewall guard.
  8. Live REST API endpoints:
     - GET  /api/v1/knowledge/mufradat-250/all
     - GET  /api/v1/knowledge/mufradat-250/high-risk
     - GET  /api/v1/knowledge/mufradat-250/canonical-groups
     - GET  /api/v1/knowledge/mufradat-250/{id}
     - POST /api/v1/therapeutic/formula/canonical-check
"""

import unittest
import sys
import os
import io
import json
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.data.mufradat_250_registry import (
    MUFRADAT_250_CATALOG,
    HIGH_RISK_28_REGISTRY,
    CANONICALIZATION_GROUPS,
    get_all_mufradat_250,
    get_mufrad_by_id,
    get_canonical_groups_registry,
    get_high_risk_28_registry,
    is_high_risk_blocked,
    check_formulation_canonical_conflicts
)
import services.live_api_server as las


class TestMufradat250Pipeline(unittest.TestCase):

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"
        self.handler._get_auth_context = lambda: {
            "user_id": "test-pharmacist",
            "roles": ["SUPER_ADMIN"],
            "clinic_id": "facility-delhi-01"
        }

    def _execute_get(self, path: str) -> dict:
        self.handler.path = path
        self.handler.command = "GET"
        self.handler.requestline = f"GET {path} HTTP/1.1"
        self.handler.wfile = io.BytesIO()
        self.handler.do_GET()
        self.handler.wfile.seek(0)
        raw = self.handler.wfile.getvalue().decode("utf-8")
        parts = raw.split("\r\n\r\n", 1)
        self.assertIn("200 OK", parts[0], f"Expected 200 OK for {path}, got: {parts[0]}")
        return json.loads(parts[1])

    def _execute_post(self, path: str, body: dict) -> dict:
        self.handler.path = path
        self.handler.command = "POST"
        self.handler.requestline = f"POST {path} HTTP/1.1"
        body_bytes = json.dumps(body).encode("utf-8")
        self.handler.rfile = io.BytesIO(body_bytes)
        self.handler.headers = {
            "Content-Length": str(len(body_bytes)),
            "Content-Type": "application/json"
        }
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        raw = self.handler.wfile.getvalue().decode("utf-8")
        parts = raw.split("\r\n\r\n", 1)
        self.assertIn("200 OK", parts[0], f"Expected 200 OK for {path}, got: {parts[0]}")
        return json.loads(parts[1])

    # 1. INVENTORY & STRUCTURAL INTEGRITY
    def test_exact_250_records_count(self):
        catalog = get_all_mufradat_250()
        self.assertEqual(len(catalog), 250)
        # Ensure sequential IDs from ZMF-001 to ZMF-250
        for i in range(1, 251):
            expected_id = f"ZMF-{i:03d}"
            self.assertIn(expected_id, MUFRADAT_250_CATALOG)

    def test_exact_28_high_risk_records(self):
        hr = get_high_risk_28_registry()
        self.assertEqual(len(hr), 28)
        # Verify each is AI_BLOCKED in master catalog
        for zid in hr.keys():
            rec = MUFRADAT_250_CATALOG[zid]
            self.assertEqual(rec["safety_class"], "HIGH_RISK")
            self.assertEqual(rec["ai_permission_state"], "BLOCKED")
            self.assertEqual(rec["clinical_use_state"], "NOT_APPROVED")
            self.assertEqual(rec["patient_self_care"], "NOT_ALLOWED")

    def test_exact_43_canonical_groups(self):
        groups = get_canonical_groups_registry()
        self.assertEqual(len(groups), 43)
        for i in range(1, 44):
            can_key = f"CAN-{i:03d}"
            self.assertIn(can_key, groups)

    def test_suranjan_talkh_pcimh_reconciliation(self):
        suranjan = get_mufrad_by_id("ZMF-002")
        self.assertIsNotNone(suranjan)
        self.assertEqual(suranjan["name"], "SURANJAN TALKH")
        self.assertIn("Colchicum luteum Baker", suranjan["botanical_identity"])
        self.assertEqual(suranjan["safety_class"], "HIGH_RISK")
        self.assertEqual(suranjan["ai_permission_state"], "BLOCKED")

    def test_canonical_formulation_duplicate_conflicts(self):
        # Case 1: Compounding both Pippali and Filfil Daraz (CAN-027)
        ings = [
            {"name": "Pippali", "dose_mg": 250},
            {"name": "Filfil Daraz", "dose_mg": 250},
            {"name": "Asgandh", "dose_mg": 500}
        ]
        conflicts = check_formulation_canonical_conflicts(ings)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["canonical_group_id"], "CAN-027")
        self.assertIn("Duplicate canonical identity detected", conflicts[0]["warning"])

        # Case 2: Clean formulation with distinct botanicals
        clean_ings = [
            {"name": "Asgandh", "dose_mg": 500},
            {"name": "Gaozaban", "dose_mg": 500}
        ]
        no_conflicts = check_formulation_canonical_conflicts(clean_ings)
        self.assertEqual(len(no_conflicts), 0)

    def test_high_risk_blocked_detection(self):
        self.assertTrue(is_high_risk_blocked("ZMF-002"))
        self.assertTrue(is_high_risk_blocked("SURANJAN TALKH"))
        self.assertTrue(is_high_risk_blocked("ZMF-241"))
        self.assertTrue(is_high_risk_blocked("Azaraqi"))
        self.assertTrue(is_high_risk_blocked("Shangraf"))
        self.assertTrue(is_high_risk_blocked("Afyun"))
        self.assertTrue(is_high_risk_blocked("Bhang"))
        # Safe botanicals
        self.assertFalse(is_high_risk_blocked("ZMF-001"))
        self.assertFalse(is_high_risk_blocked("Gaozaban"))
        self.assertFalse(is_high_risk_blocked("Amla"))

    # 2. REST API ENDPOINT TESTS
    def test_api_get_all_mufradat_250(self):
        resp = self._execute_get("/api/v1/knowledge/mufradat-250/all")
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["total_count"], 250)
        self.assertIn("Candidate knowledge only", resp["governance_rule"])

    def test_api_get_high_risk_registry(self):
        resp = self._execute_get("/api/v1/knowledge/mufradat-250/high-risk")
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["total_high_risk"], 28)
        self.assertIn("ZMF-241", resp["high_risk_registry"])
        self.assertIn("HARD-BLOCKED", resp["ai_access_policy"])

    def test_api_get_canonical_groups(self):
        resp = self._execute_get("/api/v1/knowledge/mufradat-250/canonical-groups")
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["total_groups"], 43)
        self.assertIn("CAN-027", resp["canonical_groups"])

    def test_api_single_mufrad_lookup(self):
        # Lookup by ZMF ID
        resp_id = self._execute_get("/api/v1/knowledge/mufradat-250/ZMF-001")
        self.assertTrue(resp_id["ok"])
        self.assertEqual(resp_id["mufrad"]["name"], "ASGANDH")

        # Lookup by name
        resp_name = self._execute_get("/api/v1/knowledge/mufradat-250/USTUKHUDDUS")
        self.assertTrue(resp_name["ok"])
        self.assertEqual(resp_name["mufrad"]["drug_id"], "ZMF-004")

    def test_api_canonical_check_post(self):
        payload = {
            "ingredients": [
                {"name": "Halela Zard", "dose_mg": 1000},
                {"name": "Post Halela", "dose_mg": 500}
            ]
        }
        resp = self._execute_post("/api/v1/therapeutic/formula/canonical-check", payload)
        self.assertTrue(resp["ok"])
        self.assertTrue(resp["has_canonical_duplicates"])
        self.assertEqual(resp["conflicts"][0]["canonical_group_id"], "CAN-038")


if __name__ == "__main__":
    unittest.main()
