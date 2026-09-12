from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.core.auth_dependency import CurrentUser, get_current_user

router = APIRouter(prefix="/api/v1/graph", tags=["knowledge-graph"])


def _repo(request: Request):
    return request.app.state.graph_repository


class GraphRagRequest(BaseModel):
    organ_axis: str | None = Field(default=None, description="Organ axis code (e.g. meda-amaa, mafasil)")
    symptoms: list[str] = Field(default_factory=list, description="Clinical symptoms")
    temperament: str | None = Field(default=None, description="Dominant Mizaj temperament")
    max_hops: int = Field(default=2, ge=1, le=4)


@router.get("/mufrad/{name_or_id}/network")
def get_mufrad_network(
    name_or_id: str,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    repo = _repo(request)
    network = repo.get_mufrad_network(name_or_id=name_or_id, organization_id=user.organization_id)
    if not network:
        raise HTTPException(status_code=404, detail=f"Mufrad '{name_or_id}' not found in knowledge graph")
    return network


@router.get("/compounds/{name_or_id}/network")
def get_compound_network(
    name_or_id: str,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    repo = _repo(request)
    network = repo.get_compound_network(compound_name_or_id=name_or_id)
    if not network:
        raise HTTPException(status_code=404, detail=f"Compound '{name_or_id}' not found in formula graph")
    return network


@router.get("/correctives/{mufrad_name}")
def get_correctives(
    mufrad_name: str,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    repo = _repo(request)
    return repo.find_correctives(mufrad_name=mufrad_name)


@router.get("/substitutes/{mufrad_name}")
def get_substitutes(
    mufrad_name: str,
    request: Request,
    axis: str | None = None,
    user: CurrentUser = Depends(get_current_user),
):
    repo = _repo(request)
    return repo.find_substitutes(mufrad_name=mufrad_name, target_axis=axis)


@router.post("/rag-context")
def extract_rag_context(
    payload: GraphRagRequest,
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    """Multi-hop Graph RAG context extraction for clinical decision support."""
    repo = _repo(request)
    result = repo.extract_rag_subgraph(
        organ_axis=payload.organ_axis,
        symptoms=payload.symptoms,
        temperament=payload.temperament,
        max_hops=payload.max_hops,
    )
    return result


@router.post("/seed", status_code=201)
def seed_graph(
    request: Request,
    user: CurrentUser = Depends(get_current_user),
):
    """Triggers canonical knowledge graph ingestion from UPI, NFUM, and Schedule E(1)."""
    repo = _repo(request)
    counts = repo.seed_pharmacopoeia_graph()
    return {"status": "seeded", "counts": counts}
