# Tutorials (homework)

Hands-on exercises that go one level deeper than the scripts at the repo root.
The root scripts already cover the big split — **vector PDFs** (digital text you
can pull directly) vs **raster PDFs** (pixels you must OCR). These tutorials pick
up the pieces that aren't covered yet, and **you implement them yourself**.

| # | Folder | What you'll build |
|---|--------|-------------------|
| 1 | [`01-tables-simple-vs-complex/`](01-tables-simple-vs-complex/) | Generate a PDF with a **simple** and a **complex** (merged-cell) table, then extract and tell them apart. |
| 2 | [`02-pdf-to-markdown/`](02-pdf-to-markdown/) | Read a PDF and emit clean **Markdown** — paragraphs, headings, and both kinds of table. |
| 3 | [`03-chunking-strategies/`](03-chunking-strategies/) | Apply **7 chunking strategies** to 5 structurally different PDFs and compare results. |
| 4 | [`04-debugging/`](04-debugging/) | Set up the VSCode **debugger**, step through Tutorial 03 code, find and fix a bug. |
| 5 | [`05-embeddings-math/`](05-embeddings-math/) | Understand **embeddings** from first principles, build a toy word2vec, then use a real model. |
| 6 | [`06-vector-store/`](06-vector-store/) | Store embeddings in **Postgres + pgvector**, run similarity search queries. |
| 7 | [`07-basic-rag/`](07-basic-rag/) | Wire vector search to an LLM — **retrieve → prompt → generate** with citations. |
| 8 | [`08-evaluation/`](08-evaluation/) | Build a gold-standard eval set, measure **Precision@k, Recall@k, MRR**. |
| 9 | [`09-hybrid-search/`](09-hybrid-search/) | Combine **vector + BM25 keyword search** via Reciprocal Rank Fusion. |
| 10 | [`10-reranking/`](10-reranking/) | Add a **cross-encoder reranker** for two-stage precision retrieval. |

## The pipeline

Tutorials 03–10 form a complete RAG pipeline:

```
PDF files → Markdown → Chunks → Embeddings → Postgres → RAG → Evaluation
   T03         T03       T03       T05          T06     T07      T08

Postgres → Hybrid Search (vector + BM25) → Reranking → LLM
   T06            T09                          T10       T07
```

Tutorial 04 (debugging) is standalone but uses Tutorial 03's code as its target.

Do them in order: Tutorial 2 reads the PDF that Tutorial 1 builds. Then there's a
**stretch** exercise in [`sample_pdfs/`](sample_pdfs/): build two 10+ page
documents and run your code on them to see what breaks across page boundaries.

## How the homework works

Each `*.py` file is a **skeleton**: function signatures, docstrings describing
exactly what to build, and `# TODO` markers. The logic is yours to write. Each
tutorial ships **tests** that encode the "definition of done":

```bash
uv sync   # once, from the repo root, to install dependencies

# implement the skeletons, then make the tests pass:
uv run pytest tutorials/01-tables-simple-vs-complex/ -v
uv run pytest tutorials/02-pdf-to-markdown/ -v
```

Start each tutorial by reading its `README.md`, then open the skeleton files and
fill in the TODOs until the tests are green.

## The big picture

A PDF is a **layout** format, not a **content** format. It stores *where* glyphs
and lines are drawn on a page, not "this is a paragraph" or "this is a table with
these rows." Everything downstream — search, embeddings, a vector store, feeding
an LLM — wants clean, structured text. This homework is about that gap: turning
page geometry back into structure (tables, headings, Markdown) and seeing exactly
where information is lost.
