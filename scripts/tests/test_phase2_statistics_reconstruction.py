from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

import event_history  # noqa: E402
import reconstruct_statistics_state as reconstruction  # noqa: E402
import update_model_run_statistics as statistics  # noqa: E402


class DummySlot:
    provider = "gemini"
    model = "model-a"
    spec = "gemini:model-a"
    configuration_status = "configured"
    execution_status = "eligible"
    lifecycle = "stable"
    quota_groups: tuple[str, ...] = ()


class DummyRegistry:
    _slot = DummySlot()
    configured_slots: tuple[object, ...] = (_slot,)
    slots: tuple[object, ...] = (_slot,)

    def find(self, provider: str, model: str) -> object | None:
        if (provider, model) == ("gemini", "model-a"):
            return self._slot
        return None


class StatisticsReconstructionTests(unittest.TestCase):
    def event(
        self,
        *,
        task_id: str = "task-1",
        attempt_id: str = "attempt-1",
        provider_attempts: int = 1,
    ) -> dict[str, object]:
        return {
            "event_version": 1,
            "task_id": task_id,
            "attempt_id": attempt_id,
            "workflow_run_id": "workflow-1",
            "worker_id": "gemini",
            "provider": "gemini",
            "model": "model-a",
            "attempt_started_at": "2026-08-26T10:00:00Z",
            "attempt_finished_at": "2026-08-26T10:00:01Z",
            "outcome": "valid",
            "signal_count": 1,
            "provider_attempts": provider_attempts,
            "usage": {
                "input_tokens": 10,
                "output_tokens": 5,
                "total_tokens": 15,
                "reasoning_tokens": None,
                "cached_tokens": 0,
            },
            "quota_observations": [],
            "output_sha256": "a" * 64,
            "output_artifact": "data/phase-2/results/task-1/attempt-1.md",
        }

    def write_event(self, root: Path, event: dict[str, object]) -> Path:
        path = root / str(event["task_id"]) / f"{event['attempt_id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(event), encoding="utf-8")
        return path

    def reconstructed_state(self) -> dict[str, object]:
        state = statistics.empty_state()
        state["schema_version"] = statistics.QUEUE_STATISTICS_SCHEMA_VERSION
        state["generated_at"] = "2026-08-26T11:00:00Z"
        state["collection_start_utc"] = "2026-08-20T08:44:00Z"
        state["active_rotation"] = []
        state["queue"] = {"desired_task_count": 0}
        state["seen_terminal_events"] = {}
        state["seen_events"] = {}
        state["models"] = {}
        return state

    def test_load_result_events_validates_identity_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = self.event()
            self.write_event(root, expected)
            events, count = reconstruction.load_result_events(root, DummyRegistry())
            self.assertEqual(count, 1)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["attempt_id"], "attempt-1")

    def test_load_history_events_validates_compact_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = self.event()
            event_history.append_terminal_event(root, expected)
            events = reconstruction.load_history_events(root, DummyRegistry())
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["attempt_id"], "attempt-1")

    def test_merge_durable_events_deduplicates_equivalent_overlap(self) -> None:
        result_event = self.event()
        result_event["aggregation"] = {
            "source_event_sha256": "b" * 64,
            "transport_filename": "attempt-1.json",
        }
        history_event = copy.deepcopy(result_event)
        history_event["aggregation"] = {"source_event_sha256": "b" * 64}
        merged = reconstruction.merge_durable_events([result_event], [history_event])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["attempt_id"], "attempt-1")

    def test_merge_durable_events_rejects_conflicting_overlap(self) -> None:
        result_event = self.event()
        history_event = copy.deepcopy(result_event)
        history_event["signal_count"] = 2
        with self.assertRaises(reconstruction.ReconstructionError):
            reconstruction.merge_durable_events([result_event], [history_event])

    def test_merge_durable_events_rejects_conflicting_source_identity(self) -> None:
        result_event = self.event()
        result_event["aggregation"] = {"source_event_sha256": "b" * 64}
        history_event = copy.deepcopy(result_event)
        history_event["aggregation"] = {"source_event_sha256": "c" * 64}
        with self.assertRaises(reconstruction.ReconstructionError):
            reconstruction.merge_durable_events([result_event], [history_event])

    def test_collection_window_excludes_pre_start_and_includes_boundary(self) -> None:
        before = self.event(attempt_id="before")
        before["attempt_finished_at"] = "2026-08-20T08:43:59Z"
        boundary = self.event(attempt_id="boundary")
        boundary["attempt_finished_at"] = "2026-08-20T08:44:00Z"
        after = self.event(attempt_id="after")
        after["attempt_finished_at"] = "2026-08-20T08:44:01Z"

        included, excluded = reconstruction.filter_collection_window(
            [before, boundary, after],
            "2026-08-20T08:44:00Z",
        )

        self.assertEqual(excluded, 1)
        self.assertEqual([event["attempt_id"] for event in included], ["boundary", "after"])

    def test_collection_window_requires_valid_start_timestamp(self) -> None:
        with self.assertRaises(reconstruction.ReconstructionError):
            reconstruction.filter_collection_window([self.event()], None)
        with self.assertRaises(reconstruction.ReconstructionError):
            reconstruction.filter_collection_window([self.event()], "not-a-timestamp")

    def test_result_filename_must_match_attempt_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            event = self.event()
            path = root / "task-1" / "wrong-name.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(event), encoding="utf-8")
            with self.assertRaises(reconstruction.ReconstructionError):
                reconstruction.load_result_events(root, DummyRegistry())

    def test_duplicate_attempt_id_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = self.event(task_id="task-1", attempt_id="attempt-1")
            second = self.event(task_id="task-2", attempt_id="attempt-1")
            first["output_artifact"] = "data/phase-2/results/task-1/attempt-1.md"
            second["output_artifact"] = "data/phase-2/results/task-2/attempt-1.md"
            self.write_event(root, first)
            self.write_event(root, second)
            with self.assertRaises(reconstruction.ReconstructionError):
                reconstruction.load_result_events(root, DummyRegistry())

    def test_snapshot_verification_tolerates_later_task_only_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            statistics_path = root / "data/phase-2/statistics-state.json"
            result_path = root / "data/phase-2/results/task-1/attempt-1.json"
            history_path = root / "data/phase-2/history/terminal-events-2026-08.ndjson"
            task_path = root / "data/phase-2/task-state.json"
            for path, value in (
                (statistics_path, {"schema_version": 2}),
                (result_path, {"attempt_id": "attempt-1"}),
                (task_path, {"schema_version": 2, "tasks": {}}),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(value), encoding="utf-8")
            history_path.parent.mkdir(parents=True, exist_ok=True)
            history_path.write_text('{"attempt_id":"attempt-1"}\n', encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "statistics snapshot"], cwd=root, check=True)
            snapshot = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
            ).strip()

            task_path.write_text(
                json.dumps({"schema_version": 2, "tasks": {"leased": {}}}),
                encoding="utf-8",
            )
            subprocess.run(["git", "add", task_path.relative_to(root).as_posix()], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "lease work"], cwd=root, check=True)

            self.assertEqual(
                reconstruction._statistics_snapshot_commit(root, statistics_path),
                snapshot,
            )
            reconstruction.verify_result_tree_matches_snapshot(
                repo_root=root,
                snapshot_commit=snapshot,
                result_root=Path("data/phase-2/results"),
            )
            reconstruction.verify_history_tree_matches_snapshot(
                repo_root=root,
                snapshot_commit=snapshot,
                history_root=Path("data/phase-2/history"),
            )

    def test_snapshot_verification_rejects_later_history_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            statistics_path = root / "data/phase-2/statistics-state.json"
            statistics_path.parent.mkdir(parents=True, exist_ok=True)
            statistics_path.write_text('{"schema_version":2}', encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "statistics snapshot"], cwd=root, check=True)
            snapshot = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
            ).strip()

            history_path = root / "data/phase-2/history/terminal-events-2026-08.ndjson"
            history_path.parent.mkdir(parents=True, exist_ok=True)
            history_path.write_text('{"attempt_id":"attempt-1"}\n', encoding="utf-8")
            subprocess.run(["git", "add", history_path.relative_to(root).as_posix()], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "history only"], cwd=root, check=True)

            with self.assertRaises(reconstruction.ReconstructionError):
                reconstruction.verify_history_tree_matches_snapshot(
                    repo_root=root,
                    snapshot_commit=snapshot,
                    history_root=Path("data/phase-2/history"),
                )

    def test_reconstruction_rejects_legacy_batch_counters(self) -> None:
        canonical = self.reconstructed_state()
        canonical["seen_events"] = {"legacy": {"timestamp_utc": "2026-08-20T08:44:00Z"}}
        with self.assertRaises(reconstruction.ReconstructionError):
            reconstruction.reconstruct_statistics(
                canonical_state=canonical,
                registry=DummyRegistry(),
                task_state={"tasks": {}},
                quota_state={"runtime_slots": {}, "quota_groups": {}},
                terminal_events=[],
            )

    def test_compare_reconstruction_accepts_exact_reconstructible_state(self) -> None:
        canonical = self.reconstructed_state()
        reconstructed = copy.deepcopy(canonical)
        self.assertEqual(
            reconstruction.compare_reconstruction(canonical, reconstructed),
            [],
        )

    def test_compare_reconstruction_detects_provider_attempt_mismatch(self) -> None:
        canonical = self.reconstructed_state()
        record = statistics.ensure_model_record(
            canonical,
            statistics.ProviderModelSpec(provider="gemini", model="model-a"),
        )
        record["total_provider_attempts"] = 2
        reconstructed = copy.deepcopy(canonical)
        reconstructed["models"]["gemini:model-a"]["total_provider_attempts"] = 1
        mismatches = reconstruction.compare_reconstruction(canonical, reconstructed)
        self.assertTrue(
            any("total_provider_attempts" in mismatch for mismatch in mismatches),
            mismatches,
        )

    def test_reconstruct_statistics_rebuilds_event_and_queue_counters(self) -> None:
        canonical = self.reconstructed_state()
        event = self.event()
        task_state = {
            "tasks": {
                "task-1": {
                    "identity": {"provider": "gemini", "model": "model-a"},
                    "status": "completed",
                    "created_at": "2026-08-26T09:00:00Z",
                }
            }
        }
        result = reconstruction.reconstruct_statistics(
            canonical_state=canonical,
            registry=DummyRegistry(),
            task_state=task_state,
            quota_state={"runtime_slots": {}, "quota_groups": {}},
            terminal_events=[event],
        )
        record = result["models"]["gemini:model-a"]
        self.assertEqual(record["total_called"], 1)
        self.assertEqual(record["total_provider_attempts"], 1)
        self.assertEqual(record["valid_outputs"], 1)
        self.assertEqual(record["input_tokens"], 10)
        self.assertEqual(record["output_tokens"], 5)
        self.assertEqual(result["queue"]["desired_task_count"], 1)
        self.assertEqual(result["queue"]["completed"], 1)
        self.assertIn("attempt-1", result["seen_terminal_events"])

    def test_reconstruct_statistics_is_repository_read_only(self) -> None:
        canonical = self.reconstructed_state()
        before = copy.deepcopy(canonical)
        result = reconstruction.reconstruct_statistics(
            canonical_state=canonical,
            registry=DummyRegistry(),
            task_state={"tasks": {}},
            quota_state={"runtime_slots": {}, "quota_groups": {}},
            terminal_events=[],
        )
        self.assertEqual(canonical, before)
        self.assertEqual(result["schema_version"], statistics.QUEUE_STATISTICS_SCHEMA_VERSION)


if __name__ == "__main__":
    unittest.main()
