#!/usr/bin/env python3
"""Persistent state primitives for the Phase 2 content-addressed queue."""

from __future__ import annotations

import copy
import json
import os
import string
import tempfile
from pathlib import Path
from typing import Any, Mapping

LEGACY_TASK_STATE_SCHEMA_VERSION = 1
TASK_STATE_SCHEMA_VERSION = 2
SUPPORTED_TASK_STATE_SCHEMA_VERSIONS = {LEGACY_TASK_STATE_SCHEMA_VERSION, TASK_STATE_SCHEMA_VERSION}
QUEUE_GENERATION = "phase-2-recalibration-v1"
EXECUTION_STATUSES = {
    "pending",
    "leased",
    "completed",
    "retry_due",
    "deferred_quota",
    "temporarily_unavailable",
    "blocked_provider_policy",
    "blocked_execution_configuration",
    "blocked_repeated_rejection",
    "blocked_ambiguous_attempt",
    "retired",
    "obsolete",
}
PUBLICATION_STATUSES = {
    "not_started",
    "not_required",
    "pending",
    "published",
    "retry_due",
    "superseded",
}


class TaskStateError(ValueError):
    """Raised when persistent task state is missing or invalid."""


def new_task_record(
    *,
    task_id: str,
    identity: Mapping[str, str],
    timestamp: str,
    source_commit_sha: str | None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "task_id": task_id,
        "identity": dict(identity),
        "status": "pending",
        "created_at": timestamp,
        "updated_at": timestamp,
        "attempt_count": 0,
        "validation_rejection_count": 0,
        "last_attempt_at": None,
        "retry_not_before": None,
        "lease": None,
        "last_outcome": None,
        "result_record": {
            "attempt_id": None,
            "source_event_sha256": None,
            "event_path": None,
            "output_sha256": None,
            "validated_output_path": None,
        },
        "publication": {
            "status": "not_started",
            "payload_path": None,
            "last_attempt_at": None,
            "last_error": None,
        },
    }
    if source_commit_sha:
        record["source_metadata"] = {"repository_commit_sha": source_commit_sha}
    return record


def new_task_state(*, registry_sha256: str, timestamp: str) -> dict[str, Any]:
    return {
        "schema_version": TASK_STATE_SCHEMA_VERSION,
        "queue_generation": QUEUE_GENERATION,
        "registry_sha256": registry_sha256,
        "last_reconciled_at": timestamp,
        "tasks": {},
    }


def _require_keys(value: Mapping[str, Any], keys: set[str], description: str) -> None:
    missing = sorted(keys - value.keys())
    if missing:
        raise TaskStateError(f"{description} is missing required field(s): {', '.join(missing)}.")


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in string.hexdigits for character in value)


def _validate_result_record(task_key: str, result_record: Any, schema_version: int) -> None:
    if not isinstance(result_record, dict):
        raise TaskStateError(f"Task {task_key} result_record must be an object.")
    if schema_version == LEGACY_TASK_STATE_SCHEMA_VERSION:
        _require_keys(
            result_record,
            {"event_path", "output_sha256", "validated_output_path"},
            f"Task {task_key} result_record",
        )
        return

    _require_keys(
        result_record,
        {"attempt_id", "source_event_sha256", "output_sha256", "validated_output_path"},
        f"Task {task_key} result_record",
    )
    attempt_id = result_record["attempt_id"]
    source_sha256 = result_record["source_event_sha256"]
    if (attempt_id is None) != (source_sha256 is None):
        raise TaskStateError(
            f"Task {task_key} result_record attempt_id and source_event_sha256 must both be set or null."
        )
    if attempt_id is not None and (not isinstance(attempt_id, str) or not attempt_id.strip()):
        raise TaskStateError(f"Task {task_key} result_record attempt_id must be a non-empty string or null.")
    if source_sha256 is not None and not _is_sha256(source_sha256):
        raise TaskStateError(f"Task {task_key} result_record source_event_sha256 must be a full SHA-256 or null.")


def validate_task_record(task_key: str, record: Any, *, schema_version: int = TASK_STATE_SCHEMA_VERSION) -> None:
    if not isinstance(record, dict):
        raise TaskStateError(f"Task {task_key} must be an object.")
    _require_keys(
        record,
        {
            "task_id",
            "identity",
            "status",
            "created_at",
            "updated_at",
            "attempt_count",
            "validation_rejection_count",
            "last_attempt_at",
            "retry_not_before",
            "lease",
            "last_outcome",
            "result_record",
            "publication",
        },
        f"Task {task_key}",
    )
    if record["task_id"] != task_key:
        raise TaskStateError(f"Task map key {task_key} does not match record task_id {record['task_id']!r}.")
    if not isinstance(record["identity"], dict):
        raise TaskStateError(f"Task {task_key} identity must be an object.")
    if record["status"] not in EXECUTION_STATUSES:
        raise TaskStateError(f"Task {task_key} has unsupported status {record['status']!r}.")
    for field in ("attempt_count", "validation_rejection_count"):
        if not isinstance(record[field], int) or isinstance(record[field], bool) or record[field] < 0:
            raise TaskStateError(f"Task {task_key} {field} must be a non-negative integer.")
    _validate_result_record(task_key, record["result_record"], schema_version)
    if not isinstance(record["publication"], dict):
        raise TaskStateError(f"Task {task_key} publication must be an object.")
    _require_keys(
        record["publication"],
        {"status", "payload_path", "last_attempt_at", "last_error"},
        f"Task {task_key} publication",
    )
    if record["publication"]["status"] not in PUBLICATION_STATUSES:
        raise TaskStateError(f"Task {task_key} has unsupported publication status {record['publication']['status']!r}.")


def validate_task_state(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise TaskStateError("Task state root must be an object.")
    _require_keys(
        state,
        {"schema_version", "queue_generation", "registry_sha256", "last_reconciled_at", "tasks"},
        "Task state root",
    )
    schema_version = state["schema_version"]
    if schema_version not in SUPPORTED_TASK_STATE_SCHEMA_VERSIONS:
        supported = ", ".join(str(value) for value in sorted(SUPPORTED_TASK_STATE_SCHEMA_VERSIONS))
        raise TaskStateError(f"Task state schema_version must be one of: {supported}.")
    if state["queue_generation"] != QUEUE_GENERATION:
        raise TaskStateError(f"Task state queue_generation must be {QUEUE_GENERATION!r}.")
    if not isinstance(state["registry_sha256"], str) or len(state["registry_sha256"]) != 64:
        raise TaskStateError("Task state registry_sha256 must be a full SHA-256 value.")
    if not isinstance(state["last_reconciled_at"], str) or not state["last_reconciled_at"]:
        raise TaskStateError("Task state last_reconciled_at must be a non-empty string.")
    if not isinstance(state["tasks"], dict):
        raise TaskStateError("Task state tasks must be an object.")
    for task_key, record in state["tasks"].items():
        validate_task_record(task_key, record, schema_version=schema_version)
    return state


def load_task_state(path: Path) -> dict[str, Any]:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TaskStateError(f"Task state does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TaskStateError(f"Task state is not valid JSON: {exc}") from exc
    return validate_task_state(state)


def _load_durable_result_identity(repo_root: Path, task_id: str, event_path: str) -> tuple[str, str]:
    path = repo_root / event_path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TaskStateError(f"Task {task_id} durable result event does not exist: {event_path}") from exc
    except json.JSONDecodeError as exc:
        raise TaskStateError(f"Task {task_id} durable result event is not valid JSON: {event_path}: {exc}") from exc
    if not isinstance(value, dict):
        raise TaskStateError(f"Task {task_id} durable result event must be an object: {event_path}")
    if value.get("task_id") != task_id:
        raise TaskStateError(f"Task {task_id} durable result event task_id does not match: {event_path}")
    attempt_id = value.get("attempt_id")
    if not isinstance(attempt_id, str) or not attempt_id.strip():
        raise TaskStateError(f"Task {task_id} durable result event has no valid attempt_id: {event_path}")
    aggregation = value.get("aggregation")
    source_sha256 = aggregation.get("source_event_sha256") if isinstance(aggregation, dict) else None
    if not _is_sha256(source_sha256):
        raise TaskStateError(f"Task {task_id} durable result event has no valid source_event_sha256: {event_path}")
    return attempt_id, source_sha256


def migrate_task_state_v1_to_v2(
    state: Mapping[str, Any],
    *,
    repo_root: Path,
) -> tuple[dict[str, Any], dict[str, int]]:
    """Return a validated schema-v2 copy without mutating the supplied state."""
    validated = validate_task_state(copy.deepcopy(dict(state)))
    if validated["schema_version"] == TASK_STATE_SCHEMA_VERSION:
        return validated, {
            "already_v2": len(validated["tasks"]),
            "derived_from_event": 0,
            "already_identified": 0,
            "empty": 0,
            "transient_replay": 0,
        }

    migrated = copy.deepcopy(validated)
    counts = {
        "already_v2": 0,
        "derived_from_event": 0,
        "already_identified": 0,
        "empty": 0,
        "transient_replay": 0,
    }
    for task_id, task in migrated["tasks"].items():
        result_record = task["result_record"]
        attempt_id = result_record.get("attempt_id")
        source_sha256 = result_record.get("source_event_sha256")
        if (attempt_id is None) != (source_sha256 is None):
            raise TaskStateError(
                f"Task {task_id} legacy result_record has an incomplete attempt_id/source_event_sha256 pair."
            )
        if attempt_id is not None:
            if not isinstance(attempt_id, str) or not attempt_id.strip() or not _is_sha256(source_sha256):
                raise TaskStateError(
                    f"Task {task_id} legacy result_record contains an invalid durable result identity."
                )
            counts["already_identified"] += 1
        else:
            event_path = result_record.get("event_path")
            last_outcome = task.get("last_outcome")
            replayable = (
                task.get("status") == "leased"
                and isinstance(last_outcome, dict)
                and last_outcome.get("kind") == "replayable_result"
            )
            if replayable:
                attempt_id = None
                source_sha256 = None
                counts["transient_replay"] += 1
            elif event_path is None:
                counts["empty"] += 1
            elif isinstance(event_path, str) and event_path.strip():
                attempt_id, source_sha256 = _load_durable_result_identity(repo_root, task_id, event_path)
                counts["derived_from_event"] += 1
            else:
                raise TaskStateError(
                    f"Task {task_id} legacy result_record event_path must be a non-empty string or null."
                )
        result_record["attempt_id"] = attempt_id
        result_record["source_event_sha256"] = source_sha256

    migrated["schema_version"] = TASK_STATE_SCHEMA_VERSION
    validate_task_state(migrated)
    return migrated, counts


def write_task_state(path: Path, state: Mapping[str, Any]) -> None:
    validate_task_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_file.write(payload)
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
