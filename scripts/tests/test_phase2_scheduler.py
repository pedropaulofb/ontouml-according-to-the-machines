"""Tests for adaptive scheduling, durable leases, and provider workers."""

from __future__ import annotations

import copy
import hashlib
import importlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPT_DIR = REPO_ROOT / "scripts" / "phase-2"
if str(PHASE2_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPT_DIR))

provider_worker = importlib.import_module("provider_worker")
quota_state = importlib.import_module("quota_state")
registry_module = importlib.import_module("provider_model_registry")
resolver = importlib.import_module("resolve_signal_issue")
resolver_attempt_state = importlib.import_module("resolver_attempt_state")
task_scheduler = importlib.import_module("task_scheduler")
task_reconciler = importlib.import_module("task_reconciler")
task_state_module = importlib.import_module("task_state")

REGISTRY_PATH = REPO_ROOT / "config" / "phase-2" / "provider-models.json"
NOW = datetime(2026, 8, 12, 14, 0, tzinfo=timezone.utc)
TIMESTAMP = "2026-08-12T14:00:00Z"


def identity(provider: str, model: str, page: str, agent: str = "page-hygiene-checker") -> dict[str, str]:
    return {
        "phase": "phase-2",
        "page": page,
        "agent": agent,
        "provider": provider,
        "model": model,
        "content_sha256": "a" * 64,
        "prompt_id": f"{agent}-v1.0.3",
        "prompt_sha256": "b" * 64,
        "validator_version": "check-signal-schema-v1",
        "request_config_sha256": "c" * 64,
        "segmentation_profile": "full-page-v1",
    }


def task_record(
    provider: str,
    model: str,
    page: str,
    *,
    status: str = "pending",
    created_at: str = TIMESTAMP,
) -> dict[str, object]:
    task_identity = identity(provider, model, page)
    task_id = hashlib.sha256(json.dumps(task_identity, sort_keys=True).encode()).hexdigest()
    record = task_state_module.new_task_record(
        task_id=task_id,
        identity=task_identity,
        timestamp=created_at,
        source_commit_sha=None,
    )
    record["status"] = status
    return record


def state_with(*records: dict[str, object]) -> dict[str, object]:
    state = task_state_module.new_task_state(registry_sha256="d" * 64, timestamp=TIMESTAMP)
    state["tasks"] = {str(record["task_id"]): record for record in records}
    return state


def terminal_event(record: dict[str, object], outcome: str, attempts: int) -> dict[str, object]:
    lease = record["lease"]
    assert isinstance(lease, dict)
    return {
        "event_version": 1,
        "task_id": record["task_id"],
        "attempt_id": lease["attempt_id"],
        "workflow_run_id": lease["workflow_run_id"],
        "worker_id": lease["worker_id"],
        "outcome": outcome,
        "provider_attempts": attempts,
        "_event_path": "artifact/event.json",
    }


class SchedulerSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = registry_module.load_registry(REGISTRY_PATH)

    def setUp(self) -> None:
        self.quota = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)

    def build(self, records: list[dict[str, object]], **kwargs):
        tasks = state_with(*records)
        plans = task_scheduler.build_provider_work_plans(
            task_state=tasks,
            quota_state=copy.deepcopy(self.quota),
            registry=self.registry,
            workflow_run_id="workflow-1",
            now=NOW,
            **kwargs,
        )
        return tasks, plans

    def test_completed_tasks_are_never_selected(self) -> None:
        slot = self.registry.executable_slots[0]
        _tasks, plans = self.build([task_record(slot.provider, slot.model, "completed.md", status="completed")])
        self.assertEqual(plans[slot.provider]["assignments"], [])

    def test_blocked_tasks_are_never_selected(self) -> None:
        slot = self.registry.executable_slots[0]
        _tasks, plans = self.build(
            [task_record(slot.provider, slot.model, "blocked.md", status="blocked_provider_policy")]
        )
        self.assertEqual(plans[slot.provider]["assignments"], [])

    def test_oldest_task_in_least_complete_slot_is_selected(self) -> None:
        first, second = [slot for slot in self.registry.executable_slots if slot.provider == "groq"][:2]
        records = [
            task_record(first.provider, first.model, "first-complete.md", status="completed"),
            task_record(first.provider, first.model, "first-pending.md"),
            task_record(second.provider, second.model, "newer.md", created_at="2026-08-12T13:00:00Z"),
            task_record(second.provider, second.model, "oldest.md", created_at="2026-08-12T12:00:00Z"),
        ]
        _tasks, plans = self.build(records, max_tasks_per_provider=1)
        self.assertEqual(plans["groq"]["assignments"][0]["identity"]["page"], "oldest.md")

    def test_equal_completion_ties_use_registry_order(self) -> None:
        first, second = [slot for slot in self.registry.executable_slots if slot.provider == "gemini"][:2]
        _tasks, plans = self.build(
            [
                task_record(second.provider, second.model, "second.md"),
                task_record(first.provider, first.model, "first.md"),
            ],
            max_tasks_per_provider=1,
        )
        self.assertEqual(plans["gemini"]["assignments"][0]["identity"]["model"], first.model)

    def test_second_scheduler_cannot_lease_the_same_task(self) -> None:
        slot = self.registry.executable_slots[0]
        tasks = state_with(task_record(slot.provider, slot.model, "page.md"))
        first = task_scheduler.build_provider_work_plans(
            task_state=tasks,
            quota_state=copy.deepcopy(self.quota),
            registry=self.registry,
            workflow_run_id="first",
            now=NOW,
        )
        second = task_scheduler.build_provider_work_plans(
            task_state=tasks,
            quota_state=copy.deepcopy(self.quota),
            registry=self.registry,
            workflow_run_id="second",
            now=NOW,
        )
        self.assertEqual(len(first[slot.provider]["assignments"]), 1)
        self.assertEqual(second[slot.provider]["assignments"], [])

    def test_only_the_resolver_capacity_spec_is_withheld(self) -> None:
        self.assertEqual(
            task_scheduler.SHARED_RESOLVER_SPECS,
            {("gemini", "gemini-3.5-flash"), ("gemini", "gemini-3.6-flash")},
        )
        for provider, model in task_scheduler.SHARED_RESOLVER_SPECS:
            with self.subTest(provider=provider, model=model):
                shared = self.registry.find(provider, model)
                assert shared is not None
                _tasks, plans = self.build(
                    [task_record(shared.provider, shared.model, "page.md")],
                    resolver_capacity_required=True,
                    resolver_reserved_specs={shared.spec},
                )
                self.assertEqual(plans[provider]["assignments"], [])

    def test_openrouter_shared_capacity_is_capped_at_fifty(self) -> None:
        slot = next(slot for slot in self.registry.executable_slots if slot.provider == "openrouter")
        records = [task_record(slot.provider, slot.model, f"page-{index}.md") for index in range(60)]
        _tasks, plans = self.build(records)
        self.assertEqual(len(plans["openrouter"]["assignments"]), 50)

    def test_elapsed_quota_cooldown_does_not_preserve_stale_zero_capacity(self) -> None:
        slot = next(slot for slot in self.registry.executable_slots if slot.provider == "groq")
        group = self.quota["quota_groups"][f"groq:{slot.model}"]
        group["status"] = "deferred_quota"
        group["remaining_estimate"] = 0
        group["requests_remaining_minute"] = 0
        group["retry_not_before"] = "2026-08-12T13:00:00Z"
        runtime = self.quota["runtime_slots"][slot.spec]
        runtime["status"] = "temporarily_unavailable"
        runtime["retry_not_before"] = "2026-08-12T13:00:00Z"
        _tasks, plans = self.build([task_record(slot.provider, slot.model, "page.md")])
        self.assertEqual(len(plans["groq"]["assignments"]), 1)

    def test_no_global_fixed_limit_restricts_known_useful_work(self) -> None:
        slot = next(slot for slot in self.registry.executable_slots if slot.provider == "gemini")
        records = [task_record(slot.provider, slot.model, f"page-{index}.md") for index in range(9)]
        _tasks, plans = self.build(records)
        self.assertEqual(len(plans["gemini"]["assignments"]), 9)

    def test_plan_selection_does_not_mutate_task_leases(self) -> None:
        slot = self.registry.executable_slots[0]
        tasks, plans = self.build([task_record(slot.provider, slot.model, "page.md")], lease_tasks=False)
        record = next(iter(tasks["tasks"].values()))
        self.assertEqual(record["status"], "pending")
        self.assertIsNone(record["lease"])
        self.assertEqual(len(plans[slot.provider]["assignments"]), 1)


class SchedulerCliStateNeutralityTests(unittest.TestCase):
    def test_reconciled_state_is_validated_before_planning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            task_state_path = Path(temporary) / "task-state.json"
            shutil.copy2(REPO_ROOT / "data/phase-2/task-state.json", task_state_path)
            work_plan_root = Path(temporary) / "work-plans"
            validation_error = task_reconciler.TaskReconciliationError("invalid reconciled state")

            with (
                mock.patch.object(task_scheduler, "validate_desired_state", side_effect=validation_error) as validate,
                mock.patch.object(task_scheduler, "build_provider_work_plans") as build_plans,
            ):
                result = task_scheduler.main(
                    [
                        "plan",
                        "--repo-root",
                        str(REPO_ROOT),
                        "--task-state",
                        str(task_state_path),
                        "--workflow-run-id",
                        "validation-order-workflow",
                        "--reconcile",
                        "--timestamp",
                        TIMESTAMP,
                        "--work-plan-root",
                        str(work_plan_root),
                    ]
                )

        self.assertEqual(result, 2)
        validate.assert_called_once()
        build_plans.assert_not_called()

    def test_nonlease_reconciliation_does_not_write_persistent_state(self) -> None:
        for command in ("plan", "simulate"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as temporary:
                repo_root = Path(temporary)
                for relative in (
                    Path("config/phase-2"),
                    Path("docs/stereotypes"),
                    Path("prompts/phase-2"),
                ):
                    shutil.copytree(REPO_ROOT / relative, repo_root / relative)
                fixture_data_root = repo_root / "data/phase-2"
                fixture_data_root.mkdir(parents=True)
                for filename in ("task-state.json", "quota-state.json"):
                    shutil.copy2(REPO_ROOT / "data/phase-2" / filename, fixture_data_root / filename)
                subprocess.run(["git", "init", "--quiet"], cwd=repo_root, check=True)
                subprocess.run(
                    ["git", "config", "user.email", "phase2-tests@example.invalid"],
                    cwd=repo_root,
                    check=True,
                )
                subprocess.run(["git", "config", "user.name", "Phase 2 Tests"], cwd=repo_root, check=True)
                subprocess.run(
                    ["git", "commit", "--allow-empty", "--quiet", "-m", "test fixture"],
                    cwd=repo_root,
                    check=True,
                )

                registry_path = repo_root / "config/phase-2/provider-models.json"
                task_state_path = repo_root / "data/phase-2/task-state.json"
                quota_state_path = repo_root / "data/phase-2/quota-state.json"
                registry = registry_module.load_registry(registry_path)
                desired = task_reconciler.build_desired_task_identities(repo_root=repo_root, registry=registry)
                state = task_state_module.load_task_state(task_state_path)
                state["tasks"].pop(next(iter(desired)))
                task_state_module.write_task_state(task_state_path, state)
                task_before = task_state_path.read_bytes()
                quota_before = quota_state_path.read_bytes()

                work_plan_root = repo_root / "work-plans"
                output = io.StringIO()
                with redirect_stdout(output):
                    result = task_scheduler.main(
                        [
                            command,
                            "--repo-root",
                            str(repo_root),
                            "--workflow-run-id",
                            f"{command}-workflow",
                            "--reconcile",
                            "--timestamp",
                            TIMESTAMP,
                            "--max-tasks-per-provider",
                            "1",
                            "--work-plan-root",
                            str(work_plan_root),
                        ]
                    )

                self.assertEqual(result, 0)
                self.assertEqual(task_state_path.read_bytes(), task_before)
                self.assertEqual(quota_state_path.read_bytes(), quota_before)
                self.assertIn("state_written=false", output.getvalue())
                self.assertTrue(any(work_plan_root.glob("*.json")))


class LeaseRecoveryTests(unittest.TestCase):
    def leased(self) -> tuple[dict[str, object], dict[str, object]]:
        record = task_record("groq", "openai/gpt-oss-20b", "page.md", status="leased")
        record["attempt_count"] = 1
        record["lease"] = {
            "attempt_id": "attempt-1",
            "attempt_number": 1,
            "workflow_run_id": "workflow-1",
            "worker_id": "groq",
            "leased_at": "2026-08-12T12:00:00Z",
            "expires_at": "2026-08-12T13:00:00Z",
        }
        return record, state_with(record)

    def test_expired_not_called_lease_waits_for_validated_aggregation(self) -> None:
        record, state = self.leased()
        with tempfile.TemporaryDirectory() as temporary:
            event_root = Path(temporary)
            event_path = event_root / "worker" / "event.json"
            event_path.parent.mkdir()
            event = terminal_event(record, "not_called", 0)
            event.pop("_event_path")
            event_path.write_text(json.dumps(event), encoding="utf-8")
            loaded = task_scheduler.load_terminal_events(event_root)
        self.assertEqual(loaded[0]["_event_path"], "worker/event.json")
        counts = task_scheduler.recover_expired_leases(state, loaded, now=NOW)
        self.assertEqual(record["status"], "leased")
        self.assertEqual(record["last_outcome"]["kind"], "replayable_result")
        self.assertEqual(record["last_outcome"]["outcome"], "not_called")
        self.assertEqual(counts["replayable_result"], 1)

    def test_expired_replayable_result_is_retained_without_recall(self) -> None:
        record, state = self.leased()
        counts = task_scheduler.recover_expired_leases(state, [terminal_event(record, "valid", 1)], now=NOW)
        self.assertEqual(record["status"], "leased")
        self.assertEqual(record["last_outcome"]["kind"], "replayable_result")
        self.assertEqual(counts["replayable_result"], 1)

    def test_expired_lease_without_evidence_is_blocked_ambiguous(self) -> None:
        record, state = self.leased()
        counts = task_scheduler.recover_expired_leases(state, [], now=NOW)
        self.assertEqual(record["status"], "blocked_ambiguous_attempt")
        self.assertEqual(counts["blocked_ambiguous"], 1)


class ProviderWorkerTests(unittest.TestCase):
    def assignment(self, model: str = "openai/gpt-oss-20b", suffix: str = "1") -> dict[str, object]:
        return {
            "task_id": f"task-{suffix}",
            "attempt_id": f"attempt-{suffix}",
            "attempt_number": 1,
            "identity": identity("groq", model, f"page-{suffix}.md"),
            "quota_groups": ["groq-organization", f"groq:{model}"],
            "max_completion_tokens": 3000,
        }

    def plan(self, assignments: list[dict[str, object]], concurrency: int = 1) -> dict[str, object]:
        return {
            "plan_version": 1,
            "workflow_run_id": "workflow-1",
            "worker_id": "groq",
            "provider": "groq",
            "lease_commit_sha": "lease-sha",
            "created_at": TIMESTAMP,
            "execution_budget_seconds": 720,
            "initial_concurrency": concurrency,
            "assignments": assignments,
        }

    def quota_observation(self, task_id: str, *, sent: bool = True, failure=None) -> dict[str, object]:
        return {
            "task_id": task_id,
            "request_sent": sent,
            "usage": {"input_tokens": 1, "output_tokens": 2, "total_tokens": 3},
            "headers": {},
            "failure": failure,
            "model": "openai/gpt-oss-20b",
        }

    def test_stale_worker_refuses_before_provider_call(self) -> None:
        with self.assertRaises(provider_worker.ProviderWorkerError):
            provider_worker.validate_assignment(
                plan=self.plan([]),
                provider="groq",
                task_state={"tasks": {}},
                quota_state={},
                registry=mock.Mock(),
                checkout_sha="different-sha",
                now=NOW,
            )

    def test_transient_retry_sequence_emits_one_event_with_two_attempts(self) -> None:
        assignment = self.assignment()
        plan = self.plan([assignment])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            def runner(command, **kwargs):
                output = Path(command[command.index("--output") + 1])
                output.write_text("| Signal count | 0 |\n", encoding="utf-8")
                event_root = Path(kwargs["env"]["PHASE2_QUOTA_EVENT_DIR"])
                for index in range(2):
                    value = self.quota_observation(str(assignment["task_id"]))
                    (event_root / f"event-{index}.json").write_text(json.dumps(value), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            event = provider_worker.execute_assignment(
                plan=plan,
                assignment=assignment,
                repo_root=root,
                result_root=root / "results",
                output_root=root / "outputs",
                quota_event_root=root / "quota",
                runner=runner,
            )
        self.assertEqual(event["provider_attempts"], 2)
        self.assertEqual(event["outcome"], "valid")
        self.assertFalse(Path(event["output_artifact"]).is_absolute())

    def test_missing_request_observations_make_attempt_ambiguous(self) -> None:
        assignment = self.assignment()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(provider_worker.AmbiguousProviderAttemptError):
                provider_worker.execute_assignment(
                    plan=self.plan([assignment]),
                    assignment=assignment,
                    repo_root=root,
                    result_root=root / "results",
                    output_root=root / "outputs",
                    quota_event_root=root / "quota",
                    runner=lambda command, **kwargs: subprocess.CompletedProcess(command, 2, "", "failed"),
                )

    def test_explicit_request_sent_false_permits_not_called_event(self) -> None:
        assignment = self.assignment()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            def runner(command, **kwargs):
                event_root = Path(kwargs["env"]["PHASE2_QUOTA_EVENT_DIR"])
                value = self.quota_observation(str(assignment["task_id"]), sent=False)
                (event_root / "event.json").write_text(json.dumps(value), encoding="utf-8")
                return subprocess.CompletedProcess(command, 2, "", "missing key")

            event = provider_worker.execute_assignment(
                plan=self.plan([assignment]),
                assignment=assignment,
                repo_root=root,
                result_root=root / "results",
                output_root=root / "outputs",
                quota_event_root=root / "quota",
                runner=runner,
            )
        self.assertEqual(event["outcome"], "not_called")
        self.assertEqual(event["provider_attempts"], 0)

    def test_quota_exhaustion_stops_remaining_group_work(self) -> None:
        first, second = self.assignment(suffix="1"), self.assignment(suffix="2")
        calls: list[str] = []

        def execute(**kwargs):
            assignment = kwargs["assignment"]
            calls.append(str(assignment["task_id"]))
            return {
                **provider_worker._base_event(kwargs["plan"], assignment),
                "outcome": "provider_failure",
                "quota_observations": [
                    self.quota_observation(
                        str(assignment["task_id"]),
                        failure={
                            "kind": "rate_or_quota_limited",
                            "scope": "model",
                            "quota_group_ids": ["groq:openai/gpt-oss-20b"],
                        },
                    )
                ],
            }

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            counts = provider_worker.execute_plan(
                plan=self.plan([first, second]),
                repo_root=root,
                result_root=root / "results",
                output_root=root / "outputs",
                quota_event_root=root / "quota",
                execute=execute,
                now=lambda: NOW,
            )
        self.assertEqual(calls, ["task-1"])
        self.assertEqual(counts["not_called"], 1)

    def test_model_unavailability_does_not_stop_an_unaffected_model(self) -> None:
        first = self.assignment(suffix="1")
        second = self.assignment(suffix="2")
        other = self.assignment(model="qwen/qwen3-32b", suffix="3")
        calls: list[str] = []

        def execute(**kwargs):
            assignment = kwargs["assignment"]
            calls.append(str(assignment["task_id"]))
            failure = None
            if assignment["task_id"] == "task-1":
                failure = {"kind": "provider_unavailable", "scope": "slot", "quota_group_ids": []}
            return {
                **provider_worker._base_event(kwargs["plan"], assignment),
                "outcome": "provider_failure" if failure else "valid",
                "quota_observations": [self.quota_observation(str(assignment["task_id"]), failure=failure)],
            }

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            counts = provider_worker.execute_plan(
                plan=self.plan([first, second, other], concurrency=2),
                repo_root=root,
                result_root=root / "results",
                output_root=root / "outputs",
                quota_event_root=root / "quota",
                execute=execute,
                now=lambda: NOW,
            )
        self.assertIn("task-3", calls)
        self.assertNotIn("task-2", calls)
        self.assertEqual(counts["not_called"], 1)

    def test_ambiguous_attempt_marks_only_unstarted_tasks_not_called(self) -> None:
        first, second = self.assignment(suffix="1"), self.assignment(suffix="2")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(provider_worker.AmbiguousProviderAttemptError):
                provider_worker.execute_plan(
                    plan=self.plan([first, second]),
                    repo_root=root,
                    result_root=root / "results",
                    output_root=root / "outputs",
                    quota_event_root=root / "quota",
                    execute=lambda **kwargs: (_ for _ in ()).throw(RuntimeError("crash without call evidence")),
                    now=lambda: NOW,
                )
            self.assertFalse(provider_worker.result_event_path(root / "results", first).exists())
            second_event = json.loads(provider_worker.result_event_path(root / "results", second).read_text())
        self.assertEqual(second_event["outcome"], "not_called")


class ResolverAndWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = registry_module.load_registry(REGISTRY_PATH)

    def eligibility(
        self,
        quota: dict[str, object],
        issue=1,
        attempt_state: dict[str, object] | None = None,
    ) -> resolver.ResolverEligibility:
        issue_snapshot = resolver.IssueSnapshot(
            number=1,
            title="Check signal: language-style-checker: classes/example",
            body="",
            state="OPEN",
            url="https://github.com/example/repository/issues/1",
            agent="language-style-checker",
            reviewed_page="docs/stereotypes/classes/example.md",
            comments=[],
        )
        primary = resolver.build_resolver_attempt_context(
            issue=issue_snapshot,
            page_text="Current page.\n",
            prompt="Resolver prompt.\n",
            active_comments=(resolver.ActiveSignalComment("1", "a" * 64, "gemini", "gemini-3.5-flash", "Signal."),),
            provider="gemini",
            model="gemini-3.5-flash",
            max_completion_tokens=8000,
            max_attempts=1,
        )
        with (
            mock.patch.object(resolver, "open_signal_issue_candidates", return_value=[] if issue is None else [issue]),
            mock.patch.object(resolver, "read_issue", return_value=issue_snapshot),
            mock.patch.object(resolver, "attempt_context_for_issue", return_value=primary),
            mock.patch.object(
                resolver,
                "load_resolver_attempt_state",
                return_value=attempt_state or resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP),
            ),
            mock.patch.object(resolver, "load_task_state", return_value={"tasks": {}}),
            mock.patch.object(resolver, "load_registry", return_value=self.registry),
            mock.patch.object(resolver, "load_quota_state", return_value=quota),
            mock.patch.object(resolver, "load_event_files", return_value=[]),
        ):
            return resolver.evaluate_resolver_work("owner/repo", now=NOW)

    def preflight(self, quota: dict[str, object], issue=1) -> bool:
        return self.eligibility(quota, issue=issue).capacity_required

    def test_no_open_issue_means_no_resolver_capacity_reservation(self) -> None:
        quota = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)
        self.assertFalse(self.preflight(quota, issue=None))

    def test_eligible_primary_resolver_work_reserves_shared_capacity(self) -> None:
        quota = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)
        self.assertTrue(self.preflight(quota))

    def test_quota_blocked_primary_does_not_reserve_fallback(self) -> None:
        quota = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)
        group = quota["quota_groups"]["gemini-project"]
        group["status"] = "deferred_quota"
        group["retry_not_before"] = "2026-08-12T15:00:00Z"
        self.assertFalse(self.preflight(quota))

    def test_unavailable_primary_reserves_eligible_fallback(self) -> None:
        quota = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)
        runtime = quota["runtime_slots"]["gemini:gemini-3.5-flash"]
        runtime["status"] = "temporarily_unavailable"
        runtime["retry_not_before"] = "2026-08-12T15:00:00Z"
        self.assertTrue(self.preflight(quota))

    def test_incident_state_is_deferred_without_capacity_or_provider_call(self) -> None:
        quota = quota_state.build_initial_state(self.registry, timestamp=TIMESTAMP)
        primary_runtime = quota["runtime_slots"]["gemini:gemini-3.5-flash"]
        primary_runtime["status"] = "temporarily_unavailable"
        primary_runtime["retry_not_before"] = "2026-08-12T13:00:00Z"
        eligibility = self.eligibility(quota)
        fallback = eligibility.fallback_context
        assert fallback is not None
        attempt_state = resolver_attempt_state.build_initial_state(timestamp=TIMESTAMP)
        attempt_state, _counts = resolver_attempt_state.aggregate_events(
            attempt_state,
            [
                {
                    "schema_version": resolver_attempt_state.SCHEMA_VERSION,
                    "event_id": "fallback-provider-failure",
                    "attempt_id": fallback.attempt_id,
                    "observed_at": TIMESTAMP,
                    "identity": fallback.identity,
                    "status": "provider_failure",
                    "request_sent": True,
                    "failure_kind": "provider_unavailable",
                }
            ],
        )

        incident = self.eligibility(quota, attempt_state=attempt_state)

        self.assertTrue(incident.candidate_exists)
        self.assertFalse(incident.primary_executable)
        self.assertFalse(incident.fallback_executable)
        self.assertFalse(incident.capacity_required)
        self.assertIn("primary_slot_recheck_required", incident.reason_codes)
        self.assertIn("fallback_not_eligible", incident.reason_codes)

    def test_workflows_enforce_durable_leases_and_shared_state_writer(self) -> None:
        collector = (REPO_ROOT / ".github/workflows/check-agent-signal-collector.yml").read_text(encoding="utf-8")
        resolver_workflow = (REPO_ROOT / ".github/workflows/phase-2-signal-resolver.yml").read_text(encoding="utf-8")
        self.assertIn('cron: "7,27,47 * * * *"', collector)
        self.assertIn('task_scheduler.py" lease', collector)
        self.assertNotIn("python scripts/phase-2/task_reconciler.py validate", collector)
        self.assertIn("--lease-commit-sha", collector)
        self.assertIn("ref: ${{ needs.lease-and-plan.outputs.lease_sha }}", collector)
        self.assertIn("aggregate_task_results.py", collector)
        self.assertIn("Download recent replayable provider artifacts", collector)
        self.assertEqual(collector.count("group: phase-2-operational-state-write"), 3)
        self.assertGreaterEqual(collector.count("scripts/phase-2/state_writer.py"), 3)
        self.assertIn("group: phase-2-operational-state-write", resolver_workflow)
        self.assertIn("scripts/phase-2/state_writer.py", resolver_workflow)
        self.assertNotIn("phase-2-operational-state-write-${{ github.ref }}", resolver_workflow)


if __name__ == "__main__":
    unittest.main()
