"""
ZAYVORA Health OS™ — Test Suite #67
===================================
Digital Biomarker & Continuous Monitoring OS (Phase 20) & N-of-1 Personalized Evidence (Phase 21)
- Multi-stream Telemetry Ingestion (Wearables, Home Vitals, Ambient Dynamics)
- 4 Canonical Early Risk Signal Detectors (Thermal Polarization, Autonomic Dyscrasia, VAS Rebound, Adherence Erosion)
- Humoral Stability Index Computation
- Single-Subject Within-Patient Effect Size (Cohen's d_N=1)
- Asbab-e-Sittah Ambient Temperature vs. Pain Correlation
- Individualized Bayesian Response Probability
- Clinical Orchestrator Stages 15 & 16 Integration
- Live REST Endpoints for Ingestion, Telemetry Signals & N-of-1 Dossier
"""

import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.clinical.app.engines.continuous_monitoring_engine import (
    ContinuousMonitoringEngine,
    ContinuousMonitoringReport,
    ClinicianRiskSignal,
    RiskSignalType,
    AlertSeverity,
)
from services.clinical.app.engines.n_of_1_evidence_engine import (
    NOf1EvidenceEngine,
    LongitudinalObservation,
    NOf1Dossier,
)
from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
    ClinicalIntelligenceCoreOrchestrator,
    ClinicalContinuumRequest,
)


class TestContinuousMonitoringAndNOf1Evidence(unittest.TestCase):
    """Suite #67: Continuous Monitoring & N-of-1 Personalized Evidence Verification"""

    def test_telemetry_ingestion_and_aggregation(self):
        """Verifies multi-stream data ingestion and rolling metric computation."""
        engine = ContinuousMonitoringEngine()
        data = [
            {"resting_hr_bpm": 70.0, "hrv_sdnn_ms": 48.0, "sleep_efficiency_pct": 85.0, "daily_steps": 6000, "doses_taken": 2, "doses_prescribed": 2},
            {"resting_hr_bpm": 74.0, "hrv_sdnn_ms": 52.0, "sleep_efficiency_pct": 87.0, "daily_steps": 6400, "doses_taken": 2, "doses_prescribed": 2},
            {"resting_hr_bpm": 72.0, "hrv_sdnn_ms": 50.0, "sleep_efficiency_pct": 86.0, "daily_steps": 6200, "doses_taken": 2, "doses_prescribed": 2},
        ]
        count = engine.ingest_telemetry_batch("P-TEST-001", data)
        self.assertEqual(count, 3)

        report = engine.analyze_patient_telemetry("P-TEST-001")
        self.assertEqual(report.patient_id, "P-TEST-001")
        self.assertEqual(report.analyzed_window_days, 3)
        self.assertEqual(report.mean_resting_hr, 72.0)
        self.assertEqual(report.mean_hrv_sdnn, 50.0)
        self.assertEqual(report.overall_adherence_pct, 100.0)
        self.assertEqual(len(report.active_signals), 0)
        self.assertEqual(report.humoral_stability_index, 1.0)

    def test_thermal_polarization_spike_detection(self):
        """Tests early detection of Safrawi acute inflammatory flare (HR > 85 bpm + sleep < 70%)."""
        engine = ContinuousMonitoringEngine()
        data = [
            {"resting_hr_bpm": 89.0, "hrv_sdnn_ms": 38.0, "sleep_efficiency_pct": 62.0, "daily_steps": 3200}
        ]
        engine.ingest_telemetry_batch("P-HEAT-001", data)
        report = engine.analyze_patient_telemetry("P-HEAT-001")

        self.assertEqual(len(report.active_signals), 1)
        sig = report.active_signals[0]
        self.assertEqual(sig.signal_type, RiskSignalType.THERMAL_POLARIZATION_SPIKE)
        self.assertEqual(sig.severity, AlertSeverity.ELEVATED)
        self.assertIn("Thermal Polarization Spike", sig.headline)
        self.assertIn("Ghalba-e-Hararah", sig.clinical_mechanism)

    def test_autonomic_dyscrasia_detection(self):
        """Tests autonomic dyscrasia trigger when HRV SDNN falls below 25 ms."""
        engine = ContinuousMonitoringEngine()
        data = [
            {"resting_hr_bpm": 78.0, "hrv_sdnn_ms": 21.5, "sleep_efficiency_pct": 78.0, "daily_steps": 4100}
        ]
        engine.ingest_telemetry_batch("P-AUTO-001", data)
        report = engine.analyze_patient_telemetry("P-AUTO-001")

        self.assertEqual(len(report.active_signals), 1)
        sig = report.active_signals[0]
        self.assertEqual(sig.signal_type, RiskSignalType.AUTONOMIC_DYSCRASIA)
        self.assertEqual(sig.severity, AlertSeverity.MODERATE)
        self.assertIn("Du'f al-Qalb", sig.headline)

    def test_vas_rebound_relapse_detection(self):
        """Tests relapse (Intikas) detection when VAS rebounds by >= 2.0 points above nadir."""
        engine = ContinuousMonitoringEngine()
        data = [
            {"resting_hr_bpm": 75.0, "hrv_sdnn_ms": 45.0, "sleep_efficiency_pct": 80.0, "daily_steps": 5000, "daily_pain_vas": 5.0}
        ]
        engine.ingest_telemetry_batch("P-REB-001", data)
        # Established nadir was 2.0 -> jump of +3.0 points
        report = engine.analyze_patient_telemetry("P-REB-001", established_vas_nadir=2.0)

        vas_signals = [s for s in report.active_signals if s.signal_type == RiskSignalType.VAS_REBOUND]
        self.assertEqual(len(vas_signals), 1)
        self.assertEqual(vas_signals[0].severity, AlertSeverity.CRITICAL)
        self.assertIn("Intikas", vas_signals[0].headline)

    def test_adherence_erosion_detection(self):
        """Tests alert generation when medication adherence drops below 60%."""
        engine = ContinuousMonitoringEngine()
        data = [
            {"resting_hr_bpm": 72.0, "hrv_sdnn_ms": 45.0, "sleep_efficiency_pct": 82.0, "daily_steps": 5000, "doses_taken": 5, "doses_prescribed": 10}
        ]
        engine.ingest_telemetry_batch("P-ADH-001", data)
        report = engine.analyze_patient_telemetry("P-ADH-001")

        adh_signals = [s for s in report.active_signals if s.signal_type == RiskSignalType.ADHERENCE_EROSION]
        self.assertEqual(len(adh_signals), 1)
        self.assertEqual(report.overall_adherence_pct, 50.0)

    def test_humoral_stability_index_computation(self):
        """Tests that multiple dyscrasia signals appropriately penalize the stability index."""
        engine = ContinuousMonitoringEngine()
        # High HR + Low HRV + Low sleep
        data = [
            {"resting_hr_bpm": 92.0, "hrv_sdnn_ms": 19.0, "sleep_efficiency_pct": 58.0, "daily_steps": 2500}
        ]
        engine.ingest_telemetry_batch("P-DYSC-001", data)
        report = engine.analyze_patient_telemetry("P-DYSC-001")

        self.assertGreaterEqual(len(report.active_signals), 2)
        self.assertLess(report.humoral_stability_index, 0.70)

    def test_n_of_1_cohens_d_effect_size(self):
        """Verifies calculation of within-patient standardized effect size."""
        base = [8.0, 8.5, 8.0, 9.0]
        interv = [2.5, 2.0, 1.5, 2.0]
        d = NOf1EvidenceEngine.calculate_cohens_d(base, interv)
        self.assertGreater(d, 5.0)  # Very large clinical effect size

    def test_n_of_1_weather_sensitivity_correlation(self):
        """Verifies Pearson r correlation between temperature drops and pain spikes."""
        temps = [12.0, 15.0, 18.0, 22.0, 25.0]
        pains = [8.5, 7.0, 5.5, 3.0, 2.0]  # Cold temperature correlates with higher pain
        r = NOf1EvidenceEngine.calculate_temperature_correlation(temps, pains)
        self.assertLess(r, -0.90)

    def test_n_of_1_dossier_synthesis(self):
        """Tests synthesis of the complete single-subject N-of-1 evidence dossier."""
        obs = [
            LongitudinalObservation(day_number=0, phase="BASELINE", symptom_vas=8.5, ambient_temp_c=14.0),
            LongitudinalObservation(day_number=3, phase="BASELINE", symptom_vas=8.0, ambient_temp_c=15.0),
            LongitudinalObservation(day_number=7, phase="INTERVENTION", symptom_vas=5.0, adherence_pct=95.0, ambient_temp_c=18.0),
            LongitudinalObservation(day_number=14, phase="INTERVENTION", symptom_vas=2.0, adherence_pct=92.0, ambient_temp_c=22.0),
            LongitudinalObservation(day_number=21, phase="MAINTENANCE", symptom_vas=1.5, adherence_pct=90.0, ambient_temp_c=24.0),
        ]

        dossier = NOf1EvidenceEngine.synthesize_n_of_1_dossier(
            patient_id="P-PAT-001",
            condition="Waja-ul-Mafasil",
            phenotype_code="PHENO-ARTH-BALGHAM",
            phenotype_name="Phlegmatic-Stagnant (Balghami Ghaleez)",
            observations=obs
        )

        self.assertEqual(dossier.patient_id, "P-PAT-001")
        self.assertEqual(dossier.total_observation_days, 5)
        self.assertGreaterEqual(dossier.within_patient_effect_size_d, 0.8)
        self.assertIn(dossier.effect_magnitude, ("LARGE", "VERY_LARGE"))
        self.assertGreaterEqual(dossier.bayesian_response_probability, 0.80)
        self.assertLess(dossier.weather_sensitivity_correlation, 0.0)
        self.assertIn("Standard therapeutic dose", dossier.personalized_posology_ceiling)

    def test_clinical_orchestrator_stage_15_and_16_integration(self):
        """Verifies end-to-end execution of continuum stages 15 & 16."""
        req = ClinicalContinuumRequest(
            patient_id="PAT-STAGE15-001",
            patient_name="Zafar Iqbal",
            age=54,
            gender="MALE",
            chief_complaints=["Severe knee stiffness", "Cold weather aggravation"],
            presenting_condition="Waja-ul-Mafasil",
            symptom_duration_days=60,
            baseline_pain_vas=8.5,
            constitutional_signs={"nabz": "Bateea", "mizaj": "Balghami"},
            targeted_axes=["mafasil", "meda-amaa"],
            candidate_drugs=["Suranjan Talkh", "Zanjabeel"],
            clinician_id="DOC-501",
            clinician_role="CHIEF_PHYSICIAN",
            followup_proms_day=14,
            followup_symptom_vas=2.0,
            followup_adverse_events=[]
        )

        resp = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)

        self.assertIsNotNone(resp.stage_15_continuous_monitoring)
        mon = resp.stage_15_continuous_monitoring
        self.assertEqual(mon["patient_id"], "PAT-STAGE15-001")
        self.assertIn("humoral_stability_index", mon)

        self.assertIsNotNone(resp.stage_16_n_of_1_evidence)
        n1 = resp.stage_16_n_of_1_evidence
        self.assertEqual(n1["patient_id"], "PAT-STAGE15-001")
        self.assertIn("within_patient_effect_size_d", n1)
        self.assertIn("bayesian_response_probability", n1)

    def test_live_api_server_monitoring_and_n1_endpoints(self):
        """Verifies live REST API server registration for monitoring and N-of-1."""
        import services.live_api_server as server
        self.assertIsNotNone(server.ContinuousMonitoringEngine)
        self.assertIsNotNone(server.global_monitoring_engine)
        self.assertIsNotNone(server.NOf1EvidenceEngine)
        self.assertIsNotNone(server.LongitudinalObservation)


if __name__ == "__main__":
    unittest.main()
