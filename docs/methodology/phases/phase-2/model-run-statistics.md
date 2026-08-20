# Phase 2 — Model Run Statistics

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

This page stores cumulative execution statistics and the current queue snapshot for the scheduled Phase 2 check-agent signal collector.

The tables are updated from deterministic queue state, validated terminal events, and provider quota observations.

The current desired universe is 39 canonical pages × 2 LLM check agents × 25 configured provider-model slots = 1,950 tasks. Historical obsolete and retired identities remain stored, so total records may be higher.

Statistics collection started on: `2026-08-20T08:44:00Z`

Counts shown on this page only include executions recorded since that start time.

Rows retained in the current statistics state but outside the configured, non-retired registry are shown as `inactive`.

Last generated: `2026-08-20T11:15:44Z`

## Queue snapshot

| Queue state | Tasks |
|---|---:|
| `desired_task_count` | 1950 |
| `pending` | 1637 |
| `leased` | 0 |
| `completed` | 234 |
| `retry_due` | 65 |
| `quota_deferred` | 7 |
| `temporarily_unavailable` | 3 |
| `policy_blocked` | 3 |
| `execution_configuration_blocked` | 0 |
| `rejection_blocked` | 1 |
| `ambiguous_attempt_blocked` | 0 |
| `retired` | 540 |
| `obsolete` | 2658 |

## Provider–model outcomes

| Provider | Model | Status | Configuration | Execution | Lifecycle | Called | Provider attempts | Valid | Zero-signal valid | Valid with signals | Validator rejections | Provider failures | Quota deferrals | Policy blocks | Execution-config blocks | Temporarily unavailable | Runner failures |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | `active` | `configured` | `blocked_provider_policy` | `stable` | 20 | 20 | 14 | 0 | 14 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-2.5-flash-lite` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-2.5-pro` | `inactive` | `retired` | `eligible` | `stable` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3-flash-preview` | `active` | `configured` | `blocked_provider_policy` | `preview` | 21 | 21 | 21 | 3 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.1-flash-lite` | `active` | `configured` | `blocked_provider_policy` | `stable` | 21 | 21 | 18 | 1 | 17 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.5-flash` | `active` | `configured` | `blocked_provider_policy` | `stable` | 21 | 21 | 20 | 14 | 6 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| `gemini` | `gemini-3.5-flash-lite` | `active` | `configured` | `blocked_provider_policy` | `stable` | 21 | 21 | 21 | 8 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.6-flash` | `active` | `configured` | `blocked_provider_policy` | `stable` | 20 | 20 | 19 | 16 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `gemini` | `gemini-3.7-flash` | `active` | `configured` | `blocked_provider_policy` | `stable` | 1 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| `groq` | `openai/gpt-oss-120b` | `active` | `configured` | `blocked_provider_policy` | `production` | 13 | 13 | 12 | 7 | 5 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| `groq` | `openai/gpt-oss-20b` | `active` | `configured` | `blocked_provider_policy` | `production` | 12 | 12 | 9 | 6 | 3 | 2 | 1 | 0 | 1 | 0 | 0 | 0 |
| `groq` | `qwen/qwen3.6-27b` | `active` | `configured` | `blocked_provider_policy` | `preview` | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| `openrouter` | `google/gemma-4-31b-it:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | `inactive` | `retired` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | `active` | `configured` | `blocked_execution_configuration` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | `active` | `configured` | `temporarily_unavailable` | `free-variant` | 2 | 4 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0 |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `openai/gpt-oss-20b:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-s-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `openrouter` | `poolside/laguna-xs-2.1:free` | `active` | `configured` | `eligible` | `free-variant` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.1` | `active` | `configured` | `eligible` | `production` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| `sambanova` | `DeepSeek-V3.2` | `active` | `configured` | `eligible` | `preview` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | `active` | `configured` | `eligible` | `production` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |
| `sambanova` | `MiniMax-M2.7` | `active` | `configured` | `eligible` | `production` | 62 | 62 | 10 | 6 | 4 | 51 | 1 | 1 | 0 | 0 | 0 | 0 |
| `sambanova` | `gemma-4-31B-it` | `active` | `configured` | `eligible` | `preview` | 79 | 79 | 74 | 25 | 49 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| `sambanova` | `gpt-oss-120b` | `active` | `configured` | `eligible` | `production` | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 |

## Current slot progress

| Provider | Model | Completed | Desired | Completion | Oldest pending | Last success | Last attempt | Last quota observation |
|---|---|---:|---:|---:|---|---|---|---|
| `gemini` | `gemini-2.5-flash` | 14 | 78 | 17.95% | 3d 11h | `2026-08-20T09:52:17Z` | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-2.5-flash-lite` | 0 | 0 | 0.00% |  |  |  | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-2.5-pro` | 0 | 0 | 0.00% |  |  |  | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-3-flash-preview` | 21 | 78 | 26.92% | 3d 11h | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-3.1-flash-lite` | 18 | 78 | 23.08% | 3d 11h | `2026-08-20T09:52:42Z` | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-3.5-flash` | 20 | 78 | 25.64% | 3d 11h | `2026-08-20T09:52:19Z` | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-3.5-flash-lite` | 21 | 78 | 26.92% | 3d 11h | `2026-08-20T09:52:41Z` | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-3.6-flash` | 20 | 78 | 25.64% | 3d 11h | `2026-08-20T09:52:38Z` | `2026-08-20T09:52:43Z` | `2026-08-20T09:52:42Z` |
| `gemini` | `gemini-3.7-flash` | 1 | 78 | 1.28% | 1d 22h | `2026-08-20T09:46:46Z` | `2026-08-20T09:46:46Z` | `2026-08-20T09:52:42Z` |
| `groq` | `openai/gpt-oss-120b` | 13 | 78 | 16.67% | 3d 11h | `2026-08-20T09:52:10Z` | `2026-08-20T09:52:58Z` | `2026-08-20T09:52:58Z` |
| `groq` | `openai/gpt-oss-20b` | 9 | 78 | 11.54% | 3d 11h | `2026-08-20T09:52:07Z` | `2026-08-20T09:52:58Z` | `2026-08-20T09:52:58Z` |
| `groq` | `qwen/qwen3.6-27b` | 12 | 78 | 15.38% | 3d 11h | `2026-08-20T09:52:58Z` | `2026-08-20T09:52:58Z` | `2026-08-20T09:52:58Z` |
| `openrouter` | `google/gemma-4-26b-a4b-it:free` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `google/gemma-4-31b-it:free` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `inclusionai/ling-3.0-flash:free` | 0 | 0 | 0.00% |  |  |  | `2026-08-20T10:55:33Z` |
| `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | 0 | 78 | 0.00% | 19h |  |  | `2026-08-20T10:55:33Z` |
| `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | 0 | 78 | 0.00% | 19h |  | `2026-08-20T10:55:29Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `nvidia/nemotron-3.5-lightning:free` | 0 | 78 | 0.00% | 1d 1h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `openai/gpt-oss-20b:free` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `poolside/laguna-s-2.1:free` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `openrouter` | `poolside/laguna-xs-2.1:free` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T10:55:33Z` | `2026-08-20T10:55:33Z` |
| `sambanova` | `DeepSeek-V3.1` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T11:15:23Z` | `2026-08-20T11:15:23Z` |
| `sambanova` | `DeepSeek-V3.2` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T11:15:23Z` | `2026-08-20T11:15:23Z` |
| `sambanova` | `Meta-Llama-3.3-70B-Instruct` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T11:15:23Z` | `2026-08-20T11:15:23Z` |
| `sambanova` | `MiniMax-M2.7` | 11 | 78 | 14.10% | 3d 11h | `2026-08-20T09:55:47Z` | `2026-08-20T10:14:48Z` | `2026-08-20T11:15:23Z` |
| `sambanova` | `gemma-4-31B-it` | 74 | 78 | 94.87% | 3d 11h | `2026-08-20T10:16:04Z` | `2026-08-20T11:15:23Z` | `2026-08-20T11:15:23Z` |
| `sambanova` | `gpt-oss-120b` | 0 | 78 | 0.00% | 3d 11h |  | `2026-08-20T11:15:23Z` | `2026-08-20T11:15:23Z` |

## Token observations

| Provider | Model | Input tokens | Output tokens | Reasoning tokens | Cached tokens |
|---|---|---:|---:|---:|---:|
| `gemini` | `gemini-2.5-flash` | 74107 | 13602 | `unknown` | 19382 |
| `gemini` | `gemini-2.5-flash-lite` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-2.5-pro` | `unknown` | `unknown` | `unknown` | `unknown` |
| `gemini` | `gemini-3-flash-preview` | 77027 | 8483 | `unknown` | `unknown` |
| `gemini` | `gemini-3.1-flash-lite` | 77069 | 8956 | `unknown` | `unknown` |
| `gemini` | `gemini-3.5-flash` | 74107 | 5851 | 10234 | `unknown` |
| `gemini` | `gemini-3.5-flash-lite` | 77069 | 8250 | `unknown` | `unknown` |
| `gemini` | `gemini-3.6-flash` | 74376 | 5388 | 4634 | `unknown` |
| `gemini` | `gemini-3.7-flash` | 2650 | 242 | `unknown` | `unknown` |
| `groq` | `openai/gpt-oss-120b` | 37675 | 8300 | 4054 | 6400 |
| `groq` | `openai/gpt-oss-20b` | 31776 | 8451 | 4657 | `unknown` |
| `groq` | `qwen/qwen3.6-27b` | 38725 | 2963 | `unknown` | `unknown` |
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
| `sambanova` | `MiniMax-M2.7` | 214812 | 108097 | 92927 | 0 |
| `sambanova` | `gemma-4-31B-it` | 306271 | 29830 | 0 | `unknown` |
| `sambanova` | `gpt-oss-120b` | `unknown` | `unknown` | `unknown` | `unknown` |

## Status derivation and accuracy

- `Status` is derived from the hidden configured-slot snapshot: configured, non-retired models are `active`; any other retained model row is `inactive`.
- Execution outcome counters include only events recorded in the current statistics epoch.
- Provider-attempt totals for the current statistics epoch are locally counted from validated terminal events.
- Queue completion and age fields are derived from `task-state.json`; configuration and lifecycle come from the registry; execution status comes from runtime quota state when present.
- Token values are provider-reported when available and then locally summed. `unknown` is distinct from a reported value of zero.
- Quota state is best-known capacity, not a guarantee. Provenance marks observations as provider-reported, locally counted, configured, inferred, or unknown, and `estimated: true` explicitly identifies estimates such as remaining capacity.

## Storage strategy and limitations

The human-readable tables are rendered from hidden JSON state stored in this Markdown file. Durable task results and publication payloads are stored separately under `data/phase-2/`.

The collector aggregator commits this page with task state, quota state, and durable results after each run that changes repository state.

Push conflicts are handled by fetching the latest branch and idempotently reapplying the same validated terminal events before a bounded retry.

The hidden state stores legacy batch-event keys and queue attempt IDs for de-duplication. This prevents accidental double-counting but means the Markdown file grows over time.

This page does not store secrets, raw prompts, raw completions, or provider response bodies.

<!-- model-run-statistics-state
{
  "active_rotation": [
    {
      "model": "MiniMax-M2.7",
      "provider": "sambanova",
      "spec": "sambanova:MiniMax-M2.7"
    },
    {
      "model": "DeepSeek-V3.1",
      "provider": "sambanova",
      "spec": "sambanova:DeepSeek-V3.1"
    },
    {
      "model": "Meta-Llama-3.3-70B-Instruct",
      "provider": "sambanova",
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct"
    },
    {
      "model": "gpt-oss-120b",
      "provider": "sambanova",
      "spec": "sambanova:gpt-oss-120b"
    },
    {
      "model": "DeepSeek-V3.2",
      "provider": "sambanova",
      "spec": "sambanova:DeepSeek-V3.2"
    },
    {
      "model": "gemma-4-31B-it",
      "provider": "sambanova",
      "spec": "sambanova:gemma-4-31B-it"
    },
    {
      "model": "openai/gpt-oss-120b",
      "provider": "groq",
      "spec": "groq:openai/gpt-oss-120b"
    },
    {
      "model": "openai/gpt-oss-20b",
      "provider": "groq",
      "spec": "groq:openai/gpt-oss-20b"
    },
    {
      "model": "qwen/qwen3.6-27b",
      "provider": "groq",
      "spec": "groq:qwen/qwen3.6-27b"
    },
    {
      "model": "gemini-3.6-flash",
      "provider": "gemini",
      "spec": "gemini:gemini-3.6-flash"
    },
    {
      "model": "gemini-3.5-flash",
      "provider": "gemini",
      "spec": "gemini:gemini-3.5-flash"
    },
    {
      "model": "gemini-3.5-flash-lite",
      "provider": "gemini",
      "spec": "gemini:gemini-3.5-flash-lite"
    },
    {
      "model": "gemini-3.1-flash-lite",
      "provider": "gemini",
      "spec": "gemini:gemini-3.1-flash-lite"
    },
    {
      "model": "gemini-3-flash-preview",
      "provider": "gemini",
      "spec": "gemini:gemini-3-flash-preview"
    },
    {
      "model": "gemini-2.5-flash",
      "provider": "gemini",
      "spec": "gemini:gemini-2.5-flash"
    },
    {
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "provider": "openrouter",
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free"
    },
    {
      "model": "nvidia/nemotron-3-super-120b-a12b:free",
      "provider": "openrouter",
      "spec": "openrouter:nvidia/nemotron-3-super-120b-a12b:free"
    },
    {
      "model": "google/gemma-4-26b-a4b-it:free",
      "provider": "openrouter",
      "spec": "openrouter:google/gemma-4-26b-a4b-it:free"
    },
    {
      "model": "google/gemma-4-31b-it:free",
      "provider": "openrouter",
      "spec": "openrouter:google/gemma-4-31b-it:free"
    },
    {
      "model": "poolside/laguna-s-2.1:free",
      "provider": "openrouter",
      "spec": "openrouter:poolside/laguna-s-2.1:free"
    },
    {
      "model": "poolside/laguna-xs-2.1:free",
      "provider": "openrouter",
      "spec": "openrouter:poolside/laguna-xs-2.1:free"
    },
    {
      "model": "openai/gpt-oss-20b:free",
      "provider": "openrouter",
      "spec": "openrouter:openai/gpt-oss-20b:free"
    },
    {
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "provider": "openrouter",
      "spec": "openrouter:nvidia/nemotron-nano-9b-v2:free"
    },
    {
      "model": "gemini-3.7-flash",
      "provider": "gemini",
      "spec": "gemini:gemini-3.7-flash"
    },
    {
      "model": "nvidia/nemotron-3.5-lightning:free",
      "provider": "openrouter",
      "spec": "openrouter:nvidia/nemotron-3.5-lightning:free"
    }
  ],
  "collection_start_utc": "2026-08-20T08:44:00Z",
  "generated_at": "2026-08-20T11:15:44Z",
  "models": {
    "gemini:gemini-2.5-flash": {
      "cached_tokens": 19382,
      "cached_tokens_known_events": 11,
      "called": 20,
      "completion_percentage": 17.95,
      "configuration_status": "configured",
      "current_completed_tasks": 14,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 74107,
      "input_tokens_known_events": 20,
      "invalid": 6,
      "last_attempt": "2026-08-20T09:52:43Z",
      "last_check_status": "rejected",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:43Z",
      "last_success": "2026-08-20T09:52:17Z",
      "lifecycle_status": "stable",
      "model": "gemini-2.5-flash",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 13602,
      "output_tokens_known_events": 20,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 6,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-2.5-flash",
      "temporarily_unavailable_events": 0,
      "total_called": 20,
      "total_provider_attempts": 20,
      "valid": 14,
      "valid_outputs": 14,
      "valid_outputs_with_signals": 14,
      "validator_rejections": 6,
      "zero_signal_valid_outputs": 0
    },
    "gemini:gemini-2.5-flash-lite": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "retired",
      "current_completed_tasks": 0,
      "current_desired_tasks": 0,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "last_success": "",
      "lifecycle_status": "stable",
      "model": "gemini-2.5-flash-lite",
      "oldest_pending_age_seconds": null,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-2.5-flash-lite",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "gemini:gemini-2.5-pro": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "retired",
      "current_completed_tasks": 0,
      "current_desired_tasks": 0,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "last_success": "",
      "lifecycle_status": "stable",
      "model": "gemini-2.5-pro",
      "oldest_pending_age_seconds": null,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-2.5-pro",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "gemini:gemini-3-flash-preview": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 21,
      "completion_percentage": 26.92,
      "configuration_status": "configured",
      "current_completed_tasks": 21,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 77027,
      "input_tokens_known_events": 21,
      "invalid": 0,
      "last_attempt": "2026-08-20T09:52:43Z",
      "last_check_status": "ok",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:43Z",
      "last_success": "2026-08-20T09:52:43Z",
      "lifecycle_status": "preview",
      "model": "gemini-3-flash-preview",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 8483,
      "output_tokens_known_events": 21,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-3-flash-preview",
      "temporarily_unavailable_events": 0,
      "total_called": 21,
      "total_provider_attempts": 21,
      "valid": 21,
      "valid_outputs": 21,
      "valid_outputs_with_signals": 18,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 3
    },
    "gemini:gemini-3.1-flash-lite": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 21,
      "completion_percentage": 23.08,
      "configuration_status": "configured",
      "current_completed_tasks": 18,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 77069,
      "input_tokens_known_events": 21,
      "invalid": 3,
      "last_attempt": "2026-08-20T09:52:43Z",
      "last_check_status": "ok",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:43Z",
      "last_success": "2026-08-20T09:52:42Z",
      "lifecycle_status": "stable",
      "model": "gemini-3.1-flash-lite",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 8956,
      "output_tokens_known_events": 21,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 3,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-3.1-flash-lite",
      "temporarily_unavailable_events": 0,
      "total_called": 21,
      "total_provider_attempts": 21,
      "valid": 18,
      "valid_outputs": 18,
      "valid_outputs_with_signals": 17,
      "validator_rejections": 3,
      "zero_signal_valid_outputs": 1
    },
    "gemini:gemini-3.5-flash": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 21,
      "completion_percentage": 25.64,
      "configuration_status": "configured",
      "current_completed_tasks": 20,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 74107,
      "input_tokens_known_events": 20,
      "invalid": 1,
      "last_attempt": "2026-08-20T09:52:43Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:43Z",
      "last_success": "2026-08-20T09:52:19Z",
      "lifecycle_status": "stable",
      "model": "gemini-3.5-flash",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 5851,
      "output_tokens_known_events": 20,
      "policy_blocks": 1,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 1,
      "provider_failures": 1,
      "quota_deferrals": 0,
      "reasoning_tokens": 10234,
      "reasoning_tokens_known_events": 12,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-3.5-flash",
      "temporarily_unavailable_events": 0,
      "total_called": 21,
      "total_provider_attempts": 21,
      "valid": 20,
      "valid_outputs": 20,
      "valid_outputs_with_signals": 6,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 14
    },
    "gemini:gemini-3.5-flash-lite": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 21,
      "completion_percentage": 26.92,
      "configuration_status": "configured",
      "current_completed_tasks": 21,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 77069,
      "input_tokens_known_events": 21,
      "invalid": 0,
      "last_attempt": "2026-08-20T09:52:43Z",
      "last_check_status": "ok",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:43Z",
      "last_success": "2026-08-20T09:52:41Z",
      "lifecycle_status": "stable",
      "model": "gemini-3.5-flash-lite",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 8250,
      "output_tokens_known_events": 21,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-3.5-flash-lite",
      "temporarily_unavailable_events": 0,
      "total_called": 21,
      "total_provider_attempts": 21,
      "valid": 21,
      "valid_outputs": 21,
      "valid_outputs_with_signals": 13,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 8
    },
    "gemini:gemini-3.6-flash": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 20,
      "completion_percentage": 25.64,
      "configuration_status": "configured",
      "current_completed_tasks": 20,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 74376,
      "input_tokens_known_events": 20,
      "invalid": 1,
      "last_attempt": "2026-08-20T09:52:43Z",
      "last_check_status": "ok",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:43Z",
      "last_success": "2026-08-20T09:52:38Z",
      "lifecycle_status": "stable",
      "model": "gemini-3.6-flash",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 5388,
      "output_tokens_known_events": 20,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": 4634,
      "reasoning_tokens_known_events": 8,
      "rejected": 1,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-3.6-flash",
      "temporarily_unavailable_events": 0,
      "total_called": 20,
      "total_provider_attempts": 20,
      "valid": 19,
      "valid_outputs": 19,
      "valid_outputs_with_signals": 3,
      "validator_rejections": 1,
      "zero_signal_valid_outputs": 16
    },
    "gemini:gemini-3.7-flash": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 1,
      "completion_percentage": 1.28,
      "configuration_status": "configured",
      "current_completed_tasks": 1,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 2650,
      "input_tokens_known_events": 1,
      "invalid": 0,
      "last_attempt": "2026-08-20T09:46:46Z",
      "last_check_status": "ok",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:42Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:46:46Z",
      "last_success": "2026-08-20T09:46:46Z",
      "lifecycle_status": "stable",
      "model": "gemini-3.7-flash",
      "oldest_pending_age_seconds": 168344,
      "output_tokens": 242,
      "output_tokens_known_events": 1,
      "policy_blocks": 0,
      "provider": "gemini",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "gemini:gemini-3.7-flash",
      "temporarily_unavailable_events": 1,
      "total_called": 1,
      "total_provider_attempts": 2,
      "valid": 1,
      "valid_outputs": 1,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 1
    },
    "groq:openai/gpt-oss-120b": {
      "cached_tokens": 6400,
      "cached_tokens_known_events": 3,
      "called": 13,
      "completion_percentage": 16.67,
      "configuration_status": "configured",
      "current_completed_tasks": 13,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 37675,
      "input_tokens_known_events": 12,
      "invalid": 1,
      "last_attempt": "2026-08-20T09:52:58Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:58Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:58Z",
      "last_success": "2026-08-20T09:52:10Z",
      "lifecycle_status": "production",
      "model": "openai/gpt-oss-120b",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 8300,
      "output_tokens_known_events": 12,
      "policy_blocks": 1,
      "provider": "groq",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 1,
      "provider_failures": 1,
      "quota_deferrals": 0,
      "reasoning_tokens": 4054,
      "reasoning_tokens_known_events": 12,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "groq:openai/gpt-oss-120b",
      "temporarily_unavailable_events": 0,
      "total_called": 13,
      "total_provider_attempts": 13,
      "valid": 12,
      "valid_outputs": 12,
      "valid_outputs_with_signals": 5,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 7
    },
    "groq:openai/gpt-oss-20b": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 12,
      "completion_percentage": 11.54,
      "configuration_status": "configured",
      "current_completed_tasks": 9,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 31776,
      "input_tokens_known_events": 11,
      "invalid": 3,
      "last_attempt": "2026-08-20T09:52:58Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:58Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:58Z",
      "last_success": "2026-08-20T09:52:07Z",
      "lifecycle_status": "production",
      "model": "openai/gpt-oss-20b",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 8451,
      "output_tokens_known_events": 11,
      "policy_blocks": 1,
      "provider": "groq",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 1,
      "provider_failures": 1,
      "quota_deferrals": 0,
      "reasoning_tokens": 4657,
      "reasoning_tokens_known_events": 11,
      "rejected": 2,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "groq:openai/gpt-oss-20b",
      "temporarily_unavailable_events": 0,
      "total_called": 12,
      "total_provider_attempts": 12,
      "valid": 9,
      "valid_outputs": 9,
      "valid_outputs_with_signals": 3,
      "validator_rejections": 2,
      "zero_signal_valid_outputs": 6
    },
    "groq:qwen/qwen3.6-27b": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 12,
      "completion_percentage": 15.38,
      "configuration_status": "configured",
      "current_completed_tasks": 12,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_provider_policy",
      "input_tokens": 38725,
      "input_tokens_known_events": 12,
      "invalid": 0,
      "last_attempt": "2026-08-20T09:52:58Z",
      "last_check_status": "ok",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T09:52:58Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T09:52:58Z",
      "last_success": "2026-08-20T09:52:58Z",
      "lifecycle_status": "preview",
      "model": "qwen/qwen3.6-27b",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 2963,
      "output_tokens_known_events": 12,
      "policy_blocks": 0,
      "provider": "groq",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "groq:qwen/qwen3.6-27b",
      "temporarily_unavailable_events": 0,
      "total_called": 12,
      "total_provider_attempts": 12,
      "valid": 12,
      "valid_outputs": 12,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 12
    },
    "openrouter:google/gemma-4-26b-a4b-it:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 2,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 2,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "google/gemma-4-26b-a4b-it:free",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 2,
      "provider_failures": 2,
      "quota_deferrals": 2,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:google/gemma-4-26b-a4b-it:free",
      "temporarily_unavailable_events": 0,
      "total_called": 2,
      "total_provider_attempts": 2,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:google/gemma-4-31b-it:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "google/gemma-4-31b-it:free",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:google/gemma-4-31b-it:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:inclusionai/ling-3.0-flash:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "retired",
      "current_completed_tasks": 0,
      "current_desired_tasks": 0,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "inclusionai/ling-3.0-flash:free",
      "oldest_pending_age_seconds": null,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:inclusionai/ling-3.0-flash:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:nvidia/nemotron-3-super-120b-a12b:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "blocked_execution_configuration",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "nvidia/nemotron-3-super-120b-a12b:free",
      "oldest_pending_age_seconds": 69362,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:nvidia/nemotron-3-super-120b-a12b:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 2,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "temporarily_unavailable",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 2,
      "last_attempt": "2026-08-20T10:55:29Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:29Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "oldest_pending_age_seconds": 69362,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 2,
      "provider_failures": 2,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:nvidia/nemotron-3-ultra-550b-a55b:free",
      "temporarily_unavailable_events": 2,
      "total_called": 2,
      "total_provider_attempts": 4,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:nvidia/nemotron-3.5-lightning:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "oldest_pending_age_seconds": 93344,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:nvidia/nemotron-3.5-lightning:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:nvidia/nemotron-nano-9b-v2:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:nvidia/nemotron-nano-9b-v2:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:openai/gpt-oss-20b:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "openai/gpt-oss-20b:free",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:openai/gpt-oss-20b:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:poolside/laguna-s-2.1:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "poolside/laguna-s-2.1:free",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:poolside/laguna-s-2.1:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "openrouter:poolside/laguna-xs-2.1:free": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 0,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 0,
      "last_attempt": "2026-08-20T10:55:33Z",
      "last_check_status": "",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T10:55:33Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:55:33Z",
      "last_success": "",
      "lifecycle_status": "free-variant",
      "model": "poolside/laguna-xs-2.1:free",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "openrouter",
      "provider_attempts_accuracy": "locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "openrouter:poolside/laguna-xs-2.1:free",
      "temporarily_unavailable_events": 0,
      "total_called": 0,
      "total_provider_attempts": 0,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "sambanova:DeepSeek-V3.1": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 2,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 2,
      "last_attempt": "2026-08-20T11:15:23Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T11:15:23Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T11:15:23Z",
      "last_success": "",
      "lifecycle_status": "production",
      "model": "DeepSeek-V3.1",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "sambanova",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 2,
      "provider_failures": 2,
      "quota_deferrals": 2,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "sambanova:DeepSeek-V3.1",
      "temporarily_unavailable_events": 0,
      "total_called": 2,
      "total_provider_attempts": 2,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "sambanova:DeepSeek-V3.2": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 2,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 2,
      "last_attempt": "2026-08-20T11:15:23Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T11:15:23Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T11:15:23Z",
      "last_success": "",
      "lifecycle_status": "preview",
      "model": "DeepSeek-V3.2",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "sambanova",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 2,
      "provider_failures": 2,
      "quota_deferrals": 2,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "sambanova:DeepSeek-V3.2",
      "temporarily_unavailable_events": 0,
      "total_called": 2,
      "total_provider_attempts": 2,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "sambanova:Meta-Llama-3.3-70B-Instruct": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 2,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 2,
      "last_attempt": "2026-08-20T11:15:23Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T11:15:23Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T11:15:23Z",
      "last_success": "",
      "lifecycle_status": "production",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "sambanova",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 2,
      "provider_failures": 2,
      "quota_deferrals": 2,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "sambanova:Meta-Llama-3.3-70B-Instruct",
      "temporarily_unavailable_events": 0,
      "total_called": 2,
      "total_provider_attempts": 2,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    },
    "sambanova:MiniMax-M2.7": {
      "cached_tokens": 0,
      "cached_tokens_known_events": 61,
      "called": 62,
      "completion_percentage": 14.1,
      "configuration_status": "configured",
      "current_completed_tasks": 11,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": 214812,
      "input_tokens_known_events": 61,
      "invalid": 52,
      "last_attempt": "2026-08-20T10:14:48Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T11:15:23Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T10:14:48Z",
      "last_success": "2026-08-20T09:55:47Z",
      "lifecycle_status": "production",
      "model": "MiniMax-M2.7",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 108097,
      "output_tokens_known_events": 61,
      "policy_blocks": 0,
      "provider": "sambanova",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 1,
      "provider_failures": 1,
      "quota_deferrals": 1,
      "reasoning_tokens": 92927,
      "reasoning_tokens_known_events": 61,
      "rejected": 51,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "sambanova:MiniMax-M2.7",
      "temporarily_unavailable_events": 0,
      "total_called": 62,
      "total_provider_attempts": 62,
      "valid": 10,
      "valid_outputs": 10,
      "valid_outputs_with_signals": 4,
      "validator_rejections": 51,
      "zero_signal_valid_outputs": 6
    },
    "sambanova:gemma-4-31B-it": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 79,
      "completion_percentage": 94.87,
      "configuration_status": "configured",
      "current_completed_tasks": 74,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": 306271,
      "input_tokens_known_events": 79,
      "invalid": 5,
      "last_attempt": "2026-08-20T11:15:23Z",
      "last_check_status": "rejected",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T11:15:23Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T11:15:23Z",
      "last_success": "2026-08-20T10:16:04Z",
      "lifecycle_status": "preview",
      "model": "gemma-4-31B-it",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": 29830,
      "output_tokens_known_events": 79,
      "policy_blocks": 0,
      "provider": "sambanova",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 0,
      "provider_failures": 0,
      "quota_deferrals": 0,
      "reasoning_tokens": 0,
      "reasoning_tokens_known_events": 56,
      "rejected": 5,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "sambanova:gemma-4-31B-it",
      "temporarily_unavailable_events": 0,
      "total_called": 79,
      "total_provider_attempts": 79,
      "valid": 74,
      "valid_outputs": 74,
      "valid_outputs_with_signals": 49,
      "validator_rejections": 5,
      "zero_signal_valid_outputs": 25
    },
    "sambanova:gpt-oss-120b": {
      "cached_tokens": null,
      "cached_tokens_known_events": 0,
      "called": 2,
      "completion_percentage": 0.0,
      "configuration_status": "configured",
      "current_completed_tasks": 0,
      "current_desired_tasks": 78,
      "execution_configuration_blocks": 0,
      "execution_status": "eligible",
      "input_tokens": null,
      "input_tokens_known_events": 0,
      "invalid": 2,
      "last_attempt": "2026-08-20T11:15:23Z",
      "last_check_status": "provider_failed",
      "last_event_name": "",
      "last_issue_status": "",
      "last_overall_status": "",
      "last_quota_observation": "2026-08-20T11:15:23Z",
      "last_run_attempt": "",
      "last_run_id": "",
      "last_run_utc": "2026-08-20T11:15:23Z",
      "last_success": "",
      "lifecycle_status": "production",
      "model": "gpt-oss-120b",
      "oldest_pending_age_seconds": 299744,
      "output_tokens": null,
      "output_tokens_known_events": 0,
      "policy_blocks": 0,
      "provider": "sambanova",
      "provider_attempts_accuracy": "mixed-inferred-and-locally-counted",
      "provider_failed": 2,
      "provider_failures": 2,
      "quota_deferrals": 2,
      "reasoning_tokens": null,
      "reasoning_tokens_known_events": 0,
      "rejected": 0,
      "runner_failed": 0,
      "runner_failures": 0,
      "spec": "sambanova:gpt-oss-120b",
      "temporarily_unavailable_events": 0,
      "total_called": 2,
      "total_provider_attempts": 2,
      "valid": 0,
      "valid_outputs": 0,
      "valid_outputs_with_signals": 0,
      "validator_rejections": 0,
      "zero_signal_valid_outputs": 0
    }
  },
  "queue": {
    "ambiguous_attempt_blocked": 0,
    "completed": 234,
    "desired_task_count": 1950,
    "execution_configuration_blocked": 0,
    "leased": 0,
    "obsolete": 2658,
    "pending": 1637,
    "policy_blocked": 3,
    "quota_deferred": 7,
    "rejection_blocked": 1,
    "retired": 540,
    "retry_due": 65,
    "temporarily_unavailable": 3
  },
  "schema_version": 2,
  "seen_events": {},
  "seen_terminal_events": {
    "001f77cbd98526566b0f57ba32cfcdeba984de9b3172ca7209f8a92d23b8307e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "002b04035d41235aabbfe7b88c0aaa7a8d69b1ae4b33fc14ea1959223b5523d5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "002fd6ab36f77051cecfe0ca2eaaf0cbf0172bca43ccc9006f544d18545df5db": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "00e409297fc173788528b9596fa8f5b152e5595e626d1cf451719645ff1bb28e": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "010ea49dd05193431d2e9faf73275aa21335e9e86f92569a9f9266cf13951301": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "01118120299604135fef7779d0ea01c220e7a0c9907ac23b4520e93acc29a925": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "01229bb084e2c981d056e6292677a1570f7598d66d4a2dab0663ee0f6c03b744": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0134fb38e245a3290127d44c6f30bef7401c62844bbab025d2a10c17156a15ae": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "015a7f3f6217b9b2b3ec16c5b83b06678ea24edb5a54aa344135ad1462b28998": {
      "attempt_finished_at": "2026-08-20T10:14:53Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "015b4cf8770f7e7d5fa5403eac67cf10950466ea52d1bb3de7c6c3c9e2f22d09": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "016baf2f31ae794f9de7393f924914ea9e5167d0fa3cfdf3a6afe7e7d70191f2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "016fc5f238e8544ea5677a39c84b7934026206751032ef443e789dd72597c7bb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "017d60d449cff6456744a2961e71f773ed0bef350768272d0fe973709a81f073": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "01c0aaad707fee952d6ca1e49d747be677a926f7aa1bfde8b6da902cd2959ca5": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "01d0833cca67b2f8dc003f0409c082d4ab7a3b68a4dd27c1417de4b33310c7ef": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "02507512d83b36175c5591976377280df65399675029ce8d9674b703f124d92b": {
      "attempt_finished_at": "2026-08-20T09:50:42Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "02c6ebb25327e23ba17d22bffd763a4a28e2c6630d6e9a5988938b35979c0a9b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "02e022450c3a0f055f7189fa464481624b90fce8431d9b944556b43a2d94f270": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "030fc538e9ea02a7afc3626f8604743518b58eb1bf665f812604f078600e325d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "034d0795e974f0fe80083a913d499329202ef873a38dc45419279b77bd0c0078": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "038b745154fe0c21b799a050c874d2dfca977e6bf07cbdcf59a2a28dae3d2943": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "03a072c3c67c26bbbc39debb403b399338b2c1d461ccaad774f4c64869d71330": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "03c6d197ea015cb379b22369467c4328b8e1db31c184ba169fbdb111bde3e5b5": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "03ce06f84a83d285a97f7d768576ff181f3788840f6633a8be99d027f49d65f8": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "03e47a46e5d956d83102126f6a0239fc7cef441e8b8059b450a7b3735f4c89f9": {
      "attempt_finished_at": "2026-08-20T09:51:32Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "040045fcc0ad9cd848bdc01d25987600f93714faf950f6ff58bb599a185f3888": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0401457252f45fe9ba93c6a2832c6809b1cb7b27bfaa77a0aa19d39092d93c50": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0407dec898cec884cbeb80712212ee8f9e51c8d863b67760eed4389f3c1422eb": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "04326ba761783efd728218c649fa1345a079dba8229bf559bfb292cab32c9b8a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "045ef89d5b22ebeb22cce4869ced4e7750afb521201342bfe28b5d04bb66046d": {
      "attempt_finished_at": "2026-08-20T09:47:53Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "04931d69104895b2de9a6a39383b6ac9db6f967770910cb35adffeebc1e05c0d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "04951e975573d239314969e4faeb425457f537a5cbb7d494a6b88207d7d06923": {
      "attempt_finished_at": "2026-08-20T09:47:33Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "04a0db13940c6380973cdb4e5864c7f34a316264137d1bede5f4046a0d1be916": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "04d9b38eb66d79692e1d91e1d506fe96204fe162bf5deb815a8cf9aa2e721503": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0501cb4ff7c8e73c79a05b031ac196cba06df34f4130388b3638627cc4c80275": {
      "attempt_finished_at": "2026-08-20T09:49:56Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "051427aee689691c083dac19e354e97765d9bb5e15655ae3a6d746f4647eee86": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0528f568526ee7d56ef3f9b586bfaccfef9b5395f6bd19bd6b20bb8913d54e15": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "054a55496647eeeb7c2f9413c49fae44c71839805d3a2c02f41a32a320ea6948": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "05728e7db5f1f0ce7a4d27d63a202844c75da67e3528097d1c4a1c5264ef59c1": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "06065ad2ea8b2c321fcc482a2561c25ae74bb2e4892ef50ffa3fe44ca825584c": {
      "attempt_finished_at": "2026-08-20T09:55:32Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "0639f7b21c0f436a52cdea3b3472627854db6e51ed22e31d35e21582c05d13cf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "065bf7bf2b7f5797d20851579f107143972b6b0f17a7bb5ac419859f8e849c2c": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "065ed09b3927ab728ff90978785c1d0b22f8118f6c87c5654ff35411be4f8eb0": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0679ac2add1f5763f1b20abdff8f6fae1520286ecc188cb0e676525680a0cc15": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "067bc2e1804b388879901590763c72f8077dab8292d6ff23badba10d410c72c3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0692d02f9ba712d7585b9b3dc9fdd90b87feba49f4bfd1e47e070307f9adfeae": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "06a51ba30dd846e53081ec0b42bfebe2ff5a06edc960e7b15ab07eb986e71a27": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0737d6aeca401146232fb99524d821965966290376f5b5b79cdf97390025aa5f": {
      "attempt_finished_at": "2026-08-20T10:15:51Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "0774848fc5c111a3517f4edafd5d96dba115ae00bcfd1609f3687ceb70bbf6d2": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0798edccabab51285be78909a3956aced84020aa40a394b5b5b79d5ceb5861f0": {
      "attempt_finished_at": "2026-08-20T09:56:09Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "07a263cfb9f456be46704602903edb935c34a60e00cd209319337f7ac7fd5d16": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "07be43aec8eceb4daafb09bfaf42062b70a46f65fff70b23a095f7e9378a967c": {
      "attempt_finished_at": "2026-08-20T09:56:00Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "07f88debf58920501f96f45c2e510949055189e775568e261c71bfac3655d0fb": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0839553c2badf33fa4cbd9c8fbcd7466853ec24c6c650c93a52b04b5307d7a78": {
      "attempt_finished_at": "2026-08-20T09:52:12Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "provider_failure",
      "provider": "groq"
    },
    "083b3738053e58596ea0f3cb0aa4a094fc930f0925de774e2b9f14250c5ce4d9": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0899e018f08b079c7577846284e8fa589de26ce37542ba6604daf7b0dbba7480": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "08dc8d13065cc858d600e21ff1439cc3137f3e2de9670c838d1926f73fd4ccd0": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "08feba51904094401bceecc978923a899a53a037fd99c30e9f4c4df4a6d0d621": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "091cfe5cd1c67dd68ca81c5367e8140afb9cf6e816c0b2725e734084d2747d77": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "094ab9b3e6b0ec221f35bb50509d80fd62ad2bf2fb2165660fdd6531f535600b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "096e0753259e97f3c8c2a486d108d3090cf388eeba88774395bb38f27da026b7": {
      "attempt_finished_at": "2026-08-20T09:50:24Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "09af091198c71172c2a802a81f0e56d72d10c3b1d11a54f993e939a1e5f5a65b": {
      "attempt_finished_at": "2026-08-20T09:49:41Z",
      "model": "gemini-2.5-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "09c9e3ce0790657315c22d8c082cecca492a727f6d6c7b79e5c4e4ac83e33106": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "09e0ee8bbd03b3cbdac330180ba3d568a00c3bd4c1458ba72c96115593f10d09": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "09f64f256a08961899299b88b28e62bf360707a9293827cc9bacd395dba721c3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0a1834e380c00daf1583a8989cc9f5ee66c16dd6497edba1f0913adff7fb91d9": {
      "attempt_finished_at": "2026-08-20T10:15:07Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "0a331a0bafdd4479202b8ebb487e7c2b2507912aa91d0a52c2720239e82ed4c5": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0a6c709c09718a0f666f798ab7f983b6b542e6afee3b079e937a561a7949a61b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0aa21ae6ab93fdd230a4227e31a506d0b1f9151123b2694b9efffc9f72e13334": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0aac9f1664a0a56f864f34dc479949d96a30eb60da0dcf408bfe4dc242715b4b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0b01160db9c25cac6f362a45e80b0490f91fec644f52a12cb7be48f2da24e7ce": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0b5a402881bfb4e26e2fcdb643f9ba3efece49296cb90f551a2d5773d1ce51ab": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0b5e8f6e5449cb3795160acb835b9b0f949d8cdab90d8087e36385c779bea35b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0b7b4b3da3bcf16691d48a252bda6c0a45c24c743a51df5c0d31c8c8c388dab1": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0b7d3581b71a3c641e61b7d0b556df47191d14e4751c27bc1c374ae7387552c4": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0bb6206a1331e14bd546ca4cb0f3a97b53b5e7d1a2525833c7ae134cd5a424a1": {
      "attempt_finished_at": "2026-08-20T09:53:37Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "0bc7940921bc934943cc2de0dc441261ee0b38839158c5349bc73cb6271fb172": {
      "attempt_finished_at": "2026-08-20T09:52:15Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "0bffbff18f6fec2be37a00cb5dc9345d850bd0899ee7243ee24d4435d4bbdde2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0c07e19c3de0a8d233b30bae0598b42490f48573641b7fd560d816b05e8063a6": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0c6197aa2802b77e7f039a183d2261169a4d0360926f3de2a58d01dfd40c73fc": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0c870601af3ff46f29997006fe4a27c297d935c035598de078a39504251ea9c1": {
      "attempt_finished_at": "2026-08-20T09:48:06Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "0c99e6cfd4fd3e165c14c3e6f0e69ff117e0a352bf3cd265964b0e384b5d3589": {
      "attempt_finished_at": "2026-08-20T09:50:49Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "0ca05bc8f03723d059c143a94722b3f78a407852a9e2e1a3eb0c2b6134f697bd": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0ccc21a25bd73f73c4625b052f40b4bd6da77b05348b4dc462f9bfa42c43dd76": {
      "attempt_finished_at": "2026-08-20T09:50:47Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "0cd512bd4c96d4fc7ca5d1e48cd7e0f3d35f0816375cecd52e158f810d84e8d6": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0cdc75f0828ce7d9029445ac11925119ff92acabd42a87f712e3de52cd84d702": {
      "attempt_finished_at": "2026-08-20T09:47:16Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "0cdda52ce2e80d3155c9be97c0af7b7629d2be5b0bf4b1ce2dd5912acfc692b0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0cf3bcf8ef40e86c37ba994050bc96722091623a9056bd75a9148e0cd9d95887": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "0cf47cb0d093244125f8640f67aeafee7c05870d3e245f254443ec45d6b1fd90": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0d22c82878ed6d583a9d9da0d5014e5aa4cf1936fc085870420ab45feda1636e": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0da8034f8c8a8eae7cfe44729111601f30c0c0462d6847c1efb576a50eba75bc": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0db6793abe0f461fa48fa62ed074d96aaca80518364e54b399aea4ca0ee5206d": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0dc19793e67459d666554202de5790504de57a7fe29a33e4829669cf15544d12": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0dc651abf95f2ee89d9473f5ecdaa48e47e7aa8d7f77e596cb012861a53783a2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0dc93cd07fb1a3781707c7a688ba2dfd4bc547b124da5129da7773c74404f2ba": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0de46d4b317d6999fe43b1ef705cb4e4185b4dd2e1633dca21913d5d77ed78bb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0de736c5fc2765ba1ab70c637fcbea569de8ae407261265b00891a06ef07236d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0dfe66e7a27a9781104b58ef8116b00f0676925bd3880b8e01138e2ead5c929a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0e1473ca7bf936689d1c52fa19421f21198c52b0ec948671a082ba7e1ac5f0d9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0e593aeab12b7d18f434f6032a430714e7e10aab16128d516ff42ced467c7740": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0e7196de4062ea218ceba18110b8c55b9cf9d853da6e756106e5d12cbee6db89": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0e8265c6184b9ee859b53111ebaf5ef270b9a7c96467706c0946ffec31c24071": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "0f1f65391fbedc09f82f055df9c1828665036c45131f719f29ebbcef365ef167": {
      "attempt_finished_at": "2026-08-20T09:49:59Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "0f355c44e792bb75033469e9c0212b6e984143d0ca515883f6cd529a0fa51dc9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0f47892f1e9b12f8e96b536a3814c263efeed102de5e2398c70fb6e15ed4f8e6": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0f6c00a64ade5708c1ebcd0068edc939fa7a2d73f50778a70023bb372982c120": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "0f8188206a1e70498b8cd252d39e23e984aa569832de1da04d31582ec52d0703": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0f942d8de6c5a5f074ab8a1cf5d1c5a06d2150335b7c9ccf4fefe837e81fa308": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0fc0b6405acbf48a1f1dd61fe4098589005f475cb5bf07e794a322e4466c5864": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "0fc3099e646c6e131dccb09f43fbebcfdc812cf46d55dde59d26f041dd04542f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "0fcdd1bf7aaccb8fad0989e2fc7a68be364b552dbb06055f1043c64dd60c5e46": {
      "attempt_finished_at": "2026-08-20T09:49:53Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1019743ed50dafc615943084e571e50cc539b5b664e8eefda13c80a002801033": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "101b7945f29726ef1d6c8f42472cfb75f8edbadb0f3dd8e6e589cd31a0f51486": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1037d2730ce0765b00cce8079001b239133cb7db8c2ccebfaa16db82fa70c348": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "10a7ad006d02ba95eefe699c00bdc61fdc011e023eff66ba68681a5f69a17df6": {
      "attempt_finished_at": "2026-08-20T09:50:52Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "10b89c5cf875ffb9b2c31e4bda4d21eadcd3234b7f3de0d6661fee7d2e8000f2": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "10d2c087d2f056d381c2ff3bbb4acca4bfadc5667f71ce5a882f1a74e00512e3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "10e2800d9504edb29a4e8e1305965434c1f440178123e43f05ae1aba4409331e": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "10f0f0b3bc495320cb538ce791f87fbfdc12fb0ba06394ab6b0b97b23c62d6e9": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "10f3f7a528493326687b56df0bcf8f68aafe76fa35964cd54e0207394b4a1b49": {
      "attempt_finished_at": "2026-08-20T10:55:23Z",
      "model": "gpt-oss-120b",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "1157ae46320c398d3953936d1df16a5c038d76e977677048b928871de6c54811": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "115fcfb11ab4eb057fef5d003be7de8b95fb79de82a8ef53c70f951274c7e6ed": {
      "attempt_finished_at": "2026-08-20T09:50:24Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "117dacf9541a16df0820165ea93e2e161bfed071ac6f25a5a2c80dd7f443625d": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "1192c7f8c364d11114507b5753bc1cfdd193bf9fd3aa4ab3de51cd433c0e7eab": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "11d28d2e1ae23e048de5049f0a0276b6224d6247e65b08771b725e8703b9c1b2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1203defee8735b083f7735639f6feac705f1a397bdbf4159e4b1c4571791a4bf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1224bcdec0bc08da5a1fee7283c6930ada19a5e43ba3f866c5e0027c04a4226f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "12a74f9aea2e6da54f17eaf29c32cb721390d73e9c40501c3d03f30c1824ae5a": {
      "attempt_finished_at": "2026-08-20T10:16:04Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "12ab0e7aa8371749841605323fac30618b67fb61da2ebce277b34ccf1bf6951f": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "12bc6e4feaa3cce501ff47e3d50d5997506cacf16f5c69c40e6989e4a03d1965": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "12d03e75e7d29058a89a1d6e359ba605ddbd0ed706e588096c2782f52f721227": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "1316f7910515f5bd577df87efe7c060618c51ff2fc12af6ec031ed8817d870e9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "132597aeef8d2b0d20500799e57fa800476784b527234948c627fb6fa80d6566": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "137a02482119927ad16cf06d4fc2f5665bb92a39a480c6688deb8b66d120e4ef": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1381b6fc3eeeff3f3a5661150224cdb9610c381cbc2d562a1cbf94025725012a": {
      "attempt_finished_at": "2026-08-20T09:50:21Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "139853b2577eddadb16203c7ffd230e4bc79f657f979f42c3865763e84d56e31": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "13a346c923cfb440dbe26719bdafe87c9fcd733b5e4105c52833ee0637fe4b4d": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "13a4f3191109ccccf1abfa8ddee8eafac38985f8c6b93e8a0275afca71b8c34a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "13c6a210034823a77c2a8371567ad0c7461cc6139060f3dcc88be840daa39890": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "13df368248c84e8c965f5cadffd98341833315a818d72ba7547d8b03c133a02f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "140c2136bcb145a2eb15538e0af7c5503b1c82df3225d583d093f7ebc4d3f465": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "14a74bd9e5201322f76c61493f5fe8edebda9a3c9992601180f46e9a1aae85b5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "14b0c617ed386a306899ea3c8da53c12ef5ecc7c1cdb79cf5634b9adc43f38c8": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "14d11d99b439991a504af31a53162c85611b44d59c724f886f1e06fe1dc6059d": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1552bfeed8ac0c4a7b85e30599b0a435d4a5380c9393cdf0bd4c9304e396fb9c": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "15705ee13fe738dd7933ea77a68bc68f1dff89d039fd89124e1716283b5f719c": {
      "attempt_finished_at": "2026-08-20T09:49:56Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "15880b4bebeb763bfb1b5468a7bb51c13777811c62743cc35a716f552b4be9e2": {
      "attempt_finished_at": "2026-08-20T09:50:36Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "158c5de6f4edc1aadaedbbfcd5d7747c8e0fb787cb21384cb7033a560df93b6b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "15b6f50f8aaaec707510cb365cfc8fbf628ffe0e53091dc154546dc20d2c921b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "15ba2057f8ff17d4b8dfb03590e1e30578c7a72e4603dcd321685e15dc6b0ab7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "15bfb1f166b8ee282c3cfb79b16b99abbcdfdb72e2f28f4534b209e5f8377f3c": {
      "attempt_finished_at": "2026-08-20T09:56:43Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "15c909cf71403895ff02d8d9728d6978765096a1f0be770035643ffa1740f0e1": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "15f7d90fed34022e5946eaf294cadbea0f466d39b3233e50c423ce5f06cffec8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1605c226fb34212c5f7ec1f01ee74381c7933be2b547a8da65f26d017268bb95": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "160d6a4fa645226bcd44e3080c1c10bd2a696d84652f519115390c127075728d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1616d5c37eeed097edb10d0a7a2e1baf06a282486a54c7c74adafdc6ac8014d8": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "164c1537be597ed1f28b5c106db7f584d8baa22cf260a45e1db063c16c250e58": {
      "attempt_finished_at": "2026-08-20T09:52:38Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "16752cc24409abc292d2f0f12ac684f694df399f48f4d9ad84547e4db0f30581": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "167afa2358c7ecf8c80f193ca30ed5a97d4ca290b8e149a52ca9306e678c99e3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1681b6707133e136f7e584cd7f98b6061ca6843fdf719a9886fa932a2a563874": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "168314b75a6e00b2e34115bc15f42918da421b9f443708d724628b2f97742213": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "168a13545810196a811f50c534aa996d3791899ccaa16146d27ff025e088b0da": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "168cdb081fadf0aed8eddec558277318d0a095e4bb5829bb0d05d48af05ca86e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1691e7f8abc1e6f514b63b3f7f3b5fed07df13a88e51d3f7431efe689bdbff4f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "16d4fa30c4309205c5a5433162ad87b99b9402ea9997281bf64038c3d1724f7f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "177620e37711befbe6c4ece1930496639d778cef9399dcf3a32a6340cbbd6364": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "17779e2ac037e369ed41ca11ede6347ca193c8ea4e150a4740785f272f6f47a6": {
      "attempt_finished_at": "2026-08-20T09:46:43Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "177e1b889e6f7c5346cc855e2e642ecd3fac5cfd41e30369da641ca169b062ba": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "17a15a3d8358d5deb2f10a5e2c1150aaa3b87aa5343a90e3780a05d5205da0bd": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "17a7b03cc67f722c177ab9460a90386f5b9e0cd18bb3d7b5b086ec0a21a2f42e": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "17dcc187f72bba5767509d359aaae25f99cb2ac89dcc58cc88f43c170582b341": {
      "attempt_finished_at": "2026-08-20T09:46:59Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1818bfffc70534c72410d6cd12330eb0a7a92e028679cde3e36daf1482b72b4b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "182e0e80846cf50adf94ca3803999074ce47066ba5dd8dfc1fa5b51d006579da": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "183571037a7d6dff4317f1979bdf6cdaefdbc412b285dac187763be606d37fcd": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "183718e38aa52af7f2b04e75ad35d8bb08d680489ddffb76ae60a437d3033873": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "18526c4aac738af674c36135be45087124c15003bcc923b7761b9a52c89a72da": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "185a53cb570b97b2b43d709711e602c14c3f90007d00649102d1e0e728ef523f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "187dd855cacebff795ab4cea3da5364da794dc9b23262da3092a2fb207a62d91": {
      "attempt_finished_at": "2026-08-20T09:55:24Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "189062dba674398b8e76e792fc5e1043bd4598f5bbee841eb51cdd933c31c512": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "1891ade5d79a54eb7c98c383b735d49b65facf74309043a6c27a37e4f8317f52": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1937e44d4b63135b7dde9c4a0a99f325d0ce059a100feff11881f0cde7e5ca02": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "193ffb131a2c873e3eb2ac817273be4e2442c525eb4cd179f3bc4c40847a3241": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "19a1b88686247e78d15cfec72fa3482a827fe14023867d91bc4a55ba30e3d0ea": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "19e2034cc80901dbaf42cd8308b18b436125709022237fb52591409966f86cfc": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "19f2644eff08826eca0b0f342ca58db66c9840d5984af69e5c8bb4bcb4f5f82e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "19f3d842636c7739de0bebe852160104cff07f0f26d212242680ee73e9171231": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1a01e2877ab44cde6a7aa5c4cf87daf7047e5aa25bb9d1762e22af617286fa6b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1a4b2548360573a4c184b06a408842ceaab27c2eff0f5963d5a3ca82e50ecc8c": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1aec9b91e3f157134fdbeb2ee0e459f04410ff008557b54d7ddb34d34a9b59a3": {
      "attempt_finished_at": "2026-08-20T09:50:02Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1af8b3f6aa25a3f7c8d75b0292aa297d7b7c2734136749d39b4dcc8d30116d7f": {
      "attempt_finished_at": "2026-08-20T09:50:33Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1b09cf0510843b9c6356f10664c197c3c816add92f6cb669d77d2361016247ed": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "1b21a952268bfbefdf0efc84679cd41fcf2344272fa974e0d2415ff3d67526df": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1b41ae5bd1b9cd0f1b955285eea024c4aaad5e7bffbf2766d85df0e7f16be1cc": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1b4df655623889f714f370a7a2acc8bcd74bc4ded788554ec3ebd89072ba4cf8": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "1b5759a5cf0df88b2fd42936c39f2acf5a65f1eb2bdc1c2dd9099af4e5dac3fa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1bbf324aafb14aa68d29d695c24bf4694898f81f1b9f6037c535dfa6857a8110": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1bce6150aaccebe386efb4281575c32a0436476eab835f3aaec03f50ddb5c7ef": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1bf909b2e413f1ffef323a9d7d58a89a6fd5778a3afe1f701eb8f24d37404d75": {
      "attempt_finished_at": "2026-08-20T09:46:53Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "1c0e0cb71a8c18805bcc5e1351cea9112ed827214fa21669ff701367165f518f": {
      "attempt_finished_at": "2026-08-20T09:47:49Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1c49c20661975517e0baba36cf9a5e2b5ef8a3b28f57cb18daeeeec0bf7f6860": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1c986bc6a8e1aed0e21f5fe1c73756b1c8685a3e6b5d9211f7f9325992bda58e": {
      "attempt_finished_at": "2026-08-20T09:48:59Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "1cba4f5c1e23890611ce1365d0951db53cf582d7711f19eebdd085de0465c5c9": {
      "attempt_finished_at": "2026-08-20T09:49:44Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "1cbfb8f9cba00a69f0b9b037ee645d9bb4561d695c42c90e1ef25671467e24a4": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1ce71572d02fc325cbc0cfefe704f4ae50541225373182d457ec81427a6f5eee": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1d30ec1925978536b9c93fde9e8ba47d98f4c709bd789bd1b3abace78299cbc3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1db0c61626f83b857c6f06329d9a6ab147adf3837c98c39ed78fa9216bc3307d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1df72237b68e9f12aa35ee533f055bf9ddfd3f0facab1b404133b18614f47445": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1e0565be948e2d31ead5a990f2608c8e67de4117c21ae0ad591c72056d4fd457": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1e2683015a224aed8b267cb23c6ac8f0a82f8c459e7a0fcfb05fa59f504014d8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1e53c9c4c1a4fb91c35a98bfe3a614a3ec666228bee39229d1a851563f5be570": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1ea26516ac12dc514fbac74b549fe091ec1f7c1d8a2c69be72ef82810ccdba58": {
      "attempt_finished_at": "2026-08-20T09:49:38Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1ec3f9e3c0ad3ab1a215918903f8c390bb01529977e620ce7521658003a89510": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1ec8e5a3524775e217161a1d4a6444f8c556f80724530fb3e0ee16d5b92de3ea": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1efda418a8deeb949044aa30bd47f327760f6872bb3a47abc529eef1a8db7fdc": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1f0f526981f0b2dc3907ad4603fec4ac5e4d70a456a50d546cdc91a49c9d9771": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "1f2603daeaf2f2d002bb26848243faee23d68641dfff6356b21140aafd0dddb3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1f3a413228ad9bcce7807d6381e226fe3cc113e4c1be030060176413b611e955": {
      "attempt_finished_at": "2026-08-20T09:46:55Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1f6e9375bbbc2d97016090a93fb6ccbc85e3fc92b93f8709514e68b16efe2ea2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1f78abe82f53bda9b10d5618437e0b85a524a83bf60ae332be51af32d8c5ba98": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "1f83c2167bb8c2c3dc14481795bafa4a1f977bdbd691712ea0d0ea77c9138498": {
      "attempt_finished_at": "2026-08-20T09:46:10Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "1f945018fb2dfd83d48144ba932e3cb71b36a6dd8827753ad7b7c6d922c01a8f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1fa0102bd14014c1a33fd4e842022937a48027df3a16b6ceee868353def6f224": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1fad5a5f2d1e9ffd573f4a94ee4092a00ab3d10f9bfb241b58acf6c3b7dcdccb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1fafdda3531353c2a1d233b2dee6023c43cc061ddd44170be6c702a74db939e8": {
      "attempt_finished_at": "2026-08-20T09:47:27Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "1fd524cceb81d3f5b5bb86e55f7959aa74c485e30984ffe69ffdc657694bc04d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "1fdaa60814e894a0982c30199d56319f6a3a1da98528818024166ea78722643e": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "1fe343bd43ab39f42a437c79e6aaff6b005277b3c1613cdfd84fa9f1afefe081": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "20394989f92d518c3ca0640bfed1e5b50fa57b801aed3de34d8351e89d9d949c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "20574fb8aa56a95d306f5569e2e1b3080bfe8b651ac850ea68e9cfebb5b1db69": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2076053b7b98663268bdf8edc57c41e135d8a27e8bffacc4a885acabf0673a4b": {
      "attempt_finished_at": "2026-08-20T09:47:35Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "2084505b5c59ef1deb48e6296f1625e44abb7c4c836808fdcd210f0c95c9f691": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "20845368308a672219b06ff98db1276e400e01f68d9c7fc4ac42a7b2155de5ef": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "20d8aadd4536df475a6baabc9fceaf22c2ddd1dcbf94c216c9702846888ff62b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "211459a50fb0b569a95c2d00e77ea33cdc1874fc78ddede348eb1eda155aa386": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2145ff632ed261f7d726360f1f557335a08a35a4f90ed822b30790d3a7345e48": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "218bff4a2766c8df8cd7efcdc788bd04239f8a881ec7d5bc551b8aa0160308d1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "21925f223174481c7797e4072d3bc72f0b875f5bb5cf3ef7e6709183dc46d105": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "21df39e481b621d8ae6210d700e8b32b5c1df8290475f5ab0da48c2983630ea1": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "221d73d59ceeb0c09e8a7b6535087c4e733533fc94aa1c6ca09d620a7554d841": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "222e01a4a9741d75aab34d3299fdab62d7d2fdccadb91399eecb8ac01cdc23b4": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "225dd181c919eba4e5074af8ab1b6533368f60f66ba4e77fe04e93494ec49c7e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "22659fd761910f8b5c92fd50dac018160ef4f6b8115f0f3e21b31b9f6374085c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "22d6d28e7d3f0af9920145310137fd05865e663316d0860b3829002e8995dd89": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "22f543dab85f23a2e36c330821014b06b72498bca33e3e7638adcf82e05a60a2": {
      "attempt_finished_at": "2026-08-20T09:54:23Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "232556b9efd6b9c7acb0089652a32c1aae58a092ad2beb421b5ade148f13b02c": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "232c0d80d7bbc0b8855e5b55197569e223b78f15e1e05e7115e1efa3c54fb9ff": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "234304a3b8ee522446cdb98356ee762521c815dbdc50083fb8d01170a2167c8a": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2352a437ef62d28aa940b342dd39f4d7742b1d070197dbb68d6d1731ae4b8ce8": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "2365b8485c008bf413cde6346b2ac4349b12bbdd0d0418506ddc336cee610523": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "238f74c7a6f5dfc6f2825014f44d732fad292a164d12ef84166444ae797fad72": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "23bdb1d3443e2955364a26a5eed44fbc85adedb0ac7db3455c33c6f0b54b78cc": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2427e7b3b2fa740148e1083050469c5eab68ca28d1153fc8b135c4c4c39197bb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2468ef126617659e8dccaae8623739dc8014cd0d59cd0c29a51dcf93b1d4f0d4": {
      "attempt_finished_at": "2026-08-20T09:53:28Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "24a6cfddece76247f6392aa8fc03b083ada3acc1f429b30c99774b22579cad22": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "24d6fb777e455535baf9b9a455de07bc341ba870ce4ca9985bb472cc868a1761": {
      "attempt_finished_at": "2026-08-20T09:56:37Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "24ebd1a029884ac50a1824c51e4d73d985d21c7ee16afe811b84ef101ddbb00d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "24f4edcbbbc7cf88b837b01a0141ed5f7f89f1a83b4483c6eb53dbb600e66dd6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "250b23047fe5b8e1bcb55064a010a1681c73988e4e40330c4e0ea9d11d66b9aa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "257409d4db515191b42c1bb9ddc5490a416d11178c0d8c6844cf58daf37baf59": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "25d085a91a61674bdef32e1e8054218f62297e70296755ad76ac146adec77444": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "25e6b742c5af3438dd73b092ab6c3090e1bbdffc60d7ea570b4e6ab95acd6a07": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "26958c82b80752ad76145cabe6f73db2eb4aa3e39bf5aa5a6dcf429bda9c9945": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "26cd8cf648b6952e1f9cdc9b7b9877ee0f2cdd675bceb94d9cdd5ba89fdd0e04": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "26d31c559ae1202350d94fcbdad842ae24d8770f4071b99b588f629e8cb054fc": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "26f6f104bc1a310f5a68f0c6c4c63702f618ae2ce500ffccde7c032b953dbb14": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "272c95253a9af60abedd365793b78c0b48de592d048c9d026e18cec0f9ad249f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "27807d3f7502f22b3b7d8554cc1aac9eb8fab36e55aaff8f56d9256e4721a4e3": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2797a00a73420a173e845eb1ed87aefcfd20d87d638e79d9fa1d332e248a432c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "27a5f8d9a63f146b3d3d3ddc62939021a4c04c1f285c0688001abaa123605c4b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "27c28e692bc45d4df20c7524ca5ddca840a3b0ba0f08dc33f39c9bc2f5e63a17": {
      "attempt_finished_at": "2026-08-20T09:56:52Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "27c964b4a3621badb6e39c854fe70578e53fe199a863ced11b8e4dae4e809639": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "27cc25d7a46548fd9dfa5afb178118b0e013bffbb2168391362d8fc6e965a7f2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "280bb7608138911aa90be50cd89219335c0b5b696a5d5ebf0a2a7d2ba4ee684d": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "280c15741a0bb6bd864ed7926e03c74e7d4c16f07d5c8d8ba02f95d8722a0799": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2820ed294c9adc6c65e2c904a2faf40e2b2f23e180a82c2d828c0f2202967029": {
      "attempt_finished_at": "2026-08-20T09:54:14Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "2821f18c31bb85aab71564a1ce04126f99be7b3dd0a49e2ecc39500883d2c022": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "gpt-oss-120b",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "28654444355db3d8152b63880e016c275442f46a9f0adab867930d6531b4471e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2869366598e0df4c359df872a45f847b7469b96384b6fbc332ea32edb8441a8c": {
      "attempt_finished_at": "2026-08-20T09:54:38Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "287f8dfb3b6517ff67bcab0923ca4b9c0e6ececfa4b4865b264a84695d266df8": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "28915a153aac01f2539c2e2e73c346a3d414d8b13d21e46486c35ffba05d87a0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2891b70c5693d1ac9f5f9eea660050d0a1feb58873a55cc3155afc6dc48079f6": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "28a070b13c4fdc5e0ae8783ec71b11baa0dd90a218fbde430a88557a48b5209d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "29135e36941a3d3d38f2822572e7b0525f3c06ef9868ea085a6110e5c85dea95": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "29485a005ff26d3d54dcb0c9b947bb855dc7b5305c59915dad1cf208eb9bce41": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2975f200992e605fd13f42033196117462fe1a928eaf501a713c568672af3199": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "29984c00d05987baa081776478667548de2f59ac9de3c9f5dabd364b08edc2bb": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "29ac9ed3c50cff4a9cddb08830d1112f9b4594e6ad5bb9cfb2dc5401fc13a9c5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "29c315c99a4cbf34ebe7ee0226679af682122a721a6b293659c9b139c16a72fd": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "29d44f0562a2e93fecf1d44250c0a22eba40f1776c70be9b0ab2069b36e32250": {
      "attempt_finished_at": "2026-08-20T09:51:38Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "29e110217a5cdd24447c028dd33df995aa462507f4bd027ec31bc6004c65f19a": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2a0751837b5643bcafb4b7e3f2278be6412f02b929620e026fe373268494c62e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2a13356dd67a9f29bd2c58274ac34c54b354e4bb7ad9bb46eb1cba51ad20b41e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2a40362d532af9c651c51f8214f4ba6a4865d5bd1f1096320d3c89d0757fe8f8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2a48f45e75a6df0e58027c4cdaacd2b45c610a1a228bd8c635caf1ed440d5955": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2ac9bbe6c016db4551799f70d54a7475af323d5ba2afd39b4404b6282553a23b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "2ac9cc3783df453cb977c1d0e19352215c7ff4fa223f76479f84a3323341ede5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2afbd6fc9d4d027736e4922112b5a20ac5983d7deef770eaa716dfcb58b1f45a": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2b496b46b4bc5f71bdb50abcabb47225ab582fd155395373462aeae1b9455211": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2b75a1289f8f5d4e2dd2225c596508a748d78146011ae09762de25f4e64b1460": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2b88256c9a1e9271c98b53aac38fc27d8b5bb480298d21c8b4e6de03d241ca16": {
      "attempt_finished_at": "2026-08-20T09:50:45Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "2b99656000cd074042580770922e13510a530be9548bb7964020e74854dd29be": {
      "attempt_finished_at": "2026-08-20T09:52:05Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "2bcb94d81e826a93a033997221091c69e486c2d60ba2cd6940a099347cafcde0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2bd097c11007735f55eccef3ad59b67233a435e1890ffa62fb592576b2173214": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2bdffdff6f77ea3d394a86373df37938a03790e839e8eab527256fc8dff916a3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2bfedd6fcb860abd2dc3d1e3df8b600e6f7e8be2a9ffcff144fad759e9b95650": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "2c4b7331f884ad7270a507d2d288f9393ed7b1bb80a67abb6b5e5011b7057b42": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2c5589046d082c9f60af2b60f06b10b52c99e60f9b748b178f8c54e6cf99a7de": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2c59412bdea56c37ec983cb14292106f29a643502f84687d9ab35cd589a29472": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2c59977d290233daed0d76de8c1605bb377ae93435bc2fdfa3841312aed85c6b": {
      "attempt_finished_at": "2026-08-20T09:52:23Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "2c5fb8fd6eeb135ef73047804fbb92ca3a1719213ad16f44133cbb08894bd2a2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2c92f15b05100b2259030231e75861c80dee28e6e04d54a3cfff8abd8c4f658c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2cf330ebcc0d8bd3cfe52d4fd88f1696274e046c3d5e4c1e4a455702a8331648": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2d10c134fcfc7c9dc3bf55aaefe3c44e3c8039930ef492af018ff1c4e7a28fcb": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2d99a69c3f64aa76d49ab709a43a3b86db02bd44ad411bf3222245a0794d888b": {
      "attempt_finished_at": "2026-08-20T08:58:17Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "outcome": "provider_failure",
      "provider": "openrouter"
    },
    "2dc4ddee69d36996b88aa985fec5470821d1d2c56a41d151262eb4cd86e2bf1b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2dd0e379fba4ce6cd2668b9c0cfc292feae164b47f8f6c2ff35806d1cd6a5f75": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2dff33665b6044054beeb5a5977dfb4158e88c5774f0388901cc5fe62487c54f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2e13efd7bb0352e62d57fde16010b7f1452c51b6f61f169e587c67da8e17d1a4": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2e1efc39a40620c4c5c9cae5885b5ef0157175759aef9ec0221e4099911916a7": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "2e3b27e8571104cb413be8d0928df6fa10121c81987f2d5060ec19f5e372d3d5": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2e4f63a868169ebb2236d48eda07d9371da28ad0ea7234696b32e8b82996ceda": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "2ea148c4aa4030e29dfd6fddfa76fe223b362c51f0d871fba95b737dae05972d": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2eb3156e1641d4e58f94167a44559e1f8138745a96b8e7bab89d0c8b9afc14e8": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "2eb56b2ef18383b6bd3fc2610b38cca257eccfad0ed12f57fb2eb5fefaa6e2b4": {
      "attempt_finished_at": "2026-08-20T09:46:13Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "2ec73b92d4ecab7727cfbd62ccfc8fcd14812db9eb474fb31d578929bd066e2e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2f3d82b01979b581643acebb0fe1e1d0fece8098ef19cfd32041e3ca3ddcfe0e": {
      "attempt_finished_at": "2026-08-20T09:47:24Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "2f7ab17fa20ce3f376d21a76ecabe5bceff11dad6bed2dc4c995976f2e1d4a39": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2f8e80dbb73d3a1c28cae711953187e1fd437f262a2e677ed03272242194369e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "2fc6709360320b867ade8f4ad0cd108067fabab98e1b3963f3ce00ec7edf2ead": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "2fdf346f1b49b978529b145f6d7781f9df1f72f78daca7fd9ea1432a3a34827e": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "301ddc20df3704bc7b40b535e1ebd81b59ed45077a90f9a681d8172483b1e0d5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3028b41526ed71421213f14b9199ea585466ca4418dd635b8792895bfb5be3c8": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3077bfeb4d9eb524a76deabe7f42deab7cbd0555ab5bd10744e25136428fed83": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "30cab5e8453258349119bf8e0d925994e8a815604c9e039cb0ac35b2611f5c86": {
      "attempt_finished_at": "2026-08-20T10:15:37Z",
      "model": "gemma-4-31B-it",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "30dc350cad592fe94d7588fc4f5e345e126ff20504d963b06d6e299ef39120d1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3102f88817ae413cca8e210d24ffed6e457ded0f4d4063ad495a56b23b55bd76": {
      "attempt_finished_at": "2026-08-20T09:46:49Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "3134c9a55f797544aa7fa1137e22f26b58579d8606c7b531e1dbbbe7994a919f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "31364dc6c473a5c09dcf0beea7857e85c1cf4484638ee4669adb1af457269c1a": {
      "attempt_finished_at": "2026-08-20T09:50:52Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "3154d1b41fd930516949f3a83a0d31e68f9fdb193a03eb67b077c7b9c85ffec5": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "31574ec6f748e24493efe6893659019e1368f352371d7aef75855c3b319ec66b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3180b4d691b917fe4816aa68547819bc2ba9ae0690b9328588f46613f5dade03": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "319e47349ebc70c2aa245ce7392cfc4e35f80f4b1d16621b55c90e9b1a0c3d32": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "31ab9cce3abd97c6912a9476cca902bfdcd20046094589dbe30ee3bb3d46aca0": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "31cc329b15319fdaba8eee94a9659ef4d0d7f2bfcadc7aa27a925982a6f2543d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "326d3a0c959a0e123abf250e437c58c9c36e71e31a4153eb8bc0a8f579b9be84": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "329d734394ae4ad433474684edee5664039f1da774c11fa12c8c2185d4959ff8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "32b6b0ae50125ce512a1f3be7b844ed8ca3f8f1d2bd70fbf9c530e97136c95f3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "32d39f2d8e434c7b39a2a49f6947727b9e289e4b079026db7d7c896180685c24": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "32f6a00c48c6ee761d5e68344d682f5b1d46479953ef13de1bd935efda694706": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "32fb830f479121128bf39b2c577fe8d83176db4cecb952ce8a1b2d345561b0c3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "334b88a0e9084123efb8125c899637625c7e1a9fea2c7d4d7011b3769802d6b6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3352336fe093bf7d16e7c149ededf56b5d6c9ee93da06002fa1322727d7e681a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "3381091ce7eb5b864d0e671488d8fc523ae1d23af00f0f31038fcf1129c6f01b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "338d0a33b25a359d4c38851c41505de9b6c05301ee32aed293b5025aaf6c0e86": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "33a8222a96e92f88231c122b6a0b2184737f9eb873c9bd8fc2bdb6df02c27fe7": {
      "attempt_finished_at": "2026-08-20T10:55:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "33cbb0b6cd91f518d268a0d4bebdd7299745a0e0cb80c1c6f15b644f5da0ede2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "33cd01e031494119ecdccfefd10c950e960fa795cf779299b8514abef7c091f0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "33f898e669dba9e76f0b39f8cbe8eeeed96f93c1e83339096ea70dbb52ea339e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "3410ae1880f71b0f56430218d58fcb95eb01e17b9b3ebb4894440bfbb38769f1": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "34251051c7e4d86272185746d147dcf36dbf3c099316ad2420feaf5b419a9063": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "34bde2befe9959b7bd851551acfcdfe509de85d139d61ea03cd95ac4af569b4e": {
      "attempt_finished_at": "2026-08-20T09:51:50Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "34be57efedbef3884da8e97365bbe5f75811b404ffed4c7ddd7126d613ee4add": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "34e2bf7001d63c3e3e8434635ced99499c6c3e8d00efb1f20f3e819b7a979bc7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3544c39c98213303dae8e4e7239ae1640f87be36b775265f66e94c14d16a3be0": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "354a9bbe96774c9bf511932448c09d5dd929413a08db04390fdf21d41daee2a3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3559fd820351440bc7faea85d15fae8a2517b14010e3a93aeada48785944b02d": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "35888cfef98326f5eef9d9a503348e219b849aac476f0c00cd7cd571a1331ca3": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "3594ade5a4a1c8174ad892ada3799c62f76b12e6e465762655e7bf2b80c36f47": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "360a9334d4d428d14e9b1c014e6b63de2e7cb05a9169223c924d8a905af22bfa": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "36c6e2faf64211dc1c54e303cfaf71c51ea117b7fc2942301c6cb808fb55b636": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "37407fe97fb416677abbe673fc0bac6872286e1e907f4de858ef19a4cf45f8c3": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "3744d9a5ae037004a6e07b4cc9af3a98753bbe8c8820d3802dd23f4ada7e2842": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "376edf70c0f81c1da50d450459a5779a90d71e21fc5900ab87655c3632c9bf00": {
      "attempt_finished_at": "2026-08-20T09:47:01Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "376f0d691cc8f3f9e05a28fa73b32b8c030c33d0b5d0f907673f9f83acc2a625": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "378e4904b6b55b796446a8a5802247fbdda6fc7d9feb5825c8073102d5bd79e1": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "37fc98ebeaf318ad27ecb9c8eb87960de65ae476363490ae89bac9928959452a": {
      "attempt_finished_at": "2026-08-20T09:47:00Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "38090a1f7b6fb2bf9014ba8b746383495deb2c886996feac26610536eab91123": {
      "attempt_finished_at": "2026-08-20T09:49:50Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "38173950ce09f6ef97daf64be602da00e409f7278556e4731f33f8e4e58c23a2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "383d12eedb4b7566b97e816b53eb8e7784fe1b81f09263ed19e86ddc4f291e7c": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "388dbeb53f13e4eb2218d787e0d288a2c4b6dfe05f91aebb2d6bf9f7cb846338": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "389f3499b3aaf77ce656f5b052ad5f2669e4fbf77e8669db01cb3f71f9dfb3d1": {
      "attempt_finished_at": "2026-08-20T09:52:49Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "39127339993a68eff0cc5e1a5392cce496e0195405cd5e1e11b2bfa1475a952c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "391da3e9891793a9e0c8b1d0b666db08a1248a67710632546c6ac87f2e4687d1": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "391dced3adf39096fd0f26eab43728b00eef9272b978007573a8b7d8eddd32d3": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "3922e59d722296d56fa1ec213e40055adaa8ec736a3a77421c5b357ab76636f8": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "393d6c7b838501b53b3b724c654d55ef5f132f07679e393ca8efea64440b5f5e": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3952ed00f0e4b363c9a985f14b8a0bfc943b5000064dc3292a5261f452f54f18": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "398123c81e55686135498a41c26d93a37063b96a79d8516e4c7cc926ad77c3d8": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "398401a0662399c960c683bcb456a90c632c3af65cc0ccab48508dec88245e0b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "398e9f21ba0a878f73c86f8d904a5e10fae992b4ff10370b4ad980155db09b3e": {
      "attempt_finished_at": "2026-08-20T09:56:20Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "39b6d4501fff3999b7d5ce1a20c4f7ea26a937582209b7b9c66d4d2f0e3b04db": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "39bf27cb69442f9f9ca5a0a6896b8f8e36e62cfc741f3df84bbfbdca680fd08c": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "39e90e50de84e539bd7034e9b73432a795f96bfdcf95f64ebc07f831076847d4": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3a3cc0d8e57704e5c9c5a1378adf89b9a61c63bfb5a39e5015107d8c8db93d21": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3a45c4f119ec72677acac977c2cfcc8f8ea4545aa4dd19dac8cd329b4c1ba9c6": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3ab507fbcc3cf0009c61ba270356bad5afdd2fce9b41af16695d42dc5dfa3c4f": {
      "attempt_finished_at": "2026-08-20T09:56:16Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "3af80f250997e20fad25322c9660621c64b1b8ffdb0adc6f650d3cf6d44c544c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3b1f074c4a18ac43c3f4a199b366bd8e7462bc4d209211c44f00816036050069": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3b45c728bffacf8133a25f768af6eb20a159d00bd16139d53123c33d2860b609": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3b6dd1d257b800275d5b5587eb4d3daf0458e2efe895abc71b84eb0198636328": {
      "attempt_finished_at": "2026-08-20T09:51:57Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "3b955afe69964dd812627b2b51d20a8424c926e89ceddc18fa21814c5ea94b7d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3baffd87cebb50dc55d5ff7a4cf5ba9ec7715b23ac7697325fa2038dd59ec963": {
      "attempt_finished_at": "2026-08-20T09:54:28Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "3be3d193810f68974a75aab4af1cb6c20415a86ae4a54f21ed35b4bab3c7491e": {
      "attempt_finished_at": "2026-08-20T09:48:35Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "3bf80e2245bfdc967355b3336893e562c7d25f3a4432cc2f297deb1dc46e38eb": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "3c1f8b6ea43ff37891224afcb92440f5cef5bf8ce0f05dbfa5fe2d1156aee8bf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3c21fb9fe461116df2ca5e9be67de80f86c08a46ea1af13de2f606c8d9b3fc82": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3c2499e27b4a82de6593269bb461c772b3abe7ebcb22840a82a22c669c8a5f88": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3c780d0cf060b38ed2215c3fc6058ceed7555ec75a8f95824ee1e86e421f4b0d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3cc5fc181cff1f84b7e9cc3dc3b13ca14e082156a71ca657d97e6efd1ae0aa5a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3cec093a1539a12e52c7e7eadab82ebf781bc5f80024b24babc7667d9c06aba3": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "3cf12a17085cc754fbb25f1d8a03934df652cc53c30af853d5589b4f78eb8ffc": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3d8b8b60305f2eda5fd2c0b0195a08e1f1518c02a0f72ec36e4f8b3fd49913c9": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "3d9947804c340a03ceb355755a64fe71fcaa566ec2676783ad6536b1f392de66": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "3dcd0275e05eaf69323604d621e6d587a54cf0d11c926a5681c0be055204e7e4": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3e062520050cfd5ea61178c4162f04500f180d96f8c5b74c3158d4c56aca7613": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3e49c0a07194434f5d8a2f6d2c71a9030552ce496c29636971a3c076e7c8b5b8": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "3e619435cffbc502040333017bd8a4ea63729ef478c4e03847ce084c117b6d4e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3ea8cda1b1008cbd9542ba4d8b61c8253deb56094a38d2a3ea75aa73ddf92150": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3eee11fa3ad789d326a28f73ad6e30cec13955c11c7e7832babfdcc3a3030fc4": {
      "attempt_finished_at": "2026-08-20T09:51:29Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "3f0f92cc9fd2981a806fdfc8caec7e72819d08760766a0e84ab566831c5f3406": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "3f98890c5537b2924a6b630ce0431acdef675d9d35c13edacbbc65ae0198983e": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "3f9f8b0c20294733384d813738ad4563e0030f400290ed5b6f724e286c312ee9": {
      "attempt_finished_at": "2026-08-20T09:48:30Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "3facb8c8fde32dfd73cd5ef935edd9254a244dd75e78482407b80884be9e19dd": {
      "attempt_finished_at": "2026-08-20T09:48:38Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "3fdb368b7186d5b4a0dc9c5c0a07c349177a3f4574709aa476504a5bc0c99acb": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4087b89d22213db5d82b27b98d7951f1a1a28b97dfe18bdd4939a2f552220ca4": {
      "attempt_finished_at": "2026-08-20T09:48:29Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "40bb9cf6fdec537ef9f61211088885ecbfaaef385a923ef129f3161a76e57741": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "40c921c812bfba527b9799cbf69243b7155c9c18a40cab740cf3533d52ebe8eb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "417d36f20c97728d12270ce9c9e01df25728d11afd3cfb421ddb3d00be26d058": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "418176e69100528637bdbb521bce874cfb524b476b30ef36664b7466bd6531a5": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "41d73eee7393f3efca3a0bee5d2ceb37816d37cbc177c677a137a55fee2f4b52": {
      "attempt_finished_at": "2026-08-20T09:48:16Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "42360fd479dcb5ae599286b77248b02866590ffb36ce84a7dc621610a31da4a1": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "426a448609e25cf493909ab21f43fe7e3d849e092d0b9243c5c3a391c4ebbddf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "428074388d7cec1f5d5d6d34af654c9884d91f399df84d117763207fe3bb85ea": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "42848f25f184c095200f7e097bc74b9a3161105384ed2452c4a159f0f4e46f81": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "42be52d8c1996f14997b45251d079a79c2360ec49d24501063f9fe101022f853": {
      "attempt_finished_at": "2026-08-20T09:48:15Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "42f024858cdcc11b92621b675c23dfd8fad9845acd5bb8e065a8848ea8769542": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4315a78fc3bc09397b42a412d0c381ce2940766f40e259ee8c86f6e15a8e3283": {
      "attempt_finished_at": "2026-08-20T09:52:54Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "4315fc8899a64ba25cb3638f9a33d426b51fc553568f20f74f8f2af3126c5b1a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "4341bb9b9aee6cb2bef8ab5608dc90e98887df5417779f48ec10231164feb784": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "43660102e9fab0d4bf5b728c43589e4b8f8b79c9621169f7c53c9b9c713ac89f": {
      "attempt_finished_at": "2026-08-20T09:52:25Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "4374531da4a95f69601f1a5a5fa30560559d281ea11b8dcb60c19374d04a270f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4379dd6c93d9dad30a07398ad9b0531be4bdcc6a8e9c23e668f3020f640b7959": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "439d3b0e401ca33e234acb435b5b616eecac57f93fd65e49106a0d63794c200a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "43b97f683c0fa48bf5d35ca7a726536d5eafa0666857b9c9cd12a5a1796f1cca": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "43c21591f5c857661750874b6ed3ddfaaa1be6073854e7651a2c361b3747bf96": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "43c72897461769714f2621f20a0ff30603d82a0ee518863a4cbdad9cddbb5005": {
      "attempt_finished_at": "2026-08-20T09:52:18Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "43ef62e9efa8a9db970ca570b648eeed9b5bfc7010d48968867f30aaecf2a6bb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4414ebd0d9a3eaeaccbeda582e0835d6ae48797976c53921a0afe7e1f04ae025": {
      "attempt_finished_at": "2026-08-20T09:52:07Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "44169d2bbd7617da7c9a46ae4a06ca3b81a9b8328114114fbb63a54cbc8d4f3e": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "provider_failure",
      "provider": "openrouter"
    },
    "441d11155e99f860db186567707d609e5001d409b26c4918867a158f85a517a6": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "44a02857fcd8a15352d0adc92d71914dc87103555038db45ef54c1d97ac64680": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "44b606b3c09c7dc2e55edd6e9693f4fce61c32689a5d949b357802bad0648a77": {
      "attempt_finished_at": "2026-08-20T09:48:51Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "44c1bd4de90b908cb9c6bbde02647ea51259608564f6fb7bfe989ae48683a655": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "44c66e9e922043fb65efdfca2d3989a209c764222f9998cfb50b7b048c19a6fc": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "44e2a72d789aba42237437bc1bd4131da6573e513d5902d389b7abd115754e2c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "44f1db99555cb1e2a4dd639c6bd4fb80e81604a2d9fd00e2568e3f51d421a1de": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "44fdf62104c9d2896572ba9b4f6ad1e45506cd3bc897da1d4d82290014cb73c3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4528c0edc5818a7149ea25d4da67348c85ee556a5525e5757c8db7775cc45354": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "454389f2b6a8ad4b83df806a789a4f4aeba3a96d2a8db9cd7025d5c41b870cac": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "457c3621ebd628f83d68a90a8471e730c20f3dbe51714e231fab24eec81a4c25": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "457c8d5082fc1674f14e98d4586948ea1e8a9779e5d49c4257524cbc3ebc26bd": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "457fc05311ab7f54f536c81489db77be5d72f9884b753b9dd816ea8414fc0985": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "45a94535e1ed3ffafc2d8dcebe1a01177561e26dfd6047412439dacf2048bb73": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "45e0128fd34db56e484b0499ff781d689abdb0b94a5e407270ea190fb41f5064": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4609d40248d125e94df44bb8b5ec713ad790efc807bcda4b686cdb215a705f3d": {
      "attempt_finished_at": "2026-08-20T09:49:40Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "46146e397dd581db5cb71ab05e2954c66379eb025596e30f9aa621dda2123ce7": {
      "attempt_finished_at": "2026-08-20T09:51:56Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "4630eb0d6a669238d156ba7ce42678f7e41e9a5bc623081140ec5197a4ef9fa5": {
      "attempt_finished_at": "2026-08-20T09:48:19Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "464c9512c76023b9f5f281466b7bbb377c4afd5e5ad1d958b4ed8f1711b02d86": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "464e1156903458fcc64a947451a52046d557f1d539c59fc626d6dbd03dfa8aae": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "465225c54add4361579bbd24f59927a4381237fd74c6769b285f16112731f5fa": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "46b9243bed336efcdb21f6b293f821c95930677e9655639f10b2e69697c9fd03": {
      "attempt_finished_at": "2026-08-20T09:53:41Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "46c6b86de5c8ec93dae0ae063855d90b4f819947b3e8b43ea0c61349c3d11675": {
      "attempt_finished_at": "2026-08-20T09:55:19Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "46d1b3b5d03c399e85520c934122d2074353909fd81fc6bb2536572c63eef63c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "46ec9afd0aac2f62f807a4d6897006db59efe763599cbcac99d0e29fe7696dca": {
      "attempt_finished_at": "2026-08-20T09:46:52Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "472b56ee6069e9821ed148ad6256354919828cc38d0163337681c21ff4cb6a5e": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4740a364eee36e1a1562fbfb3f5deaee5e1aedcc6ee0e410a91397f1e09ceaa4": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4759a9dd8b27fefbe35b74b28451b06e5f0c0d7130b99d72c1d254cd7db0348b": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "4765ae346dc34ae8236173ce92c445f63a1a3d8d7e08d5cf1c7f4881dca66bbd": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4767a29e48fb9eb4e40298448bfa7a87f24c41f9af4aa68b051c157318ef81d1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "47cde27b9d540a05040df20dec39830f31f65fbd14520c1e0aa42a58996b6570": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "47d9979dcfe9d6c9f99a7b402caaa9bb1c7743e2637a6b6d002fd0331c338301": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "485074c0e4ba8e2677094bcc8b6eeec069773bf69693d5f603a8a473881d7041": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "48a4154183298ef4cfa8eb0c9264c5bf14af888016002c101ea7a757f3c77cc8": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "48d2d3784351137957b985a7c3531dfc25b8f4846be9f443fb1c685deca02c93": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "48fbfe04826d1130134dba2531323a033285541f2c987ed6e4f349cb53cc768e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "48fe5561ac675257afbe61b1d461b7247c0fa66bbb2ebf3d3a061da311c51c1d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4921270b9f246735d24d309f64633dbf3e1e5a9d34aa14fda3348abd5a656145": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "493a885cb4adb9919cc2202f6027a61cef2b8b084be724533d1dae1a02c25a3b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "49a9be2f1530c57f08e7ab2d0f312192bd41afe659827951f707a3a8f7119e25": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "49cb80f61e84b38456b90a004c2325d7c54ad8759148af0aeee72c9eab6cd0c9": {
      "attempt_finished_at": "2026-08-20T09:47:31Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "4a476b18bced391d695aa9c4f9fb3251cf1cc0a85be11125466ee205a937ea95": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4a5f5035e887ca854c53b608c6630a903e9561aa721ee7db4a2a14c904ceba4f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4a6bebe8f1be3a6450d1876d72148d3d53cb0c553360c8530eaf6e49310f9bd9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4aaa9dd2aa77c41f17c09ca176ff5fe40cfd7c4afc48a5b93cfdc7f4c795c3d2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4ab857a14ab3cf01332e0cbded5d7e88f4fbb85eb5c8c3509baa4c6695e3c4fd": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "4ae4cce8e2f390e2ea11d61880c1b4d01119aaf6421c127636a0c7dcec33f4e3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4b57e6ae701c775e3a35f1a13e3ce17ab763ef0dda0f8a12a69ae4ffb228c651": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4b6400b716796ee7e2e2335992edabd105403fb4ecd0386c59840a0a48fd004b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4b90c08ecedc1fba2604830e0f936af4d47b77a79cc4937144fdb3caed6719f5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4bedd3e49a73b177876e9ca5c1dcf50aa48f359626ab304a87a7b1987bdac49f": {
      "attempt_finished_at": "2026-08-20T09:52:22Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "4c19ea17f263e037671062133b85a2d97075d1895c8056086d2a1f7d60ac1998": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4c1e4e44826e6976111651047895d79a11e843ff2d683a4b034a5c583f3d298c": {
      "attempt_finished_at": "2026-08-20T09:48:23Z",
      "model": "gemini-2.5-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "4c2402e908df806765589aba1eab449e421afd30ccf4ca36683199383967fc56": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4c49ae0665da8c6b3ed95df8a26bc5bc5a095d054ccf3737f1a250008ad26eb9": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "4c4cd6cf6493fc4e504442070be01db4e49ee1505f77385fb3fa2b2626335e7d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4c68dcf7ebac6645f72672671a65894ba8c12004d35f3d4aacfb6337dbc3afc4": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4caab187c1c1d8d5ce50e29f85459a9b0363c4d74d50ddb0ef1b519ff0220d57": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4cecec99c80db2c2dd561139098cc04663c2fff56325c5922f3025125e6e7944": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4d123a12ff65631072405a9b4a9431da79c8aea897cbfc881f612b2ae71da5c7": {
      "attempt_finished_at": "2026-08-20T10:15:32Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "4d4ca201f3de876b2cc8ea652395b642d69d9334a6ea8a9635b92375d9e9bca7": {
      "attempt_finished_at": "2026-08-20T09:47:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "4d50e89d472dd2104352e063938408c6e8bfec7e0f8c1d1c6f9503a95b75bb89": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4d767c2369bb9b745ee9b20d5e67bd150912f393f3c69434a33c3d61d5560e1b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "4dd1f9e8920299587a49e37a1365125965e65eea24b34b18d7f7f1a28d1e23d8": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4de830b31f469322b5b093a069602264737fbe52fbf06c848a614df92c512e48": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "4e002d1f873b4fc4266b040cc1c2f108c6254d679d01297270f962c490547c34": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4e2a282a1e1f7eb4ac2e7cebadc4b15bc09823c91bbdd59d75ee053d361b4038": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4e30a51b002c297c7391d0f0a7bd207fefb6d5df8c93f9477d8d061d9c42e0d7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4e57c84c81b45b5179f2a3d44f09189b84c4cd20a695f251fadf8a1b393d5a6d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4e71e9d93c351a9f8fd8c8877b70760bf232b898f8c8474e8be04f5df8ebb85b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4e798e172e648318bc41f32e5b7b8728ae476c8e0c79f0382312f0d49158b722": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4ea48d4dd4df19f039ff6879e68cdcdc0dcf120e46d08afede06a99233009d44": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4efc9672fdf81d75320c3c01933cab0c2615b13e79ca38da7a539b312432d7ff": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4f1030c8a614ddd84d67999d50e763eb3ae9f02713a212504b7a1f48997c31e7": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4f18ebe3472dd57709461aceba5b9fd936a14dd1a26096a41ee5d9214fceadeb": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "4f268b7db90b638bfd13848724eb6509014e2aed5569c188e593e5f7804ec507": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4f338049e2747fe6005e46ac4fe6555625a5b0801d4a633acedb440a9edbf7c7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4f91c2784c0ec9c1003209846bde7f515c5c3840949c6f23c7e38f96785dbe37": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4fb47cfe168673a6c8b7703298ef2b8e457c5a4c2c8dad432f51a17e6216e3f7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "4fdf2c682e4680b6d1a46383c49944f22be9c941b8f20a862fda9ccc80807eb8": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "4fe5ec87df882a1ab4e314baf6e479a189938c899b9397a27f6617a06be6b90a": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "5022d1d507f621ac915f1f28f4e339f2a6defe41dd1231ac66549df6aa6d9c5f": {
      "attempt_finished_at": "2026-08-20T09:52:28Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "502cc991e2b32366a9380f479e0dd2af005c632dfe4ee9f4b29b0fb841f4e2cb": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "503399c30be155413e068e60e1feda5d5aaee4c80493a50f7283e0570ce2d352": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "503e086481211d1207db3bf8be0a5d751ac6146970ef8a9c7d835568e9f926e3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "503eae1d47e15fcc90881b89038651442524897c5dbf3e54dcb6852d4b6414ac": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5046602a1f6f39beb3bb4f7e268c4f8fdf53f3a86c2cf4e9fc7ce652cc13a47f": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "504f587d69abc46774154b9ad269a302348b7550e926e56a98d9121b05dadc06": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5061d2628f30496d827438f52832eaf54743bd628daa69c826df481e340fd97a": {
      "attempt_finished_at": "2026-08-20T09:50:30Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "507c948d39d92c846edc7868ea8a3e382400cfd2f6c3e50c9a0a5a2d9bcced4b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "50a55fcac7a9bdf9c8c29b729fb4a877b3e429449b9c565b3d5ad80e01364863": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "50b2693a6ae2201be8a4820eac2bc88d3bc4809a09b21d4b3fe5a287b9479c1f": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "50e9fee9a50fe53f900eb3a5319a95002f68204c1afb41503831d699bf1e9c80": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "50efafb111e29c62cb8ec5dddb33444beaba44b72a9db1379faf16fea3b3ff99": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5109c8718ee852a2545ed0dc5bbdceb52e6767cbb1092d9f502fbbc363c92673": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "51117c878a1873a4aff0e78c9ce016c214f77c6947021c1db4332f2a5d5d563b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5178fd905791d4fa232d714ebaa2087fd8ccba84dd04fb7fdb861997497ed1a8": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "51b274551f6cc7cf2f00def538e949166d8c065bfdf9de8938219b5e11cc776c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "51d0254b3500d53c3abc6af6d7c05abee26c923d12a5f4db8c95d72985ce31fa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "51d7bd2a25843ef0550c7e0c8f99a8a5fbf0e0e59931b4a63a20cb633ea96b04": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "521ca8f3e1da61c1b09f32842659ec3abed842eadf4f737e63491440901a9419": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5223727d282e32b0d36ae42f8f43ea944e79347e6227e9c5be56a2cbb3ad07bd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "522a2a2684b036a170969d1507060cdfa63a75896dcebccf0f4ecd1450775bd5": {
      "attempt_finished_at": "2026-08-20T09:48:55Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "522b82264319cad2f7c9e310e5f0c76afc2dca78e5357e1bb2cea04554ae703b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5257b9f5a7de4b329b372f5026492035547a66903af6fda9b311fe46fb9342fb": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5268a7dc3fab9aea6b9efaabf9b441b27ba1e49f17fd06cbf6cd53652a56a2a5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "52bdac90aca52ea89e9604740b31181027eb1bf182ba682b8f3e6dc11ad3544e": {
      "attempt_finished_at": "2026-08-20T09:50:21Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "52bf806c20474a607609da640820f9a00a94d8dd276fe053e4e1a9f38d1b8de6": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "52f794d9d75f6b25979f1c25e9e4de8e2cbb0782e67befeb8225b6ebe5e33335": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5318c9b69d6eaa4ce14ecadf85ced8176037691d857351b1dd8e8c703cab7689": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "539e7d5129da3464f35611741fd02a77e2ec6ff648cdae9e4221f6958dbcd310": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "53ae727fc30d78d09193b4291ceecd203f8526b3dd37eed412bf5f654fd22ec7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "53b8f93395fb12c009b0b172d37724ae401b6068192c181429d939584ee3c951": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5405e2797018702a8a490e5fe7a451d190a8c626060c891130832fe8b54bc6b9": {
      "attempt_finished_at": "2026-08-20T09:52:41Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "543b940cf25f80c972b8c3dbbd39476a96ffae492080ba744314a25a2e9df29b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "54401b541fe03f77613958c5f52e9e99d4fef5075f6f4473a9dcfb4188ffc0cc": {
      "attempt_finished_at": "2026-08-20T09:50:26Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "544b39430cdc527d24cf41557f76a64ae463d64f62610aeb36173091bbefe560": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5473827da75590aa791921d7dccad2e48c90e01331185bbae15b08590c38708a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "548426873be4af0ffbb3d5e45656e8db7dd7f615f63f2e5f04a9abaf739a691a": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "54a7e5b07b85a829c0f91a524f310e890006b102a26ef5ae1a19121164a48c43": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "54b097326fde317e02e6255f8dc4febbc7dabd1a3f330697312ac89a67323dcd": {
      "attempt_finished_at": "2026-08-20T09:50:05Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "54d860534ab336e9ccd03b82af72a49e148059d905a8136829333c508447db8b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "54ed5ff8acad978a625dd70a4a7ca19f8b533559aa4c3e53a6e00d3fc17bccbf": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "552cf0570dbf654335774f2208ad22f4d2ebe40ddefd8c3224f83a1f27ff8101": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5549bb886881e0e0b79248ad6f6e829a29685b040f9e2510f1790b9a544cb197": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "555641e25efb18e1440f40c22bde1154a117db148c84949ed6f3302136487036": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "556b2018058e9f2c0f6d24bbb4b38d924f96e5c53557777d6f2470f507a37d6d": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5572d594640f6a7b0c3e8fd610d1bd249e7b5157299d2b7a8220291599fb90ff": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "55bf4762bbec2accca7303be27c4a874bcbaab910571e98210b8def2909022ac": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "56235b2d8ba00ce1362b0d5ac7eec4884e96e91d030e84bee6533d0efa74a014": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "565071a4bdd97255db7ba69f636e89456c8a3e679be9428bf36bf9cedfd1fda3": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5689d13027c676aea404106a0fe722e5596001451def4cba6f2374f8eea7bc31": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "56aafa03d94ba936646acb53fd19637b671595f94983d8161072b1b7e35b34dc": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "56b3aac1cfaeceef994fef038418e49f2452ba8851f93b25453c8aedf91f5e8f": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "56bf7e29e76ca2b0dbcc56f9e633b0eaf3464c290542db17d207ab4893297c69": {
      "attempt_finished_at": "2026-08-20T09:48:11Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "56e4274077d47ae39e886fe580e4f2579c53ed79e4a7113220122c55f9d683d0": {
      "attempt_finished_at": "2026-08-20T09:49:56Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "570d3a5968a65323e4e232367373481793fb9bdc10ca08d2b05092ffdb7fa460": {
      "attempt_finished_at": "2026-08-20T09:52:11Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "5738f614aecc516548b06c31a91704f2caba78c0fcf0fa472a174f8aa02373d4": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "57bbcdf0719e4ce26dd53f8f31f03e6c41243c53de6d5a5dcde0e6dacf21aee1": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "57c5168e3b5c56b12ab65bb857859df3c286e1b007335adc0ada5cfb3177b613": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5866e5cbd57b63ef146f9d632ca43267eb7361fdc244743f0879ccc2f8b73efe": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "58783d7d935d1bd17134f26cbc33658686bc33910a4eda2923a3fb52217d9f0a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "587e6cf4f0e952fcd4472843f33294f13c29979643cb1ba15f07b46603a09daa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "58916b5447ea59cafbdb21d8d0e7be53673750dd0ab80d807d5d9e3839f89d88": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "58e0d3209c3e63a1ea684c8c76a3f5f3e8e002db261b4cfe71e41c8957590ace": {
      "attempt_finished_at": "2026-08-20T09:49:20Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "58f4bc94f2541cc74e82b0182e888f633c1a3382e343cb0a29ce88bffc0df0d2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5902ad9c121b6c911f41e45420cdc6e0f74ef9bd2503322aa315525a67787cd6": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5990c6655e9fc5bcb265ffb58b11302b65e14d36cddb8c3ebecd0b90f37ebc92": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "59d077bdab0eb23d11adebc23e5d6c9fe36d75da7eb6900c4c2febbf692ea404": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "59ec965393687ec43396582457b98c01e9d4873001c1a3078becb180fcc29e57": {
      "attempt_finished_at": "2026-08-20T09:47:40Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "59fee509f3e16cda592c652741bc0a2da981614605d5badbe0384ba1a8364a24": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5a015f4e70ee213fbd5f7b7b7ab087b11986b256fe9d2aac33eb1d9e73c0712c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5a0fb24a6aabcc70bdeaae57d88c3fc5dfed1dc8833e1d76ef963ea8238239c0": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5a9f44f31d229abd1b42c27abcb428ee049e20eb32b30c103d54f4d0f46ec6f1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5b4f7eb9230d23aa8da68e4260cd359d946562241472a773b1892f0232b8c5a2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5b54791766b3e9d02673808ead6837b6c7d55eeec7b43a69cb6a2b7ce0e30d40": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5b57c5096a01d1cead71f31099f8c40821a93d297e2384f6fff446f28e3831ac": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5b88d3699ab71f87ecdccb63019660361cf62eca0e2f24a66d24277ed96d9658": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5b97055cd853bd53757ffa8acbd1fa00c028092e5d6471403f547790d171ad2f": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5bcaa13f04cbedf1796f71b353e1cba606ef245d014f6f45e015b2173a508173": {
      "attempt_finished_at": "2026-08-20T09:47:29Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "5c0745aa0d08311de32a595692b6c2704ac9a08f4d1029869bde7e5fff9b0bb8": {
      "attempt_finished_at": "2026-08-20T09:53:32Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "5c4b47a299ea2048756ba90c7a9821bfd8547d2c00bfaa753ce009cad7e8ef00": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5c9b54094a264035acaa7d675a07d925007d34470b0f669033ea6075f47b1d5e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5ce7318985dc7f804ae4b393114034e5a59a9863ec349c9b328483f171e82d13": {
      "attempt_finished_at": "2026-08-20T09:51:40Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "5d07ff5ce360e0ad2f32958ccf4c966bff74e003819d8b8676581a3e6441c73e": {
      "attempt_finished_at": "2026-08-20T09:51:02Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "5d188d419b6bca6edddab382bfcecdfaa2cab92c75c110321c0f93dd37b9ada1": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5d26cfccead0a19c4b66801a1446e85cebc9c7b97cfb42529538afd443501a09": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5d4b53eff6b5805ba914fe193a53526e534e8be202b990fe4ec4a478614d3556": {
      "attempt_finished_at": "2026-08-20T09:47:53Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "5d597a2e90aed03c1c70240471aa834f90ca6e4844bc9816ff4139e34daf1c30": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5d751ad53c08dfbe1c922eb28f22017297b86b6f520a8882c4dc396ae38d4caa": {
      "attempt_finished_at": "2026-08-20T09:52:12Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "provider_failure",
      "provider": "groq"
    },
    "5d9a19e90455a058f6460e6ab908d1fa7009e5372255e7cd8d85306d256c2e59": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5dc74cbc90aaedc0b5c48dd84bb6999ac33fb3d43e7213124cca1f55b62817ef": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5dc92fd01dfdabb1e362727fd332a947d7cd99ed323f3798b73e851090b8b618": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5dcbab43f26492fed4a03722854ef4e34b3393b273200b474faefa4cec9796d5": {
      "attempt_finished_at": "2026-08-20T09:49:53Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "5ded6d49f176623cd5b938659004ab3aaaf579adadc5e263c29be6b50837b8f3": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5e2c9cfb04217f5ae557bdfb9ea5bdd4cea2d7d70b3c468c7aead192927b1251": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5e4fe7cdebb61aefad5a25188857ff6f4a84eb1848e3d8d617f3415a8d62d598": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5e8e41b7f46cc0c1a6ca6e235db6434cab878f6f52d436091e7ac092ce87ff92": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5e93e029050d247d7e838779cebf4eb7bba026b89b7e21fffec056b4b1b039f4": {
      "attempt_finished_at": "2026-08-20T09:46:13Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "5e979f8ecdc59ab1dd27ae886f37a87e81c2a0d7f34c493b96b22b88331a3bd7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5eb35921b6d1de98c47613118ca3eb6a0011cbbf62289a72d051ba86f4c37a8e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5ec94561ec3bb4064a1925019e2ef44dda0db3507a91434ff67adb704ae1cba7": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "5ecfe09610c7147103d6504e18cf8db1d132000d8b7107503780360a6f8695e8": {
      "attempt_finished_at": "2026-08-20T09:47:25Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "5edeb13344b89e01fc981dc5fc39c9c4d734114502296639857cb49c719ef649": {
      "attempt_finished_at": "2026-08-20T10:15:42Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "5edf9842474d7eaefe0c4469bfd49b5e69687c3f3cf6a8bfb64afd7ce28a3c1c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5ef3749dc10a3011d0c9fd1822f2aa9df6485e2df7efe1f491ad0f526da96878": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5f1da0c44b6366d26c3455ec072334cf051d48458a097997f5e5742745335143": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5f33036ca32ebf44a41bce02582a746da2f51bf10940fbc88d19094f08c0afbf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "5f4fae179e1a8232952f59ee467f8bee792843a6770fe5fa42361e91b607b5c3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5f614fe83f4278a097eaf070f7ada1ba60174a111bfaf5124f2a4f0b56f08816": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5fdae3235d336391a410073cb9ed804eedea2e261c972b9bdc66f7e6ecafc641": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "5ff93e0d4e4b91434eb2bb959450804fe356f0caee33689fb410021ad0825121": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6018a41688e8f87ffc8ee001d2f869001ea04b98f22aed9a1373af68f287331a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "605352cdcdfd3c925919f620eb9da3bec26a63b132bf8aaffb34309e88bee100": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "605976a73a9dbafbc09c8bb0af18c9545e11cf9c64dcb6971333c2ee1a3e157b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6068304a1387858e0b799c632fb37fba9b80b77ed1a047c30df74a74d39c3918": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "60981064b01541e5b3754c007be14d1cf4d40eac6f2a23a8144b827a086cd596": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "60afec18bda53cb28d9364edee0fdd96046417bcf24390b7ea6d7b74743cdf2a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "60baebbd2c3b755879b2a27b83a7bdcee3246107392e5d77ecbd86e1e6e72b7c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "60e12a70cffcff8de49d9dd7396721910dc781d4b5c42884282e0b1c3c4fc7ce": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "610414acd5b2917fbc0d8c6c43a21955c26336325283b819b3546ffb76af0287": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6110626273771256e8db01c83ec9b11bf2d9679c8ccc222f5df7368b3b89d2f5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "613a1aae020f9396f6fe87a3a7bfec765b64ec01566423589dd58a8031178abf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6142839ddf7d70003a73b1fb54755a5644538084723740f88a6dc6fbb9c96637": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6217844dfa06e59ad53bd01ca6c95476ec99b7553f207a86c468a2730ca9c606": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "6251892d820343c69d1ae64dee98c1edc21fb77ec442ec30a870324ccdf7a58a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6293881a276a063ecd91d41f4d84e3d4f0756e73ed97d966d51c31687c90e1e0": {
      "attempt_finished_at": "2026-08-20T09:50:10Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "62cca81b45440d6c98132f6cb7d0e6eeb1fc61325750a19d2a2766fdc84bf189": {
      "attempt_finished_at": "2026-08-20T09:51:15Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "6325c2afa74c6e757ad64307c126af6935f18efa35b4890a10ba3d3035e15483": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "632fef6d1a66f4228d5369a928270ecbe429e4192dccf2780e8563118e5978fc": {
      "attempt_finished_at": "2026-08-20T09:56:26Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "6337c37539b2ce53931389745ce4a17c5a74d186ea56e108c6c7161503d70623": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6362222879587cdbd0d54f1cd3b8790d8a7b82edff91738179ce03e257dfc27c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "63a616402502d5e86abc3dc95d1f312769d7b7f38464d44728d223269604a6fa": {
      "attempt_finished_at": "2026-08-20T09:57:23Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "63c52b5824c8401972ce779e40797a44b2972ed3b9982046667fee1cfc9ef9a7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "63e4b1bae4718f2c5f49da1a2df28311946070bfeeb9f0522676822abae4d7aa": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "63e7b6b305c566e571fe74dab2ce5f8c161278e491f090b5fc1465a1d7d4d4a4": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "6412f8c0ef5c4c7f8b47ce9bb468da904f89517c76366939494339538bd18177": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "645a6d3d1649518a1ff23a065b88b30c03d467692c16db759ea1ea752d2eaf3f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "648bc1a5aef576b89b1e3fb0262f6ec4c6ee657cb0b3437217994de1cc13d887": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "652be56420a5c5565251bdcf909c3072715fc711cf8bbf01e5cd5b5798c26ae5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "657c20a34088ffcc827c0ab4234c24fecf2de3b9e7f2bda846161fe36c08434a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "657c74cce741b84600fb76ccd7113dabd6126c65e5f804c189072f5ba07333d6": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "65890149341630bf92e911cfd3d4652b72c2d0e9de2b1eb0683533b2a97f1f66": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "658cf16e0d9a8bc2e0cca4fa9590fb6885654ff329c17ced77107c4844c714c0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "65b1a012739d082437622be57e486cf26b9097e6a2cdd1e206e664365bc13359": {
      "attempt_finished_at": "2026-08-20T09:47:23Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "65c3e2eb7b929d0f7b8a83b25353e94db29dbb75a731dff6fdb8644850a473f8": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "65faff8f08b81b17c24af88562a92e6d4b62e1eb3c026b510013ab8272418bd0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "66080b1841eff54941497404462dac149f9b387cfad0d6e1a1321a8f4409aa94": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6637bad4c82312a1c6568c9a2d499c17ab116eb232dba2d0785192f0826522d6": {
      "attempt_finished_at": "2026-08-20T09:48:39Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "663a608dc447f912c98bf858bfb40d4e390a84fa62e571686345b6eb74533460": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6662cb69fa8cdcf7a8a08bd6600d4b9b0ee0c54c5165fdb7f1de59bcbc9ce77a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6698080d27c09907508df2b0a0d0c13d20ae14d69a3a669ab7f7cdad4e4b7bcd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "670e56c710c074f4ebc888b083c8aee054aa67e03bdc1d839598c4a9d55d7cf7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6726c29a834d2df223491c4d03c61f4b506915754b25cf548a6db2ec5953aae0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "678baf7cff7c5c74afe7db0443cf80f6c4a7e48c92b78619ceb59063184a58be": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "67dbd340d0993fe09d8a016ca55bdd0a2fcb3a150bcaa16ece8264ef577d0a6e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "67f6d8df02d2dc796fbde4e66ab5a8d78fdd3d69a59f61ba56295f3fd18f4909": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "67f7e846d574dc5285470b68ea32350ce3b3e4bad9f0ad22665b3f465fdfb22c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6824d60251e2be6652a4f2328baf5a0c51ec9300e2ae3f1bd70f2fb4b2a9f91f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "683a36579b49743c8db266acf487b3e4fb416626cbcaa966de7ada34c331ff7e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6870668c1748f3869b877fa6bcd1582858b9d5d8e5acb81d64c571a80aefec3f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "68835903e935ef9fa7fc6e2934e0f4b4e8a124ab055074e5b21c2d144baf39c0": {
      "attempt_finished_at": "2026-08-20T09:48:37Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "689726e0ba4a7617da27ce3ad4da05b3a83e5cb69b123ead0d042e8a23de4aaf": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "DeepSeek-V3.1",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "68989603b79f97b2355cbc33c9aa6816c296ceff3fb2fb4d69d45356d4eefb26": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "68a998b929cf48cd19724de607db78c28ab3a1c063c741d3e358a501bad125d4": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "68b1f4852eeecde9e902ccd63488d175a5a5f8e190e16212aa01f17310817f62": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "68b7cc929c1569356360cee65201264b40f313d879c2d00500b884a020e4380a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "692670fdd137c181d72b12eff852c55a45eb2437162d38e976756d0242e765ab": {
      "attempt_finished_at": "2026-08-20T09:49:50Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "692d628b6dbb3c886cf5049febe43ba57d376d2bccaa8fb2f463a17290d2652e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6993d33ee1ba994f3be26db4568bf6bf1fca50f4ff01ee3cbf53edf22b2807c1": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "69a09341b30ffac98768b95bc8fc4f7e87240aef157b7edfd999c0e019aabffb": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "6a82a15c828f2db95b9cb84bfeb9b9bfb7c1d96791fb7a3771b22db2f973b27b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6a9495c902af9fd3d082afc4b4a9b08c94d1f9d7d472ac55b4a7cf7341d3d2f8": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6a9e56380d05b446b4d67dc94e30b3533ab8afb1418eb2502be874d1d4529c59": {
      "attempt_finished_at": "2026-08-20T09:49:22Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "6abd7b28db52f63a296035125fc9defef9739481e565652ce8b6b6a4442d5a10": {
      "attempt_finished_at": "2026-08-20T09:47:40Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "6abdf51e170257a71837451f8e2a1f54a7d5e21f680f4371a982c9121c1e1f8a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6afd72bf2e519088594c0513e0062e011736532d865441bd8d81fde05df727a9": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6b322abdf6a63b6daa20a4c78c2214cd245b0eee1abb184652f438f1ce56c047": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6b359dd44a12759f8494dab8ee4f35330ff2d2671a77b9ab6e79c9d8a7c92efa": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6b662e23517e122628080229c2ca764987857253d01d776727b7f83d46a9e43b": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6b6de8b0e2e57f75b5b567baa35ecf710ec6c2aa434f8c0210cfe443e0c42ade": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6b9ea20cda36c98f32f9fe61569969e47aaad4d002df077927ad87192c4c65d4": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6ba8ecc00c0283070ba635581b186b50f1f49c83b687d8b4d8d3c6138419c3c8": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6ba92b814546bdc6df8fc421b90257c62e72a9928bd623c43e46869eca76c09f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6bb3648e086fe376af58697dde9d4d5bb531ba88713c21531b5362b399a2de14": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6bb789895419659d5fbf845a15ff2a1809067393466f9fe142d8ec50eb494137": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6c59957cc4c74cf6d0778534ea069fb2c9f09584d87627e96dadde1970b775d6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6c610838bf19202dc9e1db50e28c0cf99e2dd43da7e846b9b7f74a04419178a1": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6c71afbd9a2e138933ab300f93b5f31c82a33e8c4d3308f6e7a6831c02d6b18e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6cc5d679b46650d9dd29f7496f1e9d4af75962c7dd25057c71fff9fd89f42c65": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6cde765d47ca7a4a903e12681b46578504d25b99f80aa259d14c5b866bf5880d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6cfa860e19df6dbf1adeae8a785e99122ed337bc81c3dbff9ab1f1a8b4e34b21": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6d138209b3b0c053623828af9096c8736d24e04ae69f7991911742671f56e85c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6d21e81a5f3b087016642fa5634b970d1839b76c8b8e9752eb206e96bb176937": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6d4cc80cccd248e94a41ec8c5f8bf01a6178010aba4fe3c9a78b6a8314a290f5": {
      "attempt_finished_at": "2026-08-20T10:15:46Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "6d6d07efe256256e2fbf85522f5021c8d7fd230ae0fbfe41c988e5abd5bb7bac": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6dcca20b73e3b59da086c2262ea76e3412d21a733bd53a81e6d2992e4d6b9dd4": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6dd9f55c7d3240f7bbc86a80a8ae69dbfc8fbe057e974abcb18611e449026bac": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6ddb248a584c6546a81b41a6ecf75a83f013824bc8f2f42a9e47660bc5a5b8a2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6ddbc0a37bdb701e26d9bcf316fa101f4160bd1e4d938e1173f56a0c44ca448e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6e1f4ec1339e376ef35560c5ff843cda1b9a2609712d9105a3d23bc8434efc1a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6e2c14657bf0b0457540dd03c6bc52c5c61ea89fd6f94966f3729a2995ea002f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6e36faca1921a17f2cf9ba8782dbbd7e3d2751ac46807937d21dd1e30841df60": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6e7f59777dfb32a7d03fe84a41b4d68ed8dc9b72a3e2623466a2eb168005ae7d": {
      "attempt_finished_at": "2026-08-20T09:50:11Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "6eab18c7c62c728bd9f3cef5b83d8608021e6bfe65cc3f72046c2b90963e86fc": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6ecef19d0bf5bfc033a21ad9747692b4fbdacfce131ca7b1663ab3a865cfae09": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6f11b9de59322b958e812e5bd072dcdd3a8e29cfd046a0318b99b7ec75bdee13": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6f1e85935c80f086567d61c584d87bffcfb85869ca45e462e5d133f40ccb5004": {
      "attempt_finished_at": "2026-08-20T09:46:10Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "6f64d6394c54b7e4f27230b175925cfd01bf292b0d5d0652063966d84c0ff542": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6f72d647564ecd3e61234cbef443feeebf7a35b2ca026bab2117a70153025d31": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "6fb155ada52e1449cc88278c8ab9e8b70a877b04f25028bfdaf26f71b77e6146": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "6fca4aede277656fbae4a159f67582d23485e3e211742c5fc021a11a9dbd636c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6ff095d815b42e95378a40c87ca6211ace17e1a33abf1fb9857d0afb85180b7b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "6ff0cfec2c1df30d45c338373c58ac6c7882a7467f2f362d5116f2af023c9cb0": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "7036fa6b6f0cfd044b3eb0559570d4be76968f4a042ba4ff7aa20c0df4f3fc8f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "70445cee86b76844be569bc1b1a89136a870dd2593fcbc1e987331894cdb4eae": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "70611e49128d84d6fdb97a725750fe6361bdba6ad26fe932c79837075b247a27": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7063e345b00f9097a529ecd0f8ace460758c3fe0f1753ee57b192ce310686964": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "70a8153d885a3c2c5c8335412755280d8abadd67d2e809878cefc52534349e5c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "70fc8a811a7e107abdb39a25124e5e68a5d47ee9a3f4ee220fec2bf2dc4e57ea": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "70fe0676fea5ce2f1ee09264381e5d4948dc1ade41c510f8f69de53f569f7a92": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7105f83d6ac1ca87b19dcdfb0e5468c3b99db43daf8f4e86f9b141bcce423c71": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "710ffb60f13c10422f18ed59b12bd2d171f86dfbd4a9516c254b821a6149ab70": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "71175ef9f3d891608c31e907c4f6e5039d176242bd7263b404acfd73475deb20": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "716a644cf29ea58a39b0b6c4f4a5e1b2d99bd094af358a5b0901ce512b116f68": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "716b44b0cc544a25431def8cd1f1fb2d60a87844da37b6dbad9781f215958e5d": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "719832ab94aea2e3ca74ff41796f8980717a4a397ec315dee9734b99c3d9c825": {
      "attempt_finished_at": "2026-08-20T09:50:41Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "71b60dbae2bb72cc4fa12efb81cd04390a9e04ae2d47f2f9f574c1aad0e726e7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "71ca024b8f3caa11f53e2283c9b58898840b5821bfaec3685491e7718931c9d4": {
      "attempt_finished_at": "2026-08-20T09:55:28Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "721576c511bc5f79ee4ff6a3c31ad08e87477ca1b5f105aa48ee342deb44f2f8": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "722a4bd9e1bbcc27b8db3ff580c803fb59913ef6a9f670299c0cc839afef9d89": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "7262cc72da65722e82859112c6d33ca0529e36bb5685ca516747a99e9fe52102": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "726736fd94e187809339021bf272356eb0459b4cef713bc5e0ac6e4c51bdf25f": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "72815cf38849fd849d502b5a91b73ca93b56a3fe778eeaddfa8ce3c384abe695": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "728ef2b98fe2abc121038be73c145dbfb1e4bde4da9387b44205642e816826b6": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "72a4b0ccdf1b7734f28e28e70e2206ef8e58af488e6309a115eb4d45c2c46010": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "72b49572f85282c205a39c71dd08e908a8b6ff5e07bd9efd5275e6ad1b2a03a9": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "72ba37ace68f6a49adadba7c851923a77a0303ca199e43137f81d909a8f60811": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "72d37f97a42b005c9517c878bffc422794f41b550b0234d6c6ff16eccbd7d899": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "736622b78f71064c117a76ff9b35b12770a1466d185bae5b2683b8fd867efae7": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "73db28504ade2bd374589e9249c9746415b7df80232353817f467c0586a013fe": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "73f8ed8c012c470043e8ca3a305530d7b1cf69d293dcb25530f4ac54c987ebd1": {
      "attempt_finished_at": "2026-08-20T09:48:20Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "7401903c00599c75cd502032c99a4f58d7a7575ae185b871b8d6aec291dd9fd4": {
      "attempt_finished_at": "2026-08-20T09:54:47Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "745ce1a06f47e2abf1c5f64d576e37175f46421e8b02f4adf68fbf17b2d6e9c7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "747e035d550941849741bc3ddd12f44f999a054ed6f249dfd7ee9ca2a40b792d": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "74ddccbef4fb7a2e254069579e52256a5556f87d62340a8acb24da32238e1657": {
      "attempt_finished_at": "2026-08-20T09:53:08Z",
      "model": "gemma-4-31B-it",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "74e5a38e9c5c66ab1d31eba19363e688fcce1bdedc177c4435674bf08b3fc32a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "75056af0b4bc98e8845e6bcca6e5a97476938e5b30b493d74083c657c743abe6": {
      "attempt_finished_at": "2026-08-20T09:48:43Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "750634f550e53f02888b136f1f53a9816d3246571ace97b26bc6897996b06bab": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "753bed139a3f34d13d6a7e9b4ca3ac3efd28be3fceff949b0c4559562c12e023": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "759563485f24b621afcac5b41680b75eced7b1604d738e43499f99f1083b80bf": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "75efa2a3f2cff8a8b7fe56180f9507e15a537456ecc3351a5e043075c4d5c97b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "763221c1c483aa46619937139f5b346f1738c033be2191c7e61ef515a8df1165": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "763d7bfb04275d34570772bf9b33c1299d1ef3bf05cfc3186817083d553b661a": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7650cde380079ae063f3e4a7eec3d6f578d0f500909acf57ef670bd1c3f0dbaa": {
      "attempt_finished_at": "2026-08-20T09:46:32Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "765b03803034409a1707f69ca3fb335c7894a8699a0b648703828e5a9224bb62": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "768f27f600ce44e4d2383daac21eb60ff71d4788811f74437c2de64aef4078dc": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "769850d21250462d722318a74ad39dec04fbdf8924da71fd6be521aded8da7c5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "76f6ac716829e398ca04d4f0ade0633eaf9b3ea5ffa87a74ed728db4b5c354c9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "777514f68e87ad8e09fa5f35632b55188a1bf9c8a275987f48b4665ed7c86249": {
      "attempt_finished_at": "2026-08-20T10:16:00Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "77d74990000a913bbd4c48c3d0c8e5e2b7a6f6b387ddc24f161b2d35130a5ab0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "77df622d2ebc200409ba58547319712bf7af594783f5905dd17ef36fe03b9d78": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "780c2e4d8155633e084ebc46edae68f903ead8f16101ce3dc64f5b412ba518c0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "78157f2d8c191777fce98d18d25e1f476c13473c65380c186424cfaed0b36438": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "783a37232aed2454e345162f582856d4dac3bd7821f98babb45624d2a9ef1677": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7842a7496198bdac5bbefdc80f58d97ae81c21ef09118a5761daea8b2a3edf22": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7886d7540b177bff2d7bbafb2ecbdaa2c8a902651bb4fc8e8b5cf1d950db849d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7899c0867accf3597828aab35f460de62d8c29e0338495cda6aba5daafaf32fd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "78aa6932b482ef49eb4b713f91a047a342db0281e0d006b3cb2f134007a6694d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "79416fa6849f6b0f7d26ddc9180a40696385638dc25b125d37911a188894f086": {
      "attempt_finished_at": "2026-08-20T10:15:12Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "796d8a032aebaafe1edfaa20b322933de9854e1826a749c5c3df4cd61194b58a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "79865d2ccab23457d765fe195bf0e39bfb70910e8ea6fc1dbdf81b1cbacf0f7d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "798f47e992920d02d7bc294f7fec8e6f1f0b77e979d6ffc8ed2692ee1de3c119": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "79a51ea393d88d1a808d4d09bd294036d9e7ef2bdeb7db477d7f4300a9ba5a3e": {
      "attempt_finished_at": "2026-08-20T09:54:05Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "79cc820a65dc239febd8c9696103cd899c324902666dc4911d6fd4a34d89e572": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "79d06a432bd820ed1b31365619b3adcb3fb1a18f70e721f944cc6745bed68f91": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "79e5f0c803cc42355342dfa05b1d130ec9232ebb2c12c0316ebe9b31a6a8a045": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "79ebd7f9d53040deb042a1d3aac7ea16efd96c2eca6506784133f0a7fc6064da": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7a763ce40f73e2281e862da726a4009408061a4e4f72f217e9a78556c1646aa7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7aa93a619ce5345ef7163924f6e9f122116f28504f1892629b24283f365148d4": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "7ab6f4d29106a8d060dc192233081f32c539394c773f675721cf467c074a684c": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7ad394d7dcc988214a06a0586139efe1d7fc733d5735d0e726eb49cf9c7bb987": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7b041178f53f184e9b46bb8193f4590ee910c9d099a944ea27a11eae5dfff666": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7b3203d7b7dbc1ee027a21fa4baa7b87587bf5de376b64b92ac1d0c3b988533e": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7b71a78e09c98cb234cbc9957008884ea8057bec258316c8785c9ffb985c977e": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "7c010b67b3e25cc14366232c01dc7cd92bbdb8497e8b4bf8d615318bcc534659": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7c93727ff1cf48b517b8f0ef6a2cd309bb2ba59027903c5db1359b971ba5ca3d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7c97d87b0af812730c35c1fec3ff7cf619a7a24cda5fd879fd66f754b31525c2": {
      "attempt_finished_at": "2026-08-20T09:49:25Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "7ca1df9fe58990d882d78212dfb776d243dd0a48ea129bad3a7af1aa8b514416": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7cc76eae18a1d6d107dd7d5a2e60bda03582f0431fa9520cfe2b0fb5298e3657": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "7ce9c5df063a7558083243a7f9ffd48344377c85fdc86f7de4806fad2b5ba239": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7d27d9b2b7bdc07c2edad7094502c2a67da193458cea760b3edde0fd01b8e787": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7d2cec34a28d018c3753d1833a083165a31af8881d5de37bb32e6c88cba36335": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7d85987375b46cb8e4504b3a06199cdb3ba07a408945ae04cb94984e453828b5": {
      "attempt_finished_at": "2026-08-20T09:51:48Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "7d882ff8cd7ecedbc7bfb1806e6d18f1af605dd8b2ae0bded3cbb022948286ff": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7d9c8c8db8392c3ae6d3036524ef82b48076da1a4d82350da904d4904c5a4b78": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "7dbdbaf801d88c8f8b9bf522d646bc281d29a8c7e87b2c70bffeab6e670504d5": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7e5528b6f2cb1866a5153e81afddfa12edeee6f3f6dee9a31a11478da3e91298": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7e870f6beebeac27d794a05acdd85984916b71e42ccecc3d8d61a173dad4927a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7e8913a8d0ef9f9771931bc7843140b6bc14a89be55eda52608e19281b7aa02b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7efe5b037db76024dd5edbfb84c84b3efbac4a07ae6bb4aac82ec102ba4e64e8": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7f016a1d489b8a542deb529b72533f3be2fad9a8c535a3db7530e7c240986beb": {
      "attempt_finished_at": "2026-08-20T09:46:45Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "validator_rejected",
      "provider": "groq"
    },
    "7f103600ba6a223ec63370346e15afa66700c18ee8435c0cbcf810149d47e602": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7f11fc05cd1a5a698844d3eaeca41cd2637e8ee3585950ce07c49e577fdfefa8": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "7f17786606fad504d3825019ae4c45dc6ff1a9397fa6a687b8271d765c5e251f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7f2fce2af03d4e0d816c635d6f0732b8fbdba1053df29304a44645a0551ac26b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "7fd978e00dc502d46ea8d53a7fe71b2adcaef77c66e3387d7d023a598bb35a5a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "803d96f0adf68ecf8f0213435a816c97822ab179b5127e158fcec8abb1390cd3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "804df72dfcd505558af626be54e9d4ebaf55443c4915d7cd526b9f86f87f2982": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "805cfd22377a74b6a2ecba5845b91cd8ad12af562efd2191f6e277d2b3d26938": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8070093a68837ce38021392f2d225c7dcfbf2fcee6d7ca19e2fc5ffcc662cf0d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "80b724203de46a92528efde7726dae40c0ffe59041eda36e7e57bed71bf0ab0d": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "80ca0ea1349e8ba197e33c55a711ec8b3c622dc0d335d7ae1c5b7e819a05abef": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "80d0a957349d506f33872462b0346f51c157f71e51556d2b6275f62dc8c04f30": {
      "attempt_finished_at": "2026-08-20T09:50:45Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "80d0c944fb299a546df8a5b3039c0ece9c455bd770968ad2ae0e08c8219d9caf": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "80e09bad03db26a8006ea28a519612890b2de23069dfcec0601cbd1a70bab418": {
      "attempt_finished_at": "2026-08-20T09:49:03Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "80eddb4b8af252b3533145d412532a7f47057c94799c1ef8df4fcb17a214915c": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8119e084b8625a66ea6cc1ed620902847dbc10087a44574f5954b1cf0f7e9035": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "811ef26cff45ce98329d72495de69416c28b756b0585f63b084c5cdaa789f586": {
      "attempt_finished_at": "2026-08-20T09:51:49Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "815a3db25467a92b25e43dcea6fb9266fb3caecd64afe0adb4fa25f9321f059f": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "815d46e3df063fc0913fba2d0930905ecdc71e8e0a3a0f11bcacacb527ef3a75": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "81625042f4347f2b80fd5a4d1097f6f1e68534ecd4e972539f922f357ad1ecfb": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "819a1cefe9a05537c40ca15fec0edf9e3993ce24649d2264f475e4c87574d220": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "81afe65eb9105c1bb8835edceda07b7119063a02f0a78dd9c37e511941ded76b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "81b6c17f769acc235bfb24172b3eb0bafc0f1261b88ba26854274721d1bb691a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "81c076dda81e4823e07e87e3252e0d7e0ec893a5cc0bdb8c2fe3a8e7385e3d78": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "81df1a01499b8e55a6f052c7eca5d7af57eded4a5ef825552e3515b2cbff7e86": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8220e7e48362fc90f11f7d9995da9c1097068e81bcf94306ce83557842ffac7a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "82939ecd31f308edd52ce8af3739072379b6854c1108541eb8840899edcb172e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "829c5aa185a544c177740277ea573f0a3c733ea8c825cc6c2142c992d68fda3c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "82ad9752685ad866f926f63c340436bce4262b8ba92d634318f4bde5b523a351": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "83280a007940947da45f81cb42843a138a199e646b51f6c39ed81fe8409cd52c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8351782b2011605729a6bd148111873f5ed66001ad4b7261c2255c3e98d2b1e5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8378f684e5e8214c5eb789f39158bb270448a31b3b825afd8caff970f920061b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "83ba15adf826d2c66bc1532cfd43dd2e53e2b7690ac07ea1eaae77b344b961d5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8488723a528638689a86ef2a7600eadea12d1930f5c338a87f0ad01fe09bb81e": {
      "attempt_finished_at": "2026-08-20T09:48:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "84c95496db7d6b3e17087fd63eb0cd2f6ad81ebca15daf012e4f308d1aed67a9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "84cd5b5653879b9f335e42a995f7e3769bef884dcc6ee7f7f42f1a5b22d7bd90": {
      "attempt_finished_at": "2026-08-20T09:46:17Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "84e83507baa9546e8410b18e24f1485b69c45c60301ff7690db08d31faf0ffd4": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "84fa24ce5e7bfef6e0a3f14eb54e3b2cb10f26a0d2fce1ed8bdb1401e0d33a17": {
      "attempt_finished_at": "2026-08-20T09:49:14Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "853ce6defcb97944f2082542a7de6a8c14001d3cee65c81e16689ed0f0bc5a72": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "85490f70e185d5bb84ee83a8dc43db6436077867c43c885ba4c1363da667f49f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "85979ba2369e1eb27b9d99ca01b8dbec4456db3c93794f47c27bfce6a051d187": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "85ecd7e2e45970dc9e6c2b4dea196918802f6024f33d78b5cdd18fcd043df32d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "85f4a65ae1d3a5623b674ac4bbf64addccb50470b0b335162876e6e91afe5fc6": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "85f8c2febeeb4b86073b0a39dc9a3293e04531f41134b85a8d827d1a39a50254": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8615bcd133303ba7b9941afde44b8e8a2bf35df42c6eb234b8d25bed54d98760": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "86211b1fb7b2c62055614898039cd81c3b48ac76b3b273068359266c8d9385f1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8625e94fbbbba56721327b7a9c9186a865a745262d1b0cfa90a909ba2d9be698": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "86303fb3f6f3a009b23f9666a72dc8e4325bf53c0b3da37e217738316c266575": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "864043cfb0c314b40e7bd07d9797094371599c08deefb7c369b0f260438bd5a4": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "86591ebc15a03bbdee315d5e6e7eaad4b7dc1d7c4314f9cebee2a77aa110167a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "867ebff433ca0efffe839dad2338361153444d4fd4a658098ebb9dc628f59205": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "869801b6135fe56754cbfbabe14a9359340dc75c864cd2b8b3e25c169140fedb": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "86986d33b414b6ff135c515ec1342ecec0deb1ecbafd799c15bac54d1fc6336d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "86f18f5395e96e8c1b7aa8d798ec00abb582b53fbb696b33d8c5c010b755db3d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8703d2388c59d0fba1a63f8b5850aa83b8d926db7f6a57a62a93b4dcebe4874d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "877325a818fab2a4a7b89e7a061efed72342ab2dcc9b868a522476af66677bdc": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "878a6581e193fb7136d16fddc89224f5d4f74bd58c640793c96bd4365fc0de2c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "87f383784113301487975a82d00877d11ef306d8f9659b8c3494d73ec6a665ba": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "87fd7bef0b4cb973d008f41fa2a0484ecec8e6440768775cfbbaf92a1f18b386": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8811de2db59bf82a6b040d4b487b39c6b68827f437dac7fbbd7d64a791bce9f4": {
      "attempt_finished_at": "2026-08-20T09:52:34Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "8881302bafe35acb88ee7e9a0dbc4b39a803834ab0d64e57e6d7584947aa5c27": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "88846002bc1d63ed06c3fd1db353d3e4dde1352f58754519bb26288e69e56b24": {
      "attempt_finished_at": "2026-08-20T09:50:15Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "88fd55bd25e5b045354917707e6452ef428835495e830013993be01263a4a4fb": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "89145515501ff13ceb5da2dcdf8c984e6869113dd4b18ad5f82a2e361594c891": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8931672f5b7ed778dc47457e2ee2bc7c3a09129bf63a50dc53d158c9749ee69d": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8957f02fc5b6b576d5cdefedbfd30d891b045199ef7ab546504b08adde6622c0": {
      "attempt_finished_at": "2026-08-20T09:48:21Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "8963602dbbfa056897be81fdd3d088eb7e45e753c512a6abd28a50402d6b0461": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "897402eb7ea4af8a3bf814d549c33f40a881a60c4deee9af927305cc9c89e8a7": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "897728c1ea9e2ad97875d54c5749d65be0633a515c7f7721a365005d0da54ddb": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "898c453580b4dd199b9bf395742bf5f296ca032166b78b26f5bf4ed0ad1ecb1b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "899e74363dd43b22323c43db5a29f880584e739e535a5d417a7db735de138420": {
      "attempt_finished_at": "2026-08-20T09:49:14Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "89a04f08c122ca40e47d01ccf3b8cfff33f8ff53dce3791f5f08d70d076e0ece": {
      "attempt_finished_at": "2026-08-20T09:47:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "89dcc3bd441a077c53a101354850253eabd49a627f794fc3c02444fdbe7d0138": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "89f656af937333cf360011ac3873869732b9224d1c150fd1208293220320fbb6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8a00a946fcbef6f56f02157a987a24094c2a73ee042ca9df6859a275c027ddc1": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8a1fcdc5b8c214907ade60d6c3ad037f7cd92aeda15e265565339aefaa201da3": {
      "attempt_finished_at": "2026-08-20T09:51:17Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "validator_rejected",
      "provider": "groq"
    },
    "8a2049c1125c93435c760825647700ece28c3b5f838a1e0d55b8a6da21a2b54b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8a576f472298ed366a060023580d5aba920d104fe42f78d39dff0c02451f757d": {
      "attempt_finished_at": "2026-08-20T09:57:12Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "8a7db5f5f0ec02a35bf8e6e53accf5e40b97993c5af1787f61c7a6650b3cd236": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8a89a8d63d990c1833c4f6aaea8af92af78579577d7a8b8734a2d53c801f7dff": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "8aa4129666aedd1b65b84a24080b48cec9a429b27fcf1b42b1db374a7c1c1779": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8aeff7b0158121583b69768de3cf937d19e3e14fae21f14704c02f8315aaa6ce": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8afb6a8baac71b903c21119f759537e7ac05c14901b16b6c81454dd4f1506729": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8b01a0c6e16b15a024e8ab7a444aed6820be75f3ceb5155ab10664db68dcb93c": {
      "attempt_finished_at": "2026-08-20T09:48:54Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "8b530f95561cf801e4d93ce043ff6b01ed0a810308b049bce92a6a802152ced2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8bf52069149827280a94740773575bf9392349787ba31f6a4eab49ac6386801a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8c004649ce881283855348f66f96f15df8daadc7e1d396778a4bf62033540bd2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8c365faf90ec231e3d8b2de367c8d193e664daf511371654dc4cc2a788e3c784": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8c60db45c6e562197f912a9161496371d16014fccb62d63bdc3624951cd1c356": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8caf79345def096eb4750c43085c0fe5d0e460b43da1dc64c45d9a1c5dc3d052": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8cb382211416055c6e4c7654016ee25e4fb991ab1777d3543c424880043698bd": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8cdc0dc269e422f143bab250fa636780f0910b5119471ec9d66e30c780e1dc72": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8cf4d3d66cb36a9134f45646b671ef7305003137ae78423c769cc7a88c34ee92": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8cf58321133523791d1fd63c99df0314caf52e3164605b2ec092b7e6b48e338a": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "8d0bd7ec72547b3b8d6ada8c2cc20d81ab281ebd9c00e4b5946a9c009ddbc012": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8d2f744155c47379e5592334b08be63ab01a4a12be1e7a97a747077b4c898c5d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8de0e1234b7cc60ed6f49c9d40c12a606f9026c6e9ff0bb648db4ce1bd5cc8f6": {
      "attempt_finished_at": "2026-08-20T09:52:11Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "8e02b41b1cb3278cbb8d00753ef65a58334738796281ec2a0acc5d24c6dfe1f0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8e15e82afca25514e971c447cc186b804aa919cffc41037fc5371ba71702d9f0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "8e17b66877aead52866cc60e04ad2c296bb0345265e10dc1c989ae6d16fc69dc": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8e183c7e20134336ab11e63c74599bee5fa25bf0fc5dd92f36b55ec3e8946a65": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8e4128e9f07b80d8834e297d8d4e4844a008e4afa03ff35b319dc21f446c6292": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "8e61a06e5abce4d4e088e72f6fe7dddfe578530dc6562dd648abf55d4e73f847": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8e79cf82cad1730b785424b9987ab73e5719f23e64f7409c7ad2fb44301bbb70": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8e9e6c5b6f6f4999df62194496f5f8a3ac7ebafcd9c84d23a51466d60773e98a": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8ea946394ff41f941985d5e8d5d57976be9146e441c7cf40f6df6d6bec6ebdca": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8ebadb1305d5623fe8a4ce813c8b139f56d67b0ecaef98c9d9350804160f572a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8ebf38693eb185692143fcf35b7196b99af7cf752a4531c4e670e42af009e4c7": {
      "attempt_finished_at": "2026-08-20T10:55:29Z",
      "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
      "outcome": "provider_failure",
      "provider": "openrouter"
    },
    "8ee326a4282f4db359f9ace55ca99518c04022c6b7c5c230a2075eb7b72ace76": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8ef977ec3d7f2713cd48e3a1da076f350db9badc85892bbc1ff39404523c0152": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "8f249457f04d81e271dafaebaeabd5326c3696d185747cd6a607f79aca69c165": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "8f27afb48ad6e86cb587c28ebf94600f4c4c1dee016f27f2e7074ee91b7795b7": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "8f4402c675a5cb4c65f237b89f0d001ff9d82e023b4e076328763492c70f26c7": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "8f47e9ced73d57595de6ba54bf98c1473f4a6f3f654f3bc6f1128ab8ad9d7e37": {
      "attempt_finished_at": "2026-08-20T09:52:39Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "8f4c24ec8c7b72a181a61b8cd12ba67bb19f427645e09cf565e490356cdf41e6": {
      "attempt_finished_at": "2026-08-20T09:47:45Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "8f57222b86408423cd814153b83d4e7881037a712546e78f428f7ce20645d854": {
      "attempt_finished_at": "2026-08-20T09:48:10Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "8f6e8fec79fca69fe18f07e0f78931c7a3b0319afa98cbc36b97296328cce275": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "8fdf263da25f5f59763e4e9484962f265ba1ea828c87b186931e92e3812a8c48": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "90102aa20e530276c220ab4e9d49aa2ce5f52b4ed8f07d71bda39e5b42f95d07": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "904d80faf2d89932d4698ecab0834439211eb48fb779d6f2af491463447ad287": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "905fc996c5859190249f20de64e1cee4227d2dc6c889e8a7266b0ea590a2d384": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9096fe3a59b2e734577fb4e972b400cab0ae596ab63833046a6b20f755f84e88": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "90c5e8aece360656af184137006b81befbff38f63bd0a97cb4b4a00b5f1b491f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "90d5a52effb8b02ab9f202888b1af87843ca8d9aac755478c03ab56f93dc78e7": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "91326570f7b212df52f7b71266a099043cfaf73df1f1840eaf45aaddaf6476f2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9198aa0b67ca74634f3997d2361a5c2cb9260d68b48cd30c04823ac35530ffbf": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "91b8ab8d197d6313752b5208cbbeef0f7f7fd5c66b392df41f3b64e75c195138": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "91c020f7b4e80bab0b9a47d7791a06de87c378b1390ade8b94bf752b93fd8f05": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "91fc9158cb33ed1a9b191372b87c357d91528914ba7368c81a9acd24cbe40eaa": {
      "attempt_finished_at": "2026-08-20T09:46:10Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "92061ada475df07ef0e5b635e2ba4e2d5c0864498ca4879c1fe71af8aacbd0b2": {
      "attempt_finished_at": "2026-08-20T09:53:19Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "9219db648f8082a66a2eadcb31e08153358f12e36e82d424552416b9f7508d6e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "922a00a3dd7a8947709c82ebabdeee42cc2ee81b88d19e0aab2ae0804cc21e98": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "9235ad11ac0ec5bcfe70246777bc2fbfe7c77accaf211be99e47ff54558c5fdd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "923ff389a1b0bc1f112cbfb2fa160ef8c6d02df6b95f0b428de47a073e4295f3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "925dcf6b56b0b655e6097c47a6aad2f19d2e690c21a72feaeb250f9b7f60b112": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "92ac63974a27ea961f708f139ee1676ca1a98f7998a686befa172f94ca688bb2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "92d24fac89e35d0f2f3951c1c8c469401129aede90a80dbffeb2b41562d6ceee": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "92da1aa3ab7e060870009eb894022fbfcc3820ec130f32bac1004fbcc19eca98": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "92de21afc0c036d2096dd6aaf9349c18666beb0db640ed2b5fb9082c492ce6e7": {
      "attempt_finished_at": "2026-08-20T09:55:37Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "9348db65291471170bdeab53e0ae34a2909e5b9b387a8fcbd721a81bd579b275": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "935fd1354d7171943ddbd4013fd200105abc9da4c652b2a586b963cec6c82bd6": {
      "attempt_finished_at": "2026-08-20T09:54:18Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "93932645bf6d6053e9977b371eb5ca50b519ff1e8e829c3e8e7d2eb0cf39d9e4": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "provider_failure",
      "provider": "openrouter"
    },
    "93a2f625c383dc3a013dda2bc15d5a25ef468664cd60adc7a103c0921df60afc": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "93a363226d168a5718c0f3be93dc48b40bf3065e5396037f6694822d3c66aea8": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "93c6a0141054b6fa35f80c97ff5b359804950dd94f62c23341b37757fc8686aa": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "93ef3a8d89bc7d9e0f419fd24b47aa44044cfda6733f5563b163e962a4b9e3c4": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9423e50eeedbae9689dd3a46f0a23c161735bfa84ffecea04262dba66b560d33": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "94285c9fd2b763cdc101e49472116d2c271064d3a1e5e5e8f34e268f57f819cb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "942a44cece93a3ff88617a91ef8c3b901f546cb23f30445f79e141b634122aa9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "943e0b74f9190f90b8db5be0e9409150c54b27909b13f7e2c61ffe5c6de48202": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9445ac06b04b23c6fd4bbd4bb88d5fd746b407d48c34050d99b2cad3ac8f5b06": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "945082ab9c16b38988ea4a0fd0517ae972b40c73672612e674d843b412b56202": {
      "attempt_finished_at": "2026-08-20T09:56:33Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "94a4d124ecf8ee8caa35e6c3b462221e247969640788fc8b15f9feb8370d5b0b": {
      "attempt_finished_at": "2026-08-20T09:52:12Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "94b0f29bdadf01aff9defc2dba53afa34a7a43e886e53d576f5122396854b741": {
      "attempt_finished_at": "2026-08-20T09:50:35Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "94c63b699398b7f91afdd44a5f018e314316a0144ef8913f72e9c8bbf2b275c9": {
      "attempt_finished_at": "2026-08-20T08:57:46Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "9517c06adf91db16a91cd09bc007b4aa432e2ad9b1597b712325714938be5c0e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9522d023514bf946984a2dd0c25cad94b1e143e6e97229a7f349a27ff1097364": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9542ca05ade6e4e9baecbf135ab22efc00453c24f902396a760379bccbee4018": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "95460899f03b8fb4c23c389a265fa971a482ca89d9e02fe813b9e8c8e3d82ace": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "95aa87c5470662636e961d64d82485046654348bbcfaad423ba5b9e82ba47eb9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "95b6c6a4748d05dc8d2e91f8adf97351f7be376c0d36099883dc275aa2440d3e": {
      "attempt_finished_at": "2026-08-20T09:49:16Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "95c20d22a16e3b326999a458cd9e31efa85d52d2428c9ac34c40fd092b35475e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "95f79f79513f910cecac303004db91c064c3ba339f8448c9ba4d6b4bfcde59e1": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "95fe909485105b9ae1838bb637a28513c0494c5d1b5be977f977764cc95e0c30": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "961c83e3d06d8d906ade35efee846790f67d1e33ddff1fcdbee2f88ff7e9fd2b": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "96dd802b9c636cc86c992d5f30d94467ce584e6e1823d06f28dac27fc2508024": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "973229508c753c849233c8bb6b51549b9a32a87a936ba6eef51668641386395a": {
      "attempt_finished_at": "2026-08-20T09:49:01Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "9736204df16e7bdf3ef32984ebb5a2f39d4f3a17e3cf1c17a4feef19ad0a91ef": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "97a6245d7a46551e44fde8c80f73689df7a60d99609daf0cc92dc207b8956a79": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "981b03d655fffddc849ec7b96f8d6f3dfda7cabc69cffe1fa7ee4e12e5444d3c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "985e7b4814b3e9f6db170eee8007a501a270267aacbfbdc3c3f9e2bfe99ce95b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "98960cc58245f65350b18416954fca87c58eb0f853ffeffba07c46eef43223a2": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "989bafbdaed5bb66eef1a95f72bd80fbe428f8e5190e4c010f58344461535679": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "98a90b8f9400104bcb4972be0394c2a8b5d350e727b824e556bafef675eb6b0b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9900ec3f3c72923e026f4d36a3f11d81f598bd4baef093d725afd5567fd74d77": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9919b5942c80135bbd36cfba79134041b7e8097e12ade93b5abe5d52bb0169ac": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "993a25229d36ee53e50bffa598d1ada48fc6e5cd8ff0fed9682b24720276989c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "993d07fdbc67df66e5b9cc0951a342208953e35191a4f23c48de0607fe7673f2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "995660b82528197c9192a525069cd9257260a2f3e35a7546cc617d77dcac9265": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "995d25a8c39f32ee4c158e092e741ea0a2f5b43f828e311d6bbfd1bab4d4e8ca": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "99836700a1a54c0e9989a649264b1ef032b76527be1b61c748105b97f73018f8": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "999345e33180ef0fea62332315db6ed9dc99279e7a5c6518c5cdad2c9ae63b32": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "99992da3e27179426ed82cd6495b7c9a0c40291942c443a77012d6979f9d259f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "99b65b13850afd20966eba36892b6ddc03aad64619eb5200b5cd5932a8e079cc": {
      "attempt_finished_at": "2026-08-20T09:52:10Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "99ba5e866fac28d9476b52d0bd9eaaf0cafb686a167f4fa454a2b034d5fe88e6": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "99ea3d2147a14df3ea00b5fea455cfa35cb21d7022cbe6906810a77723c25dc8": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "99f9180bb97056e28cafcc4da35e42e87b7c6487b280a2b2fd0834faa61d2701": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "99fbd2ec96d83db4a6c3708fb40f5786df48147a7fbe2d15244e1b9ede321a25": {
      "attempt_finished_at": "2026-08-20T09:54:42Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "9a4cbc01a96f6068fafb432b420d1fcc4a65fe27497e4e00810b9b5b3be31486": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9a6acc1afb04a34a48a8433c4f8adb83c64838a318e5d487246652d166fa9025": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9a8b1489be5a5648506316b47515cbe91d4aa6fe9fa486ac324d1b1842fab840": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "9a8c59c68ce198b4499c6643248ce11966b1ee70a85b206fab9745fb44b933ed": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9a9506c617c29b53ea6ab0152eab5f420e648d7c721e6665720f726674e3e5b5": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9a960d2c1af18e8d0ef4ff29e4f9d64826450c4d360c2bc8ce5e56fb0c5aa42e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9a9840dfcb6fc5a1c162772cc51746e6e67d4ad6554d09796bb78538016b3c77": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9a9d4a225ae3ad75238448f38ce6974a11ae1468466909c54b1f1c53dbad831d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9ab79e0de3839f62e8a943809448cd66ad27f0156da6fb1761b645ef9280eff0": {
      "attempt_finished_at": "2026-08-20T09:55:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "9ac1a73a450658a3c72aa26f2fa54552d7298e8562873d6c27116b3d7ccc6a49": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "9ad40a5129f90cb8e9a5e8cfe7d73aa2581cdef2b08dca3a68a1d9412209ccf7": {
      "attempt_finished_at": "2026-08-20T09:47:02Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "9af29f9a6293de9efe2222d709dba9d681a4428b85fe51243815b7c362e78883": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "9b73413d6d33d902991824b3f021e83dc64cf75561a99386fad47673e6b75a75": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9bbc4a6889391a1d34a38ccfdeea566b7423447e9be6a98369113280983d47f6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9bcc3302060251e81ecc767f99c247b071450cf14db579a88911b128ea41a378": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9bed4d634810c833c9238d87d8b4445024b8b0cc7270efdca21f847a59814905": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9c035a4275c4e3d3c506f577eb7736575ad60003318dac9a8a67db82d3126ebd": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "9c056117a313cf2132b056806c1ae2a3b647b188b78d74689d7db5381ab1422f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9c0f1be0a2f6312d4dd59d1a73e012190fe4b045814c3aebacd0615a1a690680": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9c38e9cf4bd74ffaf1bb84b3840132de8b5847525ab9f1cc5be880dc2629f9c7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9c53a74001d5bc4b2eb5de38ce656bb4364382058dfdda54c7b6e39dc46064ed": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9c95caa738185217b426c993cec0dfcffc5672d927efc8762f5e0fafd77a5f2c": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9cc4caca25d6780a8fa817ae8804b68faf5cf98832159b9f0cdd7dac50245239": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9cd71bc4d7659ec3b9ca9eae35fa61a3b49a64a221bf1450ae802531de8ea43a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9cf0db2c40c00c9acf2da7e904fab9dbb8fd558cdb128a966794c403f055d528": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9cf0f2ddccca352e21752105d1aadc2419889d307e598d4add9baa8ce2636237": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9d68bcebb84e5da57270a4fa6677d2420e0582040ee66109efdaf73ff89da1c9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9d7fb255dd39da9e1717b48a27c51386d908e4fd9ed9a6b1815de891e5cfcb2e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9dd2282b975e83e9a8b71b82f5d9b756df4c0ddfb7812a72e706b89d7925b0d0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9de2f0cf89d2a8fd0e1bed6dabae17cae0bd7b95a2e9a6c1e1bd63b60d204bab": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9def07738659eab0899b6d79058854259fca6b190f1e5ded82c943d9335bbb6a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "9e0586adf08ee8bbe619e9fe3de38171dca8eb96fd9d0fccea1c19f1a64f925f": {
      "attempt_finished_at": "2026-08-20T09:51:11Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "9e2160d193f09eb6ae3f94ac0352706aa89c35717a549d0b103b37ce98cd22dc": {
      "attempt_finished_at": "2026-08-20T09:47:38Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "9e58595bc43737ecc99548c4f8844cf0250b24726593f2d53017e777f4a1d6f0": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9f33940ed93dcdc828db30c7b2181ab6dbf4ac9f0214573e6ced701ada5220c3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9f3af8f3c7de4aef82f5d583e764d931e240a68f85bb2a1eb69e5f359a45bad0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9f3e2c4a536ad1bbcea457882d2bae62d343ba799282efecdde20341130e512a": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "9f59fc23c541cb2b72cc65d3a1ab45bf1b7473cf704c31a71a09223aae7fdce4": {
      "attempt_finished_at": "2026-08-20T10:15:23Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "9fbc369623165336caf73baa6c3335135253b1a4e3f4af82abd3a4e883124c02": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9fcec4aae662a95fc3574470ed20b839486d11f6beca8a43cdba289d87de4fc5": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "9ff43e97bb97a7f6566a073b2ffaa660037b804bd1128fd570ed61d926222c32": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a051d45ff93bba45f75bf19060c1cb2f8e845f88938858f95bbc354f52bfbbf0": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "a0788866c4e82bdbf34dfe7080e22437846823290695ac5733fabee80e0a72ba": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a0994c12f1ecab27ca11aea12603f493733c17f624c3e955faa909d3aa659787": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a0af41704cd251a4150c05762a5bcf3ba825f4c1d6f0ffa309a886ae81ab180e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a0d5fbc985529227752e58634a65d67df391f8ffb82ab431284e829937aa8edf": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a0f59f54ba2207195b96f5fdcdbcb2778861ba71a9af4bd22b5925e204921109": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a19738279fa69a11be28ece124c463a41e061f41805e55b5e60544be38797d74": {
      "attempt_finished_at": "2026-08-20T09:52:11Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "a1aa150f0fc87da8455d064d5030e4010d6d4c1341baac2ac379612d9bca78bf": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a1ddef242b1db53d148c2d24a098fde64a41348d44e63eeab447ee7a4594431d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a208b3a14e4e4ffb3e512371d62d7d929421a358458f813f3dae42e7064e7602": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a21abcfaa7e0bad8adc55d8dd512176283a5f687af0bf5ed6591683513fe70c0": {
      "attempt_finished_at": "2026-08-20T09:49:06Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "a22e572633c5de50e573d9419e80d4cbdc643519727f324747885f03f3e65a2e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a2b5a37889b1374b91735a16944ada4479a080a5f52da65683cb8fdcc18b7cfd": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a2fb89eabd56e5ad355cd6221c47895b40c01ee85f576b963d9dbffeeafd83ae": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a34b0a386fcd25cdad1cbe384858e90c45de684d99f17dd01bb879a35d50d760": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a39397b49efd398fbb1ce7cc2e7f6e2202586bfe63bb39fea6fc5cf4aa1af109": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a3947a24de3596259f33d8799da1fee884ac104eb593cc4c4165e76616aa8bce": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a39a09d32aa4ca26622da91545547872e98dbd7a3374da92918dc8701f77f30a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a3c1b1bd0f68f578b46b4a6134c292e58d78c57747bc239547258c8771e873dd": {
      "attempt_finished_at": "2026-08-20T09:48:00Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "a3c9c15ba1e64df2842e79ba0797aa0ffbaa1db991d12b77184caea8492d1832": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a3f56b90db861f65254ac3fb8e7dfe37b3b5be9f46f1d73436a54d047e6f81f3": {
      "attempt_finished_at": "2026-08-20T09:57:34Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "a40a8afedeec1c84e055a37d8c1b9586ef6667188fd99a92b5b6410d6e24c701": {
      "attempt_finished_at": "2026-08-20T09:49:01Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "a43e551e4c1f26fac6ff3b89642753857557d6add04e06be79fa5be81ebdd82a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "a45c3d55110a8435c07fffa5c54e33f62af295efc17ddfb66aeab992826c4ff5": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a4adbfbfd37930424e150f976d55a7069f49e9b35964bd683282f19a963d655f": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a4bb8eb8dad00619a6929cb4ecd4bc779bb319bc6e2646504c23121fc2344fe4": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a4cfa2963616f638eb03c45270d6502adb1fd924d18aa7681241596193eabc7a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a4e81355009aed81a5988bb42e7d0f1ba9e307cfd56698b26e1a464ef5601952": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a4fce804b0e0513892db6e69241750fb74f4034ea1b5118f6d8e0be87724b96c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a52c83e154b7d4e95aeba6adbfd028ae5a089e1ef0c3c50744f6e66704af1690": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a581a6d07bb8074bd428c32847817970c94550eaec7e12a42b29272efcfb3060": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a5a258323ae0df674398166e22085680dfb2e7285b44619dd97e9ab6092b424f": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a5b118643569a0a6845fea9dbd7ba86de5bcee1a3fbaad42c0c894062de09ec8": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a5f8aced56ba3b641ead5ce655e5a0b38e7f7ef9ad5014616c7cd34e69d0cc47": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a63b7f98a2b16d2107cfb17dfaac7cb03cfbdfb1975066f5177e645ee14fb22a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a658988273acddbb64fb9b0c54ec33066541d668b0ac7d97798cfda7e18e8654": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a67c480fcc561586b4da4afe9843e4b40683ee6d7bc1f65360712336a77de404": {
      "attempt_finished_at": "2026-08-20T09:48:47Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "a6dfbf2d4486c95c8794afe7e7023c229a02fa38b5d86a338c4e509643d1385c": {
      "attempt_finished_at": "2026-08-20T09:51:48Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "a6ecb733802a42f2f8b7e73f9f64f1c445489cec592856d1a80025bdf68d324c": {
      "attempt_finished_at": "2026-08-20T09:48:39Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "a6ef66ffd7fbf77e44c89bc7c60fd44d9ac97f575f0b6598994f7d6256146df7": {
      "attempt_finished_at": "2026-08-20T09:49:11Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "a71332904ec067b37dea70bab166bc04ff12ca197a3bdb90ab6848b065910544": {
      "attempt_finished_at": "2026-08-20T09:48:05Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "a73e4b8284ed96b473a58bd3c7e9b07a9e27a7fb59b2b5bf8206da0df4481493": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a766804e4448b5798823a7a0c844af950f4bf5d4cd20dc6cbca8eb9d97a64217": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a76e464be8b5d4ba6ffe00f15f52bba844195c3d3fba07353f38c724873b9e12": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a7bc5bee7a737e8b28276858e17e486ed3c3ef2ef91feb2461c97f053141802e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a80a574e4f82e88e9b2abc451d8bfd7e8d33be019615daefef34fd73ee24c098": {
      "attempt_finished_at": "2026-08-20T09:50:46Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "a82502d4916e5273cc6cbbd9c383fc808f0a2df2f6e99452b969c8e5ada15c4e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "a8c937327e6536cbced5fdfa2b034e97b84896166b938bf2991b7e40dc34062a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a8fa4ab54aed16350745762b44924966a2c48520f9e109385c0a6db12319b240": {
      "attempt_finished_at": "2026-08-20T09:49:28Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "a9188694ee7e7d855297235739402b96e51c687694e07b99b6d46afc36f28c56": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a97a67057b8819573ed37acf9e56037c374c761c27c3f2750367142c851df8dd": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "a9e14233bb4a9975d26399fd20c639c87177ad40f2e2a6a5d8d4e2284b152c84": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "a9e75bcedf80f26dc7c2287b8084614cff4878dcf68ae106e9854eac88cdb3cd": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "aa05223a25a59dcd3dabde89237b5452b3fbd937a1b241efd13f936b18264d55": {
      "attempt_finished_at": "2026-08-20T10:15:55Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "aa38a088c1c73fcfbb3f8e1b065dadacc482cbc5d31af8217ea00a42adbedc49": {
      "attempt_finished_at": "2026-08-20T09:52:45Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "aab8d109bc22398130fbf6ae67a7a78e1ed12e87707a1cd4e3bebc161b6593fe": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "aae0970c0543903283d97eab654851bce0688643e3661fc29b3a3e81dc20f7a7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "aaecbde08143f8880240e90e49be930cfe92ec782dd2397234af1672830d53f8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "aaf6751f0d923919a3718b475f1776c6efc7a7f8b51b4e20f0af5b56cf95beda": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ab051c4426601278aef1ceb4ab0b7612d0d057ca21a1af129b936f5fba03e630": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ab1ee3cc16aecb1f549bbe58a09d23df22d62081a12e5c4c63d3022fed086f9a": {
      "attempt_finished_at": "2026-08-20T10:14:58Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "ab27bf5e4480e8ebe7120065a23c87203537ed2af417463ad8b045754f406043": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ab284c0a5045080711d089d56027085b299826978ac06a5b13083d99eeb29204": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ab50f298bdbe7231643f0b1a5c056d11f1b939372a3a1b19fe6728d8fef9ed7b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ab801ccec8179de7f8c8ac01a0125e385813f1fa143d80189fb9df80c0c6e419": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ab8abfc220fbebc21177166e13d18563e224ab0c67d3ba88b46de1aada204184": {
      "attempt_finished_at": "2026-08-20T09:51:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ab933309f7c0dc8ffcb08a47e2a73cafa03741820f5809f6797c5e451c29c5ff": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "abca208f0dfbe149036baa3313ae3bf9df6343cd474c45dd10fc52924a24c98c": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "abfc30c90d1e132b018324be084c9f6ac332f77ab23972eb22924d5b63578162": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ac2c3267634697ba0f83539c3e945c39cba6e397c841472a3bcf7dec432520d2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ac3a8a8878e2611b2d1b0821d7f547a3bfeb08bc58d00bc4beaa3b0253a551f7": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ac3b74f1e6d969901ae66e621cf83b89f91afb5805da9eab15a32b4feef87a08": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ac3bf52a1e2fde8afdece68b75017e02b2657dc77fc53ea4d7e8f835ad0d8341": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ac4d8ce331d062266de7b0751b4cf08d251c2beeb8a4e6747ddeba2be14f5a44": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ac82d4edabccdfb3e0f4a141b0f7069abbfb1ed349ceb2a0f3d670188a344848": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ac8db525e18321b28f2862e3ea243cc2db4afb1e3d55910ff218bb1814d86f5b": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ac9705a2925d981909262fba5d64aa91bb5401ce5f7bd4e48734634c23c8debc": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ac99c66b9b060bd16ed4f58e7e19c46cd1629bea3133ae2f649a14cafb4d1aa1": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "acc95731e1b9737b98da73d0571907d9eb899dd16de3c9a2a7fe08a5726456e8": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ace058c451ce4da3d8dd6f890c3d2a0d587186eb8262a1a7c3a014c7345067a5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ad60f9536526abbeed190f6df392c5bba40cb9302ef76255e3971084edff665f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ad74cefbfa687dfc7c79938777ebe2a744f7dd160d6e4b648205da5eb3310935": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ad910824a6b52e6c530afa6d5b4de6199e1f5facf201ff5a1cdf8740665e7a3f": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "adc6127b76b62f7fe759bf9fca1b3732bc1bcc1e835b4e2ab8a8fbe4f37f5278": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ae75b3dbb6907d18d9921ee2cb374d2d8c70faeec6c1a9eb43e3e4d5b1e9f380": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "aea7a6d79f1bf6c510f29ea4a7190b8ee86db8de0df3fe663a923afc418dba56": {
      "attempt_finished_at": "2026-08-20T09:50:17Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "aece87123a7ab5a4221043c25c3688b0b434a7bed61ac1ce9b0278370be4345e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "af5c1823853fa00cd487bb8ba15113781e0efe6801713e4b17844090815d6581": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "afffd7a3e3e70b4a0d047d907ac6a4acc951eb3bc719f3936e6487cb7bc387bc": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b004051c2c8c6872ea255c571ae2eebfedc95189db2bdcd2ca064468117837ce": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b059bd6c3aafb56e822dbfdce76db46bd7ee1c9683297a52e5b98b9e96814ccf": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "b06b90b7e3925ef2cd95ac7fffe8f9ce998864a23112446518d64246f475a17f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b07a3f049ea10d995cd49fe775c74009273f927cc29ff7b9219b3dd6dfb363ac": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b0a78f6090ad2769fd207f5b5061eba6b8e6a03272c9168ff21c8b67a06793b5": {
      "attempt_finished_at": "2026-08-20T09:46:50Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b0e818aa20ac464af0af4314c662d8cbba3db5e904537857efbffcae64b0c4cf": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b0f70c5ff40533eecd05651d8154d8438e474b87d0a94c0b412368494ddefcff": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b13725c13b3977f664373702174f9ed9732bc1a8843dc6a91cac9de2f81059fe": {
      "attempt_finished_at": "2026-08-20T09:52:16Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b14a2002a1f55cc5ac95757fc3981affa0a9b5f26c5887ce3088d2786cca716e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b159aed9798698bd139e32ec83c3b70f8afd0a05b823e378b6bfcbabc78853ce": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b15b9fcfe097a1d4b4e22a904f3f1c684e10cea8a185359383337791613849cc": {
      "attempt_finished_at": "2026-08-20T09:50:29Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b17ac1a20f24350e6749c2bf20d8aea1ef8b65858f19d74c6ddd3629641da248": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b1dccb8f69580ce8c93ba786c9f50ca84680e9874a66c388b44c94fc2057df4b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b1fd1ae9f651153839b51a0d34f3db684e2713834f15e92cebe4742985c8487c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b22b2d6dc12c9036cd69b994eede1a0d75212acc29ff87e567f6896547c7c536": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b263cd07089e14c41d5ef331abcfbb8cddc30d2e631d1ad932ba59f06b9ae5b2": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b273f14035dc634edb7cedff3745eeca06d1e75d30be1d9b2570bd38c869259e": {
      "attempt_finished_at": "2026-08-20T09:47:24Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "b28ec7450f2f7431e1be29eeb3165d115fffe76cf5818a263e8f5b8cc6e4ecca": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b2b17e694a9dd9790fe500a8f7662784005ea9f6366e9839072ce80e7154ccda": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b2b5196386b1a58202f0e56e02411a61bd402b6904b5413b1db4f78a6f3975b1": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b2b7c2b794c49596fd3bcc1fd5a6d5c00661516fda1b1ce1d4075168c74e77f0": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b2efe61e46b960f108a214f38d1736b16c9e59052220757cdd1fc8c25e98faec": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b37fcdf9472c0fb0dc0417f6e73ce73bbba0eba5e61c124b9c0a838516fecb62": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "b385649f647d14007033c03f44dc2b88fdff1600dae41952ad192d62de5d6191": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b3ae04d5016ac11c87d38fc1393fbba5dbd6c71fc6a55f72674884c0c93a8af2": {
      "attempt_finished_at": "2026-08-20T09:50:01Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "b42869f80d68602a35479bc73901e26cf2abeea896d52689df043de3c7dc12ac": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b461d8026ed3623e9a4b4b56e776eadb15c8ea6b903e4614925583ecc0a4f628": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b4627843181c1e4113bdc6229363039db4769894ba52c42cf2eeadd93fe939f5": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b484c03869680fe5434c5a2cd109a08a78fb0bf552636d65b0c161758be435ba": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b4b3ba6e0b82930cd05135a6e5335d3c391e7b29d65bc8c20cb653d5cfb2b091": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b4d2f903b1a1a635cd6a2f14c93d1920390999151cf7c5c7d4dfacf526624694": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b5a425fde9353f837723875cdee02685becd22bba30cd51536e2a0f9aad2ddfa": {
      "attempt_finished_at": "2026-08-20T09:46:10Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "b5fa0752f30b59c344a5ac494ee30ea1eb9cb20ebb2bf6e2162753df24bcf53e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b653400b10ec036ec81854fecc65dc36089e9e7b2ea4a04e8dc354a77e03604b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b6896f910dc21b2081b1fdd5f96ed5be9101604af9cac5cf78857c637e8a3d4d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b6f559352d18c6c4c05cc8fe5f261ed58b8834d69161a2c928d532744b8401c3": {
      "attempt_finished_at": "2026-08-20T10:14:47Z",
      "model": "MiniMax-M2.7",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "b6fb4b4159da129fe9f0ef06735bbb1b3ba07cdd70460ade25c0a8a2e8040450": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b7106d1ff1efddf3ceeb8de02e49d283cb80d35f8f616b971605ee535dba748f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b719223ad6b7132f93201d5d5851c28c21c211d767c591124534b23840f58292": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b7440ab89b3a1fc53948e8d7d77014bdf9c09949814c2b8b8f4b0a70fabfa98d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b7a70e17f6890b4da3c81c4b3d5916fa15d26e09ca7df6acccd59e3174b48bc7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b7c471668ae02a1d3c438f8c94c69fcccd3817961388d21b37cc673a2c953ba3": {
      "attempt_finished_at": "2026-08-20T09:47:19Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b7eea0c2632611c3ff7a9b9805459f11ee3ad29d5c2bd2b7bdf591a944e3b999": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b80f006442a09b2ba1540e739b6cd5c63099cd4509d225a5fce289f453cb25e1": {
      "attempt_finished_at": "2026-08-20T09:55:06Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "b80f645f4a861df5dd82ec7cadfd919965fecae8ed8fa8bddb2559446f798309": {
      "attempt_finished_at": "2026-08-20T09:48:46Z",
      "model": "gemini-2.5-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "b84be5ad06332789563261f8d68cba25ee6933c13723e38239ec0b017e0a9a9d": {
      "attempt_finished_at": "2026-08-20T09:48:33Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b8596cbf740e1b2badb1d54f030fbd6e562b31fd5dc57c6a605090fb80bd0876": {
      "attempt_finished_at": "2026-08-20T09:46:20Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "b87499aec99b660dbf30726626d01704e1de6a9a4815d24d8346e353e3161fe6": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b87cbdfed887982bc5d06e0e483d191260f7a1417163a518c76b5a82ee801658": {
      "attempt_finished_at": "2026-08-20T09:52:13Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "b8a0ef3eac8c0d90b092a2e100743cdabf05a8e46018968b99d88dde4803e09a": {
      "attempt_finished_at": "2026-08-20T09:48:09Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b8a114914cf8ff8dd3089ddc55112bef037b764be8fa56e8bc98d97a5b901568": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b8adf9c6ad36cfd71660749a5d01665d08323bc2026ee82f878c3c5b32e3d828": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b8d0b7dc6adc581913368da582569c5ac41bc1fda55c538fad2a7cbcd93a8eb7": {
      "attempt_finished_at": "2026-08-20T09:48:34Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "b8d515c6cd37866497306e49ee42ed4a178fae9a4df19fadbcc2cd5edf7bab70": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b8d648e301f09edaf7374d11e25aec9065e85548b96ff898159b61a403a2d991": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "b8db4ea8850863c69f2cba8872751065f7809125b28899b5729e869003ddf858": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "b918a372cdfa201bf92a8d264623fb95d9457af57d39804c3697007618792efb": {
      "attempt_finished_at": "2026-08-20T09:47:05Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b929d7e5ac6432ff78bc0972d53ae97a8de30adaeff43f68872b8ccec7cd1236": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "b9309d89448f018a608398e0fa7a598ef300813ea7712fdf14f225530c2246ea": {
      "attempt_finished_at": "2026-08-20T09:51:53Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "b9b13c484fa8a1ff78a495706a75e200e93993e3af67d8d6613726d71f02fd1d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "b9c5bfaffd2d090748dd73d7b6d5bb918cfc00bc8378caadb932592f0f4d3cb1": {
      "attempt_finished_at": "2026-08-20T09:52:09Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "b9e01e00ab4106636ffbdf63e93f4b92e8ec85413affceb0547572923f95d52b": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ba02e89cbdb13d08dda0be0dd9ce60e9cb289a9d634ecc9a6a733fc1e27be5dc": {
      "attempt_finished_at": "2026-08-20T09:48:21Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ba076035394922e3189ce9179e33be310581f086a6d826eea5331551665ddc6c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ba41a156a5c15cd3ff6b6e56b5b79f129cc563220a72644ec558e9d8c0edbfe3": {
      "attempt_finished_at": "2026-08-20T09:50:25Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ba4f4473f1f9d1331c5f34a7d8ccf93ca42d0e63bb5ab0ab0ec5d97941f9477f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ba9473c911f45158f0d678edb7b784a9730ceeaea8a4a803faa7219cba583a60": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "baaf0b7069a7660c671f2f25ae4b4f98e18f3921514c6b1942013883d43e109a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bad7605d7c6510c93cd585d67a7a889b5b0c10e162e3a624b71a8c7389e7269a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bb0b7a34d3168110a956e93d7fadef320b5583b7b00d12ea58facdecfc6466ee": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bb275345218ea049733751918d59a7fa67af7d114433b0f311614d20b8b1bdca": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bb4e4243852a78961a65321017acd41ccf3d772f06f84654a12324902ccd53b2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bb64a43139164c70406038af16b1d172ea07a394a8a77fa32ef68bd40877a838": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bb95d1c7c647a3d5a6e95be63d990399672a5eedd7db6870fe94a303ecd8511b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bc1cb93fb89a0be1ed92634765a031bd63e185bd95e17f47b1f033d73ee599a5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bc20c8bcd6e8841d14be48881e02c73b31733ba5db34039717f270d5aa8c0833": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bc487036f442f24eb2114c07a3c0e66aaed7f20ebf1fa0c434ab6d0e4a9ba5d4": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bcc13f73d3d441d64088cc5ed17a3470780ddf6da9b5de233ab845531fcf168f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bcc2bc369e44ffaa0b81fe592b4a279567b33918b234f61e21db6be6a8c47a63": {
      "attempt_finished_at": "2026-08-20T09:48:51Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "bcfcb3aa0fed137080134a96c449e66cc1c69ac8bbcacf95113244a0e6c8a281": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "bd0385683595ffe60d458f620119ad024fdb421210d065d64935d7eb60b3fa81": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "bd40242154860a9c58843c3c75f30cf965b567f42850e19f22c289c88bacbd1e": {
      "attempt_finished_at": "2026-08-20T09:50:06Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "bd4a8d6d6113fd4f04b8e8f8199a0e0830065ed71b755a196d6fff6576a08547": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bd62e4d2f2f20b5976b1774f404257e10971d5117ebb5ea0d54b7b8452284f18": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bd73892f615642da1e3d89d36b866d74feb79cdfdce4569f4084099fce38195a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bd84396508e2e47cf5a2eb6d416b98e961aa9691fabc20adf2b40527d7012f2c": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "bded25e74f5c1a5ee2badc8ee42a7e365eb991ad80eaa6ce4b504206cb774c3d": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "be13181178fb0d1bbf0807bca5edf261a7dda948735a25296dcd540c10395a03": {
      "attempt_finished_at": "2026-08-20T09:47:37Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "be3c9c49e9387a29e076fb3d9e991fa44844f05835f3ff6e1d2813a766b331e5": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "be871bf2131cf0d9cd007dc6bc13a960080c46b9e8f8432cabfd4bba6f34e70e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "be8ebe024278618c052a9a42abcb545c65627093af869e0101ed14f6c2457bb3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "be937232a8aeae89169145c7a0456585f7e5747b13560b1f0295065d195f4d4e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "be937b1cca4f60bbd3e432ccfad85dea5185e84e74dc9e8fd1dd213c354f6cba": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "be97441f5f7d61bc891e48e0c860b51902722eba60a185d4c3c865e2aa5d0916": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bead262d1c8c04b5841544adea045c1be5908148a9ed7debf8f50bc212826da9": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bec948bce8f0db23edf90226aa574ab03f9c8a1303f575b0952385724460ed59": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bf2b2b95cdcae0a38865df40f688dba706582cc0b06d374a09c615645bcd5092": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "bf4d30d2a220240eddd5da4cd25b10f85930a66654df430324daf5e86a40fb77": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bf4fdfbfbbd951784b9e6e414ccb08141756347b61993d7083cb3533513dc99a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bf501ea6240a2605e2f6b82b4b82115bd23057d2e2ad830babc72364f2b76ea6": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "bf50f048c4d6c6c0d338cd6cef35921d5c52f03467dedd58fc455a517aa54617": {
      "attempt_finished_at": "2026-08-20T09:47:36Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "bf8319cf17c836159eaba80b58c84ddd85a4aea258b240971efbd70f32ecc859": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "bf97e1ff5f8c0fe70047958f81167b86e8bc084f85787729a0b35fa03c278294": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bfe95844594ae9750ca195a77cae2bc1a66ebe58032718a2619981ce00955548": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "bfe95ebd8776fcb895734900346f8bb2b105bf15038d62baf0e63cf29da1e5ab": {
      "attempt_finished_at": "2026-08-20T08:57:58Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "bfff43e9a38b383062132cbc32394e485a469ad60dbe8cd6df290dc975e5a015": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c03c0d9d1a5d06bab08081f93eaf34252d24b6e7359cd85131a208d1f879bc29": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c099c0f4f2402ec2f60cd3cd87d7e1cf9176475485348045c9c98f0388512ada": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c0aa2494662a5df9d05dc3b249840a410c9fd4ce0ac30dd6718e779444f7f17b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c0fd9cab9d4db573069699c6ce4a87c1e8ccbea3ab492fbd3f01d845fb088389": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c16024d91c38477759c7d89d47b6476cfa8c90cd97571ade1c29f4dc6aaeb980": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c176a6f1064341aa0fb202d6d55aa725fc25b929244d12794a18939cea6e460e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "c17af7291dd8ff3806f80a3484407de405692c517a5e0ff71f2efaae8176f67b": {
      "attempt_finished_at": "2026-08-20T09:57:41Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "c193979e1007f08fd389b7c04f6d849d33561cc7e33c7cd7af8bdea4b72a0ca1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c1de466b0329f70cc82f5840fb47d6ac6ad309994b495d2f266c8265cc0d945e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c2156793d176d32372f25a034b149bd860c116d10bcaa99d01140fa95db0b151": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c225c453f909b608844abcb60af3658f5bb775a857509e00ee6e6035aaf0c598": {
      "attempt_finished_at": "2026-08-20T09:52:06Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "c26124d3a18a174c5189341e531173e38a7794198387520b9b6f4ad1d7fa4f40": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c29e67f909cbf439f69deffe826855e8807143fd3bc04ea89921ccaac595e630": {
      "attempt_finished_at": "2026-08-20T09:52:25Z",
      "model": "gemini-2.5-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "c2c8b3ae5ce093efe22599a0d3ba87633b7f3aa1cffcf361365eb7239952c417": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c2e5e61dd46d7ea51f05461e66dde811c88d67b43ad58c25f8b9e6cc97b1fcb3": {
      "attempt_finished_at": "2026-08-20T09:51:26Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "c2e881ed99b09126e2b5af52b818a0c6d3eec547d7b08eeeb53ed6979a6adfd6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c31c556d398e86095166d1a4a4ba6451976324149d448dc94879f8bd4819eeb0": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c32d9c78e538ffd63c520738d836a8d17cfc13e4fb09990afcea9c4ea8a4cd83": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c363eed57f2a357a4e8b513e552724e36f0d292e80a2739205993b1b44d53f62": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "c3f315a3cb8b8bc44b28c1a03785a04d79cf56ded803cc668db9a46f8d7f946a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c4073265335ed05059ced97f609d29259d5537e559295d46636cb4a089cbd00d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c4b4afdd8dd8e2149c7acccb43d9f227f14e7c3de5a9c40db6f85233db378610": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "c4ca9560ad31b0cb8fcb0421a6acfc1c418da7e5134193a392a33b42cf5cda64": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c4ccbc331427120b90f6876904ce32e9108453dffa48063661482105b3be48b7": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "c4fda5ef8b1397e5711e3f5378609a5e9a32922dc7d754c48eca0abd28cfb560": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c50ffd98cb51fbdd26b8e0ff42d4e9b347ef2a065038189e638e880a8e818559": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "c51a4eac519a9ea609410b8657f81c5c53c5a041dc96fffeaa3f2a128dba6dc5": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "c52c899319f0aebf1eaab697d187c243550ab6947e060e6deba98859f023624a": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "c5327e3b394bac11929df7febbbeda052e105fcd44d873ccf0d2b007e353ac0e": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "c53dbfdf2d3b0f95807e8d53e16b18fbec493ff9fffedd6115172a63b5e6ff60": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "c55b16d2e6bac3ce6aebc6a5270baf58629680f1143ad4ef69ce23818f43cc8c": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c58ca76539fe34d4cf53900c8a6b375da0f359b905501ef1e466b9cb7778c653": {
      "attempt_finished_at": "2026-08-20T09:57:54Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "c58f5a63ae574c90fdd0307a08f8ee0d57644da6208c6f4e04fbe7ea184c392a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c5c48f16e20e5b259bff9e592ef4d14b563d3e853bd87284f84c467890367486": {
      "attempt_finished_at": "2026-08-20T09:55:47Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "c5ea3e746cedc3481705f28cdfa4a0d4ffb4d89238496f27527636cdb5c73d9a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c5ebcf79bdbacdd0514529dff109f90b85bca7ddd22b60d44770d63d8bca4328": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c61c01d4f459cb472ffb22345a6428eeb4f111e086d807a321148d559122351a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c67e73a8bf7e0e0f93b8e025f59606335ac051ea2689bc26496045048ff1873b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c69196d218eaf3fc3ef60b1d5cb86b8da99d242c57d7dc443b3ed2351edbfd5f": {
      "attempt_finished_at": "2026-08-20T09:54:53Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "c6cc291a3832c56dc885cb9c5d4174d554480399f90a3970f36d54511db93d82": {
      "attempt_finished_at": "2026-08-20T09:49:19Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "c6e3c27751df50b7d37f001c3033d726be756d582c96907c5dc6f72f1206f97e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c759220f988b08a3c48e6056d0d584f85b578aec383602476795eceeaffbdb6d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c75d3c21cc12ac3b255dd72f4526aa20f8397ce07883b8271b9e9ee731cb60c9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c78957de939959b4006abc3bb577ae5d5923341b183b209330086bdbb0b80609": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c798b508a191334833626f46b4a94612b8c06fc7e7d8265e75044dca70dc8105": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c7a412f0bf486a241f5779b8256d16938b9c00572fbfe5472f3badb2396538bf": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c7ba54189cf1a2c6013d68eaddab89b9bc82d6a1d1c31a492641a88cbf01ac69": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c7d09ad951c0500b2b30efe4511040c942e11b7c8d862527f31a57b5c5b3d737": {
      "attempt_finished_at": "2026-08-20T09:51:22Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "c80ccf1f0e4a6147481b6be5b16355fe4f08e8f9ba013ada0ff1e1ecf2ffba9f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c846a62dcbabc4a294a83c461278353cffe964af3587405c345ed1f45f4bf8aa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c85741141135bee633e2dcbbd94fd13ca65ffa2b13d83870b0cbda186fc443ed": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "c883d3500ec8b88e3a2c8b42dff01ce15da7cd64ebf1c56f6a582349860174f7": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c89c1b5574cdc0f806757106846cc0737a88fc47a46ba21b02cd1c3832f530c0": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "c8afb992ac96b4a25695ccc7ac755d4bb4f2282abfb18ee4b0c48d34fba0e4c3": {
      "attempt_finished_at": "2026-08-20T09:56:05Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "c8c6701bc4a9efb20164f5010985cb5dc8bb9c3d387c80f18c70a678a765e670": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c91421309331aae955d00d015e2490088ded4434b625bef78e5cb94135dab80d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "c98f1616b2385e0ab7d1f1228124c2c1c3740778e8542bb9c131b05790b9a468": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ca0bc72ee8bfc29d7f8a71fc94d72be7c5942b72c6ec1f26837dc89ee7e39531": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ca251e087faa8cd7822aae9fbc97827a87e9c99409d97c46c98739b243ae0729": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ca3ada39ecb755c2f00f09fddcc4491b6b83458fa27e83666d508c338d5d6d5f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ca3ff42b51c64ef8a60cc7250c8d8585180598e0570df64123bf5aa9869812c6": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ca56598403cc6a6c002a4145a2796cb6cc4d8c73c9fd63d62059a8de17af5765": {
      "attempt_finished_at": "2026-08-20T09:51:38Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ca9d0e04b57d5a565877083d8344541ae7e7ceace129b6ee03eec0eb7555486a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "caab8c39d5a2fed70e0d0a1b8bb1f0611b0574925a3f66939596a287bcb3f8e1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cae18ebea76ba37562c9e45ba65cd14cf1778325c5cee6dd046abc4795af9b5a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "caf78a4162b1c2a2e718757a8e968f2f0badbf35fb0b07af49b5aff5abdd0e61": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cb1085b53197632a097e26bd355f02dac75ce3180a413f565a1e817b989e6b8b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cb1757dff1f6619fa63b61466c5062296a9e036d9c8823827b22b5cd0f9a5638": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cb3539df7b0dd632ddbc9a0e68be933b241d14a47251c81c82841ee37091d003": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cb56411bfacdeb80f0551013572126de2138894bcc2bb178c0aeb1cc92717a47": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cb63c0b1cc575ab57471cb96fbfac693ca7e01b17281102cf475420b11017f59": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cb8485e7c19cbe383714e5329fe8d51ffacab570b7e643dcf00f7f1cb172f633": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cb8cc33a0235f01e6d90eaafbc4842a1295cda8152c2bfb38d33071995df07e0": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cc02d9b5feda23f9a099b7835e46d9c0b7118198a7b1efa42a7b62c8fb73e540": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cc1bff4c3122319d50094783d80b54ce5265a32cef626f47fd36f6ee71ab49f3": {
      "attempt_finished_at": "2026-08-20T09:49:35Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "cc1e0e5bc80288d62cabe6c76724b04cd333fff27d2778727aa18b5e8283b536": {
      "attempt_finished_at": "2026-08-20T09:55:43Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "cc32a4676fbb1d10013132de1be0a6873b883d6bedb3b4b309a30ad7455f152a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cc33d7efd7bffa9c6ea8e97ac120e28ba8b01bcf2e8fa3cc72a8af24c18b2582": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "cc458b3f86b6abab5882025a7921961b1a5078bf729c562ce27c46d3d81572d8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cc46248a82f60ab0ddc875f4c26dcfe5417195c34449bcda909372b53b9ebc8a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cc6ff252531ed9c1eb3ca859e7fc825d388471560c07e3a13a40ee8c00810481": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cc8335ee3109307f38e6addf2de4c985de9266abec7440409f220c8ba8c4a202": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cc888a7a7a8b2bcf7b2e92b70a8cae7947a98bf43c211875b06a533aeba05ef4": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cc9623bde819148cd8805195c642296d1937e5991d1ab9c0992956b26f0689e2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cc9dd727557b2ff7b309d4b7ae87906f1da459016619daa8c997602a9c14e071": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "cca67c8d6a9124705c3152789b86b9a2562be9ceabebfb7569c765de36e66e5c": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "cd26225ba54c8490ca74cfe4a3e9e9d39fdb9af2553de04d60fe4389e484d4a5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cd271d6c165821d12906522c1d8638ee180a7b3d2b160f566062dd42f3aa5678": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cd54368a51e7060f67cfd3ae7ae754bccdc463f03591febc40821e425363d9e2": {
      "attempt_finished_at": "2026-08-20T09:47:04Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "cd739ee127d03876cdd040a6d2483301f8ed2b56b05b910c75e3d07fdd43886a": {
      "attempt_finished_at": "2026-08-20T09:50:35Z",
      "model": "gemini-2.5-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "cd7d22615780caa8a48cc58baa450a25603cb3c4657d9af51e1faaee6e303339": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cddc34bd0115e8223fbcdba2124e6a1b5ab8401fa60633e0d0ebb5118554aa5f": {
      "attempt_finished_at": "2026-08-20T09:49:11Z",
      "model": "gemini-3.6-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "cdf3382532c35be514853ef80e3083795989171c9af718668ecf0379f32499f3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cebb127af54bd74703336df06633eef0b06034560908b649c502991372af3af5": {
      "attempt_finished_at": "2026-08-20T09:49:45Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "cee953aba01b6d276bff231af4a491cc73f5561277a50e0b06083de6a4e18753": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cf1c2bef560dad7a2bac5b3ffba5f0d96ee9a5e643287b7f3dbdcbe73c39f824": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "cf2f262f092ca2a49fbc1fa9d9579dae01c79f19463b4b3af620de8f53ef3d88": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cf350b5c5424565f8727de7181bf4e761ce4a3032dd05a88140431df819eafcc": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cf4b20d0f788d47e63f0638e51e09186ae9de04cb8d45b6971c48f556543d735": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cf8aecad84f23e160ae08f048e1dc5c7c0a4dab6f4fd1f6545713f3dd71e6767": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cfcf52fed539c4bfb9e46cdd5469870a3c21e831c650c9a309c25435475ab39c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "cfe0d0269797c0a6bdc6ad219469fdba15d2a4a9fb00a085e5fe84c475c00993": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d029d23dd777ac59002c4d93f57e4792e245de3726a83cd176427f5ec03533ca": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d03700fb6e43ad91742613f248d7a91c85056e6c063e3eac7e133508acbec93a": {
      "attempt_finished_at": "2026-08-20T09:48:44Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "d04547a5c1ebb923d159eb74632fbad92fb75dac4efdd576bae06fa9bd58f16d": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "d045dc6eec0e7e669aa61f21acb027376b273de44ca5b849b7e5e51a1f08a8c9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d0ceac217220b24c5d7e9097aa111d7719b36b1d99e640598036af580a3c4124": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d0e61d339aebdfa02e6fec2c5413ce35937b91b50211dc6bc7fc4d9d6be19f74": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d0fc8f50084d61a32dde2f15a1893063c549bb0848471f8b9acc2b77a476d329": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d15a067dda9a1142445101a0df44c406b6a05017e11962f40475819244432a22": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d196176dbf68a3ed77096b7caad3547c121ccd64b8e6840fcba75cb7848d66ed": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d1a72734005331fbcb781a9b27849f7e22f78316b98239edfc747e46eb2f299a": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d1d6e4e071e3d10697263d6111501c4db5a908b0db69da043f4dc2f5c7bed7d9": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "d2430495d29ff017c16894749b494b2d991d1b0062ae9f943ca787dd39b89fd3": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d267c7cb39034f285035e34a03380fe8ba33800142bb64867cb2b4e88cb8b1af": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d26aaf615f10935c270b7da072a152ac02506d1cd3fad00c2bec7dd66cae860d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d27b938fca96c3054e5842b0d62116e48f1936a30fc7c2057aabdfcd44249e1a": {
      "attempt_finished_at": "2026-08-20T09:53:23Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "d2a4df5e80d47fc93a8c65c2cd4526f3954cc9a44b20c2c00e082d370c47942c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d2bf2db78ae97d8a3815259f1b63455ebe80e1dd76e0ebc4bf355a41182311aa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d2e5e05c8594d234aae5f476f43c614972f9e58f749935f408f57aa6787030af": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d2f8d32dd7927a460a9faaaa7fff02f050227cdaa09a5585c7ac79582b562579": {
      "attempt_finished_at": "2026-08-20T09:52:17Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "d33ec83db94ef3dbd4d28c20b46947274839370c6a0b44ab3d190d34a09ac634": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d3781ec0d800ab70f609fe8834de09166276e6acc12c1d204202738b36debfdd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d38cd5d92d2a656b847eee7fb5802729543e537411f3169d3b673764cc7a9129": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "d39989e429a64a69e2af70df3161ff172eceb6ceb72f2426823759798115c095": {
      "attempt_finished_at": "2026-08-20T09:57:03Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "d39cb8ae1757e208386b11e971d8a94ebddc73978b81ac7e8efeba9dcdbfe3ab": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d3d4b966444b670f9d7feb019d60ac841b6a34abaecb886ef1597f9eaf12a360": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d3e8443125f3cbd7c2ac4252e0efaf64b705ea00569696be46e4ee4673d894ad": {
      "attempt_finished_at": "2026-08-20T09:51:46Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "valid",
      "provider": "groq"
    },
    "d4105c96cb5d4c1154c53c0ccf9c2494ec3ee5ff9d44e8c0eaed206ea79e8fe2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d42513bffa4abfc0b69f251b12c481c1f7822f3c6363004de5ecf8517322a555": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d42528b5d69ea0152a6e06aa949f95107eb61cbed4830f21ea89ea2f99f28e7d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d4c6b2691da7a03105c3349c88d197476e2948590e7a2ee67bb38585dc0a2059": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d4db3b5c0addb45cfc0e31fed2e286cb3928e5be34047ca259016e215496c589": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d4ddfe8fd813d98486f3020641e1e8e62d1536c592f0ea3117e28398a56f43f3": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d5361b8ebb3e61505fa7284595cad5589e60674a41e955be364096a3fad8ca4a": {
      "attempt_finished_at": "2026-08-20T10:55:24Z",
      "model": "gemma-4-31B-it",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "d569074fbc9088d855f6ec7e9eddde56df00bda67cd0c576760e98c9c1d2ab2b": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d57dd8c33b2ad337ed5c22faf80baa9d3ec2fc80c9ab28002037d4f650fc2cdf": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d5bff66e4c80579af3ef534c23ef0178f494c409fe2ec080105121f0ad0e17dd": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d5d970956f5179a84768086634f044dec909758abe71e09bb5e15123839b46bb": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "d5ef3bfdb4609297b1bd65a3f1a44b68f18e9f6fbccffd66d9d01e3552b13761": {
      "attempt_finished_at": "2026-08-20T09:48:40Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "d63baf164864017a8b01c6d2812948224f08af62e431dbfc8d923bcab740759b": {
      "attempt_finished_at": "2026-08-20T08:58:08Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "d65024b29da48d07888b29403b7d5a804254740be756289e65723ff601463ff5": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "d65568e8fc04c1a2348d1a81f35653c3043416617ef6239f496cf50cbaceb9e5": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d65fee2d31253401fa929d4da40e6e129d381709bb6c021a46d87f97ed769aac": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d6c7ca478140702c32bbcd1eb453f6f3bbc4fd70eff9743acc26c4aea6ad8e0e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d6f79b372ff078fcd9b478d465dadc7164af3a96fe2c05647a87b6ac98d2c160": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d7200318355ae0874562155a8c21074c7b89be073716f351c290b6d8e6707ae7": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d727066d8527bfeaa9e1fdb0756850d9b86923c08061d4b3464f337733e123a3": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "d7652fe8dc0e9bc3e948a5a0a102641dc8efa3cd94de6de963a92fba24b285bf": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d7b6d0a73747cc897ba7fb49128e55d1420469b2efaed2e138025669e1896d7c": {
      "attempt_finished_at": "2026-08-20T09:51:34Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "d7d58ffeb57d9f11a813636de4fc0d7eb3a08b1fd36068c1d089e733d56c2a8d": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "d7e5487e1fcd0585cfeb92d0f2db2bce2e2fecfe2ba6155dcb8f120449265de1": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d7ede04c8ceacc5dee805056c8050e5934c19366dfcf4e7caaae909684d701a6": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "d8daf5436342c619f62cb21871814b39bee81a5d601cdba2b5b9e967b2f29805": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d8f7ecc8c453a233fb3c8679a84cc44d6fe8d1fc6093a073aa50079cfb407a42": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d92c4d1c918a125982268d196e45610bf63fdf7ede3e73f1831c42849e69fe26": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "d9335bd97d3a328fea1e5dfbeeb0d0ff2ab5b714bd1a677adc30d5a2b6396324": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d960d83f6045b4ec970707de20e83111dc4164773abcf77ce18eaa37bbf4a996": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d961e55d6a7e14e87eee079ce8925eee97a58593655ecbd52148189bba0f20dc": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d99d183b21e16e7d0a6bc5ff05d8fe26ae34ee298ff3e1e9e3c455bb896a3bf8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "d99d7d9fd78a2e01d6c85fda0c2f11c139a21cbd8b045d48038ebe686e559a2d": {
      "attempt_finished_at": "2026-08-20T09:51:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "d9d985332b4a1276dd4656126312520f095589c420e43e19480eff27ef759170": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "d9f41d957a3295b452d55abcc8db9b8d3f2c84eb503e362855c21a022a655550": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "da087c2badeee6b6c130156f9d2c8ae3fc2096827caa49cd2af9ae59cd158bd4": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "da0d74942bfcf9582392a89c99b8683286bea731b41644c4ab5e2d3c65052643": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "da3462b16f46a3745d3a3b4f46325854ebf8ef70036a6d7ed4c86fd6797c49ae": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "da3ef91bfdbb42a0d29e48532a3be5bed5a640deecaa56b92244247f2e99f20a": {
      "attempt_finished_at": "2026-08-20T09:48:09Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "da41d6f05e64ec3ba2f5c68623f7613f44373924d622f53ba6c01c0661c7bc91": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "da5eb21bd30bef8321411463d092b9b68d3d825372cafe51571a993ed45b6fac": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "da8243a47609c76569e7d82eeef8394e82595f567d2b56e356b28caab745030e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "da8bf26e79af3e094b6add98781199536dab0868038cbe245a2d28e69b3275a0": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "daa81b17910bd1c0b65ed8f1206045e6cb0590e72e3421b1deb6d5e685101e3d": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "dac9def62d1a396215ca0c4dd865fea4da8fc6aca920589e33ee8100068c26df": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "db0f9e9c3eb39eac5adfce5ac1df3eabdc797bf83e761f7b2785485cd4a1bb82": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "db18246a9ebd05054ba69697d0f15ae5ffc802c481073d2b3f846eb89f44c3cf": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "db47078037ae6d70a207ed4dbb616b8e460c42e8d19a4ffbc4dca665f06a1300": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "db4721b1769e487f2ccc529eba5991dd97f2e63174532dc3b4a5c1ac0801937a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "db4b0a0e5a65dd2a15e2dfc561fd48fa703b3d65399d24aed17489d507cb4b51": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "dbab54b0b61b2b528182c63b915d9189b237e0a9f012346d397905bc936e6644": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dbb908d85f2e9e6fce16afc70e8a97bb9d6c06537dccb15890d9f853ef44bd3b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "dbe217fef77026ef96890483c76c1ba781d9cf71de68ab3dbb77691d5f5b399d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dbf828f887bebf3af415b487a3093b7fe77f5d11e01a18778b288c87644ccafe": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dc020ecd28825821d8f94ec9a53d8cb2d6b86f554177eea56c44474d01df9221": {
      "attempt_finished_at": "2026-08-20T09:48:33Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "dc3a2544abc9978d29a0010e9980724f08e682cc639998fc2b7cb677adc5df2a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dc4af5e1942b1d9f129cf6f72e2e9ccc7f6e6363da33d356f5c84d181ca5d450": {
      "attempt_finished_at": "2026-08-20T09:57:45Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "dc5af8d9fb5e21657a6575bd809321e112bb123806002ff48bed131071c402a2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dca79034b765f4c3d6d443fe4ef2c036505dcace0e4460f980d9eed58ba8f5c5": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "dcdb0daf42806678e1807f6b55503f3aaceb0f3a5bf527902baf7e36bd3fb8eb": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "dcf457c32ff23c1c9041cdf9774ce3a730d631345e8947f6bc88e2f42ff3bb3b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "dd179ec66055c5e586ae60d2161482abbc0a316eff55f0be973943424c6a2fe3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "dd1f1eb1a81bb0605c1354495a75854060c650ade727a6ab32c9a369c49c0a2f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dd22e64fa612ccbe2012faf925dfd9434574fb227e0b0ec200f2f8e49f0c4c31": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "dd4070809bc20de6cf77aed2acdc158fe80e997cea8c2846b1f4a1155b70acf0": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "dd44d10792e33eccb4d6c57242ceae201493f813381d08e3f429aef40ba24eee": {
      "attempt_finished_at": "2026-08-20T09:51:41Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "dd55631d47e7262604eb10ab87b2da880c85e2be12473d602d959d679630a2fd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dd5d63b2925898ae0a4c9f2fed57a7d3670d8dd5cc5d1291bc472318c9217162": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "dd8329f18d0e12bdb4f33796da2e2779b14f084da6119837b6f4d3378013c946": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dda873fe3b4aee6b0eb3b9ade77ec1374cd8ba7e73f8cf3f670274d19cf46f50": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ddb913e78dd062db951f3987cad0da5882e42b2893023483027ffce9a242c35b": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "de0b4a5254d526aff46b68ea2f972f04e0c104628243c723a2257809eb1ec0a6": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "de887dba0ea22219cfe8212f952fa07b19670e332b1411e9efa806f492e7fd84": {
      "attempt_finished_at": "2026-08-20T09:52:42Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "dea66f8b3fa0343f1da55324b33879e3bc585da024b464e4253fdb90fcaa114f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "deb6d2095a5a8755bc3637c6a9f834f57a988dbb2c4d5ff99c6f8b8f74e1cfaa": {
      "attempt_finished_at": "2026-08-20T09:51:32Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "deb7af9a77ffbf030d0e7ab0ac213cd531f36c47db9c8f8cbb3a6eb4a6867bf6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "deea9f187c71bb379081735c30280c3ed90ab97a0690375e91ef8b48fd568437": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "df18581fa19b78957f90a030d1ae5f8356da659995c992b43abfb57838dfb0af": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "valid",
      "provider": "groq"
    },
    "df3f23b2533a1f698eb08d7b926295176e46007507db38c76da733991a0a7035": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "df4237faef1b57fdd7896e0cadd55cc84e63e6d3c9c85835466b9b9d5b3c42e2": {
      "attempt_finished_at": "2026-08-20T09:46:15Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "df52694ad4df60a136b979a2c6301bd10f2d9d4a332bf486eb925e186429b156": {
      "attempt_finished_at": "2026-08-20T10:55:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "df7aa020aa318babc48181abfc4a5631330924cb1369463180e1745fd6596358": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "df827038b597869f3d7265f852469119086226bd36b8608e7d8147a08b856bab": {
      "attempt_finished_at": "2026-08-20T09:52:09Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "df9a16f44112dd530d5ece56e5d6095bc418cad71ad87575789ebe6804781700": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dfa8de9024167753ccf300e08ddd67024ae4ef186de7f710fbec75ffd9d94bb3": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "dfc12c0d8db139a2c92fae99209fec984fc51d7f3622cc8dcb5194b249138c8f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "dfe48a3e3b8cab9fe26f3e68444668530202a0ee48bd95f56a9f3280ef60b415": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e0359d9245a9bd45cf5a0c0a21e17e7268775a505d0c551e92086d2d550e3f8b": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e05bdab99c3e7ee4cc8ff30e06f49018a39ca3cf9429df288ad63852516447a0": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e0927607f3e93ef6b62588dd2798026c4a2501a94d06bf4f79842bb79ec20c70": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e0a5d182d25b99b71e46e634c670c5972b53a223a873fbcfbbf025403d7cfe03": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e0b194f745b4c70bdcbff372f7ccf0f052eafe3d0a0d3015798364af8a8d1de6": {
      "attempt_finished_at": "2026-08-20T09:46:50Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "e0ed3981ce41057c507867d7e5aac41cef5f57256e876d8a5ba1ce1daf5d09ff": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e0ef01009dbd77d1824048b64ab43bbff80dd5606e736a7a9736898f8abe3b2d": {
      "attempt_finished_at": "2026-08-20T09:51:06Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "e10396fc64165aacca73cdf0019ce8e30af459787d595eebf208e6b248bc4806": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e122c9c82aa10a3ec7c6fbd18522dfeab42fd15ee1d77c707df6b336b5307214": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e19811835584e665f5539c96f110cad4e5304c387e61b8b0119fc9f82fb80d7c": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e1ab2b973a79139f6e0169c08042d996b3f23e58411e5043f7ecfe1dca774ec8": {
      "attempt_finished_at": "2026-08-20T09:48:44Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "e1ffa38512a4d1c1e383fe0ebf07fb7cde7bdebfe4bd34ac69e5a391afaf6681": {
      "attempt_finished_at": "2026-08-20T09:49:35Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "e2058003cd5bf909d73c50cfa46eaa77230272b7eddeb8b83e60f37ed5e3aed5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e2417f34cb3731e4d3263d4a98b9b0732487f034f0898745ad3bf5eed063b4a5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e2887bcd586c095fe8678a0cf5fda076f146c7fe8065628baec6744c8d9f438d": {
      "attempt_finished_at": "2026-08-20T09:51:35Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "e2c88e7efdc670cc9d41314c26917705fdfcdfe151a209920b85cf03d4513aba": {
      "attempt_finished_at": "2026-08-20T09:47:29Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "e2e34837ab0546a49aeadc089cf91a26319cbe117bf734f9e092fb5811f018ac": {
      "attempt_finished_at": "2026-08-20T09:50:20Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "e31c42233bb36c4f7a6c717e4ae039dda7957b34e6d6a9bdad3fc3801a11792c": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e32c1e14b0e5d1cdf0a724df3e77ff3af4942786c6cd5a3023c9b8b651a9a91a": {
      "attempt_finished_at": "2026-08-20T09:48:56Z",
      "model": "gemini-2.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "e364ff044d5c4caa8fdf40787c63ba4b40b76b75911dd7d5c2ad2b08c722c116": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e3a3519f227e5e4858e17f8ba1d1556b4a0cac560c8925a0804148cf64d2a2ff": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e3ac98a42275020140e5395ba7a0b6f9fe6c5107d0bbb058b734499d9b708823": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e3bd892fefb9cf0cd58ba622ed301c4b5b6252e103433d1626eb67589830f707": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e41cc5642e94f43fddfc2f71fdca2ac29e2be90659e2f08464b1c89c74d7890c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e4213d777c5582a584ac4e4d54ccd08b9c957432bc0ef08328a9fbe37459471a": {
      "attempt_finished_at": "2026-08-20T09:47:34Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "e445bea696e9892326b6f26fa9d4a3cf2c63949ab667420948014866c4d07659": {
      "attempt_finished_at": "2026-08-20T09:46:36Z",
      "model": "gemma-4-31B-it",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "e44fc4f83b9c1dd6db6998f9a0d47665bce8f981e520d31afb3ff94955369ba6": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e452da0d5c9a6fc8ab6b919507cb396ff103ac01d1668dae32141a91438ee06b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e46e114c8924965837020559dd7c9c97d89461c8f4c6d5bf516d680a7fbb4433": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e4852b3a0f394b4ed1adcb5e2e0e51ff173d666fcadad8e083ba02699e644890": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e4a383b96f58669d573a9c43c1738dd595328809f2130c93779e2e7067bb744e": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-nano-9b-v2:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e4b5488e846e29f1a6d6dc8ff82a2dda1ae5fc3d903033a3d45ed6c289ba1cc7": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e558f74c2d2ff69c3957f0b9b19070d4d93d8109988728fc50f7f6f5d533ab7e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e580de2fe693c770314885cf6167319c2741f31cc3405c288d0a6bcfd8da9592": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e592a9915968173d8d345c84406544cda04a1096f0ea78ebfb065e6509dce0e7": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e5d7e25cf4d8867b09a4a1fe3f9f9bd8a376f4a812b83c0109ebe7028e5d4d12": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e5fc7d4e08ce577fa2e48244119a8a9cc849424571644cb1a40b6aa1800f4eb4": {
      "attempt_finished_at": "2026-08-20T09:49:25Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "e64b6fc70b7ea508d9776e2e9d0cba34df1a6c868e4f3aa34a36aa0ee6f80546": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e665d00a94a81c6f6e72e1ef3f9f3afc4c41b1e1ace771ec60c36e1f0c83de52": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e66d28425ee71defcdb94db90d97845f0b6fea235be8cca91f36a41d2f06d13c": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e67cce0a34d1132f732a6d04a0c1264fd3a60ba232f605b6276949d379037308": {
      "attempt_finished_at": "2026-08-20T09:46:57Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "e68614518eb2b6fd01a73b620feb96d823abe14fe09ba3005be5d6477981b1dd": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e6f8a41ccab456bd4dab3d2c2e8f6a52bb0ea66bd8469af1e90dceb7f9961a54": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e701501b680e74a264ca8d557875906a8c1daefcb99c2de017b16b73a8a5b21e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e7105e937f1fc14871f3a4838410031162b1bda7714f1e4677983256fd836b43": {
      "attempt_finished_at": "2026-08-20T09:52:19Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "e73af9c8efb259ad8c770793cd1c52e988a3a8e5b59e21ee391bf821833706dd": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e73cd550d463bbd164a7df683f222c71a8fadda35b7669147149b55d0db57d7b": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e75e33164c88112c30c77172634c994dbb9b7fb9aa90c7654bc2c06301b2d4ef": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e78f05eb8b702fa2a31ee279ca829c342c199eee0431ad71be44a03f1a87b7d3": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e793a4a31bfd8467348566fc2b55a7799227c25db797d0a243bd3c41be508bfb": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e7996c809f530c79b6f1f8dcc5a6bfc9aa111ae9677e155c71518c0c17800676": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e7a17b7b27ed3499f71c77456ab50c6d59409d91d5fb80b5f2fc33ef2e0bbce0": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e7facef441c559c205f76a27978a5dfc3ddc4eb6cc3e30d2aa48cb03c395e4aa": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e83931381d5e3db77928352a7b6b354385854484156d1ceba16079391dde96d7": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e8676d4d16d8d3ce48d32b9fe2a0c4cbd3e0570e06a11b296918f38f215237ec": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e89b5dff9230008c55c8ded8d3e0d47e7bf6c573764b39f3790b84c218d3f9d9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e8ac4e3302c12339f88718a8f087ab98d0d3b9afe0b3f94cb56d670295d436aa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e8bd3837dacce20758c892e015afc314107ddc422b1d8c85eada84ba0312f903": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e8c906ae31190bc91b7a5dd88c90e5db87785b12d74839f5fceb60a72fd8b649": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "e8f9ebac9537b01e5f9ef7705bba7cfa5787e6914acd458ed07fb018a8e190f1": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-xs-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "e9203b655b079d40eb76ff127271e701b52be4b286ef92b96529d2d92723b1c6": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e932863b7d135095be00e8759d8641c4f8c6aa39d101ee9064fc4f0332283af8": {
      "attempt_finished_at": "2026-08-20T09:58:03Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "e939bc16cfbe266bb11adf9aca7a307dc4285968ee7fbbb8a7ed73a6960c6aad": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e93d8eb9820c280683b0b1d7f60014694c86c4af1df946e865dedffaeace58b3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "e95091b45a4fa40c4e886bbb59cca5fc51477396c88526c5b2ff7c0ef6a95803": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "e9efd57aef82a4d2ea409a129b4c8b8311db2da978aabec08573f9d9f977d1d2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ea011743a8282f94d04c46c777ed127d01bf42313259b0d28867f74c7b31fa75": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ea7043be33c980ba2c81dd1c27425ca99d1392acaf9ff89729cc8afe7b7eaad9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ea9e174c1de589983c13f378e7af4e7dc974dc77fdec5e69a87fdb4c1faaa3b6": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "eac08693663e5fb5d72e3bce78ace767f88cf15b3b70f2989d04c879e0849243": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "eaee20c71b09d4440612218069653b8a3ab5dc81233ffb14ee953dc02744f17f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "eb05f37b7db9371e8c2bf26f069428630e746072318c076b56c09c1e5f84ca88": {
      "attempt_finished_at": "2026-08-20T09:53:55Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "eb8471d4350739c8be3f1e1f64a05cc2d0a488bcb7c3994feb745aadfcea878e": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "eb84b60c5dbc12092253ba8cec82b9607c67568de730fa34af2ed5a8542de680": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ebd22a7135cfad69176df9396f6344f603631dbc0a53dd39378044e4ee8dcbae": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ec02e824899518b69ea48b04c472272e9fc44525dc22424bfe657a741aef824b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ec0c5cb711fea681916c5e9b53801823312a874cb6227ccb49e3e439a196a925": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ec166eb62c419ac8fc309b1e76fd039668a15a01cb4bfe613666b30afcf3d25c": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ec262984858e1457ad3c7cba1abf98b4667872f11207a92f19c16681309891a5": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ec3799059a28a2048a6b0b0e044bcb5887cecb47ed9df2f5d430b395137259e7": {
      "attempt_finished_at": "2026-08-20T09:49:16Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ec4c9438bc34713cb3d3638acf55c1ab19fd8a181e72b3bff98426c38c9c6cba": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ec629bb4bffdab81dce5a2b3f3303c6a64b1a4c75513ac96f29e630e245d048b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ec7e5697028f6e459fb1f6a5e76a3f72815936ae69154c73f4572557af6ca236": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ec8897c49f31869f1c5d417794df856c5f22db10322951d5f178c54da993051a": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "ec8bab878ead36e5c311703c6cb838b3ba122a801794a5d0caf19664bbb1eccc": {
      "attempt_finished_at": "2026-08-20T09:46:57Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ec90b171da7d1d23432d3e3b72303a2861cea7a07ae595744dc82061c336e0b5": {
      "attempt_finished_at": "2026-08-20T09:47:35Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ecb67be5ca23f349ece164463ca1d1f4b1a50d4c88f94133cdca3857254fb95a": {
      "attempt_finished_at": "2026-08-20T09:50:19Z",
      "model": "gemini-3.6-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "eceefe8fe99929d9927a1860815fea57319300999735166e72c75e5e00fa4f2a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ecf472d69da4427292f37850e57d56a5d83fa436688fe82d82977baef0bc95cb": {
      "attempt_finished_at": "2026-08-20T09:52:40Z",
      "model": "gemini-3.5-flash",
      "outcome": "provider_failure",
      "provider": "gemini"
    },
    "ed47dca70fe13866b0dcf732349d0de40c2ea7fef51a4d959dbf2faba0c9aab4": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ed85012392544db7c4c4d987ecd12dd7b76b1fb170c077da60d606e06efd0c12": {
      "attempt_finished_at": "2026-08-20T09:49:17Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "ed887a8945a139e3b28b6320f47911637081d453a55bfd6f8a88fcc6ec6ebb3b": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ed8c8211f932a9b11bb4959f8651b11f97b1f3bdc8178683a99165f36a62e393": {
      "attempt_finished_at": "2026-08-20T09:53:51Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "ed99a8d95b370a272c3863ef983e8e5df25f66424b84b468b09b2d58f89c2b5f": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "edb4ac8683ff500849f859851adf71d959b49eacfbb3f943e9de46bba4613539": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "edc921f50c311ced0d7e5c505666ea6e023ca7372d9888b36ebfe32427dc214b": {
      "attempt_finished_at": "2026-08-20T09:49:54Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "edd2aa16b1934d34c50babdabef06d6d56786513053fb4562e043f231a5bab54": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ede6d103359f4d36dbe7ac0cc6d6b066767e3e59c44f31ecdb65661b19498cea": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ede9a299322555f3e3a2deb656f82c7611c79c01ddb43f7281960aa7c1969589": {
      "attempt_finished_at": "2026-08-20T09:46:07Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "edfd1bee1621b1cad3b8732697ce6663cc787b61d8be938b164d52cf94b3f939": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ee17c96360c4893de85d60dcca81da681e46056eca6f564974f83ee630da59ae": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ee3c23df1bf5ee1d9b1401178084e027bf1a9db4174e821f6cfdf02601d35d6a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ee620f65ed8472248d299a4c81d3161360694f6e3b8add1be6e1643da73a7818": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ee82da8f444763ad70462e74115e435b57ec27114cc2063b0029b2d37077f901": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ee95b729017531d328fbfad4b4e3c489847894089c86af46a9d0b740ad9939fd": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ef3f705cfb56b332785411e5db98ab2623c7b7df950cf66dfcb8e7bd87282693": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ef41049c0b7d5a853f6f9229793fa61af2e3571ea32e586f1f9887f551834921": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "ef90f36bfcd28faab7f2983162aeb9aa4abc76ae6eb1d7ea1f9a69a1a8ddf65a": {
      "attempt_finished_at": "2026-08-20T09:57:17Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "ef9657bfcaba53314ed14a5ffb81cd67cf5a57ae020e9d19096f5e3719d459dd": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "efae1b88434f3bb2ae91d8ceb4cd24a408a42145b2bc7e86dfec891289c1e53b": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "google/gemma-4-31b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "effeb52dafde545cfabebad1266da44e0c1c248b370a520f61097531c73a28b5": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f005e989fe3e867c8b1dc22858b3ca416ec0eb124cd18201cd7de212815a29b9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f0532963e12a8f488a60da96a489bb70cbfbca2b7d35569dfcf5eeb5be7640aa": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f0846e0db1632c6d57b14998f6e72b6c88c3a48f18bf5590ccebf62f1d2b9c45": {
      "attempt_finished_at": "2026-08-20T09:46:42Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "f0cdecee345c3c61c222815e4f42679918ee21822c43efdc45caf07ec826a021": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f0e2000490df0f9a618717eb39742b6cffd31d66addeda93ef39fb962569bd31": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f11cdbd6cd6da88d7ddbafd55a5188ffa1d643cad8091288671a9eaeb3423442": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f131a0ec48e7ee79842b373c68bce7416056f3eb5d5eda000aa304cdd2b4ef80": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f1c35b0b29fa17610a785a959d281a6dd5b40a49a51ffca678a11d522cf1f423": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f1d07072d6e83f8f822a5791852788d20b39c364c1ad13c492fdee39ff2aeda8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f1d5df1133151f8658eb9471d82f334de4c8f4ee3b534902d96bd20923545381": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f204152e795d5816aae6b2d417a211ee17c70241591a9dbf76ffe1d8610df3c3": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f2668db9be0783c703d577adbdee24b5adc7c98b574e85d865e386a599956a8b": {
      "attempt_finished_at": "2026-08-20T09:49:52Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "valid",
      "provider": "groq"
    },
    "f2aa3fb4abfeca817077f7962b7f251c874415745ceeb434e7853b7d6d335bbe": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f2d38985928504e58be4ce1ce74517c015124b5850dcd4f9c1a44a043cbc4e9a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f2d43131b5b0e237e7bc57d737b5bfe3f4c320ee697f89874815bb908c6c7a7d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f3098c60a9bbd7b5eb34895282b45be4883a2a4f7ba27613a52863199b0c5df7": {
      "attempt_finished_at": "2026-08-20T09:47:33Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "f32eeb37dda8b6a3626a1e4155aa71d976e1e4a25363433a557b8b646a2c76ed": {
      "attempt_finished_at": "2026-08-20T09:47:56Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "f34ab96852d020c93a1a2403515f00ce5ec5ef83553c23b6e2362826ac32156f": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f39f879b897daf6e12fdbcaa12b8d5e29d581d20b1a4ba5dab65ed81737c362e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f3cbeaba9f6d09ab20f1639ac6449d62a294d7a984c17d25d17db20467f1abb2": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f409f405c05f324f3a92b3e5cb07526ea597aef1105f8cbf6e09bd2805d3b994": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f412a124e886f68a7bec6c9ba06c98af8733d54ee6fd6237b2d48e7a044f73df": {
      "attempt_finished_at": "2026-08-20T10:15:03Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "f417d0d1c21211bf3bcb0db42399763c344406293555d26b013f2999e44c17aa": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f4272cad79e7720eb382b2b7ab52f940424130e11bc6facb8a4d08bfebec70eb": {
      "attempt_finished_at": "2026-08-20T09:51:54Z",
      "model": "gemini-2.5-flash",
      "outcome": "validator_rejected",
      "provider": "gemini"
    },
    "f4648ffa5dde428c19789b3cd2ff91f8cc9ba8a7c61e085bcfef4b65de1f69ae": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f46c4ef7b882c8d4cebe0a8f33de0d8646deb22c20e17d14814d7d15c9b611db": {
      "attempt_finished_at": "2026-08-20T09:54:00Z",
      "model": "MiniMax-M2.7",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "f490e174103f9f7d4297ae6b014f5a91b557c597741a526af1f705046a3bb2e5": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f497525bb6099d2a7d33bcbc4af8a0db71fe776eff55ee106ed3a4d0d2ca754d": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f4d1baf795f285e6d2a68abfc4d36f4af8452eb55a9af40a4bc1667cde526830": {
      "attempt_finished_at": "2026-08-20T09:58:10Z",
      "model": "gemma-4-31B-it",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f4e33ff438c5e9fd67db4f624a299ef2c4ea16b0f4088d4dafba4f238e43b97d": {
      "attempt_finished_at": "2026-08-20T09:48:33Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "valid",
      "provider": "gemini"
    },
    "f4ffa474bd636ea439380e8c30b02680b608c3ba1bcc057f18c1f7ba4e08c04b": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f53803d9e1c0e7b31b509dad3beacd9793d9599f0a28f75c67c5af5c4d502469": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f540181da7373e58b90c4ace6a00b212db326dd7757ef1369d416fe8822ee7fa": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f55b49ede58a3164269f32ff8632c95b7eccdc898e6cbf85a9e23aa5a8124ed6": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f58d6a249677284f2f40b9060aec3b66bf47300dabd17577184df19a1db52139": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f644d0160c8e2b3856514697a088a397617eebff808858aebc2466936a526bd4": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "f6690e24a236a032286cce04b40d4f6a635055e2104fa46104e7d889b90949f1": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "openai/gpt-oss-20b:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "f676fc03ffa365848b3ad390f1695550634d3c1f56cf83a94f3cb37d638c8d57": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f67b28e406c920471d01bafcc263a1b60ff3a86f0cffc063e5bd0eef6143af0f": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f68460d954ed328f175bc7cf931582dd2e26ecb667b8add326013fdfeac0f265": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f68ecad48f2593ae5d89dca9555ce50ddf77f1caf4e29f388592d73d3a9c084a": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f693fcc0079bd19193a4cf679687a7434cfb1fbf19f6d6a5925862a35851d355": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f6ac93c8836e12affa1c99a6f6e0ba7740263791ad561d7ab26f63e48ffdafd6": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f6bdfb25f40b22aaa32984fe7e9ec6ed4e2a5e79aae8383630accec993de0899": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f6dac16e541783f25f0019b24dca96b668dcb082780a2a9744f6082ad627ca3e": {
      "attempt_finished_at": "2026-08-20T10:15:28Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "f6df1d94046c2c41c9dc7426a5bb9c4007731e32697d8c598f9f67aca1900d1d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f6fca0181bcd986e8f3bb31a452cc5488d1d2d55d5caf27fd6748d9b3672c53f": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f7056bc3698e3f80ccef13c631ef6e589a2dd08e78345341b4b27d11c6c543f0": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f739cad50871e9aefd755d04003da30e7cdbf3077317625b4dd5be441a9a1351": {
      "attempt_finished_at": "2026-08-20T09:47:41Z",
      "model": "MiniMax-M2.7",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "f7440a89ae313fed67488879cd78ae1758ca565141d381f20076605341302c52": {
      "attempt_finished_at": "2026-08-20T09:50:21Z",
      "model": "gemma-4-31B-it",
      "outcome": "valid",
      "provider": "sambanova"
    },
    "f787a194c9817e15ca6486a303093c969374567e13527520e4f2b372b73d6cfc": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f7af21d9ae085089b872acfba0a7bb493fde7f20f39140716429f0232696dc14": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-20b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f7f682ff775ab83975ff1cdee6113f256f173bfb4309eae1a1390a421aa2db24": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "f80cbdae8105a8fa526bb9bf9181a4560e72ee95a9ba0c9ef4d163895a77f341": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f8125ba73ef39abc7da8cdf0269ff9999159be5ac0c8f8b07fe311c892919cd8": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f812b7e67c9611ebc340c3b1242339f769fa5905a956481b363ff98a89256f74": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f8178a2675020b38f50e39e7ee17b0fd7c7fabd4fcddcc6fd4791664f4be7795": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f81bd3306cf562f465d220a9829eabb3b7b4ed445fe49d90382066af1184d99e": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f827892b5a28b86be7c12730cae9e91d16b73a68ce9ca788f2495471080140af": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f83ebdca1988610dc6d799650d16e28cfcf5ee20aa7dab3a4986c001c3942c9a": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f85592bb2210f7edb3f4be9f28f751af3a73832609655babf27860cb8ae9a5a9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f8790c23d47fca4f6e28885ee18f150acd307632d63febe1bab1198bbba12d22": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f8a0dad25d179b96a658539aa1177b6a6b928db302cb79889dc969a7f6f38f5c": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f8b302634e65bdc45efb36e6dad96c5e6183a319e60ed2cf07241a33bfb4a235": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f8d3bd8554cae6511554dfa8bb41b44180b2f15ac6836fc5efb8a1423fff2f84": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f8eeb58ae24f86dae32be37f4de483b9a7d6a178b6c3f9a0085c44388a03c19a": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f9038594623920e0b4587ccb3139c49446c38a9732cd152dd924d642bb7ed2a9": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f92a5208bfaa1154b9309521a0aeec7e92fb16485a12d10b8dbc93b816c8e658": {
      "attempt_finished_at": "2026-08-20T09:49:39Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "f92f0a0988d98f0dd8a59cdab17b2fec7ee6a4fc91112013d0d49b505f7b607d": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f9309baeea2e563073adc7c0c503c366f9471716eb117e265299ed99614fab2d": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "f94091cb2e71cea825ceb5331d3fc378284c664f690249fbb632588dc03f6eeb": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f981a1c3241d83101804e918dd05d48b616d8b326aedd336fd7c63346b423291": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "f988439b424c25d6a8a485201e49cf9a203652ab82e2f66aaba95014a6b3d447": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "f9a6dc047cbd551bdf2768b4db5da5bdf7ea40e77b1659ddbae8c9bc6f44fa3d": {
      "attempt_finished_at": "2026-08-20T09:49:53Z",
      "model": "gemini-3-flash-preview",
      "outcome": "valid",
      "provider": "gemini"
    },
    "f9e25c6b92db8b1558477286c0d81ee55d79120a1804b1e83412444de0c8ed16": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fa36c25148147c1f312693332e7d485c963c757e18bb219c5c9dfbe63438a452": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fa6d844d62b1da2df0b6a67ad147f8dc31c68f18cb5085e63058e9c3aaad950e": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fae4ea7bee805e6cf8125de6e6236734ca5e266798b196332957c87fcc4b8c1e": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fb3ec71367e7849044c121f7241e7e117453b7b6998f2a0e4b8e7f2a893239e4": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "google/gemma-4-26b-a4b-it:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "fb81c56eeabade405db513ebbf851ce073ba655108b63d6b884dcf028474db8b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fbafc38ac069f5d5a2d88ce4a130be4a7340df55f52b6a640f0f9f77553855ab": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fbebbb9ca623d4c635eb4d8b6e4cdf045912ec24d318938d41a6c6cb6b44bff2": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fc3c1a114937316f77afc171d81a5e0c12c15bcf856f29504e054967e1d2fcfe": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fc3fabcd1d032609d6c4269a6d0cc070271a90bef563084dbbaa0eadc09efde7": {
      "attempt_finished_at": "2026-08-20T09:46:11Z",
      "model": "poolside/laguna-s-2.1:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "fc5b55f679c47159e539230d8829decf6d9a2bb4872041f04153949bb15ec118": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fc8d9950f9689411b8c9e5fec22be17cc123b473d54a1416e46457f456bf6b55": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "DeepSeek-V3.1",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fc92faabef02ba133490542e0c473fa6c4da35686c48c396dc75fa6bb0b1b183": {
      "attempt_finished_at": "2026-08-20T09:46:59Z",
      "model": "gemini-3.5-flash",
      "outcome": "valid",
      "provider": "gemini"
    },
    "fcdbf8c2e80808e4d64052cc0e4e25582bab6235aa6f3e463919fcfb3461af68": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fcdcf40cdc3aee11fd4d500f355fbd45aa556c3b46d418345f1b06fa370a8af2": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fce45239aa355681dbbfad85750923f8f15adc7b4d63a5c1b3c55df7349df687": {
      "attempt_finished_at": "2026-08-20T09:46:10Z",
      "model": "DeepSeek-V3.2",
      "outcome": "provider_failure",
      "provider": "sambanova"
    },
    "fce7adb12934f67fecc3d4045ae4f138417e9ae4e2038a844f7b744f041b7e07": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fcee8e5eb894571a1642fbbcbf1ae1cc4dd3ab3920ea4f318504c7ddba6812e9": {
      "attempt_finished_at": "2026-08-20T10:14:48Z",
      "model": "MiniMax-M2.7",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fd336648f60e00090c883e3031b3c4fbfe0f07c8aa3477db95b2d519e4208f13": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fd37f936f3f6fee5fd4990f987e3faa0ce88e3d465274722a0f27bd0d0ff1c0c": {
      "attempt_finished_at": "2026-08-20T10:55:33Z",
      "model": "nvidia/nemotron-3.5-lightning:free",
      "outcome": "not_called",
      "provider": "openrouter"
    },
    "fd5f76e39dc48450da0156c6ee9d44ce5513dfb9f37d33af4533549cb0d0f124": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fdab426c062b67e8e23a08b9e8476aff63418cda6de30ba29bbf852b18725e6b": {
      "attempt_finished_at": "2026-08-20T09:46:46Z",
      "model": "gemini-3.7-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fdb51bf6e1e3fffd787083d4bd8561e3366cecbcdebd9b7fa09099232a6e8e17": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "openai/gpt-oss-120b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fdb57aaff4e2bebd7a70ac63883b3a40b0faacbfd80e9d5c79157679a53927a9": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fde1a3ac2167269a38a5ac730bb73af0aba5426bf716cbebed6711c9d61a2ffb": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fe0bfd2003aebb2bf20ff5c15570264856a3e36de905025125a08a42002d5fd1": {
      "attempt_finished_at": "2026-08-20T09:52:58Z",
      "model": "qwen/qwen3.6-27b",
      "outcome": "not_called",
      "provider": "groq"
    },
    "fe1024345aabd8455d6b962dd2cec03db982985cf222c0cd7f3f5ce50c601688": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.6-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fe102ff1b37be4f8e5f7eb6071d25c504cb1b0f2908dae557888ecf34092dfe7": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fe32ad6613a8aee8800ac3dea059519059986ef7f75daed09ee1fbf916f3b117": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-2.5-flash",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fe3a7aaba61fcb615c1fab6a896b015a1639947be121b696b8a5660a5fd11303": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fe482940b60b6faf4bb4091dd0f6818caf3bfce93ed5fcc18d31c01485489ac3": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3-flash-preview",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "fe701702baa105be980741124d427790430fd5e93148bdf407d5801a64cccd34": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "gpt-oss-120b",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fe7fe61a17ccdf100c057f7ca03fa8635de5f47875ea30349d704bb5a91f22ee": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "fe9b45cf9c5fc2c5add556e47f55df8285d3587b08755707c318f1c6b2a407be": {
      "attempt_finished_at": "2026-08-20T09:52:43Z",
      "model": "gemini-3.5-flash-lite",
      "outcome": "not_called",
      "provider": "gemini"
    },
    "ff160d7c9a18afab8df143b283a5144b3decc23d735d01a5daa42b6246926624": {
      "attempt_finished_at": "2026-08-20T11:15:23Z",
      "model": "Meta-Llama-3.3-70B-Instruct",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ff5cc4e2c388a101c32b1139e24e626407bb2a2d2481720308c52cf61077022b": {
      "attempt_finished_at": "2026-08-20T09:46:12Z",
      "model": "DeepSeek-V3.2",
      "outcome": "not_called",
      "provider": "sambanova"
    },
    "ffe33f250150b864cf80edf50e144e5284d3a4ff45a3d2c0f4a1485cc0703c6a": {
      "attempt_finished_at": "2026-08-20T10:15:18Z",
      "model": "gemma-4-31B-it",
      "outcome": "validator_rejected",
      "provider": "sambanova"
    },
    "ffe713895d1a30f808daf77cdbcd9a6c1ffed1beadd8c468e0fd4f2fa27c346a": {
      "attempt_finished_at": "2026-08-20T09:50:26Z",
      "model": "gemini-3.1-flash-lite",
      "outcome": "validator_rejected",
      "provider": "gemini"
    }
  }
}
-->

---

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →
