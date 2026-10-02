"""
ZAYVORA AGENTIC CLINICAL AI™ — Models & Schema Definitions
===========================================================
Defines the canonical data types, states, risk levels, and governance structures
for Hakeem Sahab AI™ Production Architecture.
Supports both Pydantic (in FastAPI service runtime) and pure Standard Library (in isolated tests).
"""

from __future__ import annotations
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

        def model_dump(self) -> Dict[str, Any]:
            res = {}
            for k, v in self.__dict__.items():
                if isinstance(v, BaseModel):
                    res[k] = v.model_dump()
                elif isinstance(v, list):
                    res[k] = [item.model_dump() if isinstance(item, BaseModel) else item for item in v]
                elif isinstance(v, Enum):
                    res[k] = v.value
                else:
                    res[k] = v
            return res

        def dict(self) -> Dict[str, Any]:
            return self.model_dump()

    def Field(default=None, default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory()
        return default


class AgentState(str, Enum):
    # Core Happy-Path State Machine Flow
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    RETRIEVING = "RETRIEVING"
    ANALYZING = "ANALYZING"
    SAFETY_REVIEW = "SAFETY_REVIEW"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"

    # Terminal / Hold / Exception States
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    REQUIRES_INPUT = "REQUIRES_INPUT"
    REQUIRES_CLINICIAN = "REQUIRES_CLINICIAN"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class RiskLevel(str, Enum):
    """
    Action Risk Levels (§18):
    R0 — Informational (read availability)
    R1 — Low-risk operational (create reminder)
    R2 — Sensitive (access detailed PHI)
    R3 — Clinically meaningful (prepare Nuskha draft)
    R4 — High-impact clinical (finalize/sign Rx -> Clinician only)
    R5 — Privileged/system (modify governance -> Admin only)
    """
    R0_INFORMATIONAL = "R0_INFORMATIONAL"
    R1_LOW_RISK_OPERATIONAL = "R1_LOW_RISK_OPERATIONAL"
    R2_SENSITIVE = "R2_SENSITIVE"
    R3_CLINICALLY_MEANINGFUL = "R3_CLINICALLY_MEANINGFUL"
    R4_HIGH_IMPACT_CLINICAL = "R4_HIGH_IMPACT_CLINICAL"
    R5_PRIVILEGED_SYSTEM = "R5_PRIVILEGED_SYSTEM"


class SafetyState(str, Enum):
    """
    Deterministic Safety Gate States (§7):
    PASS     -> Action can proceed to next permitted stage.
    CAUTION  -> Mandatory clinician acknowledgement where defined.
    BLOCK    -> Action cannot proceed under any circumstances.
    UNKNOWN  -> Action cannot proceed until required information is resolved.
    """
    PASS = "PASS"
    CAUTION = "CAUTION"
    BLOCK = "BLOCK"
    UNKNOWN = "UNKNOWN"


class ClinicianDecision(str, Enum):
    """
    Clinician Action at Approval Gate (§31):
    Never 'Execute AI Recommendation'. Must be explicit human decision.
    """
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    REJECT = "REJECT"
    DEFER = "DEFER"


class MemoryTier(str, Enum):
    """
    Controlled Healthcare Memory Tiers (§15):
    Never mix patient memory with organizational knowledge.
    """
    SHORT_TERM_WORKING = "SHORT_TERM_WORKING"
    LONGITUDINAL_CLINICAL = "LONGITUDINAL_CLINICAL"
    KNOWLEDGE_MEMORY = "KNOWLEDGE_MEMORY"


class ProvenanceRecord(BaseModel):
    """
    Standardized Provenance Envelope (§24):
    Answers: What data? What knowledge? Which version? What evidence?
    """
    source_id: str
    knowledge_version: str
    retrieval_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_category: str = "TRADITIONAL_TREATISE_AND_PHARMACOPOEIA"
    review_status: str = "GOVERNANCE_VERIFIED"
    reviewed_by: str = "ZAYVORA Clinical Governance Board"
    limitations: Optional[str] = None
    citations: List[str] = Field(default_factory=list)


class ToolDeclaration(BaseModel):
    """
    Controlled Tool Declaration (§17):
    Every tool must declare its parameters, scope, and safety boundaries.
    """
    tool_id: str
    description: str
    required_permission: str
    allowed_roles: List[str]
    data_scope: str
    risk_level: RiskLevel
    approval_required: bool
    audit_required: bool = True


class SafetyCheckResult(BaseModel):
    state: SafetyState
    reasons: List[str] = Field(default_factory=list)
    contraindications_found: List[Dict[str, Any]] = Field(default_factory=list)
    missing_critical_data: List[str] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SensingSignalValidation(BaseModel):
    source: str  # "NABZ" or "LISAN"
    is_usable: bool
    quality_score: float  # 0.0 to 1.0
    quality_flags: List[str] = Field(default_factory=list)
    rejection_reason: Optional[str] = None


class AgentRunRecord(BaseModel):
    """
    Observability & Audit Record for Agent Execution (§23).
    """
    run_id: str
    patient_id: Optional[str] = None
    encounter_id: Optional[str] = None
    actor_id: str = "DOC-01"
    role: str = "DOCTOR"
    organization_id: str = "ORG-ZAYVORA-01"
    facility_id: str = "FACILITY-DELHI-01"
    state: AgentState = AgentState.CREATED
    safety_result: Optional[SafetyCheckResult] = None
    clinician_decision: Optional[ClinicianDecision] = None
    clinician_notes: Optional[str] = None
    clinician_signature: Optional[str] = None
    tools_invoked: List[str] = Field(default_factory=list)
    provenance: List[ProvenanceRecord] = Field(default_factory=list)
    evidence_summary: Optional[Dict[str, Any]] = None
    output_payload: Optional[Dict[str, Any]] = None
    verification_status: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
