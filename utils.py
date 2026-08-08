import hashlib


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_chunk_id(source_hash: str, index: int) -> str:
    return f"{source_hash[:16]}-{index:06d}"


def similarity_from_cosine_distance(distance: float) -> float:
    return max(0.0, min(1.0, 1.0 - float(distance)))
