"""Prompt templates for RAG pipeline."""


SYSTEM_PROMPT = """You are a helpful assistant that answers questions based ONLY on the provided context chunks from PDF documents.

Rules:
1. Answer the question using ONLY information from the context below.
2. If the context does not contain enough information, say "I don't have enough information in the provided documents to answer this."
3. Cite your sources using [Source N] notation, where N corresponds to the chunk number.
4. Be concise but thorough.
5. If multiple chunks support the answer, cite all relevant ones.
"""


def format_context(chunks: list[dict], max_tokens: int = 3000) -> str:
    """Format retrieved chunks into a context string for the prompt.

    Each chunk is numbered and includes its source metadata.
    Respects an approximate token budget (4 chars ≈ 1 token).

    Args:
        chunks: list of dicts with keys: chunk_text, pdf_name, chunk_strategy, similarity
        max_tokens: approximate token budget for context

    Returns:
        Formatted context string
    """
    max_chars = max_tokens * 4
    context_parts = []
    total_chars = 0

    for i, chunk in enumerate(chunks, 1):
        text = chunk["chunk_text"]
        pdf = chunk.get("pdf_name", "unknown")
        strategy = chunk.get("chunk_strategy", "unknown")
        sim = chunk.get("similarity", 0.0)

        header = f"[Source {i}] (PDF: {pdf}, Strategy: {strategy}, Relevance: {sim:.2f})"
        entry = f"{header}\n{text}\n"

        if total_chars + len(entry) > max_chars:
            remaining = max_chars - total_chars
            if remaining > 200:
                entry = f"{header}\n{text[:remaining - len(header) - 10]}...\n"
                context_parts.append(entry)
            break

        context_parts.append(entry)
        total_chars += len(entry)

    return "\n---\n".join(context_parts)


def build_messages(question: str, context: str) -> list[dict]:
    """Build the full message list for the LLM call.

    Args:
        question: the user's question
        context: formatted context string from format_context()

    Returns:
        List of message dicts ready for the LLM
    """
    user_content = f"""Context from documents:

{context}

---

Question: {question}

Please answer based on the context above, citing sources with [Source N] notation."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
