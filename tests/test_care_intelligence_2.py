#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Care Intelligence 2.0 Test Suite
====================================================
Tests the 4 focused Care Intelligence front-door engines:
  1. AI Care Orchestrator (Intent classification, safety red flag, desk routing)
  2. Smart Pre-Consultation Engine (Unstructured intake to 4-pillar doctor briefing)
  3. Care Gap & Adherence Intelligence Engine (Milestone, diagnostics, and refill gaps)
  4. Explain My Health Engine (Patient translation, warm bedside manner, biomarker clarity)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.ai.app.engines.patient_care_orchestrator import (
    PatientCareOrchestrator,
    CareIntentType
)
from services.clinical.app.engines.care_gap_engine import (
    CareGapIntelligenceEngine,
    CareGapSeverity
)
from services.ai.app.engines.smart_preconsult_engine import SmartPreConsultEngine
from services.ai.app.engines.patient_health_explainer import PatientHealthExplainer


class TestCareIntelligence2Suite(unittest.TestCase):

    def test_care_orchestrator_refill_routing(self):
        decision = PatientCareOrchestrator.process_inbound_message(
            patient_id="PAT-774901",
            message_text="Meri Suranjan Majoon ki dawai khatam ho gayi hai, refill bhej dein.",
            patient_context={"name": "Hamza Farooqi", "active_prescription_id": "RX-2026-0441"}
        )
        self.assertEqual(decision.intent, CareIntentType.MEDICINE_REFILL)
        self.assertEqual(decision.assigned_desk, "PHARMACY_REFILL_DESK")
        self.assertEqual(decision.target_action, "INITIATE_REFILL_TICKET")
        self.assertFalse(decision.is_emergency)
        self.assertIn("refill", decision.patient_response.lower())
        self.assertIn("RX-2026-0441", decision.ticket_payload["current_nuskha_id"])

    def test_care_orchestrator_emergency_red_flag_guard(self):
        decision = PatientCareOrchestrator.process_inbound_message(
            patient_id="PAT-774901",
            message_text="Mujhe severe chest pain aur shortness of breath ho raha hai.",
            patient_context={"name": "Hamza Farooqi"}
        )
        self.assertEqual(decision.intent, CareIntentType.EMERGENCY_RED_FLAG)
        self.assertTrue(decision.is_emergency)
        self.assertTrue(decision.escalation_required)
        self.assertEqual(decision.assigned_desk, "EMERGENCY_CLINICAL_ESCALATION")
        self.assertIn("STAT ALERT", decision.clinical_alert)
        self.assertIn("emergency", decision.patient_response.lower())

    def test_care_orchestrator_symptom_flare_doctor_alert(self):
        decision = PatientCareOrchestrator.process_inbound_message(
            patient_id="PAT-774901",
            message_text="Mere ghutne ka dard achanak barh gaya hai aur severe stiffness hai.",
            patient_context={"name": "Hamza Farooqi"}
        )
        self.assertEqual(decision.intent, CareIntentType.SYMPTOM_FLARE_UP)
        self.assertEqual(decision.assigned_desk, "DOCTOR_CLINICAL_DESK")
        self.assertTrue(decision.escalation_required)
        self.assertIsNotNone(decision.clinical_alert)

    def test_care_gap_engine_milestone_and_refill_detection(self):
        summary = CareGapIntelligenceEngine.evaluate_patient_care_gaps(
            patient_id="PAT-774901",
            patient_name="Hamza Farooqi",
            current_day_in_protocol=25,
            days_supply_issued=21,
            labs_completed=["CBC"],
            reported_adherence_pct=72.0
        )
        self.assertGreaterEqual(summary.total_gaps_count, 3)
        self.assertGreater(summary.urgent_count, 0)
        
        gap_types = [g.gap_type for g in summary.gaps]
        self.assertIn("MISSED_FOLLOW_UP", gap_types)
        self.assertIn("OVERDUE_DIAGNOSTICS", gap_types)
        self.assertIn("MEDICINE_DEPLETION_RISK", gap_types)
        self.assertIn("ADHERENCE_DEFICIT", gap_types)
        
        # Verify root cause hints exist
        for g in summary.gaps:
            self.assertTrue(len(g.potential_root_causes) > 0)
            self.assertTrue(len(g.recommended_clinical_action) > 10)

    def test_smart_preconsult_engine_intake(self):
        intake_text = (
            "Doctor sahab pichle 4 mahine se dono ghutno mein shadid dard aur subah akadpan rehta hai. "
            "Sardi mein dard barh jata hai. Kabhi kabhi Combiflam khata tha par ab asar kam hai."
        )
        briefing = SmartPreConsultEngine.generate_briefing(
            patient_id="PAT-774901",
            patient_name="Hamza Farooqi",
            unstructured_intake_text=intake_text
        )
        self.assertEqual(briefing.patient_id, "PAT-774901")
        self.assertEqual(briefing.readiness_status, "READY_FOR_CONSULT")
        self.assertIn("knee", briefing.chief_complaint_summary.lower())
        self.assertIn("Balgham", str(briefing.suspected_humoral_axis_clues))
        self.assertGreaterEqual(len(briefing.suggested_clinician_questions), 2)

    def test_patient_health_explainer_roman_urdu(self):
        dossier = PatientHealthExplainer.explain_health_summary(
            patient_id="PAT-774901",
            patient_name="Hamza Farooqi",
            diagnosis_title="Waja-ul-Mafasil",
            prescribed_nuskha="Majun Suranjan Special",
            language="roman_urdu"
        )
        self.assertEqual(dossier.language, "roman_urdu")
        self.assertIn("Hamza Farooqi", dossier.condition_explanation)
        self.assertIn("Majun Suranjan Special", dossier.why_this_medicine)
        self.assertGreaterEqual(len(dossier.daily_care_instructions), 2)
        self.assertGreaterEqual(len(dossier.lab_markers_simplified), 2)
        self.assertGreaterEqual(len(dossier.safety_red_flags_to_watch), 1)

    def test_patient_health_explainer_english(self):
        dossier = PatientHealthExplainer.explain_health_summary(
            patient_id="PAT-774901",
            patient_name="Hamza Farooqi",
            diagnosis_title="Waja-ul-Mafasil",
            prescribed_nuskha="Majun Suranjan Special",
            language="english"
        )
        self.assertEqual(dossier.language, "english")
        self.assertIn("Hamza Farooqi", dossier.condition_explanation)
        self.assertIn("hs-CRP", dossier.lab_markers_simplified[0]["marker"])


if __name__ == "__main__":
    unittest.main()
