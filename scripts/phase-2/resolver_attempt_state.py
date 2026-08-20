#!/usr/bin/env python3
"""Build and persist content-addressed Phase 2 resolver attempts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = 1
ATTEMPT_IDENTITY_VERSION = "resolver-attempt-v1"
DEFAULT_STATE_PATH = Path("data/phase-2/resolver-attempt-state.json")
DEFAULT_EVENT_DIRECTORY = Path(".tmp/phase-2/resolver-attempt-events")
ATTEMPT_STATUSES = {
    "not_called",
    "provider_failure",
    "plan_invalid",
    "execution_failure",
    "completed",
}
BLOCKING_STATUSES = ATTEMPT_STATUSES - {"not_called"}
IDENTITY_FIELDS = {
    "identity_version",
    "issue_number",
    "agent",
    "page_content_sha256",
    "active_signal_snapshot_sha256",
    "resolver_prompt_sha256",
    "resolver_validator_version",
    "provider",
    "model",
    "request_config_sha256",
}


class ResolverAttemptStateError(ValueError):
    """Raised when resolver-attempt identity, events, or state are invalid."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_canonical_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalize_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip()


def active_signal_snapshot(comments: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return a stable snapshot of deterministically selected active comments."""
    snapshot: list[dict[str, Any]] = []
    for comment in comments:
        comment_id = comment.get("comment_id")
        task_id = comment.get("task_id")
        provider = comment.get("provider")
        model = comment.get("model")
        body = comment.get("body")
        if not isinstance(comment_id, (int, str)) or not str(comment_id).strip():
            raise ResolverAttemptStateError("Active signal comments require a non-empty comment_id.")
        if not all(isinstance(value, str) and value.strip() for value in (task_id, provider, model, body)):
            raise ResolverAttemptStateError("Active signal comments require task, provider, model, and body values.")
        snapshot.append(
            {
                "comment_id": str(comment_id).strip(),
                "task_id": task_id.strip(),
                "provider": provider.strip(),
                "model": model.strip(),
                "body": normalize_text(body),
            }
        )
    snapshot.sort(key=lambda item: (item["comment_id"], item["task_id"]))
    if len({item["comment_id"] for item in snapshot}) != len(snapshot):
        raise ResolverAttemptStateError("Active signal snapshot contains duplicate comment IDs.")
    return snapshot


def build_attempt_identity(
    *,
    issue_number: int,
    agent: str,
    page_content_sha256: str,
    active_signal_snapshot_sha256: str,
    resolver_prompt_sha256: str,
    resolver_validator_version: str,
    provider: str,
    model: str,
    request_config_sha256: str,
) -> dict[str, Any]:
    identity = {
        "identity_version": ATTEMPT_IDENTITY_VERSION,
        "issue_number": issue_number,
        "agent": agent,
        "page_content_sha256": page_content_sha256,
        "active_signal_snapshot_sha256": active_signal_snapshot_sha256,
        "resolver_prompt_sha256": resolver_prompt_sha256,
        "resolver_validator_version": resolver_validator_version,
        "provider": provider,
        "model": model,
        "request_config_sha256": request_config_sha256,
    }
    validate_attempt_identity(identity)
    return identity


def validate_attempt_identity(identity: Any) -> dict[str, Any]:
    if not isinstance(identity, dict) or set(identity) != IDENTITY_FIELDS:
        raise ResolverAttemptStateError("Resolver attempt identity has an invalid field set.")
    if identity["identity_version"] != ATTEMPT_IDENTITY_VERSION:
        raise ResolverAttemptStateError("Resolver attempt identity version is unsupported.")
    if not isinstance(identity["issue_number"], int) or identity["issue_number"] < 1:
        raise ResolverAttemptStateError("Resolver attempt issue_number must be a positive integer.")
    for field in IDENTITY_FIELDS - {"issue_number"}:
        value = identity[field]
        if not isinstance(value, str) or not value.strip():
            raise ResolverAttemptStateError(f"Resolver attempt identity field {field} must be non-empty.")
    for field in (
        "page_content_sha256",
        "active_signal_snapshot_sha256",
        "resolver_prompt_sha256",
        "request_config_sha256",
    ):
        value = identity[field]
        if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise ResolverAttemptStateError(f"Resolver attempt identity field {field} must be a SHA-256 value.")
    return identity


def attempt_id_for(identity: Mapping[str, Any]) -> str:
    validate_attempt_identity(dict(identity))
    return sha256_canonical_json(identity)


def build_initial_state(*, timestamp: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "attempts": {},
        "processed_event_ids": [],
        "last_updated_at": timestamp,
    }


def _validate_outcome(
    *,
    status: Any,
    request_sent: Any,
    failure_kind: Any,
    description: str,
) -> None:
    if status not in ATTEMPT_STATUSES or not isinstance(request_sent, bool):
        raise ResolverAttemptStateError(f"{description} has invalid status metadata.")
    if (status == "not_called") == request_sent:
        raise ResolverAttemptStateError(f"{description} has inconsistent request_sent metadata.")
    if status == "completed":
        if failure_kind is not None:
            raise ResolverAttemptStateError(f"{description} must not record a failure_kind when completed.")
    elif not isinstance(failure_kind, str) or not failure_kind.strip():
        raise ResolverAttemptStateError(f"{description} requires a non-empty failure_kind.")


def validate_state(state: Any) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise ResolverAttemptStateError("Resolver attempt state root must be an object.")
    if set(state) != {"schema_version", "attempts", "processed_event_ids", "last_updated_at"}:
        raise ResolverAttemptStateError("Resolver attempt state has an invalid field set.")
    if state["schema_version"] != SCHEMA_VERSION:
        raise ResolverAttemptStateError(f"Resolver attempt state schema_version must be {SCHEMA_VERSION}.")
    if not isinstance(state["attempts"], dict):
        raise ResolverAttemptStateError("Resolver attempt state attempts must be an object.")
    processed = state["processed_event_ids"]
    if not isinstance(processed, list) or not all(isinstance(value, str) and value for value in processed):
        raise ResolverAttemptStateError("Resolver attempt processed_event_ids must be non-empty strings.")
    if len(processed) != len(set(processed)):
        raise ResolverAttemptStateError("Resolver attempt processed_event_ids must be duplicate-free.")
    if not isinstance(state["last_updated_at"], str) or not state["last_updated_at"]:
        raise ResolverAttemptStateError("Resolver attempt state last_updated_at must be non-empty.")
    for attempt_id, record in state["attempts"].items():
        if not isinstance(attempt_id, str) or len(attempt_id) != 64:
            raise ResolverAttemptStateError("Resolver attempt state contains an invalid attempt ID.")
        if not isinstance(record, dict) or set(record) != {
            "attempt_id",
            "identity",
            "status",
            "request_sent",
            "failure_kind",
            "first_observed_at",
            "last_observed_at",
            "last_event_id",
        }:
            raise ResolverAttemptStateError(f"Resolver attempt record {attempt_id} has an invalid field set.")
        validate_attempt_identity(record["identity"])
        if attempt_id_for(record["identity"]) != attempt_id or record["attempt_id"] != attempt_id:
            raise ResolverAttemptStateError(f"Resolver attempt record {attempt_id} does not match its identity.")
        _validate_outcome(
            status=record["status"],
            request_sent=record["request_sent"],
            failure_kind=record["failure_kind"],
            description=f"Resolver attempt record {attempt_id}",
        )
        for field in ("first_observed_at", "last_observed_at", "last_event_id"):
            if not isinstance(record[field], str) or not record[field]:
                raise ResolverAttemptStateError(f"Resolver attempt record {attempt_id} has invalid {field}.")
    return state


def load_state(path: Path = DEFAULT_STATE_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ResolverAttemptStateError(f"Resolver attempt state does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ResolverAttemptStateError(f"Resolver attempt state is not valid JSON: {exc}") from exc
    return validate_state(value)


def write_state(path: Path, state: Mapping[str, Any]) -> None:
    validate_state(dict(state))
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


def _timestamp(value: datetime | None = None) -> str:
    observed = value or datetime.now(timezone.utc)
    return observed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_event(
    *,
    identity: Mapping[str, Any],
    status: str,
    request_sent: bool,
    failure_kind: str | None = None,
    event_directory: Path | None = None,
    observed_at: datetime | None = None,
) -> Path:
    validated_identity = validate_attempt_identity(dict(identity))
    if status not in ATTEMPT_STATUSES:
        raise ResolverAttemptStateError(f"Unsupported resolver attempt status: {status}.")
    if failure_kind is not None and (not isinstance(failure_kind, str) or not failure_kind.strip()):
        raise ResolverAttemptStateError("Resolver attempt failure_kind must be null or non-empty.")
    timestamp = _timestamp(observed_at)
    event_id = f"{time.time_ns():020d}-{uuid.uuid4()}"
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "attempt_id": attempt_id_for(validated_identity),
        "observed_at": timestamp,
        "identity": validated_identity,
        "status": status,
        "request_sent": request_sent,
        "failure_kind": failure_kind,
    }
    validate_event(event)
    directory = event_directory or Path(os.getenv("PHASE2_RESOLVER_ATTEMPT_EVENT_DIR", str(DEFAULT_EVENT_DIRECTORY)))
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{timestamp.replace(':', '')}-{event_id}.json"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=directory,
            prefix=".resolver-attempt-event-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            json.dump(event, temporary_file, ensure_ascii=False, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, target)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return target


def validate_event(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict) or set(event) != {
        "schema_version",
        "event_id",
        "attempt_id",
        "observed_at",
        "identity",
        "status",
        "request_sent",
        "failure_kind",
    }:
        raise ResolverAttemptStateError("Resolver attempt event has an invalid field set.")
    if event["schema_version"] != SCHEMA_VERSION:
        raise ResolverAttemptStateError("Resolver attempt event schema_version is invalid.")
    validate_attempt_identity(event["identity"])
    if event["attempt_id"] != attempt_id_for(event["identity"]):
        raise ResolverAttemptStateError("Resolver attempt event ID does not match its identity.")
    if not isinstance(event["event_id"], str) or not event["event_id"]:
        raise ResolverAttemptStateError("Resolver attempt event event_id must be non-empty.")
    if not isinstance(event["observed_at"], str) or not event["observed_at"]:
        raise ResolverAttemptStateError("Resolver attempt event observed_at must be non-empty.")
    _validate_outcome(
        status=event["status"],
        request_sent=event["request_sent"],
        failure_kind=event["failure_kind"],
        description="Resolver attempt event",
    )
    return event


def load_event_files(event_directory: Path) -> list[dict[str, Any]]:
    if not event_directory.exists():
        return []
    events: list[dict[str, Any]] = []
    for path in sorted(event_directory.glob("*.json")):
        try:
            events.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError as exc:
            raise ResolverAttemptStateError(f"Resolver attempt event is not valid JSON: {path}: {exc}") from exc
    return events


def aggregate_events(
    state: Mapping[str, Any], events: Iterable[Mapping[str, Any]]
) -> tuple[dict[str, Any], dict[str, int]]:
    updated = deepcopy(dict(state))
    validate_state(updated)
    processed = set(updated["processed_event_ids"])
    counts = {"added": 0, "ignored": 0}
    for raw_event in sorted(events, key=lambda item: (str(item.get("observed_at")), str(item.get("event_id")))):
        event = validate_event(dict(raw_event))
        if event["event_id"] in processed:
            counts["ignored"] += 1
            continue
        attempt_id = event["attempt_id"]
        existing = updated["attempts"].get(attempt_id)
        first_observed_at = existing["first_observed_at"] if isinstance(existing, dict) else event["observed_at"]
        if isinstance(existing, dict) and existing["status"] in BLOCKING_STATUSES and event["status"] == "not_called":
            status = existing["status"]
            request_sent = existing["request_sent"]
            failure_kind = existing["failure_kind"]
        else:
            status = event["status"]
            request_sent = event["request_sent"]
            failure_kind = event["failure_kind"]
        updated["attempts"][attempt_id] = {
            "attempt_id": attempt_id,
            "identity": event["identity"],
            "status": status,
            "request_sent": request_sent,
            "failure_kind": failure_kind,
            "first_observed_at": first_observed_at,
            "last_observed_at": event["observed_at"],
            "last_event_id": event["event_id"],
        }
        processed.add(event["event_id"])
        updated["last_updated_at"] = event["observed_at"]
        counts["added"] += 1
    updated["processed_event_ids"] = sorted(processed)
    validate_state(updated)
    return updated, counts


def attempt_record(state: Mapping[str, Any], identity: Mapping[str, Any]) -> dict[str, Any] | None:
    record = state["attempts"].get(attempt_id_for(identity))
    return dict(record) if isinstance(record, dict) else None


def attempt_is_blocked(state: Mapping[str, Any], identity: Mapping[str, Any]) -> bool:
    record = attempt_record(state, identity)
    return bool(record and record["status"] in BLOCKING_STATUSES)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate or aggregate Phase 2 resolver-attempt state.")
    parser.add_argument("command", choices=("initialize", "validate", "aggregate"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH))
    parser.add_argument("--events", default=str(DEFAULT_EVENT_DIRECTORY))
    parser.add_argument("--timestamp")
    return parser.parse_args(argv)


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    state_path = _resolve(repo_root, args.state)
    try:
        if args.command == "initialize":
            write_state(state_path, build_initial_state(timestamp=args.timestamp or _timestamp()))
            print("Initialized Phase 2 resolver-attempt state: attempts=0; processed_events=0.")
            return 0
        state = load_state(state_path)
        if args.command == "validate":
            print(
                f"Valid Phase 2 resolver-attempt state: attempts={len(state['attempts'])}; "
                f"processed_events={len(state['processed_event_ids'])}."
            )
            return 0
        updated, counts = aggregate_events(state, load_event_files(_resolve(repo_root, args.events)))
        write_state(state_path, updated)
        print(f"Aggregated Phase 2 resolver-attempt events: added={counts['added']}; ignored={counts['ignored']}.")
        return 0
    except (OSError, ResolverAttemptStateError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
