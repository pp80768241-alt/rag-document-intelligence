import chromadb


class VectorStore:
    def __init__(self, path: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, ids, documents, embeddings, metadatas):
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(self, query_embedding, n_results: int):
        count = self.collection.count()
        if count == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
            include=["documents", "metadatas", "distances"],
        )

    def count(self):
        return self.collection.count()

    def delete_document(self, source_hash: str):
        results = self.collection.get(
            where={"source_hash": source_hash},
            include=["metadatas"],
        )
        ids = results.get("ids", [])
        if ids:
            self.collection.delete(ids=ids)
