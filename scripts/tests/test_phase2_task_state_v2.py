"""Focused tests for Phase 2 task-state schema v2 and v1 migration."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

import migrate_task_state_v2  # noqa: E402
import task_state  # noqa: E402

TIMESTAMP = "2026-08-26T12:00:00Z"


def _record(task_id: str = "task-1") -> dict[str, object]:
    return task_state.new_task_record(
        task_id=task_id,
        identity={"provider": "gemini", "model": "gemini-3.5-flash"},
        timestamp=TIMESTAMP,
        source_commit_sha=None,
    )


def _state(record: dict[str, object], *, schema_version: int = task_state.TASK_STATE_SCHEMA_VERSION):
    state = task_state.new_task_state(registry_sha256="d" * 64, timestamp=TIMESTAMP)
    state["schema_version"] = schema_version
    state["tasks"] = {str(record["task_id"]): record}
    return state


def _legacy_record(task_id: str = "task-1") -> dict[str, object]:
    record = _record(task_id)
    record["result_record"] = {
        "event_path": None,
        "output_sha256": None,
        "validated_output_path": None,
    }
    return record


def _write_durable_event(root: Path, task_id: str, attempt_id: str, source_sha256: str) -> str:
    relative = Path("data/phase-2/results") / task_id / f"{attempt_id}.json"
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "task_id": task_id,
                "attempt_id": attempt_id,
                "aggregation": {"source_event_sha256": source_sha256},
            }
        ),
        encoding="utf-8",
    )
    return relative.as_posix()


class TaskStateSchemaV2Tests(unittest.TestCase):
    def test_new_state_and_record_are_schema_v2_compatible(self) -> None:
        record = _record()
        state = _state(record)
        self.assertEqual(state["schema_version"], 2)
        self.assertIsNone(record["result_record"]["attempt_id"])
        self.assertIsNone(record["result_record"]["source_event_sha256"])
        self.assertIsNone(record["result_record"]["event_path"])
        self.assertIs(task_state.validate_task_state(state), state)

    def test_validator_keeps_schema_v1_compatibility(self) -> None:
        record = _legacy_record()
        state = _state(record, schema_version=1)
        self.assertIs(task_state.validate_task_state(state), state)

    def test_schema_v2_requires_complete_durable_result_identity(self) -> None:
        record = _record()
        record["result_record"]["attempt_id"] = "attempt-1"
        with self.assertRaisesRegex(task_state.TaskStateError, "must both be set or null"):
            task_state.validate_task_state(_state(record))

    def test_new_record_remains_valid_inside_legacy_schema_during_transition(self) -> None:
        record = _record()
        task_state.validate_task_state(_state(record, schema_version=1))

    def test_step3_result_record_shape_is_valid_schema_v2(self) -> None:
        record = _record()
        record["result_record"] = {
            "attempt_id": "attempt-1",
            "source_event_sha256": "a" * 64,
            "event_path": "data/phase-2/results/task-1/attempt-1.json",
            "output_sha256": None,
            "validated_output_path": None,
        }
        task_state.validate_task_state(_state(record))

    def test_schema_v2_allows_transitional_event_path_extension(self) -> None:
        record = _record()
        record["result_record"]["event_path"] = "artifact/result-events/attempt-1.json"
        task_state.validate_task_state(_state(record))


class TaskStateMigrationTests(unittest.TestCase):
    def test_migration_derives_identity_from_durable_event(self) -> None:
        record = _legacy_record()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            record["result_record"]["event_path"] = _write_durable_event(root, "task-1", "attempt-1", "a" * 64)
            migrated, counts = task_state.migrate_task_state_v1_to_v2(_state(record, schema_version=1), repo_root=root)
        result = migrated["tasks"]["task-1"]["result_record"]
        self.assertEqual(migrated["schema_version"], 2)
        self.assertEqual(result["attempt_id"], "attempt-1")
        self.assertEqual(result["source_event_sha256"], "a" * 64)
        self.assertEqual(counts["derived_from_event"], 1)

    def test_migration_uses_step3_identity_without_result_json(self) -> None:
        record = _legacy_record()
        record["result_record"].update(
            {
                "attempt_id": "attempt-1",
                "source_event_sha256": "b" * 64,
                "event_path": "data/phase-2/results/task-1/missing.json",
            }
        )
        with tempfile.TemporaryDirectory() as temporary:
            migrated, counts = task_state.migrate_task_state_v1_to_v2(
                _state(record, schema_version=1), repo_root=Path(temporary)
            )
        result = migrated["tasks"]["task-1"]["result_record"]
        self.assertEqual(result["attempt_id"], "attempt-1")
        self.assertEqual(result["source_event_sha256"], "b" * 64)
        self.assertEqual(counts["already_identified"], 1)

    def test_migration_keeps_replayable_lease_without_claiming_durable_identity(self) -> None:
        record = _legacy_record()
        record["status"] = "leased"
        record["lease"] = {"attempt_id": "attempt-1"}
        record["last_outcome"] = {"kind": "replayable_result", "attempt_id": "attempt-1"}
        record["result_record"]["event_path"] = "worker/result-events/attempt-1.json"
        with tempfile.TemporaryDirectory() as temporary:
            migrated, counts = task_state.migrate_task_state_v1_to_v2(
                _state(record, schema_version=1), repo_root=Path(temporary)
            )
        result = migrated["tasks"]["task-1"]["result_record"]
        self.assertIsNone(result["attempt_id"])
        self.assertIsNone(result["source_event_sha256"])
        self.assertEqual(counts["transient_replay"], 1)

    def test_migration_fails_if_required_durable_event_is_missing(self) -> None:
        record = _legacy_record()
        record["result_record"]["event_path"] = "data/phase-2/results/task-1/missing.json"
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(task_state.TaskStateError, "does not exist"):
                task_state.migrate_task_state_v1_to_v2(_state(record, schema_version=1), repo_root=Path(temporary))

    def test_migration_rejects_durable_event_for_different_task(self) -> None:
        record = _legacy_record()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            event_path = _write_durable_event(root, "other-task", "attempt-1", "c" * 64)
            record["result_record"]["event_path"] = event_path
            with self.assertRaisesRegex(task_state.TaskStateError, "task_id does not match"):
                task_state.migrate_task_state_v1_to_v2(_state(record, schema_version=1), repo_root=root)

    def test_migrating_schema_v2_is_idempotent(self) -> None:
        state = _state(_record())
        migrated, counts = task_state.migrate_task_state_v1_to_v2(state, repo_root=Path("."))
        self.assertEqual(migrated, state)
        self.assertEqual(counts["already_v2"], 1)


class MigrationCliTests(unittest.TestCase):
    def test_dry_run_does_not_write_and_apply_is_explicit(self) -> None:
        record = _legacy_record()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path = root / "data/phase-2/task-state.json"
            state_path.parent.mkdir(parents=True)
            state_path.write_text(json.dumps(_state(record, schema_version=1)), encoding="utf-8")
            before = state_path.read_bytes()
            output = StringIO()
            with redirect_stdout(output):
                result = migrate_task_state_v2.main(["--repo-root", str(root)])
            self.assertEqual(result, 0)
            self.assertEqual(state_path.read_bytes(), before)
            self.assertIn("state_written=false", output.getvalue())

            with redirect_stdout(StringIO()):
                result = migrate_task_state_v2.main(["--repo-root", str(root), "--apply"])
            self.assertEqual(result, 0)
            migrated = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(migrated["schema_version"], 2)


if __name__ == "__main__":
    unittest.main()
