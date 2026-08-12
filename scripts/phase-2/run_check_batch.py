#!/usr/bin/env python3
"""Run Phase 2 LLM check agents across pages, agents, providers, and models.

The batch runner delegates individual LLM calls and output validation to
`scripts/phase-2/run_check_agent.py`, and optionally delegates issue dry-runs
or posting to `scripts/phase-2/issue_manager.py`.

It supports rotating scheduled execution where one provider/model triple is run
per workflow interval and failures can be treated as nonfatal so the next
scheduled rotation slot can proceed.
"""

from __future__ import annotations

import argparse
import itertools
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import (  # noqa: E402 - direct script execution needs its directory on sys.path.
    DEFAULT_REGISTRY_PATH,
    SUPPORTED_PROVIDERS,
    load_registry,
    require_executable_slot,
    validate_completion_token_cap,
)
from quota_state import (  # noqa: E402 - direct script execution needs its directory on sys.path.
    DEFAULT_EVENT_DIRECTORY,
    QuotaStateError,
    aggregate_events,
    load_event_files,
    slot_eligibility,
)
from quota_state import (  # noqa: E402 - direct script execution needs its directory on sys.path.
    DEFAULT_STATE_PATH as DEFAULT_QUOTA_STATE_PATH,
)
from quota_state import (  # noqa: E402 - direct script execution needs its directory on sys.path.
    load_state as load_quota_state,
)
from run_check_agent import AGENT_CONTRACTS  # noqa: E402 - shared active agent contracts.
from task_identity import build_task_identity, task_id_for  # noqa: E402 - shared task identity contract.

DEFAULT_AGENTS = ["page-hygiene-checker", "language-style-checker"]
DEFAULT_OUTPUT_ROOT = Path(".tmp/phase-2")
DEFAULT_SLEEP_SECONDS = 0.0
SUMMARY_FILENAME = "batch-summary.md"

RUN_CHECK_AGENT_PATH = Path("scripts/phase-2/run_check_agent.py")
ISSUE_MANAGER_PATH = Path("scripts/phase-2/issue_manager.py")

RUN_STATUS_OK = "ok"
RUN_STATUS_FAILED = "failed"
RUN_STATUS_PROVIDER_FAILED = "provider_failed"
RUN_STATUS_REJECTED = "rejected"
RUN_STATUS_SKIPPED = "skipped"
CHECK_VALIDATION_FAILURE_MARKER = "Generated issue comment failed validation:"


@dataclass(frozen=True)
class PlannedRun:
    index: int
    page: str
    agent: str
    provider: str
    model: str
    output_path: Path
    log_path: Path


@dataclass(frozen=True)
class CompletedRun:
    planned: PlannedRun
    check_status: str
    check_exit_code: int | None
    issue_status: str
    issue_exit_code: int | None
    message: str
    provider_failure_is_nonfatal: bool = False

    @property
    def rejected(self) -> bool:
        return self.check_status == RUN_STATUS_REJECTED

    @property
    def provider_failed(self) -> bool:
        return self.check_status == RUN_STATUS_PROVIDER_FAILED

    @property
    def fatal_failed(self) -> bool:
        return (
            self.check_status == RUN_STATUS_FAILED
            or (self.check_status == RUN_STATUS_PROVIDER_FAILED and not self.provider_failure_is_nonfatal)
            or self.issue_status == RUN_STATUS_FAILED
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 2 check agents across pages, agents, and models.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to the current working directory.")
    parser.add_argument("--page", action="append", default=[], help="Repository-relative Markdown page to check.")
    parser.add_argument(
        "--pages-glob", action="append", default=[], help="Repository-relative glob for Markdown pages."
    )
    parser.add_argument(
        "--exclude-page", action="append", default=[], help="Repository-relative Markdown page to exclude."
    )
    parser.add_argument(
        "--exclude-pages-glob", action="append", default=[], help="Repository-relative glob for pages to exclude."
    )
    parser.add_argument("--agent", action="append", default=[], choices=DEFAULT_AGENTS, help="Check agent to run.")
    parser.add_argument(
        "--provider", required=True, choices=SUPPORTED_PROVIDERS, help="Configured LLM provider to use."
    )
    parser.add_argument(
        "--model", action="append", required=True, help="Model to use. Must be passed at least once; may be repeated."
    )
    parser.add_argument(
        "--mode",
        choices=["generate", "dry-run", "post"],
        default="generate",
        help="Batch mode. 'generate' only writes comment files; 'dry-run' or 'post' invoke issue_manager.py.",
    )
    parser.add_argument("--repo", help="GitHub repository full name, required for --mode dry-run or --mode post.")
    parser.add_argument("--post-empty", action="store_true", help="Forward --post-empty to issue_manager.py.")
    parser.add_argument(
        "--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Root directory for generated comments."
    )
    parser.add_argument("--summary", help="Path for the Markdown batch summary.")
    parser.add_argument(
        "--sleep-seconds", type=float, default=DEFAULT_SLEEP_SECONDS, help="Seconds to sleep between runs."
    )
    parser.add_argument(
        "--max-runs", type=int, help="Maximum number of planned combinations to execute after selection."
    )
    parser.add_argument("--selection", choices=["first", "rotate"], default="first", help="How to select runs.")
    parser.add_argument(
        "--rotation-seed", choices=["hourly", "daily"], default="hourly", help="Time seed for rotation."
    )
    parser.add_argument(
        "--rotation-index", type=int, help="Explicit non-negative rotation index for --selection rotate."
    )
    parser.add_argument("--fail-fast", action="store_true", help="Stop after the first fatal failed individual run.")
    parser.add_argument(
        "--plan-only", action="store_true", help="Print and summarize planned runs without executing them."
    )
    parser.add_argument(
        "--max-completion-tokens", type=int, help="Forward --max-completion-tokens to run_check_agent.py."
    )
    parser.add_argument(
        "--allow-rejected-check-outputs",
        action="store_true",
        help="Treat check-agent output validation failures as nonfatal rejected outputs.",
    )
    parser.add_argument(
        "--allow-provider-failures",
        action="store_true",
        help=(
            "Treat transient provider-side availability failures as nonfatal. "
            "Quota, rate-limit, authentication, configuration, and request-shape failures remain fatal."
        ),
    )
    parser.add_argument(
        "--quota-state",
        default=str(DEFAULT_QUOTA_STATE_PATH),
        help="Persistent best-known quota state used by the pre-call eligibility guard.",
    )
    parser.add_argument(
        "--resolver-work-pending",
        action="store_true",
        help="Withhold the two shared resolver provider-model slots from signal calls.",
    )
    return parser.parse_args()


def normalize_repo_relative_path(path_value: str) -> str:
    return Path(path_value).as_posix().lstrip("./")


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "unnamed"


def page_identity(page: str) -> str:
    normalized = normalize_repo_relative_path(page)
    prefix = "docs/stereotypes/"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix) :]
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return normalized


def filesystem_path(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def output_path_for(*, output_root: Path, page: str, agent: str, provider: str, model: str) -> Path:
    page_dir = safe_slug(page_identity(page).replace("/", "-"))
    provider_slug = safe_slug(provider)
    model_slug = safe_slug(model)
    return output_root / agent / page_dir / f"issue-comment-{provider_slug}-{model_slug}.md"


def log_path_for(output_path: Path) -> Path:
    return output_path.with_suffix(".batch.log")


def discover_pages(
    repo_root: Path,
    explicit_pages: Sequence[str],
    globs: Sequence[str],
    explicit_excluded_pages: Sequence[str],
    excluded_globs: Sequence[str],
) -> list[str]:
    pages: set[str] = set()
    for page in explicit_pages:
        normalized = normalize_repo_relative_path(page)
        if not normalized.endswith(".md"):
            raise ValueError(f"Page is not a Markdown file: {page}")
        pages.add(normalized)
    for pattern in globs:
        for match in sorted(repo_root.glob(pattern)):
            if match.is_file() and match.suffix == ".md":
                pages.add(match.relative_to(repo_root).as_posix())

    excluded_pages: set[str] = set()
    for page in explicit_excluded_pages:
        normalized = normalize_repo_relative_path(page)
        if normalized.endswith(".md"):
            excluded_pages.add(normalized)
    for pattern in excluded_globs:
        for match in sorted(repo_root.glob(pattern)):
            if match.is_file() and match.suffix == ".md":
                excluded_pages.add(match.relative_to(repo_root).as_posix())

    pages -= excluded_pages
    if not pages:
        raise ValueError("No pages selected. Pass --page and/or --pages-glob.")
    missing = [page for page in sorted(pages) if not (repo_root / page).is_file()]
    if missing:
        missing_lines = "\n".join(f"- {page}" for page in missing)
        raise ValueError(f"Selected page(s) do not exist under repo root:\n{missing_lines}")
    return sorted(pages)


def plan_runs(
    *, pages: Sequence[str], agents: Sequence[str], provider: str, models: Sequence[str], output_root: Path
) -> list[PlannedRun]:
    combinations: Iterable[tuple[str, str, str]] = itertools.product(pages, agents, models)
    planned: list[PlannedRun] = []
    for index, (page, agent, model) in enumerate(combinations, start=1):
        output_path = output_path_for(output_root=output_root, page=page, agent=agent, provider=provider, model=model)
        planned.append(PlannedRun(index, page, agent, provider, model, output_path, log_path_for(output_path)))
    return planned


def current_rotation_index(seed: str) -> int:
    now = datetime.now(timezone.utc)
    if seed == "hourly":
        return int(now.timestamp() // 3600)
    if seed == "daily":
        return int(now.timestamp() // 86400)
    raise ValueError(f"Unsupported rotation seed: {seed}")


def select_runs(
    *,
    planned_runs: Sequence[PlannedRun],
    selection: str,
    max_runs: int | None,
    rotation_seed: str,
    rotation_index: int | None,
) -> tuple[list[PlannedRun], int | None]:
    if max_runs is not None and max_runs < 1:
        raise ValueError("--max-runs must be greater than 0 when provided.")
    if not planned_runs:
        return [], None

    selected_pool = list(planned_runs)
    applied_rotation_index: int | None = None
    if selection == "rotate":
        if rotation_index is not None and rotation_index < 0:
            raise ValueError("--rotation-index must be non-negative when provided.")
        applied_rotation_index = rotation_index if rotation_index is not None else current_rotation_index(rotation_seed)
        offset = applied_rotation_index % len(selected_pool)
        selected_pool = selected_pool[offset:] + selected_pool[:offset]
    elif selection != "first":
        raise ValueError(f"Unsupported selection mode: {selection}")

    if max_runs is not None:
        selected_pool = selected_pool[:max_runs]
    return selected_pool, applied_rotation_index


def run_subprocess(
    command: Sequence[str], repo_root: Path, *, environment: Mapping[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=environment,
    )


def is_rejected_check_output(result: subprocess.CompletedProcess[str]) -> bool:
    return result.returncode != 0 and CHECK_VALIDATION_FAILURE_MARKER in result.stderr


@dataclass(frozen=True)
class ProviderFailureClassification:
    kind: str
    message: str
    nonfatal_when_allowed: bool


NONFATAL_PROVIDER_FAILURE_KINDS = {"provider_unavailable", "empty_response"}


def explicit_provider_error_kind(stderr: str) -> str | None:
    match = re.search(r"provider_error_kind=([a-z_]+)", stderr.lower())
    return match.group(1) if match else None


def classify_provider_failure(result: subprocess.CompletedProcess[str]) -> ProviderFailureClassification | None:
    if result.returncode == 0:
        return None
    stderr = result.stderr.strip()
    if CHECK_VALIDATION_FAILURE_MARKER in stderr or "Provider call failed:" not in stderr:
        return None

    lower = stderr.lower()
    kind = explicit_provider_error_kind(lower)
    if kind is None:
        if any(
            marker in lower
            for marker in (
                "billing",
                "payment",
                "insufficient credit",
                "insufficient funds",
                "purchase",
                "paygo",
                "pay-as-you-go",
                "paid tier",
            )
        ):
            kind = "provider_policy_block"
        elif any(
            marker in lower
            for marker in (
                "429",
                "rate_limit",
                "rate limit",
                "quota",
                "resource_exhausted",
                "too many requests",
                "tpm",
                "rpm",
                "tokens per minute",
                "requests per day",
            )
        ):
            kind = "rate_or_quota_limited"
        elif any(
            marker in lower
            for marker in (
                "environment variable is not set",
                "invalid api key",
                "authentication",
                "unauthorized",
                "forbidden",
                "401",
                "403",
            )
        ):
            kind = "execution_configuration_block"
        elif any(
            marker in lower
            for marker in (
                "400",
                "404",
                "413",
                "422",
                "invalid request",
                "bad request",
                "not found",
                "request too large",
                "context length",
            )
        ):
            kind = "execution_configuration_block"
        elif "empty response" in lower:
            kind = "empty_response"
        elif any(
            marker in lower
            for marker in (
                "too busy",
                "busy",
                "overloaded",
                "capacity",
                "temporarily unavailable",
                "service_unavailable",
                "unavailable",
                "timeout",
                "timed out",
                "connection reset",
                "connection error",
                "500",
                "502",
                "503",
                "504",
            )
        ):
            kind = "provider_unavailable"
        else:
            kind = "unknown_provider_error"

    messages = {
        "provider_unavailable": (
            "Provider call failed. Reason: provider_unavailable. This usually indicates temporary provider-side "
            "load, outage, timeout, or capacity pressure."
        ),
        "empty_response": (
            "Provider call failed. Reason: empty_response. The provider returned no usable text; this is treated "
            "as provider-side noise when transient provider failures are allowed."
        ),
        "rate_or_quota_limited": (
            "Provider call failed. Reason: rate_or_quota_limited. Action required: reduce workflow frequency, "
            "reduce token usage, change model rotation, or adjust provider quota."
        ),
        "provider_policy_block": (
            "Provider call blocked. Reason: provider_policy_block. The selected capacity could not be proven free; "
            "no paid fallback is allowed."
        ),
        "execution_configuration_block": (
            "Provider call failed. Reason: execution_configuration_block. Action required: check repository secrets, "
            "API keys, provider access, or workflow configuration."
        ),
        "unknown_provider_error": (
            "Provider call failed. Reason: unknown_provider_error. Action required: inspect the per-run log stderr "
            "before suppressing this failure type."
        ),
    }
    return ProviderFailureClassification(
        kind=kind,
        message=messages.get(kind, messages["unknown_provider_error"]),
        nonfatal_when_allowed=kind in NONFATAL_PROVIDER_FAILURE_KINDS,
    )


def write_log(
    *,
    repo_root: Path,
    planned: PlannedRun,
    check_command: Sequence[str],
    check_result: subprocess.CompletedProcess[str] | None,
    issue_command: Sequence[str] | None,
    issue_result: subprocess.CompletedProcess[str] | None,
) -> None:
    log_file = filesystem_path(repo_root, planned.log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        f"# Batch log for run {planned.index}",
        "",
        f"Page: {planned.page}",
        f"Agent: {planned.agent}",
        f"Provider: {planned.provider}",
        f"Model: {planned.model}",
        f"Output: {planned.output_path.as_posix()}",
        "",
        "## run_check_agent.py",
        "",
        "Command:",
        "```text",
        " ".join(check_command),
        "```",
    ]
    if check_result is not None:
        lines.extend(
            [
                f"Exit code: {check_result.returncode}",
                "",
                "stdout:",
                "```text",
                check_result.stdout.rstrip(),
                "```",
                "",
                "stderr:",
                "```text",
                check_result.stderr.rstrip(),
                "```",
            ]
        )
    if issue_command is not None:
        lines.extend(["", "## issue_manager.py", "", "Command:", "```text", " ".join(issue_command), "```"])
    if issue_result is not None:
        lines.extend(
            [
                f"Exit code: {issue_result.returncode}",
                "",
                "stdout:",
                "```text",
                issue_result.stdout.rstrip(),
                "```",
                "",
                "stderr:",
                "```text",
                issue_result.stderr.rstrip(),
                "```",
            ]
        )
    log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def echo_child_output(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)


def build_check_command(*, planned: PlannedRun, max_completion_tokens: int | None) -> list[str]:
    command = [
        sys.executable,
        RUN_CHECK_AGENT_PATH.as_posix(),
        "--agent",
        planned.agent,
        "--page",
        planned.page,
        "--provider",
        planned.provider,
        "--model",
        planned.model,
        "--output",
        planned.output_path.as_posix(),
    ]
    if max_completion_tokens is not None:
        command.extend(["--max-completion-tokens", str(max_completion_tokens)])
    return command


def build_issue_command(
    *, planned: PlannedRun, mode: str, repo: str, post_empty: bool, task_id: str
) -> list[str] | None:
    if mode == "generate":
        return None
    command = [
        sys.executable,
        ISSUE_MANAGER_PATH.as_posix(),
        "--comment",
        planned.output_path.as_posix(),
        "--repo",
        repo,
        "--task-id",
        task_id,
    ]
    if mode == "dry-run":
        command.append("--dry-run")
    if post_empty:
        command.append("--post-empty")
    return command


def build_planned_task_id(
    *,
    planned: PlannedRun,
    repo_root: Path,
    max_completion_tokens: int | None,
) -> str:
    contract = AGENT_CONTRACTS[planned.agent]
    slot = require_executable_slot(
        planned.provider,
        planned.model,
        path=repo_root / DEFAULT_REGISTRY_PATH,
    )
    identity = build_task_identity(
        page=planned.page,
        agent=planned.agent,
        provider=planned.provider,
        model=planned.model,
        page_content=(repo_root / planned.page).read_text(encoding="utf-8"),
        prompt_id=contract.prompt_id,
        prompt_content=(repo_root / contract.prompt_path).read_text(encoding="utf-8"),
        slot=slot,
        max_completion_tokens=max_completion_tokens,
    )
    return task_id_for(identity)


def effective_quota_state(
    *,
    repo_root: Path,
    state_path: Path,
    event_directory: Path,
):
    registry = load_registry(repo_root / DEFAULT_REGISTRY_PATH)
    state = load_quota_state(filesystem_path(repo_root, state_path), registry)
    events = load_event_files(filesystem_path(repo_root, event_directory))
    if events:
        state, _ = aggregate_events(state, events, registry)
    return state


def pre_call_eligibility(
    *,
    planned: PlannedRun,
    repo_root: Path,
    max_completion_tokens: int | None,
    quota_state_path: Path,
    quota_event_directory: Path,
    resolver_work_pending: bool,
) -> tuple[bool, str]:
    task_id = build_planned_task_id(
        planned=planned,
        repo_root=repo_root,
        max_completion_tokens=max_completion_tokens,
    )
    state = effective_quota_state(
        repo_root=repo_root,
        state_path=quota_state_path,
        event_directory=quota_event_directory,
    )
    return slot_eligibility(
        state,
        provider=planned.provider,
        model=planned.model,
        task_id=task_id,
        resolver_work_pending=resolver_work_pending,
        now=datetime.now(timezone.utc),
    )


def run_one(
    *,
    planned: PlannedRun,
    repo_root: Path,
    mode: str,
    repo: str | None,
    post_empty: bool,
    max_completion_tokens: int | None,
    allow_rejected_check_outputs: bool,
    allow_provider_failures: bool,
) -> CompletedRun:
    try:
        task_id = build_planned_task_id(
            planned=planned,
            repo_root=repo_root,
            max_completion_tokens=max_completion_tokens,
        )
    except (OSError, ValueError) as exc:
        message = f"Could not construct content-addressed task identity: {exc}"
        print(f"ERROR: {message}", file=sys.stderr)
        return CompletedRun(
            planned,
            RUN_STATUS_FAILED,
            None,
            RUN_STATUS_SKIPPED,
            None,
            message,
        )
    filesystem_path(repo_root, planned.output_path).parent.mkdir(parents=True, exist_ok=True)
    check_command = build_check_command(planned=planned, max_completion_tokens=max_completion_tokens)
    print(f"[{planned.index}] {planned.agent} / {planned.provider} / {planned.model} / {planned.page}")
    check_environment = dict(os.environ)
    check_environment["PHASE2_TASK_ID"] = task_id
    check_result = run_subprocess(check_command, repo_root, environment=check_environment)
    echo_child_output(check_result)

    if check_result.returncode != 0:
        write_log(
            repo_root=repo_root,
            planned=planned,
            check_command=check_command,
            check_result=check_result,
            issue_command=None,
            issue_result=None,
        )
        if allow_rejected_check_outputs and is_rejected_check_output(check_result):
            warning = (
                "check-agent output was rejected by validation; treating as nonfatal and skipping issue_manager.py."
            )
            print(
                f"::warning title=Rejected check-agent output::{planned.agent} / {planned.provider} / {planned.model} / {planned.page}: {warning}",
                file=sys.stderr,
            )
            return CompletedRun(
                planned, RUN_STATUS_REJECTED, check_result.returncode, RUN_STATUS_SKIPPED, None, warning
            )

        provider_failure = classify_provider_failure(check_result)
        if provider_failure is not None:
            is_nonfatal = allow_provider_failures and provider_failure.nonfatal_when_allowed
            severity = "nonfatal" if is_nonfatal else "fatal"
            annotation = "warning" if is_nonfatal else "error"
            print(
                f"::{annotation} title=Provider failure ({severity}: {provider_failure.kind})::"
                f"{planned.agent} / {planned.provider} / {planned.model} / {planned.page}: {provider_failure.message}",
                file=sys.stderr,
            )
            return CompletedRun(
                planned,
                RUN_STATUS_PROVIDER_FAILED,
                check_result.returncode,
                RUN_STATUS_SKIPPED,
                None,
                provider_failure.message,
                provider_failure_is_nonfatal=is_nonfatal,
            )

        return CompletedRun(
            planned,
            RUN_STATUS_FAILED,
            check_result.returncode,
            RUN_STATUS_SKIPPED,
            None,
            "run_check_agent.py failed; issue_manager.py was not run.",
        )

    issue_command = build_issue_command(
        planned=planned,
        mode=mode,
        repo=repo or "",
        post_empty=post_empty,
        task_id=task_id,
    )
    issue_result = run_subprocess(issue_command, repo_root) if issue_command is not None else None
    if issue_result is not None:
        echo_child_output(issue_result)

    write_log(
        repo_root=repo_root,
        planned=planned,
        check_command=check_command,
        check_result=check_result,
        issue_command=issue_command,
        issue_result=issue_result,
    )

    if issue_result is not None and issue_result.returncode != 0:
        return CompletedRun(
            planned,
            RUN_STATUS_OK,
            check_result.returncode,
            RUN_STATUS_FAILED,
            issue_result.returncode,
            "issue_manager.py failed.",
        )

    return CompletedRun(
        planned,
        RUN_STATUS_OK,
        check_result.returncode,
        RUN_STATUS_OK if issue_command is not None else RUN_STATUS_SKIPPED,
        issue_result.returncode if issue_result is not None else None,
        "completed successfully.",
    )


def markdown_escape(value: object) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|").replace("\n", " ")


def summarize_completed_runs(completed_runs: Sequence[CompletedRun]) -> tuple[int, int, int, int]:
    accepted_count = sum(
        1 for run in completed_runs if run.check_status == RUN_STATUS_OK and run.issue_status != RUN_STATUS_FAILED
    )
    rejected_count = sum(1 for run in completed_runs if run.rejected)
    provider_failure_count = sum(1 for run in completed_runs if run.provider_failed)
    fatal_failure_count = sum(1 for run in completed_runs if run.fatal_failed)
    return accepted_count, rejected_count, provider_failure_count, fatal_failure_count


def status_for_summary(completed: CompletedRun | None, plan_only: bool) -> tuple[str, str]:
    if completed is None:
        return (RUN_STATUS_SKIPPED if plan_only else "not-run"), ("planned only" if plan_only else "not executed")
    if completed.fatal_failed:
        return RUN_STATUS_FAILED, completed.message
    return completed.check_status, completed.message


def write_summary(
    *,
    summary_path: Path,
    repo_root: Path,
    mode: str,
    selection: str,
    rotation_seed: str,
    applied_rotation_index: int | None,
    available_run_count: int,
    planned_runs: Sequence[PlannedRun],
    completed_runs: Sequence[CompletedRun],
    plan_only: bool,
) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    accepted_count, rejected_count, provider_failure_count, fatal_failure_count = summarize_completed_runs(
        completed_runs
    )
    lines: list[str] = [
        "# Phase 2 check batch summary",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        f"Repository root: `{repo_root}`",
        f"Mode: `{mode}`",
        f"Selection: `{selection}`",
        f"Rotation seed: `{rotation_seed}`",
        "Rotation index: " + (f"`{applied_rotation_index}`" if applied_rotation_index is not None else "`n/a`"),
        f"Plan only: `{str(plan_only).lower()}`",
        f"Available runs: `{available_run_count}`",
        f"Selected/planned runs: `{len(planned_runs)}`",
        f"Completed runs: `{len(completed_runs)}`",
        f"Accepted runs: `{accepted_count}`",
        f"Rejected check-agent outputs: `{rejected_count}`",
        f"Provider failed runs: `{provider_failure_count}`",
        f"Fatal failed runs: `{fatal_failure_count}`",
        "",
        "## Runs",
        "",
        "| # | Status | Check status | Issue status | Page | Agent | Provider | Model | Output | Log | Message |",
        "|---:|---|---|---|---|---|---|---|---|---|---|",
    ]
    completed_by_index = {run.planned.index: run for run in completed_runs}
    for planned in planned_runs:
        completed = completed_by_index.get(planned.index)
        status, message = status_for_summary(completed, plan_only)
        check_status = completed.check_status if completed is not None else status
        issue_status = completed.issue_status if completed is not None else status
        lines.append(
            "| "
            + " | ".join(
                [
                    str(planned.index),
                    f"`{markdown_escape(status)}`",
                    f"`{markdown_escape(check_status)}`",
                    f"`{markdown_escape(issue_status)}`",
                    f"`{markdown_escape(planned.page)}`",
                    f"`{markdown_escape(planned.agent)}`",
                    f"`{markdown_escape(planned.provider)}`",
                    f"`{markdown_escape(planned.model)}`",
                    f"`{markdown_escape(planned.output_path.as_posix())}`",
                    f"`{markdown_escape(planned.log_path.as_posix())}`",
                    markdown_escape(message),
                ]
            )
            + " |"
        )
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_environment(repo_root: Path, mode: str, repo: str | None) -> None:
    if not repo_root.is_dir():
        raise ValueError(f"Repository root does not exist or is not a directory: {repo_root}")
    if not (repo_root / RUN_CHECK_AGENT_PATH).is_file():
        raise ValueError(f"Missing required script: {RUN_CHECK_AGENT_PATH}")
    if mode in {"dry-run", "post"}:
        if not repo:
            raise ValueError("--repo is required for --mode dry-run or --mode post.")
        if not (repo_root / ISSUE_MANAGER_PATH).is_file():
            raise ValueError(f"Missing required script: {ISSUE_MANAGER_PATH}")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    output_root = Path(args.output_root)
    summary_path = (
        (repo_root / args.summary).resolve()
        if args.summary
        else filesystem_path(repo_root, output_root) / SUMMARY_FILENAME
    )

    try:
        validate_environment(repo_root, args.mode, args.repo)
        pages = discover_pages(repo_root, args.page, args.pages_glob, args.exclude_page, args.exclude_pages_glob)
        agents = args.agent or DEFAULT_AGENTS
        models = args.model
        if not models:
            raise ValueError("At least one --model must be provided.")
        provider = args.provider.strip().lower()
        registry_path = repo_root / DEFAULT_REGISTRY_PATH
        for model in models:
            configured_slot = require_executable_slot(provider, model, path=registry_path)
            if args.max_completion_tokens is not None:
                validate_completion_token_cap(configured_slot, args.max_completion_tokens)
        available_runs = plan_runs(
            pages=pages, agents=agents, provider=provider, models=models, output_root=output_root
        )
        planned_runs, applied_rotation_index = select_runs(
            planned_runs=available_runs,
            selection=args.selection,
            max_runs=args.max_runs,
            rotation_seed=args.rotation_seed,
            rotation_index=args.rotation_index,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Available runs: {len(available_runs)}")
    print(f"Selected runs: {len(planned_runs)}")
    print(f"Selection: {args.selection}")
    if applied_rotation_index is not None:
        print(f"Rotation seed: {args.rotation_seed}")
        print(f"Rotation index: {applied_rotation_index}")
    for planned in planned_runs:
        print(
            f"- [{planned.index}] {planned.agent} / {planned.provider} / {planned.model} / {planned.page} -> {planned.output_path.as_posix()}"
        )

    completed_runs: list[CompletedRun] = []
    if args.plan_only:
        write_summary(
            summary_path=summary_path,
            repo_root=repo_root,
            mode=args.mode,
            selection=args.selection,
            rotation_seed=args.rotation_seed,
            applied_rotation_index=applied_rotation_index,
            available_run_count=len(available_runs),
            planned_runs=planned_runs,
            completed_runs=completed_runs,
            plan_only=True,
        )
        print(f"Wrote batch summary to: {summary_path}")
        return 0

    for run_number, planned in enumerate(planned_runs, start=1):
        quota_event_directory = Path(os.getenv("PHASE2_QUOTA_EVENT_DIR", str(DEFAULT_EVENT_DIRECTORY)))
        try:
            eligible, eligibility_reason = pre_call_eligibility(
                planned=planned,
                repo_root=repo_root,
                max_completion_tokens=args.max_completion_tokens,
                quota_state_path=Path(args.quota_state),
                quota_event_directory=quota_event_directory,
                resolver_work_pending=args.resolver_work_pending,
            )
        except (OSError, QuotaStateError, ValueError) as exc:
            print(f"ERROR: Could not evaluate pre-call quota eligibility: {exc}", file=sys.stderr)
            return 2
        if not eligible:
            message = f"provider call withheld by quota/runtime guard: {eligibility_reason}."
            print(f"[{planned.index}] Skipped: {message}")
            completed_runs.append(
                CompletedRun(
                    planned,
                    RUN_STATUS_SKIPPED,
                    None,
                    RUN_STATUS_SKIPPED,
                    None,
                    message,
                )
            )
            continue
        completed = run_one(
            planned=planned,
            repo_root=repo_root,
            mode=args.mode,
            repo=args.repo,
            post_empty=args.post_empty,
            max_completion_tokens=args.max_completion_tokens,
            allow_rejected_check_outputs=args.allow_rejected_check_outputs,
            allow_provider_failures=args.allow_provider_failures,
        )
        completed_runs.append(completed)
        if args.fail_fast and completed.fatal_failed:
            print("Stopping after first fatal failed run because --fail-fast was set.")
            break
        if run_number < len(planned_runs) and args.sleep_seconds > 0:
            print(f"Sleeping for {args.sleep_seconds:g} seconds before next run...")
            time.sleep(args.sleep_seconds)

    write_summary(
        summary_path=summary_path,
        repo_root=repo_root,
        mode=args.mode,
        selection=args.selection,
        rotation_seed=args.rotation_seed,
        applied_rotation_index=applied_rotation_index,
        available_run_count=len(available_runs),
        planned_runs=planned_runs,
        completed_runs=completed_runs,
        plan_only=False,
    )
    print(f"Wrote batch summary to: {summary_path}")

    fatal_failures = [completed for completed in completed_runs if completed.fatal_failed]
    if fatal_failures:
        print(f"Batch completed with {len(fatal_failures)} fatal failed run(s).", file=sys.stderr)
        return 1

    nonfatal_rejected = [completed for completed in completed_runs if completed.rejected]
    nonfatal_provider_failures = [
        completed
        for completed in completed_runs
        if completed.provider_failed and completed.provider_failure_is_nonfatal
    ]
    if nonfatal_rejected or nonfatal_provider_failures:
        print(
            f"Batch completed successfully with {len(nonfatal_rejected)} nonfatal rejected output(s) "
            f"and {len(nonfatal_provider_failures)} nonfatal provider failure(s).",
            file=sys.stderr,
        )
        return 0

    print("Batch completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
