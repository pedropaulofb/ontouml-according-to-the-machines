from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

import migrate_statistics_state as migration  # noqa: E402
import update_model_run_statistics as statistics  # noqa: E402


class StatisticsStateTests(unittest.TestCase):
    def sample_state(self) -> dict[str, object]:
        state = statistics.empty_state()
        state["schema_version"] = statistics.QUEUE_STATISTICS_SCHEMA_VERSION
        state["generated_at"] = "2026-08-26T12:00:00Z"
        state["collection_start_utc"] = "2026-08-20T00:00:00Z"
        state["queue"] = {"desired_task_count": 1950, "pending": 100}
        state["seen_events"] = {
            "legacy-event": {
                "timestamp_utc": "2026-08-20T00:00:00Z",
                "provider": "gemini",
                "model": "model-a",
            }
        }
        state["seen_terminal_events"] = {
            "attempt-1": {
                "provider": "gemini",
                "model": "model-a",
                "outcome": "valid",
                "attempt_finished_at": "2026-08-26T12:00:00Z",
            }
        }
        state["models"] = {
            "gemini:model-a": {
                "provider": "gemini",
                "model": "model-a",
                "spec": "gemini:model-a",
                "called": 1,
                "valid": 1,
                "invalid": 0,
                "rejected": 0,
                "provider_failed": 0,
                "runner_failed": 0,
                "last_run_utc": "2026-08-26T12:00:00Z",
                "last_check_status": "ok",
                "last_issue_status": "ok",
                "last_overall_status": "ok",
                "last_event_name": "schedule",
                "last_run_id": "1",
                "last_run_attempt": "1",
            }
        }
        return state

    def legacy_page(self, state: dict[str, object]) -> str:
        return "\n".join(
            [
                "# legacy statistics page",
                "",
                statistics.STATE_START,
                json.dumps(state, indent=2, sort_keys=True),
                statistics.STATE_END,
                "",
            ]
        )

    def test_write_and_load_json_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state_path = Path(temporary) / "statistics-state.json"
            expected = self.sample_state()
            statistics.write_state(state_path, expected)
            loaded = statistics.load_state(state_path)
            self.assertEqual(loaded, expected)
            self.assertTrue(state_path.read_text(encoding="utf-8").endswith("\n"))

    def test_rendered_markdown_does_not_embed_state(self) -> None:
        state = self.sample_state()
        before = copy.deepcopy(state)
        rendered = statistics.render_markdown(state)
        self.assertEqual(state, before)
        self.assertNotIn(statistics.STATE_START, rendered)
        self.assertIn("data/phase-2/statistics-state.json", rendered)

    def test_load_state_prefers_json_over_legacy_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state_path = root / "statistics-state.json"
            page = root / "statistics.md"
            canonical = self.sample_state()
            legacy = copy.deepcopy(canonical)
            legacy["generated_at"] = "2000-01-01T00:00:00Z"
            statistics.write_state(state_path, canonical)
            page.write_text(self.legacy_page(legacy), encoding="utf-8")
            loaded = statistics.load_state(state_path, legacy_statistics_page=page)
            self.assertEqual(loaded, canonical)

    def test_invalid_existing_json_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            state_path = Path(temporary) / "statistics-state.json"
            state_path.write_text("{not-json}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                statistics.load_state(state_path)

    def test_migration_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "statistics.md"
            state_path = root / "statistics-state.json"
            original = self.legacy_page(self.sample_state())
            page.write_text(original, encoding="utf-8")
            result = migration.migrate(statistics_page=page, statistics_state=state_path, apply=False)
            self.assertEqual(result["source"], "markdown")
            self.assertFalse(result["state_written"])
            self.assertFalse(result["page_rewritten"])
            self.assertFalse(state_path.exists())
            self.assertEqual(page.read_text(encoding="utf-8"), original)

    def test_migration_apply_preserves_state_and_derives_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "statistics.md"
            state_path = root / "statistics-state.json"
            expected = self.sample_state()
            page.write_text(self.legacy_page(expected), encoding="utf-8")
            result = migration.migrate(statistics_page=page, statistics_state=state_path, apply=True)
            self.assertTrue(result["state_written"])
            self.assertTrue(result["page_rewritten"])
            self.assertEqual(statistics.load_state(state_path), expected)
            rendered = page.read_text(encoding="utf-8")
            self.assertEqual(rendered, statistics.render_markdown(copy.deepcopy(expected)))
            self.assertNotIn(statistics.STATE_START, rendered)

    def test_migration_is_idempotent_after_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "statistics.md"
            state_path = root / "statistics-state.json"
            page.write_text(self.legacy_page(self.sample_state()), encoding="utf-8")
            migration.migrate(statistics_page=page, statistics_state=state_path, apply=True)
            state_before = state_path.read_bytes()
            page_before = page.read_bytes()
            result = migration.migrate(statistics_page=page, statistics_state=state_path, apply=True)
            self.assertTrue(result["already_migrated"])
            self.assertFalse(result["state_written"])
            self.assertFalse(result["page_rewritten"])
            self.assertEqual(state_path.read_bytes(), state_before)
            self.assertEqual(page.read_bytes(), page_before)

    def test_refresh_writes_canonical_state_and_derived_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "statistics.md"
            state_path = root / "statistics-state.json"
            page.write_text(self.legacy_page(self.sample_state()), encoding="utf-8")
            registry = SimpleNamespace(configured_slots=[], slots=[])
            statistics.refresh_queue_statistics(
                statistics_state=state_path,
                statistics_page=page,
                registry=registry,
                task_state={"tasks": {}},
                quota_state={"runtime_slots": {}, "quota_groups": {}},
                terminal_events=[],
                timestamp_utc="2026-08-26T13:00:00Z",
            )
            state = statistics.load_state(state_path)
            self.assertEqual(state["schema_version"], statistics.QUEUE_STATISTICS_SCHEMA_VERSION)
            self.assertEqual(state["generated_at"], "2026-08-26T13:00:00Z")
            self.assertEqual(state["queue"]["desired_task_count"], 0)
            self.assertNotIn(statistics.STATE_START, page.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
