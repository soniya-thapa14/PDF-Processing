"""
Tutorial 10 — Keyword Search using Postgres Full-Text Search

BM25-style search using Postgres tsvector and ts_rank.

Usage:
    uv run python tutorials/10-hybrid-search/keyword_search.py --init
    uv run python tutorials/10-hybrid-search/keyword_search.py --query "R-1 zone"

Implement the functions marked # TODO.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "06-vector-store"))

SCHEMA_FTS = Path(__file__).parent / "schema_fts.sql"


def init_fts():
    """
    Apply the full-text search schema migration (schema_fts.sql).

    Reads the SQL file and executes it against the database.
    This adds the tsvector column, GIN index, and trigger.
    """
    # TODO: Implement FTS initialization.
    #   - Import get_connection from Tutorial 06's store_embeddings
    #   - Read SCHEMA_FTS file
    #   - Execute the SQL and commit
    raise NotImplementedError("TODO: implement init_fts")


def keyword_search(
    query: str,
    top_k: int = 10,
    pdf_name: str = None,
    strategy: str = None,
) -> list[dict]:
    """
    Search chunks using Postgres full-text search.

    Uses plainto_tsquery to convert natural language to a tsquery,
    then ranks results using ts_rank.

    Args:
        query: natural language search query
        top_k: number of results to return
        pdf_name: optional PDF filter
        strategy: optional strategy filter

    Returns:
        List of dicts with: chunk_text, pdf_name, chunk_strategy, chunk_index, rank
    """
    # TODO: Implement keyword search.
    #   - Import get_connection from Tutorial 06
    #   - Build WHERE clause: tsv @@ plainto_tsquery('english', query)
    #   - Add optional filters for pdf_name and strategy
    #   - SELECT with ts_rank(tsv, plainto_tsquery(...)) AS rank
    #   - ORDER BY rank DESC, LIMIT top_k
    #   - Return results as list of dicts
    raise NotImplementedError("TODO: implement keyword_search")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Keyword search on PDF chunks")
    parser.add_argument("--init", action="store_true", help="Apply FTS schema")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--pdf", help="Filter by PDF name")
    args = parser.parse_args()

    if args.init:
        init_fts()
        return

    if not args.query:
        print("Provide --query or --init")
        return

    results = keyword_search(args.query, top_k=args.top_k, pdf_name=args.pdf)
    for i, r in enumerate(results, 1):
        print(f"[{i}] rank={r['rank']:.4f}  pdf={r['pdf_name']}  strategy={r['chunk_strategy']}")
        print(f"    {r['chunk_text'][:120]}...")
        print()


if __name__ == "__main__":
    main()
