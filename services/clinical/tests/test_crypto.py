from __future__ import annotations

from app.core.crypto import (
    decrypt_phi,
    encrypt_phi,
    wrap_phi_key,
    unwrap_phi_key,
    encrypt_patient_phi,
    decrypt_patient_phi,
)


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


def test_envelope_key_wrap_and_unwrap_roundtrip():
    kek = "vault-master-key-encryption-key-2035"
    dek = b"01234567890123456789012345678901"  # 32 bytes DEK

    wrapped = wrap_phi_key(dek, kek)
    assert wrapped.startswith("wrap:")
    assert wrapped != dek.decode("latin1", errors="ignore")

    unwrapped = unwrap_phi_key(wrapped, kek)
    assert unwrapped == dek


def test_patient_phi_dict_field_encryption_and_decryption():
    dek = "clinical-service-dek-key-string"
    patient = {
        "id": "PAT-001",
        "mrn": "MRN-100",
        "full_name": "Fatima Begum",
        "contact_phone": "+91 98765 11223",
        "contact_email": "fatima.begum@example.com",
        "medical_history": "Chronic Ziabetus Shakari (Diabetes Type 2)",
    }

    encrypted_patient = encrypt_patient_phi(patient, dek)
    assert encrypted_patient["id"] == "PAT-001"
    assert encrypted_patient["full_name"] == "Fatima Begum"
    assert encrypted_patient["contact_phone"].startswith("enc:")
    assert encrypted_patient["contact_email"].startswith("enc:")
    assert encrypted_patient["medical_history"].startswith("enc:")

    decrypted_patient = decrypt_patient_phi(encrypted_patient, dek)
    assert decrypted_patient["contact_phone"] == "+91 98765 11223"
    assert decrypted_patient["contact_email"] == "fatima.begum@example.com"
    assert decrypted_patient["medical_history"] == "Chronic Ziabetus Shakari (Diabetes Type 2)"

