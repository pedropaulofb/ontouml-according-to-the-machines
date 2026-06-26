"""OpenRouter provider for Phase 2 page-review runs."""

from __future__ import annotations

import os

from providers.openai_compatible import OpenAICompatibleProviderError, generate_chat_completion


class OpenRouterProviderError(RuntimeError):
    """Raised when the OpenRouter provider cannot complete a review."""


ALLOWED_OPENROUTER_MODELS = frozenset(
    {
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "poolside/laguna-m.1:free",
    }
)


def generate_review(
    *,
    review_input: str,
    provider: str,
    model: str,
    review_date: str,
    page_path: str,
    commit_sha: str,
    page_content: str,
    max_completion_tokens: int,
) -> str:
    """Generate one Phase 2 page-review issue comment using OpenRouter."""
    del provider, review_date, page_path, commit_sha, page_content

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise OpenRouterProviderError("OPENROUTER_API_KEY environment variable is not set.")

    if model not in ALLOWED_OPENROUTER_MODELS:
        allowed_models = ", ".join(sorted(ALLOWED_OPENROUTER_MODELS))
        raise OpenRouterProviderError(
            f"Unsupported OpenRouter model: {model}. Allowed OpenRouter models: {allowed_models}."
        )

    try:
        return generate_chat_completion(
            provider_label="OpenRouter",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model=model,
            review_input=review_input,
            max_completion_tokens=max_completion_tokens,
        )
    except OpenAICompatibleProviderError as exc:
        raise OpenRouterProviderError(str(exc)) from exc
