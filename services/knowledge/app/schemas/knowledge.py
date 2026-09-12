from __future__ import annotations

from pydantic import BaseModel, Field


class MufradCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    botanical_name: str = Field(default="", max_length=200)
    part_used: str = Field(default="", max_length=200)
    synonyms: list[str] = Field(default_factory=list)
    afal: list[str] = Field(default_factory=list, description="Af'al — classical actions, e.g. Muqawwi-e-Qalb")
    traditional_uses: str = Field(default="", max_length=3000)
    contraindications: str = Field(default="", max_length=2000)
    musleh: str = Field(default="", max_length=500, description="Corrective/adjuvant ingredient")
    badal: str = Field(default="", max_length=500, description="Substitute ingredient")
    dose: str = Field(default="", max_length=200)
    modern_pharmacology: str = Field(default="", max_length=3000)


class MufradOut(BaseModel):
    id: str
    name: str
    botanicalName: str
    partUsed: str
    synonyms: list[str]
    afal: list[str]
    traditionalUses: str
    contraindications: str
    musleh: str
    badal: str
    dose: str
    modernPharmacology: str


class MufradDetailOut(MufradOut):
    mizaj: list[dict] = Field(default_factory=list)
    organAxes: list[dict] = Field(default_factory=list)


class MizajAssign(BaseModel):
    temperament: str = Field(pattern="^(Damwi|Safrawi|Saudawi|Balghami)$")
    hc_degree: int = Field(ge=1, le=4, description="Hot(+)/Cold(-) degree magnitude, classical 1st-4th degree")
    wd_degree: int = Field(ge=1, le=4, description="Wet(+)/Dry(-) degree magnitude, classical 1st-4th degree")


class AxisLink(BaseModel):
    axis_code: str


class EvidenceCreate(BaseModel):
    level: str = Field(pattern="^E[0-6]$")
    knowledge_world: str = Field(pattern="^[ABCD]$")
    source: str = Field(default="", max_length=500)
    study_type: str = Field(default="", max_length=200)
    summary: str = Field(default="", max_length=2000)
    reviewer: str = Field(default="", max_length=200)
    review_status: str = Field(default="pending", pattern="^(pending|reviewed|approved|rejected)$")


class EvidenceOut(BaseModel):
    id: str
    level: str
    knowledgeWorld: str
    source: str
    studyType: str
    summary: str
    reviewer: str
    reviewStatus: str


class EvidenceClassifyRequest(BaseModel):
    text: str = Field(min_length=5, max_length=5000, description="Title, abstract, or methodology text of study")


class EvidenceClassifyResponse(BaseModel):
    predicted_level: str
    level_name: str
    knowledge_world: str
    study_type: str
    confidence: float
    requires_peer_review: bool
    peer_review_status: str
    governance_note: str


class GRADEScoreRequest(BaseModel):
    starting_level: str = Field(pattern="^E[0-6]$")
    risk_of_bias: int = Field(default=0, ge=0, le=2)
    inconsistency: int = Field(default=0, ge=0, le=2)
    indirectness: int = Field(default=0, ge=0, le=2)
    imprecision: int = Field(default=0, ge=0, le=2)
    publication_bias: int = Field(default=0, ge=0, le=1)
    large_effect_size: int = Field(default=0, ge=0, le=2)
    dose_response_gradient: int = Field(default=0, ge=0, le=1)


class GRADEScoreResponse(BaseModel):
    starting_level: str
    baseline_score: int
    total_downgrades: int
    total_upgrades: int
    net_grade_score: int
    grade_certainty: str
    evaluation_notes: list[str]

