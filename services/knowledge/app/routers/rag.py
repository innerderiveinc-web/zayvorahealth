from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core.auth_dependency import CurrentUser, get_current_user
from app.core.hybrid_rag import HybridRAGEngine

router = APIRouter(prefix="/api/v1/knowledge/rag", tags=["hybrid-rag"])

_ENGINE_INSTANCE: HybridRAGEngine | None = None


def get_rag_engine() -> HybridRAGEngine:
    global _ENGINE_INSTANCE
    if _ENGINE_INSTANCE is None:
        engine = HybridRAGEngine()
        engine.load_canonical_corpus()
        _ENGINE_INSTANCE = engine
    return _ENGINE_INSTANCE


class HybridSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000, description="Search query or symptom description")
    organ_axis: str | None = Field(default=None, description="Target organ axis filter/boost")
    temperament: str | None = Field(default=None, description="Dominant Mizaj temperament filter/boost")
    top_k: int = Field(default=5, ge=1, le=50)
    mode: str = Field(default="rrf", description="Fusion algorithm: 'rrf' (Reciprocal Rank Fusion) or 'weighted'")


class HybridSearchItem(BaseModel):
    document_id: str
    doc_type: str
    title: str
    content: str
    score: float
    is_schedule_e1: bool
    metadata: dict[str, Any]


class HybridSearchResponse(BaseModel):
    query: str
    fusion_mode: str
    count: int
    results: list[HybridSearchItem]


@router.post("/hybrid-search", response_model=HybridSearchResponse)
def hybrid_search(
    payload: HybridSearchRequest,
    user: CurrentUser = Depends(get_current_user),
):
    """Executes multi-modal Hybrid Search fusing Dense Vector Embeddings,
    Okapi BM25 Lexical search, and Knowledge Graph context via Reciprocal Rank Fusion."""
    engine = get_rag_engine()
    results = engine.hybrid_search(
        query=payload.query,
        organ_axis=payload.organ_axis,
        temperament=payload.temperament,
        top_k=payload.top_k,
        mode=payload.mode,
    )
    return HybridSearchResponse(
        query=payload.query,
        fusion_mode=payload.mode,
        count=len(results),
        results=results,
    )


@router.get("/stats")
def get_rag_stats(
    user: CurrentUser = Depends(get_current_user),
):
    """Returns indexing and corpus health metrics for the Hybrid RAG engine."""
    engine = get_rag_engine()
    return {
        "indexed_documents": len(engine.documents),
        "bm25_terms_indexed": len(engine.bm25.doc_freqs),
        "vector_dimensions": engine.vector_store.provider.dim,
        "corpus_breakdown": {
            doc_type: sum(1 for d in engine.documents.values() if d.doc_type == doc_type)
            for doc_type in set(d.doc_type for d in engine.documents.values())
        },
    }
