"""Two-stage retrieval pipeline: broad recall → precise reranking → LLM generation."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "10-hybrid-search"))
sys.path.insert(0, str(Path(__file__).parent.parent / "08-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent))

from hybrid_search import hybrid_search
from reranker import rerank
from prompts import format_context, build_messages
import llm_client


def ask_with_reranking(
    question: str,
    retrieve_k: int = 50,
    rerank_k: int = 5,
    max_context_tokens: int = 3000,
    pdf_name: str = None,
    strategy: str = None,
    stream: bool = False,
    threshold: float = None,
):
    """Full two-stage RAG pipeline.

    Stage 1: Hybrid search retrieves top-`retrieve_k` candidates (fast, broad recall)
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
        dict with answer, sources, timings
    """
    t0 = time.time()

    candidates = hybrid_search(
        query=question, top_k=retrieve_k, pdf_name=pdf_name, strategy=strategy
    )
    t_retrieve = time.time() - t0

    t1 = time.time()
    reranked = rerank(question, candidates, top_k=rerank_k, threshold=threshold)
    t_rerank = time.time() - t1

    if not reranked:
        return {
            "answer": "No sufficiently relevant chunks found after reranking.",
            "sources": [],
            "timings": {"retrieve_ms": t_retrieve * 1000, "rerank_ms": t_rerank * 1000},
        }

    context = format_context(reranked, max_tokens=max_context_tokens)
    messages = build_messages(question, context)

    t2 = time.time()
    answer = llm_client.generate(messages, stream=stream)
    t_generate = time.time() - t2

    return {
        "answer": answer,
        "sources": reranked,
        "candidates_count": len(candidates),
        "reranked_count": len(reranked),
        "timings": {
            "retrieve_ms": round(t_retrieve * 1000),
            "rerank_ms": round(t_rerank * 1000),
            "generate_ms": round(t_generate * 1000),
            "total_ms": round((time.time() - t0) * 1000),
        },
    }


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
    print("\nSources:")
    for i, s in enumerate(result["sources"], 1):
        print(f"  [{i}] rerank_score={s.get('rerank_score', 0):.3f}  "
              f"pdf={s['pdf_name']}  chunk={s['chunk_index']}")


if __name__ == "__main__":
    main()
