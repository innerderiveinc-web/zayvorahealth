"""
Unit tests for 10-Ajnas Mizaj Assessment and Differential Diagnosis Intelligence (Phase 6).
"""
from __future__ import annotations

from app.engines.differential_engine import match_differential_considerations
from app.engines.mizaj_assessor import calculate_mizaj_assessment


def test_mizaj_assessment_10_ajnas_safrawi_dyscrasia():
    # Patient with marked Safrawi (Choleric / Hot & Dry) attributes
    answers = {
        "malmas": "hot_dry",
        "lahm_shahm": "lean_sinewy",
        "ashar": "rapid_thin",
        "laun": "yellowish_sallow",
        "hayat_aza": "narrow_sinewy",
        "kayfiyyat_infial": "quick_irritable",
        "naum_yaqzah": "short_fitful",
        "harkat_sukoon": "brisk_restless",
        "fuzalaat": "pungent_dark",
        "afal_aza": "ravenous_quick",
    }
    result = calculate_mizaj_assessment(answers)
    assert result["primary_temperament"] == "Safrawi"
    assert result["answered_count"] == 10
    assert result["distribution_percentages"]["Safrawi"] == 100.0
    assert result["dyscrasia_degree"] == 3
    assert "Har Yabis" in result["su_e_mizaj"]


def test_mizaj_assessment_mixed_constitution():
    # Mixed Damwi (Sanguine) with secondary Safrawi
    answers = {
        "malmas": "hot_moist",           # Damwi
        "lahm_shahm": "muscular_moderate",# Damwi
        "ashar": "thick_dark",           # Damwi
        "laun": "ruddy_red",             # Damwi
        "hayat_aza": "broad_strong",     # Damwi
        "kayfiyyat_infial": "quick_irritable", # Safrawi
        "naum_yaqzah": "short_fitful",         # Safrawi
        "harkat_sukoon": "robust_active",      # Damwi
        "fuzalaat": "copious_normal",          # Damwi
        "afal_aza": "strong_full",             # Damwi
    }
    result = calculate_mizaj_assessment(answers)
    assert result["primary_temperament"] == "Damwi"
    assert result["secondary_temperament"] == "Safrawi"
    assert result["distribution_percentages"]["Damwi"] == 80.0
    assert result["distribution_percentages"]["Safrawi"] == 20.0
    assert result["dyscrasia_degree"] == 3


def test_mizaj_assessment_empty_fallback():
    result = calculate_mizaj_assessment({})
    assert result["primary_temperament"] == "Motadil"
    assert result["dyscrasia_degree"] == 0
    assert result["answered_count"] == 0


def test_differential_considerations_gout():
    matches = match_differential_considerations(
        chief_complaint="intense acute pain and swelling in big toe, suspected uric acid flare",
        organ_axis="mafasil",
    )
    assert len(matches) >= 1
    top = matches[0]
    assert "Niqris" in top["unani_disease"]
    assert top["icd11_code"] == "FA25"
    assert top["organ_axis"] == "mafasil"
    assert any("septic arthritis" in rf.lower() for rf in top["red_flags"])


def test_differential_considerations_stroke_red_flags():
    matches = match_differential_considerations(
        chief_complaint="acute facial palsy and unilateral limb weakness",
        organ_axis="dimagh-aasab",
    )
    assert len(matches) >= 1
    top = matches[0]
    assert "Falij" in top["unani_disease"] or "Laqwa" in top["unani_disease"]
    assert top["icd11_code"] == "8B20"
    assert any("4.5 hours" in rf for rf in top["red_flags"])


def test_differential_considerations_dyspepsia():
    matches = match_differential_considerations(
        chief_complaint="chronic dyspepsia, post-prandial bloating and gas",
        organ_axis="meda-amaa",
    )
    assert len(matches) >= 1
    top = matches[0]
    assert "Su-e-Hazm" in top["unani_disease"]
    assert top["icd11_code"] == "MD90"
    assert any("melena" in rf.lower() or "dysphagia" in rf.lower() for rf in top["red_flags"])
