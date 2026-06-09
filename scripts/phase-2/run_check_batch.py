#!/usr/bin/env python3
"""Run Phase 2 LLM check agents across pages, agents, and models.

This batch runner is intentionally conservative:

- it delegates each individual LLM call and output validation to
  `scripts/phase-2/run_check_agent.py`;
- it can optionally delegate issue dry-runs or posting to
  `scripts/phase-2/issue_manager.py`;
- it derives stable output paths under `.tmp/phase-2`;
- it continues after individual failures so one bad page/model does not hide
  the rest of the batch;
- it writes a Markdown batch summary;
- it exits nonzero when any individual run fails.

Default behavior is local generation only. GitHub is touched only when
`--mode post` is explicitly selected.
"""

from __future__ import annotations

import argparse
import itertools
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_AGENTS = ["page-hygiene-checker", "language-style-checker"]
DEFAULT_PROVIDER = "groq"
DEFAULT_MODELS = ["llama-3.3-70b-versatile"]
DEFAULT_OUTPUT_ROOT = Path(".tmp/phase-2")
DEFAULT_SLEEP_SECONDS = 30.0
SUMMARY_FILENAME = "batch-summary.md"

RUN_CHECK_AGENT_PATH = Path("scripts/phase-2/run_check_agent.py")
ISSUE_MANAGER_PATH = Path("scripts/phase-2/issue_manager.py")

RUN_STATUS_OK = "ok"
RUN_STATUS_FAILED = "failed"
RUN_STATUS_SKIPPED = "skipped"


@dataclass(frozen=True)
class PlannedRun:
    """One page-agent-provider-model combination to execute."""

    index: int
    page: str
    agent: str
    provider: str
    model: str
    output_path: Path
    log_path: Path


def filesystem_path(repo_root: Path, path: Path) -> Path:
    """Resolve a possibly repo-relative path to an absolute filesystem path."""
    return path if path.is_absolute() else repo_root / path


@dataclass(frozen=True)
class CompletedRun:
    """Result of one planned run."""

    planned: PlannedRun
    check_status: str
    check_exit_code: int | None
    issue_status: str
    issue_exit_code: int | None
    message: str

    @property
    def succeeded(self) -> bool:
        if self.check_status != RUN_STATUS_OK:
            return False
        if self.issue_status == RUN_STATUS_FAILED:
            return False
        return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Phase 2 check agents across pages, agents, and models."
    )

    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root. Defaults to the current working directory.",
    )

    parser.add_argument(
        "--page",
        action="append",
        default=[],
        help=(
            "Repository-relative Markdown page to check. May be passed multiple "
            "times."
        ),
    )

    parser.add_argument(
        "--pages-glob",
        action="append",
        default=[],
        help=(
            "Repository-relative glob for Markdown pages, for example "
            '"docs/stereotypes/**/*.md". May be passed multiple times.'
        ),
    )

    parser.add_argument(
        "--agent",
        action="append",
        default=[],
        choices=DEFAULT_AGENTS,
        help=(
            "Check agent to run. May be passed multiple times. Defaults to both "
            "LLM-based Phase 2 agents."
        ),
    )

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        help=f"LLM provider to use. Defaults to {DEFAULT_PROVIDER!r}.",
    )

    parser.add_argument(
        "--model",
        action="append",
        default=[],
        help=(
            "Model to use. May be passed multiple times. Defaults to "
            f"{DEFAULT_MODELS[0]!r}."
        ),
    )

    parser.add_argument(
        "--mode",
        choices=["generate", "dry-run", "post"],
        default="generate",
        help=(
            "Batch mode. 'generate' only writes comment files. 'dry-run' also "
            "runs issue_manager.py --dry-run for valid outputs. 'post' also "
            "runs issue_manager.py without --dry-run. Defaults to 'generate'."
        ),
    )

    parser.add_argument(
        "--repo",
        help=(
            "GitHub repository full name, required for --mode dry-run or --mode "
            "post, for example pedropaulofb/ontouml-according-to-the-machines."
        ),
    )

    parser.add_argument(
        "--post-empty",
        action="store_true",
        help="Forward --post-empty to issue_manager.py in dry-run or post mode.",
    )

    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help=f"Root directory for generated comments. Defaults to {DEFAULT_OUTPUT_ROOT}.",
    )

    parser.add_argument(
        "--summary",
        help=(
            "Path for the Markdown batch summary. Defaults to "
            ".tmp/phase-2/batch-summary.md under --repo-root."
        ),
    )

    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=DEFAULT_SLEEP_SECONDS,
        help=(
            "Seconds to sleep between individual LLM calls. Defaults to "
            f"{DEFAULT_SLEEP_SECONDS:g}. Use 0 for no delay."
        ),
    )

    parser.add_argument(
        "--max-runs",
        type=int,
        help=(
            "Maximum number of planned combinations to execute. Useful for "
            "conservative scheduled batches. Omit for no limit."
        ),
    )

    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop after the first failed individual run.",
    )

    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Print and summarize the planned runs without executing them.",
    )

    parser.add_argument(
        "--max-completion-tokens",
        type=int,
        help="Forward --max-completion-tokens to run_check_agent.py when set.",
    )

    return parser.parse_args()


def normalize_repo_relative_path(path_value: str) -> str:
    """Normalize a user-supplied page path to POSIX-style repo-relative text."""
    return Path(path_value).as_posix().lstrip("./")


def safe_slug(value: str) -> str:
    """Convert a provider, model, or page identity to a filename-safe slug."""
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "unnamed"


def page_identity(page: str) -> str:
    """Return the stereotype-page identity used in output directories."""
    normalized = normalize_repo_relative_path(page)
    prefix = "docs/stereotypes/"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix) :]
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return normalized


def output_path_for(
    *,
    output_root: Path,
    page: str,
    agent: str,
    provider: str,
    model: str,
) -> Path:
    """Derive the batch output path for one planned run."""
    page_dir = safe_slug(page_identity(page).replace("/", "-"))
    provider_slug = safe_slug(provider)
    model_slug = safe_slug(model)
    return output_root / agent / page_dir / f"issue-comment-{provider_slug}-{model_slug}.md"


def log_path_for(output_path: Path) -> Path:
    """Derive the per-run batch log path for one output file."""
    return output_path.with_suffix(".batch.log")


def discover_pages(repo_root: Path, explicit_pages: Sequence[str], globs: Sequence[str]) -> list[str]:
    """Resolve explicit pages and globbed pages to sorted repo-relative paths."""
    pages: set[str] = set()

    for page in explicit_pages:
        normalized = normalize_repo_relative_path(page)
        if not normalized.endswith(".md"):
            raise ValueError(f"Page is not a Markdown file: {page}")
        pages.add(normalized)

    for pattern in globs:
        matches = sorted(repo_root.glob(pattern))
        for match in matches:
            if match.is_file() and match.suffix == ".md":
                pages.add(match.relative_to(repo_root).as_posix())

    if not pages:
        raise ValueError("No pages selected. Pass --page and/or --pages-glob.")

    missing = [page for page in sorted(pages) if not (repo_root / page).is_file()]
    if missing:
        missing_lines = "\n".join(f"- {page}" for page in missing)
        raise ValueError(f"Selected page(s) do not exist under repo root:\n{missing_lines}")

    return sorted(pages)


def plan_runs(
    *,
    repo_root: Path,
    pages: Sequence[str],
    agents: Sequence[str],
    provider: str,
    models: Sequence[str],
    output_root: Path,
    max_runs: int | None,
) -> list[PlannedRun]:
    """Create the cross product of pages, agents, provider, and models."""
    if max_runs is not None and max_runs < 1:
        raise ValueError("--max-runs must be greater than 0 when provided.")

    combinations: Iterable[tuple[str, str, str]] = itertools.product(pages, agents, models)
    planned: list[PlannedRun] = []

    for index, (page, agent, model) in enumerate(combinations, start=1):
        if max_runs is not None and len(planned) >= max_runs:
            break

        output_path = output_path_for(
            output_root=output_root,
            page=page,
            agent=agent,
            provider=provider,
            model=model,
        )
        planned.append(
            PlannedRun(
                index=index,
                page=page,
                agent=agent,
                provider=provider,
                model=model,
                output_path=output_path,
                log_path=log_path_for(output_path),
            )
        )

    return planned


def run_subprocess(command: Sequence[str], repo_root: Path) -> subprocess.CompletedProcess[str]:
    """Run a child command from the repository root and capture output."""
    return subprocess.run(
        list(command),
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
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
    """Write per-run command details, stdout, and stderr."""
    log_file = filesystem_path(repo_root, planned.log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# Batch log for run {planned.index}")
    lines.append("")
    lines.append(f"Page: {planned.page}")
    lines.append(f"Agent: {planned.agent}")
    lines.append(f"Provider: {planned.provider}")
    lines.append(f"Model: {planned.model}")
    lines.append(f"Output: {planned.output_path.as_posix()}")
    lines.append("")
    lines.append("## run_check_agent.py")
    lines.append("")
    lines.append("Command:")
    lines.append("```text")
    lines.append(" ".join(check_command))
    lines.append("```")

    if check_result is not None:
        lines.append(f"Exit code: {check_result.returncode}")
        lines.append("")
        lines.append("stdout:")
        lines.append("```text")
        lines.append(check_result.stdout.rstrip())
        lines.append("```")
        lines.append("")
        lines.append("stderr:")
        lines.append("```text")
        lines.append(check_result.stderr.rstrip())
        lines.append("```")

    if issue_command is not None:
        lines.append("")
        lines.append("## issue_manager.py")
        lines.append("")
        lines.append("Command:")
        lines.append("```text")
        lines.append(" ".join(issue_command))
        lines.append("```")

    if issue_result is not None:
        lines.append(f"Exit code: {issue_result.returncode}")
        lines.append("")
        lines.append("stdout:")
        lines.append("```text")
        lines.append(issue_result.stdout.rstrip())
        lines.append("```")
        lines.append("")
        lines.append("stderr:")
        lines.append("```text")
        lines.append(issue_result.stderr.rstrip())
        lines.append("```")

    log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def echo_child_output(result: subprocess.CompletedProcess[str]) -> None:
    """Echo captured child-process output to the batch runner console."""
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)


def build_check_command(
    *,
    planned: PlannedRun,
    max_completion_tokens: int | None,
) -> list[str]:
    """Build the run_check_agent.py command for one planned run."""
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
    *,
    planned: PlannedRun,
    mode: str,
    repo: str,
    post_empty: bool,
) -> list[str] | None:
    """Build the issue_manager.py command for one successful planned run."""
    if mode == "generate":
        return None

    command = [
        sys.executable,
        ISSUE_MANAGER_PATH.as_posix(),
        "--comment",
        planned.output_path.as_posix(),
        "--repo",
        repo,
    ]
    if mode == "dry-run":
        command.append("--dry-run")
    if post_empty:
        command.append("--post-empty")
    return command


def run_one(
    *,
    planned: PlannedRun,
    repo_root: Path,
    mode: str,
    repo: str | None,
    post_empty: bool,
    max_completion_tokens: int | None,
) -> CompletedRun:
    """Execute one planned run and return its status."""
    filesystem_path(repo_root, planned.output_path).parent.mkdir(parents=True, exist_ok=True)

    check_command = build_check_command(
        planned=planned,
        max_completion_tokens=max_completion_tokens,
    )
    print(
        f"[{planned.index}] {planned.agent} / {planned.provider} / "
        f"{planned.model} / {planned.page}"
    )
    check_result = run_subprocess(check_command, repo_root)
    echo_child_output(check_result)

    issue_command: list[str] | None = None
    issue_result: subprocess.CompletedProcess[str] | None = None

    if check_result.returncode != 0:
        write_log(
            repo_root=repo_root,
            planned=planned,
            check_command=check_command,
            check_result=check_result,
            issue_command=None,
            issue_result=None,
        )
        return CompletedRun(
            planned=planned,
            check_status=RUN_STATUS_FAILED,
            check_exit_code=check_result.returncode,
            issue_status=RUN_STATUS_SKIPPED,
            issue_exit_code=None,
            message="run_check_agent.py failed; issue_manager.py was not run.",
        )

    issue_command = build_issue_command(
        planned=planned,
        mode=mode,
        repo=repo or "",
        post_empty=post_empty,
    )

    if issue_command is not None:
        issue_result = run_subprocess(issue_command, repo_root)
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
            planned=planned,
            check_status=RUN_STATUS_OK,
            check_exit_code=check_result.returncode,
            issue_status=RUN_STATUS_FAILED,
            issue_exit_code=issue_result.returncode,
            message="issue_manager.py failed.",
        )

    return CompletedRun(
        planned=planned,
        check_status=RUN_STATUS_OK,
        check_exit_code=check_result.returncode,
        issue_status=RUN_STATUS_OK if issue_command is not None else RUN_STATUS_SKIPPED,
        issue_exit_code=issue_result.returncode if issue_result is not None else None,
        message="completed successfully.",
    )


def markdown_escape(value: object) -> str:
    """Escape table-sensitive characters for Markdown summary cells."""
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def write_summary(
    *,
    summary_path: Path,
    repo_root: Path,
    mode: str,
    planned_runs: Sequence[PlannedRun],
    completed_runs: Sequence[CompletedRun],
    plan_only: bool,
) -> None:
    """Write a Markdown batch summary."""
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    success_count = sum(1 for run in completed_runs if run.succeeded)
    failure_count = sum(1 for run in completed_runs if not run.succeeded)

    lines: list[str] = []
    lines.append("# Phase 2 check batch summary")
    lines.append("")
    lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Repository root: `{repo_root}`")
    lines.append(f"Mode: `{mode}`")
    lines.append(f"Plan only: `{str(plan_only).lower()}`")
    lines.append(f"Planned runs: `{len(planned_runs)}`")
    lines.append(f"Completed runs: `{len(completed_runs)}`")
    lines.append(f"Successful runs: `{success_count}`")
    lines.append(f"Failed runs: `{failure_count}`")
    lines.append("")
    lines.append("## Runs")
    lines.append("")
    lines.append(
        "| # | Status | Page | Agent | Provider | Model | Output | Log | Message |"
    )
    lines.append("|---:|---|---|---|---|---|---|---|---|")

    completed_by_index = {run.planned.index: run for run in completed_runs}
    for planned in planned_runs:
        completed = completed_by_index.get(planned.index)
        if completed is None:
            status = RUN_STATUS_SKIPPED if plan_only else "not-run"
            message = "planned only" if plan_only else "not executed"
        else:
            status = RUN_STATUS_OK if completed.succeeded else RUN_STATUS_FAILED
            message = completed.message

        lines.append(
            "| "
            + " | ".join(
                [
                    str(planned.index),
                    f"`{markdown_escape(status)}`",
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
    """Validate required files and mode-specific arguments."""
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
        pages = discover_pages(repo_root, args.page, args.pages_glob)
        agents = args.agent or DEFAULT_AGENTS
        models = args.model or DEFAULT_MODELS
        planned_runs = plan_runs(
            repo_root=repo_root,
            pages=pages,
            agents=agents,
            provider=args.provider,
            models=models,
            output_root=output_root,
            max_runs=args.max_runs,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Planned runs: {len(planned_runs)}")
    for planned in planned_runs:
        print(
            f"- [{planned.index}] {planned.agent} / {planned.provider} / "
            f"{planned.model} / {planned.page} -> {planned.output_path.as_posix()}"
        )

    completed_runs: list[CompletedRun] = []

    if args.plan_only:
        write_summary(
            summary_path=summary_path,
            repo_root=repo_root,
            mode=args.mode,
            planned_runs=planned_runs,
            completed_runs=completed_runs,
            plan_only=True,
        )
        print(f"Wrote batch summary to: {summary_path}")
        return 0

    for run_number, planned in enumerate(planned_runs, start=1):
        completed = run_one(
            planned=planned,
            repo_root=repo_root,
            mode=args.mode,
            repo=args.repo,
            post_empty=args.post_empty,
            max_completion_tokens=args.max_completion_tokens,
        )
        completed_runs.append(completed)

        if args.fail_fast and not completed.succeeded:
            print("Stopping after first failed run because --fail-fast was set.")
            break

        if run_number < len(planned_runs) and args.sleep_seconds > 0:
            print(f"Sleeping for {args.sleep_seconds:g} seconds before next run...")
            time.sleep(args.sleep_seconds)

    write_summary(
        summary_path=summary_path,
        repo_root=repo_root,
        mode=args.mode,
        planned_runs=planned_runs,
        completed_runs=completed_runs,
        plan_only=False,
    )
    print(f"Wrote batch summary to: {summary_path}")

    failures = [completed for completed in completed_runs if not completed.succeeded]
    if failures:
        print(f"Batch completed with {len(failures)} failed run(s).", file=sys.stderr)
        return 1

    print("Batch completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
