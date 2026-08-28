#!/usr/bin/env python3
"""Archive Phase 2 statistics and start a fresh statistics collection baseline."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import DEFAULT_REGISTRY_PATH, ProviderModelRegistry, load_registry  # noqa: E402
from quota_state import DEFAULT_STATE_PATH as DEFAULT_QUOTA_STATE_PATH  # noqa: E402
from quota_state import load_state as load_quota_state  # noqa: E402
from task_state import load_task_state  # noqa: E402
from update_model_run_statistics import (  # noqa: E402
    DEFAULT_STATISTICS_PAGE,
    DEFAULT_STATISTICS_STATE,
    QUEUE_STATISTICS_SCHEMA_VERSION,
    empty_state,
    refresh_queue_statistics,
    write_state,
)

DEFAULT_TASK_STATE_PATH = Path("data/phase-2/task-state.json")
ARCHIVE_DIRECTORY = Path("docs/methodology/phases/phase-2/history")

COUNTER_FIELDS = (
    "called",
    "valid",
    "invalid",
    "rejected",
    "provider_failed",
    "runner_failed",
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
    "input_tokens_known_events",
    "output_tokens_known_events",
    "reasoning_tokens_known_events",
    "cached_tokens_known_events",
)

TOKEN_FIELDS = ("input_tokens", "output_tokens", "reasoning_tokens", "cached_tokens")


class StatisticsResetError(ValueError):
    """Raised when the statistics reset cannot be prepared or applied safely."""


@dataclass(frozen=True)
class ResetCandidate:
    """Complete candidate outputs for one statistics baseline reset."""

    reset_at: str
    archive_path: Path
    archive_bytes: bytes
    statistics_state: dict[str, Any]
    statistics_page: str


def _resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _normalize_reset_at(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    normalized = value.strip()
    if not normalized:
        raise StatisticsResetError("--reset-at must be a non-empty UTC timestamp.")
    try:
        parsed = datetime.fromisoformat(normalized[:-1] + "+00:00" if normalized.endswith("Z") else normalized)
    except ValueError as exc:
        raise StatisticsResetError(f"Invalid --reset-at timestamp: {value}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise StatisticsResetError("--reset-at must include the UTC timezone.")
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _archive_path(repo_root: Path, reset_at: str) -> Path:
    date = reset_at[:10]
    return repo_root / ARCHIVE_DIRECTORY / f"model-run-statistics-before-reset-{date}.md"


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _assert_fresh_counters(state: Mapping[str, Any]) -> None:
    if state.get("seen_events") != {} or state.get("seen_terminal_events") != {}:
        raise StatisticsResetError("Fresh statistics state unexpectedly contains historical event identities.")
    models = state.get("models")
    if not isinstance(models, Mapping):
        raise StatisticsResetError("Fresh statistics state models must be an object.")
    for key, raw_record in models.items():
        if not isinstance(raw_record, Mapping):
            raise StatisticsResetError(f"Fresh statistics model record is invalid: {key}")
        for field in COUNTER_FIELDS:
            if int(raw_record.get(field, 0) or 0) != 0:
                raise StatisticsResetError(f"Fresh statistics counter is not zero: {key}.{field}")
        for field in TOKEN_FIELDS:
            if raw_record.get(field) is not None:
                raise StatisticsResetError(f"Fresh statistics token total is not unknown: {key}.{field}")


def prepare_reset(
    *,
    repo_root: Path,
    reset_at: str,
    statistics_state_path: Path,
    statistics_page_path: Path,
    registry: ProviderModelRegistry,
    task_state: Mapping[str, Any],
    quota_state: Mapping[str, Any],
) -> ResetCandidate:
    """Build reset outputs in temporary storage without mutating the repository."""
    state_path = _resolve(repo_root, statistics_state_path)
    page_path = _resolve(repo_root, statistics_page_path)
    if not state_path.is_file():
        raise StatisticsResetError(f"Canonical statistics state does not exist: {state_path}")
    if not page_path.is_file():
        raise StatisticsResetError(f"Statistics page does not exist: {page_path}")

    try:
        current_state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StatisticsResetError(f"Canonical statistics state is invalid JSON: {state_path}: {exc}") from exc
    if not isinstance(current_state, dict):
        raise StatisticsResetError("Canonical statistics state must be a JSON object.")
    archive_bytes = page_path.read_bytes()
    try:
        archive_text = archive_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StatisticsResetError(f"Statistics page is not valid UTF-8: {page_path}: {exc}") from exc
    if not archive_text.strip():
        raise StatisticsResetError("Statistics page is empty; refusing to archive an empty snapshot.")

    archive_path = _archive_path(repo_root, reset_at)
    if archive_path.exists() and archive_path.read_bytes() != archive_bytes:
        relative_archive = archive_path.relative_to(repo_root).as_posix()
        raise StatisticsResetError(f"Conflicting statistics archive already exists: {relative_archive}")

    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        candidate_state_path = temporary_root / "statistics-state.json"
        candidate_page_path = temporary_root / "model-run-statistics.md"
        seed = empty_state()
        seed["schema_version"] = QUEUE_STATISTICS_SCHEMA_VERSION
        seed["collection_start_utc"] = reset_at
        write_state(candidate_state_path, seed)
        refresh_queue_statistics(
            statistics_state=candidate_state_path,
            statistics_page=candidate_page_path,
            registry=registry,
            task_state=task_state,
            quota_state=quota_state,
            terminal_events=[],
            timestamp_utc=reset_at,
        )
        candidate_state = json.loads(candidate_state_path.read_text(encoding="utf-8"))
        candidate_page = candidate_page_path.read_text(encoding="utf-8")

    if candidate_state.get("schema_version") != QUEUE_STATISTICS_SCHEMA_VERSION:
        raise StatisticsResetError("Fresh statistics state has the wrong schema version.")
    if candidate_state.get("collection_start_utc") != reset_at:
        raise StatisticsResetError("Fresh statistics state has the wrong collection baseline.")
    if candidate_state.get("generated_at") != reset_at:
        raise StatisticsResetError("Fresh statistics state has the wrong generated_at timestamp.")
    _assert_fresh_counters(candidate_state)

    return ResetCandidate(
        reset_at=reset_at,
        archive_path=archive_path,
        archive_bytes=archive_bytes,
        statistics_state=candidate_state,
        statistics_page=candidate_page,
    )


def apply_reset(
    *,
    candidate: ResetCandidate,
    statistics_state_path: Path,
    statistics_page_path: Path,
) -> None:
    """Persist the archive and fresh canonical statistics outputs."""
    if candidate.archive_path.exists():
        if candidate.archive_path.read_bytes() != candidate.archive_bytes:
            raise StatisticsResetError(f"Conflicting statistics archive already exists: {candidate.archive_path}")
    else:
        _atomic_write_bytes(candidate.archive_path, candidate.archive_bytes)
    write_state(statistics_state_path, candidate.statistics_state)
    _atomic_write_text(statistics_page_path, candidate.statistics_page)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--statistics-state", default=str(DEFAULT_STATISTICS_STATE))
    parser.add_argument("--statistics-page", default=str(DEFAULT_STATISTICS_PAGE))
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--task-state", default=str(DEFAULT_TASK_STATE_PATH))
    parser.add_argument("--quota-state", default=str(DEFAULT_QUOTA_STATE_PATH))
    parser.add_argument("--reset-at", help="UTC baseline timestamp. Defaults to the current UTC time.")
    parser.add_argument("--apply", action="store_true", help="Archive the current page and write the fresh baseline.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    reset_at = _normalize_reset_at(args.reset_at)
    state_path = _resolve(repo_root, args.statistics_state)
    page_path = _resolve(repo_root, args.statistics_page)
    try:
        registry = load_registry(_resolve(repo_root, args.registry))
        task_state = load_task_state(_resolve(repo_root, args.task_state))
        quota_state = load_quota_state(_resolve(repo_root, args.quota_state), registry)
        candidate = prepare_reset(
            repo_root=repo_root,
            reset_at=reset_at,
            statistics_state_path=state_path,
            statistics_page_path=page_path,
            registry=registry,
            task_state=task_state,
            quota_state=quota_state,
        )
        if args.apply:
            apply_reset(
                candidate=candidate,
                statistics_state_path=state_path,
                statistics_page_path=page_path,
            )
        queue = candidate.statistics_state.get("queue", {})
        archive_relative = candidate.archive_path.relative_to(repo_root).as_posix()
        print(
            "Phase 2 statistics baseline reset: "
            f"mode={'apply' if args.apply else 'dry-run'}; reset_at={reset_at}; "
            f"archive={archive_relative}; models={len(candidate.statistics_state.get('models', {}))}; "
            f"desired_tasks={int(queue.get('desired_task_count', 0) or 0)}; "
            f"completed_tasks={int(queue.get('completed', 0) or 0)}; "
            f"written={'true' if args.apply else 'false'}."
        )
        return 0
    except (OSError, StatisticsResetError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
