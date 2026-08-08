from .document_loader import LoadedChunk
from .embeddings import OpenAIEmbedder
from .llm import OpenAILLM
from .utils import sha256_bytes, stable_chunk_id, similarity_from_cosine_distance
from .vector_store import VectorStore


class RAGService:
    def __init__(self, settings):
        self.settings = settings
        self.top_k = settings.top_k
        self.embedder = OpenAIEmbedder(
            settings.openai_api_key,
            settings.openai_embedding_model,
        )
        self.llm = OpenAILLM(
            settings.openai_api_key,
            settings.openai_chat_model,
        )
        self.store = VectorStore(
            settings.chroma_path,
            settings.collection_name,
        )

    def index_document(self, chunks: list[LoadedChunk]):
        if not chunks:
            raise ValueError("No chunks were produced.")

        source_file = chunks[0].source_file
        source_hash = sha256_bytes(
            "\n".join(chunk.text for chunk in chunks).encode("utf-8")
        )

        self.store.delete_document(source_hash)

        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedder.embed(texts)

        ids = [
            stable_chunk_id(source_hash, i)
            for i in range(len(chunks))
        ]

        metadata = [
            {
                "source_file": chunk.source_file,
                "location": chunk.location,
                "source_type": chunk.source_type,
                "source_hash": source_hash,
                "chunk_index": i,
            }
            for i, chunk in enumerate(chunks)
        ]

        self.store.add(ids, texts, embeddings, metadata)

        return {
            "status": "indexed",
            "file": source_file,
            "chunks": len(chunks),
            "source_hash": source_hash,
        }

    def _retrieve(self, question: str):
        embedding = self.embedder.embed_query(question)
        results = self.store.query(embedding, self.top_k)

        retrieved = []
        for i, (document, metadata, distance) in enumerate(
            zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ),
            start=1,
        ):
            retrieved.append({
                "index": i,
                "text": document,
                "file": metadata.get("source_file", "Unknown"),
                "location": metadata.get("location", "Unknown"),
                "similarity": similarity_from_cosine_distance(distance),
            })
        return retrieved

    @staticmethod
    def _context(chunks):
        return "\n\n---\n\n".join(
            f"[{c['index']}] Source: {c['file']} | {c['location']}\n{c['text']}"
            for c in chunks
        )

    def answer(self, question: str):
        if self.store.count() == 0:
            raise ValueError("Please index at least one document first.")

        retrieved = self._retrieve(question)
        answer = self.llm.answer(question, self._context(retrieved))

        sources = [
            {
                "index": c["index"],
                "file": c["file"],
                "location": c["location"],
                "similarity": c["similarity"],
                "preview": c["text"][:300] + ("..." if len(c["text"]) > 300 else ""),
            }
            for c in retrieved
        ]
        return {"answer": answer, "sources": sources}

    def summarize(self):
        if self.store.count() == 0:
            raise ValueError("Please index at least one document first.")

        result = self.store.collection.get(
            limit=min(self.store.count(), 30),
            include=["documents", "metadatas"],
        )

        chunks = []
        for i, (document, metadata) in enumerate(
            zip(result["documents"], result["metadatas"]),
            start=1,
        ):
            chunks.append({
                "index": i,
                "text": document,
                "file": metadata.get("source_file", "Unknown"),
                "location": metadata.get("location", "Unknown"),
            })

        raw = self.llm.summarize(self._context(chunks))
        key_points = [
            line.lstrip("-* ").strip()
            for line in raw.splitlines()
            if line.strip().startswith(("-", "*"))
        ]

        return {
            "summary": raw,
            "key_points": key_points[:8],
        }

    def collection_stats(self):
        return {
            "chunks": self.store.count(),
            "collection": self.settings.collection_name,
        }
