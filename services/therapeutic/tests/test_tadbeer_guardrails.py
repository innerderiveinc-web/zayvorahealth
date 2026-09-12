from __future__ import annotations

from app.engines.tadbeer_guardrails import run_tadbeer_guardrails


def _base_patient(**overrides):
    patient = {
        "age": 35,
        "pregnancy_status": "not_applicable",
        "lactation_status": "no",
        "allergies": [],
        "current_medications": [],
        "comorbidities": [],
        "chief_complaint": "chronic neck stiffness",
    }
    patient.update(overrides)
    return patient


def test_wet_hijama_on_anticoagulants_blocked():
    """Hijama bil-Shart on warfarin must be blocked."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(current_medications=["Warfarin 5mg"]),
        plan={"name": "Hijama bil-Shart (Wet Cupping)", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("anticoagulant" in r.lower() for r in result["reasons"])


def test_wet_hijama_in_severe_anemia_blocked():
    """Wet Hijama in patient with severe anemia must be blocked."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(comorbidities=["Severe iron-deficiency anemia"]),
        plan={"name": "Wet Cupping", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("anemia" in r.lower() for r in result["reasons"])


def test_wet_hijama_in_hypotension_blocked():
    """Wet Hijama in patient with hypotension must be blocked."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(comorbidities=["Postural hypotension"]),
        plan={"name": "Hijama bil-Shart", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("hypotension" in r.lower() for r in result["reasons"])


def test_lumbosacral_hijama_in_pregnancy_blocked():
    """Hijama over lumbosacral / abdominal area in pregnancy is contraindicated."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(pregnancy_status="pregnant"),
        plan={"name": "Dry Hijama", "category": "regimen", "method": "applied to lumbosacral spine"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("pregnancy" in r.lower() for r in result["reasons"])


def test_fasd_under_age_14_blocked():
    """Fasd is contraindicated in children under 14 years old."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(age=10),
        plan={"name": "Fasd (Venesection)", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("14" in r for r in result["reasons"])


def test_fasd_over_age_60_blocked():
    """Fasd is contraindicated in elders over 60 years old."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(age=68),
        plan={"name": "Fasd", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("60" in r for r in result["reasons"])


def test_fasd_in_pregnancy_blocked():
    """Fasd is strictly contraindicated during pregnancy."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(pregnancy_status="pregnant"),
        plan={"name": "Fasd", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"


def test_hot_hammam_in_acute_fever_blocked():
    """Hot Hammam in acute febrile state is contraindicated."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(chief_complaint="High fever and chills for 2 days"),
        plan={"name": "Hot Hammam", "category": "bathing"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("fever" in r.lower() or "humma" in r.lower() for r in result["reasons"])


def test_dalak_massage_in_dvt_blocked():
    """Medical massage (Dalak) is strictly contraindicated in deep vein thrombosis."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(comorbidities=["Left leg deep vein thrombosis"]),
        plan={"name": "Dalak (Medical Massage)", "category": "massage"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("dvt" in r.lower() or "thrombosis" in r.lower() for r in result["reasons"])


def test_qai_in_severe_hypertension_blocked():
    """Therapeutic emesis (Qai) is contraindicated in hypertension."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(comorbidities=["Essential hypertension"]),
        plan={"name": "Qai", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"


def test_cauterization_kai_in_uncontrolled_diabetes_blocked():
    """Kai (cauterization) in uncontrolled diabetes is contraindicated."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(comorbidities=["Uncontrolled diabetes with peripheral neuropathy"]),
        plan={"name": "Kai (Cauterization)", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"
    assert any("diabetes" in r.lower() for r in result["reasons"])


def test_leech_therapy_in_anticoagulants_blocked():
    """Leech therapy (Zalo / Irsal-e-Alaq) on anticoagulants is contraindicated."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(current_medications=["Apixaban 5mg"]),
        plan={"name": "Zalo (Leech therapy)", "category": "regimen"},
    )
    assert result["verdict"] == "DO_NOT_RECOMMEND"


def test_safe_tadbeer_procedure_passes():
    """Safe massage in healthy adult patient passes."""
    result = run_tadbeer_guardrails(
        patient_context=_base_patient(),
        plan={"name": "Dalak-e-Layyin (Gentle relaxing massage)", "category": "massage"},
    )
    assert result["verdict"] == "SAFE_TO_CONSIDER"
    assert not any("DO_NOT_RECOMMEND" in r for r in result["reasons"])
