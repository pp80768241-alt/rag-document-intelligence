from src.utils import (
    sha256_bytes,
    similarity_from_cosine_distance,
    stable_chunk_id,
)


def test_hash_is_stable():
    assert sha256_bytes(b"abc") == sha256_bytes(b"abc")


def test_chunk_id():
    assert stable_chunk_id("abcdef1234567890", 2) == "abcdef1234567890-000002"


def test_similarity():
    assert similarity_from_cosine_distance(0.0) == 1.0
    assert similarity_from_cosine_distance(1.0) == 0.0
