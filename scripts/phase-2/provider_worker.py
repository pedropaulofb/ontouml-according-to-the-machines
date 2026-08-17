#!/usr/bin/env python3
"""Execute one leased Phase 2 provider work plan and emit terminal events."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import (  # noqa: E402
    DEFAULT_REGISTRY_PATH,
    ProviderModelRegistry,
    load_registry,
    require_executable_slot,
)
from provider_runtime import format_timestamp, parse_timestamp, utc_now  # noqa: E402
from quota_state import DEFAULT_STATE_PATH as DEFAULT_QUOTA_STATE_PATH  # noqa: E402
from quota_state import load_state as load_quota_state  # noqa: E402
from quota_state import slot_eligibility  # noqa: E402
from task_state import load_task_state  # noqa: E402

EVENT_VERSION = 1
PLAN_VERSION = 1
DEFAULT_TASK_STATE_PATH = Path("data/phase-2/task-state.json")
DEFAULT_RESULT_ROOT = Path(".tmp/phase-2/result-events")
DEFAULT_OUTPUT_ROOT = Path(".tmp/phase-2/worker-output")
TERMINAL_OUTCOMES = {"valid", "validator_rejected", "provider_failure", "not_called"}


class ProviderWorkerError(RuntimeError):
    """Raised when a provider work plan cannot be executed safely."""


class AmbiguousProviderAttemptError(ProviderWorkerError):
    """Raised when the worker cannot prove whether a provider call occurred."""


def load_plan(path: Path) -> dict[str, Any]:
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProviderWorkerError(f"Provider work plan does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ProviderWorkerError(f"Provider work plan is not valid JSON: {exc}") from exc
    required = {
        "plan_version",
        "workflow_run_id",
        "worker_id",
        "provider",
        "lease_commit_sha",
        "created_at",
        "execution_budget_seconds",
        "initial_concurrency",
        "assignments",
    }
    if not isinstance(plan, dict) or required - plan.keys():
        raise ProviderWorkerError("Provider work plan is missing required fields.")
    if plan["plan_version"] != PLAN_VERSION or not isinstance(plan["assignments"], list):
        raise ProviderWorkerError("Provider work plan schema is invalid.")
    if not isinstance(plan["lease_commit_sha"], str) or not plan["lease_commit_sha"].strip():
        raise ProviderWorkerError("Provider work plan has not been stamped with a lease commit SHA.")
    if not isinstance(plan["initial_concurrency"], int) or plan["initial_concurrency"] < 1:
        raise ProviderWorkerError("Provider work plan initial_concurrency must be a positive integer.")
    return plan


def current_commit_sha(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise ProviderWorkerError("Could not determine the checked-out lease commit SHA.")
    return result.stdout.strip()


def validate_assignment(
    *,
    plan: Mapping[str, Any],
    provider: str,
    task_state: Mapping[str, Any],
    quota_state: Mapping[str, Any],
    registry: ProviderModelRegistry,
    checkout_sha: str,
    now: datetime,
) -> None:
    """Refuse all calls unless every assignment matches the persisted lease commit."""
    if plan["provider"] != provider or plan["worker_id"] != provider:
        raise ProviderWorkerError(f"Work plan does not belong to provider worker {provider}.")
    if plan["lease_commit_sha"] != checkout_sha:
        raise ProviderWorkerError(
            f"Stale worker checkout: expected lease commit {plan['lease_commit_sha']}, found {checkout_sha}."
        )
    task_ids: set[str] = set()
    attempt_ids: set[str] = set()
    for assignment in plan["assignments"]:
        if not isinstance(assignment, dict):
            raise ProviderWorkerError("Work-plan assignment must be an object.")
        task_id = assignment.get("task_id")
        attempt_id = assignment.get("attempt_id")
        identity = assignment.get("identity")
        if not isinstance(task_id, str) or not isinstance(attempt_id, str) or not isinstance(identity, dict):
            raise ProviderWorkerError("Work-plan assignment identity is invalid.")
        if task_id in task_ids or attempt_id in attempt_ids:
            raise ProviderWorkerError("Work plan contains duplicate task or attempt IDs.")
        task_ids.add(task_id)
        attempt_ids.add(attempt_id)
        task = task_state["tasks"].get(task_id)
        if not isinstance(task, dict) or task.get("status") != "leased":
            raise ProviderWorkerError(f"Task {task_id} is not currently leased.")
        if task.get("identity") != identity:
            raise ProviderWorkerError(f"Task {task_id} identity does not match persistent state.")
        lease = task.get("lease")
        if not isinstance(lease, dict):
            raise ProviderWorkerError(f"Task {task_id} has no persisted lease.")
        expected = {
            "attempt_id": attempt_id,
            "workflow_run_id": plan["workflow_run_id"],
            "worker_id": provider,
        }
        if any(lease.get(key) != value for key, value in expected.items()):
            raise ProviderWorkerError(f"Task {task_id} lease does not match its work-plan assignment.")
        if parse_timestamp(str(lease.get("expires_at"))) <= now:
            raise ProviderWorkerError(f"Task {task_id} lease has expired.")
        if identity.get("provider") != provider:
            raise ProviderWorkerError(f"Task {task_id} belongs to another provider.")
        slot = require_executable_slot(provider, str(identity.get("model")))
        if registry.find(provider, slot.model) is None:
            raise ProviderWorkerError(f"Task {task_id} references an unconfigured provider-model slot.")
        eligible, reason = slot_eligibility(
            quota_state,
            provider=provider,
            model=slot.model,
            task_id=task_id,
            resolver_work_pending=False,
            now=now,
        )
        if not eligible:
            raise ProviderWorkerError(f"Task {task_id} is not eligible at worker preflight: {reason}.")


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


def result_event_path(result_root: Path, assignment: Mapping[str, Any]) -> Path:
    return result_root / f"{assignment['attempt_id']}.json"


def _base_event(plan: Mapping[str, Any], assignment: Mapping[str, Any]) -> dict[str, Any]:
    identity = assignment["identity"]
    return {
        "event_version": EVENT_VERSION,
        "task_id": assignment["task_id"],
        "attempt_id": assignment["attempt_id"],
        "workflow_run_id": plan["workflow_run_id"],
        "worker_id": plan["worker_id"],
        "provider": identity["provider"],
        "model": identity["model"],
    }


def emit_not_called(
    *,
    plan: Mapping[str, Any],
    assignment: Mapping[str, Any],
    result_root: Path,
    reason: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    timestamp = format_timestamp(now or utc_now())
    event = {
        **_base_event(plan, assignment),
        "attempt_started_at": timestamp,
        "attempt_finished_at": timestamp,
        "outcome": "not_called",
        "signal_count": 0,
        "provider_attempts": 0,
        "usage": {"input_tokens": None, "output_tokens": None, "total_tokens": None},
        "quota_observations": [],
        "output_sha256": None,
        "output_artifact": None,
        "reason": reason,
    }
    _atomic_write_json(result_event_path(result_root, assignment), event)
    return event


def _load_new_quota_observations(
    event_directory: Path, existing_paths: set[Path], task_id: str
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for path in sorted(event_directory.glob("*.json")):
        if path in existing_paths:
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("task_id") == task_id:
            observations.append(value)
    return observations


def _usage_total(observations: Sequence[Mapping[str, Any]]) -> dict[str, int | None]:
    totals: dict[str, int | None] = {"input_tokens": None, "output_tokens": None, "total_tokens": None}
    for field in totals:
        values = [
            observation.get("usage", {}).get(field)
            for observation in observations
            if isinstance(observation.get("usage"), dict)
        ]
        usable = [value for value in values if isinstance(value, int) and not isinstance(value, bool)]
        if usable:
            totals[field] = sum(usable)
    return totals


def _result_outcome(returncode: int, output_path: Path) -> str:
    if returncode == 0 and output_path.exists():
        return "valid"
    invalid_path = output_path.with_suffix(f".invalid{output_path.suffix}") if output_path.suffix else output_path
    if invalid_path.exists():
        return "validator_rejected"
    return "provider_failure"


def _signal_count(output_path: Path) -> int:
    if not output_path.exists():
        return 0
    import re

    match = re.search(r"^\|\s*Signal count\s*\|\s*`?(\d+)`?\s*\|", output_path.read_text(encoding="utf-8"), re.M)
    return int(match.group(1)) if match else 0


def _sha256_file(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def _artifact_reference(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def execute_assignment(
    *,
    plan: Mapping[str, Any],
    assignment: Mapping[str, Any],
    repo_root: Path,
    result_root: Path,
    output_root: Path,
    quota_event_root: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    """Run one assigned task and collapse all raw attempts into one terminal event."""
    started_at = utc_now()
    identity = assignment["identity"]
    output_path = output_root / plan["provider"] / f"{assignment['attempt_id']}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    quota_event_root.mkdir(parents=True, exist_ok=True)
    existing_paths = set(quota_event_root.glob("*.json"))
    command = [
        sys.executable,
        str(repo_root / "scripts/phase-2/run_check_agent.py"),
        "--agent",
        identity["agent"],
        "--page",
        identity["page"],
        "--provider",
        identity["provider"],
        "--model",
        identity["model"],
        "--output",
        str(output_path),
        "--max-completion-tokens",
        str(assignment["max_completion_tokens"]),
    ]
    environment = os.environ.copy()
    environment["PHASE2_TASK_ID"] = assignment["task_id"]
    environment["PHASE2_CALL_SOURCE"] = "signal"
    environment["PHASE2_QUOTA_EVENT_DIR"] = str(quota_event_root)
    runner_started = True
    try:
        completed = runner(
            command,
            cwd=repo_root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        runner_started = False
        completed = subprocess.CompletedProcess(command, 2, "", str(exc))
    observations = _load_new_quota_observations(quota_event_root, existing_paths, assignment["task_id"])
    attempts = sum(observation.get("request_sent") is True for observation in observations)
    request_absence_proven = not runner_started or (
        bool(observations) and all(observation.get("request_sent") is False for observation in observations)
    )
    if attempts == 0 and not request_absence_proven:
        raise AmbiguousProviderAttemptError(
            f"Task {assignment['task_id']} produced no trustworthy provider-request evidence."
        )
    if attempts == 0 and completed.returncode == 0 and output_path.exists():
        raise AmbiguousProviderAttemptError(
            f"Task {assignment['task_id']} produced output that contradicts its zero-call evidence."
        )
    if attempts == 0:
        return emit_not_called(
            plan=plan,
            assignment=assignment,
            result_root=result_root,
            reason="provider runner stopped before sending a request",
            now=started_at,
        )
    outcome = _result_outcome(completed.returncode, output_path)
    artifact = output_path
    if outcome == "validator_rejected":
        artifact = output_path.with_suffix(f".invalid{output_path.suffix}")
    event = {
        **_base_event(plan, assignment),
        "attempt_started_at": format_timestamp(started_at),
        "attempt_finished_at": format_timestamp(utc_now()),
        "outcome": outcome,
        "signal_count": _signal_count(output_path) if outcome == "valid" else 0,
        "provider_attempts": attempts,
        "usage": _usage_total(observations),
        "quota_observations": observations,
        "output_sha256": _sha256_file(artifact),
        "output_artifact": _artifact_reference(artifact, repo_root) if artifact.exists() else None,
        "runner_returncode": completed.returncode,
        "runner_stdout": completed.stdout,
        "runner_stderr": completed.stderr,
    }
    _atomic_write_json(result_event_path(result_root, assignment), event)
    return event


def _reported_zero(headers: Mapping[str, Any]) -> bool:
    for key, value in headers.items():
        normalized = str(key).lower()
        if "ratelimit" in normalized and "remaining" in normalized and str(value).strip() == "0":
            return True
    return False


def _failure_semantics(event: Mapping[str, Any]) -> tuple[set[str], set[str], bool, bool]:
    stopped_groups: set[str] = set()
    unavailable_models: set[str] = set()
    provider_blocked = False
    rate_limited = False
    for observation in event.get("quota_observations") or []:
        if not isinstance(observation, dict):
            continue
        failure = observation.get("failure") if isinstance(observation.get("failure"), dict) else {}
        kind = failure.get("kind")
        scope = failure.get("scope")
        if kind == "rate_or_quota_limited":
            stopped_groups.update(str(group) for group in failure.get("quota_group_ids") or [])
            rate_limited = True
        elif kind == "provider_unavailable":
            unavailable_models.add(str(observation.get("model") or event.get("model")))
            provider_blocked = provider_blocked or scope == "provider"
        elif kind in {"provider_policy_block", "execution_configuration_block"}:
            if scope == "provider":
                provider_blocked = True
            else:
                unavailable_models.add(str(observation.get("model") or event.get("model")))
        if event.get("provider") in {"sambanova", "groq"} and _reported_zero(observation.get("headers") or {}):
            stopped_groups.add(f"{event['provider']}:{event['model']}")
            rate_limited = True
    return stopped_groups, unavailable_models, provider_blocked, rate_limited


def _next_wave(assignments: Sequence[Mapping[str, Any]], concurrency: int) -> list[Mapping[str, Any]]:
    wave: list[Mapping[str, Any]] = []
    models: set[str] = set()
    for assignment in assignments:
        model = str(assignment["identity"]["model"])
        if model in models:
            continue
        wave.append(assignment)
        models.add(model)
        if len(wave) == concurrency:
            break
    return wave


def execute_plan(
    *,
    plan: Mapping[str, Any],
    repo_root: Path,
    result_root: Path,
    output_root: Path,
    quota_event_root: Path,
    execute: Callable[..., dict[str, Any]] = execute_assignment,
    now: Callable[[], datetime] = utc_now,
) -> dict[str, int]:
    pending = list(plan["assignments"])
    counts = {outcome: 0 for outcome in TERMINAL_OUTCOMES}
    concurrency = int(plan["initial_concurrency"])
    deadline = now() + timedelta(seconds=int(plan["execution_budget_seconds"]))
    stopped_groups: set[str] = set()
    unavailable_models: set[str] = set()
    provider_blocked = False
    while pending:
        retained: list[Mapping[str, Any]] = []
        for assignment in pending:
            model = str(assignment["identity"]["model"])
            quota_groups = set(assignment.get("quota_groups") or [])
            reason: str | None = None
            if provider_blocked:
                reason = "provider stopped after a provider-scoped failure"
            elif model in unavailable_models:
                reason = "model stopped after an availability or policy failure"
            elif quota_groups & stopped_groups:
                reason = "required quota group is exhausted"
            elif now() >= deadline:
                reason = "provider execution time budget reached"
            if reason:
                emit_not_called(plan=plan, assignment=assignment, result_root=result_root, reason=reason)
                counts["not_called"] += 1
            else:
                retained.append(assignment)
        pending = retained
        if not pending:
            break
        wave = _next_wave(pending, concurrency)
        pending = [assignment for assignment in pending if assignment not in wave]
        futures: dict[Future[dict[str, Any]], Mapping[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=max(1, min(concurrency, len(wave)))) as executor:
            for assignment in wave:
                futures[
                    executor.submit(
                        execute,
                        plan=plan,
                        assignment=assignment,
                        repo_root=repo_root,
                        result_root=result_root,
                        output_root=output_root,
                        quota_event_root=quota_event_root,
                    )
                ] = assignment
            for future in as_completed(futures):
                assignment = futures[future]
                try:
                    event = future.result()
                except AmbiguousProviderAttemptError:
                    for unstarted in pending:
                        emit_not_called(
                            plan=plan,
                            assignment=unstarted,
                            result_root=result_root,
                            reason="worker stopped before this task started after another attempt became ambiguous",
                        )
                        counts["not_called"] += 1
                    pending.clear()
                    raise
                except Exception as exc:  # noqa: BLE001 - unknown call state must remain ambiguous.
                    for unstarted in pending:
                        emit_not_called(
                            plan=plan,
                            assignment=unstarted,
                            result_root=result_root,
                            reason="worker stopped before this task started after another attempt became ambiguous",
                        )
                        counts["not_called"] += 1
                    pending.clear()
                    raise AmbiguousProviderAttemptError(
                        f"Task {assignment['task_id']} failed without trustworthy terminal call evidence: {exc}"
                    ) from exc
                outcome = str(event.get("outcome"))
                if outcome not in counts:
                    raise ProviderWorkerError(f"Worker produced unsupported terminal outcome: {outcome}.")
                counts[outcome] += 1
                new_groups, new_models, new_provider_block, rate_limited = _failure_semantics(event)
                stopped_groups.update(new_groups)
                unavailable_models.update(new_models)
                provider_blocked = provider_blocked or new_provider_block
                if rate_limited and concurrency > 1:
                    concurrency = max(1, concurrency // 2)
    return counts


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute one leased Phase 2 provider work plan.")
    parser.add_argument("--provider", required=True, choices=("sambanova", "groq", "gemini", "openrouter"))
    parser.add_argument("--plan", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--task-state", default=str(DEFAULT_TASK_STATE_PATH))
    parser.add_argument("--quota-state", default=str(DEFAULT_QUOTA_STATE_PATH))
    parser.add_argument("--result-root", default=str(DEFAULT_RESULT_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--quota-event-root", default=os.getenv("PHASE2_QUOTA_EVENT_DIR", ".tmp/phase-2/quota-events"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    result_root = _resolve(repo_root, args.result_root)
    try:
        plan = load_plan(_resolve(repo_root, args.plan))
        registry = load_registry(_resolve(repo_root, args.registry))
        task_state = load_task_state(_resolve(repo_root, args.task_state))
        quota_state = load_quota_state(_resolve(repo_root, args.quota_state), registry)
        try:
            validate_assignment(
                plan=plan,
                provider=args.provider,
                task_state=task_state,
                quota_state=quota_state,
                registry=registry,
                checkout_sha=current_commit_sha(repo_root),
                now=utc_now(),
            )
        except Exception as exc:
            for assignment in plan.get("assignments", []):
                emit_not_called(
                    plan=plan,
                    assignment=assignment,
                    result_root=result_root,
                    reason=f"worker preflight failed before provider execution: {exc}",
                )
            raise
        counts = execute_plan(
            plan=plan,
            repo_root=repo_root,
            result_root=result_root,
            output_root=_resolve(repo_root, args.output_root),
            quota_event_root=_resolve(repo_root, args.quota_event_root),
        )
        print(f"Phase 2 provider worker {args.provider}: {json.dumps(counts, sort_keys=True)}")
        return 0
    except (OSError, ProviderWorkerError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
