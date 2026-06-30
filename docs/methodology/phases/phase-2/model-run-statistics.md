# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.

The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.

Statistics collection started on: `2026-06-29T12:18:18Z`

Counts shown on this page only include executions recorded since that start time.

Last generated: `2026-06-30T01:51:31Z`

## Cumulative table

| Provider | Model | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `cerebras` | `gpt-oss-120b` | 1 | 1 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-06-29T19:20:30Z` |
| `cerebras` | `zai-glm-4.7` | 2 | 1 | 1 | 0 | 0 | 1 | `ok` | `ok` | `2026-06-30T01:51:31Z` |
| `gemini` | `gemini-3.1-flash-lite` | 1 | 0 | 1 | 1 | 0 | 0 | `rejected` | `skipped` | `2026-06-29T12:18:18Z` |
| `groq` | `llama-3.3-70b-versatile` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 1 | 0 | 1 | 1 | 0 | 0 | `rejected` | `skipped` | `2026-06-29T17:17:56Z` |
| `openrouter` | `poolside/laguna-m.1:free` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `sambanova` | `DeepSeek-V3.1` | 2 | 2 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-06-29T22:19:25Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | 2 | 2 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-06-29T23:32:49Z` |

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
  "collection_start_utc": "2026-06-29T12:18:18Z",
  "generated_at": "2026-06-30T01:51:31Z",
  "models": {
    "cerebras:gpt-oss-120b": {
      "called": 1,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28396798231",
      "last_run_utc": "2026-06-29T19:20:30Z",
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "cerebras:gpt-oss-120b",
      "valid": 1
    },
    "cerebras:zai-glm-4.7": {
      "called": 2,
      "invalid": 1,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28414833292",
      "last_run_utc": "2026-06-30T01:51:31Z",
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 1,
      "spec": "cerebras:zai-glm-4.7",
      "valid": 1
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
      "called": 1,
      "invalid": 1,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "28389929977",
      "last_run_utc": "2026-06-29T17:17:56Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "provider_failed": 0,
      "rejected": 1,
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
      "called": 2,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28406411549",
      "last_run_utc": "2026-06-29T22:19:25Z",
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "valid": 2
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "called": 2,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28409638610",
      "last_run_utc": "2026-06-29T23:32:49Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "valid": 2
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
    },
    "28378693666|1|Scheduled check-agent signal collector|63|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f57e9126bb058123ba50be97552fffaed172fc2c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-06-29T14:17:14Z"
    },
    "28389929977|1|Scheduled check-agent signal collector|64|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "35e784191c08c1a953476c8f0e430e629ef8b903",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-06-29T17:17:56Z"
    },
    "28396798231|1|Scheduled check-agent signal collector|65|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b92b397198b72db4241799a71b6252e54eee51b5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-06-29T19:20:30Z"
    },
    "28402650374|1|Scheduled check-agent signal collector|65|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "38a99ae5a2ae8a1c1d2e488e8f3f082569a25664",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-06-29T21:06:21Z"
    },
    "28406411549|1|Scheduled check-agent signal collector|66|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dcaa7d76f4816d8d16daab99cd5e3e5460bb76a7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-06-29T22:19:25Z"
    },
    "28409638610|1|Scheduled check-agent signal collector|66|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3acdb521bdea83effe1959a6bbac738acda29cee",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-06-29T23:32:49Z"
    },
    "28414833292|1|Scheduled check-agent signal collector|67|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f7dc7035fea398b3b5612eee0d43ef442121d3e2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-06-30T01:51:31Z"
    },
    "local|0|local|1|cerebras|zai-glm-4.7|failed|failed|failed": {
      "check_status": "failed",
      "commit_sha": "",
      "event_name": "local",
      "issue_status": "failed",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-06-29T20:52:22Z"
    }
  }
}
-->

---

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →
