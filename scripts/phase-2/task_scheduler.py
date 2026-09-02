#!/usr/bin/env python3
"""Build deterministic Phase 2 provider work plans and persist task leases."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import datetime, timedelta
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import (  # noqa: E402
    DEFAULT_REGISTRY_PATH,
    ProviderModelRegistry,
    ProviderModelSlot,
    load_registry,
)
from provider_runtime import format_timestamp, parse_timestamp, utc_now  # noqa: E402
from quota_state import (  # noqa: E402
    DEFAULT_STATE_PATH as DEFAULT_QUOTA_STATE_PATH,
)
from quota_state import (  # noqa: E402
    authorize_slot_recheck,
    reset_daily_counters_if_due,
    slot_eligibility,
)
from quota_state import (  # noqa: E402
    load_state as load_quota_state,
)
from quota_state import (  # noqa: E402
    write_state as write_quota_state,
)
from task_identity import sha256_text  # noqa: E402
from task_reconciler import (  # noqa: E402
    build_desired_task_identities,
    current_commit_sha,
    reconcile_task_state,
    validate_desired_state,
)
from task_state import load_task_state, validate_task_state, write_task_state  # noqa: E402

PLAN_VERSION = 1
TERMINAL_EVENT_VERSION = 1
DEFAULT_TASK_STATE_PATH = Path("data/phase-2/task-state.json")
DEFAULT_WORK_PLAN_ROOT = Path(".tmp/phase-2/work-plans")
DEFAULT_RESULT_EVENT_ROOT = Path(".tmp/phase-2/result-events")
DEFAULT_LEASE_SECONDS = 3600
DEFAULT_EXECUTION_BUDGET_SECONDS = 720
DEFAULT_PROVIDER_CONCURRENCY = {
    "sambanova": 6,
    "groq": 3,
    "gemini": 4,
    "openrouter": 1,
}
SHARED_RESOLVER_SPECS = {
    ("gemini", "gemini-3.5-flash"),
    ("gemini", "gemini-3.6-flash"),
}
SCHEDULABLE_STATUSES = {
    "pending",
    "retry_due",
    "deferred_quota",
    "temporarily_unavailable",
}
TERMINAL_EVENT_OUTCOMES = {
    "valid",
    "validator_rejected",
    "provider_failure",
    "not_called",
}


class SchedulerError(ValueError):
    """Raised when scheduler inputs or persistent state are inconsistent."""


def parse_csv_values(values: Iterable[str] | None) -> set[str]:
    parsed: set[str] = set()
    for value in values or []:
        for item in value.replace("\n", ",").split(","):
            normalized = item.strip()
            if normalized:
                parsed.add(normalized)
    return parsed


def load_terminal_events(root: Path) -> list[dict[str, Any]]:
    """Load terminal events from JSON or JSONL workflow artifacts."""
    events: list[dict[str, Any]] = []
    if not root.exists():
        return events
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        if path.suffix not in {".json", ".jsonl"}:
            continue
        try:
            if path.suffix == ".jsonl":
                values = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            else:
                value = json.loads(path.read_text(encoding="utf-8"))
                values = value if isinstance(value, list) else [value]
        except json.JSONDecodeError as exc:
            raise SchedulerError(f"Terminal event artifact is not valid JSON: {path}: {exc}") from exc
        for value in values:
            if not isinstance(value, dict):
                continue
            if value.get("event_version") != TERMINAL_EVENT_VERSION:
                continue
            if value.get("outcome") not in TERMINAL_EVENT_OUTCOMES:
                continue
            event = dict(value)
            event["_event_path"] = path.relative_to(root).as_posix()
            events.append(event)
    return events


def _event_matches_lease(event: Mapping[str, Any], task_id: str, lease: Mapping[str, Any]) -> bool:
    return (
        event.get("task_id") == task_id
        and event.get("attempt_id") == lease.get("attempt_id")
        and event.get("workflow_run_id") == lease.get("workflow_run_id")
        and event.get("worker_id") == lease.get("worker_id")
    )


def recover_expired_leases(
    task_state: dict[str, Any],
    events: Sequence[Mapping[str, Any]],
    *,
    now: datetime,
) -> dict[str, int]:
    """Recover expired leases only when their terminal evidence is unambiguous."""
    counts = {"released_not_called": 0, "replayable_result": 0, "blocked_ambiguous": 0}
    for task_id, task in task_state["tasks"].items():
        if task["status"] != "leased" or not isinstance(task.get("lease"), dict):
            continue
        lease = task["lease"]
        expires_at = lease.get("expires_at")
        if not isinstance(expires_at, str) or parse_timestamp(expires_at) > now:
            continue
        matches = [event for event in events if _event_matches_lease(event, task_id, lease)]
        timestamp = format_timestamp(now)
        if len(matches) == 1:
            # The scheduler may identify replayable evidence, but only the
            # aggregator validates and durably persists a terminal event. Keep
            # the lease non-schedulable until that deterministic transition.
            task["last_outcome"] = {
                "kind": "replayable_result",
                "attempt_id": lease.get("attempt_id"),
                "outcome": matches[0].get("outcome"),
            }
            task["result_record"]["event_path"] = matches[0].get("_event_path")
            counts["replayable_result"] += 1
        else:
            task["status"] = "blocked_ambiguous_attempt"
            task["lease"] = None
            task["last_outcome"] = {
                "kind": "ambiguous_attempt",
                "attempt_id": lease.get("attempt_id"),
                "matching_terminal_events": len(matches),
            }
            counts["blocked_ambiguous"] += 1
        task["updated_at"] = timestamp
    validate_task_state(task_state)
    return counts


def _retry_ready(task: Mapping[str, Any], now: datetime) -> bool:
    retry_not_before = task.get("retry_not_before")
    return not retry_not_before or parse_timestamp(str(retry_not_before)) <= now


def _matches_filters(
    task: Mapping[str, Any],
    *,
    pages: set[str],
    agents: set[str],
    specs: set[str],
) -> bool:
    identity = task["identity"]
    spec = f"{identity['provider']}:{identity['model']}"
    return (
        (not pages or identity["page"] in pages)
        and (not agents or identity["agent"] in agents)
        and (not specs or spec in specs)
    )


def _task_candidate(task: Mapping[str, Any], now: datetime) -> bool:
    return task.get("status") in SCHEDULABLE_STATUSES and _retry_ready(task, now)


def _candidate_order(task: Mapping[str, Any]) -> tuple[str, str, str]:
    identity = task["identity"]
    return (str(task.get("created_at") or ""), identity["page"], identity["agent"])


def _attempt_id(task_id: str, workflow_run_id: str, attempt_number: int) -> str:
    payload = f"{workflow_run_id}\0{task_id}\0{attempt_number}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _known_request_capacity(group: Mapping[str, Any], *, now: datetime) -> int | None:
    """Return a trustworthy request bound, ignoring stale exhausted cooldown values."""
    retry_not_before = group.get("retry_not_before")
    if group.get("status") == "deferred_quota" and (
        not retry_not_before or parse_timestamp(str(retry_not_before)) <= now
    ):
        return None
    candidates: list[int] = []
    for field in ("remaining_estimate", "requests_remaining_minute"):
        value = group.get(field)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            candidates.append(value)
    return min(candidates) if candidates else None


def _slot_capacity(
    slot: ProviderModelSlot,
    quota_state: Mapping[str, Any],
    remaining_by_group: dict[str, int | None],
    *,
    now: datetime,
) -> int | None:
    values: list[int] = []
    for group_id in slot.quota_groups:
        if group_id not in remaining_by_group:
            value = _known_request_capacity(quota_state["quota_groups"][group_id], now=now)
            if group_id == "openrouter-free-account":
                value = min(50, value) if value is not None else 50
            remaining_by_group[group_id] = value
        if remaining_by_group[group_id] is not None:
            values.append(int(remaining_by_group[group_id]))
    return min(values) if values else None


def _decrement_slot_capacity(slot: ProviderModelSlot, remaining_by_group: dict[str, int | None]) -> None:
    for group_id in slot.quota_groups:
        value = remaining_by_group.get(group_id)
        if value is not None:
            remaining_by_group[group_id] = max(0, value - 1)


def _assignment(task: Mapping[str, Any], slot: ProviderModelSlot) -> dict[str, Any]:
    return {
        "task_id": task["task_id"],
        "identity": copy.deepcopy(task["identity"]),
        "attempt_id": task["lease"]["attempt_id"],
        "attempt_number": task["lease"]["attempt_number"],
        "quota_groups": list(slot.quota_groups),
        "max_completion_tokens": slot.max_completion_tokens,
    }


def build_provider_work_plans(
    *,
    task_state: dict[str, Any],
    quota_state: dict[str, Any],
    registry: ProviderModelRegistry,
    workflow_run_id: str,
    now: datetime,
    lease_seconds: int = DEFAULT_LEASE_SECONDS,
    execution_budget_seconds: int = DEFAULT_EXECUTION_BUDGET_SECONDS,
    max_tasks_per_provider: int = 0,
    resolver_capacity_required: bool = False,
    resolver_reserved_specs: set[str] | None = None,
    pages: set[str] | None = None,
    agents: set[str] | None = None,
    specs: set[str] | None = None,
    lease_tasks: bool = True,
) -> dict[str, dict[str, Any]]:
    """Select fair work and optionally attach durable leases to task state."""
    if lease_seconds < 1 or execution_budget_seconds < 1 or max_tasks_per_provider < 0:
        raise SchedulerError("Lease, budget, and per-provider task limits must be non-negative and usable.")
    pages = pages or set()
    agents = agents or set()
    specs = specs or set()
    resolver_reserved_specs = resolver_reserved_specs or set()
    configured_specs = {slot.spec for slot in registry.configured_slots}
    unknown_specs = specs - configured_specs
    if unknown_specs:
        raise SchedulerError(f"Unknown provider-model filter(s): {', '.join(sorted(unknown_specs))}.")
    unknown_agents = agents - {agent for slot in registry.configured_slots for agent in slot.agents}
    if unknown_agents:
        raise SchedulerError(f"Unknown agent filter(s): {', '.join(sorted(unknown_agents))}.")
    unknown_reserved_specs = resolver_reserved_specs - configured_specs
    if unknown_reserved_specs:
        raise SchedulerError(
            f"Unknown resolver-reserved provider-model spec(s): {', '.join(sorted(unknown_reserved_specs))}."
        )

    timestamp = format_timestamp(now)
    reset_daily_counters_if_due(quota_state, timestamp=timestamp)
    plans: dict[str, dict[str, Any]] = {}
    remaining_by_group: dict[str, int | None] = {}
    for provider, concurrency in DEFAULT_PROVIDER_CONCURRENCY.items():
        plans[provider] = {
            "plan_version": PLAN_VERSION,
            "workflow_run_id": workflow_run_id,
            "worker_id": provider,
            "provider": provider,
            "lease_commit_sha": None,
            "created_at": timestamp,
            "execution_budget_seconds": execution_budget_seconds,
            "initial_concurrency": concurrency,
            "assignments": [],
        }

    slots_by_provider: dict[str, list[ProviderModelSlot]] = {}
    for slot in registry.executable_slots:
        if specs and slot.spec not in specs:
            continue
        slots_by_provider.setdefault(slot.provider, []).append(slot)

    for provider, slots in slots_by_provider.items():
        slot_tasks: dict[str, list[dict[str, Any]]] = {}
        totals: dict[str, int] = {}
        completed: dict[str, int] = {}
        for slot in slots:
            relevant = [
                task
                for task in task_state["tasks"].values()
                if task["identity"]["provider"] == slot.provider
                and task["identity"]["model"] == slot.model
                and _matches_filters(task, pages=pages, agents=agents, specs=specs)
            ]
            totals[slot.spec] = len(relevant)
            completed[slot.spec] = sum(task["status"] == "completed" for task in relevant)
            slot_tasks[slot.spec] = sorted(
                [task for task in relevant if _task_candidate(task, now)],
                key=_candidate_order,
            )

        selected_count = 0
        recheck_selected: set[str] = set()
        while max_tasks_per_provider == 0 or selected_count < max_tasks_per_provider:
            eligible_slots: list[ProviderModelSlot] = []
            for slot in slots:
                candidates = slot_tasks[slot.spec]
                if not candidates:
                    continue
                task = candidates[0]
                runtime_recheck = quota_state["runtime_slots"][slot.spec]["status"] == "temporarily_unavailable"
                if runtime_recheck and slot.spec not in recheck_selected:
                    authorize_slot_recheck(
                        quota_state,
                        provider=slot.provider,
                        model=slot.model,
                        task_id=task["task_id"],
                        now=now,
                    )
                eligible, _reason = slot_eligibility(
                    quota_state,
                    provider=slot.provider,
                    model=slot.model,
                    task_id=task["task_id"],
                    resolver_capacity_required=(
                        resolver_capacity_required
                        and slot.spec in resolver_reserved_specs
                        and (slot.provider, slot.model) in SHARED_RESOLVER_SPECS
                    ),
                    now=now,
                )
                capacity = _slot_capacity(slot, quota_state, remaining_by_group, now=now)
                if eligible and (capacity is None or capacity > 0):
                    eligible_slots.append(slot)
            if not eligible_slots:
                break
            selected_slot = min(
                eligible_slots,
                key=lambda slot: (
                    Fraction(completed[slot.spec], totals[slot.spec]) if totals[slot.spec] else Fraction(1, 1),
                    slot.slot,
                    slot.spec,
                ),
            )
            task = slot_tasks[selected_slot.spec].pop(0)
            if quota_state["runtime_slots"][selected_slot.spec]["status"] == "temporarily_unavailable":
                recheck_selected.add(selected_slot.spec)
                slot_tasks[selected_slot.spec].clear()
            attempt_number = int(task["attempt_count"]) + 1
            lease = {
                "attempt_id": _attempt_id(task["task_id"], workflow_run_id, attempt_number),
                "attempt_number": attempt_number,
                "workflow_run_id": workflow_run_id,
                "worker_id": provider,
                "leased_at": timestamp,
                "expires_at": format_timestamp(now + timedelta(seconds=lease_seconds)),
            }
            if lease_tasks:
                task["status"] = "leased"
                task["lease"] = lease
                task["attempt_count"] = attempt_number
                task["last_attempt_at"] = timestamp
                task["updated_at"] = timestamp
            else:
                task = copy.deepcopy(task)
                task["lease"] = lease
            plans[provider]["assignments"].append(_assignment(task, selected_slot))
            completed[selected_slot.spec] += 1
            selected_count += 1
            _decrement_slot_capacity(selected_slot, remaining_by_group)

    validate_task_state(task_state)
    return plans


def write_work_plans(root: Path, plans: Mapping[str, Mapping[str, Any]]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for provider, plan in plans.items():
        (root / f"{provider}.json").write_text(
            json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def stamp_work_plans(root: Path, lease_commit_sha: str) -> None:
    if not lease_commit_sha.strip():
        raise SchedulerError("--lease-commit-sha must be non-empty.")
    for path in sorted(root.glob("*.json")):
        plan = json.loads(path.read_text(encoding="utf-8"))
        if plan.get("plan_version") != PLAN_VERSION:
            raise SchedulerError(f"Unsupported work-plan version in {path}.")
        plan["lease_commit_sha"] = lease_commit_sha.strip()
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan or lease adaptive Phase 2 provider work.")
    parser.add_argument("command", choices=("plan", "simulate", "lease", "stamp-plans"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--task-state", default=str(DEFAULT_TASK_STATE_PATH))
    parser.add_argument("--quota-state", default=str(DEFAULT_QUOTA_STATE_PATH))
    parser.add_argument("--work-plan-root", default=str(DEFAULT_WORK_PLAN_ROOT))
    parser.add_argument("--result-events", default=str(DEFAULT_RESULT_EVENT_ROOT))
    parser.add_argument("--workflow-run-id")
    parser.add_argument("--lease-commit-sha")
    parser.add_argument("--reconcile", action="store_true")
    parser.add_argument("--timestamp")
    parser.add_argument("--lease-seconds", type=int, default=DEFAULT_LEASE_SECONDS)
    parser.add_argument("--execution-budget-seconds", type=int, default=DEFAULT_EXECUTION_BUDGET_SECONDS)
    parser.add_argument("--max-tasks-per-provider", type=int, default=0)
    parser.add_argument("--resolver-capacity-required", action="store_true")
    parser.add_argument("--resolver-reserved-spec", action="append", default=[])
    parser.add_argument("--page", action="append", default=[])
    parser.add_argument("--agent", action="append", default=[])
    parser.add_argument("--provider-model-spec", action="append", default=[])
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    work_plan_root = _resolve(repo_root, args.work_plan_root)
    try:
        if args.command == "stamp-plans":
            stamp_work_plans(work_plan_root, args.lease_commit_sha or "")
            print(f"Stamped Phase 2 work plans with lease_commit_sha={args.lease_commit_sha}.")
            return 0
        if not args.workflow_run_id:
            raise SchedulerError(f"{args.command} requires --workflow-run-id.")
        registry_path = _resolve(repo_root, args.registry)
        task_state_path = _resolve(repo_root, args.task_state)
        quota_state_path = _resolve(repo_root, args.quota_state)
        registry = load_registry(registry_path)
        persistent_tasks = load_task_state(task_state_path)
        persistent_quota = load_quota_state(quota_state_path, registry)
        now = parse_timestamp(args.timestamp) if args.timestamp else utc_now()
        if args.reconcile:
            commit_sha = current_commit_sha(repo_root)
            if not commit_sha:
                raise SchedulerError("Could not determine the reconciliation source commit SHA.")
            desired = build_desired_task_identities(repo_root=repo_root, registry=registry)
            registry_sha256 = sha256_text(registry_path.read_text(encoding="utf-8"))
            persistent_tasks, counts = reconcile_task_state(
                existing_state=persistent_tasks,
                desired_identities=desired,
                registry_sha256=registry_sha256,
                configured_specs={(slot.provider, slot.model) for slot in registry.configured_slots},
                timestamp=format_timestamp(now),
                source_commit_sha=commit_sha,
            )
            validate_desired_state(persistent_tasks, desired, registry_sha256)
            print(
                f"Reconciled Phase 2 task state: desired_tasks={len(desired)}; added={counts['added']}; "
                f"preserved={counts['preserved']}; obsolete={counts['obsolete']}; retired={counts['retired']}."
            )
        task_state = persistent_tasks if args.command == "lease" else copy.deepcopy(persistent_tasks)
        quota_state = persistent_quota if args.command == "lease" else copy.deepcopy(persistent_quota)
        recovery = recover_expired_leases(
            task_state,
            load_terminal_events(_resolve(repo_root, args.result_events)),
            now=now,
        )
        plans = build_provider_work_plans(
            task_state=task_state,
            quota_state=quota_state,
            registry=registry,
            workflow_run_id=args.workflow_run_id,
            now=now,
            lease_seconds=args.lease_seconds,
            execution_budget_seconds=args.execution_budget_seconds,
            max_tasks_per_provider=args.max_tasks_per_provider,
            resolver_capacity_required=args.resolver_capacity_required,
            resolver_reserved_specs=parse_csv_values(args.resolver_reserved_spec),
            pages=parse_csv_values(args.page),
            agents=parse_csv_values(args.agent),
            specs=parse_csv_values(args.provider_model_spec),
            lease_tasks=args.command == "lease",
        )
        write_work_plans(work_plan_root, plans)
        if args.command == "lease":
            write_task_state(task_state_path, task_state)
            write_quota_state(quota_state_path, quota_state, registry)
        selected = {provider: len(plan["assignments"]) for provider, plan in plans.items()}
        print(
            "Phase 2 scheduler: "
            f"mode={args.command}; selected={json.dumps(selected, sort_keys=True)}; "
            f"recovery={json.dumps(recovery, sort_keys=True)}; "
            f"state_written={str(args.command == 'lease').lower()}."
        )
        return 0
    except (OSError, SchedulerError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
