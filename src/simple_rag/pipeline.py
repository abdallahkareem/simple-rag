import argparse
from pathlib import Path

from simple_rag.chunker import chunk_text
from simple_rag.cleaner import clean_document
from simple_rag.config import get_settings
from simple_rag.generator import answer
from simple_rag.ingestion import extract_text
from simple_rag.retriever import hybrid_retrieval
from simple_rag.store import build_chroma_collection, get_chroma_collection

settings = get_settings()


def ingest_document(source_path: str | Path | None = None) -> int:
    """Extract, clean, chunk, and index a source document."""
    source = Path(source_path or settings.PDF_PATH)
    raw_text = extract_text(source)
    cleaned_text = clean_document(raw_text)
    if not cleaned_text:
        raise ValueError(f"No usable text found in {source}.")

    chunks = chunk_text(cleaned_text)
    build_chroma_collection(chunks, source)
    return len(chunks)


def answer_question(question: str, top_k: int | None = None) -> str:
    """Retrieve relevant document chunks and generate a grounded answer."""
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    collection = get_chroma_collection()
    chunks = hybrid_retrieval(question, collection, top_k or settings.TOP_K)
    if not chunks:
        raise RuntimeError("No indexed document chunks found. Run the ingest command first.")

    return answer("\n\n".join(chunks), question)


def interactive_chat() -> None:
    print("Ask questions about your indexed documents. Press Enter on an empty line to exit.")
    while True:
        question = input("\nYou: ").strip()
        if not question:
            return
        print(f"\nAssistant: {answer_question(question)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents and ask grounded questions.")
    commands = parser.add_subparsers(dest="command")

    ingest_parser = commands.add_parser("ingest", help="Index a PDF, TXT, or Markdown document.")
    ingest_parser.add_argument("source", nargs="?", default=settings.PDF_PATH)

    ask_parser = commands.add_parser("ask", help="Ask one question about indexed documents.")
    ask_parser.add_argument("question", nargs="+")

    commands.add_parser("chat", help="Start an interactive chat with indexed documents.")

    args = parser.parse_args()
    if args.command == "ingest":
        count = ingest_document(args.source)
        print(f"Indexed {count} chunks from {args.source}.")
    elif args.command == "ask":
        print(answer_question(" ".join(args.question)))
    elif args.command == "chat":
        interactive_chat()
    else:
        count = ingest_document()
        print(f"Indexed {count} chunks from {settings.PDF_PATH}.")
        interactive_chat()


if __name__ == "__main__":
    main()