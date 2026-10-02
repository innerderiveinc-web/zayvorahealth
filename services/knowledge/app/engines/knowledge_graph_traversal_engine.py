#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Clinical Knowledge Graph Traversal Engine
=============================================================
Connects validated clinical entities into an authoritative multi-hop knowledge graph:
  Mufradat -> Mizaj -> Afaal -> Therapeutic Objective -> Disease/Condition -> Organ-Axis -> Murakkab -> Nuskha -> Patient -> Outcome

Provides deterministic graph traversal for Hakeem Sahab AI v2 and clinical decision support.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json

from services.knowledge.app.data.mufradat_gold_batch_monographs import (
    GOLD_BENCHMARK_25_MONOGRAPHS,
    ValidationState,
    AIPermission
)
from services.knowledge.app.engines.knowledge_intelligence_vnext import (
    CanonicalDrugRegistry,
    SafetyFirewallV2,
    AISafetyState,
    GOLD_BENCHMARK_25_IDS
)


@dataclass
class GraphNode:
    id: str
    type: str  # Mufrad, Mizaj, Afaal, TherapeuticObjective, Condition, OrganAxis, Murakkab
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relation: str  # POSSESSES_MIZAJ, EXERTS_AFAAL, TARGETS_OBJECTIVE, INDICATED_FOR, ACTS_ON_AXIS, INGREDIENT_OF, CORRECTED_BY, SUBSTITUTE_FOR
    attributes: Dict[str, Any] = field(default_factory=dict)


class ClinicalKnowledgeGraph:
    """In-memory multi-relational clinical graph with indexation and multi-hop queries."""

    def __init__(self):
        self._nodes: Dict[str, GraphNode] = {}
        self._outgoing: Dict[str, List[GraphEdge]] = {}
        self._incoming: Dict[str, List[GraphEdge]] = {}
        self._type_index: Dict[str, Set[str]] = {}
        self._initialize_graph()

    def add_node(self, node: GraphNode):
        self._nodes[node.id] = node
        if node.type not in self._type_index:
            self._type_index[node.type] = set()
        self._type_index[node.type].add(node.id)
        if node.id not in self._outgoing:
            self._outgoing[node.id] = []
        if node.id not in self._incoming:
            self._incoming[node.id] = []

    def add_edge(self, edge: GraphEdge):
        if edge.source_id not in self._outgoing:
            self._outgoing[edge.source_id] = []
        if edge.target_id not in self._incoming:
            self._incoming[edge.target_id] = []
        self._outgoing[edge.source_id].append(edge)
        self._incoming[edge.target_id].append(edge)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def get_nodes_by_type(self, node_type: str) -> List[GraphNode]:
        node_ids = self._type_index.get(node_type, set())
        return [self._nodes[nid] for nid in node_ids if nid in self._nodes]

    def get_outgoing(self, source_id: str, relation: Optional[str] = None) -> List[GraphEdge]:
        edges = self._outgoing.get(source_id, [])
        if relation:
            return [e for e in edges if e.relation == relation]
        return edges

    def get_incoming(self, target_id: str, relation: Optional[str] = None) -> List[GraphEdge]:
        edges = self._incoming.get(target_id, [])
        if relation:
            return [e for e in edges if e.relation == relation]
        return edges

    def _initialize_graph(self):
        """Seeds the clinical knowledge graph from validated gold benchmark monographs."""
        # 1. Common Organ Axes Nodes
        axes = [
            ("AXIS-01", "Jigar-Banas (Hepato-Metabolic Axis)", "Metabolic clearance, insulin sensitivity, humoral maturation"),
            ("AXIS-02", "Dimagh-Aasab (Neuro-Psychological Axis)", "Cognition, nerve conduction, psychogenic stability"),
            ("AXIS-03", "Qalb-Urooq (Cardio-Vascular Axis)", "Circulatory vigor, vascular tone, vital spirit distribution"),
            ("AXIS-04", "Riya-Sadr (Broncho-Pulmonary Axis)", "Respiratory clearance, oxygenation, mucosal protection"),
            ("AXIS-05", "Meda-Ama (Gastro-Intestinal Axis)", "First digestion (Hazm-e-Madi), gastric fire, absorption"),
            ("AXIS-06", "Kulyatain-Masana (Nephro-Urological Axis)", "Renal filtration, fluid regulation, urinary clearance"),
            ("AXIS-07", "Khusyatain-Dam (Male Reproductive Axis)", "Spermatogenesis, androgenic vitality, seminal tone"),
            ("AXIS-08", "Rahim-Takhmdan (Female Reproductive Axis)", "Ovarian balance, menstrual regularity, uterine health"),
            ("AXIS-09", "Mafasil-Azlaat (Musculo-Skeletal Axis)", "Joint lubrication, cartilage integrity, pain clearance"),
            ("AXIS-10", "Jild-Masamat (Dermato-Immunological Axis)", "Integumentary barrier, cutaneous detox, melanin balance"),
            ("AXIS-11", "Tihal-Dimagh (Spleno-Cerebral Axis)", "Black bile metabolism, melancholic clearance, splenic filter"),
            ("AXIS-12", "Hifz-e-Sehat (Immunomodulatory & Longevity Axis)", "Adaptive resilience, Tabiyat reinforcement, longevity"),
        ]
        for aid, aname, adesc in axes:
            self.add_node(GraphNode(id=aid, type="OrganAxis", name=aname, attributes={"description": adesc}))

        # 2. Classical Conditions & Therapeutic Objectives
        conditions = [
            ("COND-01", "Waja-ul-Mafasil (Joint Inflammation / Osteoarthritis)", "AXIS-09", "Musculo-Skeletal"),
            ("COND-02", "Su-e-Mizaj Barid Meda (Gastric Hypo-function / Indigestion)", "AXIS-05", "Gastro-Intestinal"),
            ("COND-03", "Zof-e-Dimagh (Cognitive Exhaustion / Neuro-Asthenia)", "AXIS-02", "Neuro-Psychological"),
            ("COND-04", "Sual-e-Balghami (Chronic Productive Cough)", "AXIS-04", "Broncho-Pulmonary"),
            ("COND-05", "Zof-e-Kabid & HOMA-IR (Hepato-Metabolic Dyscrasia)", "AXIS-01", "Hepato-Metabolic"),
            ("COND-06", "Zof-e-Bah & Oligospermia (Seminal Asthenia)", "AXIS-07", "Male Reproductive"),
            ("COND-07", "Ihtibas-e-Tams / PCOS (Ovarian-Metabolic Imbalance)", "AXIS-08", "Female Reproductive"),
        ]
        for cid, cname, ca_axis, ccat in conditions:
            self.add_node(GraphNode(id=cid, type="Condition", name=cname, attributes={"axis_id": ca_axis, "category": ccat}))
            self.add_edge(GraphEdge(source_id=cid, target_id=ca_axis, relation="ACTS_ON_AXIS"))

        objectives = [
            ("OBJ-01", "Tanqiya-e-Mawad-e-Balghami (Phlegmatic Waste Clearance)", "Eliminate accumulated cold-moist morbid humors"),
            ("OBJ-02", "Taqwiyaat-e-Aaza-e-Raeesa (Vital Organ Toning)", "Restore baseline metabolic energy and organ tone"),
            ("OBJ-03", "Taskeen-e-Waja & Tahleel-e-Waram (Analgesia & Resolvent)", "Resolve localized inflammation and acute pain"),
            ("OBJ-04", "Ta'deel-e-Mizaj (Constitutional Temperament Harmonization)", "Counteract humoral deviation towards equilibrium"),
            ("OBJ-05", "Tadbeer & Muhafizat-e-Kabid (Hepato-Protection)", "Clear hepatic congestion and enhance detoxification"),
            ("OBJ-06", "Munfith-e-Balgham (Bronchial Mucus Expectoration)", "Liquefy and expel viscous phlegmatic secretions"),
        ]
        for oid, oname, odesc in objectives:
            self.add_node(GraphNode(id=oid, type="TherapeuticObjective", name=oname, attributes={"description": odesc}))

        # Link Conditions to Therapeutic Objectives
        cond_obj_map = [
            ("COND-01", "OBJ-01"), ("COND-01", "OBJ-03"),
            ("COND-02", "OBJ-04"), ("COND-02", "OBJ-01"),
            ("COND-03", "OBJ-02"), ("COND-03", "OBJ-04"),
            ("COND-04", "OBJ-06"), ("COND-04", "OBJ-01"),
            ("COND-05", "OBJ-05"), ("COND-05", "OBJ-04"),
            ("COND-06", "OBJ-02"), ("COND-06", "OBJ-04"),
            ("COND-07", "OBJ-05"), ("COND-07", "OBJ-01"),
        ]
        for cid, oid in cond_obj_map:
            self.add_edge(GraphEdge(source_id=cid, target_id=oid, relation="TARGETS_OBJECTIVE"))

        # 3. Seed 25 Gold Benchmark Mufradat and connect their relational web
        for zid, m in GOLD_BENCHMARK_25_MONOGRAPHS.items():
            c_ident = m.get("canonical_identity", {})
            c_prof = m.get("classical_profile", {})
            p_cross = m.get("pharmacopoeial_crosswalk", {})
            m_evid = m.get("modern_evidence", {})
            s_fire = m.get("safety_firewall", {})

            # Mufrad Node
            self.add_node(GraphNode(
                id=zid,
                type="Mufrad",
                name=c_ident.get("canonical_unani_name", zid),
                attributes={
                    "botanical_name": c_ident.get("botanical_name", ""),
                    "family": c_ident.get("family", ""),
                    "part_used": c_ident.get("part_used", ""),
                    "evidence_grade": m_evid.get("evidence_grade", "MODERATE"),
                    "is_schedule_e1": s_fire.get("is_schedule_e1", False),
                    "toxicity_class": s_fire.get("toxicity_class", "SAFE"),
                    "upi_monograph": p_cross.get("official_book", "UPI"),
                    "citations": m.get("primary_unani_citations", []),
                    "state": m.get("governance", {}).get("state", "APPROVED_KNOWLEDGE")
                }
            ))

            # Mizaj Node & Edge
            mizaj_str = c_prof.get("mizaj", "Muaddil")
            daraja_str = c_prof.get("daraja", "1")
            mizaj_node_id = f"MIZAJ-{zid}"
            self.add_node(GraphNode(
                id=mizaj_node_id,
                type="Mizaj",
                name=mizaj_str,
                attributes={"daraja": daraja_str, "drug_id": zid}
            ))
            self.add_edge(GraphEdge(source_id=zid, target_id=mizaj_node_id, relation="POSSESSES_MIZAJ"))

            # Afaal Nodes & Edges
            for act in c_prof.get("afaal", []):
                act_slug = act.strip().lower().replace(" ", "-").replace("'", "")
                af_node_id = f"AFAAL-{act_slug}"
                if not self.get_node(af_node_id):
                    self.add_node(GraphNode(id=af_node_id, type="Afaal", name=act))
                self.add_edge(GraphEdge(source_id=zid, target_id=af_node_id, relation="EXERTS_AFAAL"))

                # Link Afaal to Objectives
                if any(k in act_slug for k in ["waja", "muhallil", "musakkin"]):
                    self.add_edge(GraphEdge(source_id=af_node_id, target_id="OBJ-03", relation="TARGETS_OBJECTIVE"))
                if any(k in act_slug for k in ["balgham", "tanqiya", "mushil"]):
                    self.add_edge(GraphEdge(source_id=af_node_id, target_id="OBJ-01", relation="TARGETS_OBJECTIVE"))
                if any(k in act_slug for k in ["raeesa", "muqawwi", "qalb", "dimagh"]):
                    self.add_edge(GraphEdge(source_id=af_node_id, target_id="OBJ-02", relation="TARGETS_OBJECTIVE"))
                if any(k in act_slug for k in ["kabid", "safra", "kasir"]):
                    self.add_edge(GraphEdge(source_id=af_node_id, target_id="OBJ-05", relation="TARGETS_OBJECTIVE"))
                if any(k in act_slug for k in ["munfith", "sual", "sadr"]):
                    self.add_edge(GraphEdge(source_id=af_node_id, target_id="OBJ-06", relation="TARGETS_OBJECTIVE"))

            # Organ Axis Affinity Edges
            for axis_str in m.get("organ_axis_affinity", []):
                for aid, aname, _ in axes:
                    axis_keyword = aname.split("(")[0].strip()
                    if axis_keyword.lower() in axis_str.lower() or any(w in axis_str.lower() for w in axis_keyword.lower().split("-")):
                        self.add_edge(GraphEdge(source_id=zid, target_id=aid, relation="ACTS_ON_AXIS"))

            # Musleh & Badal Edges
            musleh_val = c_prof.get("musleh")
            musleh_list = musleh_val if isinstance(musleh_val, list) else ([musleh_val] if musleh_val else [])
            for m_name in musleh_list:
                if m_name and m_name != "None" and isinstance(m_name, str):
                    reconciled_m = CanonicalDrugRegistry.reconcile_drug_identity(m_name)
                    if reconciled_m.get("matched"):
                        self.add_edge(GraphEdge(source_id=zid, target_id=reconciled_m["canonical_id"], relation="CORRECTED_BY", attributes={"musleh_name": m_name}))

            badal_val = c_prof.get("badal")
            badal_list = badal_val if isinstance(badal_val, list) else ([badal_val] if badal_val else [])
            for b_name in badal_list:
                if b_name and b_name != "None" and isinstance(b_name, str):
                    reconciled_b = CanonicalDrugRegistry.reconcile_drug_identity(b_name)
                    if reconciled_b.get("matched"):
                        self.add_edge(GraphEdge(source_id=zid, target_id=reconciled_b["canonical_id"], relation="SUBSTITUTE_FOR", attributes={"badal_name": b_name}))

        # 4. Classical Murakkab Compounds & Recipe Nodes
        murakkabat = [
            ("MUR-01", "Habb-e-Suranjan", "Classical formulation for joint inflammation and sciatica (Al-Qanun / Bayaz-e-Kabir)", [
                ("ZMF-002", "chief_drug"), ("ZMF-006", "supporting_drug"), ("ZMF-007", "musleh")
            ], "COND-01", "AXIS-09"),
            ("MUR-02", "Itrifal-e-Ustukhuddus", "Classical cerebral clarifier and neuro-protective formula (Qarabadin-e-Kabir)", [
                ("ZMF-004", "chief_drug"), ("ZMF-016", "supporting_drug"), ("ZMF-091", "supporting_drug")
            ], "COND-03", "AXIS-02"),
            ("MUR-03", "Sharbat-e-Bazoori Motadil", "Classical hepato-renal conduit and diuretic cooling syrup (UPI Part II)", [
                ("ZMF-011", "chief_drug"), ("ZMF-024", "supporting_drug"), ("ZMF-028", "supporting_drug")
            ], "COND-05", "AXIS-01"),
            ("MUR-04", "Jawarish-e-Jalinoos", "Classical multi-organ metabolic tonic and stomachic (Bayaz-e-Kabir)", [
                ("ZMF-005", "supporting_drug"), ("ZMF-013", "supporting_drug"), ("ZMF-016", "chief_drug"), ("ZMF-096", "musleh")
            ], "COND-02", "AXIS-05"),
            ("MUR-05", "Laooq-e-Sapistan", "Classical pectoral linctus for cough and bronchial catarrh (NFUM)", [
                ("ZMF-027", "supporting_drug"), ("ZMF-028", "chief_drug"), ("ZMF-096", "supporting_drug")
            ], "COND-04", "AXIS-04"),
        ]
        for mid, mname, mdesc, ings, mc_cond, mc_axis in murakkabat:
            self.add_node(GraphNode(id=mid, type="Murakkab", name=mname, attributes={"description": mdesc, "condition_id": mc_cond, "axis_id": mc_axis}))
            self.add_edge(GraphEdge(source_id=mid, target_id=mc_cond, relation="INDICATED_FOR"))
            self.add_edge(GraphEdge(source_id=mid, target_id=mc_axis, relation="ACTS_ON_AXIS"))
            for did, role in ings:
                self.add_edge(GraphEdge(source_id=did, target_id=mid, relation="INGREDIENT_OF", attributes={"role": role}))

    def query_graph_for_clinical_context(
        self,
        condition_id_or_name: str,
        patient_mizaj: str = "Balgham",
        active_axes: Optional[List[str]] = None,
        patient_risk_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Multi-hop relational reasoning:
        Condition -> Objectives -> Afaal -> Candidate Mufradat & Murakkabat -> Safety Firewall verification.
        """
        pctx = patient_risk_context or {}
        user_role = pctx.get("user_role", "CLINICIAN")

        # 1. Resolve Condition Node
        cond_node = None
        for n in self.get_nodes_by_type("Condition"):
            if condition_id_or_name.lower() in n.id.lower() or condition_id_or_name.lower() in n.name.lower():
                cond_node = n
                break

        if not cond_node:
            cond_node = self.get_node("COND-01")  # Default to Musculo-skeletal Waja-ul-Mafasil

        # 2. Hop 1: Condition -> Therapeutic Objectives
        obj_edges = self.get_outgoing(cond_node.id, relation="TARGETS_OBJECTIVE")
        objective_nodes = [self.get_node(e.target_id) for e in obj_edges if self.get_node(e.target_id)]

        # 3. Hop 2: Objectives -> Afaal
        matched_afaal_ids = set()
        for onode in objective_nodes:
            in_edges = self.get_incoming(onode.id, relation="TARGETS_OBJECTIVE")
            for ie in in_edges:
                src = self.get_node(ie.source_id)
                if src and src.type == "Afaal":
                    matched_afaal_ids.add(src.id)

        # 4. Hop 3: Afaal -> Candidate Mufradat
        candidate_drugs: Dict[str, Dict[str, Any]] = {}
        for af_id in matched_afaal_ids:
            drug_edges = self.get_incoming(af_id, relation="EXERTS_AFAAL")
            for de in drug_edges:
                dnode = self.get_node(de.source_id)
                if not dnode or dnode.type != "Mufrad":
                    continue

                if dnode.id not in candidate_drugs:
                    candidate_drugs[dnode.id] = {
                        "drug_id": dnode.id,
                        "canonical_name": dnode.name,
                        "botanical_name": dnode.attributes.get("botanical_name", ""),
                        "evidence_grade": dnode.attributes.get("evidence_grade", "MODERATE"),
                        "is_schedule_e1": dnode.attributes.get("is_schedule_e1", False),
                        "citations": dnode.attributes.get("citations", []),
                        "matched_afaal": [],
                        "safety_evaluation": None,
                        "recommendation_disposition": "RECOMMENDED"
                    }
                candidate_drugs[dnode.id]["matched_afaal"].append(self.get_node(af_id).name)

        # 5. Hop 4: Condition -> Classical Murakkabat
        murakkab_nodes = []
        for m_edge in self.get_incoming(cond_node.id, relation="INDICATED_FOR"):
            mnode = self.get_node(m_edge.source_id)
            if mnode and mnode.type == "Murakkab":
                # Get its ingredients from graph
                ing_edges = self.get_incoming(mnode.id, relation="INGREDIENT_OF")
                ings = []
                for ie in ing_edges:
                    ing_drug = self.get_node(ie.source_id)
                    if ing_drug:
                        ings.append({
                            "drug_id": ing_drug.id,
                            "name": ing_drug.name,
                            "role": ie.attributes.get("role", "supporting_drug")
                        })
                murakkab_nodes.append({
                    "compound_id": mnode.id,
                    "compound_name": mnode.name,
                    "description": mnode.attributes.get("description", ""),
                    "formula_class": "CLASSICAL_FORMULATION",
                    "ingredients": ings
                })

        # 6. Safety Firewall v2 Verification for Each Candidate Drug
        evaluated_candidates = []
        for did, cdata in candidate_drugs.items():
            safety_eval = SafetyFirewallV2.evaluate_drug_safety_state(
                drug_or_id={
                    "drug_id": did,
                    "is_schedule_e1": cdata["is_schedule_e1"],
                    "classical_state": "APPROVED"
                },
                user_role=user_role,
                patient_context=pctx
            )
            cdata["safety_evaluation"] = safety_eval
            if safety_eval["ai_state"] == AISafetyState.BLOCKED.value:
                cdata["recommendation_disposition"] = "BLOCKED_BY_FIREWALL"
            elif safety_eval["ai_state"] == AISafetyState.CLINICIAN_ONLY.value:
                cdata["recommendation_disposition"] = "CLINICIAN_ONLY_RESTRICTED"
            else:
                cdata["recommendation_disposition"] = "ACTIVE_COPILOT_ELIGIBLE"
            evaluated_candidates.append(cdata)

        # Sort candidates: active eligible first, then clinician restricted, then blocked
        order_map = {"ACTIVE_COPILOT_ELIGIBLE": 0, "CLINICIAN_ONLY_RESTRICTED": 1, "BLOCKED_BY_FIREWALL": 2}
        evaluated_candidates.sort(key=lambda x: (order_map.get(x["recommendation_disposition"], 3), -len(x["matched_afaal"])))

        # 7. Assemble Structured Multi-Hop Graph Result
        axis_edges = self.get_outgoing(cond_node.id, relation="ACTS_ON_AXIS")
        axis_names = [self.get_node(e.target_id).name for e in axis_edges if self.get_node(e.target_id)]

        return {
            "query_condition": {
                "id": cond_node.id,
                "name": cond_node.name,
                "category": cond_node.attributes.get("category", "")
            },
            "organ_axes": axis_names,
            "patient_mizaj_context": patient_mizaj,
            "therapeutic_objectives": [{"id": o.id, "name": o.name, "description": o.attributes.get("description", "")} for o in objective_nodes],
            "candidate_mufradat": evaluated_candidates,
            "classical_murakkabat": murakkab_nodes,
            "traversal_hop_sequence": [
                "Condition: " + cond_node.name,
                f"Organ Axes: {', '.join(axis_names)}",
                f"Therapeutic Objectives: {', '.join([o.name for o in objective_nodes])}",
                f"Matched Afaal Categories: {len(matched_afaal_ids)} specific actions",
                f"Candidate Single Drugs: {len(evaluated_candidates)} evaluated against Safety Firewall v2",
                f"Associated Classical Murakkabat: {len(murakkab_nodes)} formulations"
            ],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Global Singleton Knowledge Graph Instance
GLOBAL_CLINICAL_GRAPH = ClinicalKnowledgeGraph()


def get_clinical_knowledge_graph() -> ClinicalKnowledgeGraph:
    return GLOBAL_CLINICAL_GRAPH
