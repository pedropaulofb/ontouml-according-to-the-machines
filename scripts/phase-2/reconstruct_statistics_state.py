#!/usr/bin/env python3
"""Reconstruct and verify Phase 2 statistics from durable result events.

This verifier is intentionally read-only with respect to the repository. It
rebuilds reconstructible statistics in a temporary directory from durable
``data/phase-2/results/**/*.json`` terminal events plus the task, quota, and
provider-model state from the commit that last wrote the canonical
``data/phase-2/statistics-state.json`` snapshot.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from aggregate_task_results import AggregationError, validate_terminal_event  # noqa: E402
from provider_model_registry import DEFAULT_REGISTRY_PATH, ProviderModelRegistry, load_registry  # noqa: E402
from provider_runtime import parse_timestamp  # noqa: E402
from quota_state import DEFAULT_STATE_PATH as DEFAULT_QUOTA_STATE_PATH  # noqa: E402
from quota_state import load_state as load_quota_state  # noqa: E402
from task_state import load_task_state  # noqa: E402
from update_model_run_statistics import (  # noqa: E402
    DEFAULT_STATISTICS_STATE,
    QUEUE_STATISTICS_SCHEMA_VERSION,
    empty_state,
    refresh_queue_statistics,
)
from update_model_run_statistics import load_state as load_statistics_state  # noqa: E402
from update_model_run_statistics import write_state as write_statistics_state  # noqa: E402

DEFAULT_TASK_STATE_PATH = Path("data/phase-2/task-state.json")
DEFAULT_RESULT_ROOT = Path("data/phase-2/results")

RECONSTRUCTED_TOP_LEVEL_FIELDS = (
    "schema_version",
    "generated_at",
    "collection_start_utc",
    "active_rotation",
    "queue",
    "seen_terminal_events",
)

RECONSTRUCTED_MODEL_FIELDS = (
    "provider",
    "model",
    "spec",
    "called",
    "valid",
    "invalid",
    "rejected",
    "provider_failed",
    "runner_failed",
    "last_run_utc",
    "last_check_status",
    "configuration_status",
    "execution_status",
    "lifecycle_status",
    "total_called",
    "total_provider_attempts",
    "valid_outputs",
    "zero_signal_valid_outputs",
    "valid_outputs_with_signals",
    "validator_rejections",
    "provider_failures",
    "quota_deferrals",
    "policy_blocks",
    "execution_configuration_blocks",
    "temporarily_unavailable_events",
    "runner_failures",
    "input_tokens",
    "input_tokens_known_events",
    "output_tokens",
    "output_tokens_known_events",
    "reasoning_tokens",
    "reasoning_tokens_known_events",
    "cached_tokens",
    "cached_tokens_known_events",
    "current_completed_tasks",
    "current_desired_tasks",
    "completion_percentage",
    "oldest_pending_age_seconds",
    "last_success",
    "last_attempt",
    "last_quota_observation",
    "provider_attempts_accuracy",
)


class ReconstructionError(ValueError):
    """Raised when durable statistics cannot be reconstructed safely."""


def _resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _repo_relative(repo_root: Path, path: Path) -> Path:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(root)
    except ValueError as exc:
        raise ReconstructionError(f"Path must be inside the repository: {path}") from exc


def _git_text(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if completed.returncode != 0:
        diagnostic = (completed.stderr or completed.stdout).strip()
        raise ReconstructionError(f"Git command failed ({' '.join(args)}): {diagnostic or 'unknown error'}")
    return completed.stdout


def _statistics_snapshot_commit(repo_root: Path, statistics_state_path: Path) -> str:
    relative = _repo_relative(repo_root, statistics_state_path).as_posix()
    commit = _git_text(repo_root, "log", "-1", "--format=%H", "--", relative).strip()
    if not commit:
        raise ReconstructionError(f"Could not identify a committed statistics snapshot for {relative}.")
    return commit


def _git_show(repo_root: Path, commit: str, path: Path) -> str:
    relative = _repo_relative(repo_root, path).as_posix()
    return _git_text(repo_root, "show", f"{commit}:{relative}")


def load_snapshot_context(
    *,
    repo_root: Path,
    statistics_state_path: Path,
    registry_path: Path,
    task_state_path: Path,
    quota_state_path: Path,
) -> tuple[str, ProviderModelRegistry, dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load statistics and its queue inputs from one committed snapshot."""
    statistics_path = _resolve(repo_root, statistics_state_path)
    registry_file = _resolve(repo_root, registry_path)
    task_file = _resolve(repo_root, task_state_path)
    quota_file = _resolve(repo_root, quota_state_path)
    snapshot_commit = _statistics_snapshot_commit(repo_root, statistics_path)

    canonical = load_statistics_state(statistics_path)
    try:
        committed_statistics = json.loads(_git_show(repo_root, snapshot_commit, statistics_path))
    except json.JSONDecodeError as exc:
        raise ReconstructionError(f"Committed statistics state is invalid JSON at {snapshot_commit}: {exc}") from exc
    if not isinstance(committed_statistics, dict):
        raise ReconstructionError("Committed statistics state must be a JSON object.")
    if canonical != committed_statistics:
        raise ReconstructionError(
            "Working statistics-state.json differs from its latest committed snapshot; "
            "verify or commit that state before reconstruction."
        )

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        registry_snapshot = root / "provider-models.json"
        task_snapshot = root / "task-state.json"
        quota_snapshot = root / "quota-state.json"
        registry_snapshot.write_text(
            _git_show(repo_root, snapshot_commit, registry_file),
            encoding="utf-8",
            newline="\n",
        )
        task_snapshot.write_text(
            _git_show(repo_root, snapshot_commit, task_file),
            encoding="utf-8",
            newline="\n",
        )
        quota_snapshot.write_text(
            _git_show(repo_root, snapshot_commit, quota_file),
            encoding="utf-8",
            newline="\n",
        )
        registry = load_registry(registry_snapshot)
        task_state = load_task_state(task_snapshot)
        quota_state = load_quota_state(quota_snapshot, registry)

    return snapshot_commit, registry, task_state, quota_state, canonical


def verify_result_tree_matches_snapshot(
    *,
    repo_root: Path,
    snapshot_commit: str,
    result_root: Path,
) -> None:
    """Reject result evidence that is newer or locally modified versus the stats snapshot."""
    result_path = _resolve(repo_root, result_root)
    relative = _repo_relative(repo_root, result_path).as_posix()
    status = _git_text(repo_root, "status", "--porcelain", "--", relative).strip()
    if status:
        raise ReconstructionError(
            "Durable result files contain uncommitted changes; reconstruction requires committed evidence only."
        )
    ancestry = subprocess.run(
        ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", snapshot_commit, "HEAD"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if ancestry.returncode != 0:
        raise ReconstructionError(
            "The statistics snapshot commit is not an ancestor of HEAD; cannot establish "
            "a safe reconstruction baseline."
        )
    changed = _git_text(
        repo_root,
        "diff",
        "--name-only",
        f"{snapshot_commit}..HEAD",
        "--",
        relative,
    ).strip()
    if changed:
        raise ReconstructionError(
            "Durable result files changed after the latest statistics-state commit; "
            "refresh statistics before reconstruction."
        )


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReconstructionError(f"Invalid JSON result event: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReconstructionError(f"Result event must be a JSON object: {path}")
    return value


def load_result_events(
    result_root: Path,
    registry: ProviderModelRegistry,
) -> tuple[list[dict[str, Any]], int]:
    """Load every durable per-attempt result event exactly once."""
    root = Path(result_root)
    if not root.is_dir():
        raise ReconstructionError(f"Result root does not exist: {root}")

    paths = sorted(path for path in root.rglob("*.json") if path.is_file())
    events: list[dict[str, Any]] = []
    attempt_paths: dict[str, Path] = {}

    for path in paths:
        raw = _read_json_object(path)
        try:
            event = validate_terminal_event(raw, registry)
        except (AggregationError, ValueError) as exc:
            raise ReconstructionError(f"Invalid durable result event {path}: {exc}") from exc

        attempt_id = str(event["attempt_id"])
        task_id = str(event["task_id"])
        if path.stem != attempt_id:
            raise ReconstructionError(f"Result filename does not match attempt_id: {path} != {attempt_id}.json")
        if path.parent.name != task_id:
            raise ReconstructionError(f"Result directory does not match task_id: {path.parent.name} != {task_id}")

        previous = attempt_paths.get(attempt_id)
        if previous is not None:
            raise ReconstructionError(f"Duplicate durable result attempt_id {attempt_id}: {previous} and {path}")
        attempt_paths[attempt_id] = path
        events.append(event)

    return events, len(paths)


def filter_collection_window(
    terminal_events: Sequence[Mapping[str, Any]],
    collection_start_utc: object,
) -> tuple[list[Mapping[str, Any]], int]:
    """Keep events counted by the canonical statistics collection window."""
    if not isinstance(collection_start_utc, str) or not collection_start_utc.strip():
        raise ReconstructionError("Canonical statistics require a collection_start_utc timestamp.")
    try:
        collection_start = parse_timestamp(collection_start_utc)
    except ValueError as exc:
        raise ReconstructionError("Canonical statistics collection_start_utc must be a valid UTC timestamp.") from exc

    included: list[Mapping[str, Any]] = []
    excluded = 0
    for event in terminal_events:
        finished_at = parse_timestamp(str(event["attempt_finished_at"]))
        if finished_at < collection_start:
            excluded += 1
        else:
            included.append(event)
    return included, excluded


def reconstruct_statistics(
    *,
    canonical_state: Mapping[str, Any],
    registry: ProviderModelRegistry,
    task_state: Mapping[str, Any],
    quota_state: Mapping[str, Any],
    terminal_events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Rebuild canonical reconstructible statistics without repository writes."""
    if canonical_state.get("schema_version") != QUEUE_STATISTICS_SCHEMA_VERSION:
        raise ReconstructionError(
            f"Statistics reconstruction requires canonical queue statistics schema {QUEUE_STATISTICS_SCHEMA_VERSION}."
        )

    legacy_seen = canonical_state.get("seen_events")
    if not isinstance(legacy_seen, dict):
        raise ReconstructionError("Canonical statistics seen_events must be an object.")
    if legacy_seen:
        raise ReconstructionError(
            "Canonical statistics still contain legacy batch-event counters; "
            "a terminal-event-only reconstruction would be incomplete."
        )

    generated_at = canonical_state.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at.strip():
        raise ReconstructionError("Canonical statistics require a generated_at timestamp.")

    seed = empty_state()
    seed["schema_version"] = QUEUE_STATISTICS_SCHEMA_VERSION
    seed["collection_start_utc"] = canonical_state.get("collection_start_utc")

    with tempfile.TemporaryDirectory() as temporary:
        temporary_root = Path(temporary)
        state_path = temporary_root / "statistics-state.json"
        page_path = temporary_root / "model-run-statistics.md"
        write_statistics_state(state_path, seed)
        refresh_queue_statistics(
            statistics_state=state_path,
            statistics_page=page_path,
            registry=registry,
            task_state=task_state,
            quota_state=quota_state,
            terminal_events=terminal_events,
            timestamp_utc=generated_at,
        )
        return load_statistics_state(state_path)


def compare_reconstruction(
    canonical_state: Mapping[str, Any],
    reconstructed_state: Mapping[str, Any],
) -> list[str]:
    """Return exact mismatches for every reconstructible statistics field."""
    mismatches: list[str] = []

    for field in RECONSTRUCTED_TOP_LEVEL_FIELDS:
        expected = canonical_state.get(field)
        actual = reconstructed_state.get(field)
        if expected != actual:
            mismatches.append(f"{field}: canonical={expected!r}; reconstructed={actual!r}")

    canonical_models = canonical_state.get("models")
    reconstructed_models = reconstructed_state.get("models")
    if not isinstance(canonical_models, dict):
        mismatches.append("models: canonical value is not an object")
        return mismatches
    if not isinstance(reconstructed_models, dict):
        mismatches.append("models: reconstructed value is not an object")
        return mismatches

    canonical_keys = set(canonical_models)
    reconstructed_keys = set(reconstructed_models)
    if canonical_keys != reconstructed_keys:
        missing = sorted(canonical_keys - reconstructed_keys)
        extra = sorted(reconstructed_keys - canonical_keys)
        mismatches.append(f"models.keys: missing={missing!r}; extra={extra!r}")

    for key in sorted(canonical_keys & reconstructed_keys):
        canonical_record = canonical_models[key]
        reconstructed_record = reconstructed_models[key]
        if not isinstance(canonical_record, dict):
            mismatches.append(f"models.{key}: canonical record is not an object")
            continue
        if not isinstance(reconstructed_record, dict):
            mismatches.append(f"models.{key}: reconstructed record is not an object")
            continue
        for field in RECONSTRUCTED_MODEL_FIELDS:
            expected = canonical_record.get(field)
            actual = reconstructed_record.get(field)
            if expected != actual:
                mismatches.append(f"models.{key}.{field}: canonical={expected!r}; reconstructed={actual!r}")

    return mismatches


def verify(
    *,
    repo_root: Path,
    registry_path: Path,
    task_state_path: Path,
    quota_state_path: Path,
    statistics_state_path: Path,
    result_root: Path,
) -> dict[str, int | str]:
    """Reconstruct and verify statistics from repository-local durable evidence."""
    snapshot_commit, registry, task_state, quota_state, canonical = load_snapshot_context(
        repo_root=repo_root,
        statistics_state_path=statistics_state_path,
        registry_path=registry_path,
        task_state_path=task_state_path,
        quota_state_path=quota_state_path,
    )
    verify_result_tree_matches_snapshot(
        repo_root=repo_root,
        snapshot_commit=snapshot_commit,
        result_root=result_root,
    )
    events, result_files = load_result_events(_resolve(repo_root, result_root), registry)
    counted_events, historical_events_excluded = filter_collection_window(
        events,
        canonical.get("collection_start_utc"),
    )
    reconstructed = reconstruct_statistics(
        canonical_state=canonical,
        registry=registry,
        task_state=task_state,
        quota_state=quota_state,
        terminal_events=counted_events,
    )
    mismatches = compare_reconstruction(canonical, reconstructed)
    if mismatches:
        preview = "\n".join(f"- {item}" for item in mismatches[:20])
        suffix = f"\n- ... {len(mismatches) - 20} additional mismatch(es)" if len(mismatches) > 20 else ""
        raise ReconstructionError(f"Statistics reconstruction found {len(mismatches)} mismatch(es):\n{preview}{suffix}")

    canonical_models = canonical.get("models", {})
    seen_terminal_events = canonical.get("seen_terminal_events", {})
    queue = canonical.get("queue", {})
    return {
        "snapshot_commit": snapshot_commit,
        "result_files": result_files,
        "terminal_events": len(counted_events),
        "historical_events_excluded": historical_events_excluded,
        "models": len(canonical_models) if isinstance(canonical_models, dict) else 0,
        "seen_terminal_events": (len(seen_terminal_events) if isinstance(seen_terminal_events, dict) else 0),
        "queue_keys": len(queue) if isinstance(queue, dict) else 0,
        "model_fields": len(RECONSTRUCTED_MODEL_FIELDS),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only reconstruction and verification of Phase 2 statistics.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--task-state", default=str(DEFAULT_TASK_STATE_PATH))
    parser.add_argument("--quota-state", default=str(DEFAULT_QUOTA_STATE_PATH))
    parser.add_argument("--statistics-state", default=str(DEFAULT_STATISTICS_STATE))
    parser.add_argument("--result-root", default=str(DEFAULT_RESULT_ROOT))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
        summary = verify(
            repo_root=repo_root,
            registry_path=Path(args.registry),
            task_state_path=Path(args.task_state),
            quota_state_path=Path(args.quota_state),
            statistics_state_path=Path(args.statistics_state),
            result_root=Path(args.result_root),
        )
    except (OSError, ReconstructionError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(
        "Statistics reconstruction verification: "
        f"snapshot_commit={summary['snapshot_commit']}; "
        f"result_files={summary['result_files']}; "
        f"terminal_events={summary['terminal_events']}; "
        f"historical_events_excluded={summary['historical_events_excluded']}; "
        f"models={summary['models']}; "
        f"seen_terminal_events={summary['seen_terminal_events']}; "
        f"queue_keys={summary['queue_keys']}; "
        f"model_fields={summary['model_fields']}; "
        "mismatches=0; verification=passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
