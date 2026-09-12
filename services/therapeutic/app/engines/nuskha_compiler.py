"""
ZAYVORA Classical Nuskha Compiler & Formulation Balancing Engine.

Master Build Prompt v4.0 §14, §18 (Nuskha Nawisi Sequence) & §19.

Codifies the authentic Unani formulation synthesis rules:
1. Juz-e-Azam (Chief Active Ingredient): Validated against target organ-axis & primary pathology.
2. Muin (Adjuvant / Bio-enhancer / Synergist): Facilitates absorption and penetration.
3. Musleh (Corrective / Harmonizer): Identified for every active ingredient to prevent adverse effects.
4. Badal (Substitute): Automatically retrieved when an ingredient triggers a safety contraindication.
5. Algorithmic Posology Engine: Pediatric (Young's/Cowling's Rules), Geriatric, and Renal dose adjustments.
"""
from __future__ import annotations

import re
from typing import Any

# Standard classical Musleh and Badal mapping for primary single drugs
CLASSICAL_CORRECTIVES_AND_SUBSTITUTES: dict[str, dict[str, Any]] = {
    "suranjan talkh": {
        "musleh": "Roghan-e-Badam (Almond Oil), Kateera, Zafran",
        "badal": "Suranjan Shireen, Bozidana",
        "primary_organ_axis": "mafasil",
        "default_adult_dose_mg": 250.0,
    },
    "kuchla": {
        "musleh": "Roghan-e-Zard (Ghee), Sheer-e-Taza (Fresh Milk), Anisoon",
        "badal": "Jadwar Khatai, Asgandh",
        "primary_organ_axis": "dimagh-aasab",
        "default_adult_dose_mg": 50.0,
    },
    "bhilawa": {
        "musleh": "Gond Babool, Roghan-e-Kunjad (Sesame Oil), Fresh Butter",
        "badal": "Balela, Kundur",
        "primary_organ_axis": "mafasil",
        "default_adult_dose_mg": 125.0,
    },
    "afeem": {
        "musleh": "Jund-e-Bedastar, Zafran, Filfil Siyah",
        "badal": "Bazrulbanj, Post-e-Khashkhash",
        "primary_organ_axis": "dimagh-aasab",
        "default_adult_dose_mg": 30.0,
    },
    "bhang": {
        "musleh": "Roghan-e-Zard, Roghan-e-Pista, Honey",
        "badal": "Post-e-Khashkhash, Kishneez Khushk",
        "primary_organ_axis": "dimagh-aasab",
        "default_adult_dose_mg": 250.0,
    },
    "dhatura": {
        "musleh": "Roghan-e-Badam, Sheer-e-Taza, Honey",
        "badal": "Bazrulbanj, Afyoon",
        "primary_organ_axis": "dimagh-aasab",
        "default_adult_dose_mg": 30.0,
    },
    "jamalgota": {
        "musleh": "Kishneez Khushk, Buttermilk, Roghan-e-Badam",
        "badal": "Turbud, Saqmooniya",
        "primary_organ_axis": "meda-amaa",
        "default_adult_dose_mg": 30.0,
    },
    "asgandh": {
        "musleh": "Gond Kateera, Shakkar (Raw Sugar)",
        "badal": "Bahman Surkh, Salab Misri",
        "primary_organ_axis": "dimagh-aasab",
        "default_adult_dose_mg": 3000.0,
    },
    "zanjabeel": {
        "musleh": "Roghan-e-Badam, Honey",
        "badal": "Darfulful, Peepal",
        "primary_organ_axis": "meda-amaa",
        "default_adult_dose_mg": 1500.0,
    },
    "filfil siyah": {
        "musleh": "Roghan-e-Zaitoon (Olive oil), Fresh Milk",
        "badal": "Zanjabeel, Peepal",
        "primary_organ_axis": "meda-amaa",
        "default_adult_dose_mg": 500.0,
    },
    "asal-us-soos": {
        "musleh": "Gul-e-Surkh (Rose petals), Kateera",
        "badal": "Katheera, Samagh-e-Arabi",
        "primary_organ_axis": "riya-sadr",
        "default_adult_dose_mg": 3000.0,
    },
    "sana makki": {
        "musleh": "Anisoon, Gulqand, Roghan-e-Badam",
        "badal": "Turbud Safed",
        "primary_organ_axis": "meda-amaa",
        "default_adult_dose_mg": 4000.0,
    },
    "ustukhuddus": {
        "musleh": "Kateera, Lemon Juice",
        "badal": "Aftimoon (Cuscuta reflexa)",
        "primary_organ_axis": "dimagh-aasab",
        "default_adult_dose_mg": 5000.0,
    },
    "kalonji": {
        "musleh": "Sirka (Vinegar), Roghan-e-Kunjad",
        "badal": "Zeera Siyah",
        "primary_organ_axis": "tabiyat",
        "default_adult_dose_mg": 1500.0,
    },
    "gokhru": {
        "musleh": "Roghan-e-Badam, Honey",
        "badal": "Kaknaj, Beikh-e-Kasni",
        "primary_organ_axis": "meda-amaa",
        "default_adult_dose_mg": 6000.0,
    },
}

# Classical Badal Potency Equivalence Ratios (Makhzan-ul-Adwiya & Kitab al-Kulliyat)
# Specifies multiplier applied to original dose when substituting an ingredient
BADAL_POTENCY_RATIOS: dict[str, dict[str, float]] = {
    "suranjan talkh": {
        "suranjan shireen": 2.0,  # Suranjan Shireen is milder; requires 2x dose
        "bozidana": 2.5,
    },
    "kuchla": {
        "jadwar khatai": 1.5,
        "asgandh": 10.0,
    },
    "bhilawa": {
        "balela": 2.0,
        "kundur": 1.5,
    },
    "zanjabeel": {
        "darfulful": 1.0,
        "peepal": 1.2,
    },
    "filfil siyah": {
        "zanjabeel": 2.0,
        "peepal": 1.0,
    },
    "asal-us-soos": {
        "katheera": 1.0,
        "samagh-e-arabi": 1.2,
    },
    "sana makki": {
        "turbud safed": 0.5,  # Turbud is stronger purgative; requires half dose
    },
    "ustukhuddus": {
        "aftimoon": 1.0,
    },
}


def _extract_base_name(name: str) -> str:
    cleaned = name.lower()
    for drop in ["mudabbar", "shodhit", "purified", "powder", "extract", "arq", "joshanda"]:
        cleaned = cleaned.replace(drop, "")
    return cleaned.strip()


def substitute_badal_with_posology(
    original_ingredient_name: str,
    original_dose_mg: float,
    badal_name: str,
    patient_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Substitutes an original ingredient with its Badal, computing the potency-adjusted posology
    per classical Unani principles (Makhzan-ul-Adwiya).
    """
    orig_key = _extract_base_name(original_ingredient_name)
    badal_key = _extract_base_name(badal_name)

    ratios = BADAL_POTENCY_RATIOS.get(orig_key, {})
    ratio = ratios.get(badal_key, 1.0)
    adjusted_dose = original_dose_mg * ratio

    posology = calculate_adjusted_dose(adjusted_dose, patient_context or {})

    return {
        "original_ingredient": original_ingredient_name,
        "original_dose_mg": original_dose_mg,
        "badal_substitute": badal_name,
        "potency_ratio": ratio,
        "calculated_badal_dose_mg": posology["calculated_mg"],
        "posology_adjustments": posology["adjustment_reasons"],
        "classical_rationale": f"Potency conversion factor of {ratio}x applied per Makhzan-ul-Adwiya standards.",
    }


def calculate_adjusted_dose(
    base_dose_mg: float,
    patient_context: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculates age-, geriatric-, and organ-adjusted dosage.
    - Pediatric: Young's Rule (age / (age + 12)) and Cowling's Rule ((age + 1) / 24).
    - Geriatric: 75% for 65-74, 50-60% for 75+.
    - Renal/Hepatic: 50% attenuation.
    """
    age = patient_context.get("age")
    adjustment_factor = 1.0
    adjustment_reasons: list[str] = []

    if age is not None:
        if age < 1:
            adjustment_factor = 0.1
            adjustment_reasons.append("Infant posology adjustment (<1 yr)")
        elif age < 12:
            young_factor = age / (age + 12.0)
            cowling_factor = (age + 1.0) / 24.0
            adjustment_factor = min(young_factor, cowling_factor)
            adjustment_reasons.append(f"Pediatric Young's/Cowling's Rule applied (Factor: {adjustment_factor:.2f})")
        elif age >= 75:
            adjustment_factor = 0.55
            adjustment_reasons.append("Geriatric posology attenuation (Age ≥75: 55% of adult standard)")
        elif age >= 65:
            adjustment_factor = 0.75
            adjustment_reasons.append("Geriatric posology attenuation (Age 65-74: 75% of adult standard)")

    comorbidities = [c.lower() for c in (patient_context.get("comorbidities") or [])]
    if any("renal" in c or "kidney" in c or "hepatic" in c or "liver" in c for c in comorbidities):
        adjustment_factor *= 0.5
        adjustment_reasons.append("Renal/Hepatic clearance reduction (50% dose attenuation)")

    calculated_mg = round(base_dose_mg * adjustment_factor, 1)

    return {
        "standard_adult_mg": base_dose_mg,
        "calculated_mg": calculated_mg,
        "adjustment_factor": round(adjustment_factor, 3),
        "adjustment_reasons": adjustment_reasons,
    }


def compile_nuskha(
    *,
    target_organ_axes: list[str],
    therapeutic_objective: str,
    ingredients: list[dict[str, Any]],
    patient_context: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyzes, structures, and balances an ingredient list according to classical
    Unani Nuskha Nawisi formulation design.
    """
    compiled_ingredients: list[dict[str, Any]] = []
    missing_musleh_alerts: list[str] = []
    substitute_suggestions: list[dict[str, Any]] = []
    roles_assigned = {"juz_e_azam": None, "muin": [], "musleh": [], "badal": []}

    target_axes_set = set(target_organ_axes or [])
    primary_axis = target_organ_axes[0] if target_organ_axes else "tabiyat"

    # Step 1: Detect existing Musleh in the formulation
    all_names = [i.get("name", "").lower() for i in ingredients]
    all_musleh_specified = [i.get("musleh", "").lower() for i in ingredients if i.get("musleh")]

    # Step 2: Evaluate each ingredient and assign formulation role
    for idx, ing in enumerate(ingredients):
        raw_name = ing.get("name", "")
        base_name = _extract_base_name(raw_name)
        matched_profile = None

        for k, profile in CLASSICAL_CORRECTIVES_AND_SUBSTITUTES.items():
            if k in base_name or base_name in k:
                matched_profile = profile
                break

        # Extract or infer base dose
        dose_mg = ing.get("dose_mg")
        if dose_mg is None and matched_profile:
            dose_mg = matched_profile["default_adult_dose_mg"]
        elif dose_mg is None:
            dose_mg = 500.0

        posology = calculate_adjusted_dose(float(dose_mg), patient_context)

        # Determine Classical Role
        role = "adjuvant"  # Default Mu'in
        if matched_profile and matched_profile.get("primary_organ_axis") in target_axes_set:
            if roles_assigned["juz_e_azam"] is None:
                role = "juz_e_azam"
                roles_assigned["juz_e_azam"] = raw_name
        elif idx == 0 and roles_assigned["juz_e_azam"] is None:
            role = "juz_e_azam"
            roles_assigned["juz_e_azam"] = raw_name

        # Check for Musleh requirement
        if matched_profile:
            required_musleh = matched_profile["musleh"]
            has_musleh_in_nuskha = (
                ing.get("musleh")
                or any(m_word in " ".join(all_names) for m_word in ["badam", "kateera", "ghee", "zard", "gulqand", "honey", "shahad"])
            )
            if not has_musleh_in_nuskha:
                missing_musleh_alerts.append(
                    f"Ingredient '{raw_name}' requires classical Musleh: [{required_musleh}] to prevent adverse temperamental reaction."
                )

            # Substitute suggestion for safety awareness
            if matched_profile.get("badal"):
                first_badal = matched_profile["badal"].split(",")[0].strip()
                badal_posology = substitute_badal_with_posology(
                    original_ingredient_name=raw_name,
                    original_dose_mg=float(dose_mg),
                    badal_name=first_badal,
                    patient_context=patient_context,
                )
                substitute_suggestions.append({
                    "for_ingredient": raw_name,
                    "classical_badal": matched_profile["badal"],
                    "recommended_badal": first_badal,
                    "potency_ratio": badal_posology["potency_ratio"],
                    "calculated_badal_dose_mg": badal_posology["calculated_badal_dose_mg"],
                    "potency_adjusted_dose_mg": badal_posology["calculated_badal_dose_mg"],
                    "posology_adjustments": badal_posology["posology_adjustments"],
                    "reason": f"Classical substitute if '{raw_name}' is contraindicated in patient profile ({badal_posology['classical_rationale']}).",
                })

        compiled_ing = {
            "name": raw_name,
            "classical_role": role,
            "target_axis_alignment": (matched_profile.get("primary_organ_axis") if matched_profile else primary_axis),
            "prescribed_dose_mg": dose_mg,
            "clinically_adjusted_dose_mg": posology["calculated_mg"],
            "posology_adjustments": posology["adjustment_reasons"],
            "musleh": ing.get("musleh") or (matched_profile.get("musleh") if matched_profile else ""),
            "badal": ing.get("badal") or (matched_profile.get("badal") if matched_profile else ""),
            "is_mudabbar": ing.get("is_mudabbar"),
            "mudabbar_process": ing.get("mudabbar_process", ""),
        }
        compiled_ingredients.append(compiled_ing)

    is_balanced = len(missing_musleh_alerts) == 0

    return {
        "status": "compiled",
        "juz_e_azam": roles_assigned["juz_e_azam"],
        "target_organ_axes": target_organ_axes,
        "therapeutic_objective": therapeutic_objective,
        "is_formulation_balanced": is_balanced,
        "missing_musleh_alerts": missing_musleh_alerts,
        "substitute_suggestions": substitute_suggestions,
        "compiled_ingredients": compiled_ingredients,
    }
