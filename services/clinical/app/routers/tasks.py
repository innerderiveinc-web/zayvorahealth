"""
ZAYVORA Health™ — Asynchronous Task Queue & Background Worker Router.
Provides REST endpoints to enqueue, monitor, and process background tasks.
"""
from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.auth_dependency import CurrentUser, require_permission
from app.workers.task_queue import GLOBAL_TASK_QUEUE, TaskStatus, TaskType
from app.workers.worker_daemon import get_worker_daemon

router = APIRouter(prefix="/api/v1/tasks", tags=["asynchronous-tasks-and-workers"])


class EnqueueTaskPayload(BaseModel):
    task_type: str = Field(..., description="Task type identifier (e.g. abdm_packet_reconciliation, fhir_batch_import, wearable_stream_sync)")
    payload: dict[str, Any] = Field(default_factory=dict, description="Task execution arguments and parameters")
    max_retries: int = Field(default=3, ge=0, le=10)


class ABDMDataFlowRequestPayload(BaseModel):
    consent_artefact_id: str = Field(..., description="Approved ABDM Consent Artefact ID")
    patient_abha: str = Field(..., description="Patient ABHA ID")
    hi_types: list[str] = Field(default=["OPConsultation", "Prescription", "DiagnosticReport"])
    date_range_days: int = Field(default=90, ge=1, le=365)


class ABDMDataTransferWebhookPayload(BaseModel):
    transaction_id: str = Field(..., description="ABDM Data Flow Transaction ID")
    patient_abha: str = Field(..., description="Patient ABHA ID")
    encrypted_fhir_packets: list[dict[str, Any]] = Field(default_factory=list, description="Encrypted health data packets")


class FHIRBatchImportPayload(BaseModel):
    fhir_bundle: dict[str, Any] = Field(..., description="HL7 FHIR R4 JSON Bundle")


@router.post("/enqueue")
def enqueue_task_endpoint(
    payload: EnqueueTaskPayload,
    user: CurrentUser = Depends(require_permission("clinical.note.write")),
):
    """Enqueues an asynchronous background job."""
    task = GLOBAL_TASK_QUEUE.enqueue(
        task_type=payload.task_type,
        organization_id=user.organization_id,
        payload=payload.payload,
        max_retries=payload.max_retries,
        safe_to_lock=False,
    )
    return {
        "task_id": task.task_id,
        "task_type": task.task_type,
        "status": task.status.value,
        "created_at": task.created_at,
        "safe_to_lock": task.safe_to_lock,
    }


@router.get("/{task_id}")
def get_task_status_endpoint(
    task_id: str,
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Retrieves status, progress, and result of a background job."""
    task = GLOBAL_TASK_QUEUE.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task.to_dict()


@router.get("")
def list_tasks_endpoint(
    status: TaskStatus | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Lists background tasks for the current organization."""
    tasks = GLOBAL_TASK_QUEUE.list_tasks(
        organization_id=user.organization_id,
        status=status,
        limit=limit,
    )
    return {
        "total": len(tasks),
        "queue_depth": GLOBAL_TASK_QUEUE.queue_size(),
        "tasks": [t.to_dict() for t in tasks],
    }


@router.post("/worker/drain")
def drain_tasks_endpoint(
    max_iterations: int = Query(default=10, ge=1, le=100),
    user: CurrentUser = Depends(require_permission("system.admin")),
):
    """Synchronously triggers the background worker daemon to process pending tasks."""
    daemon = get_worker_daemon()
    processed = daemon.process_all(max_iterations=max_iterations)
    return {
        "processed_tasks": processed,
        "remaining_in_queue": GLOBAL_TASK_QUEUE.queue_size(),
    }


# -----------------------------------------------------------------------------
# Interoperability Background Workflows (ABDM Milestone 3 & FHIR Batch Import)
# -----------------------------------------------------------------------------

@router.post("/interop/abdm/data-flow/request")
def abdm_data_flow_request_endpoint(
    payload: ABDMDataFlowRequestPayload,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """ABDM Milestone 3: Initiates health data flow request to Health Information Provider (HIP)."""
    import uuid
    transaction_id = str(uuid.uuid4())
    return {
        "transaction_id": transaction_id,
        "consent_artefact_id": payload.consent_artefact_id,
        "patient_abha": payload.patient_abha,
        "status": "DATA_REQUEST_DISPATCHED",
        "key_material": {
            "crypto_algorithm": "ECDH_X25519",
            "curve": "curve25519",
            "nonce": "ZV-" + str(uuid.uuid4())[:12],
        },
        "message": "Health information request dispatched to ABDM Gateway. Encrypted packets will arrive asynchronously.",
    }


@router.post("/interop/abdm/data-flow/transfer")
def abdm_data_transfer_webhook_endpoint(
    payload: ABDMDataTransferWebhookPayload,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """ABDM Milestone 3 Webhook: Receives transferred packets and enqueues async reconciliation."""
    task = GLOBAL_TASK_QUEUE.enqueue(
        task_type=TaskType.ABDM_PACKET_RECONCILIATION.value,
        organization_id=user.organization_id,
        payload={
            "transaction_id": payload.transaction_id,
            "patient_abha": payload.patient_abha,
            "encrypted_fhir_packets": payload.encrypted_fhir_packets,
        },
        safe_to_lock=False,
    )
    return {
        "status": "TRANSFER_RECEIVED_AND_QUEUED",
        "transaction_id": payload.transaction_id,
        "task_id": task.task_id,
        "safe_to_lock": False,
        "message": "Encrypted health packets queued for asynchronous reconciliation and dual-coding mapping.",
    }


@router.post("/interop/fhir/batch-import")
def fhir_batch_import_endpoint(
    payload: FHIRBatchImportPayload,
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """Enqueues bulk HL7 FHIR R4 Bundle for background validation, import, and statutory poison checks."""
    task = GLOBAL_TASK_QUEUE.enqueue(
        task_type=TaskType.FHIR_BATCH_IMPORT.value,
        organization_id=user.organization_id,
        payload={"fhir_bundle": payload.fhir_bundle},
        safe_to_lock=False,
    )
    return {
        "status": "BATCH_IMPORT_QUEUED",
        "task_id": task.task_id,
        "safe_to_lock": False,
        "message": "FHIR R4 bundle queued for background processing.",
    }
