"""Tests for Tutorial 08 — Evaluation metrics."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from eval_retrieval import precision_at_k, recall_at_k, mrr, ndcg_at_k  # noqa: E402


def test_precision_at_k_perfect():
    retrieved = [1, 2, 3, 4, 5]
    gold = [1, 2, 3]
    assert precision_at_k(retrieved, gold, 5) == 3 / 5


def test_precision_at_k_none_relevant():
    retrieved = [10, 11, 12]
    gold = [1, 2, 3]
    assert precision_at_k(retrieved, gold, 3) == 0.0


def test_recall_at_k_all_found():
    retrieved = [1, 2, 3, 4, 5]
    gold = [1, 2, 3]
    assert recall_at_k(retrieved, gold, 5) == 1.0


def test_recall_at_k_partial():
    retrieved = [1, 10, 11, 12, 13]
    gold = [1, 2, 3]
    assert recall_at_k(retrieved, gold, 5) == 1 / 3


def test_mrr_first_position():
    retrieved = [5, 2, 3]
    gold = [5, 6]
    assert mrr(retrieved, gold) == 1.0


def test_mrr_second_position():
    retrieved = [10, 5, 3]
    gold = [5, 6]
    assert mrr(retrieved, gold) == 0.5


def test_mrr_not_found():
    retrieved = [10, 11, 12]
    gold = [1, 2, 3]
    assert mrr(retrieved, gold) == 0.0


def test_ndcg_perfect():
    retrieved = [1, 2, 3]
    gold = [1, 2, 3]
    assert ndcg_at_k(retrieved, gold, 3) == 1.0


def test_ndcg_imperfect():
    retrieved = [10, 1, 2]
    gold = [1, 2]
    score = ndcg_at_k(retrieved, gold, 3)
    assert 0 < score < 1.0
