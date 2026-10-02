"""
ZFIE Core Contracts & Schemas
Specifies payloads for the public ZFIE REST API & internal pipelines.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CreateFormulationPayload(BaseModel):
    name: str
    traditional_name: str
    description: Optional[str] = None
    ingredients: List[Dict[str, Any]]  # [{"mufrad_id": "...", "ratio": 0.40}]
    preparation_method: Optional[str] = "Standard Decoction"
    therapeutic_target: Optional[str] = None


class CreateFormulaVersionPayload(BaseModel):
    version_tag: str
    modified_proportions: Dict[str, float]
    change_rationale: str
    created_by: str = "SYSTEM_RESEARCH"


class CreateBatchPayload(BaseModel):
    lot_number: str
    manufacture_date: str
    expiry_date: str
    hplc_fingerprint_id: Optional[str] = None
    coas: List[str] = Field(default_factory=list)


class RunAnalysisPayload(BaseModel):
    formulation_id: str
    formula_version_id: Optional[str] = None
    batch_id: Optional[str] = None
    mode: str = "SHADOW"
    requested_by: str = "RESEARCH_USER"


class SafetyCheckPayload(BaseModel):
    formulation_id: str
    patient_id: Optional[str] = None
    encounter_id: Optional[str] = None
    dosage_mg: Optional[float] = None


class CreateHypothesisPayload(BaseModel):
    formulation_id: str
    title: str
    statement: str
    falsification_criteria: str
    proposed_assay: str
    target_protein: Optional[str] = None


class CreateExperimentPayload(BaseModel):
    hypothesis_id: str
    title: str
    protocol_reference: str
    reagents: List[str] = Field(default_factory=list)
    lead_investigator: str


class ExperimentResultPayload(BaseModel):
    raw_data_uri: str
    measured_effect_size: float
    p_value: float
    replicates_count: int
    validation_status: str  # VALIDATED, REFUTED, INCONCLUSIVE
    notes: Optional[str] = None
