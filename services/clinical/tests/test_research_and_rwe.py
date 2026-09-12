from app.research.deidentifier import (
    anonymize_patient_for_research,
    anonymize_patient_id,
    classify_therapeutic_outcome,
)


def test_anonymize_patient_id_salted_hmac():
    pid1 = "p-12345"
    pid2 = "p-67890"

    sub1 = anonymize_patient_id(pid1)
    sub2 = anonymize_patient_id(pid2)

    assert sub1.startswith("SUBJ-")
    assert sub2.startswith("SUBJ-")
    assert sub1 != sub2
    # Deterministic with same salt
    assert sub1 == anonymize_patient_id(pid1)


def test_deidentify_patient_record_hipaa_safe_harbor():
    patient = {
        "id": "p-100",
        "full_name": "Hakim Zayd",
        "mrn": "MRN-12345",
        "phone": "+919876543210",
        "address": "123 Old Delhi Bazar",
        "age": 94,  # Over 89 years old
        "gender": "male",
        "mizaj_temperament": "Damwi",
    }
    encounters = [
        {"started_at": "2026-01-01T10:00:00Z", "encounter_type": "consultation", "chief_complaint": "Joint pain"},
        {"started_at": "2026-01-15T10:00:00Z", "encounter_type": "followup", "chief_complaint": "Improved joint pain"},
    ]
    prescriptions = [
        {"created_at": "2026-01-01T10:30:00Z", "medication_name": "Majun Suranjan", "dose": "5g"},
    ]

    record = anonymize_patient_for_research(patient, encounters, prescriptions)

    assert record["subject_id"].startswith("SUBJ-")
    assert "Hakim Zayd" not in str(record)
    assert "MRN-12345" not in str(record)
    assert "+919876543210" not in str(record)

    # HIPAA age capping check (must be 90 years)
    assert record["demographics"]["age_group"] == "90 years"

    # Study relative days check
    encs = record["study_timeline"]["encounters"]
    assert len(encs) == 2
    assert encs[0]["study_day"] == 0
    assert encs[1]["study_day"] == 14

    rxs = record["study_timeline"]["prescriptions"]
    assert len(rxs) == 1
    assert rxs[0]["study_day_prescribed"] == 0


def test_classify_therapeutic_outcome():
    # 1. Kamil (Complete)
    res1 = classify_therapeutic_outcome(
        baseline_severity_score=80.0,
        followup_severity_score=10.0,
        mizaj_equilibrium_restored=True,
    )
    assert res1["response_category"] == "COMPLETE_RESPONSE"
    assert "Kamil" in res1["clinical_outcome"]
    assert res1["symptom_alleviation_percentage"] == 87.5

    # 2. Juz'i (Partial)
    res2 = classify_therapeutic_outcome(
        baseline_severity_score=70.0,
        followup_severity_score=35.0,
    )
    assert res2["response_category"] == "PARTIAL_RESPONSE"
    assert "Juz'i" in res2["clinical_outcome"]

    # 3. Ghair Mu'athir (Non-response)
    res3 = classify_therapeutic_outcome(
        baseline_severity_score=60.0,
        followup_severity_score=50.0,
    )
    assert res3["response_category"] == "NON_RESPONSE"
    assert "Ghair Mu'athir" in res3["clinical_outcome"]

    # 4. Intikas (Relapse / Worsened)
    res4 = classify_therapeutic_outcome(
        baseline_severity_score=50.0,
        followup_severity_score=65.0,
    )
    assert res4["response_category"] == "DETERIORATED"
    assert "Intikas" in res4["clinical_outcome"]
    assert res4["symptom_alleviation_percentage"] == -30.0
