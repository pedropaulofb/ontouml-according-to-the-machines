# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page presents cumulative execution statistics and the current queue snapshot for the scheduled Phase 2 check-agent signal collector.

The tables are derived from canonical machine-readable statistics state, deterministic queue state, validated terminal events, and provider quota observations.

The current desired universe is 39 canonical pages × 2 LLM check agents × 25 configured provider-model slots = 1,950 tasks. Historical obsolete and retired identities remain stored, so total records may be higher.

Statistics collection started on: `2026-08-28T08:14:33Z`

Counts shown on this page only include executions recorded since that start time.

Rows retained in the current statistics state but outside the configured, non-retired registry are shown as `inactive`.

Last generated: `2026-09-06T19:34:14Z`

## Queue snapshot

| Queue state | Tasks |
|---|---:|
| `desired_task_count` | 1950 |
| `pending` | 1253 |
| `leased` | 0 |
| `completed` | 616 |
| `retry_due` | 0 |
| `quota_deferred` | 7 |
| `temporarily_unavailable` | 2 |
| `policy_blocked` | 0 |
| `execution_configuration_blocked` | 0 |
| `rejection_blocked` | 71 |
| `ambiguous_attempt_blocked` | 1 |
| `retired` | 540 |
| `obsolete` | 3683 |

## Provider–model outcomes

| Provider | Model | Status | Configuration | Execution | Lifecycle | Called | Provider attempts | Valid | Zero-signal valid | Valid with signals | Validator rejections | Provider failures | Quota deferrals | Policy blocks | Execution-config blocks | Temporarily unavailable | Runner failures |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | `active` | `configured` | `eligible` | `stable` | 19 | 20 | 8 | 0 | 8 | 9 | 2 | 1 | 0 | 0 | 1 | 0 |
| `gemini` | `gemini-2.5-flash-lite` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-2.5-pro` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3-flash-preview` | `active` | `configured` | `eligible` | `preview` | 2 | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.1-flash-lite` | `active` | `configured` | `eligible` | `stable` | 2 | 2 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.5-flash` | `active` | `configured` | `temporarily_unavailable` | `stable` | 89 | 93 | 65 | 31 | 34 | 12 | 12 | 11 | 0 | 0 | 4 | 0 |
| `gemini` | `gemini-3.5-flash-lite` | `active` | `configured` | `eligible` | `stable` | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.6-flash` | `active` | `configured` | `eligible` | `stable` | 48 | 56 | 39 | 20 | 19 | 1 | 8 | 2 | 0 | 0 | 8 | 0 |
| `gemini` | `gemini-3.7-flash` | `active` | `configured` | `temporarily_unavailable` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `groq` | `openai/gpt-oss-120b` | `active` | `configured` | `blocked_execution_configuration` | `production` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `groq` | `openai/gpt-oss-20b` | `active` | `configured` | `blocked_execution_configuration` | `production` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `groq` | `qwen/qwen3.6-27b` | `active` | `configured` | `blocked_execution_configuration` | `preview` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 52 | 52 | 0 | 0 | 0 | 0 | 52 | 52 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-31b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | `inactive` | `retired` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | `active` | `configured` | `blocked_execution_configuration` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | `configured` | `temporarily_unavailable` | `free-variant` | 53 | 105 | 0 | 0 | 0 | 0 | 53 | 0 | 0 | 0 | 53 | 0 |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `openai/gpt-oss-20b:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-s-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-xs-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.1` | `active` | `configured` | `eligible` | `production` | 52 | 52 | 0 | 0 | 0 | 0 | 52 | 52 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.2` | `active` | `configured` | `eligible` | `preview` | 52 | 52 | 0 | 0 | 0 | 0 | 52 | 52 | 0 | 0 | 0 | 0 |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | `configured` | `temporarily_unavailable` | `production` | 52 | 53 | 0 | 0 | 0 | 0 | 52 | 52 | 0 | 0 | 1 | 0 |
| `sambanova` | `MiniMax-M2.7` | `active` | `configured` | `eligible` | `production` | 82 | 83 | 23 | 14 | 9 | 39 | 20 | 20 | 0 | 0 | 1 | 0 |
| `sambanova` | `gemma-4-31B-it` | `active` | `configured` | `eligible` | `preview` | 62 | 63 | 37 | 12 | 25 | 6 | 19 | 19 | 0 | 0 | 1 | 0 |
| `sambanova` | `gpt-oss-120b` | `active` | `configured` | `temporarily_unavailable` | `production` | 52 | 55 | 0 | 0 | 0 | 0 | 52 | 52 | 0 | 0 | 3 | 0 |

## Current slot progress

| Provider | Model | Completed | Desired | Completion | Oldest pending | Last success | Last attempt | Last quota observation |
|---|---|---:|---:|---:|---|---|---|---|
| `gemini` | `gemini-2.5-flash` | 68 | 78 | 87.18% |  | `2026-09-02T15:10:51Z` | `2026-09-02T15:18:32Z` | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-2.5-flash-lite` | 0 | 0 | 0.00% |  |  |  | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-2.5-pro` | 0 | 0 | 0.00% |  |  |  | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-3-flash-preview` | 77 | 78 | 98.72% |  | `2026-09-02T15:18:39Z` | `2026-09-02T15:18:39Z` | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-3.1-flash-lite` | 71 | 78 | 91.03% |  | `2026-09-02T15:10:49Z` | `2026-09-02T15:10:49Z` | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-3.5-flash` | 76 | 78 | 97.44% |  | `2026-09-05T12:54:18Z` | `2026-09-05T12:54:18Z` | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-3.5-flash-lite` | 77 | 78 | 98.72% |  | `2026-09-02T15:18:28Z` | `2026-09-02T15:18:28Z` | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-3.6-flash` | 78 | 78 | 100.00% |  | `2026-09-04T11:15:59Z` | `2026-09-04T11:15:59Z` | `2026-09-06T18:19:29Z` |
| `gemini` | `gemini-3.7-flash` | 36 | 78 | 46.15% | 19d 7h |  |  | `2026-09-06T18:19:29Z` |
| `groq` | `openai/gpt-oss-120b` | 7 | 78 | 8.97% | 20d 19h |  |  | `2026-08-24T20:36:14Z` |
| `groq` | `openai/gpt-oss-20b` | 6 | 78 | 7.69% | 20d 19h |  |  | `2026-08-24T20:36:14Z` |
| `groq` | `qwen/qwen3.6-27b` | 7 | 78 | 8.97% | 20d 19h |  |  | `2026-08-24T20:36:14Z` |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | 1 | 78 | 1.28% | 20d 19h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `google/gemma-4-31b-it:free` | 1 | 78 | 1.28% | 20d 19h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | 0 | 0 | 0.00% |  |  |  | `2026-09-06T19:33:24Z` |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | 0 | 78 | 0.00% | 18d 3h |  |  | `2026-09-06T19:33:24Z` |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | 78 | 0.00% | 18d 3h |  | `2026-09-06T19:33:20Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | 1 | 78 | 1.28% | 18d 10h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | 0 | 78 | 0.00% | 20d 19h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `openai/gpt-oss-20b:free` | 1 | 78 | 1.28% | 20d 19h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `poolside/laguna-s-2.1:free` | 1 | 78 | 1.28% | 20d 19h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `openrouter` | `poolside/laguna-xs-2.1:free` | 1 | 78 | 1.28% | 20d 19h |  | `2026-09-06T19:33:24Z` | `2026-09-06T19:33:24Z` |
| `sambanova` | `DeepSeek-V3.1` | 0 | 78 | 0.00% | 20d 19h |  | `2026-09-06T19:33:12Z` | `2026-09-06T19:33:11Z` |
| `sambanova` | `DeepSeek-V3.2` | 0 | 78 | 0.00% | 20d 19h |  | `2026-09-06T19:33:12Z` | `2026-09-06T19:33:11Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | 0 | 78 | 0.00% | 20d 19h |  | `2026-09-06T19:33:12Z` | `2026-09-06T19:33:11Z` |
| `sambanova` | `MiniMax-M2.7` | 33 | 78 | 42.31% |  | `2026-09-02T18:51:11Z` | `2026-09-02T18:52:29Z` | `2026-09-06T19:33:11Z` |
| `sambanova` | `gemma-4-31B-it` | 74 | 78 | 94.87% |  | `2026-09-02T15:19:15Z` | `2026-09-02T18:52:39Z` | `2026-09-06T19:33:11Z` |
| `sambanova` | `gpt-oss-120b` | 0 | 78 | 0.00% | 20d 19h |  | `2026-09-06T19:33:11Z` | `2026-09-06T19:33:11Z` |

## Token observations

| Provider | Model | Input tokens | Output tokens | Reasoning tokens | Cached tokens |
|---|---|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | 78311 | 9703 | `unknown` | 8166 |
| `gemini` | `gemini-2.5-flash-lite` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-2.5-pro` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3-flash-preview` | 7425 | 798 | `unknown` | `unknown` |
| `gemini` | `gemini-3.1-flash-lite` | 7429 | 653 | `unknown` | `unknown` |
| `gemini` | `gemini-3.5-flash` | 330858 | 28893 | 73339 | `unknown` |
| `gemini` | `gemini-3.5-flash-lite` | 7429 | 498 | `unknown` | `unknown` |
| `gemini` | `gemini-3.6-flash` | 198183 | 14054 | 8443 | `unknown` |
| `gemini` | `gemini-3.7-flash` | `unknown` | `unknown` | `unknown` | `unknown` |
| `groq` | `openai/gpt-oss-120b` | `unknown` | `unknown` | `unknown` | `unknown` |
| `groq` | `openai/gpt-oss-20b` | `unknown` | `unknown` | `unknown` | `unknown` |
| `groq` | `qwen/qwen3.6-27b` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `google/gemma-4-31b-it:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `openai/gpt-oss-20b:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `poolside/laguna-s-2.1:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `poolside/laguna-xs-2.1:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `DeepSeek-V3.1` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `DeepSeek-V3.2` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `MiniMax-M2.7` | 278768 | 128517 | 114724 | 0 |
| `sambanova` | `gemma-4-31B-it` | 213080 | 15890 | 0 | `unknown` |
| `sambanova` | `gpt-oss-120b` | `unknown` | `unknown` | `unknown` | `unknown` |

## Status derivation and accuracy

- `Status` is derived from the configured-slot snapshot in `data/phase-2/statistics-state.json`: configured, non-retired models are `active`; any other retained model row is `inactive`.
- Execution outcome counters include only events recorded in the current statistics epoch.
- Provider-attempt totals for the current statistics epoch are locally counted from validated terminal events.
- Queue completion and age fields are derived from `task-state.json`; configuration and lifecycle come from the registry; execution status comes from runtime quota state when present.
- Token values are provider-reported when available and then locally summed. `unknown` is distinct from a reported value of zero.
- Quota state is best-known capacity, not a guarantee. Provenance marks observations as provider-reported, locally counted, configured, inferred, or unknown, and `estimated: true` explicitly identifies estimates such as remaining capacity.

## Storage strategy and limitations

The canonical machine-readable statistics state is stored in `data/phase-2/statistics-state.json`. This Markdown page is derived output and does not embed the state payload.

The collector aggregator commits the statistics state and this rendered page with task state, quota state, and durable results after each run that changes repository state.

Push conflicts are handled by fetching the latest branch and idempotently reapplying the same validated terminal events before a bounded retry.

The canonical statistics state retains legacy batch-event keys and queue attempt IDs for de-duplication. Historical compaction or reconstruction is handled separately from this storage split.

Neither the statistics state nor this page stores secrets, raw prompts, raw completions, or provider response bodies.

---

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →
