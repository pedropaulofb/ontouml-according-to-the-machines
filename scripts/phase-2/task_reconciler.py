#!/usr/bin/env python3
"""Reconcile the complete desired Phase 2 task universe with persistent state."""

from __future__ import annotations

import argparse
import copy
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from provider_model_registry import DEFAULT_REGISTRY_PATH, ProviderModelRegistry, load_registry  # noqa: E402
from run_check_agent import AGENT_CONTRACTS, load_effective_prompt  # noqa: E402
from task_identity import build_task_identity, sha256_text, task_id_for  # noqa: E402
from task_state import (  # noqa: E402
    TaskStateError,
    load_task_state,
    new_task_record,
    new_task_state,
    validate_task_state,
    write_task_state,
)

DEFAULT_STATE_PATH = Path("data/phase-2/task-state.json")
CANONICAL_PAGE_GLOBS = (
    "docs/stereotypes/classes/*.md",
    "docs/stereotypes/relations/*.md",
)
EXPECTED_PAGE_COUNT = 39
EXPECTED_AGENT_COUNT = 2
EXPECTED_SLOT_COUNT = 25
EXPECTED_TASK_COUNT = EXPECTED_PAGE_COUNT * EXPECTED_AGENT_COUNT * EXPECTED_SLOT_COUNT


class TaskReconciliationError(ValueError):
    """Raised when desired tasks and persistent state cannot be reconciled safely."""


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def discover_canonical_pages(repo_root: Path) -> list[str]:
    pages: set[str] = set()
    for pattern in CANONICAL_PAGE_GLOBS:
        for match in repo_root.glob(pattern):
            if match.is_file() and match.name != "index.md":
                pages.add(match.relative_to(repo_root).as_posix())
    discovered = sorted(pages)
    if len(discovered) != EXPECTED_PAGE_COUNT:
        raise TaskReconciliationError(f"Expected {EXPECTED_PAGE_COUNT} canonical pages, discovered {len(discovered)}.")
    return discovered


def build_desired_task_identities(
    *,
    repo_root: Path,
    registry: ProviderModelRegistry,
) -> dict[str, dict[str, str]]:
    pages = discover_canonical_pages(repo_root)
    agents = sorted(AGENT_CONTRACTS)
    slots = registry.configured_slots
    if len(agents) != EXPECTED_AGENT_COUNT:
        raise TaskReconciliationError(f"Expected {EXPECTED_AGENT_COUNT} active agents, found {len(agents)}.")
    if len(slots) != EXPECTED_SLOT_COUNT:
        raise TaskReconciliationError(
            f"Expected {EXPECTED_SLOT_COUNT} configured provider-model slots, found {len(slots)}."
        )

    page_contents = {page: (repo_root / page).read_text(encoding="utf-8") for page in pages}
    prompt_contents = {
        agent: load_effective_prompt(repo_root=repo_root, contract=AGENT_CONTRACTS[agent]) for agent in agents
    }
    desired: dict[str, dict[str, str]] = {}
    for page in pages:
        for agent in agents:
            contract = AGENT_CONTRACTS[agent]
            for slot in slots:
                identity = build_task_identity(
                    page=page,
                    agent=agent,
                    provider=slot.provider,
                    model=slot.model,
                    page_content=page_contents[page],
                    prompt_id=contract.prompt_id,
                    prompt_content=prompt_contents[agent],
                    slot=slot,
                )
                task_id = task_id_for(identity)
                if task_id in desired:
                    raise TaskReconciliationError(f"Duplicate desired task ID generated: {task_id}.")
                desired[task_id] = identity

    expected = len(pages) * len(agents) * len(slots)
    if expected != EXPECTED_TASK_COUNT or len(desired) != expected:
        raise TaskReconciliationError(
            f"Expected exactly {EXPECTED_TASK_COUNT} desired tasks from {len(pages)} pages x "
            f"{len(agents)} agents x {len(slots)} slots; generated {len(desired)}."
        )
    return desired


def reconcile_task_state(
    *,
    existing_state: Mapping[str, Any] | None,
    desired_identities: Mapping[str, Mapping[str, str]],
    registry_sha256: str,
    configured_specs: set[tuple[str, str]],
    timestamp: str,
    source_commit_sha: str | None,
) -> tuple[dict[str, Any], dict[str, int]]:
    state = (
        copy.deepcopy(validate_task_state(dict(existing_state)))
        if existing_state is not None
        else new_task_state(registry_sha256=registry_sha256, timestamp=timestamp)
    )
    tasks: dict[str, Any] = state["tasks"]
    counts = {"added": 0, "obsolete": 0, "retired": 0, "preserved": 0}

    for task_id, record in list(tasks.items()):
        desired_identity = desired_identities.get(task_id)
        if desired_identity is not None:
            if record["identity"] != dict(desired_identity):
                raise TaskReconciliationError(f"Task ID collision or corrupted identity for {task_id}.")
            counts["preserved"] += 1
            continue

        identity = record["identity"]
        spec = (str(identity.get("provider", "")), str(identity.get("model", "")))
        replacement_status = "obsolete" if spec in configured_specs else "retired"
        if record["status"] != replacement_status:
            record["status"] = replacement_status
            record["updated_at"] = timestamp
            if record["publication"]["status"] in {"pending", "retry_due"}:
                record["publication"]["status"] = "superseded"
            counts[replacement_status] += 1

    for task_id, identity in desired_identities.items():
        if task_id in tasks:
            continue
        tasks[task_id] = new_task_record(
            task_id=task_id,
            identity=identity,
            timestamp=timestamp,
            source_commit_sha=source_commit_sha,
        )
        counts["added"] += 1

    state["registry_sha256"] = registry_sha256
    state["last_reconciled_at"] = timestamp
    state["tasks"] = dict(sorted(tasks.items()))
    validate_task_state(state)
    return state, counts


def current_commit_sha(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def load_existing_state_if_present(path: Path) -> dict[str, Any] | None:
    return load_task_state(path) if path.exists() else None


def validate_desired_state(
    state: Mapping[str, Any],
    desired_identities: Mapping[str, Mapping[str, str]],
    registry_sha256: str,
) -> None:
    validate_task_state(dict(state))
    if state["registry_sha256"] != registry_sha256:
        raise TaskReconciliationError("Task state registry_sha256 does not match the current registry.")
    tasks = state["tasks"]
    missing = sorted(set(desired_identities) - tasks.keys())
    if missing:
        raise TaskReconciliationError(f"Task state is missing {len(missing)} desired task(s).")
    mismatched = [task_id for task_id, identity in desired_identities.items() if tasks[task_id]["identity"] != identity]
    if mismatched:
        raise TaskReconciliationError(f"Task state contains {len(mismatched)} mismatched desired identity record(s).")
    active = [task_id for task_id in desired_identities if tasks[task_id]["status"] not in {"obsolete", "retired"}]
    if len(active) != EXPECTED_TASK_COUNT:
        raise TaskReconciliationError(f"Expected {EXPECTED_TASK_COUNT} active desired tasks, found {len(active)}.")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile or validate persistent Phase 2 task state.")
    parser.add_argument("command", choices=("reconcile", "validate"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH))
    parser.add_argument("--timestamp", help="Deterministic reconciliation timestamp for bootstrap/tests.")
    parser.add_argument("--commit-sha", help="Nonidentity repository commit metadata for newly created tasks.")
    return parser.parse_args(argv)


def resolve_from_root(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    registry_path = resolve_from_root(repo_root, args.registry)
    state_path = resolve_from_root(repo_root, args.state)
    try:
        registry = load_registry(registry_path)
        desired = build_desired_task_identities(repo_root=repo_root, registry=registry)
        registry_sha256 = sha256_text(registry_path.read_text(encoding="utf-8"))
        if args.command == "validate":
            state = load_task_state(state_path)
            validate_desired_state(state, desired, registry_sha256)
            pending = sum(1 for task_id in desired if state["tasks"][task_id]["status"] == "pending")
            print(
                f"Valid Phase 2 task state: desired_tasks={len(desired)}; "
                f"pending_desired_tasks={pending}; total_records={len(state['tasks'])}."
            )
            return 0

        timestamp = args.timestamp or utc_timestamp()
        commit_sha = args.commit_sha if args.commit_sha is not None else current_commit_sha(repo_root)
        existing_state = load_existing_state_if_present(state_path)
        configured_specs = {(slot.provider, slot.model) for slot in registry.configured_slots}
        reconciled, counts = reconcile_task_state(
            existing_state=existing_state,
            desired_identities=desired,
            registry_sha256=registry_sha256,
            configured_specs=configured_specs,
            timestamp=timestamp,
            source_commit_sha=commit_sha or None,
        )
        write_task_state(state_path, reconciled)
        print(
            f"Reconciled Phase 2 task state: desired_tasks={len(desired)}; added={counts['added']}; "
            f"preserved={counts['preserved']}; obsolete={counts['obsolete']}; retired={counts['retired']}."
        )
        return 0
    except (OSError, TaskStateError, TaskReconciliationError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
