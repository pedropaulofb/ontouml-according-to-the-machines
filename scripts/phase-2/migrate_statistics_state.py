#!/usr/bin/env python3
"""Move Phase 2 statistics state from hidden Markdown JSON to a canonical JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from update_model_run_statistics import (  # noqa: E402
    DEFAULT_STATISTICS_PAGE,
    DEFAULT_STATISTICS_STATE,
    STATE_END,
    STATE_START,
    normalize_state,
    render_markdown,
    write_state,
)


class StatisticsMigrationError(ValueError):
    """Raised when legacy statistics state cannot be migrated safely."""


def _extract_required_legacy_state(page_text: str) -> dict[str, Any]:
    start = page_text.find(STATE_START)
    if start == -1:
        raise StatisticsMigrationError("Statistics page does not contain the legacy embedded state marker.")
    json_start = page_text.find("\n", start)
    if json_start == -1:
        raise StatisticsMigrationError("Legacy statistics state marker has no JSON payload.")
    end = page_text.find(STATE_END, json_start)
    if end == -1:
        raise StatisticsMigrationError("Legacy statistics state marker is not terminated.")
    payload = page_text[json_start:end].strip()
    if not payload:
        raise StatisticsMigrationError("Legacy statistics state payload is empty.")
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise StatisticsMigrationError(f"Legacy statistics state is invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise StatisticsMigrationError("Legacy statistics state must be a JSON object.")
    return normalize_state(value)


def _load_existing_state(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StatisticsMigrationError(f"Existing statistics state is invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise StatisticsMigrationError("Existing statistics state must be a JSON object.")
    return normalize_state(value)


def migrate(
    *,
    statistics_page: Path,
    statistics_state: Path,
    apply: bool,
) -> dict[str, Any]:
    if not statistics_page.is_file():
        raise StatisticsMigrationError(f"Statistics page does not exist: {statistics_page}")
    page_text = statistics_page.read_text(encoding="utf-8")
    has_legacy_state = STATE_START in page_text
    state_exists = statistics_state.is_file()

    if state_exists:
        state = _load_existing_state(statistics_state)
        source = "json"
        if has_legacy_state:
            legacy = _extract_required_legacy_state(page_text)
            if legacy != state:
                raise StatisticsMigrationError(
                    "Existing statistics-state.json disagrees with the legacy state embedded in the Markdown page."
                )
    else:
        state = _extract_required_legacy_state(page_text)
        source = "markdown"

    rendered = render_markdown(state)
    if STATE_START in rendered:
        raise StatisticsMigrationError("Derived Markdown still contains the legacy embedded state marker.")

    state_written = False
    page_rewritten = False
    if apply:
        if not state_exists:
            write_state(statistics_state, state)
            state_written = True
        if page_text != rendered:
            statistics_page.write_text(rendered, encoding="utf-8", newline="\n")
            page_rewritten = True

    return {
        "source": source,
        "schema_version": state.get("schema_version"),
        "models": len(state.get("models", {})),
        "seen_events": len(state.get("seen_events", {})),
        "seen_terminal_events": len(state.get("seen_terminal_events", {})),
        "queue_keys": len(state.get("queue", {})),
        "state_written": state_written,
        "page_rewritten": page_rewritten,
        "already_migrated": state_exists and not has_legacy_state and page_text == rendered,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Move Phase 2 statistics state out of the Markdown page.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--statistics-page", default=str(DEFAULT_STATISTICS_PAGE))
    parser.add_argument("--statistics-state", default=str(DEFAULT_STATISTICS_STATE))
    parser.add_argument("--apply", action="store_true", help="Write the canonical state and derived Markdown page.")
    return parser.parse_args()


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    try:
        result = migrate(
            statistics_page=_resolve(repo_root, args.statistics_page),
            statistics_state=_resolve(repo_root, args.statistics_state),
            apply=args.apply,
        )
    except (OSError, StatisticsMigrationError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    fields = "; ".join(
        [
            f"source={result['source']}",
            f"schema={result['schema_version']}",
            f"models={result['models']}",
            f"seen_events={result['seen_events']}",
            f"seen_terminal_events={result['seen_terminal_events']}",
            f"queue_keys={result['queue_keys']}",
            f"already_migrated={str(result['already_migrated']).lower()}",
            f"state_written={str(result['state_written']).lower()}",
            f"page_rewritten={str(result['page_rewritten']).lower()}",
        ]
    )
    print(f"Statistics-state migration: {fields}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
