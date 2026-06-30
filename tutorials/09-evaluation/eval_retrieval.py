"""
Tutorial 09 — Retrieval Evaluation Metrics

Compute Precision@k, Recall@k, MRR, and NDCG to measure retrieval quality.

Usage:
    uv run python tutorials/09-evaluation/eval_retrieval.py --k 5

Implement the functions marked # TODO.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


EVAL_DATA = Path(__file__).parent / "eval_dataset.json"


def precision_at_k(retrieved_indices: list[int], gold_indices: list[int], k: int) -> float:
    """
    Compute Precision@k: fraction of top-k retrieved items that are relevant.

    Formula: |{retrieved[:k] ∩ gold}| / k

    Args:
        retrieved_indices: ordered list of retrieved chunk indices
        gold_indices: set of relevant chunk indices (ground truth)
        k: cutoff for top-k

    Returns:
        Float between 0.0 and 1.0
    """
    # TODO: Implement precision@k.
    #   - Take only the first k items from retrieved_indices
    #   - Count how many are in gold_indices
    #   - Divide by k
    raise NotImplementedError("TODO: implement precision_at_k")


def recall_at_k(retrieved_indices: list[int], gold_indices: list[int], k: int) -> float:
    """
    Compute Recall@k: fraction of relevant items that appear in top-k.

    Formula: |{retrieved[:k] ∩ gold}| / |gold|

    Args:
        retrieved_indices: ordered list of retrieved chunk indices
        gold_indices: set of relevant chunk indices (ground truth)
        k: cutoff for top-k

    Returns:
        Float between 0.0 and 1.0. Returns 0.0 if gold_indices is empty.
    """
    # TODO: Implement recall@k.
    #   - Return 0.0 if gold_indices is empty
    #   - Take first k from retrieved_indices
    #   - Count how many gold items appear in that set
    #   - Divide by total number of gold items
    raise NotImplementedError("TODO: implement recall_at_k")


def mrr(retrieved_indices: list[int], gold_indices: list[int]) -> float:
    """
    Compute Mean Reciprocal Rank: 1 / position of first relevant result.

    If no relevant result is found, return 0.0.
    Position is 1-indexed (first item = position 1).

    Args:
        retrieved_indices: ordered list of retrieved chunk indices
        gold_indices: set of relevant chunk indices

    Returns:
        Float between 0.0 and 1.0
    """
    # TODO: Implement MRR.
    #   - Iterate retrieved_indices with 1-based index
    #   - Return 1/position when first gold item is found
    #   - Return 0.0 if no gold item found
    raise NotImplementedError("TODO: implement mrr")


def ndcg_at_k(retrieved_indices: list[int], gold_indices: list[int], k: int) -> float:
    """
    Compute Normalized Discounted Cumulative Gain at k.

    DCG@k = Σ (relevance_i / log2(i + 1)) for i=1..k
    where relevance_i = 1 if retrieved[i] is in gold, else 0

    NDCG@k = DCG@k / ideal_DCG@k (where ideal has all relevant items first)

    Args:
        retrieved_indices: ordered list of retrieved chunk indices
        gold_indices: relevant chunk indices
        k: cutoff

    Returns:
        Float between 0.0 and 1.0. Returns 0.0 if ideal DCG is 0.
    """
    # TODO: Implement NDCG@k.
    #   - Compute DCG: sum of rel_i / log2(i+1) for top-k
    #   - Compute ideal DCG: assume all gold items ranked first
    #   - Return DCG / ideal_DCG (handle division by zero)
    raise NotImplementedError("TODO: implement ndcg_at_k")
