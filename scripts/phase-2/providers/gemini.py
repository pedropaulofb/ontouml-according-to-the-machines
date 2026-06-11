"""Google Gemini provider for Phase 2 page-review runs."""

from __future__ import annotations

import os
import time
from typing import Any

from google import genai
from google.genai import types


class GeminiProviderError(RuntimeError):
    """Raised when the Gemini provider cannot complete a review."""


SYSTEM_INSTRUCTION = (
    "Return only the GitHub issue comment requested by the prompt. "
    "Do not include analysis, prefaces, explanations, or code fences. "
    "Focus on concrete candidate findings for later aggregation."
)

# Initial request plus one retry after each delay.
# Keep this in the provider rather than the workflow so local and CI runs behave alike.
RETRY_DELAYS_SECONDS = (5.0, 15.0, 45.0)

TRANSIENT_ERROR_MARKERS = (
    "429",
    "503",
    "RESOURCE_EXHAUSTED",
    "UNAVAILABLE",
)


def _api_key() -> str:
    """Return the configured Gemini API key or raise a provider error."""
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise GeminiProviderError(
            "Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set."
        )
    return key


def _part_text(part: Any) -> str:
    """Extract text from one Gemini response part when available."""
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
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text

    candidates = getattr(response, "candidates", None) or []
    fallback_text = "".join(_candidate_text(candidate) for candidate in candidates)
    return fallback_text


def _thinking_config_for_model(model: str) -> types.ThinkingConfig | None:
    """Return a reduced-thinking configuration for strict-format review output."""
    normalized = model.strip().lower()

    if normalized.startswith("gemini-2.5-flash"):
        return types.ThinkingConfig(thinking_budget=0)

    if normalized.startswith("gemini-3."):
        return types.ThinkingConfig(thinking_level="low")

    return None


def _generation_config(*, model: str, max_completion_tokens: int) -> types.GenerateContentConfig:
    """Build the Gemini generation config used by Phase 2 check agents."""
    thinking_config = _thinking_config_for_model(model)
    kwargs: dict[str, Any] = {
        "system_instruction": SYSTEM_INSTRUCTION,
        "max_output_tokens": max_completion_tokens,
    }

    if thinking_config is not None:
        kwargs["thinking_config"] = thinking_config

    return types.GenerateContentConfig(**kwargs)


def _is_transient_error(exc: Exception) -> bool:
    """Return whether an exception looks like a retryable Gemini capacity failure."""
    diagnostic_parts = [
        str(exc),
        str(getattr(exc, "code", "")),
        str(getattr(exc, "status", "")),
        str(getattr(exc, "reason", "")),
    ]
    diagnostic = " ".join(diagnostic_parts).upper()
    return any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS)


def _generate_content_with_retries(
    *,
    client: genai.Client,
    model: str,
    review_input: str,
    config: types.GenerateContentConfig,
) -> Any:
    """Call Gemini with retries for transient provider-capacity failures."""
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
        except Exception as exc:
            last_exc = exc
            is_last_attempt = attempt_number == total_attempts

            if is_last_attempt or not _is_transient_error(exc):
                break

            delay_seconds = RETRY_DELAYS_SECONDS[attempt_number - 1]
            time.sleep(delay_seconds)

    if last_exc is None:
        raise GeminiProviderError("Gemini API call failed without an exception.")

    raise GeminiProviderError(
        "Gemini API call failed after "
        f"{attempts_made} attempt(s): {last_exc}"
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
    """Generate one Phase 2 page-review issue comment using Google Gemini.

    The runner provides all review context through `review_input`.
    The remaining arguments keep the provider interface consistent across
    Groq, Gemini, mock, and future providers.
    """
    del provider, review_date, page_path, commit_sha, page_content

    if max_completion_tokens <= 0:
        raise GeminiProviderError("max_completion_tokens must be greater than 0.")

    client = genai.Client(api_key=_api_key())
    config = _generation_config(model=model, max_completion_tokens=max_completion_tokens)

    response = _generate_content_with_retries(
        client=client,
        model=model,
        review_input=review_input,
        config=config,
    )

    content = _response_text(response)

    if not content.strip():
        raise GeminiProviderError("Gemini returned an empty response.")

    return content.strip() + "\n"
