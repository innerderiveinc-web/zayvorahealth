from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.evidence_engine import calculate_grade_certainty, classify_study_design
from app.schemas.knowledge import (
    EvidenceClassifyRequest,
    EvidenceClassifyResponse,
    EvidenceCreate,
    EvidenceOut,
    GRADEScoreRequest,
    GRADEScoreResponse,
)

router = APIRouter(prefix="/api/v1/mufradat/{mufrad_id}/evidence", tags=["evidence"])
evidence_engine_router = APIRouter(prefix="/api/v1/evidence", tags=["evidence-engine"])


def _repo(request: Request):
    return request.app.state.graph_repository


@router.post("", response_model=EvidenceOut, status_code=201)
def add_evidence(
    mufrad_id: str,
    payload: EvidenceCreate,
    request: Request,
    user: CurrentUser = Depends(require_permission("evidence.write")),
):
    """Never upgrades a claim's evidence level automatically — the caller
    states the level (E0-E6) explicitly, and review_status defaults to
    'pending' until a qualified reviewer approves it. See Master Build
    Prompt v4.0 §23: "Never transform E0 into E3/E4 automatically."""
    try:
        return _repo(request).add_evidence(
            organization_id=user.organization_id, mufrad_id=mufrad_id, evidence=payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("", response_model=list[EvidenceOut])
def list_evidence(
    mufrad_id: str,
    request: Request,
    user: CurrentUser = Depends(require_permission("evidence.read")),
):
    return _repo(request).list_evidence_for_mufrad(organization_id=user.organization_id, mufrad_id=mufrad_id)


@evidence_engine_router.post("/classify", response_model=EvidenceClassifyResponse)
def classify_study_endpoint(
    payload: EvidenceClassifyRequest,
    user: CurrentUser = Depends(require_permission("evidence.read")),
):
    """Classifies study design and recommends candidate evidence level (E0-E6)."""
    return classify_study_design(payload.text)


@evidence_engine_router.post("/grade", response_model=GRADEScoreResponse)
def grade_evidence_endpoint(
    payload: GRADEScoreRequest,
    user: CurrentUser = Depends(require_permission("evidence.read")),
):
    """Calculates GRADE certainty score based on risk of bias and upgrade factors."""
    return calculate_grade_certainty(
        starting_level=payload.starting_level,
        risk_of_bias=payload.risk_of_bias,
        inconsistency=payload.inconsistency,
        indirectness=payload.indirectness,
        imprecision=payload.imprecision,
        publication_bias=payload.publication_bias,
        large_effect_size=payload.large_effect_size,
        dose_response_gradient=payload.dose_response_gradient,
    )

