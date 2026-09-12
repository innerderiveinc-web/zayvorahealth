"""
Tests for Patient Portal (Today View, Adherence Tracking, Secure Messaging) and Disaster Recovery Engine
"""

try:
    import pytest
except ImportError:
    pytest = None

from app.patient_portal.portal_engine import (
    PatientPortalEngine,
    DailyDoseItem,
    PatientDailySchedule,
    PatientMessage,
)
from app.dr.backup_engine import (
    DisasterRecoveryEngine,
    BackupSnapshot,
    PITRHealthCertificate,
)


def test_patient_portal_schedule_and_adherence():
    patient_id = "PAT-PORTAL-001"
    schedule = PatientPortalEngine.get_daily_schedule(patient_id)

    assert schedule.patient_id == patient_id
    assert len(schedule.doses) >= 3
    morning_dose = schedule.doses[0]
    assert morning_dose.timing_slot == "MORNING"
    assert morning_dose.status == "PENDING"
    assert len(schedule.tadbeer_reminders) > 0
    assert len(schedule.ghiza_dietary_rules) > 0

    # Log adherence for morning dose
    logged = PatientPortalEngine.log_adherence(
        patient_id=patient_id,
        dose_id=morning_dose.dose_id,
        status="TAKEN",
    )
    assert logged.status == "TAKEN"
    assert logged.logged_at_utc is not None

    # Re-fetch schedule and verify merged state
    updated_schedule = PatientPortalEngine.get_daily_schedule(patient_id)
    assert updated_schedule.compliance_score_7d > 0.0


def test_patient_portal_messaging_triage():
    patient_id = "PAT-MSG-002"

    # Routine query
    msg1 = PatientPortalEngine.send_message(
        patient_id=patient_id,
        sender_type="PATIENT",
        sender_name="Fatima Zahra",
        content="Should I take Jawarish Kamuni before or after lunch?",
    )
    assert msg1.urgency == "ROUTINE"

    # Elevated query (fever, vomiting)
    msg2 = PatientPortalEngine.send_message(
        patient_id=patient_id,
        sender_type="PATIENT",
        sender_name="Fatima Zahra",
        content="I have developed mild fever and vomiting since morning.",
    )
    assert msg2.urgency == "ELEVATED"

    # Emergency query
    msg3 = PatientPortalEngine.send_message(
        patient_id=patient_id,
        sender_type="PATIENT",
        sender_name="Fatima Zahra",
        content="Experiencing severe sudden chest pain and shortness of breath.",
    )
    assert msg3.urgency == "EMERGENCY_REDIRECT"

    thread = PatientPortalEngine.get_messages(patient_id)
    assert len(thread) >= 3


def test_disaster_recovery_snapshot_creation_and_checksum():
    snapshot = DisasterRecoveryEngine.create_and_verify_snapshot("zayvora_clinical_db")
    assert snapshot.snapshot_id.startswith("SNAP-")
    assert snapshot.status == "RESTORE_TEST_PASSED"
    assert len(snapshot.sha256_checksum) == 64
    assert snapshot.size_bytes > 0


def test_disaster_recovery_pitr_compliance():
    cert = DisasterRecoveryEngine.verify_pitr_health()
    assert cert.rto_target_seconds == 3600       # 1 hour
    assert cert.rto_estimated_seconds < 3600      # compliant (<1h)
    assert cert.rto_status == "COMPLIANT"

    assert cert.rpo_target_seconds == 300        # 5 minutes
    assert cert.rpo_actual_lag_seconds < 300     # compliant (<5m)
    assert cert.rpo_status == "COMPLIANT"

    assert cert.overall_dr_readiness == "DISASTER_RECOVERY_CERTIFIED_2035"


def test_bhashini_multilingual_voice_synthesizer():
    """Verify Issue ENH-02: Bhashini Indic TTS speech synthesis and localized scripts across Urdu, Hindi, Telugu, and English."""
    from app.patient_portal.voice_synthesizer import BhashiniVoiceSynthesizer
    import base64

    # 1. Test Urdu synthesis
    urdu_res = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id="PAT-TTS-001",
        medication_name="Jawarish Kamuni",
        dosage_display="5 grams (1 teaspoon)",
        timing_slot="Morning",
        intake_vehicle="Lukewarm water",
        language="ur",
    )
    assert urdu_res["language"] == "ur"
    assert "محترم مریض" in urdu_res["script_text"]
    assert "نیم گرم پانی" in urdu_res["script_text"]
    assert urdu_res["audio_format"].startswith("audio/wav")
    assert urdu_res["audio_data_uri"].startswith("data:audio/wav;base64,")
    # Decode audio and check RIFF/WAVE header
    b64_part = urdu_res["audio_data_uri"].split(",")[1]
    raw_audio = base64.b64decode(b64_part)
    assert raw_audio[:4] == b"RIFF"
    assert raw_audio[8:12] == b"WAVE"
    assert len(urdu_res["clinical_verification_hash"]) == 64

    # 2. Test Hindi synthesis
    hi_res = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id="PAT-TTS-001",
        medication_name="Khamira Gaozaban",
        dosage_display="6g paste",
        timing_slot="Bedtime",
        intake_vehicle="Milk",
        language="hi",
    )
    assert hi_res["language"] == "hi"
    assert "प्रिय मरीज" in hi_res["script_text"]
    assert "दूध" in hi_res["script_text"]

    # 3. Test Telugu synthesis
    te_res = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id="PAT-TTS-001",
        medication_name="Sharbat Bazoori",
        dosage_display="20 ml",
        timing_slot="Morning",
        intake_vehicle="Lukewarm water",
        language="te",
    )
    assert te_res["language"] == "te"
    assert "ప్రియమైన రోగి" in te_res["script_text"]
    assert "తీసుకోండి" in te_res["script_text"]


def test_patient_portal_voice_router_integration():
    """Verify Issue ENH-02: Patient portal voice prompt synthesis with verified clinical posology."""
    from app.patient_portal.voice_synthesizer import BhashiniVoiceSynthesizer

    payload = {
        "patient_id": "PAT-VOICE-100",
        "medication_name": "Majun Suranjan",
        "dosage_display": "5g paste",
        "timing_slot": "Morning",
        "intake_vehicle": "Lukewarm water",
        "language": "ur",
    }
    res = BhashiniVoiceSynthesizer.synthesize_medication_prompt(
        patient_id=payload["patient_id"],
        medication_name=payload["medication_name"],
        dosage_display=payload["dosage_display"],
        timing_slot=payload["timing_slot"],
        intake_vehicle=payload["intake_vehicle"],
        language=payload["language"],
    )
    assert res["patient_id"] == "PAT-VOICE-100"
    assert res["language"] == "ur"
    assert "Majun Suranjan" in res["script_text"]
    assert "محترم مریض" in res["script_text"]
    assert res["audio_data_uri"].startswith("data:audio/wav;base64,")
    assert res["bhashini_pipeline"]["status"] == "SYNTHESIZED_SUCCESS"


