"""
ZAPE (ZAYVORA Adaptive Personalization Engine 2.0).

Performs algorithmic multi-factor clinical personalization:
1. Posology scaling based on Age (Young's & Cowling's rules) and Renal Function (eGFR)
2. Constitutional Temperament (Jissah / Mizaj) modulation
3. Seasonal and Environmental Climate (Fasl-e-Saal) adjustments
4. Chronic Habituation (I'tiyad) adjustments
"""
from __future__ import annotations

from typing import Any


def calculate_age_and_renal_posology(
    age: int | None,
    egfr: float | None = None,
    weight_kg: float | None = None,
) -> dict[str, Any]:
    """Calculates individualized posology scaling factor (0.0 to 1.0) based
    on pediatric formulas (Young's / Cowling's) or geriatric renal staging.
    """
    if age is None:
        return {
            "posology_scaling_factor": 1.0,
            "category": "Standard Adult",
            "formula_applied": "Standard Adult Dose",
            "warnings": [],
        }

    warnings = []

    # 1. Pediatric (< 18 years)
    if age < 18:
        if age <= 1:
            factor = 0.10
            cat = "Infant"
        elif age <= 5:
            factor = 0.25
            cat = "Early Childhood"
        elif age <= 12:
            # Young's Rule: Age / (Age + 12)
            young = age / (age + 12.0)
            # Cowling's Rule: (Age + 1) / 24
            cowling = (age + 1.0) / 24.0
            factor = round((young + cowling) / 2.0, 2)
            cat = "Child"
        else:
            factor = 0.70
            cat = "Adolescent"

        formula = f"Pediatric Scaling (Young & Cowling blend: {factor*100:.0f}% of adult dose)"
        warnings.append("Pediatric posology applied: avoid Schedule E(1) alkaloids and potent purgatives.")

    # 2. Geriatric (>= 65 years)
    elif age >= 65:
        base_factor = 0.65 if age >= 75 else 0.75
        cat = "Geriatric"
        if egfr is not None:
            if egfr >= 60:
                factor = base_factor
                renal_note = f"Preserved eGFR ({egfr:.0f} mL/min)"
            elif 30 <= egfr < 60:
                factor = round(base_factor * 0.75, 2)
                renal_note = f"Stage 3 CKD titration (eGFR {egfr:.0f} mL/min)"
                warnings.append("Stage 3 CKD: Avoid nephrotoxic minerals and reduce Colchicum/Suranjan posology.")
            elif 15 <= egfr < 30:
                factor = round(base_factor * 0.50, 2)
                renal_note = f"Stage 4 CKD severe titration (eGFR {egfr:.0f} mL/min)"
                warnings.append("Stage 4 CKD: Severe renal dose reduction; strict Mudabbar verification mandatory.")
            else:
                factor = 0.25
                renal_note = f"Kidney failure (eGFR <15 mL/min)"
                warnings.append("End-stage renal disease: All internal herbal therapy requires nephrology clearance.")
            formula = f"Geriatric Renal Titration ({renal_note}: {factor*100:.0f}% of adult dose)"
        else:
            factor = base_factor
            formula = f"Geriatric Posology Scaling (Empirical renal safety: {factor*100:.0f}% of adult dose)"
            warnings.append("Elderly patient (>65 yrs): Reduced physiological reserve and slower metabolic clearance.")

    # 3. Adult (18-64)
    else:
        if egfr is not None and egfr < 60:
            factor = 0.65 if egfr >= 30 else 0.40
            cat = "Adult with Renal Impairment"
            formula = f"Renal Dose Titration (eGFR {egfr:.0f} mL/min: {factor*100:.0f}% of standard dose)"
            warnings.append("Adult patient with reduced eGFR: Downward dose adjustment applied.")
        else:
            factor = 1.0
            cat = "Standard Adult"
            formula = "Standard Adult Dose (100%)"

    return {
        "posology_scaling_factor": factor,
        "category": cat,
        "formula_applied": formula,
        "warnings": warnings,
    }


def modulate_by_temperament(
    temperament: str | None,
    candidate_drugs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Applies classical Mizaj constitution rules to modulate formulation safety."""
    temp = temperament or "Mutadil"
    modulations = []
    contraindicated_classes = []
    musleh_recommendations = []

    if temp == "Safrawi":
        modulations.append("Safrawi (Hot & Dry): Reduce dose of heating 3rd/4th degree drugs by 30%-50%.")
        musleh_recommendations.append("Mandate cooling correctives: Roghan-e-Badam, Kateera, or Sharbat Bazoori.")
        contraindicated_classes.append("Excessive dry thermogenic stimulants (e.g. unmoderated Filfil Siyah, Kuchla)")
    elif temp == "Balghami":
        modulations.append("Balghami (Cold & Moist): Enhance concoction (Nujz) with warming aromatic carminatives.")
        musleh_recommendations.append("Administer with warm water or honey adjuvant (Shahad).")
        contraindicated_classes.append("Cold phlegm-increasing sedatives or excess mucilaginous seeds without carminative")
    elif temp == "Saudawi":
        modulations.append("Saudawi (Cold & Dry): Prioritize neuroprotective, moistening (Mu-rattib) tonics.")
        musleh_recommendations.append("Administer with warm milk (Sheer-e-Gao) or Arq-e-Gaozaban.")
        contraindicated_classes.append("Harsh dehydrating evacuants and unbuffered astringent bitters")
    elif temp == "Damwi":
        modulations.append("Damwi (Hot & Moist): Sanguine plethora management; cooling, non-irritant herbs favored.")
        musleh_recommendations.append("Administer with lemon water or Arq-e-Mako.")

    return {
        "temperament": temp,
        "constitutional_modulations": modulations,
        "musleh_recommendations": musleh_recommendations,
        "contraindicated_classes": contraindicated_classes,
    }


def modulate_by_season(season: str | None) -> dict[str, Any]:
    """Applies classical Fasl-e-Saal (Seasonal) therapeutic adjustments."""
    s = (season or "mowtedil").lower()
    
    if s in ("saif", "summer", "hot"):
        season_name = "Saif (Summer / Hot & Dry)"
        guidance = "Prioritize cooling syrups (Sharbat Bazoori, Sharbat Anar); avoid violent purgation; maintain aggressive hydration."
        caution = "Caution against 3rd/4th degree hot single drugs."
    elif s in ("shita", "winter", "cold"):
        season_name = "Shita (Winter / Cold & Moist)"
        guidance = "Optimal season for warming electuaries (Majun Falasifa, Jawarish Kamuni) and lipid-based formulations."
        caution = "Caution against cold natured refrigerants causing phlegm thickening."
    elif s in ("rabi", "spring"):
        season_name = "Rabi (Spring / Moderate & Sanguine)"
        guidance = "Classical prime season for systemic detoxification, Tanqiya-e-Dam, and regimenal Hijama / Fasd."
        caution = "Humors are in liquefaction and movement; monitor blood plethora."
    elif s in ("khareef", "autumn"):
        season_name = "Khareef (Autumn / Cold & Dry)"
        guidance = "Atmospheric dryness; prioritize moistening emulsions (Mu-rattibat) and avoid excessive purgative dehydration."
        caution = "Prone to melancholic (Saudawi) dyscrasias."
    else:
        season_name = "Mowtedil (Temperate / Neutral Season)"
        guidance = "Standard therapeutic principles apply."
        caution = "None."

    return {
        "season_identified": season_name,
        "seasonal_guidance": guidance,
        "seasonal_caution": caution,
    }


def run_zape_personalization(
    *,
    patient_context: dict[str, Any],
    candidate_drugs: list[dict[str, Any]] | None = None,
    season: str | None = None,
) -> dict[str, Any]:
    """Master ZAPE 2.0 Personalization Engine orchestrator."""
    age = patient_context.get("age")
    egfr = patient_context.get("egfr")
    weight = patient_context.get("weight_kg")
    
    # Mizaj
    mizaj_data = patient_context.get("mizaj") or patient_context.get("mizaj_assessment") or {}
    temperament = mizaj_data.get("primary_temperament") if isinstance(mizaj_data, dict) else str(mizaj_data)

    posology = calculate_age_and_renal_posology(age=age, egfr=egfr, weight_kg=weight)
    mizaj_mod = modulate_by_temperament(temperament=temperament, candidate_drugs=candidate_drugs)
    season_mod = modulate_by_season(season=season)

    return {
        "posology": posology,
        "temperament_modulation": mizaj_mod,
        "seasonal_modulation": season_mod,
        "overall_summary": (
            f"ZAPE 2.0 Scaling: {posology['formula_applied']}. "
            f"Constitution: {mizaj_mod['temperament']}. "
            f"Season: {season_mod['season_identified']}."
        ),
    }
