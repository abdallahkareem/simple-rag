from functools import lru_cache

from sentence_transformers import SentenceTransformer
from simple_rag.config import get_settings

settings = get_settings()


@lru_cache(maxsize=1)
def load_model() -> SentenceTransformer:
        return SentenceTransformer(settings.EMBEDDING_MODEL)


def embed_text(text: str) -> list[float]:
    return load_model().encode(text).tolist()


def embed_query(query: str) -> list[float]:
    return load_model().encode(query).tolist()


def vector_size() -> int:
    dimension = load_model().get_sentence_embedding_dimension()
    if dimension is None:
        raise RuntimeError("The embedding model did not report its vector size.")
    return dimension
