from __future__ import annotations

from app.engines.nuskha_compiler import (
    calculate_adjusted_dose,
    compile_nuskha,
    substitute_badal_with_posology,
)


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


def test_juz_e_azam_assigned_to_primary_axis():
    """Suranjan Talkh targeting Mafasil organ-axis should be assigned Juz-e-Azam."""
    result = compile_nuskha(
        target_organ_axes=["mafasil"],
        therapeutic_objective="Relieve gouty arthralgia",
        ingredients=[
            {"name": "Suranjan Talkh Mudabbar", "is_mudabbar": True, "dose_mg": 250.0},
            {"name": "Zanjabeel", "dose_mg": 500.0},
        ],
        patient_context=_base_patient(),
    )
    assert result["juz_e_azam"] == "Suranjan Talkh Mudabbar"
    ing0 = result["compiled_ingredients"][0]
    assert ing0["classical_role"] == "juz_e_azam"
    assert ing0["target_axis_alignment"] == "mafasil"


def test_missing_musleh_detected():
    """Prescribing Suranjan Talkh without Roghan-e-Badam or Kateera triggers missing Musleh alert."""
    result = compile_nuskha(
        target_organ_axes=["mafasil"],
        therapeutic_objective="Treat joint pain",
        ingredients=[{"name": "Suranjan Talkh Mudabbar", "is_mudabbar": True, "dose_mg": 250.0}],
        patient_context=_base_patient(),
    )
    assert not result["is_formulation_balanced"]
    assert len(result["missing_musleh_alerts"]) >= 1
    assert any("Roghan-e-Badam" in a for a in result["missing_musleh_alerts"])


def test_formulation_balanced_when_musleh_included():
    """Providing explicit Musleh balances the formulation."""
    result = compile_nuskha(
        target_organ_axes=["mafasil"],
        therapeutic_objective="Treat joint pain with corrective",
        ingredients=[
            {
                "name": "Suranjan Talkh Mudabbar",
                "is_mudabbar": True,
                "musleh": "Roghan-e-Badam (Almond oil)",
                "dose_mg": 250.0,
            }
        ],
        patient_context=_base_patient(),
    )
    assert result["is_formulation_balanced"]
    assert len(result["missing_musleh_alerts"]) == 0


def test_badal_substitute_suggested():
    """Compiler provides authenticated Badal substitutes for formulated botanicals."""
    result = compile_nuskha(
        target_organ_axes=["dimagh-aasab"],
        therapeutic_objective="Nervine strengthener",
        ingredients=[{"name": "Kuchla Mudabbar", "is_mudabbar": True, "dose_mg": 50.0}],
        patient_context=_base_patient(),
    )
    assert len(result["substitute_suggestions"]) >= 1
    sug = result["substitute_suggestions"][0]
    assert "Jadwar" in sug["classical_badal"] or "Asgandh" in sug["classical_badal"]


def test_pediatric_dose_adjustment_youngs_rule():
    """6-year-old child receives reduced dosage according to pediatric posology."""
    posology = calculate_adjusted_dose(600.0, _base_patient(age=6))
    # 6 / (6 + 12) = 1/3 -> 600 * 0.333 = ~200.0 mg
    assert posology["calculated_mg"] < 300.0
    assert any("Pediatric" in r for r in posology["adjustment_reasons"])


def test_geriatric_dose_attenuation():
    """78-year-old patient receives geriatric attenuation (55% of adult standard)."""
    posology = calculate_adjusted_dose(1000.0, _base_patient(age=78))
    assert posology["calculated_mg"] == 550.0
    assert any("Geriatric" in r for r in posology["adjustment_reasons"])


def test_renal_clearance_dose_attenuation():
    """Patient with chronic kidney disease receives 50% clearance reduction."""
    posology = calculate_adjusted_dose(1000.0, _base_patient(comorbidities=["Chronic kidney disease"]))
    assert posology["calculated_mg"] == 500.0
    assert any("Renal" in r for r in posology["adjustment_reasons"])


def test_substitute_badal_with_posology_potency_ratio():
    """Verify Suranjan Talkh -> Suranjan Shireen applies 2.0x potency multiplier."""
    res = substitute_badal_with_posology(
        original_ingredient_name="Suranjan Talkh Mudabbar",
        original_dose_mg=250.0,
        badal_name="Suranjan Shireen",
        patient_context=_base_patient(),
    )
    assert res["potency_ratio"] == 2.0
    assert res["calculated_badal_dose_mg"] == 500.0
    assert "Potency conversion factor of 2.0x" in res["classical_rationale"]

    # Turbud Safed is stronger purgative than Sana Makki, so ratio is 0.5x
    res2 = substitute_badal_with_posology(
        original_ingredient_name="Sana Makki",
        original_dose_mg=1000.0,
        badal_name="Turbud Safed",
        patient_context=_base_patient(),
    )
    assert res2["potency_ratio"] == 0.5
    assert res2["calculated_badal_dose_mg"] == 500.0


def test_compile_nuskha_includes_badal_potency_ratio():
    """Verify compile_nuskha generates substitute suggestions with potency ratios."""
    result = compile_nuskha(
        target_organ_axes=["mafasil"],
        therapeutic_objective="Gout relief",
        ingredients=[{"name": "Suranjan Talkh Mudabbar", "is_mudabbar": True, "dose_mg": 200.0}],
        patient_context=_base_patient(),
    )
    assert len(result["substitute_suggestions"]) >= 1
    sug = result["substitute_suggestions"][0]
    assert "potency_ratio" in sug
    assert "potency_adjusted_dose_mg" in sug
    assert sug["potency_ratio"] == 2.0
    assert sug["potency_adjusted_dose_mg"] == 400.0
