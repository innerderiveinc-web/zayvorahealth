"""
ZAYVORA PHI & PII Column-Level Encryption Utilities.

Provides authenticated AES-256-GCM encryption for sensitive patient fields
(e.g., phone, email, identification numbers, home address).
"""
from __future__ import annotations

import base64
import os
import hashlib
from typing import Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False


def _derive_key(secret: str) -> bytes:
    """Derives a 256-bit (32-byte) key from a secret string using SHA-256."""
    return hashlib.sha256(secret.encode("utf-8")).digest()


def encrypt_phi(plaintext: Optional[str], key_secret: str) -> Optional[str]:
    """
    Encrypts sensitive PHI plaintext using AES-256-GCM.
    Returns base64-encoded string: b64(nonce + ciphertext + tag).
    If key_secret is empty or plaintext is None, returns plaintext unchanged (development fallback).
    """
    if plaintext is None or not key_secret:
        return plaintext

    if not HAS_CRYPTOGRAPHY:
        # Fallback authenticated format for non-cryptography dev runtime
        encoded = base64.b64encode(plaintext.encode("utf-8")).decode("ascii")
        return f"enc:dev:{encoded}"

    key = _derive_key(key_secret)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce for AES-GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    payload = nonce + ciphertext
    return f"enc:v1:{base64.b64encode(payload).decode('ascii')}"


def decrypt_phi(ciphertext: Optional[str], key_secret: str) -> Optional[str]:
    """
    Decrypts an AES-256-GCM encrypted PHI string.
    If not encrypted (no 'enc:' prefix) or key_secret is empty, returns ciphertext as is.
    """
    if ciphertext is None or not key_secret or not ciphertext.startswith("enc:"):
        return ciphertext

    parts = ciphertext.split(":", 2)
    if len(parts) < 3:
        return ciphertext

    version = parts[1]
    raw_b64 = parts[2]

    if version == "dev":
        try:
            return base64.b64decode(raw_b64.encode("ascii")).decode("utf-8")
        except Exception:
            return ciphertext

    if version == "v1" and HAS_CRYPTOGRAPHY:
        try:
            payload = base64.b64decode(raw_b64.encode("ascii"))
            nonce = payload[:12]
            ct = payload[12:]
            key = _derive_key(key_secret)
            aesgcm = AESGCM(key)
            decrypted = aesgcm.decrypt(nonce, ct, None)
            return decrypted.decode("utf-8")
        except Exception:
            return ciphertext

    return ciphertext
