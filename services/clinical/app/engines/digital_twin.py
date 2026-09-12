"""
ZAYVORA Clinical Digital Twin & Longitudinal Health Trajectory Engine (Phase 11).

Provides:
1. Computational Physiological State Vector across 12 Organ Axes
2. Quwa Reserve Evaluation (Tabi'iyyah, Hayawaniyyah, Nafsaniyyah, Tabi'at)
3. Longitudinal Mizaj Drift Velocity & Concoction (Nujz) Projection
4. Treatment Trajectory Simulation (2, 4, 8, 12 Weeks)
"""
from __future__ import annotations

from datetime import datetime
from typing import Any


CANONICAL_AXES = [
    "meda-amaa",
    "qalb-urooq",
    "dimagh-asab",
    "kabid-mararah",
    "kulliya-masana",
    "tanaffus",
    "mafasil",
    "jild",
    "tawallud-m",
    "tawallud-f",
    "urooq-lymph",
    "ghudad-samah",
]


def build_digital_twin_state(
    *,
    patient_id: str,
    vital_signs: dict[str, Any] | None = None,
    mizaj_assessment: dict[str, Any] | None = None,
    active_diagnoses: list[dict[str, Any]] | None = None,
    lab_biomarkers: dict[str, Any] | None = None,
    age: int | None = None,
) -> dict[str, Any]:
    """Constructs the multidimensional Clinical Digital Twin state vector."""
    vitals = vital_signs or {}
    mizaj = mizaj_assessment or {}
    diagnoses = active_diagnoses or []
    labs = lab_biomarkers or {}

    # 1. Compute Base Organ Axis Integrity (1.0 = optimal homeostasis / Sihhat)
    axis_scores: dict[str, float] = {axis: 1.0 for axis in CANONICAL_AXES}

    # Deduct based on active diagnoses mapped to axes
    for diag in diagnoses:
        axis = diag.get("primary_axis") or diag.get("organ_axis")
        severity = diag.get("severity", "moderate").lower()
        deduction = 0.35 if severity == "severe" else (0.20 if severity == "moderate" else 0.10)
        if axis in axis_scores:
            axis_scores[axis] = max(0.1, round(axis_scores[axis] - deduction, 2))

    # Biomarker adjustments
    egfr = labs.get("egfr")
    if egfr is not None:
        if egfr < 30:
            axis_scores["kulliya-masana"] = min(axis_scores["kulliya-masana"], 0.30)
        elif egfr < 60:
            axis_scores["kulliya-masana"] = min(axis_scores["kulliya-masana"], 0.60)

    systolic = vitals.get("blood_pressure_systolic")
    if systolic is not None and (systolic > 140 or systolic < 90):
        axis_scores["qalb-urooq"] = max(0.2, round(axis_scores["qalb-urooq"] - 0.20, 2))

    # 2. Evaluate Quwa (Vital Faculties)
    # Natural Faculty (Quwwat-e-Tabi'iyyah) - reflects hepatic, digestive, nutritive reserve
    tabi_iyyah = round((axis_scores["meda-amaa"] * 0.4) + (axis_scores["kabid-mararah"] * 0.6), 2)

    # Vital Faculty (Quwwat-e-Hayawaniyyah) - reflects cardio-pulmonary pulsation
    hayawaniyyah = round((axis_scores["qalb-urooq"] * 0.5) + (axis_scores["tanaffus"] * 0.5), 2)

    # Psychic Faculty (Quwwat-e-Nafsaniyyah) - reflects neural, sensorimotor, cognitive reserve
    nafsaniyyah = round((axis_scores["dimagh-asab"] * 0.7) + (axis_scores["ghudad-samah"] * 0.3), 2)

    # Tabi'at (Homeostatic Self-Healing Intelligence)
    age_factor = 1.0 if (age is None or age < 50) else (0.85 if age < 70 else 0.70)
    tabiat_score = round(((tabi_iyyah + hayawaniyyah + nafsaniyyah) / 3.0) * age_factor, 2)

    # 3. Mizaj Drift Analysis
    primary_temp = mizaj.get("primary_temperament", "Mutadil")
    hc_dev = mizaj.get("heat_cold_score", 0.0)
    wd_dev = mizaj.get("wet_dry_score", 0.0)
    magnitude = round((hc_dev**2 + wd_dev**2) ** 0.5, 2)

    if magnitude > 3.0:
        imbalance_status = "Su-e-Mizaj Shadeed (Severe Pathological Dyscrasia)"
    elif magnitude > 1.2:
        imbalance_status = "Su-e-Mizaj Khafif (Moderate Functional Imbalance)"
    else:
        imbalance_status = "Mizaj Mu'tadil (Equilibrium Maintained)"

    return {
        "patient_id": patient_id,
        "timestamp": datetime.utcnow().isoformat(),
        "mizaj_state": {
            "primary_temperament": primary_temp,
            "heat_cold_deviation": hc_dev,
            "wet_dry_deviation": wd_dev,
            "drift_magnitude": magnitude,
            "clinical_status": imbalance_status,
        },
        "organ_axis_integrity": axis_scores,
        "quwa_faculties": {
            "quwwat_tabi_iyyah": tabi_iyyah,
            "quwwat_hayawaniyyah": hayawaniyyah,
            "quwwat_nafsaniyyah": nafsaniyyah,
            "tabiat_homeostatic_reserve": tabiat_score,
        },
        "overall_vitality_index": round((tabiat_score + (sum(axis_scores.values()) / len(axis_scores))) / 2.0, 2),
        "safe_to_lock": False,
    }


def compute_mizaj_trajectory(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Computes longitudinal shift velocity and direction over sequential assessments."""
    if not history or len(history) < 2:
        return {
            "trajectory_available": False,
            "message": "At least two longitudinal assessments are required to calculate velocity.",
            "shift_velocity": 0.0,
            "trend": "Insufficient Data",
        }

    # Sort chronologically
    sorted_history = sorted(history, key=lambda x: x.get("created_at", ""))
    first = sorted_history[0]
    latest = sorted_history[-1]

    mag1 = first.get("mizaj_state", {}).get("drift_magnitude", 1.0)
    mag2 = latest.get("mizaj_state", {}).get("drift_magnitude", 1.0)
    delta_mag = round(mag2 - mag1, 2)

    if delta_mag < -0.4:
        trend = "Ruju' ila al-I'tidal (Favorable Return Towards Equilibrium)"
    elif delta_mag > 0.4:
        trend = "Tafaqqum al-Marad (Dyscrasia Deterioration / Increasing Imbalance)"
    else:
        trend = "Istiqlal (Stable Humoral Plate)"

    return {
        "trajectory_available": True,
        "baseline_magnitude": mag1,
        "latest_magnitude": mag2,
        "net_drift_delta": delta_mag,
        "clinical_trend": trend,
        "evaluations_count": len(sorted_history),
    }


def simulate_treatment_projection(
    *,
    digital_twin: dict[str, Any],
    dominant_humor: str = "Dam",
    treatment_modalities: list[str] | None = None,
    weeks: int = 4,
) -> dict[str, Any]:
    """Simulates physiological response, Nujz (concoction) schedule,
    and axis recovery trajectory over a multi-week projection horizon.
    """
    modalities = treatment_modalities or ["Ilaj bil-Dawa", "Ilaj bil-Ghiza"]
    quwa = digital_twin.get("quwa_faculties", {})
    tabiat = quwa.get("tabiat_homeostatic_reserve", 0.70)
    base_axes = dict(digital_twin.get("organ_axis_integrity", {}))

    # Classical Nujz duration estimates by humor
    nujz_schedules = {
        "Dam": {"days": 4, "phase": "Rapid Concoction (Sanguine plethora easily liquefied)"},
        "Safra": {"days": 8, "phase": "Moderate Concoction (Biliary heat requires cooling demulcents)"},
        "Balgham": {"days": 18, "phase": "Prolonged Concoction (Viscous cold humor requires sustained Nujz electuaries)"},
        "Sauda": {"days": 35, "phase": "Resistant Concoction (Melancholic combustion requires deep moistening & Istifragh)"},
    }
    concoction_info = nujz_schedules.get(dominant_humor, nujz_schedules["Dam"])

    # Multi-horizon projection milestones
    projections = []
    current_axes = dict(base_axes)

    # Multi-modality synergy factor
    synergy_multiplier = 1.0 + (0.15 if "Ilaj bil-Tadbeer" in modalities else 0.0) + (0.10 if "Ilaj bil-Ghiza" in modalities else 0.0)
    weekly_recovery_rate = round(0.04 * tabiat * synergy_multiplier, 3)

    for w in [2, 4, 8, 12]:
        if w > weeks:
            break
        for ax in current_axes:
            current_axes[ax] = min(1.0, round(current_axes[ax] + (weekly_recovery_rate * (w / 2)), 2))

        avg_integrity = round(sum(current_axes.values()) / len(current_axes), 2)
        nujz_complete = (w * 7) >= concoction_info["days"]

        projections.append({
            "week": w,
            "projected_mean_organ_integrity": avg_integrity,
            "nujz_milestone_achieved": nujz_complete,
            "phase_description": "Post-Concoction Restoration / Tahfeez" if nujz_complete else f"Active Concoction Phase ({concoction_info['days']} days required)",
        })

    return {
        "simulation_metadata": {
            "dominant_humor": dominant_humor,
            "concoction_protocol": concoction_info,
            "active_modalities": modalities,
            "horizon_weeks": weeks,
            "homeostatic_synergy_rate": weekly_recovery_rate,
        },
        "projected_milestones": projections,
        "is_predictive_advisory": True,
        "safe_to_lock": False,
        "regulatory_notice": "Predictive Digital Twin output is strictly advisory simulation for clinical scenario modeling. Physician verification required.",
    }
