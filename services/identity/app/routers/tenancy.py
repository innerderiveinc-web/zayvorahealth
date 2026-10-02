from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth_dependency import CurrentUser, get_current_user, require_permission
from app.core.config import get_settings
from app.core.database import get_db
from app.core.permissions_catalogue import provision_owner_role
from app.models.identity import Organization, Permission, Role, User
from app.schemas.identity import OrganizationCreate, OrganizationOut, RoleCreate, RoleOut


router = APIRouter(prefix="/api/v1", tags=["tenancy"])


@router.post("/organizations", response_model=OrganizationOut, status_code=201)
def create_organization(payload: OrganizationCreate, request: Request, db: Session = Depends(get_db)):
    """Bootstrap endpoint that creates a tenant organization.
    Protected by X-Bootstrap-Token when ZAYVORA_IDENTITY_BOOTSTRAP_TOKEN is configured.
    If no bootstrap token is configured, requires SUPER_ADMIN role.
    Auto-provisions an 'Owner' role with the full baseline permission set
    (see core/permissions_catalogue.py) so the very first user who signs
    up against this organization isn't stuck in a chicken-and-egg
    situation where role creation itself requires being logged in.
    """
    settings = get_settings()
    if settings.bootstrap_token:
        token = request.headers.get("X-Bootstrap-Token", "")
        if token != settings.bootstrap_token:
            raise HTTPException(status_code=403, detail="Invalid or missing X-Bootstrap-Token")
    else:
        # No bootstrap token configured — require SUPER_ADMIN JWT instead
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required to create organizations")
        try:
            from app.core.auth_dependency import get_current_user as _get_cu
            current_user = _get_cu(request)
            if "SUPER_ADMIN" not in current_user.roles:
                raise HTTPException(status_code=403, detail="Only SUPER_ADMIN can create organizations")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    existing = db.execute(select(Organization).where(Organization.slug == payload.slug)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="An organization with this slug already exists")
    org = Organization(name=payload.name, slug=payload.slug, tier=payload.tier)
    db.add(org)
    db.flush()
    provision_owner_role(db, org.id)
    db.commit()
    db.refresh(org)
    return org


@router.get("/organizations/{slug}", response_model=OrganizationOut)
def get_organization(slug: str, db: Session = Depends(get_db)):
    org = db.execute(select(Organization).where(Organization.slug == slug)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.post("/roles", response_model=RoleOut, status_code=201)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    user=Depends(require_permission("role.manage")),
):
    org = db.execute(select(Organization).where(Organization.slug == payload.organization_slug)).scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    existing = db.execute(
        select(Role).where(Role.organization_id == org.id, Role.name == payload.name)
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="A role with this name already exists for this organization")

    permissions = []
    for code in payload.permission_codes:
        perm = db.execute(select(Permission).where(Permission.code == code)).scalar_one_or_none()
        if not perm:
            raise HTTPException(status_code=422, detail=f"Unknown permission code: {code}")
        permissions.append(perm)

    role = Role(organization_id=org.id, name=payload.name, description=payload.description, permissions=permissions)
    db.add(role)
    db.commit()
    db.refresh(role)
    return RoleOut(id=role.id, name=role.name, description=role.description, permission_codes=[p.code for p in role.permissions])


@router.get("/organizations", response_model=list[OrganizationOut], summary="List all tenant organizations")
def list_organizations(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """List organizations. SUPER_ADMIN sees all; other admins see only their own org."""
    if "SUPER_ADMIN" in current_user.roles:
        orgs = db.execute(select(Organization).order_by(Organization.created_at.desc())).scalars().all()
    else:
        if not current_user.organization_id:
            raise HTTPException(status_code=403, detail="Organization context required")
        orgs = db.execute(
            select(Organization).where(Organization.id == current_user.organization_id)
        ).scalars().all()
    return orgs
