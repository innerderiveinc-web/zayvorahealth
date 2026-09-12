"""
ZAYVORA Health™ — Prescription Delivery Logistics & Courier Tracking Router.
Handles courier dispatch orders, real-time carrier tracking webhooks, and AWB lookups.
"""
from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.engines.courier_engine import CourierLogisticsEngine
from app.models.logistics import ShipmentRecord

router = APIRouter(prefix="/api/v1/logistics", tags=["logistics-and-courier-delivery"])


class CreateShipmentRequest(BaseModel):
    prescription_id: uuid.UUID
    patient_id: uuid.UUID
    destination_pincode: str = Field(..., min_length=4, max_length=10)
    shipping_address: str = Field(..., min_length=10)
    carrier: str = Field(default="SHIPROCKET")
    temperature_controlled: bool = False
    temperature_range_celsius: str = "15C - 25C (Ambient Controlled)"


class CourierTrackingWebhookPayload(BaseModel):
    carrier: str
    awb_tracking_number: str
    event_status: str
    location: str = "Transit Facility"
    notes: str = ""
    timestamp_utc: str | None = None


@router.post("/shipments/create", status_code=status.HTTP_201_CREATED)
def create_shipment_endpoint(
    payload: CreateShipmentRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("dispensary.manage")),
):
    """Manifests a physical prescription dispatch with chosen courier carrier and issues an AWB."""
    try:
        shipment = CourierLogisticsEngine.create_shipment(
            organization_id=uuid.UUID(str(user.organization_id)),
            prescription_id=payload.prescription_id,
            patient_id=payload.patient_id,
            carrier=payload.carrier,
            destination_pincode=payload.destination_pincode,
            shipping_address=payload.shipping_address,
            temperature_controlled=payload.temperature_controlled,
            temperature_range_celsius=payload.temperature_range_celsius,
            db=db,
        )
        return {
            "shipment_id": str(shipment.id),
            "awb_tracking_number": shipment.awb_tracking_number,
            "carrier": shipment.carrier,
            "status": shipment.status,
            "temperature_controlled": shipment.temperature_controlled,
            "manifest_generated_at": shipment.manifest_generated_at.isoformat(),
        }
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.post("/webhooks/courier-tracking")
def courier_tracking_webhook_endpoint(
    payload: CourierTrackingWebhookPayload,
    db: Session = Depends(get_db),
):
    """Ingests real-time courier tracking milestone updates from third-party logistics providers."""
    try:
        res = CourierLogisticsEngine.process_tracking_webhook(
            carrier=payload.carrier,
            awb_tracking_number=payload.awb_tracking_number,
            event_status=payload.event_status,
            location=payload.location,
            notes=payload.notes,
            timestamp_utc=payload.timestamp_utc,
            db=db,
        )
        return res
    except LookupError as le:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(le))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.get("/shipments/by-prescription/{prescription_id}")
def get_shipment_by_prescription_endpoint(
    prescription_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("dispensary.read")),
):
    """Fetches courier shipment and tracking history for a prescription."""
    stmt = select(ShipmentRecord).where(
        ShipmentRecord.prescription_id == prescription_id,
        ShipmentRecord.organization_id == uuid.UUID(str(user.organization_id)),
    )
    shipment = db.execute(stmt).scalar_one_or_none()

    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment for prescription not found.")

    return {
        "shipment_id": str(shipment.id),
        "prescription_id": str(shipment.prescription_id),
        "awb_tracking_number": shipment.awb_tracking_number,
        "carrier": shipment.carrier,
        "status": shipment.status,
        "destination_pincode": shipment.destination_pincode,
        "temperature_controlled": shipment.temperature_controlled,
        "temperature_range_celsius": shipment.temperature_range_celsius,
        "manifest_generated_at": shipment.manifest_generated_at.isoformat(),
        "delivered_at": shipment.delivered_at.isoformat() if shipment.delivered_at else None,
        "tracking_history": shipment.tracking_history,
    }
