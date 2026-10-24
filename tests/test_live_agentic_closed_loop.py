#!/usr/bin/env python3
"""
ZAYVORA Health OS — Master Closed-Loop Agentic Continuum Integration Suite
==========================================================================
Validates the complete closed-loop execution across all 8 backend agentic pipelines:
1. TriageAgent: Autonomous Pre-Consultation Dossier & Vitals Grading
2. DiagnosticVisionAgent: Multimodal Tongue (Lisan) & Urine (Qaroorah) Staging
3. CanonResearchAgent: Semantic Treatise Crosswalk across 38 chapters & 250 UPI monographs
4. VoiceAgenticScribe: Ambient Vernacular Speech Parsing into Structured Nuskhas
5. PharmacyInventoryAgent: FEFO Expiry Surveillance & Schedule E(1) Mudabbar Firewall
6. ReinforcementAgent: Clinician Override Delta Tracking & Dynamic Preference Matrix
7. CareContinuityAgent: 5-Point Alamat-e-Nujz Concoction State Machine & Follow-up Scheduler
8. DeviceSyncEngine: Multi-Device Transactional Batch Ingestion & Delta Sync
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from tests.test_live_api_integration import DirectTestClient

class TestLiveAgenticClosedLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = DirectTestClient()
        cls.test_mrn = "PAT-E2E-AGENTIC-2026"

    def test_01_triage_agent_pre_consult_brief(self):
        """1. TriageAgent: Autonomous Pre-Consultation Dossier & Vitals Grading."""
        payload = {
            "mrn": self.test_mrn,
            "patient_name": "Tariq Mahmood",
            "age": 48,
            "gender": "Male",
            "vitals": {
                "bp": "138/88",
                "pulse": "76",
                "temp": "98.4",
                "spo2": "98",
                "bmi": "26.2"
            },
            "chief_complaint": "Joint stiffness in knees worse in cold weather",
            "mizaj": "Barid Balghami",
            "allopathic_meds": ["Atorvastatin 10mg"]
        }
        status, resp = self.client.request("POST", "/api/v1/clinical/agent/pre-consult-brief", payload)
        self.assertEqual(status, 200, f"TriageAgent failed: {resp}")
        self.assertTrue(resp.get("ok"))
        brief = resp.get("brief", {})
        self.assertIn("vitals_analysis", brief)
        self.assertIn("humoral_pathology", brief)
        self.assertIn("proposed_regimen", brief)

    def test_02_diagnostic_vision_agent_multimodal(self):
        """2. DiagnosticVisionAgent: Multimodal Tongue & Urine Concoction Analysis."""
        status_lisan, resp_lisan = self.client.request(
            "POST",
            "/api/v1/clinical/agent/vision/analyze",
            {"mrn": self.test_mrn, "modality": "TONGUE", "file_name": "lisan_white_thick.png"}
        )
        self.assertEqual(status_lisan, 200, f"Tongue vision failed: {resp_lisan}")
        self.assertTrue(resp_lisan.get("ok"))
        self.assertEqual(resp_lisan.get("modality"), "TONGUE")
        self.assertIn("chromatic_analysis", resp_lisan)

        # GET history
        status_get, resp_get = self.client.request("GET", f"/api/v1/clinical/agent/vision/analyses?mrn={self.test_mrn}")
        self.assertEqual(status_get, 200)
        self.assertTrue(resp_get.get("ok"))
        self.assertGreaterEqual(len(resp_get.get("analyses", [])), 1)

    def test_03_canon_research_agent_dossier(self):
        """3. CanonResearchAgent: Semantic Treatise Crosswalk across UPI & classical monographs."""
        status, resp = self.client.request(
            "POST",
            "/api/v1/research/agent/canonical-dossier",
            {"condition": "Waja-ul-Mafasil", "depth": "comprehensive"}
        )
        self.assertEqual(status, 200, f"CanonResearchAgent failed: {resp}")
        self.assertTrue(resp.get("ok"))
        dossier = resp.get("dossier", {})
        self.assertIn("matched_treatises", dossier)
        self.assertIn("validated_monographs", dossier)
        self.assertIn("markdown_content", dossier)

    def test_04_voice_agentic_scribe_prescription(self):
        """4. VoiceAgenticScribe: Ambient Vernacular Speech Parsing into Structured Nuskhas."""
        transcript_text = "Mareez ko joron me shadeed dard hai, subah jakdan rehti hai. Balghami mizaj hai. Majun Suranjan 5g subah shaam neem garam doodh se aur Roghan Suranjan local application likhein."
        status, resp = self.client.request(
            "POST",
            "/api/v1/clinical/agent/voice/transcribe-structure",
            {"transcript": transcript_text, "mrn": self.test_mrn}
        )
        self.assertEqual(status, 200, f"VoiceAgenticScribe failed: {resp}")
        self.assertTrue(resp.get("ok"))
        sdata = resp.get("structured_data", {})
        self.assertIn("chief_complaint", sdata)
        self.assertIn("extracted_medicines", sdata)
        self.assertGreater(len(sdata["extracted_medicines"]), 0)

    def test_05_pharmacy_inventory_agent_surveillance(self):
        """5. PharmacyInventoryAgent: FEFO Expiry Surveillance & Schedule E(1) Mudabbar Firewall."""
        status_fefo, resp_fefo = self.client.request("GET", "/api/v1/pharmacy/agent/inventory-audit")
        self.assertEqual(status_fefo, 200, f"FEFO surveillance failed: {resp_fefo}")
        self.assertTrue(resp_fefo.get("ok"))
        self.assertIn("summary", resp_fefo)
        self.assertGreaterEqual(resp_fefo["summary"]["total_active_lots"], 1)

    def test_06_reinforcement_agent_feedback_loop(self):
        """6. ReinforcementAgent: Clinician Override Delta Tracking & Preference Matrix."""
        payload = {
            "mrn": self.test_mrn,
            "doctor_id": "DOC-IRFAN",
            "formulation_name": "Majun Suranjan",
            "ai_proposed_dose": "5g BID",
            "doctor_prescribed_dose": "5g BID",
            "action_type": "ACCEPTED",
            "clinical_rationale": "Effective for Waja-ul-Mafasil flare",
            "organ_axis": "Test-Axis"
        }
        status, resp = self.client.request("POST", "/api/v1/clinical/agent/reinforcement/record-override", payload)
        self.assertEqual(status, 200, f"ReinforcementAgent failed: {resp}")
        self.assertTrue(resp.get("ok"))

        # Verify matrix updated
        status_m, resp_m = self.client.request("GET", "/api/v1/clinical/agent/reinforcement/matrix")
        self.assertEqual(status_m, 200)
        self.assertTrue(resp_m.get("ok"))
        self.assertIn("preferences", resp_m)

    def test_07_care_continuity_agent_followup(self):
        """7. CareContinuityAgent: 5-Point Alamat-e-Nujz Concoction State Machine & Follow-up."""
        payload = {
            "mrn": self.test_mrn,
            "day": 7,
            "adherence_confirmed": True,
            "qaroorah_sediment": "rasub_mahmood",
            "bowel_regular": True,
            "pulse_quality": "mutadil",
            "stiffness_resolved_pct": 100,
            "tongue_clearing": True,
            "notes": "Patient reports significant easing of knee stiffness and thick sediment observed."
        }
        status, resp = self.client.request("POST", "/api/v1/clinical/agent/care-continuity/evaluate-nujz", payload)
        self.assertEqual(status, 200, f"CareContinuityAgent failed: {resp}")
        self.assertTrue(resp.get("ok"))
        eval_data = resp.get("evaluation", {})
        self.assertGreaterEqual(eval_data.get("nujz_index_percent", 0), 80)
        self.assertTrue(eval_data.get("nujz_reached"))

    def test_08_device_sync_engine_telemetry(self):
        """8. DeviceSyncEngine: Multi-Device Batch Ingestion & Delta Sync."""
        batch_payload = {
            "device_id": "DEVICE-MOBILE-IPAD-01",
            "mutations": [
                {
                    "mutationId": "MUT-TEST-001",
                    "entityType": "vital_reading",
                    "patientId": self.test_mrn,
                    "data": {"bp": "128/84", "pulse": 76, "spo2": 99}
                }
            ]
        }
        status_batch, resp_batch = self.client.request("POST", "/api/v1/sync/batch", batch_payload)
        self.assertEqual(status_batch, 200, f"Sync batch failed: {resp_batch}")
        self.assertTrue(resp_batch.get("ok"))
        self.assertGreaterEqual(len(resp_batch.get("results", [])), 1)

        status_delta, resp_delta = self.client.request("GET", "/api/v1/sync/delta?since_version=0")
        self.assertEqual(status_delta, 200, f"Sync delta failed: {resp_delta}")
        self.assertTrue(resp_delta.get("ok"))
        self.assertIn("prescriptions", resp_delta)
        self.assertIn("care_continuity_plans", resp_delta)

if __name__ == "__main__":
    unittest.main()
