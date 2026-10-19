"""
ZFIE Core Enums
Defines authoritative enumeration types for computational formulation intelligence.
"""

from enum import Enum


class EvidenceLevel(str, Enum):
    E0_AI_HYPOTHESIS = "E0"
    E1_LITERATURE_ASSOCIATION = "E1"
    E2_COMPUTATIONAL_PREDICTION = "E2"
    E3_IN_VITRO = "E3"
    E4_IN_VIVO = "E4"
    E5_HUMAN_OBSERVATIONAL_PK = "E5"
    E6_CONTROLLED_CLINICAL = "E6"

    @classmethod
    def rank(cls, level: str) -> int:
        order = {
            "E0": 0,
            "E1": 1,
            "E2": 2,
            "E3": 3,
            "E4": 4,
            "E5": 5,
            "E6": 6,
        }
        return order.get(level, 0)


class FindingStatus(str, Enum):
    ESTABLISHED = "ESTABLISHED"
    SUPPORTED = "SUPPORTED"
    COMPUTATIONALLY_PREDICTED = "COMPUTATIONALLY_PREDICTED"
    TRADITIONAL_CLAIM = "TRADITIONAL_CLAIM"
    CONFLICTING = "CONFLICTING"
    UNKNOWN = "UNKNOWN"


class SafetyVerdict(str, Enum):
    PASS = "PASS"
    CAUTION = "CAUTION"
    BLOCK = "BLOCK"
    UNKNOWN = "UNKNOWN"


class ClaimType(str, Enum):
    OBSERVED = "OBSERVED"
    CURATED = "CURATED"
    CALCULATED = "CALCULATED"
    PREDICTED = "PREDICTED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"


class ContradictionStatus(str, Enum):
    OPEN = "OPEN"
    EXPLAINED = "EXPLAINED"
    RESOLVED = "RESOLVED"
    PERSISTENT = "PERSISTENT"


class SynergyModel(str, Enum):
    BLISS = "BLISS"
    LOEWE = "LOEWE"
    HSA = "HSA"
    ZIP = "ZIP"


class SynergyCandidateStatus(str, Enum):
    UNVALIDATED = "UNVALIDATED"
    PROPOSED = "PROPOSED"
    IN_VITRO_CONFIRMED = "IN_VITRO_CONFIRMED"
    IN_VIVO_CONFIRMED = "IN_VIVO_CONFIRMED"
    REFUTED = "REFUTED"


class ValidationStatus(str, Enum):
    PROPOSED = "PROPOSED"
    RUNNING = "RUNNING"
    VALIDATED = "VALIDATED"
    REFUTED = "REFUTED"
    INCONCLUSIVE = "INCONCLUSIVE"


class EvidenceStrength(str, Enum):
    ABSENT = "ABSENT"
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    DEFINITIVE = "DEFINITIVE"


class EntityType(str, Enum):
    MUFRAD = "MUFRAD"
    MURAKKAB = "MURAKKAB"
    FORMULATION = "FORMULATION"
    FORMULA_VERSION = "FORMULA_VERSION"
    BATCH = "BATCH"
    COMPOUND = "COMPOUND"
    TARGET = "TARGET"
    PATHWAY = "PATHWAY"
    BIOMARKER = "BIOMARKER"
    EVIDENCE = "EVIDENCE"
    HYPOTHESIS = "HYPOTHESIS"
    EXPERIMENT = "EXPERIMENT"
    OUTCOME = "OUTCOME"


class QualityStatus(str, Enum):
    QUARANTINED = "QUARANTINED"
    TESTING = "TESTING"
    CERTIFIED = "CERTIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
