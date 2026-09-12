"""
ZAYVORA HEALTH™ — Knowledge Search Router
Provides endpoints for Global Command Center (Cmd+K) omni-search.
"""

from fastapi import APIRouter, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from ..core.command_search import CommandSearchEngine, SearchResultItem

router = APIRouter(prefix="/api/v1/knowledge/search", tags=["Global Omni-Search"])


@router.get("/omni", summary="Unified cross-domain spotlight search")
async def omni_search(
    q: str = Query("", description="Search term across herbs, formulations, Amraz, ICD-11, and navigation"),
    limit: int = Query(20, ge=1, le=50, description="Max results to return"),
):
    items = CommandSearchEngine.search(q, limit=limit)
    return [
        {
            "id": it.id,
            "category": it.category,
            "title": it.title,
            "subtitle": it.subtitle,
            "badge": it.badge,
            "route": it.route,
            "metadata": it.metadata,
        }
        for it in items
    ]
