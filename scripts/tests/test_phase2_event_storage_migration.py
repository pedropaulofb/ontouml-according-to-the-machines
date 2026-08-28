from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

MODULE_PATH = PHASE2_SCRIPTS / "migrate_event_storage.py"
SPEC = importlib.util.spec_from_file_location("phase2_statistics_reset", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load migrate_event_storage.py")
reset = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reset
SPEC.loader.exec_module(reset)


@dataclass(frozen=True)
class DummySlot:
    provider: str = "gemini"
    model: str = "gemini-3.5-flash"
    configuration_status: str = "configured"
    execution_status: str = "eligible"
    lifecycle: str = "production"
    quota_groups: tuple[str, ...] = ()

    @property
    def spec(self) -> str:
        return f"{self.provider}:{self.model}"


class DummyRegistry:
    def __init__(self) -> None:
        self.slots = (DummySlot(),)
        self.configured_slots = self.slots


def task_state() -> dict[str, object]:
    return {
        "tasks": {
            "task-1": {
                "task_id": "task-1",
                "identity": {"provider": "gemini", "model": "gemini-3.5-flash"},
                "status": "completed",
                "created_at": "2026-08-20T00:00:00Z",
            },
            "task-2": {
                "task_id": "task-2",
                "identity": {"provider": "gemini", "model": "gemini-3.5-flash"},
                "status": "pending",
                "created_at": "2026-08-27T00:00:00Z",
            },
        }
    }


def legacy_statistics_state() -> dict[str, object]:
    return {
        "schema_version": 2,
        "generated_at": "2026-08-27T12:00:00Z",
        "collection_start_utc": "2026-08-01T00:00:00Z",
        "active_rotation": [],
        "models": {
            "gemini:gemini-3.5-flash": {
                "provider": "gemini",
                "model": "gemini-3.5-flash",
                "spec": "gemini:gemini-3.5-flash",
                "total_called": 10,
            }
        },
        "seen_events": {"old": {}},
        "seen_terminal_events": {"attempt-old": {}},
        "queue": {"desired_task_count": 2},
    }


class StatisticsBaselineResetTests(unittest.TestCase):
    RESET_AT = "2026-08-28T08:00:00Z"

    def make_repo(self, root: Path) -> tuple[Path, Path]:
        state_path = root / "data/phase-2/statistics-state.json"
        page_path = root / "docs/methodology/phases/phase-2/model-run-statistics.md"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(legacy_statistics_state()), encoding="utf-8")
        page_path.write_bytes(b"# Historical statistics\r\n\r\nCalled: 10\r\n")
        return state_path, page_path

    def prepare(self, root: Path, state_path: Path, page_path: Path):
        return reset.prepare_reset(
            repo_root=root,
            reset_at=self.RESET_AT,
            statistics_state_path=state_path,
            statistics_page_path=page_path,
            registry=DummyRegistry(),
            task_state=task_state(),
            quota_state={},
        )

    def test_prepare_is_read_only_and_archives_current_page_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path, page_path = self.make_repo(root)
            before_state = state_path.read_bytes()
            before_page = page_path.read_bytes()

            candidate = self.prepare(root, state_path, page_path)

            self.assertEqual(state_path.read_bytes(), before_state)
            self.assertEqual(page_path.read_bytes(), before_page)
            self.assertFalse(candidate.archive_path.exists())
            self.assertEqual(candidate.archive_bytes, before_page)

    def test_fresh_state_resets_execution_history_but_preserves_queue_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path, page_path = self.make_repo(root)

            candidate = self.prepare(root, state_path, page_path)
            state = candidate.statistics_state
            model = state["models"]["gemini:gemini-3.5-flash"]

            self.assertEqual(state["collection_start_utc"], self.RESET_AT)
            self.assertEqual(state["generated_at"], self.RESET_AT)
            self.assertEqual(state["seen_events"], {})
            self.assertEqual(state["seen_terminal_events"], {})
            self.assertEqual(model["total_called"], 0)
            self.assertEqual(model["total_provider_attempts"], 0)
            self.assertEqual(model["input_tokens_known_events"], 0)
            self.assertIsNone(model["input_tokens"])
            self.assertEqual(model["current_completed_tasks"], 1)
            self.assertEqual(model["current_desired_tasks"], 2)
            self.assertEqual(state["queue"]["desired_task_count"], 2)
            self.assertEqual(state["queue"]["completed"], 1)
            self.assertEqual(state["queue"]["pending"], 1)

    def test_apply_writes_archive_state_and_live_page_without_touching_other_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path, page_path = self.make_repo(root)
            sentinel = root / "data/phase-2/results/legacy.json"
            sentinel.parent.mkdir(parents=True, exist_ok=True)
            sentinel.write_text("legacy", encoding="utf-8")
            old_page = page_path.read_bytes()
            candidate = self.prepare(root, state_path, page_path)

            reset.apply_reset(
                candidate=candidate,
                statistics_state_path=state_path,
                statistics_page_path=page_path,
            )

            self.assertEqual(candidate.archive_path.read_bytes(), old_page)
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8")), candidate.statistics_state)
            self.assertEqual(page_path.read_text(encoding="utf-8"), candidate.statistics_page)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "legacy")

    def test_conflicting_existing_archive_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path, page_path = self.make_repo(root)
            archive = root / "docs/methodology/phases/phase-2/history/model-run-statistics-before-reset-2026-08-28.md"
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_text("existing", encoding="utf-8")

            with self.assertRaises(reset.StatisticsResetError):
                self.prepare(root, state_path, page_path)

    def test_matching_existing_archive_allows_partial_apply_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path, page_path = self.make_repo(root)
            old_page = page_path.read_bytes()
            archive = root / "docs/methodology/phases/phase-2/history/model-run-statistics-before-reset-2026-08-28.md"
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(old_page)

            candidate = self.prepare(root, state_path, page_path)
            reset.apply_reset(
                candidate=candidate,
                statistics_state_path=state_path,
                statistics_page_path=page_path,
            )

            self.assertEqual(archive.read_bytes(), old_page)
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8")), candidate.statistics_state)
            self.assertEqual(page_path.read_text(encoding="utf-8"), candidate.statistics_page)

    def test_reset_timestamp_requires_utc(self) -> None:
        self.assertEqual(reset._normalize_reset_at(self.RESET_AT), self.RESET_AT)
        with self.assertRaises(reset.StatisticsResetError):
            reset._normalize_reset_at("2026-08-28T10:00:00+02:00")


if __name__ == "__main__":
    unittest.main()
