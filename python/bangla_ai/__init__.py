"""bangla-ai-toolkit: AI-powered NLP library for the Bengali language."""

from .core import BanglaAI
from . import text
from .semantic import cosine_similarity, rank_by_similarity

__version__ = "0.3.0"
__all__ = ["BanglaAI", "text", "cosine_similarity", "rank_by_similarity"]
