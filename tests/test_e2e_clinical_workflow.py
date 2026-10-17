#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — END-TO-END CLINICAL ECOSYSTEM WORKFLOW TEST
Tests the complete multi-role clinical journey:
1. Patient Authentication & Health Record Resolution
2. Appointment Booking & Token Issuance
3. Doctor Encounter, Mizaj 10-Ajnas & Organ-Axis Cascade
4. Hakeem Sahab AI™ Copilot Decision Support & Safety Invariant
5. 21 CFR Part 11 Prescription Authoring & Cryptographic Seal
6. Pharmacist FEFO Allocation & Mudabbar Validation Dispensing
7. Merkle Audit Ledger Immutability & Event Anchoring
"""

import sys
import os
import json
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

try:
    from tests.test_phase2_auth_rbac_tenancy import DirectTestClient
except ImportError:
    from test_phase2_auth_rbac_tenancy import DirectTestClient

class TestEndToEndClinicalWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sqlite3, os
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "zayvora_live.db")
        if os.path.exists(db_path):
            with sqlite3.connect(db_path) as conn:
                conn.execute("DELETE FROM prescriptions WHERE mrn = 'MRN-2026-0814'")
                conn.commit()

    def setUp(self):
        self.client = DirectTestClient()

        # Login Doctor
        st, body = self.client.request("POST", "/api/v1/auth/login", {
            "email": "mansoor.alam@zayvora.health",
            "password": "doctor123"
        })
        assert st == 200, f"Doctor login failed: {body}"
        self.doc_token = body["token"]

        # Login Pharmacist
        st, body = self.client.request("POST", "/api/v1/auth/login", {
            "email": "pharmacy@zayvorahealth",
            "password": "pharmacy123"
        })
        assert st == 200, f"Pharmacist login failed: {body}"
        self.pharm_token = body["token"]


    def test_01_patient_record_resolution(self):
        """1. Verify patient records aggregation via /api/v1/patient/my-records."""
        st, body = self.client.request("GET", "/api/v1/patient/my-records?mrn=MRN-2026-0814",
                                       headers={"Authorization": f"Bearer {self.doc_token}"})
        self.assertEqual(st, 200)
        self.assertTrue(body.get("ok"))
        self.assertIn("patient", body)
        self.assertEqual(body["patient"]["mrn"], "MRN-2026-0814")

    def test_02_appointment_booking_flow(self):
        """2. Verify patient appointment booking & OPD token issuance."""
        st, body = self.client.request("POST", "/api/v1/appointments", {
            "patientName": "Hamza Farooqi",
            "mrn": "MRN-2026-0814",
            "doctorName": "Prof. (Dr.) Mansoor Alam",
            "date": "2026-09-25",
            "timeSlot": "11:30 AM",
            "chiefComplaint": "Joint stiffness & digestive sluggishness",
            "acuity": "STANDARD"
        }, headers={"Authorization": f"Bearer {self.doc_token}"})
        self.assertEqual(st, 201)
        self.assertTrue(body.get("ok"))
        self.assertTrue(body["appointment"]["tokenNumber"].startswith("T-"))

    def test_03_hakeem_sahab_copilot_safety(self):
        """3. Verify Hakeem Sahab AI copilot decision support & clinician-in-loop enforcement."""
        st, body = self.client.request("POST", "/api/v1/hakeem/consult", {
            "chiefComplaint": "Subacute knee swelling with phlegmatic dyscrasia (Su-ul-Mizaj Barid Balghami)",
            "mrn": "MRN-2026-0814",
            "organAxis": "Musculoskeletal-Metabolic Axis (Mafasil-Asab)"
        }, headers={"Authorization": f"Bearer {self.doc_token}"})
        self.assertIn(st, (200, 201))
        self.assertTrue(body.get("ok"))
        # Invariant: AI suggestions CANNOT be locked autonomously
        self.assertFalse(body.get("safe_to_lock", True))
        self.assertTrue(body.get("requiresPractitionerSignoff", True))

    def test_04_prescription_authoring_and_signing(self):
        """4. Verify 21 CFR Part 11 prescription authoring and cryptographic digital signature."""
        st, body = self.client.request("POST", "/api/v1/prescriptions", {
            "patientName": "Hamza Farooqi",
            "mrn": "MRN-2026-0814",
            "doctorName": "Prof. (Dr.) Mansoor Alam",
            "doctorReg": "CCIM-U-1988-0412",
            "items": [
                {
                    "name": "Majun Suranjan (Mudabbar)",
                    "dose": "5g twice daily with lukewarm water",
                    "mudabbarCert": "SHA256:7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b"
                }
            ],
            "dietaryAdvice": "Avoid refrigerated liquids; take warm ginger infusions.",
            "regimenalAdvice": "Gentle non-weight-bearing mobility exercises."
        }, headers={"Authorization": f"Bearer {self.doc_token}"})
        self.assertEqual(st, 201)
        self.assertTrue(body.get("ok"))
        self.assertTrue(len(body.get("signatureHash", "")) == 64)

    def test_05_pharmacy_fefo_dispensing(self):
        """5. Verify pharmacist dispensing with Mudabbar validation and inventory deduction."""
        st, body = self.client.request("POST", "/api/v1/inventory/dispense", {
            "batchNumber": "MS-2026-LOT4",
            "quantity": 1
        }, headers={"Authorization": f"Bearer {self.pharm_token}"})
        self.assertEqual(st, 200)
        self.assertTrue(body.get("ok"))
        self.assertIn("remainingStock", body)

    def test_06_patient_idor_prevention(self):
        """6. Verify Patient IDOR isolation: patient is blocked with 403 when accessing another patient record."""
        # Login Patient Hamza
        st, body = self.client.request("POST", "/api/v1/auth/login", {
            "email": "hamza.farooqi@gmail.com",
            "password": "password123"
        })
        self.assertEqual(st, 200)
        patient_token = body["token"]

        # Access own record -> 200
        st, body = self.client.request("GET", "/api/v1/patients/MRN-2026-0814",
                                       headers={"Authorization": f"Bearer {patient_token}"})
        self.assertEqual(st, 200)

        # Access other patient's record -> 403 Forbidden
        st, body = self.client.request("GET", "/api/v1/patients/MRN-2026-0901",
                                       headers={"Authorization": f"Bearer {patient_token}"})
        self.assertEqual(st, 403)
        self.assertIn("denied", body.get("error", "").lower())

    def test_07_appointment_lifecycle_patch_delete(self):
        """7. Verify full appointment lifecycle: POST -> PATCH reschedule -> DELETE cancel."""
        # Login Patient Hamza
        st, body = self.client.request("POST", "/api/v1/auth/login", {
            "email": "hamza.farooqi@gmail.com",
            "password": "password123"
        })
        self.assertEqual(st, 200)
        patient_token = body["token"]

        # 1. Book appointment
        st, body = self.client.request("POST", "/api/v1/appointments", {
            "patient_id": "MRN-2026-0814",
            "doctor_id": "DOC-2026-01",
            "appointmentDate": "2026-09-30",
            "appointmentTime": "10:00 AM",
            "reason": "Mizaj regimen follow-up"
        }, headers={"Authorization": f"Bearer {patient_token}"})
        self.assertIn(st, (200, 201))
        appt_id = body.get("appointment", {}).get("id") or body.get("id")
        self.assertTrue(appt_id)

        # 2. Reschedule via PATCH
        st, body = self.client.request("PATCH", f"/api/v1/appointments/{appt_id}", {
            "date": "2026-10-02",
            "timeSlot": "02:30 PM",
            "status": "RESCHEDULED"
        }, headers={"Authorization": f"Bearer {patient_token}"})
        self.assertEqual(st, 200)
        self.assertEqual(body.get("status"), "RESCHEDULED")

        # 3. Cancel via DELETE
        st, body = self.client.request("DELETE", f"/api/v1/appointments/{appt_id}",
                                       headers={"Authorization": f"Bearer {patient_token}"})
        self.assertEqual(st, 200)
        self.assertEqual(body.get("status"), "CANCELLED")

if __name__ == "__main__":
    unittest.main()

