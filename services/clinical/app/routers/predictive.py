"""
ZAYVORA HEALTH™ — Predictive Health & Relapse Forecaster Router
Provides endpoints for calculating Intikas-e-Marad relapse risk and retrieving proactive alerts.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from ..predictive.relapse_forecaster import (
    PredictiveAssessmentInput,
    RelapseForecasterEngine,
    RelapseForecastReport,
)

router = APIRouter(prefix="/api/v1/predictive", tags=["Predictive Relapse & Deterioration"])


class EvaluateRelapseRequest(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    primary_unani_diagnosis: str = Field(..., description="Primary Unani diagnosis (e.g. Waja-ul-Mafasil, Niqras)")
    baseline_mizaj: str = Field("Damawi Motadil", description="Patient's baseline balanced constitution")
    current_mizaj_dominant: str = Field("Safrawi", description="Current dominant humor detected")
    mizaj_drift_velocity: float = Field(..., ge=0.0, le=1.0, description="Rate/magnitude of Mizaj drift (0.0 to 1.0)")
    tabiat_reserve_index: float = Field(..., ge=0.0, le=1.0, description="Tabi'at homeostatic buffer reserve (0.0 to 1.0)")
    quwwat_hayawaniyyah_index: float = Field(0.7, ge=0.0, le=1.0, description="Vital/autonomic tone index (0.0 to 1.0)")
    medication_adherence_pct: float = Field(85.0, ge=0.0, le=100.0, description="Medication compliance percentage")
    active_symptom_severity_delta: float = Field(0.0, ge=-1.0, le=1.0, description="Symptom delta (-1.0 to +1.0)")


@router.post("/evaluate-relapse", summary="Calculate real-time relapse and deterioration risk")
async def evaluate_relapse(payload: EvaluateRelapseRequest):
    input_data = PredictiveAssessmentInput(
        patient_id=payload.patient_id,
        primary_unani_diagnosis=payload.primary_unani_diagnosis,
        baseline_mizaj=payload.baseline_mizaj,
        current_mizaj_dominant=payload.current_mizaj_dominant,
        mizaj_drift_velocity=payload.mizaj_drift_velocity,
        tabiat_reserve_index=payload.tabiat_reserve_index,
        quwwat_hayawaniyyah_index=payload.quwwat_hayawaniyyah_index,
        medication_adherence_pct=payload.medication_adherence_pct,
        active_symptom_severity_delta=payload.active_symptom_severity_delta,
    )

    report = RelapseForecasterEngine.evaluate_relapse_risk(input_data)
    return {
        "forecast_id": report.forecast_id,
        "patient_id": report.patient_id,
        "evaluated_at_utc": report.evaluated_at_utc,
        "relapse_probability_score": report.relapse_probability_score,
        "triage_band": report.triage_band,
        "morbid_humoral_shift_risk": report.morbid_humoral_shift_risk,
        "primary_contributing_factors": report.primary_contributing_factors,
        "proactive_clinical_advisory": report.proactive_clinical_advisory,
        "prophylactic_interventions": report.prophylactic_interventions,
        "requires_clinician_review": report.requires_clinician_review,
        "safe_to_lock": report.safe_to_lock,
    }


@router.get("/patient/{patient_id}/alerts", summary="Get active proactive clinical alerts for patient")
async def get_patient_alerts(patient_id: str):
    alerts = RelapseForecasterEngine.get_patient_alerts(patient_id)
    return [
        {
            "forecast_id": a.forecast_id,
            "evaluated_at_utc": a.evaluated_at_utc,
            "relapse_probability_score": a.relapse_probability_score,
            "triage_band": a.triage_band,
            "morbid_humoral_shift_risk": a.morbid_humoral_shift_risk,
            "proactive_clinical_advisory": a.proactive_clinical_advisory,
            "prophylactic_interventions": a.prophylactic_interventions,
        }
        for a in alerts
    ]
