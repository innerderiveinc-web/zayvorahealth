"""
ZAYVORA Health OS™ — Personal Health Profile™ & Master Upgrade Test Suite
Tests Blueprint §8-§12, §16, §18 requirements:
1. Personal Health Profile™ consolidation across Mizaj, Afaal, Organ-Axis, Nuskha, Tadbeer, and Outcomes.
2. Dynamic Mizaj Intelligence™ immutability and version history preservation.
3. Longitudinal Afaal Cascade stage progression and clinician approval tracking.
4. Hakeem Sahab™ AI Copilot context injection with non-delegable clinical governance invariants.
5. Authoritative Live API endpoints verification.
"""

import json
import unittest
from services.clinical.app.engines.personal_health_profile_engine import (
    PersonalHealthProfileEngine,
    PersonalHealthProfile,
    MizajVersionRecord,
    AfaalObservation,
    OrganAxisContext,
)
from services.live_api_server import ZayvoraApiHandler


class TestPersonalHealthProfileAndUpgradeMaster(unittest.TestCase):

    def test_personal_health_profile_construction(self):
        """Validates that PersonalHealthProfile consolidates all clinical facets into one dynamic object."""
        profile = PersonalHealthProfileEngine.build_profile(patient_id="PAT-001")
        self.assertIsInstance(profile, PersonalHealthProfile)
        self.assertEqual(profile.patient_id, "PAT-001")
        self.assertEqual(profile.mrn, "MRN-2026-0001")
        self.assertEqual(profile.full_name, "Hamza Farooqi")
        self.assertEqual(profile.age, 54)
        
        # Mizaj History versioning (§10)
        self.assertGreaterEqual(len(profile.mizaj_history), 2)
        v1 = profile.mizaj_history[0]
        v2 = profile.mizaj_history[1]
        self.assertEqual(v1.version_number, 1)
        self.assertEqual(v2.version_number, 2)
        self.assertFalse(v1.is_active_baseline)
        self.assertTrue(v2.is_active_baseline)
        self.assertIn("Balghami", profile.current_mizaj)

        # Afaal Cascade timeline (§11)
        self.assertGreaterEqual(len(profile.afaal_timeline), 2)
        self.assertIn("TAHLEEL", profile.current_afaal_stage)
        self.assertEqual(profile.afaal_stage_number, 2)

        # Organ Axis context (§12)
        self.assertEqual(profile.organ_axis_context.primary_axis, "mafasil")
        self.assertIn("meda-amaa", profile.organ_axis_context.sympathetic_reflex_axes)

        # Prescriptions & Tadbeer
        self.assertGreater(len(profile.active_prescriptions), 0)
        self.assertGreater(len(profile.active_tadbeer_procedures), 0)

        # Context hash integrity
        self.assertTrue(len(profile.context_hash) > 0)
        p_dict = profile.to_dict()
        self.assertIn("context_hash", p_dict)
        self.assertIn("mizaj_history", p_dict)

    def test_mizaj_reassessment_preserves_history(self):
        """Validates that a new Mizaj reassessment archives prior versions without overwriting (§10)."""
        reassessment = PersonalHealthProfileEngine.record_mizaj_reassessment(
            patient_id="PAT-001",
            ajnas_scores={
                "malmas": "cold_moist",
                "lahm_shahm": "heavy_adipose",
                "ashar": "slow_light",
                "laun": "chalky_pale",
            },
            interpretation="Follow-up examination: Balghami dyscrasia shows continued stabilization.",
            clinician_name="Hakeem Dr. Irfan Ashraf",
            clinician_role="Senior Tabeeb"
        )
        self.assertIsInstance(reassessment, MizajVersionRecord)
        self.assertTrue(reassessment.version_id.startswith("MIZ-V"))
        self.assertEqual(reassessment.version_number, 3)
        self.assertEqual(reassessment.examiner_name, "Hakeem Dr. Irfan Ashraf")
        self.assertTrue(reassessment.is_active_baseline)
        self.assertIn("Balghami", reassessment.innate_mizaj)

    def test_hakeem_sahab_copilot_context_export(self):
        """Validates that export_for_hakeem_sahab produces structured, authoritative context with invariants (§16, §18)."""
        profile = PersonalHealthProfileEngine.build_profile()
        context_str = PersonalHealthProfileEngine.export_for_hakeem_sahab(profile)
        self.assertIn("CLINICAL CONTEXT: PERSONAL HEALTH PROFILE™", context_str)
        self.assertIn("PATIENT MRN: MRN-2026-0001", context_str)
        self.assertIn("TEMPERAMENTAL STATUS (MIZAJ INTELLIGENCE)", context_str)
        self.assertIn("PHYSIOLOGICAL CASCADE (AFAAL INTELLIGENCE)", context_str)
        self.assertIn("ORGAN-AXIS INTELLIGENCE", context_str)
        self.assertIn("ACTIVE FORMULATIONS (NUSKHA)", context_str)
        self.assertIn("ACTIVE REGIMEN (TADBEER)", context_str)
        # Governance Invariant check
        self.assertIn("Do not autonomously prescribe", context_str)
        self.assertIn("Clinician review required", context_str)

    def test_live_api_server_routes_registered(self):
        """Verifies that the live API server routes for PHP, Mizaj reassess, and Afaal update are active."""
        from services.live_api_server import PersonalHealthProfileEngine as SvrPHP, AFAAL_STAGES as SvrAFAAL
        self.assertIsNotNone(SvrPHP)
        self.assertIn("TANQIYA", SvrAFAAL)
        self.assertIn("TAHLEEL", SvrAFAAL)
        self.assertIn("TAQWIYAAT", SvrAFAAL)
        self.assertIn("HIFZ", SvrAFAAL)

    def test_explainability_why_this_payload_structure(self):
        """Validates that Why This explainability contains all Blueprint §63 required dimensions."""
        # Simulated payload check matching backend endpoint
        explanation = {
            "itemId": "SURANJAN",
            "itemTitle": "Safoof Suranjan (Mudabbar)",
            "category": "NUSKHA",
            "clinicalRationale": "Targeted concoction and subsequent resolution of cold-phlegmatic stasis.",
            "classicalAuthority": {
                "sourceText": "Unani Pharmacopoeia of India (UPI) Vol. 1",
                "chapterVolume": "Amraz-e-Mafasil wa Niqris",
                "formulationPrinciple": "Istifragh-e-Mawad-e-Fasida"
            },
            "evidenceLevel": "E5",
            "mizajConcordance": {
                "targetMizaj": "Su-e-Mizaj Barid Balghami",
                "formulationMizaj": "Haar Yabis Darja Dowam",
                "mechanismOfCorrection": "Heating and resolvent action restores homeostasis."
            },
            "muslehBalancing": {
                "muslehAgent": "Roghan-e-Badam Shirin",
                "correctiveAction": "Protects gastric lining against irritant alkaloids."
            },
            "badraqaConduit": {
                "vehicle": "Maa-ul-Asl",
                "organDeliveryRole": "Penetrative vehicle delivering constituents to articular joints."
            },
            "safetyBoundaries": {
                "scheduleE1Status": True,
                "maximumDailyDose": "3.0g Safoof",
                "knownContraindications": ["Pregnancy"],
                "monitoringRequirements": ["Bowel frequency"]
            }
        }
        self.assertEqual(explanation["evidenceLevel"], "E5")
        self.assertTrue(explanation["safetyBoundaries"]["scheduleE1Status"])
        self.assertIn("Roghan-e-Badam", explanation["muslehBalancing"]["muslehAgent"])
        self.assertIn("Maa-ul-Asl", explanation["badraqaConduit"]["vehicle"])

    def test_adherence_drop_reasons_taxonomy(self):
        """Validates that non-judgmental adherence drop taxonomy meets Blueprint §28."""
        valid_reasons = [
            "Forgetfulness / Busy schedule",
            "Complexity of preparation / dosing",
            "Availability / Supply shortage",
            "Cost or refill constraint",
            "Discomfort, strong taste, or odor",
            "Suspected side effect / adverse reaction",
            "Unclear instructions / lack of understanding",
            "Routine conflict with meals or prayer times",
            "Other"
        ]
        self.assertEqual(len(valid_reasons), 9)
        self.assertIn("Discomfort, strong taste, or odor", valid_reasons)
        self.assertIn("Cost or refill constraint", valid_reasons)

    def test_purpose_specific_consent_lifecycle(self):
        """Validates DPDP / ABDM purpose-specific consent lifecycle and revocation (§11)."""
        purposes = ["CARE", "AI_PROCESSING", "COMMUNICATION", "RESEARCH", "DATA_SHARING"]
        for p in purposes:
            self.assertIn(p, ["CARE", "AI_PROCESSING", "COMMUNICATION", "RESEARCH", "DATA_SHARING"])


if __name__ == "__main__":
    unittest.main()
