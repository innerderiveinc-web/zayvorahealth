from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, get_current_user
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_jwks,
    hash_password,
    revoke_token,
    verify_password,
)
from app.models.identity import AuditLog, Organization, Role, User, user_organization_roles
from app.schemas.identity import LoginRequest, TokenResponse, UserOut, UserSignup


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _roles_and_permissions_for_user(db: Session, user_id: uuid.UUID, organization_id: uuid.UUID) -> tuple[list[str], list[str]]:
    rows = db.execute(
        select(Role)
        .join(user_organization_roles, user_organization_roles.c.role_id == Role.id)
        .where(
            user_organization_roles.c.user_id == user_id,
            user_organization_roles.c.organization_id == organization_id,
        )
    ).scalars().all()
    roles = [role.name for role in rows]
    permissions = sorted({perm.code for role in rows for perm in role.permissions})
    return roles, permissions


def _record_audit(db: Session, *, organization_id, actor_user_id, action: str, resource_type: str, resource_id: str = "", metadata: dict | None = None):
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


@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(payload: UserSignup, request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    if len(payload.password) < settings.min_password_length:
        raise HTTPException(status_code=422, detail=f"Password must be at least {settings.min_password_length} characters")

    org = db.execute(select(Organization).where(Organization.slug == payload.organization_slug)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="A user with this email already exists")

    role = db.execute(
        select(Role).where(Role.organization_id == org.id, Role.name == payload.role_name)
    ).scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=422, detail=f"Role '{payload.role_name}' does not exist for this organization")

    user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password))
    db.add(user)
    db.flush()  # populate user.id before using it in the association insert

    db.execute(
        user_organization_roles.insert().values(user_id=user.id, organization_id=org.id, role_id=role.id)
    )
    _record_audit(db, organization_id=org.id, actor_user_id=user.id, action="auth.signup", resource_type="user", resource_id=str(user.id))
    db.commit()
    db.refresh(user)

    roles, permissions = _roles_and_permissions_for_user(db, user.id, org.id)
    token, expires_in = create_access_token(user_id=user.id, organization_id=org.id, roles=roles, permissions=permissions)
    return TokenResponse(
        access_token=token,
        expires_in_seconds=expires_in,
        user=UserOut.model_validate(user),
        organization=org,
        roles=roles,
        permissions=permissions,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    limiter = request.app.state.rate_limiter
    limiter.check(
        key=f"login-ip:{_client_ip(request)}",
        limit=settings.login_rate_limit_attempts,
        window_seconds=settings.login_rate_limit_window_seconds,
    )
    limiter.check(
        key=f"login-user:{payload.email.lower()}",
        limit=settings.login_rate_limit_attempts,
        window_seconds=settings.login_rate_limit_window_seconds,
    )

    org = db.execute(select(Organization).where(Organization.slug == payload.organization_slug)).scalar_one_or_none()
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none() if org else None

    # Deliberately identical failure path regardless of which check failed,
    # so a caller cannot enumerate valid emails or organization slugs.
    if not org or not user or not user.is_active or not verify_password(payload.password, user.hashed_password):
        _record_audit(
            db,
            organization_id=org.id if org else None,
            actor_user_id=user.id if user else None,
            action="auth.login.failed",
            resource_type="session",
            metadata={"ip": _client_ip(request)},
        )
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    roles, permissions = _roles_and_permissions_for_user(db, user.id, org.id)
    if not roles:
        raise HTTPException(status_code=403, detail="User has no role assigned in this organization")

    token, expires_in = create_access_token(user_id=user.id, organization_id=org.id, roles=roles, permissions=permissions)
    _record_audit(db, organization_id=org.id, actor_user_id=user.id, action="auth.login.success", resource_type="session", metadata={"ip": _client_ip(request)})
    db.commit()

    limiter.reset(f"login-ip:{_client_ip(request)}")
    limiter.reset(f"login-user:{payload.email.lower()}")

    return TokenResponse(
        access_token=token,
        expires_in_seconds=expires_in,
        user=UserOut.model_validate(user),
        organization=org,
        roles=roles,
        permissions=permissions,
    )


@router.get("/session", response_model=dict)
def session(user: CurrentUser = Depends(get_current_user)):
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
    """Logs out an authenticated user and invalidates their bearer token via JTI revocation."""
    import time

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
    _record_audit(
        db,
        organization_id=uuid.UUID(org_id) if org_id else None,
        actor_user_id=uuid.UUID(user_id) if user_id else None,
        action="auth.logout",
        resource_type="session",
        metadata={"jti": jti},
    )
    db.commit()
    return {"message": "Logged out successfully"}
