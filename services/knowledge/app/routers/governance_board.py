"""
ZAYVORA HEALTH™ — Clinical Governance Board Router
Provides endpoints for creating change proposals, multi-expert attestation, and publishing ratified change orders.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from ..board.governance_board import (
    ClinicalGovernanceBoardEngine,
    QuorumNotReachedError,
    UnauthorizedGovernanceRoleError,
    PROPOSALS_STORE,
)

router = APIRouter(prefix="/api/v1/knowledge/governance", tags=["Clinical Governance Board"])


class CreateProposalRequest(BaseModel):
    title: str = Field(..., description="Title of the monograph or posology change proposal")
    target_type: str = Field(..., description="UPI_MUFRAD, NFUM_COMPOUND, SCHEDULE_E1_LIMIT, EVIDENCE_GRADE")
    target_id: str = Field(..., description="Entity identifier (e.g. upi-kuchla)")
    proposed_diff: Dict[str, Any] = Field(..., description="Exact field changes and clinical rationale")
    created_by: str = Field(..., description="Clinician or researcher proposing the change")


class AttestProposalRequest(BaseModel):
    attestor_id: str = Field(..., description="Clinician ID")
    attestor_name: str = Field(..., description="Clinician full name")
    attestor_role: str = Field(..., description="SENIOR_TABEEB, CLINICAL_SPECIALIST, PHARMACOPOEIA_LEAD, DIRECTOR_OF_MEDICINE")
    intent: Optional[str] = Field("Clinical Verification & Pharmacopoeial Quorum Attestation", description="Signature attestation statement")


@router.post("/proposals", summary="Create a new knowledge or posology change proposal")
async def create_proposal(payload: CreateProposalRequest):
    proposal = ClinicalGovernanceBoardEngine.create_proposal(
        title=payload.title,
        target_type=payload.target_type,
        target_id=payload.target_id,
        proposed_diff=payload.proposed_diff,
        created_by=payload.created_by,
    )
    return {
        "proposal_id": proposal.proposal_id,
        "title": proposal.title,
        "target_type": proposal.target_type,
        "target_id": proposal.target_id,
        "status": proposal.status,
        "created_by": proposal.created_by,
        "created_at_utc": proposal.created_at_utc,
    }


@router.post("/proposals/{proposal_id}/attest", summary="Apply Board Member cryptographic attestation")
async def attest_proposal(proposal_id: str, payload: AttestProposalRequest):
    try:
        updated = ClinicalGovernanceBoardEngine.attest_proposal(
            proposal_id=proposal_id,
            attestor_id=payload.attestor_id,
            attestor_name=payload.attestor_name,
            attestor_role=payload.attestor_role,
            intent=payload.intent or "Clinical Verification & Pharmacopoeial Quorum Attestation",
        )
        return {
            "proposal_id": updated.proposal_id,
            "status": updated.status,
            "attestations_count": len(updated.attestations),
            "attestations": [
                {
                    "attestor_name": a.attestor_name,
                    "attestor_role": a.attestor_role,
                    "timestamp_utc": a.timestamp_utc,
                    "digital_seal": a.digital_seal,
                }
                for a in updated.attestations
            ],
        }
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except (UnauthorizedGovernanceRoleError, ValueError) as ue:
        raise HTTPException(status_code=403, detail=str(ue))


@router.post("/proposals/{proposal_id}/publish", summary="Ratify and publish change order (Enforces 2-expert quorum)")
async def publish_change_order(proposal_id: str):
    try:
        order = ClinicalGovernanceBoardEngine.publish_change_order(proposal_id)
        return {
            "change_order_id": order.change_order_id,
            "proposal_id": order.proposal_id,
            "title": order.title,
            "target_type": order.target_type,
            "target_id": order.target_id,
            "applied_diff": order.applied_diff,
            "published_at_utc": order.published_at_utc,
            "immutable_sha256_seal": order.immutable_sha256_seal,
            "attestations_count": len(order.attestations),
        }
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except QuorumNotReachedError as qe:
        raise HTTPException(status_code=412, detail=str(qe))


@router.get("/change-orders", summary="List all published and ratified clinical change orders")
async def list_change_orders():
    orders = ClinicalGovernanceBoardEngine.get_change_orders()
    return [
        {
            "change_order_id": o.change_order_id,
            "proposal_id": o.proposal_id,
            "title": o.title,
            "target_type": o.target_type,
            "target_id": o.target_id,
            "published_at_utc": o.published_at_utc,
            "immutable_sha256_seal": o.immutable_sha256_seal,
            "attestations_count": len(o.attestations),
        }
        for o in orders
    ]
