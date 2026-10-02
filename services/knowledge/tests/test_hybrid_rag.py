import math
from app.core.hybrid_rag import (
    BM25Index,
    DeterministicSemanticEmbeddingProvider,
    DenseVectorStore,
    Document,
    ZAYVORAIntelligenceEngine,
    reciprocal_rank_fusion,
    _tokenize,
)


def test_tokenizer_unigrams_and_bigrams():
    text = "Suranjan Talkh treats Mafasil"
    tokens = _tokenize(text)
    assert "suranjan" in tokens
    assert "talkh" in tokens
    assert "mafasil" in tokens
    assert "suranjan_talkh" in tokens


def test_bm25_lexical_search():
    docs = [
        Document("doc1", "mufrad", "Suranjan Talkh", "Colchicum luteum for severe articular gout and Mafasil pain."),
        Document("doc2", "mufrad", "Sonf", "Foeniculum vulgare for Meda Amaa stomach digestion and carminative action."),
        Document("doc3", "murakkab", "Majun Falasifa", "Electuary for strengthening kidney kulliya and brain dimagh."),
    ]
    bm25 = BM25Index()
    bm25.index_documents(docs)

    # Search for gout / suranjan
    res1 = bm25.search("suranjan gout")
    assert len(res1) > 0
    assert res1[0][0] == "doc1"

    # Search for stomach / digestion
    res2 = bm25.search("stomach digestion sonf")
    assert len(res2) > 0
    assert res2[0][0] == "doc2"


def test_deterministic_embedding_provider():
    provider = DeterministicSemanticEmbeddingProvider(dim=128)
    vec1 = provider.get_embedding("articular gout and suranjan talkh")
    assert len(vec1) == 128
    # Test L2 normalization
    norm = math.sqrt(sum(x * x for x in vec1))
    assert math.isclose(norm, 1.0, rel_tol=1e-4)

    # Identical text produces identical embedding
    vec2 = provider.get_embedding("articular gout and suranjan talkh")
    assert vec1 == vec2


def test_dense_vector_store_retrieval():
    docs = [
        Document("d1", "mufrad", "Suranjan Talkh", "Colchicum toxic alkaloid colchicine for joint inflammation."),
        Document("d2", "mufrad", "Asrul", "Rauwolfia serpentina for hypertension and sedation."),
    ]
    store = DenseVectorStore()
    store.index_documents(docs)

    scores = store.search("joint inflammation arthritis")
    assert len(scores) == 2
    # d1 should have higher semantic similarity to joint inflammation
    assert scores[0][0] == "d1"


def test_reciprocal_rank_fusion():
    list_dense = [("docA", 0.95), ("docB", 0.85), ("docC", 0.70)]
    list_bm25 = [("docB", 12.4), ("docA", 8.2), ("docD", 5.1)]
    list_graph = [("docB", 2.0), ("docC", 1.0)]

    rrf = reciprocal_rank_fusion([list_dense, list_bm25, list_graph])
    # docB is rank 2 in dense, rank 1 in bm25, rank 1 in graph -> should be clear winner
    assert rrf[0][0] == "docB"


def test_hybrid_rag_engine_full_lifecycle():
    engine = ZAYVORAIntelligenceEngine()
    total_loaded = engine.load_canonical_corpus()
    assert total_loaded >= 20

    # Hybrid search for joint pain and Suranjan
    results = engine.hybrid_search(
        query="Suranjan Talkh gout and joint pain",
        organ_axis="mafasil",
        temperament="Safrawi",
        top_k=5,
        mode="rrf",
    )

    assert len(results) > 0
    top_doc = results[0]
    assert "suranjan" in top_doc["title"].lower() or "suranjan" in top_doc["content"].lower()
    # Suranjan is a Schedule E1 poison, verify flag
    assert any(r["is_schedule_e1"] for r in results)


def test_hybrid_rag_weighted_mode():
    engine = ZAYVORAIntelligenceEngine()
    engine.load_canonical_corpus()

    results = engine.hybrid_search(
        query="digestive weakness Meda-Amaa Sonf",
        organ_axis="meda-amaa",
        top_k=3,
        mode="weighted",
    )
    assert len(results) == 3
    assert all("score" in r for r in results)
