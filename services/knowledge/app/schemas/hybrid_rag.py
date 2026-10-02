# Hybrid RAG request/response schemas
"""
Pydantic models for the Hybrid RAG endpoint.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class HybridRagRequest(BaseModel):
    query: str = Field(..., description="User search query")
    organ_axis: List[str] | None = Field(None, description="Optional list of organ axis codes to filter results")
    temperament: str | None = Field(None, description="Optional temperament (mizaj) to filter results")
    top_k: int = Field(5, ge=1, le=20, description="Number of results to return")


class Document(BaseModel):
    document_id: str = Field(..., description="Unique identifier for the document")
    doc_type: str = Field(..., description="Document type, e.g., 'mufrad', 'murakkab', 'poison'")
    title: str = Field(..., description="Human readable title")
    content: str = Field(..., description="Document content/summary")
    score: float = Field(..., description="Relevance score after fusion")
    is_schedule_e1: bool = Field(False, description="Whether the document is a Schedule E(1) poison")
    metadata: dict = Field(default_factory=dict, description="Original metadata from the source")


class HybridRagResponse(BaseModel):
    results: List[Document] = Field(..., description="List of retrieved documents")
