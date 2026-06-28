#!/usr/bin/env python3
"""Maintain cumulative provider/model statistics for Phase 2 check-agent runs.

The statistics are intentionally derived from Python runner status data, not
from natural-language model output. The default persistence target is a
dedicated GitHub issue body so scheduled runs can update durable state without
committing to ``main`` on every 20-minute rotation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

DEFAULT_ISSUE_TITLE = "Phase 2 check-agent model run statistics"
STATE_SCHEMA_VERSION = 1
STATE_MARKER_START = "<!-- phase-2-check-agent-model-run-statistics:v1"
STATE_MARKER_END = "-->"
MAX_PROCESSED_RUN_KEYS = 500
RUN_KEY_DIGEST_HEX_CHARS = 20

CHECK_STATUS_OK = "ok"
CHECK_STATUS_REJECTED = "rejected"
CHECK_STATUS_PROVIDER_FAILED = "provider_failed"
CHECK_STATUS_FAILED = "failed"


class StatisticsError(RuntimeError):
    """Raised when model-run statistics cannot be updated safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repository in owner/name form.")
    parser.add_argument(
        "--summary-json",
        required=True,
        help="Structured JSON summary produced by scripts/phase-2/run_check_batch.py.",
    )
    parser.add_argument(
        "--provider-model-spec",
        action="append",
        default=[],
        help="Active provider:model spec. May be repeated.",
    )
    parser.add_argument(
        "--provider-model-specs-file",
        help="File containing one active provider:model spec per line.",
    )
    parser.add_argument(
        "--issue-title",
        default=DEFAULT_ISSUE_TITLE,
        help=f"Dedicated statistics issue title. Default: {DEFAULT_ISSUE_TITLE!r}.",
    )
    parser.add_argument("--workflow-run-id", default=os.getenv("GITHUB_RUN_ID"), help="GitHub workflow run ID.")
    parser.add_argument(
        "--workflow-run-attempt",
        default=os.getenv("GITHUB_RUN_ATTEMPT"),
        help="GitHub workflow run attempt number.",
    )
    parser.add_argument("--now", help="UTC timestamp override for tests, in ISO-8601 form.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the issue body that would be written instead of calling GitHub.",
    )
    return parser.parse_args()


def utc_now_iso(override: str | None = None) -> str:
    if override:
        return override
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def markdown_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def strip_inline_code(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("`") and stripped.endswith("`") and len(stripped) >= 2:
        return stripped[1:-1].strip()
    return stripped


def parse_provider_model_spec(spec: str) -> tuple[str, str]:
    normalized = spec.strip()
    if not normalized or normalized.startswith("#"):
        raise StatisticsError("Provider/model spec is empty or commented out.")
    if ":" not in normalized:
        raise StatisticsError(f"Invalid provider:model spec: {spec!r}")
    provider, model = normalized.split(":", 1)
    provider = provider.strip()
    model = model.strip()
    if not provider or not model:
        raise StatisticsError(f"Invalid provider:model spec: {spec!r}")
    return provider, model


def provider_model_key(provider: str, model: str) -> str:
    return f"{provider}:{model}"


def read_active_specs(args: argparse.Namespace) -> list[tuple[str, str]]:
    raw_specs: list[str] = list(args.provider_model_spec or [])
    if args.provider_model_specs_file:
        path = Path(args.provider_model_specs_file)
        if not path.is_file():
            raise StatisticsError(f"Provider/model specs file does not exist: {path}")
        raw_specs.extend(path.read_text(encoding="utf-8").splitlines())

    parsed: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw_spec in raw_specs:
        stripped = raw_spec.strip()
        if not stripped or stripped.startswith("#"):
            continue
        provider, model = parse_provider_model_spec(stripped)
        key = provider_model_key(provider, model)
        if key not in seen:
            parsed.append((provider, model))
            seen.add(key)

    if not parsed:
        raise StatisticsError("No active provider:model specs were supplied.")
    return parsed


def load_summary_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise StatisticsError(f"Structured batch summary does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StatisticsError(f"Structured batch summary is malformed JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise StatisticsError("Structured batch summary root must be a JSON object.")
    if payload.get("schema_version") != 1:
        raise StatisticsError(f"Unsupported structured batch summary schema: {payload.get('schema_version')!r}")
    return payload


def default_model_record(provider: str, model: str) -> dict[str, Any]:
    return {
        "provider": provider,
        "model": model,
        "called": 0,
        "valid": 0,
        "invalid": 0,
        "rejected": 0,
        "provider_failed": 0,
        "failed": 0,
        "last_status": "",
        "last_category": "",
        "last_run_utc": "",
        "last_workflow_run": "",
        "last_completion_cap": "",
    }


def coerce_nonnegative_int(value: Any) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, number)


def normalize_model_record(key: str, raw_record: Any) -> dict[str, Any]:
    key_provider, key_model = parse_provider_model_spec(key)
    if isinstance(raw_record, dict):
        provider = str(raw_record.get("provider") or key_provider)
        model = str(raw_record.get("model") or key_model)
    else:
        provider = key_provider
        model = key_model
        raw_record = {}

    record = default_model_record(provider, model)
    for counter in ("called", "valid", "invalid", "rejected", "provider_failed", "failed"):
        record[counter] = coerce_nonnegative_int(raw_record.get(counter))
    for field in ("last_status", "last_category", "last_run_utc", "last_workflow_run", "last_completion_cap"):
        value = raw_record.get(field)
        record[field] = "" if value is None else str(value)
    return record


def empty_state() -> dict[str, Any]:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "updated_at_utc": "",
        "models": {},
        "processed_run_keys": [],
    }


def normalize_state(raw_state: Any) -> dict[str, Any]:
    if not isinstance(raw_state, dict) or raw_state.get("schema_version") != STATE_SCHEMA_VERSION:
        return empty_state()

    state = empty_state()
    state["updated_at_utc"] = str(raw_state.get("updated_at_utc") or "")

    raw_models = raw_state.get("models")
    if isinstance(raw_models, dict):
        for key, raw_record in raw_models.items():
            try:
                provider, model = parse_provider_model_spec(str(key))
            except StatisticsError:
                continue
            normalized_key = provider_model_key(provider, model)
            state["models"][normalized_key] = normalize_model_record(normalized_key, raw_record)

    raw_keys = raw_state.get("processed_run_keys")
    if isinstance(raw_keys, list):
        state["processed_run_keys"] = [normalize_processed_run_key(key) for key in raw_keys[-MAX_PROCESSED_RUN_KEYS:]]
    return state


def extract_state_from_body(body: str) -> dict[str, Any]:
    pattern = re.compile(
        re.escape(STATE_MARKER_START) + r"\s*(?P<json>\{.*?\})\s*" + re.escape(STATE_MARKER_END),
        flags=re.DOTALL,
    )
    match = pattern.search(body or "")
    if not match:
        return empty_state()
    try:
        raw_state = json.loads(match.group("json"))
    except json.JSONDecodeError:
        return empty_state()
    return normalize_state(raw_state)


def active_key_order(active_specs: Sequence[tuple[str, str]]) -> list[str]:
    return [provider_model_key(provider, model) for provider, model in active_specs]


def ensure_active_records(state: dict[str, Any], active_specs: Sequence[tuple[str, str]]) -> None:
    models = state.setdefault("models", {})
    for provider, model in active_specs:
        key = provider_model_key(provider, model)
        if key not in models:
            models[key] = default_model_record(provider, model)
        else:
            models[key]["provider"] = provider
            models[key]["model"] = model


def run_event_digest(event_key: str) -> str:
    """Return a compact stable fingerprint for an idempotency event key."""
    return hashlib.sha256(event_key.encode("utf-8")).hexdigest()[:RUN_KEY_DIGEST_HEX_CHARS]


def normalize_processed_run_key(value: object) -> str:
    """Normalize stored idempotency keys without re-hashing existing digests."""
    text = str(value)
    if re.fullmatch(rf"[0-9a-f]{{{RUN_KEY_DIGEST_HEX_CHARS}}}", text):
        return text
    return run_event_digest(text)


def stable_run_event_key(
    *,
    summary: dict[str, Any],
    completed_run: dict[str, Any],
    fallback_index: int,
    workflow_run_id: str | None,
    workflow_run_attempt: str | None,
) -> str:
    planned = completed_run.get("planned") if isinstance(completed_run, dict) else {}
    planned_index = planned.get("index", fallback_index) if isinstance(planned, dict) else fallback_index
    if workflow_run_id:
        return f"github-run:{workflow_run_id}:attempt:{workflow_run_attempt or 'unknown'}:planned:{planned_index}"
    generated_at = summary.get("generated_at_utc") or "unknown-time"
    provider = planned.get("provider", "unknown-provider") if isinstance(planned, dict) else "unknown-provider"
    model = planned.get("model", "unknown-model") if isinstance(planned, dict) else "unknown-model"
    return f"local-run:{generated_at}:planned:{planned_index}:{provider}:{model}"


def completed_run_outcome(completed_run: dict[str, Any]) -> tuple[str, str, str]:
    """Return ``counter_outcome``, ``last_status``, and ``last_category``.

    ``valid`` means the check-agent output passed ``run_check_agent.py``'s
    deterministic Python validation. Posting failures are not treated as invalid
    model output because they occur after validation.
    """
    check_status = str(completed_run.get("check_status") or "")
    issue_status = str(completed_run.get("issue_status") or "")

    if check_status == CHECK_STATUS_OK:
        if issue_status == CHECK_STATUS_FAILED:
            return "valid", "valid_issue_failed", "issue_manager_failed"
        return "valid", "valid", ""
    if check_status == CHECK_STATUS_REJECTED:
        return "invalid", "validation_rejected", "validation_rejected"
    if check_status == CHECK_STATUS_PROVIDER_FAILED:
        category = str(completed_run.get("provider_failure_kind") or "provider_failed")
        return "invalid", "provider_failed", category
    if check_status == CHECK_STATUS_FAILED:
        return "invalid", "runner_failed", "runner_failed"
    return "invalid", check_status or "unknown", check_status or "unknown"


def apply_completed_runs(
    *,
    state: dict[str, Any],
    summary: dict[str, Any],
    active_specs: Sequence[tuple[str, str]],
    workflow_run_id: str | None,
    workflow_run_attempt: str | None,
    now_utc: str,
) -> int:
    ensure_active_records(state, active_specs)
    processed_run_keys = list(state.get("processed_run_keys") or [])
    processed_set = set(processed_run_keys)
    completed_runs = summary.get("completed_runs") or []
    if not isinstance(completed_runs, list):
        raise StatisticsError("Structured batch summary field completed_runs must be a list.")

    applied = 0
    summary_completion_cap = summary.get("max_completion_tokens")
    last_completion_cap = "" if summary_completion_cap is None else str(summary_completion_cap)
    workflow_ref = (
        f"{workflow_run_id}/{workflow_run_attempt or 'unknown'}"
        if workflow_run_id
        else str(summary.get("generated_at_utc") or "")
    )

    for index, completed_run in enumerate(completed_runs, start=1):
        if not isinstance(completed_run, dict):
            continue
        planned = completed_run.get("planned")
        if not isinstance(planned, dict):
            continue
        provider = str(planned.get("provider") or "").strip()
        model = str(planned.get("model") or "").strip()
        if not provider or not model:
            continue

        event_key = stable_run_event_key(
            summary=summary,
            completed_run=completed_run,
            fallback_index=index,
            workflow_run_id=workflow_run_id,
            workflow_run_attempt=workflow_run_attempt,
        )
        event_digest = run_event_digest(event_key)
        if event_digest in processed_set:
            continue

        key = provider_model_key(provider, model)
        state["models"].setdefault(key, default_model_record(provider, model))
        record = state["models"][key]

        outcome, last_status, last_category = completed_run_outcome(completed_run)
        record["called"] = coerce_nonnegative_int(record.get("called")) + 1
        if outcome == "valid":
            record["valid"] = coerce_nonnegative_int(record.get("valid")) + 1
        else:
            record["invalid"] = coerce_nonnegative_int(record.get("invalid")) + 1

        check_status = str(completed_run.get("check_status") or "")
        if check_status == CHECK_STATUS_REJECTED:
            record["rejected"] = coerce_nonnegative_int(record.get("rejected")) + 1
        elif check_status == CHECK_STATUS_PROVIDER_FAILED:
            record["provider_failed"] = coerce_nonnegative_int(record.get("provider_failed")) + 1
        elif check_status == CHECK_STATUS_FAILED:
            record["failed"] = coerce_nonnegative_int(record.get("failed")) + 1

        record["last_status"] = last_status
        record["last_category"] = last_category
        record["last_run_utc"] = str(summary.get("generated_at_utc") or now_utc)
        record["last_workflow_run"] = workflow_ref
        record["last_completion_cap"] = last_completion_cap

        processed_run_keys.append(event_digest)
        processed_set.add(event_digest)
        applied += 1

    state["processed_run_keys"] = processed_run_keys[-MAX_PROCESSED_RUN_KEYS:]
    state["updated_at_utc"] = now_utc
    return applied


def render_state_block(state: dict[str, Any]) -> str:
    return f"{STATE_MARKER_START}\n" + json.dumps(state, indent=2, sort_keys=True) + f"\n{STATE_MARKER_END}"


def render_statistics_table(state: dict[str, Any], active_specs: Sequence[tuple[str, str]]) -> str:
    rows: list[str] = [
        "| Provider | Model | # called | # valid | # invalid | # rejected | # provider failed | # failed | Last status | Last category | Last run UTC | Completion cap |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|",
    ]
    models = state.get("models") or {}
    for key in active_key_order(active_specs):
        record = normalize_model_record(key, models.get(key, {}))
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_escape(record['provider'])}`",
                    f"`{markdown_escape(record['model'])}`",
                    str(record["called"]),
                    str(record["valid"]),
                    str(record["invalid"]),
                    str(record["rejected"]),
                    str(record["provider_failed"]),
                    str(record["failed"]),
                    f"`{markdown_escape(record['last_status'])}`",
                    f"`{markdown_escape(record['last_category'])}`",
                    f"`{markdown_escape(record['last_run_utc'])}`",
                    f"`{markdown_escape(record['last_completion_cap'])}`",
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def render_issue_body(*, state: dict[str, Any], active_specs: Sequence[tuple[str, str]], applied_updates: int) -> str:
    return (
        "\n\n".join(
            [
                render_state_block(state),
                "# Phase 2 check-agent model run statistics",
                (
                    "This issue body is maintained by `scripts/phase-2/model_run_statistics.py` from "
                    "`scripts/phase-2/run_check_batch.py` structured status data. It does not store raw prompts, "
                    "raw completions, or provider response bodies."
                ),
                f"Last updated UTC: `{markdown_escape(state.get('updated_at_utc'))}`",
                f"Active provider/model specs: `{len(active_specs)}`",
                f"New completed run records applied in the last update: `{applied_updates}`",
                render_statistics_table(state, active_specs),
                "## Interpretation",
                (
                    "`# valid` means `run_check_agent.py` produced output that passed deterministic Python validation. "
                    "`# invalid` means the selected provider/model did not produce a Python-valid check-agent output. "
                    "Use `# rejected`, `# provider failed`, `# failed`, and `Last category` to distinguish validation "
                    "rejections from provider/API failures and runner failures."
                ),
                "## Limitations",
                (
                    "This issue-body store avoids noisy commits to `main`, but simultaneous workflow runs can still "
                    "race on the final issue-body update. Re-running the same workflow run attempt is idempotent through "
                    "the hidden processed-run fingerprint list; separate workflow attempts are counted as separate executions."
                ),
            ]
        )
        + "\n"
    )


def run_gh(args: Sequence[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["gh", *args],
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError as exc:
        raise StatisticsError("GitHub CLI `gh` is required for non-dry-run statistics updates.") from exc


def gh_json_input(args: Sequence[str], payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(payload, handle)
        temp_path = handle.name
    try:
        return run_gh([*args, "--input", temp_path])
    finally:
        Path(temp_path).unlink(missing_ok=True)


def find_statistics_issue(repo: str, title: str) -> int | None:
    result = run_gh(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--search",
            f'in:title "{title}"',
            "--json",
            "number,title",
            "--limit",
            "20",
        ]
    )
    if result.returncode != 0:
        raise StatisticsError(f"Could not search for statistics issue: {result.stderr.strip()}")
    try:
        issues = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise StatisticsError("GitHub CLI returned malformed JSON while searching for the statistics issue.") from exc
    for issue in issues:
        if isinstance(issue, dict) and issue.get("title") == title:
            return int(issue["number"])
    return None


def read_issue_body(repo: str, issue_number: int) -> str:
    result = run_gh(["api", f"repos/{repo}/issues/{issue_number}", "--jq", ".body"])
    if result.returncode != 0:
        raise StatisticsError(f"Could not read statistics issue body: {result.stderr.strip()}")
    return result.stdout


def create_issue(repo: str, title: str, body: str) -> int:
    result = gh_json_input(
        ["api", f"repos/{repo}/issues", "--method", "POST", "--jq", ".number"], {"title": title, "body": body}
    )
    if result.returncode != 0:
        raise StatisticsError(f"Could not create statistics issue: {result.stderr.strip()}")
    try:
        return int(result.stdout.strip())
    except ValueError as exc:
        raise StatisticsError(
            "GitHub CLI did not return a numeric issue number after creating the statistics issue."
        ) from exc


def update_issue_body(repo: str, issue_number: int, body: str) -> None:
    result = gh_json_input(
        ["api", f"repos/{repo}/issues/{issue_number}", "--method", "PATCH", "--silent"],
        {"body": body},
    )
    if result.returncode != 0:
        raise StatisticsError(f"Could not update statistics issue body: {result.stderr.strip()}")


def update_github_issue(*, repo: str, title: str, body: str) -> int:
    issue_number = find_statistics_issue(repo, title)
    if issue_number is None:
        issue_number = create_issue(repo, title, body)
    else:
        update_issue_body(repo, issue_number, body)
    return issue_number


def update_statistics(args: argparse.Namespace) -> tuple[str, int]:
    active_specs = read_active_specs(args)
    summary = load_summary_json(Path(args.summary_json))
    now_utc = utc_now_iso(args.now)

    issue_number = find_statistics_issue(args.repo, args.issue_title) if not args.dry_run else None
    existing_body = read_issue_body(args.repo, issue_number) if issue_number is not None else ""
    state = extract_state_from_body(existing_body)
    applied_updates = apply_completed_runs(
        state=state,
        summary=summary,
        active_specs=active_specs,
        workflow_run_id=args.workflow_run_id,
        workflow_run_attempt=args.workflow_run_attempt,
        now_utc=now_utc,
    )
    body = render_issue_body(state=state, active_specs=active_specs, applied_updates=applied_updates)

    if args.dry_run:
        print(body)
        return body, 0

    issue_number = update_github_issue(repo=args.repo, title=args.issue_title, body=body)
    print(
        f"Updated check-agent model statistics issue #{issue_number} with {applied_updates} new completed run record(s)."
    )
    return body, issue_number


def main() -> int:
    args = parse_args()
    try:
        update_statistics(args)
    except StatisticsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
