"""
ZAYVORA Health OS™ — Test Suite #59: Validated Murakkab & Nuskha Integration
==============================================================================
Verifies the Phase 9 Canonical Formulation Layer:
  1. Classical Murakkab formula integrity & UPI/NFUM citations.
  2. Ingredient functional roles (Juz-e-Azam, Muawin, Musleh, Badraqa).
  3. Strict AI governance: Schedule E(1) containing compounds are blocked.
  4. Custom Nuskha audit engine against the 60 Validated Monograph catalog.
  5. Live REST API endpoints.
"""
import sys
import os
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.therapeutic.app.engines.validated_murakkab_compiler import (
    ValidatedMurakkabCompiler,
    CLASSICAL_MURAKKABAT_REGISTRY,
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


class TestValidatedMurakkabCompiler(unittest.TestCase):
    """Verifies Classical Murakkabat & Custom Nuskha Auditing."""

    def test_murakkabat_catalog_count(self):
        """Must load classical compound formulations."""
        catalog = ValidatedMurakkabCompiler.list_all_murakkabat()
        self.assertGreaterEqual(len(catalog), 5)
        self.assertEqual(len(catalog), len(CLASSICAL_MURAKKABAT_REGISTRY))

    def test_murakkab_structure_and_ingredient_roles(self):
        """Every Murakkab must define chief drug, supporting, and vehicles."""
        itrifal = ValidatedMurakkabCompiler.get_murakkab("MRK-001")
        self.assertIsNotNone(itrifal)
        self.assertEqual(itrifal["name"], "Itrifal Ustukhuddus")
        self.assertIn("composition", itrifal)
        
        # Verify roles exist in composition
        roles = [c["role"] for c in itrifal["composition"]]
        self.assertTrue(any("Juz-e-Azam" in r for r in roles))
        self.assertTrue(any("Muawin" in r for r in roles))
        self.assertTrue(any("Musleh" in r for r in roles))

    def test_schedule_e1_murakkab_blocked_from_ai(self):
        """Habb-e-Suranjan contains Suranjan Talkh and MUST be AI-blocked."""
        habb_suranjan = ValidatedMurakkabCompiler.get_murakkab("MRK-005")
        self.assertIsNotNone(habb_suranjan)
        self.assertTrue(habb_suranjan["is_schedule_e1_containing"])
        self.assertFalse(habb_suranjan["ai_prescribing_permitted"])
        self.assertEqual(habb_suranjan["governance_status"], "SCHEDULE_E1_RESTRICTED_CLINICIAN_ONLY")

    def test_safe_murakkab_cleared_for_ai(self):
        """Itrifal Ustukhuddus and Jawarish Kamooni must be cleared for AI prescribing."""
        itrifal = ValidatedMurakkabCompiler.get_murakkab("MRK-001")
        jawarish = ValidatedMurakkabCompiler.get_murakkab("MRK-002")
        self.assertFalse(itrifal["is_schedule_e1_containing"])
        self.assertTrue(itrifal["ai_prescribing_permitted"])
        self.assertFalse(jawarish["is_schedule_e1_containing"])
        self.assertTrue(jawarish["ai_prescribing_permitted"])

    def test_audit_clean_nuskha(self):
        """A formula containing verified non-toxic drugs must be approved."""
        res = ValidatedMurakkabCompiler.audit_custom_nuskha(
            "Nuskha-e-Hazim Motadil",
            [
                {"zmf_id": "ZMF-024", "name": "Badiyan", "role": "Juz-e-Azam"},
                {"zmf_id": "ZMF-016", "name": "Zanjabeel", "role": "Muawin"},
                {"zmf_id": "ZMF-020", "name": "Zeera Siyah", "role": "Muawin"},
                {"zmf_id": "ZMF-012", "name": "Ajwain Desi", "role": "Musleh"}
            ]
        )
        self.assertEqual(res["audit_verdict"], "APPROVED_CLINICAL_NUSKHA")
        self.assertTrue(res["ai_autonomous_permitted"])
        self.assertEqual(res["verified_count"], 4)
        self.assertEqual(res["unverified_count"], 0)

    def test_audit_nuskha_with_toxic_poison_rejected(self):
        """A formula containing Suranjan Talkh must be rejected for autonomous AI."""
        res = ValidatedMurakkabCompiler.audit_custom_nuskha(
            "Nuskha-e-Mafasil High-Risk",
            [
                {"zmf_id": "ZMF-002", "name": "Suranjan Talkh", "role": "Juz-e-Azam"},
                {"zmf_id": "ZMF-057", "name": "Haldi", "role": "Muawin"}
            ]
        )
        self.assertEqual(res["audit_verdict"], "REJECTED_FOR_AUTONOMOUS_AI_CONTAINS_SCHEDULE_E1")
        self.assertFalse(res["ai_autonomous_permitted"])
        self.assertEqual(len(res["schedule_e1_detected"]), 1)

    def test_audit_nuskha_with_unverified_ingredient(self):
        """A formula with unknown synthetic/unverified drug must be flagged."""
        res = ValidatedMurakkabCompiler.audit_custom_nuskha(
            "Nuskha Mixed",
            [
                {"zmf_id": "ZMF-001", "name": "Asgandh"},
                {"zmf_id": "UNKNOWN-HERB-999", "name": "Non-Standard Plant Extract"}
            ]
        )
        self.assertEqual(res["audit_verdict"], "PENDING_CONTAINS_UNVERIFIED_INGREDIENTS")
        self.assertFalse(res["ai_autonomous_permitted"])
        self.assertEqual(res["unverified_count"], 1)

    def test_api_get_all_murakkabat(self):
        """GET /api/v1/therapeutic/murakkab-validated/all returns list."""
        resp = _call_get("/api/v1/therapeutic/murakkab-validated/all")
        self.assertTrue(resp.get("ok"))
        self.assertGreaterEqual(resp["total_murakkabat"], 5)

    def test_api_get_single_murakkab(self):
        """GET /api/v1/therapeutic/murakkab-validated/MRK-003 returns Khamira Gaozaban."""
        resp = _call_get("/api/v1/therapeutic/murakkab-validated/MRK-003")
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp["murakkab"]["name"], "Khamira Gaozaban Ambari")

    def test_api_post_audit_nuskha(self):
        """POST /api/v1/therapeutic/murakkab-validated/audit-nuskha performs audit."""
        payload = {
            "nuskha_name": "API Clinical Formulation Test",
            "ingredients": [
                {"zmf_id": "ZMF-004", "name": "Ustukhuddus"},
                {"zmf_id": "ZMF-091", "name": "Amla"},
                {"zmf_id": "ZMF-019", "name": "Kishneez"}
            ]
        }
        resp = _call_post("/api/v1/therapeutic/murakkab-validated/audit-nuskha", payload)
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp["nuskha_audit"]["audit_verdict"], "APPROVED_CLINICAL_NUSKHA")
        self.assertTrue(resp["nuskha_audit"]["ai_autonomous_permitted"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
