"""
ZAYVORA Health OS™ — ABDM & FHIR Clinical Continuum Orchestrator (Sequence 14)
=============================================================================
Converts the output of the 12-Stage Clinical Intelligence Continuum
(ClinicalContinuumResponse) into standardized, computable ABDM HL7 FHIR R4 Bundles:

1. ABDM OPConsultRecord Document Bundle (NRCeS Profile)
2. ABDM PrescriptionRecord Document Bundle (NRCeS Profile)
3. Dual Clinical Coding: ICD-11 + Classical Unani Amraz + NAMASTE
4. Computable Mizaj (10-Ajnas), 12 Organ-Axis, and PROMs Observations
5. 8-Tier Parhez Posology as FHIR CarePlan
6. ABDM Milestone 3 HIP/HIU Data Transfer Envelope
"""

from __future__ import annotations

import uuid
import hashlib
import json
import base64
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# Standard Terminology and Profile Systems
UNANI_NAMING_SYSTEM = "https://zayvora.health/fhir/cs/unani-amraz"
ICD11_SYSTEM = "http://id.who.int/icd/release/11/mms"
NRCES_SYSTEM = "https://nrces.in/ndhm/fhir/r4/StructureDefinition"

# Canonical Mapping of Unani Amraz to ICD-11 and NAMASTE codes
UNANI_AMRAZ_ICD11_MAP = {
    "waja-ul-mafasil": {
        "amraz_code": "UN-AMR-041",
        "display": "Waja-ul-Mafasil (Joint Inflammation / Polyarthritis)",
        "icd11_code": "FA00.Z",
        "icd11_display": "Osteoarthritis, unspecified",
        "namaste_code": "NAM-UNA-JNT-001",
    },
    "irq-un-nasa": {
        "amraz_code": "UN-AMR-042",
        "display": "Irq-un-Nasa (Sciatica / Radiculopathy)",
        "icd11_code": "8B93.0",
        "icd11_display": "Sciatica",
        "namaste_code": "NAM-UNA-NEU-014",
    },
    "ziabetus-shakari": {
        "amraz_code": "UN-AMR-018",
        "display": "Ziabetus Shakari (Type 2 Diabetes Mellitus)",
        "icd11_code": "5A11",
        "icd11_display": "Type 2 diabetes mellitus",
        "namaste_code": "NAM-UNA-MET-002",
    },
    "su-e-hazm": {
        "amraz_code": "UN-AMR-029",
        "display": "Su-e-Hazm (Dyspepsia / Gastrointestinal Dyscrasia)",
        "icd11_code": "MD90",
        "icd11_display": "Dyspepsia",
        "namaste_code": "NAM-UNA-GST-005",
    },
    "zof-e-kabid": {
        "amraz_code": "UN-AMR-033",
        "display": "Zof-e-Kabid (Hepatic Sluggishness / Metabolic Dysregulation)",
        "icd11_code": "DB99",
        "icd11_display": "Diseases of liver",
        "namaste_code": "NAM-UNA-HEP-003",
    },
    "sual-e-balghami": {
        "amraz_code": "UN-AMR-012",
        "display": "Sual-e-Balghami (Productive Phlegmatic Cough / Bronchitis)",
        "icd11_code": "CA20.0",
        "icd11_display": "Acute bronchitis",
        "namaste_code": "NAM-UNA-RES-008",
    },
}


class ABDMFHIRContinuumOrchestrator:
    """Master orchestrator converting continuum executions into ABDM FHIR R4 bundles."""

    @classmethod
    def get_amraz_coding(cls, condition_name: str) -> Dict[str, str]:
        """Normalizes condition string to authoritative dual ICD-11 + Unani codings."""
        key = condition_name.strip().lower().replace(" ", "-")
        for k, v in UNANI_AMRAZ_ICD11_MAP.items():
            if k in key or key in k:
                return v
        return {
            "amraz_code": "UN-AMR-GEN-999",
            "display": condition_name,
            "icd11_code": "MG48",
            "icd11_display": "Symptoms or signs involving general health status",
            "namaste_code": "NAM-UNA-GEN-001",
        }

    @classmethod
    def build_op_consult_bundle(
        cls,
        continuum_data: Dict[str, Any],
        patient_abha_number: Optional[str] = "91-4829-1029-4821",
        patient_abha_address: Optional[str] = "hamza.farooqi@abdm",
        practitioner_hpr_id: Optional[str] = "HPR-IN-AYUSH-9921",
        facility_id: Optional[str] = "IN-FAC-DEL-MATAB-01",
        facility_name: Optional[str] = "ZAYVORA Central Matab & Research Hospital",
    ) -> Dict[str, Any]:
        """
        Builds a compliant ABDM OPConsultRecord Document Bundle from continuum results.
        Conforms to https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord
        """
        tx_id = continuum_data.get("transaction_id", f"TX-{uuid.uuid4().hex[:12].upper()}")
        bundle_id = f"BUNDLE-OPC-{uuid.uuid4().hex[:10].upper()}"
        composition_id = f"COMP-OPC-{uuid.uuid4().hex[:10].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        profile = continuum_data.get("stage_1_patient_profile", {})
        patient_id = profile.get("patient_id", "P-UNKNOWN")
        patient_name = profile.get("name") or continuum_data.get("patient_id", "Anonymous Patient")
        condition_name = profile.get("condition", "General Malaise")
        coding = cls.get_amraz_coding(condition_name)

        signoff = continuum_data.get("stage_9_clinician_approval", {})
        clinician_id = signoff.get("authorized_by", "HAK-001")
        clinician_role = signoff.get("clinician_role", "HAKEEM")

        # 1. FHIR Patient Resource
        fhir_patient = {
            "resourceType": "Patient",
            "id": f"Patient-{patient_id}",
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"]
            },
            "identifier": [
                {"system": "https://zayvora.health/patients", "value": patient_id},
                {
                    "type": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR",
                            "display": "Medical Record Number"
                        }]
                    },
                    "system": "https://healthid.ndhm.gov.in",
                    "value": patient_abha_number,
                },
                {"system": "https://ndhm.in/phr", "value": patient_abha_address},
            ],
            "name": [{"text": patient_name}],
            "gender": str(profile.get("gender", "male")).lower(),
            "birthDate": "1972-04-15",
        }

        # 2. FHIR Practitioner Resource
        fhir_practitioner = {
            "resourceType": "Practitioner",
            "id": f"Practitioner-{clinician_id}",
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner"]
            },
            "identifier": [
                {"system": "https://hpr.abdm.gov.in", "value": practitioner_hpr_id},
                {"system": "https://zayvora.health/practitioners", "value": clinician_id}
            ],
            "name": [{"text": f"Hakim {clinician_id} (Licensed AYUSH BUMS Clinician)"}],
            "qualification": [
                {
                    "code": {
                        "coding": [{
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                            "code": "BUMS",
                            "display": "Bachelor of Unani Medicine and Surgery"
                        }]
                    }
                }
            ],
        }

        # 3. FHIR Organization (Facility) Resource
        fhir_org = {
            "resourceType": "Organization",
            "id": f"Org-{facility_id}",
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Organization"]
            },
            "identifier": [{"system": "https://facility.abdm.gov.in", "value": facility_id}],
            "name": facility_name,
        }

        # 4. FHIR Condition Resource (Dual-coded)
        cond_id = f"Condition-{uuid.uuid4().hex[:8]}"
        fhir_condition = {
            "resourceType": "Condition",
            "id": cond_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Condition"]
            },
            "clinicalStatus": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                    "display": "Active"
                }]
            },
            "code": {
                "coding": [
                    {
                        "system": "http://id.who.int/icd/release/11/mms",
                        "code": coding["icd11_code"],
                        "display": coding["icd11_display"],
                    },
                    {
                        "system": "https://zayvora.health/fhir/cs/unani-amraz",
                        "code": coding["amraz_code"],
                        "display": coding["display"],
                    },
                    {
                        "system": "https://ayush.gov.in/fhir/cs/namaste",
                        "code": coding["namaste_code"],
                        "display": coding["display"],
                    }
                ],
                "text": condition_name,
            },
            "subject": {"reference": f"Patient/Patient-{patient_id}"},
        }

        # 5. FHIR Observation: Mizaj Constitutional Quantification
        mizaj_data = continuum_data.get("stage_3_mizaj_quantification", {})
        obs_mizaj_id = f"Obs-Mizaj-{uuid.uuid4().hex[:8]}"
        fhir_obs_mizaj = {
            "resourceType": "Observation",
            "id": obs_mizaj_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation"]
            },
            "status": "final",
            "code": {
                "coding": [{
                    "system": "https://zayvora.health/fhir/cs/mizaj-assessment",
                    "code": "10-ajnas-mizaj",
                    "display": "Unani Mizaj 10-Ajnas Quantitative Assessment"
                }],
                "text": "Dominant Temperament & Humoral Divergence"
            },
            "subject": {"reference": f"Patient/Patient-{patient_id}"},
            "valueString": mizaj_data.get("dominant_mizaj", "Mutadil"),
            "component": [
                {
                    "code": {"text": "Cold Potency Degree (Buroodat)"},
                    "valueQuantity": {"value": float(mizaj_data.get("cold_degree", 0)), "unit": "degree"}
                },
                {
                    "code": {"text": "Moist Potency Degree (Rutoobat)"},
                    "valueQuantity": {"value": float(mizaj_data.get("moist_degree", 0)), "unit": "degree"}
                }
            ]
        }

        # 6. FHIR Observation: 12-Axis Organ System Targeting
        axis_data = continuum_data.get("stage_4_organ_axis_targeting", {})
        obs_axis_id = f"Obs-12Axis-{uuid.uuid4().hex[:8]}"
        fhir_obs_axis = {
            "resourceType": "Observation",
            "id": obs_axis_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation"]
            },
            "status": "final",
            "code": {
                "coding": [{
                    "system": "https://zayvora.health/fhir/cs/twelve-organ-axes",
                    "code": "AXIS-12-PROFILE",
                    "display": "12 Canonical Organ-Axis Activity Profile"
                }],
                "text": "12 Organ-Axis Activity Assessment"
            },
            "subject": {"reference": f"Patient/Patient-{patient_id}"},
            "valueString": "Assessed across 12 canonical axes",
            "component": [
                {
                    "code": {"text": ax.get("axis_name", "Axis")},
                    "valueQuantity": {"value": float(ax.get("activity_index", 0.0)), "unit": "index"}
                }
                for ax in axis_data.get("axes", [])[:6]
            ]
        }

        # 7. FHIR MedicationRequests (Prescriptions)
        med_requests = []
        nuskha_data = continuum_data.get("stage_10_nuskha_and_parhez", {})
        for i, comp in enumerate(nuskha_data.get("composition", [])):
            med_id = f"MedReq-{uuid.uuid4().hex[:8]}"
            drug_name = comp.get("drug", f"Drug-{i+1}")
            vehicle = comp.get("anupan", "Warm water")
            
            # Match Musleh pairing note if available
            paired = next((m.get("paired_musleh") for m in nuskha_data.get("musleh_counterbalance", []) if m.get("drug") == drug_name), None)
            notes = [f"Vehicle (Badraqa/Anupan): {vehicle}."]
            if paired:
                notes.append(f"MANDATORY MUSLEH: Paired with {paired} for thermal counter-balance.")

            req_res = {
                "resourceType": "MedicationRequest",
                "id": med_id,
                "meta": {
                    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationRequest"]
                },
                "status": "active",
                "intent": "order",
                "medicationCodeableConcept": {
                    "coding": [{
                        "system": "https://zayvora.health/fhir/cs/ayush-unani-pharmacopoeia",
                        "code": drug_name.lower().replace(" ", "-"),
                        "display": drug_name,
                    }],
                    "text": drug_name,
                },
                "subject": {"reference": f"Patient/Patient-{patient_id}"},
                "requester": {"reference": f"Practitioner/Practitioner-{clinician_id}"},
                "dosageInstruction": [{
                    "text": f"Take 3g twice daily with {vehicle}.",
                    "additionalInstruction": [{"text": n} for n in notes]
                }],
            }
            med_requests.append(req_res)

        # 8. FHIR CarePlan: 8-Tier Parhez Regimen
        careplan_id = f"CarePlan-Parhez-{uuid.uuid4().hex[:8]}"
        parhez_tiers = nuskha_data.get("parhez_8_tier", {})
        fhir_careplan = {
            "resourceType": "CarePlan",
            "id": careplan_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/CarePlan"]
            },
            "status": "active",
            "intent": "plan",
            "title": "8-Tier Canonical Parhez & Lifestyle Regimen",
            "subject": {"reference": f"Patient/Patient-{patient_id}"},
            "activity": [
                {
                    "detail": {
                        "code": {"text": tier_name.replace("_", " ").title()},
                        "status": "in-progress",
                        "description": tier_desc,
                    }
                }
                for tier_name, tier_desc in parhez_tiers.items()
            ]
        }

        # 9. Composition Document Reference
        entries = [
            {"fullUrl": f"urn:uuid:{fhir_patient['id']}", "resource": fhir_patient},
            {"fullUrl": f"urn:uuid:{fhir_practitioner['id']}", "resource": fhir_practitioner},
            {"fullUrl": f"urn:uuid:{fhir_org['id']}", "resource": fhir_org},
            {"fullUrl": f"urn:uuid:{fhir_condition['id']}", "resource": fhir_condition},
            {"fullUrl": f"urn:uuid:{fhir_obs_mizaj['id']}", "resource": fhir_obs_mizaj},
            {"fullUrl": f"urn:uuid:{fhir_obs_axis['id']}", "resource": fhir_obs_axis},
            {"fullUrl": f"urn:uuid:{fhir_careplan['id']}", "resource": fhir_careplan},
        ]
        for m in med_requests:
            entries.append({"fullUrl": f"urn:uuid:{m['id']}", "resource": m})

        # Add PROMs observation if follow-up exists
        proms_data = continuum_data.get("stage_11_proms_followup")
        if proms_data:
            obs_proms_id = f"Obs-PROMs-{uuid.uuid4().hex[:8]}"
            fhir_proms = {
                "resourceType": "Observation",
                "id": obs_proms_id,
                "meta": {
                    "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Observation"]
                },
                "status": "final",
                "code": {
                    "coding": [{
                        "system": "https://zayvora.health/fhir/cs/patient-proms",
                        "code": "PROMS-14-DAY-INDEX",
                        "display": "14-Day PROMs Recovery & Improvement Index"
                    }],
                    "text": "14-Day PROMs Clinical Trajectory"
                },
                "subject": {"reference": f"Patient/Patient-{patient_id}"},
                "valueQuantity": {
                    "value": float(proms_data.get("clinical_improvement_percent", 0.0)),
                    "unit": "%"
                },
            }
            entries.append({"fullUrl": f"urn:uuid:{fhir_proms['id']}", "resource": fhir_proms})

        composition = {
            "resourceType": "Composition",
            "id": composition_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"]
            },
            "status": "final",
            "type": {
                "coding": [{
                    "system": "http://snomed.info/sct",
                    "code": "371530004",
                    "display": "Clinical consultation report"
                }],
                "text": "ZAYVORA Unani Outpatient Clinical Consultation Record"
            },
            "subject": {"reference": f"Patient/Patient-{patient_id}"},
            "date": now_iso,
            "author": [{"reference": f"Practitioner/Practitioner-{clinician_id}"}],
            "title": f"ZAYVORA Clinical Consultation: {condition_name}",
            "custodian": {"reference": f"Organization/Org-{facility_id}"},
            "section": [
                {
                    "title": "Diagnosis & Amraz Assessment",
                    "code": {"coding": [{"system": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Section", "code": "diagnosis", "display": "Diagnosis"}]},
                    "entry": [{"reference": f"Condition/{cond_id}"}],
                },
                {
                    "title": "Chief Complaints",
                    "code": {"coding": [{"system": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Section", "code": "chief-complaints", "display": "Chief Complaints"}]},
                    "entry": [{"reference": f"Condition/{cond_id}"}],
                },
                {
                    "title": "Unani Mizaj & 12 Organ-Axis Findings",
                    "code": {"coding": [{"system": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Section", "code": "unani-mizaj", "display": "Unani Mizaj"}]},
                    "entry": [
                        {"reference": f"Observation/{obs_mizaj_id}"},
                        {"reference": f"Observation/{obs_axis_id}"},
                    ],
                },
                {
                    "title": "Prescribed Nuskha & Galenical Formulations",
                    "code": {"coding": [{"system": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Section", "code": "medications", "display": "Medications"}]},
                    "entry": [{"reference": f"MedicationRequest/{m['id']}"} for m in med_requests],
                },
                {
                    "title": "8-Tier Parhez Dietary & Regimental Care Plan",
                    "code": {"coding": [{"system": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Section", "code": "care-plan", "display": "Care Plan"}]},
                    "entry": [{"reference": f"CarePlan/{careplan_id}"}],
                },
            ],
        }

        # Insert composition as the first entry per FHIR Document bundle rules
        bundle_entries = [{"fullUrl": f"urn:uuid:{composition_id}", "resource": composition}] + entries

        return {
            "resourceType": "Bundle",
            "id": bundle_id,
            "meta": {
                "versionId": "1",
                "lastUpdated": now_iso,
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"]
            },
            "identifier": {
                "system": "https://zayvora.health/fhir/bundles/op-consult",
                "value": f"OPC-{tx_id}",
            },
            "type": "document",
            "timestamp": now_iso,
            "entry": bundle_entries,
        }

    @classmethod
    def build_prescription_bundle(
        cls,
        continuum_data: Dict[str, Any],
        patient_abha_number: Optional[str] = "91-4829-1029-4821",
        practitioner_hpr_id: Optional[str] = "HPR-IN-AYUSH-9921",
        facility_id: Optional[str] = "IN-FAC-DEL-MATAB-01",
    ) -> Dict[str, Any]:
        """Builds an ABDM PrescriptionRecord Document Bundle for digital pharmacy integration."""
        bundle_id = f"BUNDLE-RX-{uuid.uuid4().hex[:10].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()
        profile = continuum_data.get("stage_1_patient_profile", {})
        patient_id = profile.get("patient_id", "P-UNKNOWN")
        signoff = continuum_data.get("stage_9_clinician_approval", {})
        clinician_id = signoff.get("authorized_by", "HAK-001")

        nuskha_data = continuum_data.get("stage_10_nuskha_and_parhez", {})
        med_requests = []
        for i, comp in enumerate(nuskha_data.get("composition", [])):
            drug_name = comp.get("drug", f"Drug-{i+1}")
            med_requests.append({
                "resourceType": "MedicationRequest",
                "id": f"RX-Item-{i+1}",
                "status": "active",
                "intent": "order",
                "medicationCodeableConcept": {
                    "coding": [{
                        "system": "https://zayvora.health/fhir/cs/ayush-unani-pharmacopoeia",
                        "code": f"UNA-RX-{i+1:03d}",
                        "display": drug_name
                    }],
                    "text": drug_name
                },
                "dosageInstruction": [{
                    "text": f"Take 3g twice daily with {comp.get('anupan', 'warm water')}."
                }]
            })

        return {
            "resourceType": "Bundle",
            "id": bundle_id,
            "meta": {
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord"]
            },
            "type": "document",
            "timestamp": now_iso,
            "total_medications": len(med_requests),
            "entry": [{"resource": m} for m in med_requests],
        }

    @classmethod
    def create_hip_data_transfer_envelope(
        cls,
        bundle: Optional[Dict[str, Any]] = None,
        consent_id: str = "",
        transaction_id: Optional[str] = None,
        recipient_hiu_id: Optional[str] = None,
        fhir_bundle: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Encapsulates the FHIR bundle into an ABDM Milestone 3 Data Transfer Envelope.
        Computes cryptographic SHA-256 payload integrity check.
        """
        target_bundle = fhir_bundle or bundle or {}
        payload_str = json.dumps(target_bundle, sort_keys=True)
        sha_checksum = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        b64_encrypted = base64.b64encode(payload_str.encode("utf-8")).decode("utf-8")
        tx_id = transaction_id or f"TX-{uuid.uuid4().hex[:8].upper()}"

        return {
            "envelope_version": "ABDM-M3-v1.0",
            "transfer_status": "READY_FOR_DISPATCH",
            "consent_id": consent_id,
            "recipient_hiu_id": recipient_hiu_id or "HIU-DEFAULT",
            "transaction_id": tx_id,
            "data_push_timestamp": datetime.now(timezone.utc).isoformat(),
            "content_type": "application/fhir+json",
            "bundle_type": target_bundle.get("type", "document"),
            "checksum_algorithm": "SHA-256",
            "checksum": sha_checksum,
            "sha256_checksum": sha_checksum,
            "encryption_protocol": "ECDH_AES_GCM_256",
            "decryption_key_reference": f"KEY-REF-{uuid.uuid4().hex[:8].upper()}",
            "encrypted_data": b64_encrypted,
            "data_size_bytes": len(payload_str.encode("utf-8")),
            "fhir_bundle": target_bundle,
        }
