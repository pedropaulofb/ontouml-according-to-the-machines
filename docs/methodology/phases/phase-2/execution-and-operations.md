# Phase 2 — Execution and Operations

← Previous: [Signals and Issues](signals-and-issues.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →

## Batch execution model

The active LLM batch runner is:

```text
scripts/phase-2/run_check_batch.py
```

A direct `run_check_batch.py` invocation iterates over:

```text
pages × check agents × models
```

for one selected provider.

Default active LLM check agents:

```text
page-hygiene-checker
language-style-checker
```

The direct batch runner does not provide a default provider or model. Current signal-generation runs must pass an explicit supported provider and at least one model, or use the canonical scheduled workflow `provider_model_specs` rotation:

```text
--provider <provider>
--model <model>
```

Default output root:

```text
.tmp/phase-2
```

Main modes:

| Mode | Behavior |
|---|---|
| `generate` | Calls the LLM runner, validates output, and writes local files only. |
| `dry-run` | Calls the LLM runner, validates output, then calls `issue_manager.py --dry-run` for valid outputs. |
| `post` | Calls the LLM runner, validates output, then creates/updates GitHub issues/comments for valid outputs. |

Important: `dry-run` still calls the LLM provider and still validates the generated report. It only dry-runs the issue-manager operation.

Common Cerebras signal-generation example:

```bash
export CEREBRAS_API_KEY="..."

python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider cerebras \
  --model gpt-oss-120b \
  --mode generate \
  --max-runs 1 \
  --max-completion-tokens 3000 \
  --allow-rejected-check-outputs
```

Common Gemini signal-generation example:

```bash
export GEMINI_API_KEY="..."

python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider gemini \
  --model gemini-3.1-flash-lite \
  --mode generate \
  --max-runs 1 \
  --max-completion-tokens 3000 \
  --allow-rejected-check-outputs
```

On Windows PowerShell:

```powershell
$env:GEMINI_API_KEY = "..."
```

Rotating local example:

```bash
python scripts/phase-2/run_check_batch.py \
  --pages-glob "docs/stereotypes/classes/*.md" \
  --pages-glob "docs/stereotypes/relations/*.md" \
  --exclude-pages-glob "docs/stereotypes/**/index.md" \
  --provider cerebras \
  --model gpt-oss-120b \
  --selection rotate \
  --rotation-seed hourly \
  --max-runs 1 \
  --mode dry-run \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --allow-rejected-check-outputs
```

## Automated resolver commands

The resolver supports Gemini, Groq, and Cerebras directly. The scheduled workflow uses Gemini as primary and Cerebras as a cross-provider fallback.

Manual Gemini dry-run for one issue:

```bash
export GEMINI_API_KEY="..."

python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --issue 6 \
  --provider gemini \
  --model gemini-3.5-flash \
  --max-completion-tokens 8000 \
  --dry-run
```

Manual Cerebras dry-run using the scheduled fallback configuration:

```bash
export CEREBRAS_API_KEY="..."

python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --issue 6 \
  --provider cerebras \
  --model gpt-oss-120b \
  --max-completion-tokens 6000 \
  --dry-run
```

Manual real Gemini run for one issue:

```bash
python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --issue 6 \
  --provider gemini \
  --model gemini-3.5-flash \
  --max-completion-tokens 8000
```

Manual real run for the oldest eligible issue:

```bash
python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --provider gemini \
  --model gemini-3.5-flash
```

The resolver must be run from a clean repository checkout with GitHub CLI authentication and the relevant provider API key.

The cross-provider fallback from `gemini-3.5-flash` to Cerebras `gpt-oss-120b` is implemented by the GitHub Actions workflow. A local command-line run of `resolve_signal_issue.py` does not automatically select a fallback provider unless the operator reproduces the workflow logic manually.

The script itself continues to implement the existing deterministic normalization and plan validation for whichever provider/model is selected directly.

## Operator option reference

This section documents implemented runner options that are useful for maintainers but are not all shown in the common-command examples.

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
| `--page` | Select one page. May be repeated. |
| `--pages-glob` | Select pages by repository-relative glob. May be repeated. |
| `--exclude-page` | Exclude one selected page. May be repeated. |
| `--exclude-pages-glob` | Exclude pages matching a repository-relative glob. May be repeated. |
| `--agent` | Select an LLM-based Phase 2 agent. May be repeated. |
| `--provider` | Select one provider for the batch. |
| `--model` | Select one provider-specific model. May be repeated. |
| `--mode` | Choose `generate`, `dry-run`, or `post`. |
| `--repo` | Required for `dry-run` and `post` modes. |
| `--post-empty` | Forward zero-signal comments to `issue_manager.py`; otherwise missing zero-signal issues are skipped. |
| `--output-root` | Set the root directory for generated comments. |
| `--summary` | Write the Markdown batch summary to a custom path. |
| `--sleep-seconds` | Sleep between individual LLM calls. |
| `--max-runs` | Limit the number of selected planned runs. |
| `--selection` | Use `first` or `rotate` selection. |
| `--rotation-seed` | Use `hourly` or `daily` time-based rotation when no explicit rotation index is supplied. |
| `--rotation-index` | Use an explicit non-negative rotation index for deterministic runs. |
| `--fail-fast` | Stop after the first fatal failed individual run. |
| `--plan-only` | Print and summarize planned runs without executing provider calls. |
| `--max-completion-tokens` | Forward a completion-token cap to `run_check_agent.py`. |
| `--allow-rejected-check-outputs` | Treat validation-rejected LLM outputs as nonfatal and preserve invalid artifacts. |
| `--allow-provider-failures` | Treat transient provider-side availability failures and empty responses as nonfatal; quota, rate-limit, authentication, configuration, request-shape, and unknown provider failures remain fatal. |

### `run_check_agent.py`

| Option | Purpose |
|---|---|
| `--agent` | Select `page-hygiene-checker` or `language-style-checker`. |
| `--page` | Select the repository-relative canonical stereotype page. |
| `--provider` | Select the LLM provider adapter. |
| `--model` | Select the provider-specific model name. |
| `--output` | Set the generated issue-comment output path. |
| `--prompt` | Override the configured prompt path. |
| `--prompt-id` | Override prompt metadata. |
| `--commit-sha` | Override the commit SHA metadata; otherwise `git rev-parse HEAD` is used. |
| `--review-date` | Override the review date in `YYYY-MM-DD` form. |
| `--max-completion-tokens` | Set the provider completion-token cap. |

### `issue_manager.py`

| Option | Purpose |
|---|---|
| `--comment` | Select the generated Markdown issue-comment file. |
| `--repo` | Select the GitHub repository in `owner/name` form. |
| `--label` | Apply one or more labels when creating a new issue. |
| `--dry-run` | Print the derived issue/comment action without calling GitHub. |
| `--post-empty` | Create or post even when `Signal count` is `0`; by default, zero-signal comments are posted only if the issue already exists. |

### `resolve_signal_issue.py`

| Option | Purpose |
|---|---|
| `--repo` | Required repository in `owner/name` form. |
| `--issue` | Issue number or issue URL. When omitted, the oldest eligible open issue is selected. |
| `--provider` | Select `groq`, `gemini`, or `cerebras`; default `gemini`. |
| `--model` | Select the provider model; default `gemini-3.5-flash`. The Cerebras resolver path supports only `gpt-oss-120b`. |
| `--max-completion-tokens` | Completion-token cap; default `8000`. The scheduled Cerebras fallback passes `6000`. |
| `--provider-max-attempts` | Maximum provider-call attempts per resolver run; default `1`. |
| `--dry-run` | Generate and validate a plan without modifying files or writing to GitHub. |
| `--branch-prefix` | Branch prefix for accepted-change PRs; default `phase-2/auto-resolve`. |

The workflow fallback provider/model is fixed to `cerebras:gpt-oss-120b`; there is no separate `fallback_model` dispatch input.

## Execution policy

### Page-structure execution

The deterministic `page-structure-checker` runs when canonical stereotype pages are modified.

This check remains CI-oriented and blocking:

- it runs on relevant pull requests;
- it runs on relevant pushes to `main`;
- it is manually triggerable;
- it uploads reports as artifacts;
- it fails when structural signals are reported;
- it does not create GitHub issues from CI.

### LLM check-agent execution

The two LLM-based check agents run periodically through the scheduled workflow:

```text
page-hygiene-checker
language-style-checker
```

The canonical scheduled workflow is:

```text
.github/workflows/check-agent-signal-collector.yml
```

Workflow display name:

```text
Scheduled check-agent signal collector
```

It runs on this schedule:

```text
7,27,47 * * * *
```

That means it is scheduled every 20 minutes, at minutes 7, 27, and 47 UTC.

The workflow is also manually triggerable through `workflow_dispatch`.

Manual dispatch supports:

- `generate`, `dry-run`, or `post` mode;
- supported provider-adapter selection; Groq remains selectable manually only when an explicit model is supplied;
- `first` or `rotate` selection;
- `hourly` or `daily` rotation seed;
- comma-separated check-agent slugs;
- comma-separated `models`;
- comma- or newline-separated `provider_model_specs`;
- comma- or newline-separated page lists;
- explicit `rotation_index`;
- explicit `max_runs`;
- explicit `sleep_seconds`;
- explicit `max_completion_tokens`;
- explicit `update_model_statistics` toggle.

When `provider_model_specs` is supplied, it overrides the `provider` and `models` inputs.

Scheduled provider/model rotation:

```text
0 cerebras:gpt-oss-120b
1 sambanova:DeepSeek-V3.1
2 openrouter:nvidia/nemotron-3-ultra-550b-a55b:free
3 gemini:gemini-3.1-flash-lite
4 cerebras:zai-glm-4.7
5 sambanova:Meta-Llama-3.3-70B-Instruct
6 openrouter:poolside/laguna-m.1:free
```

No Groq model is currently part of the active scheduled provider/model rotation. The removed `groq:llama-3.3-70b-versatile` slot is historical/inactive and was not replaced by another Groq model.

The scheduled workflow aligns provider/model rotation buckets with the cron offset.

The cron schedule is:

```text
7,27,47 * * * *
```

The provider/model rotation period is 20 minutes, and the workflow subtracts the 7-minute schedule offset before deriving the raw rotation index:

```text
rotation_period_seconds: 1200
rotation_schedule_offset_seconds: 420
rotation_index: (rotation_timestamp - rotation_schedule_offset_seconds) / rotation_period_seconds
```

This keeps the rotation buckets aligned to the scheduled start minutes `:07`, `:27`, and `:47`. Without the offset, a delayed run near `:20` or `:40` could cross into the next Unix-anchored 20-minute bucket and select the next provider/model slot.

The workflow emits provider/model rotation diagnostics:

```text
Rotation timestamp UTC
Raw provider/model rotation index
Provider/model rotation specs
Provider/model slot count
Provider/model slot index
Runner rotation index
Selected provider/model spec
```

Effective scheduled defaults:

```text
mode: post
selection: rotate
rotation_seed: hourly
max_runs: 1
sleep_seconds: 0
max_completion_tokens: 3000
update_model_statistics: true
agents: page-hygiene-checker,language-style-checker
provider/model rotation: cerebras:gpt-oss-120b, sambanova:DeepSeek-V3.1, openrouter:nvidia/nemotron-3-ultra-550b-a55b:free, gemini:gemini-3.1-flash-lite, cerebras:zai-glm-4.7, sambanova:Meta-Llama-3.3-70B-Instruct, openrouter:poolside/laguna-m.1:free
pages: all canonical class and relation stereotype pages, excluding index.md
```

The workflow first rotates over provider/model specs and selects exactly one provider/model slot, then delegates page/agent/model selection to `run_check_batch.py` with rotating selection.

The scheduled run therefore gradually rotates over page, agent, provider, and model combinations. It does not run the full matrix in one execution, and it does not switch to another provider/model slot if the selected provider/model fails.

If a selected LLM output fails validation:

- the generated invalid output is saved as `.invalid.md`;
- `issue_manager.py` is not called for that output;
- artifacts are still uploaded;
- the workflow remains nonfatal for that rejection because it passes `--allow-rejected-check-outputs`.

If a selected provider call fails:

- transient provider-side availability failures and empty responses are emitted as warnings and remain nonfatal when `--allow-provider-failures` is active;
- quota, rate-limit, authentication, configuration, request-shape, and unknown provider failures are emitted as errors and remain fatal;
- issue-manager failures remain fatal;
- this provider-failure classification is not provider/model fallback.

### Automated resolver execution

The automated resolver runs periodically through:

```text
.github/workflows/phase-2-signal-resolver.yml
```

Workflow display name:

```text
Automated signal resolver
```

It runs on this schedule:

```text
5 */4 * * *
```

That means it is scheduled once every four hours, at minute 5 UTC, for six scheduled attempts per UTC day.

The workflow is also manually triggerable through `workflow_dispatch`.

Effective scheduled defaults:

```text
primary provider: gemini
primary model: gemini-3.5-flash
primary max_completion_tokens: 8000
fallback provider: cerebras
fallback model: gpt-oss-120b
fallback max_completion_tokens: 6000
fallback reasoning_effort: low
provider_max_attempts per resolver call: 1
issue: oldest eligible open page-hygiene-checker or language-style-checker signal issue
dry_run: false
```

Manual dispatch can:

- resolve one explicit issue;
- select `gemini` or `groq` as the primary provider;
- select a primary provider model;
- run in dry-run mode.

The production workflow intentionally has no force-fallback dispatch input. Therefore, a manual workflow dry run reaches Cerebras only if the primary Gemini invocation genuinely fails with one of the recognized provider-unavailability diagnostics. Use the direct Cerebras CLI dry-run command above to validate the provider request deterministically. Validate the end-to-end workflow fallback when a genuine qualifying primary failure occurs, or in a temporary test workflow rather than weakening the production fallback trigger.

The scheduled resolver workflow first tries the selected primary provider/model once. With the default scheduled configuration, this means one Gemini `gemini-3.5-flash` call. The fallback is fixed to Cerebras `gpt-oss-120b`; it is not a manual model override.

If that call fails with provider-unavailability or 503-like diagnostics, the workflow invokes Cerebras `gpt-oss-120b` once for the same issue. The Cerebras call uses JSON-object response mode, low reasoning effort, and a 6,000-token completion cap. The resolver also sets the OpenAI-compatible client to `max_retries=0`, so the configured single provider attempt does not hide additional SDK transport retries.

The workflow does not suppress non-provider-unavailability primary failures. It does not suppress fallback failures. Invalid plans remain genuine resolver failures and do not trigger another provider.

The resolver writes artifacts under:

```text
.tmp/phase-2/resolver
```

and uploads them as:

```text
phase-2-resolver-plan
```

The primary provider-error artifact is preserved before the Cerebras fallback starts. The existing raw-response, parsed-plan, normalization, final-plan, and error artifacts remain available according to the resolver path taken.

## Free-model and slow-automation strategy

Phase 2 is designed to work within free or low-cost model quotas.

The intended strategy is:

- keep prompts compact;
- cap check-agent outputs to a small number of signals;
- run one selected signal-generation combination per scheduled interval;
- distribute scheduled signal generation across multiple free or low-cost providers;
- use deterministic Python whenever possible;
- spread execution over time;
- rely on gradual accumulation rather than large one-shot reviews;
- resolve only one eligible signal issue per automated resolver run;
- use a cross-provider fallback so temporary Gemini unavailability does not require a second Google model;
- use a 6,000-token completion cap for the Cerebras fallback;
- use low reasoning effort for `gpt-oss-120b`;
- preserve deterministic normalization and validation for every provider response;
- fail normally when the fallback provider or fallback plan is unsuccessful.

This supports a slow continuous process: small page/agent/provider/model batches can run over time, allowing the project to accumulate and resolve signals incrementally without weakening validation.

## GitHub Actions and branch protection policy

### Page-structure workflow

The page-structure GitHub Actions workflow is CI-only.

It should be used to block structural regressions, not to create issues.

Recommended branch-protection profile for `main`:

```text
Branch name pattern: main

[x] Require a pull request before merging
[x] Require status checks to pass before merging
    [x] Require branches to be up to date before merging
    [x] Check stereotype page structure
[x] Require conversation resolution before merging
[x] Require linear history
[ ] Require signed commits
[ ] Require deployments to succeed before merging
[ ] Lock branch
[x] Do not allow bypassing the above settings
[ ] Allow force pushes
[ ] Allow deletions
```

`Require linear history` is recommended if the repository intentionally avoids merge commits. The automated resolver uses squash auto-merge and updates branches by rebase, which is compatible with a linear-history policy.

### Scheduled check-agent workflow

The scheduled check-agent workflow creates or updates GitHub issues/comments in `post` mode.

Provider repository secrets used when the corresponding provider is selected:

```text
GROQ_API_KEY
GEMINI_API_KEY
CEREBRAS_API_KEY
SAMBANOVA_API_KEY
OPENROUTER_API_KEY
```

The active scheduled rotation currently uses `GEMINI_API_KEY`, `CEREBRAS_API_KEY`, `SAMBANOVA_API_KEY`, and `OPENROUTER_API_KEY`. `GROQ_API_KEY` is still relevant only if Groq is selected manually or reintroduced in a future rotation.

Branch-write repository secret required for scheduled runs and manual runs with `update_model_statistics: true`:

```text
PHASE2_AUTOMATION_TOKEN
```

Required workflow permissions:

```yaml
permissions:
  contents: read
  issues: write
```

The workflow uploads `.tmp/phase-2` as an artifact even if the check-agent run fails or produces rejected outputs.

The scheduled check-agent workflow also updates `docs/methodology/phases/phase-2/model-run-statistics.md` with cumulative provider/model execution counters. The counters are derived from `run_check_batch.py` check-status fields, not from LLM self-reporting. The update step requires `PHASE2_AUTOMATION_TOKEN`; the workflow validates that secret for scheduled runs and for manual dispatches with `update_model_statistics: true`, then pushes the statistics commit with an authenticated `x-access-token` remote. The workflow-level `contents` permission remains `read`; repository-file persistence depends on the automation token's branch-write access and workflow-level concurrency to reduce overlapping counter updates.

### Automated resolver workflow

The automated resolver workflow may create commits, push branches, open pull requests, enable auto-merge, comment on issues, and close issues.

Required repository secrets for the default scheduled path:

```text
GEMINI_API_KEY
CEREBRAS_API_KEY
PHASE2_AUTOMATION_TOKEN
```

`GROQ_API_KEY` is required only when Groq is selected manually as the primary resolver provider.

Required workflow permissions:

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

Required repository settings:

```text
Settings → Actions → General → Workflow permissions:
[x] Read and write permissions
[x] Allow GitHub Actions to create and approve pull requests
```

The resolver workflow checks out the repository and performs GitHub writes with `PHASE2_AUTOMATION_TOKEN` rather than the default `github.token`.

Required pull-request setting:

```text
Settings → General → Pull Requests:
[x] Allow auto-merge
```

Recommended merge methods:

```text
[x] Allow squash merging
```

If branch protection requires up-to-date branches, the resolver's `gh pr update-branch --rebase` step should keep resolver branches compatible when no conflicts exist.

## Operational observations

Observed Phase 2 provider behavior has included:

- successful GitHub Actions execution for multiple Gemini, Cerebras, SambaNova, and OpenRouter signal-generation models;
- valid generated issue-comment structure after adding reduced-thinking configuration;
- transient Gemini provider failures with `503 UNAVAILABLE`;
- validation rejections caused by overly long `Location` fragments before the prompt target was tightened from 160 characters to 140 characters;
- repeated primary `gemini-3.5-flash` resolver unavailability followed by structurally or semantically invalid `gemini-2.5-flash` fallback plans;
- fallback plans that used the group-level `reject_for_phase_2_automation` value as the top-level `overall_decision`;
- fallback plans that accepted `current_text` values occurring in more than one page location;
- safe deterministic rejection of those ambiguous edit targets before any page or GitHub mutation.

The current resolver design addresses those observed classes by:

- deriving the redundant top-level decision from group decisions;
- retaining the exact-one-match validator unchanged;
- replacing the same-provider Gemini fallback with a cross-provider Cerebras `gpt-oss-120b` fallback;
- using JSON-object response mode, low reasoning effort, and a 6,000-token completion cap for the Cerebras call;
- preserving provider and plan failures as artifacts;
- continuing to fail normally when the fallback provider or fallback plan is unsuccessful.

The cross-provider fallback directly addresses primary Gemini unavailability. The already-committed deterministic `overall_decision` normalization independently addresses top-level-decision drift. The fallback does not guarantee that a Cerebras plan will satisfy page-dependent constraints such as unique exact `current_text`; the deterministic validator remains authoritative for those cases.

These observations are not guarantees of future provider behavior. The committed workflows, scripts, prompts, tests, and generated artifacts should be treated as authoritative for current automation behavior.

---

← Previous: [Signals and Issues](signals-and-issues.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →
