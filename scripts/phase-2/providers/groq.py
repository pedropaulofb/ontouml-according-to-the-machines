"""Groq provider for Phase 2 page-review runs."""

from __future__ import annotations

import os

from groq import Groq


class GroqProviderError(RuntimeError):
    """Raised when the Groq provider cannot complete a review."""


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
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Return only the GitHub issue comment requested by the prompt. "
                        "Do not include analysis, prefaces, explanations, or code fences. "
                        "Focus on concrete candidate findings for later aggregation."
                    ),
                },
                {
                    "role": "user",
                    "content": review_input,
                },
            ],
            temperature=0,
            max_completion_tokens=max_completion_tokens,
        )
    except Exception as exc:
        raise GroqProviderError(f"Groq API call failed: {exc}") from exc

    content = response.choices[0].message.content

    if content is None or not content.strip():
        raise GroqProviderError("Groq returned an empty response.")

    return content.strip() + "\n"
