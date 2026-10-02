# services/knowledge/tests/test_taxonomy_custom.py
"""Tests for the custom taxonomy router (Phase 11).
These tests verify basic CRUD operations for RegionalHerb and CustomMufrad.
"""

from __future__ import annotations

import unittest

try:
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.graph.fake_repository import InMemoryGraphRepository
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

class TestTaxonomyCustom(unittest.TestCase):
    client = None

    def setUp(self):
        if HAS_FASTAPI and self.client is None:
            app = create_app()
            # Replace real repo with in‑memory repo for isolation
            app.state.graph_repo = InMemoryGraphRepository()
            self.client = TestClient(app)

    def test_regional_herb_crud(self):
        if not self.client:
            self.skipTest("FastAPI not available in test environment")
        # Create
        herb_data = {"name": "Basil", "scientific_name": "Ocimum basilicum", "description": "Aromatic herb"}
        resp = self.client.post("/api/v1/zkb/taxonomy_custom/regional_herb", json=herb_data)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), herb_data)
        # Retrieve
        resp = self.client.get("/api/v1/zkb/taxonomy_custom/regional_herb/Basil")
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), herb_data)
        # Update
        updated = {"name": "Basil", "scientific_name": "Ocimum basilicum L.", "description": "Fresh aromatic leaf"}
        resp = self.client.put("/api/v1/zkb/taxonomy_custom/regional_herb/Basil", json=updated)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), updated)
        # Delete
        resp = self.client.delete("/api/v1/zkb/taxonomy_custom/regional_herb/Basil")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("deleted"), "Basil")

    def test_custom_mufrad_crud(self):
        if not self.client:
            self.skipTest("FastAPI not available in test environment")
        mufrad = {
            "name": "Habbat-e-Sauda",
            "botanical_name": "Rosa damascena",
            "mizaj": {"temperature": "warm", "dryness": "dry"},
            "afal": ["relieves pain", "improves digestion"]
        }
        # Create
        resp = self.client.post("/api/v1/zkb/taxonomy_custom/custom_mufrad", json=mufrad)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), mufrad)
        # Retrieve
        resp = self.client.get("/api/v1/zkb/taxonomy_custom/custom_mufrad/Habbat-e-Sauda")
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), mufrad)
        # Update
        updated = mufrad.copy()
        updated["mizaj"] = {"temperature": "hot", "dryness": "wet"}
        resp = self.client.put("/api/v1/zkb/taxonomy_custom/custom_mufrad/Habbat-e-Sauda", json=updated)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), updated)
        # Delete
        resp = self.client.delete("/api/v1/zkb/taxonomy_custom/custom_mufrad/Habbat-e-Sauda")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("deleted"), "Habbat-e-Sauda")

if __name__ == "__main__":
    unittest.main()
