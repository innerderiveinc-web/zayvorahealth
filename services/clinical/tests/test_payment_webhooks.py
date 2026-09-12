"""
Unit tests for ZAYVORA Health™ Payment Gateway Webhook Automation (Issue AUTO-09).
Tests Razorpay and Stripe HMAC-SHA256 signature verification, idempotency replay defense,
and automated settlement transitions.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import unittest
import uuid
from datetime import datetime, timezone

from app.billing.payment_gateway_engine import (
    PaymentGatewayEngine,
    PaymentSignatureVerificationError,
)


class TestPaymentGatewayWebhooks(unittest.TestCase):
    def test_razorpay_valid_hmac_signature_verification(self):
        order_id = "order_N123456789"
        payment_id = "pay_N987654321"
        secret = "test_rzp_secret_key"
        expected_sig = hmac.new(
            secret.encode(),
            f"{order_id}|{payment_id}".encode(),
            hashlib.sha256,
        ).hexdigest()

        is_valid = PaymentGatewayEngine.verify_razorpay_signature(
            order_id=order_id,
            payment_id=payment_id,
            signature=expected_sig,
            secret=secret,
        )
        self.assertTrue(is_valid)

    def test_razorpay_invalid_signature_rejection(self):
        order_id = "order_N123456789"
        payment_id = "pay_N987654321"
        secret = "test_rzp_secret_key"
        forged_sig = "a1b2c3d4e5f60000000000000000000000000000000000000000000000000000"

        is_valid = PaymentGatewayEngine.verify_razorpay_signature(
            order_id=order_id,
            payment_id=payment_id,
            signature=forged_sig,
            secret=secret,
        )
        self.assertFalse(is_valid)

    def test_stripe_signature_verification(self):
        secret = "whsec_test_stripe_secret"
        now_ts = str(int(datetime.now(timezone.utc).timestamp()))
        payload_bytes = json.dumps({"type": "payment_intent.succeeded", "data": {"object": {"id": "pi_123"}}}).encode()
        
        sig = hmac.new(secret.encode(), f"{now_ts}.".encode() + payload_bytes, hashlib.sha256).hexdigest()
        sig_header = f"t={now_ts},v1={sig}"

        is_valid = PaymentGatewayEngine.verify_stripe_signature(
            payload=payload_bytes,
            sig_header=sig_header,
            secret=secret,
        )
        self.assertTrue(is_valid)

    def test_razorpay_webhook_event_processing_and_idempotency(self):
        secret = "rzp_webhook_secret_2026"
        order_id = f"order_ZV_{uuid.uuid4().hex[:8]}"
        payment_id = f"pay_ZV_{uuid.uuid4().hex[:8]}"
        sig = hmac.new(secret.encode(), f"{order_id}|{payment_id}".encode(), hashlib.sha256).hexdigest()

        payload = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": payment_id,
                        "order_id": order_id,
                        "amount": 250000,
                        "currency": "INR",
                        "status": "captured",
                        "method": "upi",
                        "email": "patient@example.com",
                        "notes": {
                            "patient_id": str(uuid.uuid4()),
                            "appointment_id": str(uuid.uuid4()),
                        },
                    }
                }
            }
        }

        # First execution -> SETTLED
        res = PaymentGatewayEngine.process_webhook_event(
            provider="razorpay",
            payload_raw=json.dumps(payload),
            signature=sig,
            secret=secret,
        )

        self.assertEqual(res["status"], "SETTLED")
        self.assertEqual(res["payment_status"], "captured")
        self.assertTrue(res["signature_verified"])
        self.assertFalse(res["is_idempotent_replay"])

        # Replay identical webhook -> DUPLICATE_IGNORED
        replay_res = PaymentGatewayEngine.process_webhook_event(
            provider="razorpay",
            payload_raw=json.dumps(payload),
            signature=sig,
            secret=secret,
        )
        self.assertEqual(replay_res["status"], "DUPLICATE_IGNORED")
        self.assertTrue(replay_res["is_idempotent_replay"])

    def test_forged_webhook_signature_raises_error(self):
        secret = "rzp_webhook_secret_2026"
        payload = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_fake_123",
                        "order_id": "order_fake_123",
                        "amount": 1000,
                    }
                }
            }
        }
        with self.assertRaises(PaymentSignatureVerificationError):
            PaymentGatewayEngine.process_webhook_event(
                provider="razorpay",
                payload_raw=json.dumps(payload),
                signature="invalid_signature_hash",
                secret=secret,
            )


if __name__ == "__main__":
    unittest.main()
