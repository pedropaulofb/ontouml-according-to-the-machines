# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics for the scheduled Phase 2 check-agent signal collector.

The table is updated by GitHub Actions from deterministic Python-side batch statuses. It does not use LLM self-reporting, raw completions, prompts, provider responses, or token-usage estimates.

Statistics collection started on: `2026-06-29T12:18:18Z`

Counts shown on this page only include executions recorded since that start time.

Models not present in the current active rotation remain listed as `inactive` for historical continuity.

Last generated: `2026-08-19T08:50:28Z`

## Cumulative table

| Provider | Model | Status | # called | # valid | # invalid | # rejected | # provider failed | # runner failed | Last check status | Last issue status | Last run UTC |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `cerebras` | `gpt-oss-120b` | `active` | 111 | 84 | 27 | 20 | 7 | 0 | `provider_failed` | `skipped` | `2026-08-19T07:49:14Z` |
| `cerebras` | `zai-glm-4.7` | `active` | 117 | 100 | 17 | 3 | 13 | 1 | `provider_failed` | `skipped` | `2026-08-19T07:00:49Z` |
| `gemini` | `gemini-3.1-flash-lite` | `active` | 127 | 41 | 86 | 86 | 0 | 0 | `rejected` | `skipped` | `2026-08-19T08:50:28Z` |
| `groq` | `llama-3.3-70b-versatile` | `inactive` | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | 107 | 42 | 65 | 58 | 7 | 0 | `ok` | `ok` | `2026-08-19T03:57:23Z` |
| `openrouter` | `poolside/laguna-m.1:free` | `active` | 113 | 34 | 79 | 8 | 71 | 0 | `provider_failed` | `skipped` | `2026-08-19T05:16:30Z` |
| `sambanova` | `DeepSeek-V3.1` | `active` | 121 | 90 | 31 | 0 | 31 | 0 | `provider_failed` | `skipped` | `2026-08-19T05:53:42Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | 119 | 90 | 29 | 5 | 24 | 0 | `provider_failed` | `skipped` | `2026-08-19T04:47:14Z` |

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
  "generated_at": "2026-08-19T08:50:28Z",
  "models": {
    "cerebras:gpt-oss-120b": {
      "called": 111,
      "invalid": 27,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "32229555497",
      "last_run_utc": "2026-08-19T07:49:14Z",
      "model": "gpt-oss-120b",
      "provider": "cerebras",
      "provider_failed": 7,
      "rejected": 20,
      "runner_failed": 0,
      "spec": "cerebras:gpt-oss-120b",
      "valid": 84
    },
    "cerebras:zai-glm-4.7": {
      "called": 117,
      "invalid": 17,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "32225830059",
      "last_run_utc": "2026-08-19T07:00:49Z",
      "model": "zai-glm-4.7",
      "provider": "cerebras",
      "provider_failed": 13,
      "rejected": 3,
      "runner_failed": 1,
      "spec": "cerebras:zai-glm-4.7",
      "valid": 100
    },
    "gemini:gemini-3.1-flash-lite": {
      "called": 127,
      "invalid": 86,
      "last_check_status": "rejected",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "rejected",
      "last_run_attempt": "1",
      "last_run_id": "32234528105",
      "last_run_utc": "2026-08-19T08:50:28Z",
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "provider_failed": 0,
      "rejected": 86,
      "runner_failed": 0,
      "spec": "gemini:gemini-3.1-flash-lite",
      "valid": 41
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
      "called": 107,
      "invalid": 65,
      "last_check_status": "ok",
      "last_event_name": "schedule",
      "last_issue_status": "ok",
      "last_overall_status": "ok",
      "last_run_attempt": "1",
      "last_run_id": "32213915572",
      "last_run_utc": "2026-08-19T03:57:23Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "provider_failed": 7,
      "rejected": 58,
      "runner_failed": 0,
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
      "valid": 42
    },
    "openrouter:poolside/laguna-m.1:free": {
      "called": 113,
      "invalid": 79,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "32218782793",
      "last_run_utc": "2026-08-19T05:16:30Z",
      "model": "poolside/laguna-m.1:free",
      "provider": "openrouter",
      "provider_failed": 71,
      "rejected": 8,
      "runner_failed": 0,
      "spec": "openrouter:poolside/laguna-m.1:free",
      "valid": 34
    },
    "sambanova:DeepSeek-V3.1": {
      "called": 121,
      "invalid": 31,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "32221117335",
      "last_run_utc": "2026-08-19T05:53:42Z",
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "provider_failed": 31,
      "rejected": 0,
      "runner_failed": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "valid": 90
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "called": 119,
      "invalid": 29,
      "last_check_status": "provider_failed",
      "last_event_name": "schedule",
      "last_issue_status": "skipped",
      "last_overall_status": "failed",
      "last_run_attempt": "1",
      "last_run_id": "32216989766",
      "last_run_utc": "2026-08-19T04:47:14Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "provider_failed": 24,
      "rejected": 5,
      "runner_failed": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "valid": 90
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
    "30703003238|1|Scheduled check-agent signal collector|21|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "edb69051a89ce8c7c5a3c7d3d7e5189f84afc63e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-01T14:04:54Z"
    },
    "30705441205|1|Scheduled check-agent signal collector|22|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "093428936a0aa1452e7c34aeec9183f8dd65f95f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T15:14:00Z"
    },
    "30708155239|1|Scheduled check-agent signal collector|22|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8f0b36d45ee54517fdf15a647625d06305d33779",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T16:27:40Z"
    },
    "30710971573|1|Scheduled check-agent signal collector|23|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a82fe4710f7f9ab4ee5f7a74c08b5f94417a5d2d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T17:44:42Z"
    },
    "30713178668|1|Scheduled check-agent signal collector|23|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "df616d2d198670ce16dd283e489c57b2465f6bc6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-01T18:44:24Z"
    },
    "30715959929|1|Scheduled check-agent signal collector|24|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c2a162020f5e8c5633f35f87efa186176238f0e6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T19:59:39Z"
    },
    "30718408871|1|Scheduled check-agent signal collector|24|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "4d5b51be9f789e55a7336d62cae4d48c3cb9d920",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-01T21:06:44Z"
    },
    "30720627226|1|Scheduled check-agent signal collector|25|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0675b33c3e18710261914f24b680d6dd4031b937",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T22:09:18Z"
    },
    "30723333037|1|Scheduled check-agent signal collector|25|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "9fef7990506f5064ef4d1ac9b6f5d1bc899b37f3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-01T23:27:04Z"
    },
    "30726479536|1|Scheduled check-agent signal collector|26|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "931c10b94ec57411032c6bf48360d289c92ac26c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T01:09:01Z"
    },
    "30733024797|1|Scheduled check-agent signal collector|27|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6297b0c762013d429bd77aa7a0591dc63e26e8eb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T04:49:39Z"
    },
    "30738203849|1|Scheduled check-agent signal collector|29|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "145da69047c958c4f7cd242841eed70d67bb56fe",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-02T07:39:11Z"
    },
    "30742374047|1|Scheduled check-agent signal collector|29|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "68a4752b6b62d46cbb323340d36cf4ca8a7601a9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T09:45:24Z"
    },
    "30745098640|1|Scheduled check-agent signal collector|30|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5dc1d142da3f905285529494bea0226b8c55a2f6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-02T11:07:53Z"
    },
    "30748054132|1|Scheduled check-agent signal collector|31|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6aa06b7a597440b57770710c359bee67de5e0ad8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-02T12:33:39Z"
    },
    "30751705678|1|Scheduled check-agent signal collector|31|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "532aad07c98098675009abcadd7a7ee0bbbc101a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T14:16:06Z"
    },
    "30754701718|1|Scheduled check-agent signal collector|32|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "a823fc559b16ad693d286edce026d47ad2201304",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-02T15:36:14Z"
    },
    "30757069355|1|Scheduled check-agent signal collector|32|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c80aa58c2fd0b2406c51438330633de87c5c1d7b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T16:38:30Z"
    },
    "30759569074|1|Scheduled check-agent signal collector|33|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9712102196ba4d4bc195f32a4f4dd7be94874f44",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T17:47:44Z"
    },
    "30761794491|1|Scheduled check-agent signal collector|33|sambanova|Meta-Llama-3.3-70B-Instruct|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "6d6ae822bf729448823bcbe1e954c41e6c7cb23d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "rejected",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-02T18:44:50Z"
    },
    "30764567389|1|Scheduled check-agent signal collector|34|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "221b89a3c3fc914f5d7b67c4551c98e3a756cce0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T19:59:59Z"
    },
    "30767146429|1|Scheduled check-agent signal collector|34|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f1fbee79de96b590592e561522e151b891256b3a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T21:07:18Z"
    },
    "30769427535|1|Scheduled check-agent signal collector|35|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "fbb203df7ff0f8208a3e428f59eed8ed69a351e9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T22:09:26Z"
    },
    "30772281273|1|Scheduled check-agent signal collector|35|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "bf52a9a656659430d488a7e64e88743c8eba5e54",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-02T23:27:39Z"
    },
    "30776124522|1|Scheduled check-agent signal collector|36|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ec761d2ade26f8197e2dbaafb690ee6738a0b4cd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-03T01:08:33Z"
    },
    "30785849365|1|Scheduled check-agent signal collector|38|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e2a9e4dcbb607e4549099cd391fc5523d6662632",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-03T04:59:01Z"
    },
    "30798185143|1|Scheduled check-agent signal collector|39|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c06580df32c4646dadd110dd3dd91b426f96f0af",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-03T08:40:53Z"
    },
    "30811843013|1|Scheduled check-agent signal collector|41|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1e62a7e5d92675916da499fea8bdc1bf9b57f128",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-03T12:02:12Z"
    },
    "30826280805|1|Scheduled check-agent signal collector|42|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "65eff33860760b80ebdf07f8451816c1e850a60f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-03T15:11:40Z"
    },
    "30836477272|1|Scheduled check-agent signal collector|43|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "88e844a893d205a3fc0eb136b95fb9cb207b4a61",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-03T17:23:29Z"
    },
    "30844103555|1|Scheduled check-agent signal collector|44|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "96f48215de1e23ace12102379adeb8d91528706b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-03T19:04:37Z"
    },
    "30851011144|1|Scheduled check-agent signal collector|44|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "a8d23653ab66cc01434b81000167394a5e1c56e0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-03T20:37:35Z"
    },
    "30856218836|1|Scheduled check-agent signal collector|45|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "40d2d3ee12dc58bfd353c27b375e0344d9d7332c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-03T21:50:13Z"
    },
    "30861593845|1|Scheduled check-agent signal collector|46|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "29ca7b72349ebc1dbd9f09ec81060f1cfea5580f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-03T23:15:42Z"
    },
    "30867229495|1|Scheduled check-agent signal collector|46|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "26421f43b7cf8f6fa0439e52f9f96ea9ca3e9cc5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-04T00:58:49Z"
    },
    "30877524555|1|Scheduled check-agent signal collector|48|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "712c7be9a745901eecd9e61cd1b1105ec4a63dd3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-04T04:23:57Z"
    },
    "30886744796|1|Scheduled check-agent signal collector|49|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ed830f18ce0deb5c75ef6b61db73ecb65f826b81",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-04T07:10:57Z"
    },
    "30899239852|1|Scheduled check-agent signal collector|50|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f624d2e2738cd896707735b82b43cde4f21470dd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-04T10:07:10Z"
    },
    "30908358527|1|Scheduled check-agent signal collector|51|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f519987085373c17fe872412d0bd13091c967c22",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-04T12:16:54Z"
    },
    "30921628873|1|Scheduled check-agent signal collector|52|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "690787c2c2bcd5b094b1ea2f96423a027505f00f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-04T14:58:02Z"
    },
    "30931798853|1|Scheduled check-agent signal collector|53|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b508330cb1d111dde7fcacae6fc38f19272eb184",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-04T17:00:31Z"
    },
    "30940140239|1|Scheduled check-agent signal collector|54|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9f87b4d552ebfa3baa9cbe1089bd48c4814046d8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-04T18:48:09Z"
    },
    "30946894758|1|Scheduled check-agent signal collector|55|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "be646bfe0ae2d0459692e8e3a5168e15512cba43",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-04T20:14:26Z"
    },
    "30953681638|1|Scheduled check-agent signal collector|55|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "36400d1c61e7cb67ab8de4bcebb49d0241fc438d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-04T21:46:23Z"
    },
    "30957672255|1|Scheduled check-agent signal collector|56|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "77156674d49048815327aeea3c3ab3eb71e59855",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-04T22:47:24Z"
    },
    "30961136767|1|Scheduled check-agent signal collector|56|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0ab331db7aa066007bf908b4dee6a105514164b1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-04T23:47:23Z"
    },
    "30965553315|1|Scheduled check-agent signal collector|57|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4c975d9ce69653c2095ad83a5e91e11f0b4c2660",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-05T01:10:22Z"
    },
    "30975723216|1|Scheduled check-agent signal collector|58|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "43c0e11159a3e83427e4f232b0ef370b1f1a616f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-05T04:39:05Z"
    },
    "30984997872|1|Scheduled check-agent signal collector|59|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a362debc37b7bcb192abe8dd068b6048561ec820",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-05T07:26:34Z"
    },
    "30996189002|1|Scheduled check-agent signal collector|61|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "76d881c56787e6909ae188b22554ad42b0b7958f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-05T10:08:58Z"
    },
    "31005270555|1|Scheduled check-agent signal collector|61|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "7c2366075becd3fc149ec408160157022e6c4b1a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-05T12:22:13Z"
    },
    "31016686357|1|Scheduled check-agent signal collector|62|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "07758af61f96f9ac840beff4e26293180215b59c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-05T14:44:38Z"
    },
    "31024946619|1|Scheduled check-agent signal collector|63|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4c08f57155c3bcd0c6a7a895e7e0e2524aea0892",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-05T16:22:59Z"
    },
    "31032699588|1|Scheduled check-agent signal collector|64|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f43b2a4e4e643efd06092a2b00cde8e45165af20",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-05T18:02:40Z"
    },
    "31041205188|1|Scheduled check-agent signal collector|65|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6a562c7ff3bcb08252d361dbc606bb67e45e0244",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-05T19:50:21Z"
    },
    "31048290286|1|Scheduled check-agent signal collector|65|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dd29a5a7f0ad9b3250fbbea598c64c4276fdb0be",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-05T21:22:11Z"
    },
    "31053176042|1|Scheduled check-agent signal collector|66|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ce102e2a3d84952a07571fb281775022ceeebe23",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-05T22:34:17Z"
    },
    "31057156518|1|Scheduled check-agent signal collector|66|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d40cd8a74b8af4419ad43e91c358fd6b09bdaec2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-05T23:40:53Z"
    },
    "31061790139|1|Scheduled check-agent signal collector|67|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "368b461c784fbd47046f8aa6508ef860202e08d8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-06T01:07:26Z"
    },
    "31071335694|1|Scheduled check-agent signal collector|68|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "ce96ef8db85f7016dbdcc1f7a53012f6894c669d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-06T04:28:43Z"
    },
    "31080957812|1|Scheduled check-agent signal collector|70|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9f14aa984343f18b8a04f3cf34aca3dc3d2fede2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-06T07:27:31Z"
    },
    "31092199755|1|Scheduled check-agent signal collector|71|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "99805df5d22eefe15de9494322e058bc34d36a9d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-06T10:12:39Z"
    },
    "31101207546|1|Scheduled check-agent signal collector|72|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ec74ef1a82d12f70f5790543aee45d51e1a308c6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-06T12:24:34Z"
    },
    "31113026638|1|Scheduled check-agent signal collector|73|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b0f36d87e8cee8a0e86bbf9dcdb1ef885fd226e8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-06T14:55:14Z"
    },
    "31134966000|1|Scheduled check-agent signal collector|77|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0d75c4befb8f15f9743ce143a6121adc198edda9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-07T00:32:25Z"
    },
    "31145020352|1|Scheduled check-agent signal collector|78|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "989021417e22826982942390a35fce634284bb85",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-07T03:40:28Z"
    },
    "31150483935|1|Scheduled check-agent signal collector|1|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "fa5ece5aea975ee80895f290d9549bcc7a28a143",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-07T05:25:11Z"
    },
    "31155059852|1|Scheduled check-agent signal collector|2|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "25eb293fec19c9b5e6b618646e92b4056788a93c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T06:45:48Z"
    },
    "31159967402|1|Scheduled check-agent signal collector|2|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2a27d3119fe0b4ceae57351a7792d1c527b0c4d6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T08:01:41Z"
    },
    "31164841299|1|Scheduled check-agent signal collector|3|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0d6f332ed95d9b4a62422f573318b6c8ccec0757",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-07T09:12:07Z"
    },
    "31169887441|1|Scheduled check-agent signal collector|3|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6b6b0da4b1bf9a286f7ef0f7e1d769992bb3cd5e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T10:24:20Z"
    },
    "31173685489|1|Scheduled check-agent signal collector|4|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e07f7ad7850fdf1f27813d8a62623ffa5a20dbdb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T11:21:08Z"
    },
    "31176749879|1|Scheduled check-agent signal collector|4|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "17e666d215e8bfba6813baabd0f4b64d2be9eb37",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-07T12:07:30Z"
    },
    "31183266346|1|Scheduled check-agent signal collector|5|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c0e955a3621048b24bd5ab8bf433b197267216b4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T13:35:02Z"
    },
    "31188781060|1|Scheduled check-agent signal collector|5|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "db72d738026bfcdfc05f53e61ac149256faf16c8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-07T14:41:17Z"
    },
    "31193574214|1|Scheduled check-agent signal collector|5|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "dac8389797715703bc7aed045e50fc4d13ff3a34",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-07T15:38:18Z"
    },
    "31198304664|1|Scheduled check-agent signal collector|6|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "27000760820e75ed0851faff33d523e8d0ac447e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-07T16:37:24Z"
    },
    "31202958263|1|Scheduled check-agent signal collector|6|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7aad028f45037071579222dbf659880de7e21f3f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-07T17:35:29Z"
    },
    "31207308054|1|Scheduled check-agent signal collector|7|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "094173eda996853ce2e705d9280402302ead502e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-07T18:31:42Z"
    },
    "31212434181|1|Scheduled check-agent signal collector|7|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f86315636bcc7b33c3978a71ff0cd3e0a4ee96c5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T19:40:08Z"
    },
    "31215618129|1|Scheduled check-agent signal collector|7|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f66763b0e8856eb00299c37cfea6d6f8aed54a9c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-07T20:23:39Z"
    },
    "31218816969|1|Scheduled check-agent signal collector|8|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ce36b6bac652df73b29b0976ce6d54e4c9238c5b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-07T21:10:23Z"
    },
    "31222406293|1|Scheduled check-agent signal collector|8|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1e8471865d09adb54d3f921db7a29c2a959c11fa",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T22:03:48Z"
    },
    "31225214507|1|Scheduled check-agent signal collector|9|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "57ba68d58cf1a2c00cf3880a2f329c51b6432a46",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-07T22:51:39Z"
    },
    "31227982147|1|Scheduled check-agent signal collector|9|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "82016fbb92aae19e8d01a65d5edc335dd9216671",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-07T23:45:05Z"
    },
    "31230402444|1|Scheduled check-agent signal collector|9|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c70b14d1ebb1d8f405490864505c19dc0372ea84",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T00:33:30Z"
    },
    "31235629957|1|Scheduled check-agent signal collector|10|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "998d2fb0d943fe1cb6f506e3d25b101817b74037",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T02:44:42Z"
    },
    "31238389212|1|Scheduled check-agent signal collector|11|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "717c5b7c68e92979f9917bae43b2c3b335a95a3a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T03:59:01Z"
    },
    "31240955873|1|Scheduled check-agent signal collector|11|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e800a8e46eb327cc50ebdc722c2f3887dd5b80d0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T05:07:29Z"
    },
    "31242716592|1|Scheduled check-agent signal collector|12|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1aefce5a7cb79898f9d7ed23bc72e92b2e2e609c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T05:54:51Z"
    },
    "31245500316|1|Scheduled check-agent signal collector|12|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "62a5a9b202c74f550b4a6e9172a87d6a1a469d11",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T07:09:05Z"
    },
    "31247616628|1|Scheduled check-agent signal collector|12|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "a93fa81eca2dc54e02d9a37aaeeaf4838e2e5d8a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T08:05:25Z"
    },
    "31249453807|1|Scheduled check-agent signal collector|13|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "61fd6021b424d37b24dd9e9cd861d32e0e2b26c6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T08:56:28Z"
    },
    "31251419299|1|Scheduled check-agent signal collector|13|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1cab27fc629dfaf650ce03681525373ae9042aa3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T09:50:07Z"
    },
    "31253480176|1|Scheduled check-agent signal collector|14|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "14727b5d0012243d61dee0ae6782249dbeab7e0c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T10:46:03Z"
    },
    "31254499717|1|Scheduled check-agent signal collector|14|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7c76b6d626fa52f68335d2ded70c32b2791f96b5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T11:14:31Z"
    },
    "31255924042|1|Scheduled check-agent signal collector|14|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "206738c7d04412f057fc0d41043ab63f4fbb3b38",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T11:52:00Z"
    },
    "31258805018|1|Scheduled check-agent signal collector|15|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "df52ea1efa065c73f0b3b2a63501397ff6ec2682",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T13:08:06Z"
    },
    "31261059211|1|Scheduled check-agent signal collector|15|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b1ca21b2a4110db0dfb1e56b356a3b7db6757a08",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-08T14:05:01Z"
    },
    "31262763099|1|Scheduled check-agent signal collector|15|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1aed887fe0534bcc779be0db085ba4671e109f5a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T14:46:28Z"
    },
    "31263915446|1|Scheduled check-agent signal collector|16|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "db93ef7fa21da3d9978782c5f935255b7294b02d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T15:13:50Z"
    },
    "31265639864|1|Scheduled check-agent signal collector|16|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dbf24f728795e96436d1b71eeff1060104a3ba30",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T15:56:17Z"
    },
    "31267816697|1|Scheduled check-agent signal collector|16|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "af715a171f44166fcef67a164c30ded8d6501bb2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T16:48:18Z"
    },
    "31270018504|1|Scheduled check-agent signal collector|17|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2d193de186377adf6acef11fc7233b9b6fa817ca",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T17:41:16Z"
    },
    "31271354692|1|Scheduled check-agent signal collector|17|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "05ff03028ecdc1b5e851dd1cfa043b6418ae1f0f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T18:14:51Z"
    },
    "31273619189|1|Scheduled check-agent signal collector|17|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a6eb2e67fbc6a66e3c3f55387201db57a2554e6d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T19:07:28Z"
    },
    "31275095960|1|Scheduled check-agent signal collector|17|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "0deb9500bc76ec9cbeda0252a80a04578acdfeff",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T19:43:08Z"
    },
    "31276028296|1|Scheduled check-agent signal collector|18|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5a92ebe0ea9a0ea765b546075afda6013607f002",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T20:05:31Z"
    },
    "31277645696|1|Scheduled check-agent signal collector|18|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "25cff8c76205aa6cc439983b0b565481d265de56",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T20:47:12Z"
    },
    "31278824304|1|Scheduled check-agent signal collector|18|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "052a487e17b92cee33e88a8afa2ad13c2b372c7e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-08T21:14:46Z"
    },
    "31280409546|1|Scheduled check-agent signal collector|18|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "33e20f94ee98d5a43055ee248bab4e9bad08a9d0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-08T21:54:15Z"
    },
    "31282259077|1|Scheduled check-agent signal collector|19|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d65fd3e911ea2c8a7f5897fa51ca9ecd4520fe0d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T22:41:38Z"
    },
    "31283356556|1|Scheduled check-agent signal collector|19|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2f7b256a5618cea9c2a14ddb8a8884ee554ddbe2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-08T23:10:35Z"
    },
    "31284935487|1|Scheduled check-agent signal collector|19|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "75d07e7d4e13ae5e3bc67251ffb58e8371ee92cb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-08T23:52:43Z"
    },
    "31290245517|1|Scheduled check-agent signal collector|20|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b6588b80beff375ee083cd1d714afb9031f1410c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T02:24:26Z"
    },
    "31293498008|1|Scheduled check-agent signal collector|21|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "cb48fa2ef20bfa379fe13c65c516696c5145596b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-09T03:57:39Z"
    },
    "31296246199|1|Scheduled check-agent signal collector|22|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bebe9c50fe92d6ee8cf5aa5cb36d76bac40cd3d8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T05:14:42Z"
    },
    "31298117201|1|Scheduled check-agent signal collector|22|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "111bc4310d9ee844387cbb608039fea5bee37052",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T06:06:56Z"
    },
    "31300619648|1|Scheduled check-agent signal collector|22|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "0363b56c4d8c999995bc7003197b5a80ae5641e7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T07:13:02Z"
    },
    "31302704631|1|Scheduled check-agent signal collector|23|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0f631e0bebf00f8e4b9a87e72987b8639b73f835",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T08:06:36Z"
    },
    "31304813907|1|Scheduled check-agent signal collector|23|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c284d1c27a3a079d08dbf21ed9c1cd53bbbf0bc8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T08:59:41Z"
    },
    "31306919417|1|Scheduled check-agent signal collector|24|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "074bdcd954c0fd00d71d69fe81e180ec0c2a2bdd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T09:52:35Z"
    },
    "31309191463|1|Scheduled check-agent signal collector|24|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "a0ab38e18696eeb7c7a92a5cd64dac6b559ea767",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-09T10:48:11Z"
    },
    "31311288250|1|Scheduled check-agent signal collector|24|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bd58fb7a1a23dbf1785256715c0c7fa14b19174b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T11:39:01Z"
    },
    "31312383232|1|Scheduled check-agent signal collector|24|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "47f134a0cefc77363174bb6e0069d0607fda11c6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T12:05:26Z"
    },
    "31315187244|1|Scheduled check-agent signal collector|25|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c741c1f2af348c188b4f571e0eea038dda5f9fa8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-09T13:13:02Z"
    },
    "31317469562|1|Scheduled check-agent signal collector|25|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "77739f2ae7b3becaf7bb516b8e74d30cfea08305",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T14:04:38Z"
    },
    "31319418789|1|Scheduled check-agent signal collector|26|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8dd4b2b6af128980664487948377e598bef552d8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T14:49:22Z"
    },
    "31321765502|1|Scheduled check-agent signal collector|26|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "bf681baae0035dcadeb99bd4932ab6dd2c74f4ee",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-09T15:41:43Z"
    },
    "31323178478|1|Scheduled check-agent signal collector|26|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0d71dab8bcdb35d3254960425246820f970c7886",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T16:13:05Z"
    },
    "31325388133|1|Scheduled check-agent signal collector|27|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b3243b7584565a93cbd7fcef42c5bbe4f609a3eb",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T17:03:31Z"
    },
    "31327107752|1|Scheduled check-agent signal collector|27|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b3eb6444de8ebd1c7bc3e9977a24d66e9fc41483",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T17:45:21Z"
    },
    "31328553887|1|Scheduled check-agent signal collector|27|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5dec06bb97e62566551a2c28ff6dcc6ef760bada",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T18:15:51Z"
    },
    "31330918007|1|Scheduled check-agent signal collector|28|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "258f4a6945fbf478e9ec005ebf0238f8e14ac5fa",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T19:10:27Z"
    },
    "31332869578|1|Scheduled check-agent signal collector|28|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5f9273f0544baae01ac9155614bce062569e9f4e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T19:56:06Z"
    },
    "31335141950|1|Scheduled check-agent signal collector|28|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8bb461ab935a372078d7b61d48e7e57c6e0bc3e5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-09T20:48:04Z"
    },
    "31337561850|1|Scheduled check-agent signal collector|29|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0849d48e49e8c3a1c53b9f83cd4592469bdfe38b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T21:43:44Z"
    },
    "31338791910|1|Scheduled check-agent signal collector|29|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e6e55d63a6c7ce6536c3de51bc2af0324154fdfa",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T22:13:47Z"
    },
    "31340684720|1|Scheduled check-agent signal collector|29|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "15560e7b2bd1d67850d86f934a9a417028b9b4ed",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-09T22:58:03Z"
    },
    "31342514156|1|Scheduled check-agent signal collector|29|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "644bd3d55992a51cff9ac141ca62a38c310c902d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-09T23:42:04Z"
    },
    "31344903030|1|Scheduled check-agent signal collector|30|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4193ab733ebdab53ed4ad396ef6e167704346fb8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T00:38:02Z"
    },
    "31351342273|1|Scheduled check-agent signal collector|31|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "1b5071d6eae7a3844f980b592936a1414d8fff81",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T03:02:19Z"
    },
    "31356630364|1|Scheduled check-agent signal collector|32|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "471f65dea58c6a63c7b49ee76e55d208e236e9b2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T04:48:54Z"
    },
    "31361487422|1|Scheduled check-agent signal collector|32|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bcd13a8ff4c5bc3f080414e884deab0ed3f39f6d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T06:19:17Z"
    },
    "31369010185|1|Scheduled check-agent signal collector|33|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b212d21edd62856067fdf47646694b9f4a6459e7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-10T08:12:38Z"
    },
    "31376793947|1|Scheduled check-agent signal collector|34|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7584e53f50b0bfb0f8f024ae293ba5a123a5b467",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T09:56:03Z"
    },
    "31382835380|1|Scheduled check-agent signal collector|34|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "2c8f0440ecef41a491f934f72357120b8503d203",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T11:17:38Z"
    },
    "31386427902|1|Scheduled check-agent signal collector|35|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a6715afd731a169722783b3045675aeaa8d221f7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T12:06:52Z"
    },
    "31394028192|1|Scheduled check-agent signal collector|35|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "398bf54cb9e4c792cfebfd94a87f3f5d20b2c5f2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T13:40:21Z"
    },
    "31399781428|1|Scheduled check-agent signal collector|36|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "1de2ffa66ae355ab437414d54cebba0bce17e76a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T14:46:53Z"
    },
    "31405028866|1|Scheduled check-agent signal collector|36|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a4258a766b4aa9a841de42110b21c3689e562a42",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T15:43:23Z"
    },
    "31409706310|1|Scheduled check-agent signal collector|37|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3cd320d0798197ed9fe5b2798d742bae0af81c56",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T16:36:18Z"
    },
    "31414983123|1|Scheduled check-agent signal collector|37|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e21009a4325a0a545f90b02abdc369132e4eb429",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-10T17:38:37Z"
    },
    "31419806220|1|Scheduled check-agent signal collector|38|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2f55bc8ef2d5bd6e3e6d4d073e4b821aec3531b3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-10T18:35:42Z"
    },
    "31425447080|1|Scheduled check-agent signal collector|38|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "30b96f24bd725dfd483058d24db03d102bed9436",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-10T19:43:29Z"
    },
    "31428886956|1|Scheduled check-agent signal collector|38|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fd5ec23f6d76fb7935fc975d748fc59de8a807f8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T20:25:19Z"
    },
    "31432727786|1|Scheduled check-agent signal collector|39|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c25506a98e369c4b7854c8727c2308ec68cccfa0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T21:12:57Z"
    },
    "31436768905|1|Scheduled check-agent signal collector|39|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "fadacd9278900a0442069326f96d78f5834cd2fe",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-10T22:05:47Z"
    },
    "31440146242|1|Scheduled check-agent signal collector|39|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f530b755f5ac155373732352578de16a1015326a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-10T22:53:52Z"
    },
    "31443613431|1|Scheduled check-agent signal collector|40|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c7fa815f7d90fc198f88d3b8ffa7f64e9d03c49c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-10T23:47:01Z"
    },
    "31446669686|1|Scheduled check-agent signal collector|40|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "2bae782f5460088ebc9e79d9d33b5da3ae9dcd33",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-11T00:37:49Z"
    },
    "31453762006|1|Scheduled check-agent signal collector|41|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0d767a6d9b78bd377b6accd5c2f5c6ec7b3a8728",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-11T02:54:45Z"
    },
    "31458964999|1|Scheduled check-agent signal collector|42|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "49fe2f5a20b8706052cf3f8dfb004235d2c146c2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-11T04:36:18Z"
    },
    "31462496387|1|Scheduled check-agent signal collector|42|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "37d1f53d021349e847ef4f1f75436e5aa61669b8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T05:42:16Z"
    },
    "31465781339|1|Scheduled check-agent signal collector|43|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "7c0c754d3b2fe620d1fea50308e6431b2d395915",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T06:38:07Z"
    },
    "31471108661|1|Scheduled check-agent signal collector|43|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5224ae3a05ebca4f1ee45566cd07959bdf472279",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T07:58:00Z"
    },
    "31476529865|1|Scheduled check-agent signal collector|44|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "42058caa5cb19628e79d3a92489725974e89f564",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-11T09:12:39Z"
    },
    "31481927574|1|Scheduled check-agent signal collector|44|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bcd1c33bd72d954051633394f295707472eec2f0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T10:23:16Z"
    },
    "31485582406|1|Scheduled check-agent signal collector|45|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f5ddfdad84ebe3b4f5cc056f146b2cbca744c7d3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T11:12:55Z"
    },
    "31489573273|1|Scheduled check-agent signal collector|45|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "848589505d23c96ef9343a58b1f1bf38e9be2b7b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-11T12:06:02Z"
    },
    "31497153732|1|Scheduled check-agent signal collector|46|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fd92bffcef6c4bc7be97a926b4522202139ebca8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T13:48:44Z"
    },
    "31503159001|1|Scheduled check-agent signal collector|46|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "696db5215dfb290c26381228ef4a1b5f131c4e2d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-11T14:44:40Z"
    },
    "31508530319|1|Scheduled check-agent signal collector|47|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5a43105e07ab2b60a75b51767a2b13917453468d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-11T15:43:31Z"
    },
    "31513490957|1|Scheduled check-agent signal collector|47|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e3eae9833bebf25128ded0c618ae832fa9b65f3b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-11T16:39:44Z"
    },
    "31518982193|1|Scheduled check-agent signal collector|47|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c45b33271648471569b4ef3aa33c09d25671fc5f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-11T17:43:35Z"
    },
    "31523721198|1|Scheduled check-agent signal collector|48|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "241f993facb33a0791556e94dea80f0cf11b3772",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-11T18:39:27Z"
    },
    "31529626211|1|Scheduled check-agent signal collector|48|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "52f25badce1e12c5b31e6b82029910d9edfdfa13",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-11T19:47:57Z"
    },
    "31535615536|1|Scheduled check-agent signal collector|49|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "4233402efd117512f50046ed34df34825519b6ed",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-11T21:00:54Z"
    },
    "31540325914|1|Scheduled check-agent signal collector|49|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "3d9da8b4295e163d0e2b483287e4705d5068ef8b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T22:09:00Z"
    },
    "31544496856|1|Scheduled check-agent signal collector|50|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c37f11d0a542578b3532d02111af17c1db8474e4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-11T23:07:07Z"
    },
    "31548165894|1|Scheduled check-agent signal collector|50|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "662d406d88baabf3131c744369a85c3f891700e9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-11T23:53:38Z"
    },
    "31557504889|1|Scheduled check-agent signal collector|51|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "254ce59f1f9756990445ebcbe7feeb539dc113dc",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T02:38:53Z"
    },
    "31563343993|1|Scheduled check-agent signal collector|52|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5689819341351666f20939a843dc45f4f60a81de",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T04:28:25Z"
    },
    "31568689903|1|Scheduled check-agent signal collector|53|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "09847297d0e9593d841e26f83cabfdebdb5bdd18",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T06:05:24Z"
    },
    "31575458025|1|Scheduled check-agent signal collector|54|cerebras|gpt-oss-120b|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "36e2ea0245fcecb4a2ba0d28fc07298897e4fcd8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "provider_failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T07:48:14Z"
    },
    "31582435216|1|Scheduled check-agent signal collector|54|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "41f2a6f99a9bfbda8838892230085a53a16cba4b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T09:20:42Z"
    },
    "31587895237|1|Scheduled check-agent signal collector|55|sambanova|DeepSeek-V3.1|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6c9aecba4365ac78f52ba4394fea86b4b0aac2f7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "DeepSeek-V3.1",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T10:36:35Z"
    },
    "31592260200|1|Scheduled check-agent signal collector|55|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5d11066ba2ea816485ca16d7d7e67ebaf9ff186e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T11:32:32Z"
    },
    "31597025921|1|Scheduled check-agent signal collector|56|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "16a27af8ffb5251fc29ede7dc4461820af4c7833",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T12:34:26Z"
    },
    "31605010124|1|Scheduled check-agent signal collector|56|sambanova|Meta-Llama-3.3-70B-Instruct|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "540087a07e556457852eeaec19b36eb35f8d331c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "ok",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T14:07:32Z"
    },
    "31611003799|1|Scheduled check-agent signal collector|57|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "ae4369e68997cf838dfdaf3ced2cc16c1ef059b4",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T15:53:01Z"
    },
    "31617323623|1|Scheduled check-agent signal collector|57|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bf28a459dd07d64e30e7fce238a3b4a103dfb845",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T16:24:04Z"
    },
    "31622656245|1|Scheduled check-agent signal collector|58|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "9fdd89d8453dc5a8fb5edc349715ecab3ef3b911",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T17:27:31Z"
    },
    "31627708488|1|Scheduled check-agent signal collector|58|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bbd3379ce9246f122e624b2c49229fae55f426e5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T18:27:44Z"
    },
    "31634506448|1|Scheduled check-agent signal collector|59|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5d9d3716550529676d0fb8065dc9e6b1d803d02c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-12T19:49:29Z"
    },
    "31640215523|1|Scheduled check-agent signal collector|59|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "cf47e13323ceaeb4d7ce120293b4002e8df73eb4",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T20:58:07Z"
    },
    "31644810163|1|Scheduled check-agent signal collector|60|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "79b24f0566c09dc85a156ed55ff677df3702376b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-12T21:57:29Z"
    },
    "31648863546|1|Scheduled check-agent signal collector|60|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "a7b160807b993b209cfab6b42d4428747cef96d0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-12T22:55:25Z"
    },
    "31652504848|1|Scheduled check-agent signal collector|60|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "30e69e36ab6034d4a00a34e9277e51dad504ec4b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-12T23:53:47Z"
    },
    "31661521599|1|Scheduled check-agent signal collector|62|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e6c920baeca1cfe0ab7d97ffb6c138416291c9c9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T02:40:45Z"
    },
    "31667262820|1|Scheduled check-agent signal collector|62|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "3a05b460cc007e684b0e50c707d7a3fbc67544a9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T04:31:26Z"
    },
    "31672634459|1|Scheduled check-agent signal collector|63|cerebras|zai-glm-4.7|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "27c97acf0160ebf29063bb2f6c16ba810a0744c1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T06:07:05Z"
    },
    "31679388873|1|Scheduled check-agent signal collector|64|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9bf33fb66e844b45db3d401ade02b9bce2fc7f24",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T07:52:58Z"
    },
    "31686162560|1|Scheduled check-agent signal collector|64|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6ad4fb3df0fcf7a5e1d8b1b51ecafa6085850775",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T09:21:16Z"
    },
    "31691647724|1|Scheduled check-agent signal collector|65|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "02b6c65e3cadd3cfd6b14184c9d8a7d2098708d3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-13T10:34:33Z"
    },
    "31695907728|1|Scheduled check-agent signal collector|65|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "002aa18bc102d8ef66195ac8b56f4ad6767cbff1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T11:32:20Z"
    },
    "31700646957|1|Scheduled check-agent signal collector|66|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "79fda2f3f03511fe4eccd750596df960e098cfaf",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T12:37:12Z"
    },
    "31708601053|1|Scheduled check-agent signal collector|67|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "84acb089e630273fbe89c76194f5ab13f190f394",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T14:09:13Z"
    },
    "31715599336|1|Scheduled check-agent signal collector|67|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1aaaddccaf6f1ddc3dda16f411df7f36e2773c34",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T15:29:18Z"
    },
    "31721585494|1|Scheduled check-agent signal collector|68|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "131c2c9f528e511bac2eba938a1d68ffbaf598f5",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T16:37:37Z"
    },
    "31727175028|1|Scheduled check-agent signal collector|68|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f7894e411ee067cf8e63dcf377dfdfe2e0e9ec8d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-13T17:44:42Z"
    },
    "31731848139|1|Scheduled check-agent signal collector|68|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "56f0e2e74f1a3ab943f4a9067758648ece16e63e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T18:39:46Z"
    },
    "31737433123|1|Scheduled check-agent signal collector|69|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "b15e66f0299da1a154b2b68c89bbc4bf9dfaad68",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T19:48:26Z"
    },
    "31740613072|1|Scheduled check-agent signal collector|69|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e6f58b911bd57ebec4fe22ff75ac9c9a6b8ad9a8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T20:24:04Z"
    },
    "31744571229|1|Scheduled check-agent signal collector|70|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "dcce390cf4105646c7f3b17125ef0df0a34051d7",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-13T21:12:57Z"
    },
    "31748731798|1|Scheduled check-agent signal collector|70|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1e93fb5d340811b86c3416fa4b7b14158572d854",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-13T22:09:28Z"
    },
    "31752819681|1|Scheduled check-agent signal collector|70|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c597d049c3d606b67f5b4f40acde11823a57b256",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-13T23:10:40Z"
    },
    "31756167429|1|Scheduled check-agent signal collector|71|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "092408f696717a1fc2971624ef1f41d4e60c525c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-14T00:06:07Z"
    },
    "31764514153|1|Scheduled check-agent signal collector|72|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "77ad501b6577322879a969bb3a06b337ba65c63e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T02:45:29Z"
    },
    "31770036386|1|Scheduled check-agent signal collector|73|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c0e84de5a4df27677770ca86c4d76a69e36d453d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-14T04:30:20Z"
    },
    "31775084904|1|Scheduled check-agent signal collector|73|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "acf64d6da195311146d348befe7e403af4784ae0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-14T06:05:44Z"
    },
    "31781257591|1|Scheduled check-agent signal collector|74|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ffdcd2041ac0c8c7585c88eee79ad257cf16d31a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T07:47:20Z"
    },
    "31785646221|1|Scheduled check-agent signal collector|75|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "73b10441ac0b5d04ac0d8f8fd33507005635733a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T08:52:10Z"
    },
    "31791319438|1|Scheduled check-agent signal collector|75|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fb7266390430519f210da751db7751418fa3d27b",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T10:13:42Z"
    },
    "31795269236|1|Scheduled check-agent signal collector|76|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9771cf5b0fac924ba9e24ef221e84c7bdd1c85e0",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T11:12:59Z"
    },
    "31798805973|1|Scheduled check-agent signal collector|76|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4455f99553b0a8848945415aff6e3bf0550312d9",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T12:06:31Z"
    },
    "31805461601|1|Scheduled check-agent signal collector|77|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9c4a377fe1a3f9bbd6ae98d5c9fe2e541f42c118",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T13:36:31Z"
    },
    "31810604537|1|Scheduled check-agent signal collector|77|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "614bd5cd82bebcc1a9f8a9bcc82a2ad4886242d1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-14T14:40:22Z"
    },
    "31815211375|1|Scheduled check-agent signal collector|77|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "56eff06812597fe341f814d39a0835c408c71a8b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T15:35:38Z"
    },
    "31819977237|1|Scheduled check-agent signal collector|78|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5445c8e3f043ef6865084918c57964f862936373",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T16:35:23Z"
    },
    "31825026438|1|Scheduled check-agent signal collector|78|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f92fd00eacc754d56db749849737035528535ee4",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-14T17:40:24Z"
    },
    "31829300747|1|Scheduled check-agent signal collector|1|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5e57a63f8d2dd56a4af770fcc067191e1b5dc3f8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-14T18:35:15Z"
    },
    "31834159974|1|Scheduled check-agent signal collector|1|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "160e68402e3760aa8d6c795ed42fd0eaf3bf37ef",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T19:38:49Z"
    },
    "31837124257|1|Scheduled check-agent signal collector|1|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "9a4b5582bd8cbbfaf297e0e867bb3763c0f21310",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T20:16:51Z"
    },
    "31839988994|1|Scheduled check-agent signal collector|2|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "fd8dbf8dcb3dd94f594237c5386c07643ad78b6b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-14T20:54:06Z"
    },
    "31843048018|1|Scheduled check-agent signal collector|2|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "45252f8080611ab4823d3a44b6f83a1a012189cb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-14T21:35:46Z"
    },
    "31844815637|1|Scheduled check-agent signal collector|2|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "704c38988545df89a896ccb08cc3347deb5fdf34",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T22:00:21Z"
    },
    "31847138572|1|Scheduled check-agent signal collector|2|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c43507b5a9a8c64b7fc4506ba9a6493584645525",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T22:35:00Z"
    },
    "31848835835|1|Scheduled check-agent signal collector|3|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "369756be8256284cf3b33c95777d0c9d0648c8ba",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-14T23:01:51Z"
    },
    "31850677113|1|Scheduled check-agent signal collector|3|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "bfd228392f8da0543396cad573e1a8dd8f721bbe",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-14T23:33:40Z"
    },
    "31852307302|1|Scheduled check-agent signal collector|3|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "75de812fe9ca989aa11c1815c8e36f8dcb77dd35",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T00:01:53Z"
    },
    "31857371621|1|Scheduled check-agent signal collector|4|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "b7def75159f3f1dbba256d0920248a57cbb17fb6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T01:46:10Z"
    },
    "31859752306|1|Scheduled check-agent signal collector|4|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "b80caba459465abdfd276d1acb8e1b9c9a9ba793",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T02:39:47Z"
    },
    "31861718413|1|Scheduled check-agent signal collector|4|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "300710a97d504cdadf0bdd746ecba8b5f4a1aa33",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T03:24:47Z"
    },
    "31863417379|1|Scheduled check-agent signal collector|5|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "d488e8675739a449cf0eb3419b5d663f2df98e98",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T04:03:36Z"
    },
    "31865094796|1|Scheduled check-agent signal collector|5|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "3c0b34d083332811a8a55d9b283d4a830de3e6e3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T04:43:07Z"
    },
    "31866009704|1|Scheduled check-agent signal collector|5|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "9b9be3d799c032b45564217bf32a4fceaee45c1f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T05:04:21Z"
    },
    "31867337601|1|Scheduled check-agent signal collector|5|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "63b23676d1a8e5ba1223d007f7ada93a7e7f94eb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T05:36:21Z"
    },
    "31868377851|1|Scheduled check-agent signal collector|6|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "03d24961aadea7c2bc5bcd389df96c16345eadb6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T06:01:26Z"
    },
    "31870555611|1|Scheduled check-agent signal collector|6|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "68168cd1e76acd9930115c3ce8552b759a877a3e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T06:54:00Z"
    },
    "31872450347|1|Scheduled check-agent signal collector|6|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "427115125d8d6aa002f8db9315d96b679dfaf162",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T07:38:41Z"
    },
    "31873386548|1|Scheduled check-agent signal collector|6|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "32df83ebddf9d18391864288e6f11f2659da1cb7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T08:00:44Z"
    },
    "31875065710|1|Scheduled check-agent signal collector|7|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "453554deae1b4309a0ec9249e4f8bf38b02c1881",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T08:41:12Z"
    },
    "31876019184|1|Scheduled check-agent signal collector|7|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|provider_failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5f5ae2cb5dbae09d68aae03a70895ffd4f918422",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "provider_failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T09:04:12Z"
    },
    "31877389842|1|Scheduled check-agent signal collector|7|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1825e0a5f5d0dd483e5ff4c33751e2ee288fa21f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T09:36:15Z"
    },
    "31878395896|1|Scheduled check-agent signal collector|7|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "d71dae6bfbc103b6466d8909d4d99a24cd013e75",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T10:00:21Z"
    },
    "31879828188|1|Scheduled check-agent signal collector|8|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "62c3b95962b108678ba4dbfbe68afe25ee5ac91c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T10:34:23Z"
    },
    "31880928968|1|Scheduled check-agent signal collector|8|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6680ffc2e2f4de95c4a9c588dbea51248bc25e4f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T11:00:33Z"
    },
    "31882195514|1|Scheduled check-agent signal collector|8|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "3f46dc87542f31ed353cc4d32ad0d72ac377c3e5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T11:30:44Z"
    },
    "31883377097|1|Scheduled check-agent signal collector|8|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ad956b4e7fb42ae805339a0497b829c29baaf7f8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T11:58:06Z"
    },
    "31885807369|1|Scheduled check-agent signal collector|9|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "3351e9359abe3813ef8ce893eb2c6966b64efe15",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T12:55:11Z"
    },
    "31887712784|1|Scheduled check-agent signal collector|9|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "aab4dcbe0e41538056cd5fc9f0f8d50b4a2e5acf",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T13:40:20Z"
    },
    "31888706759|1|Scheduled check-agent signal collector|9|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "25822f285958e4f7aece126249cec426d531d734",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T14:00:47Z"
    },
    "31890223261|1|Scheduled check-agent signal collector|9|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "b5ffa6ddbe4f8bea9ec6e14d5e7a82da6b2c4038",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T14:33:43Z"
    },
    "31891490505|1|Scheduled check-agent signal collector|9|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "eeaf7760bebc8dcfb11ba0f2862dd9ac4b467dc7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T15:00:52Z"
    },
    "31892905130|1|Scheduled check-agent signal collector|10|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "baa4070e77d28f7827e418bb889aa5734c58c6ef",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T15:31:07Z"
    },
    "31894207823|1|Scheduled check-agent signal collector|10|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "973c5320336547e969be0c01c34d63eadbee91a8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T16:01:46Z"
    },
    "31895943400|1|Scheduled check-agent signal collector|10|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "61827d44ace1a4e95b886b599be62de4d8a0f52c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T16:36:23Z"
    },
    "31897140483|1|Scheduled check-agent signal collector|10|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "3e4483d4bc7d8596fb647e67d79950e7edb0d6a7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T17:02:07Z"
    },
    "31898503318|1|Scheduled check-agent signal collector|11|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4cfafa16da5e5f04a92650fa6cfbac49ea0391f8",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T17:31:05Z"
    },
    "31899814298|1|Scheduled check-agent signal collector|11|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "96578579a2e7c822e83a820080e421927ab96f28",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T17:58:41Z"
    },
    "31901870870|1|Scheduled check-agent signal collector|11|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ae7841d41cc1b0e3b0c89b2a042ca810d3155266",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T18:43:28Z"
    },
    "31902947965|1|Scheduled check-agent signal collector|11|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0a0715b97cfc8c06650d203ac72badacb4b5904a",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T19:06:22Z"
    },
    "31904118799|1|Scheduled check-agent signal collector|11|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "d261b9dba28a7d134546290aa8fa081a3accbb54",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T19:31:17Z"
    },
    "31905378238|1|Scheduled check-agent signal collector|12|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ce8c76754c8622ba83982783f186f48b6aa2f627",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T19:58:22Z"
    },
    "31907039827|1|Scheduled check-agent signal collector|12|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5a17a9cf02eb70efde2eee70e62ae47bc7bcb06f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T20:35:16Z"
    },
    "31908232410|1|Scheduled check-agent signal collector|12|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "c1f54e007200e04195702517fa28c474938e54f0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-15T21:00:56Z"
    },
    "31909642372|1|Scheduled check-agent signal collector|12|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "dfa404c046a0bb68844e74d760e2794a4dab7f43",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T21:31:25Z"
    },
    "31910872055|1|Scheduled check-agent signal collector|12|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "e72d474367650cfb76328b416aa11a9ded2b544c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T21:58:27Z"
    },
    "31912431256|1|Scheduled check-agent signal collector|13|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "35087ad6bbf2f41ef0568c41a8256563604fff05",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T22:33:43Z"
    },
    "31913565070|1|Scheduled check-agent signal collector|13|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "39ae2f017a21b16ecc174e01a7972f250821fb2e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-15T23:00:21Z"
    },
    "31914865133|1|Scheduled check-agent signal collector|13|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8fbb20896aeff0414e1264b900880be780d247f2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-15T23:30:11Z"
    },
    "31916052250|1|Scheduled check-agent signal collector|13|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "0a86bdc91634f945df61b80759d57f0babfd6de3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-15T23:58:17Z"
    },
    "31920590419|1|Scheduled check-agent signal collector|14|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "487e80bd224acfff8693ba073ce12384af861bb1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T01:53:52Z"
    },
    "31923546326|1|Scheduled check-agent signal collector|15|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6bd52a907e81c1187db7180d57a54223955e13f5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T03:09:27Z"
    },
    "31925833488|1|Scheduled check-agent signal collector|15|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "daa44fa02694964c2bbbe426e2f971cc4ef0faca",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-16T04:06:53Z"
    },
    "31927467192|1|Scheduled check-agent signal collector|15|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6d48eb672b2308cb42b8be992d38b5e45a25ab75",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T04:48:09Z"
    },
    "31929446312|1|Scheduled check-agent signal collector|16|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "b5b6e1d0aa58909684d60437581215ca0ff46368",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T05:38:12Z"
    },
    "31930424359|1|Scheduled check-agent signal collector|16|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "48dc738e529125c4509f3c71968acb4240123e33",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T06:04:23Z"
    },
    "31932559854|1|Scheduled check-agent signal collector|16|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "68888efdbcb17a6495bff3cc7515171f9d244eda",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T06:55:15Z"
    },
    "31934423661|1|Scheduled check-agent signal collector|17|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "6a8a67f559a86775f513dd8e3b2f1e0f70dbde86",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T07:39:50Z"
    },
    "31935401043|1|Scheduled check-agent signal collector|17|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "735fb891924b36cf0412b9842f290c056e2670a6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T08:02:09Z"
    },
    "31937095287|1|Scheduled check-agent signal collector|17|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "92f088f34cef10bffad85535e23474d96e72f2b1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-16T08:42:12Z"
    },
    "31938060098|1|Scheduled check-agent signal collector|17|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4e36a848d728cd801252feb6715c47d089419875",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T09:04:38Z"
    },
    "31939510662|1|Scheduled check-agent signal collector|17|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "86324c39fdad69de33e1c8b4faa2514498b0ac87",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T09:37:30Z"
    },
    "31940551027|1|Scheduled check-agent signal collector|18|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a86605e75cc6e6a9baefe0c22a1cea32c5708c29",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T10:01:20Z"
    },
    "31942014388|1|Scheduled check-agent signal collector|18|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2b5d401fe1f197d0ff76a2ccb22626036ec6aba2",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T10:36:30Z"
    },
    "31943162912|1|Scheduled check-agent signal collector|18|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5014a72387584cafa7b62b9cb8e2b83a1109a2ec",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-16T11:00:56Z"
    },
    "31944474855|1|Scheduled check-agent signal collector|18|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "07a5e57ef0bb545733da7333511210087a8bc95f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T11:30:17Z"
    },
    "31945774819|1|Scheduled check-agent signal collector|18|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "80dcbce49f34c7bca4f029b9590e725e1b9a3752",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T11:58:46Z"
    },
    "31948415620|1|Scheduled check-agent signal collector|19|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "802bcde1488e986ba32783a34e73624709f54443",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T12:58:20Z"
    },
    "31950416603|1|Scheduled check-agent signal collector|19|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a4d97f5f96d17883c501fb69704e591c4933c6fd",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T13:39:28Z"
    },
    "31951461072|1|Scheduled check-agent signal collector|19|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "4687e4529954220a49e43579778fa7434b447fa1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T14:01:13Z"
    },
    "31953062232|1|Scheduled check-agent signal collector|20|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "5bacffd9e8e90f2c0fb4c0b4c3dbc0ed8d2ae016",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T14:34:12Z"
    },
    "31954344976|1|Scheduled check-agent signal collector|20|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "035e1835ac5c3ddc1e18ed27b833864aa5098c45",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T15:00:43Z"
    },
    "31955907145|1|Scheduled check-agent signal collector|20|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "08443028be8c75e71c34db4751df1ad682bdd338",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-16T15:32:20Z"
    },
    "31957243347|1|Scheduled check-agent signal collector|20|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "f5844fb6797b29ffac0007458d3e27993a7b9af2",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T15:59:09Z"
    },
    "31959114740|1|Scheduled check-agent signal collector|20|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "eb5794695b474837b52194482a61afe8842004ac",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T16:37:19Z"
    },
    "31960360761|1|Scheduled check-agent signal collector|21|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "30fefeda63d806a768868405bb8ab77b672ba7c3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T17:02:11Z"
    },
    "31961746424|1|Scheduled check-agent signal collector|21|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "371d3d9c8edb5329c22710eb548efef3d5ceef9a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T17:32:17Z"
    },
    "31963133207|1|Scheduled check-agent signal collector|21|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9cb462d8f37deac6101bf1efd4e6094535f4d128",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-16T17:57:41Z"
    },
    "31965351344|1|Scheduled check-agent signal collector|21|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "a6c1533d74bf75360fee952086e3b2fc9f2ea751",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T18:42:19Z"
    },
    "31966463327|1|Scheduled check-agent signal collector|21|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "10a45430ba191fc2bdbe09a519e1699f4d3a2697",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T19:04:32Z"
    },
    "31967709321|1|Scheduled check-agent signal collector|22|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "ad8bd7eaa84febeb7e8f852bce6b1cdcae508b13",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T19:29:35Z"
    },
    "31969074918|1|Scheduled check-agent signal collector|22|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6b9cdca8c365983d4ca662c9f7fb25c7294e51f1",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T19:57:28Z"
    },
    "31970879158|1|Scheduled check-agent signal collector|22|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5c828bda75284b1f374af9e478ac4f754e82d8f3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T20:33:59Z"
    },
    "31972139503|1|Scheduled check-agent signal collector|22|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "679d00d1f3d9d716f4bef786594a3d24dd824425",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T20:59:43Z"
    },
    "31973680717|1|Scheduled check-agent signal collector|23|cerebras|gpt-oss-120b|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "d8a94399090048bb0afac9e2d688608b706e125e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "rejected",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T21:30:45Z"
    },
    "31974979642|1|Scheduled check-agent signal collector|23|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "e069040f2de0c4e62359b40501ba66eb13c1030b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-16T21:57:45Z"
    },
    "31976605774|1|Scheduled check-agent signal collector|23|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "0333b935338d882e5eafdbea1a63cd2682e56e41",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-16T22:32:56Z"
    },
    "31977819389|1|Scheduled check-agent signal collector|23|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "25ef0f88fd5979f84fa8bc9cc89787ad4e252d06",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T22:59:11Z"
    },
    "31979290321|1|Scheduled check-agent signal collector|23|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f681a1f92c0ebd6890bbdbcb2ab3284147142b29",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-16T23:30:19Z"
    },
    "31980573458|1|Scheduled check-agent signal collector|24|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6f39e6f4328f02a439a28c64750827682e7ecc9d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-16T23:57:51Z"
    },
    "31986182624|1|Scheduled check-agent signal collector|24|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f2abbedb7ecef0cb11e2962a7607b3511790aff8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T01:51:45Z"
    },
    "31990175807|1|Scheduled check-agent signal collector|25|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e954d5cc1df9dd9fcb0f64aad4faea716e2c48b3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-17T03:09:19Z"
    },
    "31993483305|1|Scheduled check-agent signal collector|25|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "96911e50cda2da41f831f9b18118f33f09e5bee4",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T04:10:08Z"
    },
    "31996647221|1|Scheduled check-agent signal collector|26|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "1797c95c1c04dc41a545262cdb7167236247c3d8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T05:05:43Z"
    },
    "31999114080|1|Scheduled check-agent signal collector|26|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "81842d1763740a90712a9ddd9986c0af123d1ad3",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T05:47:29Z"
    },
    "32001413231|1|Scheduled check-agent signal collector|26|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "c905ab15a4516cfa99da4e0252bec197f9db5aac",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T06:23:17Z"
    },
    "32006119756|1|Scheduled check-agent signal collector|27|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "5db668b36609cf43687d93c513d7c253c2be061d",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T07:32:31Z"
    },
    "32010261202|1|Scheduled check-agent signal collector|27|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "e66aeca1d670740c58be7421daae8fca8bb52395",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T08:25:35Z"
    },
    "32013747312|1|Scheduled check-agent signal collector|28|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "6506587f3685238aa4d150bbcc6c96f33999b830",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T09:09:31Z"
    },
    "32018292136|1|Scheduled check-agent signal collector|28|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "a4c299a43f770f52bdf8fd82cc123d81bfeaa9c6",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T10:05:14Z"
    },
    "32021646176|1|Scheduled check-agent signal collector|28|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "fefe682669ae2e8fd05889af423dfb5c3d8e534c",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T10:45:46Z"
    },
    "32023650181|1|Scheduled check-agent signal collector|28|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "06ef239abf7e55d1479deabbf8d5abbfe839a6e3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T11:10:58Z"
    },
    "32026648296|1|Scheduled check-agent signal collector|29|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f4e1529cd5495f5320a4c6bfa67fb7f40ebbdfd0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T11:48:12Z"
    },
    "32032856427|1|Scheduled check-agent signal collector|29|cerebras|zai-glm-4.7|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "c4d09a5bfee4d8c7b220de5fd552e28f15114006",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "zai-glm-4.7",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T13:02:24Z"
    },
    "32036759840|1|Scheduled check-agent signal collector|30|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4703c3b68dba4cce51d3883123131b088b1e318f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T13:49:15Z"
    },
    "32039720142|1|Scheduled check-agent signal collector|30|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "7d4891431faef03fd1eb26b7de61f34aa696657f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T14:40:27Z"
    },
    "32041108348|1|Scheduled check-agent signal collector|30|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "ce7380441e43b1d9798a19e473856b3d997b52c9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-17T15:04:18Z"
    },
    "32042770314|1|Scheduled check-agent signal collector|30|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "e6d6d3fca340be9d38c6fd169bba839dbc61c042",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T15:35:43Z"
    },
    "32044059963|1|Scheduled check-agent signal collector|30|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "9371c3b546c232c02ff09c49ce204734ee6a0054",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T16:01:06Z"
    },
    "32046588894|1|Scheduled check-agent signal collector|31|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "218c97c5da590ea27c80668920590b6ca79c47f9",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T16:39:44Z"
    },
    "32048932046|1|Scheduled check-agent signal collector|31|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "0af92fe32d03a743481115d3357fb3cb127cf016",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-17T17:08:18Z"
    },
    "32052256929|1|Scheduled check-agent signal collector|31|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "dcca16b527de53d65614e14b75c3a4fab7b2cb50",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T17:52:54Z"
    },
    "32057250947|1|Scheduled check-agent signal collector|32|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "385121f0b2bf3bbc32b475868870b6ac4f4fbbb8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T18:53:47Z"
    },
    "32061209264|1|Scheduled check-agent signal collector|32|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "e699c1d64fd3901f75ae8ee29919368d0365f3f0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-17T19:36:34Z"
    },
    "32063540140|1|Scheduled check-agent signal collector|32|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "ffc64de039fa71fea8eddb670f773eccd40547e8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T20:01:47Z"
    },
    "32066810555|1|Scheduled check-agent signal collector|32|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "01b076299f02910ff798e4d4a4336d9a7037591c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T20:38:13Z"
    },
    "32069107950|1|Scheduled check-agent signal collector|33|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "ef5c4c7ee0dc5e057ad3d549a89726f7b21bcb52",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-17T21:04:11Z"
    },
    "32071916877|1|Scheduled check-agent signal collector|33|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "588d53be0630f8e6a68aa7240b23ee395380168b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T21:37:02Z"
    },
    "32073984806|1|Scheduled check-agent signal collector|33|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "7fb8177321f2a786c48467e76a6415a9f5c03b7a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-17T22:01:25Z"
    },
    "32076648251|1|Scheduled check-agent signal collector|33|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "d4f0afe0839c37d42736311c663973e8ba3cc42c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T22:35:31Z"
    },
    "32078609254|1|Scheduled check-agent signal collector|33|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "dbce81f771d15e0abd1fb60f0522db5eaebbdff7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-17T23:01:33Z"
    },
    "32080812233|1|Scheduled check-agent signal collector|34|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "93954d19280c3ecee9facecdb451dbfd93fbea9b",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-17T23:32:23Z"
    },
    "32082760468|1|Scheduled check-agent signal collector|34|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "35650a14e62a73c7a7a43a3fa747148c88901707",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T00:01:41Z"
    },
    "32089409475|1|Scheduled check-agent signal collector|35|cerebras|gpt-oss-120b|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "8f3e515381629fec71374f13574bf29c71fedd77",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gpt-oss-120b",
      "overall_status": "ok",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T01:46:58Z"
    },
    "32092836139|1|Scheduled check-agent signal collector|35|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "7ba58e1f937a1f40a6d48e5ff7fac8f0413a15ac",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T02:43:56Z"
    },
    "32095627830|1|Scheduled check-agent signal collector|35|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "1b04dc7cecbf40a9a2aff573949cc746a882357a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T03:29:28Z"
    },
    "32098739402|1|Scheduled check-agent signal collector|36|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5c9b59968ae95c412e1c537e02b98f4c5e1152a0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T04:20:21Z"
    },
    "32101201674|1|Scheduled check-agent signal collector|36|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "92c1153846112321eb5b66dd5f9c73fc1c6fc6f3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T05:00:47Z"
    },
    "32103688938|1|Scheduled check-agent signal collector|36|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "4670e6847b1f4ec217d5fe5e4fad973809d2a748",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T05:39:38Z"
    },
    "32105279995|1|Scheduled check-agent signal collector|36|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "3e4b6caa3e5c5bfce6eac4048db7766ac38e4ce5",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T06:03:28Z"
    },
    "32109348669|1|Scheduled check-agent signal collector|37|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "1981d4ee850493c8848707e76abe1e68bf156d3f",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T07:01:40Z"
    },
    "32113175602|1|Scheduled check-agent signal collector|37|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "765dc37249b543cdca37ac9e2a05823770dec611",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T07:48:38Z"
    },
    "32118346843|1|Scheduled check-agent signal collector|38|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "757d918eb6f1e4549b8f74c987baac64f4d6032e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T08:49:57Z"
    },
    "32123124481|1|Scheduled check-agent signal collector|38|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "05acd5148ddc0a209b90663b644a1aca80428878",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T09:44:40Z"
    },
    "32125463007|1|Scheduled check-agent signal collector|38|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6a5369cd105fe2e5ff78fc7d261aecbc585f1da0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T10:11:21Z"
    },
    "32128980566|1|Scheduled check-agent signal collector|39|cerebras|gpt-oss-120b|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "2b29a53c3ffcd73a3197fe2883ce0f9b6467e68a",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T10:53:44Z"
    },
    "32132409701|1|Scheduled check-agent signal collector|39|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "2c1cf2226f7530811bfb571f7f60fc2407fdd7b4",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T11:36:27Z"
    },
    "32134688279|1|Scheduled check-agent signal collector|39|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "565e47debecb2fef7f8bd1186e3c7f2f4508fa63",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T12:02:27Z"
    },
    "32140170605|1|Scheduled check-agent signal collector|39|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "0ec0143bed018dd5ce51b9246429d84c68e12ed1",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T13:03:54Z"
    },
    "32144930819|1|Scheduled check-agent signal collector|40|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "d7cab130142c7535e0ce19941e0554273bc6d081",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T13:54:38Z"
    },
    "32150384504|1|Scheduled check-agent signal collector|40|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5624be3eabb48637c6ed84320985f5c0067aea9c",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T14:46:58Z"
    },
    "32153361466|1|Scheduled check-agent signal collector|40|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "0a819d554d0a4276ae7a7642940c484da1c24a06",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T15:16:03Z"
    },
    "32157269059|1|Scheduled check-agent signal collector|41|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "00e0aa59c2ddcc86a875b12411f15fd6726ceb1f",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T15:55:40Z"
    },
    "32161869349|1|Scheduled check-agent signal collector|41|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "644fd40420557c543c171624f2efae61dca9db4e",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T16:45:16Z"
    },
    "32164287669|1|Scheduled check-agent signal collector|41|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6860da28c752b49216b0d4a0ebe835015b3d5432",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T17:12:03Z"
    },
    "32167794955|1|Scheduled check-agent signal collector|42|cerebras|gpt-oss-120b|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "230cd524622cb220321237da13f0efc3311cd7b0",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T17:51:38Z"
    },
    "32173431354|1|Scheduled check-agent signal collector|42|gemini|gemini-3.1-flash-lite|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "96c3a2b8c7707ae31f58baf449c2b0d340fd3298",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "ok",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T18:54:05Z"
    },
    "32177391735|1|Scheduled check-agent signal collector|42|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "004e93592f95a047c500a68653d3950aa4faad13",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T19:35:16Z"
    },
    "32179675634|1|Scheduled check-agent signal collector|42|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "30e3f3dde8d303126347ab4a2c0df45311644d6e",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T19:59:50Z"
    },
    "32183050336|1|Scheduled check-agent signal collector|43|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "6c8d6f820993df24c4690b9cee7781c25bcdc982",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T20:35:48Z"
    },
    "32185535316|1|Scheduled check-agent signal collector|43|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "b47f80d4a76bc4aed0955a10bcb05b7f64c1cfd6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "rejected",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-18T21:05:06Z"
    },
    "32188345701|1|Scheduled check-agent signal collector|43|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "3981c33e853c4df02352226fd14770fcca276764",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T21:34:03Z"
    },
    "32190546390|1|Scheduled check-agent signal collector|43|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "43662ec8d8942944f4e87ea3ea819b5f99814cf3",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T22:00:05Z"
    },
    "32193433660|1|Scheduled check-agent signal collector|44|cerebras|gpt-oss-120b|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "50e7f02bb67de04d5c6be12ee5cb48c9f7bb59f7",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T22:36:20Z"
    },
    "32195392244|1|Scheduled check-agent signal collector|44|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "ae53bfd75c7525fbe42b3c832c24175945e47757",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-18T23:02:15Z"
    },
    "32197551879|1|Scheduled check-agent signal collector|44|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9ad1fab3027883ec6ada02ef4d5b9bcfd13505a8",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-18T23:32:27Z"
    },
    "32199437257|1|Scheduled check-agent signal collector|44|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5bfcd8f59822c17ff858d140143fe5905a58bd85",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-18T23:59:42Z"
    },
    "32206234791|1|Scheduled check-agent signal collector|45|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "17c9b86b4e2e27fe330d88acd0cf9b5132a1cd2d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-19T01:48:49Z"
    },
    "32210970973|1|Scheduled check-agent signal collector|46|cerebras|gpt-oss-120b|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "5348739a45af2be074a7674ee51dbaf92ccc2ee6",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-19T03:07:17Z"
    },
    "32213915572|1|Scheduled check-agent signal collector|46|openrouter|nvidia/nemotron-3-ultra-550b-a55b:free|ok|ok|ok": {
      "check_status": "ok",
      "commit_sha": "4a31425849128fa7942dbba3d6388f8071b2cd07",
      "event_name": "schedule",
      "issue_status": "ok",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "overall_status": "ok",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-19T03:57:23Z"
    },
    "32216989766|1|Scheduled check-agent signal collector|46|sambanova|Meta-Llama-3.3-70B-Instruct|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "51f1ad4441283d1f385dc0596da794cdf71dbe8d",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-19T04:47:14Z"
    },
    "32218782793|1|Scheduled check-agent signal collector|46|openrouter|poolside/laguna-m.1:free|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "67d16b5aca899047770c25419ce0db5bec79da84",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "poolside/laguna-m.1:free",
      "overall_status": "failed",
      "provider": "openrouter",
      "timestamp_utc": "2026-08-19T05:16:30Z"
    },
    "32221117335|1|Scheduled check-agent signal collector|47|sambanova|DeepSeek-V3.1|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "f4cab5b06a0ce2d94d8ed0b7e671b34fd2b3e7eb",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "DeepSeek-V3.1",
      "overall_status": "failed",
      "provider": "sambanova",
      "timestamp_utc": "2026-08-19T05:53:42Z"
    },
    "32225830059|1|Scheduled check-agent signal collector|47|cerebras|zai-glm-4.7|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "fd30e1793b33505342fb70faa173d2737bd00030",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "zai-glm-4.7",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-19T07:00:49Z"
    },
    "32229555497|1|Scheduled check-agent signal collector|48|cerebras|gpt-oss-120b|failed|provider_failed|skipped": {
      "check_status": "provider_failed",
      "commit_sha": "89014fe34bc1f6dd9d2ac981e135f40d3d2b1f37",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gpt-oss-120b",
      "overall_status": "failed",
      "provider": "cerebras",
      "timestamp_utc": "2026-08-19T07:49:14Z"
    },
    "32234528105|1|Scheduled check-agent signal collector|48|gemini|gemini-3.1-flash-lite|rejected|rejected|skipped": {
      "check_status": "rejected",
      "commit_sha": "9deb5cd8bbb04e492d1b08350a1d90256ae28b08",
      "event_name": "schedule",
      "issue_status": "skipped",
      "model": "gemini-3.1-flash-lite",
      "overall_status": "rejected",
      "provider": "gemini",
      "timestamp_utc": "2026-08-19T08:50:28Z"
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
