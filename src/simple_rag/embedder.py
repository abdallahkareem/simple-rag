# Cross Encoder for Reranking
from sentence_transformers import SentenceTransformer , CrossEncoder
from simple_rag.config import get_settings

settings = get_settings()

def load_model():

  embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
  return embedder


def embed_text(text: str) -> list[float]:
    embedder = load_model()
    return embedder.encode(text).tolist()


def embed_query(query: str) -> list[float]:
    embedder = load_model()
    return embedder.encode(query).tolist()

def vector_size():
    embedder = load_model()
    return embedder.get_sentence_embedding_dimension()
