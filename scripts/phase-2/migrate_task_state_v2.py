#!/usr/bin/env python3
"""Validate and explicitly migrate Phase 2 task state from schema v1 to v2."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from task_state import (  # noqa: E402
    TaskStateError,
    load_task_state,
    migrate_task_state_v1_to_v2,
    write_task_state,
)

DEFAULT_STATE_PATH = Path("data/phase-2/task-state.json")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH))
    parser.add_argument("--apply", action="store_true", help="Write the migrated schema-v2 state atomically.")
    return parser.parse_args(argv)


def _resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    state_path = _resolve(repo_root, args.state)
    try:
        original = load_task_state(state_path)
        source_schema = int(original["schema_version"])
        migrated, counts = migrate_task_state_v1_to_v2(original, repo_root=repo_root)
        if args.apply:
            write_task_state(state_path, migrated)
        print(
            "Task-state schema migration: "
            f"source_schema={source_schema}; target_schema={migrated['schema_version']}; "
            f"tasks={len(migrated['tasks'])}; derived_from_event={counts['derived_from_event']}; "
            f"already_identified={counts['already_identified']}; empty={counts['empty']}; "
            f"transient_replay={counts['transient_replay']}; already_v2={counts['already_v2']}; "
            f"state_written={'true' if args.apply else 'false'}."
        )
        return 0
    except (OSError, TaskStateError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
