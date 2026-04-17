import re
import unicodedata


THINK_BLOCK_PATTERN = re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL)
INLINE_THINK_PATTERN = re.compile(r"</?think>", re.IGNORECASE)
TABLE_SEPARATOR_CELL_PATTERN = re.compile(r"^:?-{3,}:?$")


def normalize_text_for_matching(text: str) -> str:
    """Lowercase text and remove accents so keyword matching is less brittle."""
    normalized = unicodedata.normalize("NFD", text.lower())
    without_accents = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", without_accents).strip()


def _looks_like_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.count("|") >= 2 and any(char.isalpha() for char in stripped)


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def _is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(TABLE_SEPARATOR_CELL_PATTERN.fullmatch(cell) for cell in cells if cell)


def _convert_markdown_tables(text: str) -> str:
    lines = text.splitlines()
    converted_lines: list[str] = []
    index = 0

    while index < len(lines):
        current_line = lines[index]

        if (
            index + 1 < len(lines)
            and _looks_like_table_row(current_line)
            and _is_table_separator(lines[index + 1])
        ):
            headers = _split_table_row(current_line)
            rendered_rows: list[str] = []
            index += 2

            while index < len(lines) and "|" in lines[index]:
                cells = _split_table_row(lines[index])
                if len(cells) == len(headers):
                    parts = [
                        f"{header}: {value}"
                        for header, value in zip(headers, cells)
                        if header and value
                    ]
                    if parts:
                        rendered_rows.append("- " + "; ".join(parts))
                elif any(cell for cell in cells):
                    rendered_rows.append("- " + " | ".join(cell for cell in cells if cell))
                index += 1

            if rendered_rows:
                converted_lines.extend(rendered_rows)
            continue

        converted_lines.append(current_line)
        index += 1

    return "\n".join(converted_lines)


def clean_response_text(text: str | None) -> str:
    """Remove reasoning tags, flatten markdown tables, and trim noisy whitespace."""
    if not text:
        return ""

    cleaned = THINK_BLOCK_PATTERN.sub("", text)
    cleaned = INLINE_THINK_PATTERN.sub("", cleaned)
    cleaned = _convert_markdown_tables(cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()
