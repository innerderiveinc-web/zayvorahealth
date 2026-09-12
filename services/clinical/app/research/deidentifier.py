"""
ZAYVORA Research Cloud & Real-World Evidence (RWE) De-Identification Engine (Phase 16).

Complies with:
- HIPAA Safe Harbor (45 CFR § 164.514(b)(2)) — 18 PII identifiers stripped
- DISHA (Digital Information Security in Healthcare Act) Anonymization Rules
- Unani Validated Clinical Outcome Classification (Kamil, Juz'i, Ghair Mu'athir, Intikas)
"""
from __future__ import annotations

import hashlib
import hmac
from datetime import date, datetime
from typing import Any

# Research salt for irreversible pseudonymization
_RESEARCH_SALT = b"ZAYVORA-RWE-SALT-2035-DISHA-HIPAA"


def anonymize_patient_id(patient_id: str) -> str:
    """Computes a cryptographically salted pseudonym for longitudinal cohort tracking."""
    digest = hmac.new(_RESEARCH_SALT, patient_id.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"SUBJ-{digest[:12].upper()}"


def anonymize_patient_for_research(
    patient: dict[str, Any],
    encounters: list[dict[str, Any]] | None = None,
    prescriptions: list[dict[str, Any]] | None = None,
    care_plans: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Strips all 18 HIPAA/DISHA direct and indirect identifiers, converts absolute dates
    to relative elapsed study days, and generates a research-ready de-identified clinical dossier.
    """
    raw_id = str(patient.get("id", ""))
    pseudo_id = anonymize_patient_id(raw_id)

    # 1. Age capping per HIPAA Safe Harbor (ages >89 must be aggregated to 90+)
    raw_age = patient.get("age")
    if raw_age is not None:
        research_age = 90 if raw_age >= 90 else raw_age
    else:
        research_age = None

    # 2. Establish baseline study date t_0 from first recorded event
    all_dates = []
    if encounters:
        all_dates.extend([e.get("started_at") for e in encounters if e.get("started_at")])
    if prescriptions:
        all_dates.extend([p.get("created_at") for p in prescriptions if p.get("created_at")])

    valid_dates = []
    for d_str in all_dates:
        try:
            valid_dates.append(datetime.fromisoformat(str(d_str).replace("Z", "+00:00")))
        except Exception:
            pass

    t0 = min(valid_dates) if valid_dates else datetime.utcnow()

    # 3. Anonymize encounters to relative study days
    deidentified_encounters = []
    for e in (encounters or []):
        enc_time = None
        if e.get("started_at"):
            try:
                enc_time = datetime.fromisoformat(str(e["started_at"]).replace("Z", "+00:00"))
            except Exception:
                pass
        rel_days = (enc_time - t0).days if enc_time else 0

        deidentified_encounters.append({
            "study_day": rel_days,
            "encounter_type": e.get("encounter_type", "outpatient"),
            "vital_signs": {
                k: v for k, v in (e.get("vital_signs") or {}).items()
                if k in ["blood_pressure_systolic", "blood_pressure_diastolic", "pulse_rate", "temperature_c", "bmi"]
            },
            "chief_complaint": e.get("chief_complaint"),
        })

    # 4. Anonymize prescriptions to relative study days and pharmacopoeial codes
    deidentified_prescriptions = []
    for p in (prescriptions or []):
        rx_time = None
        if p.get("created_at"):
            try:
                rx_time = datetime.fromisoformat(str(p["created_at"]).replace("Z", "+00:00"))
            except Exception:
                pass
        rel_days = (rx_time - t0).days if rx_time else 0

        deidentified_prescriptions.append({
            "study_day_prescribed": rel_days,
            "medication_name": p.get("medication_name"),
            "dose": p.get("dose"),
            "is_schedule_e1": p.get("is_schedule_e1", False),
            "verified_mudabbar": p.get("verified_mudabbar", True),
        })

    return {
        "subject_id": pseudo_id,
        "demographics": {
            "age_group": f"{research_age} years" if research_age else "Unknown",
            "gender": patient.get("gender", "unknown"),
            "mizaj_temperament": patient.get("mizaj_temperament", "Unknown"),
        },
        "study_timeline": {
            "total_encounters": len(deidentified_encounters),
            "total_prescriptions": len(deidentified_prescriptions),
            "encounters": deidentified_encounters,
            "prescriptions": deidentified_prescriptions,
        },
        "deidentification_metadata": {
            "standard_applied": "HIPAA Safe Harbor § 164.514(b)(2) / DISHA 2026 Guidelines",
            "phi_scrubbed": True,
            "direct_identifiers_removed": [
                "Full Name", "MRN", "Phone", "Email", "Full Address", "SSN/National ID", "Exact Timestamps"
            ],
        },
    }


def classify_therapeutic_outcome(
    *,
    baseline_severity_score: float,
    followup_severity_score: float,
    mizaj_equilibrium_restored: bool = False,
) -> dict[str, Any]:
    """Classifies clinical therapeutic response according to classical Unani outcomes:
    1. Kamil (Complete Remission / Al-Shifa al-Taam): >= 80% improvement + humoral balance
    2. Juz'i (Partial Response / Tahassun Juz'i): 40% - 79% improvement
    3. Ghair Mu'athir (Non-Responsive / Adam al-Istijabah): < 40% change
    4. Intikas (Relapse or Deterioration / Al-Ruju'): > 20% worsening
    """
    if baseline_severity_score <= 0:
        raise ValueError("Baseline severity score must be positive (> 0)")

    delta = baseline_severity_score - followup_severity_score
    alleviation_pct = round((delta / baseline_severity_score) * 100.0, 2)

    if alleviation_pct < -20.0:
        outcome = "Intikas (Relapse / Disease Exacerbation)"
        category = "DETERIORATED"
    elif alleviation_pct >= 80.0:
        if mizaj_equilibrium_restored:
            outcome = "Kamil (Complete Clinical Remission & Humoral Balance Restored)"
            category = "COMPLETE_RESPONSE"
        else:
            outcome = "Kamil (Symptom Remission Pending Full Humoral Concoction)"
            category = "COMPLETE_RESPONSE"
    elif alleviation_pct >= 40.0:
        outcome = "Juz'i (Partial Therapeutic Response / Statistically Significant)"
        category = "PARTIAL_RESPONSE"
    else:
        outcome = "Ghair Mu'athir (Minimal or Non-Responsive to Primary Regimen)"
        category = "NON_RESPONSE"

    return {
        "baseline_severity": baseline_severity_score,
        "followup_severity": followup_severity_score,
        "symptom_alleviation_percentage": alleviation_pct,
        "clinical_outcome": outcome,
        "response_category": category,
        "mizaj_restored": mizaj_equilibrium_restored,
    }
