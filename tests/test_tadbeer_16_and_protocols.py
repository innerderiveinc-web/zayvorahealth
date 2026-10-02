"""
ZAYVORA Health OS™ — Automated Verification Suite for Ilaj bil Tadbeer (16 Modalities)
========================================================================================
Validates the clinical integrity, deterministic safety guardrails, 7 Usool-e-Tadbeer,
condition trajectories, and home-care protocols from Dr. Irfan Ashraf's treatises (2026).
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.therapeutic.app.engines.tadbeer_guardrails import (
    ACUTE_MEDICAL_RED_FLAGS,
    HOME_SELF_CARE_SPEC,
    MULTI_MODAL_TREATMENT_TRAJECTORIES,
    TADBEER_MODALITIES_16,
    USOOL_E_TADBEER_PRINCIPLES,
    run_tadbeer_guardrails,
)


class TestTadbeer16AndProtocols(unittest.TestCase):
    """Certified test suite for Ilaj bil Tadbeer (Regimental Therapy Engine)."""

    def test_01_sixteen_classical_modalities_completeness(self):
        """Validates that all 16 classical modalities are defined with descriptions and indications."""
        expected_modalities = [
            "Riyazat", "Dalak", "Hijama", "Fasd", "Taleeq", "Kai", "Hammam",
            "Takmeed", "Nutool", "Inkebab", "Ishal", "Qai", "Huqna", "Tareeq",
            "Idrar", "Aabzan"
        ]
        for mod in expected_modalities:
            self.assertIn(mod, TADBEER_MODALITIES_16, f"Missing classical modality: {mod}")
            data = TADBEER_MODALITIES_16[mod]
            self.assertIn("name", data)
            self.assertIn("classical_description", data)
            self.assertTrue(len(data.get("indications", [])) >= 2)
            self.assertTrue(len(data.get("contraindications", [])) >= 1)

    def test_02_seven_usool_e_tadbeer_principles(self):
        """Validates all 7 core therapeutic principles (Usool-e-Tadbeer) from Chapter 1."""
        expected_principles = ["Tanqiya", "Ta'deel", "Tahleel", "Taqwiyat", "Tabreed_Taskheen", "Tarteeb", "Tabyees"]
        for p in expected_principles:
            self.assertIn(p, USOOL_E_TADBEER_PRINCIPLES, f"Missing principle: {p}")
            self.assertTrue(len(USOOL_E_TADBEER_PRINCIPLES[p]) > 10)

    def test_03_acute_medical_red_flags_triage_barrier(self):
        """Validates that life-threatening red flags trigger immediate REFER and halt elective Tadbeer."""
        patient_with_chest_pain = {
            "age": 52,
            "chief_complaint": "Acute chest pain and shortness of breath since 2 hours",
            "comorbidities": ["Hypertension"]
        }
        res = run_tadbeer_guardrails(
            patient_context=patient_with_chest_pain,
            plan={"name": "Hijama bil-Shart", "method": "upper back"}
        )
        self.assertEqual(res["verdict"], "REFER")
        self.assertTrue(res.get("emergency_red_flag_triggered"))
        self.assertTrue(any("chest pain" in r.lower() for r in res["reasons"]))

        # Test high fever persisting
        patient_fever = {
            "age": 25,
            "chief_complaint": "High fever persisting >3 days with severe chills",
            "comorbidities": []
        }
        res_fever = run_tadbeer_guardrails(
            patient_context=patient_fever,
            plan={"name": "Hammam Haar"}
        )
        self.assertEqual(res_fever["verdict"], "REFER")

    def test_04_dvt_dalak_massage_hard_block(self):
        """Validates that suspected or documented DVT blocks medical massage to prevent pulmonary embolism."""
        patient_dvt = {
            "age": 45,
            "chief_complaint": "Right calf swelling and pain",
            "comorbidities": ["Deep vein thrombosis in lower extremity"]
        }
        res = run_tadbeer_guardrails(
            patient_context=patient_dvt,
            plan={"name": "Dalak-e-Sulb", "category": "massage"}
        )
        self.assertEqual(res["verdict"], "DO_NOT_RECOMMEND")
        self.assertTrue(any("pulmonary embolism" in r.lower() for r in res["reasons"]))

    def test_05_cauterization_kai_diabetes_block(self):
        """Validates that uncontrolled diabetes blocks cauterization (Kai) due to gangrene risk."""
        patient_diabetic = {
            "age": 60,
            "chief_complaint": "Chronic severe sciatica",
            "comorbidities": ["Uncontrolled diabetes", "Diabetic neuropathy"]
        }
        res = run_tadbeer_guardrails(
            patient_context=patient_diabetic,
            plan={"name": "Kai (Cauterization)", "method": "sciatic nerve locus"}
        )
        self.assertEqual(res["verdict"], "DO_NOT_RECOMMEND")
        self.assertTrue(any("gangrene" in r.lower() for r in res["reasons"]))

    def test_06_taleeq_leech_bleeding_disorder_block(self):
        """Validates that bleeding disorders or anticoagulants block leech therapy (Taleeq)."""
        patient_anticoag = {
            "age": 68,
            "chief_complaint": "Venous ulcer on ankle",
            "current_medications": ["Warfarin 5mg daily"],
            "comorbidities": ["Atrial fibrillation"]
        }
        res = run_tadbeer_guardrails(
            patient_context=patient_anticoag,
            plan={"name": "Taleeq (Leech therapy)", "method": "peri-ulcer margin"}
        )
        self.assertEqual(res["verdict"], "DO_NOT_RECOMMEND")
        self.assertTrue(any("hirudin" in r.lower() for r in res["reasons"]))

    def test_07_pediatric_and_geriatric_fasd_age_gates(self):
        """Validates Ibn Sina Canon age rules for Fasd (venesection): <14 and >60 prohibited."""
        child_patient = {"age": 10, "chief_complaint": "Facial plethora", "comorbidities": []}
        elder_patient = {"age": 65, "chief_complaint": "Hypertensive plethora", "comorbidities": []}
        adult_patient = {"age": 35, "chief_complaint": "Hypertensive plethora", "comorbidities": []}

        res_child = run_tadbeer_guardrails(patient_context=child_patient, plan={"name": "Fasd-e-Basilic"})
        self.assertEqual(res_child["verdict"], "DO_NOT_RECOMMEND")
        self.assertTrue(any("14 years" in r for r in res_child["reasons"]))

        res_elder = run_tadbeer_guardrails(patient_context=elder_patient, plan={"name": "Fasd-e-Cephalic"})
        self.assertEqual(res_elder["verdict"], "DO_NOT_RECOMMEND")
        self.assertTrue(any("60 years" in r for r in res_elder["reasons"]))

        res_adult = run_tadbeer_guardrails(patient_context=adult_patient, plan={"name": "Fasd-e-Median"})
        self.assertEqual(res_adult["verdict"], "SAFE_TO_CONSIDER")

    def test_08_multi_modal_ibs_mizaj_divergent_protocols(self):
        """Validates that Balghami IBS gets warming/drying while Safrawi IBS gets cooling/moistening."""
        ibs_proto = MULTI_MODAL_TREATMENT_TRAJECTORIES["IBS_Mizaj_Divergent"]
        balghami = ibs_proto["sub_protocols"]["Balghami_IBS"]
        safrawi = ibs_proto["sub_protocols"]["Safrawi_IBS"]

        # Balghami regimen checks
        self.assertEqual(balghami["mizaj_type"], "Cold & Moist (Phlegmatic)")
        b_regimen_str = " ".join(balghami["regimen"]).lower()
        self.assertIn("ginger", b_regimen_str)
        self.assertIn("warm", b_regimen_str)

        # Safrawi regimen checks
        self.assertEqual(safrawi["mizaj_type"], "Hot & Dry (Choleric)")
        s_regimen_str = " ".join(safrawi["regimen"]).lower()
        self.assertIn("cooling", s_regimen_str)
        self.assertIn("rose", s_regimen_str)

    def test_09_chronic_lower_back_pain_multi_modal_trajectory(self):
        """Validates multi-phase protocol for chronic back pain (Dalak -> Takmeed -> Hijama -> Riyazat)."""
        back_proto = MULTI_MODAL_TREATMENT_TRAJECTORIES["Chronic_Low_Back_Pain"]
        self.assertEqual(back_proto["protocol_id"], "PROTO-TADB-001")
        w1_2 = back_proto["phases"]["Week_1_to_2"]
        self.assertIn("Dalak", w1_2)
        self.assertIn("Takmeed", w1_2)
        w3_4 = back_proto["phases"]["Week_3_to_4"]
        self.assertIn("Hijama", w3_4)

    def test_10_home_based_self_care_spec_and_belly_massage(self):
        """Validates the under-₹500 basic kit and clockwise belly massage protocol."""
        kit = HOME_SELF_CARE_SPEC["basic_kit_under_500_inr"]
        total_cost = sum(item["cost_est"] for item in kit)
        self.assertLessEqual(total_cost, 500)

        belly_massage = HOME_SELF_CARE_SPEC["clockwise_belly_massage_protocol"]
        self.assertEqual(belly_massage["duration_minutes"], 10)
        instructions = " ".join(belly_massage["instructions"])
        self.assertIn("clockwise", instructions.lower())
        self.assertIn("ascending", belly_massage["purpose"].lower())


if __name__ == "__main__":
    unittest.main()
