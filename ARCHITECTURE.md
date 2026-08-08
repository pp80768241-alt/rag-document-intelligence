# Architecture

## Ingestion

```text
Upload
  ↓
PDF/DOCX/TXT extraction
  ↓
Normalization + overlapping chunks
  ↓
OpenAI embeddings
  ↓
Persistent ChromaDB
```

## Question answering

```text
Question
  ↓
Query embedding
  ↓
Top-K semantic retrieval
  ↓
Numbered source context
  ↓
OpenAI Responses API
  ↓
Grounded answer + citations
```

## Metadata stored per chunk
- source filename
- page/section location
- file type
- SHA-256 source hash
- chunk index

## Why RAG?
Retrieval-Augmented Generation supplies relevant document passages to the model at generation time, allowing the application to answer questions about user-provided documents instead of relying only on the model's pretrained knowledge.

## Production upgrades
- OCR for scanned PDFs
- hybrid BM25 + vector retrieval
- reranking
- document-level permissions
- PII redaction
- prompt-injection defenses
- background ingestion workers
- PostgreSQL metadata
- Redis caching
- tracing/evaluation
- model/provider abstraction
