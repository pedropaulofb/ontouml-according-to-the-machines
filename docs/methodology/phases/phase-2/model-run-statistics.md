# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.

The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.

Last generated: `2026-06-29T12:18:18Z`

## Cumulative table

| Provider | Model | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `cerebras` | `gpt-oss-120b` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `cerebras` | `zai-glm-4.7` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `gemini` | `gemini-3.1-flash-lite` | 1 | 0 | 1 | 1 | 0 | 0 | `rejected` | `skipped` | `2026-06-29T12:18:18Z` |
| `groq` | `llama-3.3-70b-versatile` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `poolside/laguna-m.1:free` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `sambanova` | `DeepSeek-V3.1` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |

## Status derivation

- `# called` increments once for each selected provider/model run recorded in `.tmp/phase-2/batch-summary.md` with check status `ok`, `rejected`, `provider_failed`, or `failed`.
- `# valid` increments only for Python-side check status `ok`.
- `# invalid` increments for Python-side check status `rejected`, `provider_failed`, or `failed`.
- `# rejected` counts deterministic check-agent output validation rejections.
- `# provider failed` counts provider-call failures classified by the batch runner.
- `# runner failed` counts other fatal check-agent runner failures reported as `failed`.
- `Last issue status` is recorded separately because issue-manager failures are operational failures, not model-output validation failures.

## Storage strategy and limitations

The human-readable table above is rendered from hidden JSON state stored in this Markdown file. Keeping the state in the same MkDocs page makes the website page the persistence artifact while avoiding a separate GitHub issue or external store.

The workflow is expected to commit this page back to the repository after scheduled runs. That requires `contents: write` workflow permission and repository settings that allow GitHub Actions to write to the target branch.

Concurrency is controlled at the workflow level to reduce overlapping scheduled updates. Push conflicts can still occur if a human or another workflow edits the same page at the same time.

The hidden state stores processed run-event keys for de-duplication. This prevents accidental double-counting when the updater is run again for the same workflow run, but it means the Markdown file grows over time.

This page intentionally does not store secrets, raw prompts, raw completions, provider response bodies, token usage, prompt size, quotas, or request-limit metrics.

<!-- model-run-statistics-state
{
  "active_rotation": [
    {
      "model": "llama-3.3-70b-versatile",
      "provider": "groq",
      "spec": "groq:llama-3.3-70b-versatile"
    },
    {
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "spec": "cerebras:gpt-oss-120b"
    },
    {
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "spec": "sambanova:DeepSeek-V3.1"
    },
    {
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free"
    },
    {
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "spec": "gemini:gemini-3.1-flash-lite"
    },
    {
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "spec": "cerebras:zai-glm-4.7"
    },
    {
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct"
    },
    {
      "model": "poolside/laguna-m.1:free",
      "provider": "openrouter",
      "spec": "openrouter:poolside/laguna-m.1:free"
    }
  ],
  "generated_at": "2026-06-29T12:18:18Z",
  "models": {
    "cerebras:gpt-oss-120b": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "cerebras:gpt-oss-120b",
      "valid": 0
    },
    "cerebras:zai-glm-4.7": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "cerebras:zai-glm-4.7",
      "valid": 0
    },
    "gemini:gemini-3.1-flash-lite": {
      "called": 1,
      "invalid": 1,
      "last_check_status": "rejected",
      "last_event_name": "workflow_dispatch",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "28371412429",
      "last_run_utc": "2026-06-29T12:18:18Z",
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "provider_failed": 0,
      "rejected": 1,
      "runner_failed": 0,
      "spec": "gemini:gemini-3.1-flash-lite",
      "valid": 0
    },
    "groq:llama-3.3-70b-versatile": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "llama-3.3-70b-versatile",
      "provider": "groq",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "groq:llama-3.3-70b-versatile",
      "valid": 0
    },
    "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
      "valid": 0
    },
    "openrouter:poolside/laguna-m.1:free": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "poolside/laguna-m.1:free",
      "provider": "openrouter",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "openrouter:poolside/laguna-m.1:free",
      "valid": 0
    },
    "sambanova:DeepSeek-V3.1": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "valid": 0
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "called": 0,
      "invalid": 0,
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "valid": 0
    }
  },
  "schema_version": 1,
  "seen_events": {
    "28371412429|1|Scheduled check-agent signal collector|1|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "88c1271398b6bf56e4564c27399cba9ad4ec1893",
      "event_name": "workflow_dispatch",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-06-29T12:18:18Z"
    }
  }
}
-->

---

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →
