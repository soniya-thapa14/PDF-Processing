"""Tests for Tutorial 10 — Hybrid Search (RRF).

Run: uv run pytest tutorials/10-hybrid-search/ -v

These tests verify your implementation of reciprocal_rank_fusion.

Edge cases to think about:
- What happens with very long ranked lists?
- What if the same document appears at different ranks in different lists?
- What about numerical precision in score accumulation?
- What if all items have the same score?
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


# ---------------------------------------------------------------------------
# Additional edge cases: boundary conditions for robust implementation
# ---------------------------------------------------------------------------

def test_rrf_item_at_different_ranks():
    """A doc at rank 1 in list1 and rank 5 in list2 accumulates both scores."""
    list1 = [
        {"pdf_name": "a", "chunk_index": 1, "chunk_text": "top in list1"},
        {"pdf_name": "a", "chunk_index": 2, "chunk_text": "second"},
    ]
    list2 = [
        {"pdf_name": "a", "chunk_index": 3, "chunk_text": "x"},
        {"pdf_name": "a", "chunk_index": 4, "chunk_text": "x"},
        {"pdf_name": "a", "chunk_index": 5, "chunk_text": "x"},
        {"pdf_name": "a", "chunk_index": 6, "chunk_text": "x"},
        {"pdf_name": "a", "chunk_index": 1, "chunk_text": "top in list1 again at rank 5"},
    ]
    result = reciprocal_rank_fusion([list1, list2])
    chunk1 = next(r for r in result if r["chunk_index"] == 1)
    expected = 1.0 / (RRF_K + 1) + 1.0 / (RRF_K + 5)
    assert abs(chunk1["rrf_score"] - expected) < 1e-9


def test_rrf_large_list_scores_decrease():
    """Items at later ranks get progressively smaller scores."""
    items = [
        {"pdf_name": "a", "chunk_index": i, "chunk_text": f"chunk {i}"}
        for i in range(20)
    ]
    result = reciprocal_rank_fusion([items])
    for i in range(len(result) - 1):
        assert result[i]["rrf_score"] >= result[i + 1]["rrf_score"]


def test_rrf_preserves_chunk_text():
    """Original chunk metadata should be preserved in output."""
    items = [{"pdf_name": "report.pdf", "chunk_index": 7, "chunk_text": "Important finding"}]
    result = reciprocal_rank_fusion([items])
    assert result[0]["pdf_name"] == "report.pdf"
    assert result[0]["chunk_text"] == "Important finding"
    assert result[0]["chunk_index"] == 7


def test_rrf_different_pdfs_same_chunk_index():
    """(pdf_name, chunk_index) is the identity — same index in different PDFs are distinct."""
    list1 = [{"pdf_name": "a.pdf", "chunk_index": 1, "chunk_text": "from a"}]
    list2 = [{"pdf_name": "b.pdf", "chunk_index": 1, "chunk_text": "from b"}]
    result = reciprocal_rank_fusion([list1, list2])
    assert len(result) == 2  # They are distinct documents
    assert result[0]["rrf_score"] == result[1]["rrf_score"]
