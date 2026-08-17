#!/usr/bin/env python3
"""Apply an idempotent Phase 2 state mutation and push it with bounded retries."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


class StateWriterError(RuntimeError):
    """Raised when a deterministic operational-state write cannot be completed."""


@dataclass(frozen=True)
class StateWriteResult:
    commit_sha: str
    attempts: int
    changed: bool


Runner = Callable[..., subprocess.CompletedProcess[str]]


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    runner: Runner,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = runner(
        list(command),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        diagnostic = (completed.stderr or completed.stdout or "command failed").strip()
        raise StateWriterError(f"State-writer command failed: {' '.join(command[:3])}: {diagnostic}")
    return completed


def _format_apply_command(command: Sequence[str], worktree: Path) -> list[str]:
    return [part.replace("{worktree}", str(worktree)) for part in command]


def _export_path(worktree: Path, relative_source: str, destination: Path) -> None:
    source = worktree / relative_source
    if not source.exists():
        raise StateWriterError(f"Requested state-writer export does not exist: {relative_source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        shutil.copy2(source, destination)


def _write_sha(path: Path | None, sha: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(f"{sha}\n", encoding="utf-8")
    os.replace(temporary, path)


def run_state_write(
    *,
    repo_root: Path,
    branch: str,
    remote: str,
    push_url: str,
    commit_message: str,
    add_paths: Sequence[str],
    apply_command: Sequence[str],
    max_attempts: int = 3,
    exports: Sequence[tuple[str, Path]] = (),
    sha_output: Path | None = None,
    runner: Runner = subprocess.run,
) -> StateWriteResult:
    """Reapply one deterministic mutation to the latest branch until its push succeeds."""
    if not branch.strip() or not push_url.strip() or not commit_message.strip():
        raise StateWriterError("Branch, push URL, and commit message must be non-empty.")
    if not add_paths or not apply_command or max_attempts < 1:
        raise StateWriterError("State writes require staged paths, an apply command, and at least one attempt.")

    worktree_root = Path(tempfile.mkdtemp(prefix="phase-2-state-writer-"))
    try:
        for attempt in range(1, max_attempts + 1):
            worktree = worktree_root / f"attempt-{attempt}"
            _run(["git", "fetch", remote, branch], cwd=repo_root, runner=runner)
            _run(
                ["git", "worktree", "add", "--detach", str(worktree), f"{remote}/{branch}"],
                cwd=repo_root,
                runner=runner,
            )
            try:
                applied = _run(_format_apply_command(apply_command, worktree), cwd=worktree, runner=runner)
                if applied.stdout:
                    print(applied.stdout, end="")
                if applied.stderr:
                    print(applied.stderr, end="", file=sys.stderr)

                _run(["git", "add", "--", *add_paths], cwd=worktree, runner=runner)
                changed_result = _run(
                    ["git", "diff", "--cached", "--quiet"],
                    cwd=worktree,
                    runner=runner,
                    check=False,
                )
                if changed_result.returncode not in {0, 1}:
                    raise StateWriterError("Could not inspect staged operational-state changes.")
                changed = changed_result.returncode == 1
                if changed:
                    _run(["git", "config", "user.name", "github-actions[bot]"], cwd=worktree, runner=runner)
                    _run(
                        [
                            "git",
                            "config",
                            "user.email",
                            "41898282+github-actions[bot]@users.noreply.github.com",
                        ],
                        cwd=worktree,
                        runner=runner,
                    )
                    _run(["git", "commit", "-m", commit_message], cwd=worktree, runner=runner)

                sha = _run(["git", "rev-parse", "HEAD"], cwd=worktree, runner=runner).stdout.strip()
                if changed:
                    pushed = _run(
                        ["git", "push", push_url, f"HEAD:{branch}"],
                        cwd=worktree,
                        runner=runner,
                        check=False,
                    )
                    if pushed.returncode != 0:
                        if attempt == max_attempts:
                            raise StateWriterError(
                                f"Operational-state push failed after {max_attempts} bounded attempts."
                            )
                        print(
                            "Operational-state push conflicted; reapplying the same mutation to the latest branch.",
                            file=sys.stderr,
                        )
                        continue

                for relative_source, destination in exports:
                    _export_path(worktree, relative_source, destination)
                _write_sha(sha_output, sha)
                return StateWriteResult(commit_sha=sha, attempts=attempt, changed=changed)
            finally:
                _run(
                    ["git", "worktree", "remove", "--force", str(worktree)],
                    cwd=repo_root,
                    runner=runner,
                    check=False,
                )
        raise StateWriterError("Operational-state write exhausted its retry loop.")
    finally:
        _run(["git", "worktree", "prune"], cwd=repo_root, runner=runner, check=False)
        shutil.rmtree(worktree_root, ignore_errors=True)


def _parse_export(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("--export must use RELATIVE_SOURCE=DESTINATION.")
    source, destination = value.split("=", 1)
    if not source.strip() or not destination.strip():
        raise argparse.ArgumentTypeError("--export source and destination must be non-empty.")
    return source.strip(), Path(destination).resolve()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply and push one deterministic Phase 2 state mutation.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--push-url-env", default="PHASE2_PUSH_URL")
    parser.add_argument("--commit-message", required=True)
    parser.add_argument("--add", action="append", required=True, dest="add_paths")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--export", action="append", default=[], type=_parse_export)
    parser.add_argument("--sha-output")
    parser.add_argument("apply_command", nargs=argparse.REMAINDER)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    apply_command = list(args.apply_command)
    if apply_command and apply_command[0] == "--":
        apply_command.pop(0)
    try:
        push_url = os.getenv(args.push_url_env, "")
        result = run_state_write(
            repo_root=Path(args.repo_root).resolve(),
            branch=args.branch,
            remote=args.remote,
            push_url=push_url,
            commit_message=args.commit_message,
            add_paths=args.add_paths,
            apply_command=apply_command,
            max_attempts=args.max_attempts,
            exports=args.export,
            sha_output=Path(args.sha_output).resolve() if args.sha_output else None,
        )
        print(
            f"Phase 2 state write: commit_sha={result.commit_sha}; attempts={result.attempts}; "
            f"changed={str(result.changed).lower()}."
        )
        return 0
    except (OSError, StateWriterError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
