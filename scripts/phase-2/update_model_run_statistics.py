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
from typing import Any, Iterable, Sequence

DEFAULT_STATISTICS_PAGE = Path("docs/methodology/phases/phase-2/model-run-statistics.md")
DEFAULT_SUMMARY_PATH = Path(".tmp/phase-2/batch-summary.md")
STATE_START = "<!-- model-run-statistics-state"
STATE_END = "-->"
STATE_SCHEMA_VERSION = 1
DEFAULT_PROVIDER_MODEL_SPECS = (
    "groq:llama-3.3-70b-versatile,"
    "cerebras:gpt-oss-120b,"
    "sambanova:DeepSeek-V3.1,"
    "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free,"
    "gemini:gemini-3.1-flash-lite,"
    "cerebras:zai-glm-4.7,"
    "sambanova:Meta-Llama-3.3-70B-Instruct,"
    "openrouter:poolside/laguna-m.1:free"
)

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
        if counting_status == VALID_CHECK_STATUS:
            record["valid"] += 1
        else:
            record["invalid"] += 1
            if counting_status == "rejected":
                record["rejected"] += 1
            elif counting_status == "provider_failed":
                record["provider_failed"] += 1
            elif counting_status == "failed":
                record["runner_failed"] += 1
        record["last_run_utc"] = timestamp_utc
        record["last_check_status"] = summary_run.check_status
        record["last_issue_status"] = summary_run.issue_status
        record["last_overall_status"] = summary_run.overall_status
        record["last_event_name"] = event_name
        record["last_run_id"] = run_id
        record["last_run_attempt"] = run_attempt
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


def sorted_model_records(state: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        state.get("models", {}).values(),
        key=lambda record: (str(record.get("provider", "")), str(record.get("model", ""))),
    )


def render_markdown(state: dict[str, Any]) -> str:
    generated_at = state.get("generated_at") or "not generated yet"
    collection_start_utc = ensure_collection_start_utc(state) or "not recorded yet"
    lines: list[str] = [
        "# Phase 2 — Model Run Statistics",
        "",
        "← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →",
        "",
        "This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.",
        "",
        "The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.",
        "",
        f"Statistics collection started on: `{collection_start_utc}`",
        "",
        "Counts shown on this page only include executions recorded since that start time.",
        "",
        f"Last generated: `{generated_at}`",
        "",
        "## Cumulative table",
        "",
        "| Provider | Model | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for record in sorted_model_records(state):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(record.get('provider', ''))}`",
                    f"`{markdown_escape(record.get('model', ''))}`",
                    str(int(record.get("called", 0) or 0)),
                    str(int(record.get("valid", 0) or 0)),
                    str(int(record.get("invalid", 0) or 0)),
                    str(int(record.get("rejected", 0) or 0)),
                    str(int(record.get("provider_failed", 0) or 0)),
                    str(int(record.get("runner_failed", 0) or 0)),
                    f"`{markdown_escape(record.get('last_check_status', ''))}`"
                    if record.get("last_check_status")
                    else "",
                    f"`{markdown_escape(record.get('last_issue_status', ''))}`"
                    if record.get("last_issue_status")
                    else "",
                    f"`{markdown_escape(record.get('last_run_utc', ''))}`" if record.get("last_run_utc") else "",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Status derivation",
            "",
            "- `# called` increments once for each selected provider/model run recorded in `.tmp/phase-2/batch-summary.md` with check status `ok`, `rejected`, `provider_failed`, or `failed`.",
            "- `# valid` increments only for Python-side check status `ok`.",
            "- `# invalid` increments for Python-side check status `rejected`, `provider_failed`, or `failed`.",
            "- `# rejected` counts deterministic check-agent output validation rejections.",
            "- `# provider failed` counts provider-call failures classified by the batch runner.",
            "- `# runner failed` counts other fatal check-agent runner failures reported as `failed`.",
            "- `Last issue status` is recorded separately because issue-manager failures are operational failures, not model-output validation failures.",
            "",
            "## Storage strategy and limitations",
            "",
            "The human-readable table above is rendered from hidden JSON state stored in this Markdown file. Keeping the state in the same MkDocs page makes the website page the persistence artifact while avoiding a separate GitHub issue or external store.",
            "",
            "The workflow is expected to commit this page back to the repository after scheduled runs. That requires `contents: write` workflow permission and repository settings that allow GitHub Actions to write to the target branch.",
            "",
            "Concurrency is controlled at the workflow level to reduce overlapping scheduled updates. Push conflicts can still occur if a human or another workflow edits the same page at the same time.",
            "",
            "The hidden state stores processed run-event keys for de-duplication. This prevents accidental double-counting when the updater is run again for the same workflow run, but it means the Markdown file grows over time.",
            "",
            "This page intentionally does not store secrets, raw prompts, raw completions, provider response bodies, token usage, prompt size, quotas, or request-limit metrics.",
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

        run_case("ok", "ok", "ok", "groq", "llama-3.3-70b-versatile", "1")
        run_case("rejected", "rejected", "skipped", "openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", "2")
        run_case("rejected", "rejected", "skipped", "openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", "2")
        run_case("provider_failed", "provider_failed", "skipped", "openrouter", "poolside/laguna-m.1:free", "3")
        run_case("failed", "ok", "failed", "gemini", "gemini-3.1-flash-lite", "4")

        state = load_state(page)
        groq = state["models"]["groq:llama-3.3-70b-versatile"]
        nemotron = state["models"]["openrouter:nvidia/nemotron-3-ultra-550b-a55b:free"]
        laguna = state["models"]["openrouter:poolside/laguna-m.1:free"]
        gemini = state["models"]["gemini:gemini-3.1-flash-lite"]
        assert groq["called"] == 1 and groq["valid"] == 1 and groq["invalid"] == 0
        assert nemotron["called"] == 1 and nemotron["invalid"] == 1 and nemotron["rejected"] == 1
        assert laguna["called"] == 1 and laguna["invalid"] == 1 and laguna["provider_failed"] == 1
        assert gemini["called"] == 1 and gemini["valid"] == 1 and gemini["invalid"] == 0
        assert gemini["last_issue_status"] == "failed"
        assert state["collection_start_utc"] == "2026-06-28T00:00:00Z"
        assert "Statistics collection started on: `2026-06-28T00:00:00Z`" in page.read_text(encoding="utf-8")
        assert "Counts shown on this page only include executions recorded since that start time." in page.read_text(
            encoding="utf-8"
        )
        assert "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free" in state["models"]
        assert len(state["active_rotation"]) == 8
    print(
        "Self-test passed: counters increment, duplicate events are ignored, issue-manager failures do not invalidate model output, collection start is persisted, and OpenRouter colon model IDs are preserved."
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
