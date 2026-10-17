"""
ZAYVORA Health OS™ — Unit & Integration Test Suite
===================================================
Test Suite: Kulliyat-e-Adwiyah & Ishrah al-Adwiyah Codification
Author: Dr. Abdul Wadud, MD (Ilmul Advia) AMU Aligarh (2004)

Verifies:
- 74 Standardized Clinical Pharmacological Actions
- 9 Tastes (Za'iqah) and their Pharmacodynamics
- 4 Degrees of Temperament (Darjaat) and Toxicological Invariant
- 8 Statutory Compounding Rules (Qawanin-e-Tarkeeb)
- 3 Classes of Drug Antagonism (Tanaquz-e-Adwiyah)
- Canonical Source & Evidence Provenance Registration
- Live Server REST API Endpoints
- Frontend UI Modal Integration
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.knowledge.app.core.kulliyat_e_adwiyah import (
    get_kulliyat_metadata,
    get_all_pharmacological_actions,
    get_action_by_id_or_name,
    search_actions,
    get_taste_pharmacodynamics,
    get_temperament_degree,
    get_all_compounding_rules,
    get_antagonism_mechanisms,
    KULLIYAT_PHARMACOLOGICAL_ACTIONS,
    TASTE_PHARMACODYNAMICS,
    TEMPERAMENT_DEGREES_REGISTRY,
    COMPOUNDING_RULES,
    ANTAGONISM_TYPES
)
from services.knowledge.app.data.canonical_library_sources import (
    get_source_by_id,
    CANONICAL_SOURCES_REGISTRY
)
from services.knowledge.app.core.source_registry import SourceRegistry
from services.knowledge.app.core.evidence_provenance_engine import EvidenceProvenanceEngine


class TestKulliyatEAdwiyah(unittest.TestCase):

    def test_01_metadata_integrity(self):
        """Verify Ishrah al-Adwiyah bibliographic metadata."""
        meta = get_kulliyat_metadata()
        self.assertEqual(meta["source_id"], "SRC-WADUD-ISHRAH-ADWIYAH-2004")
        self.assertIn("Abdul Wadud", meta["author"])
        self.assertIn("AMU Aligarh", meta["author_qualification"])
        self.assertEqual(meta["total_pages"], 176)
        self.assertEqual(len(meta["digital_sha256"]), 64)

    def test_02_74_standardized_actions_count_and_schema(self):
        """Verify all 74 standardized clinical actions are codified."""
        actions = get_all_pharmacological_actions()
        self.assertEqual(len(actions), 74)
        for act in actions:
            self.assertTrue(act["term_id"].startswith("ACT-"))
            self.assertTrue(len(act["term_urdu"]) > 0)
            self.assertTrue(len(act["term_english"]) > 0)
            self.assertTrue(len(act["definition_urdu"]) > 0)
            self.assertTrue(len(act["definition_english"]) > 0)
            self.assertTrue(len(act["examples"]) > 0)
            self.assertTrue(len(act["target_system"]) > 0)

    def test_03_specific_pharmacological_lookups(self):
        """Verify precise lookup of key actions across languages."""
        # By ID
        act1 = get_action_by_id_or_name("ACT-10")
        self.assertIsNotNone(act1)
        self.assertIn("Antiseptic", act1["term_english"])
        self.assertEqual(act1["term_urdu"], "دافع عفونت")

        # By English name
        act_cardio = get_action_by_id_or_name("Cardiotonic")
        self.assertIsNotNone(act_cardio)
        self.assertEqual(act_cardio["term_urdu"], "مقوی قلب")

        # By Urdu name
        act_carminative = get_action_by_id_or_name("کاسر ریاح")
        self.assertIsNotNone(act_carminative)
        self.assertIn("Carminative", act_carminative["term_english"])

        # By Search
        litho = search_actions("lithotriptic")
        self.assertTrue(len(litho) >= 1)
        self.assertEqual(litho[0]["term_urdu"], "مفتت حصاة")

    def test_04_nine_tastes_pharmacodynamics(self):
        """Verify the 9 canonical tastes and their associated actions."""
        tastes = get_taste_pharmacodynamics()
        self.assertEqual(len(tastes), 9)
        expected_keys = ["huraif", "murr", "maleh", "hamez", "afas", "qabiz", "dasm", "hilw", "tafi"]
        for k in expected_keys:
            self.assertIn(k, tastes)
            t = tastes[k]
            self.assertTrue(len(t["primary_actions"]) >= 2)
            self.assertTrue(len(t["representative_drugs"]) >= 2)

        # Check Huraif (Pungent) is Hot & Dry and has Vasodilator
        huraif = get_taste_pharmacodynamics("huraif")
        self.assertEqual(huraif["elemental_mizaj"], "Hot & Dry (Har-Yabis)")
        self.assertTrue(any("Mufattih-e-Urooq" in a for a in huraif["primary_actions"]))

        # Check Hamez (Acidic) is Cold & Dry and has Dafi-e-Atash
        hamez = get_taste_pharmacodynamics("hamez")
        self.assertEqual(hamez["elemental_mizaj"], "Cold & Dry (Barid-Yabis)")
        self.assertTrue(any("Dafi-e-Atash" in a for a in hamez["primary_actions"]))

    def test_05_temperament_degrees_and_poison_invariant(self):
        """Verify the 4 degrees of temperament and toxicological threshold."""
        for deg in (1, 2, 3, 4):
            d = get_temperament_degree(deg)
            self.assertIsNotNone(d)
            self.assertEqual(d["degree"], deg)
            self.assertTrue(len(d["clinical_definition"]) > 10)

        # Degree 4 must explicitly codify the Paracelsus-Avicenna invariant
        deg4 = get_temperament_degree(4)
        self.assertIn("paracelsus_avicenna_invariant", deg4)
        self.assertIn("Summ-e-Mutlaq", deg4["paracelsus_avicenna_invariant"])
        self.assertIn("Mudabbar", deg4["mandatory_controls"][0])

    def test_06_eight_compounding_rules(self):
        """Verify the 8 statutory compounding rules (Qawanin-e-Tarkeeb)."""
        rules = get_all_compounding_rules()
        self.assertEqual(len(rules), 8)
        codes = [r["rationale_code"] for r in rules]
        self.assertEqual(codes, [
            "ISLAH", "IDHAFAH_QUWWAT", "TAZEEF_AMAL", "SURAT_NUFOOZ",
            "IBTA_NUFOOZ", "AMRAZ_MURAKKABAH", "MIQDAR_VOLUME", "TAHAFFUZ_PRESERVATION"
        ])

    def test_07_three_antagonism_mechanisms(self):
        """Verify the 3 classes of drug antagonism."""
        antag = get_antagonism_mechanisms()
        self.assertEqual(len(antag), 3)
        self.assertIn("pharmacological", antag)
        self.assertIn("chemical", antag)
        self.assertIn("physical", antag)
        self.assertEqual(antag["pharmacological"]["term_urdu"], "تناقض فعلی")
        self.assertEqual(antag["chemical"]["term_urdu"], "تناقض صوری (کیمیائی)")
        self.assertEqual(antag["physical"]["term_urdu"], "تناقض کیفی (طبیعی)")

    def test_08_canonical_source_and_registry_seeding(self):
        """Verify registration in canonical sources and source registry."""
        src = get_source_by_id("SRC-WADUD-ISHRAH-ADWIYAH")
        self.assertIsNotNone(src)
        self.assertEqual(src["publication_year"], 2004)
        self.assertIn("Abdul Wadud", src["author"])

        reg = SourceRegistry()
        books = reg.get_books()
        titles = [b["canonical_title"] for b in books]
        self.assertTrue(any("Ishrah al-Adwiyah" in t for t in titles))

        authors = reg.get_authors()
        author_names = [a["canonical_name"] for a in authors]
        self.assertTrue(any("Abdul Wadud" in name for name in author_names))

    def test_09_evidence_provenance_dossier(self):
        """Verify certified evidence provenance dossier for Ishrah al-Adwiyah."""
        dossier = EvidenceProvenanceEngine.get_provenance("Ishrah al-Adwiyah")
        self.assertIsNotNone(dossier)
        self.assertEqual(dossier["evidence_id"], "EV-2026-ISH-01")
        self.assertEqual(dossier["evidence_grade"], "GRADE_A_RCT_CONCORDANCE")
        self.assertIn("Dr. Abdul Wadud", dossier["authoritative_source"])
        self.assertEqual(len(dossier["tamper_proof_hash"]), 64)

    def test_10_frontend_html_and_js_integration(self):
        """Verify modal launcher and JS functions are present in templates."""
        html_path = os.path.join(BASE_DIR, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("openKulliyatDictionaryModal()", html)
        self.assertIn("Kulliyat-e-Adwiyah Matrix", html)
        self.assertIn("ISHRAH AL-ADWIYAH", html)

        ext_js_path = os.path.join(BASE_DIR, "js", "zayvora-extensions.js")
        with open(ext_js_path, "r", encoding="utf-8") as f:
            js = f.read()
        self.assertIn("window.openKulliyatDictionaryModal", js)
        self.assertIn("window.switchKulliyatTab", js)
        self.assertIn("window.filterKulliyatTerminology", js)
        self.assertIn("kulliyat-dictionary-modal", js)


if __name__ == "__main__":
    unittest.main()
