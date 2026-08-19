# Phase 2 — Provider Registry

← Previous: [Automated Resolver](automated-resolver.md) | [Phase 2 index](index.md) | Next: [Signals and Issues](signals-and-issues.md) →

## Authority and scope

The only authoritative configured-slot list is:

```text
config/phase-2/provider-models.json
```

`scripts/phase-2/provider_model_registry.py` validates that file before provider execution. A slot is the exact combination of provider and model; the same underlying model exposed by two providers is two independent slots. The current registry has configuration version `phase-2-recalibration-v6`, 25 configured slots, and two explicitly retired Gemini slots retained for history.

The standard signal-generation entry points support four providers:

| Provider | Adapter | Required secret | Current configured slots |
|---|---|---|---:|
| `sambanova` | `scripts/phase-2/providers/sambanova.py` | `SAMBANOVA_API_KEY` | 6 |
| `groq` | `scripts/phase-2/providers/groq.py` | `GROQ_API_KEY` | 3 |
| `gemini` | `scripts/phase-2/providers/gemini.py` | `GEMINI_API_KEY` | 7 |
| `openrouter` | `scripts/phase-2/providers/openrouter.py` | `OPENROUTER_API_KEY` | 9 |

An unused provider file is not executable support. Cerebras is not registered by the runner, batch runner, scheduler, workflow dispatch, or resolver and has no required workflow secret. Historical Cerebras statistics remain visible only as inactive/retired records.

## Configured provider-model slots

Each slot below appears once in registry order. Lifecycle, reasoning, request settings, free-policy evidence, and quota-group membership are versioned in the registry.

| Slot | Provider | Exact model ID | Lifecycle | Free-policy basis |
|---:|---|---|---|---|
| 1 | `sambanova` | `MiniMax-M2.7` | production | confirmed free account |
| 2 | `sambanova` | `DeepSeek-V3.1` | production | confirmed free account |
| 3 | `sambanova` | `Meta-Llama-3.3-70B-Instruct` | production | confirmed free account |
| 4 | `sambanova` | `gpt-oss-120b` | production | confirmed free account |
| 5 | `sambanova` | `DeepSeek-V3.2` | preview | confirmed free account |
| 6 | `sambanova` | `gemma-4-31B-it` | preview | confirmed free account |
| 7 | `groq` | `openai/gpt-oss-120b` | production | confirmed free account |
| 8 | `groq` | `openai/gpt-oss-20b` | production | confirmed free account |
| 9 | `groq` | `qwen/qwen3.6-27b` | preview | confirmed free account |
| 10 | `gemini` | `gemini-3.6-flash` | stable | confirmed no-charge project |
| 11 | `gemini` | `gemini-3.5-flash` | stable | confirmed no-charge project |
| 12 | `gemini` | `gemini-3.5-flash-lite` | stable | confirmed no-charge project |
| 13 | `gemini` | `gemini-3.1-flash-lite` | stable | confirmed no-charge project |
| 14 | `gemini` | `gemini-3-flash-preview` | preview | confirmed no-charge project |
| 16 | `gemini` | `gemini-2.5-flash` | stable | confirmed no-charge project |
| 18 | `openrouter` | `nvidia/nemotron-3-ultra-550b-a55b:free` | free variant | live zero-price metadata required |
| 19 | `openrouter` | `nvidia/nemotron-3-super-120b-a12b:free` | free variant | live zero-price metadata required |
| 20 | `openrouter` | `google/gemma-4-26b-a4b-it:free` | free variant | live zero-price metadata required |
| 21 | `openrouter` | `google/gemma-4-31b-it:free` | free variant | live zero-price metadata required |
| 22 | `openrouter` | `poolside/laguna-s-2.1:free` | free variant | live zero-price metadata required |
| 23 | `openrouter` | `poolside/laguna-xs-2.1:free` | free variant | live zero-price metadata required |
| 25 | `openrouter` | `openai/gpt-oss-20b:free` | free variant | live zero-price metadata required |
| 26 | `openrouter` | `nvidia/nemotron-nano-9b-v2:free` | free variant | live zero-price metadata required |
| 27 | `gemini` | `gemini-3.7-flash` | stable | published free Standard tier and confirmed no-charge project |
| 28 | `openrouter` | `nvidia/nemotron-3.5-lightning:free` | free variant | live zero-price metadata required |

Slots 15 (`gemini-2.5-pro`) and 17 (`gemini-2.5-flash-lite`) are `retired`. Both exact endpoints returned provider model-unavailable responses during acceptance testing. Their task and statistics records remain historical; neither is executable. Google lists [`gemini-3.7-flash`](https://ai.google.dev/gemini-api/docs/models) as a current model and publishes free Standard-tier input and output in its [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), so slot 27 is its feasible free replacement. The provider-suggested `gemini-3.1-pro-preview` replacement is not configured because its Standard tier has no free input or output. `gemini-3.5-flash-lite`, already configured in slot 12, is the active Flash-Lite replacement.

Slot 24 (`inclusionai/ling-3.0-flash:free`) is also `retired`: acceptance diagnostics found that OpenRouter now exposes only its paid variant. Slot 28 (`nvidia/nemotron-3.5-lightning:free`) replaces it with an exact current `:free` endpoint.

Display or validate the executable list without making a provider call:

```bash
python scripts/phase-2/provider_model_registry.py validate
python scripts/phase-2/provider_model_registry.py list-specs
```

## Free-only policy

No Phase 2 path may make a paid LLM request. This includes scheduled, manual, local, branch, `generate`, `dry-run`, signal-generation, resolver-primary, and resolver-fallback calls.

- SambaNova uses the maintainer-confirmed free account. A billing, credit, or payment-required response blocks the affected capacity.
- Groq uses free-plan capacity and does not request a paid service tier.
- Gemini uses a no-charge API project and does not enable paid grounding, paid tools, or billing-backed fallback.
- OpenRouter requires the exact `:free` identifier. Before every call, including diagnostics, `free_policy.py` fetches current model metadata and fails closed unless prompt and completion prices, plus any present request and internal-reasoning prices, are zero. Provider fallbacks are disabled.

Billing or payment diagnostics become `blocked_provider_policy`. Authentication, authorization, and deterministic request-configuration failures become `blocked_execution_configuration`. Neither category receives automatic transient retries. A failed or inconclusive free-policy check never authorizes a call.

## Quota groups and certainty

Every slot belongs to both a shared provider/account/project group and a model-specific group. All required groups must be eligible before the scheduler leases a task. The current state is stored in:

```text
data/phase-2/quota-state.json
```

Quota state is the best-known operational belief, not a guarantee that the next call will succeed. Each observation records its source and whether it is estimated:

- provider response headers and provider usage metadata are observations from the provider;
- repository-managed request and token counters are exact for the events that were successfully persisted, but may omit out-of-band use;
- configured limits are known configuration, not proof of remaining capacity;
- `remaining_estimate` is explicitly estimated;
- `unknown` means the provider has not supplied enough information;
- a provider quota response such as `429` or `RESOURCE_EXHAUSTED` is authoritative and updates cooldown state.

OpenRouter's shared free-account remaining count is estimated from the configured daily allowance and locally persisted calls because ordinary responses do not reliably expose the remaining free count. The default is the conservative 50-request daily allowance unless the account's actual entitlement is deliberately configured.

Validate or inspect eligibility without a provider call:

```bash
python scripts/phase-2/quota_state.py validate
python scripts/phase-2/quota_state.py eligibility --provider groq --model openai/gpt-oss-120b
```

`eligibility` returns a nonzero exit code when the slot is not eligible.

## Adapter behavior

All adapters require the exact provider-model slot to be executable in the registry and reject completion caps above the registered value.

### Groq

`scripts/phase-2/providers/groq.py` uses the Groq chat-completions SDK and `GROQ_API_KEY`. Registry reasoning policy is converted to provider request arguments, response usage and rate-limit headers are recorded when available, and reasoning output is excluded where configured.

### Gemini

`scripts/phase-2/providers/gemini.py` uses the Google GenAI SDK and `client.models.generate_content(...)`. It reads `GOOGLE_API_KEY` or `GEMINI_API_KEY`; `GEMINI_API_KEY` is the canonical workflow secret. Thinking configuration is derived from the registered model family and reasoning policy, and thought parts are excluded from the final signal comment.

### SambaNova

`scripts/phase-2/providers/sambanova.py` uses the shared OpenAI-compatible utility, requires `SAMBANOVA_API_KEY`, and defaults to `https://api.sambanova.ai/v1`. `SAMBANOVA_BASE_URL` may override that endpoint in local or alternate environments. Provider-specific reasoning settings come from the registered slot.

### OpenRouter

`scripts/phase-2/providers/openrouter.py` uses the shared OpenAI-compatible utility, requires `OPENROUTER_API_KEY`, and calls `https://openrouter.ai/api/v1`. Before constructing the completion request, it applies the live free-price check described above. Registered request configuration disables fallbacks and excludes reasoning output where required. Slots 18 and 19 use a 512-token reasoning budget because effort-only controls still exhausted most of the 3000-token completion cap during diagnostic runs; both exact OpenRouter endpoints expose direct reasoning-token budgeting.

## Provider retry and failure classification

Signal-generation adapters make one initial request plus at most one retry after 15 seconds for a genuinely transient failure. Recognized transient diagnostics include timeouts, connection failures, overload/capacity messages, and HTTP 500, 502, 503, or 504 responses.

Quota, rate-limit, billing/policy, authentication, authorization, model-not-found, deterministic invalid-request, context-length, and validator failures do not receive this immediate transient retry. Provider retry never selects an alternate provider-model slot. The queue aggregator applies the resulting classified event to task and quota state.

Resolver calls are narrower: `resolve_signal_issue.py` and the workflow default to one provider attempt. The workflow may then make the single Groq fallback described below; invalid plans and nonavailability failures do not receive another provider call.

## Retry and slot lifecycle

Runtime availability is separate from permanent configuration:

- `eligible` slots may be scheduled when all quota groups permit it;
- `temporarily_unavailable` slots wait until `retry_not_before`, then authorize exactly one recheck task;
- `blocked_provider_policy` requires successful, explicit free-policy revalidation;
- `blocked_execution_configuration` requires sanitized diagnosis and successful credential/request validation;
- a configured slot retains its desired tasks while runtime-blocked;
- a slot becomes `retired` only through an explicit registry change, verified official removal, or an explicit maintainer decision.

Retirement preserves task and statistics history. If a request-configuration, prompt, page, agent, or model change alters task identity, reconciliation marks the old identity `obsolete` and creates a new pending identity. It must not manually recycle the old identity.

## Resolver providers

The scheduled resolver uses Gemini `gemini-3.5-flash` as primary and Groq `openai/gpt-oss-120b` as its one-shot fallback. Groq is attempted only after a recognized Gemini provider-unavailability failure and only when the same content-addressed resolver attempt remains eligible. Invalid Gemini plans and other failure classes do not trigger the fallback.

Resolver primary and fallback calls emit quota events into the same quota state used by signal scheduling. Eligible resolver work has priority on the two shared slots; when there is no eligible resolver work, their remaining free capacity is available to signal generation. Content-addressed resolver-attempt state prevents unchanged terminal attempts from being called repeatedly.

See [Automated Resolver](automated-resolver.md) for exact plan-validation, edit, PR, and issue behavior.

## Adding or retiring a slot

Provider changes are configuration changes, not ad hoc command-line substitutions:

1. update `config/phase-2/provider-models.json`, preserving deterministic slot order and incrementing the configuration or request-configuration version as appropriate;
2. for a removal, set `configuration_status` to `retired` or remove it only through the documented migration while preserving history;
3. validate the registry;
4. reconcile task state so unchanged desired identities are preserved, superseded identities become obsolete, retired identities become retired, and new identities start pending;
5. initialize or update quota-state records for new quota groups;
6. run the complete Phase 2 tests before production use.

```bash
python scripts/phase-2/provider_model_registry.py validate && python scripts/phase-2/task_reconciler.py reconcile && python scripts/phase-2/task_reconciler.py validate && python scripts/phase-2/quota_state.py validate
```

OpenRouter additions are not executable unless the exact live metadata proves the route is free at call time.

---

← Previous: [Automated Resolver](automated-resolver.md) | [Phase 2 index](index.md) | Next: [Signals and Issues](signals-and-issues.md) →
