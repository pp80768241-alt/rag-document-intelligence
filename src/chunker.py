import re


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    words = normalize_text(text).split()
    if not words:
        return []

    chunks = []
    current = []
    current_length = 0

    for word in words:
        extra = len(word) + (1 if current else 0)

        if current and current_length + extra > chunk_size:
            chunks.append(" ".join(current))

            overlap_words = []
            overlap_length = 0
            for previous in reversed(current):
                extra_overlap = len(previous) + (1 if overlap_words else 0)
                if overlap_length + extra_overlap > overlap:
                    break
                overlap_words.insert(0, previous)
                overlap_length += extra_overlap

            current = overlap_words
            current_length = overlap_length

        current.append(word)
        current_length += extra

    if current:
        chunks.append(" ".join(current))

    return chunks
