"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 5C: Scientific Knowledge Decay & Freshness Engine
System: ZAYVORA Health OS™
Doctrine: Scientific knowledge is dynamic. When new evidence or contradictions emerge, dependent analyses must be flagged as STALE.
"""

import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class KnowledgeFreshnessState(str, Enum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"
    REVISED = "REVISED"
    CONTRADICTED = "CONTRADICTED"
    WITHDRAWN = "WITHDRAWN"


@dataclass
class KnowledgeDependencyEdge:
    analysis_id: str
    subject_id: str
    underlying_evidence_ids: List[str]
    freshness_state: KnowledgeFreshnessState
    invalidation_reason: Optional[str] = None
    last_evaluated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["freshness_state"] = self.freshness_state.value
        return d


class KnowledgeFreshnessEngine:
    """Detects when underlying scientific updates render prior analysis runs or findings stale."""

    _DEPENDENCY_GRAPH: Dict[str, KnowledgeDependencyEdge] = {}

    @classmethod
    def register_analysis_dependency(
        cls,
        analysis_id: str,
        subject_id: str,
        evidence_ids: List[str]
    ) -> KnowledgeDependencyEdge:
        edge = KnowledgeDependencyEdge(
            analysis_id=analysis_id,
            subject_id=subject_id,
            underlying_evidence_ids=evidence_ids,
            freshness_state=KnowledgeFreshnessState.CURRENT
        )
        cls._DEPENDENCY_GRAPH[analysis_id] = edge
        return edge

    @classmethod
    def notify_evidence_updated(cls, evidence_id: str, reason: str = "New contradictory trial published") -> List[str]:
        """Invalidates all analysis runs depending on the updated or refuted evidence."""
        affected_analyses = []
        for analysis_id, edge in cls._DEPENDENCY_GRAPH.items():
            if evidence_id in edge.underlying_evidence_ids:
                edge.freshness_state = KnowledgeFreshnessState.STALE
                edge.invalidation_reason = f"Evidence {evidence_id} updated: {reason}"
                edge.last_evaluated_at = time.time()
                affected_analyses.append(analysis_id)
        return affected_analyses

    @classmethod
    def check_freshness(cls, analysis_id: str) -> Dict[str, Any]:
        edge = cls._DEPENDENCY_GRAPH.get(analysis_id)
        if not edge:
            return {"analysis_id": analysis_id, "freshness_state": KnowledgeFreshnessState.CURRENT.value}
        return edge.to_dict()
