# Mock documents removed - documents are now managed via admin PDF upload.

INTERNAL_DOCUMENTS: list[dict] = []


def get_all_documents() -> list[dict]:
    return INTERNAL_DOCUMENTS


def get_document_by_id(doc_id: str) -> dict | None:
    return None
