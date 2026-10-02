# services/knowledge/tests/test_hybrid_rag_multi_axis.py
"""Tests for the updated Hybrid RAG engine supporting multiple organ axes.
These tests use the deterministic embedding provider (BioBERT is not installed
in the sandbox) and verify that a list of axes is accepted without error.
"""

from __future__ import annotations

import os

from app.core.hybrid_rag import ZAYVORAIntelligenceEngine

def test_hybrid_search_multi_axis():
    # Ensure BioBERT is disabled (default) – the engine will use the deterministic provider.
    os.environ["USE_BIOBERT"] = "false"
    engine = ZAYVORAIntelligenceEngine()
    # Load corpus to have data
    engine.load_canonical_corpus()
    # Use a list of axes; they may not match any document but should not raise.
    results = engine.hybrid_search(
        query="treat joint pain",
        organ_axis=["AX1", "AX2"],
        temperament=None,
        top_k=3,
    )
    assert isinstance(results, list)
    # At least one result should be returned from the corpus.
    assert len(results) > 0
    # Each result should contain expected keys.
    for r in results:
        assert "document_id" in r
        assert "score" in r
        assert "doc_type" in r
