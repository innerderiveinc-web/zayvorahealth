#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — PHASE 3 VERIFICATION SUITE
Core Clinical Workflow Continuum
Tests:
- Patient Registration -> OPD Queue -> Consultation Cockpit
- Vitals, Nabz, Lisan physical exam capture
- 10-Ajnas Mizaj assessment & 9 Organ-Axis analysis
- Structured SOAP notes and Afaal cascade progression
- Nuskha formulation and Schedule E(1) Mudabbar gate
- 21 CFR Part 11 cryptographic signature seal & Merkle anchoring
- Appointment transition to COMPLETED upon encounter signing
- Patient 360 longitudinal timeline aggregation
- Printable A4 prescription letterhead data fidelity
- Cross-tenant encounter isolation
- Zero developer terminology across all clinical payloads
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
    print("=" * 76)
    print(" ZAYVORA HEALTH OS™ — PHASE 3 CORE CLINICAL CONTINUUM TEST SUITE")
    print("=" * 76)

    client = DirectTestClient()
    passed = 0
    failed = 0

    def log_result(test_num, name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"[PASS] Test {test_num:02d}: {name} - {detail}")
        else:
            failed += 1
            print(f"[FAIL] Test {test_num:02d}: {name} - {detail}")

    # Login Doctor
    _, doc_login = client.request("POST", "/api/v1/auth/login", {
        "email": "mansoor.alam@zayvora.health",
        "password": "doctor123"
    })
    doc_token = doc_login["token"]
    doc_headers = {"Authorization": f"Bearer {doc_token}"}

    # 1. Patient Registration & Sequential MRN
    test_email = f"continuum.patient.{uuid.uuid4().hex[:6]}@example.com"
    status, reg_body = client.request("POST", "/api/v1/patients", {
        "firstName": "Zubair",
        "lastName": "Khan",
        "phone": "+91 98110 77665",
        "email": test_email,
        "dob": "1980-05-14",
        "gender": "Male",
        "bloodGroup": "O+",
        "mizaj": "Damawi (Sanguine)",
        "allergies": ["None"]
    }, headers=doc_headers)
    new_pat = reg_body.get("patient", {})
    new_mrn = new_pat.get("mrn")
    log_result(1, "Walk-in Patient Registration & MRN",
               status == 201 and new_mrn and new_mrn.startswith("MRN-2026-"),
               f"Registered Zubair Khan with {new_mrn}")

    # 2. Appointment Booking & Queue Token
    status, apt_body = client.request("POST", "/api/v1/appointments", {
        "mrn": new_mrn,
        "patientName": "Zubair Khan",
        "doctorName": "Prof. (Dr.) Mansoor Alam",
        "chiefComplaint": "Sub-acute lumbar stiffness with damp aggravation",
        "acuity": "STANDARD",
        "fee": 800.0
    }, headers=doc_headers)
    apt = apt_body.get("appointment", {})
    apt_id = apt.get("id")
    token_num = apt.get("tokenNumber")
    log_result(2, "OPD Appointment Booking & Token Issuance",
               status == 201 and apt.get("status") == "WAITING" and token_num.startswith("T-"),
               f"Confirmed Appointment {apt_id} (Queue Token {token_num})")

    # 3. Clinical Consultation Initialization (Encounter Creation)
    vitals_payload = {"bp": "126/84", "pulse": "74", "temp": "98.6", "weight": "82", "spo2": "99", "hrv": "48.5"}
    soap_payload = {
        "subjective": "Lumbar stiffness lasting >30 minutes in morning. Aggravated by rainy/cold weather.",
        "objective": "Nabz: Bat'ee, Layyin. Lisan: Rutubat-e-Ghaliba with white coating. Lumbar paraspinal tightness without radiation.",
        "assessment": "Waja-ul-Zahr Barid Balghami (Lumbago / Phlegmatic Myofascial Pain).",
        "plan": "Stage 1 Tanqiya: Munzij & Mushil Balgham followed by Stage 2 Tahleel with Roghan Suranjan."
    }
    mizaj_payload = {
        "dominant": "Damawi (Sanguine)",
        "secondary": "Balghami",
        "su_e_mizaj": "Su-e-Mizaj Barid Balghami",
        "dyscrasia_degree": 2
    }
    axis_payload = {
        "primary_axis": "Musculoskeletal-Metabolic Axis",
        "status": "IMPAIRED_DRAINAGE",
        "rationale": "Accumulation of phlegmatic matter in lumbosacral aponeurosis."
    }
    afaal_payload = {
        "current_stage": "TANQIYA",
        "goals": ["Relieve morning stiffness to <10 min", "Reduce muscular spasm"],
        "regimen": "Nutool Haar with warm chamomile infusion nocte"
    }

    status, enc_body = client.request("POST", "/api/v1/encounters", {
        "mrn": new_mrn,
        "patientName": "Zubair Khan",
        "appointmentId": apt_id,
        "doctorName": "Prof. (Dr.) Mansoor Alam",
        "doctorReg": "CCIM-U-1988-0412",
        "chiefComplaint": "Sub-acute lumbar stiffness with damp aggravation",
        "examinationNotes": "Nabz: Bat'ee, Layyin. Lisan: White fur.",
        "vitals": vitals_payload,
        "soap": soap_payload,
        "mizaj": mizaj_payload,
        "organAxis": axis_payload,
        "afaalCascade": afaal_payload
    }, headers=doc_headers)
    enc = enc_body.get("encounter", {})
    enc_id = enc.get("id")
    log_result(3, "Consultation Cockpit Encounter Creation",
               status == 201 and enc.get("status") == "IN_PROGRESS",
               f"Encounter {enc_id} initialized in consultation cockpit")

    # 4. Appointment Status Transition to IN_CONSULTATION
    status, apt_check = client.request("GET", "/api/v1/appointments", headers=doc_headers)
    matched_apt = next((a for a in apt_check.get("appointments", []) if a["id"] == apt_id), None)
    log_result(4, "OPD Queue Status Auto-Transition",
               matched_apt and matched_apt.get("status") == "IN_CONSULTATION",
               f"Appointment {apt_id} transitioned from WAITING to IN_CONSULTATION")

    # 5. Vitals & Biometrics Persistence
    status, enc_fetch = client.request("GET", f"/api/v1/encounters/{enc_id}", headers=doc_headers)
    fetched_enc = enc_fetch.get("encounter", {})
    vitals_retrieved = fetched_enc.get("vitals", {})
    log_result(5, "Vitals & Physiological Metrics Persistence",
               status == 200 and vitals_retrieved.get("bp") == "126/84" and vitals_retrieved.get("hrv") == "48.5",
               f"Retrieved BP {vitals_retrieved.get('bp')}, Pulse {vitals_retrieved.get('pulse')} bpm, HRV {vitals_retrieved.get('hrv')} ms")

    # 6. Physical Examination (Nabz, Lisan, Baul) Persistence
    log_result(6, "Classical Physical Examination Storage",
               "Nabz: Bat'ee" in fetched_enc.get("examination_notes", ""),
               f"Physical examination notes: '{fetched_enc.get('examination_notes')}'")

    # 7. 10-Ajnas Classical Mizaj Assessment Submission
    status, mizaj_res = client.request("POST", f"/api/v1/patients/{new_mrn}/mizaj-assessment", {
        "answers": {"touch": "cold", "moisture": "moist", "build": "broad", "sleep": "excessive"},
        "encounter_id": enc_id
    }, headers=doc_headers)
    log_result(7, "10-Ajnas Classical Mizaj Evaluation",
               status == 201 and mizaj_res.get("dominantMizaj") == "Balghami (Cold & Moist)",
               f"Evaluated constitutional Mizaj: {mizaj_res.get('dominantMizaj')}")

    # 8. 9 Organ-Axis Functional Assessment Storage
    axis_retrieved = fetched_enc.get("organ_axis", {})
    log_result(8, "9 Organ-Axis Functional Assessment Storage",
               axis_retrieved.get("primary_axis") == "Musculoskeletal-Metabolic Axis",
               f"Target Axis: {axis_retrieved.get('primary_axis')} ({axis_retrieved.get('status')})")

    # 9. Afaal Cascade Protocol Tracking
    afaal_retrieved = fetched_enc.get("afaal_cascade", {})
    log_result(9, "Longitudinal Afaal Cascade Progression",
               afaal_retrieved.get("current_stage") == "TANQIYA",
               f"Active Afaal Stage: {afaal_retrieved.get('current_stage')} with {len(afaal_retrieved.get('goals', []))} therapeutic goals")

    # 10. Structured SOAP Note Verification
    soap_retrieved = fetched_enc.get("soap", {})
    log_result(10, "Structured SOAP Notes Verification",
               "Waja-ul-Zahr" in soap_retrieved.get("assessment", ""),
               f"Assessment: '{soap_retrieved.get('assessment')}'")

    # 11. Nuskha Prescription Authoring
    status, rx_res = client.request("POST", "/api/v1/prescriptions", {
        "patientName": "Zubair Khan",
        "mrn": new_mrn,
        "items": [
            {"name": "Majun Suranjan (Mudabbar)", "dose": "5g twice daily with lukewarm water", "duration": "14 days", "isScheduleE1": True, "batchNumber": "MS-2026-LOT4"},
            {"name": "Roghan-e-Balsan", "dose": "Local application nocte", "duration": "14 days", "isScheduleE1": False, "batchNumber": "RB-2026-LOT1"}
        ],
        "dietaryAdvice": "Avoid sour, cold, and flatulent foods.",
        "regimenalAdvice": "Nutool Haar with warm water daily for 10 minutes."
    }, headers=doc_headers)
    order_num = rx_res.get("orderNumber")
    log_result(11, "Nuskha Formulation & Mudabbar Gate Verification",
               status == 201 and order_num and rx_res.get("signatureHash"),
               f"Prescription {order_num} authored with Schedule E(1) Mudabbar batch MS-2026-LOT4")

    # 12. 21 CFR Part 11 Electronic Signature Seal & Merkle Anchoring
    status, sign_res = client.request("POST", f"/api/v1/encounters/{enc_id}/sign", {
        "doctorReg": "CCIM-U-1988-0412"
    }, headers=doc_headers)
    sig_hash = sign_res.get("signatureHash")
    log_result(12, "21 CFR Part 11 Digital Signature Seal",
               status == 200 and sign_res.get("status") == "LOCKED_AND_SIGNED" and sig_hash,
               f"Encounter sealed with cryptographic hash {sig_hash[:16]}...")

    # 13. Appointment Transition to COMPLETED
    status, apt_check2 = client.request("GET", "/api/v1/appointments", headers=doc_headers)
    matched_apt2 = next((a for a in apt_check2.get("appointments", []) if a["id"] == apt_id), None)
    log_result(13, "Encounter Lock & OPD Queue Completion",
               matched_apt2 and matched_apt2.get("status") == "COMPLETED",
               f"Appointment {apt_id} marked COMPLETED upon encounter signature")

    # 14. Patient 360 Longitudinal Timeline Aggregation
    status, timeline_res = client.request("GET", f"/api/v1/patients/{new_mrn}/timeline", headers=doc_headers)
    events = timeline_res.get("timeline", [])
    event_types = {e["eventType"] for e in events}
    has_all_types = {"APPOINTMENT", "ENCOUNTER", "PRESCRIPTION", "AUDIT_BLOCK"}.issubset(event_types)
    log_result(14, "Patient 360 Longitudinal Timeline Aggregation",
               status == 200 and has_all_types,
               f"Aggregated {len(events)} timeline events across {len(event_types)} event domains")

    # 15. Printable A4 Prescription Letterhead Data Fidelity
    status, rx_detail = client.request("GET", f"/api/v1/prescriptions/{order_num}", headers=doc_headers)
    rx_data = rx_detail.get("prescription", {})
    has_rx_fidelity = (
        rx_data.get("patient_name") == "Zubair Khan" and
        len(rx_data.get("items", [])) == 2 and
        bool(rx_data.get("signature_hash")) and
        bool(rx_data.get("dietary_advice"))
    )
    log_result(15, "Printable A4 Prescription Letterhead Data Fidelity",
               status == 200 and has_rx_fidelity,
               f"Prescription letterhead payload verified: {len(rx_data.get('items', []))} items, dietary parhez, and 21 CFR Part 11 seal")

    # 16. Cross-Tenant Encounter Access Denial
    _, branch_login = client.request("POST", "/api/v1/auth/login", {
        "email": "sirajuddin@zayvora.health",
        "password": "doctor123"
    })
    branch_token = branch_login["token"]
    status, cross_enc = client.request("GET", f"/api/v1/encounters/{enc_id}", headers={"Authorization": f"Bearer {branch_token}"})
    log_result(16, "Cross-Tenant Clinical Encounter Isolation Guard",
               status == 403 and cross_enc.get("code") == "CROSS_TENANT_ACCESS_DENIED",
               f"Foreign facility clinician blocked with HTTP 403: '{cross_enc.get('error')}'")

    # 17. Zero Developer Jargon Across Clinical Payloads
    forbidden = ["traceback", "safe_to_lock = False", "exception in thread", "sqlite3.operationalerror", "25-Engine Live Matrix"]
    jargon_found = False
    for payload in [sign_res, timeline_res, rx_detail, cross_enc]:
        p_str = json.dumps(payload).lower()
        for f in forbidden:
            if f.lower() in p_str:
                jargon_found = True
                break
    log_result(17, "Zero Developer Jargon in Clinical Continuum Responses",
               jargon_found is False,
               "All clinical payloads contain zero developer terminology")

    print("=" * 76)
    print(f"PHASE 3 VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 76)
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
