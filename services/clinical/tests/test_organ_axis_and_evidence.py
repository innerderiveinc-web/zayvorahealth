"""
Unit tests for Organ-Axis Reflex Arcs, Pathophysiological Progression (Dawr-e-Marad),
Asbab-e-Arba'a Root Cause Deduction, and Evidence Engine 2.0 (Phase 8).
"""
import unittest

from app.engines.organ_axis_engine import (
    analyze_dawr_e_marad,
    deduce_asbab_e_arbaa,
    deduce_organ_axes_and_reflexes,
    run_complete_organ_axis_analysis,
)


class TestOrganAxisAndEvidence(unittest.TestCase):
    def test_organ_axes_deduction_primary_musculoskeletal(self):
        result = deduce_organ_axes_and_reflexes("Severe bilateral knee pain with morning stiffness and joint swelling")
        self.assertEqual(result["primary_axis"]["id"], "mafasil-asab")
        self.assertIn("Musculoskeletal Axis", result["primary_axis"]["name"])

    def test_gastro_cephalic_reflex_arc(self):
        """Tests that gastric symptoms triggering cephalic pain are identified
        as the classical Meda-o-Dimagh reflex arc."""
        result = deduce_organ_axes_and_reflexes("Severe headache after food with nausea, acid reflux, and epigastric bloating")
        self.assertTrue(result["reflex_sympathy_identified"])
        self.assertEqual(result["primary_axis"]["id"], "meda-amaa")
        self.assertIsNotNone(result["secondary_axis"])
        self.assertEqual(result["secondary_axis"]["id"], "dimagh-asab")
        self.assertEqual(len(result["detected_reflex_arcs"]), 1)
        self.assertEqual(result["detected_reflex_arcs"][0]["id"], "gastro-cephalic")
        self.assertIn("Bukharat-e-Radiya", result["detected_reflex_arcs"][0]["classical_mechanism"])

    def test_cardio_cerebral_reflex_arc(self):
        """Tests that palpitations precipitating sudden panic are mapped to
        the Qalb-o-Dimagh reflex arc."""
        result = deduce_organ_axes_and_reflexes("Palpitation anxiety with paroxysmal tachycardia and panic attack")
        self.assertTrue(result["reflex_sympathy_identified"])
        self.assertEqual(result["primary_axis"]["id"], "qalb")
        self.assertEqual(result["secondary_axis"]["id"], "dimagh-asab")
        self.assertEqual(result["detected_reflex_arcs"][0]["id"], "cardio-cerebral")

    def test_asbab_e_arbaa_four_causes(self):
        """Tests the classical 4-cause deduction: Fa'il, Maddi, Suri, Tamami."""
        asbab = deduce_asbab_e_arbaa(
            complaint="Cold phlegm stasis with swelling and joint stiffness",
            temperament_context={"primary_temperament": "Balghami"},
            primary_axis_id="mafasil-asab",
        )
        self.assertIn("Su-e-Mizaj Barid", asbab["sabab_fail"])
        self.assertIn("Khilt-e-Balgham Kham", asbab["sabab_maddi"])
        self.assertIn("Waram", asbab["sabab_suri"])
        self.assertIn("Quwwat", asbab["sabab_tamami"])

    def test_dawr_e_marad_progression_stages(self):
        """Tests staging through Ibtida, Tazayud, Intiha, and Inhitat."""
        # 1. Ibtida (early onset < 3 days)
        stage_1 = analyze_dawr_e_marad(duration_days=2, symptom_acuity="mild")
        self.assertEqual(stage_1["stage_code"], "ibtida")
        self.assertIn("Tadeel-e-Mizaj", stage_1["usool_e_ilaj"])

        # 2. Tazayud (active progression with inflammatory reaction)
        stage_2 = analyze_dawr_e_marad(duration_days=7, symptom_acuity="moderate", inflammatory_signs=True)
        self.assertEqual(stage_2["stage_code"], "tazayud")
        self.assertIn("Nujz-e-Khilt", stage_2["usool_e_ilaj"])

        # 3. Intiha (acme / peak crisis)
        stage_3 = analyze_dawr_e_marad(duration_days=18, symptom_acuity="severe")
        self.assertEqual(stage_3["stage_code"], "intiha")
        self.assertIn("Tanqiya", stage_3["usool_e_ilaj"])

        # 4. Inhitat (convalescence / recovery)
        stage_4 = analyze_dawr_e_marad(duration_days=45, symptom_acuity="mild")
        self.assertEqual(stage_4["stage_code"], "inhitat")
        self.assertIn("Taqwiyat-e-A'za", stage_4["usool_e_ilaj"])

    def test_complete_organ_axis_analysis_orchestration(self):
        analysis = run_complete_organ_axis_analysis(
            complaint="Chronic headache after food with dyspepsia",
            duration_days=5,
            symptom_acuity="moderate",
            inflammatory_signs=False,
        )
        self.assertIn("organ_axes", analysis)
        self.assertIn("asbab_e_arbaa", analysis)
        self.assertIn("dawr_e_marad", analysis)
        self.assertTrue(analysis["organ_axes"]["reflex_sympathy_identified"])

    def test_evidence_engine_study_classifier_and_grade(self):
        """Tests the Evidence Engine 2.0 automated classifier and GRADE scoring."""
        import sys
        import os

        knowledge_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "knowledge")
        )
        if knowledge_dir not in sys.path:
            sys.path.insert(0, knowledge_dir)

        from app.core.evidence_engine import calculate_grade_certainty, classify_study_design

        # 1. Systematic Review (E6)
        c6 = classify_study_design("A PRISMA Systematic Review and Meta-Analysis of Boswellia serrata in Osteoarthritis")
        self.assertEqual(c6["predicted_level"], "E6")
        self.assertIn("Systematic Review", c6["study_type"])

        # 2. Randomized Controlled Trial (E5)
        c5 = classify_study_design("A Double-Blind Randomized Controlled Trial of Withania somnifera in Anxiety Neurosis")
        self.assertEqual(c5["predicted_level"], "E5")
        self.assertIn("Randomized Controlled Trial", c5["study_type"])

        # 3. In-Vivo Preclinical (E4)
        c4 = classify_study_design("In vivo evaluation of Colchicum luteum in wistar rats with adjuvant-induced arthritis")
        self.assertEqual(c4["predicted_level"], "E4")
        self.assertIn("In-Vivo", c4["study_type"])

        # 4. Classical Canonical (E0)
        c0 = classify_study_design("Canon of Medicine (Al-Qanun fi al-Tibb) Book III Treatise on Arthralgia")
        self.assertEqual(c0["predicted_level"], "E0")
        self.assertTrue(c0["requires_peer_review"])
        self.assertEqual(c0["peer_review_status"], "pending")

        # 5. GRADE Certainty Calculation
        # High quality RCT (4 - 0 = 4)
        grade_high = calculate_grade_certainty("E5", risk_of_bias=0, inconsistency=0)
        self.assertEqual(grade_high["grade_certainty"], "HIGH")

        # RCT degraded by 1 point (4 - 1 = 3 -> MODERATE)
        grade_mod = calculate_grade_certainty("E5", risk_of_bias=1)
        self.assertEqual(grade_mod["grade_certainty"], "MODERATE")

        # RCT degraded by 2 points (4 - 2 = 2 -> LOW)
        grade_low = calculate_grade_certainty("E5", risk_of_bias=1, indirectness=1)
        self.assertEqual(grade_low["grade_certainty"], "LOW")

        # RCT degraded by 3 points (4 - 3 = 1 -> VERY_LOW)
        grade_vl = calculate_grade_certainty("E5", risk_of_bias=2, indirectness=1)
        self.assertEqual(grade_vl["grade_certainty"], "VERY_LOW")

    def test_biomarker_cross_talk_mapping(self):
        """Tests that full organ-axis analysis outputs laboratory biomarker cross-talk."""
        res = run_complete_organ_axis_analysis(
            complaint="Severe headache after food with nausea and acid reflux",
            associated_symptoms=["bloating", "epigastric burning"],
        )
        self.assertIn("biomarker_cross_talk", res)
        cross_talk = res["biomarker_cross_talk"]
        self.assertIn("primary_axis_biomarkers", cross_talk)
        self.assertIn("reflex_axis_biomarkers", cross_talk)
        self.assertTrue(len(cross_talk["primary_axis_biomarkers"]) > 0)
        self.assertTrue(len(cross_talk["cross_talk_indicators"]) > 0)
        self.assertIn("meda-amaa", cross_talk["cross_talk_indicators"][0])


if __name__ == "__main__":
    unittest.main()


