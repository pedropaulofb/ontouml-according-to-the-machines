# Phase 2 — Execution and Operations

← Previous: [Signals and Issues](signals-and-issues.md) | [Phase 2 index](index.md) | Next: [Model Run Statistics](model-run-statistics.md) →

## Operational model

Phase 2 signal collection is a content-addressed queue, not a time-based provider rotation. The desired task identity includes the scoped page content, check agent, prompt and validator configuration, provider-model slot, and request configuration. An unrelated repository commit does not create new work.

The current desired universe is:

```text
39 canonical pages × 2 LLM check agents × 25 configured provider-model slots = 1,950 tasks
```

Each slot has 78 tasks. A valid zero-signal result and a valid result with signals both complete the task. Historical identities remain in task state as `obsolete` or `retired`, so `total_records` may exceed 1,950 while `desired_tasks` remains exactly 1,950.

The production path is:

```text
reconcile desired identities
→ recover expired leases from retained terminal events
→ reserve resolver-priority capacity
→ select eligible work by age and quota state
→ persist leases and provider plans
→ run isolated provider workers
→ aggregate validated terminal events
→ publish valid signals
→ persist task, quota, result, publication, and statistics state
```

The canonical workflows are:

```text
.github/workflows/check-agent-signal-collector.yml
.github/workflows/phase-2-signal-resolver.yml
```

## Prerequisites

Local validation needs Python 3 and the repository development dependencies. Real provider calls additionally need the selected provider secret. GitHub issue or resolver operations require authenticated `gh` access.

Production secrets:

| Secret | Use |
|---|---|
| `SAMBANOVA_API_KEY` | SambaNova signal tasks |
| `GROQ_API_KEY` | Groq signal tasks and resolver fallback |
| `GEMINI_API_KEY` | Gemini signal tasks and resolver primary |
| `OPENROUTER_API_KEY` | OpenRouter signal tasks |
| `PHASE2_AUTOMATION_TOKEN` | Lease/state commits, result publication, resolver branches, PRs, and issue updates |

No Cerebras secret is used by current Phase 2 automation.

Install dependencies and validate the persisted control state:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python scripts/phase-2/provider_model_registry.py validate
python scripts/phase-2/task_reconciler.py validate
python scripts/phase-2/quota_state.py validate
python scripts/phase-2/resolver_attempt_state.py validate
```

## Collector workflow modes

The signal collector runs every 20 minutes at `7,27,47 * * * *`. Scheduled executions always use production `post` behavior. Manual dispatch exposes five modes:

| Mode | Provider call | Production task mutation | Quota observations | GitHub issue write | Purpose |
|---|---:|---:|---:|---:|---|
| `plan` | No | No | No | No | Reconcile in memory and display eligible work plans. |
| `simulate` | No | No | No | No | Exercise the same scheduler selection path without leases or calls. |
| `generate` | Yes | No | Persisted by the production diagnostic workflow | No | Produce and validate real provider output. |
| `dry-run` | Yes | No | Persisted by the production diagnostic workflow | Issue-manager dry run only | Exercise a real call and intended issue action without issue or task-state mutation. |
| `post` | Yes | Yes | Yes | Yes | Queue-managed production execution. |

`dry-run` is not call-free: it consumes real provider quota. `generate` and `dry-run` require explicit pages, agents, provider, and models; they do not lease or complete production tasks and are never scheduled. Every real diagnostic still enforces the free-only policy. Out-of-band local or branch calls can make production counters stale if their quota events are not persisted.

There is no separate `shadow` workflow input. Use `plan` or `simulate` on a feature branch for a call-free shadow of current selection. A branch-local real call is a diagnostic and never production completion.

### Call-free planning examples

Plan all currently eligible work without writing state:

```bash
python scripts/phase-2/task_scheduler.py plan --repo-root . --reconcile --workflow-run-id local-plan
```

Plan one provider-model slot and one agent:

```bash
python scripts/phase-2/task_scheduler.py plan --repo-root . --reconcile --workflow-run-id local-plan --provider-model-spec groq:openai/gpt-oss-120b --agent page-hygiene-checker
```

Simulate the scheduler path without calls or state writes:

```bash
python scripts/phase-2/task_scheduler.py simulate --repo-root . --reconcile --workflow-run-id local-simulation
```

Manual GitHub Actions plan:

```bash
gh workflow run check-agent-signal-collector.yml --ref feat/phase-2-recalibration -f mode=plan -f max_tasks_per_provider=1 -f execution_budget_seconds=720
```

### Explicit diagnostic examples

`generate` performs a real call, validates the output, and does not invoke the issue manager:

```bash
python scripts/phase-2/run_check_batch.py --page docs/stereotypes/classes/event.md --agent page-hygiene-checker --provider groq --model openai/gpt-oss-120b --mode generate --selection first --max-runs 1 --allow-rejected-check-outputs --allow-provider-failures
```

`dry-run` performs a real call and asks the issue manager to print the intended action without writing to GitHub:

```bash
python scripts/phase-2/run_check_batch.py --page docs/stereotypes/classes/event.md --agent language-style-checker --provider gemini --model gemini-3.5-flash --mode dry-run --repo OWNER/REPOSITORY --selection first --max-runs 1 --allow-rejected-check-outputs --allow-provider-failures
```

For OpenRouter, the exact model must be registered and end in `:free`; live metadata must prove zero pricing before either diagnostic sends a completion request.

## Operator option reference

The common examples above are intentionally small. The following existing command-line options remain supported.

### `run_page_structure_batch.py`

| Option | Purpose |
|---|---|
| `--dry-run` | Print planned checker commands without generating output files or calling `issue_manager.py`. |
| `--post` | Post generated reports with `Signal count > 0` through `issue_manager.py`. |
| `--issue-dry-run` | With `--post`, call `issue_manager.py --dry-run` instead of creating GitHub issues or comments. |
| `--repo` | Select the GitHub repository used by `issue_manager.py`. |
| `--output-dir` | Set the output directory for generated page-structure reports. |
| `--label` | Pass one or more labels to `issue_manager.py` when creating issues. |
| `--max-signals` | Cap the number of structural signals reported per page. |
| `--only-page` | Process one repository-relative page path only. |
| `--continue-on-error` | Continue processing remaining pages after a checker or posting failure. |

### `run_check_batch.py`

| Option | Purpose |
|---|---|
| `--repo-root` | Select the repository root. |
| `--page`, `--pages-glob` | Select pages explicitly or by repository-relative glob; each may be repeated. |
| `--exclude-page`, `--exclude-pages-glob` | Exclude selected pages explicitly or by glob; each may be repeated. |
| `--agent` | Select an LLM-based Phase 2 agent; may be repeated. |
| `--provider`, `--model` | Select one supported provider and one or more registered models. |
| `--mode` | Choose diagnostic `generate`, `dry-run`, or `post` behavior. |
| `--repo` | Required for `dry-run` and `post`. |
| `--post-empty` | Forward zero-signal comments to `issue_manager.py`. |
| `--output-root`, `--summary` | Select generated-comment and batch-summary paths. |
| `--sleep-seconds`, `--max-runs` | Bound diagnostic sequencing and selected combinations. |
| `--selection`, `--rotation-seed`, `--rotation-index` | Retained diagnostic batch-selection controls; these are not the production queue scheduler. |
| `--fail-fast` | Stop after the first fatal individual run. |
| `--plan-only` | Print and summarize batch combinations without provider calls. |
| `--max-completion-tokens` | Forward a completion-token cap to `run_check_agent.py`; the cap must not exceed the registered slot limit. |
| `--allow-rejected-check-outputs` | Preserve validator-rejected outputs without making the diagnostic batch fatal. |
| `--allow-provider-failures` | Keep recognized transient provider availability failures nonfatal; actionable failures remain fatal. |
| `--quota-state` | Select the persisted best-known quota state used by the pre-call guard. |
| `--resolver-work-pending` | Withhold the shared Gemini and Groq resolver slots from signal diagnostics. |

### `run_check_agent.py`

| Option | Purpose |
|---|---|
| `--agent`, `--page` | Select one supported LLM agent and canonical page. |
| `--provider`, `--model` | Select one registered provider-model slot. |
| `--output` | Set the generated issue-comment path. |
| `--prompt`, `--prompt-id` | Override configured prompt content or metadata. |
| `--commit-sha`, `--review-date` | Override traceability metadata. |
| `--max-completion-tokens` | Set the requested completion cap within the registry limit. |

### `issue_manager.py`

| Option | Purpose |
|---|---|
| `--comment`, `--repo` | Select the validated comment and GitHub repository. |
| `--label` | Apply one or more labels when creating an issue. |
| `--dry-run` | Print the derived issue/comment action without calling GitHub. |
| `--post-empty` | Create or post a zero-signal comment even when no matching issue exists. |
| `--task-id` | Supply the content-addressed task identity required for LLM-agent comments. |

### `resolve_signal_issue.py`

| Option | Purpose |
|---|---|
| `--repo` | Select the required repository in `owner/name` form. |
| `--issue` | Select an issue number or URL; omission selects the oldest eligible open issue. |
| `--provider`, `--model` | Select direct Gemini or Groq execution; defaults are Gemini and `gemini-3.5-flash`. |
| `--max-completion-tokens` | Set the completion cap; default 8,000. The workflow fallback passes 6,000. |
| `--provider-max-attempts` | Bound provider-call attempts; default one. |
| `--dry-run` | Generate and validate a real plan without page or GitHub mutation. |
| `--branch-prefix` | Set the accepted-change branch prefix. |
| `--attempt-state` | Select persistent content-addressed resolver-attempt state. |
| `--preflight-only` | Report whether eligible resolver work should reserve a shared slot without a provider call. |

## Production scheduling

Use `post` through GitHub Actions. The workflow serializes operational-state writes, performs resolver preflight, reconciles the queue, persists leases through `state_writer.py`, starts one isolated worker per provider with assigned work, and aggregates result artifacts even when an individual worker fails.

The scheduler:

- selects the oldest eligible tasks rather than rotating by time;
- respects every shared and model-specific quota group;
- bounds provider work by the execution-time budget and optional per-provider task limit;
- reserves Gemini `gemini-3.5-flash` and Groq `openai/gpt-oss-120b` for eligible resolver work before signal tasks;
- never calls a slot blocked by policy or execution configuration;
- allows one controlled endpoint-availability recheck after cooldown;
- emits no provider call when no eligible task exists.

Provider workers revalidate the lease commit, task identity, and quota eligibility immediately before a call. They emit replayable terminal events instead of directly editing shared state. The aggregator is the only component that completes queue tasks, persists results, publishes issue comments, and refreshes statistics.

### Filtered production dispatch

Run at most one queued task per provider while retaining normal production semantics:

```bash
gh workflow run check-agent-signal-collector.yml --ref main -f mode=post -f max_tasks_per_provider=1 -f execution_budget_seconds=720
```

Restrict a production dispatch to one provider by supplying that provider's registered specs:

```bash
gh workflow run check-agent-signal-collector.yml --ref main -f mode=post -f provider_model_specs=groq:openai/gpt-oss-120b,groq:openai/gpt-oss-20b,groq:qwen/qwen3.6-27b -f max_tasks_per_provider=1 -f execution_budget_seconds=720
```

Run one exact current page-agent-provider-model task by combining all three queue filters and limiting the provider plan to one task:

```bash
gh workflow run check-agent-signal-collector.yml --ref main -f mode=post -f pages=docs/stereotypes/classes/event.md -f agents=page-hygiene-checker -f provider_model_specs=groq:openai/gpt-oss-120b -f max_tasks_per_provider=1 -f execution_budget_seconds=720
```

Filters reduce the current dispatch only; they do not remove desired tasks from persistent state.

## Quota behavior

`data/phase-2/quota-state.json` stores the best-known state for 29 shared and model-specific quota groups and 25 runtime slots. Managed signal and resolver calls emit idempotent quota events; the state writer replays those events against the latest branch after a push conflict.

Quota certainty must be read from each field's provenance:

- `provider-reported` comes from response metadata or headers;
- `locally-counted` is exact for persisted managed events but cannot see unrelated applications or lost out-of-band events;
- `configured` is an operational limit or initial state;
- `inferred` is derived from diagnostics;
- `unknown` is intentionally unknown;
- `estimated: true`, including `remaining_estimate`, is not provider-confirmed capacity.

The scheduler may call when best-known state says capacity remains, but provider quota failures are authoritative. A quota failure defers the task, updates the affected groups, sets `retry_not_before`, and stops only work sharing the exhausted capacity. It does not trigger immediate retry or a paid fallback.

Inspect a slot without a call:

```bash
python scripts/phase-2/quota_state.py eligibility --provider openrouter --model google/gemma-4-31b-it:free
```

## Result and publication semantics

Worker outcomes are `valid`, `validator_rejected`, `provider_failure`, or `not_called`.

- `valid` completes the task after deterministic validation, even when signal count is zero.
- `validator_rejected` schedules a later retry after the first unchanged rejection and blocks the unchanged identity after the second.
- `provider_failure` changes task and quota state according to the classified error.
- `not_called` proves zero provider attempts and may safely return a recovered lease to pending only after aggregation.

Publication is downstream from task completion. A valid result with signals can be completed even if its GitHub issue update must be retried. Durable results live under `data/phase-2/results`; publication state lives under `data/phase-2/publications`.

Retry publication without another LLM call:

```bash
python scripts/phase-2/aggregate_task_results.py retry-publication --repo-root . --repository OWNER/REPOSITORY
```

Replay retained worker artifacts without publishing while diagnosing:

```bash
python scripts/phase-2/aggregate_task_results.py aggregate --repo-root . --artifact-root PATH/TO/WORKER-ARTIFACTS --no-publish
```

That aggregate command mutates local task, quota, result, publication, and statistics files. Run it only on a recovery branch, inspect the diff, and commit the audited result. Production uses `state_writer.py` so the same idempotent mutation is reapplied to the latest remote branch after conflicts.

## Automated resolver

The resolver workflow runs at `5 */4 * * *` and selects the oldest eligible open `page-hygiene-checker` or `language-style-checker` signal issue unless a manual issue is supplied.

Production defaults:

| Role | Provider/model | Attempts | Completion cap |
|---|---|---:|---:|
| Primary | `gemini:gemini-3.5-flash` | 1 | 8,000 |
| Fallback | `groq:openai/gpt-oss-120b` | 1 | 6,000 |

Groq fallback runs only for a recognized primary Gemini provider-unavailability failure. An invalid plan, quota block, policy block, authentication/configuration error, or other failure does not trigger it. Primary and fallback calls use the shared quota state. Persisted content-addressed resolver attempts prevent an unchanged terminal attempt from being repeated.

Resolver dry-run still makes a real provider call, generates and validates a plan, and writes local artifacts, but it does not edit the page or write to GitHub:

```bash
python scripts/phase-2/resolve_signal_issue.py --repo OWNER/REPOSITORY --issue ISSUE_NUMBER --provider groq --model openai/gpt-oss-120b --max-completion-tokens 6000 --provider-max-attempts 1 --dry-run
```

Preflight checks whether eligible resolver work should reserve a shared slot and makes no provider call:

```bash
python scripts/phase-2/resolve_signal_issue.py --repo OWNER/REPOSITORY --preflight-only
```

The resolver's exact-replacement validation, deterministic demotion, PR, auto-merge, and issue-closing behavior remains documented in [Automated Resolver](automated-resolver.md).

## Manual recovery

Manual recovery must preserve evidence and be auditable through a commit or pull request. There is intentionally no general-purpose command that silently resets blocked tasks.

### Expired or ambiguous leases

Before releasing an expired lease, inspect downloaded worker artifacts for a matching terminal event:

1. replay a retained `valid`, `validator_rejected`, `provider_failure`, or `not_called` event through deterministic aggregation;
2. return a task to pending only when a validated `not_called` event or other durable evidence proves that no provider request was sent;
3. if no evidence establishes whether a request was sent, keep the task `blocked_ambiguous_attempt` to prevent duplicate quota use;
4. authorize a replacement call only by an explicit state change that records the evidence reviewed and acknowledges possible duplication.

Use a call-free scheduler plan with retained result artifacts to inspect recovery classification:

```bash
python scripts/phase-2/task_scheduler.py plan --repo-root . --reconcile --workflow-run-id recovery-review --result-events PATH/TO/RESULT-EVENTS
```

### Rejection block

`blocked_repeated_rejection` means two validator rejections occurred for the unchanged identity. Normally, fix the page, prompt, validator, model selection, or request configuration and run reconciliation; the old identity becomes obsolete and the new identity starts pending. If evidence proves that the block itself is erroneous and identity is unchanged, edit only that task's audited state on a recovery branch, reset it to `pending`, validate state, and commit the evidence-backed change.

### Policy or execution-configuration block

- For `blocked_provider_policy`, first revalidate that the exact route is free. A failed or inconclusive check cannot be overridden.
- For `blocked_execution_configuration`, first complete sanitized credential/account or deterministic request validation without recording secret values.
- If identity is unchanged after successful validation, the exact affected tasks may return to `pending` and the runtime slot may become `eligible`.
- If a corrected route or request setting changes identity, preserve the old task as `obsolete` and let reconciliation create a new pending identity.

An audited runtime slot-status correction belongs in `data/phase-2/quota-state.json`, not in the registry's initial/default execution status. Record the supporting diagnostic and observation time, update only the affected runtime slot and task records, validate both state files, and commit the recovery change. OpenRouter price metadata is fetched live before every request; there is no durable metadata cache to reset. A subsequent diagnostic refreshes it, and the slot must remain blocked if that live check is unsuccessful or inconclusive.

Validate every audited recovery before commit:

```bash
python scripts/phase-2/provider_model_registry.py validate && python scripts/phase-2/task_reconciler.py validate && python scripts/phase-2/quota_state.py validate && python scripts/phase-2/resolver_attempt_state.py validate
```

### Temporary unavailability

Do not clear cooldowns merely to increase throughput. After `retry_not_before`, the scheduler authorizes exactly one desired task as the slot recheck. The command below is available for an audited manual authorization when the task is known and the persisted slot is eligible for recheck:

```bash
python scripts/phase-2/quota_state.py authorize-recheck --provider PROVIDER --model MODEL --task-id TASK_ID
```

It returns `not-authorized` and a nonzero exit code when the invariant is not satisfied.

### Incorrect quota counters

Never reset a counter simply because the provider rejected a call. Correct only a demonstrably wrong local value, preserve the prior file in Git history, record the evidence and observation time, keep provenance honest, validate the file, and submit the smallest state-only commit. A provider-reported limit or quota error remains authoritative.

### Rebuild and rollback

`task_reconciler.py reconcile` deterministically rebuilds desired identities from the registry, canonical pages, agents, prompts, validators, and request configuration while preserving existing historical records. Result events are still required to reconstruct outcomes; do not delete task, result, publication, quota, or resolver-attempt state during recovery.

To stop calls during an incident, disable the collector and resolver schedules or the affected workflow. Preserve all operational state and artifacts. Rollback must not reactivate retired providers or a paid route.

## Model retirement and free-policy recovery

Retire a model through the registry and reconciliation, never by deleting its history. Removed desired tasks become retired; model-run statistics continue to show the slot as inactive/retired. Adding or changing a model creates new task identities. See [Provider Registry](providers.md) for the required sequence.

A runtime free-policy block is not retirement. The slot stays configured so its desired work remains visible, but no calls occur until explicit, successful free-policy revalidation. This distinction prevents a temporary pricing or metadata problem from silently erasing the review obligation.

## Phase 3 allocation extension point

Phase 3 is not implemented by this recalibration. Phase 2 currently receives 100% of approved free capacity. Provider adapters and task identities do not permanently own that capacity: tasks carry `phase: phase-2`, and shared quota policy can later introduce per-phase weights, maximum shares, or reserved minimums above the adapters.

A future Phase 3 queue may therefore reallocate shared quota priorities through configuration without changing Phase 2 page, agent, task-identity, validator, or provider-adapter behavior. This extension point does not authorize private Phase 3 inputs or paid capacity.

## Unchanged CI and repository policy

The deterministic `page-structure-checker` remains CI-oriented and blocking. It runs on relevant pull requests and pushes to `main`, is manually triggerable, uploads reports as artifacts, fails when structural signals are reported, and does not create GitHub issues from CI.

Recommended `main` branch protection remains:

```text
[x] Require a pull request before merging
[x] Require status checks to pass before merging
    [x] Require branches to be up to date before merging
    [x] Check stereotype page structure
[x] Require conversation resolution before merging
[x] Require linear history
[x] Do not allow bypassing the above settings
[ ] Allow force pushes
[ ] Allow deletions
```

The resolver requires repository Actions read/write permission, permission for Actions to create pull requests, auto-merge enabled, and squash merging available. Its `PHASE2_AUTOMATION_TOKEN` must be able to push branches, create and update pull requests, enable auto-merge, comment on issues, and close issues.

## Historical operational observations

Historical executions produced valid and invalid outputs across Gemini, SambaNova, OpenRouter, and the now-retired provider slots. Observed failure classes included Gemini `503 UNAVAILABLE`, overly long `Location` fragments, invalid redundant top-level resolver decisions, and ambiguous exact-replacement targets.

The current design addresses those observed classes through deterministic decision normalization, unchanged exact-one-match validation, Groq cross-provider fallback, content-addressed attempt state, and preserved error artifacts. These observations are historical evidence, not guarantees of future provider behavior; current registry, state, workflows, scripts, and generated artifacts remain authoritative.

## Standard validation

Run the deterministic state, test, compilation, hook, and whitespace checks before committing operational changes:

```bash
python scripts/phase-2/provider_model_registry.py validate && python scripts/phase-2/task_reconciler.py validate && python scripts/phase-2/quota_state.py validate && python scripts/phase-2/resolver_attempt_state.py validate && python scripts/phase-2/update_model_run_statistics.py --self-test && python -m unittest discover -s scripts/tests -p "test_*.py" && python -m py_compile scripts/phase-2/*.py scripts/phase-2/providers/*.py scripts/tests/test_phase2_*.py && pre-commit run --all-files && git diff --check
```

---

← Previous: [Signals and Issues](signals-and-issues.md) | [Phase 2 index](index.md) | Next: [Model Run Statistics](model-run-statistics.md) →
