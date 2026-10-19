"""
ZFIE Core Validators
Validates claim integrity, evidence levels, and entity separation.
"""

from packages.zfie.core.enums import ClaimType, EvidenceLevel
from packages.zfie.core.errors import InvalidEvidencePromotionError


def validate_evidence_promotion(
    source_level: EvidenceLevel,
    target_level: EvidenceLevel,
    has_experimental_validation: bool
) -> bool:
    """
    Strictly forbids computational predictions (E0, E1, E2) from silently
    becoming in-vivo or clinical evidence (E4, E5, E6) without experimental proof.
    """
    source_rank = EvidenceLevel.rank(source_level.value)
    target_rank = EvidenceLevel.rank(target_level.value)

    if target_rank > source_rank:
        if target_rank >= 4 and not has_experimental_validation:
            raise InvalidEvidencePromotionError(
                f"Cannot promote evidence from {source_level.value} to {target_level.value} "
                f"without independent experimental / clinical validation."
            )
    return True


def classify_scientific_claim(statement: str) -> ClaimType:
    """
    Classifies scientific claims to prevent language drift from prediction to established fact.
    """
    lower = statement.lower()
    if any(k in lower for k in ["measured in batch", "hplc verified", "observed in coa", "detected in lot"]):
        return ClaimType.OBSERVED
    if any(k in lower for k in ["reported in upi", "curated from canon", "cited in literature", "recorded in text"]):
        return ClaimType.CURATED
    if any(k in lower for k in ["calculated molecular weight", "stoichiometric ratio", "exact percentage"]):
        return ClaimType.CALCULATED
    if any(k in lower for k in ["docking score", "predicted affinity", "in silico", "binding energy", "qsar"]):
        return ClaimType.PREDICTED
    if any(k in lower for k in ["pathway cluster may explain", "inferred mechanism", "hypothesized synergy"]):
        return ClaimType.INFERRED
    return ClaimType.UNKNOWN
