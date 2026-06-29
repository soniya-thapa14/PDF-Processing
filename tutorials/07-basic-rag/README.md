# Tutorial 07 — Basic RAG (Retrieval-Augmented Generation)

## Goal

Wire the vector store from Tutorial 06 to an LLM. Ask a natural-language
question about your PDFs, retrieve the most relevant chunks, and generate
a grounded answer with source citations.

## Pipeline

```
User Question
      │
      ▼
┌─────────────┐
│  Retrieve   │  ← vector search (Tutorial 06)
│  top-k      │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  Format     │  ← fit chunks into prompt within token budget
│  Context    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  Generate   │  ← LLM call with system prompt + context + question
│  Answer     │
└─────┬───────┘
      │
      ▼
Answer + Citations
```

## Key Concepts

1. **Prompt Engineering for RAG** — Structure the prompt so the LLM knows to
   answer only from the provided context and cite its sources.
2. **Token Budget Management** — Chunks vary in size; we must fit as many
   relevant chunks as possible within the model's context window.
3. **Source Attribution** — Each chunk carries metadata (pdf_name, strategy,
   chunk_index). The generated answer references which source it drew from.
4. **Streaming** — For long answers, stream tokens to the user as they arrive.

## Files

| File | Purpose |
|------|---------|
| `llm_client.py` | Thin wrapper around OpenAI-compatible API |
| `prompts.py` | System and user prompt templates |
| `rag_pipeline.py` | Orchestrates retrieve → format → generate |
| `demo.py` | Interactive CLI to ask questions about your PDFs |
| `test_tutorial7.py` | Unit tests |

## Setup

```bash
# From the repo root
uv add openai

# Set your API key (or use a local model via Ollama)
export OPENAI_API_KEY="sk-..."

# Or for Ollama (no key needed):
export OPENAI_BASE_URL="http://localhost:11434/v1"
export RAG_MODEL="llama3"
```

## Usage

```bash
# Interactive mode
uv run python tutorials/07-basic-rag/demo.py

# Single question
uv run python tutorials/07-basic-rag/demo.py --query "What are the setback requirements for R-1 zones?"

# With specific PDF filter
uv run python tutorials/07-basic-rag/demo.py --query "Explain attention mechanism" --pdf research_textbook
```

## Tasks

1. Read `llm_client.py` — understand how the OpenAI SDK is configured
2. Read `prompts.py` — study the system prompt structure
3. Read `rag_pipeline.py` — trace the retrieve → format → generate flow
4. Run `demo.py` and ask questions about different PDFs
5. Experiment: change `top_k`, `max_context_tokens`, or the system prompt
6. Observe: which chunking strategy produces better answers?

## Check Your Work

- [ ] Can ask a question and get a grounded answer
- [ ] Answer includes `[Source: pdf_name, chunk N]` citations
- [ ] Changing `top_k` from 3 to 10 changes answer quality
- [ ] Works with both OpenAI API and local Ollama
