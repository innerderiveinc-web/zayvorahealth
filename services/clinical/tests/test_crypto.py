from __future__ import annotations

from app.core.crypto import decrypt_phi, encrypt_phi


def test_encrypt_decrypt_phi_roundtrip():
    key = "super-secret-phi-encryption-key-32b"
    plaintext = "+91 98765 43210"

    encrypted = encrypt_phi(plaintext, key)
    assert encrypted != plaintext
    assert encrypted.startswith("enc:")

    decrypted = decrypt_phi(encrypted, key)
    assert decrypted == plaintext


def test_encrypt_phi_with_empty_key_passthrough():
    plaintext = "+91 98765 43210"
    encrypted = encrypt_phi(plaintext, "")
    assert encrypted == plaintext


def test_decrypt_phi_with_unencrypted_plaintext():
    raw = "+91 98765 43210"
    decrypted = decrypt_phi(raw, "any-key")
    assert decrypted == raw


def test_encrypt_decrypt_none_returns_none():
    assert encrypt_phi(None, "key") is None
    assert decrypt_phi(None, "key") is None
