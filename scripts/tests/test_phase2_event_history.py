from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE2_SCRIPTS = REPO_ROOT / "scripts/phase-2"
if str(PHASE2_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PHASE2_SCRIPTS))

import event_history  # noqa: E402


class EventHistoryTests(unittest.TestCase):
    def terminal_event(self, attempt_id: str, finished_at: str = "2026-08-17T12:00:00Z") -> dict[str, object]:
        return {
            "attempt_id": attempt_id,
            "attempt_finished_at": finished_at,
            "model": "gemini-3.5-flash",
            "outcome": "valid",
            "provider": "gemini",
            "provider_attempts": 1,
            "signal_count": 1,
            "usage": {"input_tokens": 10, "output_tokens": 4},
        }

    def rejection(self, rejection_id: str, observed_at: str = "2026-08-17T12:00:00Z") -> dict[str, object]:
        return {
            "observed_at": observed_at,
            "reason": "conflicting terminal events",
            "rejection_id": rejection_id,
            "source_sha256": "a" * 64,
        }

    def test_terminal_event_is_written_canonically_and_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            event = self.terminal_event("attempt-1")
            result = event_history.append_terminal_event(root, event)

            self.assertTrue(result.appended)
            self.assertEqual(result.path.name, "terminal-events-2026-08.ndjson")
            self.assertEqual(result.content_sha256, event_history.content_sha256(event))
            self.assertEqual(result.path.read_text(encoding="utf-8"), f"{event_history.canonical_json(event)}\n")
            self.assertEqual(
                event_history.validate_history(root),
                event_history.HistoryValidation(files=1, terminal_events=1, rejections=0),
            )

    def test_duplicate_terminal_event_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            event = self.terminal_event("attempt-1")
            first = event_history.append_terminal_event(root, event)
            before = first.path.read_bytes()
            second = event_history.append_terminal_event(root, event)

            self.assertFalse(second.appended)
            self.assertEqual(second.path, first.path)
            self.assertEqual(second.content_sha256, first.content_sha256)
            self.assertEqual(first.path.read_bytes(), before)

    def test_conflicting_terminal_event_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            event_history.append_terminal_event(root, self.terminal_event("attempt-1"))
            conflicting = self.terminal_event("attempt-1")
            conflicting["signal_count"] = 2

            with self.assertRaises(event_history.EventHistoryConflictError):
                event_history.append_terminal_event(root, conflicting)

    def test_terminal_event_existence_is_explicit_and_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertFalse(event_history.terminal_event_exists(root, "attempt-1"))

            event_history.append_terminal_event(root, self.terminal_event("attempt-1"))
            self.assertTrue(event_history.terminal_event_exists(root, "attempt-1"))
            self.assertFalse(event_history.terminal_event_exists(root, "attempt-2"))

            with self.assertRaises(event_history.EventHistoryError):
                event_history.terminal_event_exists(root, "   ")

    def test_month_is_based_on_utc_and_records_are_sorted_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            later = self.terminal_event("attempt-later", "2026-08-31T23:30:00Z")
            earlier = self.terminal_event("attempt-earlier", "2026-09-01T00:30:00+02:00")
            event_history.append_terminal_event(root, later)
            event_history.append_terminal_event(root, earlier)

            ledger = root / "terminal-events-2026-08.ndjson"
            records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([record["attempt_id"] for record in records], ["attempt-earlier", "attempt-later"])
            self.assertFalse((root / "terminal-events-2026-09.ndjson").exists())

    def test_actionable_rejections_use_their_own_idempotent_monthly_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rejection = self.rejection("reject-1")
            first = event_history.append_rejection(root, rejection)
            second = event_history.append_rejection(root, rejection)

            self.assertTrue(first.appended)
            self.assertFalse(second.appended)
            self.assertEqual(first.path.name, "rejections-2026-08.ndjson")
            self.assertEqual(
                event_history.validate_history(root),
                event_history.HistoryValidation(files=1, terminal_events=0, rejections=1),
            )

    def test_validation_rejects_duplicate_identity_across_ledgers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            august = self.terminal_event("attempt-1", "2026-08-31T23:00:00Z")
            september = self.terminal_event("attempt-1", "2026-09-01T01:00:00Z")
            (root / "terminal-events-2026-08.ndjson").write_text(
                f"{event_history.canonical_json(august)}\n", encoding="utf-8"
            )
            (root / "terminal-events-2026-09.ndjson").write_text(
                f"{event_history.canonical_json(september)}\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(event_history.EventHistoryError, "conflicting attempt_id=attempt-1"):
                event_history.validate_history(root)

    def test_validation_rejects_noncanonical_or_malformed_ledger_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger = root / "terminal-events-2026-08.ndjson"
            ledger.write_text('{"attempt_id": "attempt-1", "attempt_finished_at": "2026-08-17T12:00:00Z"}\n')

            with self.assertRaisesRegex(event_history.EventHistoryError, "not canonically encoded"):
                event_history.validate_history(root)

            ledger.write_text("{not-json}\n", encoding="utf-8")
            with self.assertRaisesRegex(event_history.EventHistoryError, "Invalid NDJSON"):
                event_history.validate_history(root)

    def test_batch_append_loads_once_semantically_and_shards_by_month(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            august = self.terminal_event("attempt-1", "2026-08-31T23:59:59Z")
            september = self.terminal_event("attempt-2", "2026-09-01T00:00:00Z")
            results = event_history.append_terminal_events(root, [september, august, august])

            self.assertEqual([result.appended for result in results], [True, True, False])
            self.assertTrue((root / "terminal-events-2026-08.ndjson").is_file())
            self.assertTrue((root / "terminal-events-2026-09.ndjson").is_file())
            self.assertEqual(event_history.validate_history(root).terminal_events, 2)

    def test_batch_conflict_does_not_write_partial_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = self.terminal_event("attempt-1")
            conflicting = self.terminal_event("attempt-1")
            conflicting["signal_count"] = 2

            with self.assertRaises(event_history.EventHistoryConflictError):
                event_history.append_terminal_events(root, [first, conflicting])

            self.assertEqual(list(root.glob("*.ndjson")), [])

    def test_load_terminal_events_returns_cross_ledger_chronological_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            september = self.terminal_event("attempt-2", "2026-09-01T00:00:00Z")
            august = self.terminal_event("attempt-1", "2026-08-31T23:59:59Z")
            event_history.append_terminal_event(root, september)
            event_history.append_terminal_event(root, august)

            loaded = event_history.load_terminal_events(root)
            self.assertEqual([event["attempt_id"] for event in loaded], ["attempt-1", "attempt-2"])


if __name__ == "__main__":
    unittest.main()
