import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.knowledge.app.core.standard_unani_terminology import (
    StandardUnaniTerminologyEngine,
    get_terminology_engine
)
from services.knowledge.app.data.grand_medical_books_corpus import (
    get_all_medical_books_in_corpus,
    search_corpus,
    get_corpus_categories_summary,
    GRAND_MEDICAL_BOOKS_CORPUS
)

class TestStandardUnaniTerminology(unittest.TestCase):
    def setUp(self):
        self.engine = get_terminology_engine()


    def test_engine_initialization_and_count(self):
        self.assertIsNotNone(self.engine)
        self.assertGreaterEqual(len(self.engine.terms), 1500)
        stats = self.engine.get_statistics()
        self.assertIn("total_terms", stats)
        self.assertGreaterEqual(stats["total_terms"], 1500)
        self.assertEqual(stats["statutory_authority"], "CCRUM / Ministry of AYUSH, Government of India")

    def test_get_term_by_code(self):
        term_0002 = self.engine.get_term_by_code("UMA-0002")
        self.assertIsNotNone(term_0002)
        self.assertEqual(term_0002["uma_code"], "UMA-0002")
        self.assertIn("Shaqiqa", term_0002["unani_term"])
        self.assertIn("migraine", term_0002["english_equivalent"].lower())

        term_1640 = self.engine.get_term_by_code("UMA-1640")
        self.assertIsNotNone(term_1640)
        self.assertIn("peritonitis", term_1640["english_equivalent"].lower())

    def test_code_lookup_normalization(self):
        # Case insensitive and number-only fallback
        t1 = self.engine.get_term_by_code("uma-0002")
        self.assertIsNotNone(t1)
        self.assertEqual(t1["uma_code"], "UMA-0002")

        t2 = self.engine.get_term_by_code("2")
        self.assertIsNotNone(t2)
        self.assertEqual(t2["uma_code"], "UMA-0002")

    def test_biomedical_reverse_lookup(self):
        matches = self.engine.lookup_biomedical_to_unani("migraine")
        self.assertTrue(len(matches) >= 1)
        codes = [m["uma_code"] for m in matches]
        self.assertIn("UMA-0002", codes)

    def test_unani_to_biomedical_lookup(self):
        matches = self.engine.lookup_unani_to_biomedical("Shaqiqa")
        self.assertTrue(len(matches) >= 1)
        self.assertTrue(any("migraine" in m["english_equivalent"].lower() for m in matches))

    def test_search_terms(self):
        hernia_results = self.engine.search_terms("hernia", limit=10)
        self.assertTrue(len(hernia_results) > 0)
        # Check that top results mention hernia or Fatq
        top_match = hernia_results[0]
        self.assertTrue("hernia" in top_match["english_equivalent"].lower() or "fatq" in top_match["unani_term"].lower() or "hernia" in top_match["definition"].lower())

    def test_nonexistent_code(self):
        res = self.engine.get_term_by_code("UMA-99999")
        self.assertIsNone(res)

class TestGrandMedicalBooksCorpus(unittest.TestCase):
    def test_corpus_count_and_integrity(self):
        books = get_all_medical_books_in_corpus()
        self.assertEqual(len(books), 97)
        ids = [b["id"] for b in books]
        self.assertEqual(len(ids), len(set(ids)), "All 97 book IDs must be strictly unique")
        filenames = [b["filename"] for b in books]
        self.assertEqual(len(filenames), len(set(filenames)), "All 97 filenames must be strictly unique")
        for b in books:
            self.assertIn("id", b)
            self.assertIn("title", b)
            self.assertIn("author", b)
            self.assertIn("category", b)
            self.assertIn("discipline", b)
            self.assertIn("file_size_mb", b)

    def test_search_corpus(self):
        razi_books = search_corpus("Razi")
        self.assertTrue(len(razi_books) >= 5)
        self.assertTrue(any("Hawi" in b["title"] for b in razi_books))

        sina_books = search_corpus("Ibn Sina")
        self.assertTrue(len(sina_books) >= 4)
        self.assertTrue(any("Qanun" in b["title"] for b in sina_books))

        modern_books = search_corpus("Harrison")
        self.assertTrue(len(modern_books) >= 3)

        robbins_books = search_corpus("Robbins")
        self.assertEqual(len(robbins_books), 1)

        bailey_books = search_corpus("Bailey & Love")
        self.assertEqual(len(bailey_books), 1)

        zahrawi_books = search_corpus("Zahrawi")
        self.assertEqual(len(zahrawi_books), 1)

        who_books = search_corpus("WHO")
        self.assertEqual(len(who_books), 1)

    def test_categories_summary(self):
        summary = get_corpus_categories_summary()
        self.assertIn("total_books", summary)
        self.assertEqual(summary["total_books"], 97)
        self.assertIn("categories_breakdown", summary)
        categories = summary["categories_breakdown"]
        self.assertIn("Classical Canon", categories)
        self.assertIn("Clinical Diagnostics", categories)
        self.assertIn("Materia Medica", categories)
        self.assertIn("Pharmacopoeia & Formulary", categories)
        self.assertIn("Modern Biomedical Medicine", categories)
        self.assertIn("Regimenal Therapy & Surgery", categories)
        self.assertIn("Pharmacopoeias & Statutory Standards", categories)
        self.assertEqual(len(categories), 7)


if __name__ == "__main__":
    unittest.main()
