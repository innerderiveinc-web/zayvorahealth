from __future__ import annotations

from app.engines.safety_firewall import run_safety_firewall


def _base_patient(**overrides):
    patient = {
        "age": 35,
        "pregnancy_status": "not_applicable",
        "lactation_status": "no",
        "allergies": [],
        "current_medications": [],
        "comorbidities": [],
        "chief_complaint": "mild joint stiffness",
    }
    patient.update(overrides)
    return patient


def test_raw_suranjan_talkh_blocked_as_do_not_recommend():
    """Unpurified (Kham) Suranjan Talkh must be blocked per Schedule E(1)."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Suranjan Talkh", "is_mudabbar": False, "dose_mg": 200.0}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("SCHEDULE E(1) POISON" in r and "Mudabbar" in r for r in result["reasons"])


def test_mudabbar_suranjan_talkh_accepted_with_caution():
    """Certified Mudabbar Suranjan Talkh within statutory dose limits passes with mandatory caution."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Suranjan Talkh Mudabbar", "is_mudabbar": True, "dose_mg": 200.0}],
    )
    assert result["verdict"] == "CAUTION"
    assert any("SCHEDULE E(1) Controlled Substance" in r for r in result["reasons"])


def test_suranjan_talkh_exceeding_statutory_ceiling_blocked():
    """Mudabbar Suranjan Talkh exceeding 750mg daily ceiling must be blocked."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Suranjan Talkh Mudabbar", "is_mudabbar": True, "dose_mg": 900.0}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("SCHEDULE E(1) DOSE CEILING EXCEEDED" in r for r in result["reasons"])


def test_raw_kuchla_blocked():
    """Unpurified Kuchla (Nux Vomica) must be blocked."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Kuchla", "is_mudabbar": False, "dose_mg": 50.0}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("SCHEDULE E(1) POISON" in r for r in result["reasons"])


def test_mudabbar_kuchla_within_limit_accepted_with_caution():
    """Mudabbar Kuchla within 65mg single / 125mg daily limit passes with caution."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Kuchla Mudabbar", "is_mudabbar": True, "dose_mg": 50.0}],
    )
    assert result["verdict"] == "CAUTION"
    assert any("SCHEDULE E(1) Controlled Substance" in r for r in result["reasons"])


def test_mudabbar_kuchla_exceeding_ceiling_blocked():
    """Mudabbar Kuchla exceeding 125mg daily ceiling must be blocked."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Kuchla Mudabbar", "is_mudabbar": True, "dose_mg": 150.0}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("SCHEDULE E(1) DOSE CEILING EXCEEDED" in r for r in result["reasons"])


def test_raw_bhilawa_blocked():
    """Unpurified Bhilawa must be blocked."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[{"name": "Bhilawa", "is_mudabbar": False, "dose_mg": 100.0}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("SCHEDULE E(1) POISON" in r for r in result["reasons"])


def test_antihypertensive_plus_licorice_blocked():
    """Licorice (Asal-us-Soos) combined with antihypertensive medication is contraindicated."""
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Amlodipine 5mg"]),
        ingredients=[{"name": "Asal-us-Soos", "is_mudabbar": True}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("pseudoaldosteronism" in r.lower() or "mineralocorticoid" in r.lower() for r in result["reasons"])


def test_digoxin_plus_licorice_blocked():
    """Licorice-induced hypokalemia with Digoxin is contraindicated."""
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Digoxin 0.25mg"]),
        ingredients=[{"name": "Licorice extract"}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("arrhythmia" in r.lower() or "hypokalemia" in r.lower() for r in result["reasons"])


def test_ssri_plus_harmal_blocked():
    """Fluoxetine (SSRI) + Harmal triggers life-threatening Serotonin Syndrome block."""
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Fluoxetine 20mg"]),
        ingredients=[{"name": "Harmal (Peganum harmala)"}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("Serotonin Syndrome" in r for r in result["reasons"])


def test_lithium_plus_gokhru_blocked():
    """Lithium + Gokhru diuretic toxicity block."""
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Lithium carbonate 300mg"]),
        ingredients=[{"name": "Gokhru (Tribulus)"}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("Lithium" in r for r in result["reasons"])


def test_ciprofloxacin_plus_kushta_forces_modify():
    """Quinolone antibiotic + mineral Kushta forces chelation warning and dose separation."""
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Ciprofloxacin 500mg"]),
        ingredients=[{"name": "Kushta-e-Faulad"}],
    )
    assert result["verdict"] == "MODIFY"
    assert any("chelate" in r.lower() for r in result["reasons"])


def test_metformin_plus_karela_forces_modify():
    """Metformin + Karela forces blood-glucose monitoring and dose modification."""
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Metformin 500mg"]),
        ingredients=[{"name": "Karela juice powder"}],
    )
    assert result["verdict"] == "MODIFY"
    assert any("hypoglycemia" in r.lower() for r in result["reasons"])


def test_tazaad_e_mizaj_extreme_temperament_conflict_without_musleh():
    """Combining extreme Hot (Degree 3) and extreme Cold (Degree 3) without Musleh gives CAUTION."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[
            {"name": "Zanjabeel", "mizaj_temperament": "Safrawi", "mizaj_degree_hc": 3},
            {"name": "Kahu", "mizaj_temperament": "Saudawi", "mizaj_degree_hc": 3},
        ],
    )
    assert result["verdict"] == "CAUTION"
    assert any("Tazaad-e-Mizaj" in r for r in result["reasons"])


def test_tazaad_e_mizaj_resolved_with_musleh():
    """Adding an explicit Musleh harmonizes the temperaments, avoiding conflict."""
    result = run_safety_firewall(
        patient_context=_base_patient(),
        ingredients=[
            {"name": "Zanjabeel", "mizaj_temperament": "Safrawi", "mizaj_degree_hc": 3, "musleh": "Roghan-e-Badam"},
            {"name": "Kahu", "mizaj_temperament": "Saudawi", "mizaj_degree_hc": 3, "musleh": "Shakkar"},
        ],
    )
    assert result["verdict"] == "SAFE_TO_CONSIDER"
    assert not any("Tazaad-e-Mizaj" in r for r in result["reasons"])


def test_mizaj_contraindication_in_acute_fever():
    """Prescribing Degree 3 Hot drug during acute fever (Su-e-Mizaj Haar) without Musleh triggers MODIFY."""
    result = run_safety_firewall(
        patient_context=_base_patient(chief_complaint="High fever and burning sensation"),
        ingredients=[{"name": "Filfil Siyah", "mizaj_temperament": "Safrawi", "mizaj_degree_hc": 3}],
    )
    assert result["verdict"] == "MODIFY"
    assert any("Su-e-Mizaj Haar" in r for r in result["reasons"])
