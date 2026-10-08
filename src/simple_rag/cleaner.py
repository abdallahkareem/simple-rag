from pathlib import Path
import re
from collections import Counter


def remove_page_numbers(text: str) -> str:
    """Remove standalone page numbers and common page-number labels."""
    return re.sub(
        r"(?im)^\s*(?:(?:page|p\.)\s*)?\d{1,4}(?:\s*(?:/|of)\s*\d{1,4})?\s*$\n?",
        "",
        text,
    )


def remove_headers_footers(text: str) -> str:
    """Remove short, non-sentence lines repeated throughout a document."""
    lines = text.splitlines()
    counts = Counter(line.strip() for line in lines if line.strip())
    return "\n".join(
        line
        for line in lines
        if not (
            line.strip()
            and len(line.strip()) <= 100
            and not re.search(r"[.!?。！？;:]$", line.strip())
            and counts[line.strip()] > 1
        )
    )


def remove_metadata(text: str) -> str:
    """Remove common bibliographic and document metadata lines."""
    metadata_patterns = (
        r"\s*(?:doi\s*:\s*|https?://doi\.org/)\S+\s*",
        r"\s*(?:isbn|issn|arxiv\s*:|copyright\b|©|published\s*:|publication date\s*:|author\s*:|keywords\s*:).*",
    )
    for pattern in metadata_patterns:
        text = re.sub(rf"(?im)^{pattern}$\n?", "", text)
    return text


def normalize_whitespace(text: str) -> str:
    """Normalize spaces and line endings without collapsing paragraphs."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t\f\v ]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()




def fix_hyphenation(text: str) -> str:
    """Rejoin words split by a line-ending hyphen in extracted text."""
    text = text.replace("\u00ad", "")
    return re.sub(r"(\w)-[ \t]*\r?\n[ \t]*(\w)", r"\1\2", text)


def clean_document(text: str) -> str:
    """Apply the document-cleaning steps in an order suited to PDF text."""
    text = remove_metadata(text)
    text = remove_page_numbers(text)
    text = remove_headers_footers(text)
    text = fix_hyphenation(text)
    return normalize_whitespace(text)



