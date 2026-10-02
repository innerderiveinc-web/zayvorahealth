"""
ZAYVORA HEALTH™ — Clinical Governance Board & Cryptographic Change Orders Engine
Enforces multi-expert peer review quorum (minimum 2 senior clinicians) before committing
revisions to UPI monographs, NFUM formulations, Schedule E(1) limits, or evidence grades.
"""

import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


import os
import sqlite3
from dataclasses import asdict

GOVERNANCE_SIGNING_KEY = os.getenv("GOVERNANCE_SIGNING_KEY", "ZAYVORA_GOVERNANCE_BOARD_ROOT_SEAL_2035")
SENIOR_BOARD_ROLES = {"SENIOR_TABEEB", "CLINICAL_SPECIALIST", "PHARMACOPOEIA_LEAD", "DIRECTOR_OF_MEDICINE"}

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
_DB_PATH = os.path.join(_BASE_DIR, "database", "zayvora_live.db")

def _get_governance_db():
    if os.path.exists(_DB_PATH):
        try:
            conn = sqlite3.connect(_DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception:
            return None
    return None

class QuorumNotReachedError(Exception):
    """Raised when an attempt is made to publish without meeting the 2-expert quorum."""
    pass


class UnauthorizedGovernanceRoleError(Exception):
    """Raised when an unauthorized role attempts to attest to a governance change order."""
    pass


@dataclass
class BoardAttestation:
    attestor_id: str
    attestor_name: str
    attestor_role: str
    timestamp_utc: str
    attestation_intent: str
    digital_seal: str


@dataclass
class ChangeProposal:
    proposal_id: str
    title: str
    target_type: str        # "UPI_MUFRAD", "NFUM_COMPOUND", "SCHEDULE_E1_LIMIT", "EVIDENCE_GRADE"
    target_id: str
    proposed_diff: Dict[str, Any]
    status: str             # "PROPOSED", "UNDER_PEER_REVIEW", "QUORUM_ATTESTED", "PUBLISHED", "REJECTED"
    created_by: str
    created_at_utc: str
    attestations: List[BoardAttestation] = field(default_factory=list)


@dataclass
class ClinicalChangeOrder:
    change_order_id: str
    proposal_id: str
    title: str
    target_type: str
    target_id: str
    applied_diff: Dict[str, Any]
    published_at_utc: str
    immutable_sha256_seal: str
    attestations: List[BoardAttestation]


PROPOSALS_STORE: Dict[str, ChangeProposal] = {}
CHANGE_ORDERS_STORE: Dict[str, ClinicalChangeOrder] = {}


class ClinicalGovernanceBoardEngine:
    """Multi-expert governance workflow manager with cryptographic sealing and SQL persistence."""

    @classmethod
    def create_proposal(
        cls,
        title: str,
        target_type: str,
        target_id: str,
        proposed_diff: Dict[str, Any],
        created_by: str,
    ) -> ChangeProposal:
        now_utc = datetime.now(timezone.utc).isoformat()
        prop_id = f"PROP-{uuid.uuid4().hex[:8].upper()}"

        proposal = ChangeProposal(
            proposal_id=prop_id,
            title=title,
            target_type=target_type,
            target_id=target_id,
            proposed_diff=proposed_diff,
            status="PROPOSED",
            created_by=created_by,
            created_at_utc=now_utc,
            attestations=[],
        )
        PROPOSALS_STORE[prop_id] = proposal

        conn = _get_governance_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("""
                    INSERT OR REPLACE INTO governance_proposals 
                    (proposal_id, title, target_type, target_id, proposed_diff_json, status, created_by, created_at_utc, attestations_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        proposal.proposal_id,
                        proposal.title,
                        proposal.target_type,
                        proposal.target_id,
                        json.dumps(proposal.proposed_diff),
                        proposal.status,
                        proposal.created_by,
                        proposal.created_at_utc,
                        json.dumps([asdict(a) for a in proposal.attestations])
                    ))
            except Exception:
                pass

        return proposal

    @classmethod
    def attest_proposal(
        cls,
        proposal_id: str,
        attestor_id: str,
        attestor_name: str,
        attestor_role: str,
        intent: str = "Clinical Verification & Pharmacopoeial Quorum Attestation",
    ) -> ChangeProposal:
        proposal = PROPOSALS_STORE.get(proposal_id)
        if not proposal:
            # Check DB
            conn = _get_governance_db()
            if conn:
                try:
                    with conn:
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM governance_proposals WHERE proposal_id = ?", (proposal_id,))
                        row = cur.fetchone()
                        if row:
                            att_list = [BoardAttestation(**a) for a in json.loads(row["attestations_json"] or "[]")]
                            proposal = ChangeProposal(
                                proposal_id=row["proposal_id"],
                                title=row["title"],
                                target_type=row["target_type"],
                                target_id=row["target_id"],
                                proposed_diff=json.loads(row["proposed_diff_json"] or "{}"),
                                status=row["status"],
                                created_by=row["created_by"],
                                created_at_utc=row["created_at_utc"],
                                attestations=att_list
                            )
                            PROPOSALS_STORE[proposal_id] = proposal
                except Exception:
                    pass

        if not proposal:
            raise KeyError(f"Proposal '{proposal_id}' not found.")

        role_upper = attestor_role.upper()
        if role_upper not in SENIOR_BOARD_ROLES:
            raise UnauthorizedGovernanceRoleError(
                f"Role '{attestor_role}' is not authorized. Must be one of {SENIOR_BOARD_ROLES}."
            )

        # Ensure no duplicate attestation from same clinician
        if any(a.attestor_id == attestor_id for a in proposal.attestations):
            raise ValueError(f"Clinician '{attestor_id}' has already attested to this proposal.")

        now_utc = datetime.now(timezone.utc).isoformat()
        seal_payload = f"{proposal_id}:{attestor_id}:{role_upper}:{now_utc}:{intent}"
        seal = hmac.new(
            GOVERNANCE_SIGNING_KEY.encode("utf-8"),
            seal_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        attestation = BoardAttestation(
            attestor_id=attestor_id,
            attestor_name=attestor_name,
            attestor_role=role_upper,
            timestamp_utc=now_utc,
            attestation_intent=intent,
            digital_seal=seal,
        )
        proposal.attestations.append(attestation)

        # Check quorum (minimum 2 distinct senior clinicians)
        if len(proposal.attestations) >= 2:
            proposal.status = "QUORUM_ATTESTED"
        else:
            proposal.status = "UNDER_PEER_REVIEW"

        conn = _get_governance_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("""
                    UPDATE governance_proposals 
                    SET status = ?, attestations_json = ?
                    WHERE proposal_id = ?
                    """, (
                        proposal.status,
                        json.dumps([asdict(a) for a in proposal.attestations]),
                        proposal.proposal_id
                    ))
            except Exception:
                pass

        return proposal

    @classmethod
    def publish_change_order(cls, proposal_id: str) -> ClinicalChangeOrder:
        """Publishes and locks the ratified change order. Requires minimum 2 attestations."""
        proposal = PROPOSALS_STORE.get(proposal_id)
        if not proposal:
            conn = _get_governance_db()
            if conn:
                try:
                    with conn:
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM governance_proposals WHERE proposal_id = ?", (proposal_id,))
                        row = cur.fetchone()
                        if row:
                            att_list = [BoardAttestation(**a) for a in json.loads(row["attestations_json"] or "[]")]
                            proposal = ChangeProposal(
                                proposal_id=row["proposal_id"],
                                title=row["title"],
                                target_type=row["target_type"],
                                target_id=row["target_id"],
                                proposed_diff=json.loads(row["proposed_diff_json"] or "{}"),
                                status=row["status"],
                                created_by=row["created_by"],
                                created_at_utc=row["created_at_utc"],
                                attestations=att_list
                            )
                            PROPOSALS_STORE[proposal_id] = proposal
                except Exception:
                    pass

        if not proposal:
            raise KeyError(f"Proposal '{proposal_id}' not found.")

        if len(proposal.attestations) < 2:
            raise QuorumNotReachedError(
                f"Governance Quorum Violation: Proposal '{proposal_id}' has {len(proposal.attestations)} attestation(s). "
                f"Minimum 2 Senior Clinicians / Specialists required to ratify."
            )

        now_utc = datetime.now(timezone.utc).isoformat()
        order_id = f"CCO-{uuid.uuid4().hex[:8].upper()}"

        diff_str = json.dumps(proposal.proposed_diff, sort_keys=True)
        seal_content = f"{order_id}:{proposal_id}:{proposal.target_id}:{diff_str}:{now_utc}"
        immutable_seal = hashlib.sha256(seal_content.encode("utf-8")).hexdigest()

        change_order = ClinicalChangeOrder(
            change_order_id=order_id,
            proposal_id=proposal_id,
            title=proposal.title,
            target_type=proposal.target_type,
            target_id=proposal.target_id,
            applied_diff=proposal.proposed_diff,
            published_at_utc=now_utc,
            immutable_sha256_seal=immutable_seal,
            attestations=list(proposal.attestations),
        )

        proposal.status = "PUBLISHED"
        CHANGE_ORDERS_STORE[order_id] = change_order

        conn = _get_governance_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("""
                    INSERT OR REPLACE INTO governance_change_orders
                    (change_order_id, proposal_id, title, target_type, target_id, applied_diff_json, published_at_utc, immutable_sha256_seal, attestations_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        change_order.change_order_id,
                        change_order.proposal_id,
                        change_order.title,
                        change_order.target_type,
                        change_order.target_id,
                        json.dumps(change_order.applied_diff),
                        change_order.published_at_utc,
                        change_order.immutable_sha256_seal,
                        json.dumps([asdict(a) for a in change_order.attestations])
                    ))
                    cur.execute("UPDATE governance_proposals SET status = 'PUBLISHED' WHERE proposal_id = ?", (proposal_id,))
            except Exception:
                pass

        return change_order

    @classmethod
    def get_change_orders(cls) -> List[ClinicalChangeOrder]:
        conn = _get_governance_db()
        if conn:
            try:
                with conn:
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM governance_change_orders ORDER BY published_at_utc DESC")
                    rows = cur.fetchall()
                    for r in rows:
                        oid = r["change_order_id"]
                        if oid not in CHANGE_ORDERS_STORE:
                            att_list = [BoardAttestation(**a) for a in json.loads(r["attestations_json"] or "[]")]
                            CHANGE_ORDERS_STORE[oid] = ClinicalChangeOrder(
                                change_order_id=r["change_order_id"],
                                proposal_id=r["proposal_id"],
                                title=r["title"],
                                target_type=r["target_type"],
                                target_id=r["target_id"],
                                applied_diff=json.loads(r["applied_diff_json"] or "{}"),
                                published_at_utc=r["published_at_utc"],
                                immutable_sha256_seal=r["immutable_sha256_seal"],
                                attestations=att_list
                            )
            except Exception:
                pass
        return list(CHANGE_ORDERS_STORE.values())
