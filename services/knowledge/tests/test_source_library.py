"""
ZAYVORA Knowledge Base (ZKB) — Source Library & Provenance Test Suite (Phase 2)
Verifies Source Registry, Rights Governance, Scan Ingestion, Bounding Boxes,
Translations, and Complete Cryptographic Provenance Chains.
"""
from __future__ import annotations

import hashlib
import os
import tempfile
from app.core.source_registry import SourceRegistry, get_source_registry


def test_canonical_source_authors_and_books():
    """Verify pre-seeded foundational treatises and official pharmacopoeias."""
    registry = get_source_registry()

    # Verify canonical authors
    authors = registry.get_authors()
    assert len(authors) >= 3
    author_names = [a["canonical_name"] for a in authors]
    assert any("Avicenna" in name for name in author_names)
    assert any("Rhazes" in name for name in author_names)
    assert any("AYUSH" in name for name in author_names)

    # Verify canonical books
    books = registry.get_books()
    assert len(books) >= 2
    titles = [b["canonical_title"] for b in books]
    assert any("Al-Qanun" in t for t in titles)
    assert any("Unani Pharmacopoeia of India" in t for t in titles)


def test_author_and_book_registration():
    """Verify registration and search of classical Unani works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SourceRegistry(storage_dir=tmpdir)

        author = registry.register_author({
            "canonical_name": "Ismail Jurjani",
            "arabic_name": "إسماعيل الجرجاني",
            "persian_name": "سید اسماعیل جرجانی",
            "era_ce": "1042–1137 CE",
            "biography_summary": "Eminent Persian physician and author of Zakhira-i Khwarizmshahi.",
            "is_classical": True,
        })
        assert author["id"].startswith("aut-")

        book = registry.register_book({
            "primary_author_id": author["id"],
            "canonical_title": "Zakhira-i Khwarizmshahi (The Treasury of Khwarizmshah)",
            "original_title": "ذخیره خوارزمشاهی",
            "language_code": "fa",
            "discipline": "Moalajat & Kulliyat",
            "historical_era": "12th Century CE",
            "source_type": "CLASSICAL_TREATISE",
        })
        assert book["id"].startswith("book-")

        # Test search
        found_books = registry.get_books(search="Khwarizmshah")
        assert len(found_books) == 1
        assert found_books[0]["canonical_title"] == book["canonical_title"]

        # Test filter by language
        persian_books = registry.get_books(language="fa")
        assert len(persian_books) >= 1
        assert any(b["canonical_title"] == book["canonical_title"] for b in persian_books)


def test_edition_registration_and_checksum():
    """Verify edition registration and cryptographic SHA-256 verification."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SourceRegistry(storage_dir=tmpdir)
        books = registry.get_books()
        qanun = [b for b in books if "Al-Qanun" in b["canonical_title"]][0]

        edition = registry.register_edition({
            "book_id": qanun["id"],
            "publisher": "Naval Kishore Press",
            "publication_year": 1895,
            "publication_place": "Lucknow, India",
            "volume_number": "Vol 1",
            "total_pages": 520,
        })
        assert edition["id"].startswith("ed-")
        assert len(edition["sha256_checksum"]) == 64

        retrieved = registry.get_edition_by_id(edition["id"])
        assert retrieved is not None
        assert retrieved["publisher"] == "Naval Kishore Press"


def test_rights_governance_and_safety_gate():
    """Verify legal rights management and automatic safety gate enforcement."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SourceRegistry(storage_dir=tmpdir)
        editions = list(registry.editions.values())
        ed = editions[0]

        # 1. Set verified public domain
        r1 = registry.set_rights_record(ed["id"], {
            "rights_status": "verified_public_domain",
            "clinical_access": "clinically_approved",
            "license_type": "PUBLIC_DOMAIN",
            "commercial_use_permitted": True,
            "ai_training_permitted": True,
            "verified_by_legal_officer": "Legal Counsel A",
        })
        assert r1["rights_status"] == "verified_public_domain"
        assert r1["clinical_access"] == "clinically_approved"
        assert r1["ai_training_permitted"] is True

        # 2. Safety Gate: Rejected rights MUST automatically force clinical_access to 'blocked'
        r2 = registry.set_rights_record(ed["id"], {
            "rights_status": "rejected",
            "clinical_access": "clinically_approved",  # Attacker attempts to allow access
            "license_type": "COPYRIGHT_INFRINGING",
        })
        assert r2["rights_status"] == "rejected"
        assert r2["clinical_access"] == "blocked"  # Gatekeeper enforced blocked


def test_high_res_scan_ingestion_and_sha256_hashing():
    """Verify multipart file ingestion, size guardrails, and SHA-256 digest."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SourceRegistry(storage_dir=tmpdir)
        editions = list(registry.editions.values())
        ed = editions[0]

        # Ingest synthetic 300DPI TIFF page scan
        mock_tiff_bytes = b"II*\x00\x08\x00\x00\x00ZAYVORA_AUTHENTIC_SCAN_PAYLOAD_BYTE_STREAM_TEST"
        expected_sha = hashlib.sha256(mock_tiff_bytes).hexdigest()

        page = registry.ingest_scan_file(
            edition_id=ed["id"],
            page_number=42,
            file_bytes=mock_tiff_bytes,
            filename="manuscript_folio_42.tiff",
            dpi=300,
            folio="42a",
        )

        assert page["page_number"] == 42
        assert page["sha256_page_hash"] == expected_sha
        assert page["image_mime_type"] == "image/tiff"
        assert os.path.exists(page["image_storage_uri"])

        # Verify empty file rejection
        try:
            registry.ingest_scan_file(ed["id"], 43, b"", "empty.tiff")
            assert False, "Should have rejected empty file"
        except ValueError as e:
            assert "empty" in str(e).lower()

        # Verify invalid extension rejection
        try:
            registry.ingest_scan_file(ed["id"], 43, b"data", "malicious.exe")
            assert False, "Should have rejected invalid extension"
        except ValueError as e:
            assert "unsupported file format" in str(e).lower()


def test_passage_segmentation_with_bounding_boxes():
    """Verify coordinate bounding boxes and passage metadata extraction."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SourceRegistry(storage_dir=tmpdir)
        ed = list(registry.editions.values())[0]

        page = registry.add_page(ed["id"], {
            "page_number": 100,
            "image_storage_uri": "uploads/sources/test_p100.tiff",
            "sha256_page_hash": "a" * 64,
        })

        passage = registry.add_passage(page["id"], {
            "passage_order": 1,
            "chapter": "Maqala 1",
            "section": "Dar Bayan-e-Mizaj",
            "original_text": "المزاج كيفية حاصلة من تفاعل الكيفيات المتضادة",
            "normalized_text": "المزاج كيفية حاصلة من تفاعل الكيفيات المتضادة",
            "script_code": "arab",
            "bounding_box": {"x_min": 0.12, "y_min": 0.20, "x_max": 0.88, "y_max": 0.35},
            "is_recipe": False,
        })

        assert passage["script_code"] == "arab"
        assert passage["bounding_box"]["x_min"] == 0.12

        # Verify coordinate boundary validation
        try:
            registry.add_passage(page["id"], {
                "original_text": "Invalid coords",
                "bounding_box": {"x_min": -0.5, "y_min": 0.0, "x_max": 1.5, "y_max": 1.0},
            })
            assert False, "Should have rejected coordinates outside 0.0 to 1.0"
        except ValueError as e:
            assert "between 0.0 and 1.0" in str(e)


def test_multilingual_scholarly_translations():
    """Verify attaching bilingual translations to classical passages."""
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = SourceRegistry(storage_dir=tmpdir)
        passages = list(registry.passages.values())
        pas = passages[0]

        trans = registry.add_translation(pas["id"], {
            "target_language": "en",
            "translated_text": "Ashwagandha / Asgandh is a potent adaptogen that strengthens vital organs.",
            "translator_type": "HUMAN_EXPERT",
            "translator_name": "Dr. A. Qadir, MD (Unani)",
            "is_canonical": True,
        })

        assert trans["target_language"] == "en"
        trans_list = registry.get_translations_by_passage(pas["id"])
        assert len(trans_list) >= 1


def test_complete_cryptographic_provenance_chain():
    """Verify unbroken chain tracing from passage back to edition, book, author, and rights."""
    registry = get_source_registry()
    asgandh_passage = registry.passages.get("pas-upi-asgandh-01")
    assert asgandh_passage is not None

    provenance = registry.get_passage_provenance("pas-upi-asgandh-01")
    assert provenance["provenance_verified"] is True
    assert provenance["page"]["page_number"] == 15
    assert len(provenance["page"]["sha256_page_hash"]) == 64
    assert provenance["edition"]["publisher"] == "Ministry of Health and Family Welfare, Govt. of India"
    assert "Unani Pharmacopoeia of India" in provenance["book"]["canonical_title"]
    assert "AYUSH" in provenance["author"]["canonical_name"]
    assert provenance["rights"]["rights_status"] == "licensed"
    assert provenance["rights"]["clinical_access"] == "clinically_approved"
    assert len(provenance["translations"]) >= 1
    assert "Page 15" in provenance["citation_string"]


def test_source_multi_field_search():
    """Verify source search by query string and metadata filters."""
    registry = get_source_registry()

    # 1. Search by Arabic title
    res1 = registry.search_sources("القانون")
    assert len(res1) >= 1
    assert "Al-Qanun" in res1[0]["book"]["canonical_title"]

    # 2. Search by discipline filter
    res2 = registry.search_sources("", filters={"discipline": "Mufradat"})
    assert len(res2) >= 1
    assert any("Pharmacopoeia" in r["book"]["canonical_title"] for r in res2)

    # 3. Search by language
    res3 = registry.search_sources("", filters={"language": "ar"})
    assert len(res3) >= 1
    assert res3[0]["book"]["language_code"] == "ar"
