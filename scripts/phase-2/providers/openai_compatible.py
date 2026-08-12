"""Shared OpenAI-compatible provider utilities for Phase 2 check-agent runs."""

from __future__ import annotations

import time
from typing import Any

from openai import OpenAI

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
    "requests per day",
    "tokens per minute",
    "tpm",
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
    "400",
    "401",
    "403",
    "404",
    "413",
    "422",
    "request too large",
    "context length",
    "maximum context length",
    "invalid api key",
    "authentication",
    "unauthorized",
    "forbidden",
)


class OpenAICompatibleProviderError(RuntimeError):
    """Raised when an OpenAI-compatible provider cannot complete a review."""


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


def _is_quota_or_rate_limit_error(exc: Exception) -> bool:
    diagnostic = _diagnostic(exc)
    return any(marker in diagnostic for marker in QUOTA_OR_RATE_LIMIT_MARKERS)


def _is_retryable_exception(exc: Exception) -> bool:
    diagnostic = _diagnostic(exc)
    if any(marker in diagnostic for marker in PROVIDER_POLICY_BLOCK_MARKERS):
        return False
    if _is_quota_or_rate_limit_error(exc):
        return False
    if any(marker in diagnostic for marker in NON_RETRYABLE_ERROR_MARKERS):
        return False
    return any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS)


def _provider_error_kind(exc: Exception) -> str:
    """Return a stable error category for workflow-level failure handling."""
    diagnostic = _diagnostic(exc)
    if any(marker in diagnostic for marker in PROVIDER_POLICY_BLOCK_MARKERS):
        return "provider_policy_block"
    if _is_quota_or_rate_limit_error(exc):
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
    try:
        choice = response.choices[0]
    except Exception:
        return "choices=<unavailable>"

    finish_reason = getattr(choice, "finish_reason", None)
    usage = getattr(response, "usage", None)
    return f"finish_reason={finish_reason!r}; usage={usage!r}"


def _extract_content(response: Any) -> str:
    try:
        content = response.choices[0].message.content
    except Exception as exc:
        raise OpenAICompatibleProviderError(
            f"OpenAI-compatible response did not contain choices[0].message.content ({_response_diagnostic(response)})."
        ) from exc

    return content if isinstance(content, str) else ""


def generate_chat_completion(
    *,
    provider_label: str,
    api_key: str,
    base_url: str,
    model: str,
    review_input: str,
    max_completion_tokens: int,
    extra_body: dict[str, Any] | None = None,
    extra_request_kwargs: dict[str, Any] | None = None,
) -> str:
    """Generate one strict check-agent comment through an OpenAI-compatible API.

    ``extra_body`` is for provider-specific OpenAI-compatible extensions that
    must be merged into the JSON request body by the OpenAI client.
    ``extra_request_kwargs`` is for standard request parameters, such as
    reasoning controls supported by the provider and by the installed OpenAI
    SDK version.
    """
    if max_completion_tokens <= 0:
        raise OpenAICompatibleProviderError("max_completion_tokens must be greater than 0.")

    client = OpenAI(base_url=base_url, api_key=api_key)
    total_attempts = len(RETRY_DELAYS_SECONDS) + 1
    last_error: Exception | None = None
    prompt_chars = len(review_input)
    prompt_bytes = len(review_input.encode("utf-8"))

    for attempt_number in range(1, total_attempts + 1):
        try:
            kwargs: dict[str, Any] = {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": review_input},
                ],
                "temperature": 0,
                "max_completion_tokens": max_completion_tokens,
            }
            if extra_body:
                kwargs["extra_body"] = extra_body
            if extra_request_kwargs:
                kwargs.update(extra_request_kwargs)

            response = client.chat.completions.create(**kwargs)
            content = _extract_content(response)
            if content.strip():
                return content.strip() + "\n"

            last_error = OpenAICompatibleProviderError(
                f"{provider_label} returned an empty response "
                f"({_response_diagnostic(response)}; prompt_chars={prompt_chars}; "
                f"prompt_bytes={prompt_bytes}; max_completion_tokens={max_completion_tokens})."
            )
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            last_error = exc
            if not _is_retryable_exception(exc):
                break

        if attempt_number == total_attempts:
            break

        time.sleep(RETRY_DELAYS_SECONDS[attempt_number - 1])

    if last_error is None:
        raise OpenAICompatibleProviderError(f"{provider_label} API call failed without an exception.")

    kind = _provider_error_kind(last_error)
    raise OpenAICompatibleProviderError(
        f"{provider_label} API call failed after {attempt_number} attempt(s); provider_error_kind={kind}: {last_error}"
    ) from last_error
