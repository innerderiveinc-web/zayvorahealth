"""
ZAYVORA Knowledge Base — Structured Clinical Knowledge REST Router.

Endpoints:
  GET  /api/v1/zkb/mufradat           — list all Mufradat with optional filters
  GET  /api/v1/zkb/mufradat/{id}      — single Mufrad monograph
  GET  /api/v1/zkb/murakkabat         — list all Murakkabat with optional search
  GET  /api/v1/zkb/murakkabat/{id}    — single Murakkab formulation
  POST /api/v1/zkb/murakkabat/validate — formulation integrity gate
  GET  /api/v1/zkb/diseases           — list all diseases
  GET  /api/v1/zkb/diseases/{id}      — single disease
  POST /api/v1/zkb/safety/evaluate    — deterministic prescription safety firewall
  POST /api/v1/zkb/mizaj/assess       — algorithmic Mizaj assessment

All routes require JWT authentication via get_current_user.
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.auth_dependency import get_current_user
from app.core.structured_knowledge import get_structured_knowledge
from app.schemas.clinical_knowledge import (
    DiseaseListResponse,
    DiseaseResponse,
    FormulationValidationRequest,
    FormulationValidationResponse,
    MizajAssessmentRequest,
    MizajAssessmentResponse,
    MufradatListResponse,
    MufradatResponse,
    MurakkabListResponse,
    MurakkabResponse,
    SafetyEvaluationRequest,
    SafetyEvaluationResponse,
    SafetyViolation,
)

router = APIRouter(prefix="/api/v1/zkb", tags=["ZKB Structured Clinical Knowledge"])


# ---------------------------------------------------------------------------
# MUFRADAT
# ---------------------------------------------------------------------------

@router.get(
    "/mufradat",
    response_model=MufradatListResponse,
    summary="List Mufradat (medicinal simples)",
    description=(
        "Returns canonical Mufradat from the ZKB structured repository. "
        "Filter by Schedule E(1) poison status and/or free-text search."
    ),
)
def list_mufradat(
    is_poison: Optional[bool] = Query(None, description="Filter: true = E(1) poisons only, false = non-poisons only"),
    search: Optional[str] = Query(None, description="Free-text search across names and UPI code"),
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    items = engine.get_all_mufradat(is_poison=is_poison, search=search)
    return MufradatListResponse(
        total=len(items),
        items=[MufradatResponse(**m) for m in items],
    )


@router.get(
    "/mufradat/{mufrad_id}",
    response_model=MufradatResponse,
    summary="Get Mufrad monograph by ID",
)
def get_mufrad(
    mufrad_id: str,
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    herb = engine.get_mufrad_by_id(mufrad_id)
    if herb is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mufrad '{mufrad_id}' not found in canonical registry.",
        )
    return MufradatResponse(**herb)


# ---------------------------------------------------------------------------
# MURAKKABAT
# ---------------------------------------------------------------------------

@router.get(
    "/murakkabat",
    response_model=MurakkabListResponse,
    summary="List Murakkabat (compound formulations)",
)
def list_murakkabat(
    search: Optional[str] = Query(None, description="Free-text search across names, dosage form and organ axis"),
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    items = engine.get_all_murakkabat(search=search)
    return MurakkabListResponse(
        total=len(items),
        items=[MurakkabResponse(**m) for m in items],
    )


@router.get(
    "/murakkabat/{murakkab_id}",
    response_model=MurakkabResponse,
    summary="Get Murakkab formulation by ID",
)
def get_murakkab(
    murakkab_id: str,
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    formula = engine.get_murakkab_by_id(murakkab_id)
    if formula is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Murakkab '{murakkab_id}' not found in canonical registry.",
        )
    return MurakkabResponse(**formula)


@router.post(
    "/murakkabat/validate",
    response_model=FormulationValidationResponse,
    summary="Formulation integrity gate — validates ingredient safety before compounding",
    description=(
        "Runs deterministic Schedule E(1) Mudabbar gate, duplicate ingredient detection, "
        "and botanical identity verification. Must pass BEFORE any manufacturing order is created."
    ),
)
def validate_formulation(
    payload: FormulationValidationRequest,
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    result = engine.validate_formulation_integrity(payload.dict())
    return FormulationValidationResponse(**result)


# ---------------------------------------------------------------------------
# DISEASES
# ---------------------------------------------------------------------------

@router.get(
    "/diseases",
    response_model=DiseaseListResponse,
    summary="List Unani diseases with ICD-11 and SNOMED mappings",
)
def list_diseases(
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    items = list(engine.diseases.values())
    return DiseaseListResponse(
        total=len(items),
        items=[DiseaseResponse(**d) for d in items],
    )


@router.get(
    "/diseases/{disease_id}",
    response_model=DiseaseResponse,
    summary="Get disease by canonical Unani disease ID",
)
def get_disease(
    disease_id: str,
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    disease = engine.diseases.get(disease_id)
    if disease is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease '{disease_id}' not found in canonical taxonomy.",
        )
    return DiseaseResponse(**disease)


# ---------------------------------------------------------------------------
# CLINICAL SAFETY FIREWALL
# ---------------------------------------------------------------------------

@router.post(
    "/safety/evaluate",
    response_model=SafetyEvaluationResponse,
    summary="Deterministic multi-variable prescription safety firewall",
    description=(
        "Non-bypassable clinical safety evaluation that checks: "
        "Schedule E(1) Mudabbar certification, dose ceilings, pregnancy/pediatric/renal "
        "contraindications, and herb-drug interactions. "
        "A BLOCKED verdict must prevent any prescription issuance."
    ),
)
def evaluate_safety(
    payload: SafetyEvaluationRequest,
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    result = engine.evaluate_prescription_safety(
        patient_context=payload.patient_context,
        prescribed_items=[item.dict() for item in payload.prescribed_items],
    )
    return SafetyEvaluationResponse(
        verdict=result["verdict"],
        is_safe=result["is_safe"],
        violations=[SafetyViolation(**v) for v in result["violations"]],
        warnings=result["warnings"],
        evaluated_at=result["evaluated_at"],
    )


# ---------------------------------------------------------------------------
# MIZAJ ASSESSMENT
# ---------------------------------------------------------------------------

@router.post(
    "/mizaj/assess",
    response_model=MizajAssessmentResponse,
    summary="Algorithmic 4-temperament Mizaj assessment",
    description=(
        "Computes dominant and secondary Mizaj (Damawi, Safrawi, Balghami, Sawdawi) "
        "from observed phenotypic signs (complexion, touch, pulse). "
        "Output is always marked PROVISIONAL_PENDING_CLINICIAN_PULSE_CHECK — "
        "clinician override required for any prescription-affecting decision."
    ),
)
def assess_mizaj(
    payload: MizajAssessmentRequest,
    _: dict = Depends(get_current_user),
):
    engine = get_structured_knowledge()
    result = engine.assess_patient_mizaj(payload.phenotype_signs)
    return MizajAssessmentResponse(**result)
