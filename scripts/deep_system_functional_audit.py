#!/usr/bin/env python3
"""
ZAYVORA Health OS™ - Comprehensive Deep System Functional Audit
Tests every core operational subsystem:
1. Database Health & Integrity
2. Auth & RBAC Security Engine
3. Master Patient Index & Appointments
4. 13-Tab Clinical Encounter & Digital Scribe
5. 21 CFR Part 11 Electronic Signature & Merkle Ledger
6. Central Pharmacy FEFO Allocation & Schedule E(1) Gates
7. Botanical Knowledge Graph & Therapeutic Products (32 Master SKUs)
8. Manufacturing BOM Server & PDF/HTML Engine
9. AI Clinical Decision Support (Hakeem Sahab v2)
10. UI Assets & Static Web Routes
"""

import os
import sys
import json
import time
import io
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler


class MockSocket:
    def __init__(self, request_bytes):
        self.rfile = io.BytesIO(request_bytes)
        self.wfile = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return self.rfile
        return self.wfile

    def sendall(self, b):
        self.wfile.write(b)


def dispatch_request(method="GET", path="/", body=None, headers=None):
    if headers is None:
        headers = {}
    body_bytes = b""
    if body is not None:
        if isinstance(body, dict):
            body_bytes = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif isinstance(body, str):
            body_bytes = body.encode("utf-8")
        headers["Content-Length"] = str(len(body_bytes))

    lines = [f"{method} {path} HTTP/1.1", "Host: localhost:8088"]
    for k, v in headers.items():
        lines.append(f"{k}: {v}")
    lines.append("")
    lines.append("")

    raw_req = "\r\n".join(lines).encode("latin1") + body_bytes
    sock = MockSocket(raw_req)

    start_t = time.perf_counter()
    try:
        handler = ZayvoraApiHandler(sock, ("127.0.0.1", 8088), None)
    except Exception as e:
        pass
    elapsed_ms = (time.perf_counter() - start_t) * 1000

    raw_resp = sock.wfile.getvalue()
    if not raw_resp:
        return 500, {}, b"", elapsed_ms

    parts = raw_resp.split(b"\r\n\r\n", 1)
    header_block = parts[0].decode("latin1", errors="ignore")
    body_resp = parts[1] if len(parts) > 1 else b""

    status_line = header_block.split("\r\n")[0]
    status_code = int(status_line.split(" ")[1])

    resp_headers = {}
    for line in header_block.split("\r\n")[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            resp_headers[k.strip().lower()] = v.strip()

    return status_code, resp_headers, body_resp, elapsed_ms


def run_deep_audit():
    audit_results = []
    
    def log_test(module, name, passed, details="", latency_ms=0.0):
        status = "PASS" if passed else "FAIL"
        audit_results.append({
            "module": module,
            "name": name,
            "status": status,
            "latency_ms": round(latency_ms, 2),
            "details": details
        })
        print(f"[{status:4s}] {module:<25} | {name:<45} | {latency_ms:6.2f}ms | {details}")

    print("=" * 100)
    print("ZAYVORA HEALTH OS™ v5.0 — ENTERPRISE DEEP FUNCTIONAL AUDIT")
    print("=" * 100)

    # ---------------- 1. Database Health ----------------
    db_path = os.path.join(BASE_DIR, "database", "zayvora_live.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA integrity_check")
    integ = cur.fetchone()[0]
    log_test("Database", "SQLite Master Integrity Check", integ == "ok", f"Integrity: {integ}")

    cur.execute("SELECT COUNT(*) FROM master_products")
    p_cnt = cur.fetchone()[0]
    log_test("Database", "Master Products Catalog (32 SKUs)", p_cnt == 32, f"Total products: {p_cnt}")

    cur.execute("SELECT COUNT(*) FROM master_products WHERE is_hero_launch = 1")
    hero_cnt = cur.fetchone()[0]
    log_test("Database", "Phase-1 Hero Launch SKUs", hero_cnt == 5, f"Heroes configured: {hero_cnt}")

    cur.execute("SELECT COUNT(*) FROM users")
    u_cnt = cur.fetchone()[0]
    log_test("Database", "Seeded User Identity Records", u_cnt >= 10, f"Total users: {u_cnt}")
    conn.close()

    # ---------------- 2. System Health & Provenance ----------------
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/health")
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    log_test("Health & Telemetry", "System Health Check", code == 200 and data.get("ok") is True, f"Code {code}, DB: {data.get('database')}", lat)

    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/system/provenance")
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    log_test("Health & Telemetry", "System Provenance & Data Truth", code == 200 and "provenance_metadata" in data, f"Code {code}, Provenance keys: {len(data.get('provenance_metadata', {}))}", lat)

    # ---------------- 3. Authentication & RBAC ----------------
    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/auth/login", {"email": "dr.irfan@zayvorahealth", "password": "doctor123"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    doctor_token = data.get("token")
    log_test("Auth & Identity", "Clinician Login (Doctor)", code == 200 and bool(doctor_token), f"Code {code}, Role: {data.get('role')}", lat)

    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/auth/login", {"email": "pharmacy@zayvorahealth", "password": "pharmacy123"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    pharm_token = data.get("token")
    log_test("Auth & Identity", "Dispensary Login (Pharmacist)", code == 200 and bool(pharm_token), f"Code {code}, Role: {data.get('role')}", lat)

    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/auth/login", {"email": "hamza.farooqi@gmail.com", "password": "password123"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    patient_token = data.get("token")
    log_test("Auth & Identity", "Patient Portal Login", code == 200 and bool(patient_token), f"Code {code}, Role: {data.get('role')}", lat)

    # Cross-role unauthorized rejection: Patient blocked from audit logs
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/audit/logs", headers={"Authorization": f"Bearer {patient_token}"})
    log_test("Auth & RBAC", "Unauthorized Audit Access Block (Patient)", code == 403, f"Code {code} (Forbidden as expected)", lat)

    # Cross-role unauthorized rejection: Doctor blocked from audit logs
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/audit/logs", headers={"Authorization": f"Bearer {doctor_token}"})
    log_test("Auth & RBAC", "Unauthorized Audit Access Block (Doctor)", code == 403, f"Code {code} (Forbidden as expected)", lat)

    # ---------------- 4. Patient Master Index & Appointments ----------------
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/patients", headers={"Authorization": f"Bearer {doctor_token}"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    pts = data.get("patients", [])
    log_test("Master Patient Index", "Fetch Registered Patients", code == 200 and len(pts) > 0, f"Found {len(pts)} active patients", lat)

    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/patient/360?patient_id=PAT-774901", headers={"Authorization": f"Bearer {doctor_token}"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    log_test("Clinical 360", "Patient 360 Holistic View", code == 200 and data.get("ok") is True, f"Code {code}, Patient: {data.get('patient', {}).get('first_name')}", lat)

    # ---------------- 5. Consultation & Clinical Continuum ----------------
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/clinical/encounter/prepare?patient_id=PAT-774901&clinician_id=DOC-01", headers={"Authorization": f"Bearer {doctor_token}"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    log_test("Clinical Encounter", "Encounter Preflight Preparation", code == 200 and data.get("ok") is True, f"Code {code}, Stage: {data.get('encounter_stage')}", lat)

    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/clinical/encounter/start", {
        "patient_id": "PAT-774901", "clinician_id": "DOC-01", "encounter_type": "IN_PERSON_OPD"
    }, headers={"Authorization": f"Bearer {doctor_token}"})
    data = json.loads(body.decode("utf-8")) if code in (200, 201) else {}
    enc_id = data.get("encounter", {}).get("encounter_id", "ENC-TEST")
    log_test("Clinical Encounter", "Start Clinical OPD Encounter", code in (200, 201) and enc_id != "ENC-TEST", f"Code {code}, Encounter ID: {enc_id}", lat)

    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/clinical/encounter/sign-off", {
        "encounter_id": enc_id, "clinician_id": "DOC-01", "signing_pin": "123456", "reason": "Chief complaint and examination locked."
    }, headers={"Authorization": f"Bearer {doctor_token}"})
    log_test("Clinical Encounter", "Encounter 21 CFR Part 11 Sign-off & Lock", code == 200, f"Code {code}", lat)

    # ---------------- 6. Prescriptions, 21 CFR Part 11 & Merkle Ledger ----------------
    rx_payload = {
        "mrn": "MRN-2026-0814",
        "patientName": "Hamza Farooqi",
        "doctorName": "Dr. Irfan Ashraf",
        "doctorReg": "CCIM-U-1988-0412",
        "items": [
            {"sku": "ZAY-007", "name": "ZAYVORA SynovoFlex™", "dosage": "5g twice daily with warm milk", "quantity": 1},
            {"sku": "ZAY-004", "name": "ZAYVORA LiverPrime™", "dosage": "1 capsule before meals", "quantity": 1}
        ],
        "dietaryAdvice": "Avoid cold/phlegmatic foods; consume ginger tea",
        "regimenalAdvice": "Nutool Haar with Roghan-e-Balsan"
    }
    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/prescriptions", rx_payload, headers={"Authorization": f"Bearer {doctor_token}"})
    data = json.loads(body.decode("utf-8")) if code in (200, 201) else {}
    rx_num = data.get("orderNumber", "")
    sig_hash = data.get("signatureHash", "")
    log_test("e-Prescribing", "21 CFR Part 11 Digital Signature Seal", code in (200, 201) and bool(sig_hash), f"Code {code}, Order: {rx_num}, Hash: {sig_hash[:16]}...", lat)

    # ---------------- 7. Central Pharmacy FEFO & Schedule E(1) Gates ----------------
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/inventory", headers={"Authorization": f"Bearer {pharm_token}"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    items = data.get("inventory", [])
    log_test("Dispensary", "Inventory Stock & Batch Inspection", code == 200 and len(items) > 0, f"Found {len(items)} batches in dispensary", lat)

    # Schedule E(1) unpurified raw poison block test
    unpurified_payload = {
        "batchNumber": "MS-2026-RAW",
        "quantity": 1
    }
    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/inventory/dispense", unpurified_payload, headers={"Authorization": f"Bearer {pharm_token}"})
    data = json.loads(body.decode("utf-8")) if code in (400, 403) else {}
    raw_blocked = code == 403 and data.get("code") == "MUDABBAR_CERTIFICATE_REQUIRED"
    log_test("Dispensary", "Schedule E(1) Poison Firewall (Unpurified Block)", raw_blocked, f"Code {code}, Gate Verdict: {data.get('code')}", lat)

    # Valid purified batch dispense test
    purified_payload = {
        "batchNumber": "MS-2026-LOT4",
        "quantity": 1
    }
    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/inventory/dispense", purified_payload, headers={"Authorization": f"Bearer {pharm_token}"})
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    log_test("Dispensary", "FEFO Authorized Batch Dispense", code == 200 and data.get("ok") is True, f"Code {code}, Dispense Record: {data.get('dispenseId')}", lat)

    # ---------------- 8. Therapeutic Catalog & Manufacturing BOM ----------------
    code, hdrs, body, lat = dispatch_request("GET", "/api/v1/therapeutic/products")
    data = json.loads(body.decode("utf-8")) if code == 200 else {}
    prods = data.get("products", [])
    has_glucovora = any("Glucovora" in p.get("name", "") for p in prods)
    log_test("Therapeutic Catalog", "Live Therapeutic Products (Coined Names)", code == 200 and has_glucovora and len(prods) == 32, f"Total products: {len(prods)}, Verified Glucovora: {has_glucovora}", lat)

    code, hdrs, body, lat = dispatch_request("GET", "/bom")
    log_test("Manufacturing BOM", "Manufacturing HTML Dossier Route (/bom)", code == 200 and b"ZAYVORA HEALTH OS" in body, f"Code {code}, Length: {len(body)} bytes", lat)

    code, hdrs, body, lat = dispatch_request("GET", "/bom.pdf")
    is_valid_pdf = body.startswith(b"%PDF-1.4")
    log_test("Manufacturing BOM", "Manufacturing PDF Binary Route (/bom.pdf)", code == 200 and is_valid_pdf, f"Code {code}, Size: {len(body)/1024:.1f} KB, PDF header: {is_valid_pdf}", lat)

    # ---------------- 9. Clinical Decision Support (Hakeem Sahab v2) ----------------
    code, hdrs, body, lat = dispatch_request("POST", "/api/v1/ai/consult", {
        "chief_complaint": "Waja-ul-Mafasil (Joint pain and morning stiffness in bilateral knees)",
        "patient_id": "PAT-774901",
        "mizaj": "Balghami (Cold & Moist)"
    }, headers={"Authorization": f"Bearer {doctor_token}"})
    data = json.loads(body.decode("utf-8")) if code in (200, 201) else {}
    cds_ok = code in (200, 201) and data.get("ok") is True and "layers" in data
    log_test("Hakeem Sahab CDS", "5-Layer AI Clinical Decision Support & RAG", cds_ok, f"Code {code}, Consultation: {data.get('consultationNumber')}, Layers: {len(data.get('layers', {}))}", lat)

    # ---------------- 10. Web Assets & Static Serving ----------------
    code, hdrs, body, lat = dispatch_request("GET", "/")
    log_test("Web Application", "Root Single-Page Application (index.html)", code == 200 and b"ZAYVORA Health OS" in body, f"Code {code}, Length: {len(body)/1024:.1f} KB", lat)

    print("=" * 100)
    passed_cnt = sum(1 for r in audit_results if r["status"] == "PASS")
    failed_cnt = sum(1 for r in audit_results if r["status"] == "FAIL")
    print(f"AUDIT SUMMARY: {passed_cnt} PASSED | {failed_cnt} FAILED | TOTAL {len(audit_results)}")
    print("=" * 100)

    return passed_cnt, failed_cnt, audit_results


if __name__ == "__main__":
    p, f, results = run_deep_audit()
    sys.exit(0 if f == 0 else 1)
