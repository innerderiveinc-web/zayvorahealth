from __future__ import annotations

import base64
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.core.config import get_settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ephemeral in-memory revocation blocklist: jti -> expiration timestamp
_revoked_tokens: dict[str, float] = {}

# Cached keypair for RS256
_rsa_private_key: Any = None
_rsa_public_key: Any = None
_rsa_public_pem: str = ""


def _get_rsa_keys() -> tuple[Any, Any, str]:
    global _rsa_private_key, _rsa_public_key, _rsa_public_pem
    if _rsa_private_key is not None:
        return _rsa_private_key, _rsa_public_key, _rsa_public_pem

    settings = get_settings()
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        if settings.jwt_private_key_pem.strip():
            _rsa_private_key = serialization.load_pem_private_key(
                settings.jwt_private_key_pem.encode("utf-8"), password=None
            )
            _rsa_public_key = _rsa_private_key.public_key()
        else:
            # Auto-generate a 2048-bit RSA keypair
            _rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            _rsa_public_key = _rsa_private_key.public_key()

        _rsa_public_pem = _rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        return _rsa_private_key, _rsa_public_key, _rsa_public_pem
    except Exception:
        return None, None, ""


def _int_to_base64url(val: int) -> str:
    val_bytes = val.to_bytes((val.bit_length() + 7) // 8, byteorder="big")
    return base64.urlsafe_b64encode(val_bytes).rstrip(b"=").decode("ascii")


def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)


def revoke_token(jti: str, expires_at: float) -> None:
    settings = get_settings()
    if settings.redis_url:
        try:
            import redis

            r = redis.from_url(settings.redis_url)
            ttl = max(1, int(expires_at - time.time()))
            r.setex(f"revoked:{jti}", ttl, "1")
        except Exception:
            pass
    _revoked_tokens[jti] = expires_at


def is_token_revoked(jti: str | None) -> bool:
    if not jti:
        return False
    settings = get_settings()
    if settings.redis_url:
        try:
            import redis

            r = redis.from_url(settings.redis_url)
            if r.exists(f"revoked:{jti}"):
                return True
        except Exception:
            pass
    now = time.time()
    if jti in _revoked_tokens:
        if _revoked_tokens[jti] > now:
            return True
        _revoked_tokens.pop(jti, None)
    return False


def get_jwks() -> dict[str, Any]:
    priv, pub, _ = _get_rsa_keys()
    if pub is not None:
        numbers = pub.public_numbers()
        return {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "alg": "RS256",
                    "kid": "zayvora-identity-key-1",
                    "n": _int_to_base64url(numbers.n),
                    "e": _int_to_base64url(numbers.e),
                }
            ]
        }
    return {
        "keys": [
            {
                "kty": "oct",
                "use": "sig",
                "alg": "HS256",
                "kid": "zayvora-identity-hmac-key",
            }
        ]
    }


def create_access_token(
    *,
    user_id: uuid.UUID,
    organization_id: uuid.UUID,
    roles: list[str],
    permissions: list[str],
) -> tuple[str, int]:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires_in = settings.access_token_ttl_seconds
    token_id = str(uuid.uuid4())
    payload = {
        "iss": "zayvora-identity",
        "jti": token_id,
        "sub": str(user_id),
        "org": str(organization_id),
        "roles": roles,
        "permissions": permissions,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
    }

    priv_key, _, _ = _get_rsa_keys()
    if priv_key is not None and settings.jwt_algorithm == "RS256":
        headers = {"kid": "zayvora-identity-key-1"}
        token = jwt.encode(payload, priv_key, algorithm="RS256", headers=headers)
    else:
        secret = settings.jwt_secret or "development-only-insecure-secret-do-not-use-in-production"
        token = jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)

    return token, expires_in


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    _, pub_key, _ = _get_rsa_keys()

    payload = None
    if pub_key is not None and settings.jwt_algorithm == "RS256":
        try:
            payload = jwt.decode(token, pub_key, algorithms=["RS256"])
        except Exception:
            payload = None

    if payload is None:
        secret = settings.jwt_secret or "development-only-insecure-secret-do-not-use-in-production"
        payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm, "HS256"])

    jti = payload.get("jti")
    if is_token_revoked(jti):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return payload

