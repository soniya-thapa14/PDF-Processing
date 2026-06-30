# Tutorial 10 — Hybrid Search (Vector + BM25)

## Goal

Combine semantic vector search with keyword-based BM25 search using Postgres
full-text search. Show when hybrid beats pure vector, and vice versa.

By the end of this tutorial you will understand:
- Why vector search alone isn't enough
- How BM25/TF-IDF keyword matching works
- How Postgres full-text search (`tsvector`, `ts_rank`) operates
- How Reciprocal Rank Fusion (RRF) merges two ranked lists
- When to use vector vs keyword vs hybrid search

---

## The Problem: When Vector Search Fails

Vector search is great for **semantic** queries — finding content that *means*
the same thing as the question, even if the words are different. But it
struggles with:

| Query Type | Example | Vector Search Problem |
|-----------|---------|----------------------|
| Exact codes | "R-1 zone" | Similar embedding to "R-2 zone" |
| Numbers | "Section 4.3.2" | Embeddings don't capture numeric identity |
| Acronyms | "RLHF" | May not distinguish from "RL" or "HF" |
| Proper names | "Kaplan et al." | Similar embedding to other author names |

**Keyword search** excels here because it matches **exact tokens**. The word
"R-1" either appears in a chunk or it doesn't — no ambiguity.

But keyword search has its own weaknesses:

| Query Type | Example | Keyword Search Problem |
|-----------|---------|------------------------|
| Paraphrasing | "building height limit" vs "maximum structure elevation" | Different words, same meaning |
| Synonyms | "car" vs "automobile" | No match despite same concept |
| Conceptual | "How does attention work?" | Too generic, matches everything |

**Hybrid search** gets the best of both worlds.

---

## How BM25 / Full-Text Search Works

BM25 (Best Matching 25) is the standard ranking algorithm for keyword search.
Postgres implements a simplified version via `ts_rank`:

```
Score(query, doc) ∝ Σ  tf(term, doc) × idf(term)
                     term ∈ query

where:
  tf  = term frequency in the document (how often the word appears)
  idf = inverse document frequency (rarer words matter more)
```

**Intuition:** A chunk scores high if it contains rare, specific terms from
your query. Common words ("the", "is") contribute almost nothing.

### Postgres Implementation

Postgres provides native full-text search via:

1. **`tsvector`** — A processed representation of text with stemmed tokens:
   ```sql
   SELECT to_tsvector('english', 'The quick brown foxes jumped');
   -- Result: 'brown':3 'fox':4 'jump':5 'quick':2
   -- (stopwords removed, words stemmed)
   ```

2. **`tsquery`** — A search query:
   ```sql
   SELECT plainto_tsquery('english', 'quick fox');
   -- Result: 'quick' & 'fox'
   ```

3. **`ts_rank`** — Relevance scoring:
   ```sql
   SELECT ts_rank(tsv, plainto_tsquery('english', 'quick fox')) FROM chunks;
   ```

4. **GIN index** — Makes full-text search fast (inverted index):
   ```sql
   CREATE INDEX idx_fts ON pdf_chunks USING GIN (tsv);
   ```

---

## Reciprocal Rank Fusion (RRF)

The key challenge: how do you merge two ranked lists with incompatible scores?
Vector similarity is 0-1, while ts_rank produces arbitrary positive numbers.
You can't just average them.

**RRF** solves this by ignoring scores and using only **rank positions**:

```
RRF_score(doc) = Σ  1 / (k + rank_i(doc))
                 i ∈ rankers

where k = 60 (standard constant that reduces impact of outlier rankings)
```

### Example

A document appears at rank 2 in vector search and rank 5 in keyword search:

```
RRF = 1/(60+2) + 1/(60+5) = 0.0161 + 0.0154 = 0.0315
```

A document appearing at rank 1 in only vector search:

```
RRF = 1/(60+1) = 0.0164
```

The document appearing in **both** lists gets a higher score, even if it
wasn't #1 in either list. This is the power of fusion — agreement between
rankers is a strong signal.

### Why k=60?

The constant `k` controls how much we trust later positions:
- Small k (e.g., 1): Heavy penalty for being ranked low
- Large k (e.g., 100): Treats all ranks similarly
- k=60 is the standard from the original RRF paper (Cormack et al., 2009)

---

## Architecture

```
         User Query
         ┌────┴────┐
         │         │
         ▼         ▼
┌─────────────┐  ┌─────────────┐
│ Vector      │  │ Keyword     │
│ Search      │  │ Search      │
│ (semantic)  │  │ (BM25/FTS)  │
│ top-20      │  │ top-20      │
└──────┬──────┘  └──────┬──────┘
       │                 │
       └────────┬────────┘
                ▼
      ┌──────────────────┐
      │ Reciprocal Rank  │
      │ Fusion (RRF)     │
      │                  │
      │ Merge by rank,   │
      │ boost agreement  │
      └────────┬─────────┘
               │
               ▼
         Top-k results
         (best of both)
```

---

## Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `schema_fts.sql` | SQL migration: adds tsvector column + GIN index + trigger | — |
| `keyword_search.py` | BM25-style search via Postgres FTS | `keyword_search()`, `init_fts()` |
| `hybrid_search.py` | Vector + keyword fusion via RRF | `reciprocal_rank_fusion()`, `hybrid_search()` |
| `compare_search.py` | Side-by-side comparison on eval set | `evaluate_search_method()` |
| `test_tutorial9.py` | Unit tests for RRF logic | 4 tests |

---

## Setup

### Step 1: Apply the FTS schema

This adds a `tsvector` column to your existing `pdf_chunks` table:

```bash
uv run python tutorials/10-hybrid-search/keyword_search.py --init
```

What this does:
1. Adds a `tsv` column (type `tsvector`) to `pdf_chunks`
2. Populates it from existing `chunk_text`
3. Creates a GIN index for fast lookups
4. Adds a trigger so new inserts get `tsv` automatically

### Step 2: Test keyword search

```bash
uv run python tutorials/10-hybrid-search/keyword_search.py --query "R-1 zone setback"
```

### Step 3: Run hybrid search

```bash
uv run python tutorials/10-hybrid-search/hybrid_search.py --query "What is the attention formula?"
```

### Step 4: Compare methods

```bash
uv run python tutorials/10-hybrid-search/compare_search.py --k 5
```

---

## Tasks

### Task 1: Initialize Full-Text Search
Run `keyword_search.py --init`. Then verify the column exists:
```sql
SELECT chunk_text, ts_rank(tsv, plainto_tsquery('english', 'attention'))
FROM pdf_chunks
WHERE tsv @@ plainto_tsquery('english', 'attention')
ORDER BY ts_rank DESC LIMIT 3;
```

### Task 2: Compare on Exact Terms
Try these queries with both methods:
- Keyword-friendly: "R-1 residential zone", "Section 4.3.2", "GloVe"
- Vector-friendly: "rules about how tall buildings can be", "learning word representations"

### Task 3: Understand RRF
Read `hybrid_search.py`. Trace through `reciprocal_rank_fusion()` with the
test cases in `test_tutorial9.py`. Can you predict the output?

### Task 4: Run the Comparison
```bash
uv run python tutorials/10-hybrid-search/compare_search.py
```
Does hybrid consistently beat both individual methods?

### Task 5: Experiment with Parameters
- Change `vector_k` and `keyword_k` (candidates per method): 10, 20, 50
- Change the RRF constant `k`: try 1, 30, 60, 120
- Observe: how sensitive are results to these parameters?

---

## Expected Results

On a typical evaluation set, you should see something like:

```
Method               Precision@k    Recall@k      MRR
====================================================
Vector Only               0.350       0.420    0.520
Keyword Only              0.280       0.310    0.450
Hybrid (RRF)              0.420       0.480    0.600
====================================================
```

Hybrid wins because:
- It catches exact-match queries that vector misses (keyword contribution)
- It catches semantic queries that keyword misses (vector contribution)
- Agreement between both rankers is a strong relevance signal

---

## Theory & References

### Reciprocal Rank Fusion — The Original Paper

**"Reciprocal Rank Fusion outperforms Condorcet and Individual Rank Learning Methods"**
Cormack, Clarke & Butt, 2009 (University of Waterloo)
[SIGIR 2009](https://dl.acm.org/doi/10.1145/1571941.1572114)

The paper that introduced RRF. Key findings:
- RRF with k=60 consistently outperforms individual rankers
- It outperforms more complex fusion methods (CombMNZ, Condorcet, Borda)
- It requires no training data or score normalization
- The constant k=60 was empirically determined across TREC datasets

> "We demonstrate that RRF is effective regardless of whether the component
> results to be combined are of high or low quality."

This is why we use k=60 — it's battle-tested across decades of IR research.

### BM25 — The Standard Keyword Ranking Algorithm

**"The Probabilistic Relevance Framework: BM25 and Beyond"**
Robertson & Zaragoza, 2009 (Microsoft Research)
[Foundations and Trends in IR](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)

BM25 builds on TF-IDF with two key improvements:
- **Term frequency saturation**: diminishing returns from repeated terms
- **Document length normalization**: prevents long documents from dominating

The formula:

```
BM25(q, d) = Σ IDF(t) × [tf(t,d) × (k₁ + 1)] / [tf(t,d) + k₁ × (1 - b + b × |d|/avgdl)]
```

Where k₁ ≈ 1.2 and b ≈ 0.75 are standard parameters. Postgres's `ts_rank`
implements a simplified version without the full BM25 tuning parameters.

### Dense vs Sparse Retrieval

**"Dense Passage Retrieval for Open-Domain Question Answering"**
Karpukhin et al., 2020 (Meta AI)
[arXiv:2004.04906](https://arxiv.org/abs/2004.04906)

DPR showed that learned dense representations (bi-encoder embeddings) can
outperform BM25 on open-domain QA — but not always. The paper acknowledges
BM25 remains competitive for:
- Entity-centric queries (proper names)
- Rare term matching
- Very short passages

This motivates our hybrid approach: vector for semantics, keyword for exactness.

**"Text Embeddings by Weakly-Supervised Contrastive Pre-training"**
Wang et al., 2022 (Microsoft — E5 model)
[arXiv:2212.03533](https://arxiv.org/abs/2212.03533)

Modern embedding models (E5, BGE) are trained to handle both semantic and
keyword-style queries. But even the best models have failure modes that
keyword search covers. The hybrid approach is robust even as embedding
models improve.

### OpenAI on Search and Retrieval

**OpenAI — "Text Search Using Embeddings"** (2023)
[platform.openai.com/docs/guides/embeddings/use-cases](https://platform.openai.com/docs/guides/embeddings/use-cases)

OpenAI's guidance acknowledges that embeddings alone aren't always sufficient:
- Recommend "hybrid search" combining embeddings with keyword filters
- Suggest using metadata filters to narrow the search space
- Advise re-ranking results by relevance

**OpenAI — "What Makes a Good Embedding?"** (2022)
[openai.com/blog/new-and-improved-embedding-model](https://openai.com/blog/new-and-improved-embedding-model)

Discusses failure modes of embeddings:
- Short queries may not carry enough semantic signal
- Highly technical/domain-specific terms may not embed well
- Numbers and codes map to similar embedding regions

### Postgres Full-Text Search

**PostgreSQL Documentation — Full Text Search**
[postgresql.org/docs/current/textsearch.html](https://www.postgresql.org/docs/current/textsearch.html)

The authoritative reference for `tsvector`, `tsquery`, `ts_rank`, GIN indexes,
and custom text search configurations. Key concepts:
- Dictionaries handle stemming and stopwords
- GIN (Generalized Inverted Index) provides sub-millisecond lookup
- `plainto_tsquery` converts natural language to tsquery automatically
- `ts_rank` considers position and frequency for scoring

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `init_fts` fails | Make sure Postgres is running and `pdf_chunks` table exists |
| Keyword search returns 0 | Check that `tsv` column was populated: `SELECT COUNT(*) FROM pdf_chunks WHERE tsv IS NOT NULL` |
| Hybrid is slower than expected | GIN index may be missing — check `\di` in psql |
| RRF scores look wrong | Remember: higher RRF = better. Scores are small (0.01-0.03 range is normal) |

---

## Check Your Work

- [ ] Keyword search finds exact matches (codes, numbers) that vector misses
- [ ] Vector search finds paraphrased content that keyword misses
- [ ] Hybrid (RRF) consistently scores equal or better than either alone
- [ ] `compare_search.py` shows measurable improvement in MRR
- [ ] Can explain when to use which method (vector vs keyword vs hybrid)
- [ ] Understand why k=60 is the RRF standard

---

## What's Next

In **Tutorial 11**, we address the final quality bottleneck: even with hybrid
search, the top-5 results aren't perfectly ordered. A cross-encoder reranker
processes each (query, chunk) pair jointly — much slower, but dramatically
more accurate. We'll build a two-stage pipeline: fast recall (hybrid, top-50)
→ precise reranking (cross-encoder, top-5) → LLM generation.
