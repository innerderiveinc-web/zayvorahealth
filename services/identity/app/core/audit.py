"""
Audit logging for the ZAYVORA Identity service (Phase 2 hardening).

Provides a single ``log_event()`` helper that records every security-relevant
action to the ``audit_logs`` database table (via the existing ``AuditLog``
SQLAlchemy model) and, optionally, to the Python ``logging`` subsystem for
stream-based log aggregation (Loki, CloudWatch, etc.).

Tracked event types
-------------------
    auth.login.success      Successful interactive login
    auth.login.failed       Credential mismatch or locked-out attempt
    auth.logout             Explicit logout / token revocation
    auth.token.refresh      Refresh-token rotation
    auth.password.change    User-initiated password update
    auth.mfa.attempt        TOTP verification attempt (success or failure)
    auth.mfa.setup          MFA secret generated / QR code requested
    auth.signup             New user registration
    auth.token.revoke       Manual token revocation (admin action)

All events capture: actor user ID, action string, resource type + ID,
originating IP address, User-Agent header, and an arbitrary JSON metadata
blob for action-specific fields (e.g. new role, revoked JTI, MFA result).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session

logger = logging.getLogger("zayvora.identity.audit")


def log_event(
    db: Session,
    *,
    user_id: Optional[Any],
    action: str,
    resource_type: str,
    resource_id: str = "",
    request_ip: str = "unknown",
    user_agent: str = "",
    organization_id: Optional[Any] = None,
    details: Optional[dict[str, Any]] = None,
    flush: bool = False,
) -> None:
    """Record a security audit event to the database and the structured log stream.

    This function is a thin wrapper around the existing ``AuditLog`` ORM model.
    It intentionally never raises – a failed audit write must not block the
    primary auth flow.  Errors are captured and emitted at ERROR level so they
    surface in the monitoring pipeline.

    Args:
        db:              Active SQLAlchemy session.  The event is added to the
                         session but **not** committed – the caller's transaction
                         owns the commit boundary.
        user_id:         UUID (or None for anonymous / pre-authentication events)
                         of the actor whose action is being recorded.
        action:          Dot-separated action string, e.g. ``"auth.login.success"``.
        resource_type:   Category of the affected object, e.g. ``"session"``,
                         ``"user"``, ``"mfa_secret"``.
        resource_id:     String identifier of the affected resource (UUID, slug, …).
        request_ip:      IP address of the originating HTTP client.
        user_agent:      Value of the ``User-Agent`` request header.
        organization_id: UUID of the tenant context (may be ``None`` for
                         system-level events).
        details:         Arbitrary JSON-serialisable dict with action-specific
                         metadata (e.g. ``{"jti": "…", "mfa_success": True}``).
        flush:           If ``True``, flush the session after adding the event so
                         the row is immediately visible within the same
                         transaction (useful in tests).

    Example::

        from app.core.audit import log_event

        log_event(
            db,
            user_id=user.id,
            action="auth.login.success",
            resource_type="session",
            organization_id=org.id,
            request_ip=client_ip,
            user_agent=request.headers.get("user-agent", ""),
            details={"roles": roles},
        )
        db.commit()
    """
    try:
        # Import here to avoid circular imports at module load time
        from app.models.identity import AuditLog

        now = datetime.now(timezone.utc)
        metadata: dict[str, Any] = {
            "ip": request_ip,
            "user_agent": user_agent,
            "timestamp": now.isoformat(),
        }
        if details:
            metadata.update(details)

        entry = AuditLog(
            organization_id=organization_id,
            actor_user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata_json=metadata,
        )
        db.add(entry)
        if flush:
            db.flush()

        # Emit a structured log line for stream-based aggregation
        logger.info(
            "audit_event",
            extra={
                "audit_action": action,
                "audit_resource_type": resource_type,
                "audit_resource_id": resource_id,
                "audit_user_id": str(user_id) if user_id else None,
                "audit_org_id": str(organization_id) if organization_id else None,
                "audit_ip": request_ip,
                "audit_user_agent": user_agent,
                "audit_details": details or {},
                "audit_timestamp": now.isoformat(),
            },
        )
    except Exception:
        logger.error(
            "Failed to persist audit event",
            exc_info=True,
            extra={
                "audit_action": action,
                "audit_user_id": str(user_id) if user_id else None,
                "audit_ip": request_ip,
            },
        )
