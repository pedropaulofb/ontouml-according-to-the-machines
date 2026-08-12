"""SambaNova provider for Phase 2 page-review runs."""

from __future__ import annotations

import os

from provider_model_registry import (
    RegistryValidationError,
    require_executable_slot,
    validate_completion_token_cap,
)

from providers.openai_compatible import OpenAICompatibleProviderError, generate_chat_completion


class SambaNovaProviderError(RuntimeError):
    """Raised when the SambaNova provider cannot complete a review."""


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
    """Generate one Phase 2 page-review issue comment using SambaNova."""
    del provider, review_date, page_path, commit_sha, page_content

    try:
        configured_slot = require_executable_slot("sambanova", model)
        validate_completion_token_cap(configured_slot, max_completion_tokens)
    except RegistryValidationError as exc:
        raise SambaNovaProviderError(f"provider_error_kind=execution_configuration_block: {exc}") from exc

    api_key = os.getenv("SAMBANOVA_API_KEY")
    if not api_key:
        raise SambaNovaProviderError("SAMBANOVA_API_KEY environment variable is not set.")

    try:
        return generate_chat_completion(
            provider_label="SambaNova",
            api_key=api_key,
            base_url=os.getenv("SAMBANOVA_BASE_URL", "https://api.sambanova.ai/v1"),
            model=model,
            review_input=review_input,
            max_completion_tokens=max_completion_tokens,
        )
    except OpenAICompatibleProviderError as exc:
        raise SambaNovaProviderError(str(exc)) from exc
