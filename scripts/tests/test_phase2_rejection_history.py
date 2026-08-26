from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import types
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

import event_history  # noqa: E402


class DummyRegistry:
    def find(self, provider: str, model: str) -> object | None:
        return object() if (provider, model) == ("gemini", "gemini-3.5-flash") else None


def _install_dependency_stubs() -> None:
    provider_model_registry = types.ModuleType("provider_model_registry")
    provider_model_registry.DEFAULT_REGISTRY_PATH = Path("config/phase-2/provider-models.json")
    provider_model_registry.ProviderModelRegistry = DummyRegistry
    provider_model_registry.load_registry = lambda _path: DummyRegistry()
    sys.modules[provider_model_registry.__name__] = provider_model_registry

    provider_runtime = types.ModuleType("provider_runtime")

    def parse_timestamp(value: str) -> datetime:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        return datetime.fromisoformat(normalized)

    provider_runtime.parse_timestamp = parse_timestamp
    provider_runtime.format_timestamp = lambda value: value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    provider_runtime.utc_now = lambda: datetime(2026, 8, 26, 10, 0, tzinfo=timezone.utc)
    sys.modules[provider_runtime.__name__] = provider_runtime

    quota_state = types.ModuleType("quota_state")
    quota_state.DEFAULT_STATE_PATH = Path("data/phase-2/quota-state.json")
    quota_state.aggregate_events = lambda state, _events, _registry: (state, {})
    quota_state.load_state = lambda _path, _registry: {}
    quota_state.validate_event = lambda event, _registry: event
    quota_state.write_state = lambda _path, _state, _registry: None
    sys.modules[quota_state.__name__] = quota_state

    task_state = types.ModuleType("task_state")
    task_state.load_task_state = lambda _path: {"tasks": {}}
    task_state.validate_task_state = lambda _state: None
    task_state.write_task_state = lambda _path, _state: None
    sys.modules[task_state.__name__] = task_state

    statistics = types.ModuleType("update_model_run_statistics")
    statistics.refresh_queue_statistics = lambda **_kwargs: None
    sys.modules[statistics.__name__] = statistics


def _load_aggregator():
    dependency_names = (
        "provider_model_registry",
        "provider_runtime",
        "quota_state",
        "task_state",
        "update_model_run_statistics",
    )
    previous = {name: sys.modules.get(name) for name in dependency_names}
    try:
        _install_dependency_stubs()
        path = PHASE2_SCRIPTS / "aggregate_task_results.py"
        spec = importlib.util.spec_from_file_location("aggregate_task_results_step2_test", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load aggregate_task_results.py for focused Step 2 tests.")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        for name, prior in previous.items():
            if prior is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = prior


aggregator = _load_aggregator()


class RejectionHistoryTests(unittest.TestCase):
    def event(self, *, task_id: str = "task-1", attempt_id: str = "attempt-1") -> dict[str, object]:
        return {
            "event_version": 1,
            "task_id": task_id,
            "attempt_id": attempt_id,
            "workflow_run_id": "workflow-1",
            "worker_id": "gemini",
            "provider": "gemini",
            "model": "gemini-3.5-flash",
            "attempt_started_at": "2026-08-26T09:59:00Z",
            "attempt_finished_at": "2026-08-26T10:00:00Z",
            "outcome": "not_called",
            "signal_count": 0,
            "provider_attempts": 0,
            "usage": {
                "input_tokens": None,
                "output_tokens": None,
                "total_tokens": None,
                "reasoning_tokens": None,
                "cached_tokens": None,
            },
            "quota_observations": [],
            "output_sha256": None,
            "output_artifact": None,
        }

    def leased_task(self) -> dict[str, object]:
        return {
            "task_id": "task-1",
            "status": "leased",
            "identity": {"provider": "gemini", "model": "gemini-3.5-flash"},
            "lease": {
                "attempt_id": "attempt-1",
                "workflow_run_id": "workflow-1",
                "worker_id": "gemini",
            },
            "result_record": {},
            "publication": {"status": "not_started"},
            "validation_rejection_count": 0,
            "retry_not_before": None,
        }

    def write_event(self, root: Path, event: dict[str, object], name: str = "event.json") -> Path:
        path = root / "worker" / "result-events" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(event), encoding="utf-8")
        return path

    def run_aggregate(
        self,
        root: Path,
        task_state: dict[str, object],
        *,
        timestamp: str = "2026-08-26T10:05:00Z",
    ):
        return aggregator.aggregate(
            repo_root=root,
            artifact_root=root / "artifacts",
            registry=DummyRegistry(),
            task_state=task_state,
            quota_state={},
            timestamp=timestamp,
        )

    def test_stale_replay_is_counted_but_not_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_event(root / "artifacts", self.event())
            task = self.leased_task()
            task["status"] = "pending"
            task["lease"] = None
            original = {"tasks": {"task-1": task}}

            updated, _quota, counts, accepted = self.run_aggregate(root, original)

            self.assertEqual(updated, original)
            self.assertEqual(accepted, [])
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(counts["stale_replay"], 1)
            self.assertEqual(counts["actionable_rejected"], 0)
            self.assertFalse((root / "data/phase-2/history").exists())
            self.assertFalse((root / "data/phase-2/rejected-events").exists())

    def test_identity_mismatch_remains_actionable_even_when_lease_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_event(root / "artifacts", self.event())
            task = self.leased_task()
            task["identity"] = {"provider": "gemini", "model": "different-model"}
            task["status"] = "pending"
            task["lease"] = None
            original = {"tasks": {"task-1": task}}

            updated, _quota, counts, accepted = self.run_aggregate(root, original)

            self.assertEqual(updated, original)
            self.assertEqual(accepted, [])
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(counts["stale_replay"], 0)
            self.assertEqual(counts["actionable_rejected"], 1)
            history_root = root / "data/phase-2/history"
            self.assertEqual(event_history.validate_history(history_root).rejections, 1)
            ledger = history_root / "rejections-2026-08.ndjson"
            record = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(record["reason"], "Terminal event provider-model identity does not match its task.")

    def test_unknown_task_is_actionable_and_uses_compact_rejection_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_event(root / "artifacts", self.event())

            _updated, _quota, counts, accepted = self.run_aggregate(root, {"tasks": {}})

            self.assertEqual(accepted, [])
            self.assertEqual(counts["rejected"], 1)
            self.assertEqual(counts["stale_replay"], 0)
            self.assertEqual(counts["actionable_rejected"], 1)
            history_root = root / "data/phase-2/history"
            self.assertEqual(event_history.validate_history(history_root).rejections, 1)
            ledger = history_root / "rejections-2026-08.ndjson"
            record = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual(record["reason"], "Terminal event references an unknown task ID.")
            self.assertEqual(record["observed_at"], "2026-08-26T10:05:00Z")
            self.assertFalse((root / "data/phase-2/rejected-events").exists())

    def test_replayed_actionable_rejection_is_idempotent_across_observation_times(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_event(root / "artifacts", self.event())
            empty_state = {"tasks": {}}

            self.run_aggregate(root, empty_state, timestamp="2026-08-26T10:05:00Z")
            ledger = root / "data/phase-2/history/rejections-2026-08.ndjson"
            before = ledger.read_bytes()
            self.run_aggregate(root, empty_state, timestamp="2026-09-01T10:05:00Z")

            self.assertEqual(ledger.read_bytes(), before)
            self.assertFalse((root / "data/phase-2/history/rejections-2026-09.ndjson").exists())
            self.assertEqual(event_history.validate_history(root / "data/phase-2/history").rejections, 1)

    def test_conflicting_terminal_events_are_actionable_and_compacted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = self.event()
            second = self.event()
            second["attempt_finished_at"] = "2026-08-26T10:00:01Z"
            self.write_event(root / "artifacts", first, "first.json")
            self.write_event(root / "artifacts", second, "second.json")

            _updated, _quota, counts, accepted = self.run_aggregate(root, {"tasks": {"task-1": self.leased_task()}})

            self.assertEqual(accepted, [])
            self.assertEqual(counts["rejected"], 2)
            self.assertEqual(counts["stale_replay"], 0)
            self.assertEqual(counts["actionable_rejected"], 2)
            self.assertEqual(event_history.validate_history(root / "data/phase-2/history").rejections, 2)

    def test_malformed_transport_is_actionable_and_compacted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "artifacts" / "worker" / "result-events" / "broken.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{not-json}", encoding="utf-8")

            _updated, _quota, counts, accepted = self.run_aggregate(root, {"tasks": {}})

            self.assertEqual(accepted, [])
            self.assertEqual(counts["transport_rejected"], 1)
            self.assertEqual(counts["actionable_rejected"], 1)
            self.assertEqual(event_history.validate_history(root / "data/phase-2/history").rejections, 1)


class RejectionLedgerIdempotencyTests(unittest.TestCase):
    def test_same_rejection_identity_ignores_later_observation_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = {
                "schema_version": 1,
                "rejection_id": "rejection-1",
                "observed_at": "2026-08-26T10:05:00Z",
                "source_sha256": "a" * 64,
                "source_filename": "first.json",
                "reason": "actionable reason",
            }
            replay = dict(original)
            replay["observed_at"] = "2026-09-01T10:05:00Z"
            replay["source_filename"] = "replayed.json"

            first = event_history.append_rejection(root, original)
            second = event_history.append_rejection(root, replay)

            self.assertTrue(first.appended)
            self.assertFalse(second.appended)
            self.assertEqual(second.path, first.path)
            self.assertEqual(first.path.read_text(encoding="utf-8"), f"{event_history.canonical_json(original)}\n")
            self.assertFalse((root / "rejections-2026-09.ndjson").exists())


if __name__ == "__main__":
    unittest.main()
