"""Groq provider for Phase 2 page-review runs."""

from __future__ import annotations

import os
import time
from typing import Any

from groq import Groq


class GroqProviderError(RuntimeError):
    """Raised when the Groq provider cannot complete a review."""


SYSTEM_MESSAGE = (
    "Return only the GitHub issue comment requested by the prompt. "
    "Do not include analysis, prefaces, explanations, or code fences. "
    "Focus on concrete candidate findings for later aggregation."
)

# Initial request plus one retry after each delay.
# Keep this in the provider rather than the workflow so local and CI runs behave alike.
RETRY_DELAYS_SECONDS = (5.0, 15.0, 45.0)

TRANSIENT_ERROR_MARKERS = (
    "429",
    "500",
    "502",
    "503",
    "504",
    "rate_limit_exceeded",
    "service_unavailable",
    "timeout",
    "temporarily unavailable",
)

NON_RETRYABLE_ERROR_MARKERS = (
    "request too large",
    "error code: 413",
)


def _is_retryable_exception(exc: Exception) -> bool:
    """Return whether a Groq exception looks transient enough to retry."""
    diagnostic = " ".join(
        [
            str(exc),
            str(getattr(exc, "code", "")),
            str(getattr(exc, "status", "")),
            str(getattr(exc, "reason", "")),
        ]
    ).lower()

    if any(marker in diagnostic for marker in NON_RETRYABLE_ERROR_MARKERS):
        return False

    return any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS)


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
            "Groq response did not contain choices[0].message.content "
            f"({_response_diagnostic(response)})."
        ) from exc

    return content if isinstance(content, str) else ""


def _call_groq_once(
    *,
    client: Groq,
    model: str,
    review_input: str,
    max_completion_tokens: int,
) -> Any:
    """Make one Groq chat-completion request."""
    return client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": review_input,
            },
        ],
        temperature=0,
        max_completion_tokens=max_completion_tokens,
    )


def _generate_with_retries(
    *,
    client: Groq,
    model: str,
    review_input: str,
    max_completion_tokens: int,
) -> str:
    """Call Groq with retries for transient errors and empty responses."""
    total_attempts = len(RETRY_DELAYS_SECONDS) + 1
    last_error: Exception | None = None
    prompt_chars = len(review_input)
    prompt_bytes = len(review_input.encode("utf-8"))

    for attempt_number in range(1, total_attempts + 1):
        try:
            response = _call_groq_once(
                client=client,
                model=model,
                review_input=review_input,
                max_completion_tokens=max_completion_tokens,
            )
            content = _extract_content(response)
            if content.strip():
                return content.strip() + "\n"

            diagnostic = _response_diagnostic(response)
            last_error = GroqProviderError(
                "Groq returned an empty response "
                f"({diagnostic}; prompt_chars={prompt_chars}; "
                f"prompt_bytes={prompt_bytes}; "
                f"max_completion_tokens={max_completion_tokens})."
            )
        except Exception as exc:
            last_error = exc
            if not _is_retryable_exception(exc):
                break

        if attempt_number == total_attempts:
            break

        time.sleep(RETRY_DELAYS_SECONDS[attempt_number - 1])

    if last_error is None:
        raise GroqProviderError("Groq API call failed without an exception.")

    raise GroqProviderError(
        "Groq API call failed after "
        f"{attempt_number} attempt(s): {last_error}"
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
    """Generate one Phase 2 page-review issue comment using Groq.

    The runner provides all review context through `review_input`.
    The remaining arguments keep the provider interface consistent across
    mock, Groq, and future providers.
    """
    del provider, review_date, page_path, commit_sha, page_content

    if not os.getenv("GROQ_API_KEY"):
        raise GroqProviderError("GROQ_API_KEY environment variable is not set.")

    if max_completion_tokens <= 0:
        raise GroqProviderError("max_completion_tokens must be greater than 0.")

    client = Groq()

    try:
        return _generate_with_retries(
            client=client,
            model=model,
            review_input=review_input,
            max_completion_tokens=max_completion_tokens,
        )
    except GroqProviderError:
        raise
    except Exception as exc:
        raise GroqProviderError(f"Groq API call failed: {exc}") from exc
