# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.

The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.

Statistics collection started on: `2026-06-29T12:18:18Z`

Counts shown on this page only include executions recorded since that start time.

Models not present in the current active rotation remain listed as `inactive` for historical continuity.

Last generated: `2026-08-01T12:11:33Z`

## Cumulative table

| Provider | Model | Status | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `cerebras` | `gpt-oss-120b` | `active` | 56 | 44 | 12 | 11 | 1 | 0 | `ok` | `ok` | `2026-07-31T20:34:51Z` |
| `cerebras` | `zai-glm-4.7` | `active` | 54 | 44 | 10 | 2 | 7 | 1 | `ok` | `ok` | `2026-08-01T09:30:58Z` |
| `gemini` | `gemini-3.1-flash-lite` | `active` | 73 | 28 | 45 | 45 | 0 | 0 | `rejected` | `skipped` | `2026-08-01T04:29:45Z` |
| `groq` | `llama-3.3-70b-versatile` | `inactive` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | 50 | 11 | 39 | 35 | 4 | 0 | `ok` | `ok` | `2026-07-31T18:51:17Z` |
| `openrouter` | `poolside/laguna-m.1:free` | `active` | 57 | 34 | 23 | 8 | 15 | 0 | `provider_failed` | `skipped` | `2026-08-01T01:00:34Z` |
| `sambanova` | `DeepSeek-V3.1` | `active` | 62 | 62 | 0 | 0 | 0 | 0 | `ok` | `ok` | `2026-08-01T11:06:53Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | 64 | 60 | 4 | 4 | 0 | 0 | `rejected` | `skipped` | `2026-08-01T12:11:33Z` |

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
  "generated_at": "2026-08-01T12:11:33Z",
  "models": {
    "cerebras:gpt-oss-120b": {
      "called": 56,
      "invalid": 12,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "30663361400",
      "last_run_utc": "2026-07-31T20:34:51Z",
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "provider_failed": 1,
      "rejected": 11,
      "runner_failed": 0,
      "spec": "cerebras:gpt-oss-120b",
      "valid": 44
    },
    "cerebras:zai-glm-4.7": {
      "called": 54,
      "invalid": 10,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "30693872652",
      "last_run_utc": "2026-08-01T09:30:58Z",
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "provider_failed": 7,
      "rejected": 2,
      "runner_failed": 1,
      "spec": "cerebras:zai-glm-4.7",
      "valid": 44
    },
    "gemini:gemini-3.1-flash-lite": {
      "called": 73,
      "invalid": 45,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "30684029376",
      "last_run_utc": "2026-08-01T04:29:45Z",
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "provider_failed": 0,
      "rejected": 45,
      "runner_failed": 0,
      "spec": "gemini:gemini-3.1-flash-lite",
      "valid": 28
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
      "called": 50,
      "invalid": 39,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "30656764682",
      "last_run_utc": "2026-07-31T18:51:17Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "provider_failed": 4,
      "rejected": 35,
      "runner_failed": 0,
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
      "valid": 11
    },
    "openrouter:poolside/laguna-m.1:free": {
      "called": 57,
      "invalid": 23,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "30676892830",
      "last_run_utc": "2026-08-01T01:00:34Z",
      "model": "poolside/laguna-m.1:free",
      "provider": "openrouter",
      "provider_failed": 15,
      "rejected": 8,
      "runner_failed": 0,
      "spec": "openrouter:poolside/laguna-m.1:free",
      "valid": 34
    },
    "sambanova:DeepSeek-V3.1": {
      "called": 62,
      "invalid": 0,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "30697030245",
      "last_run_utc": "2026-08-01T11:06:53Z",
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "valid": 62
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "called": 64,
      "invalid": 4,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "30699179167",
      "last_run_utc": "2026-08-01T12:11:33Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "provider_failed": 0,
      "rejected": 4,
      "runner_failed": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "valid": 60
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
    "28870094474|1|Scheduled check-agent signal collector|76|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "639702650ad256663e5647c4d8c6e6145d9e9cb8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-07T13:31:34Z"
    },
    "28881101285|1|Scheduled check-agent signal collector|77|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "12abf9e3b8311ee736b3b34c1d0565bb39298999",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-07T16:15:42Z"
    },
    "28889187758|1|Scheduled check-agent signal collector|78|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5895009c0774f0ace30b84c30ae7bd23ceebd5b3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-07T18:27:01Z"
    },
    "28896328115|1|Scheduled check-agent signal collector|1|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9fa0c9df9e4b866596ef6163794b26ca536e204e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-07T20:26:38Z"
    },
    "28901325603|1|Scheduled check-agent signal collector|1|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1dc70bbfc7afa310ea61eb61282c58a866a58530",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-07T21:54:47Z"
    },
    "28905124459|1|Scheduled check-agent signal collector|2|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "95ed699c739985494cf7977360ef674ab9fa519a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-07T23:13:48Z"
    },
    "28909580621|1|Scheduled check-agent signal collector|3|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f0d2d721ebd5ec7b2c67aca8bafd1eed99613054",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-08T00:58:01Z"
    },
    "28917443051|1|Scheduled check-agent signal collector|4|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5fd5490ea97be894526e7b5bd795fdd77167acf0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-08T04:26:32Z"
    },
    "28924162741|1|Scheduled check-agent signal collector|5|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1fdcf10f6f0d2ab850e5f8e872723fba8bee544d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-08T07:04:56Z"
    },
    "28932542412|1|Scheduled check-agent signal collector|6|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6a29f5e859e25d304b2fad90f54db142294201b4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-08T09:33:23Z"
    },
    "28939266379|1|Scheduled check-agent signal collector|7|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e11f47f02f997e8a2e5c3642eaa52b1388ab5a12",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-08T11:31:45Z"
    },
    "28945593895|1|Scheduled check-agent signal collector|8|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "08c3bdae831dd1996ac18a7aa599ed0f82b71364",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-08T13:19:58Z"
    },
    "28955464464|1|Scheduled check-agent signal collector|9|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "03cd9e6f0f0752dd84182a5553592695e5f7f89e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-08T15:43:02Z"
    },
    "28961467941|1|Scheduled check-agent signal collector|10|cerebras|gpt-oss-120b|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c7024aa51c2074fe6cc92bfca6759c5229618589",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-08T17:11:58Z"
    },
    "28967743345|1|Scheduled check-agent signal collector|10|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9431638b2f68c9becc1db1adfac00c354d2ef338",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-08T18:53:51Z"
    },
    "28973868110|1|Scheduled check-agent signal collector|11|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9a6250072d5fc81c3428ce254d1147b456387ed5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-08T20:36:04Z"
    },
    "28978138816|1|Scheduled check-agent signal collector|12|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0638d78994eef0ad17962a8ab4abee1b4a4ffa71",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-08T21:49:38Z"
    },
    "28982475718|1|Scheduled check-agent signal collector|12|cerebras|zai-glm-4.7|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "8a5ad608fe0589c4c50c51c700a1b04aa4427924",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-08T23:20:37Z"
    },
    "28986852735|1|Scheduled check-agent signal collector|13|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "545e9fd4005d4abcc075822a42896d4e84ce3eca",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-09T01:08:46Z"
    },
    "28996420874|1|Scheduled check-agent signal collector|15|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "35cb1a7f046fca065479b36f690c24eee10fcbe6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-09T05:36:54Z"
    },
    "29006343389|1|Scheduled check-agent signal collector|16|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b08096e0dc1d5024c3240d8dfebe35f4730d1637",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-09T08:55:09Z"
    },
    "29017453966|1|Scheduled check-agent signal collector|18|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "84e70e4193efff6c5ef5404de6358e9d0665ffdc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-09T12:14:28Z"
    },
    "29030445175|1|Scheduled check-agent signal collector|19|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1654fb2b6418e0856ac80b337846ae043285731d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-09T15:40:53Z"
    },
    "29037481705|1|Scheduled check-agent signal collector|20|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "f473a4cc7cbc914da6bb0c5f3b0af2c0f68f8dcb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-09T17:34:24Z"
    },
    "29043545198|1|Scheduled check-agent signal collector|21|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0e7e3c3356c6912a6814857b788ef88cefd9080d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-09T19:15:04Z"
    },
    "29049903333|1|Scheduled check-agent signal collector|21|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "99a8bcf8c2bf25d483d6db5f571d426fb7ed08f3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-09T21:03:17Z"
    },
    "29055226768|1|Scheduled check-agent signal collector|22|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0fc9f67d3d7dfe1eb95491664178394d76ac5212",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-09T22:41:37Z"
    },
    "29058494281|1|Scheduled check-agent signal collector|23|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3ff4c8a709964a3543490da700e050641bf63957",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-09T23:52:42Z"
    },
    "29068338231|1|Scheduled check-agent signal collector|25|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7a9d9133bb11cbdf00d6dfa484d6a46a06300bad",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-10T04:08:32Z"
    },
    "29078252132|1|Scheduled check-agent signal collector|26|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3422b0aeb0382c2c278abe3c67644e9843594f08",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-10T07:58:08Z"
    },
    "29088870396|1|Scheduled check-agent signal collector|28|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "696a1d145aa6798ce6616c3028d91c337b454daa",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-10T11:15:58Z"
    },
    "29095870310|1|Scheduled check-agent signal collector|28|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "3e412640c530f72f06c41e2b77d7fe2e542d03e2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-10T13:24:35Z"
    },
    "29105275385|1|Scheduled check-agent signal collector|30|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e990b63ec450604e5fcb3dcb21bd784637e7e4fd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-10T15:52:36Z"
    },
    "29112782160|1|Scheduled check-agent signal collector|30|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "85249ce6cce8070104d9a15a5ab877d9cff51206",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-10T18:00:09Z"
    },
    "29119178169|1|Scheduled check-agent signal collector|31|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8b0c2d75908eb055a165083d7aca651db33ce07c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-10T19:47:45Z"
    },
    "29124157006|1|Scheduled check-agent signal collector|32|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "91b92026ab608b0d5fec55ad00afea6028d7179c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-10T21:17:00Z"
    },
    "29127927638|1|Scheduled check-agent signal collector|32|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c5dcbfc226c5ba45e5a5280c86f72b149e4b5ce7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-10T22:31:59Z"
    },
    "29130875348|1|Scheduled check-agent signal collector|33|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e449fd92b7edd3592cd77dad60b6f351789b913e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-10T23:40:41Z"
    },
    "29134143008|1|Scheduled check-agent signal collector|34|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bf69294400440bda14bea065b7eea1971a547871",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-11T01:11:18Z"
    },
    "29139905899|1|Scheduled check-agent signal collector|35|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b74a7e0c5c47fe8978e5e0cca83ca29d4a6382eb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-11T04:38:06Z"
    },
    "29143716101|1|Scheduled check-agent signal collector|36|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "75f1135227117dfe0b597e26759bd74120e1e9e5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-11T06:59:29Z"
    },
    "29146916455|1|Scheduled check-agent signal collector|37|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "12b5e8ca5d09d8108b8d25deaf4c3926cdefec40",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-11T08:57:07Z"
    },
    "29149249924|1|Scheduled check-agent signal collector|37|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "160235d17c811675668f41cab757802b920e4d53",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-11T10:23:55Z"
    },
    "29151037105|1|Scheduled check-agent signal collector|38|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "f792b023306bb5de1e652620d3efc585fe914aa2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-11T11:29:26Z"
    },
    "29153034579|1|Scheduled check-agent signal collector|38|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "482ae7706961598956e9c18a797621d83f69d3fc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-11T12:42:36Z"
    },
    "29155679288|1|Scheduled check-agent signal collector|39|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "79522f1ffff4ea702dc6c9ad2cf574478fa2df62",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-11T14:12:33Z"
    },
    "29157993210|1|Scheduled check-agent signal collector|40|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "14d91c4d4d03d9d1fe06b0c158872914a3c80146",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-11T15:29:33Z"
    },
    "29160095410|1|Scheduled check-agent signal collector|40|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "07f54a02b95a7566c1431a169472172013904654",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-11T16:36:35Z"
    },
    "29162057966|1|Scheduled check-agent signal collector|41|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "80d9352f58eaf6727344975ef7ba44c004164892",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-11T17:41:37Z"
    },
    "29163794611|1|Scheduled check-agent signal collector|41|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "6281a4be8d3018dcdfde868fe9eb3e9e88c84f04",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-11T18:37:55Z"
    },
    "29166056547|1|Scheduled check-agent signal collector|42|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b9aab643cbca7348bd91c0d1229070e20c1a6fde",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-11T19:54:08Z"
    },
    "29168061613|1|Scheduled check-agent signal collector|42|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2dca8f805854bc053602112e481d716a135249ea",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-11T21:01:52Z"
    },
    "29169786245|1|Scheduled check-agent signal collector|42|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b1f8b576ce68c5bce107c1139254a40bbe31b2bd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-11T22:01:57Z"
    },
    "29171531750|1|Scheduled check-agent signal collector|43|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9f0ce97c794c55e4792c5749fd690e70013d26e5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-11T23:04:53Z"
    },
    "29173174238|1|Scheduled check-agent signal collector|43|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2a6b269279e6e55efa11de37c27f72601331b17d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-12T00:06:33Z"
    },
    "29178869858|1|Scheduled check-agent signal collector|45|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "338399c75edb6946280d0e04236154401a50b534",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-12T03:53:19Z"
    },
    "29183087373|1|Scheduled check-agent signal collector|46|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "db8f3d2be5f5850b6f8506e1589d2092ba871db8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-12T06:44:10Z"
    },
    "29186613577|1|Scheduled check-agent signal collector|47|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8609ff5b1f0d4a487c368e16113b67c1c25e607d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-12T08:55:51Z"
    },
    "29189498453|1|Scheduled check-agent signal collector|48|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5820dfbb0b4aef0333191b0e2df2c3bc03d2c97f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-12T10:40:35Z"
    },
    "29191382962|1|Scheduled check-agent signal collector|48|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2748bb476071c2f90ed828f9c846e6a54110f7c0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-12T11:45:38Z"
    },
    "29193062589|1|Scheduled check-agent signal collector|49|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5b2c078a8cf367ef1eb4fe203be351f0a9d2390d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-12T12:41:52Z"
    },
    "29195933911|1|Scheduled check-agent signal collector|49|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d79d9d3d617b79d08e0dae28ddf89e8b21a65678",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-12T14:19:05Z"
    },
    "29198371512|1|Scheduled check-agent signal collector|50|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d09a6725464162b270d820e9d953e7f84cb9ce6f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-12T15:32:45Z"
    },
    "29200466868|1|Scheduled check-agent signal collector|50|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "c29c0ab41a82231e5742fa69e3c0346a287dd665",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-12T16:40:05Z"
    },
    "29202558261|1|Scheduled check-agent signal collector|51|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "778b613b0b7a8d44bb1e0e78e0a6d63c56643dff",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-12T17:46:31Z"
    },
    "29204298717|1|Scheduled check-agent signal collector|51|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7262a68e817a7bbab155230afc9b6689589d53a5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-12T18:40:22Z"
    },
    "29206682581|1|Scheduled check-agent signal collector|52|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8daa52fca2a8c26171c513f487fcfb8a4d3878a0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-12T19:54:48Z"
    },
    "29208862872|1|Scheduled check-agent signal collector|52|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5b8e86ac371aeeb3607b88bab97cdd2aec1e126e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-12T21:02:38Z"
    },
    "29210771652|1|Scheduled check-agent signal collector|53|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bf2c452d3b6ace9b8b4077d64c577ef16edde073",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-12T22:03:20Z"
    },
    "29212705440|1|Scheduled check-agent signal collector|53|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5966cd6e5e58e2bb68353f3cf5780cd81a6eda4b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-12T23:04:16Z"
    },
    "29214648853|1|Scheduled check-agent signal collector|54|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7bba5c221193cdcec6d5f50f283f5c5b28dae946",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-13T00:07:30Z"
    },
    "29222770472|1|Scheduled check-agent signal collector|55|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1c36cd3dac17f3bad99aa5d1f1ba7e9e6883d416",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-13T03:57:14Z"
    },
    "29232399714|1|Scheduled check-agent signal collector|57|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "d8fffff422deb3e37f6672278a96d5d26da4c4a9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-13T07:33:13Z"
    },
    "29243722346|1|Scheduled check-agent signal collector|58|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8f27aff773a195b99814843eaac47d9b7acd6a38",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-13T10:43:44Z"
    },
    "29252497971|1|Scheduled check-agent signal collector|59|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b4b6f033835433a4f387a2eec67c452cac722016",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-13T13:07:46Z"
    },
    "29264769014|1|Scheduled check-agent signal collector|60|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "232b27331d3a8764a495597f13964bde27c2189b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-13T16:04:08Z"
    },
    "29272930114|1|Scheduled check-agent signal collector|61|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e7e0781546e3bbcd4dbebbfe7b75c33b282c28a6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-13T18:04:06Z"
    },
    "29279538757|1|Scheduled check-agent signal collector|62|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2dc7f17e5d31cf65be7b77cf3a22575396d02b8b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-13T19:44:00Z"
    },
    "29283509944|1|Scheduled check-agent signal collector|62|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "82a9d2efcaf14a147f4b9b0eaa06a67692d26029",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-13T20:44:25Z"
    },
    "29287027530|1|Scheduled check-agent signal collector|63|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "184218ad271e806693a0cab40243ea78a05a4305",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-13T21:38:28Z"
    },
    "29290587778|1|Scheduled check-agent signal collector|63|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fbae7e8543f27db68bc6427ff490bc1c93fe225c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-13T22:40:09Z"
    },
    "29293581793|1|Scheduled check-agent signal collector|64|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a266c072617d7e7e33133b2ba0272f0c3db101b5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-13T23:37:46Z"
    },
    "29297635979|1|Scheduled check-agent signal collector|64|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "71efa65f51fe3e48781fb65cbdb1e21fd3adddd8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-14T01:05:17Z"
    },
    "29305469078|1|Scheduled check-agent signal collector|66|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8636bd8be4c5afdca6c502c768e0d21f8d18e1d8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-14T04:14:32Z"
    },
    "29311682726|1|Scheduled check-agent signal collector|67|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d0521319fd2aafbb06c1f6a80b66d670dd9be48c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-14T06:33:27Z"
    },
    "29319780228|1|Scheduled check-agent signal collector|68|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2f2f87f73d9bd0bc8a8c4c3339f8c2854abf7a26",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-14T08:55:54Z"
    },
    "29326997070|1|Scheduled check-agent signal collector|69|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "97a3b6e49ce07ac141648a07a39922aaf4865de0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-14T10:54:45Z"
    },
    "29332109327|1|Scheduled check-agent signal collector|69|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "425e407678bfc8678e46ba20fb0b091d9a356f2f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-14T12:20:53Z"
    },
    "29340491359|1|Scheduled check-agent signal collector|70|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "6b1c7ee5e7aa6c90fc30c9cb56e40904b4dc291e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-14T14:22:15Z"
    },
    "29347391112|1|Scheduled check-agent signal collector|71|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3547374ba7c3f8b1d6c5bcfb2611ab931c00c08e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-14T15:54:58Z"
    },
    "29353600961|1|Scheduled check-agent signal collector|71|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "739f65226e5384e0ace80fea76becb25b966f06a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-14T17:24:33Z"
    },
    "29363770228|1|Scheduled check-agent signal collector|72|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d77e198a81e641c67bdcb00592db5f26b0ec453d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-14T19:58:10Z"
    },
    "29368567800|1|Scheduled check-agent signal collector|73|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ded3257f54151b8844957e3537cc04ce845d0751",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-14T21:11:30Z"
    },
    "29373075401|1|Scheduled check-agent signal collector|74|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0ddb22621051532cba7ba6c95338c130d9b99826",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-14T22:28:36Z"
    },
    "29376585680|1|Scheduled check-agent signal collector|74|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "f8e9e6ca8c86a41f9f844e7a0397460a829f2560",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-14T23:36:02Z"
    },
    "29380586575|1|Scheduled check-agent signal collector|75|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "8d0c9d12a1e8a578a8505735ecdc60f98f2accf9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-15T01:01:45Z"
    },
    "29388479210|1|Scheduled check-agent signal collector|76|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b2f364dedd6b743f0760a27d0ca383b6b1943c07",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-15T04:14:35Z"
    },
    "29394606613|1|Scheduled check-agent signal collector|77|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "12acc6cbbeab1f732556d24aa17e307587948101",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-15T06:35:02Z"
    },
    "29402900578|1|Scheduled check-agent signal collector|78|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "906b3220501d43ee1e3358f081d8dcfe7f8f02fb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-15T09:01:42Z"
    },
    "29410098555|1|Scheduled check-agent signal collector|1|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7cb8df681b5835fa52fb5833cb2540d8a06ef510",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-15T11:01:55Z"
    },
    "29414984878|1|Scheduled check-agent signal collector|1|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ed9cc813ef8946945f099e093ca2231abe0e47f6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-15T12:24:33Z"
    },
    "29422959832|1|Scheduled check-agent signal collector|2|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ef93e5b5bf350397e59793d266109e5fcc742527",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-15T14:24:32Z"
    },
    "29430470593|1|Scheduled check-agent signal collector|3|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "bdebdd1620f53b0cfcb5f69cf35f6a7d5d91c702",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-15T15:59:40Z"
    },
    "29437032038|1|Scheduled check-agent signal collector|4|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "83ec1afffc6986b493d8e7dec20d0b8bafdcc7c3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-15T17:34:43Z"
    },
    "29441922129|1|Scheduled check-agent signal collector|4|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "16b4649fdd5d4a4884f215e002a0cebaa50af940",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-15T18:47:08Z"
    },
    "29446416918|1|Scheduled check-agent signal collector|5|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6e7e0d40f3fbb2d4648be9322db0cd77c7c6cd27",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-15T19:57:23Z"
    },
    "29451050373|1|Scheduled check-agent signal collector|5|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "428019cdad4339be7a01d137bab6c6c1a08b4b8b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-15T21:12:15Z"
    },
    "29455445674|1|Scheduled check-agent signal collector|6|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "dc5682e4fbb9fa42987b3e353157a49859226aec",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-15T22:28:00Z"
    },
    "29459322026|1|Scheduled check-agent signal collector|6|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d65041c5bbd539b36b0839cca47a40d75b3e6a6a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-15T23:42:49Z"
    },
    "29463395162|1|Scheduled check-agent signal collector|7|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "3d1c1cb92ae7a5f3744f4637b408793469841077",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-16T01:09:56Z"
    },
    "29471644696|1|Scheduled check-agent signal collector|8|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b72019cc562e9644162bf2f74f149c22388571c5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-16T04:34:14Z"
    },
    "29479008769|1|Scheduled check-agent signal collector|10|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dc90a6e68087964c03bbaecf0107cbe1f9bc4dbe",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-16T07:10:41Z"
    },
    "29487583880|1|Scheduled check-agent signal collector|11|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "615c8930d6343602b40bd2459ebefb2dca3c4283",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-16T09:34:09Z"
    },
    "29494121031|1|Scheduled check-agent signal collector|11|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "16356b3717e611e41271a4b0dd75dc9a3fdf0a05",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-16T11:21:59Z"
    },
    "29500218734|1|Scheduled check-agent signal collector|12|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "974cb456785065325ff37d3e89d7f1d4e1ca968b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-16T12:58:32Z"
    },
    "29509936383|1|Scheduled check-agent signal collector|13|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "cf4b69945f9864e8a151423e47742ff0627698e9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-16T15:11:05Z"
    },
    "29517041179|1|Scheduled check-agent signal collector|14|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ca6182e7125589ec74c7bd0729e3fa1a320e45f9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-16T16:51:44Z"
    },
    "29523226444|1|Scheduled check-agent signal collector|14|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c91a8551ab546cdb98500745a1b9cf6341ee537c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-16T18:16:23Z"
    },
    "29528834631|1|Scheduled check-agent signal collector|15|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ad2a84f0741cafe4351e5cd4c04662c9dfcdaf20",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-16T19:39:50Z"
    },
    "29532682660|1|Scheduled check-agent signal collector|15|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8de185ed81d8dac2d9691e577b629e4a3d7a3958",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-16T20:35:57Z"
    },
    "29537286913|1|Scheduled check-agent signal collector|16|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "d29d3ba014b78edec0bd58b04c0470d45b6b56d9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-16T21:47:48Z"
    },
    "29540318006|1|Scheduled check-agent signal collector|16|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c2452d32e2ddca6f49ce83e275b3f8307e328daa",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-16T22:43:03Z"
    },
    "29542712259|1|Scheduled check-agent signal collector|17|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "830ac14adce4d7fef03a6b76d025041007c412fd",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-16T23:41:26Z"
    },
    "29546866422|1|Scheduled check-agent signal collector|17|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dd305b3f305384407d08334ef1ab5a3642a1e1aa",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T01:13:31Z"
    },
    "29555274895|1|Scheduled check-agent signal collector|19|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2f6f7f5f0089b9d4c02cc116ba3f2d59cf0760aa",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T04:37:11Z"
    },
    "29561945803|1|Scheduled check-agent signal collector|20|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9cd1eec1e64861d09196f39414232e9e645cada1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T07:05:05Z"
    },
    "29569496142|1|Scheduled check-agent signal collector|21|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ac6e44871c6f2ce81b76802009279bd412099832",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T09:19:12Z"
    },
    "29575537133|1|Scheduled check-agent signal collector|21|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "114d6ab69df693d3f75442b4fbd2baa6d1b426ac",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-17T11:04:15Z"
    },
    "29579787014|1|Scheduled check-agent signal collector|22|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "7e01fe3683895ba3d2fe3b2e21dc21a48a01b2bb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-17T12:19:25Z"
    },
    "29586918556|1|Scheduled check-agent signal collector|23|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "6df57fdfb4b488b95b21c9881542b956ed162869",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-17T14:13:24Z"
    },
    "29593936830|1|Scheduled check-agent signal collector|24|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b4e118f2d0bd02ac84c68a86a3b865aab611391b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-17T15:53:43Z"
    },
    "29599647339|1|Scheduled check-agent signal collector|24|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "cd66d3adc7bb27ef1ce9bf07d783adeedbdd6f9b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-17T17:20:51Z"
    },
    "29604155247|1|Scheduled check-agent signal collector|25|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7ff3cc7e5862b5301a514e08c41d7dc5635519d7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T18:32:29Z"
    },
    "29608949743|1|Scheduled check-agent signal collector|25|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0637b93ddc29a732571322a1eeeb92751b5e85e7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T19:54:39Z"
    },
    "29613484830|1|Scheduled check-agent signal collector|26|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "44f8566ba54688dfc9945b299ec26f68643aeada",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-17T21:05:21Z"
    },
    "29616711315|1|Scheduled check-agent signal collector|26|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d0338d25044c4728ab32ed7e069a2774bd297001",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-17T22:04:22Z"
    },
    "29619631505|1|Scheduled check-agent signal collector|27|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "940e1c1372713b922da7112ab37b47c15d31d4e6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-17T23:03:50Z"
    },
    "29622250569|1|Scheduled check-agent signal collector|27|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d9a9bc10d205493ea9643c0448ab2ebadc6bf325",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-18T00:04:49Z"
    },
    "29628788485|1|Scheduled check-agent signal collector|28|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3fbb1c9ab9dd6b05f7d1a17c3bc4f2f876718dce",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-18T03:26:34Z"
    },
    "29632712997|1|Scheduled check-agent signal collector|29|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f7dfc5b921b882a2ec30918ef364173529d626d8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-18T05:43:47Z"
    },
    "29635545065|1|Scheduled check-agent signal collector|30|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "65a7dca4c3d2aa045082142eee1e8892b488cd47",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-18T07:20:09Z"
    },
    "29638638746|1|Scheduled check-agent signal collector|31|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "98cc1fb1e6b7d731f5cd317ab193e74df591f8d8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-18T09:08:11Z"
    },
    "29641367218|1|Scheduled check-agent signal collector|32|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "15568f5be45eb762e6d617fac52146d262fa6be4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-18T10:45:37Z"
    },
    "29642919140|1|Scheduled check-agent signal collector|32|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "675cde618f8fe717471a56d2c2843699cf366999",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-18T11:39:25Z"
    },
    "29644715592|1|Scheduled check-agent signal collector|32|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0efcb342e99cb87b15fa0898a6f6487a5be76740",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-18T12:39:57Z"
    },
    "29647523086|1|Scheduled check-agent signal collector|33|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7081f2bce4a276f8b982e29c3a4d131208e6690d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-18T14:10:50Z"
    },
    "29650021441|1|Scheduled check-agent signal collector|34|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "cb7f4ff88a1d8983cacf0ac8a1c536893016887e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-18T15:28:52Z"
    },
    "29652343381|1|Scheduled check-agent signal collector|34|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "83404bc2a95ad2d75314624502ccde66c4dfe50b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-18T16:38:12Z"
    },
    "29654414103|1|Scheduled check-agent signal collector|35|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b03208bcc9824b28c1043c9ab1d5e8d362e029c2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-18T17:42:14Z"
    },
    "29656236405|1|Scheduled check-agent signal collector|35|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "765f7843a9a773e12e47b99902d37e60bcb36754",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-18T18:38:24Z"
    },
    "29658648227|1|Scheduled check-agent signal collector|36|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "902993c4505f878fdf2d97baa33495b409149429",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-18T19:53:57Z"
    },
    "29660806119|1|Scheduled check-agent signal collector|36|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e21b18d480bf74e50df1b3f1692c1bb62e05804f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-18T21:02:17Z"
    },
    "29662662745|1|Scheduled check-agent signal collector|36|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ac07a76c77bf3df3458854bb272642dde985aa0d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-18T22:03:05Z"
    },
    "29664554088|1|Scheduled check-agent signal collector|37|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2aadc973840b5d44765a1727d5a38a9f62f43d83",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-18T23:04:32Z"
    },
    "29666335491|1|Scheduled check-agent signal collector|37|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5aacb9e8e9abd56b3da8deca9ef82f09cf9a91a0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T00:04:56Z"
    },
    "29672285798|1|Scheduled check-agent signal collector|39|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "711ed2df77d369a5dd1c5c23a52720e125732da1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-19T03:47:27Z"
    },
    "29676219365|1|Scheduled check-agent signal collector|40|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f000f5170e8dffa6bc4e11dd4090c9c55201ba1c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-19T06:18:42Z"
    },
    "29680240544|1|Scheduled check-agent signal collector|41|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "bbb53b63eae6a7c722ee3c6046d91eac5a41cc90",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-19T08:41:44Z"
    },
    "29683034582|1|Scheduled check-agent signal collector|42|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1aa38a72fafd82c9fbcc57a1d3a1d67b7a612d1f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T10:16:12Z"
    },
    "29685379694|1|Scheduled check-agent signal collector|42|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "45eab03b102992b11c9edab146e8e66045c299ad",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T11:35:04Z"
    },
    "29687352368|1|Scheduled check-agent signal collector|43|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5c741b79178b4478b78cf92b99f58599fd8d990f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T12:38:33Z"
    },
    "29690410645|1|Scheduled check-agent signal collector|43|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d4708c7d95bcbbdabe45b9003b9e1c28f480ba71",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-19T14:15:59Z"
    },
    "29692935065|1|Scheduled check-agent signal collector|44|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "4c02d23946998a302831dea6f57a6446a00784cc",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-19T15:29:51Z"
    },
    "29695216507|1|Scheduled check-agent signal collector|44|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "958d4d81d5ea487a9e0515d1f9567f85db2981fa",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-19T16:38:20Z"
    },
    "29697382433|1|Scheduled check-agent signal collector|45|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b5befc564ec0ce46154758adc9100e14afd5ac15",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-19T17:45:21Z"
    },
    "29699126697|1|Scheduled check-agent signal collector|45|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6ca221addb511d80523705927b48804f2dae9b92",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T18:41:22Z"
    },
    "29701539913|1|Scheduled check-agent signal collector|46|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "7e7bfd3a02a7413907537a8f79b86734c18cf2ba",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-19T19:56:37Z"
    },
    "29703666270|1|Scheduled check-agent signal collector|46|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f31c980b3c0e8afe9d807f9893b2305573dd03e5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T21:03:58Z"
    },
    "29705498828|1|Scheduled check-agent signal collector|47|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "96473fef4b579db8c420c319df9bd97637ffb1df",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T22:05:09Z"
    },
    "29707381179|1|Scheduled check-agent signal collector|47|sambanova|Meta-Llama-3.3-70B-Instruct|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "c822222b5ce6e1d4d606f00571709066e8a32c46",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "rejected",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-19T23:07:37Z"
    },
    "29709065923|1|Scheduled check-agent signal collector|48|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1dea1dd704f4b69981ea8ffb98ad2cde2026ac0c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-20T00:10:11Z"
    },
    "29716297423|1|Scheduled check-agent signal collector|49|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0ccecd3476a0c7db7fdac5e74e88d9aacdea4941",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-20T04:13:02Z"
    },
    "29725310485|1|Scheduled check-agent signal collector|51|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "047bbcb55aec56f795f34a77966a4e2deedcab0f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-20T07:41:16Z"
    },
    "29735350357|1|Scheduled check-agent signal collector|52|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "7734fef361cf6b104e9826130c8df986f4e75ff8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-20T10:31:48Z"
    },
    "29744122271|1|Scheduled check-agent signal collector|53|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0af28609c307158d8b2d087cd7cde7337250692a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-20T12:56:36Z"
    },
    "29754583420|1|Scheduled check-agent signal collector|54|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "976d494673f2fbc1e6ac0b8952d0199db5fe772c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-20T15:19:23Z"
    },
    "29761379745|1|Scheduled check-agent signal collector|55|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5388018810447c1f4e990ed53e01b2a1ace55323",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-20T16:53:59Z"
    },
    "29770392319|1|Scheduled check-agent signal collector|56|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e594a0999fb3c02045068fc2e295d813801a3a20",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-20T19:03:52Z"
    },
    "29776931792|1|Scheduled check-agent signal collector|56|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "006b37c44df4af8b7733b05cdcad003558de106e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-20T20:38:53Z"
    },
    "29781677179|1|Scheduled check-agent signal collector|57|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e0a2eebbc06ee23a162d8a63fd4843bbf5cebd0e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-20T21:50:28Z"
    },
    "29786366646|1|Scheduled check-agent signal collector|58|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "76e90b514c09fa31dc88842a401f0d12b20712ca",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-20T23:11:04Z"
    },
    "29791733615|1|Scheduled check-agent signal collector|58|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dab628a93547bddb915d99bb60155f2f75c74996",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-21T00:56:49Z"
    },
    "29801176773|1|Scheduled check-agent signal collector|60|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "620cffdc0893c3fa81eb18fb16e1e43b881d74a4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-21T04:25:17Z"
    },
    "29809283211|1|Scheduled check-agent signal collector|61|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "febe04c10af070e41ceb841a4868a828a9a359c2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-21T07:08:02Z"
    },
    "29820377417|1|Scheduled check-agent signal collector|62|cerebras|zai-glm-4.7|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "441c36619680b5c1833e587e03efe949f9dea701",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-21T09:58:42Z"
    },
    "29828090192|1|Scheduled check-agent signal collector|63|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5571247aeb4b224f5192d1ed5c74bca055c5f844",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-21T11:57:19Z"
    },
    "29838322903|1|Scheduled check-agent signal collector|64|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e98843af175681f496a2b0d57755e9131a7a24df",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-21T14:17:09Z"
    },
    "29846510881|1|Scheduled check-agent signal collector|65|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ebcf6df3a900feba35ce81e7b27af5b39fe6c1c3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-21T15:59:39Z"
    },
    "29853898633|1|Scheduled check-agent signal collector|65|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "221651944a8875fc646fc6164a317185c7710fde",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-21T17:40:28Z"
    },
    "29859373439|1|Scheduled check-agent signal collector|66|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b73934ce7c365b00c7a60f0841205dfb16e21aa9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-21T18:57:25Z"
    },
    "29865495325|1|Scheduled check-agent signal collector|67|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9ae0058cc50a2a6b0db621c49ad9c8adc6da6724",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-21T20:23:26Z"
    },
    "29870703297|1|Scheduled check-agent signal collector|67|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e156fe8cce9fb70a84debc5d51f397d931cd809c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-21T21:38:02Z"
    },
    "29874428186|1|Scheduled check-agent signal collector|68|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "637d10d1d0d5153fa4d70864a2c79da3900ac994",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-21T22:38:28Z"
    },
    "29877935483|1|Scheduled check-agent signal collector|68|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5e009321793be9e8f721ce396354ad5b8b47a5cc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-21T23:42:49Z"
    },
    "29882297426|1|Scheduled check-agent signal collector|69|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "902b06d6e998a9d359c93d30dfe51a12e91a48b7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T01:09:27Z"
    },
    "29891761737|1|Scheduled check-agent signal collector|70|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "46d45850aee22ca8d5e90d61e4e817374d46ab98",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-22T04:42:48Z"
    },
    "29900103212|1|Scheduled check-agent signal collector|71|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4bb704cf8f74090e059ba4aa2ce01ec24da9e10e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T07:25:27Z"
    },
    "29910130706|1|Scheduled check-agent signal collector|72|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e429ad86e2f873365d27bb3d27bdab363e0adcba",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-22T10:01:21Z"
    },
    "29917810311|1|Scheduled check-agent signal collector|73|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6711163b49ec77760e5998c2c5b3ecff37f5d6e1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T11:59:57Z"
    },
    "29927921874|1|Scheduled check-agent signal collector|74|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "37288d58b8ba8eddbd5f39b792de2fc53b8b8452",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T14:18:53Z"
    },
    "29935733357|1|Scheduled check-agent signal collector|75|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "03e131a64c552cf33cd1a767ec9985254423c8ee",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-22T15:57:18Z"
    },
    "29943061314|1|Scheduled check-agent signal collector|76|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1facd790a68a076391547c95a4fc9520ebf62a7b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T17:37:02Z"
    },
    "29948244397|1|Scheduled check-agent signal collector|76|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2a4fedd9ac048da197f669097c711b893bf25397",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T18:48:33Z"
    },
    "29954544333|1|Scheduled check-agent signal collector|77|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "74d4b1b81cf063153317c3259175a018c1291c7d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-22T20:19:45Z"
    },
    "29959745821|1|Scheduled check-agent signal collector|77|openrouter|poolside/laguna-m.1:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "a3b9c2157761db7e415325ced8eb4bc4c956891b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-22T21:37:15Z"
    },
    "29963785226|1|Scheduled check-agent signal collector|78|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "0d14c480cf0ac0d75d1aec932e330f60d21c1387",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-22T22:43:54Z"
    },
    "29967006977|1|Scheduled check-agent signal collector|78|sambanova|Meta-Llama-3.3-70B-Instruct|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "d3fcf690b788139a9ad58d650c86a1d9be27a9ff",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "rejected",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-22T23:44:18Z"
    },
    "29971363481|1|Scheduled check-agent signal collector|1|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "3b19c219dfdd0f03b5fa184600ffd8e502664c7f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-23T01:16:45Z"
    },
    "29980382226|1|Scheduled check-agent signal collector|2|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ece31af0e6d1edaeec4449a6381d48200c5cb840",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-23T04:48:46Z"
    },
    "29988134543|1|Scheduled check-agent signal collector|4|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7c3c0c51da43aa00721e8a3e5ac32935adaef214",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-23T07:25:11Z"
    },
    "29997406010|1|Scheduled check-agent signal collector|5|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1652366a2fac43abfed3c04d2d2142a0d931fb22",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-23T09:57:45Z"
    },
    "30005192051|1|Scheduled check-agent signal collector|6|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "88dedd08f473778888c5468c5ba5720d4e497261",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-23T11:59:49Z"
    },
    "30015780940|1|Scheduled check-agent signal collector|7|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "98074ef80984764e4bce90300d7f1774c24bbed8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-23T14:26:32Z"
    },
    "30023755302|1|Scheduled check-agent signal collector|7|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "434daa01ea0d41af16c02cdffa75fffe6745b669",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-23T16:09:19Z"
    },
    "30031369418|1|Scheduled check-agent signal collector|8|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f193c8670856183dd351bca0369f301fdb3a3597",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-23T17:54:28Z"
    },
    "30038914680|1|Scheduled check-agent signal collector|9|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9e8189d46847e0537309aea82cf488aa5ab3131e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-23T19:41:18Z"
    },
    "30043302386|1|Scheduled check-agent signal collector|9|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6145ec812b2b8f2447221413511487fb4ae4965b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-23T20:44:16Z"
    },
    "30047448049|1|Scheduled check-agent signal collector|10|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "20aedc4c4db91d81355e368d146df90cfca844a9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-23T21:47:18Z"
    },
    "30050734197|1|Scheduled check-agent signal collector|10|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "939f0e6c80e6128d5e2a5723041ea3b05c724058",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-23T22:41:46Z"
    },
    "30053961711|1|Scheduled check-agent signal collector|11|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3225805888d423616bf28389857cd9c83c1a917e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-23T23:41:58Z"
    },
    "30058300525|1|Scheduled check-agent signal collector|11|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fa5ff454af30ecc0918999151ddf9081e2ed743b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-24T01:12:08Z"
    },
    "30067543638|1|Scheduled check-agent signal collector|13|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3b79295b1f8a1e41ece66d75979a9c548d0e1f40",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-24T04:44:08Z"
    },
    "30075143583|1|Scheduled check-agent signal collector|14|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8c91c09c66bcd91f568d219a14d15ed27a570a09",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-24T07:21:17Z"
    },
    "30083491656|1|Scheduled check-agent signal collector|15|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "a68aa3b0392919149760e4ac5207fadc95dd1196",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-24T09:42:53Z"
    },
    "30089543254|1|Scheduled check-agent signal collector|16|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "158bf627527e204b5d1587528cb9210ad28572cb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-24T11:26:34Z"
    },
    "30095115871|1|Scheduled check-agent signal collector|16|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "96fcdaa878920cb5a81a4c4eab7feb50bdaf8587",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-24T12:59:55Z"
    },
    "30103644372|1|Scheduled check-agent signal collector|17|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "100bc79002899d75b11a3e52e5ca563ef97dffd4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-24T15:04:01Z"
    },
    "30110817562|1|Scheduled check-agent signal collector|18|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9b0f6f8b513bc6b567ad3260ebcadd050d43d778",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-24T16:54:08Z"
    },
    "30117835700|1|Scheduled check-agent signal collector|19|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9bb13fe9c2118a0391776a24ffe3abbf18b72eee",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-24T18:40:55Z"
    },
    "30122570649|1|Scheduled check-agent signal collector|19|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ef8e0f29c8f64e7ba82e22a228d9d5d498bc27f7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-24T20:03:55Z"
    },
    "30127191117|1|Scheduled check-agent signal collector|20|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "0cb3750d1c24eeea3155af1add5c4056ec06ff1f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-24T21:18:25Z"
    },
    "30131255971|1|Scheduled check-agent signal collector|20|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "516522f8e856f5cd5e40c122e8d004124d5f4133",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-24T22:33:43Z"
    },
    "30134592485|1|Scheduled check-agent signal collector|21|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "fb09f8174850ad4ee56c082901096b57b493be91",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-24T23:46:53Z"
    },
    "30138064159|1|Scheduled check-agent signal collector|22|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "528e5d3e4b9de9f36999e43ff0246dc5cd45c9ba",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-25T01:14:40Z"
    },
    "30144389670|1|Scheduled check-agent signal collector|23|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0bd5896da87334a191a21205d96f07aa382424d2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T04:39:28Z"
    },
    "30148645731|1|Scheduled check-agent signal collector|24|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d5ccb791c8dbd7971447338dffecea3fe5a46834",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T07:04:58Z"
    },
    "30152317516|1|Scheduled check-agent signal collector|25|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "53900c62e401d0adfc81fe4c8ea2d1a171568968",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T09:09:21Z"
    },
    "30155190095|1|Scheduled check-agent signal collector|26|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2bbac1078be2e99efc1dce5e3eb26b68a84a72c4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-25T10:51:20Z"
    },
    "30157420113|1|Scheduled check-agent signal collector|26|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6fc2eea9a3793989a7079bd20c8e4b0a9c1ac822",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-25T12:07:28Z"
    },
    "30160768198|1|Scheduled check-agent signal collector|27|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e0b410e5708716e2bf8f90af8bdfd0f8d2efc0a9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T14:00:01Z"
    },
    "30163235556|1|Scheduled check-agent signal collector|28|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "cb91c829c5384bf6292cd3c32f2a5d63c4ed7de3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-25T15:15:28Z"
    },
    "30165580547|1|Scheduled check-agent signal collector|28|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e58045011579a2331a8ea215e97117deb308734f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T16:25:41Z"
    },
    "30167766694|1|Scheduled check-agent signal collector|29|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "0a3d0ae7a47ed8d0acbf19d16197687b0ef776b3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-25T17:32:02Z"
    },
    "30170104611|1|Scheduled check-agent signal collector|29|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "913c5adaeb1f006c068a93cea87b3e2ba4d7c74e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T18:41:24Z"
    },
    "30172654615|1|Scheduled check-agent signal collector|30|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1ac92f16754fe5bde87bf735357470919173f3ca",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-25T19:58:58Z"
    },
    "30174924598|1|Scheduled check-agent signal collector|30|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a78d4556fe59f10eed64f3b309d492c3b3aa4635",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T21:05:56Z"
    },
    "30176941146|1|Scheduled check-agent signal collector|31|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a7fbf5581675faa7b9c9d49e518f7a3cb189e59e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-25T22:07:20Z"
    },
    "30178906683|1|Scheduled check-agent signal collector|31|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2e403828f5245cbd83945f826ad7d7f898e6d5ad",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-25T23:10:15Z"
    },
    "30182266151|1|Scheduled check-agent signal collector|32|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fe96ffb0ba1807929ef8ac10b17b4b9e25a83867",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-26T01:04:48Z"
    },
    "30188052079|1|Scheduled check-agent signal collector|33|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dded4065472a0e875a7370dfa7b69a396a68015f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-26T04:37:08Z"
    },
    "30192712167|1|Scheduled check-agent signal collector|34|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2b33d24cd235368f3e19a4c9b9b3f83487756d85",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T07:30:21Z"
    },
    "30196613587|1|Scheduled check-agent signal collector|35|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0a482dada80dcd14e3c21a99c1bf8d46f6395c8c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T09:37:12Z"
    },
    "30199606963|1|Scheduled check-agent signal collector|36|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b2d8190de918e96a8ffff3bbc2e762076c0ab7fa",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-26T11:10:24Z"
    },
    "30202377962|1|Scheduled check-agent signal collector|37|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bb8541130d78e196d3aa0187305882bf7944c81b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-26T12:36:37Z"
    },
    "30205766044|1|Scheduled check-agent signal collector|37|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d8cfc7d06cb640de655d152755c0b038738a95b4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T14:22:34Z"
    },
    "30208571996|1|Scheduled check-agent signal collector|38|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "bbda4ab90f90d5281f3599bab1f402b490885123",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-26T15:37:20Z"
    },
    "30210845614|1|Scheduled check-agent signal collector|38|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "140767b9b2769964c121e201a16abb01401090b3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T16:42:56Z"
    },
    "30213266796|1|Scheduled check-agent signal collector|39|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "bf85352aa49745b116f0c1ed890aacbd2e6d888a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T17:48:05Z"
    },
    "30215405165|1|Scheduled check-agent signal collector|39|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ef42025aebc02a242487822ec76290a8024de144",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-26T18:46:05Z"
    },
    "30217973206|1|Scheduled check-agent signal collector|40|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "1588af6d7baf6db76cd131bafb0c93c2736dee19",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T19:59:13Z"
    },
    "30220448747|1|Scheduled check-agent signal collector|40|openrouter|poolside/laguna-m.1:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "61975bb1a60d14a72eea2934cf104e30139c9779",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T21:10:53Z"
    },
    "30223176486|1|Scheduled check-agent signal collector|41|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "de0ce051c248c7a64bf82e1864889a1e5400cb40",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-26T22:28:16Z"
    },
    "30225840301|1|Scheduled check-agent signal collector|41|openrouter|poolside/laguna-m.1:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "fc460ed97799967434e0f49814524db634476bc6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-26T23:47:59Z"
    },
    "30229550182|1|Scheduled check-agent signal collector|42|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9178395a93fd3e5b9b7faae0cbef7d4ea428fd5e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-27T01:20:12Z"
    },
    "30238757184|1|Scheduled check-agent signal collector|44|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "487aacc69dea2271c8f6a4f3622c97c0542a944f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-27T05:05:22Z"
    },
    "30251053179|1|Scheduled check-agent signal collector|45|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "68ea84da6753159559c4d72586f5ef900fef1e59",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-27T08:45:05Z"
    },
    "30264059559|1|Scheduled check-agent signal collector|47|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3a76489928a624646a876796306cd8ec0061da03",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-27T12:00:04Z"
    },
    "30278544959|1|Scheduled check-agent signal collector|48|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3aea04826185765fe9a9ce25aa2bfe95b31773a8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-27T15:08:59Z"
    },
    "30288440864|1|Scheduled check-agent signal collector|49|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "f8792018cd6a2ab440831b66579fd81f6226ff50",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-27T17:16:05Z"
    },
    "30295812152|1|Scheduled check-agent signal collector|50|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a5f15debbfb27295400b1b8b4bf8d7c3b297bab6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-27T18:54:12Z"
    },
    "30303560463|1|Scheduled check-agent signal collector|50|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "224a7c4921d6814c5bdad2782b82766c16381a39",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-27T20:40:44Z"
    },
    "30308359854|1|Scheduled check-agent signal collector|51|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5c023e85241595a8aa1fe94b8a202cec4ae210a2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-27T21:49:40Z"
    },
    "30313576628|1|Scheduled check-agent signal collector|52|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "260234a6475ff3a115c0bee07e8f63b4965117c4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-27T23:16:25Z"
    },
    "30318649450|1|Scheduled check-agent signal collector|52|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6c3b906a6b928aaa0be211256626a2571c6e04d1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-28T00:53:46Z"
    },
    "30328463735|1|Scheduled check-agent signal collector|54|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2fc5241f6f059b4dd3e188ad5f6c7a69aeed429e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-28T04:21:01Z"
    },
    "30337256367|1|Scheduled check-agent signal collector|55|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "4eb0e784b1b85ed6b6b475d98732fa4dc5290802",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-28T07:08:41Z"
    },
    "30349159914|1|Scheduled check-agent signal collector|56|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bb755d9603e7f1a822fdb17ead0a3434276e642a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-28T10:03:35Z"
    },
    "30357581697|1|Scheduled check-agent signal collector|57|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "199dba682ce96648233572e0a4a3e0140da1779f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-28T12:07:59Z"
    },
    "30370932345|1|Scheduled check-agent signal collector|58|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bc3379f89a210584fe0889737a3b4f04955de5e1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-28T14:57:44Z"
    },
    "30379908122|1|Scheduled check-agent signal collector|59|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fd685e39041ed5a1f8c2644411e4575dc0983037",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-28T16:48:28Z"
    },
    "30387244275|1|Scheduled check-agent signal collector|60|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5be2ce5db39ce188f0e41fbd79773c99a2d3eccb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-28T18:24:27Z"
    },
    "30394369040|1|Scheduled check-agent signal collector|60|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "8bae0dd75a4ab1428b05b02e47568efa984312c8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-28T20:00:40Z"
    },
    "30400068479|1|Scheduled check-agent signal collector|61|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e5e136ec7db07af4fa8bf7b48805f7a99dde923c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-28T21:18:26Z"
    },
    "30404873742|1|Scheduled check-agent signal collector|62|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ff68ab93411c4d7042477026e34b34e49d519467",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-28T22:32:20Z"
    },
    "30408827556|1|Scheduled check-agent signal collector|62|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "39f07412c003e294be325667f90629e9bec2b90e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-28T23:43:13Z"
    },
    "30413308790|1|Scheduled check-agent signal collector|63|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "42a211f45caab0a6e97403190fa4c426f6059269",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-29T01:11:14Z"
    },
    "30422961386|1|Scheduled check-agent signal collector|64|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e3a3d95dc9b0e98528f8b1e589d1137bbee97eb8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-29T04:42:16Z"
    },
    "30432019163|1|Scheduled check-agent signal collector|65|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "d44fc497d384af062d103762cc90789f801b8229",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-29T07:32:47Z"
    },
    "30443184920|1|Scheduled check-agent signal collector|67|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c681e8811cae1507dc22928b84602b08d6d017cc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-29T10:19:44Z"
    },
    "30451654192|1|Scheduled check-agent signal collector|68|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ada87d663ddedd19ef359f8ca0b4483a2a11a9eb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-29T12:27:51Z"
    },
    "30463533721|1|Scheduled check-agent signal collector|69|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e7b34572840f101732f1a587f30240b473d233d4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-29T14:58:52Z"
    },
    "30471537649|1|Scheduled check-agent signal collector|69|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2c38250cc5bcb13055f76fd826bab558865766a7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-29T16:37:24Z"
    },
    "30477665076|1|Scheduled check-agent signal collector|70|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "22d73faddae2d05c0ee47a5ad34fc47080e577fb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-29T17:58:11Z"
    },
    "30485295939|1|Scheduled check-agent signal collector|71|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "84ced126c6cab8e5ec0efe80e64d598799290e97",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-29T19:39:05Z"
    },
    "30489171582|1|Scheduled check-agent signal collector|71|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "98f422f25499f820dccdcae84b82d45b4c017c17",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-07-29T20:37:59Z"
    },
    "30493228041|1|Scheduled check-agent signal collector|71|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "79b470fa3936857500b50c894b6b12617680fc2b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-29T21:40:32Z"
    },
    "30496996871|1|Scheduled check-agent signal collector|72|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "38b8fb776862c97b4b59a8b88f0fc1ee5c78da2d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-29T22:42:06Z"
    },
    "30500460629|1|Scheduled check-agent signal collector|72|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6b79a2930225861ba239e005cc55c56a4e83fb68",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-29T23:44:35Z"
    },
    "30504562562|1|Scheduled check-agent signal collector|73|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "353049717cbc481aea0c9a0313fd66a1e8864473",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-30T01:05:40Z"
    },
    "30513396101|1|Scheduled check-agent signal collector|74|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5bb4f5bf87078595d8d2a4eb8a42fd826a39d626",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-30T04:16:17Z"
    },
    "30521894199|1|Scheduled check-agent signal collector|76|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e279d401ee346a93e6739d97eab790b9ab51c95c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-30T07:08:44Z"
    },
    "30532746606|1|Scheduled check-agent signal collector|77|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d343f75ab151a0ebced8268bf3d752e65a63a18c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-30T09:57:47Z"
    },
    "30540743350|1|Scheduled check-agent signal collector|78|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a3352ba63a975f152bd183ff1a9849f1f9e92484",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-30T12:01:00Z"
    },
    "30551734087|1|Scheduled check-agent signal collector|1|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "95520295673051debc744984650d8dd3bfd42780",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-30T14:27:22Z"
    },
    "30559987947|1|Scheduled check-agent signal collector|1|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "cb040a74815ba0e97849977f53123db70b84d6ed",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-30T16:07:50Z"
    },
    "30568067224|1|Scheduled check-agent signal collector|2|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0e6b9dc01c9747df2097f17a32dc9348c100880f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-30T17:55:24Z"
    },
    "30576248835|1|Scheduled check-agent signal collector|3|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "d256d0a26fdcc37820ab87a46428d558266481f1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-30T19:47:43Z"
    },
    "30580856852|1|Scheduled check-agent signal collector|3|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "17e5575d70b3a7e429e536e3b8e776c0f704a55c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-30T20:50:20Z"
    },
    "30586510576|1|Scheduled check-agent signal collector|4|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1eeefc482615260f3676d2afeab438b3b01d429b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-07-30T22:16:31Z"
    },
    "30590731614|1|Scheduled check-agent signal collector|5|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ebcb7405fb378542d78e0b9113639ac69516541a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-30T23:31:09Z"
    },
    "30595856180|1|Scheduled check-agent signal collector|5|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b0c48c207a52d3b3baad2626d5699fbec9d6d689",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-31T01:15:59Z"
    },
    "30605332131|1|Scheduled check-agent signal collector|7|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "793a1bb6b5248d2b4d4355f9f7f613f8f85d4843",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-31T04:55:44Z"
    },
    "30615156148|1|Scheduled check-agent signal collector|8|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "65898ebdf9f36f952170b85e8b1b67311418f722",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-31T08:07:33Z"
    },
    "30624877863|1|Scheduled check-agent signal collector|9|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6aa9f0a2a35f3ca98ce25a0fe074b12a16743016",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-31T10:50:02Z"
    },
    "30632955475|1|Scheduled check-agent signal collector|10|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3f53c37ef4ebc0aa6ade5233e46ab0b41014e8fd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-31T13:04:10Z"
    },
    "30642952945|1|Scheduled check-agent signal collector|11|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "56771b67fef00707ba21e304350331ba5e3a1527",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-31T15:27:56Z"
    },
    "30650187537|1|Scheduled check-agent signal collector|12|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "47299ba50ce86e6aa5d13ecbf87e251ff1bc4e07",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-31T17:12:06Z"
    },
    "30656764682|1|Scheduled check-agent signal collector|13|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "96b8c1608090766e25ab90af0113dd4759f9de82",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-07-31T18:51:17Z"
    },
    "30663361400|1|Scheduled check-agent signal collector|14|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ed08e125099fa67bebddaae4c023d90efef5c07a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-31T20:34:51Z"
    },
    "30667807440|1|Scheduled check-agent signal collector|14|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b491cee3bea2d2a0d8c4f0fe24f3a0311a7fad37",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-07-31T21:48:04Z"
    },
    "30672237117|1|Scheduled check-agent signal collector|15|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5d70df5babb86b20ca72e5468f802d3eecc7b646",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-07-31T23:12:58Z"
    },
    "30676892830|1|Scheduled check-agent signal collector|15|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c260002abbbcfcda7887eef22047fe0cdcecf923",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-01T01:00:34Z"
    },
    "30684029376|1|Scheduled check-agent signal collector|17|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "27895632fcab2be293625aed1e3f1f9d6b1a9c19",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-01T04:29:45Z"
    },
    "30689400196|1|Scheduled check-agent signal collector|18|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "149b229f06a548409e80e98a790dd0a74d8aed6d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T07:16:47Z"
    },
    "30693872652|1|Scheduled check-agent signal collector|19|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "42fb856aaf3b8a60ee19ab5cdf76bdda1ae44ab4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T09:30:58Z"
    },
    "30697030245|1|Scheduled check-agent signal collector|20|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b5e797cae7bff991e8920b581098d140736e1a5d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-01T11:06:53Z"
    },
    "30699179167|1|Scheduled check-agent signal collector|20|sambanova|Meta-Llama-3.3-70B-Instruct|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5de52fd0aa12a4d0994c68622365e325dd789bd5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "rejected",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-01T12:11:33Z"
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
