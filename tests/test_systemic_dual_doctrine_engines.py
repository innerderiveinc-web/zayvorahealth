#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Test Suite #55: Systemic Dual-Doctrine Engines (Modern & Unani)
====================================================================================
Tests newly codified diagnostic, lifestyle, staging, and pharmacokinetic engines:
  1. Classical Qaroorah (Urine) & Modern Urinalysis Diagnostic Engine
  2. Classical Baraaz (Stool / Alimentary) Diagnostic Engine
  3. Asbab Sitta Zarooriya Dynamic Lifestyle Scoring Engine
  4. Enhanced Emergency Red Flag & Triage Guard (Acute Abdomen, SpO2, Sepsis)
  5. Expanded Functional Lab Biomarkers (Renal, Lipid, CBC, Biliary)
  6. Munzij & Mushil (Nujz & Tanqiya) Staging Protocol Engine
  7. CYP450 Pharmacokinetic Drug-Herb Interaction Engine
  8. Dynamic Hakeem Sahab Case Brief Engine
  9. Live REST API Gateway Endpoints for all new engines
"""

import unittest
import sys
import os
import io
import json
from unittest.mock import MagicMock
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.clinical.app.engines.qaroorah_diagnostic_engine import (
    QaroorahDiagnosticEngine,
    QaroorahPhysicalInspection,
    ModernUrinalysisData
)
from services.clinical.app.engines.baraaz_diagnostic_engine import (
    BaraazDiagnosticEngine,
    BaraazInspectionInput
)
from services.clinical.app.engines.asbab_sitta_scoring_engine import (
    AsbabSittaScoringEngine,
    AsbabSittaPatientInput
)
from services.clinical.app.engines.emergency_red_flag_guard import EmergencyRedFlagGuard
from services.clinical.app.engines.functional_lab_engine import FUNCTIONAL_LAB_RANGES
from services.therapeutic.app.engines.munzij_mushil_protocol_engine import MunzijMushilProtocolEngine
from services.therapeutic.app.engines.cyp450_interaction_engine import CYP450InteractionEngine
from services.ai.app.engines.hakeem_case_brief_engine import HakeemCaseBriefEngine
import services.live_api_server as las


class TestSystemicDualDoctrineEngines(unittest.TestCase):

    def setUp(self):
        self.handler = las.ZayvoraApiHandler.__new__(las.ZayvoraApiHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {"Content-Length": "0"}
        self.handler.server = MagicMock()
        self.handler.client_address = ("127.0.0.1", 54321)
        self.handler.request_version = "HTTP/1.1"
        self.handler._get_auth_context = lambda: {
            "user_id": "test-practitioner",
            "roles": ["SUPER_ADMIN"],
            "clinic_id": "facility-delhi-01"
        }

    def _execute_post(self, path: str, body: dict) -> dict:
        self.handler.path = path
        self.handler.command = "POST"
        self.handler.requestline = f"POST {path} HTTP/1.1"
        body_bytes = json.dumps(body).encode("utf-8")
        self.handler.rfile = io.BytesIO(body_bytes)
        self.handler.headers = {
            "Content-Length": str(len(body_bytes)),
            "Content-Type": "application/json"
        }
        self.handler.wfile = io.BytesIO()
        self.handler.do_POST()
        self.handler.wfile.seek(0)
        raw = self.handler.wfile.getvalue().decode("utf-8")
        parts = raw.split("\r\n\r\n", 1)
        self.assertIn("200 OK", parts[0], f"Expected 200 OK for {path}, got: {parts[0]}")
        return json.loads(parts[1])

    # 1. QAROORAH DIAGNOSTIC ENGINE TESTS
    def test_qaroorah_balghami_thin_sediment_detection(self):
        insp = QaroorahPhysicalInspection(
            lawn="Abyad Raqeeq (Pale watery)",
            qiwam="Raqeeq",
            safa="Safi",
            rusoob="None",
            miqdar="Katheer",
            boo="Bira'ihah",
            zabd="Qaleel"
        )
        res = QaroorahDiagnosticEngine.analyze_qaroorah("PT-001", insp)
        self.assertEqual(res["dominant_humor_inferred"], "Balgham")
        self.assertIn("Buroodat-e-Mizaj (Excessive Constitutional Coldness)", res["pathological_syndromes"])
        self.assertIn("Tasgheen (Warming)", res["recommended_afaal_strategy"])

    def test_qaroorah_modern_urinalysis_fusion_proteinuria(self):
        insp = QaroorahPhysicalInspection(
            lawn="Asfar Qashiy",
            qiwam="Ghaleez",
            safa="Kadeer",
            rusoob="Mahmoof",
            zabd="Katheer_Daim (Persistent froth)"
        )
        modern = ModernUrinalysisData(
            protein_mg_dl=300.0,
            microscopic_rbc_hpf=5.0,
            crystals="Calcium Oxalate"
        )
        res = QaroorahDiagnosticEngine.analyze_qaroorah("PT-002", insp, modern)
        self.assertFalse(res["safe_to_proceed_with_herbal"])
        self.assertTrue(any("Proteinuria" in f for f in res["critical_red_flags"]))
        self.assertTrue(any("Hematuria" in f for f in res["critical_red_flags"]))
        self.assertIn("Kulyah (Glomerular Barrier)", res["involved_organs"])

    # 2. BARAAZ DIAGNOSTIC ENGINE TESTS
    def test_baraaz_melena_red_flag(self):
        inp = BaraazInspectionInput(
            lawn="Aswad Melena (Black tarry)",
            bristol_type=6,
            istihala="Ghair_Mustahil",
            riyah="Katheer",
            boo="Muntan"
        )
        res = BaraazDiagnosticEngine.analyze_baraaz("PT-003", inp)
        self.assertTrue(res["requires_urgent_endoscopy"])
        self.assertFalse(res["safe_for_routine_matab"])
        self.assertTrue(any("Ghait-e-Aswad" in f for f in res["critical_red_flags"]))

    def test_baraaz_spastic_constipation_tadbeer(self):
        inp = BaraazInspectionInput(
            lawn="Asfar Tabiyi",
            bristol_type=1,
            istihala="Mustahil",
            riyah="Qaleel",
            khurooj_ease="Usr"
        )
        res = BaraazDiagnosticEngine.analyze_baraaz("PT-004", inp)
        self.assertEqual(res["dominant_humoral_burden"], "Sawda")
        self.assertTrue(res["safe_for_routine_matab"])
        self.assertTrue(any("Isabgol" in t or "Badam" in t for t in res["recommended_regimenal_tadbeer"]))

    # 3. ASBAB SITTA SCORING ENGINE TESTS
    def test_asbab_sitta_equilibrium_scoring_and_violations(self):
        inp = AsbabSittaPatientInput(
            air_quality_exposure="HIGH_POLLUTION",
            dietary_greasy_spicy_load="HIGH",
            daily_sedentary_hours=10.0,
            chronic_psychological_stress="SEVERE",
            sleep_hours_per_night=5.0,
            bedtime_hour_24h=1.5,
            constipation_present=True
        )
        res = AsbabSittaScoringEngine.evaluate_lifestyle_equilibrium("PT-005", "Safrawi", inp)
        self.assertLess(res["asbab_sitta_equilibrium_score"], 60.0)
        self.assertTrue(res["non_pharmacological_first_line_indicated"])
        self.assertGreaterEqual(len(res["identified_lifestyle_violations"]), 4)
        self.assertTrue(any("Tadbeer-e-Naum" in t for t in res["corrective_tadbeer_prescriptions"]))
        self.assertTrue(any("Tadbeer-e-Tanqiya" in t for t in res["corrective_tadbeer_prescriptions"]))

    # 4. ENHANCED EMERGENCY RED FLAG GUARD TESTS
    def test_emergency_red_flag_surgical_and_respiratory(self):
        # Case 1: Surgical acute abdomen keyword
        res_surg = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["abdominal pain", "rebound tenderness"],
            notes="Patient has acute rigidity."
        )
        self.assertFalse(res_surg["is_safe_for_unani_care"])
        self.assertIn("EMERGENCY HARD STOP", res_surg["decision"])
        self.assertTrue(any("rebound tenderness" in f["triggered_by"] for f in res_surg["detected_red_flags"]))

        # Case 2: Severe hypoxemia SpO2 < 90%
        res_resp = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["cough"],
            labs={"spo2": 86.0}
        )
        self.assertFalse(res_resp["is_safe_for_unani_care"])
        self.assertTrue(any("SpO2" in f["triggered_by"] for f in res_resp["detected_red_flags"]))

        # Case 3: Severe Anemia Hb < 7.0 g/dL
        res_anemia = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=["fatigue"],
            labs={"hb": 6.4}
        )
        self.assertFalse(res_anemia["is_safe_for_unani_care"])
        self.assertTrue(any("Hemoglobin" in f["triggered_by"] for f in res_anemia["detected_red_flags"]))

    # 5. FUNCTIONAL LAB RANGES EXTENSION TESTS
    def test_functional_lab_ranges_renal_and_lipid_present(self):
        self.assertIn("Serum_Creatinine", FUNCTIONAL_LAB_RANGES)
        self.assertIn("Uric_Acid", FUNCTIONAL_LAB_RANGES)
        self.assertIn("Triglycerides", FUNCTIONAL_LAB_RANGES)
        self.assertIn("LDL_Cholesterol", FUNCTIONAL_LAB_RANGES)
        self.assertIn("Hemoglobin", FUNCTIONAL_LAB_RANGES)
        self.assertIn("Total_Bilirubin", FUNCTIONAL_LAB_RANGES)
        self.assertEqual(FUNCTIONAL_LAB_RANGES["Serum_Creatinine"]["referral_threshold"], 2.0)
        self.assertEqual(FUNCTIONAL_LAB_RANGES["Uric_Acid"]["action_threshold"], 6.5)

    # 6. MUNZIJ & MUSHIL STAGING PROTOCOL TESTS
    def test_munzij_mushil_balgham_staging(self):
        proto = MunzijMushilProtocolEngine.synthesize_protocol("PT-006", "Balgham", "CHRONIC", has_active_nujz=False)
        self.assertEqual(proto["target_pathological_humor"], "Balgham")
        self.assertEqual(proto["current_recommended_phase"], "PHASE_1_NUJZ_CONCOCTION")
        self.assertEqual(proto["nujz_phase"]["prescribed_duration_days"], 8)
        self.assertTrue(any("Asl-us-Soos" in i["herb"] for i in proto["nujz_phase"]["ingredients"]))
        self.assertTrue(any("Turbud" in a or "Sana" in a for a in proto["tanqiya_phase"]["actives"]))

    # 7. CYP450 PHARMACOKINETIC INTERACTION TESTS
    def test_cyp450_warfarin_piperine_critical_block(self):
        res = CYP450InteractionEngine.evaluate_pharmacokinetic_risk(
            current_allopathic_medications=["Warfarin 5mg OD"],
            candidate_herbs=["Piperine extract", "Curcumin"]
        )
        self.assertEqual(res["evaluation"], "BLOCK")
        self.assertFalse(res["safe_to_administer_simultaneously"])
        self.assertIn("CYP3A4", res["enzymes_and_transporters_modulated"])
        self.assertTrue(any("Hemorrhage" in c["clinical_risk"] for c in res["conflicts"]))

    # 8. DYNAMIC HAKEEM SAHAB CASE BRIEF TESTS
    def test_dynamic_hakeem_case_brief_synthesis(self):
        ctx = {
            "name": "Fatima Begum",
            "age": 28,
            "gender": "female",
            "chief_complaints": ["irregular menses", "weight gain", "facial hirsutism"],
            "mizaj": "Balgham"
        }
        brief = HakeemCaseBriefEngine.generate_case_brief("PT-007", ctx)
        self.assertIn("Fatima Begum", brief["case_summary"])
        self.assertIn("irregular menses", brief["case_summary"])
        self.assertIn("female", brief["case_summary"])
        self.assertTrue(any("Jigar-Rahim" in a["axis"] for a in brief["axis_map"]))

    # 9. LIVE REST API ENDPOINTS TESTS
    def test_live_api_qaroorah_endpoint(self):
        payload = {
            "patient_id": "PT-API-01",
            "inspection": {
                "lawn": "Asfar Na'i (Deep bright yellow)",
                "qiwam": "Raqeeq",
                "safa": "Safi",
                "rusoob": "None",
                "boo": "Hadd (Pungent)"
            }
        }
        resp = self._execute_post("/api/v1/clinical/diagnostics/qaroorah-analyze", payload)
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["qaroorah_diagnostic"]["dominant_humor_inferred"], "Safra")

    def test_live_api_asbab_sitta_endpoint(self):
        payload = {
            "patient_id": "PT-API-02",
            "patient_mizaj": "Balghami",
            "lifestyle": {
                "air_quality_exposure": "CLEAN",
                "daily_sedentary_hours": 4.0,
                "sleep_hours_per_night": 8.0,
                "constipation_present": False
            }
        }
        resp = self._execute_post("/api/v1/clinical/lifestyle/asbab-sitta-score", payload)
        self.assertTrue(resp["ok"])
        self.assertGreaterEqual(resp["asbab_sitta_evaluation"]["asbab_sitta_equilibrium_score"], 80.0)

    def test_live_api_munzij_mushil_endpoint(self):
        payload = {
            "patient_id": "PT-API-03",
            "target_humor": "Safra",
            "has_active_nujz": False
        }
        resp = self._execute_post("/api/v1/therapeutic/nuskha/munzij-mushil-protocol", payload)
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["munzij_mushil_protocol"]["target_pathological_humor"], "Safra")

    def test_live_api_cyp450_endpoint(self):
        payload = {
            "current_allopathic_medications": ["Atorvastatin 20mg"],
            "candidate_herbs": ["Piperine 20mg"]
        }
        resp = self._execute_post("/api/v1/therapeutic/interactions/cyp450-check", payload)
        self.assertTrue(resp["ok"])
        self.assertEqual(resp["cyp450_evaluation"]["evaluation"], "CAUTION")


if __name__ == "__main__":
    unittest.main()
