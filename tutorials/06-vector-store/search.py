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
    import psycopg2
    return psycopg2.connect(**DB_CONFIG)

def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

def search(
    query: str,
    top_k: int = 5,
    pdf_filter: str | None = None,
    strategy_filter: str | None = None,
) -> list[dict]:
    model = load_model()
    query_vec = model.encode(query).tolist()
    sql = """
        SELECT chunk_text, pdf_name, chunk_strategy,
            1 - (embedding <=> CAST(%(query_vec)s AS vector)) AS similarity
        FROM pdf_chunks
        WHERE 1=1
    """
    params = {"query_vec": query_vec, "top_k": top_k}

    if pdf_filter:
        sql += " AND pdf_name = %(pdf)s "
        params["pdf"] = pdf_filter

    if strategy_filter:
        sql += " AND chunk_strategy = %(strategy)s "
        params["strategy"] = strategy_filter
    
    sql += "ORDER BY embedding <=> CAST(%(query_vec)s AS vector) LIMIT %(top_k)s"

    conn =  None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    finally:
        if conn:
            conn.close()
    return [
        {"chunk_text": row[0], "pdf_name": row[1], "strategy": row[2], "similarity": row[3]}
        for row in rows
    ]




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
        print(f"    {r['chunk_text']}...")
        print()


if __name__ == "__main__":
    main()
