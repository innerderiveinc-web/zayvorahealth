"""
ZAYVORA Health OS™ v5.0 — Certified Test Suite: Ilaj bil Ghiza & Ilaj bil Yad (Jarahat)
======================================================================================
Validates:
  1. Ilaj bil Ghiza Engine: Nutrient hierarchy, Ilaj bil-Zidd dietetics, food antagonisms,
     and canonical dietary preparations (Maa-ul-Sha'eer, Maa-ul-Jubn, Maa-ul-Asal).
  2. Ilaj bil Yad / Jarahat Engine: Classical operative modalities (Al-Zahrawi & Ibn al-Quff),
     fail-closed surgical safety barriers (BP, anemia, age, pregnancy), and styptic wound healers.
"""

import unittest

from services.therapeutic.app.engines.ilaj_bil_ghiza_engine import (
    CANONICAL_FOOD_ANTAGONISMS,
    CANONICAL_THERAPEUTIC_PREPARATIONS,
    NUTRIENT_CATEGORIES,
    IlajBilGhizaEngine,
)
from services.therapeutic.app.engines.ilaj_bil_yad_engine import (
    AL_ZAHRAWI_INSTRUMENTS,
    CICATRIZING_STYPTIC_FORMULARY,
    CLASSICAL_JARAHAT_MODALITIES,
    IlajBilYadEngine,
    SurgicalAssessmentInput,
)


class TestGhizaAndYadEngines(unittest.TestCase):
    """Certified test suite for Unani Dietotherapy and Classical Operative Surgery."""

    # -------------------------------------------------------------------------
    # PART 1: ILAJ BIL GHIZA (DIETOTHERAPY) TESTS
    # -------------------------------------------------------------------------

    def test_01_ghiza_nutrient_hierarchy_completeness(self):
        """Invariant: All 4 classical nutrient classes defined with authentic examples."""
        expected_classes = ["GHIZA_E_MUTLAQ", "GHIZA_E_DAWAI", "DAWA_E_GHIDHAI", "DAWA_E_MUTLAQ"]
        for cat in expected_classes:
            self.assertIn(cat, NUTRIENT_CATEGORIES)
            self.assertTrue(len(NUTRIENT_CATEGORIES[cat]["classical_examples"]) >= 3)

    def test_02_ghiza_ilaj_bil_zidd_hot_dyscrasia(self):
        """Invariant: Hot dyscrasia (Su-e-Mizaj Haar) prescribes cooling Barid-Ratab diet."""
        regimen = IlajBilGhizaEngine.formulate_dietary_regimen(
            patient_mizaj="Safrawi",
            su_e_mizaj="Su-e-Mizaj Haar",
            candidate_foods=["Barley", "Cucumber"]
        )
        self.assertEqual(regimen["status"], "APPROVED")
        self.assertIn("Barid-Ratab", regimen["prescribed_dietary_quality"])
        self.assertEqual(regimen["primary_therapeutic_preparation"]["name"], CANONICAL_THERAPEUTIC_PREPARATIONS["MAA_UL_SHAEER"]["name"])
        self.assertTrue(any("Maa-ul-Sha'eer" in f["name"] for f in regimen["recommended_foods"]))

    def test_03_ghiza_ilaj_bil_zidd_cold_dyscrasia(self):
        """Invariant: Cold dyscrasia (Su-e-Mizaj Barid) prescribes warming Haar diet."""
        regimen = IlajBilGhizaEngine.formulate_dietary_regimen(
            patient_mizaj="Balghami",
            su_e_mizaj="Su-e-Mizaj Barid"
        )
        self.assertEqual(regimen["status"], "APPROVED")
        self.assertIn("Haar", regimen["prescribed_dietary_quality"])
        self.assertEqual(regimen["primary_therapeutic_preparation"]["name"], CANONICAL_THERAPEUTIC_PREPARATIONS["MAA_UL_ASAL"]["name"])
        self.assertTrue(any("Ginger" in f["name"] or "Zanjabeel" in f["name"] for f in regimen["recommended_foods"]))

    def test_04_ghiza_tanafur_food_antagonisms(self):
        """Invariant: Classical toxic food incompatibilities (e.g. Fish + Milk) trigger severe hazard."""
        foods = ["Cooked Samak fish", "Fresh Cow Milk", "Barley bread"]
        antagonisms = IlajBilGhizaEngine.check_food_incompatibilities(foods)
        self.assertEqual(len(antagonisms), 1)
        self.assertEqual(antagonisms[0]["arabic_designation"], "Samak ma'a Laban")
        self.assertEqual(antagonisms[0]["hazard_level"], "SEVERE_PROHIBITION")

    def test_05_ghiza_canonical_preparations_grounding(self):
        """Invariant: All 6 classical preparations are historically cited from Ibn Sina, Razi, or Ibn Zuhr."""
        required = ["MAA_UL_SHAEER", "MAA_UL_JUBN", "MAA_UL_ASAL", "KESHK_AB", "HARIRAH_E_BADAAM", "SIKANJABEEN"]
        for key in required:
            self.assertIn(key, CANONICAL_THERAPEUTIC_PREPARATIONS)
            meta = CANONICAL_THERAPEUTIC_PREPARATIONS[key]
            self.assertTrue(len(meta["preparation_protocol"]) > 20)
            self.assertTrue("Al-Qanun" in meta["classical_reference"] or "Hawi" in meta["classical_reference"] or "Zuhr" in meta["classical_reference"] or "Shirazi" in meta["classical_reference"])

    # -------------------------------------------------------------------------
    # PART 2: ILAJ BIL YAD & JARAHAT (OPERATIVE SURGERY) TESTS
    # -------------------------------------------------------------------------

    def test_06_jarahat_modalities_catalog(self):
        """Invariant: All 7 classical surgical modalities from Al-Zahrawi and Ibn al-Quff are codified."""
        required_modalities = ["FASD", "HIJAMA_BI_AL_SHART", "TALEEQ", "KAI", "BATA", "JABR_E_NUQSAN", "BATAR"]
        for m in required_modalities:
            self.assertIn(m, CLASSICAL_JARAHAT_MODALITIES)
            meta = CLASSICAL_JARAHAT_MODALITIES[m]
            self.assertTrue("Al-Zahrawi" in meta["classical_authority"] or "Ibn al-Quff" in meta["classical_authority"] or "Al-Qanun" in meta["classical_authority"])

    def test_07_surgical_safety_barrier_hemodynamic_stability(self):
        """Invariant: Systolic blood pressure < 100 mmHg strictly blocks operative surgery/Fasd."""
        patient = SurgicalAssessmentInput(
            patient_id="P-SURG-01",
            age=32,
            gender="male",
            systolic_bp=88,  # Hypotensive
            diastolic_bp=56,
            hemoglobin_g_dl=13.0,
            is_pregnant=False,
            proposed_procedure="FASD",
            target_site="Basaliq",
            clinical_indication="Imtila Damwi"
        )
        res = IlajBilYadEngine.evaluate_surgical_safety(patient)
        self.assertFalse(res["is_approved"])
        self.assertEqual(res["status"], "BLOCKED_BY_SAFETY_FIREWALL")
        self.assertTrue(any("Hypotension" in c for c in res["contraindications_triggered"]))

    def test_08_surgical_safety_barrier_anemia(self):
        """Invariant: Hemoglobin < 10.0 g/dL strictly blocks blood-letting procedures."""
        patient = SurgicalAssessmentInput(
            patient_id="P-SURG-02",
            age=28,
            gender="female",
            systolic_bp=118,
            diastolic_bp=75,
            hemoglobin_g_dl=8.8,  # Anemic
            is_pregnant=False,
            proposed_procedure="HIJAMA_BI_AL_SHART",
            target_site="Kahil",
            clinical_indication="Myofascial pain"
        )
        res = IlajBilYadEngine.evaluate_surgical_safety(patient)
        self.assertFalse(res["is_approved"])
        self.assertTrue(any("Anemia" in c for c in res["contraindications_triggered"]))

    def test_09_surgical_safety_barrier_age_and_pregnancy(self):
        """Invariant: Pediatric (<14), Geriatric (>60), or Pregnancy blocks major Fasd."""
        pediatric_patient = SurgicalAssessmentInput(
            patient_id="P-SURG-03",
            age=10,  # Pediatric
            gender="male",
            systolic_bp=110,
            diastolic_bp=70,
            hemoglobin_g_dl=12.5,
            is_pregnant=False,
            proposed_procedure="FASD",
            target_site="Basaliq",
            clinical_indication="Headache"
        )
        res_ped = IlajBilYadEngine.evaluate_surgical_safety(pediatric_patient)
        self.assertFalse(res_ped["is_approved"])
        self.assertTrue(any("Age Invariant" in c for c in res_ped["contraindications_triggered"]))

        pregnant_patient = SurgicalAssessmentInput(
            patient_id="P-SURG-04",
            age=26,
            gender="female",
            systolic_bp=120,
            diastolic_bp=80,
            hemoglobin_g_dl=12.0,
            is_pregnant=True,  # Pregnant
            proposed_procedure="FASD",
            target_site="Basaliq",
            clinical_indication="Plethora"
        )
        res_preg = IlajBilYadEngine.evaluate_surgical_safety(pregnant_patient)
        self.assertFalse(res_preg["is_approved"])
        self.assertTrue(any("Pregnancy Contraindication" in c for c in res_preg["contraindications_triggered"]))

    def test_10_surgical_approved_procedure_with_styptics(self):
        """Invariant: Approved procedure provides Al-Zahrawi instrument protocol and Sang-e-Jarahat dressing."""
        patient = SurgicalAssessmentInput(
            patient_id="P-SURG-05",
            age=35,
            gender="male",
            systolic_bp=124,
            diastolic_bp=82,
            hemoglobin_g_dl=14.5,
            is_pregnant=False,
            proposed_procedure="FASD",
            target_site="Basaliq",
            clinical_indication="Imtila Damwi with severe temporal cephalea"
        )
        res = IlajBilYadEngine.evaluate_surgical_safety(patient)
        self.assertTrue(res["is_approved"])
        self.assertEqual(res["status"], "APPROVED_FOR_CLINICAL_SIGNATURE")
        self.assertEqual(len(res["contraindications_triggered"]), 0)
        self.assertTrue(any("Sang-e-Jarahat" in d["name"] for d in res["post_operative_dressing"]))
        self.assertIn("MIBZA", AL_ZAHRAWI_INSTRUMENTS)


if __name__ == "__main__":
    unittest.main()
