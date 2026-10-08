from pathlib import Path

import chromadb

from simple_rag.config import get_settings
from simple_rag.embedder import embed_text

settings = get_settings()


def get_chroma_collection():
    
    client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
    return client.get_or_create_collection(name=settings.COLLECTION_NAME)


def build_chroma_collection(chunks: list[str], source: str | Path):
    
    source_id = str(Path(source).resolve())
    collection = get_chroma_collection()

    collection.delete(where={"source": source_id})
    if not chunks:
        return collection

    collection.upsert(
        documents=chunks,
        embeddings=[embed_text(chunk) for chunk in chunks],
        metadatas=[{"source": source_id, "chunk": i} for i in range(len(chunks))],
        ids=[f"{source_id}:{i}" for i in range(len(chunks))],
    )
    return collection


