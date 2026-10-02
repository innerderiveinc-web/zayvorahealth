"""
Real Neo4j implementation of GraphRepository supporting the Four-Graph
Physical Separation Architecture per ZAYVORA Clinical Architecture Specification v4.0 §27 and 2035 Horizon 1.

Databases:
- zayvora_knowledge: Ontologies of Mufradat, Mizaj, OrganAxes, Poisons, Detox Protocols.
- zayvora_formula: Curated Compound Formulations (NFUM, Qarabadeen).
- zayvora_evidence: Clinical trials, in-vitro/in-vivo, phytochemical and adverse event studies.
- zayvora_patient: Tenant-isolated clinical patient graph.
"""
from __future__ import annotations

import uuid
from typing import Any

from neo4j import Driver, GraphDatabase

from app.core.pharmacopoeia import match_schedule_e1_substance
from app.core.taxonomy import ORGAN_AXES
from app.graph.ingestion import build_canonical_graph_nodes_and_edges
from app.graph.rag import format_subgraph_as_rag_context


class Neo4jGraphRepository:
    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
        knowledge_db: str = "zayvora_knowledge",
        formula_db: str = "zayvora_formula",
        evidence_db: str = "zayvora_evidence",
        patient_db: str = "zayvora_patient",
    ):
        self._driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        self.knowledge_db = knowledge_db
        self.formula_db = formula_db
        self.evidence_db = evidence_db
        self.patient_db = patient_db

    def close(self) -> None:
        self._driver.close()

    def verify_connectivity(self) -> None:
        self._driver.verify_connectivity()

    def _get_session(self, database: str | None = None):
        # Fallback gracefully if multi-database is not configured on community edition
        try:
            return self._driver.session(database=database) if database else self._driver.session()
        except Exception:
            return self._driver.session()

    def ensure_schema_indexes_and_constraints(self) -> dict[str, list[str]]:
        """Creates Neo4j 5 unique constraints and composite query performance indexes."""
        statements = {
            self.knowledge_db: [
                "CREATE CONSTRAINT cstr_mufrad_id IF NOT EXISTS FOR (m:Mufrad) REQUIRE m.id IS UNIQUE",
                "CREATE INDEX idx_mufrad_name IF NOT EXISTS FOR (m:Mufrad) ON (m.name)",
                "CREATE INDEX idx_mufrad_botanical IF NOT EXISTS FOR (m:Mufrad) ON (m.botanicalName)",
                "CREATE CONSTRAINT cstr_mizaj_temp IF NOT EXISTS FOR (mz:Mizaj) REQUIRE mz.temperament IS UNIQUE",
                "CREATE CONSTRAINT cstr_axis_code IF NOT EXISTS FOR (ax:OrganAxis) REQUIRE ax.code IS UNIQUE",
                "CREATE INDEX idx_organ_axis_code_name IF NOT EXISTS FOR (ax:OrganAxis) ON (ax.code, ax.name)",
            ],
            self.formula_db: [
                "CREATE CONSTRAINT cstr_murakkab_id IF NOT EXISTS FOR (c:Murakkab) REQUIRE c.id IS UNIQUE",
                "CREATE INDEX idx_murakkab_name IF NOT EXISTS FOR (c:Murakkab) ON (c.name)",
                "CREATE INDEX idx_murakkab_category IF NOT EXISTS FOR (c:Murakkab) ON (c.category)",
            ],
            self.patient_db: [
                "CREATE CONSTRAINT cstr_patient_node_id IF NOT EXISTS FOR (p:Patient) REQUIRE p.id IS UNIQUE",
                "CREATE INDEX idx_patient_org_id IF NOT EXISTS FOR (p:Patient) ON (p.organization_id)",
            ],
        }
        applied = {}
        for db, stmts in statements.items():
            applied[db] = []
            with self._get_session(db) as session:
                for stmt in stmts:
                    try:
                        session.run(stmt)
                        applied[db].append(stmt)
                    except Exception:
                        pass
        return applied

    def seed_organ_axes(self, axes: list[dict]) -> None:
        query = """
        MERGE (ax:OrganAxis {code: $code})
        SET ax.name = $name,
            ax.translation = $translation,
            ax.systemsCovered = $systemsCovered
        """
        with self._get_session(self.knowledge_db) as session:
            for axis in axes:
                session.run(
                    query,
                    code=axis["code"],
                    name=axis["name"],
                    translation=axis["translation"],
                    systemsCovered=axis.get("systems_covered", ""),
                )

    def seed_pharmacopoeia_graph(self) -> dict[str, int]:
        data = build_canonical_graph_nodes_and_edges()

        # Ingest Organ Axes into Knowledge DB
        self.seed_organ_axes(ORGAN_AXES)

        # Ingest Mizaj Nodes
        with self._get_session(self.knowledge_db) as session:
            for mz in data["nodes"]["Mizaj"]:
                session.run(
                    """
                    MERGE (m:Mizaj {temperament: $temperament})
                    SET m.quality = $quality, m.humor = $humor, m.element = $element
                    """,
                    **mz,
                )

            # Ingest Mufradat Nodes & Relationships
            for m in data["nodes"]["Mufrad"]:
                session.run(
                    """
                    MERGE (m:Mufrad {id: $id})
                    SET m.name = $name,
                        m.botanicalName = $botanicalName,
                        m.partUsed = $partUsed,
                        m.synonyms = $synonyms,
                        m.afal = $afal,
                        m.traditionalUses = $traditionalUses,
                        m.contraindications = $contraindications,
                        m.musleh = $musleh,
                        m.badal = $badal,
                        m.dose = $dose,
                        m.isScheduleE1 = $isScheduleE1,
                        m.modernPharmacology = $modernPharmacology
                    """,
                    **m,
                )

            # Ingest Poison & Mudabbar Nodes
            for p in data["nodes"]["PoisonClass"]:
                session.run(
                    """
                    MERGE (pc:PoisonClass {name: $name})
                    SET pc.toxicAlkaloids = $toxicAlkaloids, pc.antidote = $antidote
                    """,
                    **p,
                )
            for mp in data["nodes"]["MudabbarProtocol"]:
                session.run(
                    """
                    MERGE (pr:MudabbarProtocol {name: $name})
                    SET pr.targetDrug = $targetDrug, pr.protocol = $protocol
                    """,
                    **mp,
                )

            # Ingest Edges
            for e in data["edges"]:
                if e["type"] == "HAS_MIZAJ":
                    session.run(
                        """
                        MATCH (m:Mufrad {id: $from_id})
                        MATCH (mz:Mizaj {temperament: $to_id})
                        MERGE (m)-[r:HAS_MIZAJ]->(mz)
                        SET r.hc_degree = $hc_degree, r.wd_degree = $wd_degree, r.quality = $quality
                        """,
                        from_id=e["from_id"],
                        to_id=e["to_id"],
                        hc_degree=e["props"].get("hc_degree", 0),
                        wd_degree=e["props"].get("wd_degree", 0),
                        quality=e["props"].get("quality", ""),
                    )
                elif e["type"] == "ACTS_ON":
                    session.run(
                        """
                        MATCH (m:Mufrad {id: $from_id})
                        MATCH (ax:OrganAxis {code: $to_id})
                        MERGE (m)-[:ACTS_ON]->(ax)
                        """,
                        from_id=e["from_id"],
                        to_id=e["to_id"],
                    )

        # Ingest Murakkabat into Formula DB
        with self._get_session(self.formula_db) as session:
            for c in data["nodes"]["Murakkab"]:
                session.run(
                    """
                    MERGE (c:Murakkab {id: $id})
                    SET c.name = $name,
                        c.urduName = $urduName,
                        c.category = $category,
                        c.classicalIndication = $classicalIndication,
                        c.dose = $dose,
                        c.scheduleE1Warning = $scheduleE1Warning,
                        c.precautions = $precautions
                    """,
                    **c,
                )

        return {
            "mufradat_nodes": len(data["nodes"]["Mufrad"]),
            "compound_nodes": len(data["nodes"]["Murakkab"]),
            "edges": len(data["edges"]),
        }

    # -- Mufrad Operations --

    def create_mufrad(self, *, organization_id: str, data: dict) -> dict:
        mufrad_id = str(uuid.uuid4())
        query = """
        CREATE (m:Mufrad {
            id: $id,
            organizationId: $organizationId,
            name: $name,
            botanicalName: $botanicalName,
            partUsed: $partUsed,
            synonyms: $synonyms,
            afal: $afal,
            traditionalUses: $traditionalUses,
            contraindications: $contraindications,
            musleh: $musleh,
            badal: $badal,
            dose: $dose,
            modernPharmacology: $modernPharmacology,
            createdAt: datetime()
        })
        RETURN m
        """
        with self._get_session(self.knowledge_db) as session:
            record = session.run(
                query,
                id=mufrad_id,
                organizationId=organization_id,
                name=data["name"],
                botanicalName=data.get("botanical_name", ""),
                partUsed=data.get("part_used", ""),
                synonyms=data.get("synonyms", []),
                afal=data.get("afal", []),
                traditionalUses=data.get("traditional_uses", ""),
                contraindications=data.get("contraindications", ""),
                musleh=data.get("musleh", ""),
                badal=data.get("badal", ""),
                dose=data.get("dose", ""),
                modernPharmacology=data.get("modern_pharmacology", ""),
            ).single()
            return _node_to_dict(record["m"])

    def get_mufrad(self, *, organization_id: str, mufrad_id: str) -> dict | None:
        query = """
        MATCH (m:Mufrad)
        WHERE (m.id = $id OR toLower(m.name) = toLower($id))
          AND ($organizationId = '' OR m.organizationId IS NULL OR m.organizationId = $organizationId)
        OPTIONAL MATCH (m)-[rm:HAS_MIZAJ]->(mz:Mizaj)
        OPTIONAL MATCH (m)-[:ACTS_ON]->(ax:OrganAxis)
        RETURN m,
               collect(DISTINCT mz {.*, hc_degree: rm.hc_degree, wd_degree: rm.wd_degree}) AS mizaj,
               collect(DISTINCT ax {.*}) AS axes
        """
        with self._get_session(self.knowledge_db) as session:
            record = session.run(query, id=mufrad_id, organizationId=organization_id).single()
            if not record or not record["m"]:
                return None
            result = _node_to_dict(record["m"])
            result["mizaj"] = record["mizaj"]
            result["organAxes"] = record["axes"]
            return result

    def list_mufradat(
        self, *, organization_id: str, organ_axis: str | None = None, mizaj_temperament: str | None = None
    ) -> list[dict]:
        clauses = [
            "MATCH (m:Mufrad)",
            "WHERE ($organizationId = '' OR m.organizationId IS NULL OR m.organizationId = $organizationId)",
        ]
        params: dict = {"organizationId": organization_id}

        if organ_axis:
            clauses.append("MATCH (m)-[:ACTS_ON]->(:OrganAxis {code: $organAxis})")
            params["organAxis"] = organ_axis
        if mizaj_temperament:
            clauses.append("MATCH (m)-[:HAS_MIZAJ]->(:Mizaj {temperament: $temperament})")
            params["temperament"] = mizaj_temperament

        clauses.append("RETURN DISTINCT m ORDER BY m.name")
        query = "\n".join(clauses)

        with self._get_session(self.knowledge_db) as session:
            records = session.run(query, **params)
            return [_node_to_dict(r["m"]) for r in records]

    def set_mufrad_mizaj(self, *, organization_id: str, mufrad_id: str, temperament: str, hc_degree: int, wd_degree: int) -> dict:
        query = """
        MATCH (m:Mufrad)
        WHERE (m.id = $mufradId OR toLower(m.name) = toLower($mufradId))
        MERGE (mz:Mizaj {temperament: $temperament})
        MERGE (m)-[r:HAS_MIZAJ]->(mz)
        SET r.hc_degree = $hcDegree, r.wd_degree = $wdDegree
        RETURN mz {.*, hcDegree: $hcDegree, wdDegree: $wdDegree} AS result
        """
        with self._get_session(self.knowledge_db) as session:
            record = session.run(
                query,
                mufradId=mufrad_id,
                temperament=temperament,
                hcDegree=hc_degree,
                wdDegree=wd_degree,
            ).single()
            if not record:
                raise ValueError(f"Mufrad {mufrad_id} not found")
            return record["result"]

    def link_mufrad_to_axis(self, *, organization_id: str, mufrad_id: str, axis_code: str) -> dict:
        query = """
        MATCH (m:Mufrad) WHERE (m.id = $mufradId OR toLower(m.name) = toLower($mufradId))
        MATCH (ax:OrganAxis {code: $axisCode})
        MERGE (m)-[:ACTS_ON]->(ax)
        RETURN ax {.*}
        """
        with self._get_session(self.knowledge_db) as session:
            record = session.run(query, mufradId=mufrad_id, axisCode=axis_code).single()
            if not record:
                raise ValueError(f"Mufrad {mufrad_id} or OrganAxis {axis_code} not found")
            return record["ax"]

    # -- Evidence Operations --

    def add_evidence(self, *, organization_id: str, mufrad_id: str, evidence: dict) -> dict:
        evidence_id = str(uuid.uuid4())
        query = """
        MATCH (m:Mufrad) WHERE (m.id = $mufradId OR toLower(m.name) = toLower($mufradId))
        CREATE (e:Evidence {
            id: $evidenceId,
            organizationId: $organizationId,
            level: $level,
            knowledgeWorld: $knowledgeWorld,
            source: $source,
            studyType: $studyType,
            summary: $summary,
            reviewer: $reviewer,
            reviewStatus: $reviewStatus,
            createdAt: datetime()
        })
        MERGE (m)-[:HAS_EVIDENCE]->(e)
        RETURN e {.*}
        """
        with self._get_session(self.evidence_db) as session:
            record = session.run(
                query,
                mufradId=mufrad_id,
                organizationId=organization_id,
                evidenceId=evidence_id,
                level=evidence["level"],
                knowledgeWorld=evidence["knowledge_world"],
                source=evidence.get("source", ""),
                studyType=evidence.get("study_type", ""),
                summary=evidence.get("summary", ""),
                reviewer=evidence.get("reviewer", ""),
                reviewStatus=evidence.get("review_status", "pending"),
            ).single()
            if not record:
                raise ValueError(f"Mufrad {mufrad_id} not found")
            return record["e"]

    def list_evidence_for_mufrad(self, *, organization_id: str, mufrad_id: str) -> list[dict]:
        query = """
        MATCH (m:Mufrad)-[:HAS_EVIDENCE]->(e:Evidence)
        WHERE (m.id = $mufradId OR toLower(m.name) = toLower($mufradId))
          AND ($organizationId = '' OR e.organizationId IS NULL OR e.organizationId = $organizationId)
        RETURN e {.*} AS e
        ORDER BY e.level
        """
        with self._get_session(self.evidence_db) as session:
            records = session.run(query, mufradId=mufrad_id, organizationId=organization_id)
            return [r["e"] for r in records]

    # -- Phase 5: Multi-Hop Traversal & Graph RAG --

    def get_mufrad_network(self, *, name_or_id: str, organization_id: str = "") -> dict[str, Any] | None:
        target = self.get_mufrad(organization_id=organization_id, mufrad_id=name_or_id)
        if not target:
            return None

        e1_substance = match_schedule_e1_substance(target["name"])
        correctives = self.find_correctives(mufrad_name=target["name"])
        substitutes = self.find_substitutes(mufrad_name=target["name"])

        return {
            "mufrad": target,
            "mizaj": target.get("mizaj"),
            "axes": target.get("organAxes"),
            "schedule_e1_profile": e1_substance,
            "correctives": correctives,
            "substitutes": substitutes,
            "evidence": self.list_evidence_for_mufrad(organization_id=organization_id, mufrad_id=target["id"]),
        }

    def find_correctives(self, *, mufrad_name: str) -> list[dict[str, Any]]:
        target = self.get_mufrad(organization_id="", mufrad_id=mufrad_name)
        if not target or not target.get("musleh"):
            return []
        musleh_str = target["musleh"]
        return [
            {
                "target_drug": target["name"],
                "musleh_name": p.strip(),
                "classical_role": "Corrective / Toxicity Mitigator",
            }
            for p in musleh_str.split(",")
            if p.strip()
        ]

    def find_substitutes(self, *, mufrad_name: str, target_axis: str | None = None) -> list[dict[str, Any]]:
        target = self.get_mufrad(organization_id="", mufrad_id=mufrad_name)
        if not target or not target.get("badal"):
            return []
        badal_str = target["badal"]
        return [
            {
                "original_drug": target["name"],
                "substitute_name": p.strip(),
                "classical_role": "Badal / Therapeutic Substitute",
                "axis_affinity": target_axis or "broad",
            }
            for p in badal_str.split(",")
            if p.strip()
        ]

    def get_compound_network(self, *, compound_name_or_id: str) -> dict[str, Any] | None:
        query = """
        MATCH (c:Murakkab)
        WHERE c.id = $id OR toLower(c.name) = toLower($id)
        RETURN c {.*} as comp
        """
        with self._get_session(self.formula_db) as session:
            record = session.run(query, id=compound_name_or_id).single()
            if not record:
                return None
            return {"compound": record["comp"], "ingredients": []}

    def extract_rag_subgraph(
        self,
        *,
        organ_axis: str | None = None,
        symptoms: list[str] | None = None,
        temperament: str | None = None,
        max_hops: int = 2,
    ) -> dict[str, Any]:
        mufradat = self.list_mufradat(organization_id="", organ_axis=organ_axis, mizaj_temperament=temperament)
        matched_axes = [ax for ax in ORGAN_AXES if ax["code"] == organ_axis] if organ_axis else []
        matched_poisons = []
        for m in mufradat:
            if m.get("isScheduleE1"):
                p_info = match_schedule_e1_substance(m["name"])
                if p_info:
                    matched_poisons.append(p_info)

        subgraph = {
            "axes": matched_axes,
            "mufradat": mufradat[:8],
            "compounds": [],
            "poisons": matched_poisons,
        }
        rag_text = format_subgraph_as_rag_context(subgraph)
        return {
            "subgraph": subgraph,
            "rag_context_text": rag_text,
        }


def _node_to_dict(node) -> dict:
    return dict(node.items())
