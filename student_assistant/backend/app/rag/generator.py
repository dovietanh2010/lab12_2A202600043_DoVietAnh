from __future__ import annotations

from typing import Any

from app import config


def generate_rag_response(query: str, chunks: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Generate a deterministic answer from retrieved chunks (no external LLM)."""
    if not chunks:
        return None

    # Filter weak matches if configured
    threshold = float(getattr(config, "RAG_RELEVANCE_THRESHOLD", 0.0) or 0.0)
    filtered = [c for c in chunks if float(c.get("score", 0.0)) >= threshold]
    if not filtered:
        return None

    top = filtered[: min(3, len(filtered))]
    bullets = []
    sources = []
    for chunk in top:
        snippet = str(chunk.get("content", "")).strip()
        if len(snippet) > 400:
            snippet = snippet[:400].rstrip() + "..."
        title = chunk.get("title") or chunk.get("doc_id")
        bullets.append(f"- {title}: {snippet}")
        sources.append(
            {
                "doc_id": chunk.get("doc_id"),
                "title": chunk.get("title"),
                "category": chunk.get("category"),
                "chunk_id": chunk.get("chunk_id"),
            }
        )

    response = (
        f"Mình tìm thấy thông tin liên quan tới: {query}\n\n"
        + "\n".join(bullets)
        + "\n\nNếu bạn muốn, mình có thể trả lời cụ thể hơn theo phần bạn đang cần."
    )

    return {
        "response": response,
        "sources": sources,
        "tool_used": "rag",
    }

