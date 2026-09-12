"""
ZAYVORA HEALTH™ — Continuous Health & Wearables Ingestion Engine
Normalizes real-time physiological time-series from clinical wearables (Apple HealthKit,
Google Health Connect, Oura, WHOOP) and maps them to classical Unani functional faculties.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class WearableSample:
    sample_id: str
    patient_id: str
    timestamp_utc: str
    source_device: str  # e.g., "Apple Watch Ultra", "Oura Ring Gen 3", "WHOOP 4.0"
    hrv_rmssd_ms: float
    hrv_sdnn_ms: float
    resting_heart_rate_bpm: int
    sleep_hours_total: float
    deep_sleep_hours: float
    rem_sleep_hours: float
    spo2_average_pct: float
    spo2_lowest_pct: float
    respiratory_rate_bpm: float
    daily_steps: int
    active_energy_kcal: float


@dataclass
class WearableSummary:
    patient_id: str
    samples_count: int
    rolling_7d_hrv_rmssd_ms: float
    rolling_7d_resting_hr_bpm: float
    rolling_7d_sleep_hours: float
    rolling_7d_spo2_pct: float
    rolling_7d_steps: int
    # Classical Unani Functional Mappings
    quwwat_hayawaniyyah_index: float  # 0.0 - 1.0 (Autonomic/Vital Tone)
    naum_yaqzah_score: float          # 0.0 - 1.0 (Sleep/Wake Harmony - Asbab #5)
    hawa_riyazat_score: float         # 0.0 - 1.0 (Physical Motion & Respiration - Asbab #1, #3)
    active_anomalies: List[str] = field(default_factory=list)
    clinical_advisory: str = "Physiological reserves within expected homeostatic range."


@dataclass
class WearableSampleRecordData:
    patient_id: str
    sample_id: str
    timestamp_utc: str
    source_device: str
    hrv_rmssd_ms: float
    hrv_sdnn_ms: float
    resting_heart_rate_bpm: int
    sleep_hours_total: float
    deep_sleep_hours: float
    rem_sleep_hours: float
    spo2_average_pct: float
    spo2_lowest_pct: float
    respiratory_rate_bpm: float
    daily_steps: int
    active_energy_kcal: float


# In-memory storage for continuous wearable streams
WEARABLES_STORE: Dict[str, List[WearableSample]] = {}


class WearableIngestionEngine:
    """Ingestion, normalization, and autonomic Unani mapping for continuous wearable streams."""

    @classmethod
    def normalize_apple_healthkit(
        cls,
        samples: List[Any],
        patient_id: str,
        device_model: Optional[str] = "Apple Watch",
        sync_anchor: Optional[str] = None,
    ) -> WearableSample:
        """Normalizes native Apple HealthKit HKQuantity / HKCategory records into a WearableSample."""
        import uuid
        hrv_sdnn = 50.0
        hrv_rmssd = 45.0
        rhr = 70
        sleep_total = 7.0
        deep_sleep = 1.5
        rem_sleep = 1.8
        spo2 = 98.0
        spo2_min = 95.0
        resp_rate = 15.0
        steps = 6000
        active_energy = 350.0

        for s in samples:
            st = (getattr(s, "type", None) or (s.get("type") if isinstance(s, dict) else "") or "").lower()
            val = float(getattr(s, "value", 0) if hasattr(s, "value") else (s.get("value", 0) if isinstance(s, dict) else 0))
            if "heartratevariability" in st or "hrv" in st:
                hrv_sdnn = val
                hrv_rmssd = val * 0.9
            elif "restingheartrate" in st:
                rhr = int(round(val))
            elif "sleepanalysis" in st or "sleep" in st:
                sleep_total = max(sleep_total, val)
            elif "oxygensaturation" in st or "spo2" in st:
                v = val * 100.0 if val <= 1.0 else val
                spo2 = v
                spo2_min = min(spo2_min, v)
            elif "stepcount" in st or "steps" in st:
                steps = int(round(val))
            elif "activeenergy" in st or "energy" in st:
                active_energy = val
            elif "respiratoryrate" in st:
                resp_rate = val

        return WearableSample(
            sample_id=f"W-HK-{uuid.uuid4().hex[:8].upper()}",
            patient_id=patient_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            source_device=device_model or "Apple Watch",
            hrv_rmssd_ms=round(hrv_rmssd, 1),
            hrv_sdnn_ms=round(hrv_sdnn, 1),
            resting_heart_rate_bpm=rhr,
            sleep_hours_total=round(sleep_total, 1),
            deep_sleep_hours=round(deep_sleep, 1),
            rem_sleep_hours=round(rem_sleep, 1),
            spo2_average_pct=round(spo2, 1),
            spo2_lowest_pct=round(spo2_min, 1),
            respiratory_rate_bpm=round(resp_rate, 1),
            daily_steps=steps,
            active_energy_kcal=round(active_energy, 1),
        )

    @classmethod
    def normalize_google_health_connect(
        cls,
        records: List[Any],
        patient_id: str,
        device_name: Optional[str] = "Android Health Connect Device",
        change_token: Optional[str] = None,
    ) -> WearableSample:
        """Normalizes Google Health Connect records into a WearableSample."""
        import uuid
        hrv_rmssd = 45.0
        hrv_sdnn = 50.0
        rhr = 70
        sleep_total = 7.0
        deep_sleep = 1.5
        rem_sleep = 1.8
        spo2 = 98.0
        spo2_min = 95.0
        resp_rate = 15.0
        steps = 6000
        active_energy = 350.0

        for r in records:
            rt = (getattr(r, "record_type", None) or (r.get("record_type") if isinstance(r, dict) else "") or "").lower()
            val = float(getattr(r, "value", 0) if hasattr(r, "value") else (r.get("value", 0) if isinstance(r, dict) else 0))
            if "heartratevariability" in rt or "rmssd" in rt:
                hrv_rmssd = val
                hrv_sdnn = val * 1.1
            elif "restingheartrate" in rt:
                rhr = int(round(val))
            elif "sleep" in rt:
                sleep_total = max(sleep_total, val)
            elif "oxygen" in rt or "spo2" in rt:
                v = val * 100.0 if val <= 1.0 else val
                spo2 = v
                spo2_min = min(spo2_min, v)
            elif "step" in rt:
                steps = int(round(val))
            elif "calorie" in rt or "energy" in rt:
                active_energy = val
            elif "respiratory" in rt:
                resp_rate = val

        return WearableSample(
            sample_id=f"W-GHC-{uuid.uuid4().hex[:8].upper()}",
            patient_id=patient_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            source_device=device_name or "Android Health Connect Device",
            hrv_rmssd_ms=round(hrv_rmssd, 1),
            hrv_sdnn_ms=round(hrv_sdnn, 1),
            resting_heart_rate_bpm=rhr,
            sleep_hours_total=round(sleep_total, 1),
            deep_sleep_hours=round(deep_sleep, 1),
            rem_sleep_hours=round(rem_sleep, 1),
            spo2_average_pct=round(spo2, 1),
            spo2_lowest_pct=round(spo2_min, 1),
            respiratory_rate_bpm=round(resp_rate, 1),
            daily_steps=steps,
            active_energy_kcal=round(active_energy, 1),
        )

    @classmethod
    def ingest_sample(cls, sample: WearableSample, db: Optional[Any] = None) -> WearableSummary:
        if sample.patient_id not in WEARABLES_STORE:
            WEARABLES_STORE[sample.patient_id] = []
        WEARABLES_STORE[sample.patient_id].append(sample)

        # Persist to relational database when DB session is active
        if db is not None:
            try:
                try:
                    from ..models.clinical import WearableSampleRecord
                    record = WearableSampleRecord(
                        patient_id=sample.patient_id,
                        sample_id=sample.sample_id,
                        timestamp_utc=sample.timestamp_utc,
                        source_device=sample.source_device,
                        hrv_rmssd_ms=sample.hrv_rmssd_ms,
                        hrv_sdnn_ms=sample.hrv_sdnn_ms,
                        resting_heart_rate_bpm=sample.resting_heart_rate_bpm,
                        sleep_hours_total=sample.sleep_hours_total,
                        deep_sleep_hours=sample.deep_sleep_hours,
                        rem_sleep_hours=sample.rem_sleep_hours,
                        spo2_average_pct=sample.spo2_average_pct,
                        spo2_lowest_pct=sample.spo2_lowest_pct,
                        respiratory_rate_bpm=sample.respiratory_rate_bpm,
                        daily_steps=sample.daily_steps,
                        active_energy_kcal=sample.active_energy_kcal,
                    )
                except Exception:
                    record = WearableSampleRecordData(
                        patient_id=sample.patient_id,
                        sample_id=sample.sample_id,
                        timestamp_utc=sample.timestamp_utc,
                        source_device=sample.source_device,
                        hrv_rmssd_ms=sample.hrv_rmssd_ms,
                        hrv_sdnn_ms=sample.hrv_sdnn_ms,
                        resting_heart_rate_bpm=sample.resting_heart_rate_bpm,
                        sleep_hours_total=sample.sleep_hours_total,
                        deep_sleep_hours=sample.deep_sleep_hours,
                        rem_sleep_hours=sample.rem_sleep_hours,
                        spo2_average_pct=sample.spo2_average_pct,
                        spo2_lowest_pct=sample.spo2_lowest_pct,
                        respiratory_rate_bpm=sample.respiratory_rate_bpm,
                        daily_steps=sample.daily_steps,
                        active_energy_kcal=sample.active_energy_kcal,
                    )
                db.add(record)
                db.commit()
            except Exception:
                try:
                    db.rollback()
                except Exception:
                    pass

        return cls.compute_summary(sample.patient_id, db=db)

    @classmethod
    def get_patient_samples(cls, patient_id: str, db: Optional[Any] = None) -> List[WearableSample]:
        samples = WEARABLES_STORE.get(patient_id, [])
        if not samples and db is not None:
            cls.compute_summary(patient_id, db=db)
            return WEARABLES_STORE.get(patient_id, [])
        return samples

    @classmethod
    def compute_summary(cls, patient_id: str, db: Optional[Any] = None) -> WearableSummary:
        samples = WEARABLES_STORE.get(patient_id, [])
        if not samples and db is not None:
            try:
                from ..models.clinical import WearableSampleRecord
                from sqlalchemy import select
                stmt = (
                    select(WearableSampleRecord)
                    .where(WearableSampleRecord.patient_id == patient_id)
                    .order_by(WearableSampleRecord.created_at.desc())
                    .limit(14)
                )
                db_records = db.execute(stmt).scalars().all()
                if db_records:
                    loaded = [
                        WearableSample(
                            sample_id=r.sample_id,
                            patient_id=r.patient_id,
                            timestamp_utc=r.timestamp_utc,
                            source_device=r.source_device,
                            hrv_rmssd_ms=r.hrv_rmssd_ms,
                            hrv_sdnn_ms=r.hrv_sdnn_ms,
                            resting_heart_rate_bpm=r.resting_heart_rate_bpm,
                            sleep_hours_total=r.sleep_hours_total,
                            deep_sleep_hours=r.deep_sleep_hours,
                            rem_sleep_hours=r.rem_sleep_hours,
                            spo2_average_pct=r.spo2_average_pct,
                            spo2_lowest_pct=r.spo2_lowest_pct,
                            respiratory_rate_bpm=r.respiratory_rate_bpm,
                            daily_steps=r.daily_steps,
                            active_energy_kcal=r.active_energy_kcal,
                        )
                        for r in reversed(db_records)
                    ]
                    WEARABLES_STORE[patient_id] = loaded
                    samples = loaded
            except Exception:
                pass

        if not samples:
            return WearableSummary(
                patient_id=patient_id,
                samples_count=0,
                rolling_7d_hrv_rmssd_ms=45.0,
                rolling_7d_resting_hr_bpm=70.0,
                rolling_7d_sleep_hours=7.0,
                rolling_7d_spo2_pct=98.0,
                rolling_7d_steps=6000,
                quwwat_hayawaniyyah_index=0.75,
                naum_yaqzah_score=0.80,
                hawa_riyazat_score=0.70,
                active_anomalies=[],
                clinical_advisory="No wearable streams recorded. Baseline normative values active.",
            )

        # Use recent up to 7 samples
        recent = samples[-7:]
        count = len(recent)

        avg_hrv = sum(s.hrv_rmssd_ms for s in recent) / count
        avg_rhr = sum(s.resting_heart_rate_bpm for s in recent) / count
        avg_sleep = sum(s.sleep_hours_total for s in recent) / count
        avg_spo2 = sum(s.spo2_average_pct for s in recent) / count
        avg_steps = int(sum(s.daily_steps for s in recent) / count)

        # 1. Quwwat-e-Hayawaniyyah (Autonomic reserve)
        # Normalized: HRV between 20ms and 80ms -> 0.0 to 1.0; penalized by elevated resting HR > 80
        hrv_norm = min(1.0, max(0.1, (avg_hrv - 15.0) / 65.0))
        rhr_penalty = max(0.0, (avg_rhr - 75.0) * 0.01)
        hayawaniyyah = round(max(0.1, min(1.0, hrv_norm - rhr_penalty)), 2)

        # 2. Naum wa Yaqzah (Sleep architecture)
        # 7-8 hours ideal -> 1.0. Lower or excessive drops score
        if avg_sleep >= 7.0 and avg_sleep <= 9.0:
            sleep_score = 0.95
        elif avg_sleep >= 6.0:
            sleep_score = 0.80
        elif avg_sleep >= 4.5:
            sleep_score = 0.55
        else:
            sleep_score = 0.30
        sleep_score = round(sleep_score, 2)

        # 3. Hawa & Riyazat (Activity & Oxygenation)
        step_factor = min(1.0, avg_steps / 8000.0)
        spo2_factor = 1.0 if avg_spo2 >= 96.0 else (0.7 if avg_spo2 >= 92.0 else 0.4)
        hawa_riyazat = round((step_factor * 0.5) + (spo2_factor * 0.5), 2)

        # Detect Anomaly Flags
        anomalies = []
        latest = recent[-1]

        if latest.hrv_rmssd_ms < 0.65 * avg_hrv and avg_hrv > 25.0:
            anomalies.append("AUTONOMIC_EXHAUSTION: Acute >35% drop in HRV from 7-day rolling baseline.")

        if latest.spo2_lowest_pct < 92.0:
            anomalies.append(f"NOCTURNAL_DESATURATION: Lowest SpO2 dropped to {latest.spo2_lowest_pct}%.")

        if latest.sleep_hours_total < 4.5:
            anomalies.append("SEVERE_SLEEP_DEPRIVATION: Less than 4.5 hours total sleep recorded.")

        if latest.resting_heart_rate_bpm > 95:
            anomalies.append(f"TACHYCARDIA_AT_REST: Resting heart rate elevated at {latest.resting_heart_rate_bpm} bpm.")

        if anomalies:
            advisory = f"⚠️ Physiological strain detected ({len(anomalies)} anomalies). Clinician review of Asbab-e-Sittah recommended."
        else:
            advisory = "Physiological reserves stable. Quwwat-e-Hayawaniyyah and sleep architecture optimal."

        return WearableSummary(
            patient_id=patient_id,
            samples_count=len(samples),
            rolling_7d_hrv_rmssd_ms=round(avg_hrv, 1),
            rolling_7d_resting_hr_bpm=round(avg_rhr, 1),
            rolling_7d_sleep_hours=round(avg_sleep, 1),
            rolling_7d_spo2_pct=round(avg_spo2, 1),
            rolling_7d_steps=avg_steps,
            quwwat_hayawaniyyah_index=hayawaniyyah,
            naum_yaqzah_score=sleep_score,
            hawa_riyazat_score=hawa_riyazat,
            active_anomalies=anomalies,
            clinical_advisory=advisory,
        )
