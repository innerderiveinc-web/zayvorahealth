"""
ZFIE Domain Exceptions
Enforces safety gates, evidence discipline, and clinical boundaries.
"""


class ZFIEError(Exception):
    """Base exception for all ZFIE domain operations."""
    pass


class ZFIESafetyBlockError(ZFIEError):
    """Raised when Safety Firewall returns BLOCK, terminating downstream execution."""
    def __init__(self, message: str, reasons: list = None):
        super().__init__(message)
        self.reasons = reasons or []


class InvalidEvidencePromotionError(ZFIEError):
    """Raised when computational predictions (E2) attempt silent promotion to clinical evidence (E5/E6)."""
    pass


class UnauthorizedClinicalMutationError(ZFIEError):
    """Raised when an AI or research component attempts to sign, approve, or alter clinical encounters."""
    pass


class KnowledgeSnapshotMismatchError(ZFIEError):
    """Raised when an analysis cannot be reproduced due to a missing or altered knowledge snapshot."""
    pass


class EntityNotFoundError(ZFIEError):
    """Raised when a canonical entity cannot be resolved."""
    pass
