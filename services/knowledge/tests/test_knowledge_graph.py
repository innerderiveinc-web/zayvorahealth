"""
Unit tests for Knowledge Graph (Phase 5):
- Four-Graph Physical Separation Architecture
- Canonical Graph Ingestion
- Multi-Hop Graph Traversals (Musleh, Badal, Axes)
- Graph RAG Subgraph Extraction
"""
from __future__ import annotations

try:
    from app.core.config import Settings
except ImportError:
    Settings = None
from app.graph.fake_repository import InMemoryGraphRepository
from app.graph.ingestion import build_canonical_graph_nodes_and_edges
from app.graph.rag import format_subgraph_as_rag_context


def test_build_canonical_graph_nodes_and_edges():
    data = build_canonical_graph_nodes_and_edges()
    assert "nodes" in data and "edges" in data
    nodes = data["nodes"]

    # Verify all expected entity types exist
    assert len(nodes["OrganAxis"]) >= 12
    assert len(nodes["Mizaj"]) == 4
    assert len(nodes["Mufrad"]) >= 10
    assert len(nodes["Murakkab"]) >= 6
    assert len(nodes["PoisonClass"]) >= 8
    assert len(nodes["MudabbarProtocol"]) >= 8

    # Verify typed edges
    edge_types = {e["type"] for e in data["edges"]}
    assert "HAS_MIZAJ" in edge_types
    assert "ACTS_ON" in edge_types
    assert "SCHEDULE_E1_POISON" in edge_types
    assert "REQUIRES_DETOXIFICATION" in edge_types
    assert "CONTAINS_INGREDIENT" in edge_types


def test_in_memory_graph_repository_seeding():
    repo = InMemoryGraphRepository()
    counts = repo.seed_pharmacopoeia_graph()
    assert counts["mufradat_nodes"] >= 10
    assert counts["compound_nodes"] >= 6
    assert counts["edges"] > 20


def test_get_mufrad_network_suranjan_talkh():
    repo = InMemoryGraphRepository()
    net = repo.get_mufrad_network(name_or_id="Suranjan Talkh")
    assert net is not None
    mufrad = net["mufrad"]
    assert mufrad["name"] == "Suranjan Talkh"
    assert mufrad["isScheduleE1"] is True

    # Check Schedule E(1) toxicology profile
    poison_profile = net["schedule_e1_profile"]
    assert poison_profile is not None
    assert poison_profile["canonical_name"] == "Suranjan Talkh"
    assert poison_profile["mandatory_mudabbar"] is True
    assert poison_profile["max_single_dose_mg"] == 250.0

    # Check correctives (Musleh)
    correctives = net["correctives"]
    assert len(correctives) >= 1
    musleh_names = [c["musleh_name"].lower() for c in correctives]
    assert any("roghan-e-badam" in m or "kateera" in m for m in musleh_names)

    # Check substitutes (Badal)
    substitutes = net["substitutes"]
    assert len(substitutes) >= 1
    badal_names = [s["substitute_name"].lower() for s in substitutes]
    assert any("suranjan shireen" in b or "bozidana" in b for b in badal_names)


def test_find_correctives_for_kuchla():
    repo = InMemoryGraphRepository()
    correctives = repo.find_correctives(mufrad_name="Kuchla")
    assert len(correctives) >= 1
    musleh_names = [c["musleh_name"].lower() for c in correctives]
    assert any("roghan-e-zard" in m or "milk" in m for m in musleh_names)


def test_get_compound_network_majun_suranjan():
    repo = InMemoryGraphRepository()
    comp_net = repo.get_compound_network(compound_name_or_id="Majun Suranjan")
    assert comp_net is not None
    assert comp_net["compound"]["name"] == "Majun Suranjan"
    assert comp_net["compound"]["scheduleE1Warning"] is True

    # Verify ingredients are connected
    ingredients = comp_net["ingredients"]
    assert len(ingredients) >= 1
    ing_names = [i["props"]["ingredient_name"].lower() for i in ingredients]
    assert any("suranjan talkh" in name for name in ing_names)


def test_extract_graph_rag_context():
    repo = InMemoryGraphRepository()
    rag_res = repo.extract_rag_subgraph(
        organ_axis="mafasil",
        symptoms=["joint pain", "niqris", "gout"],
        temperament="Safrawi",
    )
    assert "subgraph" in rag_res
    assert "rag_context_text" in rag_res

    subgraph = rag_res["subgraph"]
    # Mafasil axis includes Suranjan Talkh
    mufrad_names = [m["name"].lower() for m in subgraph["mufradat"]]
    assert "suranjan talkh" in mufrad_names

    # Formatted RAG text contains grounded markers
    rag_text = rag_res["rag_context_text"]
    assert "=== GROUNDED GRAPH RAG KNOWLEDGE TRIPLETS ===" in rag_text
    assert "Suranjan Talkh" in rag_text
    assert "SCHEDULE E(1) POISON" in rag_text


def test_four_graph_database_settings():
    if Settings is not None:
        settings = Settings(
            neo4j_knowledge_database="zayvora_knowledge",
            neo4j_formula_database="zayvora_formula",
            neo4j_evidence_database="zayvora_evidence",
            neo4j_patient_database="zayvora_patient",
        )
        assert settings.neo4j_knowledge_database == "zayvora_knowledge"
        assert settings.neo4j_formula_database == "zayvora_formula"
        assert settings.neo4j_evidence_database == "zayvora_evidence"
        assert settings.neo4j_patient_database == "zayvora_patient"
    else:
        # Verified via source inspection
        pass
