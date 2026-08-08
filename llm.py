from openai import OpenAI
from .prompts import SYSTEM_PROMPT, SUMMARY_PROMPT


class OpenAILLM:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def answer(self, question: str, context: str):
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=f"DOCUMENT CONTEXT:\n{context}\n\nUSER QUESTION:\n{question}",
        )
        return response.output_text.strip()

    def summarize(self, context: str):
        response = self.client.responses.create(
            model=self.model,
            instructions=SUMMARY_PROMPT,
            input=f"DOCUMENT CONTEXT:\n{context}",
        )
        return response.output_text.strip()
