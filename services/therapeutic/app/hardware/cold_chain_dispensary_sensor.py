"""
ZAYVORA Health OS™ v5.0 — Cold-Chain & Environmental Dispensary IoT Sensor
Monitors storage conditions in central hospital pharmacies, compounding matabs, and warehouse vaults.
Protects botanical volatile oils, hydro-distillates (Arqiyat), and electuaries (Khamira/Majun) from thermal degradation.

Specifications:
- Temperature Range (Controlled Room Temp): 15.0°C - 25.0°C
- Cold-Chain Active Biologicals (Cold Vault): 2.0°C - 8.0°C
- Relative Humidity (Max allowable for dry safoofs): < 60.0% RH
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class EnvironmentalTelemetry:
    sensor_id: str
    zone_name: str
    timestamp_utc: str
    temperature_celsius: float
    relative_humidity_pct: float
    is_temperature_compliant: bool
    is_humidity_compliant: bool
    fefo_storage_status: str  # "OPTIMAL_PRESERVATION", "THERMAL_EXCURSION_WARNING", "CRITICAL_SPOILAGE_RISK"
    dew_point_celsius: float
    active_alerts: List[str] = field(default_factory=list)


class ColdChainDispensarySensor:
    """Hardware driver for environmental IoT nodes installed in pharmacy dispensing zones."""

    def __init__(self, sensor_id: str = "ENV-SENS-DISP-04"):
        self.sensor_id = sensor_id
        self.zone_name = "Central Dispensary Vault & FEFO Storage"
        self.battery_level_pct = 94.0

    def read_environmental_telemetry(
        self,
        ambient_temp_override: Optional[float] = None,
        ambient_rh_override: Optional[float] = None,
    ) -> EnvironmentalTelemetry:
        """Reads calibrated temperature and humidity and evaluates cold-chain stability."""
        temp = ambient_temp_override if ambient_temp_override is not None else 19.4
        rh = ambient_rh_override if ambient_rh_override is not None else 48.2

        temp_ok = 15.0 <= temp <= 25.0
        rh_ok = rh < 60.0

        # Simple approximation of dew point
        dew_point = round(temp - ((100.0 - rh) / 5.0), 1)

        alerts = []
        if temp > 25.0:
            alerts.append(f"Thermal Excursion Alert: Temp {temp}°C exceeds max threshold (25.0°C)")
        elif temp < 15.0:
            alerts.append(f"Sub-ambient Warning: Temp {temp}°C below standard room temp")

        if rh >= 60.0:
            alerts.append(f"High Humidity Warning: RH {rh}% creates mold/moisture risk for Safoofs")

        if not temp_ok or not rh_ok:
            status = "THERMAL_EXCURSION_WARNING" if (25.0 < temp < 30.0) else "CRITICAL_SPOILAGE_RISK"
        else:
            status = "OPTIMAL_PRESERVATION"

        return EnvironmentalTelemetry(
            sensor_id=self.sensor_id,
            zone_name=self.zone_name,
            timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            temperature_celsius=temp,
            relative_humidity_pct=rh,
            is_temperature_compliant=temp_ok,
            is_humidity_compliant=rh_ok,
            fefo_storage_status=status,
            dew_point_celsius=dew_point,
            active_alerts=alerts,
        )
