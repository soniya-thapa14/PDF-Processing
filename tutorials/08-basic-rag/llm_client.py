"""Thin wrapper around an OpenAI-compatible LLM API.

Supports any LLM that exposes an OpenAI-compatible chat completions endpoint:
- OpenAI models (gpt-4o, gpt-4o-mini, etc.)
- Local models via Ollama (llama3, mistral, phi3, etc.)
- Anthropic via proxy (if using an OpenAI-compatible wrapper)
- Together, Groq, Fireworks, or any other OpenAI-compatible provider

Configuration is entirely via environment variables — no model is hardcoded.
"""

import os
from openai import OpenAI


DEFAULT_MODEL = os.getenv("RAG_MODEL", "")
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
        model: model name (defaults to RAG_MODEL env var — MUST be set)
        stream: if True, returns a generator of content deltas
        **kwargs: passed through to the API (temperature, max_tokens, etc.)

    Returns:
        If stream=False: the assistant's reply as a string
        If stream=True: a generator yielding content chunks

    Raises:
        ValueError: if no model is configured
    """
    client = get_client()
    model = model or DEFAULT_MODEL

    if not model:
        raise ValueError(
            "No model configured. Set the RAG_MODEL environment variable.\n"
            "Examples:\n"
            "  export RAG_MODEL=llama3          # for Ollama\n"
            "  export RAG_MODEL=gpt-4o-mini     # for OpenAI\n"
            "  export RAG_MODEL=mistral         # for Ollama/Mistral\n"
        )

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
