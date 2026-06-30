"""
Tutorial 08 — RAG Pipeline

Orchestrates the full retrieve → format → generate flow.

Usage:
    from rag_pipeline import ask
    result = ask("What are the setback requirements?")
    print(result["answer"])

Implement the functions marked # TODO.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "06-vector-store"))


def retrieve(query: str, top_k: int = 5, pdf_name: str = None, strategy: str = None) -> list[dict]:
    """
    Retrieve relevant chunks from the vector store (Tutorial 06).

    Steps:
    1. Load the embedding model (from Tutorial 06's search module)
    2. Encode the query into a vector
    3. Query Postgres for nearest neighbors using cosine distance
    4. Apply optional filters (pdf_name, strategy)

    Args:
        query: natural language question
        top_k: number of chunks to retrieve
        pdf_name: optional filter by PDF name
        strategy: optional filter by chunking strategy

    Returns:
        List of dicts with: chunk_text, pdf_name, chunk_strategy, chunk_index, similarity
    """
    # TODO: Implement retrieval.
    #   - Import get_connection, load_model from Tutorial 06's search module
    #   - Encode query with the model
    #   - Format vector as Postgres-compatible string: "[0.1,0.2,...]"
    #   - Build SQL query:
    #       SELECT chunk_text, pdf_name, chunk_strategy, chunk_index,
    #              1 - (embedding <=> %(vec)s::vector) AS similarity
    #       FROM pdf_chunks
    #       WHERE [optional filters]
    #       ORDER BY embedding <=> %(vec)s::vector
    #       LIMIT %(top_k)s
    #   - Execute and return results as list of dicts
    raise NotImplementedError("TODO: implement retrieve")


def ask(
    question: str,
    top_k: int = 5,
    max_context_tokens: int = 3000,
    pdf_name: str = None,
    strategy: str = None,
    stream: bool = False,
    model: str = None,
) -> dict:
    """
    Full RAG pipeline: retrieve → format → generate.

    Steps:
    1. Call retrieve() to get relevant chunks
    2. Call format_context() to fit chunks into token budget
    3. Call build_messages() to assemble the prompt
    4. Call generate() to get the LLM response

    Args:
        question: natural language question about the PDFs
        top_k: number of chunks to retrieve
        max_context_tokens: token budget for context
        pdf_name: optional filter by PDF source
        strategy: optional filter by chunking strategy
        stream: if True, answer is a generator of chunks
        model: LLM model name override

    Returns:
        dict with keys:
        - answer: string (or generator if stream=True)
        - sources: list of chunk dicts from retrieval
        - context_used: number of chunks that fit in context
    """
    # TODO: Implement the full pipeline.
    #   - Call retrieve(query=question, top_k=top_k, ...)
    #   - If no chunks found, return message saying so
    #   - Call format_context(chunks, max_tokens=max_context_tokens)
    #   - Call build_messages(question, context)
    #   - Call generate(messages, model=model, stream=stream)
    #   - Return dict with answer, sources, context_used
    raise NotImplementedError("TODO: implement ask")
