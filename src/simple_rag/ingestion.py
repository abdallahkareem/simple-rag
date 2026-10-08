from pathlib import Path

from pypdf import PdfReader


def pdf_to_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


if __name__ == "__main__":
    pdf_path = "docs/Harness_Engineering_Anatomy_Architecture.pdf"

    text = pdf_to_text(pdf_path)

    Path("document.txt").write_text(
        text,
        encoding="utf-8",
    )

    print("PDF converted successfully!")