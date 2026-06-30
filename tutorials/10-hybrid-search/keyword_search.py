"""Keyword search using Postgres full-text search (BM25-like ranking)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "06-vector-store"))
from store_embeddings import get_connection


SCHEMA_FTS = Path(__file__).parent / "schema_fts.sql"


def init_fts():
    """Apply the full-text search schema migration."""
    sql = SCHEMA_FTS.read_text()
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print("Full-text search schema applied successfully.")
    finally:
        conn.close()


def keyword_search(
    query: str,
    top_k: int = 10,
    pdf_name: str = None,
    strategy: str = None,
) -> list[dict]:
    """Search chunks using Postgres full-text search.

    Converts the query to a tsquery and ranks results using ts_rank.

    Args:
        query: natural language search query
        top_k: number of results to return
        pdf_name: optional PDF filter
        strategy: optional strategy filter

    Returns:
        List of dicts with chunk_text, pdf_name, chunk_strategy, rank
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            where_clauses = ["tsv @@ plainto_tsquery('english', %(query)s)"]
            params = {"query": query, "top_k": top_k}

            if pdf_name:
                where_clauses.append("pdf_name = %(pdf)s")
                params["pdf"] = pdf_name
            if strategy:
                where_clauses.append("chunk_strategy = %(strategy)s")
                params["strategy"] = strategy

            where_sql = " AND ".join(where_clauses)
            sql = f"""
                SELECT chunk_text, pdf_name, chunk_strategy, chunk_index,
                       ts_rank(tsv, plainto_tsquery('english', %(query)s)) AS rank
                FROM pdf_chunks
                WHERE {where_sql}
                ORDER BY rank DESC
                LIMIT %(top_k)s
            """
            cur.execute(sql, params)
            rows = cur.fetchall()

        return [
            {
                "chunk_text": row[0],
                "pdf_name": row[1],
                "chunk_strategy": row[2],
                "chunk_index": row[3],
                "rank": float(row[4]),
            }
            for row in rows
        ]
    finally:
        conn.close()


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
