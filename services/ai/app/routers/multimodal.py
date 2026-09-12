"""
ZAYVORA HEALTH™ — Multimodal AI & Clinical Lab Report Extractor Router
Master Build Prompt v4.0 Phase 29 (Horizon 3: Clinical & AI Runtime Intelligence)

Provides REST endpoints for:
1. LOINC clinical lab report parsing, renal safety profiling, and Unani humoral synthesis.
2. Clinical physical signs (tongue and dermatological lesions) semiotic classification.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.multimodal.lab_report_extractor import (
    LabReportExtractor,
    PhysicalSignsAnalyzer,
    LabReportExtractionResult,
    PhysicalSignsAnalysisResult,
)

router = APIRouter(prefix="/api/v1/ai/multimodal", tags=["Multimodal AI & Lab Intelligence"])


class LabExtractionRequest(BaseModel):
    text: Optional[str] = Field(default=None, description="Unstructured or semi-structured lab report text")
    measurements: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Structured key-value analyte observations e.g. [{'loinc_code': '2160-0', 'measured_value': 1.4}]",
    )
    patient_age: int = Field(default=45, ge=1, le=120, description="Patient age in years")
    patient_gender: str = Field(default="M", description="Patient biological sex ('M' or 'F')")


class PhysicalSignsRequest(BaseModel):
    tongue_notes: Optional[str] = Field(
        default=None,
        description="Clinical observation of tongue coating, moisture, and color (e.g. 'thick white coat, moist')",
    )
    skin_notes: Optional[str] = Field(
        default=None,
        description="Cutaneous inspection findings (e.g. 'depigmented macules on forearms consistent with Bars')",
    )
    pulse_notes: Optional[str] = Field(
        default=None,
        description="Pulse (Nabz) notes if available",
    )


@router.post(
    "/extract-lab",
    response_model=LabReportExtractionResult,
    summary="Extract LOINC analytes and synthesize Unani humoral correlates",
)
async def extract_lab_report(payload: LabExtractionRequest) -> LabReportExtractionResult:
    if not payload.text and not payload.measurements:
        raise HTTPException(
            status_code=400,
            detail="Either 'text' or 'measurements' must be provided for lab extraction.",
        )

    if payload.text:
        return LabReportExtractor.extract_from_text(
            text=payload.text,
            patient_age=payload.patient_age,
            patient_gender=payload.patient_gender,
        )
    else:
        return LabReportExtractor.extract_from_measurements(
            measurements=payload.measurements or [],
            patient_age=payload.patient_age,
            patient_gender=payload.patient_gender,
        )


@router.post(
    "/analyze-physical-signs",
    response_model=PhysicalSignsAnalysisResult,
    summary="Classify physical signs (tongue, skin) into Unani semiotic categories",
)
async def analyze_physical_signs(payload: PhysicalSignsRequest) -> PhysicalSignsAnalysisResult:
    if not payload.tongue_notes and not payload.skin_notes and not payload.pulse_notes:
        raise HTTPException(
            status_code=400,
            detail="At least one physical sign observation (tongue, skin, or pulse) must be provided.",
        )

    return PhysicalSignsAnalyzer.analyze_physical_signs(
        tongue_notes=payload.tongue_notes,
        skin_notes=payload.skin_notes,
        pulse_notes=payload.pulse_notes,
    )
