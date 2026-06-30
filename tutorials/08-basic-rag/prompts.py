"""
Tutorial 08 — Prompt Templates for RAG

System and user prompt templates that keep the LLM grounded in retrieved context.

Usage:
    from prompts import format_context, build_messages
    ctx = format_context(chunks, max_tokens=3000)
    msgs = build_messages("What is attention?", ctx)

Implement the functions marked # TODO.
"""

from __future__ import annotations


SYSTEM_PROMPT = """You are a helpful assistant that answers questions based ONLY on the provided context chunks from PDF documents.

Rules:
1. Answer the question using ONLY information from the context below.
2. If the context does not contain enough information, say "I don't have enough information in the provided documents to answer this."
3. Cite your sources using [Source N] notation, where N corresponds to the chunk number.
4. Be concise but thorough.
5. If multiple chunks support the answer, cite all relevant ones.
"""


def format_context(chunks: list[dict], max_tokens: int = 3000) -> str:
    """
    Format retrieved chunks into a numbered context string for the prompt.

    Each chunk gets a header like: [Source 1] (PDF: name, Strategy: x, Relevance: 0.95)
    Followed by the chunk text.

    Must respect an approximate token budget (4 chars ≈ 1 token).
    Stop adding chunks when the budget would be exceeded.
    If the last chunk partially fits, truncate it with "...".

    Args:
        chunks: list of dicts with keys: chunk_text, pdf_name, chunk_strategy, similarity
        max_tokens: approximate token budget for the entire context

    Returns:
        Formatted context string with numbered sources separated by "---"
    """
    # TODO: Implement context formatting.
    #   - Convert max_tokens to max_chars (multiply by 4)
    #   - Iterate chunks, numbering from 1
    #   - For each chunk, build a header with metadata and the text
    #   - Track total characters used
    #   - Stop when adding next chunk would exceed budget
    #   - Join chunks with "\n---\n" separator
    raise NotImplementedError("TODO: implement format_context")


def build_messages(question: str, context: str) -> list[dict]:
    """
    Build the full message list for the LLM call.

    Structure:
    - messages[0]: system message with SYSTEM_PROMPT
    - messages[1]: user message containing context + question + citation instruction

    The user message should include:
    - "Context from documents:" followed by the context string
    - "---" separator
    - "Question:" followed by the question
    - Instruction to cite sources with [Source N] notation

    Args:
        question: the user's question
        context: formatted context string from format_context()

    Returns:
        List of message dicts: [{"role": "system", ...}, {"role": "user", ...}]
    """
    # TODO: Implement message assembly.
    #   - Create system message with SYSTEM_PROMPT
    #   - Create user message combining context + question + citation instruction
    #   - Return list of both messages
    raise NotImplementedError("TODO: implement build_messages")
