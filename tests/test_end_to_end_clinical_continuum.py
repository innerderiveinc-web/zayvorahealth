"""
ZAYVORA HEALTH™ — End-to-End Complete Clinical Care Continuum Integration Test
Demonstrates the unified clinical journey from ambient acoustic scribing
to Mizaj assessment, organ-axis biomarker cross-talk, non-delegable AI consultation,
Nuskha Badal compilation, Schedule E(1) purification gate, FEFO inventory locking,
ICH E2B pharmacovigilance, 21 CFR Part 11 Merkle anchoring, wearable webhooks,
multilingual Bhashini voiceover, and ABDM FHIR consent exchange.
"""

import sys
import os

def switch_service(service_name: str):
    """Isolates service imports to prevent cross-service 'app' namespace shadowing."""
    abs_service = os.path.abspath(f"services/{service_name}")
    for s in ["services/clinical", "services/therapeutic", "services/knowledge", "services/ai", "services/identity", "services/gateway"]:
        p = os.path.abspath(s)
        while p in sys.path:
            sys.path.remove(p)
    sys.path.insert(0, abs_service)
    to_del = [k for k in list(sys.modules.keys()) if k == "app" or k.startswith("app.")]
    for k in to_del:
        del sys.modules[k]


def test_full_clinical_continuum_end_to_end():
    # =========================================================================
    # STEP 1: Ambient Clinical Scribe & Acoustic Entity Extraction (Clinical)
    # =========================================================================
    switch_service("clinical")
    from app.scribe.ambient_scribe import AmbientScribeEngine

    dialogue = """
    Hakeem: Aap ko kya takleef pesh aa rahi hai?
    Patient: Doctor sahab, pichle 3 hafton se ghutnon me dard hai, soozish rehti hai
    aur subah uthte waqt jism me akad rehti hai. Sinay me jalan bhi rehti hai.
    """
    detected_langs = AmbientScribeEngine.detect_language_markers(dialogue)
    assert any("Urdu" in l or "Roman Urdu" in l for l in detected_langs)

    entities = AmbientScribeEngine.extract_unani_entities(dialogue)
    unani_terms = [e["unani_pathology"] for e in entities]
    assert "Waja-ul-Mafasil" in unani_terms
    assert any("Hurqat-ul-Meda" in t or "Hemo-e-Meda" in t for t in unani_terms)

    soap_draft = AmbientScribeEngine.generate_soap_draft(
        patient_id="PAT-E2E-CONTINUUM-001",
        transcript=dialogue,
    )
    assert soap_draft.patient_id == "PAT-E2E-CONTINUUM-001"
    assert "chief_complaints" in soap_draft.subjective
    assert soap_draft.safe_to_lock is False
    assert soap_draft.status == "DRAFT_PENDING_CLINICIAN_REVIEW"

    # =========================================================================
    # STEP 2: 10-Ajnas Longitudinal Mizaj Assessment (Geriatric Sinn-e-Shaikhukhat)
    # =========================================================================
    from app.engines.mizaj_assessor import calculate_mizaj_assessment

    mizaj_assessment = calculate_mizaj_assessment(
        answers={
            "malmas": "cold_dry",
            "lahm_shahm": "emaciated_bony",
            "ashar": "dry_curly",
            "laun": "chalky_pale",
            "hayat_aza": "narrow_sunken",
            "kayfiyyat_infial": "anxious_brooding",
            "naum_yaqzah": "insomnia_fragmented",
            "harkat_sukoon": "slow_lethargic",
            "fuzalaat": "cold_pale",
            "afal_aza": "sluggish_slow",
        },
        age_category="geriatric",
    )
    assert mizaj_assessment["age_category"] == "geriatric"
    assert "Shaikhukhat" in mizaj_assessment["asnan_profile_name"]
    assert mizaj_assessment["calibration_applied"] is True

    # =========================================================================
    # STEP 3: Organ-Axis Evidence Biomarker Cross-Talk Evaluation
    # =========================================================================
    from app.engines.organ_axis_engine import run_complete_organ_axis_analysis

    axis_eval = run_complete_organ_axis_analysis(
        complaint="Severe headache after food with nausea, acid reflux, and epigastric bloating",
        associated_symptoms=["burning epigastric pain"],
        duration_days=21,
        symptom_acuity="moderate",
        inflammatory_signs=True,
        temperament_context={"primary_temperament": "Barid"},
    )
    assert axis_eval["organ_axes"]["primary_axis"]["id"] == "meda-amaa"
    assert axis_eval["organ_axes"]["secondary_axis"]["id"] == "dimagh-asab"
    assert "primary_axis_biomarkers" in axis_eval["biomarker_cross_talk"]
    assert len(axis_eval["biomarker_cross_talk"]["cross_talk_indicators"]) > 0

    # =========================================================================
    # STEP 4: AI Hakeem Sahab Structured Validation & Prescribing Lock (AI)
    # =========================================================================
    switch_service("ai")
    from app.engines.response_validator import validate_response_structure, validate_statutory_disclaimer
    from app.providers.fake_provider import DEFAULT_WELL_FORMED_RESPONSE

    validation_errors = validate_response_structure(DEFAULT_WELL_FORMED_RESPONSE)
    assert validation_errors == []
    assert validate_statutory_disclaimer(DEFAULT_WELL_FORMED_RESPONSE) is True

    bypass_attempt = DEFAULT_WELL_FORMED_RESPONSE.replace(
        "Yes — this is advisory only and has not been reviewed by a qualified practitioner.",
        "Proceed with dispensing immediately without doctor review."
    )
    assert "STATUTORY_DISCLAIMER_INVALID" in validate_response_structure(bypass_attempt)

    # =========================================================================
    # STEP 5: Nuskha Compiler & Badal Substitution Posology (Therapeutic)
    # =========================================================================
    switch_service("therapeutic")
    from app.engines.nuskha_compiler import substitute_badal_with_posology

    badal_substitution = substitute_badal_with_posology(
        original_ingredient_name="Suranjan Talkh",
        original_dose_mg=250.0,
        badal_name="Suranjan Shireen",
        patient_context={"age": 68},
    )
    assert badal_substitution["original_ingredient"] == "Suranjan Talkh"
    assert badal_substitution["badal_substitute"] == "Suranjan Shireen"
    assert badal_substitution["potency_ratio"] == 2.0
    assert badal_substitution["calculated_badal_dose_mg"] == 375.0

    # =========================================================================
    # STEP 6: Dispensary FEFO Concurrency Allocation & Schedule E(1) Gate
    # =========================================================================
    from app.engines.dispensary_engine import allocate_fefo_batches, MudabbarDispenseBlockError

    # 6A: Uncertified Schedule E(1) batch must raise MudabbarDispenseBlockError
    uncertified_batches = [
        {
            "id": "batch-unsafe-01",
            "batch_number": "BAT-UNSAFE-01",
            "expiry_date": "2026-11-30",
            "available_quantity": 10.0,
            "qc_release_status": "released",
            "mudabbar_certified": False,
        }
    ]
    try:
        allocate_fefo_batches(batches=uncertified_batches, requested_quantity=2.0, is_schedule_e1=True)
        assert False, "Expected MudabbarDispenseBlockError was not raised!"
    except MudabbarDispenseBlockError as err:
        assert "DISPENSE GATE BLOCKED" in str(err)

    # 6B: Certified Mudabbar batch with FEFO ordering must succeed
    certified_batches = [
        {
            "id": "batch-uuid-001",
            "batch_number": "BAT-EXP-LATER",
            "expiry_date": "2026-12-31",
            "available_quantity": 10.0,
            "qc_release_status": "released",
            "mudabbar_certified": True,
        },
        {
            "id": "batch-uuid-002",
            "batch_number": "BAT-EXP-SOONER",
            "expiry_date": "2026-11-15",
            "available_quantity": 5.0,
            "qc_release_status": "released",
            "mudabbar_certified": True,
        },
    ]
    allocation = allocate_fefo_batches(batches=certified_batches, requested_quantity=4.0, is_schedule_e1=True)
    assert allocation["total_allocated"] == 4.0
    assert allocation["mudabbar_verified"] is True
    assert allocation["allocations"][0]["batch_number"] == "BAT-EXP-SOONER"
    assert allocation["allocations"][0]["allocated_quantity"] == 4.0

    # =========================================================================
    # STEP 7: Pharmacovigilance ICH E2B(R3) ICSR XML & CIOMS-I Export
    # =========================================================================
    from app.pharmacovigilance.e2b_exporter import export_ich_e2b_r3_xml

    report_data = {
        "patient_id": "PAT-E2E-CONTINUUM-001",
        "suspected_agent": "Majun Suranjan",
        "adverse_reaction_description": "waja-ul-mafasil pain with joint swelling",
        "latency_hours": 24,
        "dechallenge_performed": True,
        "dechallenge_outcome": "improved",
    }
    icsr_report = export_ich_e2b_r3_xml(report_data)
    assert "<?xml" in icsr_report
    assert "ichicsr" in icsr_report
    assert "Majun Suranjan" in icsr_report

    # =========================================================================
    # STEP 8: 21 CFR Part 11 Cryptographic Merkle Root Audit Anchoring (Clinical)
    # =========================================================================
    switch_service("clinical")
    from app.governance.audit_trail_engine import (
        CryptographicAuditLedger,
        Part11SignatureAuthority,
    )

    doc_payload = {
        "prescription_id": "RX-E2E-001",
        "patient_id": "PAT-E2E-CONTINUUM-001",
        "medicines": [{"name": "Suranjan Shireen (Badal)", "qty": "375mg"}],
    }
    envelope = Part11SignatureAuthority.create_signature_envelope(
        signer_id="HAK-E2E-786",
        signer_name="Dr. Hakeem Tariq Ahmad",
        signer_role="Consultant Unani Physician",
        document_payload=doc_payload,
        signature_meaning="Statutory Clinical Prescribing Responsibility per 21 CFR § 11.50",
    )
    assert envelope.signer_id == "HAK-E2E-786"
    assert envelope.cryptographic_seal is not None
    assert Part11SignatureAuthority.verify_signature_envelope(envelope, doc_payload) is True

    ledger = CryptographicAuditLedger()
    ledger.record_event(
        actor_id="HAK-E2E-786",
        actor_role="CLINICIAN",
        action="SIGN_PRESCRIPTION",
        resource_type="Prescription",
        resource_id="RX-E2E-001",
        event_payload=doc_payload,
    )
    merkle_anchor = ledger.generate_merkle_anchor()
    assert merkle_anchor.anchor_id.startswith("ANC-")
    assert len(merkle_anchor.merkle_root) == 64

    # =========================================================================
    # STEP 9: Continuous Wearables Webhook Ingestion (Apple HealthKit & Unani)
    # =========================================================================
    from app.wearables.wearable_engine import WearableIngestionEngine

    hk_samples = [
        {"type": "HKQuantityTypeIdentifierHeartRateVariabilitySDNN", "value": 60.0},
        {"type": "HKQuantityTypeIdentifierRestingHeartRate", "value": 66.0},
        {"type": "HKCategoryTypeIdentifierSleepAnalysis", "value": 7.5},
        {"type": "HKQuantityTypeIdentifierOxygenSaturation", "value": 98.0},
        {"type": "HKQuantityTypeIdentifierStepCount", "value": 7500.0},
    ]
    wearable_sample = WearableIngestionEngine.normalize_apple_healthkit(
        samples=hk_samples,
        patient_id="PAT-E2E-CONTINUUM-001",
        device_model="Apple Watch Ultra",
    )
    summary = WearableIngestionEngine.ingest_sample(wearable_sample)
    assert summary.patient_id == "PAT-E2E-CONTINUUM-001"
    assert summary.quwwat_hayawaniyyah_index > 0.5
    assert summary.naum_yaqzah_score >= 0.8

    # =========================================================================
    # STEP 10: Multilingual Bhashini Regional Voice Synthesis
    # =========================================================================
    from app.patient_portal.voice_synthesizer import BhashiniVoiceSynthesizer

    voice_prompt_ur = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id="PAT-E2E-CONTINUUM-001",
        medication_name="Suranjan Shireen",
        dosage_display="375mg",
        timing_slot="Morning",
        intake_vehicle="Lukewarm water",
        language="ur",
    )
    assert voice_prompt_ur["language"] == "ur"
    assert "محترم مریض" in voice_prompt_ur["script_text"]
    assert "Suranjan Shireen" in voice_prompt_ur["script_text"]
    assert voice_prompt_ur["audio_data_uri"].startswith("data:audio/wav;base64,")

    voice_prompt_hi = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id="PAT-E2E-CONTINUUM-001",
        medication_name="Suranjan Shireen",
        dosage_display="375mg",
        timing_slot="Morning",
        intake_vehicle="Lukewarm water",
        language="hi",
    )
    assert voice_prompt_hi["language"] == "hi"
    assert "प्रिय मरीज" in voice_prompt_hi["script_text"]

    # =========================================================================
    # STEP 11: ABDM Gateway Milestone 1-3 Discovery, Consent & FHIR Push
    # =========================================================================
    from app.interop.abdm_gateway import ABDMGateway

    gw = ABDMGateway(
        client_id="zayvora-hip-sandbox-client",
        client_secret="sbx-client-secret-9921",
        gateway_url="https://dev.abdm.gov.in/gateway",
        live_mode=False,
    )
    # Milestone 1
    verif = gw.verify_abha("14-2200-3300-4400")
    assert verif["valid"] is True

    # Milestone 2
    consent = gw.request_consent(
        patient_abha="14-2200-3300-4400",
        hiu_id="ZAYVORA-CLINIC-01",
        purpose_code="CAREMGT",
        hi_types=["OPConsultation", "Prescription"],
        date_range_days=90,
    )
    assert consent["status"] == "REQUESTED"
    cid = consent["consent_request_id"]
    granted = gw.grant_consent_mock(cid)
    assert granted["status"] == "GRANTED"

    # Milestone 3
    push = gw.push_health_data_packet(
        transaction_id="TX-E2E-CONTINUUM-01",
        patient_abha="14-2200-3300-4400",
        encrypted_fhir_packets=[{"resourceType": "Bundle", "type": "document"}],
    )
    assert push["status"] == "TRANSFER_SUCCESS"
    assert push["packets_count"] == 1

    print("\n✓ COMPLETE CLINICAL CONTINUUM VERIFIED: All 11 Clinical & Regulatory Milestones Passed.")


if __name__ == "__main__":
    test_full_clinical_continuum_end_to_end()
