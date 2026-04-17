from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from app import config


INDEX_FILE = "index.json"


@dataclass(frozen=True)
class IndexedChunk:
    doc_id: str
    title: str
    category: str
    chunk_id: int
    content: str


_index: list[IndexedChunk] | None = None


def _index_path() -> str:
    return os.path.join(config.FAISS_INDEX_DIR, INDEX_FILE)


def _ensure_index_dir() -> None:
    os.makedirs(config.FAISS_INDEX_DIR, exist_ok=True)


def _serialize(chunks: list[IndexedChunk]) -> list[dict[str, Any]]:
    return [
        {
            "doc_id": chunk.doc_id,
            "title": chunk.title,
            "category": chunk.category,
            "chunk_id": chunk.chunk_id,
            "content": chunk.content,
        }
        for chunk in chunks
    ]


def _deserialize(payload: list[dict[str, Any]]) -> list[IndexedChunk]:
    chunks: list[IndexedChunk] = []
    for item in payload:
        try:
            chunks.append(
                IndexedChunk(
                    doc_id=str(item.get("doc_id", "")),
                    title=str(item.get("title", "")),
                    category=str(item.get("category", "general")),
                    chunk_id=int(item.get("chunk_id", 0)),
                    content=str(item.get("content", "")),
                )
            )
        except Exception:
            continue
    return chunks


def initialize_index() -> None:
    """Load the persisted index into memory (idempotent)."""
    global _index
    if _index is not None:
        return

    _ensure_index_dir()
    path = _index_path()
    if not os.path.exists(path):
        _index = []
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if isinstance(payload, list):
            _index = _deserialize(payload)
        else:
            _index = []
    except Exception:
        _index = []


def _save_index() -> None:
    global _index
    if _index is None:
        _index = []
    _ensure_index_dir()
    with open(_index_path(), "w", encoding="utf-8") as f:
        json.dump(_serialize(_index), f, ensure_ascii=False)


def _chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
    return chunks


def add_document_to_index(doc_id: str, title: str, category: str, text: str) -> int:
    """Add/replace a document in the local index. Returns chunk_count."""
    initialize_index()
    remove_document_from_index(doc_id)

    pieces = _chunk_text(text)
    new_chunks = [
        IndexedChunk(
            doc_id=doc_id,
            title=title,
            category=category,
            chunk_id=i,
            content=piece,
        )
        for i, piece in enumerate(pieces)
    ]

    global _index
    _index = list(_index or [])
    _index.extend(new_chunks)
    _save_index()
    return len(new_chunks)


def remove_document_from_index(doc_id: str) -> None:
    initialize_index()
    global _index
    _index = [chunk for chunk in (_index or []) if chunk.doc_id != doc_id]
    _save_index()


def get_index_snapshot() -> list[IndexedChunk]:
    initialize_index()
    return list(_index or [])

