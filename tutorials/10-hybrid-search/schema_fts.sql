-- Add full-text search support to pdf_chunks table.
-- Run this AFTER the base schema from Tutorial 06.

-- Add tsvector column for full-text search
ALTER TABLE pdf_chunks ADD COLUMN IF NOT EXISTS tsv tsvector;

-- Populate tsvector from chunk_text
UPDATE pdf_chunks SET tsv = to_tsvector('english', chunk_text) WHERE tsv IS NULL;

-- Create GIN index for fast full-text search
CREATE INDEX IF NOT EXISTS idx_chunks_fts ON pdf_chunks USING GIN (tsv);

-- Trigger to auto-update tsvector on insert/update
CREATE OR REPLACE FUNCTION pdf_chunks_tsv_trigger() RETURNS trigger AS $$
BEGIN
    NEW.tsv := to_tsvector('english', NEW.chunk_text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_pdf_chunks_tsv ON pdf_chunks;
CREATE TRIGGER trg_pdf_chunks_tsv
    BEFORE INSERT OR UPDATE OF chunk_text ON pdf_chunks
    FOR EACH ROW EXECUTE FUNCTION pdf_chunks_tsv_trigger();
