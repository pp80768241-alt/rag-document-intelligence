# RAG-Based Document Intelligence System

A portfolio-ready GenAI application for uploading PDF, DOCX and TXT files, indexing them with embeddings, asking questions using semantic retrieval, and receiving grounded answers with source citations.

## Features
- PDF, DOCX and TXT ingestion
- Text extraction and overlapping chunking
- OpenAI embeddings
- Persistent ChromaDB vector store
- Semantic Top-K retrieval
- Grounded LLM answers with numbered citations
- Collection summarization and key points
- SHA-256 based duplicate handling
- Streamlit chat UI
- Docker + GitHub Actions CI
- Unit tests

## Tech Stack
Python 3.11+, Streamlit, OpenAI API, ChromaDB, PyMuPDF, python-docx, Pydantic Settings, pytest.

## Run locally

```bash
git clone https://github.com/YOUR_USERNAME/rag-document-intelligence.git
cd rag-document-intelligence

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# Add OPENAI_API_KEY to .env

streamlit run app.py
```

## Docker

```bash
docker compose up --build
```

Open http://localhost:8501

## Example questions
- What is the main objective of this document?
- Summarize the methodology.
- What risks are mentioned?
- What are the important requirements?
- Compare the approaches discussed.
- What conclusions are supported by the documents?

## Project structure

```text
rag-document-intelligence/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── LICENSE
├── docs/ARCHITECTURE.md
├── src/
│   ├── config.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── prompts.py
│   ├── llm.py
│   ├── rag_service.py
│   └── utils.py
├── tests/
│   ├── test_chunker.py
│   ├── test_loader.py
│   └── test_utils.py
└── .github/workflows/ci.yml
```

## Resume bullet

**RAG-Based Document Intelligence System** — Built a multi-format RAG application using Python, Streamlit, OpenAI embeddings and ChromaDB for semantic document retrieval and grounded question answering; implemented document chunking, persistent vector search, duplicate detection, source citations and automated summarization.
