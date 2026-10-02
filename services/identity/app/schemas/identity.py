from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9-]+$")
    tier: str = Field(default="clinic")


class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    slug: str
    tier: str
    is_active: bool
    created_at: datetime


class UserSignup(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=12, max_length=200)
    organization_slug: str
    role_name: str = Field(default="Doctor")


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    email: EmailStr
    full_name: str
    is_active: bool
    mfa_enabled: bool
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    organization_slug: str
    mfa_code: str | None = Field(
        default=None,
        description="6-digit TOTP code. Required for clinical staff roles when MFA is enabled.",
        min_length=6,
        max_length=6,
    )


class TokenResponse(BaseModel):
    """Response body returned by /login, /signup, and /refresh endpoints."""

    access_token: str
    refresh_token: str | None = Field(
        default=None,
        description="Opaque refresh token. Present on login/signup and token rotation.",
    )
    token_type: str = "bearer"
    expires_in_seconds: int
    user: UserOut
    organization: OrganizationOut
    roles: list[str]
    permissions: list[str]
    mfa_required: bool = Field(
        default=False,
        description="True when MFA is required for this role but mfa_code was not supplied. "
                    "Client must prompt user for TOTP and re-submit.",
    )


class RoleCreate(BaseModel):
    organization_slug: str
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(default="", max_length=300)
    permission_codes: list[str] = Field(default_factory=list)


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    description: str
    permission_codes: list[str] = Field(default_factory=list)
