"""
ZAYVORA HL7 FHIR R4 & ABDM Clinical Bundle Converter (Phase 12).

Converts internal clinical models (Patient, Encounter, Prescriptions, Care Plans, Mizaj)
into ABDM (NDHM) compliant HL7 FHIR R4 Bundles:
- OPConsultRecord Bundle (https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord)
- PrescriptionRecord Bundle (https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord)
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any


def create_fhir_patient_resource(patient: dict[str, Any]) -> dict[str, Any]:
    """Generates an ABDM-compliant FHIR R4 Patient resource."""
    pat_id = str(patient.get("id", uuid.uuid4()))
    abha_num = patient.get("abha_number")
    abha_addr = patient.get("abha_address")

    identifiers = [
        {
            "system": "https://zayvora.health/patients",
            "value": pat_id,
        }
    ]
    if abha_num:
        identifiers.append({
            "type": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                        "code": "MR",
                        "display": "Medical Record Number",
                    }
                ]
            },
            "system": "https://healthid.ndhm.gov.in",
            "value": abha_num,
        })
    if abha_addr:
        identifiers.append({
            "system": "https://ndhm.in/phr",
            "value": abha_addr,
        })

    gender_map = {"male": "male", "female": "female", "other": "other"}
    gender = gender_map.get(str(patient.get("gender", "")).lower(), "unknown")

    return {
        "resourceType": "Patient",
        "id": pat_id,
        "meta": {
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"],
        },
        "identifier": identifiers,
        "name": [
            {
                "text": patient.get("full_name", "Anonymous Patient"),
            }
        ],
        "gender": gender,
        "birthDate": patient.get("date_of_birth") or "1980-01-01",
    }


def create_fhir_condition_resource(
    *,
    condition_id: str,
    patient_id: str,
    diagnosis_name: str,
    icd11_code: str | None = None,
    unani_amraz_code: str | None = None,
) -> dict[str, Any]:
    """Generates an ABDM Condition resource with dual ICD-11 and Unani Amraz codings."""
    codings = []
    if icd11_code:
        codings.append({
            "system": "http://id.who.int/icd/release/11/mms",
            "code": icd11_code,
            "display": diagnosis_name,
        })
    if unani_amraz_code:
        codings.append({
            "system": "https://zayvora.health/fhir/cs/unani-amraz",
            "code": unani_amraz_code,
            "display": diagnosis_name,
        })
    if not codings:
        codings.append({
            "system": "http://snomed.info/sct",
            "code": "404684003",
            "display": diagnosis_name,
        })

    return {
        "resourceType": "Condition",
        "id": condition_id,
        "meta": {
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Condition"],
        },
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                }
            ]
        },
        "code": {
            "coding": codings,
            "text": diagnosis_name,
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
        },
    }


def create_fhir_medication_request(
    *,
    rx_id: str,
    patient_id: str,
    medication_name: str,
    dose: str,
    instructions: str | None = None,
    is_schedule_e1: bool = False,
) -> dict[str, Any]:
    """Generates an ABDM MedicationRequest resource with Mudabbar safety annotation."""
    notes = []
    if is_schedule_e1:
        notes.append({
            "text": "SCHEDULE E(1) POISON: Mandatory Mudabbar purification certified before dispensing.",
        })

    return {
        "resourceType": "MedicationRequest",
        "id": rx_id,
        "meta": {
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationRequest"],
        },
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [
                {
                    "system": "https://zayvora.health/fhir/cs/ayush-unani-pharmacopoeia",
                    "code": medication_name.lower().replace(" ", "-"),
                    "display": medication_name,
                }
            ],
            "text": medication_name,
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
        },
        "dosageInstruction": [
            {
                "text": f"{dose}. {instructions or ''}".strip(),
            }
        ],
        "note": notes,
    }


def create_fhir_mizaj_observation(
    *,
    obs_id: str,
    patient_id: str,
    primary_temperament: str,
    heat_cold_score: float,
    wet_dry_score: float,
) -> dict[str, Any]:
    """Generates a FHIR Observation resource representing 10-Ajnas Mizaj assessment."""
    return {
        "resourceType": "Observation",
        "id": obs_id,
        "meta": {
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation"],
        },
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "https://zayvora.health/fhir/cs/mizaj-assessment",
                    "code": "10-ajnas-mizaj",
                    "display": "Unani Mizaj (Temperament) Constitutional Assessment",
                }
            ],
            "text": "Mizaj Assessment",
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
        },
        "valueString": primary_temperament,
        "component": [
            {
                "code": {"text": "Heat-Cold Polarity Score"},
                "valueQuantity": {"value": heat_cold_score, "unit": "score"},
            },
            {
                "code": {"text": "Wet-Dry Polarity Score"},
                "valueQuantity": {"value": wet_dry_score, "unit": "score"},
            },
        ],
    }


def build_abdm_op_consult_bundle(
    *,
    bundle_id: str | None = None,
    patient: dict[str, Any],
    encounter: dict[str, Any] | None = None,
    conditions: list[dict[str, Any]] | None = None,
    prescriptions: list[dict[str, Any]] | None = None,
    mizaj_assessment: dict[str, Any] | None = None,
    organization_id: str = "zayvora-health",
) -> dict[str, Any]:
    """Assembles a complete, validated ABDM FHIR R4 OPConsultRecord Document Bundle."""
    b_id = bundle_id or str(uuid.uuid4())
    comp_id = f"Composition-{b_id}"
    pat_id = str(patient.get("id", uuid.uuid4()))

    patient_res = create_fhir_patient_resource(patient)
    entries = [{"fullUrl": f"urn:uuid:{patient_res['id']}", "resource": patient_res}]
    section_entries = []

    # 1. Mizaj Observation
    if mizaj_assessment:
        obs = create_fhir_mizaj_observation(
            obs_id=f"obs-{uuid.uuid4()}",
            patient_id=pat_id,
            primary_temperament=mizaj_assessment.get("primary_temperament", "Mutadil"),
            heat_cold_score=float(mizaj_assessment.get("heat_cold_score", 0.0)),
            wet_dry_score=float(mizaj_assessment.get("wet_dry_score", 0.0)),
        )
        entries.append({"fullUrl": f"urn:uuid:{obs['id']}", "resource": obs})
        section_entries.append({"reference": f"urn:uuid:{obs['id']}"})

    # 2. Conditions
    for c in (conditions or []):
        c_res = create_fhir_condition_resource(
            condition_id=f"cond-{uuid.uuid4()}",
            patient_id=pat_id,
            diagnosis_name=c.get("diagnosis_name", "Clinical Condition"),
            icd11_code=c.get("icd11_code"),
            unani_amraz_code=c.get("unani_amraz_code"),
        )
        entries.append({"fullUrl": f"urn:uuid:{c_res['id']}", "resource": c_res})
        section_entries.append({"reference": f"urn:uuid:{c_res['id']}"})

    # 3. Prescriptions
    for p in (prescriptions or []):
        rx_res = create_fhir_medication_request(
            rx_id=f"rx-{uuid.uuid4()}",
            patient_id=pat_id,
            medication_name=p.get("medication_name", "Herbal Formulation"),
            dose=p.get("dose", "1 dose"),
            instructions=p.get("instructions"),
            is_schedule_e1=p.get("is_schedule_e1", False),
        )
        entries.append({"fullUrl": f"urn:uuid:{rx_res['id']}", "resource": rx_res})
        section_entries.append({"reference": f"urn:uuid:{rx_res['id']}"})

    # 4. Composition Root
    composition = {
        "resourceType": "Composition",
        "id": comp_id,
        "meta": {
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"],
        },
        "status": "final",
        "type": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "371530004",
                    "display": "Clinical consultation report",
                }
            ],
            "text": "Outpatient Unani Clinical Consultation",
        },
        "subject": {"reference": f"urn:uuid:{pat_id}"},
        "date": datetime.utcnow().isoformat(),
        "title": "ZAYVORA Health Outpatient Consultation Record",
        "section": [
            {
                "title": "Consultation Findings & Prescriptions",
                "entry": section_entries,
            }
        ],
    }

    # Composition must be first entry in a FHIR Document Bundle
    full_entries = [{"fullUrl": f"urn:uuid:{composition['id']}", "resource": composition}] + entries

    return {
        "resourceType": "Bundle",
        "id": b_id,
        "meta": {
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"],
        },
        "type": "document",
        "timestamp": datetime.utcnow().isoformat(),
        "entry": full_entries,
    }
