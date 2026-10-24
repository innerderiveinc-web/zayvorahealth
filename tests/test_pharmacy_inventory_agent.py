import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import (
    ZayvoraApiHandler, get_db,
    _ensure_pharmacy_po_table,
    run_pharmacy_inventory_audit,
    authorize_purchase_order
)


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestPharmacyInventoryAgent(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}
        with get_db() as conn:
            _ensure_pharmacy_po_table(conn)
            cur = conn.cursor()
            cur.execute("DELETE FROM purchase_orders WHERE po_number LIKE 'PO-TEST-%'")
            conn.commit()

    def test_run_inventory_audit_and_fefo_grading(self):
        """Verifies autonomous inventory scan, FEFO categorization, and poison firewall."""
        with get_db() as conn:
            res = run_pharmacy_inventory_audit(facility_id="FAC-HQ-01", conn=conn)

        self.assertTrue(res["ok"])
        self.assertEqual(res["agent_version"], "v1.0-PharmacyInventoryAgent")
        self.assertIn("summary", res)
        summary = res["summary"]
        self.assertGreaterEqual(summary["total_active_lots"], 5)
        # Verify expired batch detected
        self.assertGreaterEqual(summary["expired_count"], 1)
        # Verify Mudabbar uncertified toxic batch detected
        self.assertGreaterEqual(summary["mudabbar_poison_firewall_count"], 1)
        # Verify draft purchase orders were autonomously compiled
        self.assertGreaterEqual(summary["draft_pos_generated_count"], 1)

        # Check raw unpurified batch has poison_firewall_blocked = True
        raw_batches = [b for b in res["batches"] if "Raw" in b["name"] or b["id"] == "INV-008"]
        if raw_batches:
            self.assertTrue(raw_batches[0]["poison_firewall_blocked"])
            self.assertFalse(raw_batches[0]["mudabbar_certified"])

    def test_authorize_purchase_order(self):
        """Verifies pharmacist 21 CFR Part 11 electronic authorization of purchase order."""
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO purchase_orders 
                (po_number, vendor_name, sku_or_herb, requested_quantity, unit_of_measure, estimated_cost, reorder_reason, urgency_level, status)
                VALUES ('PO-TEST-001', 'Dehlvi Herbals Lab', 'Majun Suranjan', 100, 'Bottles/Jars', 15000.0, 'Critical Low Stock', 'HIGH', 'DRAFT_GENERATED')
            """)
            conn.commit()

            auth_res = authorize_purchase_order(po_number="PO-TEST-001", authorized_by="PHARM-01", notes="Verified GMP COA", conn=conn)
            self.assertTrue(auth_res["ok"])
            self.assertEqual(auth_res["status"], "AUTHORIZED")
            self.assertEqual(auth_res["authorized_by"], "PHARM-01")

            cur.execute("SELECT status, authorized_by FROM purchase_orders WHERE po_number = 'PO-TEST-001'")
            row = cur.fetchone()
            self.assertEqual(row[0], "AUTHORIZED")
            self.assertEqual(row[1], "PHARM-01")

    def test_http_pharmacy_agent_endpoints(self):
        """Verifies GET /api/v1/pharmacy/agent/inventory-audit and POST /api/v1/pharmacy/agent/authorize-po."""
        # 1. GET audit
        self.handler.path = "/api/v1/pharmacy/agent/inventory-audit?facility_id=FAC-HQ-01"
        self.handler.do_GET()

        resp_get = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_get["ok"])
        self.assertEqual(resp_get["agent_version"], "v1.0-PharmacyInventoryAgent")
        self.assertIn("summary", resp_get)

        # 2. POST authorize-po
        self.handler.wfile = MockWFile()
        self.handler.path = "/api/v1/pharmacy/agent/authorize-po"
        self.handler.rfile = MagicMock()
        payload = json.dumps({
            "po_number": "ALL_DRAFT",
            "authorized_by": "CHIEF-PHARMACIST-IRFAN",
            "notes": "Bulk authorization of autonomous inventory POs"
        }).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload)), "Content-Type": "application/json"}
        self.handler.do_POST()

        resp_post = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_post["ok"])
        self.assertEqual(resp_post["agent_version"], "v1.0-PharmacyInventoryAgent")
        self.assertEqual(resp_post["status"], "AUTHORIZED")


if __name__ == "__main__":
    unittest.main()
