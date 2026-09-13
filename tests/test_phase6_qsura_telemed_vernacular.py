#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — PHASE 6 QSURA COMMUNICATIONS, TELEMEDICINE & PATIENT PORTAL SUITE
SUITE-15: Comprehensive Automated Integration Verification Harness

Verifies:
1.  QSURA Communication Broker: Approved template catalog retrieval.
2.  QSURA Notification Dispatch: SMS message dispatch & database persistence.
3.  QSURA TRAI DLT Compliance: PHI masking for unencrypted SMS channels.
4.  QSURA Regulatory Consent Gate: Hard stop on unverified patient consent (DISHA/GDPR).
5.  QSURA Validation Gate: Missing template parameter validation.
6.  QSURA RBAC Security Gate: Patient role blocked from broadcast dispatching (HTTP 403).
7.  QSURA Scoped Notification Queries: Patient sees only own records; staff sees facility.
8.  Telemedicine Session Orchestrator: Encrypted WebRTC consultation room creation.
9.  Telemedicine Authorization Gate: Mutual patient MRN session authorization check.
10. Telemedicine Room Lifecycle: Clinical room closure and audit timestamping.
11. Vernacular Audio Posology: Nastaliq Urdu script & Roman transliteration synthesis.
12. Vernacular Audio Posology: Devanagari Hindi script & Roman transliteration synthesis.
13. Vernacular Audio Posology: Mandatory statutory Schedule E(1) Mudabbar caution.
14. Patient Portal Self-Service: Scoped unified record aggregation & boundary protection.
15. Disaster Recovery Continuum: SHA-256 integrity snapshot, RTO/RPO telemetry & zero developer jargon.
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

PROHIBITED_JARGON = [
    "sqlite", "database error", "traceback", "stack trace", "exception in thread",
    "syntax error", "null pointer", "undefined is not a function", "query failed",
    "operationalerror", "integrityerror", "cursor", "unhandled rejection", "500 internal"
]

class DirectTestClient:
    def request(self, method, path, data=None, headers=None):
        body_bytes = json.dumps(data).encode("utf-8") if data is not None else b""
        
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
    print("=" * 78)
    print(" ZAYVORA HEALTH OS™ — PHASE 6 QSURA, TELEMEDICINE & PATIENT PORTAL TEST SUITE")
    print("=" * 78)

    client = DirectTestClient()
    passed = 0
    failed = 0

    # Obtain session tokens for testing
    status, body = client.request("POST", "/api/v1/auth/login", {"email": "admin@zayvora.health", "password": "admin123"})
    admin_token = body.get("token")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "mansoor.alam@zayvora.health", "password": "doctor123"})
    doctor_token = body.get("token")
    doctor_headers = {"Authorization": f"Bearer {doctor_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "hamza.farooqi@gmail.com", "password": "password123"})
    patient1_token = body.get("token")
    patient1_headers = {"Authorization": f"Bearer {patient1_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "bilqees.begum@gmail.com", "password": "password123"})
    patient2_token = body.get("token")
    patient2_headers = {"Authorization": f"Bearer {patient2_token}"}

    # 1. QSURA Approved Template Catalog Retrieval
    try:
        status, res = client.request("GET", "/api/v1/qsura/templates", headers=doctor_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("ok") is True, "Expected ok: True"
        templates = res.get("templates", {})
        assert "APPOINTMENT_CONFIRMATION" in templates, "Missing APPOINTMENT_CONFIRMATION template"
        assert "DISPENSE_READY_NOTIFICATION" in templates, "Missing DISPENSE_READY_NOTIFICATION template"
        assert "MUDABBAR_SAFETY_ADVISORY" in templates, "Missing MUDABBAR_SAFETY_ADVISORY template"
        passed += 1
        print(" [PASS] 01: QSURA Approved Message Template Catalog Retrieval")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 01: QSURA Approved Message Template Catalog Retrieval: {e}")

    # 2. QSURA SMS Notification Dispatch & DB Persistence
    try:
        payload = {
            "channel": "sms",
            "recipient": "+919811044219",
            "message_type": "DISPENSE_READY_NOTIFICATION",
            "parameters": {
                "patient_name": "Hamza Farooqi",
                "batch_number": "MS-2026-LOT4",
                "dosage_summary": "Majun Suranjan 5g nocte"
            },
            "mrn": "MRN-2026-0814",
            "patient_consent_verified": True
        }
        status, res = client.request("POST", "/api/v1/qsura/send", payload, headers=doctor_headers)
        assert status == 201, f"Expected 201, got {status}: {res}"
        assert res.get("ok") is True, "Expected ok: True"
        dispatch = res.get("dispatch", {})
        assert dispatch.get("delivery_status") == "DELIVERED", "Expected DELIVERED status"
        assert "Hamza Farooqi" in dispatch.get("rendered_content", ""), "Rendered content missing patient name"
        
        # Verify persistence in database
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM notifications WHERE notification_id = ?", (dispatch["message_id"],))
            row = cur.fetchone()
            assert row is not None, "Notification record was not persisted in database"

        passed += 1
        print(" [PASS] 02: QSURA Notification Dispatch & Database Persistence")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 02: QSURA Notification Dispatch & Database Persistence: {e}")

    # 3. QSURA TRAI DLT PHI Masking for Unencrypted SMS
    try:
        payload = {
            "channel": "sms",
            "recipient": "+919811044219",
            "message_type": "DISPENSE_READY_NOTIFICATION",
            "parameters": {
                "patient_name": "Hamza Farooqi (Contact: 9811044219)",
                "batch_number": "MS-2026-LOT4",
                "dosage_summary": "Majun Suranjan 5g nocte"
            },
            "patient_consent_verified": True
        }
        status, res = client.request("POST", "/api/v1/qsura/send", payload, headers=doctor_headers)
        assert status == 201, f"Expected 201, got {status}"
        content = res["dispatch"]["rendered_content"]
        assert "98******19" in content, f"Expected masked phone number in SMS content: {content}"
        assert "9811044219" not in content, "Unmasked phone number leaked in SMS content"
        passed += 1
        print(" [PASS] 03: QSURA TRAI DLT PHI Masking for Unencrypted SMS")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 03: QSURA TRAI DLT PHI Masking for Unencrypted SMS: {e}")

    # 4. QSURA Regulatory Consent Hard Stop (DISHA / GDPR)
    try:
        payload = {
            "channel": "sms",
            "recipient": "+919811044219",
            "message_type": "DISPENSE_READY_NOTIFICATION",
            "parameters": {
                "patient_name": "Hamza Farooqi",
                "batch_number": "MS-2026-LOT4",
                "dosage_summary": "5g nocte"
            },
            "patient_consent_verified": False
        }
        status, res = client.request("POST", "/api/v1/qsura/send", payload, headers=doctor_headers)
        assert status == 400, f"Expected 400, got {status}"
        assert res.get("code") == "CONSENT_REQUIRED", f"Expected CONSENT_REQUIRED code: {res}"
        assert "Consent Violation" in res.get("error", ""), "Expected consent violation error message"
        passed += 1
        print(" [PASS] 04: QSURA Regulatory Consent Enforcement Barrier")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 04: QSURA Regulatory Consent Enforcement Barrier: {e}")

    # 5. QSURA Missing Template Parameters Validation
    try:
        payload = {
            "channel": "sms",
            "recipient": "+919811044219",
            "message_type": "DISPENSE_READY_NOTIFICATION",
            "parameters": {
                "patient_name": "Hamza Farooqi"
            },
            "patient_consent_verified": True
        }
        status, res = client.request("POST", "/api/v1/qsura/send", payload, headers=doctor_headers)
        assert status == 400, f"Expected 400, got {status}"
        assert res.get("code") == "MISSING_TEMPLATE_PARAMS", f"Expected MISSING_TEMPLATE_PARAMS code: {res}"
        passed += 1
        print(" [PASS] 05: QSURA Template Parameter Validation Gate")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 05: QSURA Template Parameter Validation Gate: {e}")

    # 6. QSURA RBAC Security Barrier: Patient Role Cannot Dispatch Broadcasts
    try:
        payload = {
            "channel": "sms",
            "recipient": "+919811044219",
            "message_type": "DISPENSE_READY_NOTIFICATION",
            "parameters": {
                "patient_name": "Hamza Farooqi",
                "batch_number": "MS-2026-LOT4",
                "dosage_summary": "5g nocte"
            },
            "patient_consent_verified": True
        }
        status, res = client.request("POST", "/api/v1/qsura/send", payload, headers=patient1_headers)
        assert status == 403, f"Expected 403, got {status}"
        assert res.get("code") == "INSUFFICIENT_PERMISSIONS", f"Expected INSUFFICIENT_PERMISSIONS code: {res}"
        passed += 1
        print(" [PASS] 06: QSURA RBAC Security Barrier (Patient Disallowed)")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 06: QSURA RBAC Security Barrier (Patient Disallowed): {e}")

    # 7. QSURA Scoped Notification Queries
    try:
        # Doctor views facility notifications
        status, res = client.request("GET", "/api/v1/qsura/notifications", headers=doctor_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("ok") is True
        assert res.get("count") >= 1, "Expected at least 1 facility notification"

        # Patient 1 views own notifications
        status, res = client.request("GET", "/api/v1/qsura/notifications", headers=patient1_headers)
        assert status == 200, f"Expected 200, got {status}"
        for n in res.get("notifications", []):
            assert n.get("mrn") == "MRN-2026-0814", f"Patient 1 saw record belonging to another MRN: {n.get('mrn')}"

        passed += 1
        print(" [PASS] 07: QSURA Scoped Notification Queries & Privacy Scoping")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 07: QSURA Scoped Notification Queries & Privacy Scoping: {e}")

    # 8. Telemedicine Encrypted WebRTC Session Creation
    created_room_id = None
    try:
        payload = {
            "mrn": "MRN-2026-0814",
            "patient_name": "Hamza Farooqi",
            "encounter_id": "ENC-001",
            "appointment_id": "APT-104"
        }
        status, res = client.request("POST", "/api/v1/telemedicine/rooms", payload, headers=doctor_headers)
        assert status == 201, f"Expected 201, got {status}: {res}"
        assert res.get("ok") is True
        room = res.get("room", {})
        created_room_id = room.get("room_id")
        assert created_room_id is not None, "Missing room_id"
        assert room.get("status") == "ACTIVE", "Expected status ACTIVE"
        assert room.get("session_token", "").startswith("zyv.tele."), "Invalid session token format"
        assert "ice_servers" in room, "Missing ICE servers configuration"
        assert "webrtc_signaling_url" in room, "Missing WebRTC signaling endpoint"
        passed += 1
        print(" [PASS] 08: Telemedicine WebRTC Encrypted Session Creation")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 08: Telemedicine WebRTC Encrypted Session Creation: {e}")

    # 9. Telemedicine Mutual Patient Authorization Gate
    try:
        assert created_room_id is not None, "Room ID required from test 8"
        # Authorized patient (Hamza Farooqi, MRN-2026-0814) can access room
        status, res = client.request("GET", f"/api/v1/telemedicine/rooms/{created_room_id}", headers=patient1_headers)
        assert status == 200, f"Expected 200 for authorized patient, got {status}"
        assert res.get("room", {}).get("room_id") == created_room_id

        # Unauthorized patient (Bilqees Begum, MRN-2026-0901) is strictly forbidden (HTTP 403)
        status, res = client.request("GET", f"/api/v1/telemedicine/rooms/{created_room_id}", headers=patient2_headers)
        assert status == 403, f"Expected 403 for unauthorized cross-patient access, got {status}"
        assert res.get("code") == "UNAUTHORIZED_ROOM_ACCESS", f"Expected UNAUTHORIZED_ROOM_ACCESS, got {res}"
        passed += 1
        print(" [PASS] 09: Telemedicine Mutual Patient Authorization Gate")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 09: Telemedicine Mutual Patient Authorization Gate: {e}")

    # 10. Telemedicine Room Closure Lifecycle
    try:
        assert created_room_id is not None, "Room ID required from test 8"
        status, res = client.request("POST", f"/api/v1/telemedicine/rooms/{created_room_id}/close", headers=doctor_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("status") == "CLOSED", f"Expected status CLOSED, got {res.get('status')}"

        # Verify in DB
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT status, closed_at FROM telemedicine_rooms WHERE room_id = ?", (created_room_id,))
            row = cur.fetchone()
            assert row is not None
            assert row[0] == "CLOSED", f"Expected CLOSED in DB, got {row[0]}"
            assert row[1] is not None, "Expected closed_at timestamp"

        passed += 1
        print(" [PASS] 10: Telemedicine Consultation Room Close Lifecycle")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 10: Telemedicine Consultation Room Close Lifecycle: {e}")

    # 11. Vernacular Audio Posology: Nastaliq Urdu Script & Roman Urdu Synthesis
    try:
        payload = {
            "language": "ur",
            "medication_name": "Majun Suranjan",
            "dosage": "5g",
            "patient_name": "Hamza Farooqi"
        }
        status, res = client.request("POST", "/api/v1/patient/posology/voice", payload, headers=patient1_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("ok") is True
        assert res.get("language") == "ur"
        assert "خوراک" in res.get("script", ""), "Urdu script missing expected Urdu terminology"
        assert "khorak" in res.get("transliteration", "").lower(), "Roman Urdu transliteration missing"
        assert "audio" in res, "Missing audio payload"
        assert res["audio"]["mime_type"] == "audio/mp3", "Invalid audio mime type"
        passed += 1
        print(" [PASS] 11: Vernacular Audio Posology: Nastaliq Urdu & Roman Transliteration")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 11: Vernacular Audio Posology: Nastaliq Urdu & Roman Transliteration: {e}")

    # 12. Vernacular Audio Posology: Devanagari Hindi Script & Roman Hindi Synthesis
    try:
        payload = {
            "language": "hi",
            "medication_name": "Itrifal Kishneezi",
            "dosage": "6g",
            "patient_name": "Hamza Farooqi"
        }
        status, res = client.request("POST", "/api/v1/patient/posology/voice", payload, headers=patient1_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("ok") is True
        assert res.get("language") == "hi"
        assert "खुराक" in res.get("script", ""), "Hindi script missing expected Devanagari terminology"
        assert "khurak" in res.get("transliteration", "").lower(), "Roman Hindi transliteration missing"
        assert "audio" in res, "Missing audio payload"
        passed += 1
        print(" [PASS] 12: Vernacular Audio Posology: Devanagari Hindi & Roman Transliteration")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 12: Vernacular Audio Posology: Devanagari Hindi & Roman Transliteration: {e}")

    # 13. Vernacular Audio Posology: Statutory Schedule E(1) Mudabbar Caution
    try:
        payload = {
            "language": "ur",
            "medication_name": "Majun Suranjan Mudabbar",
            "dosage": "5g"
        }
        status, res = client.request("POST", "/api/v1/patient/posology/voice", payload, headers=doctor_headers)
        assert status == 200, f"Expected 200, got {status}"
        warning = res.get("schedule_e1_warning")
        assert warning is not None, "Missing statutory Schedule E(1) Mudabbar safety caution"
        assert "تنبیہ" in warning, "Expected Urdu cautionary warning prefix"
        assert res["audio"]["duration_seconds"] > 8.0, "Expected extended duration for safety warning"
        passed += 1
        print(" [PASS] 13: Vernacular Audio Posology: Schedule E(1) Mudabbar Safety Gate")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 13: Vernacular Audio Posology: Schedule E(1) Mudabbar Safety Gate: {e}")

    # 14. Patient Portal Self-Service: Scoped Unified Record Aggregation
    try:
        # Patient 1 requests own records
        status, res = client.request("GET", "/api/v1/patient/my-records", headers=patient1_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("ok") is True
        assert res.get("mrn") == "MRN-2026-0814"
        assert "patient" in res, "Missing patient demographics"
        assert "appointments" in res, "Missing appointments"
        assert "prescriptions" in res, "Missing prescriptions"
        assert "encounters" in res, "Missing encounters"
        assert "invoices" in res, "Missing invoices"
        assert "telemedicine_rooms" in res, "Missing telemedicine rooms"
        assert "notifications" in res, "Missing notifications"

        # Patient 1 attempts to request Patient 2's MRN -> Strictly Forbidden (HTTP 403)
        status, res = client.request("GET", "/api/v1/patient/my-records?mrn=MRN-2026-0901", headers=patient1_headers)
        assert status == 403, f"Expected 403 for unauthorized MRN query, got {status}"
        assert res.get("code") == "PATIENT_PORTAL_ACCESS_VIOLATION", f"Expected PATIENT_PORTAL_ACCESS_VIOLATION, got {res}"

        passed += 1
        print(" [PASS] 14: Patient Portal Self-Service: Aggregation & Boundary Protection")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 14: Patient Portal Self-Service: Aggregation & Boundary Protection: {e}")

    # 15. Disaster Recovery Snapshot, RTO/RPO Telemetry & Zero Developer Jargon
    try:
        status, res = client.request("POST", "/api/v1/dr/snapshot", headers=admin_headers)
        assert status == 201, f"Expected 201, got {status}: {res}"
        assert res.get("ok") is True
        snap = res.get("snapshot", {})
        assert len(snap.get("database_sha256", "")) == 64, "Missing valid SHA-256 hash"
        assert snap.get("integrity_verified") is True, "Integrity verification failed"
        assert snap.get("table_counts", {}).get("patients", 0) > 0, "Zero patients in table count"

        status, res = client.request("GET", "/api/v1/dr/status", headers=admin_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("status") == "HEALTHY", f"Expected HEALTHY status, got {res.get('status')}"
        assert res.get("rto_target_minutes") <= 15, "RTO target exceeds 15 minutes"
        assert res.get("rpo_target_minutes") <= 5, "RPO target exceeds 5 minutes"
        assert res.get("zero_data_loss_guarantee") is True

        res_str = json.dumps(res).lower()
        for jargon in PROHIBITED_JARGON:
            assert jargon not in res_str, f"Prohibited developer jargon detected: '{jargon}'"

        passed += 1
        print(" [PASS] 15: Disaster Recovery Continuum & Zero Developer Jargon Compliance")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 15: Disaster Recovery Continuum & Zero Developer Jargon Compliance: {e}")

    print("=" * 78)
    print(f" PHASE 6 INTEGRATION RESULTS: {passed} PASSED | {failed} FAILED (TOTAL 15)")
    print("=" * 78)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
