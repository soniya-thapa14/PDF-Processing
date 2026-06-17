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
    """
    Connect to the Postgres database.

    Returns a psycopg connection.
    """
    # TODO: Use psycopg to connect with DB_CONFIG
    #   import psycopg
    #   return psycopg.connect(**DB_CONFIG)
    raise NotImplementedError("TODO: implement database connection")


def create_schema():
    """
    Create the pdf_chunks table and indexes (idempotent).
    Reads schema.sql and executes it.
    """
    # TODO: Read schema.sql, execute it via get_connection()
    #   schema_path = Path(__file__).parent / "schema.sql"
    #   sql = schema_path.read_text()
    #   conn = get_connection()
    #   conn.execute(sql)
    #   conn.commit()
    raise NotImplementedError("TODO: implement schema creation")


def insert_embeddings():
    """
    Load .npy files from Tutorial 05 and corresponding chunk texts from Tutorial 03.
    Insert each chunk + embedding as a row in pdf_chunks.
    """
    # TODO: Implement insertion logic:
    #   1. List all .npy files in EMBEDDINGS_DIR
    #   2. For each .npy file:
    #      - Parse pdf_name and chunk_strategy from filename (format: "{pdf}__{strategy}.npy")
    #      - Load embeddings: np.load(npy_path)
    #      - Load chunk texts from corresponding JSON in CHUNKS_DIR
    #      - For each (index, chunk_text, embedding):
    #        INSERT INTO pdf_chunks (pdf_name, chunk_strategy, chunk_index, chunk_text, embedding)
    #        VALUES (%s, %s, %s, %s, %s)
    #        ON CONFLICT DO NOTHING
    #   3. Commit and report count
    raise NotImplementedError("TODO: implement embedding insertion")


def get_stats():
    """Print database statistics."""
    # TODO: Query and print:
    #   - Total rows in pdf_chunks
    #   - Distinct pdf_names
    #   - Distinct strategies
    #   - Row count per (pdf_name, strategy)
    raise NotImplementedError("TODO: implement stats query")


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
