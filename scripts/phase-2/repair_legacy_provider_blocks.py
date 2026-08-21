#!/usr/bin/env python3
"""Repair the two known Phase 2 provider-policy misclassification incidents."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Sequence

# Provider-wide policy propagation stamped every affected runtime slot with the
# same incident timestamp. Matching provider + timestamp + untouched validation
# metadata repairs exactly those historical records while also covering every
# configured slot that was poisoned by the propagation.
LEGACY_PROVIDER_POLICY_INCIDENTS: dict[str, str] = {
    "gemini": "2026-08-20T09:52:40Z",
    "groq": "2026-08-20T09:52:12Z",
}

# The Groq incident originated from a deterministic request-size/configuration
# failure on this slot. The other Groq slots were poisoned only because the old
# classifier incorrectly promoted the failure to provider scope.
GROQ_CONFIGURATION_BLOCK_SLOT = "groq:openai/gpt-oss-20b"

# The same two misclassified quota observations also changed their originating
# task records. These exact identities and durable event paths allow the repair
# to reclassify only the affected historical tasks without touching later work.
LEGACY_TASK_RECLASSIFICATIONS: dict[str, dict[str, str]] = {
    "088ef7d25755196e92cde50522e43064df9c2084dfad6cd29535269114664b51": {
        "provider": "gemini",
        "model": "gemini-3.5-flash",
        "finished_at": "2026-08-20T09:52:40Z",
        "retry_not_before": "2026-08-20T09:52:59Z",
        "attempt_id": "ecf472d69da4427292f37850e57d56a5d83fa436688fe82d82977baef0bc95cb",
        "event_path": (
            "data/phase-2/results/"
            "088ef7d25755196e92cde50522e43064df9c2084dfad6cd29535269114664b51/"
            "ecf472d69da4427292f37850e57d56a5d83fa436688fe82d82977baef0bc95cb.json"
        ),
        "target_status": "deferred_quota",
        "target_kind": "rate_or_quota_limited",
    },
    "bb847dfdc9f94805fd2f7a42a36718007a2fbb52fd964797a6fd898061512d1d": {
        "provider": "groq",
        "model": "openai/gpt-oss-20b",
        "finished_at": "2026-08-20T09:52:12Z",
        "retry_not_before": "2026-08-20T09:53:12Z",
        "attempt_id": "0839553c2badf33fa4cbd9c8fbcd7466853ec24c6c650c93a52b04b5307d7a78",
        "event_path": (
            "data/phase-2/results/"
            "bb847dfdc9f94805fd2f7a42a36718007a2fbb52fd964797a6fd898061512d1d/"
            "0839553c2badf33fa4cbd9c8fbcd7466853ec24c6c650c93a52b04b5307d7a78.json"
        ),
        "target_status": "blocked_execution_configuration",
        "target_kind": "execution_configuration_block",
    },
}


def _matches_legacy_provider_policy_block(slot_id: str, runtime: dict[str, Any]) -> bool:
    provider = runtime.get("provider")
    expected_timestamp = LEGACY_PROVIDER_POLICY_INCIDENTS.get(str(provider))
    if expected_timestamp is None:
        return False
    expected_provider, expected_model = slot_id.split(":", 1)
    return (
        provider == expected_provider
        and runtime.get("model") == expected_model
        and runtime.get("status") == "blocked_provider_policy"
        and runtime.get("block_reason") == "provider_policy_block"
        and runtime.get("block_scope") == "provider"
        and runtime.get("last_updated_at") == expected_timestamp
        and runtime.get("validation_required") is True
        and runtime.get("last_validation_at") is None
        and runtime.get("last_validation_result") is None
        and runtime.get("authorized_recheck_task_id") is None
        and runtime.get("retry_not_before") is None
    )


def _make_eligible(runtime: dict[str, Any]) -> None:
    runtime["status"] = "eligible"
    runtime["retry_not_before"] = None
    runtime["authorized_recheck_task_id"] = None
    runtime["block_reason"] = None
    runtime["block_scope"] = None
    runtime["validation_required"] = False


def _make_groq_configuration_block(runtime: dict[str, Any]) -> None:
    runtime["status"] = "blocked_execution_configuration"
    runtime["retry_not_before"] = None
    runtime["authorized_recheck_task_id"] = None
    runtime["block_reason"] = "execution_configuration_block"
    runtime["block_scope"] = "slot"
    runtime["validation_required"] = True


def repair_legacy_provider_blocks(state: dict[str, Any]) -> list[str]:
    """Reclassify only runtime records matching the audited legacy incidents."""
    runtime_slots = state.get("runtime_slots")
    if not isinstance(runtime_slots, dict):
        return []

    repaired: list[str] = []
    for slot_id, runtime in runtime_slots.items():
        if not isinstance(slot_id, str) or not isinstance(runtime, dict):
            continue
        if not _matches_legacy_provider_policy_block(slot_id, runtime):
            continue

        if slot_id == GROQ_CONFIGURATION_BLOCK_SLOT:
            _make_groq_configuration_block(runtime)
        else:
            _make_eligible(runtime)
        repaired.append(slot_id)

    return sorted(repaired)


def _matches_legacy_task_block(task_id: str, task: dict[str, Any], expected: dict[str, str]) -> bool:
    identity = task.get("identity")
    last_outcome = task.get("last_outcome")
    result_record = task.get("result_record")
    return (
        task.get("task_id") == task_id
        and task.get("status") == "blocked_provider_policy"
        and task.get("updated_at") == expected["finished_at"]
        and task.get("retry_not_before") == expected["retry_not_before"]
        and task.get("lease") is None
        and isinstance(identity, dict)
        and identity.get("provider") == expected["provider"]
        and identity.get("model") == expected["model"]
        and isinstance(last_outcome, dict)
        and last_outcome.get("attempt_id") == expected["attempt_id"]
        and last_outcome.get("finished_at") == expected["finished_at"]
        and last_outcome.get("kind") == "provider_policy_block"
        and last_outcome.get("provider_attempts") == 1
        and isinstance(result_record, dict)
        and result_record.get("event_path") == expected["event_path"]
    )


def repair_legacy_task_blocks(task_state: dict[str, Any]) -> list[str]:
    """Reclassify only task records produced by the two audited bad events."""
    tasks = task_state.get("tasks")
    if not isinstance(tasks, dict):
        return []

    repaired: list[str] = []
    for task_id, expected in LEGACY_TASK_RECLASSIFICATIONS.items():
        task = tasks.get(task_id)
        if not isinstance(task, dict) or not _matches_legacy_task_block(task_id, task, expected):
            continue
        task["status"] = expected["target_status"]
        task["last_outcome"]["kind"] = expected["target_kind"]
        repaired.append(task_id)
    return sorted(repaired)


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
            json.dump(state, temporary_file, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _read_json(path: Path, description: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read {description}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{description} root must be an object.")
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default="data/phase-2/quota-state.json")
    parser.add_argument("--task-state", default="data/phase-2/task-state.json")
    parser.add_argument("--check", action="store_true", help="Report matches without modifying either state file.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    state_path = Path(args.state)
    task_state_path = Path(args.task_state)
    try:
        state = _read_json(state_path, "Phase 2 quota state")
        task_state = _read_json(task_state_path, "Phase 2 task state")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

    repaired_slots = repair_legacy_provider_blocks(state)
    repaired_tasks = repair_legacy_task_blocks(task_state)
    if args.check:
        print(
            "Legacy provider runtime repair check: "
            f"runtime_matches={len(repaired_slots)}; runtime_slots={','.join(repaired_slots) or 'none'}; "
            f"task_matches={len(repaired_tasks)}; tasks={','.join(repaired_tasks) or 'none'}."
        )
        return 0

    try:
        if repaired_slots:
            write_state(state_path, state)
        if repaired_tasks:
            write_state(task_state_path, task_state)
    except OSError as exc:
        print(f"ERROR: Could not write Phase 2 operational state: {exc}")
        return 2

    print(
        "Legacy provider runtime repair: "
        f"runtime_repaired={len(repaired_slots)}; runtime_slots={','.join(repaired_slots) or 'none'}; "
        f"tasks_repaired={len(repaired_tasks)}; tasks={','.join(repaired_tasks) or 'none'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
