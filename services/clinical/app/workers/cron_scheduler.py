"""
ZAYVORA Health™ — Periodic System Cron Scheduler Daemon (Issue AUTO-01).
Provides standalone scheduled time-based job execution for appointment reminders,
PROMs outcome surveys, nightly HIPAA retention audits, and PITR backup drills.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

logger = logging.getLogger("zayvora.cron")


@dataclass
class CronJobRecord:
    job_name: str
    interval_seconds: int
    description: str
    handler: Callable[..., dict[str, Any]]
    last_run_at: datetime | None = None
    last_status: str = "PENDING"
    last_result: dict[str, Any] | None = None
    last_error: str | None = None
    execution_count: int = 0


class CronSchedulerDaemon:
    """Manages scheduled periodic jobs across the clinical platform."""

    def __init__(self):
        self._jobs: dict[str, CronJobRecord] = {}
        self._is_running: bool = False
        self._register_default_jobs()

    def register_job(
        self,
        name: str,
        interval_seconds: int,
        handler: Callable[..., dict[str, Any]],
        description: str = "",
    ) -> None:
        """Registers a periodic scheduled job."""
        self._jobs[name] = CronJobRecord(
            job_name=name,
            interval_seconds=interval_seconds,
            description=description,
            handler=handler,
        )

    def _register_default_jobs(self) -> None:
        """Registers canonical ZAYVORA cron routines."""
        # 1. Appointment Reminders (Every 15 min / 900s)
        def _run_appointment_reminders() -> dict[str, Any]:
            from app.core.database import SessionLocal
            from app.workers.appointment_reminder_worker import AppointmentReminderWorker
            db = SessionLocal()
            try:
                worker = AppointmentReminderWorker(db)
                return worker.scan_and_dispatch_reminders()
            finally:
                db.close()

        self.register_job(
            name="appointment_reminders_scan",
            interval_seconds=900,
            handler=_run_appointment_reminders,
            description="Scans upcoming scheduled appointments within T-24h/T-2h and sends multi-channel reminders.",
        )

        # 2. PROMs Follow-up Survey (Every 24h / 86400s)
        def _run_proms_followup() -> dict[str, Any]:
            from app.core.database import SessionLocal
            from app.workers.proms_followup_worker import PROMsFollowupWorker
            db = SessionLocal()
            try:
                worker = PROMsFollowupWorker(db)
                return worker.scan_and_dispatch_proms_surveys(target_followup_days=7)
            finally:
                db.close()

        self.register_job(
            name="proms_followup_scan",
            interval_seconds=86400,
            handler=_run_proms_followup,
            description="Scans completed encounters at Day +7 and dispatches PROMs outcome surveys.",
        )

        # 3. Nightly HIPAA Audit Ledger Merkle Root Sealing (Every 24h)
        def _run_hipaa_audit_seal() -> dict[str, Any]:
            from app.governance.audit_trail_engine import GLOBAL_AUDIT_TRAIL
            if len(GLOBAL_AUDIT_TRAIL.chain) > 0:
                anchor = GLOBAL_AUDIT_TRAIL.generate_merkle_anchor()
                return {"status": "ANCHORED", "anchor_id": anchor.anchor_id, "merkle_root": anchor.merkle_root}
            return {"status": "NO_NEW_BLOCKS"}

        self.register_job(
            name="nightly_hipaa_retention_audit",
            interval_seconds=86400,
            handler=_run_hipaa_audit_seal,
            description="Computes SHA-256 Merkle root anchor over append-only audit ledger blocks.",
        )

        # 4. Disaster Recovery Health Drill (Every 24h)
        def _run_dr_health_drill() -> dict[str, Any]:
            from app.dr.backup_engine import DisasterRecoveryEngine
            cert = DisasterRecoveryEngine.verify_pitr_health()
            return {
                "status": "DRILL_VERIFIED",
                "certificate_id": cert.certificate_id,
                "rto_status": cert.rto_status,
                "rpo_status": cert.rpo_status,
            }

        self.register_job(
            name="pitr_backup_health_drill",
            interval_seconds=86400,
            handler=_run_dr_health_drill,
            description="Verifies point-in-time recovery backup snapshots and RTO/RPO SLA compliance.",
        )

    def execute_job(self, name: str, **kwargs) -> dict[str, Any]:
        """Manually triggers execution of a registered job by name."""
        if name not in self._jobs:
            raise KeyError(f"Cron job '{name}' is not registered.")
        
        job = self._jobs[name]
        start_time = datetime.now(timezone.utc)
        logger.info("Executing scheduled cron job '%s'...", name)

        try:
            result = job.handler(**kwargs) if kwargs else job.handler()
            job.last_run_at = start_time
            job.last_status = "SUCCESS"
            job.last_result = result
            job.last_error = None
            job.execution_count += 1
            return {
                "job_name": name,
                "status": "SUCCESS",
                "executed_at": start_time.isoformat(),
                "result": result,
            }
        except Exception as exc:
            err_msg = str(exc)
            logger.error("Cron job '%s' failed: %s", name, err_msg)
            job.last_run_at = start_time
            job.last_status = "FAILED"
            job.last_error = err_msg
            job.execution_count += 1
            return {
                "job_name": name,
                "status": "FAILED",
                "executed_at": start_time.isoformat(),
                "error": err_msg,
            }

    def run_due_jobs(self, current_time: datetime | None = None) -> list[dict[str, Any]]:
        """Evaluates intervals and triggers any jobs whose schedule is due."""
        now = current_time or datetime.now(timezone.utc)
        results = []

        for name, job in self._jobs.items():
            is_due = False
            if job.last_run_at is None:
                is_due = True
            else:
                elapsed = (now - job.last_run_at).total_seconds()
                if elapsed >= job.interval_seconds:
                    is_due = True

            if is_due:
                res = self.execute_job(name)
                results.append(res)

        return results

    def get_status(self) -> dict[str, Any]:
        """Returns registered jobs, intervals, and last execution metrics."""
        return {
            "total_registered_jobs": len(self._jobs),
            "jobs": {
                name: {
                    "interval_seconds": j.interval_seconds,
                    "description": j.description,
                    "last_run_at": j.last_run_at.isoformat() if j.last_run_at else None,
                    "last_status": j.last_status,
                    "execution_count": j.execution_count,
                    "last_error": j.last_error,
                }
                for name, j in self._jobs.items()
            },
        }


# Singleton daemon instance
GLOBAL_CRON_SCHEDULER = CronSchedulerDaemon()


def get_cron_scheduler() -> CronSchedulerDaemon:
    return GLOBAL_CRON_SCHEDULER


def main():
    print("ZAYVORA Health™ Periodic System Cron Scheduler Daemon started.")
    scheduler = get_cron_scheduler()
    try:
        while True:
            scheduler.run_due_jobs()
            time.sleep(10.0)
    except KeyboardInterrupt:
        print("Cron scheduler stopped gracefully.")


if __name__ == "__main__":
    main()
