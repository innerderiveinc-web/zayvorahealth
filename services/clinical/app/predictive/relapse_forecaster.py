"""
ZAYVORA HEALTH™ — Predictive Relapse & Deterioration Forecaster (Inzar-o-Intikas)
Synthesizes longitudinal Mizaj drift, Quwa reserves, autonomic wearable strain, and adherence
to forecast disease recurrence probability (Intikas-e-Marad) and trigger proactive clinical alerts.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class PredictiveAssessmentInput:
    patient_id: str
    primary_unani_diagnosis: str
    baseline_mizaj: str                  # e.g., "Damawi Motadil", "Balghami"
    current_mizaj_dominant: str          # e.g., "Safrawi" (if drifted)
    mizaj_drift_velocity: float          # 0.0 to 1.0 (magnitude of temperamental divergence)
    tabiat_reserve_index: float          # 0.0 to 1.0 (Homeostatic buffer)
    quwwat_hayawaniyyah_index: float     # 0.0 to 1.0 (from wearables or clinical pulse)
    medication_adherence_pct: float      # 0 to 100%
    active_symptom_severity_delta: float # -1.0 (improved) to +1.0 (worsened)


@dataclass
class RelapseForecastReport:
    forecast_id: str
    patient_id: str
    evaluated_at_utc: str
    relapse_probability_score: float     # 0.0 to 1.0
    triage_band: str                     # STABLE_EQUILIBRIUM, MILD_DRIFT_MONITOR, HIGH_RELAPSE_RISK, ACUTE_DETERIORATION_ALERT
    morbid_humoral_shift_risk: str       # e.g., "Tahawwul-e-Safrawi (Haar Yabis accumulation)"
    primary_contributing_factors: List[str]
    proactive_clinical_advisory: str
    prophylactic_interventions: List[str]
    requires_clinician_review: bool = True
    safe_to_lock: bool = False           # MANDATORY SAFETY INVARIANT


# In-memory alert store
PREDICTIVE_ALERTS_STORE: Dict[str, List[RelapseForecastReport]] = {}


class RelapseForecasterEngine:
    """Predictive deterioration and relapse forecasting engine."""

    @classmethod
    def evaluate_relapse_risk(
        cls, payload: PredictiveAssessmentInput
    ) -> RelapseForecastReport:
        now_utc = datetime.now(timezone.utc).isoformat()
        forecast_id = f"FCST-{uuid.uuid4().hex[:8].upper()}"

        # 1. Component Risk Weights:
        # - Mizaj Drift (30%)
        # - Quwa Reserve Deficit (25%)
        # - Autonomic / Wearable Strain (20%)
        # - Adherence Gap (15%)
        # - Symptom Delta (10%)

        drift_risk = min(1.0, max(0.0, payload.mizaj_drift_velocity))
        quwa_deficit = max(0.0, 1.0 - payload.tabiat_reserve_index)
        autonomic_strain = max(0.0, 1.0 - payload.quwwat_hayawaniyyah_index)
        adherence_gap = max(0.0, (100.0 - payload.medication_adherence_pct) / 100.0)
        symptom_risk = max(0.0, (payload.active_symptom_severity_delta + 1.0) / 2.0)

        composite_risk = (
            (drift_risk * 0.30)
            + (quwa_deficit * 0.25)
            + (autonomic_strain * 0.20)
            + (adherence_gap * 0.15)
            + (symptom_risk * 0.10)
        )
        relapse_prob = round(composite_risk, 3)

        # 2. Determine Triage Band
        if relapse_prob >= 0.75:
            band = "ACUTE_DETERIORATION_ALERT"
        elif relapse_prob >= 0.50:
            band = "HIGH_RELAPSE_RISK"
        elif relapse_prob >= 0.25:
            band = "MILD_DRIFT_MONITOR"
        else:
            band = "STABLE_EQUILIBRIUM"

        # 3. Contributing factors
        factors = []
        if drift_risk >= 0.40:
            factors.append(f"Pronounced Mizaj drift from baseline {payload.baseline_mizaj} towards {payload.current_mizaj_dominant} ({int(drift_risk*100)}%).")
        if quwa_deficit >= 0.40:
            factors.append(f"Depletion of Tabi'at homeostatic reserve (deficit: {int(quwa_deficit*100)}%).")
        if autonomic_strain >= 0.40:
            factors.append(f"Autonomic nervous exhaustion or suppressed Quwwat-e-Hayawaniyyah ({int(autonomic_strain*100)}%).")
        if adherence_gap >= 0.30:
            factors.append(f"Sub-therapeutic compliance: {int(payload.medication_adherence_pct)}% adherence to prescribed Nuskha.")
        if payload.active_symptom_severity_delta > 0.3:
            factors.append(f"Recent symptomatic resurgence in {payload.primary_unani_diagnosis}.")

        if not factors:
            factors.append("All homeostatic parameters within optimal tolerance.")

        # 4. Proactive Clinical Advisory & Prophylaxis
        prophylaxis = []
        if "Safrawi" in payload.current_mizaj_dominant:
            humoral_shift = "Tahawwul-e-Safrawi (Haar Yabis accumulation)"
            prophylaxis = [
                "Administer Sikanjabeen or Sharbat Bazoori for gentle Tabreed (cooling)",
                "Eliminate pungent, fried, and heavily spiced dietary articles",
                "Hydration with Arq-e-Gulab and chilled coriander water",
            ]
        elif "Balghami" in payload.current_mizaj_dominant:
            humoral_shift = "Tahawwul-e-Balghami (Barid Ratab accumulation)"
            prophylaxis = [
                "Prescribe warming Nujz-e-Balgham decoction",
                "Warm dry fomentation (Takmeed) to affected joints/organ",
                "Avoid ice water, cold curd, and daytime sleeping",
            ]
        elif "Saudawi" in payload.current_mizaj_dominant:
            humoral_shift = "Tahawwul-e-Saudawi (Barid Yabis accumulation)"
            prophylaxis = [
                "Nourishing electuary (Khamira Gaozaban) for neuro-cardiac protection",
                "Warm sesame oil massage (Dalak Layyin)",
                "Avoid dry, stale, and highly salted foodstuffs",
            ]
        else:
            humoral_shift = "Damawi Plethora (Haar Ratab tension)"
            prophylaxis = [
                "Consider prophylactic Hijama bil-shart (cupping) if plethora worsens",
                "Light digestive regimen (Kashk-e-Jao)",
            ]

        if band in ("ACUTE_DETERIORATION_ALERT", "HIGH_RELAPSE_RISK"):
            advisory = (
                f"🚨 PROACTIVE CLINICAL ALERT: Patient exhibits high Intikas probability ({int(relapse_prob * 100)}%). "
                f"Recommend immediate physician consultation, pulse reassessment (Nabz), and corrective Tabreed/Tanqiya."
            )
        else:
            advisory = (
                f"Homeostatic stability maintained ({int(relapse_prob * 100)}% risk). "
                f"Continue routine maintenance and Asbab-e-Sittah adherence."
            )

        report = RelapseForecastReport(
            forecast_id=forecast_id,
            patient_id=payload.patient_id,
            evaluated_at_utc=now_utc,
            relapse_probability_score=relapse_prob,
            triage_band=band,
            morbid_humoral_shift_risk=humoral_shift,
            primary_contributing_factors=factors,
            proactive_clinical_advisory=advisory,
            prophylactic_interventions=prophylaxis,
            requires_clinician_review=True,
            safe_to_lock=False,
        )

        if payload.patient_id not in PREDICTIVE_ALERTS_STORE:
            PREDICTIVE_ALERTS_STORE[payload.patient_id] = []
        PREDICTIVE_ALERTS_STORE[payload.patient_id].append(report)

        return report

    @classmethod
    def get_patient_alerts(cls, patient_id: str) -> List[RelapseForecastReport]:
        return PREDICTIVE_ALERTS_STORE.get(patient_id, [])
