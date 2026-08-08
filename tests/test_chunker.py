from src.chunker import chunk_text, normalize_text


def test_normalize_text():
    assert normalize_text(" hello   world \n\n\n test ") == "hello world\n\n test"


def test_chunking():
    chunks = chunk_text(" ".join(["word"] * 100), chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)


def test_invalid_overlap():
    try:
        chunk_text("hello", chunk_size=10, overlap=10)
    except ValueError:
        assert True
    else:
        assert False
