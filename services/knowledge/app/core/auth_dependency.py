from __future__ import annotations

import jwt
from fastapi import Depends, HTTPException, Request

from app.core.config import get_settings


class CurrentUser:
    def __init__(self, user_id: str, organization_id: str, roles: list[str], permissions: list[str]):
        self.user_id = user_id
        self.organization_id = organization_id
        self.roles = roles
        self.permissions = permissions


def _decode_token(token: str) -> dict:
    settings = get_settings()
    payload = None

    if settings.jwt_public_key_pem.strip():
        try:
            payload = jwt.decode(token, settings.jwt_public_key_pem, algorithms=["RS256"])
        except Exception:
            payload = None

    if payload is None:
        secret = settings.jwt_secret or "development-only-insecure-secret-do-not-use-in-production"
        payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm, "HS256", "RS256"])

    jti = payload.get("jti")
    if jti and settings.redis_url:
        try:
            import redis

            r = redis.from_url(settings.redis_url)
            if r.exists(f"revoked:{jti}"):
                raise HTTPException(status_code=401, detail="Token has been revoked")
        except HTTPException:
            raise
        except Exception:
            pass

    return payload


def get_current_user(request: Request) -> CurrentUser:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth_header.removeprefix("Bearer ").strip()
    try:
        payload = _decode_token(token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    return CurrentUser(
        user_id=payload["sub"],
        organization_id=payload["org"],
        roles=list(payload.get("roles") or []),
        permissions=list(payload.get("permissions") or []),
    )


def require_permission(permission_code: str):
    def _dependency(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if permission_code not in user.permissions:
            raise HTTPException(status_code=403, detail=f"Missing required permission: {permission_code}")
        return user

    return _dependency
