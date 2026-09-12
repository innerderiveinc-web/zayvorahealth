from app.engines.digital_twin import (
    build_digital_twin_state,
    compute_mizaj_trajectory,
    simulate_treatment_projection,
)


def test_build_digital_twin_baseline():
    twin = build_digital_twin_state(
        patient_id="patient-1",
        vital_signs={"blood_pressure_systolic": 120, "pulse_rate": 72},
        mizaj_assessment={"primary_temperament": "Damwi", "heat_cold_score": 0.5, "wet_dry_score": 0.2},
        age=32,
    )
    assert twin["patient_id"] == "patient-1"
    assert twin["safe_to_lock"] is False
    assert len(twin["organ_axis_integrity"]) == 12
    assert twin["mizaj_state"]["primary_temperament"] == "Damwi"
    assert "Mu'tadil" in twin["mizaj_state"]["clinical_status"]
    assert twin["quwa_faculties"]["tabiat_homeostatic_reserve"] > 0.8


def test_digital_twin_renal_and_pathology_deductions():
    twin = build_digital_twin_state(
        patient_id="patient-ckd",
        active_diagnoses=[{"primary_axis": "meda-amaa", "severity": "severe"}],
        lab_biomarkers={"egfr": 22.0},  # Stage 4 CKD
        age=72,
    )
    # Kulliya-Masana axis should be severely reduced due to low eGFR
    assert twin["organ_axis_integrity"]["kulliya-masana"] <= 0.30
    # Meda-Amaa should have severe deduction
    assert twin["organ_axis_integrity"]["meda-amaa"] <= 0.70
    # Tabi'iyyah should be impaired by digestive/hepatic strain
    assert twin["quwa_faculties"]["quwwat_tabi_iyyah"] < 0.90


def test_digital_twin_severe_mizaj_drift():
    twin = build_digital_twin_state(
        patient_id="patient-hot",
        mizaj_assessment={"primary_temperament": "Safrawi", "heat_cold_score": 3.5, "wet_dry_score": 2.1},
    )
    assert "Su-e-Mizaj Shadeed" in twin["mizaj_state"]["clinical_status"]
    assert twin["mizaj_state"]["drift_magnitude"] > 3.0


def test_mizaj_trajectory_healing_trend():
    history = [
        {"created_at": "2026-01-01T10:00:00", "mizaj_state": {"drift_magnitude": 3.2}},
        {"created_at": "2026-02-01T10:00:00", "mizaj_state": {"drift_magnitude": 2.1}},
        {"created_at": "2026-03-01T10:00:00", "mizaj_state": {"drift_magnitude": 1.1}},
    ]
    traj = compute_mizaj_trajectory(history)
    assert traj["trajectory_available"] is True
    assert traj["evaluations_count"] == 3
    assert "Ruju' ila al-I'tidal" in traj["clinical_trend"]
    assert traj["net_drift_delta"] < 0.0


def test_mizaj_trajectory_deteriorating_trend():
    history = [
        {"created_at": "2026-01-01T10:00:00", "mizaj_state": {"drift_magnitude": 1.0}},
        {"created_at": "2026-02-01T10:00:00", "mizaj_state": {"drift_magnitude": 2.8}},
    ]
    traj = compute_mizaj_trajectory(history)
    assert "Tafaqqum al-Marad" in traj["clinical_trend"]
    assert traj["net_drift_delta"] > 0.0


def test_treatment_trajectory_simulation():
    twin = build_digital_twin_state(
        patient_id="patient-sim",
        mizaj_assessment={"primary_temperament": "Safrawi", "heat_cold_score": 2.0, "wet_dry_score": 1.0},
    )

    sim = simulate_treatment_projection(
        digital_twin=twin,
        dominant_humor="Safra",
        treatment_modalities=["Ilaj bil-Dawa", "Ilaj bil-Tadbeer", "Ilaj bil-Ghiza"],
        weeks=8,
    )

    assert sim["is_predictive_advisory"] is True
    assert sim["safe_to_lock"] is False
    assert sim["simulation_metadata"]["dominant_humor"] == "Safra"
    assert sim["simulation_metadata"]["concoction_protocol"]["days"] == 8

    milestones = sim["projected_milestones"]
    assert len(milestones) >= 3  # Weeks 2, 4, 8
    # Mean organ integrity should monotonically improve
    scores = [m["projected_mean_organ_integrity"] for m in milestones]
    assert scores[-1] >= scores[0]
    # Week 2 (14 days) should achieve Nujz for Safra (8 days)
    assert milestones[0]["nujz_milestone_achieved"] is True
