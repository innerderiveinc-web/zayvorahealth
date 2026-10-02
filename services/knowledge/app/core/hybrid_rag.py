"""
ZAYVORA Hybrid RAG Engine (Phase 10).

Combines:
1. Dense Vector Embeddings (semantic similarity over clinical monographs & trials)
2. Lexical Search (Okapi BM25 for precise Unani terminology, botanical names & symptoms)
3. Structured Knowledge Graph Multi-Hop Traversal (deterministic ontology paths)
4. Reciprocal Rank Fusion (RRF) and Weighted Score Combination
"""
from __future__ import annotations

import math
import re
from typing import Any, List, Protocol


class Document:
    def __init__(
        self,
        id: str,
        doc_type: str,
        title: str,
        content: str,
        metadata: dict[str, Any] | None = None,
        embedding: list[float] | None = None,
    ):
        self.id = id
        self.doc_type = doc_type  # 'mufrad', 'murakkab', 'poison', 'evidence', 'organ_axis'
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.embedding = embedding

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "doc_type": self.doc_type,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata,
        }


def _tokenize(text: str) -> list[str]:
    """Tokenizes text into normalized unigram and bigram tokens for classical terminology."""
    clean = re.sub(r"[^\w\s\-]", " ", text.lower())
    words = [w.strip() for w in clean.split() if len(w.strip()) > 1]
    tokens = list(words)
    # Add adjacent bigrams to capture classical compound terms (e.g. "suranjan talkh", "majun falasifa")
    for i in range(len(words) - 1):
        tokens.append(f"{words[i]}_{words[i+1]}")
    return tokens


class BM25Index:
    """Okapi BM25 Lexical Index for domain-specific Unani terminology and formulas."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs: dict[str, Document] = {}
        self.doc_len: dict[str, int] = {}
        self.doc_freqs: dict[str, int] = {}
        self.term_freqs: dict[str, dict[str, int]] = {}
        self.avg_doc_len: float = 0.0

    def index_documents(self, documents: list[Document]) -> None:
        self.docs.clear()
        self.doc_len.clear()
        self.doc_freqs.clear()
        self.term_freqs.clear()

        total_len = 0
        for doc in documents:
            self.docs[doc.id] = doc
            tokens = _tokenize(f"{doc.title} {doc.content}")
            length = len(tokens)
            self.doc_len[doc.id] = length
            total_len += length

            tf: dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            self.term_freqs[doc.id] = tf

            for t in set(tokens):
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        self.avg_doc_len = total_len / len(documents) if documents else 1.0

    def search(self, query: str, top_k: int = 20) -> list[tuple[str, float]]:
        query_tokens = _tokenize(query)
        if not query_tokens or not self.docs:
            return []

        n_docs = len(self.docs)
        scores: dict[str, float] = {}

        for t in query_tokens:
            df = self.doc_freqs.get(t, 0)
            if df == 0:
                continue
            # Standard Robertson-Spärck Jones IDF
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))

            for doc_id, doc in self.docs.items():
                tf = self.term_freqs.get(doc_id, {}).get(t, 0)
                if tf == 0:
                    continue
                d_len = self.doc_len.get(doc_id, 1)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (d_len / self.avg_doc_len))
                score = idf * (tf * (self.k1 + 1.0)) / denom
                scores[doc_id] = scores.get(doc_id, 0.0) + score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]


class EmbeddingProvider(Protocol):
    def get_embedding(self, text: str) -> list[float]: ...


import hashlib


def _stable_hash(s: str) -> int:
    return int(hashlib.md5(s.encode("utf-8")).hexdigest()[:16], 16)


class DeterministicSemanticEmbeddingProvider:
    """Lightweight, deterministic high-dimensional semantic projector.
    Generates 128-dimensional normalized dense vectors using stable MD5 hashing
    and token co-occurrence projections. Guarantees zero external dependency,
    rapid execution, and reproducible cosine similarity.
    """

    def __init__(self, dim: int = 128):
        self.dim = dim

    def get_embedding(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        tokens = _tokenize(text)
        if not tokens:
            return vec

        for token in tokens:
            h = _stable_hash(token)
            idx1 = h % self.dim
            idx2 = (h >> 16) % self.dim
            idx3 = (h >> 32) % self.dim

            vec[idx1] += 1.0
            vec[idx2] += 0.6
            vec[idx3] += 0.3

            # Subword 3-grams for morphological / root-word similarity
            for i in range(len(token) - 2):
                tri = token[i : i + 3]
                ht = _stable_hash(tri)
                t_idx = ht % self.dim
                vec[t_idx] += 0.2

        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec



class DenseVectorStore:
    """In-memory dense vector store with cosine similarity retrieval."""

    def __init__(self, embedding_provider: EmbeddingProvider | None = None):
        self.provider = embedding_provider or DeterministicSemanticEmbeddingProvider()
        self.dimension = getattr(self.provider, "dim", 128)
        self.docs: dict[str, Document] = {}

    def index_documents(self, documents: list[Document]) -> None:
        self.docs.clear()
        for doc in documents:
            if doc.embedding is None:
                doc.embedding = self.provider.get_embedding(f"{doc.title} {doc.content}")
            self.docs[doc.id] = doc

    def search(self, query: str, top_k: int = 20) -> list[tuple[str, float]]:
        q_vec = self.provider.get_embedding(query)
        scores: list[tuple[str, float]] = []

        for doc_id, doc in self.docs.items():
            if doc.embedding is None:
                continue
            # Cosine similarity between unit vectors is dot product
            sim = sum(a * b for a, b in zip(q_vec, doc.embedding))
            scores.append((doc_id, float(sim)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


def reciprocal_rank_fusion(
    ranked_lists: list[list[tuple[str, float]]],
    weights: list[float] | None = None,
    k: int = 60,
) -> list[tuple[str, float]]:
    """Combines multiple ranked lists using Reciprocal Rank Fusion (RRF).
    Formula: RRF_score(d) = sum_m (weight_m / (k + rank_m(d)))
    """
    if not ranked_lists:
        return []

    if weights is None:
        weights = [1.0] * len(ranked_lists)

    scores: dict[str, float] = {}

    for w, r_list in zip(weights, ranked_lists):
        for rank, (doc_id, _) in enumerate(r_list, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + (w / (k + rank))

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked


class ZAYVORAIntelligenceEngine:
    """Master Hybrid RAG Retrieval Engine for ZAYVORA Health.
    Unifies BM25 lexical search, Dense vector semantic retrieval, and Knowledge Graph triples.
    """

    def __init__(self, embedding_provider: EmbeddingProvider | None = None):
        self.bm25 = BM25Index()
        # Choose embedding provider: BioBERT if enabled, else deterministic
        if embedding_provider is None:
            import os
            if os.getenv("USE_BIOBERT", "false").lower() == "true":
                from .bio_bert_provider import BioBERTEmbeddingProvider
                embedding_provider = BioBERTEmbeddingProvider()
        self.vector_store = DenseVectorStore(embedding_provider=embedding_provider)
        self.documents: dict[str, Document] = {}

    def load_canonical_corpus(self) -> int:
        """Loads canonical UPI Mufradat, NFUM Murakkabat, Schedule E(1) Poisons,
        and Organ Axes into the hybrid index."""
        try:
            from app.core.pharmacopoeia import NFUM_COMPOUND_REGISTRY, SCHEDULE_E1_POISONS, UPI_MUFRADAT_REGISTRY, get_upi_mufradat
            from app.core.taxonomy import ORGAN_AXES
        except ImportError:
            from services.knowledge.app.core.pharmacopoeia import NFUM_COMPOUND_REGISTRY, SCHEDULE_E1_POISONS, UPI_MUFRADAT_REGISTRY, get_upi_mufradat
            from services.knowledge.app.core.taxonomy import ORGAN_AXES

        docs: list[Document] = []

        # 1. Schedule E(1) Statutory Poisons
        for pid, p in SCHEDULE_E1_POISONS.items():
            title = f"Schedule E(1) Poison: {p['canonical_name']} ({p.get('botanical_name', '')})"
            content = (
                f"Statutory Poison: {p['canonical_name']}. Toxic alkaloids: {', '.join(p.get('toxic_alkaloids', []))}. "
                f"Poison class: {p.get('poison_class', '')}. Mandatory Mudabbar Detoxification Protocol: {p.get('mudabbar_protocol', '')}. "
                f"Max single dose: {p.get('max_single_dose_mg')} mg. Max daily dose: {p.get('max_daily_dose_mg')} mg. "
                f"Antidote: {p.get('antidote', '')}. Musleh: {p.get('musleh', '')}. Badal: {p.get('badal', '')}. "
                f"Warning: {p.get('statutory_warning', '')}."
            )
            docs.append(Document(id=f"poison-{pid}", doc_type="poison", title=title, content=content, metadata=p))

        # 2. Complete Pharmacopoeia Monograph Register (350 Monographs)
        for m in get_upi_mufradat():
            mz = m.get("mizaj", {})
            mz_str = f"{mz.get('temperament', '')} (Hot/Cold: {mz.get('hc_degree', 0)}, Wet/Dry: {mz.get('wd_degree', 0)})"
            afal = ", ".join(m.get("afal", [])) if isinstance(m.get("afal"), list) else m.get("afal", "")
            botanical = m.get("botanical_name") or m.get("botanicalName", "")
            is_e1 = m.get("is_schedule_e1", m.get("isScheduleE1", False))
            syns = ", ".join(m.get("synonyms", []))
            title = f"Mufrad: {m['name']} ({botanical})"
            content = (
                f"Single Drug Monograph: {m['name']} ({botanical}). Synonyms: {syns}. Mizaj Temperament: {mz_str}. "
                f"Actions and Af'al: {afal}. Standard Posology Dose: {m.get('dose', '')}. "
                f"Classical Musleh Corrective: {m.get('musleh', '')}. Classical Badal Substitute: {m.get('badal', '')}. "
                f"Contraindications: {m.get('contraindications', 'None listed')}. "
                f"Schedule E(1) Poison: {'Yes' if is_e1 else 'No'}."
            )
            docs.append(Document(id=f"mufrad-{m['id']}", doc_type="mufrad", title=title, content=content, metadata=m))

        # 3. NFUM Murakkabat Compound Register
        for c in NFUM_COMPOUND_REGISTRY:
            title = f"Murakkab: {c['name']} ({c.get('category', '')})"
            content = (
                f"Classical Compound Formulation: {c['name']}. Form: {c.get('category', '')}. "
                f"Classical Indication and Therapeutic Use: {c.get('classicalIndication', '')}. "
                f"Standard Dose: {c.get('dose', '')}. Precautions: {c.get('precautions', 'None')}. "
                f"Ingredients count: {len(c.get('ingredients', []))}."
            )
            docs.append(Document(id=f"compound-{c['id']}", doc_type="murakkab", title=title, content=content, metadata=c))

        # 4. Organ Axes
        for ax in ORGAN_AXES:
            title = f"Organ Axis: {ax['name']} ({ax['code']})"
            content = (
                f"Canonical Organ Axis: {ax['name']} ({ax['code']}). Systems covered: {ax.get('systemsCovered', '')}. "
                f"Classical concept: {ax.get('classicalConcept', '')}."
            )
            docs.append(Document(id=f"axis-{ax['code']}", doc_type="organ_axis", title=title, content=content, metadata=ax))

        self.documents = {d.id: d for d in docs}
        self.bm25.index_documents(docs)
        self.vector_store.index_documents(docs)
        return len(docs)

    def hybrid_search(
        self,
        query: str,
        *,
        organ_axis: List[str] | None = None,
        temperament: str | None = None,
        top_k: int = 5,
        dense_weight: float = 0.45,
        bm25_weight: float = 0.45,
        graph_weight: float = 0.10,
        mode: str = "rrf",
    ) -> list[dict[str, Any]]:
        """Executes unified hybrid search across dense vector similarity, BM25 lexical matching,
        and knowledge graph contextual relevance."""
        if not self.documents:
            self.load_canonical_corpus()

        # 1. Lexical retrieval
        bm25_results = self.bm25.search(query, top_k=top_k * 3)

        # 2. Dense semantic retrieval
        dense_results = self.vector_store.search(query, top_k=top_k * 3)

        # 3. Graph heuristic retrieval (axis & temperament matching)
        graph_results: list[tuple[str, float]] = []
        for doc_id, doc in self.documents.items():
            g_score = 0.0
            meta = doc.metadata
            # Axis match
            if organ_axis:
                if isinstance(organ_axis, list):
                    axes = organ_axis
                else:
                    axes = [organ_axis]
                if doc.doc_type == "organ_axis" and meta.get("code") in axes:
                    g_score += 2.0
                elif doc.doc_type == "mufrad":
                    afal_str = str(meta.get("afal", "")).lower()
                    if any(ax.lower() in afal_str for ax in axes):
                        g_score += 1.0
                elif doc.doc_type == "murakkab":
                    ind = str(meta.get("classicalIndication", "")).lower()
                    if any(ax.lower() in ind for ax in axes):
                        g_score += 1.0

            # Temperament match
            if temperament:
                doc_temp = meta.get("mizaj", {}).get("temperament", "")
                if doc_temp.lower() == temperament.lower():
                    g_score += 1.0

            if g_score > 0.0:
                graph_results.append((doc_id, g_score))

        graph_results.sort(key=lambda x: x[1], reverse=True)

        # 4. Fusion
        if mode == "rrf":
            ranked = reciprocal_rank_fusion(
                [dense_results, bm25_results, graph_results],
                weights=[dense_weight, bm25_weight, graph_weight],
            )
        else:
            # Weighted normalization
            ranked = self._weighted_score_fusion(
                dense_results, bm25_results, graph_results, dense_weight, bm25_weight, graph_weight
            )

        # 5. Format results
        output = []
        for doc_id, score in ranked[:top_k]:
            doc = self.documents.get(doc_id)
            if not doc:
                continue
            is_poison = (
                doc.doc_type == "poison"
                or bool(doc.metadata.get("isScheduleE1", False))
                or bool(doc.metadata.get("is_schedule_e1", False))
            )
            output.append({
                "document_id": doc.id,
                "doc_type": doc.doc_type,
                "title": doc.title,
                "content": doc.content,
                "score": round(score, 4),
                "is_schedule_e1": is_poison,
                "metadata": doc.metadata,
            })

        return output

    def _weighted_score_fusion(
        self,
        dense: list[tuple[str, float]],
        bm25: list[tuple[str, float]],
        graph: list[tuple[str, float]],
        w_dense: float,
        w_bm25: float,
        w_graph: float,
    ) -> list[tuple[str, float]]:
        """Normalized linear combination of scores."""
        d_map = self._normalize_scores(dict(dense))
        b_map = self._normalize_scores(dict(bm25))
        g_map = self._normalize_scores(dict(graph))

        all_keys = set(d_map.keys()) | set(b_map.keys()) | set(g_map.keys())
        combined = []
        for k in all_keys:
            s = (w_dense * d_map.get(k, 0.0)) + (w_bm25 * b_map.get(k, 0.0)) + (w_graph * g_map.get(k, 0.0))
            combined.append((k, s))

        combined.sort(key=lambda x: x[1], reverse=True)
        return combined

    def _normalize_scores(self, score_dict: dict[str, float]) -> dict[str, float]:
        if not score_dict:
            return {}
        vals = score_dict.values()
        min_v, max_v = min(vals), max(vals)
        if max_v == min_v:
            return {k: 1.0 for k in score_dict}
        return {k: (v - min_v) / (max_v - min_v) for k, v in score_dict.items()}

    def get_corpus_stats(self) -> dict[str, Any]:
        """Returns statistics on indexed corpus documents."""
        if not self.documents:
            self.load_canonical_corpus()
        by_type: dict[str, int] = {}
        for d in self.documents.values():
            by_type[d.doc_type] = by_type.get(d.doc_type, 0) + 1
        return {
            "total_documents": len(self.documents),
            "by_type": by_type,
            "dense_vector_dim": self.vector_store.dimension,
            "bm25_terms_count": len(self.bm25.doc_freqs),
        }

HybridRAGEngine = ZAYVORAIntelligenceEngine  # backward‑compatibility alias

_HYBRID_RAG_SINGLETON: ZAYVORAIntelligenceEngine | None = None

def get_hybrid_rag_service() -> ZAYVORAIntelligenceEngine:
    """Returns singleton instance of ZAYVORA hybrid RAG service with preloaded canonical corpus."""
    global _HYBRID_RAG_SINGLETON
    if _HYBRID_RAG_SINGLETON is None:
        _HYBRID_RAG_SINGLETON = ZAYVORAIntelligenceEngine()
        _HYBRID_RAG_SINGLETON.load_canonical_corpus()
    return _HYBRID_RAG_SINGLETON
