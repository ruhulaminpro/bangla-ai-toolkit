"""Bengali text summarization."""

from openai import OpenAI

_SYSTEM = """You are an expert Bengali language summarizer.
Summarize the provided Bengali text clearly and concisely.
Preserve key information and maintain the original language (Bengali).
Output only the summary — no preamble, no explanations."""


class Summarizer:
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini"):
        self._client = client
        self._model = model

    def __call__(
        self,
        text: str,
        *,
        max_sentences: int = 3,
        language: str = "bengali",
    ) -> str:
        """Summarize Bengali text.

        Args:
            text: Bengali input text.
            max_sentences: Target summary length in sentences.
            language: Output language — "bengali" (default) or "english".

        Returns:
            Summary string.
        """
        lang_instruction = (
            "Respond in Bengali (বাংলা)."
            if language == "bengali"
            else "Respond in English."
        )
        user_prompt = (
            f"Summarize the following text in {max_sentences} sentences or fewer. "
            f"{lang_instruction}\n\nText:\n{text}"
        )
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
