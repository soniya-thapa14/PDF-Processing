"""RAG pipeline: retrieve relevant chunks → format context → generate answer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "06-vector-store"))

from prompts import format_context, build_messages
import llm_client


def retrieve(query: str, top_k: int = 5, pdf_name: str = None, strategy: str = None) -> list[dict]:
    """Retrieve relevant chunks from the vector store.

    Args:
        query: natural language question
        top_k: number of chunks to retrieve
        pdf_name: optional filter by PDF name
        strategy: optional filter by chunking strategy

    Returns:
        List of dicts with chunk_text, pdf_name, chunk_strategy, similarity
    """
    from search import get_connection, load_model

    model = load_model()
    query_embedding = model.encode([query])[0]
    query_vec = "[" + ",".join(str(x) for x in query_embedding) + "]"

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            where_clauses = ["1=1"]
            params = {"query_vec": query_vec, "top_k": top_k}

            if pdf_name:
                where_clauses.append("pdf_name = %(pdf)s")
                params["pdf"] = pdf_name
            if strategy:
                where_clauses.append("chunk_strategy = %(strategy)s")
                params["strategy"] = strategy

            where_sql = " AND ".join(where_clauses)
            sql = f"""
                SELECT chunk_text, pdf_name, chunk_strategy, chunk_index,
                       1 - (embedding <=> %(query_vec)s::vector) AS similarity
                FROM pdf_chunks
                WHERE {where_sql}
                ORDER BY embedding <=> %(query_vec)s::vector
                LIMIT %(top_k)s
            """
            cur.execute(sql, params)
            rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "chunk_text": row[0],
                "pdf_name": row[1],
                "chunk_strategy": row[2],
                "chunk_index": row[3],
                "similarity": float(row[4]),
            })
        return results
    finally:
        conn.close()


def ask(
    question: str,
    top_k: int = 5,
    max_context_tokens: int = 3000,
    pdf_name: str = None,
    strategy: str = None,
    stream: bool = False,
    model: str = None,
):
    """Full RAG pipeline: retrieve → format → generate.

    Args:
        question: natural language question about the PDFs
        top_k: number of chunks to retrieve
        max_context_tokens: token budget for context
        pdf_name: optional filter by PDF source
        strategy: optional filter by chunking strategy
        stream: if True, returns a generator of answer chunks
        model: LLM model name override

    Returns:
        dict with keys: answer, sources, context_used
        (if stream=True, answer is a generator)
    """
    chunks = retrieve(query=question, top_k=top_k, pdf_name=pdf_name, strategy=strategy)

    if not chunks:
        return {
            "answer": "No relevant chunks found in the database. Make sure you've run the embedding pipeline (Tutorials 03-06).",
            "sources": [],
            "context_used": 0,
        }

    context = format_context(chunks, max_tokens=max_context_tokens)
    messages = build_messages(question, context)

    answer = llm_client.generate(messages, model=model, stream=stream)

    return {
        "answer": answer,
        "sources": chunks,
        "context_used": len(chunks),
    }
