from pathlib import Path

from pypdf import PdfReader


def pdf_to_text(pdf_path: str | Path) -> str:
    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_text(source_path: str | Path) -> str:
    """Read a PDF or a plain-text/Markdown source document."""
    source = Path(source_path)
    if not source.is_file():
        raise FileNotFoundError(f"Document not found: {source}")

    suffix = source.suffix.lower()
    if suffix == ".pdf":
        return pdf_to_text(source)
    if suffix in {".txt", ".md"}:
        return source.read_text(encoding="utf-8")
    raise ValueError(f"Unsupported document type: {suffix or '(no extension)'}")