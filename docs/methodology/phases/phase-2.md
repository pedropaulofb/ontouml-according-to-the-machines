# Phase 2 — Lightweight Check-Agent Infrastructure

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its purpose is to provide lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages. Phase 2 does not perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, automatic page repair, pull-request generation, automatic issue closure, or auto-merge.

Phase 2 produces page-local **signals**, routes those signals to deterministic GitHub issues, and leaves signal acceptance, rejection, and closure decisions to later manual review.

This document reflects the repository state on **2026-06-09**.

## Purpose

Phase 2 has six goals:

1. implement three lightweight check agents for canonical stereotype pages;
2. run the deterministic Python check agent on page modifications;
3. run the two LLM-based check agents periodically in conservative rotating batches;
4. produce structured, page-local signals about page structure, page hygiene, formatting, and writing quality;
5. route check-agent outputs to deterministic GitHub issues scoped by page and check agent;
6. support later manual ChatGPT-assisted issue closure.

Phase 2 prioritizes infrastructure, signal quality, traceability, repeatability, and controlled issue routing over deep content judgment.

## Phase 2 boundary

Phase 2 implements:

```text
check agents
→ check-agent execution
→ output validation
→ issue routing
→ planned manual issue-closure support
```

Phase 2 does **not** implement autonomous resolution agents.

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

The issue manager:

- reads validated check-agent reports;
- derives the reviewed page identity;
- derives the check-agent identity;
- creates or reuses one open GitHub issue per page and check agent;
- posts model-specific check-agent reports as comments in that issue;
- updates a matching existing comment when the stable comment identity already exists.

Manual issue-closure prompts:

- are planned Phase 2 documentation artifacts;
- are intended for use with ChatGPT by a human maintainer;
- help evaluate the signals in one issue;
- help decide whether the issue should be closed as completed, closed as not planned, or left open;
- do not run automatically;
- do not replace human judgment.

## Current Phase 2 architecture

The Phase 2 architecture contains exactly three check agents:

```text
check-agents
├── page-structure-checker
├── page-hygiene-checker
└── language-style-checker
```

The implemented execution model is:

```text
page-structure-checker
└── deterministic Python
└── runs after canonical stereotype page modifications
└── blocks structural regressions in CI

page-hygiene-checker
└── LLM-based
└── runs through the agent-aware LLM runner
└── runs periodically through the rotating scheduled workflow
└── reports page-hygiene signals

language-style-checker
└── LLM-based
└── runs through the agent-aware LLM runner
└── runs periodically through the rotating scheduled workflow
└── reports language/style signals
```

The implemented issue-routing model is:

```text
one GitHub issue per page + check agent
```

Different models executed by the same agent for the same page post comments in the same issue.

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

If `page-hygiene-checker` runs with multiple LLM models on `classes/event`, all those model outputs belong in:

```text
Check signal: page-hygiene-checker: classes/event
```

## Current implementation status

The current implementation includes the core runtime pieces of the simplified Phase 2 architecture: check execution, output validation, page-plus-agent issue routing, duplicate-control for comments, and scheduled LLM collection. Manual issue-closure prompt support remains planned.

### Implemented files and artifacts

```text
.github/workflows/page-structure-check.yml
.github/workflows/phase-2-check-agents.yml
prompts/phase-2/page-hygiene-checker-v1.0.2.md
prompts/phase-2/language-style-checker-v1.0.2.md
scripts/phase-2/run_check_agent.py
scripts/phase-2/run_check_batch.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_page_structure_batch.py
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
```

Legacy compatibility or stale artifacts still exist:

```text
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/run_review_batch.py
scripts/phase-2/providers/mock.py
```

These legacy artifacts are not the current scheduled Phase 2 LLM execution path. They should either be clearly marked as legacy or removed in a later cleanup.

A legacy prompt path is referenced by legacy code:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
```

That legacy general page-reviewer prompt is not part of the simplified three-agent Phase 2 architecture.

### Current capabilities

The current implementation can:

- run the deterministic `page-structure-checker`;
- run one LLM check-agent invocation through `run_check_agent.py`;
- route `page-hygiene-checker` to `prompts/phase-2/page-hygiene-checker-v1.0.2.md`;
- route `language-style-checker` to `prompts/phase-2/language-style-checker-v1.0.2.md`;
- call Groq models through the Groq provider adapter;
- validate generated LLM signal comments against agent-specific contracts;
- write valid generated comments to `.tmp/phase-2/`;
- write invalid generated comments to `.invalid.md` files for debugging;
- run page × agent × model batches through `run_check_batch.py`;
- select rotating scheduled triples with hourly or daily rotation seeds;
- run one selected triple per scheduled interval with `--selection rotate --max-runs 1`;
- run in `generate`, `dry-run`, or `post` mode;
- write per-run logs and a batch summary under `.tmp/phase-2/`;
- derive deterministic page-plus-agent issue titles;
- create or reuse open GitHub issues;
- add stable identity markers to issue comments;
- update an existing matching issue comment instead of posting a duplicate;
- skip issue creation for zero-signal reports unless explicitly configured with `--post-empty`;
- run deterministic page-structure checks in GitHub Actions on changed canonical stereotype pages;
- run scheduled LLM check-agent collection hourly through GitHub Actions;
- upload generated outputs as GitHub Actions artifacts.

These capabilities do not mean every scheduled LLM output is valid. Invalid model outputs are preserved as artifacts and currently make the selected batch run fail.

### Current limitations and operational risks

The current implementation still has these limitations:

- manual issue-closure prompts are planned but not yet created;
- legacy runner/config files still exist and may confuse future maintenance;
- `run_check_agent.py` currently supports only the Groq provider in the active agent-aware path;
- `providers/mock.py` is stale relative to the active `run_check_agent.py` contracts;
- `requirements.txt` does not pin or include the Groq runtime dependency used by the scheduled workflow;
- `run_check_batch.py` currently fails the batch when the selected LLM output fails validation;
- the scheduled workflow therefore turns red when the selected model output is invalid, although the next scheduled hour still runs;
- `issue_manager.py` searches only open issues, so closed issues with matching titles are not reused;
- stable comment identity includes the commit SHA, so a new commit may produce a new model comment for the same page, agent, provider, model, and prompt.

## Operational prerequisites

The current local implementation depends on:

- Python 3;
- `groq` for Groq API calls when using the active LLM provider;
- a `GROQ_API_KEY` environment variable for real Groq runs;
- GitHub CLI authentication through `gh auth login` for local issue posting;
- `GH_TOKEN` or the default `github.token` for issue posting in GitHub Actions.

The Groq API key must never be committed.

The current page-structure GitHub Actions workflow depends only on:

- repository checkout;
- Python;
- the deterministic checker script;
- read-only repository contents permission.

The scheduled LLM GitHub Actions workflow depends on:

- repository checkout;
- Python;
- `groq`;
- `GROQ_API_KEY`;
- `GH_TOKEN`;
- `contents: read`;
- `issues: write`.

## Generated output policy

Generated Phase 2 outputs are not source files and must not be committed.

Generated local and CI outputs include paths such as:

```text
.tmp/phase-2/page-structure-checker/<page-id>/issue-comment-page-structure-checker.md
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.md
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.invalid.md
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.batch.log
.tmp/phase-2/batch-summary.md
issue-comment.md
issue-comment.invalid.md
```

The repository ignores these outputs with:

```text
.tmp/
issue-comment*.md
```

## Phase 2 check agents

### 1. Page Structure Checker

| Property | Value |
|---|---|
| Agent slug | `page-structure-checker` |
| Type | Deterministic Python |
| LLM required | No |
| Phase | 2 |
| Implementation status | Implemented |
| Script | `scripts/phase-2/check_agents/page_structure_checker.py` |
| Local batch runner | `scripts/phase-2/run_page_structure_batch.py` |
| GitHub Actions workflow | `.github/workflows/page-structure-check.yml` |
| Provider metadata | `python` |
| Model metadata | `deterministic` |
| Prompt metadata | `n/a` |
| Output | Structured Markdown signal report; deterministic YAML block currently included |
| Applies changes | No |
| Target execution | On canonical stereotype page modifications |

The Page Structure Checker verifies the expected stereotype-page skeleton.

It checks:

- required headings;
- heading order;
- duplicate required headings;
- missing required sections;
- malformed required heading levels;
- unexpected level-2 sections;
- empty required sections where the project expects placeholder text.

Expected canonical stereotype-page headings are:

```text
## Description
## Stereotype Profile
## Examples
## References
### Direct Citations
### Consulted Sources
## Generation and Review Log
```

The checker may propose an exact structural repair, such as inserting a missing heading, but it must not apply the repair.

It reports:

```text
Agent: page-structure-checker
Provider: python
Model: deterministic
Prompt: n/a
```

#### Skeleton-page marker

Some pages may intentionally exist as skeleton pages before content has been produced.

Such pages may be marked with:

```markdown
<!-- skeleton-page -->
```

When this marker is present, the checker suppresses empty-section signals for that page. The checker still performs structural checks for required headings, heading levels, heading order, duplicate headings, and unexpected level-2 sections.

#### Local all-page runner

The local all-page runner is:

```text
scripts/phase-2/run_page_structure_batch.py
```

Default behavior:

- discovers canonical stereotype pages under:
  - `docs/stereotypes/classes/*.md`;
  - `docs/stereotypes/relations/*.md`;
- excludes `index.md` pages;
- runs `page_structure_checker.py` once per page;
- writes one report per page under `.tmp/phase-2/page-structure-checker/`;
- parses `Signal count`;
- prints a batch summary;
- does not create GitHub issues unless `--post` is passed.

Common commands:

```bash
python scripts/phase-2/run_page_structure_batch.py --dry-run
```

```bash
python scripts/phase-2/run_page_structure_batch.py
```

```bash
python scripts/phase-2/run_page_structure_batch.py \
  --post \
  --issue-dry-run \
  --repo pedropaulofb/ontouml-according-to-the-machines
```

```bash
python scripts/phase-2/run_page_structure_batch.py \
  --post \
  --repo pedropaulofb/ontouml-according-to-the-machines
```

When `--post` is passed, the runner posts only reports with `Signal count > 0` and skips zero-signal reports to avoid issue/comment noise.

#### GitHub Actions workflow

The page-structure CI workflow is:

```text
.github/workflows/page-structure-check.yml
```

It runs on:

- pull requests that modify canonical stereotype pages, the checker script, or the workflow file;
- pushes to `main` that modify canonical stereotype pages, the checker script, or the workflow file;
- manual `workflow_dispatch`.

Behavior:

- if canonical stereotype pages changed, it checks only those pages;
- if the checker script changed, it checks all canonical stereotype pages;
- if the workflow file changed, it checks all canonical stereotype pages;
- if manually triggered, it checks all canonical stereotype pages;
- it excludes `index.md` pages;
- it passes `--commit-sha` using the workflow commit SHA;
- it uploads generated reports as the `page-structure-check-reports` artifact;
- it fails the workflow when one or more structural signals are reported;
- it does not create GitHub issues or comments.

Recommended branch-protection setting for blocking merges:

```text
Require status checks to pass before merging
Required status check: Check stereotype page structure
```

### 2. Page Hygiene Checker

| Property | Value |
|---|---|
| Agent slug | `page-hygiene-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Implemented in the active agent-aware LLM runner and scheduled workflow |
| Runner | `scripts/phase-2/run_check_agent.py` |
| Batch runner | `scripts/phase-2/run_check_batch.py` |
| Prompt | `prompts/phase-2/page-hygiene-checker-v1.0.2.md` |
| Supported active provider | `groq` |
| Output | Structured Markdown signal comment |
| Applies changes | No |
| Target execution | Periodic conservative rotating batches |

The Page Hygiene Checker checks only visible page-hygiene issues in Markdown content that is present.

It covers:

- visible reference hygiene;
- Markdown hygiene;
- encoding hygiene;
- Generation and Review Log hygiene.

Its categories are:

```text
reference_hygiene
markdown_hygiene
encoding_hygiene
review_log_hygiene
```

It must not:

- validate quotations against original sources;
- infer source content;
- check PDFs, papers, theses, or external sources;
- compare the page with related stereotype pages;
- decide whether a citation substantively supports a claim;
- evaluate conceptual correctness;
- report missing required top-level sections;
- report missing required reference or review-log sections;
- check grammar or writing style except where a visible Markdown or encoding artifact is the issue;
- recommend conceptual rewrites;
- recommend repository actions or workflow changes.

The active `page-hygiene-checker-v1.0.2` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

`run_check_agent.py` validates the output against the configured page-hygiene contract. Invalid model output is written as `.invalid.md` and is not posted.

### 3. Language Style Checker

| Property | Value |
|---|---|
| Agent slug | `language-style-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Implemented in the active agent-aware LLM runner and scheduled workflow |
| Runner | `scripts/phase-2/run_check_agent.py` |
| Batch runner | `scripts/phase-2/run_check_batch.py` |
| Prompt | `prompts/phase-2/language-style-checker-v1.0.2.md` |
| Supported active provider | `groq` |
| Output | Structured Markdown signal comment |
| Applies changes | No |
| Target execution | Periodic conservative rotating batches |

The Language Style Checker identifies low-risk writing-quality issues in one provided canonical stereotype page.

It checks only:

- grammar;
- spelling;
- clarity;
- professional technical style;
- project or process self-reference in reader-facing documentation.

Its categories are:

```text
grammar
spelling
clarity
professional_style
project_self_reference
```

Reader-facing prose includes visible documentation text intended for readers of the stereotype page, including:

- headings;
- paragraphs;
- list items;
- table cells;
- captions;
- image alt text.

The active runner scopes the input for `language-style-checker` by excluding these sections before calling the provider:

```text
References
Direct Citations
Consulted Sources
Generation and Review Log
```

The checker must protect:

- direct quotations;
- citation locators;
- bibliographic entries;
- source titles;
- Markdown links or link targets;
- stereotype names;
- formal definitions;
- OntoUML claims;
- source interpretations;
- technical terminology when meaning could change.

It reports at most three signals. `Signal count` must exactly equal the number of emitted `#### S-...` signal sections. Signal IDs must be sequential and limited to `S-001`, `S-002`, and `S-003`.

Its location format is:

```text
Location: Section: "<nearest heading, or Document root if no heading applies>"; Fragment: "<exact affected fragment from the same location, maximum 160 characters>"
```

It may include `current_text` and `proposed_text` only when the replacement is exact, contiguous, local, low-risk, meaning-preserving, and does not cross sentence, paragraph, heading, table-cell, or list-item boundaries.

When included, `current_text` and `proposed_text` must be emitted together, wrapped in double quotation marks, and escaped when necessary.

It must not include `current_text` or `proposed_text` for issues inside protected content.

The active `language-style-checker-v1.0.2` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

`run_check_agent.py` validates the output against the configured language-style contract. Invalid model output is written as `.invalid.md` and is not posted.

## Explicitly excluded Phase 2 checks

Phase 2 does not include additional check agents beyond the three listed agents.

In particular, Phase 2 does not currently include:

- a Caution Language Checker;
- a Conceptual Adequacy Checker;
- a Source Faithfulness Checker;
- a Cross-Page Consistency Checker;
- an OntoUML/UFO Semantic Validator.

The following are outside Phase 2:

- conceptual adequacy analysis;
- source-faithfulness analysis;
- comparison with original papers or PDFs;
- cross-page consistency analysis;
- OntoUML/UFO semantic validation;
- claim acceptance or rejection;
- automatic page rewriting;
- automatic pull-request generation;
- automatic patch application;
- automatic issue closing;
- auto-merge.

These may be considered in a later phase, but they are not Phase 2 completion requirements.

## Signal terminology

Phase 2 outputs are **signals**, not accepted findings.

Use:

```text
Signal count
Signal
S-001
S-002
S-003
```

Avoid:

```text
Finding count
Finding
F-001
```

Rationale: a Phase 2 signal is a candidate observation. It has not yet been accepted, rejected, deduplicated, or converted into an edit plan.

## Signal output structure

Each check-agent output should be one structured Markdown comment.

Required heading:

```markdown
## Check signal report: <agent> / <provider> / <model> — <review date>
```

Required metadata table:

```markdown
### Run metadata

| Field | Value |
|---|---|
| Agent | <agent-slug> |
| Provider | <provider> |
| Model | <model> |
| Prompt | <prompt-id or n/a> |
| Review date | <review date> |
| Reviewed page | <path> |
| Commit SHA | <sha> |
| Signal count | <number of emitted signal sections, or 0 if none> |
```

For LLM-based check agents, `Signal count` must exactly match the number of emitted `#### S-...` signal sections.

Required summary section:

```markdown
### Summary judgment

<agent-specific summary sentence>
```

Required scope section:

```markdown
### Scope

<agent-specific scope statement>
```

Required signal section:

```markdown
### Signals

#### S-001 — <short plain-text signal title>

- Category: <agent-specific category>
- Severity: <low | medium | high>
- Confidence: <low | medium | high>
- Location: Section: "<nearest heading, or Document root if no heading applies>"; Fragment: "<exact affected fragment, maximum 160 characters>"
- Observation: <single-line observation>
- Rationale: <single-line rationale>
- Recommendation: <single-line recommendation>
```

Agent-specific contracts may allow optional exact replacement fields:

```markdown
- current_text: "<exact current text copied from the page>"
- proposed_text: "<exact local replacement text>"
```

Optional replacement fields must be emitted together or omitted together. They must not be emitted as empty values, placeholders, `None`, or `N/A`.

For no-signal runs, the prompt still requires a full comment with `Signal count` set to `0` and this exact sentence under `### Signals`:

```markdown
None identified within the configured check-agent scope.
```

## Structured signal data

Machine-readable signal data is currently agent- and version-dependent.

Current status:

- `page-structure-checker` emits YAML blocks because its output is generated deterministically by Python;
- `page-hygiene-checker-v1.0.2` is Markdown-only;
- `language-style-checker-v1.0.2` is Markdown-only;
- machine-readable signal blocks for LLM-based agents are deferred to a later prompt version or later tooling.

The Markdown text is for humans and issue readability. Structured blocks are optional infrastructure for later deterministic tooling.

## Issue routing model

The implemented Phase 2 issue routing model is one open GitHub issue per:

```text
page + check agent
```

Implemented issue title pattern:

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

The page identity is derived from the reviewed page path:

```text
docs/stereotypes/classes/event.md -> classes/event
docs/stereotypes/relations/material.md -> relations/material
```

All model outputs for the same page and same check agent are posted to the same open issue.

For example, if `page-hygiene-checker` runs with two models on `docs/stereotypes/classes/event.md`, both model reports are comments under:

```text
Check signal: page-hygiene-checker: classes/event
```

The issue manager currently searches only open issues with an exact matching title. Closed issues are not reused.

## Issue body pattern

When creating a new issue, the issue body uses this structure:

```markdown
# Check signal: <agent-slug>: <page-id>

## Reviewed page

`<docs/stereotypes/...>.md`

## Page identity

`<group>/<stereotype-id>`

## Check agent

`<agent-slug>`

## Purpose

Collect check-agent signal comments for this page and agent.

## Resolution model

Signals are candidate observations. They are not accepted findings until reviewed.

This issue may be resolved manually or by later resolution tooling.
```

## Comment identity and duplicate control

Phase 2 supports stable comment identity.

Stable identity fields:

```text
page
agent
provider
model
prompt
commit
```

The issue manager inserts a hidden marker into the posted comment:

```markdown
<!-- check-signal-comment
page: <reviewed page>
agent: <agent>
provider: <provider>
model: <model>
prompt: <prompt>
commit: <commit SHA>
-->
```

If a comment with the same stable identity already exists in the target issue, the system updates the existing comment instead of posting a new one.

If the commit SHA changes, a new comment may be posted because the reviewed page content may have changed.

## Batch execution model

The active LLM batch runner is:

```text
scripts/phase-2/run_check_batch.py
```

It iterates over:

```text
pages × check agents × models
```

Default active LLM agents:

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
openai/gpt-oss-20b
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

Common examples:

```bash
python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider groq \
  --model llama-3.3-70b-versatile \
  --mode generate
```

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
  --repo pedropaulofb/ontouml-according-to-the-machines
```

```bash
python scripts/phase-2/run_check_batch.py \
  --pages-glob "docs/stereotypes/classes/*.md" \
  --pages-glob "docs/stereotypes/relations/*.md" \
  --exclude-pages-glob "docs/stereotypes/**/index.md" \
  --provider groq \
  --selection rotate \
  --rotation-seed hourly \
  --max-runs 1 \
  --mode post \
  --repo pedropaulofb/ontouml-according-to-the-machines
```

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

### LLM-agent execution

The two LLM-based agents run periodically through the scheduled workflow:

```text
page-hygiene-checker
language-style-checker
```

The current scheduled workflow is:

```text
.github/workflows/phase-2-check-agents.yml
```

Workflow display name:

```text
Check-agent signal collector
```

It runs:

```text
17 * * * *
```

That means it is scheduled once per hour at minute 17 UTC.

The workflow is also manually triggerable through `workflow_dispatch`.

Effective scheduled defaults:

```text
mode: post
selection: rotate
rotation_seed: hourly
max_runs: 1
sleep_seconds: 0
agents: page-hygiene-checker,language-style-checker
models: llama-3.3-70b-versatile,openai/gpt-oss-20b
pages: all canonical class and relation stereotype pages, excluding index.md
```

The scheduled run therefore selects one `(page, agent, model)` triple per hour from the full plan and advances through the rotating plan over time.

If a selected LLM output fails validation:

- the generated invalid output is saved as `.invalid.md`;
- `issue_manager.py` is not called for that output;
- artifacts are still uploaded;
- the workflow run is marked failed under the current batch runner behavior;
- the next scheduled hour still runs and selects according to the current hourly rotation index.

## Free-model and slow-automation strategy

Phase 2 is designed to work within free or low-cost model quotas.

The intended strategy is:

- keep prompts compact;
- cap outputs to a small number of signals;
- run one selected triple per scheduled interval;
- use lightweight models;
- use deterministic Python whenever possible;
- spread execution over time;
- avoid heavyweight models in Phase 2;
- rely on gradual accumulation rather than large one-shot reviews.

This supports a slow continuous process: small page/agent/model batches can run over time, allowing the project to accumulate signals incrementally.

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
[ ] Require signed commits
[ ] Require deployments to succeed before merging
[ ] Lock branch
[x] Do not allow bypassing the above settings
[ ] Allow force pushes
[ ] Allow deletions
```

`Require linear history` is optional and should be enabled only if the repository intentionally avoids merge commits.

### Scheduled check-agent workflow

The scheduled check-agent workflow creates or updates GitHub issues/comments in `post` mode.

Required repository secret:

```text
GROQ_API_KEY
```

Required workflow permissions:

```yaml
permissions:
  contents: read
  issues: write
```

The workflow uploads `.tmp/phase-2` as an artifact even if the check-agent run fails.

## Manual issue-closure prompt support

Phase 2 should include three manual ChatGPT prompts for closing check-agent issues.

Planned prompt files:

```text
prompts/phase-2/issue-closure/close-page-structure-signal-issue.md
prompts/phase-2/issue-closure/close-page-hygiene-signal-issue.md
prompts/phase-2/issue-closure/close-language-style-signal-issue.md
```

These prompts are **not yet created**.

The prompts should help a human maintainer use ChatGPT to resolve one Phase 2 issue at a time.

Each closure prompt should guide ChatGPT to:

1. read the issue body and all check-agent comments;
2. inspect the referenced canonical stereotype page;
3. classify each signal as `accept`, `reject`, or `defer`;
4. explain the decision for each signal;
5. propose exact edits only when they are safe and local;
6. produce a closing comment for the GitHub issue;
7. recommend whether the issue should be closed as `completed`, closed as `not planned`, or left open.

Closure prompts must preserve the Phase 2 boundary:

- they are manually invoked;
- they do not run in CI;
- they do not directly edit repository files;
- they do not commit changes;
- they do not open pull requests;
- they do not close issues automatically.

Agent-specific closure prompts are preferred because each agent has a different scope and different protected-content rules.

### Page-structure issue-closure prompt

The page-structure closure prompt should focus on deterministic structural signals.

It should evaluate:

- missing headings;
- malformed heading levels;
- heading order;
- duplicate headings;
- unexpected level-2 sections;
- empty required sections when the page is not marked as an intentional skeleton.

It should not evaluate:

- source faithfulness;
- OntoUML correctness;
- language quality beyond structural headings;
- conceptual adequacy.

### Page-hygiene issue-closure prompt

The page-hygiene closure prompt should focus on visible hygiene signals.

It should evaluate:

- visible reference-hygiene issues;
- Markdown-hygiene issues;
- encoding issues;
- Generation and Review Log hygiene.

It should not validate source content or infer missing source support.

### Language-style issue-closure prompt

The language-style closure prompt should focus on low-risk writing-quality signals in reader-facing prose.

It should evaluate:

- grammar;
- spelling;
- clarity;
- professional technical style;
- project/process self-reference in reader-facing text.

It should protect:

- direct quotations;
- citation locators;
- bibliographic entries;
- source titles;
- stereotype names;
- formal definitions;
- OntoUML claims;
- source interpretations;
- technical terminology when meaning could change.

## Future work outside Phase 2

The following may be considered in later phases, but should not be required for Phase 2 completion:

- autonomous resolution agents;
- model quorum rules;
- signal deduplication across agents;
- patch planning;
- deterministic patch application;
- verification agents;
- automatic PR creation;
- automatic issue closure;
- auto-merge;
- source-faithfulness validation;
- heavy semantic analysis;
- local/offline model integration.

A later automated pipeline may eventually be:

```text
check agents
→ signal issues
→ resolution support
→ deterministic patching
→ verification checks
→ pull request
→ CI
→ issue update or closure
```

That later pipeline is not part of the simplified Phase 2 scope.

## Current migration status

Completed:

- Phase 2 methodology defines lightweight check-agent infrastructure;
- signal terminology is used by the current runners and issue manager;
- `page-structure-checker` exists as the deterministic Python check agent;
- `page-structure-checker` supports an explicit `<!-- skeleton-page -->` marker for intentional skeleton pages;
- `run_page_structure_batch.py` runs the deterministic page-structure checker across canonical stereotype pages;
- `.github/workflows/page-structure-check.yml` runs the page-structure checker in CI;
- the page-structure CI workflow uploads generated reports as artifacts and fails on structural signals;
- `page-hygiene-checker-v1.0.2` exists as a dedicated LLM check-agent prompt;
- `language-style-checker-v1.0.2` exists as a dedicated LLM check-agent prompt;
- `run_check_agent.py` runs the two LLM check agents through an agent-aware contract;
- `run_check_agent.py` validates generated LLM output and writes `.invalid.md` debugging files for invalid output;
- `run_check_batch.py` supports page × agent × model execution;
- `run_check_batch.py` supports rotating scheduled selection;
- `issue_manager.py` implements page-plus-agent issue routing;
- `issue_manager.py` implements stable comment identity;
- `issue_manager.py` updates matching existing comments instead of posting duplicates;
- `.github/workflows/phase-2-check-agents.yml` runs scheduled hourly LLM check-agent collection;
- scheduled runs can create or update GitHub issues/comments in `post` mode;
- generated output paths are ignored by `.gitignore`.

Pending:

1. create the three manual issue-closure prompts;
2. decide whether scheduled LLM validation failures should remain fatal or become nonfatal warnings;
3. mark or remove legacy Phase 2 runner/config/provider artifacts;
4. pin or document runtime dependencies for the active Groq-based execution path;
5. document any observed clean baseline with a dated run artifact rather than an undocumented local claim.

Deferred outside Phase 2:

- additional check agents beyond the three Phase 2 agents;
- automated GitHub issue closure;
- Phase 3 resolution agents;
- quorum evaluation;
- patch planning;
- patch application;
- automatic PR creation;
- auto-merge;
- source-faithfulness validation;
- heavy semantic analysis;
- local/offline model integration.

## Recommended next implementation steps

### Step 1 — Replace the stale Phase 2 documentation

Replace the repository’s current Phase 2 documentation with this updated version.

Suggested commit message:

```bash
docs(phase-2): align documentation with check-agent implementation
```

### Step 2 — Decide scheduled failure policy

Current behavior:

- invalid LLM output fails `run_check_agent.py`;
- the invalid report is saved as `.invalid.md`;
- `run_check_batch.py` marks the run failed;
- the workflow run becomes red;
- the next hourly schedule still runs.

If red scheduled runs are acceptable evidence of invalid model output, no change is needed.

If the goal is always-green hourly collection with invalid outputs captured only as artifacts, add an explicit nonfatal check-output policy to `run_check_batch.py` and pass it from the scheduled workflow.

Suggested commit message:

```bash
ci(phase-2): keep scheduled check-agent runs nonfatal on invalid outputs
```

### Step 3 — Clean up legacy Phase 2 execution artifacts

Clarify or remove these artifacts:

```text
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/run_review_batch.py
scripts/phase-2/providers/mock.py
```

Suggested commit message:

```bash
chore(phase-2): mark legacy review runners as deprecated
```

### Step 4 — Add manual issue-closure prompts

Add:

```text
prompts/phase-2/issue-closure/close-page-structure-signal-issue.md
prompts/phase-2/issue-closure/close-page-hygiene-signal-issue.md
prompts/phase-2/issue-closure/close-language-style-signal-issue.md
```

Suggested commit message:

```bash
docs(phase-2): add manual issue-closure prompts
```

## Completion criteria

Phase 2 can be considered complete when:

- the simplified three-agent architecture is documented;
- `page-structure-checker` is implemented and runs after canonical stereotype page modifications;
- `page-hygiene-checker` is implemented as an LLM-based check agent and runs in conservative periodic batches;
- `language-style-checker` is implemented as an LLM-based check agent and runs in conservative periodic batches;
- issue routing is page-plus-agent based;
- outputs use signal terminology;
- generated comments are structured according to each agent contract and pass validation before posting;
- all model outputs for the same page and agent are routed to the same issue;
- repeated runs update existing comments when the stable identity is unchanged;
- generated outputs remain uncommitted;
- small batch execution works locally;
- page-structure CI blocks structural regressions;
- conservative scheduled LLM execution works;
- three manual issue-closure prompts exist for human/ChatGPT-assisted issue resolution.

## Generation and review log

- Phase 2 revised from a broader check-and-future-resolution architecture into a simplified lightweight check-agent infrastructure.
- The simplified Phase 2 target has exactly three check agents: one deterministic Python agent and two LLM-based agents.
- The deterministic Python agent is `page-structure-checker`.
- The two LLM-based agents are `page-hygiene-checker` and `language-style-checker`.
- The `page-structure-checker` runs after canonical stereotype page modifications and blocks structural regressions in CI.
- The two LLM-based check agents run periodically through the scheduled rotating workflow.
- Issue routing is one GitHub issue per page and check agent.
- Different models executed by the same agent for the same page create comments in the same issue.
- Stable comment identity is implemented with page, agent, provider, model, prompt, and commit.
- Matching existing comments are updated instead of duplicated.
- Manual issue closure remains planned documentation-supported activity.
- The planned issue-closure support consists of three ChatGPT prompts, one per check agent.
- Resolution agents, quorum decisions, patch planning, patch application, PR creation, automatic issue closure, and auto-merge are outside the simplified Phase 2 scope.
