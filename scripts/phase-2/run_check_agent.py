#!/usr/bin/env python3
"""Run one agent-aware LLM check against one canonical stereotype page.

This runner is intentionally local-output only:

- it reads one canonical stereotype Markdown page;
- it reads one check-agent prompt;
- it calls one LLM provider adapter;
- it validates the returned Markdown issue comment against the check-agent contract;
- it writes a valid output file or an `.invalid.md` debugging file;
- it does not create GitHub issues;
- it does not modify canonical documentation pages;
- it does not commit changes;
- it does not open pull requests.

Posting or updating GitHub issue comments remains the responsibility of
`scripts/phase-2/issue_manager.py`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable


DEFAULT_MAX_COMPLETION_TOKENS = 3000
NO_SIGNALS_SENTENCE = "None identified within the configured check-agent scope."

AGENT_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

REQUIRED_OUTPUT_FRAGMENTS = [
    "## Check signal report:",
    "### Run metadata",
    "### Summary judgment",
    "### Scope",
    "### Signals",
]

FORBIDDEN_CHECKBOX_PATTERNS = ["- [ ]", "- [x]", "- [X]"]

SEVERITY_VALUES = {"low", "medium", "high"}
CONFIDENCE_VALUES = {"low", "medium", "high"}

SIGNAL_HEADING_PATTERN = re.compile(
    r"^####\s+(S-\d{3})\s+—\s+(.+)$",
    re.MULTILINE,
)

SIGNAL_COUNT_PATTERN = re.compile(
    r"^\|\s*Signal count\s*\|\s*`?(\d+)`?\s*\|\s*$",
    re.IGNORECASE | re.MULTILINE,
)

METADATA_ROW_PATTERN = re.compile(
    r"^\|\s*(?P<key>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|\s*$",
    re.MULTILINE,
)

SIGNAL_FIELD_PATTERN = re.compile(
    r"^- (?P<field>[A-Za-z_]+): (?P<value>.*)$",
    re.MULTILINE,
)

LOCATION_PATTERN = re.compile(
    r'^Section: "(?P<section>.*?)"; Fragment: "(?P<fragment>.*?)"$'
)

UNRESOLVED_TEMPLATE_PATTERNS = [
    "{provider}",
    "{model}",
    "{review date}",
    "{path}",
    "{sha}",
    "{number of emitted signal sections, or 0 if none}",
    "{exactly one sentence from Summary sentence choices}",
    "{short plain-text signal title}",
    "{one allowed category}",
    "{one allowed severity}",
    "{one allowed confidence}",
    "{nearest heading, or Document root if no heading applies}",
    "{exact affected fragment from the same location, maximum 160 characters}",
    "{single-line observation}",
    "{single-line rationale}",
    "{single-line recommendation}",
    "<agent>",
    "<provider>",
    "<model>",
    "<review date>",
    "<path>",
    "<sha>",
]

EXPLANATORY_PROMPT_TEXT_PATTERNS = [
    "If one or more signals are identified",
    "If and only if safe under the replacement rules",
    "Add at most `S-002` and `S-003`",
    "Add at most S-002 and S-003",
]

LANGUAGE_STYLE_EXCLUDED_LOCATION_SECTIONS = {
    "references",
    "direct citations",
    "consulted sources",
    "generation and review log",
}

SOURCE_VALIDATION_CLAIM_PATTERN = re.compile(
    r"\b(validated|verified|checked|confirmed|compared|reviewed|consulted|inspected)\b"
    r"[^.\n]{0,120}"
    r"\b(original sources?|source papers?|papers?|PDFs?|theses?|web pages?|"
    r"external sources?|external OntoUML materials?|related pages?|previous issue comments?)\b",
    re.IGNORECASE,
)

NEGATION_NEAR_SOURCE_CLAIM_PATTERN = re.compile(
    r"\b(did not|does not|not|without|no)\b[^.\n]{0,80}"
    r"\b(validated|verify|verified|checked|check|confirmed|compared|reviewed|consulted|inspected)\b",
    re.IGNORECASE,
)

AUTOMATIC_MUTATION_PATTERN = re.compile(
    r"\b(automatically\s+)?("
    r"commit|commits|committed|"
    r"open a pull request|create a pull request|open a PR|create a PR|submit a PR|"
    r"apply (the )?changes|push (the )?changes|merge (the )?changes|"
    r"close (the )?issue|label (the )?issue|change (the )?issue title|"
    r"update (the )?workflow|change (the )?workflow"
    r")\b",
    re.IGNORECASE,
)

ACTION_LINE_PATTERN = re.compile(
    r"^- Recommendation:\s*(.+)$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class AgentContract:
    """Validation contract for one LLM-based check agent."""

    slug: str
    prompt_path: str
    prompt_id: str
    allowed_categories: set[str]
    summary_sentences: set[str]


AGENT_CONTRACTS: dict[str, AgentContract] = {
    "page-hygiene-checker": AgentContract(
        slug="page-hygiene-checker",
        prompt_path="prompts/phase-2/page-hygiene-checker-v1.0.2.md",
        prompt_id="page-hygiene-checker-v1.0.2",
        allowed_categories={
            "reference_hygiene",
            "markdown_hygiene",
            "encoding_hygiene",
            "review_log_hygiene",
        },
        summary_sentences={
            "No page-hygiene signals were identified within the configured scope.",
            "Minor page-hygiene signals were identified; they mainly affect readability or reviewability.",
            "Page-hygiene signals were identified that may affect traceability, provenance, or reviewability.",
            "Page-hygiene signals were identified, and only the highest-impact three are reported.",
        },
    ),
    "language-style-checker": AgentContract(
        slug="language-style-checker",
        prompt_path="prompts/phase-2/language-style-checker-v1.0.2.md",
        prompt_id="language-style-checker-v1.0.2",
        allowed_categories={
            "grammar",
            "spelling",
            "clarity",
            "professional_style",
            "project_self_reference",
        },
        summary_sentences={
            "No language-style signals were identified within the configured scope.",
            "Minor language-style signals were identified; they mainly affect readability or professional style.",
            "Language-style signals were identified that may affect standalone professional documentation quality.",
            "Language-style signals were identified, and only the highest-impact three are reported.",
        },
    ),
}


class CheckAgentRunnerError(RuntimeError):
    """Raised when a check-agent run cannot be completed safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one agent-aware LLM check against one canonical stereotype page."
    )

    parser.add_argument(
        "--agent",
        required=True,
        choices=sorted(AGENT_CONTRACTS),
        help="Check-agent slug to run.",
    )

    parser.add_argument(
        "--page",
        required=True,
        help="Repository-relative path to the canonical stereotype Markdown page.",
    )

    parser.add_argument(
        "--provider",
        required=True,
        help="LLM provider adapter to use. Supported value: groq.",
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Provider-specific model name to use and report in metadata.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path where the generated issue comment should be written.",
    )

    parser.add_argument(
        "--prompt",
        default=None,
        help=(
            "Optional repository-relative prompt path override. "
            "Defaults to the configured prompt for the selected agent."
        ),
    )

    parser.add_argument(
        "--prompt-id",
        default=None,
        help=(
            "Optional prompt metadata override. Defaults to the selected agent's "
            "configured prompt ID."
        ),
    )

    parser.add_argument(
        "--commit-sha",
        default=None,
        help="Optional commit SHA override. If omitted, git rev-parse HEAD is used.",
    )

    parser.add_argument(
        "--review-date",
        default=None,
        help="Optional review date override in YYYY-MM-DD form. Defaults to today's date.",
    )

    parser.add_argument(
        "--max-completion-tokens",
        type=int,
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        help=(
            "Maximum completion tokens requested from the provider. "
            f"Default: {DEFAULT_MAX_COMPLETION_TOKENS}."
        ),
    )

    return parser.parse_args()


def get_repo_root() -> Path:
    """Return the repository root based on this script's location."""
    return Path(__file__).resolve().parents[2]


def resolve_repo_relative_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve and validate a repository-relative path."""
    candidate = Path(relative_path)

    if candidate.is_absolute():
        raise CheckAgentRunnerError(
            f"Expected repository-relative path, got absolute path: {relative_path}"
        )

    resolved = (repo_root / candidate).resolve()

    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise CheckAgentRunnerError(f"Path escapes repository root: {relative_path}") from exc

    return resolved


def read_text_file(path: Path, description: str) -> str:
    """Read a UTF-8 text file or raise a user-facing error."""
    if not path.exists():
        raise CheckAgentRunnerError(f"{description} does not exist: {path}")

    if not path.is_file():
        raise CheckAgentRunnerError(f"{description} is not a file: {path}")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise CheckAgentRunnerError(f"{description} is not valid UTF-8: {path}") from exc


def get_commit_sha(repo_root: Path, override: str | None) -> str:
    """Return the explicit commit SHA override or the current Git HEAD SHA."""
    if override is not None:
        sha = override.strip()
        if not sha:
            raise CheckAgentRunnerError("--commit-sha was provided but is empty.")
        return sha

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise CheckAgentRunnerError(
            "Could not determine commit SHA with `git rev-parse HEAD`. "
            "Run from a Git checkout or provide --commit-sha."
        ) from exc

    sha = result.stdout.strip()
    if not sha:
        raise CheckAgentRunnerError("`git rev-parse HEAD` returned an empty commit SHA.")

    return sha


def get_review_date(override: str | None) -> str:
    """Return a validated review date."""
    if override is None:
        return date.today().isoformat()

    normalized = override.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", normalized):
        raise CheckAgentRunnerError("--review-date must use YYYY-MM-DD format.")

    return normalized


def validate_agent_slug(agent: str) -> str:
    """Validate and return a check-agent slug."""
    normalized = agent.strip()
    if not AGENT_SLUG_PATTERN.fullmatch(normalized):
        raise CheckAgentRunnerError(
            "Agent must be a lowercase slug containing only letters, numbers, and hyphens."
        )
    return normalized


def derive_prompt_id(prompt_path: str) -> str:
    """Derive a prompt ID from a prompt file path."""
    return Path(prompt_path).name.removesuffix(".md")


def build_review_input(
    *,
    checker_prompt: str,
    agent: str,
    provider: str,
    model: str,
    prompt_id: str,
    review_date: str,
    page_path: str,
    commit_sha: str,
    max_completion_tokens: int,
    page_content: str,
) -> str:
    """Build the complete prompt payload for provider adapters."""
    return f"""# Check-agent prompt

{checker_prompt}

---

# Run input

Agent name: {agent}
Provider name: {provider}
Model name: {model}
Prompt ID: {prompt_id}
Review date: {review_date}
Reviewed page path: {page_path}
Repository commit SHA: {commit_sha}
Max completion tokens: {max_completion_tokens}

---

# Canonical stereotype page Markdown

BEGIN_CANONICAL_STEREOTYPE_PAGE_MARKDOWN
{page_content}
END_CANONICAL_STEREOTYPE_PAGE_MARKDOWN
"""


def load_provider(provider_name: str) -> Callable[..., str]:
    """Load a provider adapter by name."""
    normalized = provider_name.strip().lower()

    if normalized == "groq":
        try:
            from providers.groq import generate_review
        except ImportError as exc:
            raise CheckAgentRunnerError(
                "Could not import Groq provider adapter. "
                "Check that scripts/phase-2/providers/groq.py exists and that "
                "the groq package is installed."
            ) from exc

        return generate_review

    raise CheckAgentRunnerError(
        f"Unsupported provider: {provider_name}. Supported providers: groq."
    )


def clean_metadata_value(value: str) -> str:
    """Normalize a metadata-table cell value."""
    normalized = value.strip()

    if normalized.startswith("`") and normalized.endswith("`") and len(normalized) >= 2:
        normalized = normalized[1:-1].strip()

    return normalized


def extract_metadata_table(comment_text: str) -> dict[str, str]:
    """Extract metadata rows from all Markdown tables in the comment."""
    metadata: dict[str, str] = {}

    for match in METADATA_ROW_PATTERN.finditer(comment_text):
        key = clean_metadata_value(match.group("key")).lower()
        value = clean_metadata_value(match.group("value"))

        if key in {"field", "---"}:
            continue

        metadata[key] = value

    return metadata


def extract_signal_count(text: str) -> int | None:
    """Extract the declared signal count from the metadata table."""
    match = SIGNAL_COUNT_PATTERN.search(text)
    if not match:
        return None

    try:
        return int(match.group(1))
    except ValueError:
        return None


def extract_summary_judgment(text: str) -> str | None:
    """Extract the first non-empty paragraph under Summary judgment."""
    match = re.search(
        r"^### Summary judgment\s*\n(?P<body>.*?)(?=^###\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return None

    for line in match.group("body").splitlines():
        stripped = line.strip()
        if stripped:
            return stripped

    return None


def extract_signals_section(text: str) -> str:
    """Return the text after the Signals heading."""
    match = re.search(
        r"^### Signals\s*\n(?P<body>.*)$",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""

    return match.group("body").strip()


def extract_signal_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return signal tuples as (signal_id, title, body)."""
    matches = list(SIGNAL_HEADING_PATTERN.finditer(text))
    blocks: list[tuple[str, str, str]] = []

    for index, match in enumerate(matches):
        block_start = match.end()
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), match.group(2).strip(), text[block_start:block_end]))

    return blocks


def strip_inline_code(value: str) -> str:
    """Strip one layer of Markdown inline code from a field value."""
    normalized = value.strip()
    if normalized.startswith("`") and normalized.endswith("`") and len(normalized) >= 2:
        return normalized[1:-1].strip()
    return normalized

def normalize_location_section(section: str) -> str:
    """Normalize a Location section value for scope checks."""
    normalized = section.strip()

    while normalized.startswith("#"):
        normalized = normalized[1:].strip()

    return re.sub(r"\s+", " ", normalized).lower()

def extract_signal_fields(signal_block: str) -> list[tuple[str, str]]:
    """Extract bullet fields from one signal block in order."""
    return [(match.group("field"), match.group("value").strip()) for match in SIGNAL_FIELD_PATTERN.finditer(signal_block)]


def field_value(fields: list[tuple[str, str]], field_name: str) -> str | None:
    """Return the first field value with the requested name."""
    for key, value in fields:
        if key == field_name:
            return value
    return None


def find_unsafe_source_validation_claims(text: str) -> list[str]:
    """Find non-negated claims that the model used out-of-scope sources."""
    claims: list[str] = []

    for match in SOURCE_VALIDATION_CLAIM_PATTERN.finditer(text):
        window_start = max(0, match.start() - 120)
        window_end = min(len(text), match.end() + 40)
        context = text[window_start:window_end]

        if NEGATION_NEAR_SOURCE_CLAIM_PATTERN.search(context):
            continue

        claims.append(" ".join(match.group(0).split())[:180])

    return claims


def find_automatic_mutation_recommendations(text: str) -> list[str]:
    """Find recommendations to mutate repository or issue state."""
    recommendations: list[str] = []

    for match in ACTION_LINE_PATTERN.finditer(text):
        line = match.group(0)
        if AUTOMATIC_MUTATION_PATTERN.search(line):
            recommendations.append(line[:220])

    return recommendations


def normalize_enum_field(text: str, field_name: str, allowed_values: set[str]) -> str:
    """Wrap allowed enum values in backticks for one signal field."""
    allowed_pattern = "|".join(re.escape(value) for value in sorted(allowed_values))
    return re.sub(
        rf"^- {field_name}: ({allowed_pattern})\s*$",
        rf"- {field_name}: `\1`",
        text,
        flags=re.MULTILINE,
    )


def remove_trailing_duplicate_signals_note(text: str) -> str:
    """Remove redundant no-signal text after concrete signal sections."""
    if not SIGNAL_HEADING_PATTERN.search(text):
        return text

    return re.sub(
        r"\n+### Signals\s*\n+None identified within the configured check-agent scope\.\s*$",
        "\n",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def normalize_issue_comment(text: str, contract: AgentContract) -> str:
    """Apply safe mechanical repairs before validation.

    This function must not reinterpret, add, remove, or rewrite substantive
    signals. It only repairs predictable Markdown/template issues.
    """
    normalized = text.strip() + "\n"

    normalized = normalize_enum_field(normalized, "Category", contract.allowed_categories)
    normalized = normalize_enum_field(normalized, "Severity", SEVERITY_VALUES)
    normalized = normalize_enum_field(normalized, "Confidence", CONFIDENCE_VALUES)

    normalized = re.sub(
        r"^- (current_text|proposed_text):\s*(None|N/A|Not applicable)\s*$\n?",
        "",
        normalized,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    normalized = remove_trailing_duplicate_signals_note(normalized)

    return normalized.strip() + "\n"


def validate_optional_replacement_fields(
    *,
    signal_id: str,
    fields: list[tuple[str, str]],
    errors: list[str],
) -> None:
    """Validate current_text/proposed_text consistency."""
    current = field_value(fields, "current_text")
    proposed = field_value(fields, "proposed_text")

    if (current is None) != (proposed is None):
        errors.append(
            f"{signal_id} must include current_text and proposed_text together, or omit both."
        )
        return

    if current is None or proposed is None:
        return

    for label, value in {"current_text": current, "proposed_text": proposed}.items():
        if not (value.startswith('"') and value.endswith('"') and len(value) >= 2):
            errors.append(f"{signal_id} {label} must be wrapped in double quotation marks.")
            continue

        inner_value = value[1:-1].strip()
        if not inner_value:
            errors.append(f"{signal_id} {label} must not be empty.")
        if inner_value.lower() in {"none", "n/a", "not applicable"}:
            errors.append(f"{signal_id} {label} must not use placeholder text: {inner_value}")
        if "\n" in inner_value or "\r" in inner_value:
            errors.append(f"{signal_id} {label} must be a single-line value.")


def validate_signal_block(
    *,
    signal_id: str,
    title: str,
    body: str,
    contract: AgentContract,
    errors: list[str],
) -> None:
    """Validate one signal block."""
    if "**" in title or "`" in title or "[" in title or "]" in title:
        errors.append(f"{signal_id} title must not contain Markdown formatting.")

    fields = extract_signal_fields(body)
    field_names = [field for field, _value in fields]

    required_order = [
        "Category",
        "Severity",
        "Confidence",
        "Location",
        "Observation",
        "Rationale",
        "Recommendation",
    ]

    optional_order = ["current_text", "proposed_text"]
    allowed_order_without_optional = required_order
    allowed_order_with_optional = required_order + optional_order

    if field_names not in (allowed_order_without_optional, allowed_order_with_optional):
        errors.append(
            f"{signal_id} fields must appear exactly as required, with optional current_text/proposed_text together after Recommendation."
        )

    for field_name in required_order:
        if field_name not in field_names:
            errors.append(f"{signal_id} is missing required field: {field_name}")

    extra_fields = [
        field_name
        for field_name in field_names
        if field_name not in set(required_order + optional_order)
    ]
    for field_name in extra_fields:
        errors.append(f"{signal_id} has unexpected field: {field_name}")

    category = field_value(fields, "Category")
    severity = field_value(fields, "Severity")
    confidence = field_value(fields, "Confidence")
    location = field_value(fields, "Location")

    if category is not None:
        normalized_category = strip_inline_code(category)
        if normalized_category not in contract.allowed_categories:
            errors.append(f"{signal_id} has invalid category: {normalized_category}")

    if severity is not None:
        normalized_severity = strip_inline_code(severity)
        if normalized_severity not in SEVERITY_VALUES:
            errors.append(f"{signal_id} has invalid severity: {normalized_severity}")

    if confidence is not None:
        normalized_confidence = strip_inline_code(confidence)
        if normalized_confidence not in CONFIDENCE_VALUES:
            errors.append(f"{signal_id} has invalid confidence: {normalized_confidence}")

    if location is not None:
        location_match = LOCATION_PATTERN.fullmatch(location)
        if location_match is None:
            errors.append(
                f'{signal_id} has invalid Location format; expected Section: "..."; Fragment: "...".'
            )
        else:
            section = location_match.group("section")
            normalized_section = normalize_location_section(section)

            if (
                contract.slug == "language-style-checker"
                and normalized_section in LANGUAGE_STYLE_EXCLUDED_LOCATION_SECTIONS
            ):
                errors.append(
                    f"{signal_id} is located in an excluded non-reader-facing section "
                    f"for language-style-checker: {section}"
                )

            fragment = location_match.group("fragment")
            if len(fragment) > 160:
                errors.append(f"{signal_id} Location fragment exceeds 160 characters.")

    validate_optional_replacement_fields(signal_id=signal_id, fields=fields, errors=errors)


def validate_issue_comment(
    *,
    text: str,
    contract: AgentContract,
    provider: str,
    model: str,
    prompt_id: str,
    review_date: str,
    page_path: str,
    commit_sha: str,
) -> list[str]:
    """Return validation errors for a generated issue comment.

    This is not conceptual validation. It checks whether the model output is
    structurally usable and safe as raw candidate input for issue routing.
    """
    errors: list[str] = []

    if not text.strip():
        return ["Output is empty."]

    for fragment in REQUIRED_OUTPUT_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Missing required output fragment: {fragment}")

    for unresolved in UNRESOLVED_TEMPLATE_PATTERNS:
        if unresolved in text:
            errors.append(f"Unresolved prompt/template placeholder found: {unresolved}")

    for prompt_text in EXPLANATORY_PROMPT_TEXT_PATTERNS:
        if prompt_text in text:
            errors.append(f"Output copied explanatory prompt text: {prompt_text}")

    for checkbox in FORBIDDEN_CHECKBOX_PATTERNS:
        if checkbox in text:
            errors.append(f"Forbidden task checkbox found: {checkbox}")

    metadata = extract_metadata_table(text)
    expected_metadata_values = {
        "agent": contract.slug,
        "provider": provider,
        "model": model,
        "prompt": prompt_id,
        "review date": review_date,
        "reviewed page": page_path,
        "commit sha": commit_sha,
    }

    for key, expected_value in expected_metadata_values.items():
        actual_value = metadata.get(key)
        if actual_value is None:
            errors.append(f"Missing metadata row: {key}")
        elif actual_value != expected_value:
            errors.append(
                f"Metadata mismatch for {key}: expected {expected_value}, found {actual_value}"
            )

    declared_signal_count = extract_signal_count(text)
    signal_blocks = extract_signal_blocks(text)

    if declared_signal_count is None:
        errors.append("Missing or unparsable Signal count metadata row.")
    elif declared_signal_count != len(signal_blocks):
        errors.append(
            f"Signal count mismatch: metadata says {declared_signal_count}, "
            f"but {len(signal_blocks)} signal heading(s) were found."
        )

    if declared_signal_count is not None and declared_signal_count > 3:
        errors.append(f"Signal count exceeds prompt limit of 3: {declared_signal_count}")

    summary = extract_summary_judgment(text)
    if summary is None:
        errors.append("Missing non-empty Summary judgment sentence.")
    elif summary not in contract.summary_sentences:
        errors.append(f"Unexpected Summary judgment sentence: {summary}")

    expected_report_title = (
        f"## Check signal report: {contract.slug} / {provider} / {model} — {review_date}"
    )
    first_non_empty_line = next(
        (line.strip() for line in text.splitlines() if line.strip()),
        "",
    )
    if first_non_empty_line != expected_report_title:
        errors.append(
            "Report title mismatch: expected "
            f"{expected_report_title!r}, found {first_non_empty_line!r}"
        )

    signals_section = extract_signals_section(text)

    if declared_signal_count == 0:
        if signal_blocks:
            errors.append("Signal count is 0, but signal headings are present.")
        if signals_section != NO_SIGNALS_SENTENCE:
            errors.append(
                "Signal count is 0, but the Signals section does not contain only the required no-signals sentence."
            )

    if declared_signal_count is not None and declared_signal_count > 0:
        if NO_SIGNALS_SENTENCE in signals_section:
            errors.append(
                "Signal count is greater than 0, but the Signals section contains the no-signals sentence."
            )

        for expected_index, (signal_id, title, block_body) in enumerate(signal_blocks, start=1):
            expected_id = f"S-{expected_index:03d}"
            if signal_id != expected_id:
                errors.append(
                    f"Signal IDs must be sequential: expected {expected_id}, found {signal_id}."
                )

            validate_signal_block(
                signal_id=signal_id,
                title=title,
                body=block_body,
                contract=contract,
                errors=errors,
            )

    for claim in find_unsafe_source_validation_claims(text):
        errors.append(
            "Output appears to claim use of out-of-scope evidence: "
            f"{claim}"
        )

    for recommendation in find_automatic_mutation_recommendations(text):
        errors.append(
            "Output appears to recommend repository or issue mutation: "
            f"{recommendation}"
        )

    return errors


def write_output(path: Path, content: str) -> None:
    """Write UTF-8 Markdown output with LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def make_invalid_output_path(output_path: Path) -> Path:
    """Return the path used for invalid generated issue comments."""
    if output_path.suffix:
        return output_path.with_suffix(f".invalid{output_path.suffix}")

    return output_path.with_name(f"{output_path.name}.invalid.md")


def resolve_output_path(repo_root: Path, output: str) -> Path:
    """Resolve output path; relative paths are repository-relative."""
    output_path = Path(output)
    if output_path.is_absolute():
        return output_path
    return repo_root / output_path


def main() -> int:
    args = parse_args()

    try:
        if args.max_completion_tokens <= 0:
            raise CheckAgentRunnerError("--max-completion-tokens must be greater than 0.")

        contract = AGENT_CONTRACTS[validate_agent_slug(args.agent)]
        provider = args.provider.strip().lower()
        prompt_path = args.prompt or contract.prompt_path
        prompt_id = args.prompt_id or (contract.prompt_id if prompt_path == contract.prompt_path else derive_prompt_id(prompt_path))

        repo_root = get_repo_root()
        prompt_file = resolve_repo_relative_path(repo_root, prompt_path)
        page_file = resolve_repo_relative_path(repo_root, args.page)
        output_path = resolve_output_path(repo_root, args.output)

        checker_prompt = read_text_file(prompt_file, "Check-agent prompt")
        page_content = read_text_file(page_file, "Canonical stereotype page")

        review_date = get_review_date(args.review_date)
        commit_sha = get_commit_sha(repo_root, args.commit_sha)

        provider_function = load_provider(provider)
        review_input = build_review_input(
            checker_prompt=checker_prompt,
            agent=contract.slug,
            provider=provider,
            model=args.model,
            prompt_id=prompt_id,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
            max_completion_tokens=args.max_completion_tokens,
            page_content=page_content,
        )

        try:
            issue_comment = provider_function(
                review_input=review_input,
                provider=provider,
                model=args.model,
                review_date=review_date,
                page_path=args.page,
                commit_sha=commit_sha,
                page_content=page_content,
                max_completion_tokens=args.max_completion_tokens,
            )
        except Exception as exc:
            raise CheckAgentRunnerError(f"Provider call failed: {exc}") from exc

        issue_comment = normalize_issue_comment(issue_comment, contract)
        validation_errors = validate_issue_comment(
            text=issue_comment,
            contract=contract,
            provider=provider,
            model=args.model,
            prompt_id=prompt_id,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
        )

        if validation_errors:
            invalid_output_path = make_invalid_output_path(output_path)
            write_output(invalid_output_path, issue_comment)

            print("Generated issue comment failed validation:", file=sys.stderr)
            for error in validation_errors:
                print(f"- {error}", file=sys.stderr)
            print(f"Saved invalid issue comment to: {invalid_output_path}", file=sys.stderr)
            return 1

        write_output(output_path, issue_comment)
        print(f"Wrote issue comment to: {output_path}")
        return 0

    except CheckAgentRunnerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
