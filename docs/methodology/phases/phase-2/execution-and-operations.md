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

Default provider:

```text
groq
```

Default models:

```text
llama-3.3-70b-versatile
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

Common Groq example:

```bash
python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider groq \
  --model llama-3.3-70b-versatile \
  --mode generate
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
  --provider groq \
  --selection rotate \
  --rotation-seed hourly \
  --max-runs 1 \
  --mode dry-run \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --allow-rejected-check-outputs
```

## Automated resolver commands

Manual dry-run for one issue:

```bash
python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --issue 6 \
  --provider gemini \
  --model gemini-3.5-flash \
  --dry-run
```

Manual real run for one issue:

```bash
python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --issue 6 \
  --provider gemini \
  --model gemini-3.5-flash
```

Manual real run for the oldest eligible issue:

```bash
python scripts/phase-2/resolve_signal_issue.py \
  --repo pedropaulofb/ontouml-according-to-the-machines \
  --provider gemini \
  --model gemini-3.5-flash
```

The resolver must be run from a clean repository checkout with GitHub CLI authentication and the relevant provider API key.

The immediate fallback from `gemini-3.5-flash` to `gemini-2.5-flash` is implemented by the GitHub Actions workflow. A local command-line run of `resolve_signal_issue.py` does not automatically select a fallback model unless the operator reproduces the workflow logic manually.

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
| `--provider` | Select `groq` or `gemini`; default `gemini`. |
| `--model` | Select the provider model; default `gemini-3.5-flash`. |
| `--max-completion-tokens` | Completion-token cap; default `8000`. |
| `--provider-max-attempts` | Maximum provider-call attempts per resolver run; default `1`. |
| `--dry-run` | Generate and validate a plan without modifying files or writing to GitHub. |
| `--branch-prefix` | Branch prefix for accepted-change PRs; default `phase-2/auto-resolve`. |

The workflow input `fallback_model` belongs to `.github/workflows/phase-2-signal-resolver.yml`; it is not a `resolve_signal_issue.py` argument.

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
- `groq`, `gemini`, `cerebras`, `sambanova`, or `openrouter` provider selection;
- comma-separated `models`;
- comma- or newline-separated `provider_model_specs`;
- comma- or newline-separated page lists;
- explicit `rotation_index`;
- explicit `max_completion_tokens`.

When `provider_model_specs` is supplied, it overrides the `provider` and `models` inputs.

Scheduled provider/model rotation:

```text
0 groq:llama-3.3-70b-versatile
1 cerebras:gpt-oss-120b
2 sambanova:DeepSeek-V3.1
3 openrouter:nvidia/nemotron-3-ultra-550b-a55b:free
4 gemini:gemini-3.1-flash-lite
5 cerebras:zai-glm-4.7
6 sambanova:Meta-Llama-3.3-70B-Instruct
7 openrouter:poolside/laguna-m.1:free
```

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
agents: page-hygiene-checker,language-style-checker
provider/model rotation: groq:llama-3.3-70b-versatile, cerebras:gpt-oss-120b, sambanova:DeepSeek-V3.1, openrouter:nvidia/nemotron-3-ultra-550b-a55b:free, gemini:gemini-3.1-flash-lite, cerebras:zai-glm-4.7, sambanova:Meta-Llama-3.3-70B-Instruct, openrouter:poolside/laguna-m.1:free
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
provider: gemini
model: gemini-3.5-flash
fallback_model: gemini-2.5-flash
provider_max_attempts: 1
issue: oldest eligible open page-hygiene-checker or language-style-checker signal issue
dry_run: false
```

Manual dispatch can:

- resolve one explicit issue;
- select `gemini` or `groq`;
- select a provider model;
- select a fallback Gemini model;
- run in dry-run mode.

The scheduled resolver workflow first tries the selected provider/model once. With the default scheduled configuration, this means one `gemini-3.5-flash` attempt. If that attempt fails with provider-unavailability or 503-like diagnostics, the workflow immediately tries `gemini-2.5-flash` once for the same issue. It does not wait and retry the same model. It does not suppress non-provider-unavailability failures. It does not suppress fallback failures.

The resolver writes plan artifacts under:

```text
.tmp/phase-2/resolver
```

and uploads them as:

```text
phase-2-resolver-plan
```

## Free-model and slow-automation strategy

Phase 2 is designed to work within free or low-cost model quotas.

The intended strategy is:

- keep prompts compact;
- cap outputs to a small number of signals;
- run one selected combination per scheduled interval;
- use lightweight models;
- distribute scheduled signal generation across multiple free or low-cost providers;
- use deterministic Python whenever possible;
- spread execution over time;
- avoid heavyweight models in Phase 2;
- rely on gradual accumulation rather than large one-shot reviews;
- resolve only one eligible signal issue per automated resolver run.

This supports a slow continuous process: small page/agent/provider/model batches can run over time, allowing the project to accumulate and resolve signals incrementally.

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

Required repository secrets:

```text
GROQ_API_KEY
GEMINI_API_KEY
CEREBRAS_API_KEY
SAMBANOVA_API_KEY
OPENROUTER_API_KEY
```

Required workflow permissions:

```yaml
permissions:
  contents: read
  issues: write
```

The workflow uploads `.tmp/phase-2` as an artifact even if the check-agent run fails or produces rejected outputs.

### Automated resolver workflow

The automated resolver workflow may create commits, push branches, open pull requests, enable auto-merge, comment on issues, and close issues.

Required repository secrets:

```text
GROQ_API_KEY
GEMINI_API_KEY
```

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

Earlier operational notes reported that recent Phase 2 Gemini testing showed:

- earlier successful GitHub Actions execution for `gemini-2.5-flash`; the current scheduled signal-generation workflow selects `gemini-3.1-flash-lite`;
- valid generated issue-comment structure after adding reduced-thinking configuration;
- transient Gemini provider failures with `503 UNAVAILABLE`;
- validation rejections caused by overly long `Location` fragments before the prompt target was tightened from 160 characters to 140 characters.

Later operational updates added:

- automated signal issue resolution on a reduced schedule of one attempt every four hours;
- `gemini-3.5-flash` as the primary automated Gemini resolver model;
- immediate one-shot fallback to `gemini-2.5-flash` only for provider-unavailability or 503-like primary Gemini resolver failures;
- explicit resolver execution notices identifying primary/fallback attempts, selected provider, model, issue target, and dry-run mode;
- accepted resolver edits converted into pull requests;
- issue comments and issue closure for accepted and rejected automated resolver outcomes;
- PR branch update by rebase before auto-merge enablement;
- squash auto-merge after required checks pass;
- structured resolver log entries in the `Generation and Review Log` table;
- deterministic page-structure validation of the `Generation and Review Log` table;
- scheduled signal-generation rotation across Groq, Cerebras, SambaNova, Gemini, and OpenRouter;
- workflow-level signal-collector failure classification that keeps nonactionable provider availability noise nonfatal while keeping quota, rate-limit, authentication, configuration, request-shape, and unknown provider failures actionable.

These observations are not guarantees of future provider behavior. The committed workflows and scripts should be treated as authoritative for current automation behavior.

---

← Previous: [Signals and Issues](signals-and-issues.md) | [Phase 2 index](index.md) | Next: [Prompts and Status](prompts-and-status.md) →
