"""
ZAYVORA Health™ — Prescription Delivery Logistics & Courier Tracking Models (Issue AUTO-15).
Supports multi-carrier automated dispatch (Shiprocket, Delhivery, Bluedart), Airway Bills,
and temperature-controlled botanical cold-chain monitoring.
Provides standard library fallback for standalone testing environments.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

try:
    from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, Boolean, Integer, Float, Index
    from sqlalchemy.dialects.postgresql import UUID
    from sqlalchemy.orm import Mapped, mapped_column
    from app.models.therapeutic import Base, _uuid_pk, _now

    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    Base = object  # type: ignore


if HAS_SQLALCHEMY:
    class ShipmentRecord(Base):  # type: ignore
        """ZAYVORA Pharmacy OS Prescription Courier Shipment & Tracking Record."""

        __tablename__ = "courier_shipments"
        __table_args__ = (
            Index("idx_shipments_org_status", "organization_id", "status"),
            Index("idx_shipments_awb", "carrier", "awb_tracking_number"),
        )

        id: Mapped[uuid.UUID] = _uuid_pk()
        organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
        prescription_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
        patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)

        carrier: Mapped[str] = mapped_column(String(50), nullable=False)
        awb_tracking_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
        
        status: Mapped[str] = mapped_column(String(30), default="MANIFESTED", nullable=False, index=True)
        
        destination_pincode: Mapped[str] = mapped_column(String(20), nullable=False)
        shipping_address: Mapped[str] = mapped_column(Text, nullable=False)
        
        temperature_controlled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        temperature_range_celsius: Mapped[str] = mapped_column(String(50), default="15C - 25C (Ambient Controlled)")
        
        manifest_generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
        delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
        
        tracking_history: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
        courier_payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

else:
    @dataclass
    class ShipmentRecord:
        id: uuid.UUID = field(default_factory=uuid.uuid4)
        organization_id: uuid.UUID = field(default_factory=uuid.uuid4)
        prescription_id: uuid.UUID = field(default_factory=uuid.uuid4)
        patient_id: uuid.UUID = field(default_factory=uuid.uuid4)
        carrier: str = "SHIPROCKET"
        awb_tracking_number: str = ""
        status: str = "MANIFESTED"
        destination_pincode: str = "110025"
        shipping_address: str = "Address"
        temperature_controlled: bool = False
        temperature_range_celsius: str = "15C - 25C (Ambient Controlled)"
        manifest_generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        delivered_at: datetime | None = None
        tracking_history: list[dict[str, Any]] = field(default_factory=list)
        courier_payload_json: dict[str, Any] = field(default_factory=dict)
        created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
