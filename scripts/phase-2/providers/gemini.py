"""Google Gemini provider for Phase 2 page-review runs."""

from __future__ import annotations

import os
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


def _api_key() -> str:
    """Return the configured Gemini API key or raise a provider error."""
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise GeminiProviderError("Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set.")
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
    """Return a low-thinking configuration for strict-format review output."""
    normalized = model.strip().lower()

    if normalized.startswith("gemini-2.5-flash"):
        return types.ThinkingConfig(thinking_budget=0)

    if normalized.startswith("gemini-3."):
        return types.ThinkingConfig(thinking_level="low")

    return None


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

    try:
        response = client.models.generate_content(
            model=model,
            contents=review_input,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=max_completion_tokens,
                thinking_config=_thinking_config_for_model(model),
            ),
        )
    except Exception as exc:
        raise GeminiProviderError(f"Gemini API call failed: {exc}") from exc

    content = _response_text(response)

    if not content.strip():
        raise GeminiProviderError("Gemini returned an empty response.")

    return content.strip() + "\n"
