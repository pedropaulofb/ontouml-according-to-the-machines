#!/usr/bin/env python3
"""Update cumulative Phase 2 check-agent model run statistics.

The script consumes the deterministic Markdown batch summary written by
`scripts/phase-2/run_check_batch.py` and updates a MkDocs documentation page.
It does not inspect raw provider completions and it does not ask an LLM to
classify validity.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import ProviderModelRegistry, configured_provider_model_specs  # noqa: E402
from provider_runtime import parse_timestamp  # noqa: E402

DEFAULT_STATISTICS_PAGE = Path("docs/methodology/phases/phase-2/model-run-statistics.md")
DEFAULT_SUMMARY_PATH = Path(".tmp/phase-2/batch-summary.md")
STATE_START = "<!-- model-run-statistics-state"
STATE_END = "-->"
STATE_SCHEMA_VERSION = 1
QUEUE_STATISTICS_SCHEMA_VERSION = 2
DEFAULT_PROVIDER_MODEL_SPECS = ",".join(configured_provider_model_specs())

VALID_CHECK_STATUS = "ok"
INVALID_CHECK_STATUSES = {"failed", "provider_failed", "rejected"}
IGNORED_STATUSES = {"skipped", "not-run"}


@dataclass(frozen=True)
class ProviderModelSpec:
    provider: str
    model: str

    @property
    def key(self) -> str:
        return model_key(self.provider, self.model)

    @property
    def spec(self) -> str:
        return f"{self.provider}:{self.model}"


@dataclass(frozen=True)
class SummaryRun:
    row_number: int
    overall_status: str
    check_status: str
    issue_status: str
    provider: str
    model: str

    @property
    def key(self) -> str:
        return model_key(self.provider, self.model)

    @property
    def counting_status(self) -> str:
        """Status used for model-validity counters.

        `run_check_batch.py` can report an overall `failed` status for an
        issue-manager failure even when `run_check_agent.py` produced a valid
        output. Counting uses check status so model validity remains tied to the
        Python-side check-agent validation result.
        """

        return self.check_status or self.overall_status


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def model_key(provider: str, model: str) -> str:
    return f"{provider.strip()}:{model.strip()}"


def strip_code(value: str) -> str:
    normalized = value.strip()
    if normalized.startswith("`") and normalized.endswith("`") and len(normalized) >= 2:
        normalized = normalized[1:-1].strip()
    return normalized


def markdown_escape(value: object) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|").replace("\n", " ")


def split_markdown_row(row: str) -> list[str]:
    stripped = row.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped[1:-1]:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            current.append(char)
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def normalized_header_name(value: str) -> str:
    return re.sub(r"\s+", " ", strip_code(value).strip().lower())


def parse_provider_model_specs(value: str) -> list[ProviderModelSpec]:
    specs: list[ProviderModelSpec] = []
    normalized = value.replace("\n", ",")
    for raw_spec in normalized.split(","):
        spec = raw_spec.strip()
        if not spec:
            continue
        if ":" not in spec:
            raise ValueError(f"Invalid provider:model spec without colon: {spec}")
        provider, model = spec.split(":", 1)
        provider = provider.strip()
        model = model.strip()
        if not provider or not model:
            raise ValueError(f"Invalid empty provider or model in spec: {spec}")
        specs.append(ProviderModelSpec(provider=provider, model=model))
    if not specs:
        raise ValueError("No usable provider:model specs were provided.")
    return specs


def cells_are_separator(cells: Sequence[str]) -> bool:
    return bool(cells) and all(cell and set(cell) <= {"-", ":"} for cell in cells)


def row_value(cells: Sequence[str], header: dict[str, int], *names: str, fallback_index: int | None = None) -> str:
    for name in names:
        index = header.get(name)
        if index is not None and index < len(cells):
            return strip_code(cells[index]).strip()
    if fallback_index is not None and fallback_index < len(cells):
        return strip_code(cells[fallback_index]).strip()
    return ""


def parse_batch_summary(summary_path: Path) -> list[SummaryRun]:
    if not summary_path.is_file():
        raise FileNotFoundError(f"Batch summary does not exist: {summary_path}")
    runs: list[SummaryRun] = []
    in_runs_table = False
    header: dict[str, int] = {}
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## Runs":
            in_runs_table = True
            continue
        if not in_runs_table:
            continue
        if not line.lstrip().startswith("|"):
            if runs:
                break
            continue
        cells = split_markdown_row(line)
        if not cells:
            continue
        normalized_cells = [normalized_header_name(cell) for cell in cells]
        if "provider" in normalized_cells and "model" in normalized_cells:
            header = {name: index for index, name in enumerate(normalized_cells)}
            continue
        if cells_are_separator(cells):
            continue

        row_number_text = row_value(cells, header, "#", fallback_index=0)
        try:
            row_number = int(row_number_text)
        except ValueError:
            continue

        overall_status = row_value(cells, header, "status", fallback_index=1).lower()
        check_status = row_value(cells, header, "check status", fallback_index=1).lower()
        issue_status = row_value(cells, header, "issue status", fallback_index=1).lower()
        provider = row_value(cells, header, "provider", fallback_index=4)
        model = row_value(cells, header, "model", fallback_index=5)
        if provider and model and overall_status:
            runs.append(
                SummaryRun(
                    row_number=row_number,
                    overall_status=overall_status,
                    check_status=check_status or overall_status,
                    issue_status=issue_status or overall_status,
                    provider=provider,
                    model=model,
                )
            )
    return runs


def empty_state() -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "generated_at": None,
        "collection_start_utc": None,
        "active_rotation": [],
        "models": {},
        "seen_events": {},
        "seen_terminal_events": {},
        "queue": {},
    }


def earliest_seen_event_timestamp(state: dict[str, Any]) -> str:
    """Return the earliest persisted counted-event timestamp, if available."""

    timestamps: list[str] = []
    seen_events = state.get("seen_events", {})
    if not isinstance(seen_events, dict):
        return ""
    for raw_event in seen_events.values():
        if not isinstance(raw_event, dict):
            continue
        timestamp = str(raw_event.get("timestamp_utc", "") or "").strip()
        if timestamp:
            timestamps.append(timestamp)
    return min(timestamps) if timestamps else ""


def ensure_collection_start_utc(state: dict[str, Any]) -> str:
    """Set collection_start_utc from persisted event evidence when missing."""

    current = str(state.get("collection_start_utc") or "").strip()
    if current:
        state["collection_start_utc"] = current
        return current

    earliest = earliest_seen_event_timestamp(state)
    state["collection_start_utc"] = earliest or None
    return earliest


def extract_state(page_text: str) -> dict[str, Any]:
    start = page_text.find(STATE_START)
    if start == -1:
        return empty_state()
    json_start = page_text.find("\n", start)
    if json_start == -1:
        return empty_state()
    end = page_text.find(STATE_END, json_start)
    if end == -1:
        return empty_state()
    payload = page_text[json_start:end].strip()
    if not payload:
        return empty_state()
    try:
        state = json.loads(payload)
    except json.JSONDecodeError:
        return empty_state()
    if not isinstance(state, dict):
        return empty_state()
    state.setdefault("schema_version", STATE_SCHEMA_VERSION)
    state.setdefault("generated_at", None)
    state.setdefault("collection_start_utc", None)
    state.setdefault("active_rotation", [])
    state.setdefault("models", {})
    state.setdefault("seen_events", {})
    state.setdefault("seen_terminal_events", {})
    state.setdefault("queue", {})
    ensure_collection_start_utc(state)
    return state


def load_state(statistics_page: Path) -> dict[str, Any]:
    if not statistics_page.exists():
        return empty_state()
    return extract_state(statistics_page.read_text(encoding="utf-8"))


def ensure_model_record(state: dict[str, Any], spec: ProviderModelSpec) -> dict[str, Any]:
    models = state.setdefault("models", {})
    record = models.setdefault(
        spec.key,
        {
            "provider": spec.provider,
            "model": spec.model,
            "spec": spec.spec,
            "called": 0,
            "valid": 0,
            "invalid": 0,
            "rejected": 0,
            "provider_failed": 0,
            "runner_failed": 0,
            "last_run_utc": "",
            "last_check_status": "",
            "last_issue_status": "",
            "last_overall_status": "",
            "last_event_name": "",
            "last_run_id": "",
            "last_run_attempt": "",
        },
    )
    record.setdefault("provider", spec.provider)
    record.setdefault("model", spec.model)
    record.setdefault("spec", spec.spec)
    for counter in ("called", "valid", "invalid", "rejected", "provider_failed", "runner_failed"):
        record[counter] = int(record.get(counter, 0) or 0)
    legacy_last_status = str(record.get("last_status", "") or "")
    record.setdefault("last_run_utc", "")
    record.setdefault("last_check_status", legacy_last_status)
    record.setdefault("last_issue_status", "")
    record.setdefault("last_overall_status", legacy_last_status)
    for key in ("last_event_name", "last_run_id", "last_run_attempt"):
        record.setdefault(key, "")
    record.setdefault("configuration_status", "retired")
    record.setdefault("execution_status", "inactive")
    record.setdefault("lifecycle_status", "retired")
    record.setdefault("total_called", record["called"])
    record.setdefault("total_provider_attempts", record["called"])
    record.setdefault("valid_outputs", record["valid"])
    record.setdefault("zero_signal_valid_outputs", 0)
    record.setdefault("valid_outputs_with_signals", 0)
    record.setdefault("validator_rejections", record["rejected"])
    record.setdefault("provider_failures", record["provider_failed"])
    record.setdefault("quota_deferrals", 0)
    record.setdefault("policy_blocks", 0)
    record.setdefault("execution_configuration_blocks", 0)
    record.setdefault("temporarily_unavailable_events", 0)
    record.setdefault("runner_failures", record["runner_failed"])
    for field in ("input_tokens", "output_tokens", "reasoning_tokens", "cached_tokens"):
        record.setdefault(field, None)
        record.setdefault(f"{field}_known_events", 0)
    record.setdefault("current_completed_tasks", 0)
    record.setdefault("current_desired_tasks", 0)
    record.setdefault("completion_percentage", 0.0)
    record.setdefault("oldest_pending_age_seconds", None)
    record.setdefault("last_success", record["last_run_utc"] if record["valid"] else "")
    record.setdefault("last_attempt", record["last_run_utc"])
    record.setdefault("last_quota_observation", "")
    record.setdefault("provider_attempts_accuracy", "inferred-from-legacy-calls")
    return record


def normalize_existing_models(state: dict[str, Any]) -> None:
    models = state.setdefault("models", {})
    for key, raw_record in list(models.items()):
        if not isinstance(raw_record, dict):
            del models[key]
            continue
        provider = str(raw_record.get("provider", "")).strip()
        model = str(raw_record.get("model", "")).strip()
        if not provider or not model:
            del models[key]
            continue
        ensure_model_record(state, ProviderModelSpec(provider=provider, model=model))


def active_model_keys(state: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for raw_spec in state.get("active_rotation", []):
        if not isinstance(raw_spec, dict):
            continue
        provider = str(raw_spec.get("provider", "") or "").strip()
        model = str(raw_spec.get("model", "") or "").strip()
        if provider and model:
            keys.add(model_key(provider, model))
    return keys


def model_record_status(record: dict[str, Any], active_keys: set[str]) -> str:
    provider = str(record.get("provider", "") or "").strip()
    model = str(record.get("model", "") or "").strip()
    return "active" if provider and model and model_key(provider, model) in active_keys else "inactive"


def event_key(*, run_id: str, run_attempt: str, workflow: str, summary_run: SummaryRun) -> str:
    return "|".join(
        [
            run_id.strip() or "local",
            run_attempt.strip() or "0",
            workflow.strip() or "unknown-workflow",
            str(summary_run.row_number),
            summary_run.provider,
            summary_run.model,
            summary_run.overall_status,
            summary_run.check_status,
            summary_run.issue_status,
        ]
    )


def apply_summary_runs(
    *,
    state: dict[str, Any],
    active_specs: Sequence[ProviderModelSpec],
    summary_runs: Iterable[SummaryRun],
    run_id: str,
    run_attempt: str,
    workflow: str,
    event_name: str,
    commit_sha: str,
    timestamp_utc: str,
) -> tuple[int, int]:
    normalize_existing_models(state)
    ensure_collection_start_utc(state)
    state["active_rotation"] = [
        {"provider": spec.provider, "model": spec.model, "spec": spec.spec} for spec in active_specs
    ]
    for spec in active_specs:
        ensure_model_record(state, spec)

    seen_events = state.setdefault("seen_events", {})
    added = 0
    ignored = 0

    for summary_run in summary_runs:
        counting_status = summary_run.counting_status
        if counting_status in IGNORED_STATUSES:
            ignored += 1
            continue
        if counting_status != VALID_CHECK_STATUS and counting_status not in INVALID_CHECK_STATUSES:
            ignored += 1
            continue
        spec = ProviderModelSpec(provider=summary_run.provider, model=summary_run.model)
        record = ensure_model_record(state, spec)
        key = event_key(run_id=run_id, run_attempt=run_attempt, workflow=workflow, summary_run=summary_run)
        if key in seen_events:
            ignored += 1
            continue

        record["called"] += 1
        record["total_called"] += 1
        record["total_provider_attempts"] += 1
        record["provider_attempts_accuracy"] = "inferred-from-legacy-calls"
        if counting_status == VALID_CHECK_STATUS:
            record["valid"] += 1
            record["valid_outputs"] += 1
            record["last_success"] = timestamp_utc
        else:
            record["invalid"] += 1
            if counting_status == "rejected":
                record["rejected"] += 1
                record["validator_rejections"] += 1
            elif counting_status == "provider_failed":
                record["provider_failed"] += 1
                record["provider_failures"] += 1
            elif counting_status == "failed":
                record["runner_failed"] += 1
                record["runner_failures"] += 1
        record["last_run_utc"] = timestamp_utc
        record["last_check_status"] = summary_run.check_status
        record["last_issue_status"] = summary_run.issue_status
        record["last_overall_status"] = summary_run.overall_status
        record["last_event_name"] = event_name
        record["last_run_id"] = run_id
        record["last_run_attempt"] = run_attempt
        record["last_attempt"] = timestamp_utc
        seen_events[key] = {
            "timestamp_utc": timestamp_utc,
            "provider": summary_run.provider,
            "model": summary_run.model,
            "overall_status": summary_run.overall_status,
            "check_status": summary_run.check_status,
            "issue_status": summary_run.issue_status,
            "event_name": event_name,
            "commit_sha": commit_sha,
        }
        added += 1

    ensure_collection_start_utc(state)
    state["generated_at"] = timestamp_utc
    return added, ignored


def _terminal_failure_kinds(event: Mapping[str, Any]) -> set[str]:
    kinds: set[str] = set()
    for observation in event.get("quota_observations") or []:
        failure = observation.get("failure") if isinstance(observation, dict) else None
        if isinstance(failure, dict) and failure.get("kind"):
            kinds.add(str(failure["kind"]))
    return kinds


def apply_terminal_events(state: dict[str, Any], terminal_events: Iterable[Mapping[str, Any]]) -> tuple[int, int]:
    """Apply validated queue terminal events without double-counting an attempt."""
    normalize_existing_models(state)
    seen = state.setdefault("seen_terminal_events", {})
    added = 0
    ignored = 0
    for event in sorted(
        terminal_events,
        key=lambda value: (str(value.get("attempt_finished_at")), str(value.get("attempt_id"))),
    ):
        attempt_id = str(event.get("attempt_id") or "")
        if not attempt_id or attempt_id in seen:
            ignored += 1
            continue
        spec = ProviderModelSpec(provider=str(event["provider"]), model=str(event["model"]))
        record = ensure_model_record(state, spec)
        provider_attempts = int(event.get("provider_attempts", 0) or 0)
        outcome = str(event.get("outcome"))
        if provider_attempts:
            record["called"] += 1
            record["total_called"] += 1
            record["total_provider_attempts"] += provider_attempts
            record["provider_attempts_accuracy"] = "mixed-inferred-and-locally-counted"
        if outcome == "valid":
            record["valid"] += 1
            record["valid_outputs"] += 1
            if int(event.get("signal_count", 0) or 0) == 0:
                record["zero_signal_valid_outputs"] += 1
            else:
                record["valid_outputs_with_signals"] += 1
            record["last_success"] = str(event["attempt_finished_at"])
            record["last_check_status"] = "ok"
        elif outcome == "validator_rejected":
            record["invalid"] += 1
            record["rejected"] += 1
            record["validator_rejections"] += 1
            record["last_check_status"] = "rejected"
        elif outcome == "provider_failure":
            record["invalid"] += 1
            record["provider_failed"] += 1
            record["provider_failures"] += 1
            record["last_check_status"] = "provider_failed"

        failure_kinds = _terminal_failure_kinds(event)
        record["quota_deferrals"] += int("rate_or_quota_limited" in failure_kinds)
        record["policy_blocks"] += int("provider_policy_block" in failure_kinds)
        record["execution_configuration_blocks"] += int("execution_configuration_block" in failure_kinds)
        record["temporarily_unavailable_events"] += int("provider_unavailable" in failure_kinds)
        if outcome == "provider_failure" and not failure_kinds:
            record["runner_failed"] += 1
            record["runner_failures"] += 1

        usage = event.get("usage") if isinstance(event.get("usage"), dict) else {}
        for field in ("input_tokens", "output_tokens", "reasoning_tokens", "cached_tokens"):
            value = usage.get(field)
            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                record[field] = int(record[field] or 0) + value
                record[f"{field}_known_events"] += 1

        finished_at = str(event["attempt_finished_at"])
        record["last_attempt"] = finished_at
        record["last_run_utc"] = finished_at
        quota_timestamps = [
            str(observation.get("observed_at"))
            for observation in event.get("quota_observations") or []
            if isinstance(observation, dict) and observation.get("observed_at")
        ]
        if quota_timestamps:
            record["last_quota_observation"] = max(quota_timestamps)
        seen[attempt_id] = {
            "provider": spec.provider,
            "model": spec.model,
            "outcome": outcome,
            "attempt_finished_at": finished_at,
        }
        added += 1
    return added, ignored


def _queue_status_counts(task_state: Mapping[str, Any]) -> dict[str, int]:
    labels = {
        "pending": "pending",
        "leased": "leased",
        "completed": "completed",
        "retry_due": "retry_due",
        "deferred_quota": "quota_deferred",
        "temporarily_unavailable": "temporarily_unavailable",
        "blocked_provider_policy": "policy_blocked",
        "blocked_execution_configuration": "execution_configuration_blocked",
        "blocked_repeated_rejection": "rejection_blocked",
        "blocked_ambiguous_attempt": "ambiguous_attempt_blocked",
        "retired": "retired",
        "obsolete": "obsolete",
    }
    counts = {label: 0 for label in labels.values()}
    for task in task_state.get("tasks", {}).values():
        status = task.get("status")
        if status in labels:
            counts[labels[status]] += 1
    counts["desired_task_count"] = sum(
        task.get("status") not in {"retired", "obsolete"} for task in task_state.get("tasks", {}).values()
    )
    return counts


def _last_quota_observation(quota_state: Mapping[str, Any], group_ids: Sequence[str]) -> str:
    timestamps = [
        str(quota_state.get("quota_groups", {}).get(group_id, {}).get("last_updated_at") or "")
        for group_id in group_ids
    ]
    return max((value for value in timestamps if value), default="")


def refresh_queue_statistics(
    *,
    statistics_page: Path,
    registry: ProviderModelRegistry,
    task_state: Mapping[str, Any],
    quota_state: Mapping[str, Any],
    terminal_events: Iterable[Mapping[str, Any]],
    timestamp_utc: str,
) -> None:
    """Refresh cumulative outcomes and the current queue snapshot in one Markdown artifact."""
    state = load_state(statistics_page)
    state["schema_version"] = QUEUE_STATISTICS_SCHEMA_VERSION
    state["active_rotation"] = [
        {"provider": slot.provider, "model": slot.model, "spec": slot.spec} for slot in registry.configured_slots
    ]
    normalize_existing_models(state)
    apply_terminal_events(state, terminal_events)
    snapshot_time = parse_timestamp(timestamp_utc)
    configured_keys: set[str] = set()
    schedulable_statuses = {"pending", "leased", "retry_due", "deferred_quota", "temporarily_unavailable"}
    for slot in registry.slots:
        spec = ProviderModelSpec(slot.provider, slot.model)
        configured_keys.add(spec.key)
        record = ensure_model_record(state, spec)
        runtime = quota_state.get("runtime_slots", {}).get(slot.spec, {})
        record["configuration_status"] = slot.configuration_status
        record["execution_status"] = str(runtime.get("status") or slot.execution_status)
        record["lifecycle_status"] = slot.lifecycle
        if int(record.get("called", 0) or 0) == 0:
            record["provider_attempts_accuracy"] = "locally-counted"
        relevant = [
            task
            for task in task_state.get("tasks", {}).values()
            if task.get("identity", {}).get("provider") == slot.provider
            and task.get("identity", {}).get("model") == slot.model
            and task.get("status") not in {"obsolete", "retired"}
        ]
        desired = len(relevant)
        completed = sum(task.get("status") == "completed" for task in relevant)
        record["current_desired_tasks"] = desired
        record["current_completed_tasks"] = completed
        record["completion_percentage"] = round((completed / desired * 100) if desired else 0.0, 2)
        pending_created = [
            str(task.get("created_at"))
            for task in relevant
            if task.get("status") in schedulable_statuses and task.get("created_at")
        ]
        if pending_created:
            oldest = min(parse_timestamp(value) for value in pending_created)
            record["oldest_pending_age_seconds"] = max(0, int((snapshot_time - oldest).total_seconds()))
        else:
            record["oldest_pending_age_seconds"] = None
        quota_observation = _last_quota_observation(quota_state, slot.quota_groups)
        if quota_observation:
            record["last_quota_observation"] = max(str(record.get("last_quota_observation") or ""), quota_observation)

    for key, record in state.get("models", {}).items():
        if key in configured_keys:
            continue
        record["configuration_status"] = "retired"
        record["execution_status"] = "inactive"
        record["lifecycle_status"] = "retired"
        record["current_desired_tasks"] = 0
        record["current_completed_tasks"] = 0
        record["completion_percentage"] = 0.0
        record["oldest_pending_age_seconds"] = None

    state["queue"] = _queue_status_counts(task_state)
    state["generated_at"] = timestamp_utc
    ensure_collection_start_utc(state)
    statistics_page.parent.mkdir(parents=True, exist_ok=True)
    statistics_page.write_text(render_markdown(state), encoding="utf-8")


def sorted_model_records(state: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        state.get("models", {}).values(),
        key=lambda record: (str(record.get("provider", "")), str(record.get("model", ""))),
    )


def _token_display(record: Mapping[str, Any], field: str) -> str:
    if int(record.get(f"{field}_known_events", 0) or 0) == 0:
        return "`unknown`"
    return str(int(record.get(field, 0) or 0))


def _age_display(value: Any) -> str:
    if not isinstance(value, int) or isinstance(value, bool):
        return ""
    days, remainder = divmod(value, 86400)
    hours = remainder // 3600
    return f"{days}d {hours}h" if days else f"{hours}h"


def render_markdown(state: dict[str, Any]) -> str:
    normalize_existing_models(state)
    generated_at = state.get("generated_at") or "not generated yet"
    collection_start_utc = ensure_collection_start_utc(state) or "not recorded yet"
    active_keys = active_model_keys(state)
    lines: list[str] = [
        "# Phase 2 — Model Run Statistics",
        "",
        "← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →",
        "",
        "This page stores cumulative execution statistics and the current queue snapshot for the scheduled Phase 2 check-agent signal collector.",
        "",
        "The tables are updated from deterministic queue state, validated terminal events, and provider quota observations.",
        "",
        "The current desired universe is 39 canonical pages × 2 LLM check agents × 26 configured provider-model slots = 2,028 tasks. Historical obsolete and retired identities remain stored, so total records may be higher.",
        "",
        f"Statistics collection started on: `{collection_start_utc}`",
        "",
        "Counts shown on this page only include executions recorded since that start time.",
        "",
        "Models not present in the configured, non-retired registry remain listed as `inactive` for historical continuity.",
        "",
        f"Last generated: `{generated_at}`",
        "",
        "## Queue snapshot",
        "",
        "| Queue state | Tasks |",
        "|---|---:|",
    ]
    queue = state.get("queue", {})
    for key in (
        "desired_task_count",
        "pending",
        "leased",
        "completed",
        "retry_due",
        "quota_deferred",
        "temporarily_unavailable",
        "policy_blocked",
        "execution_configuration_blocked",
        "rejection_blocked",
        "ambiguous_attempt_blocked",
        "retired",
        "obsolete",
    ):
        lines.append(f"| `{key}` | {int(queue.get(key, 0) or 0)} |")

    lines.extend(
        [
            "",
            "## Provider–model outcomes",
            "",
            "| Provider | Model | Status | Configuration | Execution | Lifecycle | Called | Provider attempts | Valid | Zero-signal valid | Valid with signals | Validator rejections | Provider failures | Quota deferrals | Policy blocks | Execution-config blocks | Temporarily unavailable | Runner failures |",
            "|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for record in sorted_model_records(state):
        status = model_record_status(record, active_keys)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(record.get('provider', ''))}`",
                    f"`{markdown_escape(record.get('model', ''))}`",
                    f"`{status}`",
                    f"`{markdown_escape(record.get('configuration_status', ''))}`",
                    f"`{markdown_escape(record.get('execution_status', ''))}`",
                    f"`{markdown_escape(record.get('lifecycle_status', ''))}`",
                    str(int(record.get("total_called", 0) or 0)),
                    str(int(record.get("total_provider_attempts", 0) or 0)),
                    str(int(record.get("valid_outputs", 0) or 0)),
                    str(int(record.get("zero_signal_valid_outputs", 0) or 0)),
                    str(int(record.get("valid_outputs_with_signals", 0) or 0)),
                    str(int(record.get("validator_rejections", 0) or 0)),
                    str(int(record.get("provider_failures", 0) or 0)),
                    str(int(record.get("quota_deferrals", 0) or 0)),
                    str(int(record.get("policy_blocks", 0) or 0)),
                    str(int(record.get("execution_configuration_blocks", 0) or 0)),
                    str(int(record.get("temporarily_unavailable_events", 0) or 0)),
                    str(int(record.get("runner_failures", 0) or 0)),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Current slot progress",
            "",
            "| Provider | Model | Completed | Desired | Completion | Oldest pending | Last success | Last attempt | Last quota observation |",
            "|---|---|---:|---:|---:|---|---|---|---|",
        ]
    )
    for record in sorted_model_records(state):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(record.get('provider', ''))}`",
                    f"`{markdown_escape(record.get('model', ''))}`",
                    str(int(record.get("current_completed_tasks", 0) or 0)),
                    str(int(record.get("current_desired_tasks", 0) or 0)),
                    f"{float(record.get('completion_percentage', 0.0) or 0.0):.2f}%",
                    _age_display(record.get("oldest_pending_age_seconds")),
                    f"`{markdown_escape(record.get('last_success', ''))}`" if record.get("last_success") else "",
                    f"`{markdown_escape(record.get('last_attempt', ''))}`" if record.get("last_attempt") else "",
                    f"`{markdown_escape(record.get('last_quota_observation', ''))}`"
                    if record.get("last_quota_observation")
                    else "",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Token observations",
            "",
            "| Provider | Model | Input tokens | Output tokens | Reasoning tokens | Cached tokens |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for record in sorted_model_records(state):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(record.get('provider', ''))}`",
                    f"`{markdown_escape(record.get('model', ''))}`",
                    _token_display(record, "input_tokens"),
                    _token_display(record, "output_tokens"),
                    _token_display(record, "reasoning_tokens"),
                    _token_display(record, "cached_tokens"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Status derivation and accuracy",
            "",
            "- `Status` is derived from the hidden configured-slot snapshot: configured, non-retired models are `active`; previously recorded models outside it are `inactive`.",
            "- Historical called, valid, rejection, provider-failure, and runner-failure values are preserved from the previous aggregate statistics.",
            "- Historical provider-attempt totals are inferred as one attempt per legacy call; new queue attempts are locally counted from validated terminal events.",
            "- Queue completion and age fields are derived from `task-state.json`; configuration and lifecycle come from the registry; execution status comes from runtime quota state when present.",
            "- Token values are provider-reported when available and then locally summed. `unknown` is distinct from a reported value of zero.",
            "- Quota state is best-known capacity, not a guarantee. Provenance marks observations as provider-reported, locally counted, configured, inferred, or unknown, and `estimated: true` explicitly identifies estimates such as remaining capacity.",
            "",
            "## Storage strategy and limitations",
            "",
            "The human-readable tables are rendered from hidden JSON state stored in this Markdown file. Durable task results and publication payloads are stored separately under `data/phase-2/`.",
            "",
            "The collector aggregator commits this page with task state, quota state, and durable results after each run that changes repository state.",
            "",
            "Push conflicts are handled by fetching the latest branch and idempotently reapplying the same validated terminal events before a bounded retry.",
            "",
            "The hidden state stores legacy batch-event keys and queue attempt IDs for de-duplication. This prevents accidental double-counting but means the Markdown file grows over time.",
            "",
            "This page does not store secrets, raw prompts, raw completions, or provider response bodies.",
            "",
            STATE_START,
            json.dumps(state, indent=2, sort_keys=True),
            STATE_END,
            "",
            "---",
            "",
            "← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →",
            "",
        ]
    )
    return "\n".join(lines)


def update_statistics_page(args: argparse.Namespace) -> int:
    active_specs = parse_provider_model_specs(args.provider_model_specs)
    summary_runs = parse_batch_summary(Path(args.summary))
    state = load_state(Path(args.statistics_page))
    added, ignored = apply_summary_runs(
        state=state,
        active_specs=active_specs,
        summary_runs=summary_runs,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        workflow=args.workflow,
        event_name=args.event_name,
        commit_sha=args.commit_sha,
        timestamp_utc=args.timestamp_utc or utc_now_iso(),
    )
    rendered = render_markdown(state)
    if args.dry_run:
        print(rendered)
    else:
        statistics_page = Path(args.statistics_page)
        statistics_page.parent.mkdir(parents=True, exist_ok=True)
        statistics_page.write_text(rendered, encoding="utf-8")
    print(f"Processed model-run statistics events: added={added}, ignored={ignored}")
    return 0


def write_self_test_summary(
    path: Path,
    *,
    overall_status: str,
    check_status: str,
    issue_status: str,
    provider: str,
    model: str,
) -> None:
    path.write_text(
        "\n".join(
            [
                "# Phase 2 check batch summary",
                "",
                "## Runs",
                "",
                "| # | Status | Check status | Issue status | Page | Agent | Provider | Model | Output | Log | Message |",
                "|---:|---|---|---|---|---|---|---|---|---|---|",
                f"| 1 | `{overall_status}` | `{check_status}` | `{issue_status}` | `docs/stereotypes/classes/event.md` | `page-hygiene-checker` | `{provider}` | `{model}` | `.tmp/out.md` | `.tmp/out.log` | test |",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        summary = root / "batch-summary.md"
        page = root / "model-run-statistics.md"
        specs = DEFAULT_PROVIDER_MODEL_SPECS

        def run_case(
            overall_status: str,
            check_status: str,
            issue_status: str,
            provider: str,
            model: str,
            run_id: str,
        ) -> None:
            write_self_test_summary(
                summary,
                overall_status=overall_status,
                check_status=check_status,
                issue_status=issue_status,
                provider=provider,
                model=model,
            )
            ns = argparse.Namespace(
                summary=str(summary),
                statistics_page=str(page),
                provider_model_specs=specs,
                run_id=run_id,
                run_attempt="1",
                workflow="self-test",
                event_name="self-test",
                commit_sha="abc123",
                timestamp_utc="2026-06-28T00:00:00Z",
                dry_run=False,
            )
            update_statistics_page(ns)

        run_case("ok", "ok", "ok", "legacy-provider", "legacy-model", "1")
        run_case("rejected", "rejected", "skipped", "openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", "2")
        run_case("rejected", "rejected", "skipped", "openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", "2")
        run_case("provider_failed", "provider_failed", "skipped", "openrouter", "poolside/laguna-m.1:free", "3")
        run_case("failed", "ok", "failed", "gemini", "gemini-3.1-flash-lite", "4")

        state = load_state(page)
        legacy = state["models"]["legacy-provider:legacy-model"]
        nemotron = state["models"]["openrouter:nvidia/nemotron-3-ultra-550b-a55b:free"]
        laguna = state["models"]["openrouter:poolside/laguna-m.1:free"]
        gemini = state["models"]["gemini:gemini-3.1-flash-lite"]
        active_keys = active_model_keys(state)
        rendered = page.read_text(encoding="utf-8")
        assert legacy["called"] == 1 and legacy["valid"] == 1 and legacy["invalid"] == 0
        assert model_record_status(legacy, active_keys) == "inactive"
        assert nemotron["called"] == 1 and nemotron["invalid"] == 1 and nemotron["rejected"] == 1
        assert laguna["called"] == 1 and laguna["invalid"] == 1 and laguna["provider_failed"] == 1
        assert gemini["called"] == 1 and gemini["valid"] == 1 and gemini["invalid"] == 0
        assert gemini["last_issue_status"] == "failed"
        assert state["collection_start_utc"] == "2026-06-28T00:00:00Z"
        assert "Statistics collection started on: `2026-06-28T00:00:00Z`" in rendered
        assert "Models not present in the configured, non-retired registry remain listed as `inactive`" in rendered
        assert "| `legacy-provider` | `legacy-model` | `inactive` |" in rendered
        assert "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free" in state["models"]
        assert len(state["active_rotation"]) == 26
        assert sum(spec["provider"] == "sambanova" for spec in state["active_rotation"]) == 6
        assert sum(spec["provider"] == "groq" for spec in state["active_rotation"]) == 3
        assert sum(spec["provider"] == "gemini" for spec in state["active_rotation"]) == 8
        assert sum(spec["provider"] == "openrouter" for spec in state["active_rotation"]) == 9
        assert model_record_status(laguna, active_keys) == "inactive"
    print(
        "Self-test passed: counters increment, duplicate events are ignored, issue-manager failures do not invalidate model output, inactive historical models are retained, collection start is persisted, and OpenRouter colon model IDs are preserved."
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update Phase 2 model run statistics Markdown page.")
    parser.add_argument(
        "--summary", default=str(DEFAULT_SUMMARY_PATH), help="Path to run_check_batch.py summary Markdown."
    )
    parser.add_argument(
        "--statistics-page",
        default=str(DEFAULT_STATISTICS_PAGE),
        help="Markdown documentation page that stores the rendered table and hidden JSON state.",
    )
    parser.add_argument(
        "--provider-model-specs",
        default=DEFAULT_PROVIDER_MODEL_SPECS,
        help="Comma- or newline-separated provider:model specs for the active rotation.",
    )
    parser.add_argument("--run-id", default="local", help="GitHub run id used for de-duplication.")
    parser.add_argument("--run-attempt", default="0", help="GitHub run attempt used for de-duplication.")
    parser.add_argument("--workflow", default="local", help="Workflow name used for de-duplication.")
    parser.add_argument("--event-name", default="local", help="GitHub event name stored in state metadata.")
    parser.add_argument("--commit-sha", default="", help="Commit SHA stored in state metadata.")
    parser.add_argument("--timestamp-utc", default="", help="Optional fixed UTC timestamp for tests.")
    parser.add_argument("--dry-run", action="store_true", help="Print the rendered Markdown instead of writing it.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in smoke tests without provider calls.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    try:
        return update_statistics_page(args)
    except (OSError, ValueError, AssertionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
