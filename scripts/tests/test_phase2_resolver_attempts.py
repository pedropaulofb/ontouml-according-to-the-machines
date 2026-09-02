"""Stage 7 resolver identity, compaction, and persistence regression tests."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

SCRIPT_DIRECTORY = Path(__file__).resolve().parents[1] / "phase-2"
REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "config" / "phase-2" / "provider-models.json"

if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

import provider_model_registry  # noqa: E402
import quota_state  # noqa: E402
import resolve_signal_issue as resolver  # noqa: E402
import resolver_attempt_state  # noqa: E402
import task_state  # noqa: E402

TIMESTAMP = "2026-08-17T12:00:00Z"
NOW = datetime(2026, 8, 17, 12, 0, tzinfo=timezone.utc)


class ResolverAttemptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.page = "## Description\n\nCurrent wording.\n"
        self.issue = resolver.IssueSnapshot(
            number=42,
            title="Check signal: language-style-checker: classes/example",
            body="Legacy issue body must not be sent to the model.",
            state="OPEN",
            url="https://github.com/example/repository/issues/42",
            agent="language-style-checker",
            reviewed_page="docs/stereotypes/classes/example.md",
            comments=[],
        )
        self.active = (
            resolver.ActiveSignalComment(
                comment_id="100",
                task_id="a" * 64,
                provider="gemini",
                model="gemini-3.5-flash",
                body="Active signal body.",
            ),
        )

    def context(
        self,
        *,
        page: str | None = None,
        active: tuple[resolver.ActiveSignalComment, ...] | None = None,
        provider: str = "gemini",
        model: str = "gemini-3.5-flash",
        max_tokens: int = 8000,
    ) -> resolver.ResolverAttemptContext:
        return resolver.build_resolver_attempt_context(
            issue=self.issue,
            page_text=page if page is not None else self.page,
            prompt="Resolver prompt.",
            active_comments=active if active is not None else self.active,
            provider=provider,
            model=model,
            max_completion_tokens=max_tokens,
            max_attempts=1,
        )

    def state_with_attempt(
        self,
        context: resolver.ResolverAttemptContext,
        *,
        status: str,
        failure_kind: str | None,
    ) -> dict[str, object]:
        state = resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP)
        event = {
            "schema_version": resolver_attempt_state.SCHEMA_VERSION,
            "event_id": f"event-{status}",
            "attempt_id": context.attempt_id,
            "observed_at": TIMESTAMP,
            "identity": context.identity,
            "status": status,
            "request_sent": True,
            "failure_kind": failure_kind,
        }
        updated, _counts = resolver_attempt_state.aggregate_events(state, [event])
        return updated

    def test_changed_page_or_active_signal_snapshot_changes_attempt_id(self) -> None:
        original = self.context()
        changed_page = self.context(page=self.page + "\nChanged page content.\n")
        changed_signal = self.context(
            active=(
                resolver.ActiveSignalComment(
                    comment_id="100",
                    task_id="a" * 64,
                    provider="gemini",
                    model="gemini-3.5-flash",
                    body="Changed active signal body.",
                ),
            )
        )
        changed_request = self.context(max_tokens=6000)

        self.assertNotEqual(original.attempt_id, changed_page.attempt_id)
        self.assertNotEqual(original.attempt_id, changed_signal.attempt_id)
        self.assertNotEqual(original.attempt_id, changed_request.attempt_id)
        self.assertNotEqual(changed_page.attempt_id, changed_signal.attempt_id)

    def test_validator_version_reenables_known_blocked_issues_without_deleting_history(self) -> None:
        state = resolver_attempt_state.load_state(REPO_ROOT / "data/phase-2/resolver-attempt-state.json")
        old_attempt_ids = (
            "d494e0c7a67449db1f5380ecc1e2b6c05ac86ac238d13091cbd7b0108993ac95",
            "2f171b14a00e6c4d7b3ccf6f354af99f068603190079ff64be99ba55dade7027",
        )

        self.assertEqual(resolver.RESOLVER_VALIDATOR_VERSION, "resolver-plan-validator-v1.2.4")
        for old_attempt_id in old_attempt_ids:
            with self.subTest(old_attempt_id=old_attempt_id):
                old_record = state["attempts"][old_attempt_id]
                self.assertEqual(old_record["identity"]["resolver_validator_version"], "resolver-plan-validator-v1.2.3")
                new_identity = dict(old_record["identity"])
                new_identity["resolver_validator_version"] = resolver.RESOLVER_VALIDATOR_VERSION
                new_attempt_id = resolver_attempt_state.attempt_id_for(new_identity)

                self.assertNotEqual(new_attempt_id, old_attempt_id)
                self.assertNotIn(new_attempt_id, state["attempts"])
                self.assertIn(old_attempt_id, state["attempts"])

    def test_paginated_issue_search_keeps_all_matching_candidates(self) -> None:
        response = [
            {
                "items": [
                    {
                        "number": 1,
                        "title": "Check signal: language-style-checker: classes/example",
                        "created_at": "2026-08-17T10:00:00Z",
                    }
                ]
            },
            {
                "items": [
                    {
                        "number": 2,
                        "title": "Check signal: language-style-checker: relations/example",
                        "created_at": "2026-08-17T11:00:00Z",
                    }
                ]
            },
        ]
        with mock.patch.object(resolver, "run", return_value=json.dumps(response)) as run:
            matches = resolver.search_open_issues_for_agent(
                "example/repository",
                "language-style-checker",
            )

        self.assertEqual([match["number"] for match in matches], [1, 2])
        self.assertIn("--paginate", run.call_args.args[0])
        self.assertIn("--slurp", run.call_args.args[0])

    def test_active_signal_selection_excludes_stale_and_unpublished_comments(self) -> None:
        scoped_page, _scope = resolver.scope_page_content_for_agent(
            agent=self.issue.agent,
            page_content=self.page,
        )
        current_hash = resolver.sha256_text(scoped_page)
        current_task_id = "a" * 64
        stale_task_id = "b" * 64
        unpublished_task_id = "c" * 64

        def marker(task_id: str, body: str) -> str:
            return (
                "<!-- check-signal-comment\n"
                f"page: {self.issue.reviewed_page}\n"
                f"agent: {self.issue.agent}\n"
                "provider: gemini\n"
                "model: gemini-3.5-flash\n"
                f"task_id: {task_id}\n"
                "-->\n\n"
                f"{body}\n"
            )

        comments = [
            {"id": "100", "body": marker(current_task_id, "Current signal.")},
            {"id": "101", "body": marker(stale_task_id, "Stale signal.")},
            {"id": "102", "body": marker(unpublished_task_id, "Unpublished signal.")},
            {"id": "103", "body": "Untracked legacy comment."},
        ]
        issue = resolver.IssueSnapshot(**{**self.issue.__dict__, "comments": comments})

        def record(task_id: str, content_hash: str, publication: str) -> dict[str, object]:
            return {
                "task_id": task_id,
                "status": "completed",
                "publication": {"status": publication},
                "identity": {
                    "page": self.issue.reviewed_page,
                    "agent": self.issue.agent,
                    "provider": "gemini",
                    "model": "gemini-3.5-flash",
                    "content_sha256": content_hash,
                },
            }

        tasks = {
            "tasks": {
                current_task_id: record(current_task_id, current_hash, "published"),
                stale_task_id: record(stale_task_id, "0" * 64, "published"),
                unpublished_task_id: record(unpublished_task_id, current_hash, "pending"),
            }
        }

        selected = resolver.collect_active_signal_comments(issue, self.page, tasks)
        rendered = resolver.build_llm_input(issue, self.page, selected)

        self.assertEqual([comment.comment_id for comment in selected], ["100"])
        self.assertIn("Current signal.", rendered)
        self.assertNotIn("Stale signal.", rendered)
        self.assertNotIn("Unpublished signal.", rendered)
        self.assertNotIn("Untracked legacy comment.", rendered)
        self.assertNotIn(self.issue.body, rendered)
        self.assertIn(self.page, rendered)

    def test_empty_active_selection_does_not_restore_legacy_comments(self) -> None:
        issue = resolver.IssueSnapshot(
            **{**self.issue.__dict__, "comments": [{"id": "100", "body": "Legacy comment."}]}
        )
        rendered = resolver.build_llm_input(issue, self.page, ())
        self.assertNotIn("Legacy comment.", rendered)

    def test_attempt_events_are_idempotent_and_terminal_failures_block_replay(self) -> None:
        context = self.context()
        state = self.state_with_attempt(
            context,
            status="plan_invalid",
            failure_kind="plan_validation_failure",
        )
        record = resolver_attempt_state.attempt_record(state, context.identity)

        self.assertIsNotNone(record)
        self.assertEqual(record["status"], "plan_invalid")
        self.assertTrue(resolver_attempt_state.attempt_is_blocked(state, context.identity))

        event = {
            "schema_version": resolver_attempt_state.SCHEMA_VERSION,
            "event_id": "event-plan_invalid",
            "attempt_id": context.attempt_id,
            "observed_at": TIMESTAMP,
            "identity": context.identity,
            "status": "plan_invalid",
            "request_sent": True,
            "failure_kind": "plan_validation_failure",
        }
        replayed, counts = resolver_attempt_state.aggregate_events(state, [event])
        self.assertEqual(counts, {"added": 0, "ignored": 1})
        self.assertEqual(replayed, state)

    def test_not_called_event_does_not_block_later_execution(self) -> None:
        context = self.context()
        initial = resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP)
        event = {
            "schema_version": resolver_attempt_state.SCHEMA_VERSION,
            "event_id": "event-not-called",
            "attempt_id": context.attempt_id,
            "observed_at": TIMESTAMP,
            "identity": context.identity,
            "status": "not_called",
            "request_sent": False,
            "failure_kind": "rate_or_quota_limited",
        }
        state, _counts = resolver_attempt_state.aggregate_events(initial, [event])
        self.assertFalse(resolver_attempt_state.attempt_is_blocked(state, context.identity))

    def test_completed_prior_attempt_is_skipped_for_the_next_eligible_issue(self) -> None:
        first_context = self.context()
        second_issue = resolver.IssueSnapshot(
            **{
                **self.issue.__dict__,
                "number": 43,
                "url": "https://github.com/example/repository/issues/43",
                "reviewed_page": "docs/stereotypes/classes/second-example.md",
            }
        )
        second_context = resolver.build_resolver_attempt_context(
            issue=second_issue,
            page_text=self.page,
            prompt="Resolver prompt.",
            active_comments=self.active,
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            max_attempts=1,
        )
        state = self.state_with_attempt(first_context, status="completed", failure_kind=None)

        with (
            mock.patch.object(resolver, "open_signal_issue_candidates", return_value=[42, 43]),
            mock.patch.object(resolver, "read_issue", side_effect=[self.issue, second_issue]),
            mock.patch.object(resolver, "attempt_context_for_issue", side_effect=[first_context, second_context]),
            mock.patch.object(resolver, "load_resolver_attempt_state", return_value=state),
            mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
            mock.patch.object(
                resolver,
                "resolver_slot_status",
                side_effect=[(True, "eligible", None), (True, "eligible", None)],
            ),
        ):
            eligibility = resolver.evaluate_resolver_work("example/repository", now=NOW)

        self.assertTrue(eligibility.candidate_exists)
        self.assertEqual(eligibility.issue_number, 43)
        self.assertTrue(eligibility.primary_executable)

    def test_changed_signal_snapshot_is_executable_after_prior_invalid_attempt(self) -> None:
        original = self.context()
        changed = self.context(
            active=(
                resolver.ActiveSignalComment(
                    comment_id="100",
                    task_id="a" * 64,
                    provider="gemini",
                    model="gemini-3.5-flash",
                    body="Changed active signal body.",
                ),
            )
        )
        state = self.state_with_attempt(
            original,
            status="plan_invalid",
            failure_kind="plan_validation_failure",
        )

        with (
            mock.patch.object(resolver, "open_signal_issue_candidates", return_value=[42]),
            mock.patch.object(resolver, "read_issue", return_value=self.issue),
            mock.patch.object(resolver, "attempt_context_for_issue", return_value=changed),
            mock.patch.object(resolver, "load_resolver_attempt_state", return_value=state),
            mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
            mock.patch.object(
                resolver,
                "resolver_slot_status",
                side_effect=[(True, "eligible", None), (True, "eligible", None)],
            ),
        ):
            eligibility = resolver.evaluate_resolver_work("example/repository", now=NOW)

        self.assertTrue(eligibility.candidate_exists)
        self.assertEqual(eligibility.issue_number, 42)
        self.assertTrue(eligibility.primary_executable)

    def test_custom_primary_request_configuration_is_part_of_evaluated_identity(self) -> None:
        custom = self.context(max_tokens=9000)
        with (
            mock.patch.object(resolver, "open_signal_issue_candidates", return_value=[42]),
            mock.patch.object(resolver, "read_issue", return_value=self.issue),
            mock.patch.object(resolver, "attempt_context_for_issue", return_value=custom) as build_context,
            mock.patch.object(
                resolver,
                "load_resolver_attempt_state",
                return_value=resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP),
            ),
            mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
            mock.patch.object(
                resolver,
                "resolver_slot_status",
                side_effect=[(True, "eligible", None), (True, "eligible", None)],
            ),
        ):
            eligibility = resolver.evaluate_resolver_work(
                "example/repository",
                now=NOW,
                primary_max_completion_tokens=9000,
                primary_max_attempts=2,
            )

        self.assertTrue(eligibility.primary_executable)
        self.assertEqual(eligibility.primary_context, custom)
        self.assertEqual(build_context.call_args.kwargs["max_completion_tokens"], 9000)
        self.assertEqual(build_context.call_args.kwargs["max_attempts"], 2)

    def test_manual_gemini_36_selection_remains_a_direct_primary_route(self) -> None:
        context = self.context(provider="gemini", model="gemini-3.6-flash", max_tokens=6000)
        args = argparse.Namespace(
            repo="example/repository",
            issue="42",
            provider="gemini",
            model="gemini-3.6-flash",
            max_completion_tokens=6000,
            provider_max_attempts=1,
            dry_run=True,
            branch_prefix="phase-2/auto-resolve",
            attempt_state="unused.json",
            preflight_only=False,
            fallback_used=False,
        )
        plan = {"overall_decision": "no_accepted_changes", "issue_comment": "No changes."}

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with (
                mock.patch.object(resolver, "parse_args", return_value=args),
                mock.patch.object(resolver, "resolver_output_dir", return_value=output),
                mock.patch.object(
                    resolver,
                    "load_resolver_attempt_state",
                    return_value=resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP),
                ),
                mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
                mock.patch.object(resolver, "read_issue", return_value=self.issue),
                mock.patch.object(resolver, "attempt_context_for_issue", return_value=context),
                mock.patch.object(resolver, "resolver_slot_status", return_value=(True, "eligible", None)),
                mock.patch.object(resolver, "evaluate_resolver_work") as canonical_eligibility,
                mock.patch.object(resolver, "call_provider", return_value=json.dumps(plan)) as provider_call,
                mock.patch.object(resolver, "normalize_rejected_group_edits", return_value=0),
                mock.patch.object(resolver, "validate_plan_structure_before_revalidation"),
                mock.patch.object(resolver, "demote_invalid_accepted_groups", return_value=[]),
                mock.patch.object(resolver, "normalize_overall_decision", return_value=None),
                mock.patch.object(resolver, "validate_plan"),
            ):
                result = resolver.main()
            outcome = json.loads((output / "outcome.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        canonical_eligibility.assert_not_called()
        provider_call.assert_called_once()
        self.assertEqual(outcome["outcome"], "deferred")
        self.assertTrue(outcome["request_sent"])
        self.assertFalse(outcome["fallback_used"])

    def test_unchanged_invalid_plan_is_skipped_without_provider_or_fallback(self) -> None:
        context = self.context()
        state = self.state_with_attempt(
            context,
            status="plan_invalid",
            failure_kind="plan_validation_failure",
        )
        args = argparse.Namespace(
            repo="example/repository",
            issue="42",
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=False,
            branch_prefix="phase-2/auto-resolve",
            attempt_state="unused.json",
            preflight_only=False,
        )
        eligibility = resolver.ResolverEligibility(
            candidate_exists=False,
            issue_number=None,
            primary_executable=False,
            fallback_executable=False,
            capacity_required=False,
            reserved_specs=(),
            retry_not_before=None,
            reason_codes=("no_candidate",),
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with (
                mock.patch.object(resolver, "parse_args", return_value=args),
                mock.patch.object(resolver, "load_resolver_attempt_state", return_value=state),
                mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
                mock.patch.object(resolver, "evaluate_resolver_work", return_value=eligibility),
                mock.patch.object(resolver, "resolver_output_dir", return_value=output),
                mock.patch.object(resolver, "call_provider") as provider_call,
            ):
                result = resolver.main()
            outcome = json.loads((output / "outcome.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        provider_call.assert_not_called()
        self.assertEqual(outcome["outcome"], "no_candidate")
        self.assertFalse(outcome["request_sent"])

    def test_unchanged_unavailable_primary_signals_fallback_without_duplicate_call(self) -> None:
        context = self.context()
        state = self.state_with_attempt(
            context,
            status="provider_failure",
            failure_kind="provider_unavailable",
        )
        args = argparse.Namespace(
            repo="example/repository",
            issue="42",
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=False,
            branch_prefix="phase-2/auto-resolve",
            attempt_state="unused.json",
            preflight_only=False,
        )
        eligibility = resolver.ResolverEligibility(
            candidate_exists=True,
            issue_number=42,
            primary_executable=False,
            fallback_executable=True,
            capacity_required=True,
            reserved_specs=("gemini:gemini-3.6-flash",),
            retry_not_before=None,
            reason_codes=("provider_temporarily_unavailable",),
            primary_context=context,
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with (
                mock.patch.object(resolver, "parse_args", return_value=args),
                mock.patch.object(resolver, "load_resolver_attempt_state", return_value=state),
                mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
                mock.patch.object(resolver, "evaluate_resolver_work", return_value=eligibility),
                mock.patch.object(resolver, "resolver_output_dir", return_value=output),
                mock.patch.object(resolver, "call_provider") as provider_call,
            ):
                result = resolver.main()
            outcome = json.loads((output / "outcome.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        provider_call.assert_not_called()
        self.assertEqual(outcome["outcome"], "deferred")
        self.assertFalse(outcome["request_sent"])
        self.assertTrue(outcome["fallback_executable"])

    def test_incident_state_defers_without_provider_call_issue_resolution_or_pr(self) -> None:
        context = self.context()
        args = argparse.Namespace(
            repo="example/repository",
            issue="42",
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            provider_max_attempts=1,
            dry_run=False,
            branch_prefix="phase-2/auto-resolve",
            attempt_state="unused.json",
            preflight_only=False,
            fallback_used=False,
        )
        eligibility = resolver.ResolverEligibility(
            candidate_exists=True,
            issue_number=42,
            primary_executable=False,
            fallback_executable=False,
            capacity_required=False,
            reserved_specs=(),
            retry_not_before=None,
            reason_codes=("primary_slot_recheck_required", "fallback_not_eligible"),
            primary_context=context,
        )

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            with (
                mock.patch.object(resolver, "parse_args", return_value=args),
                mock.patch.object(resolver, "load_resolver_attempt_state", return_value={"attempts": {}}),
                mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
                mock.patch.object(resolver, "evaluate_resolver_work", return_value=eligibility),
                mock.patch.object(resolver, "resolver_output_dir", return_value=output),
                mock.patch.object(resolver, "call_provider") as provider_call,
                mock.patch.object(resolver, "create_pr") as create_pr,
                mock.patch.object(resolver, "comment_and_close") as close_issue,
            ):
                result = resolver.main()
            outcome = json.loads((output / "outcome.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        provider_call.assert_not_called()
        create_pr.assert_not_called()
        close_issue.assert_not_called()
        self.assertEqual(outcome["outcome"], "deferred")
        self.assertEqual(outcome["reason_code"], "primary_slot_recheck_required")
        self.assertFalse(outcome["request_sent"])
        self.assertFalse(outcome["issue_resolved"])
        self.assertIsNone(outcome["pr_url"])

    def test_fallback_eligibility_uses_gemini_36_request_identity(self) -> None:
        primary = self.context()
        fallback = self.context(
            provider="gemini",
            model="gemini-3.6-flash",
            max_tokens=6000,
        )
        state = resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP)

        with (
            mock.patch.object(resolver, "build_resolver_attempt_context", return_value=fallback) as build,
            mock.patch.object(resolver, "attempt_is_blocked", return_value=False),
            mock.patch.object(resolver, "resolver_slot_eligibility", return_value=(True, "eligible")) as eligible,
        ):
            result = resolver._fallback_remains_eligible(context=primary, attempt_state=state, now=NOW)

        self.assertTrue(result)
        build.assert_called_once_with(
            issue=primary.issue,
            page_text=primary.page_text,
            prompt=primary.prompt,
            active_comments=primary.active_comments,
            provider="gemini",
            model="gemini-3.6-flash",
            max_completion_tokens=6000,
            max_attempts=1,
        )
        eligible.assert_called_once_with("gemini", "gemini-3.6-flash", now=NOW)

    def test_groq_plan_uses_existing_exact_replacement_validation(self) -> None:
        page = (
            self.page
            + "\n## Generation and Review Log\n\n"
            + "| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |\n"
            + "|---|---|---|---|---|---|---|---|\n"
        )
        plan = {
            "issue_number": self.issue.number,
            "agent": self.issue.agent,
            "reviewed_page": self.issue.reviewed_page,
            "overall_decision": "accepted_changes",
            "signal_groups": [
                {
                    "group_id": "G-001",
                    "source_signal_refs": ["comment 100 S-001"],
                    "decision": "accept",
                    "reason_code": "in_scope_exact_edit",
                    "rationale": "The edit is local, deterministic, and meaning-preserving.",
                    "edits": [
                        {
                            "current_text": "Current wording.",
                            "proposed_text": "Revised wording.",
                            "rationale": "The replacement is exact and local.",
                        }
                    ],
                }
            ],
            "issue_comment": "Accepted edits are available at {{PR_URL}}.",
        }

        resolver.validate_plan(plan, self.issue, page)
        updated = resolver.apply_edits(page, plan)
        self.assertIn("Revised wording.", updated)
        self.assertNotIn("Current wording.", updated)


class ResolverAttemptPersistenceTests(unittest.TestCase):
    def test_shared_quota_aggregation_persists_resolver_attempt_events(self) -> None:
        registry = provider_model_registry.load_registry(REGISTRY_PATH)
        issue = resolver.IssueSnapshot(
            number=43,
            title="Check signal: language-style-checker: classes/example",
            body="",
            state="OPEN",
            url="",
            agent="language-style-checker",
            reviewed_page="docs/stereotypes/classes/example.md",
            comments=[],
        )
        context = resolver.build_resolver_attempt_context(
            issue=issue,
            page_text="Current page.\n",
            prompt="Resolver prompt.\n",
            active_comments=(
                resolver.ActiveSignalComment(
                    "200",
                    "d" * 64,
                    "groq",
                    "openai/gpt-oss-120b",
                    "Signal.",
                ),
            ),
            provider="groq",
            model="openai/gpt-oss-120b",
            max_completion_tokens=6000,
            max_attempts=1,
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            quota_path = root / "data/phase-2/quota-state.json"
            tasks_path = root / "data/phase-2/task-state.json"
            attempts_path = root / "data/phase-2/resolver-attempt-state.json"
            quota_events = root / "quota-events"
            attempt_events = root / "resolver-attempt-events"
            quota_events.mkdir()
            quota_state.write_state(
                quota_path,
                quota_state.build_initial_state(registry, timestamp=TIMESTAMP),
                registry,
            )
            task_state.write_task_state(
                tasks_path,
                task_state.new_task_state(
                    registry_sha256="0" * 64,
                    timestamp=TIMESTAMP,
                ),
            )
            resolver_attempt_state.write_state(
                attempts_path,
                resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP),
            )
            resolver_attempt_state.write_event(
                identity=context.identity,
                status="completed",
                request_sent=True,
                event_directory=attempt_events,
                observed_at=NOW,
            )

            result = quota_state.main(
                [
                    "aggregate",
                    "--repo-root",
                    str(root),
                    "--registry",
                    str(REGISTRY_PATH),
                    "--state",
                    str(quota_path),
                    "--task-state",
                    str(tasks_path),
                    "--events",
                    str(quota_events),
                    "--resolver-attempt-state",
                    str(attempts_path),
                    "--resolver-attempt-events",
                    str(attempt_events),
                ]
            )
            persisted = resolver_attempt_state.load_state(attempts_path)

        self.assertEqual(result, 0)
        self.assertEqual(persisted["attempts"][context.attempt_id]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
