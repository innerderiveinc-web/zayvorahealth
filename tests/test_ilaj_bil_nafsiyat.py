"""
ZAYVORA Health OS™ — Automated Verification Suite for Ilaj bil Nafsiyat
=======================================================================
Validates the clinical integrity, deterministic safety barrier, and case
protocols from Dr. Irfan Ashraf's treatise: "ILAJ BIL NAFSIYAT" (2026).
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.clinical.app.engines.ilaj_bil_nafsiyat_engine import (
    CLASSICAL_NAFSIYAT_TAXONOMY,
    CRISIS_KEYWORDS,
    ITRAFAT_AROMATHERAPY_CATALOG,
    TANAFFUS_BREATHWORK_PROTOCOLS,
    VERIFIED_CASE_STUDY_PROTOCOLS,
    IlajBilNafsiyatEngine,
    NafsiyatAssessmentInput,
)
from services.therapeutic.app.engines.ilaj_hierarchy_engine import (
    evaluate_ilaj_hierarchy_compliance,
)


class TestIlajBilNafsiyat(unittest.TestCase):
    """Certified test suite for Ilaj bil Nafsiyat (Unani Psychological Medicine)."""

    def test_01_psychiatric_safety_barrier_suicidal_intent(self):
        """Invariant: Suicidal ideation immediately blocks elective care and diverts to emergency."""
        text = "Patient feels deeply hopeless and has expressed suicidal thoughts."
        safety = IlajBilNafsiyatEngine.evaluate_psychiatric_safety(text)
        self.assertIsNotNone(safety)
        self.assertEqual(safety["verdict"], "EMERGENCY_PSYCHIATRIC_DIVERSION")
        self.assertEqual(safety["safety_status"], "BLOCK_ELECTIVE_PRESCRIBING")
        self.assertIn("suicidal", safety["triggered_red_flags"])
        self.assertIn("emergency_action", safety)
        self.assertIn("emergency medical facility", safety["emergency_action"].lower())

    def test_02_psychiatric_safety_barrier_psychosis(self):
        """Invariant: Psychotic hallucinations trigger fail-closed diversion."""
        text = "Patient reports hearing voices and severe paranoia about neighbors."
        safety = IlajBilNafsiyatEngine.evaluate_psychiatric_safety(text)
        self.assertIsNotNone(safety)
        self.assertEqual(safety["verdict"], "EMERGENCY_PSYCHIATRIC_DIVERSION")
        self.assertTrue(any(kw in ["hearing voices", "paranoia"] for kw in safety["triggered_red_flags"]))

    def test_03_classical_psychiatric_taxonomy_completeness(self):
        """Validates all 8 classical psychiatric entities have ICD-11, SNOMED, and Unani humors."""
        required_entities = ["Wahm", "Juzn", "Sauda_Ghalib", "Izterab", "Sahar", "Nisyan", "Ghazab", "Khauf"]
        for key in required_entities:
            self.assertIn(key, CLASSICAL_NAFSIYAT_TAXONOMY, f"Missing entity: {key}")
            meta = CLASSICAL_NAFSIYAT_TAXONOMY[key]
            self.assertTrue(meta["icd11_code"].isalnum() or "." in meta["icd11_code"])
            self.assertTrue(meta["snomed_ct"].isdigit())
            self.assertIn("primary_humor", meta)
            self.assertIn("pathophysiology_unani", meta)
            self.assertTrue(len(meta["key_symptoms"]) >= 3)

    def test_04_diagnostic_matching_wahm_and_sahar(self):
        """Tests symptom-based differential diagnosis for anxiety and insomnia."""
        complaint = "Constant what-if thinking, nervous tremors, and inability to sleep."
        symptoms = ["Excessive worry", "Difficulty falling asleep", "Tension headaches"]
        diag = IlajBilNafsiyatEngine.diagnose_condition(symptoms, complaint)
        primary = diag["primary_diagnosis"]
        self.assertIn(primary["entity_key"], ["Wahm", "Sahar"])
        self.assertTrue(primary["match_confidence"] > 0.5)

    def test_05_root_cause_analysis_asbab_nafsaniyah(self):
        """Evaluates 6 root causes from Chapter 6 of the treatise."""
        inp = NafsiyatAssessmentInput(
            patient_id="P-101",
            age=32,
            gender="Female",
            chief_complaint="Chest heaviness and isolation",
            stress_level="SEVERE",
            sleep_hours=4.5,
            social_isolation=True,
            spiritual_disconnection=True,
            grief_or_trauma_present=True,
            emotional_suppression_present=True
        )
        causes = IlajBilNafsiyatEngine.evaluate_root_causes(inp)
        self.assertEqual(causes["total_root_causes_identified"], 6)
        cause_ids = [c["cause_id"] for c in causes["primary_causes"]]
        self.assertIn("Huzn-e-Shadeed", cause_ids)
        self.assertIn("Izterab-e-Muttasil", cause_ids)
        self.assertIn("Tanhai", cause_ids)
        self.assertIn("Batini_Khushi_ki_Kami", cause_ids)
        self.assertIn("Jazabat_ka_Dabna", cause_ids)
        self.assertIn("Su-e-Tadbeer_Naum", cause_ids)

    def test_06_itrafat_aromatherapy_matrix_temperament_matching(self):
        """Tests cooling aromatherapy for Safrawi and warming for Saudawi."""
        # Safrawi (Hot) should receive cooling herbs (Sandal / Gulab)
        hot_input = NafsiyatAssessmentInput(
            patient_id="P-HOT",
            age=28,
            gender="Male",
            chief_complaint="Severe anger flares and irritability",
            current_mizaj="Safrawi",
            stress_level="SEVERE"
        )
        hot_plan = IlajBilNafsiyatEngine.generate_care_plan(hot_input)
        hot_aromas = [a["name"] for a in hot_plan["prescribed_aroma_itrafat"]]
        self.assertTrue(any("Sandalwood" in name for name in hot_aromas))
        self.assertTrue(any("Rose" in name for name in hot_aromas))

        # Saudawi (Cold & Dry) should receive warming herbs (Ustukhuddus / Zafran)
        cold_input = NafsiyatAssessmentInput(
            patient_id="P-COLD",
            age=50,
            gender="Female",
            chief_complaint="Deep melancholy and cold grief",
            current_mizaj="Saudawi",
            grief_or_trauma_present=True
        )
        cold_plan = IlajBilNafsiyatEngine.generate_care_plan(cold_input)
        cold_aromas = [a["name"] for a in cold_plan["prescribed_aroma_itrafat"]]
        self.assertTrue(any("Lavender" in name for name in cold_aromas))
        self.assertTrue(any("Saffron" in name for name in cold_aromas))

    def test_07_case_study_protocol_1_grieving_mother(self):
        """Validates Case 1 (Fatima, 45 — Bereavement & Huzn-e-Shadeed)."""
        proto = VERIFIED_CASE_STUDY_PROTOCOLS["Grieving_Mother"]
        self.assertEqual(proto["code"], "PROTO-NAFS-001")
        self.assertIn("Fatima", proto["reference_case"])
        herbs = " ".join(proto["interventions"]["herbal_therapy"])
        self.assertIn("Arq-e-Gulab", herbs)
        self.assertIn("Ustukhuddus", herbs)
        self.assertIn("Zafran", herbs)
        self.assertIn("Asgandh", herbs)
        regimen = " ".join(proto["interventions"]["tadbeer_regimen"])
        self.assertIn("Istima", regimen)
        self.assertIn("Journaling", regimen)

    def test_08_case_study_protocol_2_anxious_student(self):
        """Validates Case 2 (Ahmed, 22 — University Exam Panic / Wahm)."""
        proto = VERIFIED_CASE_STUDY_PROTOCOLS["Anxious_Student"]
        self.assertEqual(proto["code"], "PROTO-NAFS-002")
        self.assertIn("Ahmed", proto["reference_case"])
        herbs = " ".join(proto["interventions"]["herbal_therapy"])
        self.assertIn("Coriander", herbs)
        self.assertIn("Rose syrup", herbs)
        self.assertIn("Brahmi", herbs)
        regimen = " ".join(proto["interventions"]["tadbeer_regimen"])
        self.assertIn("4-7-8 Vagal Breathing", regimen)

    def test_09_case_study_protocol_3_burned_out_professional(self):
        """Validates Case 3 (Sarah, 35 — Corporate Executive Burnout & Liver Heat)."""
        proto = VERIFIED_CASE_STUDY_PROTOCOLS["Burned_Out_Professional"]
        self.assertEqual(proto["code"], "PROTO-NAFS-003")
        self.assertIn("Sarah", proto["reference_case"])
        herbs = " ".join(proto["interventions"]["herbal_therapy"])
        self.assertIn("Rose", herbs)
        self.assertIn("Coriander", herbs)
        self.assertIn("Triphala", herbs)
        regimen = " ".join(proto["interventions"]["tadbeer_regimen"])
        self.assertIn("Hijama bila-Shart", regimen)
        self.assertIn("7:00 PM", regimen)

    def test_10_daily_life_regimen_structure(self):
        """Validates Chapter 11 Daily Life Routines (Subah, Din, Shaam, Mausam)."""
        inp = NafsiyatAssessmentInput(
            patient_id="P-ROUTINE",
            age=30,
            gender="Male",
            chief_complaint="General stress and burnout"
        )
        plan = IlajBilNafsiyatEngine.generate_care_plan(inp)
        routine = plan["daily_life_regimen"]
        self.assertIn("Subah_ki_Aadat", routine)
        self.assertIn("Din_ki_Aadat", routine)
        self.assertIn("Shaam_ki_Aadat", routine)
        self.assertIn("Mausam_ke_Mutabiq_Adjustment", routine)
        subah_text = " ".join(routine["Subah_ki_Aadat"])
        self.assertIn("Baad-e-Fajr", subah_text)
        self.assertIn("Badam Shirin", subah_text)
        din_text = " ".join(routine["Din_ki_Aadat"])
        self.assertIn("Qaylulah", din_text)

    def test_11_hierarchy_engine_nafsiyat_linkage(self):
        """Validates that IlajHierarchyEngine flags unaddressed Nafsiyat and cites the 2026 treatise."""
        res = evaluate_ilaj_hierarchy_compliance(
            prescribed_dawa=[{"herb": "Asgandh", "dose": 3.0}],
            tadbeer_prescriptions=["Riyazat 30 mins"],
            ghiza_parhez_prescribed=True,
            nafsiyat_addressed=False
        )
        self.assertTrue(res["is_hierarchy_compliant"])
        self.assertEqual(res["nafsiyat_status"], "NEEDS_EVALUATION")
        recs = " ".join(res["recommendations"])
        self.assertIn("Nafsiyat Consideration", recs)
        self.assertIn("Dr. Irfan Ashraf", recs)


if __name__ == "__main__":
    unittest.main()
