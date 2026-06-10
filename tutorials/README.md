# Tutorials (homework)

Hands-on exercises that go one level deeper than the scripts at the repo root.
The root scripts already cover the big split — **vector PDFs** (digital text you
can pull directly) vs **raster PDFs** (pixels you must OCR). These tutorials pick
up the two pieces that aren't covered yet, and **you implement them yourself**.

| # | Folder | What you'll build |
|---|--------|-------------------|
| 1 | [`01-tables-simple-vs-complex/`](01-tables-simple-vs-complex/) | Generate a PDF with a **simple** and a **complex** (merged-cell) table, then extract and tell them apart. |
| 2 | [`02-pdf-to-markdown/`](02-pdf-to-markdown/) | Read a PDF and emit clean **Markdown** — paragraphs, headings, and both kinds of table. |

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
