"""
Test Suite #63: Murakkab Intelligence, Closed-Loop Pharmacy, Outcome Intelligence & Pharmacovigilance
===================================================================================================
Verifies Phases 5, 8, 9, and 10 of the ZAYVORA Clinical Evolution Roadmap:
1. Murakkab Intelligence & Formulation Compatibility Engine:
   - Mandatory classical source citations for CLASSICAL_FORMULATION.
   - Mandatory adaptation rationale for CLASSICAL_ADAPTATION.
   - Ingredient role enforcement (Juz-e-Azam, Muawin, Musleh, Badal, Badraqa).
   - Thermal/moisture conflict detection & Schedule E(1) Mudabbar enforcement.
2. Closed-Loop Pharmacy & eBMR Engine:
   - Prescription verification with 21 CFR Part 11 clinician signature.
   - FEFO lot allocation and inventory deduction.
   - Blocking uncertified or quarantined batches.
   - Multi-stage eBMR batch lifecycle (Raw Material QC -> Tadbeer -> Compounding -> IPC -> Release).
3. Outcome Intelligence Engine ("What Changed?"):
   - Longitudinal delta tracking: VAS symptom relief, biomarker shifts, Mizaj restitution.
   - Authoritative classification: Kamil (>=80%), Juz'i (40-79%), Ghair Mu'athir (<40%), Intikas (>20% worsening).
   - HIPAA Safe Harbor de-identification & RWE learning feed eligibility.
4. Safety Intelligence & Pharmacovigilance Engine:
   - Traceable ADR reporting with WHO-UMC causality evaluation.
   - Automatic batch quarantine upon serious adverse event or high causality.
   - Standardized AYUSH National Yellow Form emission.
"""

import os
import sys
import io
import json
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.therapeutic.app.engines.murakkab_intelligence_engine import (
    MurakkabIntelligenceEngine,
    MurakkabCategory,
    IngredientRole,
    FormulaIngredient
)
from services.therapeutic.app.engines.closed_loop_pharmacy_engine import (
    ClosedLoopPharmacyEngine,
    BatchStage,
    DispenseStatus,
    InventoryLot
)
from services.clinical.app.engines.outcome_intelligence_engine import (
    OutcomeIntelligenceEngine,
    ClassicalOutcome,
    BiomarkerObservation
)
from services.therapeutic.app.engines.safety_intelligence_pharmacovigilance import (
    SafetyIntelligenceEngine,
    ADRSeverity,
    WHOUmcCausality,
    SafetyAction
)
from services.live_api_server import ZayvoraApiHandler


def _call_get(path):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {}
    req.request_version = "HTTP/1.1"
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_GET()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


def _call_post(path, payload):
    data = json.dumps(payload).encode()
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {"Content-Length": str(len(data))}
    req.request_version = "HTTP/1.1"
    req.rfile = io.BytesIO(data)
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_POST()
    raw = req.wfile.getvalue().decode()
    body = raw.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw else raw
    return json.loads(body)


class TestMurakkabPharmacyOutcomesSafety(unittest.TestCase):

    def test_01_murakkab_classical_citation_mandate(self):
        """Verify CLASSICAL_FORMULATION requires valid bibliographical citation."""
        ing1 = FormulaIngredient(
            drug_id="ustukhuddus",
            drug_name="Ustukhuddus",
            botanical_or_mineral_name="Lavandula stoechas",
            role=IngredientRole.JUZ_E_AZAM,
            parts_or_ratio=1.0,
            mizaj_hararat=1,
            mizaj_buroodat=0,
            mizaj_ratoobat=-2
        )
        bad_audit = MurakkabIntelligenceEngine.audit_formulation(
            name="Itrifal Ustukhuddus",
            category=MurakkabCategory.CLASSICAL_FORMULATION,
            ingredients=[ing1],
            citation_source=None
        )
        self.assertFalse(bad_audit.is_valid)
        self.assertTrue(any("CLASSICAL_FORMULATION must cite" in err for err in bad_audit.compliance_errors))

        good_audit = MurakkabIntelligenceEngine.audit_formulation(
            name="Itrifal Ustukhuddus",
            category=MurakkabCategory.CLASSICAL_FORMULATION,
            ingredients=[ing1],
            citation_source="Qarabadin-e-Azam, Vol 1, p. 112"
        )
        self.assertTrue(good_audit.is_valid)
        self.assertEqual(good_audit.provenance_details["governance_status"], "AUTHENTICATED_CLASSICAL")

    def test_02_murakkab_schedule_e1_mudabbar_enforcement(self):
        """Verify toxic Schedule E(1) drugs require certified Mudabbar status."""
        toxic_raw = FormulaIngredient(
            drug_id="suranjan",
            drug_name="Suranjan Talkh",
            botanical_or_mineral_name="Colchicum luteum",
            role=IngredientRole.JUZ_E_AZAM,
            parts_or_ratio=1.0,
            mizaj_hararat=3,
            mizaj_buroodat=0,
            mizaj_ratoobat=-3,
            is_schedule_e1=True,
            is_mudabbar_certified=False
        )
        audit = MurakkabIntelligenceEngine.audit_formulation(
            name="Majun Suranjan Experimental",
            category=MurakkabCategory.CLASSICAL_ADAPTATION,
            ingredients=[toxic_raw],
            adaptation_rationale="Modified dosage form for modern capsule delivery."
        )
        self.assertFalse(audit.is_valid)
        self.assertFalse(audit.schedule_e1_compliant)
        self.assertTrue(any("Mudabbar" in err for err in audit.compliance_errors))

    def test_03_murakkab_thermal_polarization_neutralization(self):
        """Verify extreme antagonistic mizaj without musleh triggers warning."""
        hot_drug = FormulaIngredient(
            drug_id="filfil_siah",
            drug_name="Filfil Siah",
            botanical_or_mineral_name="Piper nigrum",
            role=IngredientRole.JUZ_E_AZAM,
            parts_or_ratio=1.0,
            mizaj_hararat=3,
            mizaj_buroodat=0,
            mizaj_ratoobat=-3
        )
        cold_drug = FormulaIngredient(
            drug_id="kafoor",
            drug_name="Kafoor",
            botanical_or_mineral_name="Cinnamomum camphora",
            role=IngredientRole.MUAWIN,
            parts_or_ratio=0.5,
            mizaj_hararat=-3,
            mizaj_buroodat=3,
            mizaj_ratoobat=-2
        )
        audit_clash = MurakkabIntelligenceEngine.audit_formulation(
            name="Opposite Temperament Blend",
            category=MurakkabCategory.ZAYVORA_RND_FORMULATION,
            ingredients=[hot_drug, cold_drug],
            rnd_dossier_id="RND-2026-TAD-004"
        )
        self.assertTrue(len(audit_clash.antagonisms) > 0)
        self.assertLess(audit_clash.compatibility_score, 1.0)

        musleh_ing = FormulaIngredient(
            drug_id="samagh_arabi",
            drug_name="Samagh-e-Arabi",
            botanical_or_mineral_name="Acacia arabica",
            role=IngredientRole.MUSLEH,
            parts_or_ratio=0.5,
            mizaj_hararat=1,
            mizaj_buroodat=0,
            mizaj_ratoobat=1
        )
        audit_reconciled = MurakkabIntelligenceEngine.audit_formulation(
            name="Balanced Blend",
            category=MurakkabCategory.ZAYVORA_RND_FORMULATION,
            ingredients=[hot_drug, cold_drug, musleh_ing],
            rnd_dossier_id="RND-2026-TAD-004"
        )
        self.assertEqual(len(audit_reconciled.antagonisms), 0)
        self.assertIn("Samagh-e-Arabi", audit_reconciled.corrections_present)

    def test_04_closed_loop_dispensing_fefo_allocation(self):
        """Verify pharmacy dispensing enforces 21 CFR Part 11 and FEFO lot selection."""
        prescribed = [{"product_code": "itrifal_ustukhuddus", "quantity": 1, "name": "Itrifal Ustukhuddus"}]

        unauth_dispense = ClosedLoopPharmacyEngine.dispense_nuskha(
            nuskha_id="NSK-TEST-001",
            patient_id="MRN-TEST-101",
            clinician_signature="",
            is_signature_valid=False,
            prescribed_items=prescribed,
            pharmacist_id="PHARM-01"
        )
        self.assertEqual(unauth_dispense.status, DispenseStatus.BLOCKED_SAFETY_HOLD)
        self.assertTrue(any("Clinician Digital Signature" in r for r in unauth_dispense.blocking_reasons))

        auth_dispense = ClosedLoopPharmacyEngine.dispense_nuskha(
            nuskha_id="NSK-TEST-002",
            patient_id="MRN-TEST-102",
            clinician_signature="VALID-SHA256-DIGITAL-SIGNATURE",
            is_signature_valid=True,
            prescribed_items=prescribed,
            pharmacist_id="PHARM-01"
        )
        self.assertEqual(auth_dispense.status, DispenseStatus.DISPENSED_VERIFIED)
        self.assertEqual(len(auth_dispense.allocated_items), 1)
        self.assertEqual(auth_dispense.allocated_items[0]["allocated_lot"], "LOT-ITR-2026-08")

    def test_05_ebmr_manufacturing_lifecycle(self):
        """Verify multi-stage Electronic Batch Manufacturing Record (eBMR) progression."""
        batch_no = "BMR-2026-ITR-99"
        batch = ClosedLoopPharmacyEngine.initiate_ebmr_batch(
            batch_number=batch_no,
            product_name="Itrifal Ustukhuddus",
            target_qty=50.0,
            unit="kg"
        )
        self.assertEqual(batch.current_stage, BatchStage.RAW_MATERIAL_QC)

        ClosedLoopPharmacyEngine.advance_ebmr_stage(batch_no, BatchStage.TADBEER_PURIFICATION, officer_id="QA-01")
        self.assertTrue(batch.raw_material_qc_passed)

        ClosedLoopPharmacyEngine.advance_ebmr_stage(batch_no, BatchStage.COMPOUNDING, officer_id="PROD-02")
        self.assertTrue(batch.tadbeer_completed)

        ClosedLoopPharmacyEngine.advance_ebmr_stage(batch_no, BatchStage.IN_PROCESS_QC, officer_id="QC-03")
        self.assertTrue(batch.ipc_passed)

        final_batch = ClosedLoopPharmacyEngine.advance_ebmr_stage(batch_no, BatchStage.RELEASED_FOR_DISPENSING, officer_id="QA-DIRECTOR")
        self.assertEqual(final_batch.current_stage, BatchStage.RELEASED_FOR_DISPENSING)
        self.assertTrue(final_batch.qa_release_signed)
        self.assertEqual(final_batch.qa_officer_id, "QA-DIRECTOR")

    def test_06_outcome_intelligence_kamil_complete_remission(self):
        """Verify Outcome Intelligence calculates >=80% response as Kamil."""
        res = OutcomeIntelligenceEngine.evaluate_followup(
            patient_id="MRN-RWE-881",
            condition="Waja-ul-Mafasil",
            protocol_nuskha_id="NSK-RWE-881",
            day_in_treatment=28,
            vas_baseline=8.0,
            vas_followup=1.0,
            mizaj_deviation_baseline=6.0,
            mizaj_deviation_followup=0.5,
            adherence_percent=95.0,
            biomarkers=[
                BiomarkerObservation(marker_name="hs-CRP", baseline_value=12.0, followup_value=1.5, unit="mg/L", is_lower_better=True),
                BiomarkerObservation(marker_name="ESR", baseline_value=45.0, followup_value=12.0, unit="mm/hr", is_lower_better=True)
            ]
        )
        self.assertEqual(res.outcome_class, ClassicalOutcome.KAMIL)
        self.assertGreaterEqual(res.composite_improvement_index, 80.0)
        self.assertTrue(res.rwe_learning_eligible)
        self.assertTrue(len(res.deidentified_hash) >= 12)

    def test_07_outcome_intelligence_juz_i_and_intikas(self):
        """Verify Partial (Juz'i) and Relapse/Worsening (Intikas) classifications."""
        partial = OutcomeIntelligenceEngine.evaluate_followup(
            patient_id="MRN-RWE-882",
            condition="Ziabetus",
            protocol_nuskha_id="NSK-RWE-882",
            day_in_treatment=14,
            vas_baseline=6.0,
            vas_followup=3.0,
            mizaj_deviation_baseline=5.0,
            mizaj_deviation_followup=2.5,
            adherence_percent=85.0
        )
        self.assertEqual(partial.outcome_class, ClassicalOutcome.JUZ_I)

        relapse = OutcomeIntelligenceEngine.evaluate_followup(
            patient_id="MRN-RWE-883",
            condition="Waja-ul-Mafasil",
            protocol_nuskha_id="NSK-RWE-883",
            day_in_treatment=7,
            vas_baseline=5.0,
            vas_followup=8.0,
            mizaj_deviation_baseline=4.0,
            mizaj_deviation_followup=8.0,
            adherence_percent=90.0
        )
        self.assertEqual(relapse.outcome_class, ClassicalOutcome.INTIKAS)

    def test_08_pharmacovigilance_who_causality_and_auto_quarantine(self):
        """Verify WHO-UMC causality evaluation and automatic inventory quarantine."""
        adr = SafetyIntelligenceEngine.report_adverse_reaction(
            patient_id="MRN-SAFE-990",
            suspected_drug="Suranjan Shirin Mudabbar",
            lot_batch_number="LOT-SRJ-2026-01",
            adverse_reaction="Severe gastrointestinal distress and bradycardia",
            severity=ADRSeverity.SEVERE,
            onset_hours=3.0,
            dechallenge_positive=True,
            rechallenge_positive=True,
            concomitant_drugs=[],
            alternative_etiology_likely=False,
            clinician_id="DOC-IRFAN-BUMS"
        )
        self.assertEqual(adr.who_causality, WHOUmcCausality.CERTAIN)
        self.assertEqual(adr.immediate_action, SafetyAction.BATCH_QUARANTINED)
        self.assertTrue(adr.quarantine_enforced)
        self.assertTrue(adr.ayush_yellow_report["submission_ready"])
        self.assertEqual(adr.ayush_yellow_report["who_causality_grade"], "CERTAIN")

        alerts = SafetyIntelligenceEngine.get_active_alerts()
        self.assertTrue(any(a["lot"] == "LOT-SRJ-2026-01" for a in alerts))

    def test_09_live_api_server_endpoints(self):
        """Verify the new HTTP endpoints work via ZayvoraApiHandler."""
        # 1. Test GET /api/v1/safety/pharmacovigilance/active-alerts
        res_alerts = _call_get("/api/v1/safety/pharmacovigilance/active-alerts")
        self.assertTrue(res_alerts.get("ok"))
        self.assertIn("active_alerts", res_alerts)

        # 2. Test POST /api/v1/therapeutic/murakkab/audit-formula
        payload_audit = {
            "formula_name": "Itrifal Ustukhuddus Formula",
            "category": "CLASSICAL_FORMULATION",
            "citation_source": "Bayaz-e-Kabir, Vol II, p. 84",
            "ingredients": [
                {
                    "drug_id": "ustukhuddus",
                    "drug_name": "Ustukhuddus",
                    "role": "JUZ_E_AZAM",
                    "parts_or_ratio": 1.0,
                    "mizaj_hararat": 1,
                    "mizaj_buroodat": 0,
                    "mizaj_ratoobat": -2
                }
            ]
        }
        res_audit = _call_post("/api/v1/therapeutic/murakkab/audit-formula", payload_audit)
        self.assertTrue(res_audit.get("ok"))
        self.assertIn("audit_result", res_audit)
        self.assertEqual(res_audit["audit_result"]["provenance_details"]["governance_status"], "AUTHENTICATED_CLASSICAL")

        # 3. Test POST /api/v1/clinical/outcomes/record-followup
        payload_outcome = {
            "patient_id": "MRN-API-TEST-900",
            "condition": "Waja-ul-Mafasil",
            "protocol_nuskha_id": "NSK-API-900",
            "day_in_treatment": 28,
            "vas_baseline": 8.0,
            "vas_followup": 1.0,
            "mizaj_deviation_baseline": 6.0,
            "mizaj_deviation_followup": 0.5,
            "adherence_percent": 90.0
        }
        res_outcome = _call_post("/api/v1/clinical/outcomes/record-followup", payload_outcome)
        self.assertTrue(res_outcome.get("ok"))
        self.assertEqual(res_outcome["outcome_evaluation"]["outcome_class"], "KAMIL")

        # 4. Test GET /api/v1/clinical/outcomes/patient-trajectory/MRN-API-TEST-900
        res_traj = _call_get("/api/v1/clinical/outcomes/patient-trajectory/MRN-API-TEST-900")
        self.assertTrue(res_traj.get("ok"))
        self.assertEqual(len(res_traj["trajectory"]), 1)


if __name__ == "__main__":
    unittest.main()
