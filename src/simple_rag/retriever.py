from collections import defaultdict

from rank_bm25 import BM25Okapi

from simple_rag.embedder import embed_query


def hybrid_retrieval(query: str, collection, top_k: int = 5, rrf_k: int = 60) -> list[str]:
    """Fuse Chroma vector results with BM25 keyword results."""
    if top_k <= 0:
        return []

    corpus = collection.get(include=["documents"])["documents"] or []
    if not corpus:
        return []

    tokenized_corpus = [chunk.split() for chunk in corpus]
    sparse_scores = BM25Okapi(tokenized_corpus).get_scores(query.split())
    sparse_results = [
        corpus[index]
        for index in sorted(range(len(corpus)), key=lambda index: sparse_scores[index], reverse=True)[:top_k]
    ]

    dense_response = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=min(len(corpus), top_k * 2),
        include=["documents"],
    )
    dense_results = (dense_response.get("documents") or [[]])[0]
    scores = defaultdict(float)

    for results in (sparse_results, dense_results):
        for rank, chunk in enumerate(results, start=1):
            scores[chunk] += 1.0 / (rrf_k + rank)

    combined = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in combined[:top_k]]