# Phase 2 — Scope and Architecture

[Phase 2 index](index.md) | Next: [Check Agents](check-agents.md) →

## Documentation structure

This document is the canonical Phase 2 methodology overview page.

Provider support, check-agent execution, issue routing, and automated signal resolution are documented across the Phase 2 methodology pages linked from `index.md`.

## Purpose

Phase 2 has eight goals:

1. implement three lightweight check agents for canonical stereotype pages;
2. run the deterministic Python check agent on canonical stereotype page modifications;
3. run the two LLM-based check agents periodically through a quota-aware content-addressed queue;
4. produce structured, page-local signals about page structure, page hygiene, formatting, and writing quality;
5. route check-agent outputs to deterministic GitHub issues scoped by page and check agent;
6. support manual ChatGPT-assisted signal review and issue resolution for the two LLM-based check agents;
7. automate narrowly scoped resolution of eligible `page-hygiene-checker` and `language-style-checker` signal issues when exact deterministic local edits are accepted;
8. gate automated resolver edits through the deterministic page-structure checker and pull-request checks before merge.

Phase 2 prioritizes infrastructure, signal quality, traceability, repeatability, controlled issue routing, and low-risk deterministic edits over deep content judgment.

## Phase 2 boundary

Phase 2 implements:

```text
check agents
→ check-agent execution
→ output validation
→ page-plus-agent issue routing
→ manual signal-review support for LLM-based check agents
→ automated signal resolution for selected LLM-based check-agent signal issues
→ pull request creation
→ page-structure validation
→ squash auto-merge after required checks pass
```

Phase 2 does **not** implement unrestricted autonomous documentation rewriting.

### Check-agent boundary

Phase 2 check agents:

- inspect one canonical stereotype page at a time;
- produce lightweight page-local signals;
- may suggest an exact local repair or replacement when safe;
- must not modify canonical documentation pages;
- must not commit changes;
- must not open pull requests;
- must not decide that a signal is accepted or rejected;
- must not close issues;
- must not perform heavy semantic or source validation.

The check-agent layer is signal collection only.

For Phase 2, a check agent is a deterministic or LLM-based checker role, identified by a check-agent slug, that inspects one canonical stereotype page and emits structured candidate signals without modifying repository content or deciding signal outcomes.

### Issue-manager boundary

The issue manager:

- reads validated check-agent reports;
- derives the reviewed page identity;
- derives the check-agent identity;
- creates or reuses one open GitHub issue per page and check agent;
- posts model-specific check-agent reports as comments in that issue;
- updates a matching existing comment when the stable comment identity already exists.

The issue manager does not resolve signals. It only routes check-agent reports.

### Manual issue-review boundary

Manual signal-review and issue-resolution prompts:

- exist for `page-hygiene-checker` and `language-style-checker`;
- do not currently exist for `page-structure-checker`;
- are intended for use with ChatGPT by a human maintainer;
- help evaluate signals in one GitHub issue against the current reviewed page;
- classify signals as `accept`, `reject`, or `defer`;
- may prepare exact local edits, issue comments, branch names, commit messages, or pull-request material when safe and in scope;
- require explicit human confirmation before any GitHub write action;
- do not replace human judgment.

### Automated resolver boundary

The automated resolver:

- is not a check agent;
- is not part of signal collection;
- operates only on open GitHub issues whose titles match the Phase 2 signal issue pattern;
- supports only `page-hygiene-checker` and `language-style-checker` issues;
- uses an LLM only to produce a strict JSON resolution plan;
- validates the plan deterministically before applying anything;
- accepts only exact local replacements whose `current_text` occurs exactly once in the current reviewed page;
- treats former `defer` cases as `reject_for_phase_2_automation`;
- rejects source-dependent, conceptual, broad, unsafe, non-local, duplicate, obsolete, or insufficiently confident signals for Phase 2 automation;
- applies accepted edits locally;
- writes a structured `Generation and Review Log` table row for accepted automated edits;
- runs the deterministic page-structure checker before opening a pull request;
- creates a pull request for accepted edits;
- rebases the pull-request branch onto the latest `main`;
- enables squash auto-merge so GitHub merges the PR only after required checks pass;
- comments on and closes the source signal issue;
- closes no-accepted-change issues as `not_planned`.

The resolver does not verify original sources, compare pages, validate OntoUML semantics, or decide conceptual correctness.

## Current Phase 2 architecture

The Phase 2 architecture contains exactly three check agents and one automated resolver wrapper:

```text
phase-2
├── check-agents
│   ├── page-structure-checker
│   ├── page-hygiene-checker
│   └── language-style-checker
└── automated-signal-resolver
    ├── page-hygiene-checker issue resolver
    └── language-style-checker issue resolver
```

The implemented check-agent execution model is:

```text
page-structure-checker
└── deterministic Python
└── runs after canonical stereotype page modifications
└── blocks structural regressions in CI

page-hygiene-checker
└── LLM-based
└── runs through the check-agent-aware LLM runner
└── runs periodically through the quota-aware scheduled workflow
└── reports page-hygiene signals

language-style-checker
└── LLM-based
└── runs through the check-agent-aware LLM runner
└── runs periodically through the quota-aware scheduled workflow
└── reports language/style signals
```

The implemented issue-routing model is:

```text
one GitHub issue per page + check agent
```

Different providers and models executed by the same check agent for the same page post comments in the same issue.

Actual issue title pattern:

```text
Check signal: <agent-slug>: <page-id>
```

Examples:

```text
Check signal: page-structure-checker: classes/event
Check signal: page-hygiene-checker: classes/event
Check signal: language-style-checker: classes/event
Check signal: page-structure-checker: relations/material
```

If `page-hygiene-checker` runs with multiple provider/model combinations on `classes/event`, all those outputs belong in:

```text
Check signal: page-hygiene-checker: classes/event
```

## Current implementation status

The current implementation includes check execution, output validation, page-plus-agent issue routing, duplicate-control for comments, content-addressed quota-aware collection through SambaNova, Groq, Gemini, and OpenRouter, archived manual signal-review prompts for the two LLM-based check agents, automated signal-resolution prompts for those check agents, deterministic patch application, PR creation, branch update by rebase, squash auto-merge enablement, issue closure, and a one-shot Gemini `gemini-3.6-flash` fallback for recognized primary Gemini resolver unavailability.

Signal collection reconciles 39 canonical pages × 2 LLM check agents × 25 configured provider-model slots into 1,950 desired tasks. The global repository SHA is traceability metadata rather than completion identity, so unrelated commits do not repeat completed work.

There is no current dedicated manual or automated closure prompt for `page-structure-checker`; page-structure issues remain subject to direct maintainer review and normal PR review.

### Implemented files and artifacts

```text
.github/workflows/page-structure-check.yml
.github/workflows/check-agent-signal-collector.yml
.github/workflows/phase-2-signal-resolver.yml
requirements.txt
prompts/phase-2/check-signal-shared-contract-v1.0.0.md
prompts/phase-2/page-hygiene-checker-v1.1.0.md
prompts/phase-2/language-style-checker-v1.1.0.md
archive/phase-2/manual-closure-prompts/close-page-hygiene-signal-issue-v1.0.0.md
archive/phase-2/manual-closure-prompts/close-language-style-signal-issue-v1.0.0.md
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.2.md
prompts/phase-2/resolve-language-style-signal-issue-v1.2.2.md
scripts/phase-2/run_check_agent.py
scripts/phase-2/run_check_batch.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_page_structure_batch.py
scripts/phase-2/resolve_signal_issue.py
scripts/phase-2/provider_model_registry.py
scripts/phase-2/task_identity.py
scripts/phase-2/task_state.py
scripts/phase-2/task_reconciler.py
scripts/phase-2/quota_state.py
scripts/phase-2/task_scheduler.py
scripts/phase-2/provider_worker.py
scripts/phase-2/aggregate_task_results.py
scripts/phase-2/state_writer.py
scripts/phase-2/free_policy.py
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/openai_compatible.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/gemini.py
scripts/phase-2/providers/sambanova.py
scripts/phase-2/providers/openrouter.py
config/phase-2/provider-models.json
data/phase-2/task-state.json
data/phase-2/quota-state.json
data/phase-2/resolver-attempt-state.json
```

Non-canonical or legacy-support artifacts may also exist:

```text
.github/workflows/phase-2-check-agents.yml.bak
scripts/phase-2/providers/mock.py
```

These are not the canonical scheduled Phase 2 LLM execution path. The `.bak` workflow reflects older single-provider assumptions and should not be used as operational documentation. The canonical shared LLM workflow is:

```text
.github/workflows/check-agent-signal-collector.yml
```

The repository ignores `scripts/local/`. Any machine-local dispatcher or helper under that path is outside canonical repository infrastructure unless it is intentionally committed and documented as reusable tooling.

### Current capabilities

The current implementation can:

- run the deterministic `page-structure-checker`;
- validate the `Generation and Review Log` table structure in canonical stereotype pages;
- run one LLM check-agent invocation through `run_check_agent.py`;
- compose `page-hygiene-checker` from the shared signal contract and `prompts/phase-2/page-hygiene-checker-v1.1.0.md`;
- compose `language-style-checker` from the shared signal contract and `prompts/phase-2/language-style-checker-v1.1.0.md`;
- call Groq models through `scripts/phase-2/providers/groq.py`;
- call Gemini models through `scripts/phase-2/providers/gemini.py`;
- call SambaNova models through `scripts/phase-2/providers/sambanova.py`;
- call registered OpenRouter `:free` models only after live zero-price metadata validation;
- validate generated LLM signal comments against agent-specific contracts;
- write valid generated comments to `.tmp/phase-2/`;
- write invalid generated comments to `.invalid.md` files for debugging;
- run page × check agent × provider × model collection through the scheduled workflow;
- run page × check agent × model batches for one selected provider through `run_check_batch.py`;
- reconcile and schedule the 1,950-task content-addressed queue by eligibility, age, provider capacity, and quota state;
- isolate provider workers and aggregate replayable terminal events into durable operational state;
- run the collector in `plan`, `simulate`, `generate`, `dry-run`, or `post` mode;
- write per-run logs and a batch summary under `.tmp/phase-2/`;
- derive deterministic page-plus-agent issue titles;
- create or reuse open GitHub issues;
- add stable identity markers to issue comments;
- update an existing matching issue comment instead of posting a duplicate;
- skip issue creation for zero-signal reports unless explicitly configured with `--post-empty`;
- treat rejected LLM outputs as nonfatal when `--allow-rejected-check-outputs` is used;
- treat transient provider-side availability failures as nonfatal when `--allow-provider-failures` is used;
- keep quota, rate-limit, authentication, configuration, request-shape, and unknown provider failures fatal;
- run deterministic page-structure checks in GitHub Actions on changed canonical stereotype pages;
- run scheduled LLM check-agent collection through GitHub Actions;
- upload generated check-agent outputs as GitHub Actions artifacts;
- provide manual, confirmation-gated issue-review workflows for `page-hygiene-checker` and `language-style-checker` issues;
- select the oldest eligible open `page-hygiene-checker` or `language-style-checker` signal issue for automated resolution;
- manually resolve a selected issue through `workflow_dispatch`;
- keep `gemini-3.5-flash` as the primary Gemini model for automated signal resolution;
- run Gemini `gemini-3.6-flash` once as the resolver fallback when the primary Gemini call fails with recognized provider-unavailability diagnostics;
- fail normally when the primary resolver call fails for non-provider-unavailability reasons;
- fail normally when the fallback resolver model also fails;
- generate and validate a strict JSON resolution plan;
- apply accepted exact local edits;
- insert automated resolver entries into the `Generation and Review Log` table;
- reject former deferred cases as `reject_for_phase_2_automation`;
- open pull requests for accepted resolver edits;
- update resolver PR branches by rebase;
- enable squash auto-merge for resolver PRs;
- comment on and close resolved signal issues;
- close issues with no accepted changes as `not_planned`;
- upload resolver plans as GitHub Actions artifacts.

These capabilities do not mean every scheduled LLM output is valid. Invalid model outputs are preserved as artifacts. In the canonical scheduled workflow, rejected check-agent outputs are nonfatal because the workflow passes:

```text
--allow-rejected-check-outputs
```

Transient provider-side availability failures and empty provider responses can remain nonfatal in the canonical scheduled signal-collector workflow when `--allow-provider-failures` is used. Quota, rate-limit, authentication, configuration, request-shape, unknown provider, resolver, and issue-manager failures remain fatal unless the relevant retry or wrapper logic succeeds.

The automated resolver workflow has a different failure-handling policy. It does not suppress primary resolver failures in general. It performs one Gemini `gemini-3.6-flash` fallback attempt only for recognized primary Gemini provider unavailability; invalid plans and other failures do not trigger fallback.

### Current limitations and operational risks

The current implementation still has these limitations and risks:

- manual issue-review prompts currently exist only for `page-hygiene-checker` and `language-style-checker`;
- the automated resolver currently supports only `page-hygiene-checker` and `language-style-checker`;
- no dedicated `page-structure-checker` issue-closure prompt exists; this prompt was intentionally discarded rather than left pending;
- page-structure signals should be handled through direct maintainer review and normal PR review;
- `providers/mock.py` is not part of the active `run_check_agent.py` provider set;
- `issue_manager.py` searches only open issues, so closed issues with matching titles are not reused;
- stable task identity is content- and configuration-addressed; unrelated commit SHAs are traceability metadata and do not create new work;
- provider transient-error and actionable-error detection is marker-based and may need extension if future observed SDK diagnostics are not caught by the current marker lists;
- scheduled LLM signal collection uses maximum safely usable free capacity but remains bounded by provider quotas and the workflow execution budget;
- automated resolver output quality depends on strict JSON compliance by the selected model;
- accepted resolver edits must be exact local replacements and may fail if `current_text` no longer occurs exactly once;
- resolver fallback detection is marker-based and currently depends on provider-error artifacts under `.tmp/phase-2/resolver`;
- the resolver fallback is workflow-level behavior, not a general `resolve_signal_issue.py` CLI option;
- the resolver closes the source signal issue after resolver completion, not after the PR has actually merged;
- PR merge still depends on repository settings, branch protection, required checks, and auto-merge availability;
- `gh pr update-branch --rebase` can fail if the branch cannot be cleanly rebased;
- auto-merge can remain pending if required checks are pending, blocked, or not configured correctly;
- `PHASE2_AUTOMATION_TOKEN` must have sufficient repository permissions to create pull requests, update branches, enable auto-merge, comment on issues, close issues, and push model-run statistics updates.

## Operational prerequisites

The current local implementation depends on:

- Python 3;
- dependencies from `requirements.txt`;
- a provider API key for real LLM runs;
- GitHub CLI authentication through `gh auth login` for local issue posting or local resolver use;
- `GH_TOKEN` or the default `github.token` for scheduled issue posting in GitHub Actions;
- `PHASE2_AUTOMATION_TOKEN` for GitHub Actions branch-write operations, including automated resolver operations and model-run statistics updates.

Current Python runtime dependencies from `requirements.txt` include:

```text
mkdocs>=1.6.1,<2.0.0
mkdocs-material==9.7.6
groq==1.5.0
google-genai>=2.10.0,<3.0.0
openai>=2.44.0,<3.0.0
```

The provider secrets used when the corresponding provider is selected are:

```text
GROQ_API_KEY
GEMINI_API_KEY
SAMBANOVA_API_KEY
OPENROUTER_API_KEY
```

The provider adapters use:

| Provider | Local/API environment variable behavior | GitHub Actions repository secret |
|---|---|---|
| `groq` | requires `GROQ_API_KEY` | `GROQ_API_KEY` |
| `gemini` | reads `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `GEMINI_API_KEY` |
| `sambanova` | requires `SAMBANOVA_API_KEY`; may use `SAMBANOVA_BASE_URL` override | `SAMBANOVA_API_KEY` |
| `openrouter` | requires `OPENROUTER_API_KEY` | `OPENROUTER_API_KEY` |

`GOOGLE_API_KEY` is only a provider-code fallback for local or alternate environments. It is not the canonical workflow secret.

API key values must never be committed or documented.

### Page-structure workflow prerequisites

The page-structure GitHub Actions workflow depends only on:

- repository checkout;
- Python;
- the deterministic checker script;
- read-only repository contents permission.

### Scheduled signal-collector workflow prerequisites

The scheduled LLM GitHub Actions workflow depends on:

- repository checkout;
- Python;
- dependencies from `requirements.txt`;
- `GROQ_API_KEY` when Groq is selected;
- `GEMINI_API_KEY` when Gemini is selected;
- `SAMBANOVA_API_KEY` when SambaNova is selected;
- `OPENROUTER_API_KEY` when OpenRouter is selected;
- `GH_TOKEN` backed by the default `github.token` for issue posting;
- `PHASE2_AUTOMATION_TOKEN` for lease and aggregate state commits;
- `contents: write`;
- `issues: write`.

The scheduled signal-collector workflow has repository contents write permission and uses `PHASE2_AUTOMATION_TOKEN` for serialized lease and aggregation commits through the state writer.

### Automated resolver workflow prerequisites

The automated resolver workflow depends on:

- repository checkout with full history;
- Python;
- dependencies from `requirements.txt`;
- `GROQ_API_KEY` when Groq is selected;
- `GEMINI_API_KEY` when Gemini is selected;
- `PHASE2_AUTOMATION_TOKEN` exposed as `GH_TOKEN`/`GITHUB_TOKEN` in GitHub Actions, or GitHub CLI authentication for local runs;
- GitHub CLI;
- a repository setting that gives GitHub Actions read/write workflow permissions;
- a repository setting that allows GitHub Actions to create and approve pull requests;
- repository auto-merge enabled;
- branch-protection rules that allow squash auto-merge after required checks pass.

The resolver workflow declares:

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

## Generated output policy

Generated Phase 2 outputs are not source files and must not be committed.

Generated local and CI outputs include paths such as:

```text
.tmp/phase-2/page-structure-checker/<page-id>/issue-comment-page-structure-checker.md
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.md
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.invalid.md
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.batch.log
.tmp/phase-2/batch-summary.md
.tmp/phase-2/resolver/issue-<issue-number>-plan.json
.tmp/phase-2/resolver/issue-<issue-number>-provider-error.txt
.tmp/phase-2/resolver/issue-<issue-number>-primary-provider-error.txt
issue-comment.md
issue-comment.invalid.md
```

The repository ignores these outputs with:

```text
.tmp/
issue-comment*.md
```

Resolver branches and pull requests are repository artifacts, not generated local output. They are intentionally created only when the resolver accepts at least one exact local edit and the deterministic page-structure check passes.

## Explicitly excluded Phase 2 checks

Phase 2 does not include additional check agents beyond the three listed agents.

In particular, Phase 2 does not currently include:

- a Caution Language Checker;
- a Conceptual Adequacy Checker;
- a Source Faithfulness Checker;
- a Cross-Page Consistency Checker;
- an OntoUML/UFO Semantic Validator.

The following remain outside Phase 2:

- conceptual adequacy analysis;
- source-faithfulness analysis;
- comparison with original papers or PDFs;
- cross-page consistency analysis;
- OntoUML/UFO semantic validation;
- claim acceptance or rejection as expert truth;
- broad automatic page rewriting;
- semantic patch planning;
- quorum evaluation across models;
- local/offline model integration.

Constrained automatic PR creation, automatic issue closure, and squash auto-merge are now part of the Phase 2 automated resolver only for exact local accepted edits in `page-hygiene-checker` and `language-style-checker` issues.

---

[Phase 2 index](index.md) | Next: [Check Agents](check-agents.md) →
