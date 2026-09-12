"""
Tests for Ambient Clinical Scribe (Urdu/Hindi/English) and 21 CFR Part 11 Regulatory Governance
"""

try:
    import pytest
except ImportError:
    pytest = None

from app.scribe.ambient_scribe import AmbientScribeEngine, UnaniSOAPNote
from app.governance.audit_trail_engine import (
    CryptographicAuditLedger,
    Part11SignatureAuthority,
    GLOBAL_AUDIT_LEDGER,
)


def test_ambient_scribe_multilingual_detection():
    # Urdu Nastaliq
    urdu_text = "مریض کو گھٹنوں میں شدید درد اور جلن کی شکایت ہے۔"
    langs1 = AmbientScribeEngine.detect_language_markers(urdu_text)
    assert any("Urdu" in l for l in langs1)

    # Hindi Devanagari
    hindi_text = "मरीज को सीने में जलन और खट्टी डकार आ रही है।"
    langs2 = AmbientScribeEngine.detect_language_markers(hindi_text)
    assert any("Hindi" in l for l in langs2)

    # Roman Urdu / Hinglish
    roman_text = "Patient keh raha hai ke usko ghutnon me shaded dard aur thakan rehti hai."
    langs3 = AmbientScribeEngine.detect_language_markers(roman_text)
    assert any("Roman Urdu" in l for l in langs3)
    assert any("English" in l for l in langs3)


def test_ambient_scribe_entity_extraction():
    dialogue = """
    Doctor: Aap ko kya takleef hai?
    Patient: Doctor sahab, pichle 2 hafton se ghutnon me dard hai aur sinay me jalan rehti hai.
    Raat ko neend na aana bhi ek masla hai.
    """
    entities = AmbientScribeEngine.extract_unani_entities(dialogue)
    unani_terms = [e["unani_pathology"] for e in entities]

    assert "Waja-ul-Mafasil" in unani_terms
    assert any("Hurqat-ul-Meda" in t or "Hemo-e-Meda" in t for t in unani_terms)
    assert "Sahar (Insomnia)" in unani_terms


def test_ambient_scribe_soap_generation_and_invariants():
    transcript = "Patient reports acute ghutnon me dard and morning stiffness with mild fever."
    soap = AmbientScribeEngine.generate_soap_draft(
        patient_id="PAT-12345",
        transcript=transcript,
    )

    # Verify structural sections
    assert "chief_complaints" in soap.subjective
    assert "asbab_sittah_zarooriyyah" in soap.subjective
    assert "nabz_examination" in soap.objective
    assert "lisan_examination" in soap.objective
    assert "dominant_mizaj" in soap.assessment
    assert "ilaj_bil_ghiza" in soap.plan
    assert "ilaj_bil_tadbeer" in soap.plan

    # Verify Mandatory Invariant
    assert soap.safe_to_lock is False
    assert soap.status == "DRAFT_PENDING_CLINICIAN_REVIEW"
    assert soap.signed_by is None


def test_ambient_scribe_clinician_sign_and_lock():
    transcript = "Patient has severe acid reflux and sinay me jalan."
    soap = AmbientScribeEngine.generate_soap_draft(
        patient_id="PAT-999",
        transcript=transcript,
    )
    assert soap.safe_to_lock is False

    # Attempt sign-off by unauthorized role
    try:
        AmbientScribeEngine.clinician_sign_and_lock(
            soap_note=soap,
            clinician_id="USR-INTERN",
            clinician_name="John Doe",
            clinician_role="receptionist",
        )
        assert False, "Should have raised PermissionError for unauthorized role"
    except PermissionError:
        pass

    # Authorized sign-off by Hakeem/Clinician
    signed_soap = AmbientScribeEngine.clinician_sign_and_lock(
        soap_note=soap,
        clinician_id="HAK-4401",
        clinician_name="Hakim Zafarullah Khan",
        clinician_role="hakeem",
        clinician_notes="Prescription verified with Sikanjabeen Sada; safe to proceed.",
    )

    assert signed_soap.status == "CLINICALLY_VERIFIED_AND_LOCKED"
    assert signed_soap.safe_to_lock is True
    assert "Hakim Zafarullah Khan" in signed_soap.signed_by
    assert signed_soap.signed_at is not None


def test_cryptographic_audit_ledger_chain_and_tamper_detection():
    ledger = CryptographicAuditLedger()
    assert len(ledger.chain) == 1  # Genesis block
    genesis = ledger.chain[0]
    assert genesis.index == 0
    assert genesis.previous_hash == "0" * 64

    # Record two clinical events
    block1 = ledger.record_event(
        actor_id="DOC-101",
        actor_role="CLINICIAN",
        action="PRESCRIPTION_ISSUED",
        resource_type="Prescription",
        resource_id="RX-777",
        event_payload={"drug": "Majun Suranjan", "dose": "5g bid"},
    )
    assert block1.index == 1
    assert block1.previous_hash == genesis.block_hash

    block2 = ledger.record_event(
        actor_id="PHARM-202",
        actor_role="PHARMACIST",
        action="MUDABBAR_CHECK_VERIFIED",
        resource_type="InventoryBatch",
        resource_id="BATCH-009",
        event_payload={"substance": "Kuchla", "cert": "MUD-2026-X"},
    )
    assert block2.index == 2
    assert block2.previous_hash == block1.block_hash

    # Verify pristine chain
    verif = ledger.verify_chain_integrity()
    assert verif.is_valid is True
    assert verif.total_blocks == 3
    assert verif.tampered_block_index is None

    # Simulate retroactive modification (tamper) in block 1
    original_diff = block1.diff_hash
    block1.diff_hash = "f" * 64  # Corrupt the hash payload

    tampered_verif = ledger.verify_chain_integrity()
    assert tampered_verif.is_valid is False
    assert tampered_verif.tampered_block_index == 1
    assert "modified after recording" in tampered_verif.verification_message

    # Restore
    block1.diff_hash = original_diff
    restored_verif = ledger.verify_chain_integrity()
    assert restored_verif.is_valid is True


def test_part11_signature_envelope_and_verification():
    doc_payload = {
        "prescription_id": "RX-8889",
        "patient_id": "PAT-400",
        "medicines": [{"name": "Sharbat Bazoori", "qty": "200ml"}],
    }

    envelope = Part11SignatureAuthority.create_signature_envelope(
        signer_id="HAK-992",
        signer_name="Hakim Maryam Siddiqui",
        signer_role="Consultant Physician",
        document_payload=doc_payload,
        signature_meaning="Statutory Clinical Approval per 21 CFR § 11.50",
    )

    assert envelope.signer_id == "HAK-992"
    assert envelope.signer_name == "Hakim Maryam Siddiqui"
    assert envelope.cryptographic_seal is not None
    assert envelope.signature_id.startswith("SIG-")

    # Verify matching document passes
    is_valid = Part11SignatureAuthority.verify_signature_envelope(envelope, doc_payload)
    assert is_valid is True

    # Tampered document fails
    tampered_doc = dict(doc_payload)
    tampered_doc["medicines"] = [{"name": "Sharbat Bazoori", "qty": "5000ml"}]
    is_tampered_valid = Part11SignatureAuthority.verify_signature_envelope(envelope, tampered_doc)
    assert is_tampered_valid is False


def test_ambient_scribe_audio_streaming_and_synthesis():
    import base64
    audio_sample = bytes([0, 12, 45, 120] * 256)
    b64_chunk = base64.b64encode(audio_sample).decode("ascii")

    soap = AmbientScribeEngine.process_audio_stream_and_synthesize(
        patient_id="PAT-9912",
        audio_chunks_base64=[b64_chunk, b64_chunk],
        simulated_transcript="Marez ko ghutnon me dard aur khansi ki takleef hai.",
    )

    assert soap.safe_to_lock is False
    assert soap.status == "DRAFT_PENDING_CLINICIAN_REVIEW"
    assert "audio_stream_metadata" in soap.objective
    assert soap.objective["audio_stream_metadata"]["chunks_processed"] == 2
    assert soap.objective["audio_stream_metadata"]["total_bytes"] == len(audio_sample) * 2
    assert "Waja-ul-Mafasil" in soap.subjective["chief_complaints"]


def test_cryptographic_audit_ledger_merkle_anchoring():
    ledger = CryptographicAuditLedger()
    # Add blocks
    for i in range(5):
        ledger.record_event(
            actor_id=f"ACTOR-{i}",
            actor_role="CLINICIAN",
            action=f"ACTION_{i}",
            resource_type="Prescription",
            resource_id=f"RX-{i}",
            event_payload={"idx": i, "status": "active"},
        )

    # Generate first Merkle anchor
    anchor1 = ledger.generate_merkle_anchor()
    assert anchor1.anchor_id.startswith("ANC-")
    assert anchor1.from_block_index == 0
    assert anchor1.to_block_index == 5
    assert anchor1.total_blocks_anchored == 6  # Genesis (0) + 5 events
    assert anchor1.previous_anchor_hash == "0" * 64
    assert len(anchor1.merkle_root) == 64
    assert len(anchor1.signature_seal) == 64

    # Add more blocks and anchor again
    for i in range(5, 8):
        ledger.record_event(
            actor_id=f"ACTOR-{i}",
            actor_role="PHARMACIST",
            action=f"ACTION_{i}",
            resource_type="Dispensary",
            resource_id=f"DISP-{i}",
            event_payload={"idx": i},
        )
    anchor2 = ledger.generate_merkle_anchor()
    assert anchor2.from_block_index == 6
    assert anchor2.to_block_index == 8
    assert anchor2.total_blocks_anchored == 3
    assert anchor2.previous_anchor_hash == anchor1.anchor_hash

    # Verify anchor chain integrity
    assert ledger.verify_anchor_integrity() is True
    anchors = ledger.get_anchors()
    assert len(anchors) == 2

    # Verify tamper detection on anchor chain
    original_seal = anchor2.signature_seal
    anchor2.signature_seal = "0" * 64
    assert ledger.verify_anchor_integrity() is False
    anchor2.signature_seal = original_seal
    assert ledger.verify_anchor_integrity() is True

