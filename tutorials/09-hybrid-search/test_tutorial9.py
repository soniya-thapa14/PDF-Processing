"""Tests for Tutorial 09 — Hybrid search and RRF."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from hybrid_search import reciprocal_rank_fusion, RRF_K


def test_rrf_single_list():
    items = [
        {"pdf_name": "a", "chunk_index": 1, "chunk_text": "one"},
        {"pdf_name": "a", "chunk_index": 2, "chunk_text": "two"},
    ]
    result = reciprocal_rank_fusion([items])
    assert len(result) == 2
    assert result[0]["chunk_index"] == 1
    assert result[0]["rrf_score"] > result[1]["rrf_score"]


def test_rrf_merge_two_lists():
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
    assert result[0]["rrf_score"] == 2.0 / (RRF_K + 1)


def test_rrf_disjoint_lists():
    list1 = [{"pdf_name": "a", "chunk_index": 1, "chunk_text": "x"}]
    list2 = [{"pdf_name": "a", "chunk_index": 2, "chunk_text": "y"}]
    result = reciprocal_rank_fusion([list1, list2])
    assert len(result) == 2
    assert result[0]["rrf_score"] == result[1]["rrf_score"]


def test_rrf_preserves_metadata():
    items = [{"pdf_name": "test", "chunk_index": 5, "chunk_text": "hello", "extra": "data"}]
    result = reciprocal_rank_fusion([items])
    assert result[0]["pdf_name"] == "test"
    assert result[0]["chunk_index"] == 5
    assert "rrf_score" in result[0]
