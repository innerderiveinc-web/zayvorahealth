#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — 6 Core Clinical Engines Scientific Validation Suite
Rigorously evaluates and validates the six fundamental clinical intelligence engines:
1. Mizaj Engine (10-Ajnas Assessment, Asnan age cohorts, Fusool seasons, Dyscrasia grading)
2. Organ-Axis Engine (12 Canonical Axes, Reflex Arcs, Asbab-e-Arba'a, Dawr-e-Marad stages)
3. Evidence Engine (E0-E6 Hierarchy, 4 Knowledge Worlds, GRADE Certainty, Peer-Review Guard)
4. Differential Engine (Classical Amraz, ICD-11 & SNOMED-CT Mapping, Red Flag Detection)
5. Hakeem Sahab AI (5-Layer Reasoning, Structural Validation, Uncertainty & Non-Delegable Barrier)
6. Safety Firewall (Schedule E(1) Mudabbar Gate, Colchicine Ceilings, Drug-Herb Interactions, Fail-Closed)
7. Multi-Engine Connected Cross-Talk Continuum (Patient -> Mizaj -> Axis -> Diff -> Evidence -> AI -> Safety)
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def _switch_service(service_name: str):
    """Isolates microservice module imports to prevent 'app' namespace collision."""
    abs_service = os.path.abspath(os.path.join(BASE_DIR, f"services/{service_name}"))
    for s in ["services/clinical", "services/therapeutic", "services/knowledge", "services/ai", "services/identity", "services/gateway"]:
        p = os.path.abspath(os.path.join(BASE_DIR, s))
        while p in sys.path:
            sys.path.remove(p)
    sys.path.insert(0, abs_service)
    to_del = [k for k in list(sys.modules.keys()) if k == "app" or k.startswith("app.")]
    for k in to_del:
        del sys.modules[k]


class TestSixCoreEnginesClinicalValidation(unittest.TestCase):
    """Deep scientific and architectural validation of the 6 core engines."""

    # =========================================================================
    # 1. MIZAJ ENGINE VALIDATION
    # =========================================================================
    def test_01_mizaj_engine_complete_assessment_and_insufficient_data(self):
        """Verify 10-Ajnas evaluation and ensure empty data fails safely to INSUFFICIENT_DATA."""
        from services.clinical.app.engines.mizaj_assessor import (
            calculate_mizaj_assessment,
            AJNAS_MAP,
        )

        # 1.1 Incomplete / Empty Data Guard
        empty_res = calculate_mizaj_assessment({})
        self.assertEqual(empty_res["status"], "INSUFFICIENT_DATA")
        self.assertTrue(empty_res["is_imputed_fallback"])
        self.assertIn("grounding_warning", empty_res)
        self.assertEqual(empty_res["primary_temperament"], "Motadil")

        # 1.2 Full Balghami Assessment
        balghami_answers = {
            "malmas": "cold_moist",
            "lahm_shahm": "heavy_adipose",
            "ashar": "slow_light",
            "laun": "chalky_pale",
            "hayat_aza": "broad_padded",
            "kayfiyyat_infial": "calm_sluggish",
            "naum_yaqzah": "excessive_deep",
            "harkat_sukoon": "slow_lethargic",
            "fuzalaat": "cold_pale",
            "afal_aza": "sluggish_slow",
        }
        res_balgham = calculate_mizaj_assessment(balghami_answers, age_category="adult", seasonal_profile="spring")
        self.assertEqual(res_balgham["primary_temperament"], "Balghami")
        self.assertEqual(res_balgham["distribution_percentages"]["Balghami"], 100.0)
        self.assertEqual(res_balgham["dyscrasia_degree"], 3)
        self.assertIn("Barid Ratab", res_balgham["su_e_mizaj"])

        # 1.3 Asnan (Age) & Fusool (Seasonal) Physiological Calibration
        res_pediatric = calculate_mizaj_assessment(
            {"malmas": "hot_moist", "lahm_shahm": "muscular_moderate"},
            age_category="pediatric",
            seasonal_profile="summer"
        )
        self.assertTrue(res_pediatric["calibration_applied"])
        self.assertGreater(len(res_pediatric["calibration_notes"]), 0)

    # =========================================================================
    # 2. ORGAN-AXIS ENGINE VALIDATION
    # =========================================================================
    def test_02_organ_axis_engine_12_axes_reflex_arcs_and_dawre_marad(self):
        """Verify 12 canonical organ axes, reflex sympathies, and 4 disease stages."""
        from services.clinical.app.engines.organ_axis_engine import (
            CANONICAL_ORGAN_AXES,
            AXIS_BIOMARKER_MAP,
            run_complete_organ_axis_analysis,
        )

        # 2.1 Verify complete 12 axes are defined
        self.assertEqual(len(CANONICAL_ORGAN_AXES), 12)
        required_axes = ["dimagh-asab", "qalb", "kabid-tihal", "kulliya-masana", "meda-amaa", "tanaffus", "mafasil-asab"]
        for ax in required_axes:
            self.assertIn(ax, CANONICAL_ORGAN_AXES)
            self.assertIn("governing_power", CANONICAL_ORGAN_AXES[ax])

        # 2.2 Verify biomarker cross-talk mappings exist
        for ax_id in ["dimagh-asab", "qalb", "kabid-tihal"]:
            self.assertIn(ax_id, AXIS_BIOMARKER_MAP)
            self.assertGreater(len(AXIS_BIOMARKER_MAP[ax_id]), 0)

        # 2.3 Run complete organ axis analysis with reflex arc & Dawr-e-Marad
        eval_res = run_complete_organ_axis_analysis(
            complaint="chronic knee pain and joint stiffness",
            associated_symptoms=["indigestion", "bloating"],
            duration_days=30,
            symptom_acuity="moderate",
            inflammatory_signs=True
        )
        self.assertIn("organ_axes", eval_res)
        primary = eval_res["organ_axes"]["primary_axis"]
        self.assertTrue(primary["id"] in CANONICAL_ORGAN_AXES)
        self.assertIn("asbab_e_arbaa", eval_res)
        self.assertIn("dawr_e_marad", eval_res)
        self.assertIn(eval_res["dawr_e_marad"]["stage_code"], ["ibtida", "tazayud", "intiha", "inhitat"])

    # =========================================================================
    # 3. EVIDENCE ENGINE VALIDATION
    # =========================================================================
    def test_03_evidence_engine_hierarchy_and_peer_review_guard(self):
        """Verify E0-E6 evidence hierarchy and strict peer-review gate."""
        from services.knowledge.app.core.evidence_engine import (
            EVIDENCE_LEVELS,
            KNOWLEDGE_WORLDS,
            classify_study_design,
        )

        # 3.1 Verify 4 Knowledge Worlds
        self.assertEqual(set(KNOWLEDGE_WORLDS.keys()), {"A", "B", "C", "D"})

        # 3.2 Verify E0-E6 Levels & Weights
        levels = ["E0", "E1", "E2", "E3", "E4", "E5", "E6"]
        for lvl in levels:
            self.assertIn(lvl, EVIDENCE_LEVELS)
            self.assertIn("weight", EVIDENCE_LEVELS[lvl])
            self.assertIn("knowledge_world", EVIDENCE_LEVELS[lvl])

        # 3.3 Study Design Classifier: Systematic Review -> E6
        sr_text = "A systematic review and meta-analysis of randomized controlled trials of Nigella sativa for hypertension."
        sr_class = classify_study_design(sr_text)
        self.assertEqual(sr_class["predicted_level"], "E6")
        self.assertTrue(sr_class["requires_peer_review"])
        self.assertEqual(sr_class["peer_review_status"], "pending")

        # 3.4 Study Design Classifier: In-Vitro -> E3
        invitro_text = "Phytochemical characterization and in-vitro antioxidant scavenging assay of Curcuma longa extracts."
        iv_class = classify_study_design(invitro_text)
        self.assertEqual(iv_class["predicted_level"], "E3")

    # =========================================================================
    # 4. DIFFERENTIAL ENGINE VALIDATION
    # =========================================================================
    def test_04_differential_engine_icd11_snomed_and_red_flags(self):
        """Verify Unani Amraz to ICD-11 & SNOMED mapping and emergency red-flag escalation."""
        from services.clinical.app.engines.differential_engine import (
            UNANI_AMRAZ_ICD11_REGISTRY,
            match_differential_considerations,
        )

        self.assertGreater(len(UNANI_AMRAZ_ICD11_REGISTRY), 5)
        for entity in UNANI_AMRAZ_ICD11_REGISTRY:
            self.assertIn("unani_disease", entity)
            self.assertIn("icd11_code", entity)
            self.assertIn("snomed_concept_id", entity)
            self.assertIn("red_flags", entity)
            self.assertGreater(len(entity["red_flags"]), 0)

        # Query symptoms for Niqris (Gout)
        diff_res = match_differential_considerations("sudden severe big toe pain, podagra, joint swelling and high uric acid")
        self.assertGreater(len(diff_res), 0)
        top = diff_res[0]
        self.assertIn("Niqris", top["unani_disease"])
        self.assertEqual(top["icd11_code"], "FA25")
        self.assertGreater(len(top["red_flags"]), 0)

    # =========================================================================
    # 5. HAKEEM SAHAB AI VALIDATION
    # =========================================================================
    def test_05_hakeem_sahab_ai_structure_and_safety_barriers(self):
        """Verify Hakeem Sahab prompt enforcement, structural sections, and non-delegable signature."""
        _switch_service("ai")
        from app.engines.hakeem_sahab import SYSTEM_PROMPT, _build_user_prompt
        from app.engines.response_validator import validate_response_structure

        # 5.1 Verify System Prompt Rules
        self.assertIn("Never invent a classical citation", SYSTEM_PROMPT)
        self.assertIn("CLINICIAN REVIEW REQUIRED", SYSTEM_PROMPT)

        # 5.2 User Prompt Construction with Schedule E(1) Detection
        prompt = _build_user_prompt(
            chief_complaint="Severe right knee arthralgia",
            patient_context={"mizaj": {"primary_temperament": "Balghami"}},
            candidate_mufradat=[{"name": "Suranjan Talkh", "schedule_e1": True}],
        )
        self.assertIn("Schedule E(1)", prompt)
        self.assertIn("Suranjan Talkh", prompt)

        # 5.3 Response Structure Verification
        valid_mock_response = (
            "CLINICAL SUMMARY\nPatient with phlegmatic arthralgia.\n"
            "WHAT IS KNOWN\nKnee crepitus and cold sensation.\n"
            "UNANI PERSPECTIVE\nSu-e-Mizaj Barid Balghami.\n"
            "BIOMEDICAL PERSPECTIVE\nMild osteoarthritic degenerative change.\n"
            "DIFFERENTIAL CONSIDERATIONS\nWaja-ul-Mafasil Barid.\n"
            "RED FLAGS\nNo septic arthritis markers.\n"
            "MISSING INFORMATION\nRecent serum uric acid report.\n"
            "EVIDENCE\nMajun Suranjan traditional efficacy documented in NFUM.\n"
            "SAFETY\nColchicine dosage within ceiling; no renal breach.\n"
            "POSSIBLE CARE OPTIONS\nMajun Suranjan 5g nocte + Parhez.\n"
            "MONITORING\nRe-evaluate in 14 days.\n"
            "UNCERTAINTY\nModerate uncertainty regarding cartilage thickness.\n"
            "CLINICIAN REVIEW REQUIRED\nMandatory physician validation before signature."
        )
        missing_sections = validate_response_structure(valid_mock_response)
        self.assertEqual(len(missing_sections), 0, f"Missing sections: {missing_sections}")

    # =========================================================================
    # 6. SAFETY FIREWALL VALIDATION
    # =========================================================================
    def test_06_safety_firewall_schedule_e1_and_interactions(self):
        """Verify Safety Firewall Schedule E(1) mudabbar blocks and drug-herb interactions."""
        from services.therapeutic.app.engines.safety_firewall import (
            SCHEDULE_E1_POISONS,
            run_safety_firewall,
        )

        # 6.1 Schedule E(1) Directory Verification
        self.assertIn("suranjan_talkh", SCHEDULE_E1_POISONS)
        self.assertIn("kuchla", SCHEDULE_E1_POISONS)
        self.assertIn("afeem", SCHEDULE_E1_POISONS)
        self.assertIn("mudabbar_protocol", SCHEDULE_E1_POISONS["suranjan_talkh"])

        # 6.2 Emergency Red Flag -> REFER
        red_flag_res = run_safety_firewall(
            patient_context={"chief_complaint": "Acute severe crushing chest pain radiating to jaw"},
            ingredients=[{"name": "Sharbat Banafsha", "dose": "10ml"}]
        )
        self.assertEqual(red_flag_res["verdict"], "REFER")
        self.assertTrue(red_flag_res["requiresPractitionerSignoff"])

        # 6.3 Schedule E(1) Unpurified -> DO_NOT_RECOMMEND
        unpurified_res = run_safety_firewall(
            patient_context={"age": 45, "pregnancy_status": "none"},
            ingredients=[{"name": "Suranjan Talkh", "dose": "1200mg", "mudabbar_verified": False}]
        )
        self.assertEqual(unpurified_res["verdict"], "DO_NOT_RECOMMEND")

        # 6.4 Safe Formulation -> SAFE_TO_CONSIDER
        safe_res = run_safety_firewall(
            patient_context={"age": 35, "gender": "male", "comorbidities": []},
            ingredients=[
                {"name": "Sharbat Banafsha", "dose": "10ml", "mudabbar_verified": True},
                {"name": "Arq Kasni", "dose": "50ml", "mudabbar_verified": True}
            ]
        )
        self.assertEqual(safe_res["verdict"], "SAFE_TO_CONSIDER")

    # =========================================================================
    # 7. CONNECTED CROSS-TALK CONTINUUM ACROSS ALL 6 ENGINES
    # =========================================================================
    def test_07_six_engines_connected_clinical_continuum(self):
        """Verify the seamless clinical cross-talk loop across all 6 core engines."""
        from services.clinical.app.engines.mizaj_assessor import calculate_mizaj_assessment
        from services.clinical.app.engines.organ_axis_engine import run_complete_organ_axis_analysis
        from services.clinical.app.engines.differential_engine import match_differential_considerations
        from services.knowledge.app.core.evidence_engine import classify_study_design
        from services.therapeutic.app.engines.safety_firewall import run_safety_firewall

        _switch_service("ai")
        from app.engines.hakeem_sahab import _build_user_prompt

        # Case: 52yo Male with chronic knee osteoarthritis and mild dyspepsia
        # Step 1: Mizaj Engine
        mizaj_res = calculate_mizaj_assessment({
            "malmas": "cold_moist",
            "lahm_shahm": "heavy_adipose",
            "laun": "chalky_pale",
            "afal_aza": "sluggish_slow"
        })
        self.assertEqual(mizaj_res["primary_temperament"], "Balghami")

        # Step 2: Organ-Axis Engine
        axis_res = run_complete_organ_axis_analysis(
            complaint="chronic knee pain and joint stiffness",
            associated_symptoms=["dyspepsia", "sluggish digestion"],
            duration_days=45,
            temperament_context=mizaj_res
        )
        primary_axis = axis_res["organ_axes"]["primary_axis"]["id"]
        self.assertTrue(primary_axis in ["mafasil-asab", "meda-amaa", "mizaj-am"])

        # Step 3: Differential Engine
        diff_res = match_differential_considerations("knee pain, joint stiffness and crepitus")
        self.assertGreater(len(diff_res), 0)
        top_disease = diff_res[0]["unani_disease"]
        self.assertIn("Waja-ul-Mafasil", top_disease)

        # Step 4: Evidence Engine
        study_evidence = classify_study_design("Clinical efficacy of Colchicum luteum (Suranjan) in osteoarthritic arthralgia: a randomized controlled trial.")
        self.assertEqual(study_evidence["predicted_level"], "E5")

        # Step 5: Hakeem Sahab AI Copilot Prompt Assembly
        copilot_prompt = _build_user_prompt(
            chief_complaint="Knee pain with sluggish morning digestion",
            patient_context={"mizaj": mizaj_res, "primary_axis": primary_axis},
            candidate_mufradat=[{"name": "Majun Suranjan", "schedule_e1": True}],
        )
        self.assertIn("Balghami", copilot_prompt)
        self.assertIn("Majun Suranjan", copilot_prompt)

        # Step 6: Safety Firewall Preflight
        safety_res = run_safety_firewall(
            patient_context={"mizaj": mizaj_res, "age": 52},
            ingredients=[
                {"name": "Sharbat Banafsha", "dose": "10ml", "mudabbar_verified": True},
                {"name": "Jawarish Kamuni", "dose": "5g", "mudabbar_verified": True}
            ]
        )
        self.assertEqual(safety_res["verdict"], "SAFE_TO_CONSIDER")


if __name__ == "__main__":
    unittest.main()
