"""
ZAYVORA Health™ — Prescription Delivery Logistics & Courier Tracking Engine.
Handles Airway Bill (AWB) generation, multi-carrier dispatch (Shiprocket / Delhivery / Bluedart),
botanical cold-chain enforcement, and real-time carrier tracking webhook ingestion.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

try:
    from sqlalchemy import select
    from sqlalchemy.orm import Session
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    Session = Any  # type: ignore

from app.models.logistics import ShipmentRecord

logger = logging.getLogger("zayvora.logistics")

VALID_CARRIERS = {"SHIPROCKET", "DELHIVERY", "BLUEDART", "INDIA_POST"}

VALID_STATUSES = {
    "MANIFESTED",
    "PICKED_UP",
    "IN_TRANSIT",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "RTO_INITIATED",
    "RETURNED",
}


class CourierLogisticsEngine:
    """Automates multi-carrier courier dispatch and lifecycle tracking for Unani pharmacy dispensations."""

    @staticmethod
    def generate_awb(carrier: str) -> str:
        """Generates deterministic, carrier-prefixed Airway Bill (AWB) tracking number."""
        prefix = carrier.upper().replace("_", "")[:4]
        return f"AWB-{prefix}-{uuid.uuid4().hex[:10].upper()}"

    @classmethod
    def create_shipment(
        cls,
        *,
        organization_id: uuid.UUID | str,
        prescription_id: uuid.UUID | str,
        patient_id: uuid.UUID | str,
        carrier: str = "SHIPROCKET",
        destination_pincode: str,
        shipping_address: str,
        temperature_controlled: bool = False,
        temperature_range_celsius: str = "15C - 25C (Ambient Controlled)",
        db: Session | None = None,
    ) -> ShipmentRecord:
        """Manifests a new courier shipment and issues an Airway Bill."""
        carrier_clean = carrier.upper().strip()
        if carrier_clean not in VALID_CARRIERS:
            raise ValueError(f"Unsupported courier carrier '{carrier}'. Supported: {sorted(VALID_CARRIERS)}")

        awb = cls.generate_awb(carrier_clean)
        now_utc = datetime.now(timezone.utc)

        initial_event = {
            "status": "MANIFESTED",
            "timestamp": now_utc.isoformat(),
            "location": "ZAYVORA Central Pharmacy Hub",
            "notes": "Prescription manifest generated; ready for carrier pickup.",
        }

        shipment = ShipmentRecord(
            id=uuid.uuid4(),
            organization_id=uuid.UUID(str(organization_id)),
            prescription_id=uuid.UUID(str(prescription_id)),
            patient_id=uuid.UUID(str(patient_id)),
            carrier=carrier_clean,
            awb_tracking_number=awb,
            status="MANIFESTED",
            destination_pincode=destination_pincode,
            shipping_address=shipping_address,
            temperature_controlled=temperature_controlled,
            temperature_range_celsius=temperature_range_celsius,
            manifest_generated_at=now_utc,
            tracking_history=[initial_event],
            courier_payload_json={"manifest_source": "ZAYVORA_PHARMACY_OS"},
        )

        if db is not None and hasattr(db, "add"):
            db.add(shipment)
            if hasattr(db, "commit"):
                db.commit()
            if hasattr(db, "refresh"):
                db.refresh(shipment)

        return shipment

    @classmethod
    def process_tracking_webhook(
        cls,
        *,
        carrier: str,
        awb_tracking_number: str,
        event_status: str,
        location: str = "In Transit Hub",
        notes: str = "",
        timestamp_utc: str | None = None,
        db: Session,
    ) -> dict[str, Any]:
        """Ingests real-time courier tracking milestone updates from carrier webhooks."""
        status_clean = event_status.upper().strip()
        if status_clean not in VALID_STATUSES:
            raise ValueError(f"Invalid courier tracking status '{event_status}'. Valid: {sorted(VALID_STATUSES)}")

        shipment = None
        if HAS_SQLALCHEMY and hasattr(db, "execute"):
            stmt = select(ShipmentRecord).where(
                ShipmentRecord.awb_tracking_number == awb_tracking_number
            )
            shipment = db.execute(stmt).scalar_one_or_none()
        elif hasattr(db, "get_shipment_by_awb"):
            shipment = db.get_shipment_by_awb(awb_tracking_number)
        elif hasattr(db, "shipments"):
            shipment = db.shipments.get(awb_tracking_number)

        if not shipment:
            raise LookupError(f"Shipment with AWB '{awb_tracking_number}' not found.")

        event_time = timestamp_utc or datetime.now(timezone.utc).isoformat()
        new_event = {
            "status": status_clean,
            "timestamp": event_time,
            "location": location,
            "notes": notes,
        }

        # Update shipment state
        shipment.status = status_clean
        history = list(shipment.tracking_history or [])
        history.append(new_event)
        shipment.tracking_history = history

        if status_clean == "DELIVERED":
            shipment.delivered_at = datetime.now(timezone.utc)

        if hasattr(db, "commit"):
            db.commit()
        if hasattr(db, "refresh"):
            db.refresh(shipment)

        logger.info("Shipment %s updated to status %s (%s)", awb_tracking_number, status_clean, location)
        return {
            "status": "PROCESSED",
            "awb_tracking_number": shipment.awb_tracking_number,
            "carrier": shipment.carrier,
            "current_status": shipment.status,
            "latest_event": new_event,
            "total_events": len(history),
            "delivered_at": shipment.delivered_at.isoformat() if shipment.delivered_at else None,
        }
