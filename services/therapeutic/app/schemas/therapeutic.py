from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PatientSafetyContext(BaseModel):
    """The caller (eventually an orchestrator in Phase 4 assembling this
    from services/clinical + services/knowledge) supplies patient safety
    context directly for now — see docs/PHASE3-THERAPEUTIC-CORE.md for why
    this service doesn't call other services itself yet."""

    age: int | None = None
    pregnancy_status: str = Field(default="not_applicable", pattern="^(pregnant|not_pregnant|unknown|not_applicable)$")
    lactation_status: str = Field(default="no", pattern="^(yes|no)$")
    allergies: list[str] = Field(default_factory=list)
    current_medications: list[str] = Field(default_factory=list)
    comorbidities: list[str] = Field(default_factory=list)
    chief_complaint: str = Field(default="", max_length=2000)


class NuskhaIngredient(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    mufrad_id: str | None = None
    afal: str = Field(default="", max_length=500)
    miqdaar: str = Field(default="", max_length=100)
    musleh: str = Field(default="", max_length=200)
    badal: str = Field(default="", max_length=200)
    is_mudabbar: bool | None = Field(default=None, description="Whether ingredient has undergone classical Mudabbar detoxification")
    mudabbar_process: str = Field(default="", max_length=500, description="Classical detoxification method applied")
    dose_mg: float | None = Field(default=None, description="Ingredient dose in milligrams for ceiling evaluation")
    mizaj_temperament: str | None = Field(default=None, description="Mizaj temperament (Damwi, Safrawi, Saudawi, Balghami)")
    mizaj_degree_hc: int | None = Field(default=None, ge=1, le=4, description="Hot/Cold degree (1-4)")
    mizaj_degree_wd: int | None = Field(default=None, ge=1, le=4, description="Wet/Dry degree (1-4)")


class NuskhaDraftCreate(BaseModel):
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    patient_safety_context: PatientSafetyContext
    mizaj_context: dict = Field(default_factory=dict)
    asbab: str = Field(default="", max_length=2000)
    tashkhis: str = Field(default="", max_length=2000)
    organ_axis_context: list[str] = Field(default_factory=list)
    usool_e_ilaj: str = Field(default="", max_length=1000)
    therapeutic_objective: str = Field(default="", max_length=1000)
    ingredients: list[NuskhaIngredient] = Field(min_length=1)
    dosage_form: str = Field(default="", max_length=100)
    dose: str = Field(default="", max_length=200)
    timing: str = Field(default="", max_length=200)
    duration: str = Field(default="", max_length=200)
    parhez: str = Field(default="", max_length=1000)


class NuskhaApprove(BaseModel):
    safety_override_justification: str = Field(default="", max_length=2000)
    clinician_registration_number: str = Field(default="", max_length=100)


class NuskhaReject(BaseModel):
    rejection_reason: str = Field(min_length=1, max_length=2000)


class NuskhaDraftOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    created_by_user_id: str
    mizaj_context: dict
    asbab: str
    tashkhis: str
    organ_axis_context: list[str]
    usool_e_ilaj: str
    therapeutic_objective: str
    ingredients: list[dict]
    dosage_form: str
    dose: str
    timing: str
    duration: str
    parhez: str
    safety_verdict: str
    safety_reasons: list[str]
    status: str
    reviewed_by_user_id: str | None
    clinician_registration_number: str = ""
    reviewed_at: datetime | None
    rejection_reason: str
    safety_override_justification: str
    created_at: datetime


class TadbeerPlanCreate(BaseModel):
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    patient_safety_context: PatientSafetyContext | None = None
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(pattern="^(regimen|rest|physical_activity|massage|bathing|other)$")
    indication: str = Field(default="", max_length=1000)
    method: str = Field(default="", max_length=2000)
    frequency: str = Field(default="", max_length=100)
    duration: str = Field(default="", max_length=100)
    contraindications: str = Field(default="", max_length=1000)
    practitioner_requirements: str = Field(default="", max_length=1000)


class TadbeerPlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    name: str
    category: str
    indication: str
    method: str
    frequency: str
    duration: str
    contraindications: str
    practitioner_requirements: str
    safety_verdict: str = "SAFE_TO_CONSIDER"
    safety_reasons: list[str] = Field(default_factory=list)
    status: str
    created_at: datetime


class NuskhaCompileRequest(BaseModel):
    target_organ_axes: list[str] = Field(default_factory=list)
    therapeutic_objective: str = Field(default="", max_length=1000)
    patient_safety_context: PatientSafetyContext
    ingredients: list[NuskhaIngredient] = Field(min_length=1)


class CompiledIngredientOut(BaseModel):
    name: str
    classical_role: str
    target_axis_alignment: str
    prescribed_dose_mg: float
    clinically_adjusted_dose_mg: float
    posology_adjustments: list[str] = Field(default_factory=list)
    musleh: str = ""
    badal: str = ""
    is_mudabbar: bool | None = None
    mudabbar_process: str = ""


class NuskhaCompileResponse(BaseModel):
    status: str
    juz_e_azam: str | None
    target_organ_axes: list[str]
    therapeutic_objective: str
    is_formulation_balanced: bool
    missing_musleh_alerts: list[str]
    substitute_suggestions: list[dict]
    compiled_ingredients: list[CompiledIngredientOut]


class GhizaPlanCreate(BaseModel):
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    dietary_goals: str = Field(default="", max_length=1000)
    meal_structure: str = Field(default="", max_length=2000)
    foods_recommended: list[str] = Field(default_factory=list)
    foods_to_limit: list[str] = Field(default_factory=list)
    hydration_guidance: str = Field(default="", max_length=500)


class GhizaPlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    dietary_goals: str
    meal_structure: str
    foods_recommended: list[str]
    foods_to_limit: list[str]
    hydration_guidance: str
    status: str
    created_at: datetime


class AsbabSittahSchema(BaseModel):
    """The Six Essential Pre-requisites of Health (Asbab Sittah Daruriyyah)."""
    hawa_muheet: str = Field(default="", description="Ambient Air, Season, Environmental Ventilation")
    makool_mashroob: str = Field(default="", description="Food and Drink, Dietary Temperament & Timing")
    harkat_sukoon_badani: str = Field(default="", description="Bodily Movement and Rest, Physical Exercise/Regimens")
    harkat_sukoon_nafsani: str = Field(default="", description="Psychic/Emotional Movement and Rest, Stress & Mental Equilibrium")
    naum_yaqzah: str = Field(default="", description="Sleep and Wakefulness, Circadian Sleep Hygiene")
    istifragh_ihtibas: str = Field(default="", description="Evacuation and Retention, Normal Excretory Dynamics")


class CarePlanCreate(BaseModel):
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    title: str = Field(min_length=3, max_length=255)
    horizon: str = Field(default="stabilization", pattern="^(acute|stabilization|maintenance)$")
    duration_days: int = Field(default=30, ge=1, le=365)
    mizaj_context: dict = Field(default_factory=dict)
    usool_e_ilaj: str = Field(default="", max_length=2000)
    primary_indication: str = Field(default="", max_length=255)
    ilaj_bid_dawa: list[dict] = Field(default_factory=list)
    ilaj_bit_tadbeer: list[dict] = Field(default_factory=list)
    ilaj_bil_ghiza: dict = Field(default_factory=dict)
    asbab_sittah: AsbabSittahSchema = Field(default_factory=AsbabSittahSchema)
    review_milestones: list[dict] = Field(default_factory=list)
    prognosis_notes: str = Field(default="", max_length=2000)


class CarePlanSign(BaseModel):
    clinician_registration_number: str = Field(min_length=3, max_length=100)
    statutory_affirmation: bool = Field(..., description="Clinician confirms personal clinical review of posology and safety")


class CarePlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: uuid.UUID
    created_by_user_id: str
    title: str
    horizon: str
    duration_days: int
    mizaj_context: dict
    usool_e_ilaj: str
    primary_indication: str
    ilaj_bid_dawa: list[dict]
    ilaj_bit_tadbeer: list[dict]
    ilaj_bil_ghiza: dict
    asbab_sittah: dict
    review_milestones: list[dict]
    prognosis_notes: str
    safe_to_lock: bool
    signed_by_clinician_id: str | None
    clinician_registration_number: str
    signed_at: datetime | None
    status: str
    created_at: datetime
    updated_at: datetime


class ADRReportCreate(BaseModel):
    """Adverse Drug Reaction / Botanical Adverse Event Report for Pharmacovigilance."""
    patient_id: uuid.UUID
    suspected_agent: str = Field(min_length=1, max_length=255, description="Herb, compound, or medicine name")
    batch_number: str = Field(default="", max_length=100)
    adverse_reaction_description: str = Field(min_length=5, max_length=2000)
    latency_hours: float | None = Field(default=None, description="Onset time after drug administration in hours")
    dechallenge_performed: bool = Field(default=False)
    dechallenge_outcome: str = Field(default="unknown", pattern="^(improved|no_change|worsened|unknown)$")
    rechallenge_performed: bool = Field(default=False)
    rechallenge_outcome: str = Field(default="not_applicable", pattern="^(positive|negative|not_applicable)$")
    concomitant_drugs: list[str] = Field(default_factory=list)
    alternative_etiologies_considered: list[str] = Field(default_factory=list)
    is_schedule_e1_substance: bool = Field(default=False)
    verified_mudabbar_protocol_followed: bool = Field(default=True)


class WHOUMCResultOut(BaseModel):
    causality_category: str  # CERTAIN, PROBABLE, POSSIBLE, UNLIKELY, CONDITIONAL_UNCLASSIFIED, UNCLASSIFIABLE
    causality_score: int
    rationale: str
    statutory_warning: str | None = None
    regulatory_action_required: bool
    recommendations: list[str]


class InventoryBatchCreate(BaseModel):
    medication_name: str = Field(min_length=1, max_length=255)
    formulation_type: str = Field(default="murakkab", pattern="^(mufrad|murakkab|oil|syrup|kushta|powder)$")
    batch_number: str = Field(min_length=1, max_length=100)
    manufacturer: str = Field(default="ZAYVORA GMP Dispensary", max_length=255)
    manufacturing_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    expiry_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    initial_quantity: float = Field(gt=0)
    unit: str = Field(default="g", max_length=30)
    is_schedule_e1: bool = Field(default=False)
    mudabbar_certified: bool = Field(default=False)
    mudabbar_certificate_number: str | None = None


class InventoryBatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    organization_id: uuid.UUID
    medication_name: str
    formulation_type: str
    batch_number: str
    manufacturer: str
    manufacturing_date: str
    expiry_date: str
    initial_quantity: float
    available_quantity: float
    unit: str
    is_schedule_e1: bool
    mudabbar_certified: bool
    mudabbar_certificate_number: str | None
    qc_release_status: str
    created_at: datetime


class DispenseRequest(BaseModel):
    prescription_id: uuid.UUID
    patient_id: uuid.UUID
    medication_name: str = Field(min_length=1, max_length=255)
    quantity_requested: float = Field(gt=0)
    is_schedule_e1: bool = Field(default=False)
    pharmacist_license_number: str = Field(min_length=3, max_length=100)
    patient_counseling_notes: str = Field(default="", max_length=2000)


class DispenseRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    organization_id: uuid.UUID
    prescription_id: uuid.UUID
    patient_id: uuid.UUID
    batch_id: uuid.UUID
    batch_number: str
    quantity_dispensed: float
    dispensed_by_pharmacist_id: str
    pharmacist_license_number: str
    patient_counseling_notes: str
    mudabbar_verified_at_dispense: bool
    dispensed_at: datetime


class BatchRecallRequest(BaseModel):
    reason: str = Field(min_length=5, max_length=2000)
    recall_class: str = Field(default="CLASS_I", pattern="^(CLASS_I|CLASS_II|CLASS_III)$")


class BatchRecallOut(BaseModel):
    batch_number: str
    medication_name: str
    previous_status: str
    new_status: str
    recall_class: str
    reason: str
    recalled_by_user_id: str
    recalled_at: str
    action_required: str


