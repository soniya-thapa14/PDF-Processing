# PDF Processing — From Raw Pages to Production RAG

A hands-on learning repository that takes you from PDF extraction fundamentals
through a complete Retrieval-Augmented Generation (RAG) pipeline.

## What You'll Learn

| Stage | Tutorials | Skills |
|-------|-----------|--------|
| **Extraction** | 01–02 | Parse tables (simple + merged-cell), convert PDF → Markdown |
| **Chunking** | 03–04 | 7 chunking strategies on 5 document types, debugging |
| **Embeddings** | 05–06 | Vector math from scratch, pgvector similarity search |
| **LLM + RAG** | 07–11 | Local LLMs, RAG pipeline, evaluation, hybrid search, reranking |

## The Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    End-to-End RAG Pipeline                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PDF Files ──→ Markdown ──→ Chunks ──→ Embeddings ──→ Postgres   │
│    (T01-02)     (T02)       (T03)      (T05)         (T06)       │
│                                                                  │
│  Query ──→ Hybrid Search ──→ Reranking ──→ LLM Generation        │
│             (T10: Vec+BM25)   (T11)        (T08)                 │
│                                                                  │
│  Gold-Standard Evaluation (T09): Precision@k, Recall@k, MRR     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Sample PDFs for Testing

Tutorial 03 generates 5 structurally different PDFs to stress-test chunking:

| Generator | Document Type | Key Challenge |
|-----------|--------------|---------------|
| `generate_textbook.py` | 45-page NLP textbook | Long-form prose with chapters, math, cross-references |
| `generate_financial_report.py` | Financial report | Dense tables, numeric data, short sections |
| `generate_technical_manual.py` | Technical manual | Numbered procedures, warnings, nested lists |
| `generate_zoning_ordinance.py` | Legal ordinance | Section/subsection hierarchy, legal citations |
| `generate_permit_matrix.py` | Permit matrix | Large complex table spanning multiple pages |

### `generate_textbook.py` — The Primary Test Document

This generator creates a ~45 page research textbook on "Embeddings and Large
Language Models" with realistic academic structure:

- **8 chapters** spanning Part I (Embeddings) and Part II (LLMs)
- **Mathematical formulas** (cosine similarity, attention, softmax)
- **Cross-chapter references** ("As discussed in Chapter 3...")
- **Academic citations** (author-year format in running text)
- **Progressive concept building** (each chapter depends on the previous)

This document is the ideal stress-test for chunking because:
1. **Semantic boundaries** don't align with page boundaries
2. **Context windows** matter — a chunk about "attention" needs to reference earlier
   definitions of "embeddings" and "query/key/value"
3. **Mathematical notation** can be broken mid-formula by naive chunkers
4. **Section hierarchy** (Chapter → Section → Subsection) creates natural breakpoints
   that semantic chunking should discover

Use this document to test whether your RAG pipeline correctly:
- Retrieves the right chapter when asked about a specific concept
- Handles multi-hop questions ("How does attention relate to embeddings?")
- Preserves formula integrity in retrieved chunks

## How the Homework Works

Each `*.py` file is a **skeleton**: function signatures, docstrings, and `# TODO`
markers. You implement the logic. Tests encode the "definition of done":

```bash
uv sync                                    # install dependencies (once)
uv run pytest tutorials/08-basic-rag/ -v   # run tests for one tutorial
uv run pytest tutorials/ -v                # run ALL tests
```

### Learning Philosophy

1. **Fundamentals first** — understand the math before using libraries
2. **Edge cases matter** — every test file includes boundary conditions
3. **Think before coding** — each README has a "Thinking About Edge Cases" section
4. **Build incrementally** — tutorials form a dependency chain (do them in order)

## Quick Start

```bash
# Clone and install
git clone <repo-url>
cd PDF-Processing
uv sync

# Generate test PDFs (Tutorial 03)
uv run python tutorials/03-chunking-strategies/run_all.py

# Start Postgres for vector store (Tutorial 06+)
docker compose -f tutorials/06-vector-store/docker-compose.yml up -d

# Install Ollama for local LLM (Tutorial 07+)
brew install ollama && ollama pull llama3

# Run tests
uv run pytest tutorials/ -v
```

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (for Postgres + pgvector)
- Ollama (for local LLM inference)
- ~8GB free disk (for model + database)
