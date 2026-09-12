"""
Tests for Global Command Center (Cmd+K) Unified Search Engine
"""

try:
    import pytest
except ImportError:
    pytest = None

from app.core.command_search import CommandSearchEngine, SearchResultItem


def test_command_search_empty_returns_shortcuts():
    results = CommandSearchEngine.search("")
    assert len(results) >= 4
    categories = [r.category for r in results]
    assert "navigation" in categories
    assert any("Digital Twin" in r.title for r in results)


def test_command_search_mufradat_query():
    results = CommandSearchEngine.search("Suranjan")
    assert len(results) > 0
    mufrad_results = [r for r in results if r.category == "mufradat"]
    assert len(mufrad_results) > 0
    item = mufrad_results[0]
    assert "Suranjan" in item.title
    assert "Colchicum" in item.subtitle or item.metadata.get("botanical")


def test_command_search_schedule_e1_badge():
    results = CommandSearchEngine.search("Kuchla")
    e1_items = [r for r in results if r.badge == "Schedule E(1)"]
    assert len(e1_items) > 0
    assert e1_items[0].metadata.get("is_schedule_e1") is True


def test_command_search_murakkabat_query():
    results = CommandSearchEngine.search("Majun")
    assert len(results) > 0
    compound_results = [r for r in results if r.category == "murakkabat"]
    assert len(compound_results) > 0
    assert any("Majun" in r.title for r in compound_results)


def test_command_search_amraz_and_icd11():
    results = CommandSearchEngine.search("Gout")
    assert len(results) > 0
    amraz_items = [r for r in results if r.category == "amraz"]
    assert len(amraz_items) > 0
    assert "FA20" in amraz_items[0].badge
    assert "Niqras" in amraz_items[0].title


def test_command_search_tadbeer_query():
    results = CommandSearchEngine.search("Hijama")
    assert len(results) > 0
    tadbeer_items = [r for r in results if r.category == "tadbeer"]
    assert len(tadbeer_items) > 0
    assert "Cupping" in tadbeer_items[0].title
