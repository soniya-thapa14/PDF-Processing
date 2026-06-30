"""Tests for Tutorial 10 — Hybrid Search (RRF).

Run: uv run pytest tutorials/10-hybrid-search/ -v

These tests verify your implementation of reciprocal_rank_fusion.
Edge cases included to teach you about score accumulation and merging.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from hybrid_search import reciprocal_rank_fusion, RRF_K


# ---------------------------------------------------------------------------
# RRF: basic behavior
# ---------------------------------------------------------------------------

def test_rrf_single_list_preserves_order():
    """With one list, RRF preserves the original order."""
    items = [
        {"pdf_name": "a", "chunk_index": 1, "chunk_text": "first"},
        {"pdf_name": "a", "chunk_index": 2, "chunk_text": "second"},
    ]
    result = reciprocal_rank_fusion([items])
    assert len(result) == 2
    assert result[0]["chunk_index"] == 1
    assert result[0]["rrf_score"] > result[1]["rrf_score"]


def test_rrf_shared_item_ranks_higher():
    """A doc appearing in BOTH lists should score higher than one in only one list."""
    list1 = [
        {"pdf_name": "a", "chunk_index": 1, "chunk_text": "shared"},
        {"pdf_name": "a", "chunk_index": 2, "chunk_text": "only-vec"},
    ]
    list2 = [
        {"pdf_name": "a", "chunk_index": 1, "chunk_text": "shared"},
        {"pdf_name": "a", "chunk_index": 3, "chunk_text": "only-kw"},
    ]
    result = reciprocal_rank_fusion([list1, list2])
    assert result[0]["chunk_index"] == 1, "shared item should rank first"
    # Score = 1/(60+1) + 1/(60+1) = 2/(61)
    expected = 2.0 / (RRF_K + 1)
    assert abs(result[0]["rrf_score"] - expected) < 1e-9


def test_rrf_disjoint_lists_equal_scores():
    """Docs appearing at same rank in different lists get equal scores."""
    list1 = [{"pdf_name": "a", "chunk_index": 1, "chunk_text": "x"}]
    list2 = [{"pdf_name": "a", "chunk_index": 2, "chunk_text": "y"}]
    result = reciprocal_rank_fusion([list1, list2])
    assert len(result) == 2
    assert result[0]["rrf_score"] == result[1]["rrf_score"]


# ---------------------------------------------------------------------------
# RRF: edge cases
# ---------------------------------------------------------------------------

def test_rrf_empty_lists():
    """Empty input lists should return empty result."""
    assert reciprocal_rank_fusion([]) == [] or reciprocal_rank_fusion([[]])  == []


def test_rrf_adds_score_key():
    """Every result should have an 'rrf_score' key."""
    items = [{"pdf_name": "test", "chunk_index": 5, "chunk_text": "hello"}]
    result = reciprocal_rank_fusion([items])
    assert "rrf_score" in result[0]


def test_rrf_three_lists():
    """RRF works with 3+ ranked lists."""
    list1 = [{"pdf_name": "a", "chunk_index": 1, "chunk_text": "x"}]
    list2 = [{"pdf_name": "a", "chunk_index": 1, "chunk_text": "x"}]
    list3 = [{"pdf_name": "a", "chunk_index": 1, "chunk_text": "x"}]
    result = reciprocal_rank_fusion([list1, list2, list3])
    expected = 3.0 / (RRF_K + 1)
    assert abs(result[0]["rrf_score"] - expected) < 1e-9
