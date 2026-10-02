"""
Stripe Payments Integration for ZAYVORA Identity Service.

Handles customer creation, subscriptions, payment intents, and webhook processing.
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def _get_stripe():
    import stripe
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
    return stripe


class StripeClient:
    """Stripe payment integration client."""

    def create_customer(self, email: str, name: str, metadata: dict | None = None) -> str:
        """Create a Stripe customer. Returns customer_id."""
        stripe = _get_stripe()
        customer = stripe.Customer.create(
            email=email, name=name, metadata=metadata or {}
        )
        logger.info("Stripe customer created: %s", customer.id)
        return customer.id

    def create_subscription(self, customer_id: str, price_id: str, trial_days: int = 0) -> dict[str, Any]:
        """Create a subscription for a customer."""
        stripe = _get_stripe()
        kwargs: dict[str, Any] = {"customer": customer_id, "items": [{"price": price_id}]}
        if trial_days > 0:
            kwargs["trial_period_days"] = trial_days
        subscription = stripe.Subscription.create(**kwargs)
        return dict(subscription)

    def create_payment_intent(
        self, amount: int, currency: str = "usd", customer_id: str = "", description: str = ""
    ) -> dict[str, Any]:
        """Create a PaymentIntent. Amount is in smallest currency unit (e.g. cents)."""
        stripe = _get_stripe()
        kwargs: dict[str, Any] = {"amount": amount, "currency": currency}
        if customer_id:
            kwargs["customer"] = customer_id
        if description:
            kwargs["description"] = description
        intent = stripe.PaymentIntent.create(**kwargs)
        return {"client_secret": intent.client_secret, "payment_intent_id": intent.id, "status": intent.status}

    def cancel_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Cancel a subscription immediately."""
        stripe = _get_stripe()
        result = stripe.Subscription.cancel(subscription_id)
        return {"subscription_id": result.id, "status": result.status}

    def get_subscription(self, customer_id: str) -> dict[str, Any] | None:
        """Retrieve the active subscription for a customer."""
        stripe = _get_stripe()
        subs = stripe.Subscription.list(customer=customer_id, status="active", limit=1)
        if subs.data:
            s = subs.data[0]
            return {"subscription_id": s.id, "status": s.status, "current_period_end": s.current_period_end}
        return None

    def handle_webhook(self, payload: bytes, sig_header: str) -> dict[str, Any]:
        """Verify and parse a Stripe webhook event."""
        stripe = _get_stripe()
        webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
            return {"event_type": event["type"], "data": event["data"]["object"]}
        except stripe.error.SignatureVerificationError as exc:
            raise ValueError("Invalid Stripe webhook signature") from exc
