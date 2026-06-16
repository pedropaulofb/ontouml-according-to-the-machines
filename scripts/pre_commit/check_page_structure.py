#!/usr/bin/env python3
"""Pre-commit wrapper for the deterministic Phase 2 page-structure checker.

The underlying checker writes Phase 2 check-signal reports and returns zero when
it can complete safely. This wrapper makes it suitable for pre-commit by failing
when one or more structural signals are reported for a staged canonical
stereotype page.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_OUTPUT_DIR = ".tmp/pre-commit/page-structure-checker"
DEFAULT_MAX_SIGNALS = 3
CANONICAL_PAGE_PATTERN = re.compile(r"^docs/stereotypes/(classes|relations)/[^/]+\.md$")
SIGNAL_COUNT_PATTERN = re.compile(
    r"^\|\s*Signal count\s*\|\s*(?P<count>\d+)\s*\|\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class PageCheckResult:
    """Result of running the page-structure checker for one page."""

    page: str
    output_path: Path
    checker_return_code: int
    signal_count: int | None


class PageStructurePreCommitError(RuntimeError):
    """Raised when the pre-commit wrapper cannot proceed safely."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the Phase 2 page-structure checker for staged canonical stereotype pages."
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for generated check reports. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--max-signals",
        type=int,
        default=DEFAULT_MAX_SIGNALS,
        help=f"Maximum structural signals to report per page. Default: {DEFAULT_MAX_SIGNALS}",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Repository-relative files passed by pre-commit.",
    )
    return parser.parse_args()


def normalize_path(path: str) -> str:
    """Normalize a path to a repository-relative POSIX path string."""
    return path.replace("\\", "/").strip()


def find_repo_root() -> Path:
    """Return the repository root."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise PageStructurePreCommitError("Could not determine the repository root with git.") from exc

    repo_root = Path(result.stdout.strip()).resolve()
    if not repo_root.is_dir():
        raise PageStructurePreCommitError(f"Resolved repository root is not a directory: {repo_root}")
    return repo_root


def is_canonical_stereotype_page(path: str) -> bool:
    """Return whether a path is a canonical stereotype page checked by Phase 2."""
    normalized = normalize_path(path)
    return bool(CANONICAL_PAGE_PATTERN.fullmatch(normalized)) and not normalized.endswith("/index.md")


def page_identity(page: str) -> str:
    """Return a stable filesystem-safe identity for a page."""
    normalized = normalize_path(page)
    if normalized.startswith("docs/stereotypes/"):
        normalized = normalized[len("docs/stereotypes/") :]
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return normalized.replace("/", "-")


def output_path_for_page(output_dir: Path, page: str) -> Path:
    """Return the check report path for one page."""
    return output_dir / page_identity(page) / "issue-comment-page-structure-checker.md"


def parse_signal_count(output_path: Path) -> int:
    """Parse the signal count from one generated check report."""
    if not output_path.is_file():
        raise PageStructurePreCommitError(f"Expected check report was not created: {output_path}")

    text = output_path.read_text(encoding="utf-8")
    match = SIGNAL_COUNT_PATTERN.search(text)
    if not match:
        raise PageStructurePreCommitError(f"Could not parse Signal count from check report: {output_path}")
    return int(match.group("count"))


def run_checker(repo_root: Path, page: str, output_path: Path, max_signals: int) -> PageCheckResult:
    """Run the underlying deterministic checker for one page."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(repo_root / "scripts/phase-2/check_agents/page_structure_checker.py"),
        "--page",
        page,
        "--output",
        str(output_path),
        "--max-signals",
        str(max_signals),
    ]

    result = subprocess.run(
        command,
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    if result.returncode != 0:
        return PageCheckResult(
            page=page,
            output_path=output_path,
            checker_return_code=result.returncode,
            signal_count=None,
        )

    return PageCheckResult(
        page=page,
        output_path=output_path,
        checker_return_code=result.returncode,
        signal_count=parse_signal_count(output_path),
    )


def select_pages(repo_root: Path, filenames: list[str]) -> list[str]:
    """Select existing canonical stereotype pages from pre-commit filenames."""
    selected: list[str] = []

    for filename in filenames:
        normalized = normalize_path(filename)
        if not is_canonical_stereotype_page(normalized):
            continue
        if not (repo_root / normalized).is_file():
            continue
        selected.append(normalized)

    return sorted(set(selected))


def print_summary(results: list[PageCheckResult]) -> None:
    """Print a concise result summary."""
    print("Page-structure checker summary")
    print(f"Pages checked: {len(results)}")

    for result in results:
        signal_text = "unknown" if result.signal_count is None else str(result.signal_count)
        print(f"- {result.page}: {signal_text} signal(s); report: {result.output_path}")


def main() -> int:
    """Run the pre-commit page-structure wrapper."""
    args = parse_args()

    try:
        if args.max_signals < 0:
            raise PageStructurePreCommitError("--max-signals must not be negative.")

        repo_root = find_repo_root()
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = repo_root / output_dir

        pages = select_pages(repo_root, args.filenames)
        if not pages:
            return 0

        results = [
            run_checker(
                repo_root=repo_root,
                page=page,
                output_path=output_path_for_page(output_dir, page),
                max_signals=args.max_signals,
            )
            for page in pages
        ]

        print_summary(results)

        checker_failures = [result for result in results if result.checker_return_code != 0]
        signal_failures = [result for result in results if result.signal_count is not None and result.signal_count > 0]

        if checker_failures:
            print("ERROR: page-structure-checker failed for at least one page.", file=sys.stderr)
            return 1

        if signal_failures:
            print("ERROR: structural signal(s) found in canonical stereotype page(s).", file=sys.stderr)
            return 1

        return 0

    except PageStructurePreCommitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
