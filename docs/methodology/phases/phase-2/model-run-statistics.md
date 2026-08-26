# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page presents cumulative execution statistics and the current queue snapshot for the scheduled Phase 2 check-agent signal collector.

The tables are derived from canonical machine-readable statistics state, deterministic queue state, validated terminal events, and provider quota observations.

The current desired universe is 39 canonical pages × 2 LLM check agents × 25 configured provider-model slots = 1,950 tasks. Historical obsolete and retired identities remain stored, so total records may be higher.

Statistics collection started on: `2026-08-20T08:44:00Z`

Counts shown on this page only include executions recorded since that start time.

Rows retained in the current statistics state but outside the configured, non-retired registry are shown as `inactive`.

Last generated: `2026-08-26T16:58:50Z`

## Queue snapshot

| Queue state | Tasks |
|---|---:|
| `desired_task_count` | 1950 |
| `pending` | 1463 |
| `leased` | 0 |
| `completed` | 431 |
| `retry_due` | 2 |
| `quota_deferred` | 9 |
| `temporarily_unavailable` | 1 |
| `policy_blocked` | 0 |
| `execution_configuration_blocked` | 0 |
| `rejection_blocked` | 43 |
| `ambiguous_attempt_blocked` | 1 |
| `retired` | 540 |
| `obsolete` | 3633 |

## Provider–model outcomes

| Provider | Model | Status | Configuration | Execution | Lifecycle | Called | Provider attempts | Valid | Zero-signal valid | Valid with signals | Validator rejections | Provider failures | Quota deferrals | Policy blocks | Execution-config blocks | Temporarily unavailable | Runner failures |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | `active` | `configured` | `eligible` | `stable` | 175 | 182 | 79 | 0 | 79 | 47 | 49 | 46 | 0 | 0 | 7 | 0 |
| `gemini` | `gemini-2.5-flash-lite` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-2.5-pro` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3-flash-preview` | `active` | `configured` | `eligible` | `preview` | 144 | 145 | 104 | 4 | 100 | 7 | 33 | 33 | 0 | 0 | 1 | 0 |
| `gemini` | `gemini-3.1-flash-lite` | `active` | `configured` | `eligible` | `stable` | 135 | 136 | 110 | 4 | 106 | 25 | 0 | 0 | 0 | 0 | 1 | 0 |
| `gemini` | `gemini-3.5-flash` | `active` | `configured` | `temporarily_unavailable` | `stable` | 22 | 22 | 21 | 14 | 7 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| `gemini` | `gemini-3.5-flash-lite` | `active` | `configured` | `eligible` | `stable` | 125 | 125 | 115 | 43 | 72 | 10 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.6-flash` | `active` | `configured` | `eligible` | `stable` | 106 | 107 | 75 | 59 | 16 | 6 | 25 | 25 | 0 | 0 | 1 | 0 |
| `gemini` | `gemini-3.7-flash` | `active` | `configured` | `temporarily_unavailable` | `stable` | 138 | 191 | 74 | 60 | 14 | 1 | 63 | 38 | 0 | 0 | 53 | 0 |
| `groq` | `openai/gpt-oss-120b` | `active` | `configured` | `blocked_execution_configuration` | `production` | 13 | 13 | 12 | 7 | 5 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| `groq` | `openai/gpt-oss-20b` | `active` | `configured` | `blocked_execution_configuration` | `production` | 12 | 12 | 9 | 6 | 3 | 2 | 1 | 0 | 1 | 0 | 0 | 0 |
| `groq` | `qwen/qwen3.6-27b` | `active` | `configured` | `blocked_execution_configuration` | `preview` | 14 | 14 | 13 | 13 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 69 | 69 | 2 | 2 | 0 | 0 | 67 | 67 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-31b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 30 | 30 | 1 | 0 | 1 | 0 | 29 | 29 | 0 | 0 | 0 | 0 |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | `inactive` | `retired` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | `active` | `configured` | `blocked_execution_configuration` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | `configured` | `temporarily_unavailable` | `free-variant` | 96 | 192 | 0 | 0 | 0 | 0 | 96 | 0 | 0 | 0 | 96 | 0 |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | `active` | `configured` | `eligible` | `free-variant` | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | `active` | `configured` | `eligible` | `free-variant` | 4 | 4 | 1 | 1 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `openai/gpt-oss-20b:free` | `active` | `configured` | `eligible` | `free-variant` | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-s-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-xs-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.1` | `active` | `configured` | `eligible` | `production` | 98 | 98 | 0 | 0 | 0 | 0 | 98 | 98 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.2` | `active` | `configured` | `eligible` | `preview` | 98 | 98 | 0 | 0 | 0 | 0 | 98 | 98 | 0 | 0 | 0 | 0 |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | `configured` | `eligible` | `production` | 97 | 97 | 0 | 0 | 0 | 0 | 97 | 97 | 0 | 0 | 0 | 0 |
| `sambanova` | `MiniMax-M2.7` | `active` | `configured` | `eligible` | `production` | 146 | 146 | 20 | 11 | 9 | 120 | 6 | 6 | 0 | 0 | 0 | 0 |
| `sambanova` | `gemma-4-31B-it` | `active` | `configured` | `eligible` | `preview` | 87 | 87 | 74 | 25 | 49 | 8 | 5 | 5 | 0 | 0 | 0 | 0 |
| `sambanova` | `gpt-oss-120b` | `active` | `configured` | `eligible` | `production` | 98 | 98 | 0 | 0 | 0 | 0 | 98 | 98 | 0 | 0 | 0 | 0 |

## Current slot progress

| Provider | Model | Completed | Desired | Completion | Oldest pending | Last success | Last attempt | Last quota observation |
|---|---|---:|---:|---:|---|---|---|---|
| `gemini` | `gemini-2.5-flash` | 53 | 78 | 67.95% | 8h | `2026-08-26T15:59:34Z` | `2026-08-26T16:57:39Z` | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-2.5-flash-lite` | 0 | 0 | 0.00% |  |  |  | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-2.5-pro` | 0 | 0 | 0.00% |  |  |  | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-3-flash-preview` | 65 | 78 | 83.33% | 8h | `2026-08-26T15:59:59Z` | `2026-08-26T15:59:59Z` | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-3.1-flash-lite` | 71 | 78 | 91.03% |  | `2026-08-26T10:48:02Z` | `2026-08-26T10:48:08Z` | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-3.5-flash` | 12 | 78 | 15.38% | 9d 16h | `2026-08-24T21:52:06Z` | `2026-08-24T21:52:06Z` | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-3.5-flash-lite` | 77 | 78 | 98.72% |  | `2026-08-26T10:47:58Z` | `2026-08-26T10:47:58Z` | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-3.6-flash` | 39 | 78 | 50.00% | 8h | `2026-08-22T10:01:31Z` | `2026-08-22T10:01:31Z` | `2026-08-26T16:57:39Z` |
| `gemini` | `gemini-3.7-flash` | 37 | 78 | 47.44% | 8d 4h | `2026-08-25T12:08:02Z` | `2026-08-25T12:11:05Z` | `2026-08-26T16:57:39Z` |
| `groq` | `openai/gpt-oss-120b` | 8 | 78 | 10.26% | 9d 16h | `2026-08-20T09:52:10Z` | `2026-08-20T09:52:58Z` | `2026-08-24T20:36:14Z` |
| `groq` | `openai/gpt-oss-20b` | 7 | 78 | 8.97% | 9d 16h | `2026-08-20T09:52:07Z` | `2026-08-20T09:52:58Z` | `2026-08-24T20:36:14Z` |
| `groq` | `qwen/qwen3.6-27b` | 8 | 78 | 10.26% | 9d 16h | `2026-08-21T13:56:00Z` | `2026-08-21T13:56:01Z` | `2026-08-24T20:36:14Z` |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | 1 | 78 | 1.28% | 9d 16h | `2026-08-25T13:09:11Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `google/gemma-4-31b-it:free` | 1 | 78 | 1.28% | 9d 16h | `2026-08-21T18:53:12Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | 0 | 0 | 0.00% |  |  |  | `2026-08-26T16:09:06Z` |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | 0 | 78 | 0.00% | 7d 0h |  |  | `2026-08-26T16:09:06Z` |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | 78 | 0.00% | 7d 0h |  | `2026-08-26T16:09:02Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | 1 | 78 | 1.28% | 7d 7h | `2026-08-21T18:54:59Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | 0 | 78 | 0.00% | 9d 16h | `2026-08-22T00:03:06Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `openai/gpt-oss-20b:free` | 1 | 78 | 1.28% | 9d 16h | `2026-08-21T18:54:05Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `poolside/laguna-s-2.1:free` | 1 | 78 | 1.28% | 9d 16h | `2026-08-21T18:53:19Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `openrouter` | `poolside/laguna-xs-2.1:free` | 1 | 78 | 1.28% | 9d 16h | `2026-08-21T18:53:32Z` | `2026-08-26T16:09:06Z` | `2026-08-26T16:09:06Z` |
| `sambanova` | `DeepSeek-V3.1` | 0 | 78 | 0.00% | 9d 16h |  | `2026-08-26T15:58:52Z` | `2026-08-26T15:58:51Z` |
| `sambanova` | `DeepSeek-V3.2` | 0 | 78 | 0.00% | 9d 16h |  | `2026-08-26T15:58:52Z` | `2026-08-26T15:58:51Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | 0 | 78 | 0.00% | 9d 16h |  | `2026-08-26T15:58:52Z` | `2026-08-26T15:58:51Z` |
| `sambanova` | `MiniMax-M2.7` | 10 | 78 | 12.82% | 8h | `2026-08-20T13:08:24Z` | `2026-08-26T15:58:52Z` | `2026-08-26T15:58:51Z` |
| `sambanova` | `gemma-4-31B-it` | 38 | 78 | 48.72% | 8h | `2026-08-20T10:16:04Z` | `2026-08-26T15:58:52Z` | `2026-08-26T15:58:51Z` |
| `sambanova` | `gpt-oss-120b` | 0 | 78 | 0.00% | 9d 16h |  | `2026-08-26T15:58:52Z` | `2026-08-26T15:58:51Z` |

## Token observations

| Provider | Model | Input tokens | Output tokens | Reasoning tokens | Cached tokens |
|---|---|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | 544649 | 73686 | `unknown` | 79606 |
| `gemini` | `gemini-2.5-flash-lite` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-2.5-pro` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3-flash-preview` | 463854 | 50470 | `unknown` | 4074 |
| `gemini` | `gemini-3.1-flash-lite` | 580161 | 58682 | `unknown` | `unknown` |
| `gemini` | `gemini-3.5-flash` | 77027 | 6284 | 11705 | `unknown` |
| `gemini` | `gemini-3.5-flash-lite` | 537821 | 49845 | `unknown` | `unknown` |
| `gemini` | `gemini-3.6-flash` | 318292 | 24318 | 17806 | `unknown` |
| `gemini` | `gemini-3.7-flash` | 289805 | 22564 | 313 | `unknown` |
| `groq` | `openai/gpt-oss-120b` | 37675 | 8300 | 4054 | 6400 |
| `groq` | `openai/gpt-oss-20b` | 31776 | 8451 | 4657 | `unknown` |
| `groq` | `qwen/qwen3.6-27b` | 41601 | 3206 | `unknown` | `unknown` |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | 6397 | 529 | 0 | 0 |
| `openrouter` | `google/gemma-4-31b-it:free` | 2653 | 375 | 0 | 0 |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `unknown` | `unknown` | `unknown` | `unknown` |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | 2609 | 234 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | 12634 | 9914 | 8611 | 0 |
| `openrouter` | `openai/gpt-oss-20b:free` | 2523 | 902 | 283 | 0 |
| `openrouter` | `poolside/laguna-s-2.1:free` | 2537 | 233 | 0 | 0 |
| `openrouter` | `poolside/laguna-xs-2.1:free` | 2537 | 233 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.1` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `DeepSeek-V3.2` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `MiniMax-M2.7` | 499467 | 268664 | 238724 | 0 |
| `sambanova` | `gemma-4-31B-it` | 321532 | 31302 | 0 | `unknown` |
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
