"""OpenRouter provider for Phase 2 page-review runs."""

from __future__ import annotations

import os

from free_policy import FreePolicyError, verify_openrouter_free_model
from provider_model_registry import (
    RegistryValidationError,
    require_executable_slot,
    validate_completion_token_cap,
)

from providers.openai_compatible import OpenAICompatibleProviderError, generate_chat_completion


class OpenRouterProviderError(RuntimeError):
    """Raised when the OpenRouter provider cannot complete a review."""


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

    try:
        configured_slot = require_executable_slot("openrouter", model)
        validate_completion_token_cap(configured_slot, max_completion_tokens)
    except RegistryValidationError as exc:
        raise OpenRouterProviderError(f"provider_error_kind=execution_configuration_block: {exc}") from exc

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise OpenRouterProviderError("OPENROUTER_API_KEY environment variable is not set.")

    try:
        verify_openrouter_free_model(model, api_key)
    except FreePolicyError as exc:
        raise OpenRouterProviderError(str(exc)) from exc

    try:
        return generate_chat_completion(
            provider_label="OpenRouter",
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model=model,
            review_input=review_input,
            max_completion_tokens=max_completion_tokens,
            extra_body={"provider": {"allow_fallbacks": False}},
        )
    except OpenAICompatibleProviderError as exc:
        raise OpenRouterProviderError(str(exc)) from exc
