#!/usr/bin/env python3
"""Resolve Phase 2 check-signal issues automatically.

The script reads one selected GitHub issue, or selects the oldest eligible open
page-hygiene/language-style signal issue when no issue is supplied. It then asks
a resolver LLM for a strict JSON resolution plan, validates exact local edits,
optionally creates a pull request for accepted edits, comments on the issue, and
closes the issue.

The LLM is used only to classify signals and propose exact replacements. All
file edits and GitHub mutations are performed by this deterministic wrapper.
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
from typing import Any

SUPPORTED_AGENTS = {
    "page-hygiene-checker": "prompts/phase-2/resolve-page-hygiene-signal-issue-v1.1.0.md",
    "language-style-checker": "prompts/phase-2/resolve-language-style-signal-issue-v1.1.0.md",
}

AUTOMATED_ISSUE_AGENTS = (
    "page-hygiene-checker",
    "language-style-checker",
)

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
TRANSIENT_ERROR_MARKERS = (
    "429",
    "500",
    "502",
    "503",
    "504",
    "rate_limit_exceeded",
    "resource_exhausted",
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
    """Return the oldest open issue for one supported signal-agent title prefix."""
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
    items = data.get("items") or []
    for item in items:
        title = item.get("title") or ""
        match = ISSUE_TITLE_RE.match(title)
        if not match:
            continue
        if match.group("agent") != agent:
            continue
        page_identity = match.group("page")
        if not (page_identity.startswith("classes/") or page_identity.startswith("relations/")):
            continue
        return item
    return None


def find_oldest_open_signal_issue(repo: str) -> int | None:
    """Return the oldest eligible open Phase 2 signal issue number, if one exists."""
    candidates: list[dict[str, Any]] = []
    for agent in AUTOMATED_ISSUE_AGENTS:
        issue = search_oldest_open_issue_for_agent(repo, agent)
        if issue is not None:
            candidates.append(issue)

    if not candidates:
        return None

    def created_key(item: dict[str, Any]) -> str:
        return str(item.get("created_at") or "")

    oldest = min(candidates, key=created_key)
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
        comment_blocks.append(
            "\n".join(
                [
                    f"COMMENT ID: {comment.get('id', '')}",
                    f"AUTHOR: {author.get('login', '')}",
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


def _is_transient_error(exc: Exception) -> bool:
    diagnostic = " ".join(
        [
            str(exc),
            str(getattr(exc, "code", "")),
            str(getattr(exc, "status", "")),
            str(getattr(exc, "reason", "")),
        ]
    ).lower()
    return any(marker in diagnostic for marker in TRANSIENT_ERROR_MARKERS)


def call_with_retries(operation_name: str, fn: Any) -> str:
    delays = (5.0, 15.0, 45.0)
    total_attempts = len(delays) + 1
    last_exc: Exception | None = None

    for attempt_number in range(1, total_attempts + 1):
        try:
            content = fn()
            if isinstance(content, str) and content.strip():
                return content.strip() + "\n"
            raise ResolverError(f"{operation_name} returned an empty response.")
        except Exception as exc:  # noqa: BLE001 - provider SDKs raise heterogeneous exceptions.
            last_exc = exc
            if attempt_number == total_attempts or not _is_transient_error(exc):
                break
            time.sleep(delays[attempt_number - 1])

    if last_exc is None:
        raise ResolverError(f"{operation_name} failed without an exception.")
    raise ResolverError(f"{operation_name} failed after {attempt_number} attempt(s): {last_exc}") from last_exc


def call_groq_json(model: str, review_input: str, max_completion_tokens: int) -> str:
    if not os.getenv("GROQ_API_KEY"):
        raise ResolverError("GROQ_API_KEY environment variable is not set.")

    def invoke() -> str:
        from groq import Groq

        client = Groq()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": JSON_SYSTEM_INSTRUCTION},
                {"role": "user", "content": review_input},
            ],
            temperature=0,
            max_completion_tokens=max_completion_tokens,
        )
        content = response.choices[0].message.content
        return content if isinstance(content, str) else ""

    return call_with_retries("Groq resolver call", invoke)


def call_gemini_json(model: str, review_input: str, max_completion_tokens: int) -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ResolverError("Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set.")

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
        response = client.models.generate_content(
            model=model,
            contents=review_input,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        text = getattr(response, "text", None)
        if isinstance(text, str) and text.strip():
            return text

        candidates = getattr(response, "candidates", None) or []
        parts_text: list[str] = []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) if content is not None else None
            for part in parts or []:
                part_text = getattr(part, "text", None)
                if isinstance(part_text, str):
                    parts_text.append(part_text)
        return "".join(parts_text)

    return call_with_retries("Gemini resolver call", invoke)


def call_provider(provider: str, model: str, prompt: str, user_input: str, max_tokens: int) -> str:
    review_input = f"{prompt}\n\n## Input\n\n{user_input}"
    if provider == "groq":
        return call_groq_json(model, review_input, max_tokens)
    if provider == "gemini":
        return call_gemini_json(model, review_input, max_tokens)
    raise ResolverError(f"Unsupported provider: {provider}")


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
    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            raise ResolverError(f"Signal group {index} must be an object.")

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
        if not isinstance(refs, list) or not all(isinstance(ref, str) and ref.strip() for ref in refs):
            raise ResolverError("Each signal group must include non-empty source_signal_refs.")

        edits = group.get("edits")
        if not isinstance(edits, list):
            raise ResolverError("Group edits must be a list.")

        if decision == "accept":
            accepted += 1
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

                if not isinstance(current, str) or not current:
                    raise ResolverError("Accepted edit current_text must be a non-empty string.")
                if not isinstance(proposed, str):
                    raise ResolverError("Accepted edit proposed_text must be a string.")
                if not isinstance(edit_rationale, str) or not edit_rationale.strip():
                    raise ResolverError("Accepted edit rationale must be a non-empty string.")
                if current == proposed:
                    raise ResolverError("Accepted edit current_text and proposed_text must differ.")
                if "{{" in current or "}}" in current or "{{" in proposed or "}}" in proposed:
                    raise ResolverError("Accepted edits must not contain template placeholders.")
                if page_text.count(current) != 1:
                    raise ResolverError(
                        f"Accepted edit current_text must occur exactly once in the current page: {current[:120]!r}"
                    )
                if current in seen_current:
                    raise ResolverError(f"Duplicate current_text across accepted edits: {current[:120]!r}")
                seen_current.add(current)
        elif edits:
            raise ResolverError("Rejected groups must have an empty edits array.")

    expected_decision = "accepted_changes" if accepted else "no_accepted_changes"
    if plan.get("overall_decision") != expected_decision:
        raise ResolverError(f"overall_decision must be {expected_decision}.")

    comment = plan.get("issue_comment")
    if not isinstance(comment, str) or not comment.strip():
        raise ResolverError("Plan issue_comment must be a non-empty string.")
    if accepted and "{{PR_URL}}" not in comment:
        raise ResolverError("Accepted-change comments must contain {{PR_URL}} placeholder.")
    if not accepted and "{{PR_URL}}" in comment:
        raise ResolverError("No-accepted-change comments must not contain {{PR_URL}} placeholder.")


def apply_edits(page_text: str, plan: dict[str, Any]) -> str:
    updated = page_text
    for group in plan["signal_groups"]:
        if group["decision"] != "accept":
            continue
        for edit in group["edits"]:
            updated = updated.replace(edit["current_text"], edit["proposed_text"], 1)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_entry = (
        f"\n- {stamp}: Phase 2 automated resolver applied accepted "
        f"{plan['agent']} signal edits from issue #{plan['issue_number']}.\n"
    )
    if "## Generation and Review Log" in updated and log_entry.strip() not in updated:
        updated = updated.rstrip() + log_entry
    return updated


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

    run(["git", "commit", "-m", f"fix(phase-2): resolve {issue.agent} signals for issue #{issue.number}"])
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


def comment_issue(repo: str, issue_number_value: int, body: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(body.rstrip() + "\n")
        comment_path = Path(tmp.name)

    try:
        run(["gh", "issue", "comment", str(issue_number_value), "--repo", repo, "--body-file", str(comment_path)])
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

        raw = call_provider(
            args.provider,
            args.model,
            prompt,
            build_llm_input(issue, page_text),
            args.max_completion_tokens,
        )
        plan = parse_json(raw)
        validate_plan(plan, issue, page_text)

        output_dir = Path(".tmp/phase-2/resolver")
        output_dir.mkdir(parents=True, exist_ok=True)
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
