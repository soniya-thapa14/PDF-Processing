-- Schema for storing PDF chunk embeddings with pgvector
-- Automatically run on first container startup via docker-entrypoint-initdb.d

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS pdf_chunks (
    id              SERIAL PRIMARY KEY,
    pdf_name        TEXT NOT NULL,
    chunk_strategy  TEXT NOT NULL,
    chunk_index     INTEGER NOT NULL,
    chunk_text      TEXT NOT NULL,
    embedding       vector(384) NOT NULL,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (pdf_name, chunk_strategy, chunk_index)
);

-- IVFFlat index for approximate nearest neighbor search
-- Lists=100 is a good default for up to ~100k vectors
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_ivfflat
    ON pdf_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Metadata indexes for filtered queries
CREATE INDEX IF NOT EXISTS idx_chunks_pdf_name ON pdf_chunks (pdf_name);
CREATE INDEX IF NOT EXISTS idx_chunks_strategy ON pdf_chunks (chunk_strategy);
