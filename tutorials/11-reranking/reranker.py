"""Cross-encoder reranker for two-stage retrieval."""

from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_model = None


def get_model() -> CrossEncoder:
    """Load the cross-encoder model (cached after first call)."""
    global _model
    if _model is None:
        _model = CrossEncoder(MODEL_NAME)
    return _model


def rerank(query: str, chunks: list[dict], top_k: int = 5, threshold: float = None) -> list[dict]:
    """Rerank chunks using a cross-encoder.

    The cross-encoder scores each (query, chunk_text) pair jointly, producing
    a relevance score that is much more accurate than bi-encoder cosine similarity.

    Args:
        query: the user's question
        chunks: list of dicts with at least 'chunk_text' key
        top_k: number of top results to return after reranking
        threshold: optional minimum score to include (filters low-confidence)

    Returns:
        Top-k chunks sorted by cross-encoder score, with 'rerank_score' added
    """
    if not chunks:
        return []

    model = get_model()
    pairs = [(query, chunk["chunk_text"]) for chunk in chunks]
    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    ranked = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)

    if threshold is not None:
        ranked = [c for c in ranked if c["rerank_score"] >= threshold]

    return ranked[:top_k]
