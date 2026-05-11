"""Bengali question answering."""

from openai import OpenAI

_SYSTEM = """You are an expert Bengali language question answering assistant.
Given a context passage in Bengali and a question, answer the question accurately.
Base your answer strictly on the provided context.
If the answer is not in the context, say so clearly in the same language as the question."""


class QA:
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini"):
        self._client = client
        self._model = model

    def __call__(
        self,
        context: str,
        question: str,
        *,
        language: str = "bengali",
    ) -> str:
        """Answer a question based on Bengali context.

        Args:
            context: Bengali passage containing the answer.
            question: Question in Bengali or English.
            language: Response language — "bengali" (default) or "english".

        Returns:
            Answer string.
        """
        lang_instruction = (
            "Answer in Bengali (বাংলা)."
            if language == "bengali"
            else "Answer in English."
        )
        user_prompt = (
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"{lang_instruction}"
        )
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()
