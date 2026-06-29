# Tutorial 07 — Basic RAG (Retrieval-Augmented Generation)

## Goal

Wire the vector store from Tutorial 06 to an LLM. Ask a natural-language
question about your PDFs, retrieve the most relevant chunks, and generate
a grounded answer with source citations.

By the end of this tutorial you will understand how RAG works end-to-end:
why we retrieve before generating, how to engineer prompts that keep the
model grounded, and how to attribute answers back to their source documents.

---

## What Is RAG and Why Does It Matter?

Large Language Models are powerful, but they have two critical weaknesses:

1. **Knowledge cutoff** — They only know what was in their training data.
   Your PDFs contain domain-specific information the model has never seen.
2. **Hallucination** — When asked about unfamiliar topics, models confidently
   generate plausible-sounding but incorrect answers.

RAG solves both problems by injecting **retrieved evidence** into the prompt
before generation. The model doesn't need to "know" the answer — it just needs
to read the relevant text and synthesize a response.

```
Without RAG:  User → LLM → (may hallucinate)
With RAG:     User → Retrieve docs → LLM + docs → (grounded answer)
```

This is the same pattern used by ChatGPT's web browsing, Perplexity, and
every enterprise Q&A system built on top of internal documents.

---

## Pipeline Architecture

```
User Question
      │
      ▼
┌─────────────────────────────────────────────┐
│  Stage 1: RETRIEVE                          │
│  • Embed the question (same model as T05)   │
│  • Vector similarity search in Postgres     │
│  • Return top-k most relevant chunks        │
└─────────────────────┬───────────────────────┘
                      │  top-k chunks (with metadata)
                      ▼
┌─────────────────────────────────────────────┐
│  Stage 2: FORMAT CONTEXT                    │
│  • Number each chunk [Source 1], [Source 2] │
│  • Truncate to fit token budget             │
│  • Include metadata (PDF name, strategy)    │
└─────────────────────┬───────────────────────┘
                      │  formatted context string
                      ▼
┌─────────────────────────────────────────────┐
│  Stage 3: GENERATE                          │
│  • System prompt: "answer from context only"│
│  • User prompt: context + question          │
│  • LLM produces answer with [Source N] refs │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
            Answer + Citations
```

---

## Key Concepts

### 1. Prompt Engineering for RAG

The system prompt is the most important piece. It tells the LLM:
- Only answer from the provided context (no prior knowledge)
- Say "I don't know" if the context doesn't contain the answer
- Cite sources using `[Source N]` notation

A well-structured RAG prompt looks like:

```
SYSTEM: You answer questions using ONLY the provided context. Cite sources.
USER:   Context: [Source 1] ... [Source 2] ...
        Question: What is the maximum building height?
```

**Why this matters:** Without the grounding instruction, the model will blend
its training knowledge with the retrieved context, making it impossible to
trust the answer or verify it against a source.

### 2. Token Budget Management

Models have a finite context window (e.g., 8K, 32K, 128K tokens). You must
decide how to allocate it:

| Component | Typical Budget |
|-----------|---------------|
| System prompt | ~200 tokens |
| Retrieved context | 3,000–6,000 tokens |
| User question | ~50 tokens |
| Space for answer | remaining |

If you retrieve 10 chunks of 500 tokens each (5,000 total), that may exceed
your budget. The `format_context()` function handles this by:
1. Adding chunks in relevance order
2. Stopping when the budget is exhausted
3. Truncating the last chunk if it partially fits

**Approximation:** 1 token ≈ 4 characters (for English text)

### 3. Source Attribution

Every chunk stored in the vector database carries metadata:
- `pdf_name` — which document it came from
- `chunk_strategy` — how it was chunked (from Tutorial 03)
- `chunk_index` — position in the document

When we format the context, each chunk gets a numbered label (`[Source 1]`,
`[Source 2]`). The LLM is instructed to reference these labels in its answer.
This lets the user verify claims against the original document.

### 4. Streaming Responses

For long answers, waiting for the full response is a poor UX. Streaming
sends tokens to the user as they're generated:

```python
for chunk in ask(question, stream=True)["answer"]:
    print(chunk, end="", flush=True)
```

The OpenAI SDK supports this natively via `stream=True`.

---

## Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `llm_client.py` | Thin wrapper around OpenAI-compatible API | `get_client()`, `generate()` |
| `prompts.py` | System and user prompt templates | `format_context()`, `build_messages()` |
| `rag_pipeline.py` | Orchestrates retrieve → format → generate | `retrieve()`, `ask()` |
| `demo.py` | Interactive CLI to ask questions about your PDFs | `run_interactive()`, `run_single()` |
| `test_tutorial7.py` | Unit tests (mocked, no API key needed) | 5 tests |

### How the files connect

```
demo.py
  └── rag_pipeline.ask()
        ├── rag_pipeline.retrieve()    → calls Tutorial 06's search module
        ├── prompts.format_context()   → fits chunks into token budget
        ├── prompts.build_messages()   → assembles system + user messages
        └── llm_client.generate()      → calls OpenAI-compatible API
```

---

## Setup

### Option A: OpenAI API (easiest)

```bash
uv add openai  # already added if you followed the tutorials in order

export OPENAI_API_KEY="sk-..."
```

### Option B: Local model via Ollama (free, private)

```bash
# Install Ollama: https://ollama.ai
ollama pull llama3

export OPENAI_BASE_URL="http://localhost:11434/v1"
export RAG_MODEL="llama3"
# No API key needed — llm_client.py handles this automatically
```

### Option C: Any OpenAI-compatible endpoint

```bash
export OPENAI_BASE_URL="https://api.together.xyz/v1"
export OPENAI_API_KEY="your-together-key"
export RAG_MODEL="meta-llama/Llama-3-8b-chat-hf"
```

### Prerequisites

Make sure you have:
1. Tutorials 03-06 completed (chunks stored in Postgres with embeddings)
2. Postgres running with pgvector (`docker compose up` from Tutorial 06)
3. At least one PDF's embeddings stored in the `pdf_chunks` table

---

## Usage

```bash
# Interactive mode — ask multiple questions in a loop
uv run python tutorials/07-basic-rag/demo.py

# Single question — prints answer and exits
uv run python tutorials/07-basic-rag/demo.py --query "What are the setback requirements for R-1 zones?"

# Filter by specific PDF
uv run python tutorials/07-basic-rag/demo.py --query "Explain attention mechanism" --pdf research_textbook

# Retrieve more chunks for richer context
uv run python tutorials/07-basic-rag/demo.py --query "Compare GloVe and Word2Vec" --top-k 10
```

---

## Tasks

### Task 1: Understand the LLM Client
Read `llm_client.py`. Notice how it:
- Reads `OPENAI_BASE_URL` and `RAG_MODEL` from environment
- Handles the "no API key needed" case for local models
- Supports both streaming and non-streaming responses

### Task 2: Study the Prompt Templates
Read `prompts.py`. Pay attention to:
- The system prompt rules (ground in context, cite sources, say "I don't know")
- How `format_context()` numbers each chunk and respects the token budget
- How `build_messages()` assembles the final message list

### Task 3: Trace the Pipeline
Read `rag_pipeline.py`. Follow the flow:
1. `retrieve()` calls Tutorial 06's vector search
2. `ask()` orchestrates the full pipeline
3. The response includes the answer, sources, and how many chunks were used

### Task 4: Run the Demo
Run `demo.py` in interactive mode. Try:
- A factual question with a clear answer in one PDF
- A comparison question requiring multiple chunks
- A question where the answer is NOT in any PDF (should get "I don't know")

### Task 5: Experiment with Parameters
Change these and observe the effect on answer quality:
- `top_k`: 3 vs 5 vs 10 — more context = richer answers but more noise
- `max_context_tokens`: 1000 vs 3000 vs 6000 — budget tradeoff
- Edit the system prompt in `prompts.py` — try removing the "cite sources" rule

### Task 6: Compare Chunking Strategies
Run the same question against different strategies:
```bash
# Edit rag_pipeline.py's retrieve() to filter by strategy, or:
uv run python -c "
from tutorials.07_basic_rag.rag_pipeline import ask
result = ask('What is attention?', strategy='chunk_recursive')
print(result['answer'][:200])
"
```
Which strategy produces better answers? Why?

---

## Common Issues

| Problem | Solution |
|---------|----------|
| "No relevant chunks found" | Make sure Postgres is running and embeddings are stored (run Tutorial 06) |
| "openai.AuthenticationError" | Set `OPENAI_API_KEY` or use Ollama with `OPENAI_BASE_URL` |
| Answer ignores context | Check system prompt — the model may not be following instructions (try a stronger model) |
| Answer is too short | Increase `max_context_tokens` or `top_k` to give more context |
| Slow responses | Use `stream=True` for UX, or switch to a smaller/faster model |

---

## Conceptual Deep Dive: Why RAG Beats Fine-Tuning

| Aspect | Fine-Tuning | RAG |
|--------|-------------|-----|
| Data freshness | Stale (must retrain) | Always current (just update the store) |
| Cost | Expensive (GPU hours) | Cheap (API call + vector search) |
| Transparency | Black box | Citable sources |
| Hallucination | Still possible | Controlled (grounded in context) |
| Multi-tenant | One model per tenant | One model, many vector stores |

RAG is the standard approach for production Q&A systems over private documents.
Fine-tuning is reserved for changing the model's *style* or teaching it new *skills*,
not for injecting factual knowledge.

---

## Theory & References

### Foundational Paper

**"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"**
Lewis et al., 2020 (Meta AI / Facebook Research)
[arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

This paper introduced the RAG framework. Key insight: combine a pre-trained
retriever (DPR — Dense Passage Retrieval) with a pre-trained generator
(BART) and fine-tune them jointly. The retriever fetches relevant passages
from a knowledge base, and the generator conditions on both the question and
the retrieved passages.

> "We build RAG models where the parametric memory is a pre-trained seq2seq
> model and the non-parametric memory is a dense vector index of Wikipedia,
> accessed with a pre-trained neural retriever."

The paper demonstrated that RAG outperforms purely parametric models on
open-domain QA, fact verification, and knowledge-intensive generation.

### Prompt Engineering for Grounded Generation

**Anthropic — "Long Context Window Prompting"** (2024)
[docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

Anthropic's prompt engineering guide details how to structure prompts with
retrieved context. Key recommendations we use in this tutorial:
- Put the context *before* the question (model attends to recent tokens more)
- Explicitly instruct "answer ONLY from the provided context"
- Request citations so the model is accountable for each claim
- Use XML tags or clear delimiters to separate context from instructions

**OpenAI — "Retrieval Strategies" Cookbook** (2023)
[cookbook.openai.com/examples/question_answering_using_embeddings](https://cookbook.openai.com/examples/question_answering_using_embeddings)

OpenAI's official guide walks through:
- Embedding questions and documents with the same model
- Cosine similarity for retrieval
- Fitting context into token budgets
- System prompts that prevent hallucination

### On Hallucination and Faithfulness

**"A Survey on Hallucination in Large Language Models"**
Huang et al., 2023
[arXiv:2311.05232](https://arxiv.org/abs/2311.05232)

Categorizes hallucination into:
- **Intrinsic**: contradicting the source material
- **Extrinsic**: generating claims not found in any source

RAG specifically targets extrinsic hallucination by providing source material,
but intrinsic hallucination (misinterpreting the context) remains a risk.

### Token Budget and Context Utilization

**"Lost in the Middle: How Language Models Use Long Contexts"**
Liu et al., 2023 (Stanford)
[arXiv:2307.03172](https://arxiv.org/abs/2307.03172)

Critical finding: models attend most strongly to information at the
**beginning** and **end** of the context window. Information in the middle
is often ignored. This has direct implications for how we order chunks:
- Put the most relevant chunk first
- If budget allows, also put a highly relevant chunk last
- The "lost in the middle" effect worsens as context length increases

### Streaming and Latency

**OpenAI — "Streaming" API Documentation**
[platform.openai.com/docs/api-reference/streaming](https://platform.openai.com/docs/api-reference/streaming)

Server-Sent Events (SSE) allow token-by-token delivery. First-token latency
is typically 200-500ms; total generation time depends on response length.
Streaming significantly improves perceived performance for the user.

---

## Check Your Work

- [ ] Can ask a question and get a grounded answer
- [ ] Answer includes `[Source N]` citations referencing specific chunks
- [ ] Changing `top_k` from 3 to 10 changes answer quality/length
- [ ] Works with both OpenAI API and local Ollama
- [ ] Asking about something NOT in the PDFs returns "I don't have enough information"
- [ ] Can explain why RAG is preferred over fine-tuning for document Q&A

---

## What's Next

In **Tutorial 08**, we'll measure how good this retrieval actually is.
Right now we're eyeballing answers — but how do we know if the right chunks
were retrieved? We'll build a gold-standard evaluation set and compute
Precision@k, Recall@k, and MRR to objectively compare strategies.
