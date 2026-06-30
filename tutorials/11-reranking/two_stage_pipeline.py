"""
Tutorial 11 — Two-Stage Retrieval Pipeline

Retrieve broadly (top-50 via hybrid search) → rerank to top-5 → generate answer.

Usage:
    uv run python tutorials/11-reranking/two_stage_pipeline.py --query "What is attention?"

Implement the functions marked # TODO.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "10-hybrid-search"))
sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent))


def ask_with_reranking(
    question: str,
    retrieve_k: int = 50,
    rerank_k: int = 5,
    max_context_tokens: int = 3000,
    pdf_name: str = None,
    strategy: str = None,
    stream: bool = False,
    threshold: float = None,
) -> dict:
    """
    Full two-stage RAG pipeline: retrieve → rerank → generate.

    Stage 1: Hybrid search retrieves top-`retrieve_k` candidates (fast, broad)
    Stage 2: Cross-encoder reranks to top-`rerank_k` (slow, precise)
    Stage 3: LLM generates answer from reranked context

    Args:
        question: user's question
        retrieve_k: candidates from first-stage retrieval
        rerank_k: final chunks after reranking
        max_context_tokens: token budget for LLM context
        pdf_name: optional PDF filter
        strategy: optional strategy filter
        stream: stream LLM response
        threshold: minimum rerank score to include

    Returns:
        dict with keys:
        - answer: the generated response
        - sources: reranked chunk dicts
        - candidates_count: how many first-stage results
        - reranked_count: how many survived reranking
        - timings: dict with retrieve_ms, rerank_ms, generate_ms, total_ms
    """
    # TODO: Implement two-stage pipeline.
    #   - Time each stage using time.time()
    #   - Stage 1: hybrid_search(query=question, top_k=retrieve_k, ...)
    #   - Stage 2: rerank(question, candidates, top_k=rerank_k, threshold=threshold)
    #   - Stage 3: format_context → build_messages → generate
    #   - Return dict with answer, sources, timings
    raise NotImplementedError("TODO: implement ask_with_reranking")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Two-stage RAG with reranking")
    parser.add_argument("--query", "-q", required=True)
    parser.add_argument("--retrieve-k", type=int, default=50)
    parser.add_argument("--rerank-k", type=int, default=5)
    parser.add_argument("--pdf", help="Filter by PDF")
    parser.add_argument("--threshold", type=float, help="Min rerank score")
    args = parser.parse_args()

    result = ask_with_reranking(
        args.query,
        retrieve_k=args.retrieve_k,
        rerank_k=args.rerank_k,
        pdf_name=args.pdf,
        threshold=args.threshold,
    )

    print(f"Question: {args.query}\n")
    print(f"Answer: {result['answer']}\n")
    print(f"Timings: {result['timings']}")
    print(f"Candidates: {result.get('candidates_count', 0)} → Reranked: {result.get('reranked_count', 0)}")


if __name__ == "__main__":
    main()
