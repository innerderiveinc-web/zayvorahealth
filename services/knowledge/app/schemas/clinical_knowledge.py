"""
ZAYVORA Knowledge Base — Structured Clinical Knowledge Pydantic Schemas.

Covers Mufradat, Murakkabat, Diseases, Safety Firewall and Mizaj Assessment.
All schemas use strict field definitions — no arbitrary dict passing into API contracts.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ===========================================================================
# MUFRADAT
# ===========================================================================

class MufradatResponse(BaseModel):
    id: str
    canonical_name_latin: str
    canonical_name_urdu: str
    canonical_name_arabic: Optional[str] = None
    canonical_name_english: Optional[str] = None
    botanical_name: Optional[str] = None
    upi_code: Optional[str] = None
    origin_category: str
    plant_part_used: Optional[str] = None
    mizaj_primary_quality: Optional[str] = None
    mizaj_degree: int
    is_schedule_e1_poison: bool
    mandatory_mudabbar: bool
    mudabbar_protocol: Optional[str] = None
    historical_dose: Optional[str] = None
    approved_single_dose_max_grams: float
    approved_daily_dose_max_grams: float
    therapeutic_actions: List[str] = Field(default_factory=list)
    badal_substitutes: List[str] = Field(default_factory=list)
    musleh_correctives: List[str] = Field(default_factory=list)
    pregnancy_status: str
    lactation_status: str
    pediatric_status: str
    geriatric_status: str
    evidence_level: str
    current_lifecycle_state: str
    safe_for_ai: bool

    class Config:
        extra = "ignore"


class MufradatListResponse(BaseModel):
    total: int
    items: List[MufradatResponse]


# ===========================================================================
# MURAKKABAT
# ===========================================================================

class MurakkabIngredientResponse(BaseModel):
    mufradat_id: str
    ratio: float
    is_chief: bool
    requires_mudabbar: bool


class MurakkabResponse(BaseModel):
    id: str
    canonical_name_urdu: str
    canonical_name_english: str
    dosage_form: str
    nfum_code: Optional[str] = None
    primary_organ_axis: Optional[str] = None
    therapeutic_objective: Optional[str] = None
    overall_mizaj: Optional[str] = None
    approved_single_dose_min_grams: float
    approved_single_dose_max_grams: float
    approved_daily_dose_max_grams: float
    anupan_vehicle: Optional[str] = None
    shelf_life_months: int
    manufacturing_protocol: Optional[str] = None
    ingredients: List[MurakkabIngredientResponse] = Field(default_factory=list)
    evidence_level: str
    current_lifecycle_state: str
    safe_for_ai: bool

    class Config:
        extra = "ignore"


class MurakkabListResponse(BaseModel):
    total: int
    items: List[MurakkabResponse]


# ===========================================================================
# FORMULATION INTEGRITY GATE
# ===========================================================================

class FormulationIngredientInput(BaseModel):
    mufradat_id: str
    ratio: float = Field(gt=0.0, le=1.0, description="Weight ratio in formulation (0–1)")
    is_chief: bool = False
    requires_mudabbar: bool = False


class FormulationValidationRequest(BaseModel):
    name: str = Field(..., description="Working name of the formulation under review")
    ingredients: List[FormulationIngredientInput]


class FormulationValidationResponse(BaseModel):
    is_valid: bool
    has_schedule_e1: bool
    errors: List[str]
    warnings: List[str]


# ===========================================================================
# DISEASES
# ===========================================================================

class DiseaseResponse(BaseModel):
    id: str
    unani_name_arabic: Optional[str] = None
    unani_name_urdu: str
    transliterated_name: str
    icd11_code: Optional[str] = None
    snomed_ct_id: Optional[str] = None
    biomedical_mapping_type: str
    primary_organ_axis: Optional[str] = None
    pathology_mizaj_derangement: Optional[str] = None
    clinical_manifestations: Optional[str] = None
    treatment_principles: Optional[str] = None

    class Config:
        extra = "ignore"


class DiseaseListResponse(BaseModel):
    total: int
    items: List[DiseaseResponse]


# ===========================================================================
# CLINICAL SAFETY FIREWALL
# ===========================================================================

class PrescribedItemInput(BaseModel):
    mufradat_id: str
    single_dose_grams: float = Field(gt=0.0)
    mudabbar_certified: bool = False


class SafetyEvaluationRequest(BaseModel):
    patient_context: Dict[str, Any] = Field(
        ...,
        description=(
            "age (int), is_pregnant (bool), is_lactating (bool), "
            "egfr (float, mL/min/1.73m²), alt (float, U/L), "
            "modern_drugs (list[str]) — generic or class keywords"
        ),
    )
    prescribed_items: List[PrescribedItemInput]


class SafetyViolation(BaseModel):
    rule: str
    severity: str
    message: str


class SafetyEvaluationResponse(BaseModel):
    verdict: str          # ALLOWED | ALLOWED_WITH_WARNING | BLOCKED
    is_safe: bool
    violations: List[SafetyViolation]
    warnings: List[str]
    evaluated_at: str


# ===========================================================================
# MIZAJ ASSESSMENT
# ===========================================================================

class MizajAssessmentRequest(BaseModel):
    phenotype_signs: Dict[str, Any] = Field(
        ...,
        description=(
            "Observed phenotypic signs: complexion (str), touch (str), pulse (str). "
            "All values should be descriptive English text matching canonical qualifiers."
        ),
    )


class MizajAssessmentResponse(BaseModel):
    dominant_mizaj: str
    secondary_mizaj: str
    confidence: float
    scores: Dict[str, float]
    supporting_findings: List[str]
    contradicting_findings: List[str]
    clinician_review_status: str
