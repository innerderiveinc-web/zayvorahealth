"""
ZAYVORA Health™ — Billing & Payment Transaction Domain Models.
Supports multi-tenant payment gateway integrations (Razorpay, Stripe, UPI).
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
    from app.models.clinical import Base, _uuid_pk, _now

    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    Base = object  # type: ignore


if HAS_SQLALCHEMY:
    class PaymentTransaction(Base):  # type: ignore
        """Immutable audit record of payment gateway transactions (Razorpay / Stripe / UPI)."""

        __tablename__ = "payment_transactions"
        __table_args__ = (
            Index("idx_payments_org_status", "organization_id", "status"),
            Index("idx_payments_gateway_tx", "gateway_provider", "gateway_transaction_id"),
        )

        id: Mapped[uuid.UUID] = _uuid_pk()
        organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
        patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
        appointment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=True, index=True)
        prescription_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("prescriptions.id"), nullable=True, index=True)

        amount_in_cents: Mapped[int] = mapped_column(Integer, nullable=False)
        currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
        gateway_provider: Mapped[str] = mapped_column(String(30), nullable=False)
        gateway_transaction_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
        gateway_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
        
        status: Mapped[str] = mapped_column(String(30), default="created", nullable=False, index=True)
        idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
        signature_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        
        payment_method: Mapped[str] = mapped_column(String(50), default="card")
        receipt_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
        payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
        failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    class InvoiceRecord(Base):  # type: ignore
        """Clinical and pharmacy billing invoice."""

        __tablename__ = "invoices"

        id: Mapped[uuid.UUID] = _uuid_pk()
        organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
        patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
        invoice_number: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
        
        total_amount_in_cents: Mapped[int] = mapped_column(Integer, nullable=False)
        currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
        status: Mapped[str] = mapped_column(String(30), default="issued")
        
        line_items: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
        issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
        paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

else:
    @dataclass
    class PaymentTransaction:
        id: uuid.UUID = field(default_factory=uuid.uuid4)
        organization_id: uuid.UUID = field(default_factory=uuid.uuid4)
        patient_id: uuid.UUID = field(default_factory=uuid.uuid4)
        amount_in_cents: int = 0
        currency: str = "INR"
        gateway_provider: str = "razorpay"
        gateway_transaction_id: str = ""
        gateway_order_id: str | None = None
        status: str = "created"
        idempotency_key: str = ""
        signature_verified: bool = False
        appointment_id: uuid.UUID | None = None
        prescription_id: uuid.UUID | None = None
        payment_method: str = "card"
        receipt_email: str | None = None
        payload_json: dict[str, Any] = field(default_factory=dict)
        failure_reason: str | None = None
        created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @dataclass
    class InvoiceRecord:
        id: uuid.UUID = field(default_factory=uuid.uuid4)
        organization_id: uuid.UUID = field(default_factory=uuid.uuid4)
        patient_id: uuid.UUID = field(default_factory=uuid.uuid4)
        invoice_number: str = ""
        total_amount_in_cents: int = 0
        currency: str = "INR"
        status: str = "issued"
        line_items: list[dict[str, Any]] = field(default_factory=list)
        issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        paid_at: datetime | None = None
