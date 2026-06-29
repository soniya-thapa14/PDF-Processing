"""Hybrid search: combine vector search + keyword search using Reciprocal Rank Fusion."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "07-basic-rag"))
sys.path.insert(0, str(Path(__file__).parent))

from rag_pipeline import retrieve as vector_search
from keyword_search import keyword_search


RRF_K = 60  # standard RRF constant


def reciprocal_rank_fusion(
    ranked_lists: list[list[dict]],
    k: int = RRF_K,
    id_key: str = None,
) -> list[dict]:
    """Merge multiple ranked lists using Reciprocal Rank Fusion.

    RRF_score(doc) = sum(1 / (k + rank_i)) for each list i where doc appears.

    Args:
        ranked_lists: list of ranked result lists (each item is a dict)
        k: RRF constant (default 60)
        id_key: not used; items are matched by (pdf_name, chunk_index)

    Returns:
        Merged list sorted by RRF score descending
    """
    scores = {}
    items = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, 1):
            doc_id = (item["pdf_name"], item["chunk_index"])
            if doc_id not in scores:
                scores[doc_id] = 0.0
                items[doc_id] = item
            scores[doc_id] += 1.0 / (k + rank)

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    results = []
    for doc_id, score in sorted_docs:
        item = items[doc_id].copy()
        item["rrf_score"] = score
        results.append(item)

    return results


def hybrid_search(
    query: str,
    top_k: int = 5,
    vector_k: int = 20,
    keyword_k: int = 20,
    pdf_name: str = None,
    strategy: str = None,
) -> list[dict]:
    """Run hybrid search combining vector and keyword retrieval.

    Args:
        query: search query
        top_k: final number of results to return
        vector_k: number of vector search candidates
        keyword_k: number of keyword search candidates
        pdf_name: optional PDF filter
        strategy: optional strategy filter

    Returns:
        Top-k results after RRF fusion
    """
    vector_results = vector_search(
        query=query, top_k=vector_k, pdf_name=pdf_name, strategy=strategy
    )
    keyword_results = keyword_search(
        query=query, top_k=keyword_k, pdf_name=pdf_name, strategy=strategy
    )

    fused = reciprocal_rank_fusion([vector_results, keyword_results])
    return fused[:top_k]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hybrid search (vector + keyword)")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--pdf", help="Filter by PDF name")
    args = parser.parse_args()

    print(f"Hybrid search: '{args.query}'\n")
    results = hybrid_search(args.query, top_k=args.top_k, pdf_name=args.pdf)

    for i, r in enumerate(results, 1):
        print(f"[{i}] rrf={r['rrf_score']:.4f}  pdf={r['pdf_name']}  "
              f"strategy={r['chunk_strategy']}  chunk={r['chunk_index']}")
        print(f"    {r['chunk_text'][:120]}...")
        print()


if __name__ == "__main__":
    main()
