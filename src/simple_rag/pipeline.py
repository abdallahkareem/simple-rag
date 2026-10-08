from pathlib import Path
from simple_rag.cleaner import clean_document
from simple_rag.chunker import chunk_text
from simple_rag.store import build_chroma_collection

if __name__ == "__main__":
    input_path = Path("docs/processed/cleaned_document.txt")

    text = input_path.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    
    collection = build_chroma_collection(chunks)