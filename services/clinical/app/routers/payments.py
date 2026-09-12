"""
ZAYVORA Health™ — Payment Gateway & Webhook Endpoints (Razorpay / Stripe).
Processes asynchronous billing webhooks, verifies HMAC signatures, and updates clinical state.
"""
from __future__ import annotations

import uuid
from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.billing.payment_gateway_engine import (
    PaymentGatewayEngine,
    PaymentSignatureVerificationError,
)
from app.core.auth_dependency import CurrentUser, require_permission
from app.core.database import get_db
from app.models.billing import PaymentTransaction

router = APIRouter(prefix="/api/v1/payments", tags=["payments-and-billing"])


class CreatePaymentOrderRequest(BaseModel):
    patient_id: uuid.UUID
    amount_in_cents: int = Field(..., gt=0, description="Amount in cents/paise (e.g. 150000 = 1500.00 INR)")
    currency: str = Field(default="INR", max_length=10)
    gateway_provider: str = Field(default="razorpay", pattern="^(razorpay|stripe)$")
    appointment_id: uuid.UUID | None = None
    prescription_id: uuid.UUID | None = None
    receipt_email: str | None = None


@router.post("/orders/create", status_code=status.HTTP_201_CREATED)
def create_payment_order(
    payload: CreatePaymentOrderRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.write")),
):
    """Initializes a new payment transaction order prior to checkout."""
    order_id = f"ORDER_{uuid.uuid4().hex[:12].upper()}"
    tx_id = f"TX_INIT_{uuid.uuid4().hex[:12].upper()}"
    idempotency_key = f"init_{order_id}_{payload.patient_id}"

    tx = PaymentTransaction(
        organization_id=uuid.UUID(str(user.organization_id)),
        patient_id=payload.patient_id,
        appointment_id=payload.appointment_id,
        prescription_id=payload.prescription_id,
        amount_in_cents=payload.amount_in_cents,
        currency=payload.currency.upper(),
        gateway_provider=payload.gateway_provider.lower(),
        gateway_transaction_id=tx_id,
        gateway_order_id=order_id,
        status="created",
        idempotency_key=idempotency_key,
        signature_verified=False,
        receipt_email=payload.receipt_email,
        payload_json={"initiator_user_id": user.user_id},
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "order_id": order_id,
        "transaction_id": str(tx.id),
        "amount_in_cents": tx.amount_in_cents,
        "currency": tx.currency,
        "gateway_provider": tx.gateway_provider,
        "status": tx.status,
    }


@router.post("/webhooks/razorpay")
async def razorpay_webhook_endpoint(
    request: Request,
    x_razorpay_signature: str = Header(..., alias="X-Razorpay-Signature"),
    db: Session = Depends(get_db),
):
    """Receives inbound Razorpay payment webhooks and verifies HMAC-SHA256 signature."""
    raw_body = await request.body()
    try:
        res = PaymentGatewayEngine.process_webhook_event(
            provider="razorpay",
            payload_raw=raw_body,
            signature=x_razorpay_signature,
            db=db,
        )
        return res
    except PaymentSignatureVerificationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/webhooks/stripe")
async def stripe_webhook_endpoint(
    request: Request,
    stripe_signature: str = Header(..., alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):
    """Receives inbound Stripe payment webhooks and verifies cryptographic signature header."""
    raw_body = await request.body()
    try:
        res = PaymentGatewayEngine.process_webhook_event(
            provider="stripe",
            payload_raw=raw_body,
            signature=stripe_signature,
            db=db,
        )
        return res
    except PaymentSignatureVerificationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/transactions/{transaction_id}")
def get_payment_transaction(
    transaction_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_permission("patient.read")),
):
    """Fetches payment transaction record and verification status."""
    tx = db.execute(
        select(PaymentTransaction).where(
            PaymentTransaction.id == transaction_id,
            PaymentTransaction.organization_id == uuid.UUID(str(user.organization_id)),
        )
    ).scalar_one_or_none()

    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment transaction not found")

    return {
        "id": str(tx.id),
        "organization_id": str(tx.organization_id),
        "patient_id": str(tx.patient_id),
        "appointment_id": str(tx.appointment_id) if tx.appointment_id else None,
        "prescription_id": str(tx.prescription_id) if tx.prescription_id else None,
        "amount_in_cents": tx.amount_in_cents,
        "currency": tx.currency,
        "gateway_provider": tx.gateway_provider,
        "gateway_transaction_id": tx.gateway_transaction_id,
        "status": tx.status,
        "signature_verified": tx.signature_verified,
        "created_at": tx.created_at.isoformat(),
    }
