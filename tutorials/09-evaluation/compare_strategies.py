"""
Tutorial 09 — Compare chunking strategies on retrieval metrics.

Runs eval_retrieval for each chunking strategy to find the best one.

Usage:
    uv run python tutorials/09-evaluation/compare_strategies.py --k 5

Implement the functions marked # TODO.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


STRATEGIES = [
    "chunk_fixed_char",
    "chunk_fixed_token",
    "chunk_recursive",
    "chunk_by_headers",
    "chunk_semantic",
    "chunk_table_aware",
    "chunk_sliding_window",
]


def compare_all(k: int = 5) -> dict:
    """
    Run evaluation for each strategy and produce a comparison.

    For each strategy in STRATEGIES:
    1. Call evaluate_retrieval(k=k, strategy=strategy)
    2. Store the aggregate metrics

    Args:
        k: top-k for retrieval evaluation

    Returns:
        dict mapping strategy_name → {avg_precision, avg_recall, avg_mrr, avg_ndcg}
    """
    # TODO: Implement strategy comparison.
    #   - Import evaluate_retrieval from eval_retrieval module
    #   - Loop through STRATEGIES
    #   - Call evaluate_retrieval for each (handle errors gracefully)
    #   - Return dict of strategy → aggregate metrics
    raise NotImplementedError("TODO: implement compare_all")


def print_comparison(results: dict):
    """
    Print a formatted comparison table sorted by precision.

    Args:
        results: dict from compare_all()
    """
    # TODO: Implement formatted table output.
    #   - Print header: Strategy, Precision@k, Recall@k, MRR, NDCG
    #   - Sort by avg_precision descending
    #   - Print each row formatted with alignment
    #   - Print the best strategy at the end
    raise NotImplementedError("TODO: implement print_comparison")
