"""
ZAYVORA Health OS™ — Population Learning Network Engine (Phase 27)
==================================================================
Implements macro-epidemiological intelligence, seasonal humoral trend compilation,
and multi-clinic pharmacovigilance signal detection across global clinical nodes:

1. Macro-Epidemiological Humoral Surveillance:
   - Cohort-wide humoral distribution tracking (Dam, Safra, Balgham, Sawda)
   - Cross-clinic phenotype frequency analytics
2. Macro-Regional Seasonal Trend Compiler:
   - Telemetry-informed Asbab-e-Sittah weather coupling (Temp, Humidity, Barometer)
   - Canonical 4-season humoral vulnerability index (Bahar, Saif, Khazan, Shita)
3. Global Pharmacovigilance Signal Detector (Evans / MHRA / WHO Standard):
   - Proportional Reporting Ratio (PRR) computation
   - Chi-Square (chi^2) with Yates' continuity correction
   - Signal threshold criteria: a >= 3, PRR >= 2.0, chi^2 >= 4.0
4. Public Health Alert & Cluster Notification Protocol (ICD-11 TM cross-mapped)
"""

from __future__ import annotations

import enum
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class CanonicalMausim(str, enum.Enum):
    MAUSIM_E_BAHAR = "MAUSIM_E_BAHAR"    # Spring (Haar-Ratab: Hot & Moist)
    MAUSIM_E_SAIF = "MAUSIM_E_SAIF"      # Summer (Haar-Yabis: Hot & Dry)
    MAUSIM_E_KHAZAN = "MAUSIM_E_KHAZAN"  # Autumn (Barid-Yabis: Cold & Dry)
    MAUSIM_E_SHITA = "MAUSIM_E_SHITA"    # Winter (Barid-Ratab: Cold & Moist)


@dataclass
class MacroWeatherTelemetry:
    region_id: str
    ambient_temp_c: float
    relative_humidity_pct: float
    barometric_pressure_hpa: float
    recorded_at: str


@dataclass
class SeasonalHumoralVulnerability:
    season: CanonicalMausim
    season_name: str
    elemental_quality: str
    predominant_humor: str
    vulnerability_index: float  # 0.0 to 1.0
    clinical_manifestations: List[str]
    preventive_parhez_principles: List[str]
    asbab_sitta_guidance: Dict[str, str]


@dataclass
class SafetySurveillanceSignal:
    signal_id: str
    suspected_drug: str
    adverse_reaction: str
    case_count_a: int
    other_adverse_events_b: int
    control_cases_c: int
    control_other_d: int
    proportional_reporting_ratio: float
    chi_square_yates: float
    is_statistically_significant_signal: bool
    signal_strength: str  # "NONE", "POTENTIAL_SIGNAL", "CONFIRMED_SIGNAL", "CRITICAL_SAFETY_HOLD"
    icd_11_tm_code: str
    recommended_clinical_action: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MacroHumoralCensusReport:
    reporting_period: str
    total_active_patients: int
    participating_clinics_count: int
    humoral_distribution: Dict[str, float]
    top_dominant_phenotypes: List[Dict[str, Any]]
    seasonal_vulnerability: SeasonalHumoralVulnerability
    active_safety_signals: List[SafetySurveillanceSignal]
    generated_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PopulationLearningNetworkEngine:
    """
    Macro-epidemiological intelligence and safety surveillance network engine.
    Computes authentic multi-clinic pharmacovigilance signals and seasonal humoral trends.
    """

    SEASON_PROFILES: Dict[CanonicalMausim, Dict[str, Any]] = {
        CanonicalMausim.MAUSIM_E_BAHAR: {
            "name": "Mausim-e-Bahar (Spring)",
            "quality": "Haar-Ratab (Hot & Moist)",
            "humor": "Dam (Blood)",
            "manifestations": [
                "Blood agitation and epistaxis",
                "Cutaneous eruptions and urticaria (Hikka)",
                "Hypertensive surges",
            ],
            "parhez": [
                "Avoid excessively heavy, sweet, or oily foods",
                "Incorporate cooling sikanjabeen and mild venesection (Fasd) if indicated",
            ],
            "asbab": {
                "hawa": "Air is warming and moistening; open windows in morning",
                "makul_mashrub": "Favor barley water (Ma-ul-Shaeer) and light potherbs",
                "harakat": "Moderate aerobic movement before noon",
            },
        },
        CanonicalMausim.MAUSIM_E_SAIF: {
            "name": "Mausim-e-Saif (Summer)",
            "quality": "Haar-Yabis (Hot & Dry)",
            "humor": "Safra (Yellow Bile)",
            "manifestations": [
                "Bilious gastritis and nausea",
                "Dehydration and heat exhaustion",
                "Hepato-biliary irritability and pruritus",
            ],
            "parhez": [
                "Strict avoidance of pungent, spicy, or fried foods",
                "Liberal use of Tamarind, Plum syrup (Sharbat-e-Aloo Bukhara), and cold infusions",
            ],
            "asbab": {
                "hawa": "Avoid midday solar exposure (Loo)",
                "makul_mashrub": "Consume cooling mucilages (Gond Katira, Tukhm-e-Balanga)",
                "naum_yaqza": "Brief midday siesta (Qailula) encouraged",
            },
        },
        CanonicalMausim.MAUSIM_E_KHAZAN: {
            "name": "Mausim-e-Khazan (Autumn)",
            "quality": "Barid-Yabis (Cold & Dry)",
            "humor": "Sawda (Black Bile)",
            "manifestations": [
                "Dry dermatoses and pruritus hiemalis",
                "Arthralgia and joint crepitus",
                "Melancholic insomnia and anxiety exacerbations",
            ],
            "parhez": [
                "Avoid dry, stale, cold, or astringent foods (cabbage, beef, brinjal)",
                "Favor unctuous broths, almond oil (Roghan Badam Shireen), and warm milk",
            ],
            "asbab": {
                "hawa": "Guard against sudden diurnal temperature drops",
                "makul_mashrub": "Warm, lubricating unctuous foods (Charba broth)",
                "riyazat": "Gentle oil massage (Dalk layyin) with warm chamomile or sesame oil",
            },
        },
        CanonicalMausim.MAUSIM_E_SHITA: {
            "name": "Mausim-e-Shita (Winter)",
            "quality": "Barid-Ratab (Cold & Moist)",
            "humor": "Balgham (Phlegm)",
            "manifestations": [
                "Bronchial congestion, catarrh (Nazla & Zukam)",
                "Joint stiffness and Waja-ul-Mafasil flare-ups",
                "Sluggish gastrointestinal digestion (Su-e-Hazm)",
            ],
            "parhez": [
                "Avoid ice-cold beverages, dairy curd, and refrigerated foods",
                "Favor warming spices: Ginger (Zanjabeel), Clove (Qaranfal), Cinnamon (Darchini)",
            ],
            "asbab": {
                "hawa": "Protect limbs and chest from cold draughts",
                "makul_mashrub": "Hot infusions of Ustukhuddus and Zanjabeel",
                "harakat": "Vigorous indoor exercise to stimulate Hararat-e-Ghariziyya",
            },
        },
    }

    @classmethod
    def compile_seasonal_vulnerability(
        cls, telemetry: Optional[MacroWeatherTelemetry] = None
    ) -> SeasonalHumoralVulnerability:
        """
        Determines current canonical season and calculates seasonal vulnerability index
        based on weather telemetry and classical Asbab-e-Sittah dynamics.
        """
        now = datetime.now(timezone.utc)
        month = now.month

        # Fallback or telemetry-informed season selection
        if telemetry:
            t = telemetry.ambient_temp_c
            rh = telemetry.relative_humidity_pct
            if t > 30.0:
                season = CanonicalMausim.MAUSIM_E_SAIF
            elif t < 18.0 and rh > 60.0:
                season = CanonicalMausim.MAUSIM_E_SHITA
            elif t < 24.0 and rh < 45.0:
                season = CanonicalMausim.MAUSIM_E_KHAZAN
            else:
                season = CanonicalMausim.MAUSIM_E_BAHAR
        else:
            if month in (2, 3, 4):
                season = CanonicalMausim.MAUSIM_E_BAHAR
            elif month in (5, 6, 7):
                season = CanonicalMausim.MAUSIM_E_SAIF
            elif month in (8, 9, 10):
                season = CanonicalMausim.MAUSIM_E_KHAZAN
            else:
                season = CanonicalMausim.MAUSIM_E_SHITA

        profile = cls.SEASON_PROFILES[season]
        # Vulnerability index peaks in extreme heat or cold
        vuln_index = 0.75 if season in (CanonicalMausim.MAUSIM_E_SAIF, CanonicalMausim.MAUSIM_E_SHITA) else 0.55

        return SeasonalHumoralVulnerability(
            season=season,
            season_name=profile["name"],
            elemental_quality=profile["quality"],
            predominant_humor=profile["humor"],
            vulnerability_index=vuln_index,
            clinical_manifestations=profile["manifestations"],
            preventive_parhez_principles=profile["parhez"],
            asbab_sitta_guidance=profile["asbab"],
        )

    @classmethod
    def evaluate_pharmacovigilance_signal(
        cls,
        suspected_drug: str,
        adverse_reaction: str,
        a: int,  # Drug + Reaction
        b: int,  # Drug + Other reactions
        c: int,  # Other drugs + Reaction
        d: int,  # Other drugs + Other reactions
        icd_11_tm_code: str = "TM-ADR-001",
    ) -> SafetySurveillanceSignal:
        """
        Calculates Proportional Reporting Ratio (PRR) and Chi-Square with Yates' continuity correction
        according to the Evans / WHO / UK MHRA pharmacovigilance standard.

        Signal Criteria:
        - a >= 3
        - PRR >= 2.0
        - chi^2 >= 4.0
        """
        n = a + b + c + d
        if (a + b) == 0 or (c + d) == 0 or (a + c) == 0 or (b + d) == 0 or n == 0:
            return SafetySurveillanceSignal(
                signal_id=f"SIG-NULL-{suspected_drug[:4]}",
                suspected_drug=suspected_drug,
                adverse_reaction=adverse_reaction,
                case_count_a=a,
                other_adverse_events_b=b,
                control_cases_c=c,
                control_other_d=d,
                proportional_reporting_ratio=0.0,
                chi_square_yates=0.0,
                is_statistically_significant_signal=False,
                signal_strength="NONE",
                icd_11_tm_code=icd_11_tm_code,
                recommended_clinical_action="Insufficient surveillance data.",
            )

        # Proportional Reporting Ratio: (a / (a+b)) / (c / (c+d))
        rate_drug = a / (a + b)
        rate_control = c / (c + d)
        prr = round(rate_drug / max(1e-6, rate_control), 2)

        # Chi-Square with Yates' continuity correction:
        # chi^2 = N * (|ad - bc| - N/2)^2 / ((a+b)*(c+d)*(a+c)*(b+d))
        numerator_raw = abs(a * d - b * c) - (n / 2.0)
        numerator = max(0.0, numerator_raw) ** 2 * n
        denominator = (a + b) * (c + d) * (a + c) * (b + d)
        chi2 = round(numerator / denominator, 2) if denominator > 0 else 0.0

        is_significant = (a >= 3) and (prr >= 2.0) and (chi2 >= 4.0)

        if is_significant:
            if prr >= 4.0 and chi2 >= 10.0:
                strength = "CRITICAL_SAFETY_HOLD"
                action = "IMMEDIATE DSMB ALERT: High-magnitude safety signal. Restrict dispensing and initiate batch assay."
            else:
                strength = "CONFIRMED_SIGNAL"
                action = "Active pharmacovigilance watch: Notify clinical committee and request targeted follow-up."
        elif a >= 2 and prr >= 1.5:
            strength = "POTENTIAL_SIGNAL"
            action = "Monitor trend in subsequent reporting periods."
        else:
            strength = "NONE"
            action = "Routine surveillance."

        return SafetySurveillanceSignal(
            signal_id=f"SIG-{suspected_drug[:4].upper()}-{abs(hash(adverse_reaction)) % 10000:04d}",
            suspected_drug=suspected_drug,
            adverse_reaction=adverse_reaction,
            case_count_a=a,
            other_adverse_events_b=b,
            control_cases_c=c,
            control_other_d=d,
            proportional_reporting_ratio=prr,
            chi_square_yates=chi2,
            is_statistically_significant_signal=is_significant,
            signal_strength=strength,
            icd_11_tm_code=icd_11_tm_code,
            recommended_clinical_action=action,
        )

    @classmethod
    def generate_population_census(
        cls,
        patient_records: List[Dict[str, Any]],
        clinic_ids: List[str],
        weather_telemetry: Optional[MacroWeatherTelemetry] = None,
        safety_reports: Optional[List[Dict[str, Any]]] = None,
    ) -> MacroHumoralCensusReport:
        """
        Compiles cohort-wide macro-epidemiological census across participating clinics:
        - Humoral distribution percentages
        - Dominant sub-phenotypes
        - Current seasonal vulnerability guidance
        - Evaluated statistical safety signals
        """
        total = len(patient_records)
        humor_counts: Dict[str, int] = {
            "Damwi (Sanguinous)": 0,
            "Safrawi (Choleric)": 0,
            "Balghami (Phlegmatic)": 0,
            "Sawdawi (Melancholic)": 0,
            "Mu'tadil (Equilibrium)": 0,
        }
        phenotype_counts: Dict[str, int] = {}

        for p in patient_records:
            mizaj = str(p.get("dominant_humor", "Balghami")).upper()
            if "DAM" in mizaj:
                humor_counts["Damwi (Sanguinous)"] += 1
            elif "SAFRA" in mizaj:
                humor_counts["Safrawi (Choleric)"] += 1
            elif "BALGHAM" in mizaj:
                humor_counts["Balghami (Phlegmatic)"] += 1
            elif "SAWDA" in mizaj:
                humor_counts["Sawdawi (Melancholic)"] += 1
            else:
                humor_counts["Mu'tadil (Equilibrium)"] += 1

            ptype = p.get("phenotype_code", "UNKNOWN")
            phenotype_counts[ptype] = phenotype_counts.get(ptype, 0) + 1

        denom = max(1, total)
        distribution = {k: round((v / denom) * 100.0, 1) for k, v in humor_counts.items()}

        sorted_phenos = sorted(phenotype_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_phenos = [{"code": k, "count": v, "pct": round((v / denom) * 100.0, 1)} for k, v in sorted_phenos]

        seasonal_advisory = cls.compile_seasonal_vulnerability(weather_telemetry)

        # Evaluate safety signals if contingency data provided
        signals: List[SafetySurveillanceSignal] = []
        if safety_reports:
            for rep in safety_reports:
                sig = cls.evaluate_pharmacovigilance_signal(
                    suspected_drug=rep.get("drug", "Unknown"),
                    adverse_reaction=rep.get("reaction", "Unknown"),
                    a=rep.get("a", 0),
                    b=rep.get("b", 0),
                    c=rep.get("c", 0),
                    d=rep.get("d", 0),
                    icd_11_tm_code=rep.get("icd_code", "TM-ADR-001"),
                )
                signals.append(sig)

        return MacroHumoralCensusReport(
            reporting_period=datetime.now(timezone.utc).strftime("%Y-Q%m"),
            total_active_patients=total,
            participating_clinics_count=len(clinic_ids),
            humoral_distribution=distribution,
            top_dominant_phenotypes=top_phenos,
            seasonal_vulnerability=seasonal_advisory,
            active_safety_signals=signals,
        )
