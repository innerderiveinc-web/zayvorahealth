"""
Tests for Clinical Governance Board, Quorum Enforcement, and Cryptographic Change Orders
"""

try:
    import pytest
except ImportError:
    pytest = None

from app.board.governance_board import (
    ClinicalGovernanceBoardEngine,
    ChangeProposal,
    ClinicalChangeOrder,
    QuorumNotReachedError,
    UnauthorizedGovernanceRoleError,
)


def test_governance_proposal_lifecycle_and_single_attestation():
    proposal = ClinicalGovernanceBoardEngine.create_proposal(
        title="Revise maximum posology ceiling for Suranjan Talkh Mudabbar",
        target_type="SCHEDULE_E1_LIMIT",
        target_id="upi-suranjan-talkh",
        proposed_diff={"field": "max_single_dose_mg", "old_val": 250, "new_val": 300, "rationale": "Evidence level E5 validation"},
        created_by="Hakim Zafarullah Khan",
    )
    assert proposal.proposal_id.startswith("PROP-")
    assert proposal.status == "PROPOSED"
    assert len(proposal.attestations) == 0

    # Attestation 1 by Senior Tabeeb
    ClinicalGovernanceBoardEngine.attest_proposal(
        proposal_id=proposal.proposal_id,
        attestor_id="TAB-101",
        attestor_name="Hakim Maryam Siddiqui",
        attestor_role="SENIOR_TABEEB",
    )
    assert proposal.status == "UNDER_PEER_REVIEW"
    assert len(proposal.attestations) == 1

    # Attempt to publish with only 1 attestation (MUST FAIL)
    try:
        ClinicalGovernanceBoardEngine.publish_change_order(proposal.proposal_id)
        assert False, "Should have raised QuorumNotReachedError"
    except QuorumNotReachedError as qe:
        assert "Quorum Violation" in str(qe)


def test_governance_quorum_ratification_and_publication():
    proposal = ClinicalGovernanceBoardEngine.create_proposal(
        title="Add clinical indication for Majun Chobchini in Rheumatoid Polyarthritis",
        target_type="NFUM_COMPOUND",
        target_id="nfum-majun-chobchini",
        proposed_diff={"action": "ADD_INDICATION", "indication": "Waja-ul-Mafasil Balghami"},
        created_by="Hakim Dr. Ahmed Raza",
    )

    # Attestation 1
    ClinicalGovernanceBoardEngine.attest_proposal(
        proposal_id=proposal.proposal_id,
        attestor_id="TAB-201",
        attestor_name="Hakim Zafarullah Khan",
        attestor_role="SENIOR_TABEEB",
    )

    # Attestation 2 (Reaches Quorum)
    ClinicalGovernanceBoardEngine.attest_proposal(
        proposal_id=proposal.proposal_id,
        attestor_id="TAB-202",
        attestor_name="Dr. Shireen Parveen",
        attestor_role="PHARMACOPOEIA_LEAD",
    )
    assert proposal.status == "QUORUM_ATTESTED"
    assert len(proposal.attestations) == 2

    # Publish change order
    order = ClinicalGovernanceBoardEngine.publish_change_order(proposal.proposal_id)
    assert order.change_order_id.startswith("CCO-")
    assert proposal.status == "PUBLISHED"
    assert len(order.immutable_sha256_seal) == 64
    assert len(order.attestations) == 2


def test_governance_unauthorized_role_rejected():
    proposal = ClinicalGovernanceBoardEngine.create_proposal(
        title="Unauthorized modification attempt",
        target_type="UPI_MUFRAD",
        target_id="upi-kuchla",
        proposed_diff={"illegal": True},
        created_by="Intern",
    )

    try:
        ClinicalGovernanceBoardEngine.attest_proposal(
            proposal_id=proposal.proposal_id,
            attestor_id="USER-INTERN",
            attestor_name="Junior Trainee",
            attestor_role="STUDENT_INTERN",
        )
        assert False, "Should have raised UnauthorizedGovernanceRoleError"
    except UnauthorizedGovernanceRoleError:
        pass
