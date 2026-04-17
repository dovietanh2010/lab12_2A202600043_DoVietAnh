from __future__ import annotations

import re
from collections import Counter
from typing import Any

from app import config
from app.rag.ingestion import get_index_snapshot


def _tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"[^0-9A-Za-zÀ-ỹ]+", text.lower()) if t]


def _score(query_tokens: list[str], chunk_tokens: list[str]) -> float:
    if not query_tokens or not chunk_tokens:
        return 0.0
    q = Counter(query_tokens)
    c = Counter(chunk_tokens)
    overlap = sum(min(q[t], c.get(t, 0)) for t in q)
    return float(overlap) / float(len(query_tokens))


def retrieve(query: str, top_k: int | None = None) -> list[dict[str, Any]]:
    """Return best-matching chunks from the persisted index."""
    k = int(top_k or config.RAG_TOP_K)
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scored: list[tuple[float, dict[str, Any]]] = []
    for chunk in get_index_snapshot():
        s = _score(query_tokens, _tokenize(chunk.content))
        if s <= 0:
            continue
        scored.append(
            (
                s,
                {
                    "doc_id": chunk.doc_id,
                    "title": chunk.title,
                    "category": chunk.category,
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "score": s,
                },
            )
        )

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:k]]

