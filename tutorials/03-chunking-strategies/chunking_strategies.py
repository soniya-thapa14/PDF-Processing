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
    chunks = []
    start = 0
    stride = chunk_size - overlap

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk:
            chunks.append(chunk)
        start += stride
    return chunks


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
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    chunks = []
    stride =chunk_size - overlap
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        window = tokens[start:end]
        chunks.append(enc.decode(window))
        start += stride
    return chunks

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
    if separators is None:
        separators = ["\n\n", "\n", ". ", " "]

    def _split(text: str, seps: list[str]) -> list[str]:
        if not text:
            return []
        
        if len(text) <= chunk_size:
            return[text]
        
        if not seps:
            return [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        sep = seps[0]
        pieces = text.split(sep)

        result = []
        for piece in pieces:
            if not piece.strip():
                continue
            if len(piece) <= chunk_size:
                result.append(piece)
            else:
                result.extend(_split(piece, seps[1:]))

        merged = []
        buffer = ""
        for piece in result:
            candidate = (buffer + sep + piece).strip() if buffer else piece
            if len(candidate) <= chunk_size:
                buffer = candidate
            else:
                if buffer:
                    merged.append(buffer)
                buffer = piece

        if buffer:
            merged.append(buffer)
        
        return merged
    return _split(text, separators)

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

    chunks = []
    current_heading = None
    current_level = 0
    current_lines = []

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)", line)
        if match:
            content = "\n".join(current_lines).strip()
            if content or current_heading is not None:
                chunks.append({
                    "heading": current_heading,
                    "level": current_level,
                    "content": content,
                })
            current_level = len(match.group(1))
            current_heading = match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    content = "\n".join(current_lines).strip()
    if content or current_heading is not None:
        chunks.append({
            "heading": current_heading,
            "level": current_level,
            "content": content,
        })
    return chunks

# ---------------------------------------------------------------------------
# Strategy 5: Semantic chunking
# ---------------------------------------------------------------------------

from sentence_transformers import SentenceTransformer
import numpy as np

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
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if s.strip()]

    if len(sentences) <= 1:
        return sentences
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences, convert_to_numpy=True)

    def cosine_sim(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))
    
    similarities = [cosine_sim(embeddings[i], embeddings[i + 1]) for i in range(len(embeddings) - 1)]

    break_points = {i +1 for i, sim in enumerate(similarities) if sim < threshold}

    chunks = []
    current = []
    for i, sentence in enumerate(sentences):
        if i in break_points and current:
            chunks.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))

    merged = []
    for chunk in chunks:
        if merged and len(chunk) < min_chunk_size:
            merged[-1] = merged[-1] + " " + chunk
        else:
            merged.append(chunk)

    return merged
   


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
    lines = text.splitlines(keepends = True)

    segments = []
    buffer = []
    in_table = False

    def is_table_line(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("|")
    
    for line in lines:
        if is_table_line(line):
            if not in_table:
                if buffer:
                    segments.append(("prose", "".join(buffer)))
                    buffer = []
                in_table = True
            buffer.append(line)
        else:
            if in_table:
                segments.append(("table", "".join(buffer)))
                buffer = []
                in_table = False
            buffer.append(line)
    if buffer:
        seg_type = "table" if in_table else "prose"
        segments.append((seg_type, "".join(buffer)))
    chunks = []
    for seg_type, seg_text in segments:
        if not seg_text:
            continue
        if seg_type == "table":
            chunks.append(seg_text)
        else:
            chunks.append(chunk_recursive(seg_text, chunk_size=chunk_size))
    return chunks

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

    chunks = []
    start = 0

    while start < len(text):
        end = start + window_size

        if end < len(text):
            search_start = max(end - 50, start)
            search_end = min(end + 50, len(text))
            segment = text[search_start:search_end]
            match = None
            for m in re.finditer(R"[.!?]\s", segment):
                match =m
            if match:
                end = search_start + match.end()
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)

        start += stride
    return chunks


   


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
