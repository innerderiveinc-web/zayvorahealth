"""
ZAYVORA HEALTH™ — Wearables & Continuous Health Router
Provides endpoints for continuous physiological data ingestion and 7-day autonomic summaries.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..wearables.wearable_engine import (
    WearableSample,
    WearableIngestionEngine,
    WearableSummary,
)

router = APIRouter(prefix="/api/v1/wearables", tags=["Continuous Wearables & Health Ingestion"])


class IngestSampleRequest(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    source_device: Optional[str] = Field("Apple Watch", description="Wearable device model")
    hrv_rmssd_ms: float = Field(..., description="Root Mean Square of Successive Differences (ms)")
    hrv_sdnn_ms: Optional[float] = Field(50.0, description="Standard Deviation of NN intervals (ms)")
    resting_heart_rate_bpm: int = Field(..., description="Resting heart rate in beats per minute")
    sleep_hours_total: float = Field(..., description="Total sleep duration in hours")
    deep_sleep_hours: Optional[float] = Field(1.5, description="Deep sleep duration in hours")
    rem_sleep_hours: Optional[float] = Field(1.8, description="REM sleep duration in hours")
    spo2_average_pct: float = Field(..., description="Average blood oxygen saturation percentage")
    spo2_lowest_pct: Optional[float] = Field(95.0, description="Lowest nocturnal SpO2 recorded")
    respiratory_rate_bpm: Optional[float] = Field(15.0, description="Sleeping respiratory rate")
    daily_steps: int = Field(..., description="Total daily step count")
    active_energy_kcal: Optional[float] = Field(350.0, description="Active calorie expenditure")


@router.post("/ingest", summary="Ingest time-series wearable sample block")
async def ingest_wearable_sample(payload: IngestSampleRequest, db: Session = Depends(get_db)):
    sample = WearableSample(
        sample_id=f"W-SMP-{uuid.uuid4().hex[:8].upper()}",
        patient_id=payload.patient_id,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        source_device=payload.source_device or "Wearable Device",
        hrv_rmssd_ms=payload.hrv_rmssd_ms,
        hrv_sdnn_ms=payload.hrv_sdnn_ms or 50.0,
        resting_heart_rate_bpm=payload.resting_heart_rate_bpm,
        sleep_hours_total=payload.sleep_hours_total,
        deep_sleep_hours=payload.deep_sleep_hours or 1.5,
        rem_sleep_hours=payload.rem_sleep_hours or 1.8,
        spo2_average_pct=payload.spo2_average_pct,
        spo2_lowest_pct=payload.spo2_lowest_pct or 95.0,
        respiratory_rate_bpm=payload.respiratory_rate_bpm or 15.0,
        daily_steps=payload.daily_steps,
        active_energy_kcal=payload.active_energy_kcal or 350.0,
    )

    summary = WearableIngestionEngine.ingest_sample(sample, db=db)
    return {
        "sample_id": sample.sample_id,
        "patient_id": sample.patient_id,
        "summary": {
            "samples_count": summary.samples_count,
            "rolling_7d_hrv_rmssd_ms": summary.rolling_7d_hrv_rmssd_ms,
            "rolling_7d_resting_hr_bpm": summary.rolling_7d_resting_hr_bpm,
            "rolling_7d_sleep_hours": summary.rolling_7d_sleep_hours,
            "rolling_7d_spo2_pct": summary.rolling_7d_spo2_pct,
            "rolling_7d_steps": summary.rolling_7d_steps,
            "quwwat_hayawaniyyah_index": summary.quwwat_hayawaniyyah_index,
            "naum_yaqzah_score": summary.naum_yaqzah_score,
            "hawa_riyazat_score": summary.hawa_riyazat_score,
            "active_anomalies": summary.active_anomalies,
            "clinical_advisory": summary.clinical_advisory,
        },
    }


@router.get("/patient/{patient_id}/summary", summary="Get 7-day rolling physiological baseline and anomalies")
async def get_patient_wearable_summary(patient_id: str, db: Session = Depends(get_db)):
    summary = WearableIngestionEngine.compute_summary(patient_id, db=db)
    return {
        "patient_id": summary.patient_id,
        "samples_count": summary.samples_count,
        "rolling_7d_hrv_rmssd_ms": summary.rolling_7d_hrv_rmssd_ms,
        "rolling_7d_resting_hr_bpm": summary.rolling_7d_resting_hr_bpm,
        "rolling_7d_sleep_hours": summary.rolling_7d_sleep_hours,
        "rolling_7d_spo2_pct": summary.rolling_7d_spo2_pct,
        "rolling_7d_steps": summary.rolling_7d_steps,
        "quwwat_hayawaniyyah_index": summary.quwwat_hayawaniyyah_index,
        "naum_yaqzah_score": summary.naum_yaqzah_score,
        "hawa_riyazat_score": summary.hawa_riyazat_score,
        "active_anomalies": summary.active_anomalies,
        "clinical_advisory": summary.clinical_advisory,
    }


# =====================================================================
# Issue ENH-01: Direct Wearable Hardware Webhooks
# Apple HealthKit & Google Health Connect Synchronization Receivers
# =====================================================================

class AppleHealthKitSample(BaseModel):
    type: str = Field(..., description="HKQuantityTypeIdentifier or HKCategoryTypeIdentifier")
    value: float = Field(..., description="Numeric value recorded")
    unit: Optional[str] = Field("count", description="Unit of measurement (ms, count/min, %, kcal, count, hr)")
    startDate: Optional[str] = Field(None, description="Start timestamp in ISO-8601")
    endDate: Optional[str] = Field(None, description="End timestamp in ISO-8601")


class AppleHealthKitWebhookPayload(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    device_model: Optional[str] = Field("Apple Watch", description="Specific Apple hardware model")
    sync_anchor: Optional[str] = Field(None, description="HealthKit background delivery sync anchor")
    samples: List[AppleHealthKitSample] = Field(..., description="Array of HKQuantity samples")


class GoogleHealthConnectRecord(BaseModel):
    record_type: str = Field(..., description="Health Connect Record Type")
    value: float = Field(..., description="Measurement value")
    start_time: Optional[str] = Field(None, description="Start timestamp ISO-8601")
    end_time: Optional[str] = Field(None, description="End timestamp ISO-8601")


class GoogleHealthConnectWebhookPayload(BaseModel):
    patient_id: str = Field(..., description="UUID of the patient")
    device_name: Optional[str] = Field("Android Health Connect Device", description="Originating client device")
    change_token: Optional[str] = Field(None, description="Health Connect sync change token")
    records: List[GoogleHealthConnectRecord] = Field(..., description="Array of Health Connect records")


@router.post("/webhooks/apple-healthkit", summary="Direct webhook receiver for Apple HealthKit background delivery (Issue ENH-01)")
async def apple_healthkit_webhook(payload: AppleHealthKitWebhookPayload, db: Session = Depends(get_db)):
    """
    Receives native Apple HealthKit background delivery payloads, normalizes HKQuantity types,
    and updates the patient's Unani autonomic functional reserves.
    """
    if not payload.samples:
        raise HTTPException(status_code=400, detail="Empty Apple HealthKit sample collection")

    sample = WearableIngestionEngine.normalize_apple_healthkit(
        samples=payload.samples,
        patient_id=payload.patient_id,
        device_model=payload.device_model,
        sync_anchor=payload.sync_anchor,
    )

    summary = WearableIngestionEngine.ingest_sample(sample, db=db)
    return {
        "status": "PROCESSED",
        "platform": "APPLE_HEALTHKIT",
        "patient_id": payload.patient_id,
        "sample_id": sample.sample_id,
        "sync_anchor": payload.sync_anchor,
        "items_aggregated": len(payload.samples),
        "unani_autonomic_reserves": {
            "quwwat_hayawaniyyah_index": summary.quwwat_hayawaniyyah_index,
            "naum_yaqzah_score": summary.naum_yaqzah_score,
            "hawa_riyazat_score": summary.hawa_riyazat_score,
        },
        "active_anomalies": summary.active_anomalies,
        "clinical_advisory": summary.clinical_advisory,
    }


@router.post("/webhooks/google-health-connect", summary="Direct webhook receiver for Google Health Connect sync (Issue ENH-01)")
async def google_health_connect_webhook(payload: GoogleHealthConnectWebhookPayload, db: Session = Depends(get_db)):
    """
    Receives Google Health Connect sync records, extracts physiological markers,
    and updates the continuous Unani health balance indices.
    """
    if not payload.records:
        raise HTTPException(status_code=400, detail="Empty Google Health Connect record collection")

    sample = WearableIngestionEngine.normalize_google_health_connect(
        records=payload.records,
        patient_id=payload.patient_id,
        device_name=payload.device_name,
        change_token=payload.change_token,
    )

    summary = WearableIngestionEngine.ingest_sample(sample, db=db)
    return {
        "status": "PROCESSED",
        "platform": "GOOGLE_HEALTH_CONNECT",
        "patient_id": payload.patient_id,
        "sample_id": sample.sample_id,
        "change_token": payload.change_token,
        "records_aggregated": len(payload.records),
        "unani_autonomic_reserves": {
            "quwwat_hayawaniyyah_index": summary.quwwat_hayawaniyyah_index,
            "naum_yaqzah_score": summary.naum_yaqzah_score,
            "hawa_riyazat_score": summary.hawa_riyazat_score,
        },
        "active_anomalies": summary.active_anomalies,
        "clinical_advisory": summary.clinical_advisory,
    }


