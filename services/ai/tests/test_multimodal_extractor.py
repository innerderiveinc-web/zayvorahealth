"""
Unit Tests for Multimodal AI Lab Report Extractor & Physical Signs Analyzer
Master Build Prompt v4.0 Phase 29 (Horizon 3: Clinical & AI Runtime Intelligence)
"""

import unittest
from app.multimodal.lab_report_extractor import (
    LabReportExtractor,
    PhysicalSignsAnalyzer,
    LOINC_DEFINITIONS,
)


class TestMultimodalLabExtractor(unittest.TestCase):
    def test_loinc_definitions_completeness(self):
        """Verify all mandatory LOINC analytes are registered with Unani humoral correlations."""
        mandatory_loincs = ["1558-6", "4548-4", "2160-0", "33914-3", "3084-1", "1975-2", "1742-6", "1920-8", "30341-2", "30522-7"]
        for code in mandatory_loincs:
            self.assertIn(code, LOINC_DEFINITIONS)
            meta = LOINC_DEFINITIONS[code]
            self.assertIn("analyte", meta)
            self.assertIn("unani_humoral_correlation", meta)
            self.assertIn("organ_axis", meta)

    def test_raw_text_extraction_and_dual_synthesis(self):
        """Verify parsing of laboratory report text into structured LOINC analytes and Unani humoral correlates."""
        sample_lab_text = """
        PATHOLOGY LABORATORY REPORT
        Patient: Ahmad Khan, Age: 52, Male
        ------------------------------------------
        Fasting Blood Glucose: 168 mg/dL (Ref: 70 - 99)
        HbA1c: 8.4 % (Ref: 4.0 - 5.6)
        Serum Creatinine: 1.1 mg/dL (Ref: 0.6 - 1.2)
        Serum Uric Acid: 8.6 mg/dL (Ref: 3.5 - 7.2)
        Total Bilirubin: 0.8 mg/dL (Ref: 0.2 - 1.2)
        ALT: 32 U/L (Ref: 7 - 56)
        AST: 28 U/L (Ref: 10 - 40)
        ESR: 35 mm/hr (Ref: 0 - 20)
        hs-CRP: 3.8 mg/L (Ref: 0.0 - 1.0)
        """
        result = LabReportExtractor.extract_from_text(sample_lab_text, patient_age=52, patient_gender="M")

        # Invariant checks
        self.assertFalse(result.safe_to_lock, "Master Invariant: safe_to_lock MUST be False until signed by clinician.")
        self.assertTrue(result.requires_clinician_signoff)

        # Verify extracted analytes
        extracted_codes = {a.loinc_code for a in result.analytes}
        self.assertIn("1558-6", extracted_codes)  # Fasting glucose
        self.assertIn("4548-4", extracted_codes)  # HbA1c
        self.assertIn("2160-0", extracted_codes)  # Creatinine
        self.assertIn("3084-1", extracted_codes)  # Uric acid
        self.assertIn("30341-2", extracted_codes)  # ESR
        self.assertIn("30522-7", extracted_codes)  # hs-CRP
        self.assertIn("33914-3", extracted_codes)  # Calculated eGFR

        # Check interpretations
        glucose_analyte = next(a for a in result.analytes if a.loinc_code == "1558-6")
        self.assertEqual(glucose_analyte.interpretation, "HIGH")

        uric_analyte = next(a for a in result.analytes if a.loinc_code == "3084-1")
        self.assertEqual(uric_analyte.interpretation, "HIGH")
        self.assertIn("Niqras", uric_analyte.unani_humoral_correlation)

        # Check humoral synthesis
        self.assertIn("Niqras (Gout / Hyperuricemia)", result.humoral_synthesis.pathological_entities)
        self.assertIn("Zia-e-Baitus Shakari (Metabolic Dysregulation)", result.humoral_synthesis.pathological_entities)
        self.assertEqual(result.humoral_synthesis.inflammatory_status, "Severe (Hararat-e-Ghariba)")

    def test_ckd_epi_egfr_and_renal_safety_profile(self):
        """Verify automated CKD-EPI eGFR calculation and renal posology scaling."""
        # Patient with elevated creatinine 1.8 mg/dL at age 50
        result = LabReportExtractor.extract_from_text(
            "Serum Creatinine: 1.8 mg/dL",
            patient_age=50,
            patient_gender="M",
        )
        self.assertIsNotNone(result.renal_safety)
        self.assertLess(result.renal_safety.egfr_value, 60.0)
        self.assertGreaterEqual(result.renal_safety.egfr_value, 30.0)
        self.assertTrue(result.renal_safety.requires_dose_adjustment)
        self.assertIn("Stage 3", result.renal_safety.renal_stage)
        self.assertEqual(result.renal_safety.recommended_dose_scaling_factor, 0.5)
        self.assertIn("Suranjan Talkh (Colchicum autumnale)", result.renal_safety.contraindicated_herbs)

    def test_structured_measurements_extraction(self):
        """Verify normalization of structured measurement payloads."""
        payload = [
            {"loinc_code": "1975-2", "analyte_name": "Total Bilirubin", "measured_value": 3.2, "unit": "mg/dL"},
            {"loinc_code": "1742-6", "analyte_name": "ALT", "measured_value": 115.0, "unit": "U/L"},
            {"loinc_code": "1920-8", "analyte_name": "AST", "measured_value": 98.0, "unit": "U/L"},
        ]
        result = LabReportExtractor.extract_from_measurements(payload, patient_age=38, patient_gender="F")
        self.assertFalse(result.safe_to_lock)
        self.assertEqual(len(result.analytes), 3)

        # Hepatobiliary heat and Safra dominance
        self.assertIn("Safra (Yellow Bile)", result.humoral_synthesis.dominant_humor_burden)
        self.assertIn("Su-i-Mizaj Safrawi Haar Yabis (Hepatobiliary Heat)", result.humoral_synthesis.pathological_entities)


class TestMultimodalPhysicalSignsAnalyzer(unittest.TestCase):
    def test_tongue_signs_semiotic_mapping(self):
        """Verify tongue inspection signs are correctly classified into Unani humors."""
        # Yellow dry coat
        res_safra = PhysicalSignsAnalyzer.analyze_physical_signs(
            tongue_notes="Thick yellow coat with prominent dry fissured surface (Asfar Yabis)."
        )
        self.assertFalse(res_safra.safe_to_lock)
        self.assertIsNotNone(res_safra.tongue_finding)
        self.assertEqual(res_safra.tongue_finding.coating_color, "Yellow (Asfar)")
        self.assertIn("Safra", res_safra.tongue_finding.humoral_inference)
        self.assertIn("Hammam (Moist steam bath)", res_safra.suggested_tadbeer)

        # White thick moist coat
        res_balgham = PhysicalSignsAnalyzer.analyze_physical_signs(
            tongue_notes="Pale swollen tongue with white thick creamy coat (Abyaz Ratab)."
        )
        self.assertFalse(res_balgham.safe_to_lock)
        self.assertEqual(res_balgham.tongue_finding.coating_color, "White Thick (Abyaz)")
        self.assertIn("Balgham", res_balgham.tongue_finding.humoral_inference)
        self.assertIn("Tanqiya-e-Balgham", res_balgham.suggested_tadbeer)

    def test_skin_signs_dermatological_mapping(self):
        """Verify classical Unani skin lesions are mapped to correct clinical entities."""
        # Vitiligo / Bars
        res_bars = PhysicalSignsAnalyzer.analyze_physical_signs(
            skin_notes="Well-circumscribed depigmented white macules on bilateral extensor surfaces, suspected Bars."
        )
        self.assertFalse(res_bars.safe_to_lock)
        self.assertIsNotNone(res_bars.skin_finding)
        self.assertIn("Bars (Vitiligo)", res_bars.skin_finding.lesion_type)
        self.assertIn("Babchi", res_bars.suggested_tadbeer[0])

        # Tinea / Qooba
        res_qooba = PhysicalSignsAnalyzer.analyze_physical_signs(
            skin_notes="Annular scaling erythematous plaque with central clearing, classic Qooba."
        )
        self.assertFalse(res_qooba.safe_to_lock)
        self.assertIn("Qooba", res_qooba.skin_finding.lesion_type)
        self.assertTrue(any("Zimad" in t for t in res_qooba.suggested_tadbeer))


if __name__ == "__main__":
    unittest.main()
