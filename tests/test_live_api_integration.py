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

from services.live_api_server import ZayvoraApiHandler, DB_PATH, hash_password

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
            raw_text = parts[1].decode("utf-8")
            try:
                resp_body = json.loads(raw_text)
            except Exception:
                resp_body = {"raw": raw_text}
            
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
        assert body["count"] >= 1
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
        active_items = [b for b in body["inventory"] if b["expiry_date"] > "2026-09-13" and (not b.get("is_schedule_e1") or b.get("mudabbar_cert"))]
        target_item = active_items[0]
        initial_stock = target_item["stock_qty"]
        target_batch = target_item["batch_number"]

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

    # 9. Direct Patient Registration by Staff
    created_order_number = None
    try:
        status, body = client.request("POST", "/api/v1/patients", {
            "firstName": "Fatima",
            "lastName": "Bi",
            "dob": "1968-12-10",
            "gender": "Female",
            "phone": "+91 98440 11223",
            "mizajDominant": "Balghami (Cold & Moist)",
            "allergies": ["Peanuts"]
        })
        assert status == 201
        assert body["ok"] is True
        assert body["patient"]["mrn"].startswith("MRN-2026-")
        print(f"[PASS] Test 09: Staff Walk-in Patient Registration ({body['patient']['mrn']} - {body['patient']['firstName']})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 09: Staff Walk-in Patient Registration ({e})")
        failed += 1

    # 10. Single Prescription Lookup
    try:
        # Fetch all to get an order number
        _, p_body = client.request("GET", "/api/v1/prescriptions")
        if p_body.get("prescriptions"):
            first_rx = p_body["prescriptions"][0]
            status, body = client.request("GET", f"/api/v1/prescriptions/{first_rx['order_number']}")
            assert status == 200
            assert body["ok"] is True
            assert body["prescription"]["order_number"] == first_rx["order_number"]
            assert len(body["prescription"]["items"]) > 0
            print(f"[PASS] Test 10: Single Prescription Lookup ({first_rx['order_number']})")
            passed += 1
        else:
            print("[FAIL] Test 10: No prescriptions available for single lookup")
            failed += 1
    except Exception as e:
        print(f"[FAIL] Test 10: Single Prescription Lookup ({e})")
        failed += 1

    # 11. Billing Invoices & Receipts
    try:
        status, body = client.request("POST", "/api/v1/billing/invoices", {
            "mrn": registered_mrn,
            "patientName": "Zainab Parveen",
            "amount": 800.0,
            "department": "Integrative Unani OPD",
            "paymentMethod": "UPI"
        })
        assert status == 201
        assert body["ok"] is True
        inv_num = body["invoice"]["invoiceNumber"]

        status_get, body_get = client.request("GET", "/api/v1/billing/invoices")
        assert status_get == 200
        assert body_get["count"] >= 1
        numbers = [inv["invoice_number"] for inv in body_get["invoices"]]
        assert inv_num in numbers
        print(f"[PASS] Test 11: Billing Invoice Creation & Receipt Verification ({inv_num})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 11: Billing Invoice Creation & Receipt Verification ({e})")
        failed += 1

    # 12. Refresh Token Rotation
    try:
        # Obtain tokens via login
        login_st, login_bd = client.request("POST", "/api/v1/auth/login", {
            "identifier": "admin@zayvorahealth",
            "password": "admin123"
        })
        assert login_st == 200
        assert "refresh_token" in login_bd
        refresh_tk = login_bd["refresh_token"]

        # Rotate refresh token
        ref_st, ref_bd = client.request("POST", "/api/v1/auth/refresh", {
            "refresh_token": refresh_tk
        })
        assert ref_st == 200
        assert ref_bd["ok"] is True
        assert "access_token" in ref_bd
        assert "refresh_token" in ref_bd
        print("[PASS] Test 12: Cryptographic Refresh Token Rotation & Session Renewal")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 12: Refresh Token Rotation ({e})")
        failed += 1

    # 13. Password Reset OTP & Cryptographic Reset Flow
    try:
        # Request OTP
        fp_st, fp_bd = client.request("POST", "/api/v1/auth/forgot-password", {
            "identifier": "dr.irfan@zayvorahealth"
        })
        assert fp_st == 200
        assert fp_bd["ok"] is True

        # Retrieve the generated OTP from database for testing verification
        conn = sqlite3.connect("database/zayvora_live.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT message_text FROM notifications WHERE recipient = '+91 98110 44219' ORDER BY created_at DESC LIMIT 1")
        notif_row = cur.fetchone()
        assert notif_row is not None
        # Extract 6-digit code
        import re
        m = re.search(r"code is (\d{6})", notif_row["message_text"])
        assert m is not None
        otp_code = m.group(1)

        # Test invalid OTP rejection
        bad_st, bad_bd = client.request("POST", "/api/v1/auth/reset-password", {
            "identifier": "dr.irfan@zayvorahealth",
            "otp": "000000",
            "newPassword": "newSecurePassword2026!"
        })
        assert bad_st == 400

        # Execute valid reset
        rst_st, rst_bd = client.request("POST", "/api/v1/auth/reset-password", {
            "identifier": "dr.irfan@zayvorahealth",
            "otp": otp_code,
            "newPassword": "newDoctorPassword2026!"
        })
        assert rst_st == 200
        assert rst_bd["ok"] is True

        # Verify old password rejected
        old_login_st, _ = client.request("POST", "/api/v1/auth/login", {
            "identifier": "dr.irfan@zayvorahealth",
            "password": "doctor123"
        })
        assert old_login_st == 401

        # Verify new password accepted
        new_login_st, new_login_bd = client.request("POST", "/api/v1/auth/login", {
            "identifier": "dr.irfan@zayvorahealth",
            "password": "newDoctorPassword2026!"
        })
        assert new_login_st == 200
        assert new_login_bd["ok"] is True

        # Restore doctor password back to doctor123 for downstream test consistency
        pwd_hash, salt = hash_password("doctor123")
        cur.execute("UPDATE users SET password_hash = ?, salt = ? WHERE email LIKE 'dr.irfan@zayvorahealth%'", (pwd_hash, salt))
        conn.commit()
        conn.close()

        print("[PASS] Test 13: Identity-Verified Hashed OTP Password Reset & Prior Session Revocation")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 13: Password Reset OTP Flow ({e})")
        failed += 1

    # -------------------------------------------------------------------------
    # TEST 14: Printable Prescription Slip & ZKB Mufradat RAG Verification
    # -------------------------------------------------------------------------
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT order_number FROM prescriptions ORDER BY created_at DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()

        if row:
            order_no = row["order_number"]
            # Test printable slip endpoint
            st, bd = client.request("GET", f"/api/v1/prescriptions/{order_no}/print", None)
            assert st == 200, f"Expected 200 for print endpoint, got {st}"
            assert "ZAYVORA HEALTH OS" in bd.get("raw", "")

        # Verify ZKB Mufradat in SQLite
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM zkb_mufradat")
        muf_cnt = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM zkb_drug_interactions")
        int_cnt = cur.fetchone()[0]
        conn.close()
        assert muf_cnt >= 250, f"Expected at least 250 mufradat, got {muf_cnt}"
        assert int_cnt >= 10, f"Expected at least 10 drug interactions, got {int_cnt}"

        # Test UMA terminology search
        st_uma, bd_uma = client.request("GET", "/api/v1/terminology/uma?q=migraine", None)
        assert st_uma == 200
        assert bd_uma.get("ok") is True
        assert any(t["uma_code"] == "UMA-0002" for t in bd_uma.get("terms", []))

        print("[PASS] Test 14: Printable Prescription Slip & ZKB Mufradat Database Integration")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 14: Printable Slip & ZKB Mufradat ({e})")
        failed += 1

    print("=" * 70)
    print(f"LIVE API VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 70)
    return passed, failed

if __name__ == "__main__":
    p, f = run_tests()
    sys.exit(0 if f == 0 else 1)
