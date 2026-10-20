"""
Authentication router for the ZAYVORA Identity service.

Endpoints
---------
POST /api/v1/auth/signup        Register a new user and return access + refresh tokens.
POST /api/v1/auth/login         Authenticate and return access + refresh tokens.
POST /api/v1/auth/refresh       Rotate a refresh token and return a new token pair.
POST /api/v1/auth/logout        Revoke the current bearer token.
GET  /api/v1/auth/session       Return the decoded session for the current token.
GET  /api/v1/auth/jwks.json     RFC 7517 JWKS public-key discovery endpoint.
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import log_event
from app.core.auth_dependency import CurrentUser, get_current_user
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    get_jwks,
    hash_password,
    revoke_token,
    rotate_refresh_token,
    validate_password_strength,
    verify_password,
)
from app.models.identity import AuditLog, Organization, Role, User, user_organization_roles
from app.schemas.identity import LoginRequest, TokenResponse, UserOut, UserSignup


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _client_ip(request: Request) -> str:
    """Return the originating IP, honouring X-Forwarded-For when set."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _user_agent(request: Request) -> str:
    return request.headers.get("User-Agent", "")


def _roles_and_permissions_for_user(
    db: Session, user_id: uuid.UUID, organization_id: uuid.UUID
) -> tuple[list[str], list[str]]:
    rows = (
        db.execute(
            select(Role)
            .join(user_organization_roles, user_organization_roles.c.role_id == Role.id)
            .where(
                user_organization_roles.c.user_id == user_id,
                user_organization_roles.c.organization_id == organization_id,
            )
        )
        .scalars()
        .all()
    )
    roles = [role.name for role in rows]
    permissions = sorted({perm.code for role in rows for perm in role.permissions})
    return roles, permissions


def _record_audit(
    db: Session,
    *,
    organization_id,
    actor_user_id,
    action: str,
    resource_type: str,
    resource_id: str = "",
    metadata: dict | None = None,
) -> None:
    """Backwards-compatible audit helper wrapping ``app.core.audit.log_event``."""
    db.add(
        AuditLog(
            organization_id=organization_id,
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata_json=metadata or {},
        )
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(payload: UserSignup, request: Request, db: Session = Depends(get_db)):
    """Register a new user and return an access token + refresh token.

    Validates password strength against the Phase-2 policy before creating
    the account.
    """
    settings = get_settings()

    # Phase-2 password strength check (more thorough than min-length alone)
    ok, reason = validate_password_strength(payload.password)
    if not ok:
        raise HTTPException(status_code=422, detail=reason)
    if len(payload.password) < settings.min_password_length:
        raise HTTPException(
            status_code=422,
            detail=f"Password must be at least {settings.min_password_length} characters",
        )

    org = db.execute(
        select(Organization).where(Organization.slug == payload.organization_slug)
    ).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="A user with this email already exists")

    # Security Hardening (OS-012): Prevent privilege escalation on public self-registration
    requested_role_name = (payload.role_name or "PATIENT").strip().upper()
    if requested_role_name != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Public self-registration only permits the 'PATIENT' role. Privileged roles must be provisioned by an administrator."
        )

    role = db.execute(
        select(Role).where(Role.organization_id == org.id, Role.name == requested_role_name)
    ).scalar_one_or_none()
    if not role:
        # Fallback to case-insensitive match for patient
        role = db.execute(
            select(Role).where(Role.organization_id == org.id, Role.name.ilike("patient"))
        ).scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=422,
            detail=f"Role '{payload.role_name}' does not exist for this organization",
        )

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.flush()  # populate user.id

    db.execute(
        user_organization_roles.insert().values(
            user_id=user.id, organization_id=org.id, role_id=role.id
        )
    )

    log_event(
        db,
        user_id=user.id,
        action="auth.signup",
        resource_type="user",
        resource_id=str(user.id),
        organization_id=org.id,
        request_ip=_client_ip(request),
        user_agent=_user_agent(request),
    )
    db.commit()
    db.refresh(user)

    roles, permissions = _roles_and_permissions_for_user(db, user.id, org.id)
    token, expires_in = create_access_token(
        user_id=user.id,
        organization_id=org.id,
        roles=roles,
        permissions=permissions,
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    return TokenResponse(
        access_token=token,
        refresh_token=refresh_token,
        expires_in_seconds=expires_in,
        user=UserOut.model_validate(user),
        organization=org,
        roles=roles,
        permissions=permissions,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Authenticate with email + password and return a token pair.

    Applies IP-based and per-user sliding-window rate limits, plus the
    Phase-2 lockout manager (5 consecutive failures → 15-minute lockout).
    """
    settings = get_settings()
    client_ip = _client_ip(request)

    # Sliding-window rate limits (existing RateLimiter)
    limiter = request.app.state.rate_limiter
    limiter.check(
        key=f"login-ip:{client_ip}",
        limit=settings.login_rate_limit_attempts,
        window_seconds=settings.login_rate_limit_window_seconds,
    )
    limiter.check(
        key=f"login-user:{payload.email.lower()}",
        limit=settings.login_rate_limit_attempts,
        window_seconds=settings.login_rate_limit_window_seconds,
    )

    # Phase-2: lockout check
    if hasattr(request.app.state, "lockout_manager"):
        lockout = request.app.state.lockout_manager
        lockout.check(identifier=payload.email.lower())
        lockout.check(identifier=f"ip:{client_ip}")

    org = db.execute(
        select(Organization).where(Organization.slug == payload.organization_slug)
    ).scalar_one_or_none()
    user = (
        db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
        if org
        else None
    )

    # Identical failure path regardless of which check failed to prevent enumeration
    if not org or not user or not user.is_active or not verify_password(payload.password, user.hashed_password):
        log_event(
            db,
            user_id=user.id if user else None,
            action="auth.login.failed",
            resource_type="session",
            organization_id=org.id if org else None,
            request_ip=client_ip,
            user_agent=_user_agent(request),
            details={"email": payload.email},
        )
        db.commit()

        # Phase-2: record failure for lockout
        if hasattr(request.app.state, "lockout_manager"):
            lockout = request.app.state.lockout_manager
            lockout.record_failure(payload.email.lower())
            lockout.record_failure(f"ip:{client_ip}")

        raise HTTPException(status_code=401, detail="Invalid credentials")

    roles, permissions = _roles_and_permissions_for_user(db, user.id, org.id)
    if not roles:
        raise HTTPException(status_code=403, detail="User has no role assigned in this organization")

    # ---------------------------------------------------------------------------
    # MFA enforcement for clinical staff roles
    # Clinical roles that handle PHI must complete TOTP verification every login.
    # ---------------------------------------------------------------------------
    CLINICAL_ROLES = {"hakeem", "doctor", "pharmacist", "nurse", "clinic_admin"}
    user_roles_lower = {r.lower() for r in roles}
    requires_mfa = bool(user_roles_lower & CLINICAL_ROLES)

    if requires_mfa and user.mfa_enabled:
        if not payload.mfa_code:
            # Signal to the frontend that it must collect a TOTP code
            log_event(
                db,
                user_id=user.id,
                action="auth.login.mfa_challenge",
                resource_type="session",
                organization_id=org.id,
                request_ip=client_ip,
                user_agent=_user_agent(request),
                details={"roles": roles},
            )
            db.commit()
            raise HTTPException(
                status_code=403,
                detail={
                    "code": "MFA_REQUIRED",
                    "message": "Multi-factor authentication is required for your role. "
                               "Please provide your 6-digit authenticator code.",
                },
            )

        # Verify the supplied TOTP code
        if user.mfa_secret:
            from app.core.mfa import verify_totp
            if not verify_totp(user.mfa_secret, payload.mfa_code):
                log_event(
                    db,
                    user_id=user.id,
                    action="auth.login.mfa_failed",
                    resource_type="session",
                    organization_id=org.id,
                    request_ip=client_ip,
                    user_agent=_user_agent(request),
                    details={"roles": roles},
                )
                if hasattr(request.app.state, "lockout_manager"):
                    request.app.state.lockout_manager.record_failure(payload.email.lower())
                db.commit()
                raise HTTPException(status_code=401, detail="Invalid MFA code")

    token, expires_in = create_access_token(
        user_id=user.id, organization_id=org.id, roles=roles, permissions=permissions
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    log_event(
        db,
        user_id=user.id,
        action="auth.login.success",
        resource_type="session",
        organization_id=org.id,
        request_ip=client_ip,
        user_agent=_user_agent(request),
        details={"roles": roles},
    )
    db.commit()

    # Reset rate-limit and lockout counters on success
    limiter.reset(f"login-ip:{client_ip}")
    limiter.reset(f"login-user:{payload.email.lower()}")
    if hasattr(request.app.state, "lockout_manager"):
        lockout = request.app.state.lockout_manager
        lockout.record_success(payload.email.lower())
        lockout.record_success(f"ip:{client_ip}")

    return TokenResponse(
        access_token=token,
        refresh_token=refresh_token,
        expires_in_seconds=expires_in,
        user=UserOut.model_validate(user),
        organization=org,
        roles=roles,
        permissions=permissions,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token_endpoint(
    request: Request,
    refresh_token: str = Body(..., embed=True, description="The refresh token to rotate."),
    db: Session = Depends(get_db),
):
    """Rotate a refresh token and return a new access + refresh token pair.

    The old refresh token is immediately revoked after this call (one-time-use
    rotation).  If a previously-used token is presented, all sessions for the
    subject are considered compromised and the request is rejected with 401.

    Request body::

        { "refresh_token": "<token>" }

    Returns the same ``TokenResponse`` shape as ``/login``, including a new
    ``refresh_token`` field.
    """
    client_ip = _client_ip(request)
    user_agent = _user_agent(request)

    # rotate_refresh_token returns (subject_str, new_refresh_token)
    subject, new_refresh = rotate_refresh_token(refresh_token)

    # Re-load the user and their current roles from the database
    try:
        user_uuid = uuid.UUID(subject)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token subject") from exc

    user = db.get(User, user_uuid)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    # Determine the user's primary organisation (first found)
    from sqlalchemy import select as sa_select

    org_row = db.execute(
        sa_select(Organization)
        .join(
            user_organization_roles,
            user_organization_roles.c.organization_id == Organization.id,
        )
        .where(user_organization_roles.c.user_id == user_uuid)
        .limit(1)
    ).scalar_one_or_none()

    if org_row is None:
        raise HTTPException(status_code=403, detail="User has no organisation assigned")

    roles, permissions = _roles_and_permissions_for_user(db, user_uuid, org_row.id)
    new_access_token, expires_in = create_access_token(
        user_id=user_uuid,
        organization_id=org_row.id,
        roles=roles,
        permissions=permissions,
    )

    log_event(
        db,
        user_id=user_uuid,
        action="auth.token.refresh",
        resource_type="session",
        organization_id=org_row.id,
        request_ip=client_ip,
        user_agent=user_agent,
    )
    db.commit()

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh,
        expires_in_seconds=expires_in,
        user=UserOut.model_validate(user),
        organization=org_row,
        roles=roles,
        permissions=permissions,
    )


@router.get("/session", response_model=dict)
def session(user: CurrentUser = Depends(get_current_user)):
    """Return the decoded session claims for the bearer token."""
    return {
        "userId": user.user_id,
        "organizationId": user.organization_id,
        "roles": user.roles,
        "permissions": user.permissions,
    }


@router.get("/jwks.json", response_model=dict)
def jwks():
    """RFC 7517 JSON Web Key Set (JWKS) public key discovery endpoint."""
    return get_jwks()


@router.post("/logout", response_model=dict)
def logout(request: Request, db: Session = Depends(get_db)):
    """Revoke the current bearer token via JTI blocklisting."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth_header.removeprefix("Bearer ").strip()
    try:
        payload = decode_access_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    jti = payload.get("jti")
    exp = payload.get("exp", time.time() + 3600)
    if jti:
        revoke_token(jti, float(exp))

    org_id = payload.get("org")
    user_id = payload.get("sub")

    log_event(
        db,
        user_id=uuid.UUID(user_id) if user_id else None,
        action="auth.logout",
        resource_type="session",
        organization_id=uuid.UUID(org_id) if org_id else None,
        request_ip=_client_ip(request),
        user_agent=_user_agent(request),
        details={"jti": jti},
    )
    db.commit()

    return {"message": "Logged out successfully"}

# ---------------------------------------------------------------------------
# MFA Enrollment endpoints
# ---------------------------------------------------------------------------

@router.post("/mfa/setup", response_model=dict, summary="Generate TOTP secret for MFA enrollment")
def mfa_setup(
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a TOTP secret for the current user.

    Returns an otpauth:// URI that can be displayed as a QR code in the
    frontend so the user can register their authenticator app.
    The secret is NOT activated until ``POST /mfa/verify-setup`` confirms
    the first valid code.
    """
    from app.core.mfa import generate_totp_secret, generate_qr_code_uri

    user = db.execute(select(User).where(User.id == current_user.id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    secret = generate_totp_secret()
    # Temporarily store the pending secret (not yet confirmed)
    user.mfa_secret = secret
    db.commit()

    uri = generate_qr_code_uri(
        secret=secret,
        email=user.email,
        issuer="ZAYVORA Health OS™",
    )
    return {"secret": secret, "otpauth_uri": uri, "message": "Scan the QR code with your authenticator app, then call /mfa/verify-setup with your first code."}


@router.post("/mfa/verify-setup", response_model=dict, summary="Confirm MFA enrollment with first TOTP code")
def mfa_verify_setup(
    code: str = Body(..., embed=True, min_length=6, max_length=6),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verify the first TOTP code and activate MFA for the account."""
    from app.core.mfa import verify_totp

    user = db.execute(select(User).where(User.id == current_user.id)).scalar_one_or_none()
    if not user or not user.mfa_secret:
        raise HTTPException(status_code=400, detail="No pending MFA setup. Call /mfa/setup first.")

    if not verify_totp(user.mfa_secret, code):
        raise HTTPException(status_code=401, detail="Invalid MFA code. Please try again with a fresh code from your authenticator app.")

    user.mfa_enabled = True
    log_event(db, user_id=user.id, action="auth.mfa.enabled", resource_type="user", details={})
    db.commit()
    return {"ok": True, "message": "MFA activated successfully. You will be required to supply a TOTP code on every login."}


@router.delete("/mfa/disable", response_model=dict, summary="Disable MFA for the current user")
def mfa_disable(
    code: str = Body(..., embed=True, min_length=6, max_length=6, description="Current valid TOTP code to confirm disable"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Disable MFA — requires a valid current TOTP code as confirmation."""
    from app.core.mfa import verify_totp

    user = db.execute(select(User).where(User.id == current_user.id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.mfa_enabled and user.mfa_secret:
        if not verify_totp(user.mfa_secret, code):
            raise HTTPException(status_code=401, detail="Invalid MFA code")

    user.mfa_enabled = False
    user.mfa_secret = None
    log_event(db, user_id=user.id, action="auth.mfa.disabled", resource_type="user", details={})
    db.commit()
    return {"ok": True, "message": "MFA disabled."}


# ---------------------------------------------------------------------------
# GDPR Compliance endpoints (Article 17 & 20)
# ---------------------------------------------------------------------------

@router.get("/gdpr-export", response_model=dict, summary="GDPR Article 20 — Export all personal data")
def gdpr_export(
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all personal data held about the authenticated user.

    Implements GDPR Article 20 (Right to Data Portability).
    Data is returned as structured JSON covering identity, audit logs.
    Clinical data export is handled by the clinical service.
    """
    user = db.execute(select(User).where(User.id == current_user.id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    audit_logs = db.execute(
        select(AuditLog).where(AuditLog.user_id == user.id).limit(1000)
    ).scalars().all()

    log_event(db, user_id=user.id, action="gdpr.export.requested", resource_type="user",
              request_ip=_client_ip(request), details={})
    db.commit()

    return {
        "gdpr_export": {
            "request_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "subject": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "date_of_birth": str(user.date_of_birth) if getattr(user, "date_of_birth", None) else None,
                "gender": getattr(user, "gender", None),
                "is_active": user.is_active,
                "created_at": str(user.created_at),
                "mfa_enabled": user.mfa_enabled,
            },
            "audit_trail": [
                {
                    "id": str(e.id),
                    "action": e.action,
                    "resource_type": e.resource_type,
                    "timestamp": str(e.created_at),
                    "ip": e.request_ip,
                }
                for e in audit_logs
            ],
            "note": "Clinical records, prescriptions and lab results are available from the clinical data export endpoint.",
        }
    }


@router.delete("/gdpr-erase", response_model=dict, summary="GDPR Article 17 — Right to be forgotten")
def gdpr_erase(
    request: Request,
    confirmation: str = Body(..., embed=True, description="Must equal 'ERASE MY DATA' to confirm"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Anonymise all personal data for the authenticated user.

    Implements GDPR Article 17 (Right to Erasure / Right to be Forgotten).
    The user record is anonymised (email, name, phone replaced with hashed placeholders).
    Audit log entries are preserved as required by 21 CFR Part 11 but stripped of PII.
    Clinical records anonymisation is delegated to the clinical service.
    """
    if confirmation != "ERASE MY DATA":
        raise HTTPException(
            status_code=400,
            detail="Confirmation mismatch. Send {\"confirmation\": \"ERASE MY DATA\"} to proceed.",
        )

    user = db.execute(select(User).where(User.id == current_user.id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    import hashlib
    uid_hash = hashlib.sha256(str(user.id).encode()).hexdigest()[:12]

    # Anonymise PII fields — preserve the record for audit trail integrity
    user.email = f"erased-{uid_hash}@gdpr.zayvora.health"
    user.full_name = f"[ERASED-{uid_hash}]"
    user.phone = None
    user.hashed_password = ""
    user.mfa_secret = None
    user.mfa_enabled = False
    user.is_active = False

    log_event(
        db,
        user_id=user.id,
        action="gdpr.erasure.completed",
        resource_type="user",
        request_ip=_client_ip(request),
        details={"uid_hash": uid_hash},
    )
    db.commit()

    return {
        "ok": True,
        "message": "Your personal data has been anonymised and your account deactivated. "
                   "Audit trail entries are retained as required by applicable law.",
    }


@router.get("/users", response_model=list[UserOut], summary="List all registered users")
def list_users(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """List users. SUPER_ADMIN sees all tenants; other admins see only their org."""
    query = select(User).order_by(User.created_at.desc())
    # Tenant isolation: non-super-admins only see users in their own organization
    if "SUPER_ADMIN" not in current_user.roles:
        if not current_user.organization_id:
            raise HTTPException(status_code=403, detail="Organization context required")
        query = query.where(User.organization_id == current_user.organization_id)
    users = db.execute(query).scalars().all()
    return users
