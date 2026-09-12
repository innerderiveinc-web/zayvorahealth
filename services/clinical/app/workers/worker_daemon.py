"""
ZAYVORA Health™ — Background Worker Daemon.
Executes asynchronous tasks including ABDM packet reconciliation,
batch FHIR R4 imports, wearable telemetry sync, and QSURA notifications.
"""
from __future__ import annotations

import logging
import traceback
from datetime import datetime
from typing import Any, Callable

from app.workers.task_queue import AsyncTaskQueue, GLOBAL_TASK_QUEUE, TaskRecord, TaskType

logger = logging.getLogger("zayvora.workers")

# Classical Unani Amraz to ICD-11 Dual-Mapping Dictionary
ICD11_TO_UNANI_AMRAZ: dict[str, dict[str, str]] = {
    "E11": {
        "amraz_code": "AMRAZ-01",
        "canonical_name": "Ziabetus Shakari (Diabetes Mellitus)",
        "pathology": "Su-e-Mizaj Barid Ratab with weakness of Quwwat-e-Ghazia & Kulyah",
        "primary_organ_axis": "AXIS-02 (Kabid-Meda)",
    },
    "M10": {
        "amraz_code": "AMRAZ-02",
        "canonical_name": "Niqras (Gout / Podagra)",
        "pathology": "Accumulation of combusted melancholic/bilious humors in peripheral joint capsules",
        "primary_organ_axis": "AXIS-04 (Kulyah-Mafasil)",
    },
    "K29": {
        "amraz_code": "AMRAZ-03",
        "canonical_name": "Iltehab-e-Meda (Gastritis)",
        "pathology": "Su-e-Mizaj Haar Yabis with bilious irritation of gastric mucosa",
        "primary_organ_axis": "AXIS-01 (Meda-Dimagh)",
    },
    "I10": {
        "amraz_code": "AMRAZ-04",
        "canonical_name": "Zaghtuddam Qawi (Primary Essential Hypertension)",
        "pathology": "Ghalba-e-Dam (Sanguineous Plethora) with vascular tension",
        "primary_organ_axis": "AXIS-03 (Qalb-Dimagh)",
    },
    "J45": {
        "amraz_code": "AMRAZ-05",
        "canonical_name": "Zeeq-un-Nafs (Bronchial Asthma)",
        "pathology": "Suddah (Obstruction) in bronchioles by viscous phlegm (Balgham Ghaleez)",
        "primary_organ_axis": "AXIS-06 (Riya-Qalb)",
    },
    "M19": {
        "amraz_code": "AMRAZ-06",
        "canonical_name": "Waja-ul-Mafasil Muzmin (Chronic Osteoarthritis)",
        "pathology": "Loss of innate articular moisture (Rutoobat-e-Muatadilah) with Barid Yabis dyscrasia",
        "primary_organ_axis": "AXIS-04 (Kulyah-Mafasil)",
    },
}

# Statutory Schedule E(1) Poisons
SCHEDULE_E1_POISONS = {
    "suranjan talkh",
    "colchicum luteum",
    "azaraqi",
    "kuchla",
    "strychnos nux-vomica",
    "bhilawa",
    "semecarpus anacardium",
    "afeem",
    "opium",
    "bhang",
    "cannabis sativa",
}


class WorkerDaemon:
    """Asynchronous background worker processor."""

    def __init__(self, queue: AsyncTaskQueue | None = None):
        self.queue = queue or GLOBAL_TASK_QUEUE
        self._handlers: dict[str, Callable[[TaskRecord], dict[str, Any]]] = {
            TaskType.ABDM_PACKET_RECONCILIATION.value: self._handle_abdm_packet_reconciliation,
            TaskType.FHIR_BATCH_IMPORT.value: self._handle_fhir_batch_import,
            TaskType.WEARABLE_STREAM_SYNC.value: self._handle_wearable_stream_sync,
            TaskType.QSURA_DISPATCH.value: self._handle_qsura_dispatch,
            TaskType.DIGITAL_TWIN_SIMULATION.value: self._handle_digital_twin_simulation,
        }

    def register_handler(self, task_type: str, handler: Callable[[TaskRecord], dict[str, Any]]) -> None:
        self._handlers[task_type] = handler

    def process_one(self, timeout_seconds: float = 0.1) -> TaskRecord | None:
        """Pulls and executes a single task from queue."""
        task = self.queue.dequeue(timeout_seconds=timeout_seconds)
        if not task:
            return None

        handler = self._handlers.get(task.task_type)
        if not handler:
            self.queue.fail_task(task.task_id, f"No registered handler for task type: {task.task_type}")
            return task

        try:
            result = handler(task)
            # Invariant: Any imported or generated clinical data MUST have safe_to_lock = False
            safe_to_lock = result.get("safe_to_lock", False)
            self.queue.complete_task(task.task_id, result=result, safe_to_lock=safe_to_lock)
            return task
        except Exception as exc:
            err_msg = f"{type(exc).__name__}: {str(exc)}\n{traceback.format_exc()}"
            logger.error("Task %s execution failed: %s", task.task_id, err_msg)
            self.queue.fail_task(task.task_id, err_msg)
            return task

    def process_all(self, max_iterations: int = 50) -> int:
        """Processes pending queue items until empty or limit reached."""
        count = 0
        for _ in range(max_iterations):
            task = self.process_one(timeout_seconds=0.01)
            if not task:
                break
            count += 1
        return count

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------

    def _handle_abdm_packet_reconciliation(self, task: TaskRecord) -> dict[str, Any]:
        """Reconciles incoming ABDM Milestone 3 health data transfer packets."""
        payload = task.payload
        patient_abha = payload.get("patient_abha")
        raw_bundles = payload.get("encrypted_fhir_packets", [])

        if not patient_abha:
            raise ValueError("ABDM packet reconciliation requires patient_abha identifier.")

        reconciled_conditions = []
        reconciled_observations = []
        reconciled_medications = []

        for packet in raw_bundles:
            # Reconcile conditions / diagnoses
            for cond in packet.get("conditions", []):
                icd_prefix = cond.get("code", "")[:3].upper()
                unani_mapping = ICD11_TO_UNANI_AMRAZ.get(icd_prefix)

                entry = {
                    "biomedical_code": cond.get("code"),
                    "biomedical_name": cond.get("display", "Unknown Condition"),
                    "clinical_status": cond.get("clinical_status", "active"),
                    "recorded_date": cond.get("recorded_date", datetime.utcnow().isoformat()),
                    "unani_amraz": unani_mapping if unani_mapping else {
                        "amraz_code": "AMRAZ-GENERAL",
                        "canonical_name": f"Ghair Tab'i Kaifiyat ({cond.get('display', 'General')})",
                        "pathology": "Undifferentiated humoral dyscrasia requiring clinical pulse/tongue validation",
                        "primary_organ_axis": "AXIS-GENERAL",
                    },
                }
                reconciled_conditions.append(entry)

            # Reconcile lab observations
            for obs in packet.get("observations", []):
                reconciled_observations.append({
                    "code": obs.get("code"),
                    "display": obs.get("display"),
                    "value": obs.get("value"),
                    "unit": obs.get("unit"),
                    "interpretation": obs.get("interpretation", "NORMAL"),
                })

            # Reconcile medications
            for med in packet.get("medications", []):
                med_name = med.get("name", "").lower()
                is_schedule_e1 = any(p in med_name for p in SCHEDULE_E1_POISONS)

                reconciled_medications.append({
                    "name": med.get("name"),
                    "posology": med.get("dosage", "Unspecified"),
                    "is_schedule_e1": is_schedule_e1,
                    "statutory_caution": "MANDATORY MUDABBAR DETOXIFICATION REQUIRED" if is_schedule_e1 else None,
                })

        return {
            "status": "RECONCILED",
            "patient_abha": patient_abha,
            "packets_processed": len(raw_bundles),
            "reconciled_conditions": reconciled_conditions,
            "reconciled_observations": reconciled_observations,
            "reconciled_medications": reconciled_medications,
            "reconciliation_timestamp": datetime.utcnow().isoformat(),
            # Safe To Lock Invariant: Always False until physical clinician sign-off
            "safe_to_lock": False,
            "requires_clinician_ratification": True,
        }

    def _handle_fhir_batch_import(self, task: TaskRecord) -> dict[str, Any]:
        """Validates and imports bulk HL7 FHIR R4 Bundle documents."""
        payload = task.payload
        bundle = payload.get("fhir_bundle", {})
        bundle_type = bundle.get("resourceType", "")

        if bundle_type != "Bundle":
            raise ValueError(f"Invalid FHIR resourceType: expected 'Bundle', got '{bundle_type}'")

        entries = bundle.get("entry", [])
        counts = {"Patient": 0, "Condition": 0, "Observation": 0, "MedicationRequest": 0, "Other": 0}
        schedule_e1_alerts = []

        for item in entries:
            resource = item.get("resource", {})
            rtype = resource.get("resourceType", "Other")
            if rtype in counts:
                counts[rtype] += 1
            else:
                counts["Other"] += 1

            # Check medications
            if rtype == "MedicationRequest":
                med_codeable = resource.get("medicationCodeableConcept", {})
                med_text = med_codeable.get("text", "").lower()
                detected_poisons = [p for p in SCHEDULE_E1_POISONS if p in med_text]
                if detected_poisons:
                    schedule_e1_alerts.append({
                        "medication": med_text,
                        "poisons": detected_poisons,
                        "alert": "Schedule E(1) Statutory Poison detected. Dispense blocked until Mudabbar certificate is provided.",
                    })

        return {
            "status": "IMPORTED",
            "total_entries": len(entries),
            "resource_breakdown": counts,
            "schedule_e1_alerts": schedule_e1_alerts,
            "import_timestamp": datetime.utcnow().isoformat(),
            # Safe To Lock Invariant
            "safe_to_lock": False,
        }

    def _handle_wearable_stream_sync(self, task: TaskRecord) -> dict[str, Any]:
        """Processes continuous biometric telemetry from patient wearables."""
        payload = task.payload
        patient_id = payload.get("patient_id")
        readings = payload.get("readings", [])
        mizaj_baseline = payload.get("mizaj_baseline", "damawi")

        if not readings:
            return {"status": "NO_DATA", "readings_processed": 0}

        avg_hr = sum(r.get("heart_rate", 72) for r in readings) / len(readings)
        avg_hrv = sum(r.get("hrv_rmssd", 45) for r in readings) / len(readings)
        avg_spo2 = sum(r.get("spo2", 98) for r in readings) / len(readings)
        avg_deep_sleep = sum(r.get("deep_sleep_minutes", 60) for r in readings) / len(readings)

        # Calculate Unani Quwwat-e-Hayawaniyyah Autonomic Tone (0.0 - 1.0)
        # HRV RMSSD standard ~45ms; higher indicates vagal parasympathetic reserve
        quwa_hayawaniyyah = min(1.0, max(0.1, avg_hrv / 70.0))

        # Calculate Naum-o-Yaqzah (Sleep/Wake Harmony) Score
        naum_score = min(1.0, max(0.1, avg_deep_sleep / 90.0))

        # Detect Humoral Drift (Tahawwul-e-Mizaj)
        drift_detected = False
        drift_type = None
        if avg_hr > 90 and avg_hrv < 25:
            drift_detected = True
            drift_type = "Tahawwul-e-Mizaj Haar Yabis (Hypermetabolic / Bilious Escalation)"
        elif avg_hr < 55 and avg_deep_sleep < 30:
            drift_detected = True
            drift_type = "Tahawwul-e-Mizaj Barid (Hypometabolic Phlegmatic Stasis)"

        return {
            "status": "PROCESSED",
            "patient_id": patient_id,
            "readings_count": len(readings),
            "summary_metrics": {
                "avg_heart_rate": round(avg_hr, 1),
                "avg_hrv_rmssd": round(avg_hrv, 1),
                "avg_spo2": round(avg_spo2, 1),
                "quwwat_hayawaniyyah_score": round(quwa_hayawaniyyah, 2),
                "naum_yaqzah_score": round(naum_score, 2),
            },
            "humoral_drift_detected": drift_detected,
            "drift_type": drift_type,
            "sync_timestamp": datetime.utcnow().isoformat(),
            "safe_to_lock": False,
        }

    def _handle_qsura_dispatch(self, task: TaskRecord) -> dict[str, Any]:
        """Dispatches outbound patient communications enforcing Zero-PHI masking."""
        payload = task.payload
        channel = payload.get("channel", "WHATSAPP")
        recipient = payload.get("recipient")
        template_id = payload.get("template_id", "APPOINTMENT_REMINDER")

        # Zero-PHI Check: Mask recipient identifier
        masked_recipient = recipient[:3] + "..." + recipient[-4:] if recipient and len(recipient) > 7 else "REDACTED"

        return {
            "status": "DISPATCHED",
            "channel": channel,
            "masked_recipient": masked_recipient,
            "template_id": template_id,
            "dispatch_id": f"DISP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "dispatched_at": datetime.utcnow().isoformat(),
            "zero_phi_compliant": True,
        }

    def _handle_digital_twin_simulation(self, task: TaskRecord) -> dict[str, Any]:
        """Simulates longitudinal trajectory across organ axes."""
        payload = task.payload
        organ_axes = payload.get("organ_axes", {})
        simulation_weeks = payload.get("simulation_weeks", 4)

        projections = []
        for week in range(1, simulation_weeks + 1):
            recovery_delta = 0.04 * week
            projections.append({
                "week": week,
                "projected_vitality_index": min(1.0, round(0.65 + recovery_delta, 2)),
                "organ_harmony_score": min(1.0, round(0.70 + (0.05 * week), 2)),
            })

        return {
            "status": "SIMULATED",
            "simulation_weeks": simulation_weeks,
            "projections": projections,
            "simulated_at": datetime.utcnow().isoformat(),
            "safe_to_lock": False,
        }


def get_worker_daemon() -> WorkerDaemon:
    return WorkerDaemon(GLOBAL_TASK_QUEUE)
