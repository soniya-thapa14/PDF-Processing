"""Tests for Tutorial 10 — Reranking."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))


def test_rerank_sorts_by_score():
    from reranker import rerank

    chunks = [
        {"chunk_text": "low relevance text about weather", "pdf_name": "a", "chunk_index": 0},
        {"chunk_text": "attention mechanism in transformers uses scaled dot product", "pdf_name": "a", "chunk_index": 1},
        {"chunk_text": "medium relevance about neural networks", "pdf_name": "a", "chunk_index": 2},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.1, 0.9, 0.5])
        mock_model.return_value = mock_ce

        result = rerank("What is attention?", chunks, top_k=3)
        assert result[0]["chunk_index"] == 1
        assert result[0]["rerank_score"] == 0.9
        assert result[-1]["chunk_index"] == 0


def test_rerank_respects_top_k():
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


def test_rerank_threshold_filters():
    from reranker import rerank

    chunks = [
        {"chunk_text": "good", "pdf_name": "a", "chunk_index": 0},
        {"chunk_text": "bad", "pdf_name": "a", "chunk_index": 1},
    ]

    with patch("reranker.get_model") as mock_model:
        mock_ce = MagicMock()
        mock_ce.predict.return_value = np.array([0.8, 0.1])
        mock_model.return_value = mock_ce

        result = rerank("test", chunks, top_k=5, threshold=0.5)
        assert len(result) == 1
        assert result[0]["chunk_index"] == 0


def test_rerank_empty_input():
    from reranker import rerank
    result = rerank("test", [], top_k=5)
    assert result == []
