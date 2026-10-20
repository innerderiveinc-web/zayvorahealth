"""
ZAYVORA Health OS™ — Clinical Intelligence Continuum, Interoperability & Federation Router
========================================================================================
Exposes:
- POST /api/v1/clinical/continuum/execute: Full 12-stage clinical loop
- GET  /api/v1/clinical/continuum/who-smart-dak/mufrad/{name}: Level 3 WHO SMART DAK artifact
- GET  /api/v1/clinical/continuum/learning-health-system/summary: Closed-Loop LHS registry summary
- POST /api/v1/clinical/continuum/fhir-bundle/op-consult: ABDM FHIR R4 OPConsultRecord Bundle
- POST /api/v1/clinical/continuum/fhir-bundle/prescription: ABDM FHIR R4 PrescriptionRecord Bundle
- GET  /api/v1/clinical/continuum/federation/clinics: Multi-facility federation clinic directory
- POST /api/v1/clinical/continuum/federation/referral: Cryptographic inter-clinic referral creation
- POST /api/v1/clinical/continuum/federation/referral/redeem: Inter-clinic referral redemption
- GET  /api/v1/clinical/continuum/population-health/seasonal-alerts: Canonical seasonal advisory
- GET  /api/v1/clinical/continuum/population-health/epidemiology: Cohort humoral distribution
- GET  /api/v1/clinical/continuum/population-health/adr-clusters: Pharmacovigilance cluster detection
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth_dependency import get_current_user, CurrentUser

from app.engines.clinical_intelligence_core_orchestrator import (
    ClinicalIntelligenceCoreOrchestrator,
    ClinicalContinuumRequest,
)
from app.engines.closed_loop_learning_engine import ClosedLoopLearningEngine
from app.interop.abdm_fhir_continuum_orchestrator import ABDMFHIRContinuumOrchestrator
from app.engines.multi_clinic_federation_engine import MultiClinicFederationEngine
from app.engines.population_health_engine import PopulationHealthEngine, CanonicalSeason
from services.knowledge.app.core.who_smart_dak_engine import WHOSmartDAKEngine
from services.knowledge.app.core.pharmacopoeia import get_upi_mufradat

router = APIRouter(prefix="/api/v1/clinical/continuum", tags=["clinical-continuum-vnext"])


class ContinuumExecutionPayload(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    patient_name: str = Field(..., description="Patient full legal name")
    age: int = Field(..., ge=0, le=120, description="Age in years")
    gender: str = Field(..., description="Biological sex / gender")
    chief_complaints: List[str] = Field(..., min_items=1, description="Presenting complaints")
    presenting_condition: str = Field(..., description="Diagnostic entity e.g. Waja-ul-Mafasil")
    symptom_duration_days: int = Field(..., ge=1, description="Duration of symptoms")
    baseline_pain_vas: float = Field(..., ge=0.0, le=10.0, description="Baseline pain/distress VAS")
    constitutional_signs: Dict[str, Any] = Field(default_factory=dict, description="Nabz, Baul, Baraz signs")
    targeted_axes: List[str] = Field(default_factory=list, description="Targeted 12 Organ-Axes")
    candidate_drugs: List[str] = Field(..., min_items=1, description="Proposed pharmacopeial interventions")
    clinician_id: str = Field(..., description="Licensed clinician practitioner ID")
    clinician_role: str = Field(default="HAKEEM", description="Clinician role e.g. HAKEEM, DOCTOR, CLINICIAN")
    is_pregnant: bool = Field(default=False, description="Pregnancy flag for teratogenic hard-block")
    has_renal_impairment: bool = Field(default=False, description="Renal impairment flag")
    followup_proms_day: Optional[int] = Field(default=None, description="Follow-up day e.g. 14")
    followup_symptom_vas: Optional[float] = Field(default=None, description="Follow-up pain VAS")
    followup_adverse_events: List[str] = Field(default_factory=list, description="Adverse events if any")


class InterClinicReferralPayload(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    source_facility_id: str = Field(..., description="Originating clinic node")
    target_facility_id: str = Field(..., description="Target specialized facility node")
    referring_clinician_id: str = Field(..., description="Referring clinician practitioner ID")
    clinical_condition: str = Field(..., description="Presenting clinical condition")
    specialty_axis_required: str = Field(..., description="Required specialty axis e.g. MAFASIL, JIGAR-BANAS")
    reason_for_referral: str = Field(..., description="Clinical rationale and referral context")
    validity_days: int = Field(default=30, ge=1, le=90, description="Validity period in days")


class ReferralRedeemPayload(BaseModel):
    referral_token: str = Field(..., description="Cryptographic referral token")
    receiving_facility_id: str = Field(..., description="Receiving clinic facility ID")
    accepting_clinician_id: str = Field(..., description="Accepting practitioner ID")


@router.post("/execute", summary="Execute Complete 12-Stage Clinical Intelligence Continuum")
def execute_clinical_continuum(payload: ContinuumExecutionPayload, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    clinician_id = current_user.user_id
    clinician_role = current_user.roles[0] if current_user.roles else payload.clinician_role
    req = ClinicalContinuumRequest(
        patient_id=payload.patient_id,
        patient_name=payload.patient_name,
        age=payload.age,
        gender=payload.gender,
        chief_complaints=payload.chief_complaints,
        presenting_condition=payload.presenting_condition,
        symptom_duration_days=payload.symptom_duration_days,
        baseline_pain_vas=payload.baseline_pain_vas,
        constitutional_signs=payload.constitutional_signs,
        targeted_axes=payload.targeted_axes,
        candidate_drugs=payload.candidate_drugs,
        clinician_id=clinician_id,
        clinician_role=clinician_role,
        is_pregnant=payload.is_pregnant,
        has_renal_impairment=payload.has_renal_impairment,
        followup_proms_day=payload.followup_proms_day,
        followup_symptom_vas=payload.followup_symptom_vas,
        followup_adverse_events=payload.followup_adverse_events,
    )
    res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
    return asdict(res)


@router.post("/fhir-bundle/op-consult", summary="Generate ABDM FHIR R4 OPConsultRecord Document Bundle")
def generate_abdm_op_consult_bundle(payload: ContinuumExecutionPayload, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    clinician_id = current_user.user_id
    clinician_role = current_user.roles[0] if current_user.roles else payload.clinician_role
    req = ClinicalContinuumRequest(
        patient_id=payload.patient_id,
        patient_name=payload.patient_name,
        age=payload.age,
        gender=payload.gender,
        chief_complaints=payload.chief_complaints,
        presenting_condition=payload.presenting_condition,
        symptom_duration_days=payload.symptom_duration_days,
        baseline_pain_vas=payload.baseline_pain_vas,
        constitutional_signs=payload.constitutional_signs,
        targeted_axes=payload.targeted_axes,
        candidate_drugs=payload.candidate_drugs,
        clinician_id=clinician_id,
        clinician_role=clinician_role,
        is_pregnant=payload.is_pregnant,
        has_renal_impairment=payload.has_renal_impairment,
        followup_proms_day=payload.followup_proms_day,
        followup_symptom_vas=payload.followup_symptom_vas,
        followup_adverse_events=payload.followup_adverse_events,
    )
    res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
    bundle = ABDMFHIRContinuumOrchestrator.build_op_consult_bundle(asdict(res))
    return {
        "ok": True,
        "abdm_profile": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord",
        "fhir_bundle": bundle,
    }


@router.post("/fhir-bundle/prescription", summary="Generate ABDM FHIR R4 PrescriptionRecord Document Bundle")
def generate_abdm_prescription_bundle(payload: ContinuumExecutionPayload, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    clinician_id = current_user.user_id
    clinician_role = current_user.roles[0] if current_user.roles else payload.clinician_role
    req = ClinicalContinuumRequest(
        patient_id=payload.patient_id,
        patient_name=payload.patient_name,
        age=payload.age,
        gender=payload.gender,
        chief_complaints=payload.chief_complaints,
        presenting_condition=payload.presenting_condition,
        symptom_duration_days=payload.symptom_duration_days,
        baseline_pain_vas=payload.baseline_pain_vas,
        constitutional_signs=payload.constitutional_signs,
        targeted_axes=payload.targeted_axes,
        candidate_drugs=payload.candidate_drugs,
        clinician_id=clinician_id,
        clinician_role=clinician_role,
        is_pregnant=payload.is_pregnant,
        has_renal_impairment=payload.has_renal_impairment,
        followup_proms_day=payload.followup_proms_day,
        followup_symptom_vas=payload.followup_symptom_vas,
        followup_adverse_events=payload.followup_adverse_events,
    )
    res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
    bundle = ABDMFHIRContinuumOrchestrator.build_prescription_bundle(asdict(res))
    return {
        "ok": True,
        "abdm_profile": "https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord",
        "fhir_bundle": bundle,
    }


@router.get("/who-smart-dak/mufrad/{mufrad_name}", summary="Get WHO SMART Guidelines Level 3 Computable DAK")
def get_who_smart_dak(mufrad_name: str, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    matched = next((m for m in get_upi_mufradat() if mufrad_name.lower() in m["name"].lower()), None)
    if not matched:
        raise HTTPException(status_code=404, detail=f"Mufrad '{mufrad_name}' not found in ratified pharmacopoeia")
    artifact = WHOSmartDAKEngine.transform_mufrad_to_smart_artifact(matched)
    return asdict(artifact)


@router.get("/learning-health-system/summary", summary="Get Closed-Loop Learning Health System Cohort Summary")
def get_lhs_summary(current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    registry = ClosedLoopLearningEngine.get_registry_summary()
    return {
        "status": "OPERATIONAL",
        "doctrine": "WHO Learning Health Systems & HIPAA § 164.514(b)(2)",
        "registry": registry,
    }


@router.get("/federation/clinics", summary="List All Federated Facilities in Multi-Clinic Network")
def list_federated_clinics(current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    clinics = MultiClinicFederationEngine.list_clinics()
    return {"ok": True, "facilities": clinics, "total_facilities": len(clinics)}


@router.post("/federation/referral", summary="Create Cryptographically Signed Inter-Clinic Referral")
def create_federated_referral(payload: InterClinicReferralPayload, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    referring_clinician_id = current_user.user_id
    try:
        ref = MultiClinicFederationEngine.create_inter_clinic_referral(
            patient_id=payload.patient_id,
            source_facility_id=payload.source_facility_id,
            target_facility_id=payload.target_facility_id,
            referring_clinician_id=referring_clinician_id,
            clinical_condition=payload.clinical_condition,
            specialty_axis_required=payload.specialty_axis_required,
            reason_for_referral=payload.reason_for_referral,
            validity_days=payload.validity_days,
        )
        return {"ok": True, "referral": asdict(ref)}
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.post("/federation/referral/redeem", summary="Redeem Inter-Clinic Referral at Target Clinic")
def redeem_federated_referral(payload: ReferralRedeemPayload, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    accepting_clinician_id = current_user.user_id
    res = MultiClinicFederationEngine.redeem_inter_clinic_referral(
        referral_token=payload.referral_token,
        receiving_facility_id=payload.receiving_facility_id,
        accepting_clinician_id=accepting_clinician_id,
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Referral redemption failed"))
    return {"ok": True, "redemption": res}


@router.get("/population-health/seasonal-alerts", summary="Get Asbab-e-Sittah Seasonal Humoral Surveillance Advisory")
def get_seasonal_humoral_alerts(season: Optional[str] = None, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    s_enum = CanonicalSeason(season) if season else None
    advisory = PopulationHealthEngine.generate_seasonal_surveillance_advisory(s_enum)
    return {"ok": True, "advisory": asdict(advisory)}


@router.get("/population-health/epidemiology", summary="Get Cohort Humoral Temperament Distribution")
def get_population_epidemiology(facility_id: Optional[str] = None, current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    dist = PopulationHealthEngine.get_humoral_epidemiology_distribution(facility_id)
    return {"ok": True, "epidemiology": dist}


@router.get("/population-health/adr-clusters", summary="Scan for Multi-Clinic Pharmacovigilance Clusters")
def scan_adr_clusters(current_user: CurrentUser = Depends(get_current_user)) -> Dict[str, Any]:
    alerts = PopulationHealthEngine.scan_adr_clusters()
    return {"ok": True, "cluster_alerts": [asdict(a) for a in alerts], "count": len(alerts)}
