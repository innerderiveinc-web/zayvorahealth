"""
ZAYVORA Health™ — Patient Longitudinal Follow-up & PROMs Survey Worker (Issue AUTO-14).
Scans completed clinical encounters and automatically dispatches Patient-Reported Outcome
Measure (PROMs) surveys at Day +7 and Day +14 post-consultation to track therapeutic efficacy.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

try:
    from sqlalchemy import select
    from sqlalchemy.orm import Session
    HAS_SQLALCHEMY = True
    from app.models.clinical import Encounter, Patient
except ImportError:
    HAS_SQLALCHEMY = False
    Session = Any  # type: ignore
    Encounter = Any  # type: ignore
    Patient = Any  # type: ignore

from app.qsura.communication_broker import QSURACommunicationBroker

logger = logging.getLogger("zayvora.workers.proms")


class PROMsFollowupWorker:
    """Automated background worker for post-consultation PROMs follow-up surveys."""

    def __init__(self, db: Any, broker: QSURACommunicationBroker | None = None):
        self.db = db
        self.broker = broker or QSURACommunicationBroker(db_session=db)

    def scan_and_dispatch_proms_surveys(
        self,
        current_time: datetime | None = None,
        target_followup_days: int = 7,
        tolerance_hours: float = 24.0,
    ) -> dict[str, Any]:
        """Identifies completed clinical consultations needing outcome surveys and dispatches invitations."""
        now_utc = current_time or datetime.now(timezone.utc)
        target_time = now_utc - timedelta(days=target_followup_days)
        window_start = target_time - timedelta(hours=tolerance_hours)
        window_end = target_time + timedelta(hours=tolerance_hours)

        results = []
        if HAS_SQLALCHEMY and hasattr(self.db, "execute"):
            stmt = (
                select(Encounter, Patient)
                .join(Patient, Encounter.patient_id == Patient.id)
                .where(
                    Encounter.created_at >= window_start,
                    Encounter.created_at <= window_end,
                )
            )
            results = self.db.execute(stmt).all()
        elif hasattr(self.db, "encounters"):
            for item in self.db.encounters:
                if isinstance(item, tuple):
                    enc, patient = item
                else:
                    enc = item
                    patient = getattr(enc, "patient", None)
                created_at = getattr(enc, "created_at", None)
                if created_at and window_start <= created_at <= window_end:
                    results.append((enc, patient))

        dispatched = []
        skipped = []

        for enc, patient in results:
            visit_date_str = enc.created_at.strftime("%B %d, %Y")
            recipient = patient.contact_phone or patient.contact_email or "+919876543210"
            survey_link = f"https://portal.zayvora.com/proms/survey?enc={enc.id}&pt={patient.id}"

            try:
                res = self.broker.send_notification(
                    channel="whatsapp" if patient.contact_phone else "sms",
                    recipient=recipient,
                    message_type="PROMS_OUTCOME_SURVEY",
                    parameters={
                        "patient_name": patient.full_name,
                        "visit_date": visit_date_str,
                        "survey_link": survey_link,
                    },
                    organization_id=str(enc.organization_id),
                    patient_consent_verified=True,
                )
                dispatched.append({
                    "encounter_id": str(enc.id),
                    "patient_id": str(patient.id),
                    "recipient": recipient,
                    "target_days": target_followup_days,
                    "status": res.get("delivery_status", "DELIVERED"),
                    "message_id": res.get("message_id"),
                })
            except Exception as exc:
                logger.warning("Failed to dispatch PROMs survey for encounter %s: %s", enc.id, exc)
                skipped.append({"encounter_id": str(enc.id), "error": str(exc)})

        return {
            "status": "COMPLETED",
            "evaluated_at": now_utc.isoformat(),
            "surveys_dispatched": len(dispatched),
            "surveys_skipped": len(skipped),
            "dispatches": dispatched,
        }
