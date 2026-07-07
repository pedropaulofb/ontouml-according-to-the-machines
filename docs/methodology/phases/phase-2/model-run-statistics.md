# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.

The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.

Statistics collection started on: `2026-06-29T12:18:18Z`

Counts shown on this page only include executions recorded since that start time.

Models not present in the current active rotation remain listed as `inactive` for historical continuity.

Last generated: `2026-07-07T11:17:53Z`

## Cumulative table

| Provider | Model | Status | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `cerebras` | `gpt-oss-120b` | `active` | 12 | 11 | 1 | 1 | 0 | 0 | `rejected` | `skipped` | `2026-07-05T21:43:17Z` |
| `cerebras` | `zai-glm-4.7` | `active` | 14 | 12 | 2 | 0 | 1 | 1 | `ok` | `ok` | `2026-07-06T17:30:01Z` |
| `gemini` | `gemini-3.1-flash-lite` | `active` | 14 | 4 | 10 | 10 | 0 | 0 | `ok` | `ok` | `2026-07-05T22:42:31Z` |
| `groq` | `llama-3.3-70b-versatile` | `inactive` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | 11 | 1 | 10 | 7 | 3 | 0 | `rejected` | `skipped` | `2026-07-06T23:49:24Z` |
| `openrouter` | `poolside/laguna-m.1:free` | `active` | 13 | 9 | 4 | 0 | 4 | 0 | `provider_failed` | `skipped` | `2026-07-06T11:11:12Z` |
| `sambanova` | `DeepSeek-V3.1` | `active` | 13 | 13 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-07-07T11:17:53Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | 12 | 11 | 1 | 1 | 0 | 0 | `ok` | `ok` | `2026-07-07T07:57:45Z` |

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
  "generated_at": "2026-07-07T11:17:53Z",
  "models": {
    "cerebras:gpt-oss-120b": {
      "called": 12,
      "invalid": 1,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "28755858435",
      "last_run_utc": "2026-07-05T21:43:17Z",
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "provider_failed": 0,
      "rejected": 1,
      "runner_failed": 0,
      "spec": "cerebras:gpt-oss-120b",
      "valid": 11
    },
    "cerebras:zai-glm-4.7": {
      "called": 14,
      "invalid": 2,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28810555482",
      "last_run_utc": "2026-07-06T17:30:01Z",
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "provider_failed": 1,
      "rejected": 0,
      "runner_failed": 1,
      "spec": "cerebras:zai-glm-4.7",
      "valid": 12
    },
    "gemini:gemini-3.1-flash-lite": {
      "called": 14,
      "invalid": 10,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28757396872",
      "last_run_utc": "2026-07-05T22:42:31Z",
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "provider_failed": 0,
      "rejected": 10,
      "runner_failed": 0,
      "spec": "gemini:gemini-3.1-flash-lite",
      "valid": 4
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
      "called": 11,
      "invalid": 10,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "28831172684",
      "last_run_utc": "2026-07-06T23:49:24Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "provider_failed": 3,
      "rejected": 7,
      "runner_failed": 0,
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
      "valid": 1
    },
    "openrouter:poolside/laguna-m.1:free": {
      "called": 13,
      "invalid": 4,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "28787280232",
      "last_run_utc": "2026-07-06T11:11:12Z",
      "model": "poolside/laguna-m.1:free",
      "provider": "openrouter",
      "provider_failed": 4,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "openrouter:poolside/laguna-m.1:free",
      "valid": 9
    },
    "sambanova:DeepSeek-V3.1": {
      "called": 13,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28862083972",
      "last_run_utc": "2026-07-07T11:17:53Z",
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "valid": 13
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "called": 12,
      "invalid": 1,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "28850768013",
      "last_run_utc": "2026-07-07T07:57:45Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 1,
      "runner_failed": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "valid": 11
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
    "28619898838|1|Scheduled check-agent signal collector|27|sambanova|Meta-Llama-3.3-70B-Instruct|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e1074020b36f4fa4a81a6bf11a0444dfc7a17edc",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "rejected",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-02T20:36:19Z"
    },
    "28623808664|1|Scheduled check-agent signal collector|28|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fb0a065cb50c29eb1befef8a931e7724342cfaa2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-02T21:52:45Z"
    },
    "28627688743|1|Scheduled check-agent signal collector|28|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "69356d3f50f21dc64876d0b3e871cb39c262f523",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-02T23:20:37Z"
    },
    "28631694202|1|Scheduled check-agent signal collector|29|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3e6fce5ff9d4acdb1e5e68f44d23576a8cc78697",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-03T01:08:33Z"
    },
    "28639809803|1|Scheduled check-agent signal collector|31|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "8c70d9952b780b79875c90672394765b9ab6362f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-03T05:09:48Z"
    },
    "28648603833|1|Scheduled check-agent signal collector|32|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d53a92b50f53ed3974a2aac89bad16772094ff4f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-03T08:33:32Z"
    },
    "28657103939|1|Scheduled check-agent signal collector|34|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8ba52100a7829ed83e34b42d1bb58769153669dc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-03T11:18:30Z"
    },
    "28663173067|1|Scheduled check-agent signal collector|34|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "97f38aecaeafa8cc0b721f1b0c9d1f2e00402e08",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-03T13:21:08Z"
    },
    "28670059574|1|Scheduled check-agent signal collector|35|openrouter|poolside/laguna-m.1:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "a0231255ec98f739df9096ff1601ac68738b981d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-03T15:35:48Z"
    },
    "28674179908|1|Scheduled check-agent signal collector|36|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "7b8818cfaad4bff31a747cff6c00b21c02e2c81a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-03T17:05:25Z"
    },
    "28677865995|1|Scheduled check-agent signal collector|37|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "91f3f1544acfbec0a0c627d4fc8996405a36e751",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-03T18:37:41Z"
    },
    "28681158792|1|Scheduled check-agent signal collector|37|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "17026943f4ac5cb09f6e568b1e1a584cef1d2b83",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-03T20:04:33Z"
    },
    "28683861055|1|Scheduled check-agent signal collector|38|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "1e6efb026d6f36469eb45ad62ef3dbaae3dd06a2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-03T21:23:17Z"
    },
    "28686189094|1|Scheduled check-agent signal collector|38|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a8b04004adad064ed5516d005083ba782ee0e030",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-03T22:35:04Z"
    },
    "28688186150|1|Scheduled check-agent signal collector|39|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "52ada9294f4aa8571ce2e33ed928c0ee922f38f0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-03T23:47:58Z"
    },
    "28690561316|1|Scheduled check-agent signal collector|40|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "43414925cc2d27495c3aab752779aff899c13c59",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T01:20:29Z"
    },
    "28695680968|1|Scheduled check-agent signal collector|41|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6b0516f842ce478d77e767d5f31b6f263e38ae29",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T05:03:41Z"
    },
    "28699916008|1|Scheduled check-agent signal collector|42|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bd6d10f2b622a66bba87f05d5cd71b80a0ec922b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-04T08:02:54Z"
    },
    "28703184763|1|Scheduled check-agent signal collector|43|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f489e571a3ee304169195356276ad300eed73ea9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-04T10:22:20Z"
    },
    "28705270406|1|Scheduled check-agent signal collector|44|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "22765cb20c5a53c5b2300432161cbf8efc87f900",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T11:50:16Z"
    },
    "28708372462|1|Scheduled check-agent signal collector|45|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "6267fabab39d64392b3c73083b8d3df837d8fd89",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-04T13:54:45Z"
    },
    "28710564225|1|Scheduled check-agent signal collector|46|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dcf381c7a08ae9e1453b766922adf6e7d699018d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T15:18:38Z"
    },
    "28712521994|1|Scheduled check-agent signal collector|46|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4cb52d7a8cadf148a664e9866de1822a8bc58dda",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T16:31:09Z"
    },
    "28714519301|1|Scheduled check-agent signal collector|47|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8324455cbee9d4707e36b64b3012d23e7c44d26a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T17:46:57Z"
    },
    "28716069332|1|Scheduled check-agent signal collector|47|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "139827f0ee8a731463854db46992cb516517eb45",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-04T18:45:36Z"
    },
    "28717949245|1|Scheduled check-agent signal collector|48|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6433cc925001c7569748d3f2f19ce848f5fbc247",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T19:59:23Z"
    },
    "28719779551|1|Scheduled check-agent signal collector|48|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a10c875c94a8d1484d58aca4de43209092fa2291",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T21:11:52Z"
    },
    "28721600943|1|Scheduled check-agent signal collector|49|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6b48c13a2aaa855771319682f3c94f922ef5c29b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T22:26:10Z"
    },
    "28723142151|1|Scheduled check-agent signal collector|49|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fc0bfb939025493d6816a18a5eeeeef20a66c18a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-04T23:32:21Z"
    },
    "28725616943|1|Scheduled check-agent signal collector|50|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "1bcbf4be3b1934a66b666743224d70d811634967",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-05T01:27:53Z"
    },
    "28730922650|1|Scheduled check-agent signal collector|52|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0d2c0be317ff59ca923d7e58f26ec2c1edec149d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-05T05:39:28Z"
    },
    "28734864073|1|Scheduled check-agent signal collector|53|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "c39075ba35df3f756899f5c12bac3cd2bc8f0868",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-05T08:32:16Z"
    },
    "28738337446|1|Scheduled check-agent signal collector|54|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "d8e81c205afb79e1a5c963a34582f94d752f6e8c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-05T10:53:30Z"
    },
    "28740635629|1|Scheduled check-agent signal collector|55|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "27f8ded1cd2d40fd5936604706d8ec4a9ae69aa0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-05T12:23:25Z"
    },
    "28743656332|1|Scheduled check-agent signal collector|55|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d723d1609a0f3d95abe8276b51704caf501b7d9a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-05T14:16:50Z"
    },
    "28746123745|1|Scheduled check-agent signal collector|56|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "07da1d62a4dabd7e34c99601489a276515ef893b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-05T15:44:56Z"
    },
    "28747845615|1|Scheduled check-agent signal collector|57|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0b9e677766023f8347d3886ee4c2d21431b2eb5f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-05T16:47:10Z"
    },
    "28749576578|1|Scheduled check-agent signal collector|57|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f3261ebcaf804ae26da218dbbf5e0f3901997050",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-05T17:51:18Z"
    },
    "28752539340|1|Scheduled check-agent signal collector|58|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "420e4cffc2edc035cf0b86bc5b2f8221fc2aa7b1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-05T19:39:57Z"
    },
    "28754233302|1|Scheduled check-agent signal collector|58|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "60c09070f95654821282833ae905f80de265fa66",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-05T20:41:50Z"
    },
    "28755858435|1|Scheduled check-agent signal collector|59|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ed1ad8f5a5d60016d548f98827817010c4fc756d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-05T21:43:17Z"
    },
    "28757396872|1|Scheduled check-agent signal collector|59|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "201f544231ac6529d3e106ce92cf93b565e894c6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-05T22:42:31Z"
    },
    "28759069028|1|Scheduled check-agent signal collector|59|openrouter|poolside/laguna-m.1:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f64bd2a96599b743652e36cf38bfc56f4022a696",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-05T23:49:15Z"
    },
    "28762077592|1|Scheduled check-agent signal collector|60|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "34afb6d3b63f5ddb1b1e49924bcbba74c0545773",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-06T01:28:51Z"
    },
    "28771548225|1|Scheduled check-agent signal collector|62|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5539c1600f0f8259a6f230c1f7b48dbdd54b5854",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-06T06:10:57Z"
    },
    "28787280232|1|Scheduled check-agent signal collector|64|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "d5effcc329584364855fc51ab18bac9e84350923",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-06T11:11:12Z"
    },
    "28799940042|1|Scheduled check-agent signal collector|66|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "9f403e10671d0dc429b858515cfe5add907f5615",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-06T14:42:19Z"
    },
    "28810555482|1|Scheduled check-agent signal collector|67|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b3985fbf11e04fd611fa4f4c14e0ca2eb670923f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-06T17:30:01Z"
    },
    "28817367065|1|Scheduled check-agent signal collector|68|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6a0b63b8a46b17bf993554ea9f5e9e65b26663aa",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-06T19:24:35Z"
    },
    "28823465088|1|Scheduled check-agent signal collector|69|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "73a68f779fbada42b0177e07fa9e0961bdd872cb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-06T21:10:04Z"
    },
    "28828344299|1|Scheduled check-agent signal collector|69|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "45cdd0dd65e7897459f2136d99a506adfa3fc31d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-06T22:44:32Z"
    },
    "28831172684|1|Scheduled check-agent signal collector|70|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "38d85d4bcbe284d44007c37445d83eda2959f693",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-06T23:49:24Z"
    },
    "28840984390|1|Scheduled check-agent signal collector|72|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0d53c10b8d37ebac8f9353a5f5873ce348f9f320",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-07T04:13:18Z"
    },
    "28850768013|1|Scheduled check-agent signal collector|73|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "100c0e739d038c186a16c44888b75a8cabcd645a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-07T07:57:45Z"
    },
    "28862083972|1|Scheduled check-agent signal collector|75|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ed0c639ec997b7e67dacd4e4228ea9a00184c702",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-07T11:17:53Z"
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
