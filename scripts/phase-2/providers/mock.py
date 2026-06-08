"""Mock provider for Phase 2 check-signal runs.

The mock provider does not call an LLM. It produces a deterministic signal
comment so the runner, prompt loading, metadata handling, output writing, and
validation can be tested without consuming API quota.
"""

from __future__ import annotations


AGENT_ID = "general-page-checker"
PROMPT_ID = "page-reviewer-v1.0.3"

EXPECTED_SECTIONS = [
    "## Description",
    "## Stereotype Profile",
    "## Examples",
    "## References",
    "### Direct Citations",
    "### Consulted Sources",
    "## Generation and Review Log",
]


def _escape_table_value(value: str) -> str:
    return value.replace("|", r"\|")


def _find_missing_sections(page_content: str) -> list[str]:
    return [section for section in EXPECTED_SECTIONS if section not in page_content]


def _build_methodology_signal(index: int, missing_section: str) -> str:
    signal_id = f"S-{index:03d}"
    return f"""#### {signal_id} — Missing expected section

- Category: `methodology_compliance`
- Severity: `high`
- Confidence: `high`
- Location: `Page structure`
- Observation: `The expected section {missing_section} was not found in the provided Markdown.`
- Rationale: `The Phase 2 check-agent scope expects canonical stereotype pages to expose this section for reviewability.`
- Recommendation: `Review whether the missing section heading should be added.`
- Suggested repair: `Add the missing heading if the page is intended to follow the canonical stereotype-page structure.`
"""


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
    """Generate a deterministic mock check-signal comment.

    The `review_input` and `max_completion_tokens` arguments are accepted to
    match the provider interface used by real LLM adapters.
    """
    del review_input, max_completion_tokens

    missing_sections = _find_missing_sections(page_content)
    reported_sections = missing_sections[:3]
    omitted_count = max(0, len(missing_sections) - len(reported_sections))
    signal_count = len(reported_sections)

    agent_value = _escape_table_value(AGENT_ID)
    provider_value = _escape_table_value(provider)
    model_value = _escape_table_value(model)
    page_path_value = _escape_table_value(page_path)
    commit_sha_value = _escape_table_value(commit_sha)

    if signal_count == 0:
        summary = (
            "The mock provider completed a deterministic structural smoke test and found no missing expected sections. "
            "This is not a substantive LLM check."
        )
        signals = "None identified within the configured check-agent scope."
    else:
        omitted_note = (
            f" {omitted_count} additional missing expected section(s) were omitted because Phase 2 signal reports are capped at 3 signals."
            if omitted_count
            else ""
        )
        summary = (
            f"The mock provider completed a deterministic structural smoke test and reports {signal_count} missing expected section(s)."
            f"{omitted_note} This is not a substantive LLM check."
        )
        signals = "\n\n".join(
            _build_methodology_signal(index, section)
            for index, section in enumerate(reported_sections, start=1)
        )

    return f"""## Check signal report: {agent_value} / {provider_value} / {model_value} — {review_date}

### Run metadata

| Field | Value |
|---|---|
| Agent | {agent_value} |
| Provider | {provider_value} |
| Model | {model_value} |
| Prompt | {PROMPT_ID} |
| Review date | {review_date} |
| Reviewed page | {page_path_value} |
| Commit SHA | {commit_sha_value} |
| Signal count | {signal_count} |

### Summary judgment

{summary}

### Scope

Page-level check only. This run did not check intermediate files, original sources, related pages, previous issue comments, or external OntoUML materials.

### Signals

{signals}
"""
