#!/usr/bin/env python3
"""Run one agent-aware LLM check against one canonical stereotype page.

The runner calls one provider, validates the returned Markdown against the
configured check-agent contract, and writes only deterministic, publishable
signal output. It never mutates canonical pages or GitHub state.
"""

from __future__ import annotations

import argparse
import importlib
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Callable

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import (  # noqa: E402 - direct script execution needs its directory on sys.path.
    RegistryValidationError,
    require_executable_slot,
    validate_completion_token_cap,
)
from task_identity import (  # noqa: E402 - direct script execution needs its directory on sys.path.
    FENCED_BLOCK_PATTERN,
    LANGUAGE_STYLE_EXCLUDED_SECTIONS,
    TaskIdentityError,
    build_review_input,
    normalize_markdown_section_title,
)
from task_identity import (  # noqa: E402 - Ruff separates aliased imports.
    scope_page_content_for_agent as scope_identity_page_content,
)

DEFAULT_MAX_COMPLETION_TOKENS = 3000
NO_SIGNALS_SENTENCE = "None identified within the configured check-agent scope."
SEMANTIC_PLACEHOLDER_VALUES = {"none", "n/a", "not applicable"}
MAX_LOCATION_FRAGMENT_CHARS = 160
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

SIGNAL_HEADING_PATTERN = re.compile(r"^####\s+(S-\d{3})\s+—\s+(.+)$", re.MULTILINE)
SIGNAL_COUNT_PATTERN = re.compile(
    r"^\|\s*Signal count\s*\|\s*`?(\d+)`?\s*\|\s*$",
    re.IGNORECASE | re.MULTILINE,
)
METADATA_ROW_PATTERN = re.compile(
    r"^\|\s*(?P<key>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|\s*$",
    re.MULTILINE,
)
SIGNAL_FIELD_PATTERN = re.compile(r"^- (?P<field>[A-Za-z_]+): (?P<value>.*)$", re.MULTILINE)
LOCATION_PATTERN = re.compile(r'^Section: "(?P<section>.*?)"; Fragment: "(?P<fragment>.*?)"$')
LOCATION_LINE_PATTERN = re.compile(
    r'^(?P<prefix>- Location: Section: "[^"]*"; Fragment: ")(?P<fragment>[^"]*)(?P<suffix>")\s*$',
    re.MULTILINE,
)
MARKDOWN_HEADING_PATTERN = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")

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
    "For each signal, use exactly:",
    "Only when safe under the exact-replacement rules",
    "If there are no signals, set `Signal count`",
]
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
ACTION_LINE_PATTERN = re.compile(r"^- Recommendation:\s*(.+)$", re.MULTILINE)

SUMMARY_SENTENCE_NORMALIZATIONS = {
    "Page-hygiene signals were identified; they mainly affect readability or reviewability.": (
        "Minor page-hygiene signals were identified; they mainly affect readability or reviewability."
    ),
    "Language-style signals were identified; they mainly affect readability or professional style.": (
        "Minor language-style signals were identified; they mainly affect readability or professional style."
    ),
}
HIGH_SEVERITY_SUMMARY_NORMALIZATIONS = {
    "Page-hygiene signals were identified; they mainly affect readability or reviewability.": (
        "Page-hygiene signals were identified that may affect traceability, provenance, or reviewability."
    ),
    "Language-style signals were identified; they mainly affect readability or professional style.": (
        "Language-style signals were identified that may affect standalone professional documentation quality."
    ),
}


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
        prompt_path="prompts/phase-2/page-hygiene-checker-v1.0.3.md",
        prompt_id="page-hygiene-checker-v1.0.3",
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
        prompt_path="prompts/phase-2/language-style-checker-v1.0.3.md",
        prompt_id="language-style-checker-v1.0.3",
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

SUPPORTED_PROVIDERS: dict[str, str] = {
    "gemini": "providers.gemini",
    "groq": "providers.groq",
    "openrouter": "providers.openrouter",
    "sambanova": "providers.sambanova",
}


class CheckAgentRunnerError(RuntimeError):
    """Raised when a check-agent run cannot be completed safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one agent-aware LLM check against one canonical stereotype page.")
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
        choices=sorted(SUPPORTED_PROVIDERS),
        help="LLM provider adapter to use.",
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
        help="Optional repository-relative prompt path override.",
    )
    parser.add_argument("--prompt-id", default=None, help="Optional prompt metadata override.")
    parser.add_argument("--commit-sha", default=None, help="Optional commit SHA override.")
    parser.add_argument(
        "--review-date",
        default=None,
        help="Optional review date override in YYYY-MM-DD form.",
    )
    parser.add_argument(
        "--max-completion-tokens",
        type=int,
        default=DEFAULT_MAX_COMPLETION_TOKENS,
        help=f"Maximum completion tokens requested from the provider. Default: {DEFAULT_MAX_COMPLETION_TOKENS}.",
    )
    return parser.parse_args()


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_repo_relative_path(repo_root: Path, relative_path: str) -> Path:
    candidate = Path(relative_path)
    if candidate.is_absolute():
        raise CheckAgentRunnerError(f"Expected repository-relative path, got absolute path: {relative_path}")
    resolved = (repo_root / candidate).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise CheckAgentRunnerError(f"Path escapes repository root: {relative_path}") from exc
    return resolved


def read_text_file(path: Path, description: str) -> str:
    if not path.exists():
        raise CheckAgentRunnerError(f"{description} does not exist: {path}")
    if not path.is_file():
        raise CheckAgentRunnerError(f"{description} is not a file: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise CheckAgentRunnerError(f"{description} is not valid UTF-8: {path}") from exc


def get_commit_sha(repo_root: Path, override: str | None) -> str:
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
            "Could not determine commit SHA with `git rev-parse HEAD`. Run from a Git checkout or provide --commit-sha."
        ) from exc
    sha = result.stdout.strip()
    if not sha:
        raise CheckAgentRunnerError("`git rev-parse HEAD` returned an empty commit SHA.")
    return sha


def get_review_date(override: str | None) -> str:
    if override is None:
        return date.today().isoformat()
    normalized = override.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", normalized):
        raise CheckAgentRunnerError("--review-date must use YYYY-MM-DD format.")
    return normalized


def validate_agent_slug(agent: str) -> str:
    normalized = agent.strip()
    if not AGENT_SLUG_PATTERN.fullmatch(normalized):
        raise CheckAgentRunnerError("Agent must be a lowercase slug containing only letters, numbers, and hyphens.")
    return normalized


def derive_prompt_id(prompt_path: str) -> str:
    return Path(prompt_path).name.removesuffix(".md")


def load_provider(provider_name: str) -> Callable[..., str]:
    normalized = provider_name.strip().lower()
    module_name = SUPPORTED_PROVIDERS.get(normalized)
    if module_name is None:
        supported = ", ".join(sorted(SUPPORTED_PROVIDERS))
        raise CheckAgentRunnerError(f"Unsupported provider: {provider_name}. Supported providers: {supported}.")
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise CheckAgentRunnerError(
            f"Could not import provider adapter {normalized!r}. Check scripts/phase-2/providers/{normalized}.py."
        ) from exc
    try:
        return getattr(module, "generate_review")
    except AttributeError as exc:
        raise CheckAgentRunnerError(f"Provider adapter {module_name!r} does not define generate_review.") from exc


def clean_metadata_value(value: str) -> str:
    normalized = value.strip()
    if normalized.startswith("`") and normalized.endswith("`") and len(normalized) >= 2:
        normalized = normalized[1:-1].strip()
    return normalized


def extract_metadata_table(comment_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for match in METADATA_ROW_PATTERN.finditer(comment_text):
        key = clean_metadata_value(match.group("key")).lower()
        value = clean_metadata_value(match.group("value"))
        if key in {"field", "---"}:
            continue
        metadata[key] = value
    return metadata


def extract_signal_count(text: str) -> int | None:
    match = SIGNAL_COUNT_PATTERN.search(text)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def extract_summary_judgment(text: str) -> str | None:
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
    match = re.search(r"^### Signals\s*\n(?P<body>.*)$", text, flags=re.MULTILINE | re.DOTALL)
    return match.group("body").strip() if match else ""


def extract_signal_blocks(text: str) -> list[tuple[str, str, str]]:
    matches = list(SIGNAL_HEADING_PATTERN.finditer(text))
    blocks: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        block_start = match.end()
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), match.group(2).strip(), text[block_start:block_end]))
    return blocks


def strip_inline_code(value: str) -> str:
    normalized = value.strip()
    if normalized.startswith("`") and normalized.endswith("`") and len(normalized) >= 2:
        return normalized[1:-1].strip()
    return normalized


def scope_page_content_for_agent(*, contract: AgentContract, page_content: str) -> tuple[str, str]:
    try:
        return scope_identity_page_content(agent=contract.slug, page_content=page_content)
    except TaskIdentityError as exc:
        raise CheckAgentRunnerError(f"{exc} Refusing to call provider.") from exc


def extract_signal_fields(signal_block: str) -> list[tuple[str, str]]:
    return [
        (match.group("field"), match.group("value").strip()) for match in SIGNAL_FIELD_PATTERN.finditer(signal_block)
    ]


def field_value(fields: list[tuple[str, str]], field_name: str) -> str | None:
    for key, value in fields:
        if key == field_name:
            return value
    return None


def find_unsafe_source_validation_claims(text: str) -> list[str]:
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
    recommendations: list[str] = []
    for match in ACTION_LINE_PATTERN.finditer(text):
        line = match.group(0)
        if AUTOMATIC_MUTATION_PATTERN.search(line):
            recommendations.append(line[:220])
    return recommendations


def normalize_enum_field(text: str, field_name: str, allowed_values: set[str]) -> str:
    allowed_pattern = "|".join(re.escape(value) for value in sorted(allowed_values))
    return re.sub(
        rf"^- {field_name}: ({allowed_pattern})\s*$",
        rf"- {field_name}: `\1`",
        text,
        flags=re.MULTILINE,
    )


def replace_first_non_empty_line(text: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip():
            lines[index] = replacement
            return "\n".join(lines).strip() + "\n"
    return text


def replace_summary_judgment_sentence(text: str, replacement: str) -> str:
    section_match = re.search(
        r"^### Summary judgment\s*\n(?P<body>.*?)(?=^###\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if section_match is None:
        return text
    body_lines = section_match.group("body").splitlines()
    for index, line in enumerate(body_lines):
        if line.strip():
            leading_whitespace = line[: len(line) - len(line.lstrip())]
            body_lines[index] = f"{leading_whitespace}{replacement}"
            new_body = "\n".join(body_lines)
            return text[: section_match.start("body")] + new_body + text[section_match.end("body") :]
    return text


def has_high_severity_signal(text: str) -> bool:
    for _signal_id, _title, block_body in extract_signal_blocks(text):
        severity = field_value(extract_signal_fields(block_body), "Severity")
        if severity is not None and strip_inline_code(severity) == "high":
            return True
    return False


def shorten_location_fragment(fragment: str, max_chars: int = MAX_LOCATION_FRAGMENT_CHARS) -> str:
    normalized = re.sub(r"\s+", " ", fragment).strip()
    if len(normalized) <= max_chars:
        return normalized
    window = normalized[: max_chars + 1]
    minimum_useful_cutoff = min(80, max_chars // 2)
    best_cutoff = -1
    for separators in ((". ", "; ", ": "), (", ",), (" ",)):
        for separator in separators:
            position = window.rfind(separator, 0, max_chars + 1)
            if position == -1:
                continue
            cutoff = position + 1 if separator[0] in ".;:" else position
            best_cutoff = max(best_cutoff, cutoff)
        if best_cutoff >= minimum_useful_cutoff:
            break
    shortened = normalized[:best_cutoff] if best_cutoff >= minimum_useful_cutoff else normalized[:max_chars]
    shortened = shortened.rstrip(" ,;:")
    return shortened or normalized[:max_chars].strip()


def normalize_location_fragments(text: str) -> tuple[str, int]:
    replacements = 0

    def replace_location(match: re.Match[str]) -> str:
        nonlocal replacements
        fragment = match.group("fragment")
        shortened = shorten_location_fragment(fragment)
        if shortened == fragment:
            return match.group(0)
        replacements += 1
        return f"{match.group('prefix')}{shortened}{match.group('suffix')}"

    return LOCATION_LINE_PATTERN.sub(replace_location, text), replacements


def normalize_schema_level_drift(
    *, text: str, contract: AgentContract, provider: str, model: str, review_date: str
) -> tuple[str, list[str]]:
    """Apply narrow, mechanically recoverable wrapper-format normalizations."""
    normalized = text
    changes: list[str] = []
    expected_title = f"## Check signal report: {contract.slug} / {provider} / {model} — {review_date}"
    title_without_model = f"## Check signal report: {contract.slug} / {provider} — {review_date}"
    first_non_empty_line = next((line.strip() for line in normalized.splitlines() if line.strip()), "")
    metadata = extract_metadata_table(normalized)
    if first_non_empty_line == title_without_model and metadata.get("model") == model:
        normalized = replace_first_non_empty_line(normalized, expected_title)
        changes.append("inserted missing model into report title")
    summary = extract_summary_judgment(normalized)
    replacement_summary = SUMMARY_SENTENCE_NORMALIZATIONS.get(summary or "")
    if has_high_severity_signal(normalized):
        replacement_summary = HIGH_SEVERITY_SUMMARY_NORMALIZATIONS.get(summary or "", replacement_summary)
    if replacement_summary is not None and replacement_summary in contract.summary_sentences:
        normalized = replace_summary_judgment_sentence(normalized, replacement_summary)
        changes.append("normalized known Summary judgment sentence variant")
    normalized, shortened_location_count = normalize_location_fragments(normalized)
    if shortened_location_count:
        suffix = "s" if shortened_location_count != 1 else ""
        changes.append(f"shortened {shortened_location_count} overlong Location fragment{suffix}")
    return normalized.strip() + "\n", changes


def normalize_issue_comment(text: str, contract: AgentContract) -> str:
    normalized = text.strip() + "\n"
    normalized = normalize_enum_field(normalized, "Category", contract.allowed_categories)
    normalized = normalize_enum_field(normalized, "Severity", SEVERITY_VALUES)
    normalized = normalize_enum_field(normalized, "Confidence", CONFIDENCE_VALUES)
    return normalized.strip() + "\n"


def decode_quoted_replacement_value(value: str) -> str | None:
    """Decode the limited escaping allowed in quoted replacement fields."""
    if not (value.startswith('"') and value.endswith('"') and len(value) >= 2):
        return None
    inner = value[1:-1]
    decoded: list[str] = []
    index = 0
    while index < len(inner):
        char = inner[index]
        if char == "\\" and index + 1 < len(inner) and inner[index + 1] in {'"', "\\", "|"}:
            decoded.append(inner[index + 1])
            index += 2
            continue
        decoded.append(char)
        index += 1
    return "".join(decoded)


def is_semantic_placeholder_field_value(value: str) -> bool:
    """Return whether a quoted or unquoted replacement field is a known sentinel placeholder."""
    decoded = decode_quoted_replacement_value(value)
    normalized = decoded if decoded is not None else value.strip()
    return normalized.strip().lower() in SEMANTIC_PLACEHOLDER_VALUES


def exact_occurrence_count(text: str, needle: str) -> int:
    """Count all exact occurrences, including overlapping occurrences."""
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        index = text.find(needle, start)
        if index == -1:
            return count
        count += 1
        start = index + 1


def is_well_formed_replacement_pair(current: str, proposed: str) -> bool:
    """Return whether a decoded pair is safe to sanitize rather than reject."""
    if not current.strip() or not proposed.strip():
        return False
    if (
        current.strip().lower() in SEMANTIC_PLACEHOLDER_VALUES
        or proposed.strip().lower() in SEMANTIC_PLACEHOLDER_VALUES
    ):
        return False
    if current == proposed:
        return False
    if "{{" in current or "}}" in current or "{{" in proposed or "}}" in proposed:
        return False
    return True


def declared_location(fields: list[tuple[str, str]]) -> tuple[str, str] | None:
    """Return the decoded Location section and fragment when existing syntax is valid."""
    location = field_value(fields, "Location")
    if location is None:
        return None
    location_match = LOCATION_PATTERN.fullmatch(location)
    if location_match is None:
        return None
    section = decode_quoted_replacement_value(f'"{location_match.group("section")}"')
    fragment = decode_quoted_replacement_value(f'"{location_match.group("fragment")}"')
    if section is None or fragment is None:
        return None
    return section, fragment


def declared_location_fragment(fields: list[tuple[str, str]]) -> str | None:
    """Return the decoded Location fragment when its existing syntax is valid."""
    location = declared_location(fields)
    return location[1] if location is not None else None


def nearest_section_for_offset(page_content: str, offset: int) -> str:
    """Return the normalized nearest Markdown heading at one page offset."""
    nearest_section = "document root"
    in_fenced_block = False
    cursor = 0
    for line in page_content.splitlines(keepends=True):
        line_end = cursor + len(line)
        content_line = line.rstrip("\r\n")
        if FENCED_BLOCK_PATTERN.match(content_line):
            in_fenced_block = not in_fenced_block
        elif not in_fenced_block:
            heading_match = MARKDOWN_HEADING_PATTERN.match(content_line)
            if heading_match is not None:
                nearest_section = normalize_markdown_section_title(heading_match.group("title"))
        if offset < line_end:
            return nearest_section
        cursor = line_end
    return nearest_section


def target_corresponds_to_declared_location(
    *, fields: list[tuple[str, str]], current_text: str, page_content: str
) -> bool:
    """Return whether the exact target identifies the declared local occurrence."""
    location = declared_location(fields)
    if location is None:
        return False
    section, fragment = location
    if not fragment or not (fragment in current_text or current_text in fragment):
        return False
    current_start = page_content.find(current_text)
    if current_start == -1 or page_content.find(current_text, current_start + 1) != -1:
        return False
    normalized_section = normalize_markdown_section_title(section)
    if nearest_section_for_offset(page_content, current_start) != normalized_section:
        return False
    current_end = current_start + len(current_text)
    fragment_start = 0
    while True:
        fragment_start = page_content.find(fragment, fragment_start)
        if fragment_start == -1:
            return False
        fragment_end = fragment_start + len(fragment)
        same_occurrence = (current_start <= fragment_start and fragment_end <= current_end) or (
            fragment_start <= current_start and current_end <= fragment_end
        )
        if same_occurrence and nearest_section_for_offset(page_content, fragment_start) == normalized_section:
            return True
        fragment_start += 1


def has_page_grounded_signal_location(signal_block: str, page_content: str) -> bool:
    """Return whether the declared Location fragment occurs under its declared section."""
    location = declared_location(extract_signal_fields(signal_block))
    if location is None:
        return False
    section, fragment = location
    if not fragment:
        return False
    normalized_section = normalize_markdown_section_title(section)
    start = 0
    while True:
        match = page_content.find(fragment, start)
        if match == -1:
            return False
        if nearest_section_for_offset(page_content, match) == normalized_section:
            return True
        start = match + 1


def strip_ambiguous_exact_replacement_fields(text: str, page_content: str) -> tuple[str, list[str]]:
    """Remove unsafe optional replacement fields while preserving their signals.

    The current signal schema supports non-automatable reports by omitting the
    optional pair. Therefore a signal whose Location fragment is grounded under
    its declared section is retained when its otherwise well-formed
    ``current_text`` has zero or multiple exact page matches. Malformed or
    incomplete pairs, and signals whose declared Location is not grounded in the
    reviewed page, are left untouched so strict validation can reject the
    generated report rather than guessing at model intent.
    """
    matches = list(SIGNAL_HEADING_PATTERN.finditer(text))
    replacements: list[tuple[int, int, str]] = []
    messages: list[str] = []
    pair_pattern = re.compile(
        r"^- current_text: (?P<current>.*)\n- proposed_text: (?P<proposed>.*)(?:\n|$)",
        re.MULTILINE,
    )
    for index, heading in enumerate(matches):
        block_start = heading.end()
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[block_start:block_end]
        pair = pair_pattern.search(block)
        if pair is None:
            continue
        raw_current = pair.group("current").strip()
        raw_proposed = pair.group("proposed").strip()
        if is_semantic_placeholder_field_value(raw_current) or is_semantic_placeholder_field_value(raw_proposed):
            if not has_page_grounded_signal_location(block, page_content):
                continue
            absolute_start = block_start + pair.start()
            absolute_end = block_start + pair.end()
            replacements.append((absolute_start, absolute_end, ""))
            messages.append(
                f"removed unsafe exact-replacement fields from {heading.group(1)} because the pair contained a recognized placeholder value"
            )
            continue
        current = decode_quoted_replacement_value(raw_current)
        proposed = decode_quoted_replacement_value(raw_proposed)
        if current is None or proposed is None or not is_well_formed_replacement_pair(current, proposed):
            continue
        match_count = exact_occurrence_count(page_content, current)
        target_matches_location = target_corresponds_to_declared_location(
            fields=extract_signal_fields(block),
            current_text=current,
            page_content=page_content,
        )
        if match_count == 1 and target_matches_location:
            continue
        if not has_page_grounded_signal_location(block, page_content):
            continue
        absolute_start = block_start + pair.start()
        absolute_end = block_start + pair.end()
        replacements.append((absolute_start, absolute_end, ""))
        if match_count != 1:
            reason = f"current_text matched {match_count} location(s) in the full reviewed page"
        else:
            reason = "the unique current_text did not correspond to the signal's declared Location fragment and section"
        messages.append(f"removed unsafe exact-replacement fields from {heading.group(1)} because {reason}")
    normalized = text
    for start, end, replacement in reversed(replacements):
        normalized = normalized[:start] + replacement + normalized[end:]
    return normalized.strip() + "\n", messages


def validate_optional_replacement_fields(
    *,
    signal_id: str,
    fields: list[tuple[str, str]],
    page_content: str,
    errors: list[str],
) -> None:
    current = field_value(fields, "current_text")
    proposed = field_value(fields, "proposed_text")
    if (current is None) != (proposed is None):
        errors.append(f"{signal_id} must include current_text and proposed_text together, or omit both.")
        return
    if current is None or proposed is None:
        return
    decoded_values: dict[str, str] = {}
    for label, value in {"current_text": current, "proposed_text": proposed}.items():
        decoded = decode_quoted_replacement_value(value)
        if decoded is None:
            errors.append(f"{signal_id} {label} must be wrapped in double quotation marks.")
            continue
        inner_value = decoded.strip()
        decoded_values[label] = decoded
        if not inner_value:
            errors.append(f"{signal_id} {label} must not be empty.")
        if inner_value.lower() in SEMANTIC_PLACEHOLDER_VALUES:
            errors.append(f"{signal_id} {label} must not use placeholder text: {inner_value}")
        if "\n" in decoded or "\r" in decoded:
            errors.append(f"{signal_id} {label} must be a single-line value.")
    decoded_current = decoded_values.get("current_text")
    decoded_proposed = decoded_values.get("proposed_text")
    if decoded_current is not None and decoded_proposed is not None:
        if decoded_current == decoded_proposed:
            errors.append(f"{signal_id} current_text and proposed_text must differ.")
        if "{{" in decoded_current or "}}" in decoded_current or "{{" in decoded_proposed or "}}" in decoded_proposed:
            errors.append(f"{signal_id} replacement fields must not contain template placeholders.")
    if decoded_current:
        match_count = exact_occurrence_count(page_content, decoded_current)
        if match_count != 1:
            errors.append(
                f"{signal_id} current_text must occur exactly once in the full reviewed page; found {match_count} matches."
            )
        elif not target_corresponds_to_declared_location(
            fields=fields,
            current_text=decoded_current,
            page_content=page_content,
        ):
            errors.append(
                f"{signal_id} current_text must correspond to the signal's declared Location fragment and section."
            )


def validate_signal_block(
    *,
    signal_id: str,
    title: str,
    body: str,
    contract: AgentContract,
    page_content: str,
    errors: list[str],
) -> None:
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
    if field_names not in (required_order, required_order + optional_order):
        errors.append(
            f"{signal_id} fields must appear exactly as required, with optional current_text/proposed_text together after Recommendation."
        )
    for field_name in required_order:
        if field_name not in field_names:
            errors.append(f"{signal_id} is missing required field: {field_name}")
    for field_name in [name for name in field_names if name not in set(required_order + optional_order)]:
        errors.append(f"{signal_id} has unexpected field: {field_name}")
    category = field_value(fields, "Category")
    severity = field_value(fields, "Severity")
    confidence = field_value(fields, "Confidence")
    location = field_value(fields, "Location")
    if category is not None and strip_inline_code(category) not in contract.allowed_categories:
        errors.append(f"{signal_id} has invalid category: {strip_inline_code(category)}")
    if severity is not None and strip_inline_code(severity) not in SEVERITY_VALUES:
        errors.append(f"{signal_id} has invalid severity: {strip_inline_code(severity)}")
    if confidence is not None and strip_inline_code(confidence) not in CONFIDENCE_VALUES:
        errors.append(f"{signal_id} has invalid confidence: {strip_inline_code(confidence)}")
    if location is not None:
        location_match = LOCATION_PATTERN.fullmatch(location)
        if location_match is None:
            errors.append(f'{signal_id} has invalid Location format; expected Section: "..."; Fragment: "...".')
        else:
            section = location_match.group("section")
            normalized_section = normalize_markdown_section_title(section)
            if contract.slug == "language-style-checker" and normalized_section in LANGUAGE_STYLE_EXCLUDED_SECTIONS:
                errors.append(
                    f"{signal_id} is located in an excluded non-reader-facing section for language-style-checker: {section}"
                )
            if len(location_match.group("fragment")) > MAX_LOCATION_FRAGMENT_CHARS:
                errors.append(f"{signal_id} Location fragment exceeds {MAX_LOCATION_FRAGMENT_CHARS} characters.")
    validate_optional_replacement_fields(signal_id=signal_id, fields=fields, page_content=page_content, errors=errors)


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
    page_content: str,
) -> list[str]:
    errors: list[str] = []
    if not text.strip():
        return ["Output is empty."]
    expected_report_title = f"## Check signal report: {contract.slug} / {provider} / {model} — {review_date}"
    first_non_empty_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if first_non_empty_line != expected_report_title:
        errors.append(f"Report title mismatch: expected {expected_report_title!r}, found {first_non_empty_line!r}")
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
            errors.append(f"Metadata mismatch for {key}: expected {expected_value}, found {actual_value}")
    declared_signal_count = extract_signal_count(text)
    signal_blocks = extract_signal_blocks(text)
    signals_section = extract_signals_section(text)
    if declared_signal_count is None:
        errors.append("Missing or unparsable Signal count metadata row.")
    elif declared_signal_count != len(signal_blocks):
        errors.append(
            f"Signal count mismatch: metadata says {declared_signal_count}, but {len(signal_blocks)} signal heading(s) were found."
        )
    if declared_signal_count is not None and declared_signal_count > 3:
        errors.append(f"Signal count exceeds prompt limit of 3: {declared_signal_count}")
    summary = extract_summary_judgment(text)
    if summary is None:
        errors.append("Missing non-empty Summary judgment sentence.")
    elif summary not in contract.summary_sentences:
        errors.append(f"Unexpected Summary judgment sentence: {summary}")
    if declared_signal_count == 0:
        if signal_blocks:
            errors.append("Signal count is 0, but signal headings are present.")
        if signals_section != NO_SIGNALS_SENTENCE:
            errors.append(
                "Signal count is 0, but the Signals section does not contain only the required no-signals sentence."
            )
    if declared_signal_count is not None and declared_signal_count > 0:
        if NO_SIGNALS_SENTENCE in signals_section:
            errors.append("Signal count is greater than 0, but the Signals section contains the no-signals sentence.")
        for expected_index, (signal_id, title, block_body) in enumerate(signal_blocks, start=1):
            expected_id = f"S-{expected_index:03d}"
            if signal_id != expected_id:
                errors.append(f"Signal IDs must be sequential: expected {expected_id}, found {signal_id}.")
            validate_signal_block(
                signal_id=signal_id,
                title=title,
                body=block_body,
                contract=contract,
                page_content=page_content,
                errors=errors,
            )
    for claim in find_unsafe_source_validation_claims(text):
        errors.append(f"Output appears to claim use of out-of-scope evidence: {claim}")
    for recommendation in find_automatic_mutation_recommendations(text):
        errors.append(f"Output appears to recommend repository or issue mutation: {recommendation}")
    return errors


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def make_invalid_output_path(output_path: Path) -> Path:
    if output_path.suffix:
        return output_path.with_suffix(f".invalid{output_path.suffix}")
    return output_path.with_name(f"{output_path.name}.invalid.md")


def resolve_output_path(repo_root: Path, output: str) -> Path:
    output_path = Path(output)
    return output_path if output_path.is_absolute() else repo_root / output_path


def main() -> int:
    args = parse_args()
    try:
        if args.max_completion_tokens <= 0:
            raise CheckAgentRunnerError("--max-completion-tokens must be greater than 0.")
        contract = AGENT_CONTRACTS[validate_agent_slug(args.agent)]
        provider = args.provider.strip().lower()
        model = args.model.strip()
        try:
            configured_slot = require_executable_slot(provider, model)
            validate_completion_token_cap(configured_slot, args.max_completion_tokens)
        except RegistryValidationError as exc:
            raise CheckAgentRunnerError(str(exc)) from exc
        if contract.slug not in configured_slot.agents:
            raise CheckAgentRunnerError(
                f"Check agent {contract.slug!r} is not configured for provider-model slot {configured_slot.spec}."
            )
        prompt_path = args.prompt or contract.prompt_path
        prompt_id = args.prompt_id or (
            contract.prompt_id if prompt_path == contract.prompt_path else derive_prompt_id(prompt_path)
        )
        repo_root = get_repo_root()
        prompt_file = resolve_repo_relative_path(repo_root, prompt_path)
        page_file = resolve_repo_relative_path(repo_root, args.page)
        output_path = resolve_output_path(repo_root, args.output)
        checker_prompt = read_text_file(prompt_file, "Check-agent prompt")
        page_content = read_text_file(page_file, "Canonical stereotype page")
        scoped_page_content, input_scope_note = scope_page_content_for_agent(
            contract=contract, page_content=page_content
        )
        review_date = get_review_date(args.review_date)
        commit_sha = get_commit_sha(repo_root, args.commit_sha)
        provider_function = load_provider(provider)
        review_input = build_review_input(
            checker_prompt=checker_prompt,
            agent=contract.slug,
            provider=provider,
            model=model,
            prompt_id=prompt_id,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
            max_completion_tokens=args.max_completion_tokens,
            page_content=scoped_page_content,
            input_scope_note=input_scope_note,
        )
        try:
            issue_comment = provider_function(
                review_input=review_input,
                provider=provider,
                model=model,
                review_date=review_date,
                page_path=args.page,
                commit_sha=commit_sha,
                page_content=scoped_page_content,
                max_completion_tokens=args.max_completion_tokens,
            )
        except Exception as exc:
            raise CheckAgentRunnerError(f"Provider call failed: {exc}") from exc
        issue_comment = normalize_issue_comment(issue_comment, contract)
        issue_comment, replacement_normalizations = strip_ambiguous_exact_replacement_fields(
            issue_comment, page_content
        )
        issue_comment, schema_normalizations = normalize_schema_level_drift(
            text=issue_comment,
            contract=contract,
            provider=provider,
            model=model,
            review_date=review_date,
        )
        for normalization in [*replacement_normalizations, *schema_normalizations]:
            print(
                f"Applied check-agent output normalization: {normalization}",
                file=sys.stderr,
            )
        validation_errors = validate_issue_comment(
            text=issue_comment,
            contract=contract,
            provider=provider,
            model=model,
            prompt_id=prompt_id,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
            page_content=page_content,
        )
        if validation_errors:
            invalid_output_path = make_invalid_output_path(output_path)
            write_output(invalid_output_path, issue_comment)
            print("Generated issue comment failed validation:", file=sys.stderr)
            for error in validation_errors:
                print(f"- {error}", file=sys.stderr)
            print(
                f"Saved invalid issue comment to: {invalid_output_path}",
                file=sys.stderr,
            )
            return 1
        write_output(output_path, issue_comment)
        print(f"Wrote issue comment to: {output_path}")
        return 0
    except CheckAgentRunnerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
