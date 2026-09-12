"""
Tests for Continuous Wearables Ingestion, Predictive Relapse Forecasting, and APM Observability
"""

try:
    import pytest
except ImportError:
    pytest = None

from app.wearables.wearable_engine import (
    WearableSample,
    WearableIngestionEngine,
    WearableSummary,
)
from app.predictive.relapse_forecaster import (
    PredictiveAssessmentInput,
    RelapseForecasterEngine,
    RelapseForecastReport,
)
from app.observability.telemetry import GLOBAL_TELEMETRY


def test_wearable_ingestion_and_rolling_summary():
    patient_id = "PAT-WEARABLE-001"
    sample1 = WearableSample(
        sample_id="W-1",
        patient_id=patient_id,
        timestamp_utc="2026-09-10T08:00:00Z",
        source_device="Apple Watch Ultra",
        hrv_rmssd_ms=55.0,
        hrv_sdnn_ms=62.0,
        resting_heart_rate_bpm=68,
        sleep_hours_total=7.5,
        deep_sleep_hours=1.8,
        rem_sleep_hours=1.9,
        spo2_average_pct=98.5,
        spo2_lowest_pct=95.0,
        respiratory_rate_bpm=14.5,
        daily_steps=8500,
        active_energy_kcal=420.0,
    )
    summary = WearableIngestionEngine.ingest_sample(sample1)

    assert summary.patient_id == patient_id
    assert summary.samples_count >= 1
    assert summary.rolling_7d_hrv_rmssd_ms == 55.0
    assert summary.quwwat_hayawaniyyah_index > 0.5
    assert summary.naum_yaqzah_score >= 0.8
    assert len(summary.active_anomalies) == 0


def test_wearable_anomaly_detection_autonomic_exhaustion():
    patient_id = "PAT-WEARABLE-ANOMALY"
    # Seed 3 normal baseline samples
    for i in range(3):
        WearableIngestionEngine.ingest_sample(WearableSample(
            sample_id=f"W-NORM-{i}",
            patient_id=patient_id,
            timestamp_utc=f"2026-09-0{i+1}T08:00:00Z",
            source_device="Oura Ring Gen 3",
            hrv_rmssd_ms=60.0,
            hrv_sdnn_ms=65.0,
            resting_heart_rate_bpm=64,
            sleep_hours_total=7.8,
            deep_sleep_hours=2.0,
            rem_sleep_hours=2.0,
            spo2_average_pct=98.0,
            spo2_lowest_pct=96.0,
            respiratory_rate_bpm=14.0,
            daily_steps=7500,
            active_energy_kcal=380.0,
        ))

    # Ingest an acute exhaustion sample (HRV collapses to 18ms, sleep collapses to 3.5h, SpO2 89%)
    exhaustion_sample = WearableSample(
        sample_id="W-EXHAUST",
        patient_id=patient_id,
        timestamp_utc="2026-09-04T08:00:00Z",
        source_device="Oura Ring Gen 3",
        hrv_rmssd_ms=18.0,  # >35% drop
        hrv_sdnn_ms=22.0,
        resting_heart_rate_bpm=98,  # Tachycardia
        sleep_hours_total=3.2,      # Severe sleep deprivation
        deep_sleep_hours=0.4,
        rem_sleep_hours=0.3,
        spo2_average_pct=91.0,
        spo2_lowest_pct=88.0,       # Nocturnal desaturation
        respiratory_rate_bpm=19.0,
        daily_steps=2100,
        active_energy_kcal=120.0,
    )
    summary = WearableIngestionEngine.ingest_sample(exhaustion_sample)

    assert len(summary.active_anomalies) >= 2
    anomaly_text = " ".join(summary.active_anomalies)
    assert "AUTONOMIC_EXHAUSTION" in anomaly_text
    assert "NOCTURNAL_DESATURATION" in anomaly_text
    assert "SEVERE_SLEEP_DEPRIVATION" in anomaly_text


def test_predictive_relapse_forecasting_stable():
    payload = PredictiveAssessmentInput(
        patient_id="PAT-PRED-STABLE",
        primary_unani_diagnosis="Niqras",
        baseline_mizaj="Damawi Motadil",
        current_mizaj_dominant="Damawi",
        mizaj_drift_velocity=0.10,
        tabiat_reserve_index=0.85,
        quwwat_hayawaniyyah_index=0.80,
        medication_adherence_pct=95.0,
        active_symptom_severity_delta=-0.4,
    )
    report = RelapseForecasterEngine.evaluate_relapse_risk(payload)

    assert report.relapse_probability_score < 0.25
    assert report.triage_band == "STABLE_EQUILIBRIUM"
    assert report.safe_to_lock is False
    assert report.requires_clinician_review is True


def test_predictive_relapse_forecasting_acute_deterioration():
    payload = PredictiveAssessmentInput(
        patient_id="PAT-PRED-ACUTE",
        primary_unani_diagnosis="Su-i-Mizaj Meda Haar",
        baseline_mizaj="Damawi Motadil",
        current_mizaj_dominant="Safrawi",
        mizaj_drift_velocity=0.85,
        tabiat_reserve_index=0.25,
        quwwat_hayawaniyyah_index=0.30,
        medication_adherence_pct=40.0,
        active_symptom_severity_delta=0.80,
    )
    report = RelapseForecasterEngine.evaluate_relapse_risk(payload)

    assert report.relapse_probability_score >= 0.70
    assert report.triage_band in ("HIGH_RELAPSE_RISK", "ACUTE_DETERIORATION_ALERT")
    assert "Tahawwul-e-Safrawi" in report.morbid_humoral_shift_risk
    assert len(report.prophylactic_interventions) >= 2
    assert report.safe_to_lock is False
    assert report.requires_clinician_review is True


def test_telemetry_metrics_and_prometheus_export():
    GLOBAL_TELEMETRY.record_request("GET", "/api/v1/patients", 200, 0.045)
    GLOBAL_TELEMETRY.record_request("POST", "/api/v1/prescriptions", 201, 0.120)
    GLOBAL_TELEMETRY.record_safety_block("SCHEDULE_E1_MUDABBAR_MANDATE")
    GLOBAL_TELEMETRY.record_predictive_alert("HIGH_RELAPSE_RISK")

    span = GLOBAL_TELEMETRY.start_span("simulate_trajectory")
    GLOBAL_TELEMETRY.finish_span(span)
    assert span.end_time is not None

    prom_text = GLOBAL_TELEMETRY.export_prometheus_metrics()
    assert "zayvora_http_requests_total" in prom_text
    assert "zayvora_safety_firewall_blocks_total" in prom_text
    assert "zayvora_predictive_alerts_total" in prom_text


def test_wearables_database_persistence():
    """Verify that WearableIngestionEngine persists samples when a database session is provided."""
    class MockDbSession:
        def __init__(self):
            self.added = []
            self.committed = False

        def add(self, obj):
            self.added.append(obj)

        def commit(self):
            self.committed = True

        def rollback(self):
            pass

    mock_db = MockDbSession()
    patient_id = "PAT-DB-WEARABLE-001"
    sample = WearableSample(
        sample_id="W-DB-01",
        patient_id=patient_id,
        timestamp_utc="2026-09-12T10:00:00Z",
        source_device="Apple Watch Ultra 2",
        hrv_rmssd_ms=52.0,
        hrv_sdnn_ms=58.0,
        resting_heart_rate_bpm=66,
        sleep_hours_total=7.8,
        deep_sleep_hours=2.1,
        rem_sleep_hours=1.9,
        spo2_average_pct=99.0,
        spo2_lowest_pct=96.0,
        respiratory_rate_bpm=14.0,
        daily_steps=9200,
        active_energy_kcal=480.0,
    )

    summary = WearableIngestionEngine.ingest_sample(sample, db=mock_db)
    assert summary.patient_id == patient_id
    assert summary.samples_count >= 1

    # Verify directly from mock database session
    assert mock_db.committed is True
    assert len(mock_db.added) == 1
    row = mock_db.added[0]
    assert row.sample_id == "W-DB-01"
    assert row.patient_id == patient_id
    assert row.source_device == "Apple Watch Ultra 2"
    assert row.hrv_rmssd_ms == 52.0
    assert row.daily_steps == 9200
