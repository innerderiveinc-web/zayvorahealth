"""
Unit tests for ZAYVORA Health™ Asynchronous Task Queue & Worker Daemon.
Tests ABDM packet reconciliation, FHIR batch import with Schedule E(1) alerts,
wearable telemetry sync, QSURA zero-PHI dispatch, and the safe_to_lock invariant.
"""
from __future__ import annotations

import unittest
from app.workers.task_queue import AsyncTaskQueue, TaskStatus, TaskType
from app.workers.worker_daemon import WorkerDaemon


class TestTasksAndABDMWorkers(unittest.TestCase):
    def setUp(self):
        # Fresh in-memory task queue and daemon for test isolation
        self.queue = AsyncTaskQueue(redis_url=None)
        self.daemon = WorkerDaemon(queue=self.queue)

    def test_task_queue_enqueue_dequeue_and_complete(self):
        task = self.queue.enqueue(
            task_type=TaskType.WEARABLE_STREAM_SYNC.value,
            organization_id="org-test-01",
            payload={"patient_id": "p-100", "readings": []},
            safe_to_lock=False,
        )
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertFalse(task.safe_to_lock)
        self.assertEqual(self.queue.queue_size(), 1)

        dequeued = self.queue.dequeue()
        self.assertIsNotNone(dequeued)
        self.assertEqual(dequeued.task_id, task.task_id)
        self.assertEqual(dequeued.status, TaskStatus.PROCESSING)

        completed = self.queue.complete_task(task.task_id, result={"ok": True}, safe_to_lock=False)
        self.assertIsNotNone(completed)
        self.assertEqual(completed.status, TaskStatus.COMPLETED)
        self.assertFalse(completed.safe_to_lock)
        self.assertEqual(completed.result, {"ok": True})

    def test_task_retry_and_terminal_failure(self):
        task = self.queue.enqueue(
            task_type="custom_task",
            organization_id="org-test-01",
            payload={},
            max_retries=1,
        )
        # First failure -> RETRYING
        retrying = self.queue.fail_task(task.task_id, "Network timeout")
        self.assertEqual(retrying.status, TaskStatus.RETRYING)
        self.assertEqual(retrying.retry_count, 1)

        # Dequeue the retried item and fail again -> FAILED
        dequeued = self.queue.dequeue()
        self.assertIsNotNone(dequeued)
        failed = self.queue.fail_task(task.task_id, "Permanent connection failure")
        self.assertEqual(failed.status, TaskStatus.FAILED)
        self.assertEqual(failed.retry_count, 2)
        self.assertIsNotNone(failed.completed_at)

    def test_abdm_packet_reconciliation_dual_coding(self):
        packets = [
            {
                "conditions": [
                    {"code": "E11.9", "display": "Type 2 Diabetes Mellitus"},
                    {"code": "M10.0", "display": "Idiopathic Gout"},
                    {"code": "I10", "display": "Essential Hypertension"},
                ],
                "observations": [
                    {"code": "LOINC-1558-6", "display": "Fasting Glucose", "value": 142, "unit": "mg/dL"},
                ],
                "medications": [
                    {"name": "Metformin 500mg", "dosage": "Twice daily with meals"},
                ],
            }
        ]

        task = self.queue.enqueue(
            task_type=TaskType.ABDM_PACKET_RECONCILIATION.value,
            organization_id="org-test-01",
            payload={
                "patient_abha": "91-1234-5678-9012",
                "encrypted_fhir_packets": packets,
            },
            safe_to_lock=False,
        )

        processed = self.daemon.process_one()
        self.assertIsNotNone(processed)
        self.assertEqual(processed.status, TaskStatus.COMPLETED)

        result = processed.result
        self.assertEqual(result["status"], "RECONCILED")
        self.assertEqual(result["patient_abha"], "91-1234-5678-9012")
        self.assertEqual(len(result["reconciled_conditions"]), 3)

        # Invariant Verification: safe_to_lock MUST be False
        self.assertFalse(result["safe_to_lock"])
        self.assertTrue(result["requires_clinician_ratification"])

        # Dual-coding verification: E11 -> Ziabetus Shakari, M10 -> Niqras, I10 -> Zaghtuddam Qawi
        cond_map = {c["biomedical_code"][:3]: c["unani_amraz"]["canonical_name"] for c in result["reconciled_conditions"]}
        self.assertIn("Ziabetus Shakari", cond_map["E11"])
        self.assertIn("Niqras", cond_map["M10"])
        self.assertIn("Zaghtuddam Qawi", cond_map["I10"])

    def test_fhir_batch_import_schedule_e1_poison_detection(self):
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "pat-01",
                        "name": [{"text": "Ahmad Khan"}],
                    }
                },
                {
                    "resource": {
                        "resourceType": "MedicationRequest",
                        "id": "med-01",
                        "medicationCodeableConcept": {"text": "Hab-e-Suranjan (contains Suranjan Talkh)"},
                    }
                },
                {
                    "resource": {
                        "resourceType": "MedicationRequest",
                        "id": "med-02",
                        "medicationCodeableConcept": {"text": "Hab-e-Azaraqi (Strychnos Nux-Vomica)"},
                    }
                },
            ],
        }

        task = self.queue.enqueue(
            task_type=TaskType.FHIR_BATCH_IMPORT.value,
            organization_id="org-test-01",
            payload={"fhir_bundle": bundle},
            safe_to_lock=False,
        )

        processed = self.daemon.process_one()
        self.assertIsNotNone(processed)
        self.assertEqual(processed.status, TaskStatus.COMPLETED)

        result = processed.result
        self.assertEqual(result["status"], "IMPORTED")
        self.assertEqual(result["total_entries"], 3)
        self.assertFalse(result["safe_to_lock"])

        # Statutory Schedule E(1) Alert Verification
        alerts = result["schedule_e1_alerts"]
        self.assertEqual(len(alerts), 2)
        all_poisons = [p for a in alerts for p in a["poisons"]]
        self.assertIn("suranjan talkh", all_poisons)
        self.assertIn("azaraqi", all_poisons)

    def test_wearable_stream_sync_and_humoral_drift(self):
        # 1. Normal Biometric Telemetry
        normal_readings = [
            {"heart_rate": 70, "hrv_rmssd": 50, "spo2": 98, "deep_sleep_minutes": 75},
            {"heart_rate": 72, "hrv_rmssd": 48, "spo2": 99, "deep_sleep_minutes": 80},
        ]
        task_normal = self.queue.enqueue(
            task_type=TaskType.WEARABLE_STREAM_SYNC.value,
            organization_id="org-test-01",
            payload={"patient_id": "p-01", "readings": normal_readings},
        )
        self.daemon.process_one()
        res_normal = self.queue.get_task(task_normal.task_id).result
        self.assertFalse(res_normal["humoral_drift_detected"])
        self.assertGreater(res_normal["summary_metrics"]["quwwat_hayawaniyyah_score"], 0.6)

        # 2. Abnormal Hypermetabolic / Bilious Telemetry (High HR, Depleted HRV)
        abnormal_readings = [
            {"heart_rate": 105, "hrv_rmssd": 18, "spo2": 97, "deep_sleep_minutes": 25},
            {"heart_rate": 98, "hrv_rmssd": 20, "spo2": 96, "deep_sleep_minutes": 20},
        ]
        task_abnormal = self.queue.enqueue(
            task_type=TaskType.WEARABLE_STREAM_SYNC.value,
            organization_id="org-test-01",
            payload={"patient_id": "p-02", "readings": abnormal_readings},
        )
        self.daemon.process_one()
        res_abnormal = self.queue.get_task(task_abnormal.task_id).result
        self.assertTrue(res_abnormal["humoral_drift_detected"])
        self.assertIn("Haar Yabis", res_abnormal["drift_type"])

    def test_qsura_dispatch_zero_phi_masking(self):
        task = self.queue.enqueue(
            task_type=TaskType.QSURA_DISPATCH.value,
            organization_id="org-test-01",
            payload={
                "channel": "SMS_TRAI",
                "recipient": "+919876543210",
                "template_id": "APPOINTMENT_CONFIRMED",
            },
        )
        self.daemon.process_one()
        res = self.queue.get_task(task.task_id).result
        self.assertEqual(res["status"], "DISPATCHED")
        self.assertTrue(res["zero_phi_compliant"])
        self.assertEqual(res["masked_recipient"], "+91...3210")


if __name__ == "__main__":
    unittest.main()
