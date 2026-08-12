#!/usr/bin/env python3
"""Resolve Phase 2 check-signal issues automatically.

The script reads one selected GitHub issue, or selects the oldest eligible open
page-hygiene/language-style signal issue when no issue is supplied. It then asks
a resolver LLM for a strict JSON resolution plan, deterministically revalidates
accepted edit groups against the current page, safely demotes non-applicable
atomic groups, optionally creates a pull request for remaining accepted edits,
comments on the issue, and closes the issue.

The LLM is used only to classify signals and propose exact replacements. All
file edits, exact-target checks, automatic demotions, and GitHub mutations are
performed by this deterministic wrapper.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import (  # noqa: E402
    DEFAULT_REGISTRY_PATH,
    RegistryValidationError,
    load_registry,
    require_executable_slot,
)
from provider_runtime import record_provider_event, record_provider_failure  # noqa: E402
from quota_state import (  # noqa: E402
    DEFAULT_EVENT_DIRECTORY,
    DEFAULT_STATE_PATH,
    QuotaStateError,
    aggregate_events,
    load_event_files,
    slot_eligibility,
)
from quota_state import load_state as load_quota_state  # noqa: E402

SUPPORTED_AGENTS = {
    "page-hygiene-checker": "prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.2.md",
    "language-style-checker": "prompts/phase-2/resolve-language-style-signal-issue-v1.2.2.md",
}
AUTOMATED_ISSUE_AGENTS = ("page-hygiene-checker", "language-style-checker")
SEMANTIC_PLACEHOLDER_VALUES = {"none", "n/a", "not applicable"}
REASON_CODES = {
    "in_scope_exact_edit",
    "out_of_scope",
    "obsolete",
    "insufficient_confidence",
    "source_check_required",
    "not_deterministic_or_local",
    "duplicate",
    "unsafe_edit",
    "no_current_page_match",
    "other",
}
ISSUE_TITLE_RE = re.compile(r"^Check signal: (?P<agent>[a-z0-9-]+): (?P<page>[^\s]+)$")
GENERATION_REVIEW_LOG_HEADER = "| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |"
GENERATION_REVIEW_LOG_SEPARATOR_RE = re.compile(
    r"^\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*$"
)
LEGACY_AUTO_RESOLVER_LOG_RE = re.compile(
    r"^\s*-\s+\d{4}-\d{2}-\d{2}:\s+Phase 2 automated resolver applied accepted "
    r"(?P<agent>[a-z0-9-]+) signal edits from issue #(?P<issue>\d+)\.\s*$"
)
TRANSIENT_ERROR_MARKERS = (
    "500",
    "502",
    "503",
    "504",
    "service_unavailable",
    "temporarily unavailable",
    "timeout",
    "unavailable",
)
JSON_SYSTEM_INSTRUCTION = (
    "Return only valid JSON matching the requested schema. "
    "Do not include Markdown fences, analysis, prefaces, or explanations outside JSON."
)


class ResolverError(RuntimeError):
    """Raised when automated resolution cannot proceed safely."""


@dataclass(frozen=True)
class IssueSnapshot:
    """Minimal GitHub issue state needed by the resolver."""

    number: int
    title: str
    body: str
    state: str
    url: str
    agent: str
    reviewed_page: str
    comments: list[dict[str, Any]]


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"expected a positive integer, got {value!r}") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError(f"expected a positive integer, got {value!r}")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automatically resolve one Phase 2 signal issue.")
    parser.add_argument("--repo", required=True, help="Repository in owner/name form.")
    parser.add_argument(
        "--issue",
        help=(
            "Issue number or issue URL. When omitted, the script selects the "
            "oldest open page-hygiene-checker or language-style-checker signal issue."
        ),
    )
    parser.add_argument("--provider", choices=["groq", "gemini"], default="gemini")
    parser.add_argument("--model", default="gemini-3.5-flash")
    parser.add_argument("--max-completion-tokens", type=int, default=8000)
    parser.add_argument(
        "--provider-max-attempts",
        type=positive_int,
        default=1,
        help=(
            "Maximum provider-call attempts per resolver run. The default is 1 to avoid "
            "spending additional quota on immediate retries."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate and validate a plan without modifying files or writing to GitHub.",
    )
    parser.add_argument("--branch-prefix", default="phase-2/auto-resolve")
    return parser.parse_args()


def run(cmd: list[str], *, cwd: Path | None = None, input_text: str | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ResolverError(f"Command failed ({' '.join(cmd)}):\n{detail}")
    return result.stdout


def issue_number(value: str) -> int:
    match = re.search(r"/(?:issues|pull)/(\d+)(?:$|[/?#])", value)
    if match:
        return int(match.group(1))
    if value.isdigit():
        return int(value)
    raise ResolverError(f"Could not parse issue number: {value}")


def search_oldest_open_issue_for_agent(repo: str, agent: str) -> dict[str, Any] | None:
    query = f'repo:{repo} is:issue is:open in:title "Check signal: {agent}:"'
    raw = run(
        [
            "gh",
            "api",
            "--method",
            "GET",
            "search/issues",
            "-f",
            f"q={query}",
            "-f",
            "sort=created",
            "-f",
            "order=asc",
            "-f",
            "per_page=10",
        ]
    )
    data = json.loads(raw)
    for item in data.get("items") or []:
        title = item.get("title") or ""
        match = ISSUE_TITLE_RE.match(title)
        if not match or match.group("agent") != agent:
            continue
        page_identity = match.group("page")
        if page_identity.startswith("classes/") or page_identity.startswith("relations/"):
            return item
    return None


def find_oldest_open_signal_issue(repo: str) -> int | None:
    candidates: list[dict[str, Any]] = []
    for agent in AUTOMATED_ISSUE_AGENTS:
        issue = search_oldest_open_issue_for_agent(repo, agent)
        if issue is not None:
            candidates.append(issue)
    if not candidates:
        return None
    oldest = min(candidates, key=lambda item: str(item.get("created_at") or ""))
    title = oldest.get("title") or ""
    number = oldest.get("number")
    if not isinstance(number, int):
        raise ResolverError(f"Oldest eligible issue has invalid number: {number!r}")
    print(f"Selected oldest eligible open Phase 2 signal issue #{number}: {title}")
    return number


def read_issue(repo: str, number: int) -> IssueSnapshot:
    raw = run(
        [
            "gh",
            "issue",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "number,title,body,state,url,comments",
        ]
    )
    data = json.loads(raw)
    title = data["title"]
    match = ISSUE_TITLE_RE.match(title)
    if not match:
        raise ResolverError(f"Issue title does not match Phase 2 signal pattern: {title}")
    agent = match.group("agent")
    if agent not in SUPPORTED_AGENTS:
        raise ResolverError(f"Unsupported resolver agent: {agent}")
    page_identity = match.group("page")
    if not (page_identity.startswith("classes/") or page_identity.startswith("relations/")):
        raise ResolverError(f"Unsupported page identity: {page_identity}")
    state = data.get("state") or ""
    if state.upper() != "OPEN":
        raise ResolverError(f"Issue must be open before automated resolution: state={state}")
    return IssueSnapshot(
        number=int(data["number"]),
        title=title,
        body=data.get("body") or "",
        state=state,
        url=data.get("url") or "",
        agent=agent,
        reviewed_page=f"docs/stereotypes/{page_identity}.md",
        comments=data.get("comments") or [],
    )


def load_text(path: Path) -> str:
    if not path.exists():
        raise ResolverError(f"Missing file: {path}")
    if not path.is_file():
        raise ResolverError(f"Expected a file: {path}")
    return path.read_text(encoding="utf-8")


def build_llm_input(issue: IssueSnapshot, page_text: str) -> str:
    comment_blocks: list[str] = []
    for comment in issue.comments:
        author = comment.get("author") or {}
        author_login = author.get("login", "") if isinstance(author, dict) else str(author)
        comment_blocks.append(
            "\n".join(
                [
                    f"COMMENT ID: {comment.get('id', '')}",
                    f"AUTHOR: {author_login}",
                    f"CREATED AT: {comment.get('createdAt', '')}",
                    "BODY:",
                    comment.get("body") or "",
                ]
            )
        )
    comments_text = "\n\n---\n\n".join(comment_blocks)
    return f"""ISSUE NUMBER: {issue.number}
ISSUE TITLE: {issue.title}
ISSUE URL: {issue.url}
AGENT: {issue.agent}
REVIEWED PAGE: {issue.reviewed_page}

ISSUE BODY:
{issue.body}

ISSUE COMMENTS:
{comments_text}

CURRENT REVIEWED PAGE CONTENT:
```markdown
{page_text}
```
"""


def _error_diagnostic(exc: Exception) -> str:
    return " ".join(
        [
            str(exc),
            str(getattr(exc, "code", "")),
            str(getattr(exc, "status", "")),
            str(getattr(exc, "reason", "")),
            str(getattr(exc, "body", "")),
        ]
    ).lower()


def _is_transient_error(exc: Exception) -> bool:
    diagnostic = _error_diagnostic(exc)
    return any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS)


def call_with_retries(operation_name: str, fn: Callable[[], str], *, max_attempts: int = 1) -> str:
    delays = (5.0, 15.0, 45.0)
    last_exc: Exception | None = None
    attempt_number = 0
    for attempt_number in range(1, max_attempts + 1):
        try:
            content = fn()
            if isinstance(content, str) and content.strip():
                return content.strip() + "\n"
            raise ResolverError(f"{operation_name} returned an empty response.")
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            last_exc = exc
            if attempt_number == max_attempts or not _is_transient_error(exc):
                break
            time.sleep(delays[min(attempt_number - 1, len(delays) - 1)])
    if last_exc is None:
        raise ResolverError(f"{operation_name} failed without an exception.")
    raise ResolverError(f"{operation_name} failed after {attempt_number} attempt(s): {last_exc}") from last_exc


def call_groq_json(model: str, review_input: str, max_completion_tokens: int, max_attempts: int) -> str:
    if not os.getenv("GROQ_API_KEY"):
        error = ResolverError("GROQ_API_KEY environment variable is not set.")
        record_provider_failure(provider="groq", model=model, exc=error, request_sent=False)
        raise error

    def invoke() -> str:
        from groq import Groq

        client = Groq()
        kwargs = {
            "model": model,
            "messages": [
                {"role": "system", "content": JSON_SYSTEM_INSTRUCTION},
                {"role": "user", "content": review_input},
            ],
            "temperature": 0,
            "max_completion_tokens": max_completion_tokens,
        }
        try:
            raw_resource = getattr(client.chat.completions, "with_raw_response", None)
            if raw_resource is None:
                response = client.chat.completions.create(**kwargs)
                headers: dict[str, str] = {}
            else:
                raw_response = raw_resource.create(**kwargs)
                response = raw_response.parse()
                headers = dict(getattr(raw_response, "headers", {}) or {})
            content = response.choices[0].message.content
            if not isinstance(content, str) or not content.strip():
                raise ResolverError("Groq resolver call returned an empty response.")
            record_provider_event(
                provider="groq",
                model=model,
                outcome="success",
                request_sent=True,
                response=response,
                headers=headers,
            )
            return content
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            record_provider_failure(provider="groq", model=model, exc=exc, request_sent=True)
            raise

    return call_with_retries("Groq resolver call", invoke, max_attempts=max_attempts)


def call_gemini_json(model: str, review_input: str, max_completion_tokens: int, max_attempts: int) -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        error = ResolverError("Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set.")
        record_provider_failure(provider="gemini", model=model, exc=error, request_sent=False)
        raise error

    def invoke() -> str:
        from google import genai
        from google.genai import types

        normalized = model.strip().lower()
        thinking_config = None
        if normalized.startswith("gemini-2.5-flash"):
            thinking_config = types.ThinkingConfig(thinking_budget=0)
        elif normalized.startswith("gemini-3."):
            thinking_config = types.ThinkingConfig(thinking_level="low")
        config_kwargs: dict[str, Any] = {
            "system_instruction": JSON_SYSTEM_INSTRUCTION,
            "max_output_tokens": max_completion_tokens,
            "temperature": 0,
        }
        if thinking_config is not None:
            config_kwargs["thinking_config"] = thinking_config
        client = genai.Client(api_key=api_key)
        try:
            response = client.models.generate_content(
                model=model,
                contents=review_input,
                config=types.GenerateContentConfig(**config_kwargs),
            )
            text = getattr(response, "text", None)
            if not isinstance(text, str) or not text.strip():
                candidates = getattr(response, "candidates", None) or []
                parts_text: list[str] = []
                for candidate in candidates:
                    content = getattr(candidate, "content", None)
                    parts = getattr(content, "parts", None) if content is not None else None
                    for part in parts or []:
                        part_text = getattr(part, "text", None)
                        if isinstance(part_text, str):
                            parts_text.append(part_text)
                text = "".join(parts_text)
            if not text.strip():
                raise ResolverError("Gemini resolver call returned an empty response.")
            record_provider_event(
                provider="gemini",
                model=model,
                outcome="success",
                request_sent=True,
                response=response,
            )
            return text
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            record_provider_failure(provider="gemini", model=model, exc=exc, request_sent=True)
            raise

    return call_with_retries("Gemini resolver call", invoke, max_attempts=max_attempts)


def call_provider(
    provider: str,
    model: str,
    prompt: str,
    user_input: str,
    max_tokens: int,
    max_attempts: int,
) -> str:
    review_input = f"{prompt}\n\n## Input\n\n{user_input}"
    if provider not in {"groq", "gemini"}:
        raise ResolverError(f"Unsupported provider: {provider}")
    try:
        require_executable_slot(provider, model)
    except RegistryValidationError as exc:
        raise ResolverError(str(exc)) from exc
    try:
        registry = load_registry(DEFAULT_REGISTRY_PATH)
        quota = load_quota_state(DEFAULT_STATE_PATH, registry)
        pending_events = load_event_files(Path(os.getenv("PHASE2_QUOTA_EVENT_DIR", str(DEFAULT_EVENT_DIRECTORY))))
        if pending_events:
            quota, _ = aggregate_events(quota, pending_events, registry)
        eligible, reason = slot_eligibility(
            quota,
            provider=provider,
            model=model,
            task_id=None,
            resolver_work_pending=False,
            now=datetime.now(timezone.utc),
        )
    except (OSError, QuotaStateError, ValueError) as exc:
        raise ResolverError(f"Could not evaluate resolver quota eligibility: {exc}") from exc
    if not eligible:
        failure_marker = (
            " provider_error_kind=provider_unavailable" if reason in {"slot-cooldown", "slot-recheck-required"} else ""
        )
        raise ResolverError(f"Resolver provider call withheld by quota/runtime guard: {reason}.{failure_marker}")
    if provider == "groq":
        return call_groq_json(model, review_input, max_tokens, max_attempts)
    if provider == "gemini":
        return call_gemini_json(model, review_input, max_tokens, max_attempts)
    raise ResolverError(f"Unsupported provider: {provider}")  # pragma: no cover - guarded above.


def parse_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    if not stripped.startswith("{"):
        first = stripped.find("{")
        last = stripped.rfind("}")
        if first != -1 and last != -1 and last > first:
            stripped = stripped[first : last + 1]
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise ResolverError(f"Resolver did not return valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ResolverError("Resolver JSON root must be an object.")
    return parsed


def normalize_rejected_group_edits(plan: dict[str, Any]) -> int:
    """Normalize omitted/null edits arrays for already rejected groups only."""
    groups = plan.get("signal_groups")
    if not isinstance(groups, list):
        return 0
    normalized = 0
    for group in groups:
        if not isinstance(group, dict) or group.get("decision") != "reject_for_phase_2_automation":
            continue
        if "edits" not in group or group.get("edits") is None:
            group["edits"] = []
            normalized += 1
    return normalized


def normalize_overall_decision(plan: dict[str, Any]) -> tuple[Any, str] | None:
    """Derive overall_decision from structurally recognizable group decisions."""
    groups = plan.get("signal_groups")
    if not isinstance(groups, list):
        return None
    accepted = False
    for group in groups:
        if not isinstance(group, dict):
            return None
        decision = group.get("decision")
        if decision not in {"accept", "reject_for_phase_2_automation"}:
            return None
        accepted = accepted or decision == "accept"
    derived = "accepted_changes" if accepted else "no_accepted_changes"
    original = plan.get("overall_decision")
    if original == derived:
        return None
    plan["overall_decision"] = derived
    return original, derived


def exact_occurrence_spans(text: str, needle: str) -> list[tuple[int, int]]:
    """Return all exact occurrence spans, including overlapping occurrences."""
    if not needle:
        return []
    spans: list[tuple[int, int]] = []
    start = 0
    while True:
        index = text.find(needle, start)
        if index == -1:
            return spans
        spans.append((index, index + len(needle)))
        start = index + 1


def line_numbers_for_exact_text(text: str, needle: str) -> list[int]:
    """Return 1-based line numbers where needle occurs exactly in text."""
    return [text.count("\n", 0, start) + 1 for start, _end in exact_occurrence_spans(text, needle)]


def nearest_markdown_heading(lines: list[str], line_number: int) -> str:
    for index in range(min(line_number, len(lines)), 0, -1):
        stripped = lines[index - 1].strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            return heading or stripped
    return ""


def format_match_locations(page_text: str, line_numbers: list[int]) -> str:
    if not line_numbers:
        return "none"
    lines = page_text.splitlines()
    locations: list[str] = []
    for line_number in line_numbers:
        heading = nearest_markdown_heading(lines, line_number)
        locations.append(f"line {line_number} under heading {heading!r}" if heading else f"line {line_number}")
    return "; ".join(locations)


def truncate_for_diagnostic(value: str, limit: int = 500) -> str:
    if len(value) <= limit:
        return value
    return f"{value[:limit]}... [truncated; {len(value)} characters total]"


def current_text_match_error(
    *,
    issue: IssueSnapshot,
    group_id: str,
    group_index: int,
    edit_index: int,
    current_text: str,
    page_text: str,
    match_lines: list[int],
) -> str:
    if not match_lines:
        cause = "The accepted edit target does not exist in the current reviewed page."
    else:
        cause = "The accepted edit target is ambiguous because it matches more than one location in the current reviewed page."
    rendered_group = group_id or f"group index {group_index}"
    return "\n".join(
        [
            "Accepted edit current_text must occur exactly once in the current page.",
            f"Issue: #{issue.number} — {issue.title}",
            f"Page: {issue.reviewed_page}",
            f"Signal group: {rendered_group}",
            f"Edit index: {edit_index}",
            f"Cause: {cause}",
            f"Matched location(s): {format_match_locations(page_text, match_lines)}",
            "Invalid current_text:",
            repr(truncate_for_diagnostic(current_text)),
            "Result: no reviewed page was changed, no pull request was created, and the issue remains open.",
        ]
    )


def _group_label(group: dict[str, Any], group_index: int) -> str:
    group_id = group.get("group_id")
    return str(group_id).strip() if isinstance(group_id, str) and group_id.strip() else f"group index {group_index}"


def _refs_text(group: dict[str, Any]) -> str:
    refs = group.get("source_signal_refs")
    if isinstance(refs, list):
        rendered = [str(ref).strip() for ref in refs if isinstance(ref, str) and ref.strip()]
        if rendered:
            return ", ".join(rendered)
    return "unspecified source signal"


def _automatic_rejection_rationale(label: str, failures: list[dict[str, Any]]) -> str:
    details = "; ".join(str(failure["message"]) for failure in failures)
    return (
        f"Automatically converted {label} to reject_for_phase_2_automation by the deterministic resolver wrapper: "
        f"{details}. The group is atomic, so none of its edits will be applied."
    )


def _reason_code_for_failures(failures: list[dict[str, Any]]) -> str:
    codes = {str(failure.get("reason_code") or "") for failure in failures}
    if codes == {"no_current_page_match"}:
        return "no_current_page_match"
    if "unsafe_edit" in codes:
        return "unsafe_edit"
    return "not_deterministic_or_local"


def is_semantic_placeholder_edit_value(value: str) -> bool:
    """Return whether an edit field is a known sentinel placeholder rather than exact text."""
    return value.strip().lower() in SEMANTIC_PLACEHOLDER_VALUES


def _edit_local_failures(
    *,
    edit: Any,
    edit_index: int,
    page_text: str,
) -> tuple[list[dict[str, Any]], tuple[int, int] | None]:
    failures: list[dict[str, Any]] = []
    if not isinstance(edit, dict):
        return (
            [
                {
                    "edit_index": edit_index,
                    "reason_code": "not_deterministic_or_local",
                    "message": f"edit {edit_index} is not an object",
                }
            ],
            None,
        )
    current = edit.get("current_text")
    proposed = edit.get("proposed_text")
    edit_rationale = edit.get("rationale")
    if not isinstance(current, str) or not current.strip():
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "not_deterministic_or_local",
                "message": f"edit {edit_index} has no non-empty current_text",
            }
        )
        return failures, None
    if not isinstance(proposed, str) or not proposed.strip():
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "not_deterministic_or_local",
                "message": f"edit {edit_index} has no non-empty proposed_text",
                "current_text": current,
            }
        )
    if is_semantic_placeholder_edit_value(current):
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "unsafe_edit",
                "message": f"edit {edit_index} current_text is a recognized placeholder value",
                "current_text": current,
            }
        )
    if isinstance(proposed, str) and is_semantic_placeholder_edit_value(proposed):
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "unsafe_edit",
                "message": f"edit {edit_index} proposed_text is a recognized placeholder value",
                "current_text": current,
            }
        )
    if not isinstance(edit_rationale, str) or not edit_rationale.strip():
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "not_deterministic_or_local",
                "message": f"edit {edit_index} has no non-empty rationale",
                "current_text": current,
            }
        )
    if isinstance(proposed, str) and current == proposed:
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "unsafe_edit",
                "message": f"edit {edit_index} has identical current_text and proposed_text",
                "current_text": current,
            }
        )
    if isinstance(proposed, str) and ("{{" in current or "}}" in current or "{{" in proposed or "}}" in proposed):
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "unsafe_edit",
                "message": f"edit {edit_index} contains an unresolved template placeholder",
                "current_text": current,
            }
        )
    spans = exact_occurrence_spans(page_text, current)
    if not spans:
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "no_current_page_match",
                "message": f"edit {edit_index} current_text has zero matches in the current page",
                "current_text": current,
                "match_count": 0,
            }
        )
    elif len(spans) > 1:
        failures.append(
            {
                "edit_index": edit_index,
                "reason_code": "not_deterministic_or_local",
                "message": f"edit {edit_index} current_text has {len(spans)} matches in the current page",
                "current_text": current,
                "match_count": len(spans),
                "match_lines": line_numbers_for_exact_text(page_text, current),
            }
        )
    return failures, spans[0] if len(spans) == 1 and not failures else None


def _accepted_change_comment_sentences(agent: str) -> tuple[str, str]:
    """Return the established agent-specific accepted-change comment sentences."""
    if agent == "page-hygiene-checker":
        return (
            "A pull request with the accepted deterministic local page-hygiene edits is available here: {{PR_URL}}",
            "The pull request applies only the remaining deterministic local Phase 2 page-hygiene edits.",
        )
    if agent == "language-style-checker":
        return (
            "A pull request with the accepted deterministic local language/style edits is available here: {{PR_URL}}",
            "The pull request applies only the remaining deterministic local Phase 2 language/style edits.",
        )
    raise ResolverError(f"Cannot render an automatic-rejection comment for unsupported agent: {agent}")


def render_automatic_rejection_issue_comment(plan: dict[str, Any], automatic_rejections: list[dict[str, Any]]) -> str:
    """Render a deterministic issue record that distinguishes automatic and model rejections."""
    groups = plan.get("signal_groups")
    if not isinstance(groups, list):
        raise ResolverError("Cannot render automatic-rejection comment without signal_groups.")
    automatic_indices = {int(record["group_index"]) for record in automatic_rejections}
    accepted_groups: list[tuple[int, dict[str, Any]]] = []
    explicit_rejections: list[tuple[int, dict[str, Any]]] = []
    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            continue
        if group.get("decision") == "accept":
            accepted_groups.append((index, group))
        elif index not in automatic_indices:
            explicit_rejections.append((index, group))

    lines = ["## Automated Phase 2 resolution", ""]
    if accepted_groups:
        pr_sentence, scope_sentence = _accepted_change_comment_sentences(str(plan.get("agent") or ""))
        lines.extend(
            [
                pr_sentence,
                "",
                scope_sentence,
                "",
                "### Accepted groups",
                "",
            ]
        )
        for index, group in accepted_groups:
            lines.append(
                f"- **{_group_label(group, index)}** ({_refs_text(group)}): {str(group.get('rationale') or '').strip()}"
            )
            edits = group.get("edits")
            if isinstance(edits, list):
                for edit_index, edit in enumerate(edits, start=1):
                    if not isinstance(edit, dict):
                        continue
                    edit_rationale = str(edit.get("rationale") or "").strip()
                    if edit_rationale:
                        lines.append(f"  - Accepted edit {edit_index}: {edit_rationale}")
    else:
        lines.extend(
            [
                "No page changes were applied. This issue is no longer automatically actionable under the current Phase 2 constraints and is closed as not planned for Phase 2 automation.",
                "",
                "### Accepted groups",
                "",
                "- None.",
            ]
        )

    lines.extend(["", "### Automatic deterministic rejections", ""])
    for record in automatic_rejections:
        label = str(record["group_label"])
        refs = ", ".join(record.get("source_signal_refs") or []) or "unspecified source signal"
        lines.append(
            f"- **{label}** ({refs}) was automatically converted to `reject_for_phase_2_automation` "
            f"with reason code `{record['reason_code']}`. {record['rationale']}"
        )

    lines.extend(["", "### Resolver rejections", ""])
    if explicit_rejections:
        for index, group in explicit_rejections:
            lines.append(
                f"- **{_group_label(group, index)}** ({_refs_text(group)}): explicitly rejected during normal "
                f"resolution with reason code `{group.get('reason_code')}`. {str(group.get('rationale') or '').strip()}"
            )
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "Automatic deterministic rejections are wrapper-enforced safety outcomes, not additional LLM decisions.",
            "Signals rejected for Phase 2 automation are not necessarily false; they are not safely actionable by this automated resolver.",
            "This resolution did not perform source-faithfulness validation, conceptual validation, cross-page semantic analysis, or OntoUML/UFO semantic validation.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def validate_plan_structure_before_revalidation(plan: dict[str, Any], issue: IssueSnapshot) -> None:
    """Validate non-page-dependent plan structure before automatic demotion.

    Automatic target revalidation must not conceal unrelated schema errors. This
    preflight therefore checks plan identity, group structure, group-level
    required fields, decision/reason-code consistency, rejected-group shape,
    and non-empty issue-comment shape before any accepted group can be rewritten.
    PR-placeholder consistency is checked by final plan validation after any
    deterministic issue-comment regeneration. Accepted edit-array shape,
    edit-local required fields, target counts,
    overlaps, unchanged edits, and unresolved edit placeholders remain the
    responsibility of automatic group revalidation so only the affected atomic
    group is demoted.
    """
    if plan.get("issue_number") != issue.number:
        raise ResolverError("Plan issue_number does not match the selected issue.")
    if plan.get("agent") != issue.agent:
        raise ResolverError("Plan agent does not match the selected issue.")
    if plan.get("reviewed_page") != issue.reviewed_page:
        raise ResolverError("Plan reviewed_page does not match the selected issue.")

    groups = plan.get("signal_groups")
    if not isinstance(groups, list):
        raise ResolverError("Plan signal_groups must be a list.")

    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            raise ResolverError(f"Signal group {index} must be an object.")

        expected_group_id = f"G-{index:03d}"
        group_id = group.get("group_id")
        if group_id != expected_group_id:
            raise ResolverError(
                f"Signal group IDs must be sequential: expected {expected_group_id}, found {group_id!r}."
            )

        decision = group.get("decision")
        if decision not in {"accept", "reject_for_phase_2_automation"}:
            raise ResolverError(f"Invalid group decision: {decision}")

        reason_code = group.get("reason_code")
        if reason_code not in REASON_CODES:
            raise ResolverError(f"Invalid reason_code: {reason_code}")

        rationale = group.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ResolverError("Each signal group must include a non-empty rationale.")

        refs = group.get("source_signal_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
            raise ResolverError("Each signal group must include non-empty source_signal_refs.")

        edits = group.get("edits")

        if decision == "accept":
            if reason_code != "in_scope_exact_edit":
                raise ResolverError("Accepted groups must use reason_code=in_scope_exact_edit.")
            # Accepted edit-array and edit-local shape failures are handled by
            # demote_invalid_accepted_groups so one malformed atomic group does
            # not fail otherwise valid independent groups.
        else:
            if reason_code == "in_scope_exact_edit":
                raise ResolverError("Rejected groups must not use reason_code=in_scope_exact_edit.")
            if not isinstance(edits, list):
                raise ResolverError("Rejected group edits must be a list.")
            if edits:
                raise ResolverError("Rejected groups must have an empty edits array.")

    comment = plan.get("issue_comment")
    if not isinstance(comment, str) or not comment.strip():
        raise ResolverError("Plan issue_comment must be a non-empty string.")


def demote_invalid_accepted_groups(plan: dict[str, Any], issue: IssueSnapshot, page_text: str) -> list[dict[str, Any]]:
    """Demote only accepted atomic groups that cannot be applied deterministically.

    Each group is treated as atomic. Local edit validity is checked first, then
    exact target spans are compared across accepted groups to prevent duplicate
    or overlapping application. All groups participating in a cross-group
    conflict are demoted, avoiding arbitrary first-wins behavior.
    """
    groups = plan.get("signal_groups")
    if not isinstance(groups, list):
        return []

    failures_by_group: dict[int, list[dict[str, Any]]] = {}
    valid_spans: list[tuple[int, int, int, int, str]] = []

    for group_index, group in enumerate(groups, start=1):
        if not isinstance(group, dict) or group.get("decision") != "accept":
            continue
        edits = group.get("edits")
        if not isinstance(edits, list) or not edits:
            failures_by_group.setdefault(group_index, []).append(
                {
                    "edit_index": None,
                    "reason_code": "not_deterministic_or_local",
                    "message": "the accepted group does not contain a non-empty edits array",
                }
            )
            continue
        for edit_index, edit in enumerate(edits, start=1):
            failures, span = _edit_local_failures(edit=edit, edit_index=edit_index, page_text=page_text)
            if failures:
                failures_by_group.setdefault(group_index, []).extend(failures)
            elif span is not None:
                current = str(edit["current_text"])
                valid_spans.append((span[0], span[1], group_index, edit_index, current))

    # Detect overlaps within each atomic group first. A group that is already
    # invalid must be excluded from cross-group conflict detection because none
    # of its edits will be applied; otherwise its discarded spans could
    # incorrectly demote an independent valid group.
    spans_by_group: dict[int, list[tuple[int, int, int, int, str]]] = {}
    for span in valid_spans:
        spans_by_group.setdefault(span[2], []).append(span)
    for group_index, group_spans in spans_by_group.items():
        if group_index in failures_by_group:
            continue
        ordered_group_spans = sorted(group_spans, key=lambda item: item[0])
        for left_index, left in enumerate(ordered_group_spans):
            left_start, left_end, _left_group, left_edit, left_current = left
            for right in ordered_group_spans[left_index + 1 :]:
                right_start, right_end, _right_group, right_edit, _right_current = right
                if left_end <= right_start:
                    break
                if right_end <= left_start:
                    continue
                failures_by_group.setdefault(group_index, []).append(
                    {
                        "edit_index": left_edit,
                        "reason_code": "not_deterministic_or_local",
                        "message": (
                            f"edits {left_edit} and {right_edit} have overlapping targets within the same atomic group"
                        ),
                        "current_text": left_current,
                    }
                )

    cross_group_spans = [span for span in valid_spans if span[2] not in failures_by_group]
    for left_index, left in enumerate(cross_group_spans):
        left_start, left_end, left_group, left_edit, left_current = left
        for right in cross_group_spans[left_index + 1 :]:
            right_start, right_end, right_group, right_edit, right_current = right
            if left_group == right_group:
                continue
            if left_end <= right_start or right_end <= left_start:
                continue
            failures_by_group.setdefault(left_group, []).append(
                {
                    "edit_index": left_edit,
                    "reason_code": "not_deterministic_or_local",
                    "message": (
                        f"edit {left_edit} overlaps the target of edit {right_edit} in "
                        f"{_group_label(groups[right_group - 1], right_group)}"
                    ),
                    "current_text": left_current,
                }
            )
            failures_by_group.setdefault(right_group, []).append(
                {
                    "edit_index": right_edit,
                    "reason_code": "not_deterministic_or_local",
                    "message": (
                        f"edit {right_edit} overlaps the target of edit {left_edit} in "
                        f"{_group_label(groups[left_group - 1], left_group)}"
                    ),
                    "current_text": right_current,
                }
            )

    records: list[dict[str, Any]] = []
    for group_index in sorted(failures_by_group):
        group = groups[group_index - 1]
        if not isinstance(group, dict) or group.get("decision") != "accept":
            continue
        failures = failures_by_group[group_index]
        label = _group_label(group, group_index)
        reason_code = _reason_code_for_failures(failures)
        rationale = _automatic_rejection_rationale(label, failures)
        refs = group.get("source_signal_refs")
        source_signal_refs = (
            [ref for ref in refs if isinstance(ref, str) and ref.strip()] if isinstance(refs, list) else []
        )
        record = {
            "group_index": group_index,
            "group_id": group.get("group_id"),
            "group_label": label,
            "source_signal_refs": source_signal_refs,
            "reason_code": reason_code,
            "rationale": rationale,
            "failures": failures,
        }
        records.append(record)
        group["decision"] = "reject_for_phase_2_automation"
        group["reason_code"] = reason_code
        group["rationale"] = rationale
        group["edits"] = []

    if records:
        plan["issue_comment"] = render_automatic_rejection_issue_comment(plan, records)
    return records


def validate_plan(plan: dict[str, Any], issue: IssueSnapshot, page_text: str) -> None:
    if plan.get("issue_number") != issue.number:
        raise ResolverError("Plan issue_number does not match the selected issue.")
    if plan.get("agent") != issue.agent:
        raise ResolverError("Plan agent does not match the selected issue.")
    if plan.get("reviewed_page") != issue.reviewed_page:
        raise ResolverError("Plan reviewed_page does not match the selected issue.")
    groups = plan.get("signal_groups")
    if not isinstance(groups, list):
        raise ResolverError("Plan signal_groups must be a list.")
    accepted = 0
    seen_current: set[str] = set()
    occupied_spans: list[tuple[int, int]] = []
    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            raise ResolverError(f"Signal group {index} must be an object.")
        expected_group_id = f"G-{index:03d}"
        group_id = group.get("group_id")
        if group_id != expected_group_id:
            raise ResolverError(
                f"Signal group IDs must be sequential: expected {expected_group_id}, found {group_id!r}."
            )
        decision = group.get("decision")
        if decision not in {"accept", "reject_for_phase_2_automation"}:
            raise ResolverError(f"Invalid group decision: {decision}")
        reason_code = group.get("reason_code")
        if reason_code not in REASON_CODES:
            raise ResolverError(f"Invalid reason_code: {reason_code}")
        rationale = group.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ResolverError("Each signal group must include a non-empty rationale.")
        refs = group.get("source_signal_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
            raise ResolverError("Each signal group must include non-empty source_signal_refs.")
        edits = group.get("edits")
        if not isinstance(edits, list):
            raise ResolverError("Group edits must be a list.")
        if decision == "accept":
            accepted += 1
            group_id = str(group.get("group_id") or "")
            if reason_code != "in_scope_exact_edit":
                raise ResolverError("Accepted groups must use reason_code=in_scope_exact_edit.")
            if not edits:
                raise ResolverError("Accepted groups must contain at least one edit.")
            for edit_index, edit in enumerate(edits, start=1):
                if not isinstance(edit, dict):
                    raise ResolverError(f"Edit {edit_index} in group {index} must be an object.")
                current = edit.get("current_text")
                proposed = edit.get("proposed_text")
                edit_rationale = edit.get("rationale")
                if not isinstance(current, str) or not current.strip():
                    raise ResolverError("Accepted edit current_text must be a non-empty string.")
                if not isinstance(proposed, str) or not proposed.strip():
                    raise ResolverError("Accepted edit proposed_text must be a non-empty string.")
                if is_semantic_placeholder_edit_value(current) or is_semantic_placeholder_edit_value(proposed):
                    raise ResolverError("Accepted edit fields must not use recognized placeholder values.")
                if not isinstance(edit_rationale, str) or not edit_rationale.strip():
                    raise ResolverError("Accepted edit rationale must be a non-empty string.")
                if current == proposed:
                    raise ResolverError("Accepted edit current_text and proposed_text must differ.")
                if "{{" in current or "}}" in current or "{{" in proposed or "}}" in proposed:
                    raise ResolverError("Accepted edits must not contain template placeholders.")
                spans = exact_occurrence_spans(page_text, current)
                match_lines = line_numbers_for_exact_text(page_text, current)
                if len(spans) != 1:
                    raise ResolverError(
                        current_text_match_error(
                            issue=issue,
                            group_id=group_id,
                            group_index=index,
                            edit_index=edit_index,
                            current_text=current,
                            page_text=page_text,
                            match_lines=match_lines,
                        )
                    )
                if current in seen_current:
                    raise ResolverError(f"Duplicate current_text across accepted edits: {current[:120]!r}")
                span = spans[0]
                if any(not (span[1] <= start or end <= span[0]) for start, end in occupied_spans):
                    raise ResolverError("Accepted edit targets must not overlap.")
                seen_current.add(current)
                occupied_spans.append(span)
        else:
            if reason_code == "in_scope_exact_edit":
                raise ResolverError("Rejected groups must not use reason_code=in_scope_exact_edit.")
            if edits:
                raise ResolverError("Rejected groups must have an empty edits array.")
    expected_decision = "accepted_changes" if accepted else "no_accepted_changes"
    if plan.get("overall_decision") != expected_decision:
        raise ResolverError(f"overall_decision must be {expected_decision}.")
    comment = plan.get("issue_comment")
    if not isinstance(comment, str) or not comment.strip():
        raise ResolverError("Plan issue_comment must be a non-empty string.")
    placeholder_count = comment.count("{{PR_URL}}")
    if accepted and placeholder_count != 1:
        raise ResolverError("Accepted-change comments must contain {{PR_URL}} placeholder exactly once.")
    if not accepted and placeholder_count != 0:
        raise ResolverError("No-accepted-change comments must not contain {{PR_URL}} placeholder.")


def markdown_table_cell(value: str) -> str:
    return value.replace("\n", " ").replace("|", "\\|").strip()


def resolver_prompt_metadata(agent: str) -> tuple[str, str]:
    if agent == "page-hygiene-checker":
        return (
            "resolve-page-hygiene-signal-issue-v1.2.2",
            "Phase 2 automated resolver: page-hygiene signals v1.2.2",
        )
    if agent == "language-style-checker":
        return (
            "resolve-language-style-signal-issue-v1.2.2",
            "Phase 2 automated resolver: language-style signals v1.2.2",
        )
    raise ResolverError(f"Unsupported resolver agent for log metadata: {agent}")


def render_generation_review_log_row(plan: dict[str, Any]) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    agent = str(plan["agent"])
    issue = int(plan["issue_number"])
    prompt_id, prompt_title = resolver_prompt_metadata(agent)
    cells = [
        stamp,
        "Phase 2",
        "Phase 2 automated resolver",
        "Signal resolution",
        prompt_id,
        prompt_title,
        f"GitHub issue #{issue}",
        (
            f"Applied accepted {agent} signal edits through automated Phase 2 resolution; "
            "not a conceptual or source-faithfulness validation."
        ),
    ]
    return "| " + " | ".join(markdown_table_cell(cell) for cell in cells) + " |"


def remove_legacy_auto_resolver_log_lines(page_text: str, plan: dict[str, Any]) -> str:
    expected_agent = str(plan["agent"])
    expected_issue = str(plan["issue_number"])
    retained_lines: list[str] = []
    for line in page_text.splitlines():
        match = LEGACY_AUTO_RESOLVER_LOG_RE.match(line)
        if match and match.group("agent") == expected_agent and match.group("issue") == expected_issue:
            continue
        retained_lines.append(line)
    return "\n".join(retained_lines) + ("\n" if page_text.endswith("\n") else "")


def append_generation_review_log_row(page_text: str, plan: dict[str, Any]) -> str:
    row = render_generation_review_log_row(plan)
    updated = remove_legacy_auto_resolver_log_lines(page_text, plan)
    if row in updated:
        return updated
    lines = updated.rstrip("\n").splitlines()
    header_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == GENERATION_REVIEW_LOG_HEADER:
            header_index = index
    if header_index is None:
        raise ResolverError("Generation and Review Log table header was not found.")
    separator_index = header_index + 1
    if separator_index >= len(lines) or not GENERATION_REVIEW_LOG_SEPARATOR_RE.match(lines[separator_index].strip()):
        raise ResolverError("Generation and Review Log table separator row was not found.")
    insert_index = separator_index + 1
    while insert_index < len(lines) and lines[insert_index].strip().startswith("|"):
        insert_index += 1
    lines.insert(insert_index, row)
    return "\n".join(lines).rstrip() + "\n"


def apply_edits(page_text: str, plan: dict[str, Any]) -> str:
    """Apply validated edits by their original-page spans, from right to left.

    Positional application prevents an earlier replacement from introducing a
    new copy of a later edit's ``current_text`` and redirecting a sequential
    ``str.replace(..., 1)`` call to the wrong occurrence.
    """
    applications: list[tuple[int, int, str]] = []
    for group in plan["signal_groups"]:
        if group["decision"] != "accept":
            continue
        for edit in group["edits"]:
            spans = exact_occurrence_spans(page_text, edit["current_text"])
            if len(spans) != 1:
                raise ResolverError("Accepted edit target changed after validation; refusing to apply edits.")
            start, end = spans[0]
            applications.append((start, end, edit["proposed_text"]))

    ordered = sorted(applications, key=lambda item: item[0])
    for (left_start, left_end, _), (right_start, _right_end, _) in zip(ordered, ordered[1:]):
        if left_end > right_start:
            raise ResolverError("Accepted edit targets overlap; refusing to apply edits.")

    updated = page_text
    for start, end, proposed in reversed(ordered):
        updated = updated[:start] + proposed + updated[end:]
    return append_generation_review_log_row(updated, plan)


def run_structure_check(page: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tmp:
        output_path = Path(tmp.name)
    try:
        run(
            [
                "python",
                "scripts/phase-2/check_agents/page_structure_checker.py",
                "--page",
                page,
                "--output",
                str(output_path),
                "--commit-sha",
                "WORKTREE",
                "--max-signals",
                "3",
            ]
        )
        report = output_path.read_text(encoding="utf-8")
        match = re.search(r"\|\s*Signal count\s*\|\s*(\d+)\s*\|", report)
        if not match:
            raise ResolverError("Could not parse page-structure checker Signal count.")
        if int(match.group(1)) > 0:
            raise ResolverError("Updated page produced page-structure signals; refusing to create PR.")
    finally:
        output_path.unlink(missing_ok=True)


def create_pr(repo: str, issue: IssueSnapshot, branch_prefix: str) -> str:
    branch = f"{branch_prefix}-issue-{issue.number}"
    run(["git", "checkout", "-B", branch])
    run(["git", "add", issue.reviewed_page])
    diff_cached = run(["git", "diff", "--cached", "--name-only"])
    if issue.reviewed_page not in diff_cached.splitlines():
        raise ResolverError("No staged page change after applying accepted edits.")
    run(
        [
            "git",
            "commit",
            "-m",
            f"fix(phase-2): resolve {issue.agent} signals for issue #{issue.number}",
        ]
    )
    run(["git", "push", "--force-with-lease", "origin", branch])
    title = f"Resolve Phase 2 {issue.agent} signals for issue #{issue.number}"
    body = (
        f"Automated Phase 2 resolver PR for {issue.url}.\n\n"
        "This PR applies accepted deterministic local edits only. "
        "Rejected signals, including cases rejected for Phase 2 automation, "
        "are documented in the issue closure comment."
    )
    return run(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            repo,
            "--title",
            title,
            "--body",
            body,
            "--base",
            "main",
            "--head",
            branch,
        ]
    ).strip()


def update_pr_branch(repo: str, pr_url: str) -> None:
    run(["gh", "pr", "update-branch", pr_url, "--repo", repo, "--rebase"])


def enable_pr_auto_merge(repo: str, pr_url: str) -> None:
    run(
        [
            "gh",
            "pr",
            "merge",
            pr_url,
            "--repo",
            repo,
            "--auto",
            "--squash",
            "--delete-branch",
        ]
    )


def comment_issue(repo: str, issue_number_value: int, body: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body.rstrip() + "\n")
        comment_path = Path(tmp.name)
    try:
        run(
            [
                "gh",
                "issue",
                "comment",
                str(issue_number_value),
                "--repo",
                repo,
                "--body-file",
                str(comment_path),
            ]
        )
    finally:
        comment_path.unlink(missing_ok=True)


def close_issue(repo: str, issue_number_value: int, state_reason: str) -> None:
    if state_reason not in {"completed", "not_planned"}:
        raise ResolverError(f"Unsupported state_reason: {state_reason}")
    run(
        [
            "gh",
            "api",
            f"repos/{repo}/issues/{issue_number_value}",
            "-X",
            "PATCH",
            "-f",
            "state=closed",
            "-f",
            f"state_reason={state_reason}",
        ]
    )


def comment_and_close(repo: str, issue: IssueSnapshot, body: str, state_reason: str) -> None:
    comment_issue(repo, issue.number, body)
    close_issue(repo, issue.number, state_reason)


def resolver_output_dir() -> Path:
    output_dir = Path(".tmp/phase-2/resolver")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_text_artifact(output_dir: Path, filename: str, content: str) -> None:
    suffix = "" if content.endswith("\n") else "\n"
    (output_dir / filename).write_text(content + suffix, encoding="utf-8")


def write_json_artifact(output_dir: Path, filename: str, value: Any) -> None:
    (output_dir / filename).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        if args.issue:
            number = issue_number(args.issue)
        else:
            selected = find_oldest_open_signal_issue(args.repo)
            if selected is None:
                print(
                    "No open eligible Phase 2 signal issue found for "
                    "page-hygiene-checker or language-style-checker. Nothing to resolve."
                )
                return 0
            number = selected
        issue = read_issue(args.repo, number)
        page_path = Path(issue.reviewed_page)
        page_text = load_text(page_path)
        prompt = load_text(Path(SUPPORTED_AGENTS[issue.agent]))
        output_dir = resolver_output_dir()
        try:
            raw = call_provider(
                args.provider,
                args.model,
                prompt,
                build_llm_input(issue, page_text),
                args.max_completion_tokens,
                args.provider_max_attempts,
            )
        except ResolverError as exc:
            write_text_artifact(output_dir, f"issue-{issue.number}-provider-error.txt", str(exc))
            raise
        write_text_artifact(output_dir, f"issue-{issue.number}-raw-response.txt", raw)
        try:
            plan = parse_json(raw)
            write_json_artifact(output_dir, f"issue-{issue.number}-parsed-plan.json", plan)
            normalization_messages: list[str] = []
            normalized_count = normalize_rejected_group_edits(plan)
            if normalized_count:
                normalization_messages.append(
                    f"Normalized {normalized_count} rejected signal group edits value(s) to []."
                )
            validate_plan_structure_before_revalidation(plan, issue)
            automatic_rejections = demote_invalid_accepted_groups(plan, issue, page_text)
            if automatic_rejections:
                normalization_messages.append(
                    f"Automatically demoted {len(automatic_rejections)} invalid accepted atomic signal group(s)."
                )
                write_json_artifact(
                    output_dir,
                    f"issue-{issue.number}-automatic-rejections.json",
                    automatic_rejections,
                )
            overall_decision_change = normalize_overall_decision(plan)
            if overall_decision_change is not None:
                original_decision, derived_decision = overall_decision_change
                normalization_messages.append(
                    "Normalized overall_decision from "
                    f"{original_decision!r} to {derived_decision!r} based on signal group decisions."
                )
            if normalization_messages:
                normalization_summary = "\n".join(normalization_messages)
                print(normalization_summary)
                write_text_artifact(
                    output_dir,
                    f"issue-{issue.number}-normalization.txt",
                    normalization_summary,
                )
                write_json_artifact(output_dir, f"issue-{issue.number}-normalized-plan.json", plan)
            validate_plan(plan, issue, page_text)
        except ResolverError as exc:
            write_text_artifact(output_dir, f"issue-{issue.number}-plan-error.txt", str(exc))
            raise
        output_path = output_dir / f"issue-{issue.number}-plan.json"
        output_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.dry_run:
            print(json.dumps(plan, indent=2, ensure_ascii=False))
            return 0
        if plan["overall_decision"] == "accepted_changes":
            updated = apply_edits(page_text, plan)
            page_path.write_text(updated, encoding="utf-8")
            run_structure_check(issue.reviewed_page)
            pr_url = create_pr(args.repo, issue, args.branch_prefix)
            update_pr_branch(args.repo, pr_url)
            enable_pr_auto_merge(args.repo, pr_url)
            comment = plan["issue_comment"].replace("{{PR_URL}}", pr_url)
            comment_and_close(args.repo, issue, comment, "completed")
        else:
            comment_and_close(args.repo, issue, plan["issue_comment"], "not_planned")
        return 0
    except ResolverError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
