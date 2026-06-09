#!/usr/bin/env python3
"""Run page-structure-checker once across all canonical stereotype pages.

This is a one-time local runner for the deterministic Phase 2
page-structure-checker.

Default behavior:
- finds all Markdown files under docs/stereotypes/classes/ and docs/stereotypes/relations/;
- runs scripts/phase-2/check_agents/page_structure_checker.py for each page;
- writes one issue-comment Markdown file per page under .tmp/phase-2/page-structure-checker/;
- prints a summary;
- does not create GitHub issues unless --post is passed.

When --post is passed:
- posts only reports with Signal count > 0;
- uses scripts/phase-2/issue_manager.py;
- skips reports with Signal count = 0 to avoid issue/comment noise.

When --issue-dry-run is passed with --post:
- generates real checker outputs;
- calls issue_manager.py with --dry-run;
- does not create GitHub issues or comments.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPO = "pedropaulofb/ontouml-according-to-the-machines"
DEFAULT_OUTPUT_DIR = ".tmp/phase-2/page-structure-checker"

PAGE_PATTERNS = (
    "docs/stereotypes/classes/*.md",
    "docs/stereotypes/relations/*.md",
)

SIGNAL_COUNT_PATTERN = re.compile(
    r"^\|\s*Signal count\s*\|\s*(?P<count>\d+)\s*\|\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class PageRunResult:
    page: str
    output_path: Path
    checker_return_code: int
    signal_count: int | None
    issue_manager_return_code: int | None
    issue_manager_mode: str


class PageStructureBatchError(RuntimeError):
    """Raised when the one-time page-structure batch cannot proceed."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run page-structure-checker once across all stereotype pages."
    )

    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"GitHub repository used by issue_manager.py. Default: {DEFAULT_REPO}",
    )

    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for generated issue-comment files. Default: {DEFAULT_OUTPUT_DIR}",
    )

    parser.add_argument(
        "--post",
        action="store_true",
        help=(
            "Post generated comments with Signal count > 0 using issue_manager.py. "
            "Requires GitHub CLI authentication unless --issue-dry-run is also used."
        ),
    )

    parser.add_argument(
        "--issue-dry-run",
        action="store_true",
        help=(
            "With --post, generate checker outputs and call issue_manager.py with "
            "--dry-run instead of creating GitHub issues or comments."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Print planned checker commands without executing them. This mode does "
            "not generate output files and does not call issue_manager.py."
        ),
    )

    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help=(
            "Optional GitHub issue label to pass to issue_manager.py when creating issues. "
            "May be repeated."
        ),
    )

    parser.add_argument(
        "--max-signals",
        type=int,
        default=3,
        help="Maximum number of structural signals per page. Default: 3.",
    )

    parser.add_argument(
        "--only-page",
        default=None,
        help=(
            "Optional repository-relative page path to process only one page, "
            "useful for testing."
        ),
    )

    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue processing remaining pages if one checker or posting command fails.",
    )

    return parser.parse_args()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def discover_pages(repo_root: Path, only_page: str | None) -> list[str]:
    if only_page:
        page = normalize_path(only_page)
        path = repo_root / page
        if not path.is_file():
            raise PageStructureBatchError(f"Selected page does not exist: {page}")
        return [page]

    pages: list[str] = []

    for pattern in PAGE_PATTERNS:
        for path in repo_root.glob(pattern):
            if path.is_file() and path.name != "index.md":
                pages.append(path.relative_to(repo_root).as_posix())

    pages = sorted(set(pages))

    if not pages:
        raise PageStructureBatchError(
            "No stereotype pages found under docs/stereotypes/classes/ or docs/stereotypes/relations/."
        )

    return pages


def page_identity(page: str) -> str:
    normalized = normalize_path(page)

    if normalized.startswith("docs/stereotypes/"):
        normalized = normalized[len("docs/stereotypes/") :]

    if normalized.endswith(".md"):
        normalized = normalized[:-3]

    return normalized.replace("/", "-")


def issue_comment_path(output_dir: Path, page: str) -> Path:
    return output_dir / page_identity(page) / "issue-comment-page-structure-checker.md"


def quote_arg(value: str) -> str:
    if not value:
        return '""'
    if any(char.isspace() for char in value):
        return f'"{value}"'
    return value


def format_command(command: list[str]) -> str:
    return " ".join(quote_arg(part) for part in command)


def run_command(command: list[str], *, cwd: Path, dry_run: bool) -> int:
    print(format_command(command))

    if dry_run:
        return 0

    result = subprocess.run(command, cwd=cwd, check=False)
    return result.returncode


def parse_signal_count(output_path: Path) -> int:
    if not output_path.is_file():
        raise PageStructureBatchError(f"Expected output file was not created: {output_path}")

    text = output_path.read_text(encoding="utf-8")

    match = SIGNAL_COUNT_PATTERN.search(text)
    if not match:
        raise PageStructureBatchError(f"Could not parse Signal count from: {output_path}")

    return int(match.group("count"))


def build_checker_command(
    *,
    repo_root: Path,
    page: str,
    output_path: Path,
    max_signals: int,
) -> list[str]:
    return [
        sys.executable,
        str(repo_root / "scripts/phase-2/check_agents/page_structure_checker.py"),
        "--page",
        page,
        "--output",
        str(output_path),
        "--max-signals",
        str(max_signals),
    ]


def build_issue_manager_command(
    *,
    repo_root: Path,
    repo: str,
    comment_path: Path,
    labels: list[str],
    issue_dry_run: bool,
) -> list[str]:
    command = [
        sys.executable,
        str(repo_root / "scripts/phase-2/issue_manager.py"),
        "--comment",
        str(comment_path),
        "--repo",
        repo,
    ]

    for label in labels:
        command.extend(["--label", label])

    if issue_dry_run:
        command.append("--dry-run")

    return command


def run_for_page(
    *,
    repo_root: Path,
    page: str,
    output_path: Path,
    repo: str,
    labels: list[str],
    max_signals: int,
    post: bool,
    issue_dry_run: bool,
    dry_run: bool,
) -> PageRunResult:
    checker_command = build_checker_command(
        repo_root=repo_root,
        page=page,
        output_path=output_path,
        max_signals=max_signals,
    )

    if not dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    checker_return_code = run_command(checker_command, cwd=repo_root, dry_run=dry_run)

    if checker_return_code != 0:
        return PageRunResult(
            page=page,
            output_path=output_path,
            checker_return_code=checker_return_code,
            signal_count=None,
            issue_manager_return_code=None,
            issue_manager_mode="not-run",
        )

    if dry_run:
        return PageRunResult(
            page=page,
            output_path=output_path,
            checker_return_code=checker_return_code,
            signal_count=None,
            issue_manager_return_code=None,
            issue_manager_mode="not-run",
        )

    signal_count = parse_signal_count(output_path)

    if not post:
        return PageRunResult(
            page=page,
            output_path=output_path,
            checker_return_code=checker_return_code,
            signal_count=signal_count,
            issue_manager_return_code=None,
            issue_manager_mode="not-run",
        )

    if signal_count == 0:
        return PageRunResult(
            page=page,
            output_path=output_path,
            checker_return_code=checker_return_code,
            signal_count=signal_count,
            issue_manager_return_code=None,
            issue_manager_mode="skipped-zero-signals",
        )

    issue_manager_command = build_issue_manager_command(
        repo_root=repo_root,
        repo=repo,
        comment_path=output_path,
        labels=labels,
        issue_dry_run=issue_dry_run,
    )

    issue_manager_return_code = run_command(
        issue_manager_command,
        cwd=repo_root,
        dry_run=False,
    )

    return PageRunResult(
        page=page,
        output_path=output_path,
        checker_return_code=checker_return_code,
        signal_count=signal_count,
        issue_manager_return_code=issue_manager_return_code,
        issue_manager_mode="dry-run" if issue_dry_run else "posted",
    )


def print_summary(results: list[PageRunResult], *, dry_run: bool) -> None:
    print()
    print("=" * 80)
    print("Page structure batch summary")
    print("=" * 80)

    total = len(results)
    checker_failures = [result for result in results if result.checker_return_code != 0]
    parsed_results = [result for result in results if result.signal_count is not None]
    pages_with_signals = [
        result for result in parsed_results if result.signal_count and result.signal_count > 0
    ]
    issue_manager_runs = [
        result for result in results if result.issue_manager_return_code is not None
    ]
    issue_manager_failures = [
        result
        for result in issue_manager_runs
        if result.issue_manager_return_code != 0
    ]

    print(f"Pages processed: {total}")
    print(f"Checker failures: {len(checker_failures)}")

    if dry_run:
        print("Signal counts: not parsed in dry-run mode")
    else:
        print(f"Pages with structural signals: {len(pages_with_signals)}")
        print(f"Issue-manager runs: {len(issue_manager_runs)}")
        print(f"Issue-manager failures: {len(issue_manager_failures)}")

    print()
    print("Outputs:")
    for result in results:
        signal_text = (
            "dry-run"
            if dry_run
            else "unknown"
            if result.signal_count is None
            else str(result.signal_count)
        )
        print(
            f"- {result.page} -> {result.output_path} ; "
            f"Signal count: {signal_text} ; Issue manager: {result.issue_manager_mode}"
        )

    if checker_failures:
        print()
        print("Checker failures:")
        for result in checker_failures:
            print(f"- {result.page}: exit code {result.checker_return_code}")

    if issue_manager_failures:
        print()
        print("Issue-manager failures:")
        for result in issue_manager_failures:
            print(f"- {result.page}: exit code {result.issue_manager_return_code}")


def main() -> int:
    args = parse_args()

    try:
        if args.max_signals < 0:
            raise PageStructureBatchError("--max-signals must not be negative.")

        if args.issue_dry_run and not args.post:
            raise PageStructureBatchError("--issue-dry-run requires --post.")

        repo_root = repo_root_from_script()
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = repo_root / output_dir

        labels = [label.strip() for label in args.label if label.strip()]
        pages = discover_pages(repo_root, args.only_page)

        print("One-time page-structure-checker batch")
        print()
        print(f"Repository root: {repo_root}")
        print(f"GitHub repo: {args.repo}")
        print(f"Output directory: {output_dir}")
        print(f"Pages discovered: {len(pages)}")
        print(f"Post issues/comments: {args.post}")
        print(f"Issue-manager dry run: {args.issue_dry_run}")
        print(f"Command dry run: {args.dry_run}")
        print(f"Labels: {', '.join(labels) if labels else '(none)'}")
        print()

        results: list[PageRunResult] = []

        for index, page in enumerate(pages, start=1):
            print()
            print("-" * 80)
            print(f"Page {index}/{len(pages)}: {page}")
            print("-" * 80)

            output_path = issue_comment_path(output_dir, page)

            result = run_for_page(
                repo_root=repo_root,
                page=page,
                output_path=output_path,
                repo=args.repo,
                labels=labels,
                max_signals=args.max_signals,
                post=args.post,
                issue_dry_run=args.issue_dry_run,
                dry_run=args.dry_run,
            )

            results.append(result)

            failed = result.checker_return_code != 0 or (
                result.issue_manager_return_code is not None
                and result.issue_manager_return_code != 0
            )

            if failed and not args.continue_on_error:
                print_summary(results, dry_run=args.dry_run)
                return 1

        print_summary(results, dry_run=args.dry_run)

        has_failures = any(
            result.checker_return_code != 0
            or (
                result.issue_manager_return_code is not None
                and result.issue_manager_return_code != 0
            )
            for result in results
        )

        return 1 if has_failures else 0

    except PageStructureBatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())