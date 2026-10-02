"""
ZAYVORA Knowledge Base (ZKB) — OCR Pipeline & Extraction Test Suite (Phase 3)
Verifies Script/Language Detection, Page-level OCR, Confidence Scoring,
Human-in-the-loop Correction Desk, and Clinical Entity Extraction.
"""
from __future__ import annotations

from app.core.ocr_pipeline import (
    OcrPipelineEngine,
    detect_script_and_language,
    get_ocr_pipeline,
)


def test_detect_script_and_language():
    """Verify script and language classification for non-Latin medical literature."""
    # 1. Urdu Nastaliq with specific characters (ٹ، ڈ، ڑ، ے)
    urdu_text = "اسگندھ ایک مشہور دوا ہے جو ضعفِ باہ میں مفید ہے۔"
    script, lang = detect_script_and_language(urdu_text)
    assert script == "nastaliq"
    assert lang == "ur"

    # 2. Classical Arabic Naskh
    arabic_text = "المزاج كيفية حاصلة من تفاعل الكيفيات المتضادة في الأركان"
    script, lang = detect_script_and_language(arabic_text)
    assert script == "arab"
    assert lang == "ar"

    # 3. Persian Farsi with specific characters (چ، پ، گ)
    persian_text = "در علاج بیماریهای چشم و گوش با ادویه مفرد چاره ساز است"
    script, lang = detect_script_and_language(persian_text)
    assert script == "farsi"
    assert lang == "fa"

    # 4. Devanagari Hindi
    hindi_text = "अश्वगंधा एक प्रमुख बल्य रसायन औषधि है"
    script, lang = detect_script_and_language(hindi_text)
    assert script == "deva"
    assert lang == "hi"

    # 5. Latin English
    english_text = "Withania somnifera Dunal root exhibits potent adaptogenic activity."
    script, lang = detect_script_and_language(english_text)
    assert script == "latn"
    assert lang == "en"


def test_submit_ocr_job_and_processing():
    """Verify batch OCR job submission and segment generation."""
    pipeline = OcrPipelineEngine()

    pages = {
        1: (
            "ASGANDH (Withania somnifera Dunal)\n"
            "Mizaj: Hot 1st degree, Dry 1st degree.\n"
            "Dose: 3 to 6 g powder."
        ),
        2: (
            "SURANJAN TALKH (Colchicum luteum Baker)\n"
            "Statutory Warning: Schedule E(1) Poison. Mandatory Mudabbar required.\n"
            "Dose: 250 mg maximum single dose."
        ),
    }

    job = pipeline.submit_ocr_job(
        edition_id="ed-upi-vol1-2007",
        engine_name="Tesseract-Urdu-Arabic-v5.3",
        target_scripts=["latn", "arab"],
        raw_text_pages=pages,
    )

    assert job["status"] == "COMPLETED"
    assert job["total_pages_processed"] == 2
    assert job["overall_confidence"] > 0.90

    segments = pipeline.get_segments_by_job(job["id"])
    assert len(segments) == 6


def test_ocr_confidence_scoring_and_needs_review_flag():
    """Verify confidence calculation and routing degraded text to review queue."""
    pipeline = OcrPipelineEngine()

    # Page 1 contains clear text; Page 2 contains degraded/noisy OCR tokens (~ or ?)
    pages = {
        1: "Clear pharmacopoeial text with canonical terminology.",
        2: "Degraded manuscript ~? illegible marginalia glyph ~??",
    }

    job = pipeline.submit_ocr_job(
        edition_id="ed-qanun-bulaq-1877",
        engine_name="Tesseract-Urdu-Arabic-v5.3",
        raw_text_pages=pages,
    )

    review_queue = pipeline.get_needs_review_segments(job["id"])
    assert len(review_queue) == 1
    flagged_segment = review_queue[0]
    assert flagged_segment["needs_review"] is True
    assert flagged_segment["confidence"] < 0.95
    assert "Degraded manuscript" in flagged_segment["segment_text"]


def test_scholarly_human_correction_desk():
    """Verify scholar correction workflow and audit record creation."""
    pipeline = OcrPipelineEngine()

    pages = {
        1: "Uncorrected error: Asgndh is ~? unani root",
    }

    job = pipeline.submit_ocr_job(edition_id="ed-test-01", raw_text_pages=pages)
    segments = pipeline.get_segments_by_job(job["id"])
    seg = segments[0]
    assert seg["needs_review"] is True

    # Scholar submits correction
    correction = pipeline.submit_correction(
        segment_id=seg["id"],
        corrected_text="Corrected: Asgandh is canonical Unani root",
        reviewer_id="usr-scholar-mansoor",
        reviewer_name="Dr. Hakim Mansoor Alam",
        notes="Corrected erroneous OCR glyph to 'canonical'.",
    )

    assert correction["segment_id"] == seg["id"]
    assert correction["original_ocr_text"] == "Uncorrected error: Asgndh is ~? unani root"
    assert correction["corrected_text"] == "Corrected: Asgandh is canonical Unani root"

    # Verify segment was updated
    assert seg["is_corrected"] is True
    assert seg["needs_review"] is False
    assert seg["confidence"] == 1.000
    assert seg["segment_text"] == "Corrected: Asgandh is canonical Unani root"

    # Verify review queue is now empty
    remaining_queue = pipeline.get_needs_review_segments(job["id"])
    assert len(remaining_queue) == 0


def test_clinical_entity_extraction():
    """Verify structured parsing of Mufradat, Mizaj, Af'al, doses, and safety warnings."""
    pipeline = get_ocr_pipeline()

    passage_text = (
        "Asgandh (Withania somnifera) has temperament Hot & Dry in 1st degree. "
        "It acts as Muqawwi-e-Aam and Musakkin. Dose: 3 to 6 g daily. "
        "Caution: Schedule E(1) poison rules do not apply, but pregnant women should avoid."
    )

    extraction = pipeline.extract_clinical_entities("pas-upi-asgandh-01", passage_text)
    entities = extraction["extracted_entities"]

    assert "Asgandh" in entities["mufradat"]
    assert any("Hot & Dry" in m for m in entities["mizaj"])
    assert any("Muqawwi-E-Aam" in a for a in entities["afaal"])
    assert any("3 to 6 g" in d for d in entities["doses"])
    assert len(entities["warnings"]) >= 1
    assert extraction["extraction_confidence"] >= 0.90
    assert extraction["review_status"] == "EXPERT_REVIEW_PENDING"
