"""
Abstract graph repository interface.

Master Build Prompt v4.0 §27 and 2035 Horizon 1 specify the Four-Graph
physical separation model across:
1. zayvora_knowledge: Ontologies of Mufradat, Mizaj, Akhlat, Quwa, Af'al,
   OrganAxes, Diseases, Schedule E(1) poisons, and Mudabbar protocols.
2. zayvora_formula: Static / Curated Murakkabat compositions (NFUM, Qarabadeen).
3. zayvora_evidence: Clinical trial, in-vitro, in-vivo, and adverse event reports.
4. zayvora_patient: Tenant-isolated patient clinical graph.

This module defines that contract as a Python Protocol so routers and services
depend on the interface, decoupled from physical Neo4j storage.
"""
from __future__ import annotations

from typing import Any, Protocol


class GraphRepository(Protocol):
    # -- Base Mufrad Operations --
    def create_mufrad(self, *, organization_id: str, data: dict) -> dict: ...

    def get_mufrad(self, *, organization_id: str, mufrad_id: str) -> dict | None: ...

    def list_mufradat(
        self, *, organization_id: str, organ_axis: str | None = None, mizaj_temperament: str | None = None
    ) -> list[dict]: ...

    def set_mufrad_mizaj(self, *, organization_id: str, mufrad_id: str, temperament: str, hc_degree: int, wd_degree: int) -> dict: ...

    def link_mufrad_to_axis(self, *, organization_id: str, mufrad_id: str, axis_code: str) -> dict: ...

    # -- Evidence Operations --
    def add_evidence(self, *, organization_id: str, mufrad_id: str, evidence: dict) -> dict: ...

    def list_evidence_for_mufrad(self, *, organization_id: str, mufrad_id: str) -> list[dict]: ...

    # -- Phase 5: Multi-Hop Graph Traversal & Ontologies --
    def get_mufrad_network(self, *, name_or_id: str, organization_id: str = "") -> dict[str, Any] | None: ...

    def find_correctives(self, *, mufrad_name: str) -> list[dict[str, Any]]: ...

    def find_substitutes(self, *, mufrad_name: str, target_axis: str | None = None) -> list[dict[str, Any]]: ...

    def get_compound_network(self, *, compound_name_or_id: str) -> dict[str, Any] | None: ...

    def extract_rag_subgraph(
        self,
        *,
        organ_axis: str | None = None,
        symptoms: list[str] | None = None,
        temperament: str | None = None,
        max_hops: int = 2,
    ) -> dict[str, Any]: ...

    def seed_pharmacopoeia_graph(self) -> dict[str, int]: ...
