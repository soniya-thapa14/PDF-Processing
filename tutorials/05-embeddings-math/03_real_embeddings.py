"""
Tutorial 05, Part 3 — Real Embeddings with sentence-transformers

Use a pre-trained embedding model (all-MiniLM-L6-v2, 384 dimensions) to embed
the chunks from Tutorial 03. Save the results for Tutorial 06 (vector store).

Usage:
    uv run python tutorials/05-embeddings-math/03_real_embeddings.py
"""

import json
import sys
from pathlib import Path

import numpy as np

CHUNKS_DIR = Path(__file__).parent.parent / "03-chunking-strategies" / "results" / "chunks"
RESULTS_DIR = Path(__file__).parent / "results"


def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(model, chunks: list[str]) -> np.ndarray:
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar = True)
    return embeddings


def compute_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / norms
    return normalized @ normalized.T


def demo_similarity(model, chunks: list[str], embeddings: np.ndarray):
    """Show that same-section chunks are more similar than cross-section chunks."""
    print("\nSimilarity Demo:")
    print("-" * 50)

    if len(chunks) < 4:
        print("  Need at least 4 chunks for demo")
        return

    sim_matrix = compute_similarity_matrix(embeddings)

    print(f"  Chunk 0 vs Chunk 1 (adjacent):    {sim_matrix[0, 1]:.4f}")
    print(f"  Chunk 0 vs Chunk 2 (nearby):      {sim_matrix[0, 2]:.4f}")
    print(f"  Chunk 0 vs Chunk {len(chunks)-1} (far away): {sim_matrix[0, -1]:.4f}")

    upper_triangle = sim_matrix[np.triu_indices(len(chunks), k=1)]
    print(f"\n  Overall statistics:")
    print(f"    Mean similarity:   {upper_triangle.mean():.4f}")
    print(f"    Median similarity: {np.median(upper_triangle):.4f}")
    print(f"    Min similarity:    {upper_triangle.min():.4f}")
    print(f"    Max similarity:    {upper_triangle.max():.4f}")


def search(model, embeddings: np.ndarray, chunks: list[str], query: str, top_k: int = 5):
    query_vec = model.encode(query)
    sim = embeddings @ query_vec
    top_indicies = np.argsort(sim)[::-1][:top_k]
    return [(chunks[i], sim[i]) for i in top_indicies]


def main():
    print("=" * 60)
    print("REAL EMBEDDINGS (all-MiniLM-L6-v2)")
    print("=" * 60)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n1. Loading model...")
    model = load_model()
    print("   Model loaded (384 dimensions)")

    print("\n2. Loading chunks from Tutorial 03...")
    chunk_files = sorted(CHUNKS_DIR.glob("*.json"))
    if not chunk_files:
        print(f"   No chunk files found in {CHUNKS_DIR}")
        print("   Run Tutorial 03 first: uv run python tutorials/03-chunking-strategies/run_all.py")
        sys.exit(1)

    for chunk_file in chunk_files[:5]:
        data = json.loads(chunk_file.read_text())
        chunks = data.get("chunks", [])
        if not chunks:
            continue

        pdf_strat = chunk_file.stem
        print(f"\n   Processing {pdf_strat} ({len(chunks)} chunks)...")

        embeddings = embed_chunks(model, chunks)
        print(f"   Embeddings shape: {embeddings.shape}")

        out_path = RESULTS_DIR / f"{pdf_strat}.npy"
        np.save(out_path, embeddings)
        print(f"   Saved to {out_path.name}")

        meta_path = RESULTS_DIR / f"{pdf_strat}_meta.json"
        meta_path.write_text(json.dumps({
            "source_file": chunk_file.name,
            "num_chunks": len(chunks),
            "embedding_dim": embeddings.shape[1],
            "model": "all-MiniLM-L6-v2",
        }, indent=2))

        demo_similarity(model, chunks, embeddings)

    print("\n3. Interactive search demo...")
    # NEW
    if chunk_files:
        zoning_file = [f for f in chunk_files if "zoning" in f.name.lower()][0]
        data = json.loads(zoning_file.read_text())
        chunks = data.get("chunks", [])
        if chunks:
            embeddings = embed_chunks(model, chunks)
            query = "What are the zoning requirements for residential areas?"
            print(f"\n   Query: '{query}'")
            results = search(model, embeddings, chunks, query, top_k=3)
            for i, (chunk, score) in enumerate(results):
                print(f"   [{i+1}] (sim={score:.4f}) {chunk["content"]}...")

    print("\nDone! Embeddings saved to results/")


if __name__ == "__main__":
    main()
