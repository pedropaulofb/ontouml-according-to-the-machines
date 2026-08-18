"""Regression tests for deterministic Phase 2 resolver plan normalization."""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "phase-2" / "resolve_signal_issue.py"
MODULE_NAME = "phase_2_resolve_signal_issue"
SPEC = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load resolver module from {MODULE_PATH}")
resolver = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = resolver
SPEC.loader.exec_module(resolver)


class OverallDecisionNormalizationTests(unittest.TestCase):
    def make_issue(
        self,
        *,
        number: int = 218,
        agent: str = "page-hygiene-checker",
        reviewed_page: str = "docs/stereotypes/relations/comparative.md",
    ) -> resolver.IssueSnapshot:
        return resolver.IssueSnapshot(
            number=number,
            title=f"Check signal: {agent}: relations/comparative",
            body="",
            state="OPEN",
            url=f"https://github.com/example/repository/issues/{number}",
            agent=agent,
            reviewed_page=reviewed_page,
            comments=[],
        )

    def rejected_plan(self) -> dict[str, object]:
        return {
            "issue_number": 218,
            "agent": "page-hygiene-checker",
            "reviewed_page": "docs/stereotypes/relations/comparative.md",
            "overall_decision": "reject_for_phase_2_automation",
            "signal_groups": [
                {
                    "group_id": "G-001",
                    "source_signal_refs": ["issue body"],
                    "decision": "reject_for_phase_2_automation",
                    "reason_code": "out_of_scope",
                    "rationale": "The reported change is outside the automated resolver scope.",
                    "edits": [],
                }
            ],
            "issue_comment": "No changes were accepted for Phase 2 automation.",
        }

    def accepted_plan(self) -> dict[str, object]:
        return {
            "issue_number": 219,
            "agent": "language-style-checker",
            "reviewed_page": "docs/stereotypes/classes/example.md",
            "overall_decision": "no_accepted_changes",
            "signal_groups": [
                {
                    "group_id": "G-001",
                    "source_signal_refs": ["comment 1 S-001"],
                    "decision": "accept",
                    "reason_code": "in_scope_exact_edit",
                    "rationale": "The change is a local meaning-preserving language correction.",
                    "edits": [
                        {
                            "current_text": "Old sentence.",
                            "proposed_text": "Improved sentence.",
                            "rationale": "Improves wording without changing technical meaning.",
                        }
                    ],
                }
            ],
            "issue_comment": (
                "A pull request with the accepted deterministic local language/style edits "
                "is available here: {{PR_URL}}"
            ),
        }

    def test_normalizes_rejected_only_plan_to_no_accepted_changes(self) -> None:
        plan = self.rejected_plan()

        change = resolver.normalize_overall_decision(plan)

        self.assertEqual(
            change,
            ("reject_for_phase_2_automation", "no_accepted_changes"),
        )
        self.assertEqual(plan["overall_decision"], "no_accepted_changes")
        resolver.validate_plan(plan, self.make_issue(), "Current page content.\n")

    def test_normalizes_accepted_plan_to_accepted_changes(self) -> None:
        plan = self.accepted_plan()
        issue = self.make_issue(
            number=219,
            agent="language-style-checker",
            reviewed_page="docs/stereotypes/classes/example.md",
        )

        change = resolver.normalize_overall_decision(plan)

        self.assertEqual(change, ("no_accepted_changes", "accepted_changes"))
        self.assertEqual(plan["overall_decision"], "accepted_changes")
        resolver.validate_plan(plan, issue, "Old sentence.\n")

    def test_leaves_matching_overall_decision_unchanged(self) -> None:
        plan = self.rejected_plan()
        plan["overall_decision"] = "no_accepted_changes"

        change = resolver.normalize_overall_decision(plan)

        self.assertIsNone(change)
        self.assertEqual(plan["overall_decision"], "no_accepted_changes")

    def test_does_not_conceal_invalid_group_decision(self) -> None:
        plan = self.rejected_plan()
        signal_groups = plan["signal_groups"]
        assert isinstance(signal_groups, list)
        group = signal_groups[0]
        assert isinstance(group, dict)
        group["decision"] = "reject"
        original_overall_decision = plan["overall_decision"]

        change = resolver.normalize_overall_decision(plan)

        self.assertIsNone(change)
        self.assertEqual(plan["overall_decision"], original_overall_decision)
        with self.assertRaisesRegex(resolver.ResolverError, "Invalid group decision"):
            resolver.validate_plan(plan, self.make_issue(), "Current page content.\n")

    def test_exact_match_validation_remains_strict_after_normalization(self) -> None:
        plan = self.accepted_plan()
        issue = self.make_issue(
            number=219,
            agent="language-style-checker",
            reviewed_page="docs/stereotypes/classes/example.md",
        )

        resolver.normalize_overall_decision(plan)

        with self.assertRaisesRegex(
            resolver.ResolverError,
            "Accepted edit current_text must occur exactly once",
        ):
            resolver.validate_plan(plan, issue, "Old sentence.\n\nOld sentence.\n")

    def test_main_records_combined_normalization_artifacts(self) -> None:
        plan = self.rejected_plan()
        signal_groups = plan["signal_groups"]
        assert isinstance(signal_groups, list)
        group = signal_groups[0]
        assert isinstance(group, dict)
        group["edits"] = None
        issue = self.make_issue()
        args = argparse.Namespace(
            repo="example/repository",
            issue="218",
            provider="gemini",
            model="gemini-2.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=True,
            branch_prefix="phase-2/auto-resolve",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            with (
                mock.patch.object(resolver, "parse_args", return_value=args),
                mock.patch.object(resolver, "load_resolver_attempt_state", return_value={"attempts": {}}),
                mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
                mock.patch.object(
                    resolver,
                    "collect_active_signal_comments",
                    return_value=(
                        resolver.ActiveSignalComment("1", "task-218", "gemini", "gemini-2.5-flash", "Active signal."),
                    ),
                ),
                mock.patch.object(resolver, "read_issue", return_value=issue),
                mock.patch.object(
                    resolver,
                    "load_text",
                    side_effect=lambda path: (
                        "Current page content.\n" if str(path) == issue.reviewed_page else "Resolver prompt"
                    ),
                ),
                mock.patch.object(resolver, "resolver_output_dir", return_value=output_dir),
                mock.patch.object(resolver, "call_provider", return_value=json.dumps(plan)),
                contextlib.redirect_stdout(io.StringIO()) as stdout,
            ):
                result = resolver.main()

            self.assertEqual(result, 0)
            normalization = (output_dir / "issue-218-normalization.txt").read_text(encoding="utf-8")
            self.assertIn("Normalized 1 rejected signal group edits value(s) to [].", normalization)
            self.assertIn(
                "Normalized overall_decision from 'reject_for_phase_2_automation' to 'no_accepted_changes'",
                normalization,
            )
            self.assertIn("Normalized 1 rejected signal group edits value(s) to [].", stdout.getvalue())
            self.assertIn("Normalized overall_decision", stdout.getvalue())

            parsed_plan = json.loads((output_dir / "issue-218-parsed-plan.json").read_text(encoding="utf-8"))
            normalized_plan = json.loads((output_dir / "issue-218-normalized-plan.json").read_text(encoding="utf-8"))
            final_plan = json.loads((output_dir / "issue-218-plan.json").read_text(encoding="utf-8"))

            self.assertEqual(parsed_plan["overall_decision"], "reject_for_phase_2_automation")
            self.assertIsNone(parsed_plan["signal_groups"][0]["edits"])
            self.assertEqual(normalized_plan["overall_decision"], "no_accepted_changes")
            self.assertEqual(normalized_plan["signal_groups"][0]["edits"], [])
            self.assertEqual(final_plan["overall_decision"], "no_accepted_changes")
            self.assertEqual(final_plan["signal_groups"][0]["edits"], [])
            self.assertFalse((output_dir / "issue-218-plan-error.txt").exists())


if __name__ == "__main__":
    unittest.main()
