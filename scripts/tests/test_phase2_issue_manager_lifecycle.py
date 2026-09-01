"""Regression coverage for Phase 2 signal issue publication semantics."""

from __future__ import annotations

import argparse
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIRECTORY = Path(__file__).resolve().parents[1] / "phase-2"
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

import issue_manager  # noqa: E402


def report(signal_count: int) -> str:
    signals = (
        "None identified within the configured check-agent scope."
        if signal_count == 0
        else "#### S-001 — Clear wording\n\n- Observation: A local wording issue exists."
    )
    return f"""## Check signal report: language-style-checker / gemini / gemini-3.5-flash — 2026-08-31

### Run metadata

| Field | Value |
|---|---|
| Agent | language-style-checker |
| Provider | gemini |
| Model | gemini-3.5-flash |
| Prompt | language-style-checker-v1.1.0 |
| Review date | 2026-08-31 |
| Reviewed page | docs/stereotypes/classes/example.md |
| Commit SHA | {"a" * 40} |
| Signal count | {signal_count} |

### Summary judgment

Signal publication lifecycle test.

### Scope

Language-style check only.

### Signals

{signals}
"""


class IssueManagerLifecycleTests(unittest.TestCase):
    def run_main(
        self,
        *,
        signal_count: int,
        existing_issue: issue_manager.GitHubIssue | None,
        matching_comment: issue_manager.GitHubIssueComment | None = None,
    ) -> tuple[int, str, mock.Mock, mock.Mock, mock.Mock]:
        with tempfile.TemporaryDirectory() as temporary:
            comment_path = Path(temporary) / "report.md"
            comment_path.write_text(report(signal_count), encoding="utf-8")
            args = argparse.Namespace(
                comment=str(comment_path),
                repo="example/repository",
                task_id="b" * 64,
                label=[],
                post_empty=False,
                dry_run=False,
            )
            create = mock.Mock(
                return_value=issue_manager.GitHubIssue(
                    number=101,
                    title="Check signal: language-style-checker: classes/example",
                    url="https://github.com/example/repository/issues/101",
                )
            )
            post = mock.Mock()
            update = mock.Mock()
            with (
                mock.patch.object(issue_manager, "parse_args", return_value=args),
                mock.patch.object(issue_manager, "ensure_gh_available"),
                mock.patch.object(issue_manager, "search_open_issue", return_value=existing_issue),
                mock.patch.object(issue_manager, "list_issue_comments", return_value=[]),
                mock.patch.object(issue_manager, "find_matching_issue_comment", return_value=matching_comment),
                mock.patch.object(issue_manager, "create_issue", create),
                mock.patch.object(issue_manager, "post_issue_comment", post),
                mock.patch.object(issue_manager, "update_issue_comment", update),
                contextlib.redirect_stdout(io.StringIO()) as stdout,
            ):
                result = issue_manager.main()
        return result, stdout.getvalue(), create, post, update

    def test_positive_signal_without_open_match_creates_exactly_one_issue(self) -> None:
        result, output, create, post, update = self.run_main(signal_count=1, existing_issue=None)

        self.assertEqual(result, 0)
        create.assert_called_once()
        post.assert_called_once()
        update.assert_not_called()
        self.assertIn("publication_outcome=new_issue_created", output)

    def test_positive_signal_with_open_match_comments_without_duplicate_issue(self) -> None:
        existing = issue_manager.GitHubIssue(100, "existing", None)
        result, output, create, post, update = self.run_main(signal_count=1, existing_issue=existing)

        self.assertEqual(result, 0)
        create.assert_not_called()
        post.assert_called_once()
        update.assert_not_called()
        self.assertIn("publication_outcome=existing_issue_commented", output)

    def test_same_stable_identity_updates_existing_comment(self) -> None:
        existing = issue_manager.GitHubIssue(100, "existing", None)
        comment = issue_manager.GitHubIssueComment(900, "existing body", None)
        result, output, create, post, update = self.run_main(
            signal_count=1,
            existing_issue=existing,
            matching_comment=comment,
        )

        self.assertEqual(result, 0)
        create.assert_not_called()
        post.assert_not_called()
        update.assert_called_once()
        self.assertIn("publication_outcome=existing_comment_updated", output)

    def test_zero_signal_without_open_match_does_not_create_issue(self) -> None:
        result, output, create, post, update = self.run_main(signal_count=0, existing_issue=None)

        self.assertEqual(result, 0)
        create.assert_not_called()
        post.assert_not_called()
        update.assert_not_called()
        self.assertIn("publication_outcome=zero_signal_no_publication", output)


if __name__ == "__main__":
    unittest.main()
