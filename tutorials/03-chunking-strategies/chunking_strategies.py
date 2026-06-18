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
import tiktoken
def chunk_fixed_token(text: str, chunk_size: int = 256, overlap: int = 50) -> list[str]:
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
