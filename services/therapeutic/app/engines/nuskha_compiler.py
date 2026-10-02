"""
ZAYVORA Classical Nuskha Compiler & Formulation Balancing Engine.

ZAYVORA Clinical Architecture Specification v4.0 §14, §18 (Nuskha Nawisi Sequence) & §19.

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
    if not ratios:
        for k, r in BADAL_POTENCY_RATIOS.items():
            if k in orig_key or orig_key in k:
                ratios = r
                break

    ratio = ratios.get(badal_key)
    if ratio is None:
        for bk, r in ratios.items():
            if bk in badal_key or badal_key in bk:
                ratio = r
                break
    if ratio is None:
        ratio = 1.0

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

        sub_identity = None
        try:
            from services.knowledge.app.core.canonical_substance_identity import CanonicalSubstanceIdentityService
            sub_res = CanonicalSubstanceIdentityService.resolve_substance(raw_name)
            if sub_res.get("matched"):
                sub_identity = sub_res
        except Exception:
            pass

        for k, profile in CLASSICAL_CORRECTIVES_AND_SUBSTITUTES.items():
            if k in base_name or base_name in k:
                matched_profile = profile
                break

        if not matched_profile and sub_identity:
            matched_profile = {
                "musleh": sub_identity.get("musleh") or "",
                "badal": sub_identity.get("badal") or "",
                "primary_organ_axis": sub_identity.get("primary_organ_axis") or primary_axis,
                "default_adult_dose_mg": sub_identity.get("default_adult_dose_mg") or 500.0,
            }

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
        if matched_profile and matched_profile.get("musleh"):
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
            "canonical_id": sub_identity.get("canonical_id") if sub_identity else None,
            "canonical_name": sub_identity.get("canonical_name") if sub_identity else raw_name,
            "classical_role": role,
            "target_axis_alignment": (matched_profile.get("primary_organ_axis") if matched_profile else primary_axis),
            "prescribed_dose_mg": dose_mg,
            "clinically_adjusted_dose_mg": posology["calculated_mg"],
            "posology_adjustments": posology["adjustment_reasons"],
            "musleh": ing.get("musleh") or (matched_profile.get("musleh") if matched_profile else ""),
            "badal": ing.get("badal") or (matched_profile.get("badal") if matched_profile else ""),
            "is_mudabbar": ing.get("is_mudabbar") or (sub_identity.get("mandatory_mudabbar") if sub_identity else False),
            "mudabbar_process": ing.get("mudabbar_process", "") or (sub_identity.get("mudabbar_protocol") if sub_identity else ""),
            "is_schedule_e1": sub_identity.get("is_schedule_e1", False) if sub_identity else False,
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


# -----------------------------------------------------------------------------
# Four-Tier Nuskha Architecture & 80/20 Clinical Rule
# -----------------------------------------------------------------------------
FORBIDDEN_RAW_TOXICS = [
    "raw kuchla", "unpurified nux-vomica", "raw strychnos",
    "raw shingraf", "unpurified cinnabar",
    "raw suranjan", "unpurified colchicum",
    "raw jamalgota", "unpurified croton",
    "raw bhilawa", "unpurified marking nut",
    "unpurified aconite", "raw bish"
]


def verify_four_tier_nuskha_architecture(
    ingredients: list[dict[str, Any]],
    total_batch_weight_mg: float | None = None
) -> dict[str, Any]:
    """
    Validates a prescription against the Classical 4-Tier Nuskha Architecture:
    1. Tier 1: Asl / Juz-e-Azam (Primary therapeutic driver)
    2. Tier 2: Mua'wwid / Muin (Synergist & bioavailability catalyst)
    3. Tier 3: Musleh (Corrective / harmonizer neutralizing toxicity)
    4. Tier 4: Muhsin (Vehicle, demulcent, taste & mucosal protector)
    
    Also enforces the 80/20 rule:
    - Active therapeutic mass (Tier 1 + 2) ~ 75-85% (target 80%)
    - Protective/vehicle buffer (Tier 3 + 4) ~ 15-25% (target 20%)
    """
    tiers = {
        "tier1_asl": [],
        "tier2_muawwid": [],
        "tier3_musleh": [],
        "tier4_muhsin": []
    }
    tier_weights = {
        "tier1_asl": 0.0,
        "tier2_muawwid": 0.0,
        "tier3_musleh": 0.0,
        "tier4_muhsin": 0.0
    }
    
    toxic_alerts = []
    
    for ing in ingredients:
        name = ing.get("name", "").lower()
        role = (ing.get("classical_role") or ing.get("role") or "").lower()
        dose = float(ing.get("prescribed_dose_mg") or ing.get("dose_mg") or 0.0)
        is_mudabbar = ing.get("is_mudabbar", False)
        
        # Check raw toxic substances
        for tox in FORBIDDEN_RAW_TOXICS:
            if tox in name and not is_mudabbar:
                toxic_alerts.append(
                    f"CRITICAL SAFETY VIOLATION: '{ing.get('name')}' is classified as toxic and requires certified Mudabbar purification before dispensing."
                )
                
        # Categorize tier
        if "asl" in role or "juz_e_azam" in role or "chief" in role or "active" in role:
            tiers["tier1_asl"].append(ing)
            tier_weights["tier1_asl"] += dose
        elif "muawwid" in role or "muin" in role or "synergist" in role or "bio-enhancer" in role:
            tiers["tier2_muawwid"].append(ing)
            tier_weights["tier2_muawwid"] += dose
        elif "musleh" in role or "corrective" in role or "harmonizer" in role:
            tiers["tier3_musleh"].append(ing)
            tier_weights["tier3_musleh"] += dose
        elif "muhsin" in role or "vehicle" in role or "base" in role or "protective" in role:
            tiers["tier4_muhsin"].append(ing)
            tier_weights["tier4_muhsin"] += dose
        else:
            # Default to Tier 1 Asl if unspecified
            tiers["tier1_asl"].append(ing)
            tier_weights["tier1_asl"] += dose

    total_weight = sum(tier_weights.values()) or total_batch_weight_mg or 1.0
    therapeutic_core_pct = round(((tier_weights["tier1_asl"] + tier_weights["tier2_muawwid"]) / total_weight) * 100, 1)
    protective_buffer_pct = round(((tier_weights["tier3_musleh"] + tier_weights["tier4_muhsin"]) / total_weight) * 100, 1)
    
    rule_80_20_compliant = 65.0 <= therapeutic_core_pct <= 90.0
    
    return {
        "status": "passed" if len(toxic_alerts) == 0 else "failed_safety",
        "is_four_tier_complete": all(len(v) > 0 for v in tiers.values()),
        "tiers": tiers,
        "tier_weights_mg": tier_weights,
        "therapeutic_core_pct": therapeutic_core_pct,
        "protective_buffer_pct": protective_buffer_pct,
        "rule_80_20_compliant": rule_80_20_compliant,
        "toxic_alerts": toxic_alerts,
        "clinical_notes": (
            f"Active Core: {therapeutic_core_pct}% | Protective/Vehicle: {protective_buffer_pct}%. "
            + ("80/20 balance optimal." if rule_80_20_compliant else "Rebalance formulation towards 80% active / 20% protective.")
        )
    }
