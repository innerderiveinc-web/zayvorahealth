"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 5B: Scientific Review Board & Multi-Stage Governance Workflow
System: ZAYVORA Health OS™
Doctrine: Automated AI proposals require staged, auditable, multidisciplinary human governance approval before release.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class GovernanceStage(str, Enum):
    PROPOSAL = "PROPOSAL"
    SCIENTIFIC_REVIEW = "SCIENTIFIC_REVIEW"
    SAFETY_REVIEW = "SAFETY_REVIEW"
    CLINICAL_REVIEW = "CLINICAL_REVIEW"
    GOVERNANCE_APPROVED = "GOVERNANCE_APPROVED"
    RELEASED = "RELEASED"
    REJECTED = "REJECTED"


class ProposalDomain(str, Enum):
    FORMULATION_DESIGN = "FORMULATION_DESIGN"
    MOLECULAR_MECHANISM = "MOLECULAR_MECHANISM"
    SAFETY_RULE = "SAFETY_RULE"
    MODEL_PROMOTION = "MODEL_PROMOTION"
    EVIDENCE_PROMOTION = "EVIDENCE_PROMOTION"


@dataclass
class GovernanceSignoff:
    stage: GovernanceStage
    reviewer_id: str
    reviewer_role: str  # e.g., "CHIEF_PHARMACOLOGIST", "SAFETY_OFFICER", "SENIOR_TABEEB", "IRB_CHAIR"
    verdict: str        # "APPROVED" or "REJECTED"
    comments: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class ScientificProposal:
    proposal_id: str
    domain: ProposalDomain
    title: str
    proposed_by: str
    summary: str
    supporting_evidence_ids: List[str]
    current_stage: GovernanceStage
    signoffs: List[GovernanceSignoff] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["domain"] = self.domain.value
        d["current_stage"] = self.current_stage.value
        return d


class ScientificReviewBoard:
    """Enterprise Governance Workflow ensuring AI proposals undergo multidisciplinary review."""

    _PROPOSALS: Dict[str, ScientificProposal] = {}

    @classmethod
    def submit_proposal(
        cls,
        domain: ProposalDomain,
        title: str,
        proposed_by: str,
        summary: str,
        evidence_ids: List[str]
    ) -> ScientificProposal:
        pid = f"SRB-{uuid.uuid4().hex[:6].upper()}"
        prop = ScientificProposal(
            proposal_id=pid,
            domain=domain,
            title=title,
            proposed_by=proposed_by,
            summary=summary,
            supporting_evidence_ids=evidence_ids,
            current_stage=GovernanceStage.PROPOSAL
        )
        cls._PROPOSALS[pid] = prop
        return prop

    @classmethod
    def advance_stage(
        cls,
        proposal_id: str,
        reviewer_id: str,
        reviewer_role: str,
        approved: bool,
        comments: str = ""
    ) -> ScientificProposal:
        """Transitions proposal through the governance lifecycle."""
        if proposal_id not in cls._PROPOSALS:
            raise KeyError(f"Proposal {proposal_id} not found.")

        prop = cls._PROPOSALS[proposal_id]

        signoff = GovernanceSignoff(
            stage=prop.current_stage,
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            verdict="APPROVED" if approved else "REJECTED",
            comments=comments
        )
        prop.signoffs.append(signoff)

        if not approved:
            prop.current_stage = GovernanceStage.REJECTED
            return prop

        # Advance along the strict governance pipeline
        stage_flow = [
            GovernanceStage.PROPOSAL,
            GovernanceStage.SCIENTIFIC_REVIEW,
            GovernanceStage.SAFETY_REVIEW,
            GovernanceStage.CLINICAL_REVIEW,
            GovernanceStage.GOVERNANCE_APPROVED,
            GovernanceStage.RELEASED
        ]

        curr_idx = stage_flow.index(prop.current_stage)
        if curr_idx < len(stage_flow) - 1:
            prop.current_stage = stage_flow[curr_idx + 1]

        return prop

    @classmethod
    def list_proposals(cls) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in cls._PROPOSALS.values()]


# Pre-seed foundational canonical proposal
_seed_prop = ScientificReviewBoard.submit_proposal(
    domain=ProposalDomain.FORMULATION_DESIGN,
    title="Majun Suranjan Optimization for Targeted NF-kB/Microtubule Dual Inhibition",
    proposed_by="RESEARCH_AGENT_SYNTH",
    summary="Tripartite ratio of Suranjan, Filfil Siyah, and Muqil with calibrated Schedule E1 purification.",
    evidence_ids=["ZAY-EVD-91", "ZAY-EVD-0005"]
)
ScientificReviewBoard.advance_stage(
    _seed_prop.proposal_id,
    reviewer_id="DR-FAROOQI",
    reviewer_role="CHIEF_PHARMACOLOGIST",
    approved=True,
    comments="Biochemical mechanistic rationale verified against in-vitro binding data."
)
