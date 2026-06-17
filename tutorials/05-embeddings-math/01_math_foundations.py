"""
Tutorial 05, Part 1 — Math Foundations of Embeddings

Implement vector operations from scratch with numpy, then demonstrate
why cosine similarity is the right metric for comparing text embeddings.

Usage:
    uv run python tutorials/05-embeddings-math/01_math_foundations.py
"""

import numpy as np


# ---------------------------------------------------------------------------
# Core operations (implement these)
# ---------------------------------------------------------------------------

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute the dot product of two vectors.
    dot(a, b) = sum(a_i * b_i)

    Do NOT use np.dot — implement with element-wise ops.
    """
    # TODO: Implement dot product manually
    raise NotImplementedError("TODO: implement dot product")


def magnitude(v: np.ndarray) -> float:
    """
    Compute the L2 norm (magnitude) of a vector.
    |v| = sqrt(sum(v_i^2))

    Do NOT use np.linalg.norm — implement manually.
    """
    # TODO: Implement magnitude
    raise NotImplementedError("TODO: implement magnitude")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    cos(a, b) = dot(a, b) / (|a| * |b|)

    Use your dot_product() and magnitude() functions.
    Returns a value between -1 and 1.
    """
    # TODO: Implement cosine similarity using your functions above
    raise NotImplementedError("TODO: implement cosine similarity")


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute Euclidean distance between two vectors.
    d(a, b) = sqrt(sum((a_i - b_i)^2))
    """
    # TODO: Implement Euclidean distance
    raise NotImplementedError("TODO: implement euclidean distance")


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------

def demo_similarity():
    """
    Show that cosine similarity captures semantic similarity better
    than Euclidean distance for text-like vectors.
    """
    print("=" * 60)
    print("DEMO: Cosine Similarity vs Euclidean Distance")
    print("=" * 60)

    # Simulated "embeddings" for demonstration
    # In reality these come from a model, but the math is the same
    np.random.seed(42)

    # Similar concepts (vectors pointing in similar directions)
    king = np.array([0.8, 0.2, 0.9, 0.1, 0.7])
    queen = np.array([0.75, 0.25, 0.85, 0.15, 0.65])
    man = np.array([0.6, 0.1, 0.7, 0.05, 0.5])
    woman = np.array([0.55, 0.15, 0.65, 0.1, 0.45])

    # Unrelated concept
    car = np.array([0.1, 0.9, 0.2, 0.8, 0.1])

    pairs = [
        ("king", "queen", king, queen),
        ("king", "man", king, man),
        ("queen", "woman", queen, woman),
        ("king", "car", king, car),
        ("woman", "car", woman, car),
    ]

    print(f"\n{'Pair':<20} {'Cosine Sim':<15} {'Euclidean Dist':<15}")
    print("-" * 50)
    for name_a, name_b, vec_a, vec_b in pairs:
        cos_sim = cosine_similarity(vec_a, vec_b)
        euc_dist = euclidean_distance(vec_a, vec_b)
        print(f"{name_a + ' vs ' + name_b:<20} {cos_sim:<15.4f} {euc_dist:<15.4f}")

    # Demonstrate scale invariance of cosine
    print("\n\nSCALE INVARIANCE (why cosine > euclidean for text):")
    print("-" * 50)
    scaled_king = king * 10  # Same direction, different magnitude
    print(f"king vs 10*king:")
    print(f"  Cosine:    {cosine_similarity(king, scaled_king):.4f} (same direction = 1.0)")
    print(f"  Euclidean: {euclidean_distance(king, scaled_king):.4f} (large distance!)")
    print("\nCosine only cares about DIRECTION, not magnitude.")
    print("This is why it works for embeddings: a longer document's")
    print("embedding may have larger magnitude, but similar meaning = similar direction.")


if __name__ == "__main__":
    demo_similarity()
