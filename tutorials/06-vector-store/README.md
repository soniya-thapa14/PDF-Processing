# Tutorial 06 — Store Embeddings in Postgres (pgvector)

## What you'll build

Persist the embeddings from Tutorial 05 into a local Postgres database using
the `pgvector` extension. Define a schema, insert embeddings, and run
similarity search queries — the retrieval half of RAG.

## Why it matters

Embeddings in `.npy` files are fine for experiments. In production, you need:
- Persistence across restarts
- Indexed similarity search (not brute-force O(n))
- Filtering by metadata (search within one document, one strategy, etc.)
- ACID guarantees

pgvector gives you all of this inside Postgres — no separate vector DB needed.

## Prerequisites

- Docker installed and running
- Embeddings from Tutorial 05 (`.npy` files in `../05-embeddings-math/results/`)

## Setup

Start Postgres with pgvector:

```bash
cd tutorials/06-vector-store
docker compose up -d
```

This starts Postgres 16 + pgvector on port 5433 (non-default to avoid conflicts).

Create the schema:
```bash
uv run python tutorials/06-vector-store/store_embeddings.py --init
```

## Your task

1. **Start the database** — `docker compose up -d`
2. **Create schema** — implement `create_schema()` in `store_embeddings.py`
3. **Insert embeddings** — implement `insert_embeddings()` to load `.npy` files and insert rows
4. **Search** — implement `search()` in `search.py` to find similar chunks
5. **Experiment** — try different index types (ivfflat vs hnsw), filter by PDF name

## Run / check your work

```bash
# Start database:
cd tutorials/06-vector-store && docker compose up -d

# Initialize schema and insert embeddings:
uv run python tutorials/06-vector-store/store_embeddings.py

# Run similarity search:
uv run python tutorials/06-vector-store/search.py "What are the zoning requirements?"

# Tests:
uv run pytest tutorials/06-vector-store/ -v

# Cleanup:
docker compose down -v
```

## Definition of done

- [ ] `docker compose up -d` starts Postgres with pgvector
- [ ] Schema created with vector column and index
- [ ] Embeddings from Tutorial 05 inserted into the database
- [ ] Similarity search returns relevant chunks
- [ ] `uv run pytest tutorials/06-vector-store/ -v` all green

## Stretch goals

1. Compare search quality: ivfflat vs hnsw index (speed vs recall)
2. Add a metadata filter: search only within `financial_report` chunks
3. Implement hybrid search: combine vector similarity with keyword matching
