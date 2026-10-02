"""
Qdrant Vector Store Client for ZAYVORA AI Service.

Handles embedding storage and semantic search for the knowledge base,
clinical notes, and Unani formulary documents.
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class VectorStoreError(Exception):
    pass


class QdrantVectorStore:
    """Client for Qdrant vector database."""

    def __init__(
        self,
        url: str = "",
        api_key: str = "",
        collection_name: str = "zayvora_knowledge",
    ) -> None:
        self.url = url or os.environ.get("QDRANT_URL", "http://localhost:6333")
        self.api_key = api_key or os.environ.get("QDRANT_API_KEY", "")
        self.collection_name = collection_name or os.environ.get("QDRANT_COLLECTION", "zayvora_knowledge")
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            from qdrant_client import QdrantClient
            kwargs: dict[str, Any] = {"url": self.url}
            if self.api_key:
                kwargs["api_key"] = self.api_key
            self._client = QdrantClient(**kwargs)
        return self._client

    def create_collection(self, vector_size: int = 1536) -> bool:
        """Create the collection if it does not exist (idempotent)."""
        from qdrant_client.models import Distance, VectorParams
        client = self._get_client()
        try:
            existing = [c.name for c in client.get_collections().collections]
            if self.collection_name in existing:
                logger.info("Qdrant collection '%s' already exists.", self.collection_name)
                return True
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            logger.info("Qdrant collection '%s' created.", self.collection_name)
            return True
        except Exception as exc:
            logger.error("Qdrant create_collection failed: %s", exc)
            raise VectorStoreError(str(exc)) from exc

    def upsert_embeddings(self, doc_id: str, vector: list[float], payload: dict) -> bool:
        """Insert or update a vector with associated payload metadata."""
        from qdrant_client.models import PointStruct
        client = self._get_client()
        try:
            client.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(id=doc_id, vector=vector, payload=payload)],
            )
            return True
        except Exception as exc:
            logger.error("Qdrant upsert_embeddings failed: %s", exc)
            raise VectorStoreError(str(exc)) from exc

    def search(
        self,
        query_vector: list[float],
        limit: int = 10,
        score_threshold: float = 0.7,
        filter_payload: dict | None = None,
    ) -> list[dict]:
        """Semantic similarity search. Returns list of {id, score, payload} dicts."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        client = self._get_client()
        try:
            qdrant_filter = None
            if filter_payload:
                conditions = [
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_payload.items()
                ]
                qdrant_filter = Filter(must=conditions)

            results = client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=qdrant_filter,
            )
            return [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]
        except Exception as exc:
            logger.error("Qdrant search failed: %s", exc)
            raise VectorStoreError(str(exc)) from exc

    def delete(self, doc_id: str) -> bool:
        """Delete a vector by ID."""
        from qdrant_client.models import PointIdsList
        client = self._get_client()
        try:
            client.delete(
                collection_name=self.collection_name,
                points_selector=PointIdsList(points=[doc_id]),
            )
            return True
        except Exception as exc:
            logger.error("Qdrant delete failed: %s", exc)
            raise VectorStoreError(str(exc)) from exc
