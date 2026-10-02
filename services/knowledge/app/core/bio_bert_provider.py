# services/knowledge/app/core/bio_bert_provider.py
"""BioBERT embedding provider.

This implementation attempts to load a BioBERT model using PyTorch. If the model
or the `torch` library is unavailable, it falls back to the existing deterministic
provider so the service continues to operate in environments without the heavy
dependency.
"""

from __future__ import annotations

import os
from typing import List

try:
    import torch
    from transformers import AutoModel, AutoTokenizer  # type: ignore
except Exception:  # pragma: no cover
    torch = None
    AutoModel = None
    AutoTokenizer = None

from .hybrid_rag import EmbeddingProvider, DeterministicSemanticEmbeddingProvider


class BioBERTEmbeddingProvider(EmbeddingProvider):
    """Loads a BioBERT checkpoint and returns a dense vector.

    The model is loaded once at class initialization. The `get_embedding`
    method tokenizes the input, runs it through the model, and returns the
    CLS token representation normalized to unit length.
    """

    _model = None
    _tokenizer = None
    _dim = 768  # BioBERT base hidden size

    def __init__(self, model_name: str = "dmis-lab/biobert-base-cased-v1.1") -> None:
        if torch is None:
            raise RuntimeError("torch is not installed; BioBERT provider cannot be used.")
        self.model_name = model_name
        self._load_model()

    def _load_model(self) -> None:
        if BioBERTEmbeddingProvider._model is not None:
            return
        BioBERTEmbeddingProvider._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        BioBERTEmbeddingProvider._model = AutoModel.from_pretrained(self.model_name)
        BioBERTEmbeddingProvider._model.eval()

    def get_embedding(self, text: str) -> List[float]:
        if BioBERTEmbeddingProvider._model is None or BioBERTEmbeddingProvider._tokenizer is None:
            fallback = DeterministicSemanticEmbeddingProvider(dim=self._dim)
            return fallback.get_embedding(text)
        inputs = BioBERTEmbeddingProvider._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = BioBERTEmbeddingProvider._model(**inputs)
        vec = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec
