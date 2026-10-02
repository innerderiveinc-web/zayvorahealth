"""
ZAYVORA Health OS™ v5.0 — Asbab Sitta Zarooriya Dynamic Scoring & Lifestyle Engine
==================================================================================
Codifies the 6 Essential Determinants of Health in Unani Medicine:
  1. Hawa-e-Muheet (Ambient Air, Environmental Quality & Seasonal Weather)
  2. Makool wa Mashroob (Dietary Quality, Quantity, Glycemic Load & Hydration)
  3. Harkat wa Sukoon Badani (Physical Movement, Sedentary Hours & Exercise)
  4. Harkat wa Sukoon Nafsani (Emotional Equilibrium, Stress & Mental Agitation)
  5. Naum wa Yaqzah (Sleep Architecture, Circadian Timing & Sleep Duration)
  6. Ihtibas wa Istifragh (Retention of Essentials & Evacuation of Metabolic Wastes)

Invariants:
  - Generates a quantitative Asbab Sitta Equilibrium Score (0 - 100).
  - Identifies humoral lifestyle aggravations (Safra, Balgham, Sawda, Dam).
  - Outputs actionable, personalized Tadbeer-e-Asbab-e-Sitta corrective regimens.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AsbabSittaPatientInput:
    # 1. Hawa-e-Muheet
    air_quality_exposure: str = "MODERATE"     # "CLEAN" | "MODERATE" | "HIGH_POLLUTION" | "INDOOR_AC_CHRONIC"
    seasonal_climate_fit: bool = True          # True if dressed/housed appropriately for season

    # 2. Makool wa Mashroob
    meals_on_time: bool = True                 # Regular eating schedule
    dietary_greasy_spicy_load: str = "LOW"     # "LOW" | "MODERATE" | "HIGH"
    hydration_adequate: bool = True            # >= 2.5L clean water / herbal infusions
    refined_sugar_consumption: str = "LOW"     # "LOW" | "MODERATE" | "HIGH"

    # 3. Harkat wa Sukoon Badani
    daily_sedentary_hours: float = 6.0         # Hours sitting
    exercise_minutes_per_week: int = 150       # Moderate physical activity

    # 4. Harkat wa Sukoon Nafsani
    chronic_psychological_stress: str = "LOW"  # "LOW" | "MODERATE" | "SEVERE"
    anxiety_or_anger_episodes: str = "RARE"    # "RARE" | "OCCASIONAL" | "FREQUENT"

    # 5. Naum wa Yaqzah
    sleep_hours_per_night: float = 7.5         # Ideal 7.0 - 8.5
    bedtime_hour_24h: float = 23.0             # Hour of sleep (ideal <= 23.0)
    sleep_restorative: bool = True             # Wakes up refreshed

    # 6. Ihtibas wa Istifragh
    daily_bowel_movements: int = 1             # 1-2 is optimal
    constipation_present: bool = False         # Straining / dry stools
    sweat_production_normal: bool = True       # Neither excessive nor anhidrotic
    menses_regular_if_female: Optional[bool] = None  # None for male / not applicable


class AsbabSittaScoringEngine:
    """Quantitative scoring and corrective prescription engine for Asbab Sitta Zarooriya."""

    @classmethod
    def evaluate_lifestyle_equilibrium(
        cls,
        patient_id: str,
        patient_mizaj: str,
        data: AsbabSittaPatientInput
    ) -> Dict[str, Any]:
        scores: Dict[str, float] = {}
        violations: List[str] = []
        humoral_aggravations: Dict[str, int] = {"Safra": 0, "Balgham": 0, "Sawda": 0, "Dam": 0}
        tadbeer_prescriptions: List[str] = []

        # -------------------------------------------------------------
        # 1. Hawa-e-Muheet (Max 15 pts)
        # -------------------------------------------------------------
        hawa_score = 15.0
        if data.air_quality_exposure == "HIGH_POLLUTION":
            hawa_score -= 6.0
            violations.append("Chronic exposure to atmospheric pollutants (Fasad-e-Hawa)")
            humoral_aggravations["Sawda"] += 2
        elif data.air_quality_exposure == "INDOOR_AC_CHRONIC":
            hawa_score -= 4.0
            violations.append("Continuous artificial refrigeration drying airway mucosa (Buroodat wa Yuboosat)")
            humoral_aggravations["Balgham"] += 2
        if not data.seasonal_climate_fit:
            hawa_score -= 3.0
            violations.append("Inadequate adaptation to prevailing seasonal temperament (Tadbeer-e-Fusool deficit)")
        scores["hawa_muheet"] = max(0.0, hawa_score)

        # -------------------------------------------------------------
        # 2. Makool wa Mashroob (Max 20 pts)
        # -------------------------------------------------------------
        diet_score = 20.0
        if not data.meals_on_time:
            diet_score -= 4.0
            violations.append("Irregular meal timings disrupting Hazm-e-Meda circadian clock")
            humoral_aggravations["Safra"] += 1
        if data.dietary_greasy_spicy_load == "HIGH":
            diet_score -= 5.0
            violations.append("Excessive heating, greasy and pungent foods (Aghziya Harrah Harifah)")
            humoral_aggravations["Safra"] += 3
        if data.refined_sugar_consumption == "HIGH":
            diet_score -= 5.0
            violations.append("High glycemic refined carbohydrate intake (Sudad-e-Jigar trigger)")
            humoral_aggravations["Balgham"] += 3
        if not data.hydration_adequate:
            diet_score -= 4.0
            violations.append("Insufficient hydration causing cellular and renal yuboosat (dryness)")
            humoral_aggravations["Sawda"] += 2
        scores["makool_mashroob"] = max(0.0, diet_score)

        # -------------------------------------------------------------
        # 3. Harkat wa Sukoon Badani (Max 15 pts)
        # -------------------------------------------------------------
        move_score = 15.0
        if data.daily_sedentary_hours > 8.0:
            move_score -= 5.0
            violations.append(f"Excessive physical sedentariness ({data.daily_sedentary_hours} hrs/day) causing humoral stasis (Kasrat-us-Sukoon)")
            humoral_aggravations["Balgham"] += 3
        if data.exercise_minutes_per_week < 90:
            move_score -= 5.0
            violations.append("Sub-optimal weekly exercise failing to stimulate Hararat-e-Ghariziyyah (Innate Metabolic Heat)")
        elif data.exercise_minutes_per_week > 300:
            # Excessive physical exhaustion
            move_score -= 2.0
            violations.append("Excessive physical overexertion causing vital moisture dissipation (Tahlil-e-Rutoobat)")
        scores["harkat_badani"] = max(0.0, move_score)

        # -------------------------------------------------------------
        # 4. Harkat wa Sukoon Nafsani (Max 15 pts)
        # -------------------------------------------------------------
        mind_score = 15.0
        if data.chronic_psychological_stress == "SEVERE":
            mind_score -= 8.0
            violations.append("Severe unremitting psychic distress inducing chronic cortisol/HPA hyperdrive (Fikr wa Gham)")
            humoral_aggravations["Sawda"] += 4
        elif data.chronic_psychological_stress == "MODERATE":
            mind_score -= 4.0
            violations.append("Moderate psychological tension affecting gastric tone (Su-e-Hazm Nafsani)")
            humoral_aggravations["Sawda"] += 2
        if data.anxiety_or_anger_episodes == "FREQUENT":
            mind_score -= 4.0
            violations.append("Recurrent spikes of fury and agitation causing acute bile surge (Harkat-e-Nafsaniyah Harrah)")
            humoral_aggravations["Safra"] += 3
        scores["harkat_nafsani"] = max(0.0, mind_score)

        # -------------------------------------------------------------
        # 5. Naum wa Yaqzah (Max 20 pts)
        # -------------------------------------------------------------
        sleep_score = 20.0
        if data.sleep_hours_per_night < 6.0:
            sleep_score -= 7.0
            violations.append(f"Sleep deprivation ({data.sleep_hours_per_night} hrs) causing visceral dryness and neuro-exhaustion (Qillat-un-Naum)")
            humoral_aggravations["Safra"] += 2
            humoral_aggravations["Sawda"] += 2
        elif data.sleep_hours_per_night > 9.5:
            sleep_score -= 4.0
            violations.append("Excessive daytime or prolonged sleep increasing cold phlegmatic stasis (Kasrat-un-Naum)")
            humoral_aggravations["Balgham"] += 3

        if data.bedtime_hour_24h >= 24.0 or data.bedtime_hour_24h < 4.0:
            sleep_score -= 5.0
            violations.append(f"Late nocturnal sleep onset ({data.bedtime_hour_24h}:00) disrupting melatonin & liver clearance rhythms")
            humoral_aggravations["Safra"] += 2

        if not data.sleep_restorative:
            sleep_score -= 3.0
            violations.append("Non-restorative, fragmented sleep architecture")
        scores["naum_yaqzah"] = max(0.0, sleep_score)

        # -------------------------------------------------------------
        # 6. Ihtibas wa Istifragh (Max 15 pts)
        # -------------------------------------------------------------
        waste_score = 15.0
        if data.constipation_present or data.daily_bowel_movements < 1:
            waste_score -= 8.0
            violations.append("Intestinal constipation retaining toxic metabolic wastes in circulation (Ihtibas-e-Fasida)")
            humoral_aggravations["Sawda"] += 3
            humoral_aggravations["Balgham"] += 2
        if not data.sweat_production_normal:
            waste_score -= 3.0
            violations.append("Impaired diaphoresis / cutaneous pore retention (Ihtibas-e-Araq)")
        if data.menses_regular_if_female is False:
            waste_score -= 4.0
            violations.append("Uterine oligomenorrhea / retention of uterine wastes (Ehtibas-e-Tams)")
            humoral_aggravations["Dam"] += 2
        scores["ihtibas_istifragh"] = max(0.0, waste_score)

        # Total Equilibrium Score (0 - 100)
        total_score = round(sum(scores.values()), 1)

        # -------------------------------------------------------------
        # Targeted Tadbeer-e-Asbab-e-Sitta Prescriptions
        # -------------------------------------------------------------
        if scores["naum_yaqzah"] < 15.0:
            tadbeer_prescriptions.append("Tadbeer-e-Naum: Hard curfew of 10:30 PM bedtime; cease blue screens 60 mins before sleep; massage soles of feet with warm sesame or pumpkin seed oil (Tadheen-e-Kaf-e-Pa).")
        if scores["ihtibas_istifragh"] < 11.0:
            tadbeer_prescriptions.append("Tadbeer-e-Tanqiya: Daily morning lukewarm water with 1 tbsp soaked Isabgol husk or 5 soaked figs (Anjeer) to restore natural peristaltic Istifragh.")
        if scores["harkat_badani"] < 11.0:
            tadbeer_prescriptions.append("Tadbeer-e-Riyazat: Prescribe 30 minutes of brisk walking (Riyazat-e-Motadilah) during morning hours before breakfast to ignite Hararat-e-Ghariziyyah.")
        if scores["harkat_nafsani"] < 11.0:
            tadbeer_prescriptions.append("Tadbeer-e-Nafsani: Prescribe daily deep diaphragmatic breathing (Tanaffus-e-Ameeq) for 15 minutes twice daily; Chamomile / Gaozaban infusion in evening.")
        if scores["makool_mashroob"] < 15.0:
            tadbeer_prescriptions.append("Tadbeer-e-Ghiza: Strictly enforce 3-column Parhez-e-Khas; eliminate late-night dining; prioritize freshly cooked warm whole foods matching constitutional Mizaj.")

        # Determine if lifestyle aligns with patient's baseline Mizaj
        dominant_agg = max(humoral_aggravations, key=humoral_aggravations.get)
        mizaj_conflict = False
        if patient_mizaj.lower() in dominant_agg.lower() and humoral_aggravations[dominant_agg] >= 4:
            mizaj_conflict = True
            violations.insert(0, f"CRITICAL TEMPERAMENT CONFLICT: Lifestyle is actively escalating patient's innate {patient_mizaj} tendency into pathological Su-e-Mizaj.")

        # Status Grade
        if total_score >= 85.0:
            grade = "EXCELLENT_EQUILIBRIUM"
        elif total_score >= 70.0:
            grade = "MODERATE_EQUILIBRIUM"
        elif total_score >= 50.0:
            grade = "SUBSTANTIAL_DYSREGULATION"
        else:
            grade = "CRITICAL_LIFESTYLE_COLLAPSE"

        return {
            "patient_id": patient_id,
            "patient_mizaj": patient_mizaj,
            "asbab_sitta_equilibrium_score": total_score,
            "grade": grade,
            "domain_scores": scores,
            "identified_lifestyle_violations": violations,
            "humoral_aggravation_vectors": humoral_aggravations,
            "primary_aggravated_humor": dominant_agg,
            "temperament_conflict_flag": mizaj_conflict,
            "corrective_tadbeer_prescriptions": tadbeer_prescriptions,
            "non_pharmacological_first_line_indicated": total_score < 70.0
        }
