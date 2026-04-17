import json
import os
from datetime import datetime

from app.config import DOCUMENTS_META_PATH

_documents: list[dict] = []
_loaded = False


def _ensure_loaded():
    global _documents, _loaded
    if _loaded:
        return
    if os.path.exists(DOCUMENTS_META_PATH):
        with open(DOCUMENTS_META_PATH, "r", encoding="utf-8") as f:
            _documents = json.load(f)
    else:
        _documents = []
    _loaded = True


def _save():
    os.makedirs(os.path.dirname(DOCUMENTS_META_PATH), exist_ok=True)
    with open(DOCUMENTS_META_PATH, "w", encoding="utf-8") as f:
        json.dump(_documents, f, ensure_ascii=False, indent=2)


def get_all_documents() -> list[dict]:
    _ensure_loaded()
    return list(_documents)


def add_document(
    doc_id: str,
    filename: str,
    title: str,
    category: str,
    page_count: int,
    chunk_count: int,
    uploaded_by: str,
) -> dict:
    _ensure_loaded()
    doc = {
        "doc_id": doc_id,
        "filename": filename,
        "title": title,
        "category": category,
        "upload_date": datetime.now().isoformat(),
        "uploaded_by": uploaded_by,
        "page_count": page_count,
        "chunk_count": chunk_count,
    }
    _documents.append(doc)
    _save()
    return doc


def remove_document(doc_id: str) -> dict | None:
    _ensure_loaded()
    for i, doc in enumerate(_documents):
        if doc["doc_id"] == doc_id:
            removed = _documents.pop(i)
            _save()
            return removed
    return None
