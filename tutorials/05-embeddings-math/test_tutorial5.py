"""
Tutorial 05 — Tests

    uv run pytest tutorials/05-embeddings-math/ -v
"""

import numpy as np
from _01_math_foundations import dot_product, magnitude, cosine_similarity, euclidean_distance


def test_dot_product():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    result = dot_product(a, b)
    assert abs(result - 32.0) < 1e-6, f"expected 32.0, got {result}"


def test_dot_product_orthogonal():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert abs(dot_product(a, b)) < 1e-6, "orthogonal vectors should have dot product 0"


def test_magnitude():
    v = np.array([3.0, 4.0])
    assert abs(magnitude(v) - 5.0) < 1e-6, "magnitude of [3,4] should be 5"


def test_magnitude_unit_vector():
    v = np.array([1.0, 0.0, 0.0])
    assert abs(magnitude(v) - 1.0) < 1e-6


def test_cosine_similarity_identical():
    v = np.array([1.0, 2.0, 3.0])
    assert abs(cosine_similarity(v, v) - 1.0) < 1e-6, "same vector should have similarity 1.0"


def test_cosine_similarity_opposite():
    a = np.array([1.0, 0.0])
    b = np.array([-1.0, 0.0])
    assert abs(cosine_similarity(a, b) - (-1.0)) < 1e-6, "opposite vectors should have similarity -1.0"


def test_cosine_similarity_scale_invariant():
    a = np.array([1.0, 2.0, 3.0])
    b = a * 100
    assert abs(cosine_similarity(a, b) - 1.0) < 1e-6, "scaling should not change cosine similarity"


def test_euclidean_distance_same():
    v = np.array([1.0, 2.0, 3.0])
    assert abs(euclidean_distance(v, v)) < 1e-6, "distance to self should be 0"


def test_euclidean_distance_known():
    a = np.array([0.0, 0.0])
    b = np.array([3.0, 4.0])
    assert abs(euclidean_distance(a, b) - 5.0) < 1e-6
