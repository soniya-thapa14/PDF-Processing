"""
Tutorial 11 — Cross-Encoder Reranker

Rerank retrieved chunks using a cross-encoder model for improved precision.

Usage:
    from reranker import rerank
    reranked = rerank("What is attention?", chunks, top_k=5)

Implement the functions marked # TODO.
"""

from __future__ import annotations

from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_model = None


def get_model() -> CrossEncoder:
    """
    Load the cross-encoder model (cached after first call).

    Uses the global _model variable to avoid reloading on every call.

    Returns:
        CrossEncoder instance
    """
    # TODO: Implement model loading with caching.
    #   - Use `global _model`
    #   - If _model is None, load CrossEncoder(MODEL_NAME)
    #   - Return _model
    raise NotImplementedError("TODO: implement get_model")


def rerank(query: str, chunks: list[dict], top_k: int = 5, threshold: float = None) -> list[dict]:
    """
    Rerank chunks using a cross-encoder.

    The cross-encoder scores each (query, chunk_text) pair jointly.
    This is more accurate than bi-encoder cosine similarity because
    it captures token-level interactions between query and passage.

    Steps:
    1. Create (query, chunk_text) pairs for all chunks
    2. Score all pairs with the cross-encoder
    3. Sort by score descending
    4. Optionally filter by threshold
    5. Return top_k results with 'rerank_score' added

    Args:
        query: the user's question
        chunks: list of dicts with at least 'chunk_text' key
        top_k: number of results after reranking
        threshold: optional minimum score (filter low-confidence)

    Returns:
        Top-k chunks sorted by cross-encoder score, with 'rerank_score' added
    """
    # TODO: Implement reranking.
    #   - Return [] if chunks is empty
    #   - Load model via get_model()
    #   - Create list of (query, chunk["chunk_text"]) pairs
    #   - Call model.predict(pairs) to get scores array
    #   - Add "rerank_score" to each chunk dict
    #   - Sort by rerank_score descending
    #   - If threshold is set, filter out scores below it
    #   - Return top_k results
    raise NotImplementedError("TODO: implement rerank")
