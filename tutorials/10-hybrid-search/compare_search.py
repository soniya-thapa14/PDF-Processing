"""
Tutorial 10 — Compare vector, keyword, and hybrid search.

Side-by-side evaluation using the gold-standard eval set.

Usage:
    uv run python tutorials/10-hybrid-search/compare_search.py --k 5

Implement the functions marked # TODO.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "09-evaluation"))
sys.path.insert(0, str(Path(__file__).parent))


EVAL_DATA = Path(__file__).parent.parent / "09-evaluation" / "eval_dataset.json"


def evaluate_search_method(search_fn, questions: list[dict], k: int = 5) -> dict:
    """
    Evaluate a search function across all questions.

    For each question:
    1. Call search_fn(query=..., top_k=k, pdf_name=...)
    2. Extract chunk_index from results
    3. Compute precision@k, recall@k, mrr against gold_chunk_indices

    Args:
        search_fn: callable that accepts (query, top_k, pdf_name) kwargs
        questions: list of eval dataset entries
        k: top-k for evaluation

    Returns:
        dict with avg precision, recall, mrr
    """
    # TODO: Implement search method evaluation.
    #   - Import precision_at_k, recall_at_k, mrr from eval_retrieval
    #   - For each question, call search_fn and compute metrics
    #   - Return averaged scores
    raise NotImplementedError("TODO: implement evaluate_search_method")


def main():
    """
    Load eval dataset and compare vector, keyword, and hybrid search.
    Print formatted results table.
    """
    # TODO: Implement comparison.
    #   - Load eval_dataset.json
    #   - Import vector search (from rag_pipeline), keyword_search, hybrid_search
    #   - Call evaluate_search_method for each
    #   - Print comparison table
    raise NotImplementedError("TODO: implement main comparison")


if __name__ == "__main__":
    main()
