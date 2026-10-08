# Simple RAG

A small Python project for extracting text from a PDF, cleaning it, and splitting it into chunks. The current pipeline demonstrates ingestion and chunking; vector storage, retrieval, and answer generation are not implemented yet.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)

## Setup

From the repository root, install the project dependencies and create the local settings file:

```sh
uv sync
cp .env.example .env
```

The chunker reads `CHUNK_SIZE` and `CHUNK_OVERLAP` from `.env`. `GROQ_API_KEY` is currently required by the settings model but is not used by the pipeline; replace the example placeholder if you use code that calls Groq.

## Run the pipeline

The ingestion module extracts text from `docs/Harness_Engineering_Anatomy_Architecture.pdf` and writes it to `document.txt`:

```sh
uv run python -m simple_rag.ingestion
```

Clean that extracted text into the path expected by the pipeline:

```sh
mkdir -p docs/processed
uv run python -c 'from pathlib import Path; from simple_rag.cleaner import clean_document; source = Path("document.txt"); target = Path("docs/processed/cleaned_document.txt"); target.write_text(clean_document(source.read_text(encoding="utf-8")), encoding="utf-8")'
```

Then split the cleaned text and print the first chunk and total chunk count:

```sh
uv run python -m simple_rag.pipeline
```

Run these commands from the repository root. To process a different PDF, update the `pdf_path` in `src/simple_rag/ingestion.py` first.

## Configuration

| Setting         | Purpose                                                                          | Example          |
| --------------- | -------------------------------------------------------------------------------- | ---------------- |
| `PDF_PATH`      | PDF path setting (the ingestion script currently uses a hard-coded path instead) | `docs/input.pdf` |
| `GROQ_API_KEY`  | Groq API key setting; not currently used by the pipeline                         | `your-key`       |
| `CHUNK_SIZE`    | Maximum chunk size in characters                                                 | `1000`           |
| `CHUNK_OVERLAP` | Overlap between adjacent chunks in characters                                    | `200`            |

## Other commands

Run the package's greeting entry point:

```sh
uv run simple-rag
```
