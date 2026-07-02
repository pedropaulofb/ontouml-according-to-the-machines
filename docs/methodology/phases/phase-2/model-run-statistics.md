# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.

The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.

Statistics collection started on: `2026-06-29T12:18:18Z`

Counts shown on this page only include executions recorded since that start time.

Models not present in the current active rotation remain listed as `inactive` for historical continuity.

Last generated: `2026-07-02T18:55:51Z`

## Cumulative table

| Provider | Model | Status | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `cerebras` | `gpt-oss-120b` | `active` | 3 | 3 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-07-02T18:55:51Z` |
| `cerebras` | `zai-glm-4.7` | `active` | 7 | 5 | 2 | 0 | 1 | 1 | `ok` | `ok` | `2026-07-02T15:28:41Z` |
| `gemini` | `gemini-3.1-flash-lite` | `active` | 5 | 1 | 4 | 4 | 0 | 0 | `ok` | `ok` | `2026-07-02T13:04:25Z` |
| `groq` | `llama-3.3-70b-versatile` | `inactive` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | 4 | 0 | 4 | 3 | 1 | 0 | `rejected` | `skipped` | `2026-07-02T17:22:57Z` |
| `openrouter` | `poolside/laguna-m.1:free` | `active` | 3 | 3 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-07-01T23:54:15Z` |
| `sambanova` | `DeepSeek-V3.1` | `active` | 7 | 7 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-07-01T22:25:09Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | 5 | 5 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-07-02T04:17:37Z` |

## Status derivation

- `Status` is derived from the hidden `active_rotation` state: models in that list are `active`; previously recorded models outside it are `inactive`.
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
  "generated_at": "2026-07-02T18:55:51Z",
  "models": {
    "cerebras:gpt-oss-120b": {
      "called": 3,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28614316887",
      "last_run_utc": "2026-07-02T18:55:51Z",
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "cerebras:gpt-oss-120b",
      "valid": 3
    },
    "cerebras:zai-glm-4.7": {
      "called": 7,
      "invalid": 2,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28601826780",
      "last_run_utc": "2026-07-02T15:28:41Z",
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "provider_failed": 1,
      "rejected": 0,
      "runner_failed": 1,
      "spec": "cerebras:zai-glm-4.7",
      "valid": 5
    },
    "gemini:gemini-3.1-flash-lite": {
      "called": 5,
      "invalid": 4,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28592183389",
      "last_run_utc": "2026-07-02T13:04:25Z",
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "provider_failed": 0,
      "rejected": 4,
      "runner_failed": 0,
      "spec": "gemini:gemini-3.1-flash-lite",
      "valid": 1
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
      "called": 4,
      "invalid": 4,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "28608768126",
      "last_run_utc": "2026-07-02T17:22:57Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "provider_failed": 1,
      "rejected": 3,
      "runner_failed": 0,
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
      "valid": 0
    },
    "openrouter:poolside/laguna-m.1:free": {
      "called": 3,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28555492713",
      "last_run_utc": "2026-07-01T23:54:15Z",
      "model": "poolside/laguna-m.1:free",
      "provider": "openrouter",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "openrouter:poolside/laguna-m.1:free",
      "valid": 3
    },
    "sambanova:DeepSeek-V3.1": {
      "called": 7,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28551743118",
      "last_run_utc": "2026-07-01T22:25:09Z",
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "valid": 7
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "called": 5,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28565014269",
      "last_run_utc": "2026-07-02T04:17:37Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "valid": 5
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
    "28424667904|1|Scheduled check-agent signal collector|69|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bd02cedb4febcd6f3ed8e54f004c0b0547dac0b1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-06-30T06:22:46Z"
    },
    "28436466020|1|Scheduled check-agent signal collector|70|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bc21b3dd076b3a8814e57f1c22ab99dfb5314aff",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-06-30T10:06:19Z"
    },
    "28443934133|1|Scheduled check-agent signal collector|71|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "09f70088997e40d383db43a6f835e5562a05fbc4",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-06-30T12:23:15Z"
    },
    "28454634741|1|Scheduled check-agent signal collector|72|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "641b6ce183231ff4dd4a1549f908acb97c377228",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-06-30T15:08:15Z"
    },
    "28463057281|1|Scheduled check-agent signal collector|73|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b11ed1a299eaa868f2ea34f84e2772b80105e5f2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-06-30T17:22:27Z"
    },
    "28469717528|1|Scheduled check-agent signal collector|74|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "be23a3ca7142e8bfc326fa31a9a75e09e79d2927",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-06-30T19:16:02Z"
    },
    "28476233702|1|Scheduled check-agent signal collector|7|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "33554ff437afd8b05aca26ac62be7d6ee809ee23",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-06-30T21:13:32Z"
    },
    "28480869577|1|Scheduled check-agent signal collector|8|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "aec8b8810c56e5f03917946dc39eb6f54b53fae6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-06-30T22:49:08Z"
    },
    "28484528803|1|Scheduled check-agent signal collector|8|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "21291f99963d28203416425a1c2d25125b18b04c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-01T00:18:18Z"
    },
    "28494693116|1|Scheduled check-agent signal collector|10|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "434fb1db512851dd150f8c84556814a17e8de2dc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-01T05:01:19Z"
    },
    "28505624084|1|Scheduled check-agent signal collector|12|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "4c37b079e06df56cd8c035fbb73217871dd11036",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-01T08:54:33Z"
    },
    "28516795255|1|Scheduled check-agent signal collector|13|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "508a694e55569700cc9df0cc11e94d338c89bcfd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-01T12:16:37Z"
    },
    "28528133883|1|Scheduled check-agent signal collector|15|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8e96af8f0e03c8e4d674072bf8f69de10ea4ba56",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-01T15:18:28Z"
    },
    "28535667202|1|Scheduled check-agent signal collector|16|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1c3ece77fca5cc5c3db38df3f0bf5bf266ef714a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-01T17:27:09Z"
    },
    "28541905473|1|Scheduled check-agent signal collector|16|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "52d94b5e1a750b56983d6741c6b6126866613dc7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-01T19:26:23Z"
    },
    "28547495089|1|Scheduled check-agent signal collector|17|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "e967513ae03fb03f21cb7deda70cb38a605cdff7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-01T21:01:25Z"
    },
    "28551743118|1|Scheduled check-agent signal collector|18|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "769e33f865d55bec88c3133687981f7deede8ffd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-01T22:25:09Z"
    },
    "28555492713|1|Scheduled check-agent signal collector|18|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "edb8bc80a8de9303a62ce38753a13e7dcec269a4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-01T23:54:15Z"
    },
    "28565014269|1|Scheduled check-agent signal collector|20|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "406c0cbb849c422022dbf8c661b7d6de57eb7f6d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-02T04:17:37Z"
    },
    "28574197867|1|Scheduled check-agent signal collector|22|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "dc736757c8f7500318e1c45332badccdac9fc680",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-02T07:49:49Z"
    },
    "28584420700|1|Scheduled check-agent signal collector|23|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8fd6d309c9acc2d58b94fc1f8b631bee69b7ea07",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-02T10:50:34Z"
    },
    "28592183389|1|Scheduled check-agent signal collector|24|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "15576ee8a6759088750f69ab05b7971dde83379c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-02T13:04:25Z"
    },
    "28601826780|1|Scheduled check-agent signal collector|25|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "53323f6b45a71f7c9492d9b38f05979a9e5d19ed",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-02T15:28:41Z"
    },
    "28608768126|1|Scheduled check-agent signal collector|26|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "8b3eb26653d91d0360d70292f1629ab67f7a95ea",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-02T17:22:57Z"
    },
    "28614316887|1|Scheduled check-agent signal collector|27|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a53aa84505b1e40d40b50b5be6767c99fe315128",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-02T18:55:51Z"
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
