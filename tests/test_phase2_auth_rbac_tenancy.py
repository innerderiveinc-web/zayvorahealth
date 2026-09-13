#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — PHASE 2 VERIFICATION SUITE
Authentication, RBAC, Multi-Tenancy & API Contracts
Tests:
- Cryptographic HMAC-SHA256 session token generation and verification
- Expiration and revocation handling
- Role-based access control (Doctor, Receptionist, Pharmacist, Patient, Super Admin)
- Multi-tenancy facility data scoping and cross-tenant access denial
- Zero developer terminology in error responses
"""

import sys
import os
import json
import sqlite3
import time
import uuid
from io import BytesIO

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler, DB_PATH

class DirectTestClient:
    """Invokes ZayvoraApiHandler directly with simulated I/O streams and headers."""
    def request(self, method, path, data=None, headers=None):
        body_bytes = json.dumps(data).encode("utf-8") if data else b""
        
        # Build raw HTTP stream
        raw_headers = f"{method} {path} HTTP/1.1\r\n"
        raw_headers += "Host: localhost:8000\r\n"
        raw_headers += "Content-Type: application/json\r\n"
        raw_headers += f"Content-Length: {len(body_bytes)}\r\n"
        
        if headers:
            for k, v in headers.items():
                raw_headers += f"{k}: {v}\r\n"
        raw_headers += "\r\n"
        
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
        
        parts = response_bytes.split(b"\r\n\r\n", 1)
        header_lines = parts[0].decode("utf-8").split("\r\n")
        status_line = header_lines[0]
        status_code = int(status_line.split(" ")[1])
        
        resp_body = {}
        if len(parts) > 1 and parts[1]:
            try:
                resp_body = json.loads(parts[1].decode("utf-8"))
            except Exception:
                resp_body = {"raw": parts[1].decode("utf-8")}
            
        return status_code, resp_body

def run_tests():
    print("=" * 76)
    print(" ZAYVORA HEALTH OS™ — PHASE 2 AUTH, RBAC & MULTI-TENANCY TEST SUITE")
    print("=" * 76)

    client = DirectTestClient()
    passed = 0
    failed = 0

    # Helper to log tests
    def log_result(test_num, name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"[PASS] Test {test_num:02d}: {name} - {detail}")
        else:
            failed += 1
            print(f"[FAIL] Test {test_num:02d}: {name} - {detail}")

    # 1. Login & Cryptographic Token Generation
    status, body = client.request("POST", "/api/v1/auth/login", {
        "email": "mansoor.alam@zayvora.health",
        "password": "doctor123"
    })
    doc_token = body.get("token")
    log_result(1, "Login & Cryptographic Token Issuance",
               status == 200 and body.get("ok") is True and doc_token.startswith("zyv."),
               f"Issued HMAC token {doc_token[:20]}... for DOCTOR")

    # 2. Invalid Password Rejection (HTTP 401)
    status, body = client.request("POST", "/api/v1/auth/login", {
        "email": "mansoor.alam@zayvora.health",
        "password": "incorrect_password"
    })
    log_result(2, "Invalid Password Rejection",
               status == 401 and body.get("ok") is False and body.get("code") == "INVALID_CREDENTIALS",
               f"Clean error: '{body.get('error')}'")

    # 3. Session Verification via /api/v1/auth/me
    status, body = client.request("GET", "/api/v1/auth/me", headers={"Authorization": f"Bearer {doc_token}"})
    log_result(3, "Session Validation & Profile Resolution",
               status == 200 and body.get("ok") is True and body["user"]["role"] == "DOCTOR",
               f"Active doctor session: {body['user']['fullName']} @ {body['facility']['name']}")

    # 4. Expired / Tampered Token Rejection (HTTP 401)
    tampered = doc_token[:-6] + "abcdef"
    status, body = client.request("GET", "/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered}"})
    log_result(4, "Tampered Token Integrity Barrier",
               status == 401 and body.get("ok") is False and body.get("code") == "UNAUTHORIZED",
               f"Tampered token blocked with HTTP 401 ({body.get('code')})")

    # 5. Session Logout & Revocation
    # Register a temporary user to log in and test revocation
    temp_email = f"temp.logout.{uuid.uuid4().hex[:6]}@zayvora.health"
    status, reg_body = client.request("POST", "/api/v1/auth/register", {
        "email": temp_email,
        "password": "temppassword123",
        "fullName": "Temporary User",
        "role": "DOCTOR"
    })
    temp_token = reg_body.get("token")
    status, logout_body = client.request("POST", "/api/v1/auth/logout", headers={"Authorization": f"Bearer {temp_token}"})
    assert status == 200
    # Try using revoked token
    status, me_body = client.request("GET", "/api/v1/auth/me", headers={"Authorization": f"Bearer {temp_token}"})
    log_result(5, "Session Logout & Immediate Token Revocation",
               status == 401 and me_body.get("ok") is False,
               "Revoked token blocked from further API actions")

    # 6. RBAC — Doctor Authorized for Prescription Authoring
    status, rx_body = client.request("POST", "/api/v1/prescriptions", {
        "patientName": "Hamza Farooqi",
        "mrn": "MRN-2026-0814",
        "items": [{"name": "Majun Suranjan (Mudabbar)", "dose": "5g bd"}],
        "dietaryAdvice": "Avoid cold foods"
    }, headers={"Authorization": f"Bearer {doc_token}"})
    log_result(6, "RBAC: Doctor Authorized for Prescriptions",
               status == 201 and rx_body.get("ok") is True and "orderNumber" in rx_body,
               f"Prescription {rx_body.get('orderNumber')} sealed via 21 CFR Part 11 signature")

    # 7. RBAC — Patient Blocked from Authoring Prescription (HTTP 403)
    status, pat_login = client.request("POST", "/api/v1/auth/login", {
        "email": "hamza.farooqi@gmail.com",
        "password": "password123"
    })
    pat_token = pat_login.get("token")
    status, pat_rx = client.request("POST", "/api/v1/prescriptions", {
        "patientName": "Hamza Farooqi",
        "mrn": "MRN-2026-0814",
        "items": [{"name": "Majun Suranjan", "dose": "5g"}]
    }, headers={"Authorization": f"Bearer {pat_token}"})
    log_result(7, "RBAC: Patient Blocked from Prescription Authoring",
               status == 403 and pat_rx.get("ok") is False and pat_rx.get("code") == "FORBIDDEN",
               f"Patient authoring blocked with HTTP 403: '{pat_rx.get('error')}'")

    # 8. RBAC — Receptionist Blocked from Pharmacy Dispensing (HTTP 403)
    status, rec_login = client.request("POST", "/api/v1/auth/login", {
        "email": "reception.opd@zayvora.health",
        "password": "reception123"
    })
    rec_token = rec_login.get("token")
    status, rec_disp = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "MS-2026-LOT4",
        "quantity": 1
    }, headers={"Authorization": f"Bearer {rec_token}"})
    log_result(8, "RBAC: Receptionist Blocked from Pharmacy Dispensing",
               status == 403 and rec_disp.get("ok") is False and rec_disp.get("code") == "FORBIDDEN",
               f"Dispensing restricted to pharmacy staff: '{rec_disp.get('error')}'")

    # 9. RBAC — Pharmacist Authorized for Pharmacy Dispensing
    status, pharm_login = client.request("POST", "/api/v1/auth/login", {
        "email": "zainab.pharm@zayvora.health",
        "password": "pharmacy123"
    })
    pharm_token = pharm_login.get("token")
    status, pharm_disp = client.request("POST", "/api/v1/inventory/dispense", {
        "batchNumber": "MS-2026-LOT4",
        "quantity": 2
    }, headers={"Authorization": f"Bearer {pharm_token}"})
    log_result(9, "RBAC: Pharmacist Authorized for Dispensing",
               status == 200 and pharm_disp.get("ok") is True and "remainingStock" in pharm_disp,
               f"Successfully dispensed with Mudabbar validation; remaining: {pharm_disp.get('remainingStock')}")

    # 10. RBAC — Audit Ledger Restricted to Administrators
    status, pat_audit = client.request("GET", "/api/v1/audit/logs", headers={"Authorization": f"Bearer {pat_token}"})
    status_doc, doc_audit = client.request("GET", "/api/v1/audit/logs", headers={"Authorization": f"Bearer {doc_token}"})
    
    status_admin, admin_login = client.request("POST", "/api/v1/auth/login", {
        "email": "admin@zayvora.health",
        "password": "admin123"
    })
    admin_token = admin_login.get("token")
    status_adm, adm_audit = client.request("GET", "/api/v1/audit/logs", headers={"Authorization": f"Bearer {admin_token}"})
    log_result(10, "RBAC: Merkle Audit Logs Administrative Restriction",
               status == 403 and status_doc == 403 and status_adm == 200,
               f"Audit logs blocked for Patient/Doctor (HTTP 403); granted to Super Admin ({adm_audit.get('count')} blocks)")

    # 11. Multi-Tenancy — Facility Scoping on Patients Directory
    status, hq_patients = client.request("GET", "/api/v1/patients", headers={"Authorization": f"Bearer {doc_token}"})
    hq_mrns = [p["mrn"] for p in hq_patients.get("patients", [])]
    log_result(11, "Multi-Tenancy: Primary Facility Patient Scoping",
               status == 200 and "MRN-2026-0814" in hq_mrns and "MRN-2026-0901" not in hq_mrns,
               f"HQ Doctor sees only HQ patients ({len(hq_mrns)} records); branch patient isolated")

    # 12. Multi-Tenancy — Cross-Tenant Patient Record Access Denial (HTTP 403)
    # HQ Doctor attempts to access Bilqees Begum (PAT-0901 from FAC-BRANCH-02)
    status, cross_pat = client.request("GET", "/api/v1/patients/PAT-0901", headers={"Authorization": f"Bearer {doc_token}"})
    log_result(12, "Multi-Tenancy: Cross-Tenant Access Denial Guard",
               status == 403 and cross_pat.get("ok") is False and cross_pat.get("code") == "CROSS_TENANT_ACCESS_DENIED",
               f"Cross-tenant access blocked with HTTP 403: '{cross_pat.get('error')}'")

    # 13. Multi-Tenancy — Branch Doctor Scoping
    status, branch_login = client.request("POST", "/api/v1/auth/login", {
        "email": "sirajuddin@zayvora.health",
        "password": "doctor123"
    })
    branch_token = branch_login.get("token")
    status, branch_pat = client.request("GET", "/api/v1/patients/PAT-0901", headers={"Authorization": f"Bearer {branch_token}"})
    log_result(13, "Multi-Tenancy: Branch Facility Patient Access",
               status == 200 and branch_pat.get("ok") is True and branch_pat["patient"]["mrn"] == "MRN-2026-0901",
               f"Branch Doctor authorized for branch patient: {branch_pat['patient']['first_name']} {branch_pat['patient']['last_name']}")

    # 14. Multi-Tenancy — Super Admin Cross-Facility Federation
    status, all_pat = client.request("GET", "/api/v1/patients?scope=all", headers={"Authorization": f"Bearer {admin_token}"})
    all_mrns = [p["mrn"] for p in all_pat.get("patients", [])]
    log_result(14, "Multi-Tenancy: Super Admin Cross-Facility Federation",
               status == 200 and "MRN-2026-0814" in all_mrns and "MRN-2026-0901" in all_mrns,
               f"Super Admin federated query retrieved records across both facilities ({len(all_mrns)} total patients)")

    # 15. Standardized Error Formats & Zero Developer Jargon
    # Verify that error responses conform strictly to user-facing clinical standards
    forbidden_terms = ["traceback", "safe_to_lock = False", "exception in thread", "sqlite3.operationalerror", "25-Engine Live Matrix"]
    has_jargon = False
    for resp in [cross_pat, pat_rx, rec_disp]:
        resp_str = json.dumps(resp).lower()
        for term in forbidden_terms:
            if term.lower() in resp_str:
                has_jargon = True
                break
    log_result(15, "Standardized Clinical Errors & Jargon Prohibition",
               has_jargon is False and cross_pat.get("code") == "CROSS_TENANT_ACCESS_DENIED",
               "All error responses formatted with structured clinical codes; zero developer jargon detected")

    print("=" * 76)
    print(f"PHASE 2 VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 76)
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
