#!/usr/bin/env python3
"""Persist best-known Phase 2 quota, cooldown, and runtime slot state."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from provider_model_registry import DEFAULT_REGISTRY_PATH, ProviderModelRegistry, load_registry
from provider_runtime import format_timestamp, parse_timestamp, retry_after_seconds, utc_now
from resolver_attempt_state import aggregate_events as aggregate_resolver_attempt_events
from resolver_attempt_state import load_event_files as load_resolver_attempt_event_files
from resolver_attempt_state import load_state as load_resolver_attempt_state
from resolver_attempt_state import write_state as write_resolver_attempt_state
from task_state import load_task_state, write_task_state

SCHEMA_VERSION = 1
DEFAULT_STATE_PATH = Path("data/phase-2/quota-state.json")
DEFAULT_EVENT_DIRECTORY = Path(".tmp/phase-2/quota-events")
QUOTA_GROUP_STATUSES = {"eligible", "deferred_quota"}
RUNTIME_STATUSES = {
    "eligible",
    "temporarily_unavailable",
    "blocked_provider_policy",
    "blocked_execution_configuration",
}
PROVENANCE_LABELS = {"provider-reported", "locally-counted", "configured", "inferred", "unknown"}
QUOTA_PROVENANCE_FIELDS = {
    "status",
    "requests_limit_minute",
    "requests_remaining_minute",
    "requests_limit_day",
    "requests_used_day_local",
    "tokens_limit_minute",
    "tokens_remaining_minute",
    "input_tokens_used_day_local",
    "output_tokens_used_day_local",
    "total_tokens_used_day_local",
    "remaining_estimate",
    "reset_at",
    "retry_not_before",
}
SHARED_RESOLVER_SPECS = {("gemini", "gemini-3.5-flash"), ("gemini", "gemini-3.6-flash")}


class QuotaStateError(ValueError):
    """Raised when quota state or an observation event is invalid."""


def new_quota_group(group_id: str, *, timestamp: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "scope": "model",
        "provider": group_id.split(":", 1)[0].split("-", 1)[0],
        "status": "eligible",
        "requests_limit_minute": None,
        "requests_remaining_minute": None,
        "requests_limit_day": None,
        "requests_used_day_local": 0,
        "tokens_limit_minute": None,
        "tokens_remaining_minute": None,
        "input_tokens_used_day_local": 0,
        "output_tokens_used_day_local": 0,
        "total_tokens_used_day_local": 0,
        "remaining_estimate": None,
        "reset_at": None,
        "retry_not_before": None,
        "source": "unknown",
        "last_updated_at": timestamp,
    }
    record["provenance"] = {
        field: {
            "source": "locally-counted" if field.endswith("_used_day_local") else "unknown",
            "observed_at": timestamp,
            "estimated": field == "remaining_estimate",
        }
        for field in sorted(QUOTA_PROVENANCE_FIELDS)
    }
    record["provenance"]["status"]["source"] = "configured"
    if group_id in {"sambanova-account", "openrouter-free-account"}:
        record["scope"] = "account"
    elif group_id == "groq-organization":
        record["scope"] = "organization"
    elif group_id == "gemini-project":
        record["scope"] = "project"
    if group_id == "openrouter-free-account":
        record["requests_limit_day"] = 50
        record["remaining_estimate"] = 50
        record["source"] = "configured"
        record["provenance"]["requests_limit_day"]["source"] = "configured"
        record["provenance"]["remaining_estimate"]["source"] = "inferred"
    return record


def new_runtime_record(provider: str, model: str, *, timestamp: str) -> dict[str, Any]:
    return {
        "provider": provider,
        "model": model,
        "status": "eligible",
        "retry_not_before": None,
        "authorized_recheck_task_id": None,
        "block_reason": None,
        "block_scope": None,
        "validation_required": False,
        "last_validation_at": None,
        "last_validation_result": None,
        "last_updated_at": timestamp,
    }


def build_initial_state(
    registry: ProviderModelRegistry,
    *,
    timestamp: str,
    openrouter_request_limit_day: int = 50,
) -> dict[str, Any]:
    quota_group_ids = sorted({group for slot in registry.configured_slots for group in slot.quota_groups})
    runtime_slots = {
        slot.spec: new_runtime_record(slot.provider, slot.model, timestamp=timestamp)
        for slot in registry.configured_slots
    }
    state = {
        "schema_version": SCHEMA_VERSION,
        "configuration_version": registry.configuration_version,
        "counter_period": {"daily_period_start": timestamp[:10], "source": "configured"},
        "quota_groups": {group_id: new_quota_group(group_id, timestamp=timestamp) for group_id in quota_group_ids},
        "runtime_slots": runtime_slots,
        "provider_blocks": {},
        "processed_event_ids": [],
        "last_updated_at": timestamp,
    }
    openrouter_group = state["quota_groups"]["openrouter-free-account"]
    openrouter_group["requests_limit_day"] = openrouter_request_limit_day
    openrouter_group["remaining_estimate"] = openrouter_request_limit_day
    return state


def validate_quota_state(state: Any, registry: ProviderModelRegistry) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise QuotaStateError("Quota state root must be an object.")
    required = {
        "schema_version",
        "configuration_version",
        "counter_period",
        "quota_groups",
        "runtime_slots",
        "provider_blocks",
        "processed_event_ids",
        "last_updated_at",
    }
    missing = sorted(required - state.keys())
    if missing:
        raise QuotaStateError(f"Quota state is missing required field(s): {', '.join(missing)}.")
    if state["schema_version"] != SCHEMA_VERSION:
        raise QuotaStateError(f"Quota state schema_version must be {SCHEMA_VERSION}.")
    if state["configuration_version"] != registry.configuration_version:
        raise QuotaStateError("Quota state configuration_version does not match the provider-model registry.")
    if not isinstance(state["processed_event_ids"], list) or len(state["processed_event_ids"]) != len(
        set(state["processed_event_ids"])
    ):
        raise QuotaStateError("Quota state processed_event_ids must be a duplicate-free list.")
    expected_groups = {group for slot in registry.configured_slots for group in slot.quota_groups}
    if set(state["quota_groups"]) != expected_groups:
        raise QuotaStateError("Quota state quota groups do not exactly match the configured registry groups.")
    expected_specs = {slot.spec for slot in registry.configured_slots}
    if set(state["runtime_slots"]) != expected_specs:
        raise QuotaStateError("Quota state runtime slots do not exactly match configured provider-model slots.")
    for group_id, group in state["quota_groups"].items():
        if not isinstance(group, dict) or group.get("status") not in QUOTA_GROUP_STATUSES:
            raise QuotaStateError(f"Quota group {group_id} has invalid state.")
        if group.get("source") not in PROVENANCE_LABELS:
            raise QuotaStateError(f"Quota group {group_id} has invalid provenance label {group.get('source')!r}.")
        provenance = group.get("provenance")
        if not isinstance(provenance, dict) or set(provenance) != QUOTA_PROVENANCE_FIELDS:
            raise QuotaStateError(f"Quota group {group_id} does not provide field-specific provenance.")
        for field, field_provenance in provenance.items():
            if not isinstance(field_provenance, dict) or field_provenance.get("source") not in PROVENANCE_LABELS:
                raise QuotaStateError(f"Quota group {group_id} field {field} has invalid provenance.")
            if not isinstance(field_provenance.get("estimated"), bool):
                raise QuotaStateError(f"Quota group {group_id} field {field} lacks an estimate label.")
    for spec, runtime in state["runtime_slots"].items():
        if not isinstance(runtime, dict) or runtime.get("status") not in RUNTIME_STATUSES:
            raise QuotaStateError(f"Runtime slot {spec} has invalid state.")
    if not isinstance(state["provider_blocks"], dict):
        raise QuotaStateError("Quota state provider_blocks must be an object.")
    return state


def write_state(path: Path, state: Mapping[str, Any], registry: ProviderModelRegistry) -> None:
    validate_quota_state(dict(state), registry)
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


def load_state(path: Path, registry: ProviderModelRegistry) -> dict[str, Any]:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise QuotaStateError(f"Quota state does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QuotaStateError(f"Quota state is not valid JSON: {exc}") from exc
    return validate_quota_state(state, registry)


def reset_daily_counters_if_due(state: dict[str, Any], *, timestamp: str) -> None:
    current_period = timestamp[:10]
    if state["counter_period"]["daily_period_start"] == current_period:
        return
    for group in state["quota_groups"].values():
        group["requests_used_day_local"] = 0
        group["input_tokens_used_day_local"] = 0
        group["output_tokens_used_day_local"] = 0
        group["total_tokens_used_day_local"] = 0
        for field in (
            "requests_used_day_local",
            "input_tokens_used_day_local",
            "output_tokens_used_day_local",
            "total_tokens_used_day_local",
        ):
            _set_provenance(group, field, source="locally-counted", timestamp=timestamp)
        if group["source"] == "locally-counted" and group["status"] == "deferred_quota":
            group["status"] = "eligible"
            group["retry_not_before"] = None
            _set_provenance(group, "status", source="inferred", timestamp=timestamp)
            _set_provenance(group, "retry_not_before", source="inferred", timestamp=timestamp)
        if group["requests_limit_day"] is not None:
            group["remaining_estimate"] = group["requests_limit_day"]
            _set_provenance(group, "remaining_estimate", source="inferred", timestamp=timestamp)
    state["counter_period"]["daily_period_start"] = current_period


def _int_header(headers: Mapping[str, str], key: str) -> int | None:
    value = headers.get(key)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _set_provenance(group: dict[str, Any], field: str, *, source: str, timestamp: str) -> None:
    group["provenance"][field] = {
        "source": source,
        "observed_at": timestamp,
        "estimated": field == "remaining_estimate",
    }


def _reset_delay_seconds(headers: Mapping[str, str], header_names: Iterable[str], *, timestamp: str) -> int | None:
    now = parse_timestamp(timestamp)
    candidates: list[int] = []
    retry_after = headers.get("retry-after")
    if retry_after:
        parsed = retry_after_seconds({"retry-after": retry_after}, "", now=now)
        if parsed is not None:
            candidates.append(parsed)
    for header_name in header_names:
        value = headers.get(header_name)
        if not value:
            continue
        parsed = retry_after_seconds({"retry-after": value}, "", now=now)
        if parsed is not None:
            candidates.append(parsed)
    return max(candidates) if candidates else None


def _apply_provider_headers(group: dict[str, Any], headers: Mapping[str, str], *, timestamp: str) -> None:
    field_map = {
        "x-ratelimit-limit-tokens": "tokens_limit_minute",
        "x-ratelimit-remaining-tokens": "tokens_remaining_minute",
        "x-ratelimit-limit-requests-minute": "requests_limit_minute",
        "x-ratelimit-remaining-requests-minute": "requests_remaining_minute",
        "x-ratelimit-limit-requests-day": "requests_limit_day",
    }
    if group["provider"] == "groq":
        field_map["x-ratelimit-limit-requests"] = "requests_limit_day"
    else:
        field_map["x-ratelimit-limit-requests"] = "requests_limit_minute"
        field_map["x-ratelimit-remaining-requests"] = "requests_remaining_minute"
    changed = False
    for header, field in field_map.items():
        parsed = _int_header(headers, header)
        if parsed is not None:
            group[field] = parsed
            _set_provenance(group, field, source="provider-reported", timestamp=timestamp)
            changed = True
    remaining_day = _int_header(headers, "x-ratelimit-remaining-requests-day")
    if group["provider"] == "groq":
        remaining_day = _int_header(headers, "x-ratelimit-remaining-requests")
    if remaining_day is not None and group["requests_limit_day"] is not None:
        group["remaining_estimate"] = remaining_day
        _set_provenance(group, "remaining_estimate", source="provider-reported", timestamp=timestamp)
        changed = True
    if changed:
        requests_exhausted = group["requests_remaining_minute"] == 0
        tokens_exhausted = group["tokens_remaining_minute"] == 0
        daily_requests_exhausted = group["remaining_estimate"] == 0
        exhausted = requests_exhausted or tokens_exhausted or daily_requests_exhausted
        reset_headers: list[str] = ["x-ratelimit-reset"]
        if requests_exhausted or daily_requests_exhausted:
            reset_headers.append("x-ratelimit-reset-requests")
        if tokens_exhausted:
            reset_headers.append("x-ratelimit-reset-tokens")
        reset_seconds = _reset_delay_seconds(headers, reset_headers, timestamp=timestamp)
        if reset_seconds is not None:
            group["reset_at"] = format_timestamp(parse_timestamp(timestamp) + timedelta(seconds=reset_seconds))
            _set_provenance(group, "reset_at", source="provider-reported", timestamp=timestamp)
        if exhausted:
            group["status"] = "deferred_quota"
            if reset_seconds is not None:
                retry_not_before = group["reset_at"]
                retry_source = "provider-reported"
            elif daily_requests_exhausted:
                next_period = parse_timestamp(timestamp).replace(hour=0, minute=0, second=0) + timedelta(days=1)
                retry_not_before = format_timestamp(next_period)
                retry_source = "inferred"
            else:
                retry_not_before = format_timestamp(parse_timestamp(timestamp) + timedelta(minutes=1))
                retry_source = "inferred"
            group["retry_not_before"] = retry_not_before
            _set_provenance(group, "status", source="provider-reported", timestamp=timestamp)
            _set_provenance(
                group,
                "retry_not_before",
                source=retry_source,
                timestamp=timestamp,
            )
        group["source"] = "provider-reported"
        group["last_updated_at"] = timestamp


def _active_group_ids(state: Mapping[str, Any], provider: str, model: str) -> list[str]:
    prefix = f"{provider}:{model}"
    model_group = prefix if prefix in state["quota_groups"] else None
    provider_shared = {
        "sambanova": "sambanova-account",
        "groq": "groq-organization",
        "gemini": "gemini-project",
        "openrouter": "openrouter-free-account",
    }.get(provider)
    return [group for group in (provider_shared, model_group) if group is not None]


def _increment_local_usage(group: dict[str, Any], event: Mapping[str, Any], *, timestamp: str) -> None:
    if event.get("request_sent"):
        group["requests_used_day_local"] += 1
        _set_provenance(group, "requests_used_day_local", source="locally-counted", timestamp=timestamp)
    usage = event.get("usage") if isinstance(event.get("usage"), dict) else {}
    for usage_field, state_field in (
        ("input_tokens", "input_tokens_used_day_local"),
        ("output_tokens", "output_tokens_used_day_local"),
        ("total_tokens", "total_tokens_used_day_local"),
    ):
        value = usage.get(usage_field)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            group[state_field] += value
            _set_provenance(group, state_field, source="locally-counted", timestamp=timestamp)
    if group["requests_limit_day"] is not None and event.get("request_sent"):
        current_remaining = group["remaining_estimate"]
        if isinstance(current_remaining, int) and not isinstance(current_remaining, bool):
            group["remaining_estimate"] = max(0, current_remaining - 1)
        else:
            group["remaining_estimate"] = max(
                0,
                group["requests_limit_day"] - group["requests_used_day_local"],
            )
        _set_provenance(group, "remaining_estimate", source="inferred", timestamp=timestamp)
        if group["remaining_estimate"] == 0:
            group["status"] = "deferred_quota"
            next_period = parse_timestamp(timestamp).replace(hour=0, minute=0, second=0) + timedelta(days=1)
            group["retry_not_before"] = format_timestamp(next_period)
            _set_provenance(group, "status", source="inferred", timestamp=timestamp)
            _set_provenance(group, "retry_not_before", source="inferred", timestamp=timestamp)
    if group["source"] != "provider-reported":
        group["source"] = "locally-counted"
    group["last_updated_at"] = timestamp


def _apply_failure(state: dict[str, Any], event: Mapping[str, Any], *, timestamp: str) -> None:
    failure = event.get("failure")
    if not isinstance(failure, dict):
        return
    provider = str(event["provider"])
    model = str(event["model"])
    spec = f"{provider}:{model}"
    kind = failure.get("kind")
    scope = failure.get("scope")
    if kind == "rate_or_quota_limited":
        for group_id in failure.get("quota_group_ids") or []:
            group = state["quota_groups"].get(group_id)
            if group is None:
                continue
            retry_not_before = failure.get("retry_not_before")
            existing_retry = group.get("retry_not_before")
            preserved_existing_retry = False
            if existing_retry and (
                retry_not_before is None
                or parse_timestamp(str(existing_retry)) > parse_timestamp(str(retry_not_before))
            ):
                retry_not_before = existing_retry
                preserved_existing_retry = True
            group["status"] = "deferred_quota"
            group["retry_not_before"] = retry_not_before
            group["source"] = "provider-reported"
            group["last_updated_at"] = timestamp
            _set_provenance(group, "status", source="provider-reported", timestamp=timestamp)
            if not preserved_existing_retry:
                _set_provenance(
                    group,
                    "retry_not_before",
                    source=str(failure.get("retry_source") or "inferred"),
                    timestamp=timestamp,
                )
    elif kind == "provider_unavailable":
        runtime = state["runtime_slots"][spec]
        runtime["status"] = "temporarily_unavailable"
        runtime["retry_not_before"] = failure.get("retry_not_before")
        runtime["authorized_recheck_task_id"] = None
        runtime["block_reason"] = kind
        runtime["block_scope"] = "slot"
        runtime["last_updated_at"] = timestamp
    elif kind == "provider_policy_block":
        affected_specs = [spec]
        if scope == "provider":
            affected_specs = [
                slot_spec for slot_spec, slot in state["runtime_slots"].items() if slot["provider"] == provider
            ]
        for affected_spec in affected_specs:
            runtime = state["runtime_slots"][affected_spec]
            runtime["status"] = "blocked_provider_policy"
            runtime["block_reason"] = kind
            runtime["block_scope"] = scope
            runtime["validation_required"] = True
            runtime["last_updated_at"] = timestamp
    elif kind == "execution_configuration_block":
        affected_specs = [spec]
        if scope == "provider":
            affected_specs = [
                slot_spec for slot_spec, slot in state["runtime_slots"].items() if slot["provider"] == provider
            ]
            state["provider_blocks"][provider] = {
                "kind": kind,
                "validation_required": True,
                "last_updated_at": timestamp,
            }
        for affected_spec in affected_specs:
            runtime = state["runtime_slots"][affected_spec]
            runtime["status"] = "blocked_execution_configuration"
            runtime["block_reason"] = kind
            runtime["block_scope"] = scope
            runtime["validation_required"] = True
            runtime["last_updated_at"] = timestamp


def _apply_success_availability(state: dict[str, Any], event: Mapping[str, Any], *, timestamp: str) -> None:
    if event.get("outcome") != "success":
        return
    spec = f"{event['provider']}:{event['model']}"
    runtime = state["runtime_slots"][spec]
    if runtime["status"] != "temporarily_unavailable":
        return
    runtime["status"] = "eligible"
    runtime["retry_not_before"] = None
    runtime["authorized_recheck_task_id"] = None
    runtime["block_reason"] = None
    runtime["block_scope"] = None
    runtime["last_updated_at"] = timestamp


def validate_event(event: Any, registry: ProviderModelRegistry) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise QuotaStateError("Quota event must be an object.")
    required = {
        "schema_version",
        "event_id",
        "observed_at",
        "call_source",
        "provider",
        "model",
        "task_id",
        "outcome",
        "request_sent",
        "headers",
        "usage",
        "failure",
    }
    missing = sorted(required - event.keys())
    if missing:
        raise QuotaStateError(f"Quota event is missing required field(s): {', '.join(missing)}.")
    if event["schema_version"] != 1 or event["outcome"] not in {"success", "failure"}:
        raise QuotaStateError("Quota event schema_version or outcome is invalid.")
    if event["call_source"] not in {"signal", "resolver-primary", "resolver-fallback"}:
        raise QuotaStateError(f"Quota event has unsupported call_source: {event['call_source']!r}.")
    if registry.find(str(event["provider"]), str(event["model"])) is None:
        raise QuotaStateError(f"Quota event references an unconfigured slot: {event['provider']}:{event['model']}.")
    return event


def apply_failure_events_to_task_state(
    task_state: dict[str, Any],
    events: Iterable[Mapping[str, Any]],
    *,
    ignored_event_ids: set[str],
) -> int:
    changed_task_ids: set[str] = set()
    tasks = task_state["tasks"]
    latest_task_events: dict[str, Mapping[str, Any]] = {}
    for event in sorted(events, key=lambda item: (str(item.get("observed_at")), str(item.get("event_id")))):
        event_task_id = event.get("task_id")
        if isinstance(event_task_id, str) and event_task_id in tasks:
            latest_task_events[event_task_id] = event
    for event_task_id, event in latest_task_events.items():
        if event.get("event_id") in ignored_event_ids or event.get("outcome") != "failure":
            continue
        failure = event.get("failure")
        if not isinstance(failure, dict):
            continue
        kind = failure.get("kind")
        target_status = {
            "rate_or_quota_limited": "deferred_quota",
            "provider_unavailable": "temporarily_unavailable",
            "provider_policy_block": "blocked_provider_policy",
            "execution_configuration_block": "blocked_execution_configuration",
        }.get(kind)
        if target_status is None:
            continue

        task = tasks[event_task_id]
        if task["status"] in {"completed", "obsolete", "retired"}:
            continue
        task["status"] = target_status
        task["retry_not_before"] = failure.get("retry_not_before")
        task["last_outcome"] = {
            "kind": kind,
            "event_id": event["event_id"],
            "observed_at": event["observed_at"],
        }
        task["updated_at"] = event["observed_at"]
        changed_task_ids.add(event_task_id)
    return len(changed_task_ids)


def aggregate_events(
    state: Mapping[str, Any],
    events: Iterable[Mapping[str, Any]],
    registry: ProviderModelRegistry,
) -> tuple[dict[str, Any], dict[str, int]]:
    updated = deepcopy(dict(state))
    processed = set(updated["processed_event_ids"])
    counts = {"added": 0, "ignored": 0}
    for raw_event in sorted(events, key=lambda item: (str(item.get("observed_at")), str(item.get("event_id")))):
        event = validate_event(dict(raw_event), registry)
        if event["event_id"] in processed:
            counts["ignored"] += 1
            continue
        timestamp = str(event["observed_at"])
        reset_daily_counters_if_due(updated, timestamp=timestamp)
        provider = str(event["provider"])
        model = str(event["model"])
        headers = event["headers"] if isinstance(event["headers"], dict) else {}
        for group_id in _active_group_ids(updated, provider, model):
            group = updated["quota_groups"][group_id]
            _increment_local_usage(group, event, timestamp=timestamp)
            if provider in {"sambanova", "groq"} and group_id == f"{provider}:{model}":
                _apply_provider_headers(group, headers, timestamp=timestamp)
        _apply_failure(updated, event, timestamp=timestamp)
        _apply_success_availability(updated, event, timestamp=timestamp)
        processed.add(event["event_id"])
        updated["last_updated_at"] = timestamp
        counts["added"] += 1
    updated["processed_event_ids"] = sorted(processed)
    validate_quota_state(updated, registry)
    return updated, counts


def _cooldown_active(retry_not_before: str | None, now: datetime) -> bool:
    return bool(retry_not_before and now < parse_timestamp(retry_not_before))


def authorize_slot_recheck(
    state: dict[str, Any],
    *,
    provider: str,
    model: str,
    task_id: str,
    now: datetime,
) -> bool:
    runtime = state["runtime_slots"][f"{provider}:{model}"]
    if runtime["status"] != "temporarily_unavailable" or _cooldown_active(runtime["retry_not_before"], now):
        return False
    current = runtime["authorized_recheck_task_id"]
    if current not in {None, task_id}:
        return False
    runtime["authorized_recheck_task_id"] = task_id
    runtime["last_updated_at"] = format_timestamp(now)
    return True


def complete_slot_recheck(
    state: dict[str, Any],
    *,
    provider: str,
    model: str,
    task_id: str,
    endpoint_available: bool,
    now: datetime,
    cooldown_seconds: int = 3600,
) -> None:
    runtime = state["runtime_slots"][f"{provider}:{model}"]
    if runtime["status"] != "temporarily_unavailable" or runtime["authorized_recheck_task_id"] != task_id:
        raise QuotaStateError("Slot recheck result does not match the sole authorized recheck task.")
    runtime["authorized_recheck_task_id"] = None
    if endpoint_available:
        runtime["status"] = "eligible"
        runtime["retry_not_before"] = None
        runtime["block_reason"] = None
        runtime["block_scope"] = None
    else:
        runtime["retry_not_before"] = format_timestamp(now + timedelta(seconds=cooldown_seconds))
    runtime["last_updated_at"] = format_timestamp(now)


def unblock_tasks_after_audited_validation(
    task_state: dict[str, Any],
    *,
    provider: str,
    model: str | None,
    blocked_status: str,
    timestamp: str,
) -> int:
    if blocked_status not in {"blocked_provider_policy", "blocked_execution_configuration"}:
        raise QuotaStateError(f"Unsupported audited unblock task status: {blocked_status}.")
    changed = 0
    for task in task_state.get("tasks", {}).values():
        identity = task.get("identity", {})
        if identity.get("provider") != provider or (model is not None and identity.get("model") != model):
            continue
        if task.get("status") != blocked_status:
            continue
        task["status"] = "pending"
        task["retry_not_before"] = None
        task["updated_at"] = timestamp
        changed += 1
    return changed


def slot_eligibility(
    state: Mapping[str, Any],
    *,
    provider: str,
    model: str,
    task_id: str | None,
    resolver_capacity_required: bool,
    now: datetime,
) -> tuple[bool, str]:
    spec = f"{provider}:{model}"
    runtime = state["runtime_slots"][spec]
    provider_block = state["provider_blocks"].get(provider)
    if provider_block and provider_block.get("validation_required"):
        return False, "provider-blocked-pending-audited-validation"
    if runtime["status"] in {"blocked_provider_policy", "blocked_execution_configuration"}:
        return False, runtime["status"]
    if runtime["status"] == "temporarily_unavailable":
        if _cooldown_active(runtime["retry_not_before"], now):
            return False, "slot-cooldown"
        if not task_id or runtime["authorized_recheck_task_id"] != task_id:
            return False, "slot-recheck-required"
    for group_id in _active_group_ids(state, provider, model):
        group = state["quota_groups"][group_id]
        if group["status"] == "deferred_quota" and _cooldown_active(group["retry_not_before"], now):
            return False, f"quota-group-deferred:{group_id}"
    if resolver_capacity_required and (provider, model) in SHARED_RESOLVER_SPECS:
        return False, "reserved-for-eligible-resolver-work"
    return True, "eligible-recheck" if runtime["status"] == "temporarily_unavailable" else "eligible"


def record_audited_validation(
    state: dict[str, Any],
    *,
    provider: str,
    model: str | None,
    kind: str,
    successful: bool,
    timestamp: str,
) -> None:
    if kind not in {"free_policy", "execution_configuration"}:
        raise QuotaStateError(f"Unsupported validation kind: {kind}.")
    matching = [
        runtime
        for runtime in state["runtime_slots"].values()
        if runtime["provider"] == provider and (model is None or runtime["model"] == model)
    ]
    if not matching:
        raise QuotaStateError(f"No configured runtime slot matches {provider}:{model or '*'}.")
    for runtime in matching:
        target_status = "blocked_provider_policy" if kind == "free_policy" else "blocked_execution_configuration"
        if runtime["status"] != target_status:
            continue
        runtime["last_validation_at"] = timestamp
        runtime["last_validation_result"] = "passed" if successful else "failed"
        if successful:
            runtime["status"] = "eligible"
            runtime["block_reason"] = None
            runtime["block_scope"] = None
            runtime["validation_required"] = False
        runtime["last_updated_at"] = timestamp
    if kind == "execution_configuration" and successful and model is None:
        state["provider_blocks"].pop(provider, None)
    state["last_updated_at"] = timestamp


def load_event_files(event_directory: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not event_directory.exists():
        return events
    for path in sorted(event_directory.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise QuotaStateError(f"Quota event is not valid JSON: {path}: {exc}") from exc
        events.append(value)
    return events


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate, aggregate, or inspect Phase 2 quota state.")
    parser.add_argument("command", choices=("initialize", "validate", "aggregate", "eligibility", "authorize-recheck"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH))
    parser.add_argument("--task-state", default="data/phase-2/task-state.json")
    parser.add_argument("--events", default=str(DEFAULT_EVENT_DIRECTORY))
    parser.add_argument("--resolver-attempt-state")
    parser.add_argument("--resolver-attempt-events")
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--task-id")
    parser.add_argument("--resolver-capacity-required", action="store_true")
    parser.add_argument("--timestamp")
    parser.add_argument("--openrouter-request-limit-day", type=int, default=50)
    return parser.parse_args(argv)


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    registry_path = _resolve(repo_root, args.registry)
    state_path = _resolve(repo_root, args.state)
    event_directory = _resolve(repo_root, args.events)
    try:
        registry = load_registry(registry_path)
        if args.command == "initialize":
            if args.openrouter_request_limit_day < 1:
                raise QuotaStateError("--openrouter-request-limit-day must be greater than 0.")
            timestamp = args.timestamp or format_timestamp(utc_now())
            state = build_initial_state(
                registry,
                timestamp=timestamp,
                openrouter_request_limit_day=args.openrouter_request_limit_day,
            )
            write_state(state_path, state, registry)
            print(
                f"Initialized Phase 2 quota state: quota_groups={len(state['quota_groups'])}; "
                f"runtime_slots={len(state['runtime_slots'])}; "
                f"openrouter_request_limit_day={args.openrouter_request_limit_day}."
            )
            return 0
        state = load_state(state_path, registry)
        if args.command == "validate":
            print(
                f"Valid Phase 2 quota state: quota_groups={len(state['quota_groups'])}; "
                f"runtime_slots={len(state['runtime_slots'])}; processed_events={len(state['processed_event_ids'])}."
            )
            return 0
        if args.command == "aggregate":
            if bool(args.resolver_attempt_state) != bool(args.resolver_attempt_events):
                raise QuotaStateError(
                    "Resolver-attempt aggregation requires both --resolver-attempt-state and --resolver-attempt-events."
                )
            events = load_event_files(event_directory)
            previously_processed = set(state["processed_event_ids"])
            updated, counts = aggregate_events(state, events, registry)
            task_state_path = _resolve(repo_root, args.task_state)
            persistent_tasks = load_task_state(task_state_path)
            changed_tasks = apply_failure_events_to_task_state(
                persistent_tasks,
                events,
                ignored_event_ids=previously_processed,
            )
            resolver_counts = {"added": 0, "ignored": 0}
            resolver_state_path: Path | None = None
            updated_resolver_state: dict[str, Any] | None = None
            if args.resolver_attempt_state and args.resolver_attempt_events:
                resolver_state_path = _resolve(repo_root, args.resolver_attempt_state)
                resolver_state = load_resolver_attempt_state(resolver_state_path)
                updated_resolver_state, resolver_counts = aggregate_resolver_attempt_events(
                    resolver_state,
                    load_resolver_attempt_event_files(_resolve(repo_root, args.resolver_attempt_events)),
                )
            write_state(state_path, updated, registry)
            write_task_state(task_state_path, persistent_tasks)
            if resolver_state_path is not None and updated_resolver_state is not None:
                write_resolver_attempt_state(resolver_state_path, updated_resolver_state)
            print(
                f"Aggregated Phase 2 quota events: added={counts['added']}; ignored={counts['ignored']}; "
                f"changed_tasks={changed_tasks}; resolver_attempts_added={resolver_counts['added']}; "
                f"resolver_attempts_ignored={resolver_counts['ignored']}."
            )
            return 0
        if not args.provider or not args.model:
            raise QuotaStateError(f"{args.command} requires --provider and --model.")
        now = parse_timestamp(args.timestamp) if args.timestamp else utc_now()
        if args.command == "authorize-recheck":
            if not args.task_id:
                raise QuotaStateError("authorize-recheck requires --task-id.")
            authorized = authorize_slot_recheck(
                state,
                provider=args.provider,
                model=args.model,
                task_id=args.task_id,
                now=now,
            )
            if authorized:
                write_state(state_path, state, registry)
            print("authorized" if authorized else "not-authorized")
            return 0 if authorized else 1
        eligible, reason = slot_eligibility(
            state,
            provider=args.provider,
            model=args.model,
            task_id=args.task_id,
            resolver_capacity_required=args.resolver_capacity_required,
            now=now,
        )
        print(f"eligible={str(eligible).lower()}; reason={reason}")
        return 0 if eligible else 1
    except (OSError, QuotaStateError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
