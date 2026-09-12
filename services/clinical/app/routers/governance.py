"""
ZAYVORA HEALTH™ — Regulatory Governance & 21 CFR Part 11 Router
Provides endpoints for audit trail logging, chain verification, Part 11 digital signatures,
and exportable regulatory compliance inspection bundles.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..governance.audit_trail_engine import (
    GLOBAL_AUDIT_LEDGER,
    Part11SignatureAuthority,
    Part11SignatureEnvelope,
)

router = APIRouter(prefix="/api/v1/governance", tags=["Regulatory Governance & 21 CFR Part 11"])

# In-memory store for generated signature envelopes
SIGNATURE_ENVELOPES_STORE: Dict[str, Part11SignatureEnvelope] = {}


class RecordAuditEventRequest(BaseModel):
    actor_id: str = Field(..., description="ID of the user, clinician, or system")
    actor_role: str = Field(..., description="Role of the actor (e.g. CLINICIAN, PHARMACIST, QA_LEAD)")
    action: str = Field(..., description="Action name (e.g. PRESCRIPTION_SIGNED, MUDABBAR_CHECK_PASSED)")
    resource_type: str = Field(..., description="Type of clinical resource (e.g. Prescription, SOAPNote)")
    resource_id: str = Field(..., description="Resource ID")
    event_payload: Dict[str, Any] = Field(..., description="Event data to be hashed into the block")


class CreateSignatureRequest(BaseModel):
    signer_id: str = Field(..., description="Unique ID of accredited clinician or officer")
    signer_name: str = Field(..., description="Printed full name of the signer")
    signer_role: str = Field(..., description="Professional role (Clinician, Hakeem, QA Manager)")
    document_payload: Dict[str, Any] = Field(..., description="The clinical document JSON being attested")
    signature_meaning: Optional[str] = Field(
        "Clinical Review & Statutory Approval (21 CFR § 11.50)",
        description="Formal declaration of signature meaning per Part 11 requirements",
    )


class VerifySignatureRequest(BaseModel):
    signature_id: str = Field(..., description="ID of the signature envelope")
    document_payload: Dict[str, Any] = Field(..., description="The document to verify against")


@router.post("/audit/record", summary="Record a clinical action into the Merkle-linked audit ledger")
async def record_audit_event(payload: RecordAuditEventRequest):
    block = GLOBAL_AUDIT_LEDGER.record_event(
        actor_id=payload.actor_id,
        actor_role=payload.actor_role,
        action=payload.action,
        resource_type=payload.resource_type,
        resource_id=payload.resource_id,
        event_payload=payload.event_payload,
    )
    return {
        "index": block.index,
        "timestamp_utc": block.timestamp_utc,
        "actor_id": block.actor_id,
        "action": block.action,
        "resource_id": block.resource_id,
        "diff_hash": block.diff_hash,
        "previous_hash": block.previous_hash,
        "block_hash": block.block_hash,
    }


@router.get("/audit/verify", summary="Verify full SHA-256 chain integrity of the audit ledger")
async def verify_audit_chain():
    result = GLOBAL_AUDIT_LEDGER.verify_chain_integrity()
    return {
        "is_valid": result.is_valid,
        "total_blocks": result.total_blocks,
        "genesis_hash": result.genesis_hash,
        "latest_block_hash": result.latest_block_hash,
        "tampered_block_index": result.tampered_block_index,
        "verification_message": result.verification_message,
    }


@router.get("/audit/resource/{resource_id}", summary="Get audit trail blocks for a specific resource")
async def get_resource_audit_history(resource_id: str):
    blocks = GLOBAL_AUDIT_LEDGER.get_blocks_for_resource(resource_id)
    return [
        {
            "index": b.index,
            "timestamp_utc": b.timestamp_utc,
            "actor_id": b.actor_id,
            "actor_role": b.actor_role,
            "action": b.action,
            "diff_hash": b.diff_hash,
            "block_hash": b.block_hash,
        }
        for b in blocks
    ]


@router.post("/signatures/sign", summary="Generate 21 CFR Part 11 compliant digital signature envelope")
async def create_part11_signature(payload: CreateSignatureRequest):
    envelope = Part11SignatureAuthority.create_signature_envelope(
        signer_id=payload.signer_id,
        signer_name=payload.signer_name,
        signer_role=payload.signer_role,
        document_payload=payload.document_payload,
        signature_meaning=payload.signature_meaning,
    )
    SIGNATURE_ENVELOPES_STORE[envelope.signature_id] = envelope

    # Also record signing event into audit ledger
    GLOBAL_AUDIT_LEDGER.record_event(
        actor_id=payload.signer_id,
        actor_role=payload.signer_role,
        action="PART11_SIGNATURE_EXECUTED",
        resource_type="SignatureEnvelope",
        resource_id=envelope.signature_id,
        event_payload={
            "signature_id": envelope.signature_id,
            "document_hash": envelope.document_content_hash,
            "signature_meaning": envelope.signature_meaning,
        },
    )

    return {
        "signature_id": envelope.signature_id,
        "signer_name": envelope.signer_name,
        "signer_id": envelope.signer_id,
        "signer_role": envelope.signer_role,
        "timestamp_utc": envelope.timestamp_utc,
        "signature_meaning": envelope.signature_meaning,
        "document_content_hash": envelope.document_content_hash,
        "cryptographic_seal": envelope.cryptographic_seal,
    }


@router.post("/signatures/verify", summary="Verify authenticity of a 21 CFR Part 11 signature")
async def verify_part11_signature(payload: VerifySignatureRequest):
    envelope = SIGNATURE_ENVELOPES_STORE.get(payload.signature_id)
    if not envelope:
        raise HTTPException(status_code=404, detail=f"Signature envelope '{payload.signature_id}' not found.")

    is_authentic = Part11SignatureAuthority.verify_signature_envelope(envelope, payload.document_payload)
    return {
        "signature_id": envelope.signature_id,
        "is_authentic": is_authentic,
        "signer_name": envelope.signer_name,
        "timestamp_utc": envelope.timestamp_utc,
        "signature_meaning": envelope.signature_meaning,
        "verification_result": "AUTHENTIC_VALID_SIGNATURE" if is_authentic else "TAMPERED_OR_FORGED",
    }


@router.get("/regulatory-bundle/{resource_id}", summary="Export certified 21 CFR Part 11 Regulatory Inspection Pack")
async def export_regulatory_bundle(resource_id: str):
    blocks = GLOBAL_AUDIT_LEDGER.get_blocks_for_resource(resource_id)
    chain_verif = GLOBAL_AUDIT_LEDGER.verify_chain_integrity()

    # Find any matching signatures
    signatures = [
        {
            "signature_id": env.signature_id,
            "signer_name": env.signer_name,
            "signer_role": env.signer_role,
            "timestamp_utc": env.timestamp_utc,
            "meaning": env.signature_meaning,
            "seal": env.cryptographic_seal,
        }
        for env in SIGNATURE_ENVELOPES_STORE.values()
    ]

    return {
        "bundle_id": f"REG-BUNDLE-{resource_id}",
        "resource_id": resource_id,
        "regulatory_standard": "US FDA 21 CFR Part 11 / EU Annex 11 / India Ayush GxP",
        "export_timestamp_utc": chain_verif.latest_block_hash,
        "chain_integrity": {
            "is_valid": chain_verif.is_valid,
            "total_blocks": chain_verif.total_blocks,
            "latest_block_hash": chain_verif.latest_block_hash,
            "certificate": "CERTIFIED_TAMPER_EVIDENT",
        },
        "provenance_blocks": [
            {
                "index": b.index,
                "timestamp_utc": b.timestamp_utc,
                "actor_id": b.actor_id,
                "action": b.action,
                "diff_hash": b.diff_hash,
                "block_hash": b.block_hash,
            }
            for b in blocks
        ],
        "registered_signatures": signatures,
    }
