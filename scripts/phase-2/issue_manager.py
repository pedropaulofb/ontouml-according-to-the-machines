#!/usr/bin/env python3
"""Post a Phase 2 candidate page-review comment to the correct GitHub issue.

This script bridges the current local Phase 2 output model and the planned
GitHub issue pattern.

Input:
- one generated issue-comment Markdown file produced by run_page_review.py;
- one GitHub repository in owner/name form.

Behavior:
- extract Reviewed page and Finding count from the comment metadata table;
- derive the deterministic issue title from the reviewed page;
- find an existing open issue with that exact title;
- create the issue if needed and allowed;
- post the candidate review comment as a new issue comment.

Important:
- this script does not run an LLM;
- this script does not modify canonical documentation pages;
- this script does not open pull requests;
- this script uses the GitHub CLI (`gh`) and expects local authentication via
  `gh auth login`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COMMENT_FRAGMENTS = [
    "## Model review:",
    "### Run metadata",
    "### Summary judgment",
    "### Scope",
    "### Findings",
]

METADATA_ROW_PATTERN = re.compile(
    r"^\|\s*(?P<key>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|\s*$",
    re.MULTILINE,
)

ISSUE_TITLE_PREFIX = "Phase 2 page review"


class IssueManagerError(RuntimeError):
    """Raised when issue-manager execution cannot proceed safely."""


@dataclass(frozen=True)
class ReviewCommentMetadata:
    """Metadata extracted from a generated candidate review comment."""

    reviewed_page: str
    finding_count: int
    provider: str | None = None
    model: str | None = None
    prompt: str | None = None
    commit_sha: str | None = None


@dataclass(frozen=True)
class GitHubIssue:
    """Minimal GitHub issue snapshot returned by the GitHub CLI."""

    number: int
    title: str
    url: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Post a generated Phase 2 candidate review comment to the "
            "deterministic GitHub issue for the reviewed stereotype page."
        )
    )

    parser.add_argument(
        "--comment",
        required=True,
        help="Path to the generated issue-comment Markdown file.",
    )

    parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository in owner/name form.",
    )

    parser.add_argument(
        "--label",
        action="append",
        default=[],
        help=(
            "Optional label to apply when creating a new issue. "
            "Can be provided multiple times. If labels fail, the script "
            "retries issue creation without labels."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the derived issue action without calling GitHub.",
    )

    parser.add_argument(
        "--post-empty",
        action="store_true",
        help=(
            "Create/post even when Finding count is 0 and no issue exists. "
            "By default, zero-finding comments are posted only if the issue "
            "already exists."
        ),
    )

    return parser.parse_args()


def read_text_file(path: Path, description: str) -> str:
    if not path.exists():
        raise IssueManagerError(f"{description} does not exist: {path}")

    if not path.is_file():
        raise IssueManagerError(f"{description} is not a file: {path}")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise IssueManagerError(f"{description} is not valid UTF-8: {path}") from exc


def clean_metadata_value(value: str) -> str:
    """Normalize a metadata-table cell value.

    The runner currently emits plain values, but this accepts optional
    backticks and common Markdown spacing.
    """
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


def validate_comment_structure(comment_text: str) -> None:
    if not comment_text.strip():
        raise IssueManagerError("Comment file is empty.")

    for fragment in REQUIRED_COMMENT_FRAGMENTS:
        if fragment not in comment_text:
            raise IssueManagerError(f"Comment is missing required fragment: {fragment}")


def extract_review_comment_metadata(comment_text: str) -> ReviewCommentMetadata:
    validate_comment_structure(comment_text)

    metadata = extract_metadata_table(comment_text)

    reviewed_page = metadata.get("reviewed page")
    if not reviewed_page:
        raise IssueManagerError("Comment metadata is missing Reviewed page.")

    finding_count_raw = metadata.get("finding count")
    if finding_count_raw is None:
        raise IssueManagerError("Comment metadata is missing Finding count.")

    try:
        finding_count = int(finding_count_raw)
    except ValueError as exc:
        raise IssueManagerError(
            f"Finding count is not an integer: {finding_count_raw}"
        ) from exc

    if finding_count < 0:
        raise IssueManagerError(f"Finding count must not be negative: {finding_count}")

    return ReviewCommentMetadata(
        reviewed_page=reviewed_page,
        finding_count=finding_count,
        provider=metadata.get("provider"),
        model=metadata.get("model"),
        prompt=metadata.get("prompt"),
        commit_sha=metadata.get("commit sha"),
    )


def derive_page_identity(reviewed_page: str) -> str:
    """Derive identity such as classes/role from a stereotype page path."""
    normalized = reviewed_page.replace("\\", "/").strip()
    prefix = "docs/stereotypes/"

    if not normalized.startswith(prefix):
        raise IssueManagerError(
            "Reviewed page must be under docs/stereotypes/: "
            f"{reviewed_page}"
        )

    remainder = normalized[len(prefix):]

    if not remainder.endswith(".md"):
        raise IssueManagerError(f"Reviewed page must be a Markdown file: {reviewed_page}")

    identity = remainder[:-3]

    parts = identity.split("/")
    if len(parts) != 2 or parts[0] not in {"classes", "relations"} or not parts[1]:
        raise IssueManagerError(
            "Reviewed page must match docs/stereotypes/{classes|relations}/<id>.md: "
            f"{reviewed_page}"
        )

    return identity


def derive_issue_title(page_identity: str) -> str:
    return f"{ISSUE_TITLE_PREFIX}: {page_identity}"


def build_issue_body(issue_title: str, reviewed_page: str, page_identity: str) -> str:
    return f"""# {issue_title}

## Reviewed page

`{reviewed_page}`

## Page identity

`{page_identity}`

## Purpose

Collect Phase 2 model-review comments for this page.
"""


def run_gh(args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run a GitHub CLI command and capture text output."""
    command = ["gh", *args]

    try:
        return subprocess.run(
            command,
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise IssueManagerError(
            "GitHub CLI `gh` was not found. Install it and authenticate with `gh auth login`."
        ) from exc


def ensure_gh_available() -> None:
    result = run_gh(["auth", "status"])

    if result.returncode != 0:
        raise IssueManagerError(
            "GitHub CLI authentication check failed. Run `gh auth login` first.\n"
            f"{result.stderr.strip() or result.stdout.strip()}"
        )


def search_open_issue(repo: str, issue_title: str) -> GitHubIssue | None:
    """Find an open issue with an exact matching title."""
    search_query = f'"{issue_title}" in:title'

    result = run_gh(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--search",
            search_query,
            "--json",
            "number,title,url",
            "--limit",
            "50",
        ]
    )

    if result.returncode != 0:
        raise IssueManagerError(
            "Failed to search GitHub issues.\n"
            f"{result.stderr.strip() or result.stdout.strip()}"
        )

    try:
        issues = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise IssueManagerError("GitHub issue search did not return valid JSON.") from exc

    for issue in issues:
        if issue.get("title") == issue_title:
            return GitHubIssue(
                number=int(issue["number"]),
                title=str(issue["title"]),
                url=issue.get("url"),
            )

    return None


def parse_issue_number_from_create_output(output: str) -> int | None:
    """Parse an issue number from common `gh issue create` output."""
    match = re.search(r"/issues/(\d+)\b", output)
    if match:
        return int(match.group(1))

    stripped = output.strip()
    if stripped.isdigit():
        return int(stripped)

    return None


def create_issue(repo: str, title: str, body: str, labels: list[str]) -> GitHubIssue:
    """Create a GitHub issue.

    If label application fails, retry once without labels, as agreed for the
    first implementation.
    """
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        suffix=".md",
        delete=False,
    ) as body_file:
        body_file.write(body)
        body_path = Path(body_file.name)

    try:
        command = [
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            title,
            "--body-file",
            str(body_path),
        ]

        for label in labels:
            command.extend(["--label", label])

        result = run_gh(command)

        if result.returncode != 0 and labels:
            print(
                "WARNING: Issue creation with labels failed. Retrying without labels.",
                file=sys.stderr,
            )
            print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)

            result = run_gh(
                [
                    "issue",
                    "create",
                    "--repo",
                    repo,
                    "--title",
                    title,
                    "--body-file",
                    str(body_path),
                ]
            )

        if result.returncode != 0:
            raise IssueManagerError(
                "Failed to create GitHub issue.\n"
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        output = result.stdout.strip()
        issue_number = parse_issue_number_from_create_output(output)

        if issue_number is None:
            found_issue = search_open_issue(repo, title)
            if found_issue is None:
                raise IssueManagerError(
                    "Issue was created, but its number could not be determined."
                )
            return found_issue

        return GitHubIssue(number=issue_number, title=title, url=output or None)

    finally:
        try:
            body_path.unlink(missing_ok=True)
        except OSError:
            pass


def post_issue_comment(repo: str, issue_number: int, comment_path: Path) -> None:
    result = run_gh(
        [
            "issue",
            "comment",
            str(issue_number),
            "--repo",
            repo,
            "--body-file",
            str(comment_path),
        ]
    )

    if result.returncode != 0:
        raise IssueManagerError(
            "Failed to post GitHub issue comment.\n"
            f"{result.stderr.strip() or result.stdout.strip()}"
        )


def print_dry_run(
    *,
    comment_path: Path,
    repo: str,
    metadata: ReviewCommentMetadata,
    page_identity: str,
    issue_title: str,
    issue_body: str,
    labels: list[str],
    post_empty: bool,
) -> None:
    print("DRY RUN")
    print()
    print(f"Repository: {repo}")
    print(f"Comment file: {comment_path}")
    print(f"Reviewed page: {metadata.reviewed_page}")
    print(f"Page identity: {page_identity}")
    print(f"Issue title: {issue_title}")
    print(f"Finding count: {metadata.finding_count}")
    print(f"Provider: {metadata.provider or '(not found)'}")
    print(f"Model: {metadata.model or '(not found)'}")
    print(f"Prompt: {metadata.prompt or '(not found)'}")
    print(f"Commit SHA: {metadata.commit_sha or '(not found)'}")
    print(f"Labels: {', '.join(labels) if labels else '(none)'}")
    print(f"Post empty if issue is missing: {post_empty}")
    print()
    print("Would search for an existing open issue with this exact title.")

    if metadata.finding_count == 0 and not post_empty:
        print(
            "If no issue exists, would skip issue creation because Finding count is 0."
        )
        print("If an issue exists, would post the candidate review as a new comment.")
    else:
        print("Would create the issue if missing.")
        print("Would post the candidate review as a new comment.")

    print()
    print("Issue body that would be used if creating a new issue:")
    print()
    print(issue_body.rstrip())


def main() -> int:
    args = parse_args()

    try:
        comment_path = Path(args.comment).resolve()
        comment_text = read_text_file(comment_path, "Candidate issue comment")
        metadata = extract_review_comment_metadata(comment_text)

        page_identity = derive_page_identity(metadata.reviewed_page)
        issue_title = derive_issue_title(page_identity)
        issue_body = build_issue_body(
            issue_title=issue_title,
            reviewed_page=metadata.reviewed_page,
            page_identity=page_identity,
        )

        labels = [label.strip() for label in args.label if label.strip()]

        if args.dry_run:
            print_dry_run(
                comment_path=comment_path,
                repo=args.repo,
                metadata=metadata,
                page_identity=page_identity,
                issue_title=issue_title,
                issue_body=issue_body,
                labels=labels,
                post_empty=args.post_empty,
            )
            return 0

        ensure_gh_available()

        existing_issue = search_open_issue(args.repo, issue_title)

        if existing_issue is not None:
            print(f"Found existing issue #{existing_issue.number}: {issue_title}")
            post_issue_comment(args.repo, existing_issue.number, comment_path)
            print(f"Posted candidate review comment to issue #{existing_issue.number}")
            return 0

        print(f"No open issue found for: {issue_title}")

        if metadata.finding_count == 0 and not args.post_empty:
            print("Finding count is 0.")
            print("Skipped issue creation by default.")
            return 0

        created_issue = create_issue(
            repo=args.repo,
            title=issue_title,
            body=issue_body,
            labels=labels,
        )

        print(f"Created issue #{created_issue.number}: {issue_title}")

        post_issue_comment(args.repo, created_issue.number, comment_path)
        print(f"Posted candidate review comment to issue #{created_issue.number}")

        return 0

    except IssueManagerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
