from pathlib import Path
from simple_rag.cleaner import clean_document
from simple_rag.chunker import chunk_text
from simple_rag.embedder import embed_text , embed_query , vector_size

if __name__ == "__main__":
    input_path = Path("docs/processed/cleaned_document.txt")

    text = input_path.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    embeddings = [embed_text(chunk) for chunk in chunks]
    size = vector_size()
    print(embeddings[0])
    print(f"Vector size: {size}")