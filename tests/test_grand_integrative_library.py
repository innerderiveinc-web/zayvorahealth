"""
Test Suite: ZAYVORA Grand Classical & Modern Integrative Medical Library
=========================================================================
Validates the complete 12-volume authoritative medical encyclopedia:
- Volume and chapter schema integrity
- Dual-language terminology (English + Urdu/Arabic)
- Classical literature citations (Ibn Sina, Al-Razi, Al-Majusi, Najmul Ghani, Kabiruddin)
- Modern biomedical correlations (Biomarkers, Imaging, Metagenomics, IoT, Epigenetics)
- Fast semantic search across clinical concepts
- Clinical diagnostic criteria and actionable protocols
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.knowledge.app.data.grand_integrative_library_master import (
    GRAND_INTEGRATIVE_LIBRARY,
    LIBRARY_METADATA,
    get_all_volumes,
    get_volume_by_id,
    get_chapter_by_id,
    get_chapter_treatise,
    search_library,
    get_all_mufradat,
    get_mufrad_by_id,
    search_mufradat,
    get_all_murakkabat,
    get_murakkab_by_id,
    search_murakkabat,
    get_all_drug_interactions,
    search_drug_interactions,
)


class TestGrandIntegrativeLibrary(unittest.TestCase):

    def test_01_library_metadata_and_structure(self):
        """Validates library high-level metadata and standard conformance."""
        self.assertIn("ZAYVORA Grand Classical & Modern Integrative Medical Library", LIBRARY_METADATA["title"])
        self.assertEqual(LIBRARY_METADATA["total_volumes"], 12)
        self.assertEqual(LIBRARY_METADATA["curation_status"], "AUTHENTIC_CLINICAL_GRADE")
        self.assertIn("UPI Parts I-II", LIBRARY_METADATA["statutory_standards"])

    def test_02_all_12_volumes_present_and_complete(self):
        """Ensures all 12 volumes are properly structured with required fields."""
        volumes = get_all_volumes()
        self.assertEqual(len(volumes), 12, "Must have exactly 12 master volumes")
        
        expected_vol_ids = [f"vol-{i:02d}" for i in range(1, 13)]
        actual_vol_ids = [v["id"] for v in volumes]
        self.assertEqual(actual_vol_ids, expected_vol_ids)

        for v in volumes:
            self.assertTrue(v["title_en"], f"Volume {v['id']} missing English title")
            self.assertTrue(v["title_ur"], f"Volume {v['id']} missing Urdu title")
            self.assertTrue(v["icon"], f"Volume {v['id']} missing icon")
            self.assertTrue(v["badge"], f"Volume {v['id']} missing badge")
            self.assertTrue(v["summary"], f"Volume {v['id']} missing summary")
            self.assertGreater(v["chapter_count"], 0, f"Volume {v['id']} has no chapters")

    def test_03_chapter_rich_schema_integrity(self):
        """Verifies every chapter has authentic clinical depth and no placeholder text."""
        volumes = GRAND_INTEGRATIVE_LIBRARY["volumes"]
        total_chapters = 0

        for v in volumes:
            for c in v["chapters"]:
                total_chapters += 1
                self.assertTrue(c["id"].startswith("ch-"))
                self.assertTrue(c["chapter_number"])
                self.assertTrue(c["title_en"])
                self.assertTrue(c["title_ur"])
                
                # Check key concepts
                self.assertGreaterEqual(len(c["key_concepts"]), 2, f"Chapter {c['id']} must have at least 2 key concepts")
                
                # Check classical citations
                self.assertGreaterEqual(len(c["classical_citations"]), 1, f"Chapter {c['id']} must cite classical texts")
                for cit in c["classical_citations"]:
                    self.assertTrue(cit.get("book"))
                    self.assertTrue(cit.get("author"))
                    self.assertTrue(cit.get("text"))

                # Check modern biomedical correlation
                self.assertGreater(len(c["modern_biomedical_correlation"]), 40, f"Chapter {c['id']} must have detailed biomedical correlation")
                
                # Check diagnostic criteria and protocols
                self.assertTrue(c["clinical_diagnostic_criteria"])
                self.assertTrue(c["actionable_protocols"])
                self.assertTrue(c["safety_and_contraindications"])

        self.assertGreaterEqual(total_chapters, 35, "Must have comprehensive chapter coverage")

    def test_04_lookup_by_volume_and_chapter_id(self):
        """Validates specific retrieval of volumes and individual chapters."""
        vol_01 = get_volume_by_id("vol-01")
        self.assertIsNotNone(vol_01)
        self.assertEqual(vol_01["volume_number"], 1)

        # Lookup by integer string
        vol_05 = get_volume_by_id("5")
        self.assertIsNotNone(vol_05)
        self.assertEqual(vol_05["title_en"], "Radio-Diagnostics & Medical Imaging")

        # Chapter retrieval with inherited volume context
        ch_nabz = get_chapter_by_id("ch-03-01")
        self.assertIsNotNone(ch_nabz)
        self.assertIn("Ajnas", ch_nabz["title_en"])
        self.assertEqual(ch_nabz["volume_id"], "vol-03")
        self.assertEqual(ch_nabz["volume_icon"], "🩺")

    def test_05_clinical_biomarkers_volume_verification(self):
        """Validates Volume IV (Clinical Lab Biomarkers & Modern Pathology)."""
        vol_04 = get_volume_by_id("vol-04")
        self.assertIsNotNone(vol_04)
        chapter_titles = [c["title_en"] for c in vol_04["chapters"]]
        self.assertTrue(any("hs-CRP" in t for t in chapter_titles))
        self.assertTrue(any("HbA1c" in t for t in chapter_titles))
        self.assertTrue(any("Hepatorenal" in t for t in chapter_titles))

    def test_06_radio_diagnostics_and_imaging_verification(self):
        """Validates Volume V (Radio-Diagnostics & Medical Imaging)."""
        vol_05 = get_volume_by_id("vol-05")
        self.assertIsNotNone(vol_05)
        chapter_titles = [c["title_en"] for c in vol_05["chapters"]]
        self.assertTrue(any("X-Ray & MRI" in t for t in chapter_titles))
        self.assertTrue(any("Ultrasound & FibroScan" in t for t in chapter_titles))
        self.assertTrue(any("DEXA" in t for t in chapter_titles))

    def test_07_gut_microbiome_and_epigenetics_verification(self):
        """Validates Volume VI (Gut Microbiome, Metagenomics & Epigenetics)."""
        vol_06 = get_volume_by_id("vol-06")
        self.assertIsNotNone(vol_06)
        all_concepts = [concept for c in vol_06["chapters"] for concept in c["key_concepts"]]
        self.assertTrue(any("Hazm-e-Meda" in conc or "Kiloos" in conc for conc in all_concepts))
        self.assertTrue(any("Short-Chain Fatty Acids" in conc or "Butyrate" in conc for conc in all_concepts))

    def test_08_wearables_iot_and_computer_vision_verification(self):
        """Validates Volume VII (Continuous Wearables, IoT & Smartphone AI Vision)."""
        vol_07 = get_volume_by_id("vol-07")
        self.assertIsNotNone(vol_07)
        ch_titles = [c["title_en"] for c in vol_07["chapters"]]
        self.assertTrue(any("Continuous Glucose Monitoring" in t for t in ch_titles))
        self.assertTrue(any("Heart Rate Variability" in t for t in ch_titles))
        self.assertTrue(any("Computer Vision" in t for t in ch_titles))

    def test_09_preventive_and_mental_health_verification(self):
        """Validates Volume II (Asbab-e-Sitta / Preventive) and Volume X (Mental Health)."""
        vol_02 = get_volume_by_id("vol-02")
        self.assertEqual(len(vol_02["chapters"]), 6, "Asbab-e-Sitta must have all 6 prerequisites codified")
        
        vol_10 = get_volume_by_id("vol-10")
        all_concepts_10 = [concept for c in vol_10["chapters"] for concept in c["key_concepts"]]
        self.assertTrue(any("Malikhooliya" in conc for conc in all_concepts_10))
        self.assertTrue(any("Waswas" in conc for conc in all_concepts_10))
        self.assertTrue(any("Sahar" in conc for conc in all_concepts_10))

    def test_10_specialized_disciplines_verification(self):
        """Validates Volume XI (Specialized Clinical Disciplines: PCOS, Pediatrics, Sports)."""
        vol_11 = get_volume_by_id("vol-11")
        all_concepts_11 = [concept for c in vol_11["chapters"] for concept in c["key_concepts"]]
        self.assertTrue(any("PCOS" in conc for conc in all_concepts_11))
        self.assertTrue(any("Pediatrics" in conc or "Atfaal" in conc for conc in all_concepts_11))
        self.assertTrue(any("Vitiligo" in conc or "Babchi" in conc for conc in all_concepts_11))

    def test_11_cyp450_safety_and_emergency_triage_verification(self):
        """Validates Volume XII (Safety, CYP450 Herb-Drug Interactions & Triage)."""
        vol_12 = get_volume_by_id("vol-12")
        all_concepts_12 = [concept for c in vol_12["chapters"] for concept in c["key_concepts"]]
        self.assertTrue(any("CYP3A4" in conc or "CYP2D6" in conc for conc in all_concepts_12))
        self.assertTrue(any("Dual-Track Tapering" in conc for conc in all_concepts_12))
        self.assertTrue(any("Myocardial Infarction" in conc for conc in all_concepts_12))

    def test_12_fast_semantic_search_engine(self):
        """Tests the multi-token clinical search engine across the library."""
        # Test exact term
        res_crp = search_library("hs-CRP")
        self.assertGreaterEqual(len(res_crp), 1)
        self.assertIn("Inflammatory", res_crp[0]["title_en"])

        # Test classical term
        res_nabz = search_library("10-Ajnas")
        self.assertGreaterEqual(len(res_nabz), 1)
        self.assertIn("Nabz", res_nabz[0]["title_en"])

        # Test imaging term
        res_fibro = search_library("FibroScan")
        self.assertGreaterEqual(len(res_fibro), 1)
        self.assertIn("Ultrasound", res_fibro[0]["title_en"])

        # Test mental health term
        res_dep = search_library("Malikhooliya")
        self.assertGreaterEqual(len(res_dep), 1)
        self.assertIn("Psychiatric", res_dep[0]["title_en"])

        # Empty search
        self.assertEqual(search_library(""), [])

    def test_13_dual_layer_full_treatise_completeness(self):
        """Verifies that all 38 chapters possess an exhaustive Layer 2 Canonical Treatise."""
        volumes = GRAND_INTEGRATIVE_LIBRARY["volumes"]
        total_treatises = 0

        required_sections = [
            "canonical_philosophy_and_doctrine",
            "molecular_and_cellular_pathophysiology",
            "step_by_step_clinical_examination",
            "comprehensive_pharmacopeia_and_recipes",
            "clinical_case_study"
        ]

        for v in volumes:
            for c in v["chapters"]:
                total_treatises += 1
                self.assertIn("full_treatise", c, f"Chapter {c['id']} must have 'full_treatise' for Layer 2")
                tr = c["full_treatise"]
                self.assertIsNotNone(tr, f"Treatise for chapter {c['id']} cannot be None")

                # Verify all 5 canonical sections
                for sec in required_sections:
                    self.assertIn(sec, tr, f"Chapter {c['id']} treatise missing section '{sec}'")
                    content = tr[sec]
                    self.assertTrue(isinstance(content, str) and len(content.strip()) > 100,
                                    f"Chapter {c['id']} section '{sec}' is too short or empty ({len(content)} chars)")

        self.assertEqual(total_treatises, 38, "Must have exactly 38 enriched treatises")

    def test_14_get_chapter_treatise_api_helper(self):
        """Verifies get_chapter_treatise helper function across volumes."""
        tr_01 = get_chapter_treatise("ch-01-01")
        self.assertIsNotNone(tr_01)
        self.assertIn("Arkan", tr_01["chapter_title_en"])
        self.assertIn("Ibn Sina", tr_01["canonical_philosophy_and_doctrine"])
        self.assertIn("mitochondrial", tr_01["molecular_and_cellular_pathophysiology"].lower())

        tr_12 = get_chapter_treatise("ch-12-01")
        self.assertIsNotNone(tr_12)
        self.assertIn("CYP450", tr_12["chapter_title_en"])
        self.assertIn("Warfarin", tr_12["molecular_and_cellular_pathophysiology"])

    def test_15_mufradat_materia_medica_completeness(self):
        """Verifies canonical Mufradat monographs with Mizaj, Afaal, Musleh, Badal, and Tadbeer."""
        mufradat = get_all_mufradat()
        self.assertGreaterEqual(len(mufradat), 250, "Must have at least 250 canonical Mufradat monographs")

        # Test lookup by ID
        asgandh = get_mufrad_by_id("ZMF-001")
        self.assertIsNotNone(asgandh)
        self.assertEqual(asgandh["name"].upper(), "ASGANDH")
        self.assertIn("Withania", asgandh["botanical"])
        self.assertTrue(asgandh["musleh"])
        self.assertTrue(asgandh["badal"])
        self.assertTrue(asgandh["tadbeer"])

        # Test high-risk / schedule E-1
        suranjan = get_mufrad_by_id("ZMF-002")
        self.assertIsNotNone(suranjan)
        self.assertTrue(suranjan["schedule_e1"])
        self.assertTrue(suranjan["high_risk"])

        # Test search
        res = search_mufradat("Asgandh")
        self.assertGreaterEqual(len(res), 1)
        self.assertEqual(res[0]["id"], "ZMF-001")

    def test_16_murakkabat_classical_formulary_completeness(self):
        """Verifies classical compound formulations with authentic recipe ingredients and indications."""
        murakkabat = get_all_murakkabat()
        self.assertGreaterEqual(len(murakkabat), 50, "Must have at least 50 classical compound recipes")

        itrifal = get_murakkab_by_id("nfum-itrifal-kishneezi")
        self.assertIsNotNone(itrifal)
        self.assertEqual(itrifal["name"], "Itrifal Kishneezi")
        self.assertIn("Bayaz-e-Kabir", itrifal["classical_source"])
        self.assertGreater(len(itrifal["key_ingredients"]), 3)

        res = search_murakkabat("Kishneezi")
        self.assertGreaterEqual(len(res), 1)

    def test_17_cyp450_drug_herb_interactions_completeness(self):
        """Verifies master CYP450 drug-herb interaction registry."""
        interactions = get_all_drug_interactions()
        self.assertGreaterEqual(len(interactions), 10, "Must have at least 10 master interaction alerts")

        res = search_drug_interactions("Warfarin")
        self.assertGreaterEqual(len(res), 1)
        self.assertEqual(res[0]["severity"], "CRITICAL")

    def test_18_multilingual_search(self):
        """Verifies searching across Urdu script, English, and botanical terms."""
        res_urdu = search_mufradat("اسگندھ")
        self.assertGreaterEqual(len(res_urdu), 1)

        res_botanical = search_mufradat("Withania")
        self.assertGreaterEqual(len(res_botanical), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

