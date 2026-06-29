# Tutorial 09 — Hybrid Search (Vector + BM25)

## Goal

Combine semantic vector search with keyword-based BM25 search using Postgres
full-text search. Learn when hybrid beats pure vector search.

## Key Concepts

1. **BM25 / TF-IDF** — Term-frequency keyword matching, excels at exact terms
2. **Postgres `tsvector`** — Native full-text search with `ts_rank` scoring
3. **Reciprocal Rank Fusion (RRF)** — Combine two ranked lists without score normalization
4. **When vector fails** — Exact names, codes, numbers, acronyms
5. **When keyword fails** — Paraphrasing, synonyms, conceptual queries

## The RRF Formula

```
RRF_score(doc) = Σ  1 / (k + rank_i(doc))
                 i

where k = 60 (constant), rank_i = position in ranker i's list
```

## Files

| File | Purpose |
|------|---------|
| `schema_fts.sql` | Adds tsvector column + GIN index to pdf_chunks |
| `keyword_search.py` | BM25-style search using Postgres full-text search |
| `hybrid_search.py` | Combines vector + keyword via RRF |
| `compare_search.py` | Side-by-side comparison on eval set |
| `test_tutorial9.py` | Unit tests |

## Setup

```bash
# Apply the FTS schema migration
uv run python tutorials/09-hybrid-search/keyword_search.py --init

# Run comparison
uv run python tutorials/09-hybrid-search/compare_search.py
```

## Tasks

1. Run `keyword_search.py --init` to add full-text search columns
2. Try keyword-only search on exact terms (zone codes, names)
3. Try vector-only search on conceptual questions
4. Run hybrid search and compare results
5. Run `compare_search.py` with the eval set — observe when hybrid wins

## Check Your Work

- [ ] Keyword search finds exact matches (codes, numbers) that vector misses
- [ ] Vector search finds paraphrased content that keyword misses
- [ ] Hybrid (RRF) consistently scores equal or better than either alone
- [ ] `compare_search.py` shows measurable improvement in MRR
