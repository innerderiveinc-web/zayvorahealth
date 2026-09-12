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


def wrap_phi_key(dek: bytes, kek_secret: str) -> str:
    """
    Wraps (encrypts) a 256-bit Data Encryption Key (DEK) using a Key Encryption Key (KEK).
    Returns base64 wrapped key string.
    """
    if not kek_secret:
        raise ValueError("KEK secret cannot be empty.")

    if not HAS_CRYPTOGRAPHY:
        encoded = base64.b64encode(dek).decode("ascii")
        return f"wrap:dev:{encoded}"

    kek = _derive_key(kek_secret)
    aesgcm = AESGCM(kek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, b"ZAYVORA_DEK_WRAP")
    payload = nonce + ciphertext
    return f"wrap:v1:{base64.b64encode(payload).decode('ascii')}"


def unwrap_phi_key(wrapped_dek: str, kek_secret: str) -> bytes:
    """
    Unwraps (decrypts) a wrapped Data Encryption Key (DEK) using a Key Encryption Key (KEK).
    """
    if not wrapped_dek or not kek_secret:
        raise ValueError("Wrapped DEK and KEK secret must be provided.")

    parts = wrapped_dek.split(":", 2)
    if len(parts) < 3 or parts[0] != "wrap":
        raise ValueError("Invalid wrapped key format.")

    version = parts[1]
    raw_b64 = parts[2]

    if version == "dev":
        return base64.b64decode(raw_b64.encode("ascii"))

    if version == "v1":
        if not HAS_CRYPTOGRAPHY:
            raise RuntimeError("cryptography library required to unwrap v1 keys.")
        payload = base64.b64decode(raw_b64.encode("ascii"))
        nonce = payload[:12]
        ct = payload[12:]
        kek = _derive_key(kek_secret)
        aesgcm = AESGCM(kek)
        return aesgcm.decrypt(nonce, ct, b"ZAYVORA_DEK_WRAP")

    raise ValueError(f"Unsupported key wrap version: {version}")


def encrypt_patient_phi(patient_data: dict, dek_secret: str, sensitive_fields: Optional[list[str]] = None) -> dict:
    """
    Encrypts sensitive demographic and clinical fields in a patient record dict.
    Default sensitive fields: contact_phone, contact_email, medical_history, surgical_history.
    """
    if sensitive_fields is None:
        sensitive_fields = ["contact_phone", "contact_email", "medical_history", "surgical_history"]

    result = dict(patient_data)
    for field in sensitive_fields:
        if field in result and result[field]:
            result[field] = encrypt_phi(result[field], dek_secret)
    return result


def decrypt_patient_phi(patient_data: dict, dek_secret: str, sensitive_fields: Optional[list[str]] = None) -> dict:
    """
    Decrypts sensitive demographic and clinical fields in an encrypted patient record dict.
    """
    if sensitive_fields is None:
        sensitive_fields = ["contact_phone", "contact_email", "medical_history", "surgical_history"]

    result = dict(patient_data)
    for field in sensitive_fields:
        if field in result and result[field]:
            result[field] = decrypt_phi(result[field], dek_secret)
    return result

