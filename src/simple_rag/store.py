import chromadb

from simple_rag.config import get_settings
from simple_rag.chunker import chunk_text
from simple_rag.embedder import embed_text , embed_query , vector_size

settings = get_settings()


def build_chroma_collection(chunks):
    """Get or create a Chroma collection."""
    client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=settings.COLLECTION_NAME)

    collection.add(
        documents=chunks,
        embeddings=[embed_text(chunk) for chunk in chunks],
        metadatas=[{"source": f"chunk_{i}"} for i in range(len(chunks))],
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    return collection


