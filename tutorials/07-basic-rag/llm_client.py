"""Thin wrapper around an OpenAI-compatible LLM API.

Supports:
- OpenAI (default)
- Local models via Ollama (set OPENAI_BASE_URL=http://localhost:11434/v1)
- Any OpenAI-compatible endpoint (Together, Groq, etc.)
"""

import os
from openai import OpenAI


DEFAULT_MODEL = os.getenv("RAG_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("OPENAI_BASE_URL", None)


def get_client() -> OpenAI:
    kwargs = {}
    if BASE_URL:
        kwargs["base_url"] = BASE_URL
    if not os.getenv("OPENAI_API_KEY") and BASE_URL:
        kwargs["api_key"] = "not-needed"
    return OpenAI(**kwargs)


def generate(messages: list[dict], model: str = None, stream: bool = False, **kwargs):
    """Call the LLM with a list of messages.

    Args:
        messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
        model: model name (defaults to RAG_MODEL env var or gpt-4o-mini)
        stream: if True, returns a generator of content deltas
        **kwargs: passed through to the API (temperature, max_tokens, etc.)

    Returns:
        If stream=False: the assistant's reply as a string
        If stream=True: a generator yielding content chunks
    """
    client = get_client()
    model = model or DEFAULT_MODEL

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
        **kwargs,
    )

    if stream:
        return _stream_content(response)
    return response.choices[0].message.content


def _stream_content(response):
    """Yield content deltas from a streaming response."""
    for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content
