"""
Classical 10 Ajnas-e-Ashara Algorithmic Mizaj Assessment Engine.
Sources: Al-Qanoon fit-Tibb (Avicenna), Kitab al-Kulliyat (Averroes), Kamil-us-Sana'ah.

Evaluates the 10 physiological and morphological determinants of temperament:
1. Malmas (Tactile / Skin Texture & Temperature)
2. Lahm wa Shahm (Musculature & Adipose Ratio)
3. Ash'ar (Hair Attributes)
4. Laun (Complexion)
5. Hay'at-ul-A'za (Skeletal & Thoracic Morphology)
6. Kayfiyyat-ul-Infial (Emotional Reactivity & Psychic State)
7. Naum wa Yaqzah (Sleep & Vigilance Architecture)
8. Harkat wa Sukoon (Motor Velocity & Agility)
9. Fuzalaat (Excretory Products: Sweat, Urine, Stool)
10. Af'al-ul-A'za (Digestion, Appetite & Pulse / Nabz)
"""
from __future__ import annotations

from typing import Any, TypedDict


class AjnasInput(TypedDict, total=False):
    malmas: str  # "hot_moist" | "hot_dry" | "cold_moist" | "cold_dry"
    lahm_shahm: str  # "muscular_moderate" | "lean_sinewy" | "heavy_adipose" | "emaciated_bony"
    ashar: str  # "thick_dark" | "rapid_thin" | "slow_light" | "dry_curly"
    laun: str  # "ruddy_red" | "yellowish_sallow" | "chalky_pale" | "dark_leaden"
    hayat_aza: str  # "broad_strong" | "narrow_sinewy" | "broad_padded" | "narrow_sunken"
    kayfiyyat_infial: str  # "cheerful_courageous" | "quick_irritable" | "calm_sluggish" | "anxious_brooding"
    naum_yaqzah: str  # "moderate_sound" | "short_fitful" | "excessive_deep" | "insomnia_fragmented"
    harkat_sukoon: str  # "robust_active" | "brisk_restless" | "slow_lethargic" | "hesitant_variable"
    fuzalaat: str  # "copious_normal" | "pungent_dark" | "cold_pale" | "scanty_dry"
    afal_aza: str  # "strong_full" | "ravenous_quick" | "sluggish_slow" | "variable_hard"


AJNAS_MAP = {
    "malmas": {
        "hot_moist": "Damwi",
        "hot_dry": "Safrawi",
        "cold_moist": "Balghami",
        "cold_dry": "Saudawi",
    },
    "lahm_shahm": {
        "muscular_moderate": "Damwi",
        "lean_sinewy": "Safrawi",
        "heavy_adipose": "Balghami",
        "emaciated_bony": "Saudawi",
    },
    "ashar": {
        "thick_dark": "Damwi",
        "rapid_thin": "Safrawi",
        "slow_light": "Balghami",
        "dry_curly": "Saudawi",
    },
    "laun": {
        "ruddy_red": "Damwi",
        "yellowish_sallow": "Safrawi",
        "chalky_pale": "Balghami",
        "dark_leaden": "Saudawi",
    },
    "hayat_aza": {
        "broad_strong": "Damwi",
        "narrow_sinewy": "Safrawi",
        "broad_padded": "Balghami",
        "narrow_sunken": "Saudawi",
    },
    "kayfiyyat_infial": {
        "cheerful_courageous": "Damwi",
        "quick_irritable": "Safrawi",
        "calm_sluggish": "Balghami",
        "anxious_brooding": "Saudawi",
    },
    "naum_yaqzah": {
        "moderate_sound": "Damwi",
        "short_fitful": "Safrawi",
        "excessive_deep": "Balghami",
        "insomnia_fragmented": "Saudawi",
    },
    "harkat_sukoon": {
        "robust_active": "Damwi",
        "brisk_restless": "Safrawi",
        "slow_lethargic": "Balghami",
        "hesitant_variable": "Saudawi",
    },
    "fuzalaat": {
        "copious_normal": "Damwi",
        "pungent_dark": "Safrawi",
        "cold_pale": "Balghami",
        "scanty_dry": "Saudawi",
    },
    "afal_aza": {
        "strong_full": "Damwi",
        "ravenous_quick": "Safrawi",
        "sluggish_slow": "Balghami",
        "variable_hard": "Saudawi",
    },
}


def calculate_mizaj_assessment(answers: dict[str, str]) -> dict[str, Any]:
    """Computes quantitative Mizaj breakdown and dyscrasia classification."""
    scores = {"Damwi": 0, "Safrawi": 0, "Balghami": 0, "Saudawi": 0}
    answered_count = 0

    for ajnas_key, mapping in AJNAS_MAP.items():
        val = answers.get(ajnas_key)
        if val and val in mapping:
            humor = mapping[val]
            scores[humor] += 1
            answered_count += 1

    if answered_count == 0:
        return {
            "primary_temperament": "Motadil",
            "secondary_temperament": "Motadil",
            "distribution_percentages": {"Damwi": 25.0, "Safrawi": 25.0, "Balghami": 25.0, "Saudawi": 25.0},
            "su_e_mizaj": "None (Motadil / Equable)",
            "dyscrasia_degree": 0,
            "raw_scores": scores,
            "answered_count": 0,
        }

    # Percentages
    percentages = {
        humor: round((count / answered_count) * 100, 1)
        for humor, count in scores.items()
    }

    # Sort descending
    sorted_humors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_humors[0][0]
    secondary = sorted_humors[1][0]

    # Evaluate Su-e-Mizaj (Dyscrasia)
    highest_score = sorted_humors[0][1]
    pct = percentages[primary]

    dyscrasia_degree = 0
    su_e_mizaj = "None (Motadil / Balanced)"

    if pct >= 65.0:
        dyscrasia_degree = 3
    elif pct >= 45.0:
        dyscrasia_degree = 2
    elif pct >= 35.0:
        dyscrasia_degree = 1

    if dyscrasia_degree > 0:
        mizaj_qualities = {
            "Damwi": "Har Ratab (Hot & Moist)",
            "Safrawi": "Har Yabis (Hot & Dry)",
            "Balghami": "Barid Ratab (Cold & Moist)",
            "Saudawi": "Barid Yabis (Cold & Dry)",
        }
        su_e_mizaj = f"Su-e-Mizaj {primary} ({mizaj_qualities.get(primary, '')}) — Degree {dyscrasia_degree}"

    return {
        "primary_temperament": primary,
        "secondary_temperament": secondary,
        "distribution_percentages": percentages,
        "su_e_mizaj": su_e_mizaj,
        "dyscrasia_degree": dyscrasia_degree,
        "raw_scores": scores,
        "answered_count": answered_count,
    }
