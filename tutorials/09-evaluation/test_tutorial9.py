"""Tests for Tutorial 09 — Retrieval Evaluation metrics.

Run: uv run pytest tutorials/09-evaluation/ -v

These tests verify your implementations of precision_at_k, recall_at_k,
mrr, and ndcg_at_k.

Edge cases to think about:
- What if k=0? (division by zero)
- What if retrieved list is empty?
- What about very large k values?
- Tie-breaking behavior in NDCG?
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from eval_retrieval import precision_at_k, recall_at_k, mrr, ndcg_at_k


# ---------------------------------------------------------------------------
# Precision@k
# ---------------------------------------------------------------------------

def test_precision_perfect_retrieval():
    """All retrieved items are relevant."""
    assert precision_at_k([1, 2, 3], [1, 2, 3], k=3) == 1.0


def test_precision_partial_match():
    """3 of 5 retrieved are relevant."""
    assert precision_at_k([1, 2, 3, 4, 5], [1, 2, 3], k=5) == 3 / 5


def test_precision_no_match():
    """None of the retrieved are relevant."""
    assert precision_at_k([10, 11, 12], [1, 2, 3], k=3) == 0.0


def test_precision_k_larger_than_retrieved():
    """k can be larger than retrieved list (denominator is still k)."""
    assert precision_at_k([1, 2], [1, 2, 3], k=5) == 2 / 5


# ---------------------------------------------------------------------------
# Recall@k
# ---------------------------------------------------------------------------

def test_recall_all_found():
    """All gold items are in top-k."""
    assert recall_at_k([1, 2, 3, 4, 5], [1, 2, 3], k=5) == 1.0


def test_recall_partial():
    """Only 1 of 3 gold items found."""
    assert recall_at_k([1, 10, 11, 12, 13], [1, 2, 3], k=5) == 1 / 3


def test_recall_empty_gold():
    """If there are no relevant items, recall is 0."""
    assert recall_at_k([1, 2, 3], [], k=3) == 0.0


def test_recall_none_found():
    """No gold items in retrieved."""
    assert recall_at_k([10, 11, 12], [1, 2, 3], k=3) == 0.0


# ---------------------------------------------------------------------------
# MRR (Mean Reciprocal Rank)
# ---------------------------------------------------------------------------

def test_mrr_first_position():
    """Relevant item at position 1 → RR = 1.0."""
    assert mrr([5, 2, 3], [5, 6]) == 1.0


def test_mrr_second_position():
    """Relevant item at position 2 → RR = 0.5."""
    assert mrr([10, 5, 3], [5, 6]) == 0.5


def test_mrr_third_position():
    """Relevant item at position 3 → RR = 1/3."""
    assert abs(mrr([10, 11, 5], [5]) - 1 / 3) < 1e-9


def test_mrr_not_found():
    """No relevant items → RR = 0.0."""
    assert mrr([10, 11, 12], [1, 2, 3]) == 0.0


# ---------------------------------------------------------------------------
# NDCG@k
# ---------------------------------------------------------------------------

def test_ndcg_perfect_ranking():
    """All relevant items ranked first → NDCG = 1.0."""
    assert ndcg_at_k([1, 2, 3], [1, 2, 3], k=3) == 1.0


def test_ndcg_imperfect_ranking():
    """Relevant items not first → 0 < NDCG < 1."""
    score = ndcg_at_k([10, 1, 2], [1, 2], k=3)
    assert 0 < score < 1.0


def test_ndcg_no_relevant():
    """No relevant items retrieved → NDCG = 0."""
    assert ndcg_at_k([10, 11, 12], [1, 2], k=3) == 0.0


# ---------------------------------------------------------------------------
# Additional edge cases: boundary conditions students must handle
# ---------------------------------------------------------------------------

def test_precision_empty_retrieved():
    """Empty retrieved list with k>0 should return 0.0."""
    assert precision_at_k([], [1, 2, 3], k=5) == 0.0


def test_recall_single_item_found():
    """One gold item, found at first position."""
    assert recall_at_k([7], [7], k=1) == 1.0


def test_mrr_all_relevant():
    """When ALL retrieved items are relevant, RR still = 1.0 (first hit)."""
    assert mrr([1, 2, 3], [1, 2, 3]) == 1.0


def test_mrr_large_list():
    """Relevant item at position 100 → RR = 1/100."""
    retrieved = list(range(200, 300)) + [42]
    assert abs(mrr(retrieved, [42]) - 1.0 / 101) < 1e-9


def test_ndcg_single_relevant_at_k():
    """One relevant item at exactly position k should still contribute."""
    score = ndcg_at_k([10, 11, 12, 13, 1], [1], k=5)
    assert score > 0.0
    assert score < 1.0


def test_ndcg_k_smaller_than_retrieved():
    """k truncates evaluation — items beyond k are ignored."""
    full_score = ndcg_at_k([10, 1, 2, 3, 4], [1, 2, 3, 4], k=5)
    partial_score = ndcg_at_k([10, 1, 2, 3, 4], [1, 2, 3, 4], k=2)
    assert partial_score <= full_score


def test_precision_k_equals_one():
    """Precision@1: only first item matters."""
    assert precision_at_k([1, 2, 3], [1], k=1) == 1.0
    assert precision_at_k([2, 1, 3], [1], k=1) == 0.0


def test_recall_with_duplicate_retrieved():
    """Duplicates in retrieved list should not inflate recall."""
    assert recall_at_k([1, 1, 1, 1, 1], [1, 2, 3], k=5) == 1 / 3
