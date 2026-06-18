# Tutorials 03–06: Plan Document

## Overview

Four new tutorials extending the PDF-Processing homework. They form a pipeline:
**PDF → Markdown → Chunks → Embeddings → Postgres Storage**

```
Tutorial 03 (Chunking)        → produces chunks from 5 PDF structures
Tutorial 04 (Debugging)       → learn to debug Python code (standalone)
Tutorial 05 (Embeddings Math) → understand & create embeddings of chunks from T03
Tutorial 06 (Vector Store)    → persist embeddings in Postgres with pgvector
```

---

## Tutorial 03 — PDF Chunking Strategies

### Goal
The learner reads 5 structurally different PDFs, converts each to Markdown,
then applies 5–7 chunking strategies to each — producing a matrix of ~35
combinations. They observe which strategy works best for which PDF structure.

### The 5 PDF Structures (all vector, generated with reportlab)

| # | Name | Structure | Pages | Source |
|---|------|-----------|-------|--------|
| 1 | `zoning_ordinance.pdf` | Deeply nested legal text: TOC, articles, sections, sub-sections, cross-references, definitions | ~45 | **Based on `ashevillenc-nc-1.pdf`** (289-page zoning code) — generate a vector replica of its structure |
| 2 | `permit_use_matrix.pdf` | Dense tabular data: multi-page zoning matrix with merged headers, column-spanning zones, footnotes | ~40 | **Based on `permit-uses.pdf`** (7-page use table) — expand to 40 pages with more zones/categories |
| 3 | `research_textbook.pdf` | Long-form prose: chapters, numbered sections, paragraphs, citations, no tables | ~45 | Computer science textbook covering AI/ML topics |
| 4 | `technical_manual.pdf` | Mixed layout: bullet lists, numbered steps, code snippets, warning boxes, small tables, diagrams-as-text | ~50 | Software deployment/operations manual |
| 5 | `financial_report.pdf` | Data-heavy: balance sheets, P&L tables, quarterly comparisons, minimal narrative between dense tables | ~40 | Annual report for a fictional company |

> **Note:** Each PDF is ~40–50 pages to give chunking strategies enough material
> to show meaningful differences. All PDFs are **vector** (text-layer embedded via
> reportlab) so pymupdf can extract text directly — no llamaparse or VLM needed.

### Generator Details

#### PDF 1: `zoning_ordinance.pdf` (from `ashevillenc-nc-1.pdf`)

Replicate the structure of Asheville's development code:
- Title page + Table of Contents (2 pages)
- 8 Articles, each with 5–8 Sections (e.g., `Sec. 7-2-5. — Definitions.`)
- Deep nesting: Article → Section → Subsection (a), (b), (c) → Sub-subsection (1), (2)
- Cross-references: "See Section 7-4-3(b)(2)" scattered throughout
- Definitions section with alphabetical terms
- Varied paragraph lengths (some sections are 1 line, some are full pages)

**Why it's interesting for chunking:** Hierarchy matters — a chunk that loses its
section context becomes meaningless. Header-based chunking shines; fixed-size fails.

#### PDF 2: `permit_use_matrix.pdf` (from `permit-uses.pdf`)

Expand the permit-use table into a full 40-page document:
- Header page with legend explaining zone codes and symbols (P, C, S, —)
- 30+ pages of wide tables: rows = land use categories, columns = zone districts
- Multi-row headers spanning 2–3 rows (zone groups → sub-zones)
- Merged row labels grouping related uses (e.g., "Residential" spans 8 rows)
- Footnotes per page referencing special conditions
- Appendix pages with supplemental standards text

**Why it's interesting for chunking:** Tables are atomic units. Fixed-size chunking
splits tables mid-row creating garbage. Table-aware chunking preserves meaning.

#### PDF 3: `research_textbook.pdf` (generated)

A synthetic CS textbook on machine learning fundamentals:
- 6 chapters: "Introduction", "Linear Algebra Review", "Probability",
  "Supervised Learning", "Neural Networks", "Evaluation Methods"
- Each chapter: 6–8 pages of dense prose paragraphs
- Numbered definitions, theorems, examples (Definition 3.1, Theorem 4.2)
- Inline math notation rendered as text (e.g., "f(x) = w^T x + b")
- Chapter summaries and "Further Reading" lists
- No tables, no bullet lists — pure flowing academic text

**Why it's interesting for chunking:** Long unbroken prose. Recursive and semantic
chunking must find natural break points. Paragraph boundaries vs sentence boundaries
produce very different chunk quality.

#### PDF 4: `technical_manual.pdf` (generated)

A Kubernetes deployment operations manual:
- Sections: "Prerequisites", "Installation", "Configuration", "Troubleshooting",
  "Monitoring", "Backup & Recovery", "Security Hardening", "Appendix: CLI Reference"
- Mixed content per page:
  - Bullet lists (requirements, checklist items)
  - Numbered step-by-step procedures ("Step 1: Run `kubectl apply`...")
  - Code blocks (YAML configs, shell commands) rendered in monospace
  - Warning/Note boxes (indented paragraphs with "⚠ WARNING:" prefix)
  - Small 3–4 row tables (port mappings, environment variables)
- Frequent section/subsection changes within a single page

**Why it's interesting for chunking:** High structural variety on every page.
Markdown-header splitting works for sections, but code blocks and step sequences
need to stay together. Tests whether strategies respect logical groupings.

#### PDF 5: `financial_report.pdf` (generated)

Annual report for "Acme Corp" fiscal year 2024:
- Executive summary (2 pages prose)
- 10 quarterly/annual tables: income statement, balance sheet, cash flow,
  segment revenue, geographic breakdown, headcount, capex, debt schedule,
  ratio analysis, 5-year comparison
- Each table is 1–3 pages with 15–40 rows and 6–10 columns
- Between tables: 1–3 short paragraphs of commentary
- Footnotes at bottom of table pages (numbered references)
- Appendix with accounting policy notes (dense text)

**Why it's interesting for chunking:** The ratio of table-to-prose is very high.
Chunks that contain partial tables are useless for Q&A. Strategies must either
keep tables whole or provide enough context (column headers) in each chunk.

### Generator Implementation Notes

All generators use `reportlab.platypus` (SimpleDocTemplate + story list):
- Headings via `Paragraph(text, styles["Heading1/2/3"])`
- Body text via `Paragraph(text, styles["BodyText"])`
- Tables via `Table(data, colWidths=[...])` with `TableStyle` for grid/merges
- Code blocks via `Preformatted(text, styles["Code"])` or monospace Paragraphs
- Page breaks via `PageBreak()` where needed
- All text is actual text (not images) so pymupdf extracts it cleanly

The generators live in `tutorials/03-chunking-strategies/generate_pdfs.py`.

### The 5–7 Chunking Strategies

| # | Strategy | Description |
|---|----------|-------------|
| 1 | **Fixed-size (character)** | Split at every N characters with M-character overlap |
| 2 | **Fixed-size (token)** | Split at every N tokens (tiktoken) with overlap |
| 3 | **Recursive text splitting** | Split by `\n\n` → `\n` → `. ` → ` ` (LangChain-style) |
| 4 | **Markdown-header splitting** | Split at `#`, `##`, `###` boundaries, keeping heading as metadata |
| 5 | **Semantic chunking** | Group consecutive sentences whose embeddings are similar; split at drops in similarity |
| 6 | **Table-aware chunking** | Keep tables as atomic units; split prose around them |
| 7 | **Sliding-window with overlap** | Fixed window but stride < window (higher overlap for context preservation) |

### Output Matrix

```
For each (PDF, strategy) pair:
  - Number of chunks produced
  - Average chunk size (chars / tokens)
  - Sample: first 3 chunks printed
  - Quality note: does a table get split? Does a heading get separated from its body?
```

Results written to `tutorials/03-chunking-strategies/results/` as JSON + a summary
Markdown table.

### File Structure

```
tutorials/03-chunking-strategies/
├── README.md                    # Explanation + task
├── generate_pdfs.py             # Build the 5 sample PDFs
├── pdf_to_markdown.py           # Convert each PDF → .md (reuses Tutorial 02 logic)
├── chunking_strategies.py       # Implement the 7 strategies (skeleton + TODOs)
├── run_all.py                   # Apply all strategies to all PDFs, write results
├── test_tutorial3.py            # Tests
└── results/                     # Output directory (gitignored)
```

### Definition of Done

- [ ] 5 PDFs generated, each with distinct structure
- [ ] Each PDF converted to Markdown
- [ ] 7 chunking strategies implemented
- [ ] Results matrix produced (35 combinations)
- [ ] Tests pass: `uv run pytest tutorials/03-chunking-strategies/ -v`

---

## Tutorial 04 — Code Debugging in Python (VSCode)

### Goal
The learner sets up the VSCode Python debugger, runs an existing program under
it, and practices: breakpoints, step-in, step-out, step-over, inspect variables,
watch expressions, and the call stack. They document their findings.

### What They Debug

Use the existing `tutorials/03-chunking-strategies/chunking_strategies.py` — a
non-trivial program with loops, function calls, and data transformations. The
learner sets breakpoints inside a chunking function and inspects intermediate
state (the chunk list, current position, overlap buffer).

### File Structure

```
tutorials/04-debugging/
├── README.md                    # Setup instructions + exercises
├── .vscode/
│   └── launch.json              # Pre-configured debug configurations
├── debug_target.py              # A small buggy program to fix via debugging
├── exercises.md                 # Step-by-step debugging exercises
└── findings_template.md         # Template for the learner to fill in
```

### README Content (outline)

1. **Setup**: Install Python extension, verify interpreter
2. **launch.json**: Explain the configuration (program, args, console)
3. **Exercise 1 — Breakpoints**: Set a breakpoint in `debug_target.py`, run, inspect locals
4. **Exercise 2 — Step In/Out**: Step into a function call, observe call stack, step out
5. **Exercise 3 — Watch & Conditional Breakpoints**: Watch a variable, set a conditional
   breakpoint that triggers only when `chunk_count > 5`
6. **Exercise 4 — Fix the Bug**: `debug_target.py` has an intentional off-by-one error in
   a chunking loop. Use the debugger to find it, then fix it.
7. **Exercise 5 — Inspect Complex Objects**: Pause inside `pdf_to_markdown()` and inspect
   the `blocks` list — record the structure in `findings_template.md`

### Definition of Done

- [ ] `launch.json` works out of the box
- [ ] `debug_target.py` has a real bug that requires debugging to find
- [ ] `exercises.md` has clear step-by-step instructions with screenshots placeholders
- [ ] Learner fills in `findings_template.md` after debugging

---

## Tutorial 05 — Math Behind Embeddings

### Goal
The learner understands embeddings from first principles:
1. The math (vector spaces, dot product, cosine similarity)
2. Building a toy embedding from scratch with numpy
3. Using a real embedding model on the chunks from Tutorial 03

### File Structure

```
tutorials/05-embeddings-math/
├── README.md                    # Concepts + exercises
├── 01_math_foundations.py       # Vector ops: dot product, cosine similarity, distance
├── 02_toy_embedding.py          # Build a simple word2vec-style embedding (skip-gram with numpy)
├── 03_real_embeddings.py        # Use sentence-transformers to embed Tutorial 03 chunks
├── test_tutorial5.py            # Tests
└── results/                     # Output: embeddings as .npy files
```

### Content Breakdown

#### Part 1: Math Foundations (`01_math_foundations.py`)
- What is a vector? (represent words/sentences as points in N-dim space)
- Dot product: geometric meaning, formula, implementation
- Cosine similarity: why it's better than Euclidean for text
- Demonstrate: similar sentences have high cosine similarity, unrelated ones don't
- Visualization: project 2D/3D with matplotlib (optional stretch)

#### Part 2: Toy Embedding from Scratch (`02_toy_embedding.py`)
- Implement a minimal skip-gram word2vec using only numpy:
  - Build vocabulary from a small corpus
  - One-hot encoding → projection to embedding dimension (e.g., 50-d)
  - Training loop: forward pass, loss (negative sampling or softmax), backprop
  - After training: show that "king" - "man" + "woman" ≈ "queen" (on toy data)
- Keep it CPU-only, ~100 lines, educational not production

#### Part 3: Real Embeddings (`03_real_embeddings.py`)
- Install `sentence-transformers` (or `langchain` embeddings)
- Load a small model: `all-MiniLM-L6-v2` (~80MB, runs on CPU)
- Read chunks from Tutorial 03 results
- Embed each chunk → save as numpy arrays
- Compare: cosine similarity between chunks from same section vs different sections
- Output: `results/embeddings_{pdf_name}_{strategy}.npy`

### Definition of Done

- [ ] Math concepts explained with runnable code
- [ ] Toy embedding trains and shows similarity patterns
- [ ] Real model embeds Tutorial 03 chunks
- [ ] Tests pass: `uv run pytest tutorials/05-embeddings-math/ -v`

---

## Tutorial 06 — Store Embeddings in Postgres (pgvector)

### Goal
Persist the embeddings from Tutorial 05 into a local Postgres database with
the `pgvector` extension. Define a schema, insert embeddings, and run similarity
search queries.

### Prerequisites
- Docker (to run Postgres + pgvector locally)
- Embeddings from Tutorial 05

### File Structure

```
tutorials/06-vector-store/
├── README.md                    # Setup + exercises
├── docker-compose.yml           # Postgres + pgvector container
├── schema.sql                   # CREATE TABLE with vector column
├── store_embeddings.py          # Read .npy files, insert into Postgres
├── search.py                    # Query: "find chunks similar to X"
├── test_tutorial6.py            # Tests (uses testcontainers or subprocess)
└── results/                     # Query output examples
```

### Schema Design

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE pdf_chunks (
    id              SERIAL PRIMARY KEY,
    pdf_name        TEXT NOT NULL,          -- e.g. "prose_heavy"
    chunk_strategy  TEXT NOT NULL,          -- e.g. "recursive_text"
    chunk_index     INTEGER NOT NULL,       -- position within the document
    chunk_text      TEXT NOT NULL,          -- the actual markdown text
    embedding       vector(384) NOT NULL,   -- 384-d for all-MiniLM-L6-v2
    metadata        JSONB,                  -- page number, heading, etc.
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON pdf_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### Content Breakdown

1. **Setup**: `docker compose up -d` starts Postgres with pgvector
2. **Schema**: Run `schema.sql` to create tables + index
3. **Insert**: `store_embeddings.py` reads numpy files from Tutorial 05, inserts rows
4. **Search**: `search.py` takes a query string, embeds it, runs:
   ```sql
   SELECT chunk_text, 1 - (embedding <=> query_vec) AS similarity
   FROM pdf_chunks
   ORDER BY embedding <=> query_vec
   LIMIT 5;
   ```
5. **Exercises**:
   - Compare search quality across chunking strategies
   - Filter by `pdf_name` to search within one document
   - Experiment with `ivfflat` vs `hnsw` index types

### Definition of Done

- [ ] `docker compose up` starts Postgres with pgvector
- [ ] Schema created and embeddings inserted
- [ ] Similarity search returns relevant chunks
- [ ] Tests pass: `uv run pytest tutorials/06-vector-store/ -v`

---

## Dependencies to Add

```
# pyproject.toml additions
tiktoken          # token counting for chunking
sentence-transformers  # real embedding model
psycopg[binary]   # Postgres driver
pgvector          # pgvector Python bindings
numpy             # math + array storage
```

---

## Resolved Decisions

1. **Semantic chunking**: Use the same embedding model from Tutorial 05 (`all-MiniLM-L6-v2`) — builds toward the full pipeline. More tutorials coming after these.
2. **Tutorial 04 (Debugging)**: Debug Tutorial 03 code (same context, better continuity).
3. **Tutorial 06 (Postgres)**: Docker mode (docker-compose with pgvector image).
4. **Numbering**: Tutorials 03–06, continuing from existing 01–02.
