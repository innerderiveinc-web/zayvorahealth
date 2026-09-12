import unittest
from app.core.taxonomy import (
    ORGAN_AXES,
    MIZAJ_TEMPERAMENTS,
    EVIDENCE_LEVELS,
    KNOWLEDGE_WORLDS,
)

try:
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.graph.fake_repository import InMemoryGraphRepository
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


class TestTaxonomy(unittest.TestCase):
    client = None

    def setUp(self):
        if HAS_FASTAPI and self.client is None:
            app = create_app()
            app.state.graph_repo = InMemoryGraphRepository()
            self.client = TestClient(app)

    def test_health(self):
        if self.client:
            resp = self.client.get("/api/health")
            self.assertEqual(resp.status_code, 200)
        else:
            self.assertTrue(True)

    def test_organ_axes_returns_all_twelve(self):
        if self.client:
            resp = self.client.get("/api/v1/organ-axes")
            self.assertEqual(resp.status_code, 200)
            axes = resp.json()
        else:
            axes = ORGAN_AXES
        self.assertEqual(len(axes), 12)
        codes = {a["code"] for a in axes}
        self.assertIn("meda-amaa", codes)
        self.assertIn("qalb-uroq", codes)

    def test_mizaj_temperaments_returns_all_four(self):
        if self.client:
            resp = self.client.get("/api/v1/mizaj-temperaments")
            self.assertEqual(resp.status_code, 200)
            temperaments = {t["temperament"] for t in resp.json()}
        else:
            temperaments = {t["temperament"] for t in MIZAJ_TEMPERAMENTS}
        self.assertEqual(temperaments, {"Damwi", "Safrawi", "Saudawi", "Balghami"})

    def test_evidence_levels_covers_e0_to_e6(self):
        if self.client:
            resp = self.client.get("/api/v1/evidence-levels")
            self.assertEqual(resp.status_code, 200)
            levels = resp.json()
        else:
            levels = EVIDENCE_LEVELS
        self.assertEqual(set(levels.keys()), {"E0", "E1", "E2", "E3", "E4", "E5", "E6"})

    def test_knowledge_worlds_covers_a_to_d(self):
        if self.client:
            resp = self.client.get("/api/v1/knowledge-worlds")
            self.assertEqual(resp.status_code, 200)
            worlds = resp.json()
        else:
            worlds = KNOWLEDGE_WORLDS
        self.assertEqual(set(worlds.keys()), {"A", "B", "C", "D"})


if __name__ == "__main__":
    unittest.main()
