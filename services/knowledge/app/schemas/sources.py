"""
ZAYVORA Knowledge Base (ZKB) — Pydantic Schemas for Source Library & Provenance
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AuthorCreate(BaseModel):
    canonical_name: str
    arabic_name: Optional[str] = None
    persian_name: Optional[str] = None
    urdu_name: Optional[str] = None
    era_hijri: Optional[str] = None
    era_ce: Optional[str] = None
    biography_summary: Optional[str] = None
    is_classical: bool = True


class AuthorResponse(AuthorCreate):
    id: str
    created_at: str
    updated_at: str


class BookCreate(BaseModel):
    primary_author_id: Optional[str] = None
    canonical_title: str
    original_title: str
    transliterated_title: Optional[str] = None
    language_code: str
    discipline: str
    historical_era: Optional[str] = None
    source_type: str = "CLASSICAL_TREATISE"
    description: Optional[str] = None


class BookResponse(BookCreate):
    id: str
    created_at: str
    updated_at: str


class EditionCreate(BaseModel):
    book_id: str
    editor_translator: Optional[str] = None
    publisher: str
    publication_year: int
    publication_place: Optional[str] = None
    edition_number: Optional[str] = None
    volume_number: Optional[str] = None
    isbn_issn: Optional[str] = None
    total_pages: int = 0
    call_number: Optional[str] = None
    digital_scan_url: Optional[str] = None
    sha256_checksum: Optional[str] = None


class EditionResponse(EditionCreate):
    id: str
    sha256_checksum: str
    created_at: str
    updated_at: str


class RightsCreate(BaseModel):
    rights_status: str = "unknown"
    clinical_access: str = "research_only"
    license_type: str = "PUBLIC_DOMAIN"
    rights_holder: Optional[str] = None
    licensed_to_facility: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    commercial_use_permitted: bool = False
    ai_training_permitted: bool = False
    verified_by_legal_officer: Optional[str] = None


class RightsResponse(RightsCreate):
    id: str
    edition_id: str
    verified_at: Optional[str] = None
    created_at: str


class PageCreate(BaseModel):
    page_number: int
    folio_recto_verso: Optional[str] = None
    image_storage_uri: str
    image_mime_type: str = "image/tiff"
    width_px: int = 0
    height_px: int = 0
    dpi: int = 300
    sha256_page_hash: str


class PageResponse(PageCreate):
    id: str
    edition_id: str
    created_at: str


class PassageCreate(BaseModel):
    passage_order: int = 1
    chapter: Optional[str] = None
    section: Optional[str] = None
    original_text: str
    normalized_text: Optional[str] = None
    script_code: str = "arab"
    bounding_box: Optional[Dict[str, float]] = None
    is_verse: bool = False
    is_recipe: bool = False
    is_margin_note: bool = False


class PassageResponse(PassageCreate):
    id: str
    page_id: str
    created_at: str


class TranslationCreate(BaseModel):
    target_language: str
    translated_text: str
    translator_type: str = "HUMAN_EXPERT"
    translator_name: Optional[str] = None
    translation_notes: Optional[str] = None
    is_canonical: bool = True


class TranslationResponse(TranslationCreate):
    id: str
    passage_id: str
    created_at: str


class SourceSearchRequest(BaseModel):
    query: str = ""
    filters: Optional[Dict[str, Any]] = None


class ProvenanceResponse(BaseModel):
    provenance_verified: bool
    passage_id: str
    original_text: str
    script_code: str
    bounding_box: Optional[Dict[str, float]] = None
    page: Dict[str, Any]
    edition: Dict[str, Any]
    book: Dict[str, Any]
    author: Dict[str, Any]
    rights: Dict[str, Any]
    translations: List[Dict[str, Any]]
    citation_string: str
