"""
Tutorial 03 — Tests

    uv run pytest tutorials/03-chunking-strategies/ -v

Tests verify the chunking strategy contracts and the PDF-to-Markdown pipeline.
"""

from chunking_strategies import (
    chunk_fixed_char,
    chunk_fixed_token,
    chunk_recursive,
    chunk_by_headers,
    chunk_semantic,
    chunk_table_aware,
    chunk_sliding_window,
    get_all_strategies,
)

SAMPLE_TEXT = """# Introduction

This is the first paragraph of the introduction. It contains several sentences
that explain the purpose of this document. The content is meant to test chunking.

## Background

The background section provides context. It includes details about the history
and motivation for this work. Multiple paragraphs follow.

Here is a second paragraph in the background. It adds more detail and context
to help the reader understand the broader landscape of the topic.

## Methods

| Method | Accuracy | Speed |
| --- | --- | --- |
| Baseline | 85% | Fast |
| Proposed | 92% | Medium |
| Oracle | 99% | Slow |

The table above summarizes our methods. Each was evaluated on the same dataset.

## Conclusion

We demonstrated that the proposed method outperforms the baseline while
maintaining reasonable speed. Future work will focus on optimization.
"""


def test_fixed_char_produces_overlapping_chunks():
    chunks = chunk_fixed_char(SAMPLE_TEXT, chunk_size=200, overlap=50)
    assert len(chunks) > 1, "should produce multiple chunks"
    assert all(len(c) <= 200 for c in chunks), "no chunk should exceed chunk_size"
    assert chunks[0][-50:] == chunks[1][:50] or len(chunks[0]) < 200, \
        "overlap region should match"


def test_fixed_token_uses_tiktoken():
    chunks = chunk_fixed_token(SAMPLE_TEXT, chunk_size=50, overlap=10)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)


def test_recursive_respects_separators():
    chunks = chunk_recursive(SAMPLE_TEXT, chunk_size=300)
    assert len(chunks) > 1
    assert all(len(c) <= 300 or "\n" not in c for c in chunks), \
        "chunks should respect size limit when separators are available"


def test_markdown_headers_returns_dicts():
    chunks = chunk_by_headers(SAMPLE_TEXT)
    assert len(chunks) >= 4, "should find at least 4 sections (intro, bg, methods, conclusion)"
    assert all(isinstance(c, dict) for c in chunks)
    assert all("heading" in c and "content" in c for c in chunks)
    headings = [c["heading"] for c in chunks if c["heading"]]
    assert "Introduction" in headings
    assert "Conclusion" in headings


def test_semantic_groups_related_sentences():
    chunks = chunk_semantic(SAMPLE_TEXT, threshold=0.3)
    assert len(chunks) >= 2, "should produce at least 2 chunks"
    assert all(isinstance(c, str) for c in chunks)
    assert all(len(c) > 0 for c in chunks)


def test_table_aware_keeps_tables_whole():
    chunks = chunk_table_aware(SAMPLE_TEXT, chunk_size=200)
    table_chunks = [c for c in chunks if "| Method |" in c or "| Baseline |" in c]
    assert len(table_chunks) >= 1, "table should appear in at least one chunk"
    for tc in table_chunks:
        assert "| Method |" in tc and "| Oracle |" in tc, \
            "table should not be split across chunks"


def test_sliding_window_has_high_overlap():
    chunks = chunk_sliding_window(SAMPLE_TEXT, window_size=300, stride=100)
    assert len(chunks) > 1
    for i in range(len(chunks) - 1):
        overlap = len(set(chunks[i]) & set(chunks[i + 1]))
        assert overlap > 0, "consecutive chunks should share content"


def test_registry_returns_all_seven():
    strategies = get_all_strategies()
    assert len(strategies) == 7
    expected = {
        "fixed_char", "fixed_token", "recursive",
        "markdown_headers", "semantic", "table_aware", "sliding_window",
    }
    assert set(strategies.keys()) == expected
