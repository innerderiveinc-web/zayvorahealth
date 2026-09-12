"""
Unit tests for ZAYVORA Health™ Standalone Cron Scheduler & Scheduled Scanners.
Tests appointment reminders (AUTO-13), PROMs follow-up (AUTO-14), cron daemon execution (AUTO-01),
and Dead Letter Queue (DLQ) poison pill containment.
"""
from __future__ import annotations

import unittest
import uuid
from datetime import datetime, timedelta, timezone

from app.qsura.communication_broker import QSURACommunicationBroker
from app.workers.appointment_reminder_worker import AppointmentReminderWorker
from app.workers.cron_scheduler import CronSchedulerDaemon
from app.workers.proms_followup_worker import PROMsFollowupWorker
from app.workers.task_queue import AsyncTaskQueue, TaskStatus


class MockPatient:
    def __init__(self, id, organization_id, mrn, full_name, sex, contact_phone):
        self.id = id
        self.organization_id = organization_id
        self.mrn = mrn
        self.full_name = full_name
        self.sex = sex
        self.contact_phone = contact_phone
        self.contact_email = ""


class MockAppointment:
    def __init__(self, id, organization_id, patient_id, clinician_user_id, scheduled_at, status, reason):
        self.id = id
        self.organization_id = organization_id
        self.patient_id = patient_id
        self.clinician_user_id = clinician_user_id
        self.scheduled_at = scheduled_at
        self.status = status
        self.reason = reason


class MockEncounter:
    def __init__(self, id, organization_id, patient_id, clinician_user_id, encounter_type, created_at):
        self.id = id
        self.organization_id = organization_id
        self.patient_id = patient_id
        self.clinician_user_id = clinician_user_id
        self.encounter_type = encounter_type
        self.created_at = created_at


class MockDb:
    def __init__(self):
        self.appointments = []
        self.encounters = []

    def add(self, obj):
        pass

    def commit(self):
        pass

    def close(self):
        pass


class TestCronAndScheduledJobs(unittest.TestCase):
    def setUp(self):
        self.db = MockDb()
        self.org_id = uuid.uuid4()
        self.patient = MockPatient(
            id=uuid.uuid4(),
            organization_id=self.org_id,
            mrn="MRN-CRON-01",
            full_name="Hakim Ajmal Khan",
            sex="male",
            contact_phone="+919876543210",
        )

    def tearDown(self):
        self.db.close()

    def test_cron_scheduler_registration_and_execution(self):
        daemon = CronSchedulerDaemon()
        executed = []

        def sample_job():
            executed.append(True)
            return {"count": len(executed)}

        daemon.register_job("test_sample", interval_seconds=10, handler=sample_job, description="Test routine")
        
        status = daemon.get_status()
        self.assertIn("test_sample", status["jobs"])

        res = daemon.execute_job("test_sample")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(len(executed), 1)

    def test_appointment_reminder_worker_scans_and_dispatches(self):
        now_utc = datetime.now(timezone.utc)
        # Create an appointment 2 hours from now
        appt = MockAppointment(
            id=uuid.uuid4(),
            organization_id=self.org_id,
            patient_id=self.patient.id,
            clinician_user_id="dr-unani-101",
            scheduled_at=now_utc + timedelta(hours=2),
            status="scheduled",
            reason="Arthritis Evaluation",
        )
        self.db.appointments.append((appt, self.patient))

        broker = QSURACommunicationBroker(db_session=self.db)
        worker = AppointmentReminderWorker(self.db, broker=broker)

        result = worker.scan_and_dispatch_reminders(current_time=now_utc, lookahead_hours=5.0)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["reminders_dispatched"], 1)
        self.assertEqual(len(broker.dispatched_logs), 1)
        self.assertIn("Hakim Ajmal Khan", broker.dispatched_logs[0]["rendered_content"])

    def test_proms_followup_worker_scans_and_dispatches(self):
        now_utc = datetime.now(timezone.utc)
        # Create an encounter completed 7 days ago
        encounter = MockEncounter(
            id=uuid.uuid4(),
            organization_id=self.org_id,
            patient_id=self.patient.id,
            clinician_user_id="dr-unani-101",
            encounter_type="consultation",
            created_at=now_utc - timedelta(days=7),
        )
        self.db.encounters.append((encounter, self.patient))

        broker = QSURACommunicationBroker(db_session=self.db)
        worker = PROMsFollowupWorker(self.db, broker=broker)

        result = worker.scan_and_dispatch_proms_surveys(current_time=now_utc, target_followup_days=7)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["surveys_dispatched"], 1)
        self.assertEqual(len(broker.dispatched_logs), 1)
        self.assertIn("Hakim Ajmal Khan", broker.dispatched_logs[0]["rendered_content"])

    def test_dead_letter_queue_isolation_and_requeue(self):
        queue = AsyncTaskQueue()
        task = queue.enqueue("poison_pill_task", str(self.org_id), {"bad": "payload"}, max_retries=1)

        # Fail attempt 1 -> RETRYING
        queue.fail_task(task.task_id, "Error 1")
        # Dequeue retrying task
        dequeued = queue.dequeue()
        self.assertIsNotNone(dequeued)

        # Fail attempt 2 -> FAILED & Pushed to DLQ
        queue.fail_task(task.task_id, "Error 2 (Fatal)")

        dlq_tasks = queue.list_dlq_tasks()
        self.assertEqual(len(dlq_tasks), 1)
        self.assertEqual(dlq_tasks[0].task_id, task.task_id)
        self.assertEqual(dlq_tasks[0].status, TaskStatus.FAILED)

        # Requeue from DLQ
        requeued = queue.requeue_dlq_task(task.task_id)
        self.assertIsNotNone(requeued)
        self.assertEqual(requeued.status, TaskStatus.PENDING)
        self.assertEqual(requeued.retry_count, 0)
        self.assertEqual(len(queue.list_dlq_tasks()), 0)


if __name__ == "__main__":
    unittest.main()
