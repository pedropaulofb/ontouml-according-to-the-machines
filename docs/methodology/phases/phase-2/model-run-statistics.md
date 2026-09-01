# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page presents cumulative execution statistics and the current queue snapshot for the scheduled Phase 2 check-agent signal collector.

The tables are derived from canonical machine-readable statistics state, deterministic queue state, validated terminal events, and provider quota observations.

The current desired universe is 39 canonical pages × 2 LLM check agents × 25 configured provider-model slots = 1,950 tasks. Historical obsolete and retired identities remain stored, so total records may be higher.

Statistics collection started on: `2026-08-28T08:14:33Z`

Counts shown on this page only include executions recorded since that start time.

Rows retained in the current statistics state but outside the configured, non-retired registry are shown as `inactive`.

Last generated: `2026-09-01T07:47:38Z`

## Queue snapshot

| Queue state | Tasks |
|---|---:|
| `desired_task_count` | 1950 |
| `pending` | 1430 |
| `leased` | 0 |
| `completed` | 461 |
| `retry_due` | 0 |
| `quota_deferred` | 7 |
| `temporarily_unavailable` | 2 |
| `policy_blocked` | 0 |
| `execution_configuration_blocked` | 0 |
| `rejection_blocked` | 49 |
| `ambiguous_attempt_blocked` | 1 |
| `retired` | 540 |
| `obsolete` | 3633 |

## Provider–model outcomes

| Provider | Model | Status | Configuration | Execution | Lifecycle | Called | Provider attempts | Valid | Zero-signal valid | Valid with signals | Validator rejections | Provider failures | Quota deferrals | Policy blocks | Execution-config blocks | Temporarily unavailable | Runner failures |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | `active` | `configured` | `eligible` | `stable` | 16 | 17 | 7 | 0 | 7 | 7 | 2 | 1 | 0 | 0 | 1 | 0 |
| `gemini` | `gemini-2.5-flash-lite` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-2.5-pro` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3-flash-preview` | `active` | `configured` | `eligible` | `preview` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.1-flash-lite` | `active` | `configured` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.5-flash` | `active` | `configured` | `eligible` | `stable` | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.5-flash-lite` | `active` | `configured` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.6-flash` | `active` | `configured` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.7-flash` | `active` | `configured` | `temporarily_unavailable` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `groq` | `openai/gpt-oss-120b` | `active` | `configured` | `blocked_execution_configuration` | `production` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `groq` | `openai/gpt-oss-20b` | `active` | `configured` | `blocked_execution_configuration` | `production` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `groq` | `qwen/qwen3.6-27b` | `active` | `configured` | `blocked_execution_configuration` | `preview` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 19 | 19 | 0 | 0 | 0 | 0 | 19 | 19 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-31b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | `inactive` | `retired` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | `active` | `configured` | `blocked_execution_configuration` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | `configured` | `temporarily_unavailable` | `free-variant` | 20 | 39 | 0 | 0 | 0 | 0 | 20 | 0 | 0 | 0 | 20 | 0 |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `openai/gpt-oss-20b:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-s-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-xs-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.1` | `active` | `configured` | `eligible` | `production` | 19 | 19 | 0 | 0 | 0 | 0 | 19 | 19 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.2` | `active` | `configured` | `eligible` | `preview` | 19 | 19 | 0 | 0 | 0 | 0 | 19 | 19 | 0 | 0 | 0 | 0 |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | `configured` | `eligible` | `production` | 19 | 19 | 0 | 0 | 0 | 0 | 19 | 19 | 0 | 0 | 0 | 0 |
| `sambanova` | `MiniMax-M2.7` | `active` | `configured` | `eligible` | `production` | 20 | 20 | 0 | 0 | 0 | 0 | 20 | 20 | 0 | 0 | 0 | 0 |
| `sambanova` | `gemma-4-31B-it` | `active` | `configured` | `eligible` | `preview` | 19 | 19 | 0 | 0 | 0 | 0 | 19 | 19 | 0 | 0 | 0 | 0 |
| `sambanova` | `gpt-oss-120b` | `active` | `configured` | `eligible` | `production` | 19 | 19 | 0 | 0 | 0 | 0 | 19 | 19 | 0 | 0 | 0 | 0 |

## Current slot progress

| Provider | Model | Completed | Desired | Completion | Oldest pending | Last success | Last attempt | Last quota observation |
|---|---|---:|---:|---:|---|---|---|---|
| `gemini` | `gemini-2.5-flash` | 69 | 78 | 88.46% |  | `2026-08-29T15:09:38Z` | `2026-08-29T18:41:50Z` | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-2.5-flash-lite` | 0 | 0 | 0.00% |  |  |  | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-2.5-pro` | 0 | 0 | 0.00% |  |  |  | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-3-flash-preview` | 77 | 78 | 98.72% |  |  |  | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-3.1-flash-lite` | 71 | 78 | 91.03% |  |  |  | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-3.5-flash` | 13 | 78 | 16.67% | 15d 7h | `2026-09-01T07:46:22Z` | `2026-09-01T07:46:22Z` | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-3.5-flash-lite` | 77 | 78 | 98.72% |  |  |  | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-3.6-flash` | 40 | 78 | 51.28% | 5d 23h |  |  | `2026-09-01T07:46:22Z` |
| `gemini` | `gemini-3.7-flash` | 37 | 78 | 47.44% | 13d 19h |  |  | `2026-09-01T07:46:22Z` |
| `groq` | `openai/gpt-oss-120b` | 8 | 78 | 10.26% | 15d 7h |  |  | `2026-08-24T20:36:14Z` |
| `groq` | `openai/gpt-oss-20b` | 7 | 78 | 8.97% | 15d 7h |  |  | `2026-08-24T20:36:14Z` |
| `groq` | `qwen/qwen3.6-27b` | 8 | 78 | 10.26% | 15d 7h |  |  | `2026-08-24T20:36:14Z` |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | 1 | 78 | 1.28% | 15d 7h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `google/gemma-4-31b-it:free` | 1 | 78 | 1.28% | 15d 7h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | 0 | 0 | 0.00% |  |  |  | `2026-09-01T07:46:33Z` |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | 0 | 78 | 0.00% | 12d 15h |  |  | `2026-09-01T07:46:33Z` |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | 78 | 0.00% | 12d 15h |  | `2026-09-01T07:46:33Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | 1 | 78 | 1.28% | 12d 22h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | 0 | 78 | 0.00% | 15d 7h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `openai/gpt-oss-20b:free` | 1 | 78 | 1.28% | 15d 7h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `poolside/laguna-s-2.1:free` | 1 | 78 | 1.28% | 15d 7h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `openrouter` | `poolside/laguna-xs-2.1:free` | 1 | 78 | 1.28% | 15d 7h |  | `2026-09-01T05:02:54Z` | `2026-09-01T07:46:33Z` |
| `sambanova` | `DeepSeek-V3.1` | 0 | 78 | 0.00% | 15d 7h |  | `2026-09-01T05:01:47Z` | `2026-09-01T07:46:23Z` |
| `sambanova` | `DeepSeek-V3.2` | 0 | 78 | 0.00% | 15d 7h |  | `2026-09-01T05:01:47Z` | `2026-09-01T07:46:23Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | 0 | 78 | 0.00% | 15d 7h |  | `2026-09-01T05:01:47Z` | `2026-09-01T07:46:23Z` |
| `sambanova` | `MiniMax-M2.7` | 10 | 78 | 12.82% | 5d 23h |  | `2026-09-01T07:46:23Z` | `2026-09-01T07:46:23Z` |
| `sambanova` | `gemma-4-31B-it` | 38 | 78 | 48.72% | 5d 23h |  | `2026-09-01T05:01:47Z` | `2026-09-01T07:46:23Z` |
| `sambanova` | `gpt-oss-120b` | 0 | 78 | 0.00% | 15d 7h |  | `2026-09-01T05:01:47Z` | `2026-09-01T07:46:23Z` |

## Token observations

| Provider | Model | Input tokens | Output tokens | Reasoning tokens | Cached tokens |
|---|---|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | 66287 | 7281 | `unknown` | 8166 |
| `gemini` | `gemini-2.5-flash-lite` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-2.5-pro` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3-flash-preview` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3.1-flash-lite` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3.5-flash` | 3827 | 252 | `unknown` | `unknown` |
| `gemini` | `gemini-3.5-flash-lite` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3.6-flash` | `unknown` | `unknown` | `unknown` | `unknown` |
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
| `sambanova` | `MiniMax-M2.7` | `unknown` | `unknown` | `unknown` | `unknown` |
| `sambanova` | `gemma-4-31B-it` | `unknown` | `unknown` | `unknown` | `unknown` |
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
