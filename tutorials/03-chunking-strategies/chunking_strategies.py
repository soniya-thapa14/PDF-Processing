"""
Tutorial 03 — Chunking Strategies

Implements 7 different text chunking strategies. Each takes a Markdown string
and returns a list of chunk strings.

Usage:
    from chunking_strategies import get_all_strategies
    strategies = get_all_strategies()
    for name, chunk_fn in strategies.items():
        chunks = chunk_fn(markdown_text)

Implement the functions marked # TODO.
"""

from __future__ import annotations

import re
from typing import Callable


# ---------------------------------------------------------------------------
# Strategy 1: Fixed-size character splitting
# ---------------------------------------------------------------------------

def chunk_fixed_char(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Split text into chunks of `chunk_size` characters with `overlap` characters
    of overlap between consecutive chunks.

    Returns a list of strings, each at most `chunk_size` characters.
    The last chunk may be smaller.
    """
    # TODO: Implement fixed-size character splitting with overlap.
    #   - Start at position 0
    #   - Take chunk_size characters
    #   - Advance by (chunk_size - overlap)
    #   - Repeat until end of text
    #   - Don't create empty chunks
    raise NotImplementedError("TODO: implement fixed-size character chunking")


# ---------------------------------------------------------------------------
# Strategy 2: Fixed-size token splitting
# ---------------------------------------------------------------------------

def chunk_fixed_token(text: str, chunk_size: int = 256, overlap: int = 50) -> list[str]:
    """
    Split text into chunks of `chunk_size` tokens with `overlap` token overlap.
    Uses tiktoken (cl100k_base encoding).

    Returns a list of strings (decoded back from tokens).
    """
    # TODO: Implement token-based splitting.
    #   - Encode the entire text with tiktoken (cl100k_base)
    #   - Slide a window of chunk_size tokens with stride (chunk_size - overlap)
    #   - Decode each window back to a string
    #   - Return the list of decoded chunks
    raise NotImplementedError("TODO: implement fixed-size token chunking")


# ---------------------------------------------------------------------------
# Strategy 3: Recursive text splitting
# ---------------------------------------------------------------------------

def chunk_recursive(
    text: str,
    chunk_size: int = 1000,
    separators: list[str] | None = None,
) -> list[str]:
    """
    Recursively split text using a hierarchy of separators:
        ["\n\n", "\n", ". ", " "]

    At each level, split the text by the current separator. If any piece is
    still larger than chunk_size, split it with the next separator down.

    Returns a list of chunks, each <= chunk_size characters (best effort).
    """
    # TODO: Implement recursive splitting.
    #   - Default separators: ["\n\n", "\n", ". ", " "]
    #   - Split by first separator
    #   - For each piece: if len <= chunk_size, keep it
    #   - If len > chunk_size, recursively split with next separator
    #   - If no separators left and still too big, force-split at chunk_size
    #   - Merge small consecutive pieces back together (up to chunk_size)
    raise NotImplementedError("TODO: implement recursive text splitting")


# ---------------------------------------------------------------------------
# Strategy 4: Markdown-header splitting
# ---------------------------------------------------------------------------

def chunk_by_headers(text: str) -> list[dict]:
    """
    Split Markdown text at heading boundaries (lines starting with #, ##, ###).

    Returns a list of dicts:
        [{"heading": "Section Title", "level": 2, "content": "...body text..."}, ...]

    Each chunk contains the text from one heading until the next heading of
    equal or higher level. Top-level content before any heading gets
    heading=None, level=0.
    """
    # TODO: Implement header-based splitting.
    #   - Scan line by line for lines matching r'^(#{1,6})\s+(.+)'
    #   - Accumulate body lines between headings
    #   - Return list of dicts with heading metadata
    raise NotImplementedError("TODO: implement markdown-header chunking")


# ---------------------------------------------------------------------------
# Strategy 5: Semantic chunking
# ---------------------------------------------------------------------------

def chunk_semantic(
    text: str,
    threshold: float = 0.5,
    min_chunk_size: int = 100,
) -> list[str]:
    """
    Group consecutive sentences by embedding similarity. Split at points
    where cosine similarity between adjacent sentence groups drops below
    `threshold`.

    Uses sentence-transformers (all-MiniLM-L6-v2) for embeddings.

    Returns a list of chunks (groups of sentences).
    """
    # TODO: Implement semantic chunking.
    #   - Split text into sentences (by ". " or regex)
    #   - Embed each sentence with sentence-transformers
    #   - Compute cosine similarity between each pair of adjacent sentences
    #   - Find "break points" where similarity < threshold
    #   - Group sentences between break points into chunks
    #   - Merge chunks smaller than min_chunk_size with their neighbor
    raise NotImplementedError("TODO: implement semantic chunking")


# ---------------------------------------------------------------------------
# Strategy 6: Table-aware chunking
# ---------------------------------------------------------------------------

def chunk_table_aware(text: str, chunk_size: int = 1000) -> list[str]:
    """
    Keep Markdown tables as atomic units (never split mid-table).
    Split prose sections using recursive splitting.

    A table is detected as a block of consecutive lines where every line
    starts with '|' or is a separator row (| --- | --- |).

    Returns a list of chunks. Table chunks may exceed chunk_size if the
    table itself is larger.
    """
    # TODO: Implement table-aware chunking.
    #   - Parse text into segments: "prose" blocks and "table" blocks
    #   - A table block = consecutive lines starting with '|'
    #   - For prose blocks: apply recursive splitting (chunk_size)
    #   - For table blocks: keep whole (even if > chunk_size)
    #   - Return all chunks in document order
    raise NotImplementedError("TODO: implement table-aware chunking")


# ---------------------------------------------------------------------------
# Strategy 7: Sliding window with high overlap
# ---------------------------------------------------------------------------

def chunk_sliding_window(
    text: str,
    window_size: int = 1500,
    stride: int = 500,
) -> list[str]:
    """
    Fixed-size window with stride < window (high overlap for context).
    Overlap = window_size - stride.

    Like Strategy 1 but with much higher overlap ratio (default 67%).
    Useful when downstream retrieval benefits from redundant context.

    Returns a list of chunks.
    """
    # TODO: Implement sliding window chunking.
    #   - Start at position 0
    #   - Take window_size characters
    #   - Advance by stride
    #   - Repeat until end
    #   - Try to break at sentence boundaries within ±50 chars of the cut point
    raise NotImplementedError("TODO: implement sliding-window chunking")


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def get_all_strategies() -> dict[str, Callable[[str], list]]:
    """Return a dict mapping strategy names to their chunking functions."""
    return {
        "fixed_char": chunk_fixed_char,
        "fixed_token": chunk_fixed_token,
        "recursive": chunk_recursive,
        "markdown_headers": chunk_by_headers,
        "semantic": chunk_semantic,
        "table_aware": chunk_table_aware,
        "sliding_window": chunk_sliding_window,
    }
