from __future__ import annotations

from fastapi import Depends, HTTPException, Request

from app.core.security import decode_access_token


class CurrentUser:
    def __init__(self, user_id: str, organization_id: str, roles: list[str], permissions: list[str]):
        self.user_id = user_id
        self.organization_id = organization_id
        self.roles = roles
        self.permissions = permissions


def get_current_user(request: Request) -> CurrentUser:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth_header.removeprefix("Bearer ").strip()
    try:
        payload = decode_access_token(token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    return CurrentUser(
        user_id=payload["sub"],
        organization_id=payload["org"],
        roles=list(payload.get("roles") or []),
        permissions=list(payload.get("permissions") or []),
    )


def require_permission(permission_code: str):
    """Dependency factory: require_permission('patient.create') gates a
    route to only users whose role grants that specific permission.

    This is the RBAC enforcement point referenced across Master Build
    Prompt v4.0 (§2 human clinical authority, §49 security). Every
    state-changing route in every service should be gated like this —
    no route should rely on the frontend hiding a button as its only
    protection.
    """

    def _dependency(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if permission_code not in user.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Missing required permission: {permission_code}",
            )
        return user

    return _dependency
