"""
ZAYVORA HEALTH™ — Regulatory Readiness & 21 CFR Part 11 Audit Trail Engine
Implements SHA-256 Merkle-linked audit ledger, 21 CFR Part 11 electronic signature envelopes,
and tamper-evident inspection-ready compliance bundles.
"""

import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict


SIGNING_SECRET_KEY = "ZAYVORA_PART11_COMPLIANCE_SIGNING_ROOT_2035"


@dataclass
class AuditBlock:
    index: int
    timestamp_utc: str
    actor_id: str
    actor_role: str
    action: str
    resource_type: str
    resource_id: str
    diff_hash: str
    previous_hash: str
    block_hash: str


@dataclass
class Part11SignatureEnvelope:
    signature_id: str
    signer_name: str
    signer_id: str
    signer_role: str
    timestamp_utc: str
    signature_meaning: str  # e.g., "Review and Clinical Approval per 21 CFR § 11.50"
    document_content_hash: str
    cryptographic_seal: str  # HMAC-SHA256 seal


@dataclass
class AuditAnchor:
    anchor_id: str
    timestamp_utc: str
    from_block_index: int
    to_block_index: int
    total_blocks_anchored: int
    merkle_root: str
    previous_anchor_hash: str
    anchor_hash: str
    signature_seal: str


@dataclass
class AuditVerificationResult:
    is_valid: bool
    total_blocks: int
    genesis_hash: str
    latest_block_hash: str
    tampered_block_index: Optional[int] = None
    verification_message: str = "Audit trail integrity verified: 100% untampered."


class CryptographicAuditLedger:
    """In-memory cryptographic audit trail with SHA-256 hash chaining and Merkle root anchoring."""

    def __init__(self):
        self.chain: List[AuditBlock] = []
        self.anchors: List[AuditAnchor] = []
        self.last_anchored_index: int = -1
        self._initialize_genesis_block()

    def _initialize_genesis_block(self):
        genesis_diff = hashlib.sha256(b"ZAYVORA_GENESIS_STATE_2026").hexdigest()
        genesis_prev = "0" * 64
        genesis_hash = self._calculate_block_hash(
            index=0,
            timestamp="2026-01-01T00:00:00Z",
            actor_id="SYSTEM",
            actor_role="ROOT",
            action="GENESIS_INITIALIZATION",
            resource_type="SYSTEM",
            resource_id="ZAYVORA_ROOT",
            diff_hash=genesis_diff,
            previous_hash=genesis_prev,
        )
        genesis_block = AuditBlock(
            index=0,
            timestamp_utc="2026-01-01T00:00:00Z",
            actor_id="SYSTEM",
            actor_role="ROOT",
            action="GENESIS_INITIALIZATION",
            resource_type="SYSTEM",
            resource_id="ZAYVORA_ROOT",
            diff_hash=genesis_diff,
            previous_hash=genesis_prev,
            block_hash=genesis_hash,
        )
        self.chain.append(genesis_block)

    @staticmethod
    def _calculate_block_hash(
        index: int,
        timestamp: str,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        diff_hash: str,
        previous_hash: str,
    ) -> str:
        payload = f"{index}:{timestamp}:{actor_id}:{actor_role}:{action}:{resource_type}:{resource_id}:{diff_hash}:{previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def record_event(
        self,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        event_payload: Dict[str, Any],
    ) -> AuditBlock:
        """Appends an immutable block linked to the previous block hash."""
        now_utc = datetime.now(timezone.utc).isoformat()
        diff_raw = json.dumps(event_payload, sort_keys=True)
        diff_hash = hashlib.sha256(diff_raw.encode("utf-8")).hexdigest()

        previous_block = self.chain[-1]
        next_index = previous_block.index + 1
        previous_hash = previous_block.block_hash

        block_hash = self._calculate_block_hash(
            index=next_index,
            timestamp=now_utc,
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            diff_hash=diff_hash,
            previous_hash=previous_hash,
        )

        block = AuditBlock(
            index=next_index,
            timestamp_utc=now_utc,
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            diff_hash=diff_hash,
            previous_hash=previous_hash,
            block_hash=block_hash,
        )
        self.chain.append(block)
        return block

    def verify_chain_integrity(self) -> AuditVerificationResult:
        """Verifies full hash chain continuity from genesis to latest block."""
        if not self.chain:
            return AuditVerificationResult(
                is_valid=False,
                total_blocks=0,
                genesis_hash="",
                latest_block_hash="",
                tampered_block_index=0,
                verification_message="Empty audit chain.",
            )

        # Check genesis
        genesis = self.chain[0]
        expected_genesis_hash = self._calculate_block_hash(
            index=genesis.index,
            timestamp=genesis.timestamp_utc,
            actor_id=genesis.actor_id,
            actor_role=genesis.actor_role,
            action=genesis.action,
            resource_type=genesis.resource_type,
            resource_id=genesis.resource_id,
            diff_hash=genesis.diff_hash,
            previous_hash=genesis.previous_hash,
        )
        if genesis.block_hash != expected_genesis_hash or genesis.previous_hash != "0" * 64:
            return AuditVerificationResult(
                is_valid=False,
                total_blocks=len(self.chain),
                genesis_hash=genesis.block_hash,
                latest_block_hash=self.chain[-1].block_hash,
                tampered_block_index=0,
                verification_message="Genesis block hash mismatch or broken origin.",
            )

        # Check subsequent blocks
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # 1. Previous hash link check
            if curr.previous_hash != prev.block_hash:
                return AuditVerificationResult(
                    is_valid=False,
                    total_blocks=len(self.chain),
                    genesis_hash=genesis.block_hash,
                    latest_block_hash=self.chain[-1].block_hash,
                    tampered_block_index=curr.index,
                    verification_message=f"Hash chain broken at block {curr.index}: previous_hash does not match parent block {prev.index}.",
                )

            # 2. Re-compute block hash
            recomputed = self._calculate_block_hash(
                index=curr.index,
                timestamp=curr.timestamp_utc,
                actor_id=curr.actor_id,
                actor_role=curr.actor_role,
                action=curr.action,
                resource_type=curr.resource_type,
                resource_id=curr.resource_id,
                diff_hash=curr.diff_hash,
                previous_hash=curr.previous_hash,
            )
            if curr.block_hash != recomputed:
                return AuditVerificationResult(
                    is_valid=False,
                    total_blocks=len(self.chain),
                    genesis_hash=genesis.block_hash,
                    latest_block_hash=self.chain[-1].block_hash,
                    tampered_block_index=curr.index,
                    verification_message=f"Block {curr.index} payload or header was modified after recording (hash mismatch).",
                )

        return AuditVerificationResult(
            is_valid=True,
            total_blocks=len(self.chain),
            genesis_hash=genesis.block_hash,
            latest_block_hash=self.chain[-1].block_hash,
            tampered_block_index=None,
            verification_message=f"Audit chain intact ({len(self.chain)} blocks). All SHA-256 cryptographic proofs verified.",
        )

    def get_blocks_for_resource(self, resource_id: str) -> List[AuditBlock]:
        return [b for b in self.chain if b.resource_id == resource_id]

    @staticmethod
    def _compute_merkle_root(hashes: List[str]) -> str:
        if not hashes:
            return hashlib.sha256(b"EMPTY_MERKLE_ROOT").hexdigest()
        level = list(hashes)
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else left
                combined = hashlib.sha256((left + right).encode("utf-8")).hexdigest()
                next_level.append(combined)
            level = next_level
        return level[0]

    def generate_merkle_anchor(self) -> AuditAnchor:
        """Calculates and signs a certified Merkle root anchor of the ledger blocks."""
        if not self.chain:
            raise ValueError("Cannot anchor an empty ledger.")

        start_idx = self.last_anchored_index + 1
        end_idx = len(self.chain) - 1
        if start_idx > end_idx:
            start_idx = end_idx

        blocks_to_anchor = self.chain[start_idx : end_idx + 1]
        block_hashes = [b.block_hash for b in blocks_to_anchor]
        merkle_root = self._compute_merkle_root(block_hashes)

        prev_anchor_hash = self.anchors[-1].anchor_hash if self.anchors else ("0" * 64)
        now_utc = datetime.now(timezone.utc).isoformat()
        anchor_id = f"ANC-{hashlib.sha256(f'{start_idx}:{end_idx}:{merkle_root}:{now_utc}'.encode()).hexdigest()[:12].upper()}"

        raw_payload = f"{anchor_id}:{start_idx}:{end_idx}:{merkle_root}:{prev_anchor_hash}:{now_utc}"
        anchor_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

        seal = hmac.new(
            SIGNING_SECRET_KEY.encode("utf-8"),
            raw_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        anchor = AuditAnchor(
            anchor_id=anchor_id,
            timestamp_utc=now_utc,
            from_block_index=start_idx,
            to_block_index=end_idx,
            total_blocks_anchored=len(blocks_to_anchor),
            merkle_root=merkle_root,
            previous_anchor_hash=prev_anchor_hash,
            anchor_hash=anchor_hash,
            signature_seal=seal,
        )
        self.anchors.append(anchor)
        self.last_anchored_index = end_idx
        return anchor

    def get_anchors(self) -> List[AuditAnchor]:
        return list(self.anchors)

    def verify_anchor_integrity(self) -> bool:
        if not self.anchors:
            return True
        prev_hash = "0" * 64
        for anc in self.anchors:
            if anc.previous_anchor_hash != prev_hash:
                return False
            raw_payload = f"{anc.anchor_id}:{anc.from_block_index}:{anc.to_block_index}:{anc.merkle_root}:{anc.previous_anchor_hash}:{anc.timestamp_utc}"
            recomputed_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()
            if recomputed_hash != anc.anchor_hash:
                return False
            expected_seal = hmac.new(
                SIGNING_SECRET_KEY.encode("utf-8"),
                raw_payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            if not hmac.compare_digest(anc.signature_seal, expected_seal):
                return False
            prev_hash = anc.anchor_hash
        return True


class Part11SignatureAuthority:
    """Generates and verifies FDA 21 CFR Part 11 compliant digital signatures."""

    @classmethod
    def create_signature_envelope(
        cls,
        signer_id: str,
        signer_name: str,
        signer_role: str,
        document_payload: Dict[str, Any],
        signature_meaning: str = "Clinical Review & Statutory Approval (21 CFR § 11.50)",
    ) -> Part11SignatureEnvelope:
        now_utc = datetime.now(timezone.utc).isoformat()
        doc_raw = json.dumps(document_payload, sort_keys=True)
        doc_hash = hashlib.sha256(doc_raw.encode("utf-8")).hexdigest()

        # Compute cryptographic HMAC seal
        seal_payload = f"{signer_id}:{signer_role}:{now_utc}:{signature_meaning}:{doc_hash}"
        seal = hmac.new(
            SIGNING_SECRET_KEY.encode("utf-8"),
            seal_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        sig_id = f"SIG-{hashlib.sha256(seal.encode()).hexdigest()[:12].upper()}"

        return Part11SignatureEnvelope(
            signature_id=sig_id,
            signer_name=signer_name,
            signer_id=signer_id,
            signer_role=signer_role,
            timestamp_utc=now_utc,
            signature_meaning=signature_meaning,
            document_content_hash=doc_hash,
            cryptographic_seal=seal,
        )

    @classmethod
    def verify_signature_envelope(
        cls, envelope: Part11SignatureEnvelope, document_payload: Dict[str, Any]
    ) -> bool:
        doc_raw = json.dumps(document_payload, sort_keys=True)
        expected_doc_hash = hashlib.sha256(doc_raw.encode("utf-8")).hexdigest()

        if envelope.document_content_hash != expected_doc_hash:
            return False

        seal_payload = f"{envelope.signer_id}:{envelope.signer_role}:{envelope.timestamp_utc}:{envelope.signature_meaning}:{expected_doc_hash}"
        expected_seal = hmac.new(
            SIGNING_SECRET_KEY.encode("utf-8"),
            seal_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(envelope.cryptographic_seal, expected_seal)


# Singleton audit ledger for clinical service runtime
GLOBAL_AUDIT_LEDGER = CryptographicAuditLedger()
