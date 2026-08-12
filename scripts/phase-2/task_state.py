#!/usr/bin/env python3
"""Persistent state primitives for the Phase 2 content-addressed queue."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

TASK_STATE_SCHEMA_VERSION = 1
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


def validate_task_record(task_key: str, record: Any) -> None:
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
    if not isinstance(record["result_record"], dict):
        raise TaskStateError(f"Task {task_key} result_record must be an object.")
    _require_keys(
        record["result_record"],
        {"event_path", "output_sha256", "validated_output_path"},
        f"Task {task_key} result_record",
    )
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
    if state["schema_version"] != TASK_STATE_SCHEMA_VERSION:
        raise TaskStateError(f"Task state schema_version must be {TASK_STATE_SCHEMA_VERSION}.")
    if state["queue_generation"] != QUEUE_GENERATION:
        raise TaskStateError(f"Task state queue_generation must be {QUEUE_GENERATION!r}.")
    if not isinstance(state["registry_sha256"], str) or len(state["registry_sha256"]) != 64:
        raise TaskStateError("Task state registry_sha256 must be a full SHA-256 value.")
    if not isinstance(state["last_reconciled_at"], str) or not state["last_reconciled_at"]:
        raise TaskStateError("Task state last_reconciled_at must be a non-empty string.")
    if not isinstance(state["tasks"], dict):
        raise TaskStateError("Task state tasks must be an object.")
    for task_key, record in state["tasks"].items():
        validate_task_record(task_key, record)
    return state


def load_task_state(path: Path) -> dict[str, Any]:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise TaskStateError(f"Task state does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise TaskStateError(f"Task state is not valid JSON: {exc}") from exc
    return validate_task_state(state)


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
