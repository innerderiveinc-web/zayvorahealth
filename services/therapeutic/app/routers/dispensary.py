from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.dispensary_engine import (
    MudabbarDispenseBlockError,
    allocate_fefo_batches,
    execute_batch_recall,
)
from app.models.therapeutic import DispenseRecord, InventoryBatch, NuskhaDraft
from app.schemas.therapeutic import (
    BatchRecallOut,
    BatchRecallRequest,
    DispenseRecordOut,
    DispenseRequest,
    InventoryBatchCreate,
    InventoryBatchOut,
)

router = APIRouter(prefix="/api/v1/dispensary", tags=["dispensary-pharmacy-os"])


@router.post("/batches", response_model=InventoryBatchOut, status_code=201)
def create_inventory_batch(
    payload: InventoryBatchCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("dispensary.manage")),
):
    """Registers a new pharmaceutical batch in the dispensary inventory.
    Schedule E(1) batches must include authenticated Mudabbar certificate."""
    if payload.is_schedule_e1 and not payload.mudabbar_certified:
        raise HTTPException(
            status_code=400,
            detail="Schedule E(1) poison batch cannot be admitted without authenticated Mudabbar certificate.",
        )

    batch = InventoryBatch(
        organization_id=uuid.UUID(user.organization_id),
        medication_name=payload.medication_name,
        formulation_type=payload.formulation_type,
        batch_number=payload.batch_number,
        manufacturer=payload.manufacturer,
        manufacturing_date=payload.manufacturing_date,
        expiry_date=payload.expiry_date,
        initial_quantity=payload.initial_quantity,
        available_quantity=payload.initial_quantity,
        unit=payload.unit,
        is_schedule_e1=payload.is_schedule_e1,
        mudabbar_certified=payload.mudabbar_certified,
        mudabbar_certificate_number=payload.mudabbar_certificate_number,
        qc_release_status="released",
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


@router.get("/batches", response_model=list[InventoryBatchOut])
def list_inventory_batches(
    medication_name: str | None = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("dispensary.read")),
):
    """Lists inventory batches ordered strictly by Expiry Date ascending (FEFO priority)."""
    stmt = select(InventoryBatch).where(
        InventoryBatch.organization_id == uuid.UUID(user.organization_id)
    )
    if medication_name:
        stmt = stmt.where(InventoryBatch.medication_name.ilike(f"%{medication_name}%"))
    stmt = stmt.order_by(InventoryBatch.expiry_date.asc())
    return db.execute(stmt).scalars().all()


@router.post("/dispense", response_model=list[DispenseRecordOut])
def dispense_prescription(
    payload: DispenseRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("dispensary.dispense")),
):
    """Fulfills prescription via First-Expired, First-Out (FEFO) batch allocation.
    Enforces the Mudabbar purification check before releasing any Schedule E(1) drugs."""
    batches = db.execute(
        select(InventoryBatch).where(
            InventoryBatch.organization_id == uuid.UUID(user.organization_id),
            InventoryBatch.medication_name.ilike(payload.medication_name),
            InventoryBatch.qc_release_status == "released",
        ).order_by(InventoryBatch.expiry_date.asc())
    ).scalars().all()

    if not batches:
        raise HTTPException(
            status_code=404,
            detail=f"No released inventory batches found for '{payload.medication_name}'.",
        )

    batch_dicts = [
        {
            "id": b.id,
            "batch_number": b.batch_number,
            "expiry_date": b.expiry_date,
            "available_quantity": b.available_quantity,
            "qc_release_status": b.qc_release_status,
            "mudabbar_certified": b.mudabbar_certified,
        }
        for b in batches
    ]

    try:
        allocation_result = allocate_fefo_batches(
            batches=batch_dicts,
            requested_quantity=payload.quantity_requested,
            is_schedule_e1=payload.is_schedule_e1,
        )
    except MudabbarDispenseBlockError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if allocation_result["status"] != "ALLOCATED":
        raise HTTPException(
            status_code=409,
            detail=(
                f"Insufficient stock for FEFO fulfillment. Required: {payload.quantity_requested}, "
                f"Available eligible: {allocation_result['total_allocated']}."
            ),
        )

    # Persist dispenses and update inventory quantities
    dispense_records = []
    batch_map = {b.id: b for b in batches}

    for alloc in allocation_result["allocations"]:
        batch_id = alloc["batch_id"]
        qty = alloc["allocated_quantity"]
        b_model = batch_map[batch_id]
        b_model.available_quantity = round(b_model.available_quantity - qty, 2)

        record = DispenseRecord(
            organization_id=uuid.UUID(user.organization_id),
            prescription_id=payload.prescription_id,
            patient_id=payload.patient_id,
            batch_id=batch_id,
            batch_number=alloc["batch_number"],
            quantity_dispensed=qty,
            dispensed_by_pharmacist_id=user.user_id,
            pharmacist_license_number=payload.pharmacist_license_number,
            patient_counseling_notes=payload.patient_counseling_notes,
            mudabbar_verified_at_dispense=alloc.get("mudabbar_certified", False),
        )
        db.add(record)
        dispense_records.append(record)

    db.commit()
    for dr in dispense_records:
        db.refresh(dr)

    return dispense_records


@router.post("/batches/{batch_id}/recall", response_model=BatchRecallOut)
def recall_batch(
    batch_id: uuid.UUID,
    payload: BatchRecallRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("dispensary.manage")),
):
    """Executes statutory batch recall, locking further dispensing of this lot."""
    batch = db.execute(
        select(InventoryBatch).where(
            InventoryBatch.id == batch_id,
            InventoryBatch.organization_id == uuid.UUID(user.organization_id),
        )
    ).scalar_one_or_none()

    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    batch_dict = {
        "batch_number": batch.batch_number,
        "medication_name": batch.medication_name,
        "qc_release_status": batch.qc_release_status,
    }

    recall_directive = execute_batch_recall(
        batch=batch_dict,
        reason=payload.reason,
        recalled_by_user_id=user.user_id,
        recall_class=payload.recall_class,
    )

    batch.qc_release_status = "recalled"
    db.commit()

    return recall_directive
