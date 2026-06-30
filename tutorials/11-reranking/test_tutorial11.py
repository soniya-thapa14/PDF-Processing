"""Tests for Tutorial 11 — Reranking with Cross-Encoders.

Run: uv run pytest tutorials/11-reranking/ -v

These tests mock the cross-encoder model so they run without downloading it.
They verify your rerank() logic: sorting, top_k, and threshold filtering.

Edge cases to think about:
- What if all chunks score identically?
- What if threshold filters out everything?
- What about negative cross-encoder scores (valid for ms-marco models)?
- Numerical stability with very close scores?
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))


# ---------------------------------------------------------------------------
# Core reranking behavior
# ---------------------------------------------------------------------------

def test_rerank_sorts_by_score():
    """Results should be sorted by cross-encoder score, highest first."""
    from reranker import rerank

    chunks = [
        {"chunk_text": "irrelevant weather", "pdf_name": "a", "chunk_index": 0},
        {"chunk_text": "highly relevant attention", "pdf_name": "a", "chunk_index": 1},
        {"chunk_text": "medium relevance", "pdf_name": "a", "chunk_index": 2},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.1, 0.9, 0.5])
        mock_model.return_value = mock_ce

        result = rerank("What is attention?", chunks, top_k=3)
        assert result[0]["chunk_index"] == 1, "highest scored chunk should be first"
        assert result[1]["chunk_index"] == 2
        assert result[2]["chunk_index"] == 0


def test_rerank_adds_score():
    """Each result should have a 'rerank_score' key."""
    from reranker import rerank

    chunks = [{"chunk_text": "test", "pdf_name": "a", "chunk_index": 0}]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.75])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=1)
        assert "rerank_score" in result[0]
        assert result[0]["rerank_score"] == 0.75


# ---------------------------------------------------------------------------
# top_k and threshold
# ---------------------------------------------------------------------------

def test_rerank_respects_top_k():
    """Should return at most top_k results."""
    from reranker import rerank

    chunks = [
        {"chunk_text": f"chunk {i}", "pdf_name": "a", "chunk_index": i}
        for i in range(10)
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.arange(10, 0, -1, dtype=float)
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=3)
        assert len(result) == 3


def test_rerank_threshold_filters_low_scores():
    """Chunks below threshold should be excluded."""
    from reranker import rerank

    chunks = [
        {"chunk_text": "good", "pdf_name": "a", "chunk_index": 0},
        {"chunk_text": "bad", "pdf_name": "a", "chunk_index": 1},
        {"chunk_text": "terrible", "pdf_name": "a", "chunk_index": 2},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.8, 0.1, -0.5])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=5, threshold=0.5)
        assert len(result) == 1
        assert result[0]["chunk_index"] == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_rerank_empty_input():
    """Empty chunk list should return empty list."""
    from reranker import rerank
    result = rerank("test", [], top_k=5)
    assert result == []


def test_rerank_single_chunk():
    """Single chunk should be returned as-is (with score)."""
    from reranker import rerank

    chunks = [{"chunk_text": "only one", "pdf_name": "a", "chunk_index": 0}]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.6])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=5)
        assert len(result) == 1
        assert result[0]["rerank_score"] == 0.6


# ---------------------------------------------------------------------------
# Additional edge cases: robust reranking under real-world conditions
# ---------------------------------------------------------------------------

def test_rerank_negative_scores():
    """ms-marco cross-encoders can output negative scores (not relevant). Must still sort correctly."""
    from reranker import rerank

    chunks = [
        {"chunk_text": "somewhat relevant", "pdf_name": "a", "chunk_index": 0},
        {"chunk_text": "not relevant at all", "pdf_name": "a", "chunk_index": 1},
        {"chunk_text": "very irrelevant", "pdf_name": "a", "chunk_index": 2},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([-0.5, -3.0, -7.0])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=3)
        assert result[0]["chunk_index"] == 0
        assert result[0]["rerank_score"] == -0.5
        assert result[2]["rerank_score"] == -7.0


def test_rerank_threshold_filters_all():
    """If threshold is very high, result can be empty."""
    from reranker import rerank

    chunks = [
        {"chunk_text": "low", "pdf_name": "a", "chunk_index": 0},
        {"chunk_text": "also low", "pdf_name": "a", "chunk_index": 1},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.2, 0.1])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=5, threshold=0.9)
        assert result == []


def test_rerank_preserves_original_metadata():
    """Reranking should preserve all original chunk keys (not just chunk_text)."""
    from reranker import rerank

    chunks = [
        {"chunk_text": "data", "pdf_name": "report.pdf", "chunk_index": 42,
         "chunk_strategy": "semantic", "similarity": 0.8},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.9])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=5)
        assert result[0]["pdf_name"] == "report.pdf"
        assert result[0]["chunk_index"] == 42
        assert result[0]["chunk_strategy"] == "semantic"


def test_rerank_identical_scores_stable():
    """When multiple chunks score identically, all should be returned (order may vary)."""
    from reranker import rerank

    chunks = [
        {"chunk_text": f"chunk {i}", "pdf_name": "a", "chunk_index": i}
        for i in range(5)
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=5)
        assert len(result) == 5
        assert all(r["rerank_score"] == 0.5 for r in result)
