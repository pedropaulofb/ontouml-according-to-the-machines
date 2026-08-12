"""Groq provider for Phase 2 page-review runs."""

from __future__ import annotations

import os
import time
from typing import Any

from groq import Groq
from provider_model_registry import (
    RegistryValidationError,
    require_executable_slot,
    validate_completion_token_cap,
)
from provider_runtime import classify_provider_failure, record_provider_event, record_provider_failure


class GroqProviderError(RuntimeError):
    """Raised when the Groq provider cannot complete a review."""


SYSTEM_MESSAGE = (
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
    "tokens per minute",
    "tpm",
    "requests per minute",
    "rpm",
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
    "service_unavailable",
    "temporarily unavailable",
    "timeout",
    "timed out",
    "connection error",
    "connection reset",
    "too busy",
    "overloaded",
    "capacity",
    "try again later",
    "unavailable",
)

NON_RETRYABLE_ERROR_MARKERS = (
    "request too large",
    "error code: 413",
    "context length",
    "invalid api key",
    "authentication",
    "unauthorized",
    "forbidden",
)


def _diagnostic(exc: Exception) -> str:
    return " ".join(
        [
            str(exc),
            str(getattr(exc, "code", "")),
            str(getattr(exc, "status", "")),
            str(getattr(exc, "reason", "")),
            str(getattr(exc, "body", "")),
        ]
    ).lower()


def _is_retryable_exception(exc: Exception) -> bool:
    """Return whether a Groq exception looks transient enough to retry."""
    diagnostic = _diagnostic(exc)
    if any(marker in diagnostic for marker in PROVIDER_POLICY_BLOCK_MARKERS):
        return False
    if any(marker in diagnostic for marker in QUOTA_OR_RATE_LIMIT_MARKERS):
        return False
    if any(marker in diagnostic for marker in NON_RETRYABLE_ERROR_MARKERS):
        return False
    return any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS)


def _provider_error_kind(exc: Exception) -> str:
    """Return a stable error category for workflow-level failure handling."""
    diagnostic = _diagnostic(exc)
    if any(marker in diagnostic for marker in PROVIDER_POLICY_BLOCK_MARKERS):
        return "provider_policy_block"
    if any(marker in diagnostic for marker in QUOTA_OR_RATE_LIMIT_MARKERS):
        return "rate_or_quota_limited"
    if "empty response" in diagnostic:
        return "empty_response"
    if "request too large" in diagnostic or "413" in diagnostic or "context length" in diagnostic:
        return "execution_configuration_block"
    if any(
        marker in diagnostic
        for marker in ("invalid api key", "authentication", "unauthorized", "forbidden", "401", "403")
    ):
        return "execution_configuration_block"
    if any(marker in diagnostic for marker in ("400", "404", "422", "invalid request", "bad request", "not found")):
        return "execution_configuration_block"
    if any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS):
        return "provider_unavailable"
    return "unknown_provider_error"


def _response_diagnostic(response: Any) -> str:
    """Return safe Groq response metadata for logs without exposing prompt text."""
    try:
        choice = response.choices[0]
    except Exception:
        return "choices=<unavailable>"

    finish_reason = getattr(choice, "finish_reason", None)
    usage = getattr(response, "usage", None)
    return f"finish_reason={finish_reason!r}; usage={usage!r}"


def _extract_content(response: Any) -> str:
    """Extract the generated message content from a Groq chat-completion response."""
    try:
        content = response.choices[0].message.content
    except Exception as exc:
        raise GroqProviderError(
            f"Groq response did not contain choices[0].message.content ({_response_diagnostic(response)})."
        ) from exc

    return content if isinstance(content, str) else ""


def _call_groq_once(
    *,
    client: Groq,
    model: str,
    review_input: str,
    max_completion_tokens: int,
) -> tuple[Any, dict[str, str]]:
    """Make one Groq chat-completion request."""
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": review_input},
        ],
        "temperature": 0,
        "max_completion_tokens": max_completion_tokens,
    }
    raw_resource = getattr(client.chat.completions, "with_raw_response", None)
    if raw_resource is None:
        return client.chat.completions.create(**kwargs), {}
    raw_response = raw_resource.create(**kwargs)
    return raw_response.parse(), dict(getattr(raw_response, "headers", {}) or {})


def _generate_with_retries(
    *,
    client: Groq,
    model: str,
    review_input: str,
    max_completion_tokens: int,
) -> str:
    """Call Groq with one retry for transient errors and no retries for quota/rate limits."""
    total_attempts = len(RETRY_DELAYS_SECONDS) + 1
    last_error: Exception | None = None
    prompt_chars = len(review_input)
    prompt_bytes = len(review_input.encode("utf-8"))

    for attempt_number in range(1, total_attempts + 1):
        try:
            response, headers = _call_groq_once(
                client=client,
                model=model,
                review_input=review_input,
                max_completion_tokens=max_completion_tokens,
            )
            content = _extract_content(response)
            if content.strip():
                record_provider_event(
                    provider="groq",
                    model=model,
                    outcome="success",
                    request_sent=True,
                    response=response,
                    headers=headers,
                )
                return content.strip() + "\n"

            diagnostic = _response_diagnostic(response)
            last_error = GroqProviderError(
                "Groq returned an empty response "
                f"({diagnostic}; prompt_chars={prompt_chars}; prompt_bytes={prompt_bytes}; "
                f"max_completion_tokens={max_completion_tokens})."
            )
            record_provider_failure(provider="groq", model=model, exc=last_error, request_sent=True)
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            last_error = exc
            classification = record_provider_failure(provider="groq", model=model, exc=exc, request_sent=True)
            if not classification.retryable_immediately:
                break

        if attempt_number == total_attempts:
            break

        time.sleep(RETRY_DELAYS_SECONDS[attempt_number - 1])

    if last_error is None:
        raise GroqProviderError("Groq API call failed without an exception.")

    kind = classify_provider_failure(provider="groq", model=model, exc=last_error).kind
    raise GroqProviderError(
        f"Groq API call failed after {attempt_number} attempt(s); provider_error_kind={kind}: {last_error}"
    ) from last_error


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
    """Generate one Phase 2 page-review issue comment using Groq."""
    del provider, review_date, page_path, commit_sha, page_content

    try:
        configured_slot = require_executable_slot("groq", model)
        validate_completion_token_cap(configured_slot, max_completion_tokens)
    except RegistryValidationError as exc:
        raise GroqProviderError(f"provider_error_kind=execution_configuration_block: {exc}") from exc

    if not os.getenv("GROQ_API_KEY"):
        error = GroqProviderError("GROQ_API_KEY environment variable is not set.")
        record_provider_failure(provider="groq", model=model, exc=error, request_sent=False)
        raise error

    if max_completion_tokens <= 0:
        raise GroqProviderError("max_completion_tokens must be greater than 0.")

    client = Groq()
    return _generate_with_retries(
        client=client,
        model=model,
        review_input=review_input,
        max_completion_tokens=max_completion_tokens,
    )
