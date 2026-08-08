from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import fitz
from docx import Document

from .chunker import chunk_text


@dataclass
class LoadedChunk:
    text: str
    source_file: str
    location: str
    source_type: str


def _pdf(data: bytes, filename: str):
    output = []
    with fitz.open(stream=data, filetype="pdf") as pdf:
        for page_no, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()
            for piece in chunk_text(text):
                output.append(
                    LoadedChunk(piece, filename, f"Page {page_no}", "pdf")
                )
    return output


def _docx(data: bytes, filename: str):
    document = Document(BytesIO(data))
    text = "\n\n".join(
        p.text.strip()
        for p in document.paragraphs
        if p.text.strip()
    )
    return [
        LoadedChunk(piece, filename, "Document", "docx")
        for piece in chunk_text(text)
    ]


def _txt(data: bytes, filename: str):
    text = data.decode("utf-8", errors="replace")
    return [
        LoadedChunk(piece, filename, "Document", "txt")
        for piece in chunk_text(text)
    ]


def load_uploaded_file(uploaded_file):
    filename = Path(uploaded_file.name).name
    data = uploaded_file.getvalue()
    if not data:
        raise ValueError(f"{filename} is empty.")

    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        chunks = _pdf(data, filename)
    elif ext == ".docx":
        chunks = _docx(data, filename)
    elif ext == ".txt":
        chunks = _txt(data, filename)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX or TXT.")

    if not chunks:
        raise ValueError(
            f"No readable text found in {filename}. Scanned PDFs need OCR."
        )
    return chunks
