"""Cerebras provider for Phase 2 page-review runs."""

from __future__ import annotations

import os
from typing import Any

from providers.openai_compatible import OpenAICompatibleProviderError, generate_chat_completion


class CerebrasProviderError(RuntimeError):
    """Raised when the Cerebras provider cannot complete a review."""


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
    """Generate one Phase 2 page-review issue comment using Cerebras."""
    del provider, review_date, page_path, commit_sha, page_content

    api_key = os.getenv("CEREBRAS_API_KEY")
    if not api_key:
        raise CerebrasProviderError("CEREBRAS_API_KEY environment variable is not set.")

    extra_body: dict[str, Any] | None = None
    extra_request_kwargs: dict[str, Any] | None = None
    if model == "zai-glm-4.7":
        # GLM 4.7 enables reasoning by default. For strict Markdown signal
        # generation, disable reasoning so the completion budget is available
        # for the required issue-comment content instead of hidden reasoning.
        extra_body = {"clear_thinking": False}
        extra_request_kwargs = {"reasoning_effort": "none"}

    try:
        return generate_chat_completion(
            provider_label="Cerebras",
            api_key=api_key,
            base_url=os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1"),
            model=model,
            review_input=review_input,
            max_completion_tokens=max_completion_tokens,
            extra_body=extra_body,
            extra_request_kwargs=extra_request_kwargs,
        )
    except OpenAICompatibleProviderError as exc:
        raise CerebrasProviderError(str(exc)) from exc
