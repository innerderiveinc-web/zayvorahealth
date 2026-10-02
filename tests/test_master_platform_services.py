#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Master Platform Services & Connected Architecture Test Suite

Validates the 10-Service Spine:
  - Universal Task Engine (Service 8)
  - Encounter OS & 3-Zone Cockpit (Service 3)
  - Patient 360 Center of Gravity (Service 2)
  - Care Plan OS & Longitudinal Chronic Care (Service 9)
  - Canonical Terminology & Prototype Cleanup (Service 4 & 10)
  - Secure Patient ↔ Care Team Messaging with Emergency Red-Flag Triage
"""

import io
import json
import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.clinical.app.engines.universal_task_engine import UniversalTaskEngine
from services.clinical.app.engines.encounter_os_engine import EncounterOSEngine
from services.clinical.app.engines.patient_360_master import Patient360Master
from services.clinical.app.engines.care_plan_os_engine import CarePlanOSEngine
from services.knowledge.app.core.canonical_terminology_service import CanonicalTerminologyService
from services.live_api_server import ZayvoraApiHandler


class TestMasterPlatformServices(unittest.TestCase):

    def setUp(self):
        class DummySocket:
            def __init__(self, rfile, wfile):
                self.rfile = rfile
                self.wfile = wfile
            def makefile(self, mode, *args, **kwargs):
                return self.rfile if "r" in mode else self.wfile
            def sendall(self, b):
                self.wfile.write(b)

        self.DummySocket = DummySocket

    def _call_handler(self, method: str, path: str, body: dict = None):
        body_bytes = json.dumps(body).encode("utf-8") if body else b""
        req = f"{method} {path} HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Length: {len(body_bytes)}\r\nContent-Type: application/json\r\n\r\n".encode("utf-8") + body_bytes
        rfile = io.BytesIO(req)
        wfile = io.BytesIO()
        sock = self.DummySocket(rfile, wfile)
        handler = ZayvoraApiHandler(sock, ("127.0.0.1", 54321), None)
        wfile.seek(0)
        raw_output = wfile.getvalue().decode("utf-8")
        parts = raw_output.split("\r\n\r\n", 1)
        headers = parts[0].split("\r\n")
        status_code = int(headers[0].split(" ")[1])
        resp_body = json.loads(parts[1]) if len(parts) > 1 and parts[1] else {}
        return status_code, resp_body

    # 1. Universal Task Engine Tests
    def test_01_universal_task_lifecycle(self):
        """Verify Task creation, priority ordering, and completion."""
        task = UniversalTaskEngine.create_task(
            title="Review Urgent Synovial Aspirate",
            description="Patient shows acute joint swelling. Exclude septic arthritis before continuing Cupping/Hijama.",
            owner_id="DOC-01",
            owner_role="DOCTOR",
            task_type="LAB_REVIEW",
            source_module="encounter",
            priority="STAT",
            patient_id="MRN-2026-0001",
            due_in_hours=2
        )
        self.assertTrue(task.id.startswith("TSK-2026-"))
        self.assertEqual(task.status, "PENDING")
        self.assertEqual(task.priority, "STAT")

        # Fetch tasks for doctor
        tasks = UniversalTaskEngine.get_tasks_for_role("DOCTOR", status="PENDING")
        self.assertGreaterEqual(len(tasks), 1)
        # Top task should be STAT priority
        self.assertEqual(tasks[0]["priority"], "STAT")

        # Complete task
        res = UniversalTaskEngine.complete_task(task.id, actor_id="dr-hakeem-irfan", resolution_notes="Aspirate clear. Safe to proceed.")
        self.assertTrue(res["ok"])
        self.assertEqual(res["status"], "COMPLETED")

    # 2. Encounter OS Tests
    def test_02_encounter_os_workflow(self):
        """Verify Pre-Encounter preparation, Encounter start, and 21 CFR Part 11 Digital Signature."""
        prep = EncounterOSEngine.prepare_pre_encounter("PAT-774901", "DOC-01")
        self.assertIn("pre_encounter_brief", prep)
        self.assertIn("last_visit_summary", prep["pre_encounter_brief"])

        record = EncounterOSEngine.start_encounter("PAT-774901", "DOC-01", "FAC-HQ-01", "IN_PERSON_OPD")
        self.assertTrue(record.encounter_id.startswith("ENC-2026-"))
        self.assertEqual(record.status, "IN_CONSULTATION")
        self.assertEqual(record.safety_rail_decision, "PASS")
        self.assertEqual(len(record.parhez_8_tier), 8)

        # 21 CFR Part 11 Sign-off
        sign_res = EncounterOSEngine.sign_off_encounter(record.encounter_id, "DOC-01", "882910")
        self.assertTrue(sign_res["ok"])
        self.assertEqual(sign_res["status"], "SIGNED_OFF")
        self.assertIn("signature_hash", sign_res["signature"])
        self.assertIn("merkle_anchor", sign_res["signature"])

    # 3. Patient 360 Master Center of Gravity Tests
    def test_03_patient_360_master_facets(self):
        """Verify all 12 facets of Patient 360 are populated."""
        p360 = Patient360Master.get_patient_360("PAT-774901")
        self.assertEqual(p360["mrn"], "MRN-2026-0001")
        self.assertEqual(p360["full_name"], "Hamza Farooqi")
        self.assertIn("mafasil", p360["organ_axes_status"])
        self.assertGreaterEqual(len(p360["active_nuskha"]), 1)
        self.assertGreaterEqual(len(p360["parhez_guidelines"]), 1)
        self.assertGreaterEqual(len(p360["tadbeer_sessions"]), 1)
        self.assertIn("uric_acid_trend", p360["biomarkers"])
        self.assertGreaterEqual(len(p360["proms_scores"]), 1)
        self.assertIn("current_phase", p360["care_plan"])
        self.assertIn("abdm_health_data_sharing", p360["consents"])
        self.assertGreaterEqual(len(p360["documents"]), 1)

    # 4. Care Plan OS Tests
    def test_04_longitudinal_care_plan_lifecycle(self):
        """Verify 90-day Metabolic Reset longitudinal care plan phases."""
        plan = CarePlanOSEngine.create_metabolic_reset_90("PAT-774901", "DOC-01")
        self.assertEqual(plan.program_name, "Metabolic & Musculoskeletal Reset 90 (MR-90)")
        self.assertEqual(len(plan.phases), 3)
        self.assertEqual(plan.phases[0].classical_unani_concept, "Munzij wa Mushil-e-Balgham (Coction & Evacuation of Phlegmatic Morbidity)")
        self.assertEqual(plan.phases[1].status, "ACTIVE")
        self.assertGreaterEqual(plan.adherence_overall_pct, 90.0)

    # 5. Canonical Terminology Service Tests
    def test_05_canonical_terminology_and_copy_sanitization(self):
        """Verify multi-tier audience mapping and zero mock leakage in patient text."""
        # Patient vs Clinician term
        pat_term = CanonicalTerminologyService.get_term_for_audience("CYP450_INTERACTION", "PATIENT")
        clin_term = CanonicalTerminologyService.get_term_for_audience("CYP450_INTERACTION", "CLINICIAN")
        self.assertEqual(pat_term, "Safety Check with Modern Medicines")
        self.assertEqual(clin_term, "Cytochrome P450 Herb-Drug Interaction Screening")

        # Copy compliance
        dirty_copy = "This mock patient record was retrieved from vector DB and Neo4j for simulation."
        audit = CanonicalTerminologyService.audit_copy_compliance(dirty_copy)
        self.assertFalse(audit["is_compliant"])
        self.assertIn("mock", audit["violations"])
        self.assertIn("vector db", audit["violations"])

        clean_preview = audit["sanitized_preview"]
        self.assertNotIn("mock", clean_preview.lower())
        self.assertNotIn("vector db", clean_preview.lower())

    # 6. Live API Endpoints Tests
    def test_06_live_api_task_endpoints(self):
        """Test GET /api/v1/tasks and POST /api/v1/tasks."""
        status, body = self._call_handler("GET", "/api/v1/tasks?role=DOCTOR")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertIn("tasks", body)

        status, body = self._call_handler("POST", "/api/v1/tasks", {
            "title": "Review Serum Uric Acid Repeat",
            "description": "Evaluate day-21 response to Munzij wa Mushil protocol",
            "owner_id": "DOC-01",
            "owner_role": "DOCTOR",
            "priority": "HIGH"
        })
        self.assertEqual(status, 201)
        self.assertTrue(body["ok"])
        self.assertIn("task", body)

    def test_07_live_api_patient_360_endpoint(self):
        """Test GET /api/v1/patient/360."""
        status, body = self._call_handler("GET", "/api/v1/patient/360?patient_id=PAT-774901")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(body["patient_360"]["mrn"], "MRN-2026-0001")

    def test_08_live_api_encounter_os_endpoints(self):
        """Test GET /api/v1/clinical/encounter/prepare and POST /api/v1/clinical/encounter/start."""
        status, body = self._call_handler("GET", "/api/v1/clinical/encounter/prepare?patient_id=PAT-774901&clinician_id=DOC-01")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertIn("pre_encounter_brief", body["pre_encounter"])

        status, body = self._call_handler("POST", "/api/v1/clinical/encounter/start", {
            "patient_id": "PAT-774901",
            "clinician_id": "DOC-01",
            "facility_id": "FAC-HQ-01"
        })
        self.assertEqual(status, 201)
        self.assertTrue(body["ok"])
        enc_id = body["encounter"]["encounter_id"]

        # Sign-off
        status, body = self._call_handler("POST", "/api/v1/clinical/encounter/sign-off", {
            "encounter_id": enc_id,
            "clinician_id": "DOC-01",
            "signing_pin": "991024"
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(body["status"], "SIGNED_OFF")

    def test_09_live_api_secure_messaging_and_emergency_triage(self):
        """Test POST /api/v1/communication/messages routine and emergency triage."""
        # Routine message
        status, body = self._call_handler("POST", "/api/v1/communication/messages", {
            "sender_id": "PAT-774901",
            "message": "Doctor sahab, should I take Roghan before or after bath?",
            "category": "MEDICATION"
        })
        self.assertEqual(status, 201)
        self.assertTrue(body["ok"])
        self.assertEqual(body["status"], "DELIVERED_TO_QUEUE")

        # Emergency red-flag message
        status, body = self._call_handler("POST", "/api/v1/communication/messages", {
            "sender_id": "PAT-774901",
            "message": "I am having sudden severe chest pain and severe breathlessness!",
            "category": "CLINICAL"
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertTrue(body["is_emergency_flagged"])
        self.assertEqual(body["triage_priority"], "STAT_EMERGENCY")
        self.assertIn("112", body["emergency_advisory"])

    def test_10_live_api_appointment_lifecycle_and_checkin(self):
        """Test GET /api/v1/appointments/patient/{id} and POST /api/v1/appointments/check-in."""
        # 1. Fetch appointments
        status, body = self._call_handler("GET", "/api/v1/appointments/patient/PAT-774901")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertGreaterEqual(body["count"], 1)
        apt = body["appointments"][0]
        apt_id = apt["appointment_id"]

        # 2. Digital Check-in
        status, body = self._call_handler("POST", "/api/v1/appointments/check-in", {
            "appointment_id": apt_id,
            "proms_score": 3.5
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(body["current_state"], "PRE_CHECKED_IN")

        # 3. Transition to WAITING_IN_OPD
        status, body = self._call_handler("POST", "/api/v1/appointments/transition", {
            "appointment_id": apt_id,
            "target_state": "WAITING_IN_OPD",
            "actor_id": "RECEPTIONIST-01",
            "notes": "Patient arrived at Matab OPD reception."
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(body["current_state"], "WAITING_IN_OPD")

    def test_11_live_api_lab_diagnostics_and_state_transition(self):
        """Test GET /api/v1/diagnostics/reports and POST /api/v1/diagnostics/transition."""
        # 1. Fetch lab reports
        status, body = self._call_handler("GET", "/api/v1/diagnostics/reports?patient_id=PAT-774901")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertGreaterEqual(body["count"], 1)
        rep = body["reports"][0]
        rep_id = rep["report_id"]

        # 2. Transition test state
        status, body = self._call_handler("POST", "/api/v1/diagnostics/transition", {
            "report_id": rep_id,
            "test_code": "URIC_ACID",
            "target_state": "ACTION_REQUIRED",
            "clinician_note": "Initiate Phase 1 Munzij wa Mushil with Hab-e-Suranjan."
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertEqual(body["new_state"], "ACTION_REQUIRED")

    def test_12_live_api_evidence_provenance_lookup(self):
        """Test GET /api/v1/evidence/lookup for authoritative 6-question dossier."""
        status, body = self._call_handler("GET", "/api/v1/evidence/lookup?entity=Suranjan%20Shirin")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertGreaterEqual(body["count"], 1)
        dossier = body["evidence_dossiers"][0]
        self.assertEqual(dossier["target_entity"], "Suranjan Shirin")
        self.assertIn("authoritative_source", dossier)
        self.assertIn("evidence_grade", dossier)
        self.assertIn("clinical_limitations", dossier)


if __name__ == "__main__":
    unittest.main()
