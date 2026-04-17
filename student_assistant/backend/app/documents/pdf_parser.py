import pymupdf


def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
    """Extract all text from a PDF file using PyMuPDF.

    Returns (full_text, page_count).
    """
    doc = pymupdf.open(file_path)
    page_count = len(doc)
    pages = []
    for page in doc:
        text = page.get_text("text")
        if text.strip():
            pages.append(text)
    doc.close()
    return "\n\n".join(pages), page_count
