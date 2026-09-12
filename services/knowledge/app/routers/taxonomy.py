from __future__ import annotations

from fastapi import APIRouter

from app.core.taxonomy import EVIDENCE_LEVELS, KNOWLEDGE_WORLDS, MIZAJ_TEMPERAMENTS, ORGAN_AXES

router = APIRouter(prefix="/api/v1", tags=["taxonomy"])


@router.get("/organ-axes")
def list_organ_axes():
    return ORGAN_AXES


@router.get("/mizaj-temperaments")
def list_mizaj_temperaments():
    return MIZAJ_TEMPERAMENTS


@router.get("/evidence-levels")
def list_evidence_levels():
    return EVIDENCE_LEVELS


@router.get("/knowledge-worlds")
def list_knowledge_worlds():
    return KNOWLEDGE_WORLDS
