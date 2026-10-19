"""
ZFIE Core Types & Dataclasses
Defines immutable representations for scientific findings, multi-dimensional evidence,
provenance, and knowledge snapshots.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from packages.zfie.core.enums import (
    ClaimType,
    EvidenceLevel,
    EvidenceStrength,
    FindingStatus,
    SafetyVerdict,
    SynergyCandidateStatus,
    SynergyModel,
    ValidationStatus,
)


@dataclass
class ScientificEvidenceProfile:
    """Multidimensional evidence profile — eliminates deceptive single AI confidence scores."""
    traditional: EvidenceStrength = EvidenceStrength.STRONG
    chemical: EvidenceStrength = EvidenceStrength.MODERATE
    target: EvidenceStrength = EvidenceStrength.MODERATE
    pathway: EvidenceStrength = EvidenceStrength.MODERATE
    exposure: EvidenceStrength = EvidenceStrength.WEAK
    safety: EvidenceStrength = EvidenceStrength.STRONG
    human: EvidenceStrength = EvidenceStrength.WEAK
    combination: EvidenceStrength = EvidenceStrength.WEAK

    def to_dict(self) -> Dict[str, str]:
        return {k: v.value for k, v in asdict(self).items()}


@dataclass
class ZFIEFinding:
    """Standardized finding output contract for all ZFIE engines."""
    finding_id: str
    subject_id: str
    subject_version: str
    statement: str
    status: FindingStatus
    evidence_ids: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    provenance_ids: List[str] = field(default_factory=list)
    knowledge_version: str = "ZKB-2026.09"
    safety_state: SafetyVerdict = SafetyVerdict.PASS
    requires_clinician_review: bool = True
    model_version: Optional[str] = "ZFIE-MECH-0.4"
    claim_type: ClaimType = ClaimType.PREDICTED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "findingId": self.finding_id,
            "subjectId": self.subject_id,
            "subjectVersion": self.subject_version,
            "statement": self.statement,
            "status": self.status.value,
            "evidenceIds": self.evidence_ids,
            "limitations": self.limitations,
            "provenanceIds": self.provenance_ids,
            "knowledgeVersion": self.knowledge_version,
            "safetyState": self.safety_state.value,
            "requiresClinicianReview": self.requires_clinician_review,
            "modelVersion": self.model_version,
            "claimType": self.claim_type.value,
        }


@dataclass
class ProvenanceRecord:
    """Full scientific and licensing lineage for external data points."""
    provenance_id: str
    source_name: str
    dataset_version: str
    retrieval_date: str
    license_type: str
    commercial_use_permitted: bool
    derivative_rights_permitted: bool
    redistribution_permitted: bool
    attribution_requirement: str
    restrictions: List[str] = field(default_factory=list)
    doi_or_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KnowledgeSnapshot:
    """Exact version snapshot captured at the start of any analysis for guaranteed reproducibility."""
    snapshot_id: str
    created_at: float
    zkb_version: str = "2026.09"
    external_data_version: str = "snapshot-2026-09"
    models_version: str = "mechanism-0.4"
    safety_rules_version: str = "safety-2026.09"
    pathways_version: str = "snapshot-97"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BiologicalStateProfile:
    """Analytical biological-state representations covering 8 physiological systems."""
    metabolic: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["Glucose", "HbA1c"], "uncertainty": 0.12})
    inflammatory: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["hs-CRP", "TNF-a"], "uncertainty": 0.08})
    hepatic: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["ALT", "AST", "Bilirubin"], "uncertainty": 0.05})
    gastrointestinal: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["Microbiome diversity", "Permeability"], "uncertainty": 0.22})
    hormonal: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["Cortisol", "Thyroid Axis"], "uncertainty": 0.15})
    oxidative: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["MDA", "SOD"], "uncertainty": 0.14})
    mitochondrial: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["ATP synthesis", "Lactate/Pyruvate"], "uncertainty": 0.30})
    neurophysiological: Dict[str, Any] = field(default_factory=lambda: {"status": "EVALUATED", "markers": ["HRV", "Sleep efficiency"], "uncertainty": 0.18})

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnalysisJob:
    """Asynchronous analysis job envelope for heavy scientific computations."""
    job_id: str
    formulation_id: str
    formula_version_id: str
    batch_id: Optional[str]
    requested_by: str
    mode: str = "SHADOW"
    status: str = "QUEUED"  # QUEUED, PROCESSING, COMPLETED, FAILED
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
