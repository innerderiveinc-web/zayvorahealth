"""
ZAYVORA Knowledge Base (ZKB) — OCR Extraction & Scholarly Review Router
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException

from app.core.auth_dependency import CurrentUser, get_current_user
from app.core.ocr_pipeline import get_ocr_pipeline
from app.schemas.ocr import (
    ExtractionRequest,
    ExtractionResponse,
    OcrCorrectionCreate,
    OcrCorrectionResponse,
    OcrJobCreate,
    OcrJobResponse,
    OcrSegmentResponse,
)

router = APIRouter(prefix="/api/v1/zkb/ocr", tags=["zkb-ocr-pipeline"])


@router.post("/jobs", response_model=OcrJobResponse)
def submit_ocr_job(payload: OcrJobCreate, user: CurrentUser = Depends(get_current_user)):
    pipeline = get_ocr_pipeline()
    job = pipeline.submit_ocr_job(
        edition_id=payload.edition_id,
        engine_name=payload.engine_name,
        target_scripts=payload.target_scripts,
        raw_text_pages=payload.raw_text_pages,
    )
    return job


@router.get("/jobs/{job_id}", response_model=OcrJobResponse)
def get_ocr_job(job_id: str):
    pipeline = get_ocr_pipeline()
    job = pipeline.get_ocr_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"OCR job '{job_id}' not found")
    return job


@router.get("/jobs/{job_id}/segments", response_model=List[OcrSegmentResponse])
def get_segments(job_id: str):
    pipeline = get_ocr_pipeline()
    return pipeline.get_segments_by_job(job_id)


@router.get("/review-queue", response_model=List[OcrSegmentResponse])
def get_review_queue(job_id: Optional[str] = None):
    pipeline = get_ocr_pipeline()
    return pipeline.get_needs_review_segments(job_id)


@router.post("/segments/{segment_id}/correct", response_model=OcrCorrectionResponse)
def correct_segment(
    segment_id: str,
    payload: OcrCorrectionCreate,
    user: CurrentUser = Depends(get_current_user),
):
    pipeline = get_ocr_pipeline()
    try:
        correction = pipeline.submit_correction(
            segment_id=segment_id,
            corrected_text=payload.corrected_text,
            reviewer_id=user.user_id,
            reviewer_name=f"Scholar-{user.user_id[:8]}",
            notes=payload.correction_notes,
        )
        return correction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/extract-entities", response_model=ExtractionResponse)
def extract_entities(payload: ExtractionRequest, user: CurrentUser = Depends(get_current_user)):
    pipeline = get_ocr_pipeline()
    return pipeline.extract_clinical_entities(payload.passage_id, payload.passage_text)
