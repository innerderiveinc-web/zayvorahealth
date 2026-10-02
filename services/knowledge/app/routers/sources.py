"""
ZAYVORA Knowledge Base (ZKB) — Source Library & Provenance API Router
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from app.core.auth_dependency import CurrentUser, get_current_user
from app.core.source_registry import get_source_registry
from app.schemas.sources import (
    AuthorCreate,
    AuthorResponse,
    BookCreate,
    BookResponse,
    EditionCreate,
    EditionResponse,
    PageCreate,
    PageResponse,
    PassageCreate,
    PassageResponse,
    ProvenanceResponse,
    RightsCreate,
    RightsResponse,
    SourceSearchRequest,
    TranslationCreate,
    TranslationResponse,
)

router = APIRouter(prefix="/api/v1/zkb/sources", tags=["zkb-source-library"])


# ----------------------------------------------------------------------------
# 1. AUTHORS
# ----------------------------------------------------------------------------
@router.post("/authors", response_model=AuthorResponse)
def create_author(payload: AuthorCreate, user: CurrentUser = Depends(get_current_user)):
    registry = get_source_registry()
    author = registry.register_author(payload.model_dump())
    return author


@router.get("/authors", response_model=List[AuthorResponse])
def list_authors(query: Optional[str] = None):
    registry = get_source_registry()
    return registry.get_authors(query)


# ----------------------------------------------------------------------------
# 2. BOOKS
# ----------------------------------------------------------------------------
@router.post("/books", response_model=BookResponse)
def create_book(payload: BookCreate, user: CurrentUser = Depends(get_current_user)):
    registry = get_source_registry()
    book = registry.register_book(payload.model_dump())
    return book


@router.get("/books", response_model=List[BookResponse])
def list_books(
    discipline: Optional[str] = None,
    language: Optional[str] = None,
    search: Optional[str] = None,
):
    registry = get_source_registry()
    return registry.get_books(discipline=discipline, language=language, search=search)


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: str):
    registry = get_source_registry()
    book = registry.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Source book '{book_id}' not found")
    return book


# ----------------------------------------------------------------------------
# 3. EDITIONS
# ----------------------------------------------------------------------------
@router.post("/editions", response_model=EditionResponse)
def create_edition(payload: EditionCreate, user: CurrentUser = Depends(get_current_user)):
    registry = get_source_registry()
    try:
        edition = registry.register_edition(payload.model_dump())
        return edition
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/editions/{edition_id}", response_model=EditionResponse)
def get_edition(edition_id: str):
    registry = get_source_registry()
    edition = registry.get_edition_by_id(edition_id)
    if not edition:
        raise HTTPException(status_code=404, detail=f"Edition '{edition_id}' not found")
    return edition


# ----------------------------------------------------------------------------
# 4. RIGHTS GOVERNANCE
# ----------------------------------------------------------------------------
@router.post("/editions/{edition_id}/rights", response_model=RightsResponse)
def set_rights(
    edition_id: str,
    payload: RightsCreate,
    user: CurrentUser = Depends(get_current_user),
):
    registry = get_source_registry()
    try:
        data = payload.model_dump()
        # Automatically capture legal reviewer if not explicitly provided
        if not data.get("verified_by_legal_officer"):
            data["verified_by_legal_officer"] = f"Officer-{user.user_id[:8]}"
        record = registry.set_rights_record(edition_id, data)
        return record
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/editions/{edition_id}/rights", response_model=RightsResponse)
def get_rights(edition_id: str):
    registry = get_source_registry()
    record = registry.get_rights_record(edition_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"No rights record found for edition '{edition_id}'")
    return record


# ----------------------------------------------------------------------------
# 5. HIGH-RESOLUTION SCAN UPLOAD & INGESTION
# ----------------------------------------------------------------------------
@router.post("/editions/{edition_id}/pages/upload", response_model=PageResponse)
async def upload_page_scan(
    edition_id: str,
    page_number: int = Form(...),
    dpi: int = Form(300),
    folio: Optional[str] = Form(None),
    file: UploadFile = File(...),
    user: CurrentUser = Depends(get_current_user),
):
    registry = get_source_registry()
    file_bytes = await file.read()
    try:
        page = registry.ingest_scan_file(
            edition_id=edition_id,
            page_number=page_number,
            file_bytes=file_bytes,
            filename=file.filename or "scan.tiff",
            dpi=dpi,
            folio=folio,
        )
        return page
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/editions/{edition_id}/pages", response_model=PageResponse)
def create_page_metadata(
    edition_id: str,
    payload: PageCreate,
    user: CurrentUser = Depends(get_current_user),
):
    registry = get_source_registry()
    try:
        return registry.add_page(edition_id, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/editions/{edition_id}/pages", response_model=List[PageResponse])
def list_pages(edition_id: str):
    registry = get_source_registry()
    return registry.get_pages_by_edition(edition_id)


# ----------------------------------------------------------------------------
# 6. PASSAGES & TRANSLATIONS
# ----------------------------------------------------------------------------
@router.post("/pages/{page_id}/passages", response_model=PassageResponse)
def create_passage(
    page_id: str,
    payload: PassageCreate,
    user: CurrentUser = Depends(get_current_user),
):
    registry = get_source_registry()
    try:
        return registry.add_passage(page_id, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pages/{page_id}/passages", response_model=List[PassageResponse])
def list_passages(page_id: str):
    registry = get_source_registry()
    return registry.get_passages_by_page(page_id)


@router.post("/passages/{passage_id}/translations", response_model=TranslationResponse)
def add_translation(
    passage_id: str,
    payload: TranslationCreate,
    user: CurrentUser = Depends(get_current_user),
):
    registry = get_source_registry()
    try:
        return registry.add_translation(passage_id, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------------------------------------------------------
# 7. PROVENANCE CHAIN LOOKUP
# ----------------------------------------------------------------------------
@router.get("/passages/{passage_id}/provenance", response_model=ProvenanceResponse)
def get_provenance(passage_id: str):
    registry = get_source_registry()
    try:
        return registry.get_passage_provenance(passage_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ----------------------------------------------------------------------------
# 8. MULTI-FIELD SEARCH
# ----------------------------------------------------------------------------
@router.post("/search")
def search_sources(payload: SourceSearchRequest):
    registry = get_source_registry()
    results = registry.search_sources(query=payload.query, filters=payload.filters)
    return {"total": len(results), "results": results}
