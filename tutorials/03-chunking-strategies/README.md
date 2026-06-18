# Tutorial 03 — PDF Chunking Strategies

## What you'll build

A pipeline that takes 5 structurally different PDFs, converts each to Markdown,
then applies 7 chunking strategies — producing a 35-combination matrix that shows
which strategy works best for which document structure.

## Why it matters

Chunking is the bridge between raw documents and a vector store. Bad chunks
produce bad retrieval, bad retrieval produces bad answers. There is no single
"best" strategy — the right choice depends on the document's structure. This
tutorial makes that trade-off tangible by running every combination.

## The 5 PDFs

| # | File | Structure | Why it's interesting |
|---|------|-----------|---------------------|
| 1 | `zoning_ordinance.pdf` | Deeply nested legal text (articles, sections, sub-sections) | Header-based splitting shines; fixed-size loses context |
| 2 | `permit_use_matrix.pdf` | Dense wide tables with merged headers | Table-aware chunking essential; fixed-size splits tables mid-row |
| 3 | `research_textbook.pdf` | Pure flowing prose (chapters, definitions, theorems) | Semantic chunking finds natural breaks; naive splitting mid-paragraph |
| 4 | `technical_manual.pdf` | Mixed: bullets, code blocks, small tables, warnings | Must respect logical groupings; code blocks should stay whole |
| 5 | `financial_report.pdf` | Table-heavy with short narrative between | Chunks with partial tables are useless for Q&A |

Generate them (if not already present):
```bash
uv run python tutorials/03-chunking-strategies/generate_pdfs.py
```

## The 7 Chunking Strategies

| # | Strategy | Key Idea |
|---|----------|----------|
| 1 | Fixed-size (character) | Split every N characters with M overlap |
| 2 | Fixed-size (token) | Split every N tokens (tiktoken) with overlap |
| 3 | Recursive text splitting | Split by `\n\n` → `\n` → `. ` → ` ` progressively |
| 4 | Markdown-header splitting | Split at `#`/`##`/`###` boundaries, heading as metadata |
| 5 | Semantic chunking | Group sentences by embedding similarity; split at drops |
| 6 | Table-aware chunking | Keep tables atomic; split prose around them |
| 7 | Sliding-window with overlap | Fixed window, stride < window for high overlap |

---

### Strategy 1: Fixed-Size Character Splitting

**Theory:** The simplest possible approach — treat text as a flat character stream
and slice it into uniform pieces. Overlap ensures that no sentence is split without
appearing fully in at least one chunk.

**Trade-offs:**
- Pros: Dead simple, predictable chunk sizes, works on any text
- Cons: Cuts mid-word, mid-sentence, mid-table. Completely ignores structure.

**When to use:** Baseline comparison only. Rarely the right choice in production.

**Pseudocode:**
```
function chunk_fixed_char(text, chunk_size=1000, overlap=200):
    chunks = []
    stride = chunk_size - overlap
    position = 0
    while position < len(text):
        chunk = text[position : position + chunk_size]
        chunks.append(chunk)
        position += stride
    return chunks
```

---

### Strategy 2: Fixed-Size Token Splitting

**Theory:** Like character splitting, but counts *tokens* (the units an LLM
sees) instead of characters. This aligns chunk boundaries with how models
actually consume text. Uses tiktoken's `cl100k_base` encoding (GPT-4 tokenizer).

**Trade-offs:**
- Pros: Chunk sizes map directly to model context windows. A "500-token chunk"
  is meaningful — you know it fits in the model.
- Cons: Still ignores document structure. Slightly more expensive (must encode
  the full text first).

**When to use:** When you need to guarantee chunks fit within a token budget.

**Pseudocode:**
```
function chunk_fixed_token(text, chunk_size=256, overlap=50):
    tokens = tiktoken.encode(text)  # e.g., [12, 8765, 432, ...]
    chunks = []
    stride = chunk_size - overlap
    position = 0
    while position < len(tokens):
        window = tokens[position : position + chunk_size]
        chunks.append(tiktoken.decode(window))
        position += stride
    return chunks
```

---

### Strategy 3: Recursive Text Splitting

**Theory:** The core insight: not all whitespace is equal. A double newline
(`\n\n`) separates paragraphs — a much stronger boundary than a single newline
(`\n`) or a space. This strategy tries the strongest separator first; if any
resulting piece is still too large, it recurses with the next weaker separator.

This is LangChain's `RecursiveCharacterTextSplitter` approach.

**Separator hierarchy:** `["\n\n", "\n", ". ", " "]`

**Trade-offs:**
- Pros: Respects natural text boundaries (paragraphs > lines > sentences > words).
  Much better quality than naive fixed-size.
- Cons: Doesn't understand structure beyond whitespace. A heading and its first
  paragraph may end up in separate chunks if the paragraph is too long.

**When to use:** Good general-purpose default for prose-heavy documents.

**Pseudocode:**
```
function chunk_recursive(text, chunk_size, separators=["\n\n", "\n", ". ", " "]):
    if len(text) <= chunk_size:
        return [text]

    sep = separators[0]
    pieces = text.split(sep)
    remaining_seps = separators[1:]

    chunks = []
    current = ""
    for piece in pieces:
        candidate = current + sep + piece if current else piece
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(piece) > chunk_size and remaining_seps:
                # Piece still too big — recurse with weaker separator
                chunks.extend(chunk_recursive(piece, chunk_size, remaining_seps))
                current = ""
            else:
                current = piece
    if current:
        chunks.append(current)
    return chunks
```

---

### Strategy 4: Markdown-Header Splitting

**Theory:** Documents converted to Markdown have explicit structure markers:
`#`, `##`, `###`. Each heading starts a logical section. Split at these
boundaries and carry the heading as metadata — so the retrieval system knows
*which section* a chunk belongs to without reading the chunk text.

**Trade-offs:**
- Pros: Chunks align with the document's actual structure. Metadata (heading
  path) gives context for free. No content is split mid-section.
- Cons: Section sizes vary wildly — one section might be 50 characters, another
  5000. Large sections may still need sub-splitting. Only works on Markdown input.

**When to use:** Ideal for structured documents (legal, technical docs, manuals).

**Pseudocode:**
```
function chunk_by_headers(text):
    chunks = []
    current_heading = None
    current_level = 0
    current_body = []

    for line in text.split("\n"):
        if line starts with "#":
            // Save previous section
            if current_body or current_heading:
                chunks.append({
                    heading: current_heading,
                    level: current_level,
                    content: join(current_body)
                })
            // Parse new heading
            hashes = count leading '#' in line
            current_heading = line.strip("# ")
            current_level = hashes
            current_body = []
        else:
            current_body.append(line)

    // Don't forget the last section
    chunks.append({heading: current_heading, level: current_level, content: join(current_body)})
    return chunks
```

---

### Strategy 5: Semantic Chunking

**Theory:** Instead of splitting by characters or syntax, split by *meaning*.
Embed each sentence, then measure cosine similarity between adjacent sentences.
When similarity drops below a threshold, that's a "topic boundary" — a natural
place to split.

This produces chunks that are semantically coherent: sentences in the same chunk
talk about the same thing.

**Trade-offs:**
- Pros: Chunks are topically coherent regardless of formatting. Works even on
  poorly structured text. Best retrieval quality in theory.
- Cons: Expensive (must embed every sentence). Requires an embedding model.
  Threshold tuning is tricky. Slow for large documents.

**When to use:** When retrieval quality is critical and compute budget allows.

**Pseudocode:**
```
function chunk_semantic(text, threshold=0.5, min_chunk_size=100):
    sentences = split_into_sentences(text)
    embeddings = embed_model.encode(sentences)  // shape: (N, 384)

    // Compute similarity between adjacent sentences
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity(embeddings[i], embeddings[i+1])
        similarities.append(sim)

    // Find break points where similarity drops
    break_points = [i+1 for i, sim in enumerate(similarities) if sim < threshold]

    // Group sentences between break points
    chunks = []
    start = 0
    for bp in break_points:
        chunk = " ".join(sentences[start:bp])
        if len(chunk) >= min_chunk_size:
            chunks.append(chunk)
            start = bp
        // else: merge with next group (too small)
    // Add remaining
    chunks.append(" ".join(sentences[start:]))
    return chunks
```

---

### Strategy 6: Table-Aware Chunking

**Theory:** Tables in Markdown are blocks of lines starting with `|`. A table
split across two chunks is useless — you lose column alignment, headers, or
data rows. This strategy identifies table blocks, keeps them atomic (never split),
and applies recursive splitting only to the prose between tables.

**Trade-offs:**
- Pros: Tables always appear whole. Prose still gets reasonable splitting.
  Essential for documents with data tables.
- Cons: A large table (100 rows) becomes one giant chunk — might exceed token
  limits. No sub-table splitting available.

**When to use:** Any document with tables (financial reports, specs, data sheets).

**Pseudocode:**
```
function chunk_table_aware(text, chunk_size=1000):
    // Separate text into segments: "prose" and "table"
    segments = []
    current_type = "prose"
    current_lines = []

    for line in text.split("\n"):
        is_table_line = line.strip().startswith("|")
        if is_table_line and current_type == "prose":
            segments.append(("prose", join(current_lines)))
            current_lines = [line]
            current_type = "table"
        elif not is_table_line and current_type == "table":
            segments.append(("table", join(current_lines)))
            current_lines = [line]
            current_type = "prose"
        else:
            current_lines.append(line)
    segments.append((current_type, join(current_lines)))

    // Chunk each segment
    chunks = []
    for seg_type, content in segments:
        if seg_type == "table":
            chunks.append(content)  // Keep whole, even if > chunk_size
        else:
            chunks.extend(chunk_recursive(content, chunk_size))
    return chunks
```

---

### Strategy 7: Sliding Window with High Overlap

**Theory:** Like fixed-size character splitting but with much higher overlap
(default 67%: window=1500, stride=500). Each token appears in ~3 different
chunks. This is redundant by design — it maximizes the chance that any piece
of context appears fully within at least one chunk.

The key improvement over naive overlap: try to snap cut points to the nearest
sentence boundary (within ±50 characters) so you don't cut mid-sentence.

**Trade-offs:**
- Pros: Every sentence appears in context in at least one chunk. Good for
  retrieval where you'd rather have redundancy than miss a match.
- Cons: 3× the storage and embedding cost (more chunks to embed and store).
  Redundant results in search (multiple chunks contain the same info).

**When to use:** When recall matters more than efficiency (e.g., legal discovery,
compliance). Pairs well with re-ranking to deduplicate.

**Pseudocode:**
```
function chunk_sliding_window(text, window_size=1500, stride=500):
    chunks = []
    position = 0
    while position < len(text):
        end = position + window_size

        // Try to snap end to a sentence boundary (". ")
        if end < len(text):
            // Look for ". " within ±50 chars of the cut point
            search_start = max(end - 50, position)
            search_end = min(end + 50, len(text))
            best_break = text.rfind(". ", search_start, search_end)
            if best_break != -1:
                end = best_break + 2  // Include the period and space

        chunks.append(text[position:end])
        position += stride
    return chunks
```

---

### When to Use Which Strategy

| Document Type | Best Strategy | Why |
|---------------|--------------|-----|
| Legal/regulatory (nested sections) | Markdown-header | Preserves section context |
| Dense tables (financial, matrices) | Table-aware | Tables must stay whole |
| Academic prose (textbooks) | Semantic or Recursive | Natural topic boundaries |
| Mixed (manuals, reports) | Table-aware + recursive | Handle both structure types |
| Unknown / general | Recursive | Good default, respects paragraphs |
| High-recall requirement | Sliding window | Redundancy maximizes coverage |

## Your task

1. **Generate PDFs** — run `generate_pdfs.py` (or use the pre-built ones in `pdfs/`)
2. **Convert to Markdown** — `pdf_to_markdown.py` converts each PDF → `.md`
3. **Implement chunking** — fill in the `# TODO` functions in `chunking_strategies.py`
4. **Run the matrix** — `run_all.py` applies all strategies to all PDFs and writes results

## Run / check your work

```bash
# Generate sample PDFs (skip if pdfs/ already populated):
uv run python tutorials/03-chunking-strategies/generate_pdfs.py

# Convert PDFs to Markdown:
uv run python tutorials/03-chunking-strategies/pdf_to_markdown.py

# Run all chunking strategies:
uv run python tutorials/03-chunking-strategies/run_all.py

# Tests:
uv run pytest tutorials/03-chunking-strategies/ -v
```

## Definition of done

- [ ] All 5 PDFs exist in `pdfs/` (40–50 pages each, all vector)
- [ ] Each PDF converted to Markdown in `results/markdown/`
- [ ] 7 chunking strategies implemented in `chunking_strategies.py`
- [ ] `run_all.py` produces results matrix in `results/chunks/`
- [ ] Summary table showing chunk counts, avg sizes, and quality notes
- [ ] `uv run pytest tutorials/03-chunking-strategies/ -v` all green

## Stretch goals

1. Add a **quality score** per (PDF, strategy) pair: does any chunk split a table?
   Does any heading end up separated from its body paragraph?
2. Visualize chunk boundaries overlaid on the original Markdown
3. Benchmark: which strategy produces the most uniform chunk sizes?
