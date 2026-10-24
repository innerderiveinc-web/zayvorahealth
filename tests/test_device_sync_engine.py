import unittest
import json
from unittest.mock import MagicMock
from services.live_api_server import (
    ZayvoraApiHandler, get_db,
    _ensure_device_sync_tables,
    process_sync_batch,
    get_sync_delta
)


class MockWFile:
    def __init__(self):
        self.data = b""

    def write(self, b):
        self.data += b


class TestDeviceSyncEngine(unittest.TestCase):
    def setUp(self):
        self.handler = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
        self.handler.wfile = MockWFile()
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.headers = {"Content-Type": "application/json"}
        with get_db() as conn:
            _ensure_device_sync_tables(conn)
            cur = conn.cursor()
            cur.execute("DELETE FROM device_sync_ledger WHERE device_id LIKE 'TEST-DEV-%'")
            conn.commit()

    def test_process_sync_batch_direct(self):
        """Verifies ingestion of offline dirty-queue mutations and patient updates."""
        mutations = [
            {
                "mutationId": "MUT-TEST-001",
                "entityType": "vital_reading",
                "patientId": "PAT-0816",
                "data": {"bp": "128/84", "pulse": 76, "spo2": 99}
            },
            {
                "mutationId": "MUT-TEST-002",
                "entityType": "asbab_sittah",
                "patientId": "PAT-0816",
                "data": {"air_quality": "Moderate", "sleep_hours": 7.5}
            },
            {
                "mutationId": "MUT-TEST-003",
                "entityType": "prescription_acknowledgement",
                "patientId": "PAT-0816",
                "data": {"order_number": "RX-2026-001", "adherence_status": "TAKEN"}
            }
        ]

        with get_db() as conn:
            res = process_sync_batch(device_id="TEST-DEV-01", mutations=mutations, conn=conn)
            self.assertTrue(res["ok"])
            self.assertEqual(res["applied_count"], 3)
            self.assertEqual(res["total_received"], 3)

            # Verify recorded in ledger
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM device_sync_ledger WHERE device_id = 'TEST-DEV-01'")
            self.assertEqual(cur.fetchone()[0], 3)

    def test_get_sync_delta(self):
        """Verifies delta changes retrieval for multi-device cloud synchronization."""
        with get_db() as conn:
            delta = get_sync_delta(device_id="TEST-DEV-01", conn=conn)
            self.assertTrue(delta["ok"])
            self.assertIn("server_time_utc", delta)
            self.assertIsInstance(delta["prescriptions"], list)
            self.assertIsInstance(delta["care_continuity_plans"], list)
            self.assertIsInstance(delta["formulation_preferences"], list)

    def test_http_sync_endpoints(self):
        """Verifies HTTP POST /api/v1/sync/batch and GET /api/v1/sync/delta routes."""
        # 1. POST /api/v1/sync/batch
        self.handler.path = "/api/v1/sync/batch"
        self.handler.rfile = MagicMock()
        payload = json.dumps({
            "device_id": "TEST-DEV-HTTP",
            "mutations": [
                {
                    "mutationId": "MUT-TEST-HTTP-1",
                    "entityType": "vital_reading",
                    "patientId": "PAT-0816",
                    "data": {"bp": "120/80", "pulse": 72}
                }
            ]
        }).encode("utf-8")
        self.handler.rfile.read = MagicMock(return_value=payload)
        self.handler.headers = {"Content-Length": str(len(payload)), "Content-Type": "application/json"}
        self.handler.do_POST()

        resp_post = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_post["ok"])
        self.assertEqual(resp_post["applied_count"], 1)

        # 2. GET /api/v1/sync/delta
        self.handler.wfile = MockWFile()
        self.handler.path = "/api/v1/sync/delta?device_id=TEST-DEV-HTTP"
        self.handler.do_GET()

        resp_get = json.loads(self.handler.wfile.data.decode("utf-8"))
        self.assertTrue(resp_get["ok"])
        self.assertEqual(resp_get["device_id"], "TEST-DEV-HTTP")


if __name__ == "__main__":
    unittest.main()
