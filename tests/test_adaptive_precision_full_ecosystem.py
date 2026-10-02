"""
ZAYVORA Health OS™ — Test Suite #68: Adaptive Precision OS & Global Learning Ecosystem
========================================================================================
Comprehensive clinical and mathematical verification of Phases 22-27:
- Phase 22: Clinical Trial OS (CDISC ODM, Permuted Block Randomization, DSMB Stopping Rules)
- Phase 23: Federated Multi-Clinic Learning ((eps, delta)-DP, FedAvg, HMAC Authentication)
- Phase 25: Clinical Simulation & Digital Twin Layer (Markov DTMC, Prediction != Diagnosis)
- Phase 26: Global Clinical Knowledge Localization (FDA, EMA HMPC, GCC, AYUSH, WHO Crosswalk)
- Phase 27: Population Learning Network (Macro-Surveillance, PRR / Chi-Square Safety Signals)
- Master 21-Stage Clinical Intelligence Orchestrator End-to-End Execution
- Live REST Server API Endpoints Parity
"""

import math
import os
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in [repo_root, os.path.join(repo_root, "services", "knowledge"), os.path.join(repo_root, "services", "clinical"), os.path.join(repo_root, "services", "therapeutic"), os.path.join(repo_root, "services", "ai")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)

from services.clinical.app.engines.clinical_trial_os_engine import (
    ClinicalTrialOSEngine,
    TrialPhase,
    BlindingType,
    DeviationSeverity,
    TrialStatus,
    TreatmentArm,
    eDCCaseReportForm,
)
from services.clinical.app.engines.federated_learning_engine import (
    FederatedLearningEngine,
    ClinicNodeCredentials,
    LocalModelUpdate,
)
from services.clinical.app.engines.digital_twin_simulation_engine import (
    DigitalTwinSimulationEngine,
    HumoralState,
    SimulationConfig,
)
from services.knowledge.app.core.global_localization_engine import (
    GlobalLocalizationEngine,
    RegulatoryJurisdiction,
    RegulatoryCategory,
)
from services.clinical.app.engines.population_learning_network import (
    PopulationLearningNetworkEngine,
    CanonicalMausim,
    MacroWeatherTelemetry,
)
from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
    ClinicalIntelligenceCoreOrchestrator,
    ClinicalContinuumRequest,
)


class TestAdaptivePrecisionFullEcosystem(unittest.TestCase):

    # -------------------------------------------------------------------------
    # Phase 22: Clinical Trial OS Engine
    # -------------------------------------------------------------------------
    def test_01_clinical_trial_permuted_block_randomization(self):
        trial = ClinicalTrialOSEngine(
            trial_id="TR-TEST-001",
            study_title="Pragmatic Unani Trial for Osteoarthritis",
            phase=TrialPhase.PHASE_3_COMPARATIVE_EFFECTIVENESS,
            blinding=BlindingType.DOUBLE_BLIND,
        )
        arm_a = TreatmentArm(
            arm_id="ARM-UNANI",
            arm_name="Classical Munzij-Mushil + Majun Suranjan",
            arm_type="INVESTIGATIONAL_UNANI",
            description="Active Unani Protocol",
            intervention_formula={"drugs": ["Suranjan Talkh", "Zanjabeel"]},
            dosing_schedule="B.I.D.",
        )
        arm_b = TreatmentArm(
            arm_id="ARM-CTRL",
            arm_name="Standard of Care Analgesia",
            arm_type="ACTIVE_CONTROL",
            description="Standard Care",
            intervention_formula={"drugs": ["Paracetamol"]},
            dosing_schedule="Daily",
        )
        trial.register_treatment_arm(arm_a)
        trial.register_treatment_arm(arm_b)

        # Gate trial with IRB credentials
        trial.set_irb_approval(irb_code="IRB-APPROVAL-9941", pi_id="PI-DR-QASIM")
        self.assertEqual(trial.status, TrialStatus.ACTIVE_ENROLLING)

        # Randomize 8 subjects (2 blocks of 4)
        subjects = []
        for i in range(8):
            subj = trial.randomize_subject(patient_mrn=f"MRN-TEST-{i:03d}", stratum="BALGHAMI")
            subjects.append(subj)
            self.assertTrue(subj.blinded_kit_code.startswith("KIT-"))
            self.assertEqual(subj.trial_id, "TR-TEST-001")

        # Verify exact 1:1 balance in 8 subjects (4 in arm A, 4 in arm B)
        arm_counts = {arm_a.arm_id: 0, arm_b.arm_id: 0}
        for s in subjects:
            arm_counts[s.arm_id] += 1
        self.assertEqual(arm_counts["ARM-UNANI"], 4)
        self.assertEqual(arm_counts["ARM-CTRL"], 4)

    def test_02_clinical_trial_edc_deviations_and_dsmb_export(self):
        trial = ClinicalTrialOSEngine(
            trial_id="TR-SAFETY-002",
            study_title="Safety Trial",
            phase=TrialPhase.PHASE_2_DOSE_FINDING_PROOF_OF_CONCEPT,
            blinding=BlindingType.DOUBLE_BLIND,
        )
        trial.register_treatment_arm(TreatmentArm("ARM-1", "Arm 1", "UNANI", "Desc", {}, "B.I.D."))
        trial.register_treatment_arm(TreatmentArm("ARM-2", "Arm 2", "CTRL", "Desc", {}, "Daily"))
        trial.set_irb_approval("IRB-TEST-02", "PI-ALVI")

        # Enroll subjects and log CRFs
        s1 = trial.randomize_subject("MRN-S1")
        s2 = trial.randomize_subject("MRN-S2")

        crf1 = eDCCaseReportForm(
            crf_id="CRF-01",
            trial_id=trial.trial_id,
            subject_id=s1.subject_id,
            visit_code="V0_BASELINE",
            recorded_at="2026-09-19T00:00:00Z",
            recorded_by="CR-COORD-01",
            symptom_vas=7.5,
            mizaj_deviation_score=3.0,
            functional_biomarkers={"crp": 5.2},
            doses_taken=14,
            doses_scheduled=14,
            adverse_events=[{"name": "Mild Head Rush", "is_serious": False}],
        )
        trial.record_edc_crf(crf1)
        self.assertEqual(crf1.compliance_pct, 100.0)

        # Log a protocol deviation
        dev = trial.log_protocol_deviation(
            subject_id=s1.subject_id,
            visit_id="V0_BASELINE",
            deviation_code="DEV-VISIT-WINDOW",
            severity=DeviationSeverity.MINOR,
            description="Patient attended baseline visit 1 day late due to transport delay.",
            clinician_id="CLINICIAN-01",
        )
        self.assertEqual(dev.severity, DeviationSeverity.MINOR)
        self.assertEqual(len(trial.deviations), 1)

        # DSMB Interim Safety Export
        dsmb = trial.generate_dsmb_safety_export(analysis_num=1)
        self.assertEqual(dsmb.trial_id, trial.trial_id)
        self.assertEqual(dsmb.total_enrolled, 2)
        self.assertFalse(dsmb.stopping_recommended)

        # CDISC ODM export
        cdisc = trial.to_cdisc_odm_summary()
        self.assertEqual(cdisc["odm_version"], "1.3.2")
        self.assertEqual(cdisc["study"]["study_oid"], "STUDY.TR-SAFETY-002")

    # -------------------------------------------------------------------------
    # Phase 23: Federated Multi-Clinic Learning Engine
    # -------------------------------------------------------------------------
    def test_03_federated_learning_hmac_and_dp_noise(self):
        engine = FederatedLearningEngine(
            model_id="FED-TEST-2026",
            initial_weights={"w_dam": 0.25, "w_safra": 0.25, "w_balgham": 0.25, "w_sawda": 0.25},
            min_node_quorum=2,
            epsilon_per_round=0.5,
            max_total_epsilon=5.0,
            sensitivity_clip_c=1.0,
        )

        token1 = engine.register_clinic_node("NODE-1", "Central Matab Delhi", "New Delhi")
        token2 = engine.register_clinic_node("NODE-2", "NIUM Hospital", "Bengaluru")
        self.assertEqual(len(engine.registered_nodes), 2)

        # Submit valid updates
        w1 = {"w_dam": 0.30, "w_safra": 0.20, "w_balgham": 0.28, "w_sawda": 0.22}
        sig1 = engine.sign_update_payload("NODE-1", w1, samples=50)
        up1 = engine.submit_local_update("NODE-1", 50, w1, sig1, apply_dp_locally=True)
        self.assertEqual(up1.round_number, 1)

        # Submit forged signature should fail
        with self.assertRaises(ValueError):
            engine.submit_local_update("NODE-2", 40, w1, "FORGED_SIGNATURE_HASH", apply_dp_locally=True)

        w2 = {"w_dam": 0.22, "w_safra": 0.28, "w_balgham": 0.24, "w_sawda": 0.26}
        sig2 = engine.sign_update_payload("NODE-2", w2, samples=50)
        up2 = engine.submit_local_update("NODE-2", 50, w2, sig2, apply_dp_locally=True)

        # Aggregate round
        snapshot = engine.aggregate_round()
        self.assertEqual(snapshot.round_number, 1)
        self.assertEqual(snapshot.participating_nodes_count, 2)
        self.assertEqual(snapshot.total_samples_represented, 100)
        self.assertGreater(snapshot.cumulative_epsilon, 0.0)

        # Audit manifest check
        manifest = engine.get_audit_manifest()
        self.assertTrue(manifest["zero_raw_phi_guarantee"])
        self.assertTrue(manifest["cryptographic_hmac_enforced"])

    # -------------------------------------------------------------------------
    # Phase 25: Clinical Simulation & Digital Twin Layer
    # -------------------------------------------------------------------------
    def test_04_digital_twin_markov_simulation_and_guardrails(self):
        res = DigitalTwinSimulationEngine.run_simulation(
            patient_id="P-TWIN-001",
            initial_mizaj="Balghami (Cold & Moist)",
            baseline_vas=8.0,
            config=SimulationConfig(
                simulation_days=60,
                adherence_factor=0.92,
                has_munzij_mushil=True,
                has_strict_parhez=True,
                has_regimental_therapy=True,
                cohort_sample_size=300,
            ),
        )

        self.assertEqual(res.baseline_dominant_state, HumoralState.BALGHAMI)
        self.assertEqual(res.baseline_symptom_vas, 8.0)
        self.assertGreater(res.probability_restitution_at_day_60, res.probability_restitution_at_day_30)
        self.assertGreater(len(res.trajectory_curve), 4)

        # Pain VAS trajectory must decrease monotonically on average
        v0 = res.trajectory_curve[0].mean_projected_vas
        v_latest = res.trajectory_curve[-1].mean_projected_vas
        self.assertLess(v_latest, v0)

        # STRICT Programmatic Guardrail: Prediction != Diagnosis
        self.assertFalse(res.is_clinical_diagnosis)
        self.assertFalse(res.prediction_equals_diagnosis)
        self.assertIn("IN-SILICO MARKOV SIMULATION ONLY", res.simulation_disclaimer)
        self.assertIn("Prediction != Diagnosis", res.simulation_disclaimer)

    # -------------------------------------------------------------------------
    # Phase 26: Global Clinical Knowledge Localization Engine
    # -------------------------------------------------------------------------
    def test_05_global_localization_crosswalk_and_prescription_audit(self):
        # Lookup Asgandh crosswalk
        asg = GlobalLocalizationEngine.get_crosswalk("ASGANDH")
        self.assertIsNotNone(asg)
        self.assertEqual(asg.botanical_name, "Withania somnifera (L.) Dunal")

        # US FDA: Dietary supplement under DSHEA
        us_rule = asg.jurisdiction_rules[RegulatoryJurisdiction.US_FDA]
        self.assertEqual(us_rule.category, RegulatoryCategory.DIETARY_SUPPLEMENT)
        self.assertIn("Food and Drug Administration", us_rule.mandatory_label_warning)

        # Lookup Suranjan Talkh (Colchicum luteum Baker)
        sur = GlobalLocalizationEngine.get_crosswalk("SURANJAN_TALKH")
        self.assertIsNotNone(sur)

        # AYUSH: Schedule E1 poison requiring prescription
        ayush_rule = sur.jurisdiction_rules[RegulatoryJurisdiction.IN_AYUSH]
        self.assertEqual(ayush_rule.category, RegulatoryCategory.PRESCRIPTION_ONLY_SCHEDULE_E1)
        self.assertTrue(ayush_rule.requires_prescription)

        # US FDA: Prohibited in OTC dietary supplements
        fda_rule = sur.jurisdiction_rules[RegulatoryJurisdiction.US_FDA]
        self.assertTrue(fda_rule.is_prohibited)

        # Prescription Audit for US FDA export (should flag Suranjan as prohibited)
        audit_us = GlobalLocalizationEngine.audit_prescription_for_jurisdiction(
            drug_items=[
                {"drug_name": "Asgandh", "daily_dose_mg": 800.0},
                {"drug_name": "Suranjan Talkh", "daily_dose_mg": 150.0},
            ],
            target_jurisdiction=RegulatoryJurisdiction.US_FDA,
        )
        self.assertFalse(audit_us.is_fully_compliant)
        self.assertTrue(any("Prohibited in US_FDA" in p for p in audit_us.prohibited_items))

        # Prescription Audit for AYUSH (compliant with prescription)
        audit_ayush = GlobalLocalizationEngine.audit_prescription_for_jurisdiction(
            drug_items=[
                {"drug_name": "Asgandh", "daily_dose_mg": 3000.0},
                {"drug_name": "Zanjabeel", "daily_dose_mg": 1500.0},
            ],
            target_jurisdiction=RegulatoryJurisdiction.IN_AYUSH,
        )
        self.assertTrue(audit_ayush.is_fully_compliant)
        self.assertIn("AYUSH_CLASSICAL_UNANI_MEDICINE", audit_ayush.eligible_product_class)

    # -------------------------------------------------------------------------
    # Phase 27: Population Learning Network Engine
    # -------------------------------------------------------------------------
    def test_06_population_learning_and_prr_safety_signals(self):
        # Weather coupling & seasonal advisory
        telemetry = MacroWeatherTelemetry(
            region_id="IN-DELHI-NCR",
            ambient_temp_c=14.5,
            relative_humidity_pct=72.0,
            barometric_pressure_hpa=1018.0,
            recorded_at="2026-01-15T08:00:00Z",
        )
        vuln = PopulationLearningNetworkEngine.compile_seasonal_vulnerability(telemetry)
        self.assertEqual(vuln.season, CanonicalMausim.MAUSIM_E_SHITA)
        self.assertEqual(vuln.predominant_humor, "Balgham (Phlegm)")

        # Evans / WHO PRR Signal Detection:
        # a=5 (Drug + Nausea), b=45 (Drug + Other ADRs), c=10 (Other drugs + Nausea), d=490 (Other drugs + Other ADRs)
        # Rate in drug = 5/50 = 0.10. Rate in control = 10/500 = 0.02. PRR = 5.0 (Signal!)
        signal = PopulationLearningNetworkEngine.evaluate_pharmacovigilance_signal(
            suspected_drug="Suranjan Talkh",
            adverse_reaction="Severe Nausea & Diarrhea",
            a=5,
            b=45,
            c=10,
            d=490,
        )
        self.assertTrue(signal.is_statistically_significant_signal)
        self.assertGreaterEqual(signal.proportional_reporting_ratio, 2.0)
        self.assertGreaterEqual(signal.chi_square_yates, 4.0)
        self.assertIn(signal.signal_strength, ("CONFIRMED_SIGNAL", "CRITICAL_SAFETY_HOLD"))

        # Population Census
        census = PopulationLearningNetworkEngine.generate_population_census(
            patient_records=[
                {"dominant_humor": "Balghami", "phenotype_code": "PHENO-ARTH-01"},
                {"dominant_humor": "Safrawi", "phenotype_code": "PHENO-HEP-02"},
                {"dominant_humor": "Balghami", "phenotype_code": "PHENO-ARTH-01"},
            ],
            clinic_ids=["CLINIC-A", "CLINIC-B"],
        )
        self.assertEqual(census.total_active_patients, 3)
        self.assertEqual(census.participating_clinics_count, 2)
        self.assertGreater(census.humoral_distribution["Balghami (Phlegmatic)"], 50.0)

    # -------------------------------------------------------------------------
    # Master Clinical Orchestrator: Full 21-Stage Continuum
    # -------------------------------------------------------------------------
    def test_07_master_orchestrator_complete_21_stages(self):
        req = ClinicalContinuumRequest(
            patient_id="P-2026-ECOSYSTEM-99",
            patient_name="Tariq Mansoor",
            age=49,
            gender="Male",
            chief_complaints=["Bilateral knee swelling", "Morning joint stiffness > 45 mins", "Aggravated by wet weather"],
            presenting_condition="Waja-ul-Mafasil",
            symptom_duration_days=90,
            baseline_pain_vas=8.2,
            constitutional_signs={
                "nabz_speed": "Bati (Slow)",
                "nabz_strength": "Layyin (Soft)",
                "baul_color": "Abyad (Pale/Whitish)",
                "baraz_consistency": "Layyin",
                "skin_temperature": "Barid (Cold)",
            },
            targeted_axes=["mafasil", "meda-amaa"],
            candidate_drugs=["Suranjan Talkh", "Asgandh", "Zanjabeel"],
            clinician_id="CLIN-HAKEEM-007",
            clinician_role="HAKEEM_CLINICIAN",
            followup_proms_day=14,
            followup_symptom_vas=3.8,
            followup_adverse_events=[],
            target_regulatory_jurisdiction="IN_AYUSH",
        )

        res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)

        # Verify all 21 stages exist and are populated
        self.assertIsNotNone(res.stage_1_patient_profile)
        self.assertIsNotNone(res.stage_2_triage_assessment)
        self.assertIsNotNone(res.stage_3_mizaj_quantification)
        self.assertIsNotNone(res.stage_4_organ_axis_targeting)
        self.assertIsNotNone(res.stage_5_knowledge_retrieval)
        self.assertIsNotNone(res.stage_6_evidence_hierarchy)
        self.assertIsNotNone(res.stage_7_safety_firewall)
        self.assertIsNotNone(res.stage_8_hakeem_sahab_brief)
        self.assertIsNotNone(res.stage_9_clinician_approval)
        self.assertIsNotNone(res.stage_10_nuskha_and_parhez)
        self.assertIsNotNone(res.stage_11_proms_followup)
        self.assertIsNotNone(res.stage_12_outcome_and_learning)
        self.assertIsNotNone(res.stage_13_precision_patient_model)
        self.assertIsNotNone(res.stage_14_phenotype_and_response)
        self.assertIsNotNone(res.stage_15_continuous_monitoring)
        self.assertIsNotNone(res.stage_16_n_of_1_evidence)
        self.assertIsNotNone(res.stage_17_clinical_trial_os)
        self.assertIsNotNone(res.stage_18_federated_learning)
        self.assertIsNotNone(res.stage_19_digital_twin_simulation)
        self.assertIsNotNone(res.stage_20_global_localization)
        self.assertIsNotNone(res.stage_21_population_learning_network)

        # Deep assertion on Stage 17 (Trial OS)
        self.assertTrue(res.stage_17_clinical_trial_os["blinded_kit_code"].startswith("KIT-"))
        self.assertEqual(res.stage_17_clinical_trial_os["cdisc_odm"]["odm_version"], "1.3.2")

        # Deep assertion on Stage 18 (Federated Learning)
        self.assertTrue(res.stage_18_federated_learning["zero_raw_phi_guarantee"])
        self.assertGreater(res.stage_18_federated_learning["cumulative_epsilon"], 0.0)

        # Deep assertion on Stage 19 (Digital Twin)
        self.assertFalse(res.stage_19_digital_twin_simulation["is_clinical_diagnosis"])
        self.assertIn("IN-SILICO MARKOV SIMULATION ONLY", res.stage_19_digital_twin_simulation["simulation_disclaimer"])

        # Deep assertion on Stage 20 (Localization)
        self.assertEqual(res.stage_20_global_localization["target_jurisdiction"], "IN_AYUSH")

        # Deep assertion on Stage 21 (Population Network)
        self.assertIn("humoral_distribution", res.stage_21_population_learning_network)

        # Compliance summary
        self.assertTrue(res.compliance_summary["clinical_trial_cdisc_odm_ready"])
        self.assertTrue(res.compliance_summary["federated_dp_epsilon_guarantee"])
        self.assertTrue(res.compliance_summary["simulation_prediction_ne_diagnosis_enforced"])
        self.assertTrue(res.compliance_summary["global_regulatory_crosswalk_validated"])

    # -------------------------------------------------------------------------
    # Live REST Server Endpoints Parity
    # -------------------------------------------------------------------------
    def test_08_live_server_endpoints_parity(self):
        import services.live_api_server as server

        self.assertIsNotNone(server.ClinicalTrialOSEngine)
        self.assertIsNotNone(server.FederatedLearningEngine)
        self.assertIsNotNone(server.DigitalTwinSimulationEngine)
        self.assertIsNotNone(server.GlobalLocalizationEngine)
        self.assertIsNotNone(server.PopulationLearningNetworkEngine)


if __name__ == "__main__":
    unittest.main(verbosity=2)
