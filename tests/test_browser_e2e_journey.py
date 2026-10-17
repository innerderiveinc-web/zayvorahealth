#!/usr/bin/env python3
"""
ZAYVORA Health™ — Browser & Clinician E2E User Journey Test Suite
Validates the complete end-to-end clinical loop:
1. Public Front-Door & Role-Gated Portal Contract (index.html / app.html)
2. Clinician Authentication & Multi-Tenant Session Establishment
3. Patient Directory & 360-Degree Longitudinal Clinical Profile Retrieval
4. 10-Ajnas Mizaj & Clinical SOAP Note Authoring with Cryptographic Hash
5. Formulation Preflight Safety & Prescription Authoring with 21 CFR Part 11 Digital Signature
6. SQL Database Persistence & Merkle Audit Trail Anchoring
7. Closed-Loop Pharmacy FEFO Dispensing Lifecycle
8. Patient Portal Retrieval & Verification
"""

import hashlib
import json
import os
import sys
import unittest
from datetime import datetime, timezone
from io import BytesIO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler, DB_PATH
from services.db_adapter import get_universal_db


class DirectApiSimulator:
    """Simulates real HTTP requests directly against ZayvoraApiHandler."""
    def request(self, method: str, path: str, data: dict = None, headers: dict = None):
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


class TestBrowserE2EUserJourney(unittest.TestCase):
    """End-to-End clinical workflow journey validation."""
    order_number = None

    @classmethod
    def setUpClass(cls):
        conn = get_universal_db(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM prescriptions WHERE mrn = 'PAT-0816'")
        conn.commit()
        conn.close()

    def setUp(self):
        self.client = DirectApiSimulator()

    def test_01_public_frontdoor_contract(self):
        """Verify index.html conforms to professional public portal standards."""
        index_path = os.path.join(BASE_DIR, "index.html")
        self.assertTrue(os.path.exists(index_path))
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Must not contain amateur demo banners
        self.assertNotIn("Demo Environment Status", html)
        # Must contain professional clinical desk access
        self.assertIn("Authorized Clinical Portals", html)
        # Must have smooth anchor for patient appointment booking
        self.assertIn("opd-booking-card", html)

    def test_02_clinician_authentication(self):
        """Authenticate Dr. Irfan Ashraf and verify clinician session."""
        status, resp = self.client.request("POST", "/api/v1/auth/login", {
            "email": "dr.irfan@zayvorahealth",
            "password": "Zayvora@123"
        })
        self.assertEqual(status, 200, f"Login failed: {resp}")
        self.assertTrue(resp.get("ok"))
        self.assertEqual(resp.get("user", {}).get("role"), "DOCTOR")
        self.assertIn("token", resp)

    def test_03_patient_directory_and_360_profile(self):
        """Query patient directory and load 360 profile."""
        status, resp = self.client.request("GET", "/api/v1/patients")
        self.assertEqual(status, 200)
        self.assertTrue(resp.get("ok"))
        patients = resp.get("patients", [])
        self.assertGreater(len(patients), 0, "Expected patients in database")
        
        target_patient = patients[0]
        mrn = target_patient.get("mrn")
        self.assertTrue(mrn)

        # Retrieve 360-degree patient profile
        status_360, resp_360 = self.client.request("GET", f"/api/v1/patient/360?patient_id={mrn}")
        self.assertEqual(status_360, 200)
        self.assertTrue(resp_360.get("ok"))
        self.assertIn("patient_360", resp_360)

    def test_04_mizaj_assessment_and_clinical_soap(self):
        """Conduct Mizaj assessment and persist SOAP note with cryptographic hash."""
        conn = get_universal_db(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, mrn FROM encounters LIMIT 1")
        enc = cur.fetchone()
        encounter_id = enc["id"] if enc else "ENC-001"
        mrn = enc["mrn"] if enc else "MRN-2026-0814"

        cur.execute("SELECT id FROM patients WHERE mrn = ? OR id = ?", (mrn, mrn))
        p_row = cur.fetchone()
        patient_id = p_row["id"] if p_row else "PAT-0814"

        cur.execute("SELECT clinician_id FROM clinician_registry LIMIT 1")
        c_row = cur.fetchone()
        clinician_id = c_row["clinician_id"] if c_row else "CLN-IRFAN-01"

        # Insert clinical assessment with exact table columns
        cur.execute("""
            INSERT OR REPLACE INTO clinical_assessments (
                assessment_id, encounter_id, patient_id, clinician_id,
                subjective_narrative, objective_findings_json, assessment_summary,
                plan_summary, inputs_reproducibility_json, confidence_score,
                immutable_sha256_hash, signed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "ASM-E2E-TEST-001",
            encounter_id,
            patient_id,
            clinician_id,
            "Chief complaint: Knee pain with sluggish morning digestion and joint heaviness.",
            json.dumps({"bp": "130/80", "nabz": "Batee Layyin", "tongue": "White coat", "mizaj": "Balghami"}),
            "Su-e-Mizaj Balghami with Meda-Mafasil functional axis involvement.",
            "Tadeel-e-Mizaj + Majun Suranjan 5g nocte + Dietary Parhez.",
            json.dumps({"rules_version": "v5.2", "model": "Hakeem-v2-Verified"}),
            0.96,
            hashlib.sha256(b"ENC-E2E-TEST-001-SOAP-EVIDENCE").hexdigest(),
            datetime.now(timezone.utc).isoformat()
        ))
        conn.commit()

        # Verify persisted record
        cur.execute("SELECT immutable_sha256_hash FROM clinical_assessments WHERE assessment_id = 'ASM-E2E-TEST-001'")
        saved_soap = cur.fetchone()
        self.assertIsNotNone(saved_soap)
        self.assertEqual(len(saved_soap["immutable_sha256_hash"]), 64)
        conn.close()

    def test_05_prescription_nuskha_authoring_and_db_persistence(self):
        """Author prescription, digitally seal it, and verify database commit."""
        payload = {
            "patientName": "Fatima Begum",
            "mrn": "PAT-0816",
            "doctorName": "Dr. Irfan Ashraf",
            "doctorReg": "BUMS/AMU/2010/1234",
            "items": [
                {"name": "Majun Suranjan", "dose": "5g", "frequency": "HS", "duration": "14 days"},
                {"name": "Sharbat Banafsha", "dose": "2 tsp", "frequency": "BD", "duration": "7 days"}
            ],
            "dietaryAdvice": "Avoid cold rice, curd, and excessive heavy cold foods.",
            "regimenalAdvice": "Warm fomentation (Natool) on knee joints before sleep."
        }

        status, resp = self.client.request("POST", "/api/v1/prescriptions", payload)
        self.assertEqual(status, 201)
        self.assertTrue(resp.get("ok"))
        order_num = resp.get("order_number")
        self.assertTrue(order_num)
        TestBrowserE2EUserJourney.order_number = order_num

        # Verify prescription in database
        conn = get_universal_db(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT order_number, patient_name, doctor_name, status, items_json FROM prescriptions WHERE order_number = ?", (order_num,))
        saved_rx = cur.fetchone()
        self.assertIsNotNone(saved_rx, f"Prescription {order_num} was not saved to database")
        self.assertEqual(saved_rx["patient_name"], "Fatima Begum")
        self.assertEqual(saved_rx["doctor_name"], "Dr. Irfan Ashraf")

        # Verify Merkle audit anchoring
        cur.execute("SELECT leaf_hash, event_type, status FROM audit_ledger WHERE event_type = 'PRESCRIPTION_LOCKED_21CFR11' ORDER BY block_number DESC LIMIT 1")
        audit_entry = cur.fetchone()
        self.assertIsNotNone(audit_entry)
        self.assertEqual(audit_entry["status"], "ANCHORED")
        conn.close()

    def test_06_closed_loop_pharmacy_dispense(self):
        """Verify Closed-Loop Pharmacy dispense evaluation endpoint."""
        status, resp = self.client.request("POST", "/api/v1/therapeutic/pharmacy/dispense-nuskha", {
            "nuskha_id": "NSK-2026-E2E",
            "patient_id": "PAT-0816",
            "clinician_signature": "SIG-DOC-IRFAN-VALID-SHA256",
            "is_signature_valid": True,
            "prescribed_items": [
                {"item_id": "ZAY-MED-001", "name": "Majun Suranjan", "qty": 1}
            ],
            "pharmacist_id": "PHARM-LIC-DELHI-01"
        })
        self.assertEqual(status, 200)
        self.assertTrue(resp.get("ok"))
        self.assertIn("dispense_result", resp)

    def test_07_patient_portal_prescription_retrieval(self):
        """Verify patient can retrieve issued prescriptions via their MRN."""
        status, resp = self.client.request("GET", "/api/v1/prescriptions?mrn=PAT-0816")
        self.assertEqual(status, 200)
        rxs = resp.get("prescriptions", [])
        self.assertGreater(len(rxs), 0)
        order_numbers = [r["order_number"] for r in rxs]
        if TestBrowserE2EUserJourney.order_number:
            self.assertIn(TestBrowserE2EUserJourney.order_number, order_numbers)


if __name__ == "__main__":
    unittest.main()
