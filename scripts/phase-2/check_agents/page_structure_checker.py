#!/usr/bin/env python3
"""Deterministic Phase 2 page-structure checker.

This check agent inspects one canonical stereotype Markdown page and produces a
Phase 2 check-signal report. It does not call an LLM, edit documentation pages,
commit changes, open pull requests, or post to GitHub.

It checks:
- required stereotype-page headings;
- heading order;
- duplicate required headings;
- malformed required heading levels;
- unexpected level-2 sections;
- empty required sections.

The output is compatible with the Phase 2 signal-comment structure consumed by
scripts/phase-2/issue_manager.py after the signal-terminology migration.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


AGENT_ID = "page-structure-checker"
PROVIDER_ID = "python"
MODEL_ID = "deterministic"
PROMPT_ID = "n/a"
DEFAULT_MAX_SIGNALS = 3

EXPECTED_HEADINGS = [
    (2, "Description"),
    (2, "Stereotype Profile"),
    (2, "Examples"),
    (2, "References"),
    (3, "Direct Citations"),
    (3, "Consulted Sources"),
    (2, "Generation and Review Log"),
]

EXPECTED_HEADING_LABELS = [
    f"{'#' * level} {title}" for level, title in EXPECTED_HEADINGS
]

EXPECTED_H2_TITLES = {
    title for level, title in EXPECTED_HEADINGS if level == 2
}

REQUIRED_SECTION_TITLES = {title for _level, title in EXPECTED_HEADINGS}

PLACEHOLDER_TEXTS = {
    "tbd in a later phase.",
    "tbd.",
    "none identified within the configured check-agent scope.",
}

HEADING_PATTERN = re.compile(
    r"^(?P<marks>#{1,6})[ \t]+(?P<title>.*?)(?:[ \t]+#+[ \t]*)?$",
    re.MULTILINE,
)


class PageStructureCheckerError(RuntimeError):
    """Raised when the page-structure checker cannot proceed safely."""


@dataclass(frozen=True)
class Heading:
    """A parsed Markdown heading."""

    level: int
    title: str
    line: int
    raw: str

    @property
    def label(self) -> str:
        return f"{'#' * self.level} {self.title}"


@dataclass(frozen=True)
class Signal:
    """One deterministic Phase 2 page-structure signal."""

    signal_id: str
    title: str
    category: str
    severity: str
    confidence: str
    location: str
    observation: str
    rationale: str
    recommendation: str
    suggested_repair: str | None = None
    details: dict[str, object] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the deterministic Phase 2 page-structure checker for one "
            "canonical stereotype Markdown page."
        )
    )

    parser.add_argument(
        "--page",
        required=True,
        help="Repository-relative path to the canonical stereotype Markdown page.",
    )

    parser.add_argument(
        "--output",
        default="issue-comment.md",
        help="Path where the generated check-signal report should be written.",
    )

    parser.add_argument(
        "--commit-sha",
        default=None,
        help="Optional commit SHA override. If omitted, git rev-parse HEAD is used.",
    )

    parser.add_argument(
        "--max-signals",
        type=int,
        default=DEFAULT_MAX_SIGNALS,
        help=f"Maximum number of signals to report. Default: {DEFAULT_MAX_SIGNALS}.",
    )

    return parser.parse_args()


def find_repo_root() -> Path:
    """Find the repository root from the current working directory or script path."""
    candidates: list[Path] = []

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_path = Path(__file__).resolve()
    candidates.extend([script_path.parent, *script_path.parents])

    seen: set[Path] = set()

    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)

        if (candidate / ".git").exists():
            return candidate

        if (candidate / "docs" / "stereotypes").exists() and (candidate / "scripts").exists():
            return candidate

    raise PageStructureCheckerError(
        "Could not determine repository root. Run from the repository checkout "
        "or place this script under scripts/phase-2/check_agents/."
    )


def resolve_repo_relative_path(repo_root: Path, relative_path: str) -> Path:
    """Resolve and validate a repository-relative path."""
    candidate = Path(relative_path)

    if candidate.is_absolute():
        raise PageStructureCheckerError(
            f"Expected repository-relative path, got absolute path: {relative_path}"
        )

    resolved = (repo_root / candidate).resolve()

    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise PageStructureCheckerError(f"Path escapes repository root: {relative_path}") from exc

    return resolved


def read_text_file(path: Path, description: str) -> str:
    """Read a UTF-8 text file."""
    if not path.exists():
        raise PageStructureCheckerError(f"{description} does not exist: {path}")

    if not path.is_file():
        raise PageStructureCheckerError(f"{description} is not a file: {path}")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PageStructureCheckerError(f"{description} is not valid UTF-8: {path}") from exc


def get_commit_sha(repo_root: Path, override: str | None) -> str:
    """Return the explicit commit SHA override or the current Git HEAD SHA."""
    if override:
        sha = override.strip()
        if not sha:
            raise PageStructureCheckerError("--commit-sha was provided but is empty.")
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
        raise PageStructureCheckerError(
            "Could not determine commit SHA with `git rev-parse HEAD`. "
            "Run from a Git checkout or provide --commit-sha."
        ) from exc

    sha = result.stdout.strip()

    if not sha:
        raise PageStructureCheckerError("`git rev-parse HEAD` returned an empty commit SHA.")

    return sha


def parse_headings(markdown: str) -> list[Heading]:
    """Parse Markdown ATX headings from the page."""
    headings: list[Heading] = []

    for match in HEADING_PATTERN.finditer(markdown):
        line = markdown.count("\n", 0, match.start()) + 1
        marks = match.group("marks")
        raw_title = match.group("title").strip()
        title = re.sub(r"\s+", " ", raw_title).strip()

        if not title:
            continue

        headings.append(
            Heading(
                level=len(marks),
                title=title,
                line=line,
                raw=match.group(0).strip(),
            )
        )

    return headings


def heading_index_by_title(headings: Iterable[Heading]) -> dict[str, list[Heading]]:
    """Group headings by exact title."""
    grouped: dict[str, list[Heading]] = {}

    for heading in headings:
        grouped.setdefault(heading.title, []).append(heading)

    return grouped


def expected_heading_exists(headings_by_title: dict[str, list[Heading]], level: int, title: str) -> bool:
    """Return whether the exact expected heading exists."""
    return any(heading.level == level for heading in headings_by_title.get(title, []))


def section_body(markdown_lines: list[str], heading: Heading, headings: list[Heading]) -> str:
    """Return the Markdown body belonging to a heading.

    The body extends until the next heading with level less than or equal to the
    current heading level.
    """
    start_index = heading.line
    end_index = len(markdown_lines)

    for next_heading in headings:
        if next_heading.line <= heading.line:
            continue

        if next_heading.level <= heading.level:
            end_index = next_heading.line - 1
            break

    return "\n".join(markdown_lines[start_index:end_index]).strip()


def strip_non_content_lines(section_text: str) -> str:
    """Remove lines that should not count as substantive section content."""
    content_lines: list[str] = []

    for raw_line in section_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("<!--") and line.endswith("-->"):
            continue

        content_lines.append(line)

    return "\n".join(content_lines).strip()


def is_effectively_empty(section_text: str) -> bool:
    """Return whether a section body is effectively empty."""
    normalized = strip_non_content_lines(section_text)

    if not normalized:
        return True

    lower = normalized.lower().strip()

    if lower in PLACEHOLDER_TEXTS:
        return False

    return False


def make_signal(
    *,
    title: str,
    severity: str,
    location: str,
    observation: str,
    rationale: str,
    recommendation: str,
    suggested_repair: str | None = None,
    details: dict[str, object] | None = None,
) -> Signal:
    """Create a signal without assigning its final sequential ID yet."""
    return Signal(
        signal_id="S-000",
        title=title,
        category="methodology_compliance",
        severity=severity,
        confidence="high",
        location=location,
        observation=observation,
        rationale=rationale,
        recommendation=recommendation,
        suggested_repair=suggested_repair,
        details=details,
    )


def detect_missing_required_headings(headings_by_title: dict[str, list[Heading]]) -> Signal | None:
    """Detect expected headings that are completely missing."""
    missing = [
        label
        for (level, title), label in zip(EXPECTED_HEADINGS, EXPECTED_HEADING_LABELS)
        if not expected_heading_exists(headings_by_title, level, title)
    ]

    if not missing:
        return None

    return make_signal(
        title="Missing expected required heading",
        severity="high",
        location="Page structure",
        observation=(
            "The page is missing the following expected heading(s): "
            + ", ".join(f"`{item}`" for item in missing)
            + "."
        ),
        rationale=(
            "Canonical stereotype pages must expose the expected sections so that "
            "later check and resolution agents can evaluate the page consistently."
        ),
        recommendation="Review whether the missing heading(s) should be added.",
        suggested_repair=(
            "Add the missing heading(s) in the canonical order if the page is "
            "intended to follow the stereotype-page structure."
        ),
        details={"missing_headings": missing},
    )


def detect_malformed_required_heading_levels(headings_by_title: dict[str, list[Heading]]) -> Signal | None:
    """Detect required headings that appear with the wrong heading level."""
    malformed: list[str] = []

    for expected_level, title in EXPECTED_HEADINGS:
        headings_with_title = headings_by_title.get(title, [])

        if not headings_with_title:
            continue

        if any(heading.level == expected_level for heading in headings_with_title):
            continue

        observed = ", ".join(f"`{heading.label}` at line {heading.line}" for heading in headings_with_title)
        malformed.append(f"`{'#' * expected_level} {title}` expected; observed {observed}")

    if not malformed:
        return None

    return make_signal(
        title="Required heading uses unexpected level",
        severity="high",
        location="Page structure",
        observation="; ".join(malformed) + ".",
        rationale=(
            "The page structure depends on stable heading levels, not only heading "
            "titles. Incorrect heading levels can break automated section detection."
        ),
        recommendation="Change the malformed heading(s) to the expected heading level.",
        suggested_repair="Normalize the affected heading marker(s) to match the expected canonical structure.",
        details={"malformed_heading_levels": malformed},
    )


def detect_duplicate_required_headings(headings_by_title: dict[str, list[Heading]]) -> Signal | None:
    """Detect duplicate exact required headings."""
    duplicates: list[str] = []

    for expected_level, title in EXPECTED_HEADINGS:
        exact_matches = [
            heading
            for heading in headings_by_title.get(title, [])
            if heading.level == expected_level
        ]

        if len(exact_matches) > 1:
            locations = ", ".join(str(heading.line) for heading in exact_matches)
            duplicates.append(f"`{'#' * expected_level} {title}` at lines {locations}")

    if not duplicates:
        return None

    return make_signal(
        title="Duplicate required heading",
        severity="medium",
        location="Page structure",
        observation=(
            "The page contains duplicate required heading(s): "
            + "; ".join(duplicates)
            + "."
        ),
        rationale=(
            "Duplicate required headings make section boundaries ambiguous for "
            "both readers and automated check agents."
        ),
        recommendation="Review the duplicate heading(s) and merge, rename, or remove the unintended duplicate.",
        suggested_repair=None,
        details={"duplicate_headings": duplicates},
    )


def detect_heading_order_issue(headings_by_title: dict[str, list[Heading]]) -> Signal | None:
    """Detect expected headings that appear out of canonical order."""
    observed: list[tuple[str, int]] = []

    for expected_level, title in EXPECTED_HEADINGS:
        exact_matches = [
            heading
            for heading in headings_by_title.get(title, [])
            if heading.level == expected_level
        ]

        if exact_matches:
            first = min(exact_matches, key=lambda heading: heading.line)
            observed.append((first.label, first.line))

    if len(observed) < 2:
        return None

    out_of_order_pairs: list[str] = []

    for previous, current in zip(observed, observed[1:]):
        previous_label, previous_line = previous
        current_label, current_line = current

        if current_line < previous_line:
            out_of_order_pairs.append(
                f"`{current_label}` at line {current_line} appears before `{previous_label}` at line {previous_line}"
            )

    # The adjacent-pair test above catches local inversions, but not every
    # permutation. Also compare the observed sequence to canonical order.
    observed_labels = [label for label, _line in sorted(observed, key=lambda item: item[1])]
    expected_subset_order = [label for label in EXPECTED_HEADING_LABELS if label in observed_labels]

    if observed_labels == expected_subset_order:
        return None

    if not out_of_order_pairs:
        out_of_order_pairs.append(
            "Observed order is "
            + " -> ".join(f"`{label}`" for label in observed_labels)
            + "; expected order is "
            + " -> ".join(f"`{label}`" for label in expected_subset_order)
        )

    return make_signal(
        title="Required headings appear out of order",
        severity="medium",
        location="Page structure",
        observation="; ".join(out_of_order_pairs) + ".",
        rationale=(
            "Canonical heading order makes stereotype pages predictable and makes "
            "later automated checks easier to scope."
        ),
        recommendation="Review whether the required headings should be reordered to match the canonical sequence.",
        suggested_repair=(
            "Reorder the affected sections only after confirming that their content "
            "moves with the correct heading."
        ),
        details={"observed_order": observed_labels, "expected_order": expected_subset_order},
    )


def detect_unexpected_level_two_sections(headings: list[Heading]) -> Signal | None:
    """Detect unexpected level-2 headings in the canonical page skeleton."""
    unexpected = [
        f"`## {heading.title}` at line {heading.line}"
        for heading in headings
        if heading.level == 2 and heading.title not in EXPECTED_H2_TITLES
    ]

    if not unexpected:
        return None

    return make_signal(
        title="Unexpected level-2 section",
        severity="low",
        location="Page structure",
        observation=(
            "The page contains unexpected level-2 section(s): "
            + "; ".join(unexpected)
            + "."
        ),
        rationale=(
            "Unexpected top-level sections may be intentional, but they can also "
            "indicate drift from the canonical stereotype-page structure."
        ),
        recommendation=(
            "Review whether the unexpected section(s) should remain, be renamed, "
            "or be nested under an existing canonical section."
        ),
        suggested_repair=None,
        details={"unexpected_h2_sections": unexpected},
    )


def detect_empty_required_sections(markdown: str, headings: list[Heading]) -> Signal | None:
    """Detect required sections with no visible body content."""
    markdown_lines = markdown.splitlines()
    empty_sections: list[str] = []

    for expected_level, title in EXPECTED_HEADINGS:
        matching_headings = [
            heading
            for heading in headings
            if heading.level == expected_level and heading.title == title
        ]

        if not matching_headings:
            continue

        heading = min(matching_headings, key=lambda item: item.line)
        body = section_body(markdown_lines, heading, headings)

        if is_effectively_empty(body):
            empty_sections.append(f"`{heading.label}` at line {heading.line}")

    if not empty_sections:
        return None

    return make_signal(
        title="Required section is empty",
        severity="medium",
        location="Page structure",
        observation=(
            "The following required section(s) appear to have no visible body content: "
            + "; ".join(empty_sections)
            + "."
        ),
        rationale=(
            "Empty required sections reduce page reviewability and may indicate that "
            "the page skeleton was generated or edited incompletely."
        ),
        recommendation=(
            "Review whether each empty section should receive content or an explicit "
            "placeholder such as `TBD in a later phase.`."
        ),
        suggested_repair=None,
        details={"empty_required_sections": empty_sections},
    )


def collect_signals(markdown: str) -> list[Signal]:
    """Collect deterministic page-structure signals in priority order."""
    headings = parse_headings(markdown)
    headings_by_title = heading_index_by_title(headings)

    detectors = [
        lambda: detect_missing_required_headings(headings_by_title),
        lambda: detect_malformed_required_heading_levels(headings_by_title),
        lambda: detect_duplicate_required_headings(headings_by_title),
        lambda: detect_heading_order_issue(headings_by_title),
        lambda: detect_empty_required_sections(markdown, headings),
        lambda: detect_unexpected_level_two_sections(headings),
    ]

    signals: list[Signal] = []

    for detector in detectors:
        signal = detector()
        if signal is not None:
            signals.append(signal)

    return [
        Signal(
            signal_id=f"S-{index:03d}",
            title=signal.title,
            category=signal.category,
            severity=signal.severity,
            confidence=signal.confidence,
            location=signal.location,
            observation=signal.observation,
            rationale=signal.rationale,
            recommendation=signal.recommendation,
            suggested_repair=signal.suggested_repair,
            details=signal.details,
        )
        for index, signal in enumerate(signals, start=1)
    ]


def escape_table_value(value: str) -> str:
    """Escape Markdown table cell separators."""
    return value.replace("|", r"\|")


def yaml_quote(value: str) -> str:
    """Return a conservative double-quoted YAML scalar."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", "\\n")
    return f'"{escaped}"'


def render_yaml_value(value: object, indent: int = 0) -> list[str]:
    """Render simple Python values as a small YAML subset."""
    prefix = " " * indent

    if isinstance(value, str):
        return [prefix + yaml_quote(value)]

    if isinstance(value, bool):
        return [prefix + ("true" if value else "false")]

    if isinstance(value, int | float):
        return [prefix + str(value)]

    if isinstance(value, list):
        if not value:
            return [prefix + "[]"]

        lines: list[str] = []
        for item in value:
            if isinstance(item, str):
                lines.append(prefix + "- " + yaml_quote(item))
            else:
                lines.append(prefix + "- " + yaml_quote(str(item)))
        return lines

    if isinstance(value, dict):
        if not value:
            return [prefix + "{}"]

        lines = []
        for key, item in value.items():
            rendered = render_yaml_value(item, indent + 2)
            if len(rendered) == 1 and not rendered[0].lstrip().startswith("-"):
                lines.append(prefix + f"{key}: " + rendered[0].strip())
            else:
                lines.append(prefix + f"{key}:")
                lines.extend(rendered)
        return lines

    return [prefix + yaml_quote(str(value))]


def render_structured_block(signal: Signal, page_path: str) -> str:
    """Render a machine-readable YAML block for a signal."""
    payload: dict[str, object] = {
        "signal_id": signal.signal_id,
        "agent": AGENT_ID,
        "page": page_path,
        "category": signal.category,
        "severity": signal.severity,
        "confidence": signal.confidence,
        "location": signal.location,
        "observation": signal.observation,
        "rationale": signal.rationale,
        "recommendation": signal.recommendation,
        "application_mode": "manual_review",
        "risk": signal.severity,
    }

    if signal.suggested_repair:
        payload["suggested_repair"] = signal.suggested_repair

    if signal.details:
        payload["details"] = signal.details

    lines = ["```yaml"]
    for key, value in payload.items():
        rendered = render_yaml_value(value, 0)
        if len(rendered) == 1 and not rendered[0].startswith("-"):
            lines.append(f"{key}: {rendered[0]}")
        else:
            lines.append(f"{key}:")
            lines.extend("  " + line for line in rendered)
    lines.append("```")

    return "\n".join(lines)


def render_signal(signal: Signal, page_path: str) -> str:
    """Render one signal as Markdown."""
    parts = [
        f"#### {signal.signal_id} — {signal.title}",
        "",
        f"- Category: `{signal.category}`",
        f"- Severity: `{signal.severity}`",
        f"- Confidence: `{signal.confidence}`",
        f"- Location: `{signal.location}`",
        f"- Observation: {signal.observation}",
        f"- Rationale: {signal.rationale}",
        f"- Recommendation: {signal.recommendation}",
    ]

    if signal.suggested_repair:
        parts.append(f"- Suggested repair: {signal.suggested_repair}")

    parts.extend(["", render_structured_block(signal, page_path)])

    return "\n".join(parts)


def render_summary(signals: list[Signal], total_signal_count: int, omitted_count: int) -> str:
    """Render the summary paragraph."""
    if not signals:
        return (
            "The deterministic page-structure checker found no structural signals "
            "within the configured scope."
        )

    omitted_sentence = (
        f" {omitted_count} additional structural signal(s) were omitted because this run is capped."
        if omitted_count
        else ""
    )

    return (
        f"The deterministic page-structure checker reported {len(signals)} structural "
        f"signal(s) out of {total_signal_count} detected structural issue(s)."
        f"{omitted_sentence}"
    )


def render_report(
    *,
    signals: list[Signal],
    total_signal_count: int,
    omitted_count: int,
    review_date: str,
    page_path: str,
    commit_sha: str,
) -> str:
    """Render the full Phase 2 check-signal report."""
    signal_count = len(signals)

    metadata_values = {
        "Agent": AGENT_ID,
        "Provider": PROVIDER_ID,
        "Model": MODEL_ID,
        "Prompt": PROMPT_ID,
        "Review date": review_date,
        "Reviewed page": page_path,
        "Commit SHA": commit_sha,
        "Signal count": str(signal_count),
    }

    metadata_rows = "\n".join(
        f"| {field} | {escape_table_value(value)} |"
        for field, value in metadata_values.items()
    )

    if signals:
        signals_body = "\n\n".join(render_signal(signal, page_path) for signal in signals)
    else:
        signals_body = "None identified within the configured check-agent scope."

    return f"""## Check signal report: {AGENT_ID} / {PROVIDER_ID} / {MODEL_ID} — {review_date}

### Run metadata

| Field | Value |
|---|---|
{metadata_rows}

### Summary judgment

{render_summary(signals, total_signal_count, omitted_count)}

### Scope

Deterministic page-structure check only. This run did not check source faithfulness, original sources, related pages, previous issue comments, external OntoUML materials, grammar, style, citation adequacy, or conceptual correctness. It did not modify the page.

### Signals

{signals_body}
"""


def write_output(path: Path, content: str) -> None:
    """Write UTF-8 Markdown output with LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    args = parse_args()

    try:
        if args.max_signals < 0:
            raise PageStructureCheckerError("--max-signals must not be negative.")

        repo_root = find_repo_root()
        page_path = resolve_repo_relative_path(repo_root, args.page)
        page_markdown = read_text_file(page_path, "Canonical stereotype page")
        commit_sha = get_commit_sha(repo_root, args.commit_sha)
        review_date = date.today().isoformat()

        all_signals = collect_signals(page_markdown)
        reported_signals = all_signals[: args.max_signals]
        omitted_count = max(0, len(all_signals) - len(reported_signals))

        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path

        report = render_report(
            signals=reported_signals,
            total_signal_count=len(all_signals),
            omitted_count=omitted_count,
            review_date=review_date,
            page_path=args.page,
            commit_sha=commit_sha,
        )

        write_output(output_path, report)

        print(f"Wrote page-structure check report to: {output_path}")
        print(f"Detected structural signals: {len(all_signals)}")
        print(f"Reported structural signals: {len(reported_signals)}")

        if omitted_count:
            print(f"Omitted structural signals due to cap: {omitted_count}")

        return 0

    except PageStructureCheckerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
