#!/usr/bin/env python3
"""Validate, persist, publish, and aggregate Phase 2 worker terminal events."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import DEFAULT_REGISTRY_PATH, ProviderModelRegistry, load_registry  # noqa: E402
from provider_runtime import format_timestamp, parse_timestamp, utc_now  # noqa: E402
from quota_state import (  # noqa: E402
    DEFAULT_STATE_PATH as DEFAULT_QUOTA_STATE_PATH,
)
from quota_state import aggregate_events as aggregate_quota_events  # noqa: E402
from quota_state import load_state as load_quota_state  # noqa: E402
from quota_state import validate_event as validate_quota_event  # noqa: E402
from quota_state import write_state as write_quota_state  # noqa: E402
from task_state import load_task_state, validate_task_state, write_task_state  # noqa: E402
from update_model_run_statistics import refresh_queue_statistics  # noqa: E402

EVENT_VERSION = 1
DEFAULT_TASK_STATE_PATH = Path("data/phase-2/task-state.json")
DEFAULT_ARTIFACT_ROOT = Path(".tmp/phase-2/worker-artifacts")
DEFAULT_RESULT_ROOT = Path("data/phase-2/results")
DEFAULT_PUBLICATION_ROOT = Path("data/phase-2/publications")
DEFAULT_REJECTION_ROOT = Path("data/phase-2/rejected-events")
DEFAULT_STATISTICS_PAGE = Path("docs/methodology/phases/phase-2/model-run-statistics.md")
TERMINAL_OUTCOMES = {"valid", "validator_rejected", "provider_failure", "not_called"}
USAGE_FIELDS = ("input_tokens", "output_tokens", "total_tokens", "reasoning_tokens", "cached_tokens")


class AggregationError(ValueError):
    """Raised when a terminal event cannot be applied safely."""


@dataclass(frozen=True)
class TransportEvent:
    path: Path
    value: dict[str, Any]
    source_sha256: str


@dataclass(frozen=True)
class PublicationResult:
    status: str
    diagnostic: str | None = None


Publisher = Callable[[Mapping[str, Any], Path], PublicationResult]


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _require_string(event: Mapping[str, Any], field: str) -> str:
    value = event.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AggregationError(f"Terminal event {field} must be a non-empty string.")
    return value


def validate_terminal_event(raw: Any, registry: ProviderModelRegistry) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise AggregationError("Terminal event must be an object.")
    required = {
        "event_version",
        "task_id",
        "attempt_id",
        "workflow_run_id",
        "worker_id",
        "provider",
        "model",
        "attempt_started_at",
        "attempt_finished_at",
        "outcome",
        "signal_count",
        "provider_attempts",
        "usage",
        "quota_observations",
        "output_sha256",
        "output_artifact",
    }
    missing = sorted(required - raw.keys())
    if missing:
        raise AggregationError(f"Terminal event is missing required field(s): {', '.join(missing)}.")
    if raw["event_version"] != EVENT_VERSION:
        raise AggregationError(f"Terminal event event_version must be {EVENT_VERSION}.")
    for field in ("task_id", "attempt_id", "workflow_run_id", "worker_id", "provider", "model"):
        _require_string(raw, field)
    if registry.find(str(raw["provider"]), str(raw["model"])) is None:
        raise AggregationError(f"Terminal event references an unconfigured slot: {raw['provider']}:{raw['model']}.")
    if raw["worker_id"] != raw["provider"]:
        raise AggregationError("Terminal event worker_id must match provider.")
    try:
        started = parse_timestamp(_require_string(raw, "attempt_started_at"))
        finished = parse_timestamp(_require_string(raw, "attempt_finished_at"))
    except ValueError as exc:
        raise AggregationError("Terminal event timestamps must be valid UTC timestamps.") from exc
    if finished < started:
        raise AggregationError("Terminal event finished before it started.")
    outcome = raw.get("outcome")
    if outcome not in TERMINAL_OUTCOMES:
        raise AggregationError(f"Terminal event has unsupported outcome: {outcome!r}.")
    if not _is_nonnegative_integer(raw.get("signal_count")):
        raise AggregationError("Terminal event signal_count must be a non-negative integer.")
    if not _is_nonnegative_integer(raw.get("provider_attempts")):
        raise AggregationError("Terminal event provider_attempts must be a non-negative integer.")
    if outcome == "not_called" and raw["provider_attempts"] != 0:
        raise AggregationError("A not_called terminal event must record zero provider attempts.")
    if outcome != "not_called" and raw["provider_attempts"] < 1:
        raise AggregationError("A called terminal outcome must record at least one provider attempt.")
    if outcome != "valid" and raw["signal_count"] != 0:
        raise AggregationError("Only a valid terminal event may report signals.")

    usage = raw.get("usage")
    if not isinstance(usage, dict):
        raise AggregationError("Terminal event usage must be an object.")
    normalized_usage: dict[str, int | None] = {}
    for field in USAGE_FIELDS:
        value = usage.get(field)
        if value is not None and not _is_nonnegative_integer(value):
            raise AggregationError(f"Terminal event usage.{field} must be null or a non-negative integer.")
        normalized_usage[field] = value

    observations = raw.get("quota_observations")
    if not isinstance(observations, list):
        raise AggregationError("Terminal event quota_observations must be a list.")
    for observation in observations:
        validated = validate_quota_event(observation, registry)
        if validated.get("task_id") != raw["task_id"]:
            raise AggregationError("Quota observation task_id does not match its terminal event.")
        if validated.get("provider") != raw["provider"] or validated.get("model") != raw["model"]:
            raise AggregationError("Quota observation slot does not match its terminal event.")

    output_sha = raw.get("output_sha256")
    output_artifact = raw.get("output_artifact")
    requires_output = outcome in {"valid", "validator_rejected"}
    if requires_output:
        if not isinstance(output_sha, str) or len(output_sha) != 64:
            raise AggregationError(f"A {outcome} terminal event requires a full output SHA-256.")
        if not isinstance(output_artifact, str) or not output_artifact.strip():
            raise AggregationError(f"A {outcome} terminal event requires an output artifact reference.")
        if Path(output_artifact).is_absolute():
            raise AggregationError("Terminal output artifact references must be repository-relative.")
    elif output_sha is not None or output_artifact is not None:
        raise AggregationError(f"A {outcome} terminal event must not claim an output artifact.")

    normalized = copy.deepcopy(raw)
    normalized["usage"] = normalized_usage
    return normalized


def load_transport_events(root: Path) -> tuple[list[TransportEvent], list[tuple[Path, str]]]:
    events: list[TransportEvent] = []
    rejected: list[tuple[Path, str]] = []
    if not root.exists():
        return events, rejected
    candidates = sorted(
        path for path in root.rglob("*.json") if path.parent.name == "result-events" or "result-events" in path.parts
    )
    for path in candidates:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rejected.append((path, f"Terminal event is not valid JSON: {exc}"))
            continue
        values = raw if isinstance(raw, list) else [raw]
        for index, value in enumerate(values):
            if not isinstance(value, dict) or value.get("event_version") is None:
                rejected.append((path, f"Terminal event #{index + 1} is not an event object."))
                continue
            events.append(TransportEvent(path=path, value=value, source_sha256=_canonical_sha256(value)))
    return events, rejected


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_output_artifact(event: TransportEvent, artifact_root: Path) -> Path:
    reference = Path(str(event.value["output_artifact"]))
    root = artifact_root.resolve()
    references = [reference]
    prefix = Path(".tmp/phase-2")
    try:
        references.append(reference.relative_to(prefix))
    except ValueError:
        pass
    for candidate_reference in references:
        for base in (event.path.parent, *event.path.parents):
            candidate = (base / candidate_reference).resolve()
            if _inside(candidate, root) and candidate.is_file():
                return candidate
            if base.resolve() == root:
                break
        direct = (root / candidate_reference).resolve()
        if _inside(direct, root) and direct.is_file():
            return direct
    raise AggregationError(f"Output artifact is missing from the worker transport: {reference.as_posix()}.")


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as temporary_file:
        json.dump(value, temporary_file, ensure_ascii=False, indent=2, sort_keys=True)
        temporary_file.write("\n")
        temporary_path = Path(temporary_file.name)
    os.replace(temporary_path, path)


def _atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=f".{target.name}.", suffix=".tmp", delete=False) as out:
        temporary_path = Path(out.name)
    try:
        shutil.copyfile(source, temporary_path)
        os.replace(temporary_path, target)
    finally:
        temporary_path.unlink(missing_ok=True)


def _record_rejection(root: Path, transport: TransportEvent | None, path: Path, reason: str) -> None:
    source_hash = transport.source_sha256 if transport is not None else hashlib.sha256(path.read_bytes()).hexdigest()
    value = {
        "schema_version": 1,
        "source_sha256": source_hash,
        "source_filename": path.name,
        "reason": reason,
    }
    _atomic_write_json(root / f"{source_hash}.json", value)


def _lease_matches(task: Mapping[str, Any], event: Mapping[str, Any]) -> bool:
    lease = task.get("lease")
    return isinstance(lease, dict) and all(
        lease.get(field) == event.get(field) for field in ("attempt_id", "workflow_run_id", "worker_id")
    )


def _failure_status(event: Mapping[str, Any]) -> tuple[str, str | None, str]:
    for observation in reversed(event.get("quota_observations") or []):
        failure = observation.get("failure") if isinstance(observation, dict) else None
        if not isinstance(failure, dict):
            continue
        kind = str(failure.get("kind") or "unknown_provider_error")
        status = {
            "rate_or_quota_limited": "deferred_quota",
            "provider_unavailable": "temporarily_unavailable",
            "provider_policy_block": "blocked_provider_policy",
            "execution_configuration_block": "blocked_execution_configuration",
        }.get(kind, "retry_due")
        return status, failure.get("retry_not_before"), kind
    finished = parse_timestamp(str(event["attempt_finished_at"]))
    return "retry_due", format_timestamp(finished + timedelta(hours=1)), "runner_failure"


def _durable_paths(
    repo_root: Path,
    result_root: Path,
    event: Mapping[str, Any],
) -> tuple[Path, Path]:
    directory = repo_root / result_root / str(event["task_id"])
    event_path = directory / f"{event['attempt_id']}.json"
    suffix = ".invalid.md" if event["outcome"] == "validator_rejected" else ".md"
    return event_path, directory / f"{event['attempt_id']}{suffix}"


def _existing_source_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AggregationError(f"Durable result event is corrupted: {path}: {exc}") from exc
    aggregation = value.get("aggregation") if isinstance(value, dict) else None
    return aggregation.get("source_event_sha256") if isinstance(aggregation, dict) else None


def _persist_terminal_event(
    *,
    repo_root: Path,
    result_root: Path,
    publication_root: Path,
    artifact_root: Path,
    transport: TransportEvent,
    event: Mapping[str, Any],
    task: dict[str, Any],
) -> tuple[str, bool]:
    durable_event_path, durable_output_path = _durable_paths(repo_root, result_root, event)
    relative_event_path = durable_event_path.relative_to(repo_root).as_posix()
    existing_hash = _existing_source_hash(durable_event_path)
    already_applied = task["result_record"].get("event_path") == relative_event_path
    if existing_hash is not None and existing_hash != transport.source_sha256:
        raise AggregationError("A distinct terminal event already exists for the same task attempt.")
    if already_applied:
        if existing_hash != transport.source_sha256:
            raise AggregationError("Persisted task state and durable terminal event disagree.")
        return "duplicate", False
    if task.get("status") != "leased" or not _lease_matches(task, event):
        raise AggregationError("Terminal event does not match the task's current persisted lease.")
    identity = task.get("identity", {})
    if identity.get("provider") != event["provider"] or identity.get("model") != event["model"]:
        raise AggregationError("Terminal event provider-model identity does not match its task.")

    output_relative: str | None = None
    if event["outcome"] in {"valid", "validator_rejected"}:
        source_output = resolve_output_artifact(transport, artifact_root)
        if _file_sha256(source_output) != event["output_sha256"]:
            raise AggregationError("Terminal output artifact SHA-256 does not match the event.")
        _atomic_copy(source_output, durable_output_path)
        output_relative = durable_output_path.relative_to(repo_root).as_posix()

    durable_event = {
        key: copy.deepcopy(value) for key, value in event.items() if key not in {"runner_stdout", "runner_stderr"}
    }
    durable_event["output_artifact"] = output_relative
    durable_event["aggregation"] = {
        "source_event_sha256": transport.source_sha256,
        "transport_filename": transport.path.name,
    }
    _atomic_write_json(durable_event_path, durable_event)

    timestamp = str(event["attempt_finished_at"])
    task["updated_at"] = timestamp
    task["lease"] = None
    task["retry_not_before"] = None
    task["result_record"] = {
        "event_path": relative_event_path,
        "output_sha256": event.get("output_sha256"),
        "validated_output_path": output_relative if event["outcome"] == "valid" else None,
    }
    outcome = str(event["outcome"])
    task["last_outcome"] = {
        "kind": outcome,
        "attempt_id": event["attempt_id"],
        "provider_attempts": event["provider_attempts"],
        "finished_at": timestamp,
    }
    if outcome == "valid":
        task["status"] = "completed"
        payload_path = repo_root / publication_root / f"{task['task_id']}.json"
        payload = {
            "schema_version": 1,
            "task_id": task["task_id"],
            "attempt_id": event["attempt_id"],
            "signal_count": event["signal_count"],
            "output_sha256": event["output_sha256"],
            "validated_output_path": output_relative,
        }
        _atomic_write_json(payload_path, payload)
        task["publication"] = {
            "status": "pending",
            "payload_path": payload_path.relative_to(repo_root).as_posix(),
            "last_attempt_at": None,
            "last_error": None,
        }
    elif outcome == "validator_rejected":
        task["validation_rejection_count"] += 1
        if task["validation_rejection_count"] >= 2:
            task["status"] = "blocked_repeated_rejection"
        else:
            task["status"] = "retry_due"
            task["retry_not_before"] = format_timestamp(parse_timestamp(timestamp) + timedelta(hours=1))
        task["publication"]["status"] = "not_required"
    elif outcome == "provider_failure":
        status, retry_not_before, kind = _failure_status(event)
        task["status"] = status
        task["retry_not_before"] = retry_not_before
        task["last_outcome"]["kind"] = kind
        task["publication"]["status"] = "not_required"
    else:
        task["status"] = "pending"
        task["publication"]["status"] = "not_started"
    return "applied", True


def issue_manager_publisher(repo_root: Path, repository: str) -> Publisher:
    def publish(task: Mapping[str, Any], output_path: Path) -> PublicationResult:
        completed = subprocess.run(
            [
                sys.executable,
                str(repo_root / "scripts/phase-2/issue_manager.py"),
                "--comment",
                str(output_path),
                "--repo",
                repository,
                "--task-id",
                str(task["task_id"]),
            ],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
        diagnostic = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
        if completed.returncode != 0:
            return PublicationResult("retry_due", diagnostic[:1000] or "issue manager failed")
        if "Skipped issue creation by default." in completed.stdout:
            return PublicationResult("not_required")
        return PublicationResult("published")

    return publish


def retry_publications(
    *,
    repo_root: Path,
    task_state: dict[str, Any],
    publisher: Publisher,
    timestamp: str,
) -> dict[str, int]:
    counts = {"published": 0, "not_required": 0, "retry_due": 0}
    for task in sorted(task_state["tasks"].values(), key=lambda value: value["task_id"]):
        publication = task["publication"]
        if task["status"] != "completed" or publication["status"] not in {"pending", "retry_due"}:
            continue
        output_reference = task["result_record"].get("validated_output_path")
        if not isinstance(output_reference, str):
            publication["status"] = "retry_due"
            publication["last_attempt_at"] = timestamp
            publication["last_error"] = "validated output path is missing"
            counts["retry_due"] += 1
            continue
        output_path = repo_root / output_reference
        if not output_path.is_file() or _file_sha256(output_path) != task["result_record"].get("output_sha256"):
            publication["status"] = "retry_due"
            publication["last_attempt_at"] = timestamp
            publication["last_error"] = "validated output artifact is missing or corrupted"
            counts["retry_due"] += 1
            continue
        result = publisher(task, output_path)
        if result.status not in counts:
            raise AggregationError(f"Publisher returned unsupported status: {result.status}.")
        publication["status"] = result.status
        publication["last_attempt_at"] = timestamp
        publication["last_error"] = result.diagnostic if result.status == "retry_due" else None
        task["updated_at"] = timestamp
        counts[result.status] += 1
    return counts


def aggregate(
    *,
    repo_root: Path,
    artifact_root: Path,
    registry: ProviderModelRegistry,
    task_state: dict[str, Any],
    quota_state: dict[str, Any],
    result_root: Path = DEFAULT_RESULT_ROOT,
    publication_root: Path = DEFAULT_PUBLICATION_ROOT,
    rejection_root: Path = DEFAULT_REJECTION_ROOT,
    publisher: Publisher | None = None,
    timestamp: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, int], list[dict[str, Any]]]:
    updated_tasks = copy.deepcopy(task_state)
    updated_quota = copy.deepcopy(quota_state)
    counts = {"applied": 0, "duplicate": 0, "rejected": 0, "transport_rejected": 0}
    accepted_events: list[dict[str, Any]] = []
    transport_events, transport_rejections = load_transport_events(artifact_root)
    rejection_path = repo_root / rejection_root
    for path, reason in transport_rejections:
        _record_rejection(rejection_path, None, path, reason)
        counts["transport_rejected"] += 1

    grouped: dict[str, list[TransportEvent]] = {}
    for transport in transport_events:
        attempt_key = str(transport.value.get("attempt_id") or f"invalid:{transport.source_sha256}")
        grouped.setdefault(attempt_key, []).append(transport)
    selected: list[TransportEvent] = []
    for attempt_key, values in sorted(grouped.items()):
        hashes = {value.source_sha256 for value in values}
        if len(hashes) > 1:
            for value in values:
                _record_rejection(
                    rejection_path,
                    value,
                    value.path,
                    f"Conflicting terminal events were delivered for attempt {attempt_key}.",
                )
                counts["rejected"] += 1
            continue
        selected.append(values[0])
        counts["duplicate"] += len(values) - 1

    for transport in selected:
        try:
            event = validate_terminal_event(transport.value, registry)
            task = updated_tasks["tasks"].get(event["task_id"])
            if not isinstance(task, dict):
                raise AggregationError("Terminal event references an unknown task ID.")
            disposition, changed = _persist_terminal_event(
                repo_root=repo_root,
                result_root=result_root,
                publication_root=publication_root,
                artifact_root=artifact_root,
                transport=transport,
                event=event,
                task=task,
            )
            counts[disposition] += 1
            if changed:
                accepted_events.append(event)
        except (AggregationError, OSError, ValueError) as exc:
            _record_rejection(rejection_path, transport, transport.path, str(exc))
            counts["rejected"] += 1

    quota_observations = [
        observation for event in accepted_events for observation in event.get("quota_observations") or []
    ]
    updated_quota, _quota_counts = aggregate_quota_events(updated_quota, quota_observations, registry)
    effective_timestamp = timestamp or format_timestamp(utc_now())
    if publisher is not None:
        publication_counts = retry_publications(
            repo_root=repo_root,
            task_state=updated_tasks,
            publisher=publisher,
            timestamp=effective_timestamp,
        )
        for key, value in publication_counts.items():
            counts[f"publication_{key}"] = value
    validate_task_state(updated_tasks)
    return updated_tasks, updated_quota, counts, accepted_events


def _resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate Phase 2 provider-worker terminal events.")
    parser.add_argument("command", choices=("aggregate", "retry-publication"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--repository", help="GitHub repository in owner/name form for publication.")
    parser.add_argument("--no-publish", action="store_true")
    parser.add_argument("--artifact-root", default=str(DEFAULT_ARTIFACT_ROOT))
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--task-state", default=str(DEFAULT_TASK_STATE_PATH))
    parser.add_argument("--quota-state", default=str(DEFAULT_QUOTA_STATE_PATH))
    parser.add_argument("--result-root", default=str(DEFAULT_RESULT_ROOT))
    parser.add_argument("--publication-root", default=str(DEFAULT_PUBLICATION_ROOT))
    parser.add_argument("--rejection-root", default=str(DEFAULT_REJECTION_ROOT))
    parser.add_argument("--statistics-page", default=str(DEFAULT_STATISTICS_PAGE))
    parser.add_argument("--timestamp")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
        if not args.no_publish and not args.repository:
            raise AggregationError("Publication requires --repository, or use --no-publish.")
        registry = load_registry(_resolve(repo_root, args.registry))
        task_path = _resolve(repo_root, args.task_state)
        quota_path = _resolve(repo_root, args.quota_state)
        task_state = load_task_state(task_path)
        quota_state = load_quota_state(quota_path, registry)
        publisher = None if args.no_publish else issue_manager_publisher(repo_root, args.repository)
        artifact_root = _resolve(repo_root, args.artifact_root)
        if args.command == "retry-publication":
            artifact_root = repo_root / ".tmp/phase-2/no-new-events"
        updated_tasks, updated_quota, counts, accepted_events = aggregate(
            repo_root=repo_root,
            artifact_root=artifact_root,
            registry=registry,
            task_state=task_state,
            quota_state=quota_state,
            result_root=Path(args.result_root),
            publication_root=Path(args.publication_root),
            rejection_root=Path(args.rejection_root),
            publisher=publisher,
            timestamp=args.timestamp,
        )
        write_task_state(task_path, updated_tasks)
        write_quota_state(quota_path, updated_quota, registry)
        refresh_queue_statistics(
            statistics_page=_resolve(repo_root, args.statistics_page),
            registry=registry,
            task_state=updated_tasks,
            quota_state=updated_quota,
            terminal_events=accepted_events,
            timestamp_utc=args.timestamp or format_timestamp(utc_now()),
        )
        print(f"Aggregated Phase 2 terminal events: {json.dumps(counts, sort_keys=True)}")
        return 0
    except (AggregationError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
