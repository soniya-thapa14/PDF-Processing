"""
Tutorial 06 — Similarity search against the vector store

Embed a query and find the most similar chunks in Postgres.

Usage:
    uv run python tutorials/06-vector-store/search.py "What are zoning requirements?"
    uv run python tutorials/06-vector-store/search.py "revenue growth" --pdf financial_report
    uv run python tutorials/06-vector-store/search.py "kubectl apply" --strategy table_aware
"""

import sys
from pathlib import Path

import numpy as np


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "pdf_embeddings",
    "user": "tutorial",
    "password": "tutorial_pass",
}


def get_connection():
    """Connect to Postgres."""
    # TODO: Same as store_embeddings.py
    raise NotImplementedError("TODO: implement database connection")


def load_model():
    """Load the embedding model (same as Tutorial 05)."""
    # TODO: from sentence_transformers import SentenceTransformer
    #   return SentenceTransformer('all-MiniLM-L6-v2')
    raise NotImplementedError("TODO: load embedding model")


def search(
    query: str,
    top_k: int = 5,
    pdf_filter: str | None = None,
    strategy_filter: str | None = None,
) -> list[dict]:
    """
    Embed the query and find the top_k most similar chunks.

    Uses pgvector's <=> operator (cosine distance).
    Similarity = 1 - cosine_distance.

    Args:
        query: the search text
        top_k: number of results
        pdf_filter: if set, only search within this PDF's chunks
        strategy_filter: if set, only search chunks from this strategy

    Returns list of dicts:
        [{"chunk_text": "...", "similarity": 0.85, "pdf_name": "...", "strategy": "..."}, ...]
    """
    # TODO: Implement vector search:
    #   1. Embed the query with the model
    #   2. Build SQL:
    #      SELECT chunk_text, pdf_name, chunk_strategy,
    #             1 - (embedding <=> %(query_vec)s) AS similarity
    #      FROM pdf_chunks
    #      WHERE 1=1
    #        [AND pdf_name = %(pdf)s]
    #        [AND chunk_strategy = %(strategy)s]
    #      ORDER BY embedding <=> %(query_vec)s
    #      LIMIT %(top_k)s
    #   3. Execute and return results
    raise NotImplementedError("TODO: implement vector search")


def main():
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [--pdf NAME] [--strategy NAME] [--top_k N]")
        sys.exit(1)

    query = sys.argv[1]
    pdf_filter = None
    strategy_filter = None
    top_k = 5

    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--pdf" and i + 1 < len(args):
            pdf_filter = args[i + 1]
        elif arg == "--strategy" and i + 1 < len(args):
            strategy_filter = args[i + 1]
        elif arg == "--top_k" and i + 1 < len(args):
            top_k = int(args[i + 1])

    print(f"Query: '{query}'")
    if pdf_filter:
        print(f"Filter: pdf_name = '{pdf_filter}'")
    if strategy_filter:
        print(f"Filter: strategy = '{strategy_filter}'")
    print()

    results = search(query, top_k=top_k, pdf_filter=pdf_filter, strategy_filter=strategy_filter)

    for i, r in enumerate(results, 1):
        print(f"[{i}] similarity={r['similarity']:.4f}  pdf={r['pdf_name']}  strategy={r['strategy']}")
        print(f"    {r['chunk_text'][:120]}...")
        print()


if __name__ == "__main__":
    main()
