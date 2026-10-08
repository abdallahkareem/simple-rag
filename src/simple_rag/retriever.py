import numpy as np

from rank_bm25 import BM25Okapi
from collections import defaultdict

from simple_rag.config import get_settings
from simple_rag.embedder import embed_text, embed_query , vector_size
from simple_rag.store import build_chroma_collection


def sparse_retrieval(query: str, chunks: list[str], top_k: int = 5) -> list[str]:
    """Retrieve the most relevant chunks using BM25."""
    tokenized_chunks = [chunk.split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_indices]


def dense_retrieval(query: str, chunks: list[str], top_k: int = 5) -> list[str]:
    """Retrieve the most relevant chunks using dense embeddings."""
    query_embedding = embed_query(query)
    chunk_embeddings = [embed_text(chunk) for chunk in chunks]
    similarities = np.dot(chunk_embeddings, query_embedding)
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [chunks[i] for i in top_indices]


# Hybrid Retrieval using RRF (Reciprocal Rank Fusion)
def hybrid_retrieval(query: str, chunks: list[str], top_k: int = 5 , rrf_k = 60) -> list[str]:
    
    sparse_results = sparse_retrieval(query, chunks, top_k)
    dense_results = dense_retrieval(query, chunks, top_k)

    scores = defaultdict(float)

    for results in (sparse_results, dense_results):
      for rank, chunk in enumerate(results, start=1):
        scores[chunk] += 1.0 / (rrf_k + rank)

    combined = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in combined[:top_k]]