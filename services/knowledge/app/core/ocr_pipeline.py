"""
ZAYVORA Knowledge Base (ZKB) — Multilingual OCR & Knowledge Extraction Engine
Supports Arabic, Urdu Nastaliq, Persian, Hindi, English, Right-to-Left (RTL) handling,
Confidence Scoring, Scholarly Human Correction Desk, and Clinical Entity Recognition.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

CONFIDENCE_ACCEPTANCE_THRESHOLD = 0.95

# Classical Unani entity patterns for structured extraction
UNANI_ENTITIES_LEXICON = {
    "mufradat": [
        "asgandh", "suranjan", "suranjan talkh", "kuchla", "azaraqi", "filfil siyah",
        "ustukhuddus", "zafran", "gawzaban", "bhang", "afeem", "senna", "mulethi",
        "kishneez", "kaloanji", "hilteet", "turbud", "badiyan", "karanjwa"
    ],
    "mizaj_qualities": [
        "hot & dry", "hot and dry", "cold & moist", "cold and moist",
        "hot & moist", "cold & dry", "garam khushk", "sard tar", "garam tar", "sard khushk",
        "har yabis", "barid ratab", "har ratab", "barid yabis"
    ],
    "afaal_actions": [
        "muqawwi", "muqawwi-e-aam", "muqawwi-e-dimagh", "muqawwi-e-qalb",
        "muhallil", "musakkin", "munaffis", "mudirr", "mufattih",
        "kasir-e-riyah", "qabiz", "dafe-taffun", "muharrik"
    ],
}


def detect_script_and_language(text: str) -> Tuple[str, str]:
    """Identify script family and language from textual tokens."""
    arabic_persian_urdu_chars = len(re.findall(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]", text))
    devanagari_chars = len(re.findall(r"[\u0900-\u097F]", text))
    latin_chars = len(re.findall(r"[a-zA-Z]", text))

    total = arabic_persian_urdu_chars + devanagari_chars + latin_chars
    if total == 0:
        return "latn", "en"

    if arabic_persian_urdu_chars > devanagari_chars and arabic_persian_urdu_chars > latin_chars:
        # Check for specific Urdu Nastaliq characters (ٹ، ڈ، ڑ، ں، ے، ہ)
        if re.search(r"[\u0679\u0688\u0691\u06BA\u06D2\u06C1]", text):
            return "nastaliq", "ur"
        # Check for Persian specific characters (پ، چ، ژ، گ)
        elif re.search(r"[\u067E\u0686\u0698\u06AF]", text):
            return "farsi", "fa"
        else:
            return "arab", "ar"
    elif devanagari_chars > latin_chars:
        return "deva", "hi"
    else:
        return "latn", "en"


class OcrPipelineEngine:
    """Manages OCR jobs, text segmentation, confidence scoring, and human corrections."""

    def __init__(self):
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.segments: Dict[str, Dict[str, Any]] = {}
        self.corrections: Dict[str, Dict[str, Any]] = {}
        self.extractions: Dict[str, Dict[str, Any]] = {}

    def submit_ocr_job(
        self,
        edition_id: str,
        engine_name: str = "Tesseract-Urdu-Arabic-v5.3",
        target_scripts: Optional[List[str]] = None,
        raw_text_pages: Optional[Dict[int, str]] = None,
    ) -> Dict[str, Any]:
        """Submit a document OCR extraction job."""
        job_id = f"ocr-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        scripts = target_scripts or ["arab", "nastaliq", "latn"]

        doc = {
            "id": job_id,
            "edition_id": edition_id,
            "engine_name": engine_name,
            "engine_version": "5.3.0-unani-multilingual",
            "status": "PROCESSING",
            "target_scripts": scripts,
            "overall_confidence": 0.0,
            "total_pages_processed": 0,
            "needs_review_count": 0,
            "started_at": now,
            "completed_at": None,
            "created_at": now,
        }
        self.documents[job_id] = doc

        # If raw text pages are provided, process segments immediately
        if raw_text_pages:
            self._process_simulated_ocr(job_id, edition_id, raw_text_pages)

        return doc

    def _process_simulated_ocr(self, job_id: str, edition_id: str, pages_dict: Dict[int, str]) -> None:
        total_conf = 0.0
        segment_count = 0
        needs_review_count = 0

        for page_num, raw_content in pages_dict.items():
            lines = [ln.strip() for ln in raw_content.splitlines() if ln.strip()]
            for idx, line in enumerate(lines, start=1):
                script, lang = detect_script_and_language(line)

                # Simulated OCR noise & confidence calculation
                # Lines with obscure or non-dictionary tokens receive lower confidence
                if "~" in line or "?" in line or len(line) < 5:
                    confidence = 0.82
                else:
                    confidence = 0.98

                needs_review = confidence < CONFIDENCE_ACCEPTANCE_THRESHOLD
                if needs_review:
                    needs_review_count += 1

                seg_id = f"seg-{uuid.uuid4().hex[:8]}"
                segment = {
                    "id": seg_id,
                    "ocr_document_id": job_id,
                    "page_id": f"page-{edition_id}-{page_num}",
                    "line_number": idx,
                    "detected_script": script,
                    "detected_language": lang,
                    "segment_text": line,
                    "confidence": confidence,
                    "bounding_polygon": {
                        "p1": [0.1, 0.1 * idx],
                        "p2": [0.9, 0.1 * idx],
                        "p3": [0.9, 0.1 * idx + 0.05],
                        "p4": [0.1, 0.1 * idx + 0.05],
                    },
                    "needs_review": needs_review,
                    "is_corrected": False,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
                self.segments[seg_id] = segment
                total_conf += confidence
                segment_count += 1

        doc = self.documents[job_id]
        doc["status"] = "COMPLETED"
        doc["total_pages_processed"] = len(pages_dict)
        doc["needs_review_count"] = needs_review_count
        doc["overall_confidence"] = round(total_conf / max(1, segment_count), 3)
        doc["completed_at"] = datetime.now(timezone.utc).isoformat()

    def get_ocr_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.documents.get(job_id)

    def get_segments_by_job(self, job_id: str) -> List[Dict[str, Any]]:
        return [s for s in self.segments.values() if s["ocr_document_id"] == job_id]

    def get_needs_review_segments(self, job_id: Optional[str] = None) -> List[Dict[str, Any]]:
        segs = [s for s in self.segments.values() if s["needs_review"] and not s["is_corrected"]]
        if job_id:
            segs = [s for s in segs if s["ocr_document_id"] == job_id]
        return segs

    # ------------------------------------------------------------------------
    # HUMAN CORRECTION WORKFLOW
    # ------------------------------------------------------------------------
    def submit_correction(
        self,
        segment_id: str,
        corrected_text: str,
        reviewer_id: str,
        reviewer_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Human-in-the-loop scholar correction of OCR text."""
        segment = self.segments.get(segment_id)
        if not segment:
            raise ValueError(f"OCR Segment {segment_id} not found.")

        correction_id = f"corr-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        correction = {
            "id": correction_id,
            "segment_id": segment_id,
            "original_ocr_text": segment["segment_text"],
            "corrected_text": corrected_text,
            "reviewer_user_id": reviewer_id,
            "reviewer_name": reviewer_name or "Scholarly Reviewer",
            "correction_notes": notes or "",
            "reviewed_at": now,
        }
        self.corrections[correction_id] = correction

        # Update segment
        segment["segment_text"] = corrected_text
        segment["is_corrected"] = True
        segment["needs_review"] = False
        segment["confidence"] = 1.000  # Expert-verified

        return correction

    # ------------------------------------------------------------------------
    # STRUCTURED CLINICAL KNOWLEDGE EXTRACTION
    # ------------------------------------------------------------------------
    def extract_clinical_entities(self, passage_id: str, passage_text: str) -> Dict[str, Any]:
        """Parses medical entities from passage text into structured representations."""
        text_lower = passage_text.lower()

        extracted = {
            "mufradat": [],
            "mizaj": [],
            "afaal": [],
            "doses": [],
            "warnings": [],
        }

        # Match single drugs
        for herb in UNANI_ENTITIES_LEXICON["mufradat"]:
            if herb in text_lower:
                extracted["mufradat"].append(herb.title())

        # Match Mizaj
        for mizaj in UNANI_ENTITIES_LEXICON["mizaj_qualities"]:
            if mizaj in text_lower:
                extracted["mizaj"].append(mizaj.title())

        # Match actions
        for act in UNANI_ENTITIES_LEXICON["afaal_actions"]:
            if act in text_lower:
                extracted["afaal"].append(act.title())

        # Extract dosage patterns (e.g. "3 to 6 g", "500 mg", "1 masha")
        dose_matches = re.findall(r"\b\d+(?:\s*(?:to|-)\s*\d+)?\s*(?:g|grams?|mg|masha|ratti)\b", text_lower)
        extracted["doses"] = list(set(dose_matches))

        # Toxic / warning check
        if any(term in text_lower for term in ["schedule e(1)", "poison", "toxic", "mudabbar", "contraindicated"]):
            extracted["warnings"].append("Statutory or toxicological caution flag detected.")

        confidence = 0.95 if (extracted["mufradat"] or extracted["mizaj"]) else 0.70
        ext_id = f"ext-{uuid.uuid4().hex[:8]}"

        record = {
            "id": ext_id,
            "passage_id": passage_id,
            "extracted_entities": extracted,
            "extraction_confidence": confidence,
            "extraction_method": "CANONICAL_UNANI_LEXICAL_NER",
            "review_status": "EXPERT_REVIEW_PENDING",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.extractions[ext_id] = record
        return record


_GLOBAL_OCR_PIPELINE: Optional[OcrPipelineEngine] = None

def get_ocr_pipeline() -> OcrPipelineEngine:
    global _GLOBAL_OCR_PIPELINE
    if _GLOBAL_OCR_PIPELINE is None:
        _GLOBAL_OCR_PIPELINE = OcrPipelineEngine()
    return _GLOBAL_OCR_PIPELINE
