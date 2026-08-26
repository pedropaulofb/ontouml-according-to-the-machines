from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

import aggregate_task_results as aggregator  # noqa: E402
import provider_model_registry  # noqa: E402
import quota_state  # noqa: E402
import state_writer  # noqa: E402
import task_scheduler  # noqa: E402
import task_state  # noqa: E402
import update_model_run_statistics as statistics  # noqa: E402

TIMESTAMP = "2026-08-17T12:00:00Z"


class AggregationFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = provider_model_registry.load_registry(REPO_ROOT / "config/phase-2/provider-models.json")
        self.slot = self.registry.executable_slots[0]
        self.quota = quota_state.build_initial_state(self.registry, timestamp="2026-08-17T11:00:00Z")

    def identity(self, suffix: str = "1") -> dict[str, str]:
        return {
            "page": f"docs/stereotypes/classes/page-{suffix}.md",
            "agent": "page-hygiene-checker",
            "provider": self.slot.provider,
            "model": self.slot.model,
            "page_content_sha256": "a" * 64,
            "prompt_id": "prompt",
            "prompt_sha256": "b" * 64,
            "validator_version": "1",
            "request_config_sha256": "c" * 64,
        }

    def leased_task(self, suffix: str = "1", attempt: int = 1) -> dict[str, object]:
        record = task_state.new_task_record(
            task_id=f"task-{suffix}",
            identity=self.identity(suffix),
            timestamp="2026-08-17T10:00:00Z",
            source_commit_sha="commit",
        )
        record["status"] = "leased"
        record["attempt_count"] = attempt
        record["last_attempt_at"] = "2026-08-17T11:50:00Z"
        record["lease"] = {
            "attempt_id": f"attempt-{suffix}-{attempt}",
            "attempt_number": attempt,
            "workflow_run_id": "workflow-1",
            "worker_id": self.slot.provider,
            "leased_at": "2026-08-17T11:50:00Z",
            "expires_at": "2026-08-17T12:50:00Z",
        }
        return record

    def state_with(self, *records: dict[str, object]) -> dict[str, object]:
        state = task_state.new_task_state(registry_sha256="d" * 64, timestamp="2026-08-17T10:00:00Z")
        state["tasks"] = {record["task_id"]: record for record in records}
        return state

    def event(
        self,
        record: dict[str, object],
        *,
        outcome: str = "valid",
        signal_count: int = 1,
        provider_attempts: int = 1,
        observations: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        lease = record["lease"]
        identity = record["identity"]
        assert isinstance(lease, dict) and isinstance(identity, dict)
        return {
            "event_version": 1,
            "task_id": record["task_id"],
            "attempt_id": lease["attempt_id"],
            "workflow_run_id": lease["workflow_run_id"],
            "worker_id": lease["worker_id"],
            "provider": identity["provider"],
            "model": identity["model"],
            "attempt_started_at": "2026-08-17T11:55:00Z",
            "attempt_finished_at": TIMESTAMP,
            "outcome": outcome,
            "signal_count": signal_count if outcome == "valid" else 0,
            "provider_attempts": provider_attempts,
            "usage": {
                "input_tokens": 10,
                "output_tokens": 0,
                "total_tokens": 10,
                "reasoning_tokens": None,
                "cached_tokens": 0,
            },
            "quota_observations": observations or [],
            "output_sha256": None,
            "output_artifact": None,
        }

    def quota_event(self, record: dict[str, object], *, failure=None) -> dict[str, object]:
        identity = record["identity"]
        assert isinstance(identity, dict)
        return {
            "schema_version": 1,
            "event_id": f"quota-{record['task_id']}-{failure and failure.get('kind') or 'success'}",
            "observed_at": TIMESTAMP,
            "call_source": "signal",
            "provider": identity["provider"],
            "model": identity["model"],
            "task_id": record["task_id"],
            "outcome": "failure" if failure else "success",
            "request_sent": True,
            "headers": {},
            "usage": {"input_tokens": 10, "output_tokens": 0, "total_tokens": 10},
            "failure": failure,
        }

    def write_transport(
        self,
        root: Path,
        event: dict[str, object],
        *,
        content: str = "valid output",
        provider_directory: str = "worker",
        filename: str | None = None,
    ) -> None:
        base = root / provider_directory
        if event["outcome"] in {"valid", "validator_rejected"}:
            suffix = ".invalid.md" if event["outcome"] == "validator_rejected" else ".md"
            output = base / "worker-output" / str(event["provider"]) / f"{event['attempt_id']}{suffix}"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content, encoding="utf-8")
            event["output_sha256"] = hashlib.sha256(content.encode()).hexdigest()
            event["output_artifact"] = f".tmp/phase-2/worker-output/{event['provider']}/{event['attempt_id']}{suffix}"
        event_path = base / "result-events" / (filename or f"{event['attempt_id']}.json")
        event_path.parent.mkdir(parents=True, exist_ok=True)
        event_path.write_text(json.dumps(event), encoding="utf-8")

    def run_aggregate(self, root: Path, tasks: dict[str, object], publisher=None):
        return aggregator.aggregate(
            repo_root=root,
            artifact_root=root / "artifacts",
            registry=self.registry,
            task_state=tasks,
            quota_state=self.quota,
            publisher=publisher,
            timestamp=TIMESTAMP,
        )


class ResultAggregationTests(AggregationFixture):
    def test_valid_zero_signal_completes_and_observes_empty_publication_policy(self) -> None:
        record = self.leased_task()
        event = self.event(record, signal_count=0)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, _quota, counts, _events = self.run_aggregate(
                root,
                self.state_with(record),
                publisher=lambda _task, _output: aggregator.PublicationResult("not_required"),
            )
            updated = tasks["tasks"][record["task_id"]]
            self.assertEqual(updated["status"], "completed")
            self.assertEqual(updated["publication"]["status"], "not_required")
            self.assertTrue((root / updated["result_record"]["event_path"]).is_file())
            self.assertTrue((root / updated["result_record"]["validated_output_path"]).is_file())
            self.assertEqual(updated["result_record"]["attempt_id"], event["attempt_id"])
            self.assertEqual(updated["result_record"]["source_event_sha256"], aggregator._canonical_sha256(event))
            self.assertEqual(counts["applied"], 1)

    def test_publication_failure_retries_without_reapplying_the_terminal_event(self) -> None:
        record = self.leased_task()
        event = self.event(record)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, quota, _counts, _events = self.run_aggregate(
                root,
                self.state_with(record),
                publisher=lambda _task, _output: aggregator.PublicationResult("retry_due", "temporary failure"),
            )
            self.assertEqual(tasks["tasks"][record["task_id"]]["status"], "completed")
            self.assertEqual(tasks["tasks"][record["task_id"]]["publication"]["status"], "retry_due")
            empty = root / "empty-artifacts"
            retried_tasks, _quota, counts, accepted = aggregator.aggregate(
                repo_root=root,
                artifact_root=empty,
                registry=self.registry,
                task_state=tasks,
                quota_state=quota,
                publisher=lambda _task, _output: aggregator.PublicationResult("published"),
                timestamp=TIMESTAMP,
            )
            self.assertEqual(accepted, [])
            self.assertEqual(counts["applied"], 0)
            self.assertEqual(retried_tasks["tasks"][record["task_id"]]["publication"]["status"], "published")

    def test_duplicate_delivery_is_idempotent_without_durable_event_file(self) -> None:
        record = self.leased_task()
        event = self.event(record)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, quota, _counts, _events = self.run_aggregate(root, self.state_with(record))
            durable_event_path = root / tasks["tasks"][record["task_id"]]["result_record"]["event_path"]
            durable_event_path.unlink()

            tasks_again, _quota, counts, accepted = aggregator.aggregate(
                repo_root=root,
                artifact_root=root / "artifacts",
                registry=self.registry,
                task_state=tasks,
                quota_state=quota,
                timestamp=TIMESTAMP,
            )
            self.assertEqual(counts["duplicate"], 1)
            self.assertEqual(accepted, [])
            self.assertEqual(tasks_again, tasks)

    def test_conflicting_replay_uses_state_identity_without_durable_event_file(self) -> None:
        record = self.leased_task()
        event = self.event(record)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            self.write_transport(artifacts, event)
            tasks, quota, _counts, _events = self.run_aggregate(root, self.state_with(record))
            durable_event_path = root / tasks["tasks"][record["task_id"]]["result_record"]["event_path"]
            durable_event_path.unlink()

            conflicting = copy.deepcopy(event)
            conflicting["attempt_finished_at"] = "2026-08-17T12:00:01Z"
            self.write_transport(artifacts, conflicting)
            tasks_again, _quota, counts, accepted = aggregator.aggregate(
                repo_root=root,
                artifact_root=artifacts,
                registry=self.registry,
                task_state=tasks,
                quota_state=quota,
                timestamp=TIMESTAMP,
            )
            self.assertEqual(tasks_again, tasks)
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(counts["actionable_rejected"], 1)
            self.assertEqual(counts["stale_replay"], 0)
            self.assertEqual(accepted, [])

    def test_legacy_duplicate_delivery_still_uses_event_path(self) -> None:
        record = self.leased_task()
        event = self.event(record)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, quota, _counts, _events = self.run_aggregate(root, self.state_with(record))
            legacy_tasks = copy.deepcopy(tasks)
            result_record = legacy_tasks["tasks"][record["task_id"]]["result_record"]
            result_record.pop("attempt_id")
            result_record.pop("source_event_sha256")

            tasks_again, _quota, counts, accepted = aggregator.aggregate(
                repo_root=root,
                artifact_root=root / "artifacts",
                registry=self.registry,
                task_state=legacy_tasks,
                quota_state=quota,
                timestamp=TIMESTAMP,
            )
            self.assertEqual(counts["duplicate"], 1)
            self.assertEqual(accepted, [])
            self.assertEqual(tasks_again, legacy_tasks)

    def test_prior_result_identity_does_not_block_a_new_leased_attempt(self) -> None:
        record = self.leased_task()
        first = self.event(record, outcome="not_called", provider_attempts=0)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            self.write_transport(artifacts, first)
            tasks, quota, _counts, _events = self.run_aggregate(root, self.state_with(record))

            shutil.rmtree(artifacts)
            updated = tasks["tasks"][record["task_id"]]
            updated["status"] = "leased"
            updated["attempt_count"] = 2
            updated["last_attempt_at"] = "2026-08-17T12:10:00Z"
            updated["lease"] = {
                "attempt_id": "attempt-1-2",
                "attempt_number": 2,
                "workflow_run_id": "workflow-2",
                "worker_id": self.slot.provider,
                "leased_at": "2026-08-17T12:10:00Z",
                "expires_at": "2026-08-17T13:10:00Z",
            }
            second = self.event(updated, outcome="not_called", provider_attempts=0)
            self.write_transport(artifacts, second)

            tasks_again, _quota, counts, accepted = aggregator.aggregate(
                repo_root=root,
                artifact_root=artifacts,
                registry=self.registry,
                task_state=tasks,
                quota_state=quota,
                timestamp=TIMESTAMP,
            )
            result_record = tasks_again["tasks"][record["task_id"]]["result_record"]
            self.assertEqual(counts["applied"], 1)
            self.assertEqual(len(accepted), 1)
            self.assertEqual(result_record["attempt_id"], "attempt-1-2")
            self.assertEqual(result_record["source_event_sha256"], aggregator._canonical_sha256(second))

    def test_recovered_not_called_is_persisted_before_returning_pending(self) -> None:
        record = self.leased_task()
        record["lease"]["expires_at"] = "2026-08-17T11:59:00Z"
        event = self.event(record, outcome="not_called", provider_attempts=0)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            recovered = self.state_with(record)
            loaded = task_scheduler.load_terminal_events(root / "artifacts")
            recovery_counts = task_scheduler.recover_expired_leases(
                recovered,
                loaded,
                now=task_scheduler.parse_timestamp(TIMESTAMP),
            )
            self.assertEqual(record["status"], "leased")
            self.assertEqual(recovery_counts["replayable_result"], 1)

            tasks, _quota, counts, accepted = self.run_aggregate(root, recovered)
            updated = tasks["tasks"][record["task_id"]]
            self.assertEqual(updated["status"], "pending")
            self.assertIsNone(updated["lease"])
            self.assertTrue((root / updated["result_record"]["event_path"]).is_file())
            self.assertEqual(counts["applied"], 1)
            self.assertEqual(len(accepted), 1)

    def test_mismatched_lease_event_is_rejected_without_state_mutation(self) -> None:
        record = self.leased_task()
        original = self.state_with(record)
        event = self.event(record)
        event["attempt_id"] = "wrong-attempt"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, _quota, counts, accepted = self.run_aggregate(root, original)
            self.assertEqual(tasks, original)
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(accepted, [])

    def test_stale_event_is_rejected_without_state_mutation(self) -> None:
        record = self.leased_task()
        event = self.event(record)
        record["status"] = "pending"
        record["lease"] = None
        original = self.state_with(record)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, _quota, counts, accepted = self.run_aggregate(root, original)
            self.assertEqual(tasks, original)
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(accepted, [])

    def test_conflicting_terminal_events_for_one_attempt_are_both_rejected(self) -> None:
        record = self.leased_task()
        first = self.event(record)
        second = copy.deepcopy(first)
        second["attempt_finished_at"] = "2026-08-17T12:00:01Z"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            self.write_transport(artifacts, first, filename="first.json")
            self.write_transport(artifacts, second, filename="second.json", content="other output")
            tasks, _quota, counts, accepted = self.run_aggregate(root, self.state_with(record))
            self.assertEqual(tasks["tasks"][record["task_id"]]["status"], "leased")
            self.assertEqual(counts["rejected"], 2)
            self.assertEqual(accepted, [])

    def test_invalid_event_does_not_discard_another_provider_result(self) -> None:
        first = self.leased_task("1")
        second = self.leased_task("2")
        good = self.event(first)
        invalid = self.event(second)
        invalid["provider_attempts"] = 0
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            self.write_transport(artifacts, good, provider_directory="good")
            self.write_transport(artifacts, invalid, provider_directory="bad")
            tasks, _quota, counts, accepted = self.run_aggregate(root, self.state_with(first, second))
            self.assertEqual(tasks["tasks"][first["task_id"]]["status"], "completed")
            self.assertEqual(tasks["tasks"][second["task_id"]]["status"], "leased")
            self.assertEqual(counts["applied"], 1)
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(len(accepted), 1)

    def test_missing_provider_artifact_does_not_discard_available_provider_result(self) -> None:
        available = self.leased_task("1")
        missing = self.leased_task("2")
        event = self.event(available)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, _quota, counts, accepted = self.run_aggregate(root, self.state_with(available, missing))
            self.assertEqual(tasks["tasks"][available["task_id"]]["status"], "completed")
            self.assertEqual(tasks["tasks"][missing["task_id"]]["status"], "leased")
            self.assertEqual(counts["applied"], 1)
            self.assertEqual(len(accepted), 1)

    def test_quota_failure_defers_task_and_updates_quota_state(self) -> None:
        record = self.leased_task()
        failure = {
            "kind": "rate_or_quota_limited",
            "scope": "quota_group",
            "quota_group_ids": [self.slot.quota_groups[-1]],
            "retryable_immediately": False,
            "retry_after_seconds": 3600,
            "retry_not_before": "2026-08-17T13:00:00Z",
            "retry_source": "inferred",
            "diagnostic": "quota",
        }
        observation = self.quota_event(record, failure=failure)
        event = self.event(record, outcome="provider_failure", observations=[observation])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, quota, _counts, _events = self.run_aggregate(root, self.state_with(record))
            self.assertEqual(tasks["tasks"][record["task_id"]]["status"], "deferred_quota")
            self.assertEqual(tasks["tasks"][record["task_id"]]["lease"], None)
            self.assertIn(observation["event_id"], quota["processed_event_ids"])

    def test_second_validator_rejection_blocks_unchanged_task(self) -> None:
        record = self.leased_task(attempt=2)
        record["validation_rejection_count"] = 1
        event = self.event(record, outcome="validator_rejected")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event)
            tasks, _quota, _counts, _events = self.run_aggregate(root, self.state_with(record))
            updated = tasks["tasks"][record["task_id"]]
            self.assertEqual(updated["validation_rejection_count"], 2)
            self.assertEqual(updated["status"], "blocked_repeated_rejection")

    def test_validator_rejected_output_preserves_bytes_and_sha256(self) -> None:
        record = self.leased_task()
        event = self.event(record, outcome="validator_rejected")
        content = "validator-rejected output with trailing whitespace   "
        expected_bytes = content.encode("utf-8")
        expected_sha256 = hashlib.sha256(expected_bytes).hexdigest()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_transport(root / "artifacts", event, content=content)
            tasks, _quota, counts, _events = self.run_aggregate(root, self.state_with(record))

            updated = tasks["tasks"][record["task_id"]]
            durable_event_path = root / updated["result_record"]["event_path"]
            durable_event = json.loads(durable_event_path.read_text(encoding="utf-8"))
            durable_output_path = root / durable_event["output_artifact"]
            durable_bytes = durable_output_path.read_bytes()

            self.assertEqual(counts["applied"], 1)
            self.assertTrue(durable_output_path.name.endswith(".invalid.md"))
            self.assertEqual(durable_bytes, expected_bytes)
            self.assertTrue(durable_bytes.endswith(b"   "))
            self.assertEqual(durable_event["output_sha256"], expected_sha256)
            self.assertEqual(updated["result_record"]["output_sha256"], expected_sha256)
            self.assertEqual(hashlib.sha256(durable_bytes).hexdigest(), expected_sha256)


class StatisticsTests(AggregationFixture):
    def test_token_zero_is_distinct_from_unknown(self) -> None:
        state = statistics.empty_state()
        record = self.leased_task()
        known = self.event(record)
        unknown_record = self.leased_task("2")
        unknown = self.event(unknown_record)
        unknown["usage"] = {field: None for field in aggregator.USAGE_FIELDS}
        statistics.apply_terminal_events(state, [known, unknown])
        rendered = statistics.render_markdown(state)
        known_stats = state["models"][f"{self.slot.provider}:{self.slot.model}"]
        self.assertEqual(known_stats["output_tokens"], 0)
        self.assertGreater(known_stats["output_tokens_known_events"], 0)
        self.assertIn("`unknown`", rendered)

    def test_refresh_excludes_pre_recalibration_only_rows_and_sums_queue(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "statistics.md"
            shutil.copy2(REPO_ROOT / statistics.DEFAULT_STATISTICS_PAGE, page)
            tasks = task_state.load_task_state(REPO_ROOT / "data/phase-2/task-state.json")
            quota = quota_state.load_state(REPO_ROOT / "data/phase-2/quota-state.json", self.registry)
            statistics.refresh_queue_statistics(
                statistics_page=page,
                registry=self.registry,
                task_state=tasks,
                quota_state=quota,
                terminal_events=[],
                timestamp_utc=TIMESTAMP,
            )
            state = statistics.load_state(page)
            self.assertNotIn("cerebras:gpt-oss-120b", state["models"])
            self.assertNotIn("openrouter:poolside/laguna-m.1:free", state["models"])
            queue = state["queue"]
            status_total = sum(value for key, value in queue.items() if key != "desired_task_count")
            self.assertEqual(status_total, len(tasks["tasks"]))
            self.assertEqual(queue["desired_task_count"], 1950)


class StateWriterTests(unittest.TestCase):
    def git(self, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=True)

    def test_non_fast_forward_reapplies_without_losing_other_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote = root / "remote.git"
            source = root / "source"
            rival = root / "rival"
            self.git("init", "--bare", str(remote), cwd=root)
            self.git("clone", str(remote), str(source), cwd=root)
            self.git("config", "user.name", "Test", cwd=source)
            self.git("config", "user.email", "test@example.com", cwd=source)
            (source / "seed.txt").write_text("seed\n", encoding="utf-8")
            self.git("add", "seed.txt", cwd=source)
            self.git("commit", "-m", "seed", cwd=source)
            self.git("branch", "-M", "main", cwd=source)
            self.git("push", "-u", "origin", "main", cwd=source)
            self.git("clone", "--branch", "main", str(remote), str(rival), cwd=root)
            self.git("config", "user.name", "Rival", cwd=rival)
            self.git("config", "user.email", "rival@example.com", cwd=rival)

            pushed_conflict = False

            def runner(command, **kwargs):
                nonlocal pushed_conflict
                if command[:2] == ["git", "push"] and not pushed_conflict:
                    pushed_conflict = True
                    (rival / "other.txt").write_text("other\n", encoding="utf-8")
                    self.git("add", "other.txt", cwd=rival)
                    self.git("commit", "-m", "rival", cwd=rival)
                    self.git("push", "origin", "main", cwd=rival)
                return subprocess.run(command, **kwargs)

            result = state_writer.run_state_write(
                repo_root=source,
                branch="main",
                remote="origin",
                push_url=str(remote),
                commit_message="apply state",
                add_paths=["state.txt"],
                apply_command=[
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path('state.txt').write_text('applied\\n', encoding='utf-8')",
                ],
                runner=runner,
            )
            self.assertEqual(result.attempts, 2)
            verify = root / "verify"
            self.git("clone", "--branch", "main", str(remote), str(verify), cwd=root)
            self.assertEqual((verify / "state.txt").read_text(encoding="utf-8"), "applied\n")
            self.assertEqual((verify / "other.txt").read_text(encoding="utf-8"), "other\n")

    def test_unrecoverable_push_failure_preserves_replay_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote = root / "remote.git"
            source = root / "source"
            replay = root / "replay" / "attempt.json"
            self.git("init", "--bare", str(remote), cwd=root)
            self.git("clone", str(remote), str(source), cwd=root)
            self.git("config", "user.name", "Test", cwd=source)
            self.git("config", "user.email", "test@example.com", cwd=source)
            (source / "seed.txt").write_text("seed\n", encoding="utf-8")
            self.git("add", "seed.txt", cwd=source)
            self.git("commit", "-m", "seed", cwd=source)
            self.git("branch", "-M", "main", cwd=source)
            self.git("push", "-u", "origin", "main", cwd=source)
            replay.parent.mkdir(parents=True)
            replay.write_text('{"attempt_id":"attempt-1"}\n', encoding="utf-8")

            def runner(command, **kwargs):
                if command[:2] == ["git", "push"]:
                    return subprocess.CompletedProcess(command, 1, "", "rejected")
                return subprocess.run(command, **kwargs)

            with self.assertRaises(state_writer.StateWriterError):
                state_writer.run_state_write(
                    repo_root=source,
                    branch="main",
                    remote="origin",
                    push_url=str(remote),
                    commit_message="apply state",
                    add_paths=["state.txt"],
                    apply_command=[
                        sys.executable,
                        "-c",
                        "from pathlib import Path; Path('state.txt').write_text('applied\\n', encoding='utf-8')",
                    ],
                    runner=runner,
                )
            self.assertTrue(replay.is_file())
            self.assertFalse((source / "state.txt").exists())


if __name__ == "__main__":
    unittest.main()
