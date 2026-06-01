import os
from typing import Optional

from src.core.llm_provider import LLMProvider


def _build_openai(model_name: str) -> Optional[LLMProvider]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return None

    from src.core.openai_provider import OpenAIProvider

    return OpenAIProvider(model_name=model_name, api_key=api_key)


def _build_gemini(model_name: str) -> Optional[LLMProvider]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    from src.core.gemini_provider import GeminiProvider

    if not model_name.startswith("gemini"):
        model_name = "gemini-1.5-flash"
    return GeminiProvider(model_name=model_name, api_key=api_key)


def _build_local() -> Optional[LLMProvider]:
    model_path = os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf")
    if not os.path.exists(model_path):
        return None

    from src.core.local_provider import LocalProvider

    return LocalProvider(model_path=model_path)


def build_llm_from_env() -> LLMProvider:
    """
    Build an LLM provider based on DEFAULT_PROVIDER with graceful fallback.
    Priority order follows user preference, then falls back to available providers.
    """
    preferred = os.getenv("DEFAULT_PROVIDER", "openai").strip().lower()
    model_name = os.getenv("DEFAULT_MODEL", "gpt-4o").strip()

    builders = {
        "openai": lambda: _build_openai(model_name),
        "google": lambda: _build_gemini(model_name),
        "gemini": lambda: _build_gemini(model_name),
        "local": _build_local,
    }

    fallback_order = [preferred, "openai", "google", "local"]
    seen = set()

    for provider_key in fallback_order:
        if provider_key in seen:
            continue
        seen.add(provider_key)

        builder = builders.get(provider_key)
        if not builder:
            continue

        provider = builder()
        if provider:
            return provider

    raise RuntimeError(
        "No available LLM provider. Configure one of: OPENAI_API_KEY, GEMINI_API_KEY, or LOCAL_MODEL_PATH."
    )
