"""
Tutorial 06 — Tests

    uv run pytest tutorials/06-vector-store/ -v

Note: These tests require Docker running with the postgres container.
Start it with: cd tutorials/06-vector-store && docker compose up -d
"""

import subprocess
import time

import pytest


def _postgres_running() -> bool:
    """Check if the postgres container is accepting connections."""
    try:
        result = subprocess.run(
            ["docker", "exec", "pdf_vectorstore", "pg_isready", "-U", "tutorial"],
            capture_output=True, timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


@pytest.fixture(scope="session", autouse=True)
def require_postgres():
    if not _postgres_running():
        pytest.skip("Postgres container not running. Start with: docker compose up -d")


def test_schema_creation():
    from store_embeddings import create_schema, get_connection
    create_schema()
    conn = get_connection()
    cur = conn.execute(
        "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'pdf_chunks')"
    )
    assert cur.fetchone()[0] is True
    conn.close()


def test_insert_and_query():
    import numpy as np
    from store_embeddings import get_connection, create_schema

    create_schema()
    conn = get_connection()

    test_embedding = np.random.randn(384).astype(np.float32)
    embedding_str = "[" + ",".join(str(x) for x in test_embedding) + "]"

    conn.execute(
        """
        INSERT INTO pdf_chunks (pdf_name, chunk_strategy, chunk_index, chunk_text, embedding)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        """,
        ("test_pdf", "test_strategy", 0, "This is a test chunk.", embedding_str),
    )
    conn.commit()

    cur = conn.execute("SELECT COUNT(*) FROM pdf_chunks WHERE pdf_name = 'test_pdf'")
    count = cur.fetchone()[0]
    assert count >= 1, "should have inserted at least one row"

    conn.execute("DELETE FROM pdf_chunks WHERE pdf_name = 'test_pdf'")
    conn.commit()
    conn.close()


def test_vector_search():
    import numpy as np
    from store_embeddings import get_connection, create_schema

    create_schema()
    conn = get_connection()

    np.random.seed(42)
    target = np.random.randn(384).astype(np.float32)
    similar = target + np.random.randn(384).astype(np.float32) * 0.1
    dissimilar = np.random.randn(384).astype(np.float32)

    for i, (emb, text) in enumerate([
        (target, "target chunk"),
        (similar, "similar chunk"),
        (dissimilar, "dissimilar chunk"),
    ]):
        emb_str = "[" + ",".join(str(x) for x in emb) + "]"
        conn.execute(
            """
            INSERT INTO pdf_chunks (pdf_name, chunk_strategy, chunk_index, chunk_text, embedding)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            ("search_test", "test", i, text, emb_str),
        )
    conn.commit()

    query_str = "[" + ",".join(str(x) for x in target) + "]"
    cur = conn.execute(
        """
        SELECT chunk_text, 1 - (embedding <=> %s::vector) AS similarity
        FROM pdf_chunks
        WHERE pdf_name = 'search_test'
        ORDER BY embedding <=> %s::vector
        LIMIT 3
        """,
        (query_str, query_str),
    )
    results = cur.fetchall()
    assert results[0][0] == "target chunk", "most similar should be itself"
    assert results[1][0] == "similar chunk", "second should be the similar one"
    assert results[0][1] > results[2][1], "target should be more similar than dissimilar"

    conn.execute("DELETE FROM pdf_chunks WHERE pdf_name = 'search_test'")
    conn.commit()
    conn.close()
