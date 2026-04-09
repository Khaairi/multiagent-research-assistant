from google.adk.models.lite_llm import LiteLlm

from research_agent.config import OLLAMA_MODEL


def make_model() -> LiteLlm:
    """Returns a LiteLlm instance pointing at the local Ollama server."""
    return LiteLlm(model=f"ollama_chat/{OLLAMA_MODEL}")