"""
Tutorial 10 — Hybrid Search (Vector + Keyword via RRF)

Combine vector similarity search with Postgres full-text search using
Reciprocal Rank Fusion.

Usage:
    uv run python tutorials/10-hybrid-search/hybrid_search.py --query "R-1 zone"

Implement the functions marked # TODO.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent))


RRF_K = 60  # standard RRF constant (Cormack et al., 2009)


def reciprocal_rank_fusion(
    ranked_lists: list[list[dict]],
    k: int = RRF_K,
) -> list[dict]:
    """
    Merge multiple ranked lists using Reciprocal Rank Fusion.

    Formula: RRF_score(doc) = Σ 1/(k + rank_i) for each list i where doc appears.

    Documents are identified by (pdf_name, chunk_index) tuple.
    Each input list is ordered by relevance (best first).

    Args:
        ranked_lists: list of ranked result lists (each item is a dict
                      with at least 'pdf_name' and 'chunk_index' keys)
        k: RRF constant (default 60)

    Returns:
        Merged list sorted by RRF score descending, with 'rrf_score' key added
    """
    # TODO: Implement RRF.
    #   - For each ranked_list, iterate items with 1-based rank
    #   - Identify each doc by (pdf_name, chunk_index) tuple
    #   - Accumulate score: 1/(k + rank) for each appearance
    #   - Sort by accumulated score descending
    #   - Add 'rrf_score' to each result dict
    #   - Return the sorted merged list
    raise NotImplementedError("TODO: implement reciprocal_rank_fusion")


def hybrid_search(
    query: str,
    top_k: int = 5,
    vector_k: int = 20,
    keyword_k: int = 20,
    pdf_name: str = None,
    strategy: str = None,
) -> list[dict]:
    """
    Run hybrid search combining vector and keyword retrieval with RRF.

    Steps:
    1. Run vector search (from Tutorial 08's rag_pipeline.retrieve)
    2. Run keyword search (from keyword_search module)
    3. Fuse results with reciprocal_rank_fusion
    4. Return top_k fused results

    Args:
        query: search query
        top_k: final number of results to return
        vector_k: number of vector search candidates
        keyword_k: number of keyword search candidates
        pdf_name: optional PDF filter
        strategy: optional strategy filter

    Returns:
        Top-k results after RRF fusion
    """
    # TODO: Implement hybrid search.
    #   - Import and call vector search (retrieve from rag_pipeline)
    #   - Import and call keyword_search from this directory
    #   - Pass both result lists to reciprocal_rank_fusion
    #   - Return first top_k items from fused results
    raise NotImplementedError("TODO: implement hybrid_search")
