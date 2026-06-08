"""Mock provider for Phase 2 page-review runs.

The mock provider does not call an LLM. It produces a deterministic issue
comment so the runner, prompt loading, metadata handling, output writing, and
validation can be tested without consuming API quota.
"""

from __future__ import annotations


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


def _build_methodology_finding(index: int, missing_section: str) -> str:
    finding_id = f"F-{index:03d}"
    return f"""#### {finding_id} — Missing expected section

- Category: `methodology_compliance`
- Severity: `high`
- Confidence: `high`
- Location: `Page structure`
- Observation: `The expected section {missing_section} was not found in the provided Markdown.`
- Rationale: `The Phase 2 page-review scope expects canonical stereotype pages to expose this section for reviewability.`
- Recommendation: `Add or restore the missing section heading if this page is intended to follow the canonical stereotype-page structure.`
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
    """Generate a deterministic mock review comment.

    The `review_input` and `max_completion_tokens` arguments are accepted to
    match the provider interface used by real LLM adapters.
    """
    del review_input, max_completion_tokens

    missing_sections = _find_missing_sections(page_content)
    finding_count = len(missing_sections)

    provider_value = _escape_table_value(provider)
    model_value = _escape_table_value(model)
    page_path_value = _escape_table_value(page_path)
    commit_sha_value = _escape_table_value(commit_sha)

    if finding_count == 0:
        summary = (
            "The mock provider completed a deterministic structural smoke test and found no missing expected sections. "
            "This is not a substantive LLM review."
        )
        findings = "None identified within the configured page-level review scope."
    else:
        summary = (
            f"The mock provider completed a deterministic structural smoke test and found {finding_count} missing expected section(s). "
            "This is not a substantive LLM review."
        )
        findings = "\n\n".join(
            _build_methodology_finding(index, section)
            for index, section in enumerate(missing_sections, start=1)
        )

    return f"""## Model review: {provider_value} / {model_value} — {review_date}

### Run metadata

| Field | Value |
|---|---|
| Provider | {provider_value} |
| Model | {model_value} |
| Prompt | {PROMPT_ID} |
| Review date | {review_date} |
| Reviewed page | {page_path_value} |
| Commit SHA | {commit_sha_value} |
| Finding count | {finding_count} |

### Summary judgment

{summary}

### Scope

Page-level review only. This run did not check intermediate files, original sources, related pages, previous issue comments, or external OntoUML materials.

### Findings

{findings}
"""
