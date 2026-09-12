from app.engines.safety_firewall import run_safety_firewall


def _base_patient(**overrides):
    patient = {
        "age": 35,
        "pregnancy_status": "not_applicable",
        "lactation_status": "no",
        "allergies": [],
        "current_medications": [],
        "comorbidities": [],
        "chief_complaint": "mild fatigue",
    }
    patient.update(overrides)
    return patient


def test_no_concerns_gives_safe_to_consider():
    result = run_safety_firewall(patient_context=_base_patient(), ingredients=[{"name": "Sonf"}])
    assert result["verdict"] == "SAFE_TO_CONSIDER"


def test_red_flag_complaint_forces_refer():
    result = run_safety_firewall(
        patient_context=_base_patient(chief_complaint="severe chest pain since this morning"),
        ingredients=[{"name": "Sonf"}],
    )
    assert result["verdict"] == "REFER"
    assert any("chest pain" in r.lower() for r in result["reasons"])


def test_pregnancy_forces_do_not_recommend():
    result = run_safety_firewall(patient_context=_base_patient(pregnancy_status="pregnant"), ingredients=[{"name": "Sonf"}])
    assert result["verdict"] == "DO_NOT_RECOMMEND"


def test_allergy_conflict_forces_do_not_recommend():
    result = run_safety_firewall(
        patient_context=_base_patient(allergies=["garlic"]),
        ingredients=[{"name": "Garlic extract"}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("allerg" in r.lower() for r in result["reasons"])


def test_no_allergy_conflict_when_ingredient_unrelated():
    result = run_safety_firewall(
        patient_context=_base_patient(allergies=["penicillin"]),
        ingredients=[{"name": "Sonf"}],
    )
    assert result["verdict"] == "SAFE_TO_CONSIDER"


def test_warfarin_plus_garlic_forces_modify():
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Warfarin 5mg"]),
        ingredients=[{"name": "Garlic extract"}],
    )
    assert result["verdict"] == "MODIFY"


def test_warfarin_alone_gives_caution_not_modify():
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Warfarin 5mg"]),
        ingredients=[{"name": "Sonf"}],
    )
    assert result["verdict"] == "CAUTION"


def test_immunosuppressant_forces_do_not_recommend():
    result = run_safety_firewall(
        patient_context=_base_patient(current_medications=["Tacrolimus (immunosuppressant)"]),
        ingredients=[{"name": "Ashwagandha"}],
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"


def test_pediatric_patient_gives_caution():
    result = run_safety_firewall(patient_context=_base_patient(age=8), ingredients=[{"name": "Sonf"}])
    assert result["verdict"] == "CAUTION"


def test_elderly_patient_gives_caution():
    result = run_safety_firewall(patient_context=_base_patient(age=75), ingredients=[{"name": "Sonf"}])
    assert result["verdict"] == "CAUTION"


def test_renal_comorbidity_gives_caution():
    result = run_safety_firewall(patient_context=_base_patient(comorbidities=["Chronic kidney disease"]), ingredients=[{"name": "Sonf"}])
    assert result["verdict"] == "CAUTION"


def test_multiple_severe_issues_escalate_to_highest_verdict():
    result = run_safety_firewall(
        patient_context=_base_patient(pregnancy_status="pregnant", chief_complaint="severe chest pain"),
        ingredients=[{"name": "Sonf"}],
    )
    assert result["verdict"] == "REFER"  # REFER outranks DO_NOT_RECOMMEND


def test_result_always_has_required_fields():
    result = run_safety_firewall(patient_context=_base_patient(), ingredients=[{"name": "Sonf"}])
    assert set(result.keys()) == {"verdict", "reasons", "requiresPractitionerSignoff"}
    assert result["requiresPractitionerSignoff"] is True
    assert len(result["reasons"]) >= 1  # always explains itself, even when safe
