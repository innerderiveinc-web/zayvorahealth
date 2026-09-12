from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth_dependency import CurrentUser, require_permission
from app.qsura.communication_broker import MESSAGE_TEMPLATES, QSURACommunicationBroker

router = APIRouter(prefix="/api/v1/qsura", tags=["qsura-clinical-communication"])

_QSURA_BROKER = QSURACommunicationBroker()


class NotificationSendRequest(BaseModel):
    channel: str = Field(pattern="^(whatsapp|sms|email|webhook)$")
    recipient: str = Field(min_length=3, max_length=100)
    message_type: str = Field(min_length=3, max_length=100)
    parameters: dict[str, Any]
    patient_consent_verified: bool = Field(default=True)


@router.post("/send")
def send_qsura_notification(
    payload: NotificationSendRequest,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """Dispatches a compliant, templated clinical message to patients or clinicians."""
    try:
        record = _QSURA_BROKER.send_notification(
            channel=payload.channel,
            recipient=payload.recipient,
            message_type=payload.message_type,
            parameters=payload.parameters,
            patient_consent_verified=payload.patient_consent_verified,
        )
        return record
    except (ValueError, PermissionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/templates")
def list_qsura_templates(
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Returns approved HSM / DLT templates with parameter definitions."""
    return MESSAGE_TEMPLATES


@router.get("/logs")
def list_qsura_logs(
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Returns the dispatch audit log for the current organization."""
    return _QSURA_BROKER.dispatched_logs
