#!/usr/bin/env python3
"""Post a candidate check-signal comment to the correct GitHub issue.

This script bridges generated check-agent output and the GitHub issue pattern
used by the project.

Input:
- one generated issue-comment Markdown file produced by a check-agent runner;
- one GitHub repository in owner/name form.

Behavior:
- extract Agent, Reviewed page, and Signal count from the comment metadata table;
- derive the deterministic page-plus-agent issue title from the reviewed page and agent;
- find an existing open issue with that exact title;
- create the issue if needed and allowed;
- add a stable identity marker to the issue comment body;
- update an existing matching issue comment when the same stable identity exists;
- post the candidate check-signal comment as a new issue comment otherwise.

Important:
- this script does not run an LLM;
- this script does not modify canonical documentation pages;
- this script does not open pull requests;
- this script does not close issues;
- this script uses the GitHub CLI (`gh`) and expects local authentication via
  `gh auth login`.

Compatibility:
- during the signal migration, this script accepts legacy `Finding count`
  metadata as a fallback, but emits and documents `Signal count` as the primary
  contract;
- page-plus-agent routing requires an `Agent` metadata row.
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
    "### Run metadata",
    "### Summary judgment",
    "### Scope",
]

PRIMARY_COMMENT_FRAGMENTS = [
    "## Check signal report:",
    "### Signals",
]

LEGACY_COMMENT_FRAGMENTS = [
    "## Model review:",
    "### Findings",
]

METADATA_ROW_PATTERN = re.compile(
    r"^\|\s*(?P<key>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|\s*$",
    re.MULTILINE,
)

COMMENT_IDENTITY_MARKER_PATTERN = re.compile(
    r"<!--\s*check-signal-comment\s*\n(?P<body>.*?)\n-->",
    re.DOTALL,
)

AGENT_SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ISSUE_TITLE_PREFIX = "Check signal"
COMMENT_IDENTITY_MARKER_NAME = "check-signal-comment"
COMMENT_IDENTITY_KEYS = ("page", "agent", "provider", "model", "prompt", "commit")


class IssueManagerError(RuntimeError):
    """Raised when issue-manager execution cannot proceed safely."""


@dataclass(frozen=True)
class ReviewCommentMetadata:
    """Metadata extracted from a generated candidate signal comment."""

    reviewed_page: str
    signal_count: int
    agent: str
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


@dataclass(frozen=True)
class GitHubIssueComment:
    """Minimal GitHub issue-comment snapshot returned by the GitHub API."""

    comment_id: int
    body: str
    url: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Post a generated candidate check-signal comment to the "
            "deterministic GitHub issue for the reviewed stereotype page and check agent."
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
            "Create/post even when Signal count is 0 and no issue exists. "
            "By default, zero-signal comments are posted only if the issue "
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
    """Normalize a metadata-table cell value."""
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

    has_primary_structure = all(fragment in comment_text for fragment in PRIMARY_COMMENT_FRAGMENTS)
    has_legacy_structure = all(fragment in comment_text for fragment in LEGACY_COMMENT_FRAGMENTS)

    if not has_primary_structure and not has_legacy_structure:
        raise IssueManagerError(
            "Comment does not match the current signal-comment structure or the legacy review-comment structure."
        )


def normalize_agent_slug(agent: str | None) -> str:
    """Return a validated check-agent slug for issue routing."""
    if agent is None:
        raise IssueManagerError("Comment metadata is missing Agent.")

    normalized = clean_metadata_value(agent)

    if not normalized or normalized.lower() in {"n/a", "none", "null"}:
        raise IssueManagerError("Comment metadata Agent must contain a check-agent slug.")

    if not AGENT_SLUG_PATTERN.fullmatch(normalized):
        raise IssueManagerError(
            "Comment metadata Agent must be a lowercase slug containing only "
            f"letters, numbers, and hyphens: {normalized}"
        )

    return normalized


def require_identity_value(value: str | None, field_name: str) -> str:
    """Return a safe non-empty metadata value for stable comment identity."""
    if value is None:
        raise IssueManagerError(f"Comment metadata is missing {field_name}.")

    normalized = clean_metadata_value(value)

    if not normalized:
        raise IssueManagerError(f"Comment metadata {field_name} must not be empty.")

    if "\n" in normalized or "\r" in normalized or "-->" in normalized:
        raise IssueManagerError(
            f"Comment metadata {field_name} contains characters that cannot be used "
            "inside a stable identity marker."
        )

    return normalized


def build_comment_identity(metadata: ReviewCommentMetadata) -> dict[str, str]:
    """Build the stable identity used to find an existing issue comment."""
    return {
        "page": require_identity_value(metadata.reviewed_page, "Reviewed page"),
        "agent": metadata.agent,
        "provider": require_identity_value(metadata.provider, "Provider"),
        "model": require_identity_value(metadata.model, "Model"),
        "prompt": require_identity_value(metadata.prompt, "Prompt"),
        "commit": require_identity_value(metadata.commit_sha, "Commit SHA"),
    }


def render_comment_identity_marker(identity: dict[str, str]) -> str:
    """Render the hidden marker that identifies one posted check-signal comment."""
    lines = [f"<!-- {COMMENT_IDENTITY_MARKER_NAME}"]

    for key in COMMENT_IDENTITY_KEYS:
        lines.append(f"{key}: {identity[key]}")

    lines.append("-->")
    return "\n".join(lines)


def strip_existing_comment_identity_marker(comment_text: str) -> str:
    """Remove one existing identity marker before re-rendering the comment body."""
    return COMMENT_IDENTITY_MARKER_PATTERN.sub("", comment_text, count=1).lstrip("\n")


def build_issue_comment_body(comment_text: str, identity: dict[str, str]) -> str:
    """Build the body posted to GitHub, including a hidden stable identity marker."""
    marker = render_comment_identity_marker(identity)
    visible_comment = strip_existing_comment_identity_marker(comment_text).rstrip()
    return f"{marker}\n\n{visible_comment}\n"


def parse_comment_identity_marker(comment_body: str) -> dict[str, str] | None:
    """Parse the first hidden stable identity marker in an issue comment."""
    match = COMMENT_IDENTITY_MARKER_PATTERN.search(comment_body)
    if not match:
        return None

    identity: dict[str, str] = {}

    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key in COMMENT_IDENTITY_KEYS:
            identity[key] = value

    if any(key not in identity for key in COMMENT_IDENTITY_KEYS):
        return None

    return identity


def comment_identity_matches(comment_body: str, identity: dict[str, str]) -> bool:
    """Return whether an existing GitHub comment has the same stable identity."""
    existing_identity = parse_comment_identity_marker(comment_body)
    return existing_identity == identity


def extract_review_comment_metadata(comment_text: str) -> ReviewCommentMetadata:
    validate_comment_structure(comment_text)

    metadata = extract_metadata_table(comment_text)

    reviewed_page = metadata.get("reviewed page")
    if not reviewed_page:
        raise IssueManagerError("Comment metadata is missing Reviewed page.")

    signal_count_raw = metadata.get("signal count")
    if signal_count_raw is None:
        signal_count_raw = metadata.get("finding count")

    if signal_count_raw is None:
        raise IssueManagerError("Comment metadata is missing Signal count.")

    try:
        signal_count = int(signal_count_raw)
    except ValueError as exc:
        raise IssueManagerError(
            f"Signal count is not an integer: {signal_count_raw}"
        ) from exc

    if signal_count < 0:
        raise IssueManagerError(f"Signal count must not be negative: {signal_count}")

    return ReviewCommentMetadata(
        reviewed_page=reviewed_page,
        signal_count=signal_count,
        agent=normalize_agent_slug(metadata.get("agent")),
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


def derive_issue_title(page_identity: str, agent: str) -> str:
    """Derive the phase-neutral issue title for one page plus one check agent."""
    return f"{ISSUE_TITLE_PREFIX}: {agent}: {page_identity}"


def build_issue_body(
    *,
    issue_title: str,
    reviewed_page: str,
    page_identity: str,
    agent: str,
) -> str:
    return f"""# {issue_title}

## Reviewed page

`{reviewed_page}`

## Page identity

`{page_identity}`

## Check agent

`{agent}`

## Purpose

Collect check-agent signal comments for this page and agent.

## Resolution model

Signals are candidate observations. They are not accepted findings until reviewed.

This issue may be resolved manually or by later resolution tooling.
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


def list_issue_comments(repo: str, issue_number: int) -> list[GitHubIssueComment]:
    """Fetch all issue comments for one issue using the GitHub API."""
    result = run_gh(
        [
            "api",
            f"repos/{repo}/issues/{issue_number}/comments?per_page=100",
            "--paginate",
            "--slurp",
        ]
    )

    if result.returncode != 0:
        raise IssueManagerError(
            "Failed to list GitHub issue comments.\n"
            f"{result.stderr.strip() or result.stdout.strip()}"
        )

    try:
        payload = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise IssueManagerError("GitHub issue comments did not return valid JSON.") from exc

    if payload and all(isinstance(page, list) for page in payload):
        raw_comments = [comment for page in payload for comment in page]
    elif isinstance(payload, list):
        raw_comments = payload
    else:
        raise IssueManagerError("GitHub issue comments returned an unexpected JSON shape.")

    comments: list[GitHubIssueComment] = []

    for raw_comment in raw_comments:
        if not isinstance(raw_comment, dict):
            continue

        comment_id = raw_comment.get("id")
        body = raw_comment.get("body")

        if comment_id is None or body is None:
            continue

        comments.append(
            GitHubIssueComment(
                comment_id=int(comment_id),
                body=str(body),
                url=raw_comment.get("html_url") or raw_comment.get("url"),
            )
        )

    return comments


def find_matching_issue_comment(
    comments: list[GitHubIssueComment],
    identity: dict[str, str],
) -> GitHubIssueComment | None:
    """Find an existing issue comment with the same stable identity marker."""
    for comment in comments:
        if comment_identity_matches(comment.body, identity):
            return comment

    return None


def write_temp_text_file(text: str, suffix: str) -> Path:
    """Write text to a temporary file and return its path."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        suffix=suffix,
        delete=False,
    ) as text_file:
        text_file.write(text)
        return Path(text_file.name)


def post_issue_comment(repo: str, issue_number: int, comment_body: str) -> None:
    body_path = write_temp_text_file(comment_body, ".md")

    try:
        result = run_gh(
            [
                "issue",
                "comment",
                str(issue_number),
                "--repo",
                repo,
                "--body-file",
                str(body_path),
            ]
        )
    finally:
        try:
            body_path.unlink(missing_ok=True)
        except OSError:
            pass

    if result.returncode != 0:
        raise IssueManagerError(
            "Failed to post GitHub issue comment.\n"
            f"{result.stderr.strip() or result.stdout.strip()}"
        )


def update_issue_comment(repo: str, comment_id: int, comment_body: str) -> None:
    payload_path = write_temp_text_file(json.dumps({"body": comment_body}), ".json")

    try:
        result = run_gh(
            [
                "api",
                "--method",
                "PATCH",
                f"repos/{repo}/issues/comments/{comment_id}",
                "--input",
                str(payload_path),
            ]
        )
    finally:
        try:
            payload_path.unlink(missing_ok=True)
        except OSError:
            pass

    if result.returncode != 0:
        raise IssueManagerError(
            "Failed to update GitHub issue comment.\n"
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
    comment_identity: dict[str, str],
    labels: list[str],
    post_empty: bool,
) -> None:
    print("DRY RUN")
    print()
    print(f"Repository: {repo}")
    print(f"Comment file: {comment_path}")
    print(f"Reviewed page: {metadata.reviewed_page}")
    print(f"Page identity: {page_identity}")
    print(f"Agent: {metadata.agent}")
    print(f"Issue title: {issue_title}")
    print(f"Signal count: {metadata.signal_count}")
    print(f"Provider: {metadata.provider or '(not found)'}")
    print(f"Model: {metadata.model or '(not found)'}")
    print(f"Prompt: {metadata.prompt or '(not found)'}")
    print(f"Commit SHA: {metadata.commit_sha or '(not found)'}")
    print("Stable comment identity:")
    for key in COMMENT_IDENTITY_KEYS:
        print(f"  {key}: {comment_identity[key]}")
    print(f"Labels: {', '.join(labels) if labels else '(none)'}")
    print(f"Post empty if issue is missing: {post_empty}")
    print()
    print("Would search for an existing open issue with this exact title.")

    print("If an issue exists, would search its comments for the stable identity marker.")
    print("If a matching comment exists, would update that comment.")
    print("If no matching comment exists, would post a new comment.")

    if metadata.signal_count == 0 and not post_empty:
        print(
            "If no issue exists, would skip issue creation because Signal count is 0."
        )
    else:
        print("If no issue exists, would create the issue and post a new comment.")

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
        issue_title = derive_issue_title(page_identity, metadata.agent)
        issue_body = build_issue_body(
            issue_title=issue_title,
            reviewed_page=metadata.reviewed_page,
            page_identity=page_identity,
            agent=metadata.agent,
        )

        comment_identity = build_comment_identity(metadata)
        issue_comment_body = build_issue_comment_body(comment_text, comment_identity)

        labels = [label.strip() for label in args.label if label.strip()]

        if args.dry_run:
            print_dry_run(
                comment_path=comment_path,
                repo=args.repo,
                metadata=metadata,
                page_identity=page_identity,
                issue_title=issue_title,
                issue_body=issue_body,
                comment_identity=comment_identity,
                labels=labels,
                post_empty=args.post_empty,
            )
            return 0

        ensure_gh_available()

        existing_issue = search_open_issue(args.repo, issue_title)

        if existing_issue is not None:
            print(f"Found existing issue #{existing_issue.number}: {issue_title}")
            existing_comments = list_issue_comments(args.repo, existing_issue.number)
            matching_comment = find_matching_issue_comment(existing_comments, comment_identity)

            if matching_comment is not None:
                update_issue_comment(
                    args.repo,
                    matching_comment.comment_id,
                    issue_comment_body,
                )
                print(
                    "Updated existing candidate signal comment "
                    f"#{matching_comment.comment_id} on issue #{existing_issue.number}"
                )
                return 0

            post_issue_comment(args.repo, existing_issue.number, issue_comment_body)
            print(f"Posted candidate signal comment to issue #{existing_issue.number}")
            return 0

        print(f"No open issue found for: {issue_title}")

        if metadata.signal_count == 0 and not args.post_empty:
            print("Signal count is 0.")
            print("Skipped issue creation by default.")
            return 0

        created_issue = create_issue(
            repo=args.repo,
            title=issue_title,
            body=issue_body,
            labels=labels,
        )

        print(f"Created issue #{created_issue.number}: {issue_title}")

        post_issue_comment(args.repo, created_issue.number, issue_comment_body)
        print(f"Posted candidate signal comment to issue #{created_issue.number}")

        return 0

    except IssueManagerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
