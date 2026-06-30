"""
Tutorial 06 — Store embeddings in Postgres (pgvector)

Reads .npy embedding files from Tutorial 05 and inserts them into Postgres.

Usage:
    uv run python tutorials/06-vector-store/store_embeddings.py          # insert all
    uv run python tutorials/06-vector-store/store_embeddings.py --init   # create schema only
"""

import json
import sys
from pathlib import Path

import numpy as np

EMBEDDINGS_DIR = Path(__file__).parent.parent / "05-embeddings-math" / "results"
CHUNKS_DIR = Path(__file__).parent.parent / "03-chunking-strategies" / "results" / "chunks"

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


def create_schema():
    schema_path = Path(__file__).parent / "schema.sql"
    sql = schema_path.read_text()

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()


def insert_embeddings():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            for npy_path in EMBEDDINGS_DIR.glob("*.npy"):
                pdf_name, chunk_strategy = npy_path.stem.split("__")
                embeddings = np.load(npy_path)
                chunks = json.loads((CHUNKS_DIR / f"{npy_path.stem}.json").read_text())["chunks"]

                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    chunk_text = chunk["content"]
                    cur.execute("INSERT INTO pdf_chunks (pdf_name, chunk_strategy, chunk_index, chunk_text, embedding) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                                (pdf_name, chunk_strategy, i, chunk_text, embedding.tolist()))
        conn.commit()
        print(f"\nInserted chunks successfully")
    finally:
        conn.close()
           
def get_stats():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM pdf_chunks")
            total = cur.fetchone()[0]
            print(f"Total rows: {total}")
            cur.execute("SELECT DISTINCT pdf_name FROM pdf_chunks")
            pdf_names = cur.fetchall()
            print(f"PDFS: {pdf_names}")
            cur.execute("SELECT DISTINCT chunk_strategy FROM pdf_chunks")
            strategies = cur.fetchall()
            print(f"strategies: {strategies}")
            cur.execute("SELECT pdf_name, chunk_strategy, COUNT(*) FROM pdf_chunks GROUP BY pdf_name, chunk_strategy")
            rows = cur.fetchall()
            print(f"Rows per (pdf, strategy): {rows}")    
    finally:
        conn.close()

def main():
    if "--init" in sys.argv:
        print("Creating schema...")
        create_schema()
        print("Schema created.")
        return

    print("=" * 60)
    print("STORE EMBEDDINGS IN POSTGRES")
    print("=" * 60)

    print("\n1. Ensuring schema exists...")
    create_schema()

    print("\n2. Inserting embeddings...")
    insert_embeddings()

    print("\n3. Database stats:")
    get_stats()


if __name__ == "__main__":
    main()
    