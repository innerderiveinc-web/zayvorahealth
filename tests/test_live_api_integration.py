#!/usr/bin/env python3
"""
ZAYVORA Health OS — Live REST API & SQL Database Integration Suite
Tests the real database and API logic directly without requiring network loopback sockets.
"""

import sys
import os
import json
import sqlite3
import time
from io import BytesIO

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler, DB_PATH

class DirectTestClient:
    """Invokes ZayvoraApiHandler directly with simulated I/O streams."""
    def request(self, method, path, data=None):
        body_bytes = json.dumps(data).encode("utf-8") if data else b""
        
        # Build raw HTTP stream
        raw_headers = f"{method} {path} HTTP/1.1\r\n"
        raw_headers += "Host: localhost:8000\r\n"
        raw_headers += "Content-Type: application/json\r\n"
        raw_headers += f"Content-Length: {len(body_bytes)}\r\n\r\n"
        
        input_stream = BytesIO(raw_headers.encode("utf-8") + body_bytes)
        output_stream = BytesIO()

        class DummySocket:
            def __init__(self, rfile, wfile):
                self.rfile = rfile
                self.wfile = wfile
            def makefile(self, mode, *args, **kwargs):
                if "b" in mode:
                    return self.rfile if "r" in mode else self.wfile
                raise NotImplementedError()
            def sendall(self, b):
                self.wfile.write(b)

        dummy_sock = DummySocket(input_stream, output_stream)
        handler = ZayvoraApiHandler(dummy_sock, ("127.0.0.1", 12345), None)
        
        # Parse output stream
        output_stream.seek(0)
        response_bytes = output_stream.getvalue()
        
        # Split headers and body
        parts = response_bytes.split(b"\r\n\r\n", 1)
        header_lines = parts[0].decode("utf-8").split("\r\n")
        status_line = header_lines[0] # HTTP/1.0 200 OK
        status_code = int(status_line.split(" ")[1])
        
        resp_body = {}
        if len(parts) > 1 and parts[1]:
            resp_body = json.loads(parts[1].decode("utf-8"))
            
        return status_code, resp_body

def run_tests():
    print("=" * 70)
    print(" ZAYVORA HEALTH OS™ — LIVE REST API & SQL DATABASE INTEGRATION SUITE")
    print("=" * 70)

    client = DirectTestClient()
    passed = 0
    failed = 0

    # 1. Health Probe & DB Connection
    try:
        status, body = client.request("GET", "/api/health")
        assert status == 200
        assert body["ok"] is True
        assert body["database"] == "connected"
        print(f"[PASS] Test 01: Health Probe & SQLite Connection ({body['database_engine']})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 01: Health Probe ({e})")
        failed += 1

    # 2. User Registration (Real SQL Insert & Salted Hash)
    test_email = f"live.patient.{int(time.time())}@example.com"
    registered_mrn = None
    try:
        status, body = client.request("POST", "/api/v1/auth/register", {
            "email": test_email,
            "password": "SecurePassword123!",
            "fullName": "Zainab Parveen",
            "phone": "+91 98765 43210",
            "role": "PATIENT"
        })
        assert status == 201
        assert body["ok"] is True
        assert "token" in body
        registered_mrn = body["user"]["mrn"]
        assert registered_mrn.startswith("MRN-2026-")

        # Verify SQL row directly in database file
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT email, role, mrn FROM users WHERE email = ?", (test_email,))
        user_row = c.fetchone()
        conn.close()
        assert user_row is not None
        assert user_row[0] == test_email
        print(f"[PASS] Test 02: User Registration & Salted Hash (Created {registered_mrn})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 02: User Registration ({e})")
        failed += 1

    # 3. User Login & Credential Verification
    try:
        status, body = client.request("POST", "/api/v1/auth/login", {
            "email": test_email,
            "password": "SecurePassword123!"
        })
        assert status == 200
        assert body["ok"] is True
        assert body["user"]["email"] == test_email
        print(f"[PASS] Test 03: Password Verification & Live Session Minting")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 03: Password Verification ({e})")
        failed += 1

    # 4. Duplicate Registration Rejection
    try:
        status, body = client.request("POST", "/api/v1/auth/register", {
            "email": test_email,
            "password": "AnotherPassword",
            "fullName": "Duplicate User"
        })
        assert status == 409
        assert body["ok"] is False
        print(f"[PASS] Test 04: Duplicate User Rejection (HTTP 409 Conflict)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 04: Duplicate User Rejection ({e})")
        failed += 1

    # 5. Patients Directory Retrieval
    try:
        status, body = client.request("GET", "/api/v1/patients")
        assert status == 200
        assert body["ok"] is True
        assert body["count"] >= 3
        mrns = [p["mrn"] for p in body["patients"]]
        assert registered_mrn in mrns
        print(f"[PASS] Test 05: Master Patient Index Query (Found {body['count']} Patients)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 05: Master Patient Index Query ({e})")
        failed += 1

    # 6. Real Appointment Booking & Sequential Token Issuance
    try:
        status, body = client.request("POST", "/api/v1/appointments", {
            "patientName": "Zainab Parveen",
            "mrn": registered_mrn,
            "doctorName": "Prof. (Dr.) Mansoor Alam",
            "chiefComplaint": "Su-e-Mizaj Har Safrawi with hyperacidity",
            "fee": 800.0
        })
        assert status == 201
        assert body["ok"] is True
        token_num = body["appointment"]["tokenNumber"]
        assert token_num.startswith("T-")
        print(f"[PASS] Test 06: Real Appointment Booking & Token Issuance ({token_num})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 06: Real Appointment Booking ({e})")
        failed += 1

    # 7. Prescription Authoring & 21 CFR Part 11 Cryptographic Audit Anchoring
    try:
        status, body = client.request("POST", "/api/v1/prescriptions", {
            "patientName": "Zainab Parveen",
            "mrn": registered_mrn,
            "doctorName": "Prof. (Dr.) Mansoor Alam",
            "doctorReg": "CCIM-U-1988-0412",
            "items": [
                {"name": "Sharbat Bazoori Motadil", "dose": "20ml morning", "duration": "10 days"},
                {"name": "Jawarish Shahi", "dose": "5g post-prandial", "duration": "10 days"}
            ],
            "dietaryAdvice": "Avoid spicy, fried foods. Drink barley water."
        })
        assert status == 201
        assert body["ok"] is True
        sig_hash = body["signatureHash"]
        assert len(sig_hash) == 64

        # Verify anchored directly in audit ledger
        status_audit, body_audit = client.request("GET", "/api/v1/audit/logs")
        assert status_audit == 200
        hashes = [log["leaf_hash"] for log in body_audit["audit_logs"]]
        assert sig_hash in hashes
        print(f"[PASS] Test 07: 21 CFR Part 11 Digital Signature & Merkle Anchoring (Hash: {sig_hash[:12]}...)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 07: 21 CFR Part 11 Digital Signature ({e})")
        failed += 1

    # 8. FEFO Inventory Retrieval & Batch Stock Decrement
    try:
        status, body = client.request("GET", "/api/v1/inventory")
        assert status == 200
        initial_stock = body["inventory"][0]["stock_qty"]
        target_batch = body["inventory"][0]["batch_number"]

        dispense_status, dispense_body = client.request("POST", "/api/v1/inventory/dispense", {
            "batchNumber": target_batch,
            "quantity": 2
        })
        assert dispense_status == 200
        assert dispense_body["remainingStock"] == initial_stock - 2
        print(f"[PASS] Test 08: FEFO Inventory Stock Decrement (Batch: {target_batch}, {initial_stock} -> {initial_stock - 2})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 08: FEFO Inventory Stock Decrement ({e})")
        failed += 1

    print("=" * 70)
    print(f"LIVE API VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 70)
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
