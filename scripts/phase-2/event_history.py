#!/usr/bin/env python3
"""Compact, deterministic durable history ledgers for Phase 2 events."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

TERMINAL_LEDGER_PREFIX = "terminal-events"
REJECTION_LEDGER_PREFIX = "rejections"
NDJSON_SUFFIX = ".ndjson"


class EventHistoryError(RuntimeError):
    """Raised when a Phase 2 history ledger is malformed or inconsistent."""


class EventHistoryConflictError(EventHistoryError):
    """Raised when one durable event identity maps to conflicting content."""


@dataclass(frozen=True)
class AppendResult:
    """Result of an idempotent append to a compact history ledger."""

    path: Path
    key: str
    content_sha256: str
    appended: bool


@dataclass(frozen=True)
class HistoryValidation:
    """Summary returned after validating all recognized history ledgers."""

    files: int
    terminal_events: int
    rejections: int


def canonical_json(value: Mapping[str, Any]) -> str:
    """Serialize a JSON object in the stable form used for hashing and NDJSON storage."""
    try:
        return json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise EventHistoryError(f"History record is not canonical JSON data: {exc}") from exc


def content_sha256(value: Mapping[str, Any]) -> str:
    """Return the SHA-256 of a record's canonical UTF-8 JSON representation."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _required_text(record: Mapping[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise EventHistoryError(f"History record requires a non-empty string field: {field}")
    return value.strip()


def _timestamp_sort_key(timestamp: str) -> datetime:
    normalized = timestamp.strip()
    try:
        parsed = datetime.fromisoformat(normalized[:-1] + "+00:00" if normalized.endswith("Z") else normalized)
    except ValueError as exc:
        raise EventHistoryError(f"Invalid history timestamp: {timestamp}") from exc
    if parsed.tzinfo is None:
        raise EventHistoryError(f"History timestamp must include a timezone: {timestamp}")
    return parsed.astimezone(timezone.utc)


def _utc_month(timestamp: str) -> str:
    return _timestamp_sort_key(timestamp).strftime("%Y-%m")


def _ledger_path(history_root: Path, prefix: str, month: str) -> Path:
    return history_root / f"{prefix}-{month}{NDJSON_SUFFIX}"


def _recognized_ledgers(history_root: Path, prefix: str) -> list[Path]:
    if not history_root.exists():
        return []
    return sorted(path for path in history_root.glob(f"{prefix}-????-??{NDJSON_SUFFIX}") if path.is_file())


def _load_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            raise EventHistoryError(f"Blank NDJSON line in {path}:{line_number}")
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise EventHistoryError(f"Invalid NDJSON in {path}:{line_number}: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise EventHistoryError(f"History ledger entry must be a JSON object: {path}:{line_number}")
        if raw_line != canonical_json(value):
            raise EventHistoryError(f"History ledger entry is not canonically encoded: {path}:{line_number}")
        records.append(value)
    return records


def _atomic_write_ledger(path: Path, records: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(f"{canonical_json(record)}\n" for record in records)
    file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _load_collection(
    history_root: Path,
    *,
    prefix: str,
    key_field: str,
    timestamp_field: str,
) -> tuple[dict[Path, list[dict[str, Any]]], dict[str, tuple[Path, dict[str, Any], str]]]:
    by_path: dict[Path, list[dict[str, Any]]] = {}
    by_key: dict[str, tuple[Path, dict[str, Any], str]] = {}
    for path in _recognized_ledgers(history_root, prefix):
        filename_month = path.stem.removeprefix(f"{prefix}-")
        records = _load_ledger(path)
        by_path[path] = records
        for record in records:
            key = _required_text(record, key_field)
            timestamp = _required_text(record, timestamp_field)
            event_month = _utc_month(timestamp)
            if event_month != filename_month:
                raise EventHistoryError(
                    f"History record {key_field}={key} belongs to {event_month}, not ledger {filename_month}"
                )
            digest = content_sha256(record)
            previous = by_key.get(key)
            if previous is not None:
                previous_path, _previous_record, previous_digest = previous
                qualifier = "conflicting" if previous_digest != digest else "duplicate"
                raise EventHistoryError(f"History contains {qualifier} {key_field}={key} in {previous_path} and {path}")
            by_key[key] = (path, record, digest)
    return by_path, by_key


def _append_many_unique(
    history_root: Path,
    records: Iterable[Mapping[str, Any]],
    *,
    prefix: str,
    key_field: str,
    timestamp_field: str,
    sort_fields: Sequence[str],
) -> list[AppendResult]:
    root = Path(history_root)
    by_path, by_key = _load_collection(
        root,
        prefix=prefix,
        key_field=key_field,
        timestamp_field=timestamp_field,
    )
    results: list[AppendResult] = []
    touched_paths: set[Path] = set()

    for raw_record in records:
        normalized = dict(raw_record)
        key = _required_text(normalized, key_field)
        timestamp = _required_text(normalized, timestamp_field)
        target = _ledger_path(root, prefix, _utc_month(timestamp))
        digest = content_sha256(normalized)

        existing = by_key.get(key)
        if existing is not None:
            existing_path, existing_record, existing_digest = existing
            if existing_digest != digest or canonical_json(existing_record) != canonical_json(normalized):
                raise EventHistoryConflictError(f"Conflicting history record for {key_field}={key}")
            results.append(AppendResult(path=existing_path, key=key, content_sha256=digest, appended=False))
            continue

        by_path.setdefault(target, []).append(normalized)
        by_key[key] = (target, normalized, digest)
        touched_paths.add(target)
        results.append(AppendResult(path=target, key=key, content_sha256=digest, appended=True))

    for path in sorted(touched_paths):
        month_records = by_path[path]
        month_records.sort(
            key=lambda value: (
                _timestamp_sort_key(_required_text(value, timestamp_field)),
                *(str(value.get(field, "")) for field in sort_fields if field != timestamp_field),
            )
        )
        _atomic_write_ledger(path, month_records)
    return results


def append_terminal_events(history_root: Path, events: Iterable[Mapping[str, Any]]) -> list[AppendResult]:
    """Idempotently persist terminal events, loading existing ledgers only once per batch."""
    return _append_many_unique(
        Path(history_root),
        events,
        prefix=TERMINAL_LEDGER_PREFIX,
        key_field="attempt_id",
        timestamp_field="attempt_finished_at",
        sort_fields=("attempt_finished_at", "attempt_id"),
    )


def append_terminal_event(history_root: Path, event: Mapping[str, Any]) -> AppendResult:
    """Idempotently persist one terminal event in its UTC-month ledger."""
    return append_terminal_events(history_root, [event])[0]


def terminal_event_exists(history_root: Path, attempt_id: str) -> bool:
    """Return whether a terminal event with the given attempt ID is already durable."""
    key = attempt_id.strip()
    if not key:
        raise EventHistoryError("Terminal-event existence checks require a non-empty attempt_id.")
    _by_path, by_key = _load_collection(
        Path(history_root),
        prefix=TERMINAL_LEDGER_PREFIX,
        key_field="attempt_id",
        timestamp_field="attempt_finished_at",
    )
    return key in by_key


def append_rejections(history_root: Path, rejections: Iterable[Mapping[str, Any]]) -> list[AppendResult]:
    """Idempotently persist actionable rejections, loading existing ledgers once per batch."""
    return _append_many_unique(
        Path(history_root),
        rejections,
        prefix=REJECTION_LEDGER_PREFIX,
        key_field="rejection_id",
        timestamp_field="observed_at",
        sort_fields=("observed_at", "rejection_id"),
    )


def append_rejection(history_root: Path, rejection: Mapping[str, Any]) -> AppendResult:
    """Idempotently persist one actionable rejection in its UTC-month ledger."""
    return append_rejections(history_root, [rejection])[0]


def load_terminal_events(history_root: Path) -> list[dict[str, Any]]:
    """Load terminal events in deterministic timestamp/attempt order."""
    by_path, _by_key = _load_collection(
        Path(history_root),
        prefix=TERMINAL_LEDGER_PREFIX,
        key_field="attempt_id",
        timestamp_field="attempt_finished_at",
    )
    events = [event for path in sorted(by_path) for event in by_path[path]]
    events.sort(
        key=lambda value: (
            _timestamp_sort_key(_required_text(value, "attempt_finished_at")),
            _required_text(value, "attempt_id"),
        )
    )
    return events


def validate_history(history_root: Path) -> HistoryValidation:
    """Validate all recognized terminal-event and rejection ledgers."""
    root = Path(history_root)
    terminal_by_path, terminal_by_key = _load_collection(
        root,
        prefix=TERMINAL_LEDGER_PREFIX,
        key_field="attempt_id",
        timestamp_field="attempt_finished_at",
    )
    rejection_by_path, rejection_by_key = _load_collection(
        root,
        prefix=REJECTION_LEDGER_PREFIX,
        key_field="rejection_id",
        timestamp_field="observed_at",
    )
    return HistoryValidation(
        files=len(terminal_by_path) + len(rejection_by_path),
        terminal_events=len(terminal_by_key),
        rejections=len(rejection_by_key),
    )


def canonicalize_records(records: Iterable[Mapping[str, Any]]) -> list[str]:
    """Return canonical JSON lines for diagnostics and migration tooling."""
    return [canonical_json(record) for record in records]
