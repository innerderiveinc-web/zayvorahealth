from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.hybrid_rag import ZAYVORAIntelligenceEngine
from app.core.structured_knowledge import get_structured_knowledge
from app.graph.repository import GraphRepository
from app.schemas.hybrid_rag import HybridRagRequest, HybridRagResponse, Document

router = APIRouter(prefix="/api/v1/zkb/hybrid_rag", tags=["Hybrid RAG"])

# Placeholder dependency for auth – can be expanded later
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_graph_repository() -> GraphRepository:
    # FastAPI will have the repository stored in app.state; this function is a stub that could be
    # replaced with a proper Depends that pulls from the request state.
    from fastapi import Request
    async def _dependency(request: Request) -> GraphRepository:
        return request.app.state.graph_repository
    return _dependency

@router.post("/search", response_model=HybridRagResponse)
def hybrid_search(
    request: HybridRagRequest,
    repo: GraphRepository = Depends(get_graph_repository()),
    token: str = Depends(oauth2_scheme),
):
    """Execute a hybrid search and enforce safety firewall.

    The `token` dependency is a placeholder for future authentication; it is not validated here.
    """
    engine = ZAYVORAIntelligenceEngine()
    results = engine.hybrid_search(
        request.query,
        organ_axis=request.organ_axis,
        temperament=request.temperament,
        top_k=request.top_k,
    )

    # Safety check – for any clinical recommendation (mufrad or murakkab), run the safety engine.
    knowledge = get_structured_knowledge()
    safe_documents: list[Document] = []
    for item in results:
        doc_type = item.get("doc_type")
        if doc_type in {"mufrad", "murakkab"}:
            # Extract id without prefix
            raw_id = item["document_id"].split("-")[1]
            safety = knowledge.evaluate_prescription_safety(
                mufrad_id=raw_id,
                patient_context={
                    "mizaj": request.temperament or "",
                    "organ_axis": request.organ_axis or "",
                },
            )
            if safety["verdict"] == "BLOCKED":
                raise HTTPException(status_code=403, detail={"blocked": safety["violations"]})
        safe_documents.append(Document(**item))

    return HybridRagResponse(results=safe_documents)
