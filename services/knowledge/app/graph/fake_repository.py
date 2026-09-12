"""
In-memory implementation of GraphRepository for testing and standalone operation.
Provides multi-hop relationship indexing, multi-graph isolation, and graph RAG traversal.
"""
from __future__ import annotations

import uuid
from typing import Any

from app.core.pharmacopoeia import (
    NFUM_COMPOUND_REGISTRY,
    SCHEDULE_E1_POISONS,
    UPI_MUFRADAT_REGISTRY,
    match_schedule_e1_substance,
)
from app.core.taxonomy import ORGAN_AXES
from app.graph.ingestion import build_canonical_graph_nodes_and_edges
from app.graph.rag import format_subgraph_as_rag_context


class InMemoryGraphRepository:
    def __init__(self, seed_axes: list[dict] | None = None):
        self._mufradat: dict[str, dict] = {}
        self._mizaj_by_mufrad: dict[str, dict] = {}
        self._axes_by_mufrad: dict[str, list[str]] = {}
        self._evidence_by_mufrad: dict[str, list[dict]] = {}
        self._compounds: dict[str, dict] = {}
        self._compound_ingredients: dict[str, list[dict]] = {}
        self._axis_codes = {a["code"] for a in (seed_axes or ORGAN_AXES)}

        # Seed baseline graph
        self.seed_pharmacopoeia_graph()

    def seed_pharmacopoeia_graph(self) -> dict[str, int]:
        data = build_canonical_graph_nodes_and_edges()
        mufrad_count = 0
        compound_count = 0

        # Ingest Mufradat
        for m in data["nodes"]["Mufrad"]:
            self._mufradat[m["id"]] = dict(m)
            self._mufradat[m["name"].lower()] = self._mufradat[m["id"]]
            mufrad_count += 1

        # Ingest Compounds
        for c in data["nodes"]["Murakkab"]:
            self._compounds[c["id"]] = dict(c)
            self._compounds[c["name"].lower()] = self._compounds[c["id"]]
            compound_count += 1

        # Ingest Edges
        for edge in data["edges"]:
            etype = edge["type"]
            if etype == "HAS_MIZAJ":
                self._mizaj_by_mufrad[edge["from_id"]] = {
                    "temperament": edge["to_id"],
                    **edge["props"],
                }
            elif etype == "ACTS_ON":
                self._axes_by_mufrad.setdefault(edge["from_id"], []).append(edge["to_id"])
            elif etype == "CONTAINS_INGREDIENT":
                self._compound_ingredients.setdefault(edge["from_id"], []).append({
                    "mufrad_id": edge["to_id"],
                    **edge["props"],
                })

        return {"mufradat_nodes": mufrad_count, "compound_nodes": compound_count, "edges": len(data["edges"])}

    # -- Base Operations --

    def create_mufrad(self, *, organization_id: str, data: dict) -> dict:
        mufrad_id = str(uuid.uuid4())
        record = {
            "id": mufrad_id,
            "organizationId": organization_id,
            "name": data["name"],
            "botanicalName": data.get("botanical_name", ""),
            "partUsed": data.get("part_used", ""),
            "synonyms": data.get("synonyms", []),
            "afal": data.get("afal", []),
            "traditionalUses": data.get("traditional_uses", ""),
            "contraindications": data.get("contraindications", ""),
            "musleh": data.get("musleh", ""),
            "badal": data.get("badal", ""),
            "dose": data.get("dose", ""),
            "isScheduleE1": data.get("is_schedule_e1", False),
            "modernPharmacology": data.get("modern_pharmacology", ""),
        }
        self._mufradat[mufrad_id] = record
        self._mufradat[data["name"].lower()] = record
        self._axes_by_mufrad[mufrad_id] = []
        self._evidence_by_mufrad[mufrad_id] = []
        return dict(record)

    def get_mufrad(self, *, organization_id: str, mufrad_id: str) -> dict | None:
        record = self._mufradat.get(mufrad_id) or self._mufradat.get(mufrad_id.lower())
        if not record:
            return None
        # Organization check if set, otherwise global
        if record.get("organizationId") and organization_id and record["organizationId"] != organization_id:
            return None

        result = dict(record)
        mizaj = self._mizaj_by_mufrad.get(result["id"])
        result["mizaj"] = [mizaj] if mizaj else []
        result["organAxes"] = [{"code": code} for code in self._axes_by_mufrad.get(result["id"], [])]
        return result

    def list_mufradat(
        self, *, organization_id: str, organ_axis: str | None = None, mizaj_temperament: str | None = None
    ) -> list[dict]:
        seen_ids = set()
        results = []
        for key, record in self._mufradat.items():
            rid = record["id"]
            if rid in seen_ids:
                continue
            seen_ids.add(rid)

            if record.get("organizationId") and organization_id and record["organizationId"] != organization_id:
                continue
            if organ_axis and organ_axis not in self._axes_by_mufrad.get(rid, []):
                continue
            if mizaj_temperament:
                mz = self._mizaj_by_mufrad.get(rid)
                if not mz or mz.get("temperament") != mizaj_temperament:
                    continue
            results.append(dict(record))
        return sorted(results, key=lambda r: r["name"])

    def set_mufrad_mizaj(self, *, organization_id: str, mufrad_id: str, temperament: str, hc_degree: int, wd_degree: int) -> dict:
        record = self.get_mufrad(organization_id=organization_id, mufrad_id=mufrad_id)
        if not record:
            raise ValueError(f"Mufrad {mufrad_id} not found")
        real_id = record["id"]
        mizaj = {"id": str(uuid.uuid4()), "temperament": temperament, "hcDegree": hc_degree, "wdDegree": wd_degree}
        self._mizaj_by_mufrad[real_id] = mizaj
        return dict(mizaj)

    def link_mufrad_to_axis(self, *, organization_id: str, mufrad_id: str, axis_code: str) -> dict:
        record = self.get_mufrad(organization_id=organization_id, mufrad_id=mufrad_id)
        if not record:
            raise ValueError(f"Mufrad {mufrad_id} not found")
        if axis_code not in self._axis_codes:
            raise ValueError(f"OrganAxis {axis_code} not found")
        axes = self._axes_by_mufrad.setdefault(record["id"], [])
        if axis_code not in axes:
            axes.append(axis_code)
        return {"code": axis_code}

    def add_evidence(self, *, organization_id: str, mufrad_id: str, evidence: dict) -> dict:
        record = self.get_mufrad(organization_id=organization_id, mufrad_id=mufrad_id)
        if not record:
            raise ValueError(f"Mufrad {mufrad_id} not found")
        entry = {
            "id": str(uuid.uuid4()),
            "organizationId": organization_id,
            "level": evidence["level"],
            "knowledgeWorld": evidence["knowledge_world"],
            "source": evidence.get("source", ""),
            "studyType": evidence.get("study_type", ""),
            "summary": evidence.get("summary", ""),
            "reviewer": evidence.get("reviewer", ""),
            "reviewStatus": evidence.get("review_status", "pending"),
        }
        self._evidence_by_mufrad.setdefault(record["id"], []).append(entry)
        return dict(entry)

    def list_evidence_for_mufrad(self, *, organization_id: str, mufrad_id: str) -> list[dict]:
        record = self.get_mufrad(organization_id=organization_id, mufrad_id=mufrad_id)
        if not record:
            return []
        entries = self._evidence_by_mufrad.get(record["id"], [])
        return sorted([dict(e) for e in entries], key=lambda e: e["level"])

    # -- Phase 5: Multi-Hop Traversals & Graph RAG --

    def get_mufrad_network(self, *, name_or_id: str, organization_id: str = "") -> dict[str, Any] | None:
        target = self.get_mufrad(organization_id=organization_id, mufrad_id=name_or_id)
        if not target:
            return None

        m_id = target["id"]
        mizaj = self._mizaj_by_mufrad.get(m_id)
        axes = [ax for ax in ORGAN_AXES if ax["code"] in self._axes_by_mufrad.get(m_id, [])]
        e1_substance = match_schedule_e1_substance(target["name"])

        # Find compounds containing this mufrad
        contained_in = []
        for cid, ings in self._compound_ingredients.items():
            if any(ing["mufrad_id"] == m_id for ing in ings):
                comp = self._compounds.get(cid)
                if comp:
                    contained_in.append({
                        "id": comp["id"],
                        "name": comp["name"],
                        "category": comp["category"],
                    })

        return {
            "mufrad": target,
            "mizaj": mizaj,
            "axes": axes,
            "schedule_e1_profile": e1_substance,
            "correctives": self.find_correctives(mufrad_name=target["name"]),
            "substitutes": self.find_substitutes(mufrad_name=target["name"]),
            "contained_in_compounds": contained_in,
            "evidence": self._evidence_by_mufrad.get(m_id, []),
        }

    def find_correctives(self, *, mufrad_name: str) -> list[dict[str, Any]]:
        record = self._mufradat.get(mufrad_name.lower())
        if not record:
            # Fallback to search
            found = next((m for m in UPI_MUFRADAT_REGISTRY if mufrad_name.lower() in m["name"].lower()), None)
            if found:
                record = found
        if not record or not record.get("musleh"):
            return []

        musleh_str = record["musleh"]
        correctives = []
        for part in musleh_str.split(","):
            cleaned = part.strip()
            if cleaned:
                correctives.append({
                    "target_drug": record["name"],
                    "musleh_name": cleaned,
                    "classical_role": "Corrective / Toxicity Mitigator",
                })
        return correctives

    def find_substitutes(self, *, mufrad_name: str, target_axis: str | None = None) -> list[dict[str, Any]]:
        record = self._mufradat.get(mufrad_name.lower())
        if not record:
            found = next((m for m in UPI_MUFRADAT_REGISTRY if mufrad_name.lower() in m["name"].lower()), None)
            if found:
                record = found
        if not record or not record.get("badal"):
            return []

        badal_str = record["badal"]
        substitutes = []
        for part in badal_str.split(","):
            cleaned = part.strip()
            if cleaned:
                substitutes.append({
                    "original_drug": record["name"],
                    "substitute_name": cleaned,
                    "classical_role": "Badal / Therapeutic Substitute",
                    "axis_affinity": target_axis or "broad",
                })
        return substitutes

    def get_compound_network(self, *, compound_name_or_id: str) -> dict[str, Any] | None:
        target = self._compounds.get(compound_name_or_id) or self._compounds.get(compound_name_or_id.lower())
        if not target:
            target = next((c for c in NFUM_COMPOUND_REGISTRY if compound_name_or_id.lower() in c["name"].lower()), None)
        if not target:
            return None

        c_id = target["id"]
        ingredients = []
        for ing in self._compound_ingredients.get(c_id, []):
            m_id = ing["mufrad_id"]
            m_node = self._mufradat.get(m_id)
            ingredients.append({
                "mufrad": m_node,
                "props": ing,
            })

        return {
            "compound": target,
            "ingredients": ingredients,
        }

    def extract_rag_subgraph(
        self,
        *,
        organ_axis: str | None = None,
        symptoms: list[str] | None = None,
        temperament: str | None = None,
        max_hops: int = 2,
    ) -> dict[str, Any]:
        matched_axes = []
        if organ_axis:
            matched_axes = [ax for ax in ORGAN_AXES if ax["code"] == organ_axis]

        # Find mufradat for this axis or symptoms
        matched_mufradat = []
        seen = set()
        for mid, axes in self._axes_by_mufrad.items():
            if organ_axis and organ_axis in axes:
                node = self._mufradat.get(mid)
                if node and node["id"] not in seen:
                    seen.add(node["id"])
                    mz = self._mizaj_by_mufrad.get(node["id"], {})
                    matched_mufradat.append({**node, "mizaj": mz})

        # Match compound formulations
        matched_compounds = []
        for cid, comp in self._compounds.items():
            # Check indication
            ind = comp.get("classicalIndication", "").lower()
            if organ_axis and organ_axis in ind:
                matched_compounds.append(comp)
            elif symptoms:
                if any(s.lower() in ind for s in symptoms):
                    matched_compounds.append(comp)

        # Matched poisons in these mufradat
        matched_poisons = []
        for m in matched_mufradat:
            if m.get("isScheduleE1"):
                p_info = match_schedule_e1_substance(m["name"])
                if p_info:
                    matched_poisons.append(p_info)

        subgraph = {
            "axes": matched_axes,
            "mufradat": matched_mufradat[:8],
            "compounds": matched_compounds[:5],
            "poisons": matched_poisons,
        }
        rag_text = format_subgraph_as_rag_context(subgraph)
        return {
            "subgraph": subgraph,
            "rag_context_text": rag_text,
        }
