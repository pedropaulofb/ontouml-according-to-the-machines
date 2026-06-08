#!/usr/bin/env python3
"""Run a Phase 2 page-level check for one canonical stereotype page.

Current implementation scope:
- one page per run;
- provider adapters for mock and Groq;
- local issue-comment Markdown output only;
- no GitHub issue creation;
- no canonical page modification;
- configurable completion-token budget;
- deterministic normalization of safe Markdown/template issues;
- structural/safety validation for candidate check-signal comments.

Design note:
Reviewer outputs are candidate signals for later aggregation or resolution, not
accepted project decisions. The validator enforces structure and safety but does
not reject every imperfect or low-quality recommendation. A later resolution
step should decide which signals to accept, reject, merge, defer, or escalate.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Callable


PROMPT_PATH = Path("prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md")
PROMPT_ID = "page-reviewer-v1.0.3"
AGENT_ID = "general-page-checker"
DEFAULT_MAX_COMPLETION_TOKENS = 3000

REQUIRED_OUTPUT_FRAGMENTS = [
    "## Check signal report:",
    "### Run metadata",
    "### Summary judgment",
    "### Scope",
    "### Signals",
]

UNRESOLVED_PLACEHOLDERS = [
    "<agent>",
    "<provider>",
    "<model>",
    "<review date>",
    "<path>",
    "<sha>",
    "<number of signals",
]

FORBIDDEN_CHECKBOX_PATTERNS = [
    "- [ ]",
    "- [x]",
    "- [X]",
]

ALLOWED_CATEGORIES = {
    "methodology_compliance",
    "no_visible_support_in_page",
    "weak_visible_support",
    "overstatement_risk",
    "citation_hygiene",
    "encoding_or_formatting",
}

ALLOWED_SEVERITIES = {"low", "medium", "high"}

ALLOWED_CONFIDENCE_VALUES = {"low", "medium", "high"}

SIGNAL_HEADING_PATTERN = re.compile(
    r"^####\s+(S-\d{3})\s+—\s+(.+)$",
    re.MULTILINE,
)

SIGNAL_COUNT_PATTERN = re.compile(
    r"\|\s*Signal count\s*\|\s*`?(\d+)`?\s*\|",
    re.IGNORECASE,
)

NO_SIGNALS_SENTENCE = "None identified within the configured check-agent scope."

SOURCE_VALIDATION_CLAIM_PATTERN = re.compile(
    r"\b(validated|verified|checked|confirmed|compared|reviewed|consulted|inspected)\b"
    r"[^.\n]{0,120}"
    r"\b(intermediate files?|original sources?|source papers?|papers?|PDFs?|theses?|"
    r"external OntoUML materials?|related pages?|previous issue comments?)\b",
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
    r"apply (the )?changes|push (the )?changes|merge (the )?changes"
    r")\b",
    re.IGNORECASE,
)

ACTION_LINE_PATTERN = re.compile(
    r"^- (Recommendation|Suggested repair):\s*(.+)$",
    re.MULTILINE,
)


class PageReviewError(RuntimeError):
    """Raised when the page-check run cannot be completed safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Phase 2 page-level check for one canonical stereotype page."
    )

    parser.add_argument(
        "--page",
        required=True,
        help="Repository-relative path to the canonical stereotype Markdown page.",
    )

    parser.add_argument(
        "--provider",
        required=True,
        help="Provider adapter to use. Supported values: mock, groq.",
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Model name to report in the issue comment metadata.",
    )

    parser.add_argument(
        "--output",
        default="issue-comment.md",
        help="Path where the generated issue comment should be written.",
    )

    parser.add_argument(
        "--commit-sha",
        default=None,
        help="Optional commit SHA override. If omitted, git rev-parse HEAD is used.",
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
        raise PageReviewError(
            f"Expected repository-relative path, got absolute path: {relative_path}"
        )

    resolved = (repo_root / candidate).resolve()

    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise PageReviewError(f"Path escapes repository root: {relative_path}") from exc

    return resolved


def read_text_file(path: Path, description: str) -> str:
    """Read a UTF-8 text file or raise a user-facing page-check error."""
    if not path.exists():
        raise PageReviewError(f"{description} does not exist: {path}")

    if not path.is_file():
        raise PageReviewError(f"{description} is not a file: {path}")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PageReviewError(f"{description} is not valid UTF-8: {path}") from exc


def get_commit_sha(repo_root: Path, override: str | None) -> str:
    """Return the explicit commit SHA override or the current Git HEAD SHA."""
    if override:
        sha = override.strip()
        if not sha:
            raise PageReviewError("--commit-sha was provided but is empty.")
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
        raise PageReviewError(
            "Could not determine commit SHA with `git rev-parse HEAD`. "
            "Run from a Git checkout or provide --commit-sha."
        ) from exc

    sha = result.stdout.strip()

    if not sha:
        raise PageReviewError("`git rev-parse HEAD` returned an empty commit SHA.")

    return sha


def build_review_input(
    *,
    reviewer_prompt: str,
    agent: str,
    provider: str,
    model: str,
    review_date: str,
    page_path: str,
    commit_sha: str,
    max_completion_tokens: int,
    page_content: str,
) -> str:
    """Build the complete prompt payload for provider adapters."""
    return f"""# Reviewer prompt

{reviewer_prompt}

---

# Run input

Agent name: {agent}
Provider name: {provider}
Model name: {model}
Prompt ID: {PROMPT_ID}
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

    if normalized == "mock":
        try:
            from providers.mock import generate_review
        except ImportError as exc:
            raise PageReviewError("Could not import mock provider adapter.") from exc

        return generate_review

    if normalized == "groq":
        try:
            from providers.groq import generate_review
        except ImportError as exc:
            raise PageReviewError(
                "Could not import Groq provider adapter. "
                "Check that scripts/phase-2/providers/groq.py exists and that "
                "the groq package is installed."
            ) from exc

        return generate_review

    raise PageReviewError(
        f"Unsupported provider: {provider_name}. Supported providers: mock, groq."
    )


def _extract_signal_count(text: str) -> int | None:
    """Extract the declared signal count from the metadata table."""
    match = SIGNAL_COUNT_PATTERN.search(text)
    if not match:
        return None

    try:
        return int(match.group(1))
    except ValueError:
        return None


def _extract_field_value(signal_block: str, field_name: str) -> tuple[str | None, bool]:
    """Extract a signal field value and whether it was wrapped in backticks."""
    pattern = re.compile(
        rf"^- {re.escape(field_name)}: (`([^`\n]+)`|([^\n]+))$",
        re.MULTILINE,
    )
    match = pattern.search(signal_block)

    if not match:
        return None, False

    backticked_value = match.group(2)
    plain_value = match.group(3)

    if backticked_value is not None:
        return backticked_value.strip(), True

    if plain_value is not None:
        return plain_value.strip(), False

    raw_value = match.group(1).strip()
    return raw_value.strip("`").strip(), raw_value.startswith("`") and raw_value.endswith("`")


def _has_field(signal_block: str, field_name: str) -> bool:
    """Return whether a required signal field is present."""
    pattern = re.compile(rf"^- {re.escape(field_name)}:", re.MULTILINE)
    return bool(pattern.search(signal_block))


def _normalize_enum_field(text: str, field_name: str, allowed_values: set[str]) -> str:
    """Wrap allowed enum values in backticks for one signal field."""
    allowed_pattern = "|".join(re.escape(value) for value in sorted(allowed_values))
    return re.sub(
        rf"^- {field_name}: ({allowed_pattern})\s*$",
        rf"- {field_name}: `\1`",
        text,
        flags=re.MULTILINE,
    )


def _remove_trailing_duplicate_signals_note(text: str) -> str:
    """Remove a redundant second Signals section after concrete signals."""
    if len(list(SIGNAL_HEADING_PATTERN.finditer(text))) == 0:
        return text

    return re.sub(
        r"\n+### Signals\s*\n+(?:None identified beyond.*?configured check-agent scope\.|No additional signals.*?configured check-agent scope\.)\s*$",
        "\n",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def normalize_issue_comment(text: str) -> str:
    """Apply safe mechanical repairs before validation.

    This function must not reinterpret, add, remove, or rewrite substantive
    signals. It only repairs predictable Markdown/template issues.
    """
    normalized = text.strip() + "\n"

    normalized = _normalize_enum_field(normalized, "Category", ALLOWED_CATEGORIES)
    normalized = _normalize_enum_field(normalized, "Severity", ALLOWED_SEVERITIES)
    normalized = _normalize_enum_field(normalized, "Confidence", ALLOWED_CONFIDENCE_VALUES)

    normalized = re.sub(
        r"^- Suggested repair:\s*(None|N/A|Not applicable|Not useful)\s*$\n?",
        "",
        normalized,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    normalized = _remove_trailing_duplicate_signals_note(normalized)

    return normalized.strip() + "\n"


def _is_negated_claim(text: str, match: re.Match[str]) -> bool:
    """Return whether a source-validation match is visibly negated nearby."""
    window_start = max(0, match.start() - 120)
    window_end = min(len(text), match.end() + 40)
    context = text[window_start:window_end]
    return bool(NEGATION_NEAR_SOURCE_CLAIM_PATTERN.search(context))


def _find_unsafe_source_validation_claims(text: str) -> list[str]:
    """Find non-negated claims that the model used out-of-scope sources."""
    claims: list[str] = []

    for match in SOURCE_VALIDATION_CLAIM_PATTERN.finditer(text):
        if _is_negated_claim(text, match):
            continue

        snippet = " ".join(match.group(0).split())
        claims.append(snippet[:180])

    return claims


def _find_automatic_mutation_recommendations(text: str) -> list[str]:
    """Find recommendations to automatically mutate the repository.

    This scans only action-bearing signal lines. Scanning the full comment can
    create false positives on metadata such as "Commit SHA".
    """
    recommendations: list[str] = []

    for match in ACTION_LINE_PATTERN.finditer(text):
        line = match.group(0)
        if not AUTOMATIC_MUTATION_PATTERN.search(line):
            continue

        recommendations.append(line[:220])

    return recommendations


def validate_issue_comment(
    *,
    text: str,
    agent: str,
    provider: str,
    model: str,
    review_date: str,
    page_path: str,
    commit_sha: str,
) -> list[str]:
    """Return validation errors for a generated issue comment.

    This is not conceptual validation. It checks whether the model output is
    structurally usable and safe as raw candidate input for later resolution.
    """
    errors: list[str] = []

    if not text.strip():
        errors.append("Output is empty.")
        return errors

    for fragment in REQUIRED_OUTPUT_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Missing required output fragment: {fragment}")

    for placeholder in UNRESOLVED_PLACEHOLDERS:
        if placeholder in text:
            errors.append(f"Unresolved placeholder found: {placeholder}")

    for checkbox in FORBIDDEN_CHECKBOX_PATTERNS:
        if checkbox in text:
            errors.append(f"Forbidden task checkbox found: {checkbox}")

    expected_metadata_values = {
        "agent": agent,
        "provider": provider,
        "model": model,
        "prompt": PROMPT_ID,
        "review date": review_date,
        "reviewed page": page_path,
        "commit SHA": commit_sha,
    }

    for label, value in expected_metadata_values.items():
        if value not in text:
            errors.append(f"Missing expected metadata value for {label}: {value}")

    for claim in _find_unsafe_source_validation_claims(text):
        errors.append(
            "Output appears to claim use of out-of-scope evidence: "
            f"{claim}"
        )

    for recommendation in _find_automatic_mutation_recommendations(text):
        errors.append(
            "Output appears to recommend automatic repository mutation: "
            f"{recommendation}"
        )

    signal_matches = list(SIGNAL_HEADING_PATTERN.finditer(text))
    declared_signal_count = _extract_signal_count(text)

    if declared_signal_count is None:
        errors.append("Missing or unparsable Signal count metadata row.")
    elif declared_signal_count != len(signal_matches):
        errors.append(
            f"Signal count mismatch: metadata says {declared_signal_count}, "
            f"but {len(signal_matches)} signal heading(s) were found."
        )

    if declared_signal_count == 0 and signal_matches:
        errors.append("Signal count is 0, but signal headings are present.")

    if declared_signal_count is not None and declared_signal_count > 3:
        errors.append(f"Signal count exceeds prompt limit of 3: {declared_signal_count}")

    if declared_signal_count and declared_signal_count > 0:
        for expected_index, match in enumerate(signal_matches, start=1):
            signal_id = match.group(1)
            expected_id = f"S-{expected_index:03d}"

            if signal_id != expected_id:
                errors.append(
                    f"Signal IDs must be sequential: expected {expected_id}, found {signal_id}."
                )

            block_start = match.end()
            block_end = (
                signal_matches[expected_index].start()
                if expected_index < len(signal_matches)
                else len(text)
            )
            signal_block = text[block_start:block_end]

            required_fields = [
                "Category",
                "Severity",
                "Confidence",
                "Location",
                "Observation",
                "Rationale",
                "Recommendation",
            ]

            for field_name in required_fields:
                if not _has_field(signal_block, field_name):
                    errors.append(f"{signal_id} is missing required field: {field_name}")

            category, _category_has_backticks = _extract_field_value(
                signal_block, "Category"
            )
            severity, _severity_has_backticks = _extract_field_value(
                signal_block, "Severity"
            )
            confidence, _confidence_has_backticks = _extract_field_value(
                signal_block, "Confidence"
            )

            if category is not None and category not in ALLOWED_CATEGORIES:
                errors.append(f"{signal_id} has invalid category: {category}")

            if severity is not None and severity not in ALLOWED_SEVERITIES:
                errors.append(f"{signal_id} has invalid severity: {severity}")

            if confidence is not None and confidence not in ALLOWED_CONFIDENCE_VALUES:
                errors.append(f"{signal_id} has invalid confidence: {confidence}")

    if declared_signal_count == 0:
        if NO_SIGNALS_SENTENCE not in text:
            errors.append(
                "Signal count is 0, but the required no-signals sentence is missing."
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


def main() -> int:
    args = parse_args()

    try:
        if args.max_completion_tokens <= 0:
            raise PageReviewError("--max-completion-tokens must be greater than 0.")

        repo_root = get_repo_root()

        prompt_file = resolve_repo_relative_path(repo_root, str(PROMPT_PATH))
        page_file = resolve_repo_relative_path(repo_root, args.page)

        reviewer_prompt = read_text_file(prompt_file, "Reviewer prompt")
        page_content = read_text_file(page_file, "Canonical stereotype page")

        review_date = date.today().isoformat()
        commit_sha = get_commit_sha(repo_root, args.commit_sha)

        provider_function = load_provider(args.provider)

        review_input = build_review_input(
            reviewer_prompt=reviewer_prompt,
            agent=AGENT_ID,
            provider=args.provider,
            model=args.model,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
            max_completion_tokens=args.max_completion_tokens,
            page_content=page_content,
        )

        try:
            issue_comment = provider_function(
                review_input=review_input,
                provider=args.provider,
                model=args.model,
                review_date=review_date,
                page_path=args.page,
                commit_sha=commit_sha,
                page_content=page_content,
                max_completion_tokens=args.max_completion_tokens,
            )
        except Exception as exc:
            raise PageReviewError(f"Provider call failed: {exc}") from exc

        issue_comment = normalize_issue_comment(issue_comment)

        validation_errors = validate_issue_comment(
            text=issue_comment,
            agent=AGENT_ID,
            provider=args.provider,
            model=args.model,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
        )

        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path

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

    except PageReviewError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
