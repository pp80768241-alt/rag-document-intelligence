from src.document_loader import load_uploaded_file


class FakeUpload:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def getvalue(self):
        return self.data


def test_txt_loader():
    upload = FakeUpload("notes.txt", b"Hello RAG world. " * 20)
    chunks = load_uploaded_file(upload)
    assert chunks
    assert chunks[0].source_file == "notes.txt"


def test_unsupported_extension():
    upload = FakeUpload("image.png", b"abc")
    try:
        load_uploaded_file(upload)
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        assert False
