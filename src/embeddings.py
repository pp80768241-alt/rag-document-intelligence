from openai import OpenAI


class OpenAIEmbedder:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed(self, texts):
        if not texts:
            return []
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str):
        return self.embed([text])[0]
