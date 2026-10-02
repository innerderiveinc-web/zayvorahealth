"""
ZAYVORA Knowledge Base (ZKB) — Pydantic Schemas for OCR & Extraction
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OcrJobCreate(BaseModel):
    edition_id: str
    engine_name: str = "Tesseract-Urdu-Arabic-v5.3"
    target_scripts: List[str] = Field(default_factory=lambda: ["arab", "nastaliq", "latn"])
    raw_text_pages: Optional[Dict[int, str]] = None


class OcrJobResponse(BaseModel):
    id: str
    edition_id: str
    engine_name: str
    engine_version: str
    status: str
    target_scripts: List[str]
    overall_confidence: float
    total_pages_processed: int
    needs_review_count: int
    started_at: str
    completed_at: Optional[str] = None
    created_at: str


class OcrSegmentResponse(BaseModel):
    id: str
    ocr_document_id: str
    page_id: str
    line_number: int
    detected_script: str
    detected_language: str
    segment_text: str
    confidence: float
    bounding_polygon: Optional[Dict[str, Any]] = None
    needs_review: bool
    is_corrected: bool
    created_at: str


class OcrCorrectionCreate(BaseModel):
    corrected_text: str
    correction_notes: Optional[str] = None


class OcrCorrectionResponse(BaseModel):
    id: str
    segment_id: str
    original_ocr_text: str
    corrected_text: str
    reviewer_user_id: str
    reviewer_name: Optional[str] = None
    correction_notes: Optional[str] = None
    reviewed_at: str


class ExtractionRequest(BaseModel):
    passage_id: str
    passage_text: str


class ExtractionResponse(BaseModel):
    id: str
    passage_id: str
    extracted_entities: Dict[str, Any]
    extraction_confidence: float
    extraction_method: str
    review_status: str
    created_at: str
