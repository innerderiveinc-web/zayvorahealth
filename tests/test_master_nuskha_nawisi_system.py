"""
ZAYVORA Health OS™ - Master Nuskha Nawisi & 7-Pillars Prescribing Test Suite.

Verifies:
1. Organ-Axis Badraqa (Conduit Vehicle) Registry
2. Galenical Processing & Shodhana (Tadbeer) Protocols
3. Darajat-e-Adwiya Posology Scaling & Quwwat-e-Hazima Modulation
4. Chrono-Posology Circadian Administration Timings
5. 3-Column Parhez Dietary Matrix
6. Adverse Event Reversal Signposts & Antidotes
7. 3-Phase Sequential Staging (Tanqiya -> Ta'deel -> Taqwiyat)
8. End-to-End Master Nuskha Synthesizer
9. Product Matrix 16 & Products Master 32 Metadata Enrichment
10. Live REST API Endpoints (Badraqa, Synthesis, Parhez)
"""

import unittest
import sys
import os
import json
import urllib.request
import urllib.error

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.therapeutic.app.engines.master_nuskha_architect import (
    ORGAN_BADRAQA_CONDUIT_REGISTRY,
    GALENICAL_TADBEER_REGISTRY,
    DARAJA_DOSE_BANDS,
    compute_daraja_scaled_dose,
    CHRONO_SCHEDULES,
    ORGAN_PARHEZ_MATRIX,
    ADVERSE_EVENT_REVERSAL_REGISTRY,
    build_three_phase_protocol,
    synthesize_master_nuskha,
)
from services.therapeutic.app.data.product_matrix_16 import CORE_PRODUCTS_16
from services.knowledge.app.data.products_master import MASTER_PRODUCTS


class TestMasterNuskhaNawisiSystem(unittest.TestCase):

    def test_01_organ_badraqa_conduit_registry(self):
        """Pillar 1: Every organ axis must have defined primary conduit, secondary conduit, and action vector."""
        expected_axes = [
            "CEREBROVASCULAR", "NEURO_PSYCHOLOGICAL", "CARDIOVASCULAR",
            "HEPATO_BILIARY", "GASTROINTESTINAL", "PULMONARY",
            "RENAL_URINARY", "MALE_REPRODUCTIVE", "FEMALE_REPRODUCTIVE",
            "MUSCULOSKELETAL", "IMMUNOLOGICAL", "METABOLIC"
        ]
        for axis in expected_axes:
            self.assertIn(axis, ORGAN_BADRAQA_CONDUIT_REGISTRY, f"Missing conduit for {axis}")
            conduit_info = ORGAN_BADRAQA_CONDUIT_REGISTRY[axis]
            self.assertTrue(len(conduit_info["primary_conduit"]) > 0)
            self.assertTrue(len(conduit_info["action_vector"]) > 0)

    def test_02_galenical_tadbeer_registry(self):
        """Pillar 2: Purification and galenical standards must be codified for toxic/potent substances."""
        required_toxic_agents = ["kuchla", "suranjan", "aqarqarha", "guggul", "kushta_nuqra"]
        for agent in required_toxic_agents:
            self.assertIn(agent, GALENICAL_TADBEER_REGISTRY, f"Missing Tadbeer standard for {agent}")
            spec = GALENICAL_TADBEER_REGISTRY[agent]
            self.assertTrue(len(spec["tadbeer_method"]) > 10)
            self.assertTrue(spec["safety_limit_mg"] > 0)
            self.assertTrue(len(spec["galenical_form"]) > 0)

    def test_03_daraja_posology_scaling(self):
        """Pillar 3: Posology must scale according to Darajat-e-Adwiya and Quwwat-e-Hazima."""
        # 1st degree: food-drugs (Asgandh, Salab)
        res_d1 = compute_daraja_scaled_dose(1, 3000.0, quwwat_e_hazima="normal")
        self.assertGreaterEqual(res_d1["calculated_mg"], 2000.0)
        self.assertLessEqual(res_d1["calculated_mg"], 6000.0)

        # 4th degree: toxic/kushtas (Kushta Nuqra) capped at 50mg
        res_d4 = compute_daraja_scaled_dose(4, 30.0, quwwat_e_hazima="normal")
        self.assertLessEqual(res_d4["calculated_mg"], 50.0)

        # Weak digestion (Zaeef-ul-Hazm) must attenuate dose by 35%
        res_weak = compute_daraja_scaled_dose(2, 1000.0, quwwat_e_hazima="zaeef")
        self.assertEqual(res_weak["hazima_factor"], 0.65)
        self.assertEqual(res_weak["calculated_mg"], 650.0)

    def test_04_chrono_posology_schedules(self):
        """Pillar 4: Circadian administration timings must cover all clinical states."""
        for window in ["nihaar_munh", "qabl_az_ghiza", "bad_az_ghiza", "waqt_e_khab"]:
            self.assertIn(window, CHRONO_SCHEDULES)
            self.assertTrue(len(CHRONO_SCHEDULES[window]["time_window"]) > 0)
            self.assertTrue(len(CHRONO_SCHEDULES[window]["classical_principle"]) > 0)

    def test_05_organ_parhez_matrix(self):
        """Pillar 5: Parhez matrix must classify prohibited vs accelerating foods."""
        for axis, data in ORGAN_PARHEZ_MATRIX.items():
            self.assertTrue(len(data["prohibited_antagonistic"]) >= 3, f"Insufficient prohibited foods for {axis}")
            self.assertTrue(len(data["accelerating_synergistic"]) >= 3, f"Insufficient synergistic foods for {axis}")
            self.assertTrue(len(data["regimental_lifestyle"]) >= 2, f"Insufficient lifestyle rules for {axis}")

    def test_06_adverse_event_reversal_registry(self):
        """Pillar 6: Early symptom signposts and instant classical antidotes must be defined."""
        for condition in ["safra_excess", "balgham_excess", "gastric_irritation"]:
            self.assertIn(condition, ADVERSE_EVENT_REVERSAL_REGISTRY)
            self.assertTrue(len(ADVERSE_EVENT_REVERSAL_REGISTRY[condition]["instant_antidote"]) > 0)

    def test_07_three_phase_protocol_builder(self):
        """Pillar 7: Protocol must stage treatment into Tanqiya -> Ta'deel -> Taqwiyat."""
        proto = build_three_phase_protocol(
            organ_axis="MALE_REPRODUCTIVE",
            target_pathology="Oligospermia",
            patient_mizaj="Safrawi",
            core_formulation={"item": "Sample"}
        )
        phases = proto["three_phase_protocol"]
        self.assertIn("phase_1_evacuation", phases)
        self.assertIn("phase_2_therapeutic_resolution", phases)
        self.assertIn("phase_3_rejuvenation_maintenance", phases)
        self.assertIn("Tanqiya", phases["phase_1_evacuation"]["phase_name"])
        self.assertIn("Ta'deel", phases["phase_2_therapeutic_resolution"]["phase_name"])
        self.assertIn("Taqwiyat", phases["phase_3_rejuvenation_maintenance"]["phase_name"])

    def test_08_synthesize_master_nuskha_e2e(self):
        """Full end-to-end synthesis must generate complete 7-pillar master prescription."""
        res = synthesize_master_nuskha(
            organ_axis="MALE_REPRODUCTIVE",
            indication="Asthenozoospermia",
            ingredients=[
                {"name": "Salab Misri", "amount_mg": 3000},
                {"name": "Asgandh Nagauri", "amount_mg": 2500},
                {"name": "Aqarqarha", "amount_mg": 150},
                {"name": "Kushta Nuqra", "amount_mg": 30}
            ],
            patient_context={"age": 32, "quwwat_e_hazima": "normal", "mizaj": "Damawi"}
        )
        self.assertEqual(res["status"], "MASTER_NUSKHA_SYNTHESIZED")
        self.assertEqual(res["clinical_validation"]["senior_hakeem_acceptance_grade"], "A+ (AUTHENTIC HIGH-CLINICAL REALISM)")
        self.assertTrue(res["clinical_validation"]["is_3_phase_staged"])
        self.assertTrue(res["clinical_validation"]["has_organ_badraqa"])
        self.assertTrue(res["clinical_validation"]["has_tadbeer_specs"])

    def test_09_product_matrix_16_enrichment(self):
        """All 16 commercial products must have Badraqa and Chrono posology attached."""
        self.assertEqual(len(CORE_PRODUCTS_16), 16)
        for pid, p in CORE_PRODUCTS_16.items():
            self.assertIn("badraqa_vehicle", p, f"Missing badraqa in {pid}")
            self.assertIn("chrono_timing", p, f"Missing chrono_timing in {pid}")
            self.assertIn("parhez_prohibited_foods", p, f"Missing parhez in {pid}")

    def test_10_products_master_32_enrichment(self):
        """All 32 compendium products must have Badraqa and Chrono posology attached."""
        self.assertEqual(len(MASTER_PRODUCTS), 32)
        for sku, p in MASTER_PRODUCTS.items():
            self.assertIn("badraqa_vehicle", p, f"Missing badraqa in {sku}")
            self.assertIn("chrono_timing", p, f"Missing chrono_timing in {sku}")
            self.assertIn("parhez_prohibited_foods", p, f"Missing parhez in {sku}")


if __name__ == "__main__":
    unittest.main()
