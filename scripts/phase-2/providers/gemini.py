"""Google Gemini provider for Phase 2 page-review runs."""

from __future__ import annotations

import os
import time
from typing import Any

from google import genai
from google.genai import types
from provider_model_registry import (
    RegistryValidationError,
    require_executable_slot,
    validate_completion_token_cap,
)
from provider_runtime import classify_provider_failure, record_provider_event, record_provider_failure
from reasoning_policy import gemini_thinking_kwargs


class GeminiProviderError(RuntimeError):
    """Raised when the Gemini provider cannot complete a review."""


SYSTEM_INSTRUCTION = (
    "Return only the GitHub issue comment requested by the prompt. "
    "Do not include analysis, prefaces, explanations, or code fences. "
    "Focus on concrete candidate findings for later aggregation."
)

# Initial request plus at most one retry for genuinely transient failures.
RETRY_DELAYS_SECONDS = (15.0,)

QUOTA_OR_RATE_LIMIT_MARKERS = (
    "429",
    "rate_limit",
    "rate limit",
    "rate_limit_exceeded",
    "resource_exhausted",
    "quota",
    "too many requests",
    "requests per day",
    "generate_content_free_tier_requests",
    "generaterequestsperday",
    "tokens per minute",
    "tpm",
)

PROVIDER_POLICY_BLOCK_MARKERS = (
    "402",
    "billing",
    "payment required",
    "payment method",
    "insufficient credit",
    "insufficient funds",
    "purchase",
    "paygo",
    "pay-as-you-go",
    "paid tier",
)

TRANSIENT_ERROR_MARKERS = (
    "500",
    "502",
    "503",
    "504",
    "UNAVAILABLE",
    "SERVICE_UNAVAILABLE",
    "temporarily unavailable",
    "timeout",
    "timed out",
    "too busy",
    "overloaded",
    "capacity",
    "try again later",
)

NON_RETRYABLE_ERROR_MARKERS = (
    "400",
    "401",
    "403",
    "404",
    "413",
    "invalid api key",
    "authentication",
    "unauthorized",
    "forbidden",
    "context length",
)


def _api_key() -> str:
    """Return the configured Gemini API key or raise a provider error."""
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise GeminiProviderError("Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set.")
    return key


def _part_text(part: Any) -> str:
    """Extract text from one Gemini response part when available."""
    if getattr(part, "thought", False):
        return ""
    text = getattr(part, "text", None)
    return text if isinstance(text, str) else ""


def _candidate_text(candidate: Any) -> str:
    """Extract text from one Gemini candidate when response.text is unavailable."""
    content = getattr(candidate, "content", None)
    parts = getattr(content, "parts", None) if content is not None else None
    if not parts:
        return ""
    return "".join(_part_text(part) for part in parts)


def _response_text(response: Any) -> str:
    """Extract generated text from a Gemini response."""
    candidates = getattr(response, "candidates", None) or []
    candidate_text = "".join(_candidate_text(candidate) for candidate in candidates)
    if candidates:
        return candidate_text
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text

    return ""


def _generation_config(*, slot: Any, max_completion_tokens: int) -> types.GenerateContentConfig:
    """Build the Gemini generation config used by Phase 2 check agents."""
    kwargs: dict[str, Any] = {
        "system_instruction": SYSTEM_INSTRUCTION,
        "max_output_tokens": max_completion_tokens,
    }
    if "temperature" in slot.request_config:
        kwargs["temperature"] = slot.request_config["temperature"]
    kwargs["thinking_config"] = types.ThinkingConfig(**gemini_thinking_kwargs(slot))
    return types.GenerateContentConfig(**kwargs)


def _diagnostic(exc: Exception) -> str:
    return " ".join(
        [
            str(exc),
            str(getattr(exc, "code", "")),
            str(getattr(exc, "status", "")),
            str(getattr(exc, "reason", "")),
        ]
    )


def _is_retryable_error(exc: Exception) -> bool:
    """Return whether an exception should receive the single transient retry."""
    diagnostic_lower = _diagnostic(exc).lower()
    diagnostic_upper = _diagnostic(exc).upper()
    if any(marker in diagnostic_lower for marker in PROVIDER_POLICY_BLOCK_MARKERS):
        return False
    if any(marker in diagnostic_lower for marker in QUOTA_OR_RATE_LIMIT_MARKERS):
        return False
    if any(marker in diagnostic_lower for marker in NON_RETRYABLE_ERROR_MARKERS):
        return False
    return any(marker in diagnostic_upper for marker in TRANSIENT_ERROR_MARKERS)


def _provider_error_kind(exc: Exception) -> str:
    """Return a stable error category for workflow-level failure handling."""
    diagnostic_lower = _diagnostic(exc).lower()
    diagnostic_upper = _diagnostic(exc).upper()
    if any(marker in diagnostic_lower for marker in PROVIDER_POLICY_BLOCK_MARKERS):
        return "provider_policy_block"
    if any(marker in diagnostic_lower for marker in QUOTA_OR_RATE_LIMIT_MARKERS):
        return "rate_or_quota_limited"
    if "empty response" in diagnostic_lower:
        return "empty_response"
    if "request too large" in diagnostic_lower or "413" in diagnostic_lower or "context length" in diagnostic_lower:
        return "execution_configuration_block"
    if any(
        marker in diagnostic_lower
        for marker in ("invalid api key", "authentication", "unauthorized", "forbidden", "401", "403")
    ):
        return "execution_configuration_block"
    if any(
        marker in diagnostic_lower for marker in ("400", "404", "422", "invalid request", "bad request", "not found")
    ):
        return "execution_configuration_block"
    if any(marker in diagnostic_upper for marker in TRANSIENT_ERROR_MARKERS):
        return "provider_unavailable"
    return "unknown_provider_error"


def _generate_content_with_retries(
    *,
    client: genai.Client,
    model: str,
    review_input: str,
    config: types.GenerateContentConfig,
) -> Any:
    """Call Gemini with one retry for transient errors and no retries for quota/rate limits."""
    total_attempts = len(RETRY_DELAYS_SECONDS) + 1
    attempts_made = 0
    last_exc: Exception | None = None

    for attempt_number in range(1, total_attempts + 1):
        attempts_made = attempt_number
        try:
            return client.models.generate_content(
                model=model,
                contents=review_input,
                config=config,
            )
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            last_exc = exc
            classification = record_provider_failure(provider="gemini", model=model, exc=exc, request_sent=True)
            if attempt_number == total_attempts or not classification.retryable_immediately:
                break
            time.sleep(RETRY_DELAYS_SECONDS[attempt_number - 1])

    if last_exc is None:
        raise GeminiProviderError("Gemini API call failed without an exception.")
    kind = classify_provider_failure(provider="gemini", model=model, exc=last_exc).kind
    raise GeminiProviderError(
        f"Gemini API call failed after {attempts_made} attempt(s); provider_error_kind={kind}: {last_exc}"
    ) from last_exc


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
    """Generate one Phase 2 page-review issue comment using Google Gemini."""
    del provider, review_date, page_path, commit_sha, page_content

    try:
        configured_slot = require_executable_slot("gemini", model)
        validate_completion_token_cap(configured_slot, max_completion_tokens)
    except RegistryValidationError as exc:
        raise GeminiProviderError(f"provider_error_kind=execution_configuration_block: {exc}") from exc

    if max_completion_tokens <= 0:
        raise GeminiProviderError("max_completion_tokens must be greater than 0.")

    try:
        api_key = _api_key()
    except GeminiProviderError as exc:
        record_provider_failure(provider="gemini", model=model, exc=exc, request_sent=False)
        raise
    client = genai.Client(api_key=api_key)
    config = _generation_config(slot=configured_slot, max_completion_tokens=max_completion_tokens)
    response = _generate_content_with_retries(
        client=client,
        model=model,
        review_input=review_input,
        config=config,
    )

    content = _response_text(response)
    if not content.strip():
        error = GeminiProviderError("Gemini returned an empty response.")
        record_provider_failure(provider="gemini", model=model, exc=error, request_sent=True)
        raise error
    record_provider_event(
        provider="gemini",
        model=model,
        outcome="success",
        request_sent=True,
        response=response,
    )
    return content.strip() + "\n"
