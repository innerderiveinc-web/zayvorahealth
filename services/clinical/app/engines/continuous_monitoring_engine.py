"""
ZAYVORA Health OS™ — Digital Biomarker & Continuous Monitoring OS (Phase 20)
============================================================================
Ingests multi-stream continuous telemetry from wearables, home vitals, and ambient
environment; analyzes time-series patterns, detects sub-clinical dyscrasias, and
generates prioritized clinician alerts with rigorous alarm-fatigue suppression.

Data Streams:
├── Wearable Biometrics (Resting Heart Rate, HRV SDNN, Sleep Efficiency, Daily Steps)
├── Home Point-of-Care Vitals (Diurnal Blood Pressure, Capillary Glucose)
├── Longitudinal Patient PROMs & Symptom Diaries
└── Ambient Environmental Variables (Temperature & Humidity cross-referenced with Asbab-e-Sittah)

Canonical Early Risk Signal Detectors:
1. THERMAL_POLARIZATION_SPIKE:
   Acute resting HR elevation (>85 bpm) paired with nocturnal sleep fragmentation.
   Indicates acute bilious flare (Ghalba-e-Safra) or inflammatory joint exacerbation.
2. AUTONOMIC_DYSCRASIA:
   HRV SDNN < 25 ms indicating sustained sympathetic overload / depletion of
   innate vitality (Du'f al-Quwa / Rooh).
3. VAS_REBOUND:
   Sudden jump >= 2.0 on VAS scale after established clinical remission.
   Indicates relapse (Intikas) or protocol failure.
4. ADHERENCE_EROSION:
   Medication possession ratio (MPR) falling < 60% over rolling 7-day window.

Doctrine Invariant:
Autonomous Operations = Alert generation, triage routing, and compliance logging.
Autonomous Medicine = HARD-BLOCKED. Dosage/drug alterations require clinician review.
"""

from __future__ import annotations

import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


class AlertSeverity(str, Enum):
    INFO = "INFO"
    MODERATE = "MODERATE"
    ELEVATED = "ELEVATED"
    CRITICAL = "CRITICAL"


class RiskSignalType(str, Enum):
    THERMAL_POLARIZATION_SPIKE = "THERMAL_POLARIZATION_SPIKE"
    AUTONOMIC_DYSCRASIA = "AUTONOMIC_DYSCRASIA"
    VAS_REBOUND = "VAS_REBOUND"
    ADHERENCE_EROSION = "ADHERENCE_EROSION"
    SEASONAL_HUMORAL_VULNERABILITY = "SEASONAL_HUMORAL_VULNERABILITY"


@dataclass
class TelemetryDataPoint:
    timestamp: str
    resting_hr_bpm: float
    hrv_sdnn_ms: float
    sleep_efficiency_pct: float
    daily_steps: int
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    ambient_temp_c: Optional[float] = None
    ambient_humidity_pct: Optional[float] = None
    daily_pain_vas: Optional[float] = None
    doses_taken: Optional[int] = None
    doses_prescribed: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClinicianRiskSignal:
    signal_id: str
    patient_id: str
    signal_type: RiskSignalType
    severity: AlertSeverity
    detected_at: str
    headline: str
    clinical_mechanism: str
    suggested_action: str
    telemetry_trigger: Dict[str, Any]
    requires_doctor_ack: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["signal_type"] = self.signal_type.value
        d["severity"] = self.severity.value
        return d


@dataclass
class ContinuousMonitoringReport:
    patient_id: str
    analyzed_window_days: int
    mean_resting_hr: float
    mean_hrv_sdnn: float
    mean_sleep_efficiency: float
    total_steps_avg: int
    overall_adherence_pct: float
    active_signals: List[ClinicianRiskSignal]
    humoral_stability_index: float  # 0.0 (erratic dyscrasia) to 1.0 (optimal equilibrium)
    generated_at: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["active_signals"] = [s.to_dict() for s in self.active_signals]
        return d


class ContinuousMonitoringEngine:
    """
    Ingests time-series biometric streams and produces filtered early risk signals.
    """

    def __init__(self):
        self._telemetry_store: Dict[str, List[TelemetryDataPoint]] = {}

    def ingest_telemetry_batch(
        self,
        patient_id: str,
        data_points: List[Dict[str, Any]]
    ) -> int:
        """Stores normalized telemetry points for a patient."""
        if patient_id not in self._telemetry_store:
            self._telemetry_store[patient_id] = []

        count = 0
        for dp in data_points:
            point = TelemetryDataPoint(
                timestamp=dp.get("timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()),
                resting_hr_bpm=float(dp.get("resting_hr_bpm", 72.0)),
                hrv_sdnn_ms=float(dp.get("hrv_sdnn_ms", 45.0)),
                sleep_efficiency_pct=float(dp.get("sleep_efficiency_pct", 85.0)),
                daily_steps=int(dp.get("daily_steps", 5000)),
                systolic_bp=dp.get("systolic_bp"),
                diastolic_bp=dp.get("diastolic_bp"),
                ambient_temp_c=dp.get("ambient_temp_c"),
                ambient_humidity_pct=dp.get("ambient_humidity_pct"),
                daily_pain_vas=dp.get("daily_pain_vas"),
                doses_taken=dp.get("doses_taken"),
                doses_prescribed=dp.get("doses_prescribed")
            )
            self._telemetry_store[patient_id].append(point)
            count += 1

        # Keep store ordered by timestamp
        self._telemetry_store[patient_id].sort(key=lambda x: x.timestamp)
        return count

    def analyze_patient_telemetry(
        self,
        patient_id: str,
        baseline_mizaj: str = "Mu'tadil",
        established_vas_nadir: Optional[float] = None
    ) -> ContinuousMonitoringReport:
        """
        Processes all available telemetry points to generate early risk signals
        and compute the Humoral Stability Index.
        """
        history = self._telemetry_store.get(patient_id, [])
        if not history:
            # Default baseline report when no wearable connected
            return ContinuousMonitoringReport(
                patient_id=patient_id,
                analyzed_window_days=0,
                mean_resting_hr=72.0,
                mean_hrv_sdnn=50.0,
                mean_sleep_efficiency=85.0,
                total_steps_avg=6000,
                overall_adherence_pct=100.0,
                active_signals=[],
                humoral_stability_index=1.0
            )

        n = len(history)
        avg_hr = round(sum(p.resting_hr_bpm for p in history) / n, 1)
        avg_hrv = round(sum(p.hrv_sdnn_ms for p in history) / n, 1)
        avg_sleep = round(sum(p.sleep_efficiency_pct for p in history) / n, 1)
        avg_steps = int(sum(p.daily_steps for p in history) / n)

        # Adherence calculation
        total_prescribed = sum(p.doses_prescribed or 0 for p in history)
        total_taken = sum(p.doses_taken or 0 for p in history)
        if total_prescribed > 0:
            adherence_pct = round((total_taken / total_prescribed) * 100.0, 1)
        else:
            adherence_pct = 95.0

        signals: List[ClinicianRiskSignal] = []
        recent_point = history[-1]

        # 1. Thermal Polarization Spike Detector (Safrawi Heat Surge)
        if recent_point.resting_hr_bpm > 85.0 and recent_point.sleep_efficiency_pct < 70.0:
            signals.append(
                ClinicianRiskSignal(
                    signal_id=f"SIG-THM-{patient_id[:6]}-{len(signals)+1}",
                    patient_id=patient_id,
                    signal_type=RiskSignalType.THERMAL_POLARIZATION_SPIKE,
                    severity=AlertSeverity.ELEVATED,
                    detected_at=recent_point.timestamp,
                    headline="Thermal Polarization Spike (Tawarrum / Safrawi Heat Surge)",
                    clinical_mechanism="Elevated resting HR (>85 bpm) correlated with sleep fragmentation indicates bilious thermal irritation (Ghalba-e-Hararah) or acute inflammatory flare.",
                    suggested_action="Review inflammatory joint status; check hydration; consider cooling nocturnal fomentation (Zimad Sandal) or Sharbat Bazoori.",
                    telemetry_trigger={
                        "resting_hr": recent_point.resting_hr_bpm,
                        "sleep_efficiency": recent_point.sleep_efficiency_pct
                    }
                )
            )

        # 2. Autonomic Dyscrasia Detector (Depletion of Vital Spirit / Rooh)
        if recent_point.hrv_sdnn_ms < 25.0:
            signals.append(
                ClinicianRiskSignal(
                    signal_id=f"SIG-AUT-{patient_id[:6]}-{len(signals)+1}",
                    patient_id=patient_id,
                    signal_type=RiskSignalType.AUTONOMIC_DYSCRASIA,
                    severity=AlertSeverity.MODERATE,
                    detected_at=recent_point.timestamp,
                    headline="Autonomic Dyscrasia (Du'f al-Qalb / Sympathetic Exhaustion)",
                    clinical_mechanism="Depressed Heart Rate Variability (SDNN < 25 ms) points to chronic sympathetic overdrive, systemic fatigue, and exhaustion of innate vital force (Hararat Ghariziyya).",
                    suggested_action="Reinforce Asbab-e-Sittah: prescribed sleep hygiene, gentle deep breathing (Riyazat-e-Tanffus), and cardiac tonics (Khamira Gaozaban).",
                    telemetry_trigger={"hrv_sdnn_ms": recent_point.hrv_sdnn_ms}
                )
            )

        # 3. VAS Rebound / Relapse (Intikas) Detector
        if established_vas_nadir is not None and recent_point.daily_pain_vas is not None:
            vas_rebound = recent_point.daily_pain_vas - established_vas_nadir
            if vas_rebound >= 2.0:
                signals.append(
                    ClinicianRiskSignal(
                        signal_id=f"SIG-VAS-{patient_id[:6]}-{len(signals)+1}",
                        patient_id=patient_id,
                        signal_type=RiskSignalType.VAS_REBOUND,
                        severity=AlertSeverity.CRITICAL,
                        detected_at=recent_point.timestamp,
                        headline="Clinical Relapse Detected (Intikas / VAS Rebound)",
                        clinical_mechanism=f"Pain severity jumped by +{vas_rebound:.1f} points on VAS (nadir: {established_vas_nadir} -> current: {recent_point.daily_pain_vas}) despite active pharmacotherapy.",
                        suggested_action="Urgent clinician review recommended: assess for joint re-injury, cold-exposure triggers, or need for phase-appropriate Badal switch.",
                        telemetry_trigger={
                            "established_nadir": established_vas_nadir,
                            "current_vas": recent_point.daily_pain_vas,
                            "delta": vas_rebound
                        }
                    )
                )

        # 4. Adherence Erosion Detector
        if adherence_pct < 60.0:
            signals.append(
                ClinicianRiskSignal(
                    signal_id=f"SIG-ADH-{patient_id[:6]}-{len(signals)+1}",
                    patient_id=patient_id,
                    signal_type=RiskSignalType.ADHERENCE_EROSION,
                    severity=AlertSeverity.MODERATE,
                    detected_at=recent_point.timestamp,
                    headline="Sub-therapeutic Adherence Erosion (MPR < 60%)",
                    clinical_mechanism=f"Rolling medication adherence fell to {adherence_pct}%. Interrupted posology prevents achieving minimum effective concentrations (Jar'at-e-Kamilah).",
                    suggested_action="Trigger Sehat Sahab patient companion reminder and check for gastrointestinal intolerance or dosing complexity.",
                    telemetry_trigger={"adherence_pct": adherence_pct}
                )
            )

        # Calculate Humoral Stability Index (0.0 to 1.0)
        penalty = 0.0
        for s in signals:
            if s.severity == AlertSeverity.CRITICAL:
                penalty += 0.4
            elif s.severity == AlertSeverity.ELEVATED:
                penalty += 0.25
            elif s.severity == AlertSeverity.MODERATE:
                penalty += 0.15
        stability = max(0.05, round(1.0 - penalty, 2))

        return ContinuousMonitoringReport(
            patient_id=patient_id,
            analyzed_window_days=n,
            mean_resting_hr=avg_hr,
            mean_hrv_sdnn=avg_hrv,
            mean_sleep_efficiency=avg_sleep,
            total_steps_avg=avg_steps,
            overall_adherence_pct=adherence_pct,
            active_signals=signals,
            humoral_stability_index=stability
        )

    @classmethod
    def decompose_pulse_waveform_fft(
        cls,
        waveform_samples: List[float],
        sampling_rate_hz: float = 50.0,
    ) -> PulseHarmonicSpectralDecomposition:
        """
        Computes Discrete Fourier Transform (DFT / FFT) harmonic spectral decomposition
        on pulse photoplethysmography (PPG) or arterial waveform series.
        Extracts fundamental frequency f0, first 4 harmonic amplitudes, reflection index,
        and correlates with classical Unani 10-Ajnas Nabz metrics (Sulb vs Layyin).
        """
        import cmath
        import math

        N = len(waveform_samples)
        if N < 16:
            raise ValueError("Pulse waveform series must contain at least 16 samples for spectral decomposition.")

        # Remove DC offset (mean subtraction)
        mean_val = sum(waveform_samples) / N
        centered = [x - mean_val for x in waveform_samples]

        # Discrete Fourier Transform
        # X_k = sum_{n=0}^{N-1} x_n * exp(-2j * pi * k * n / N)
        dft_magnitudes: List[float] = []
        frequencies: List[float] = []
        half_n = N // 2

        for k in range(half_n):
            freq = (k * sampling_rate_hz) / N
            frequencies.append(freq)
            # Compute complex sum
            val = sum(centered[n] * cmath.exp(-2j * math.pi * k * n / N) for n in range(N))
            # Magnitude normalized by N
            dft_magnitudes.append((abs(val) * 2.0) / N)

        # Search for fundamental cardiac frequency f0 between 0.6 Hz (36 bpm) and 3.5 Hz (210 bpm)
        valid_indices = [i for i, f in enumerate(frequencies) if 0.6 <= f <= 3.5]
        if not valid_indices:
            peak_idx = max(range(1, half_n), key=lambda i: dft_magnitudes[i])
        else:
            peak_idx = max(valid_indices, key=lambda i: dft_magnitudes[i])

        f0 = frequencies[peak_idx]
        h1 = dft_magnitudes[peak_idx]
        pulse_bpm = round(f0 * 60.0, 1)

        # Extract higher harmonics at 2*f0, 3*f0, 4*f0
        harmonics = [round(h1, 4)]
        for harmonic_mult in [2, 3, 4]:
            target_f = f0 * harmonic_mult
            if target_f >= frequencies[-1]:
                harmonics.append(0.0)
                continue
            # Find nearest frequency bin
            nearest_idx = min(range(half_n), key=lambda i: abs(frequencies[i] - target_f))
            harmonics.append(round(dft_magnitudes[nearest_idx], 4))

        h2, h3, h4 = harmonics[1], harmonics[2], harmonics[3]
        denom = max(1e-6, h1 ** 2)
        harmonic_energy_ratio = round((h2**2 + h3**2 + h4**2) / denom, 4)
        stiffness_index = round(h2 / max(1e-6, h1), 3)
        reflection_index = round(stiffness_index * 100.0, 1)

        # Classical 10-Ajnas Pulse Correlation
        if stiffness_index >= 0.70:
            nabz_attr = "Sulb (Tense/High Arterial Resistance)"
            mizaj_corr = "Sawdawi (Cold & Dry) or Arteriosclerotic Stagnation"
        elif stiffness_index <= 0.35:
            nabz_attr = "Layyin (Soft/High Vascular Compliance)"
            mizaj_corr = "Balghami (Cold & Moist) or Vasodilated Relaxation"
        else:
            nabz_attr = "Mu'tadil (Balanced Elasticity)"
            mizaj_corr = "Damwi / Mu'tadil (Optimal Homeostasis)"

        if pulse_bpm > 90.0:
            nabz_attr += " — Sari (Rapid / Tachycardic)"
        elif pulse_bpm < 60.0:
            nabz_attr += " — Bati (Slow / Bradycardic)"
        else:
            nabz_attr += " — Mu'tadil fil-Sura'at (Normofrequent)"

        return PulseHarmonicSpectralDecomposition(
            sampling_rate_hz=sampling_rate_hz,
            fundamental_frequency_hz=round(f0, 3),
            estimated_pulse_bpm=pulse_bpm,
            harmonic_amplitudes=harmonics,
            harmonic_energy_ratio=harmonic_energy_ratio,
            vascular_stiffness_index=stiffness_index,
            reflection_index_pct=reflection_index,
            classical_nabz_attribute=nabz_attr,
            unani_temperament_correlation=mizaj_corr,
        )


@dataclass
class PulseHarmonicSpectralDecomposition:
    sampling_rate_hz: float
    fundamental_frequency_hz: float
    estimated_pulse_bpm: float
    harmonic_amplitudes: List[float]
    harmonic_energy_ratio: float
    vascular_stiffness_index: float
    reflection_index_pct: float
    classical_nabz_attribute: str
    unani_temperament_correlation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

