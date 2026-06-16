# Phase 2 — Lightweight Check-Agent and Automated Signal-Resolution Infrastructure

Phase 2 is the second documented project phase of **OntoUML According to the Machines**.

Its purpose is to provide lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages, plus a tightly bounded automated resolver for selected Phase 2 signal issues.

Phase 2 still does **not** perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, OntoUML/UFO semantic validation, or conceptual adequacy assessment. Phase 2 signals remain candidate observations until they are reviewed or resolved within the documented workflow.

This document reflects the repository state verified from committed repository files on **2026-06-16**, with the latest observed Phase 2 commit:

```text
96a2e6c8dd43f32fdaac5b15d6fa706cdf33b3d2
```

That commit extends the deterministic page-structure checker to validate the `Generation and Review Log` table schema.

## Documentation structure

This document is the canonical Phase 2 methodology page.

Gemini provider support, check-agent execution, issue routing, and automated signal resolution are documented inline here. A separate `phase-2-gemini-provider.md` or resolver-only methodology page is not required unless a later documentation split is intentionally added to the MkDocs navigation.

## Purpose

Phase 2 has eight goals:

1. implement three lightweight check agents for canonical stereotype pages;
2. run the deterministic Python check agent on canonical stereotype page modifications;
3. run the two LLM-based check agents periodically in conservative rotating batches;
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
→ manual signal-review support for LLM-based agents
→ automated signal resolution for selected LLM-based signal issues
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

Different providers and models executed by the same agent for the same page post comments in the same issue.

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

The current implementation includes check execution, output validation, page-plus-agent issue routing, duplicate-control for comments, scheduled LLM collection, Groq/Gemini provider support, manual signal-review prompts for the two LLM-based agents, automated signal-resolution prompts for those agents, deterministic patch application, PR creation, branch update by rebase, squash auto-merge enablement, and issue closure.

There is no current dedicated manual or automated closure prompt for `page-structure-checker`; page-structure issues remain subject to direct maintainer review and normal PR review.

### Implemented files and artifacts

```text
.github/workflows/page-structure-check.yml
.github/workflows/check-agent-signal-collector.yml
.github/workflows/phase-2-signal-resolver.yml
requirements.txt
prompts/phase-2/page-hygiene-checker-v1.0.2.md
prompts/phase-2/language-style-checker-v1.0.2.md
prompts/phase-2/close-page-hygiene-signal-issue-v1.0.0.md
prompts/phase-2/close-language-style-signal-issue-v1.0.0.md
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.1.0.md
prompts/phase-2/resolve-language-style-signal-issue-v1.1.0.md
scripts/phase-2/run_check_agent.py
scripts/phase-2/run_check_batch.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_page_structure_batch.py
scripts/phase-2/resolve_signal_issue.py
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/gemini.py
```

Non-canonical or legacy-support artifacts may also exist:

```text
.github/workflows/phase-2-check-agents.yml.bak
scripts/phase-2/providers/mock.py
```

These are not the canonical scheduled Phase 2 LLM execution path. The `.bak` workflow reflects older Groq-only and 20-minute-cadence assumptions and should not be used as operational documentation. The canonical shared LLM workflow is:

```text
.github/workflows/check-agent-signal-collector.yml
```

The repository ignores `scripts/local/`. Any machine-local dispatcher or helper under that path is outside canonical repository infrastructure unless it is intentionally committed and documented as reusable tooling.

### Current capabilities

The current implementation can:

- run the deterministic `page-structure-checker`;
- validate the `Generation and Review Log` table structure in canonical stereotype pages;
- run one LLM check-agent invocation through `run_check_agent.py`;
- route `page-hygiene-checker` to `prompts/phase-2/page-hygiene-checker-v1.0.2.md`;
- route `language-style-checker` to `prompts/phase-2/language-style-checker-v1.0.2.md`;
- call Groq models through `scripts/phase-2/providers/groq.py`;
- call Gemini models through `scripts/phase-2/providers/gemini.py`;
- validate generated LLM signal comments against agent-specific contracts;
- write valid generated comments to `.tmp/phase-2/`;
- write invalid generated comments to `.invalid.md` files for debugging;
- run page × agent × provider × model collection through the scheduled workflow;
- run page × agent × model batches for one selected provider through `run_check_batch.py`;
- select rotating scheduled combinations over time;
- run in `generate`, `dry-run`, or `post` mode;
- write per-run logs and a batch summary under `.tmp/phase-2/`;
- derive deterministic page-plus-agent issue titles;
- create or reuse open GitHub issues;
- add stable identity markers to issue comments;
- update an existing matching issue comment instead of posting a duplicate;
- skip issue creation for zero-signal reports unless explicitly configured with `--post-empty`;
- treat rejected LLM outputs as nonfatal when `--allow-rejected-check-outputs` is used;
- run deterministic page-structure checks in GitHub Actions on changed canonical stereotype pages;
- run scheduled LLM check-agent collection through GitHub Actions;
- upload generated check-agent outputs as GitHub Actions artifacts;
- provide manual, confirmation-gated issue-review workflows for `page-hygiene-checker` and `language-style-checker` issues;
- select the oldest eligible open `page-hygiene-checker` or `language-style-checker` signal issue for automated resolution;
- manually resolve a selected issue through `workflow_dispatch`;
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

Provider failures, configuration failures, resolver failures, and issue-manager failures remain fatal unless provider retry logic succeeds or the failure is explicitly handled by the relevant wrapper.

### Current limitations and operational risks

The current implementation still has these limitations and risks:

- manual issue-review prompts currently exist only for `page-hygiene-checker` and `language-style-checker`;
- the automated resolver currently supports only `page-hygiene-checker` and `language-style-checker`;
- no dedicated `page-structure-checker` issue-closure prompt exists; this prompt was intentionally discarded rather than left pending;
- page-structure signals should be handled through direct maintainer review and normal PR review;
- `providers/mock.py` is not part of the active `run_check_agent.py` provider set;
- `issue_manager.py` searches only open issues, so closed issues with matching titles are not reused;
- stable comment identity includes the commit SHA, so a new commit may produce a new model comment for the same page, agent, provider, model, and prompt;
- Gemini transient-error detection is marker-based and may need extension if future observed SDK diagnostics are not caught by the current marker list;
- scheduled LLM signal-collection runs intentionally collect signals gradually rather than executing the full matrix in one workflow execution;
- automated resolver output quality depends on strict JSON compliance by the selected model;
- accepted resolver edits must be exact local replacements and may fail if `current_text` no longer occurs exactly once;
- the resolver closes the source signal issue after resolver completion, not after the PR has actually merged;
- PR merge still depends on repository settings, branch protection, required checks, and auto-merge availability;
- `gh pr update-branch --rebase` can fail if the branch cannot be cleanly rebased;
- auto-merge can remain pending if required checks are pending, blocked, or not configured correctly;
- the GitHub Actions token must have sufficient repository permissions to create pull requests, update branches, enable auto-merge, comment on issues, and close issues.

## Operational prerequisites

The current local implementation depends on:

- Python 3;
- dependencies from `requirements.txt`;
- a provider API key for real LLM runs;
- GitHub CLI authentication through `gh auth login` for local issue posting or local resolver use;
- `GH_TOKEN` or the default `github.token` for issue posting and resolver operations in GitHub Actions.

Current Python runtime dependencies include:

```text
mkdocs-material==9.7.6
groq==1.4.0
google-genai>=2.8.0,<3.0.0
```

The operational provider secrets are:

```text
GROQ_API_KEY
GEMINI_API_KEY
```

The provider adapters use:

| Provider | Local/API environment variable behavior | GitHub Actions repository secret |
|---|---|---|
| `groq` | requires `GROQ_API_KEY` | `GROQ_API_KEY` |
| `gemini` | reads `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `GEMINI_API_KEY` |

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
- `GH_TOKEN`;
- `contents: read`;
- `issues: write`.

### Automated resolver workflow prerequisites

The automated resolver workflow depends on:

- repository checkout with full history;
- Python;
- dependencies from `requirements.txt`;
- `GROQ_API_KEY` when Groq is selected;
- `GEMINI_API_KEY` when Gemini is selected;
- `GH_TOKEN`/`GITHUB_TOKEN`;
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
issue-comment.md
issue-comment.invalid.md
```

The repository ignores these outputs with:

```text
.tmp/
issue-comment*.md
```

Resolver branches and pull requests are repository artifacts, not generated local output. They are intentionally created only when the resolver accepts at least one exact local edit and the deterministic page-structure check passes.

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
- empty required sections where the project expects placeholder text;
- `Generation and Review Log` table structure.

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

The expected `Generation and Review Log` table header is:

```markdown
| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
```

The checker validates that:

- the `Generation and Review Log` section starts with the expected 8-column table header;
- the header is followed by a valid 8-column Markdown separator row;
- all non-empty non-comment lines after the separator are table rows;
- each row has exactly eight cells;
- required cells are non-empty for `Date`, `Phase`, `Agent`, and `Action`;
- `Date` values use `YYYY-MM-DD`;
- `Phase` values match `Phase N`;
- bullet-style automated resolver log entries are not present outside the table.

This rule was added after automated resolver logs were briefly written as Markdown bullets after the table. The corrected structure is a table row inside the existing log table.

The checker may propose an exact structural repair, such as inserting a missing heading or rewriting the log section as a valid table, but it must not apply the repair.

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

When this marker is present, the checker suppresses empty-section signals and `Generation and Review Log` table-structure signals for that page. The checker still performs structural checks for required headings, heading levels, heading order, duplicate headings, and unexpected level-2 sections.

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

Workflow display name:

```text
Phase 2 page-structure check
```

Job name:

```text
Check stereotype page structure
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
| Supported active providers | `groq`, `gemini` |
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
| Supported active providers | `groq`, `gemini` |
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

Its validator location format is:

```text
Location: Section: "<nearest heading, or Document root if no heading applies>"; Fragment: "<exact affected fragment from the same location, maximum 160 characters>"
```

The current prompts ask models to keep `Location` fragments below 140 characters. The validator hard limit remains 160 characters.

It may include `current_text` and `proposed_text` only when the replacement is exact, contiguous, local, low-risk, meaning-preserving, and does not cross sentence, paragraph, heading, table-cell, or list-item boundaries.

When included, `current_text` and `proposed_text` must be emitted together, wrapped in double quotation marks, and escaped when necessary.

It must not include `current_text` or `proposed_text` for issues inside protected content.

The active `language-style-checker-v1.0.2` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

`run_check_agent.py` validates the output against the configured language-style contract. Invalid model output is written as `.invalid.md` and is not posted.

## Automated signal resolver

The automated signal resolver is implemented by:

```text
scripts/phase-2/resolve_signal_issue.py
```

Its scheduled workflow is:

```text
.github/workflows/phase-2-signal-resolver.yml
```

Its resolver prompts are:

```text
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.1.0.md
prompts/phase-2/resolve-language-style-signal-issue-v1.1.0.md
```

The resolver operates on only these agents:

```text
page-hygiene-checker
language-style-checker
```

It does not support `page-structure-checker`.

### Resolver issue selection

When no issue is supplied manually, the resolver selects the oldest open eligible issue for the supported resolver agents.

Eligibility requires the issue title to match:

```text
Check signal: <agent-slug>: <page-id>
```

with `<agent-slug>` equal to one of:

```text
page-hygiene-checker
language-style-checker
```

and `<page-id>` under:

```text
classes/<id>
relations/<id>
```

Manual workflow dispatch may provide an explicit issue number or issue URL.

### Resolver decision model

The resolver prompts return strict JSON only.

Every signal group receives one of:

```text
accept
reject_for_phase_2_automation
```

There is no `defer` decision in automated resolution. Cases that would previously have been deferred are classified as:

```text
reject_for_phase_2_automation
```

with a concrete reason.

Accepted groups must use:

```text
reason_code: in_scope_exact_edit
```

Accepted edits must include:

```text
current_text
proposed_text
rationale
```

Rejected groups must have an empty `edits` array.

The wrapper validates that accepted `current_text` values occur exactly once in the current reviewed page before applying the edit.

### Resolver accepted-change flow

When the plan contains accepted changes, the implemented flow is:

```text
read issue
→ read current reviewed page
→ call resolver prompt/provider
→ parse strict JSON
→ validate plan
→ apply exact local replacements
→ add Generation and Review Log table row
→ run page-structure checker on the modified page
→ create branch
→ commit changed page
→ push branch
→ open pull request
→ update PR branch by rebase
→ enable squash auto-merge
→ comment on source issue
→ close source issue as completed
→ GitHub later merges PR after required checks pass
```

The local pre-PR validation step runs:

```text
python scripts/phase-2/check_agents/page_structure_checker.py
```

against the modified page and refuses to create a PR if the report has `Signal count > 0`.

The PR branch naming pattern is:

```text
phase-2/auto-resolve-issue-<issue-number>
```

The commit message pattern is:

```text
fix(phase-2): resolve <agent> signals for issue #<issue-number>
```

The PR title pattern is:

```text
Resolve Phase 2 <agent> signals for issue #<issue-number>
```

### Resolver no-accepted-change flow

When no signal group is accepted, the resolver:

```text
read issue
→ read current reviewed page
→ call resolver prompt/provider
→ parse strict JSON
→ validate plan
→ write resolver plan artifact
→ comment on source issue
→ close source issue as not_planned
```

No branch, commit, pull request, or page edit is created.

### Resolver review-log row

Accepted automated edits create a `Generation and Review Log` table row with this structure:

```markdown
| <date> | Phase 2 | Phase 2 automated resolver | Signal resolution | <resolver-prompt-id> | <resolver-prompt-title> | GitHub issue #<issue-number> | Applied accepted <agent> signal edits through automated Phase 2 resolution; not a conceptual or source-faithfulness validation. |
```

Current resolver prompt metadata:

| Agent | Prompt ID | Prompt title |
|---|---|---|
| `page-hygiene-checker` | `resolve-page-hygiene-signal-issue-v1.1.0` | `Phase 2 automated resolver: page-hygiene signals v1.1.0` |
| `language-style-checker` | `resolve-language-style-signal-issue-v1.1.0` | `Phase 2 automated resolver: language-style signals v1.1.0` |

Legacy bullet-style resolver log entries are removed for the same issue when the resolver applies accepted edits.

### Resolver auto-merge behavior

The resolver enables squash auto-merge with:

```text
gh pr merge <pr-url> --repo <repo> --auto --squash --delete-branch
```

This means GitHub merges the PR only after required merge requirements are met.

The resolver also updates the PR branch before enabling auto-merge with:

```text
gh pr update-branch <pr-url> --repo <repo> --rebase
```

The source issue is closed after the resolver successfully creates the PR, updates the branch, enables auto-merge, and posts its closure comment. The source issue closure records that the Phase 2 resolution step is complete. It does not by itself prove that the PR has already merged.

### Resolver dry-run mode

Manual dispatch supports `dry_run: true`.

Dry-run mode:

- selects or reads the issue;
- calls the resolver LLM;
- parses and validates the JSON plan;
- writes the resolver plan artifact;
- prints the plan;
- does not modify files;
- does not create a branch;
- does not create a pull request;
- does not comment on or close the issue.

### Resolver workflow

The automated resolver workflow is:

```text
.github/workflows/phase-2-signal-resolver.yml
```

Workflow display name:

```text
Phase 2 automated signal resolver
```

Schedule:

```text
17 */4 * * *
```

This means it is scheduled every four hours at minute 17 UTC.

Manual dispatch inputs:

| Input | Purpose |
|---|---|
| `issue` | Issue number or URL. Empty means oldest eligible open issue. |
| `provider` | `gemini` or `groq`; default `gemini`. |
| `model` | Provider model; default `gemini-3.5-flash`. |
| `dry_run` | Generate and validate a resolution plan without GitHub writes. |

Workflow permissions:

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

Concurrency group:

```text
phase-2-automated-signal-resolver
```

with:

```text
cancel-in-progress: false
```

The workflow uploads resolver plan artifacts from:

```text
.tmp/phase-2/resolver
```

as:

```text
phase-2-resolver-plan
```

## LLM provider support

The active provider set in `run_check_agent.py` and the resolver is:

```text
groq
gemini
```

| Provider | Adapter | API key |
|---|---|---|
| `groq` | `scripts/phase-2/providers/groq.py` | `GROQ_API_KEY` |
| `gemini` | `scripts/phase-2/providers/gemini.py` | `GEMINI_API_KEY` in GitHub Actions; `GEMINI_API_KEY` or `GOOGLE_API_KEY` locally |

### Groq provider

Groq was the original provider for Phase 2 LLM check-agent generation.

The Groq adapter calls the Groq chat-completions API and uses:

```text
GROQ_API_KEY
```

The direct batch-runner defaults remain Groq-oriented:

```text
provider: groq
models: llama-3.3-70b-versatile,openai/gpt-oss-20b
```

`openai/gpt-oss-20b` is available through direct `run_check_batch.py` use and manual workflow dispatch when explicitly selected. It is not part of the current scheduled provider/model rotation.

### Gemini provider

The Gemini adapter is:

```text
scripts/phase-2/providers/gemini.py
```

It uses the Google GenAI SDK:

```python
from google import genai
from google.genai import types
```

It calls Gemini through:

```python
client.models.generate_content(...)
```

Current scheduled Gemini model:

```text
gemini-3.5-flash
```

`gemini-2.5-flash` remains supported by provider-level reduced-thinking configuration and may be selected manually, but it is not the current scheduled Gemini default.

Gemini runs should use:

```text
--max-completion-tokens 8000
```

The scheduled signal-collector workflow and the automated resolver use this automatically for Gemini when no manual completion-token value is supplied or when the resolver default is used.

The Gemini adapter includes reduced-thinking configuration for strict-format output reliability:

| Model family | Thinking configuration |
|---|---|
| `gemini-2.5-flash*` | `types.ThinkingConfig(thinking_budget=0)` |
| `gemini-3.*` | `types.ThinkingConfig(thinking_level="low")` |

This setting improves strict-format output reliability but does not replace validation.

For current Phase 2 automation, `gemini-3.5-flash` is the scheduled Gemini default. Other Gemini model names should not be added to the scheduled rotation unless they are first verified operationally and documented.

### Gemini retry behavior

The Gemini provider includes provider-level retry handling for transient provider/API failures.

The configured retry delays are:

```text
5 seconds
15 seconds
45 seconds
```

Current transient detection is marker-based and recognizes diagnostics containing values such as:

```text
429
500
502
503
504
rate_limit_exceeded
resource_exhausted
service_unavailable
temporarily unavailable
timeout
unavailable
```

Validation failures are not retried. A structurally invalid model output is treated as a rejected check-agent output or resolver failure, not as a transient provider failure.

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

Resolver decisions are not expert validation. They are automation decisions over Phase 2 signals and use this terminology:

```text
accept
reject_for_phase_2_automation
accepted_changes
no_accepted_changes
```

A signal rejected for Phase 2 automation is not necessarily false. It may be out of scope, source-dependent, obsolete, insufficiently deterministic, unsafe for automated edit application, duplicate, or otherwise unsuitable for Phase 2 automation.

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

For LLM-based check agents, the prompt target for `Location` fragments is stricter:

```text
maximum 140 characters
```

The validator hard acceptance limit remains:

```text
maximum 160 characters
```

The lower prompt target gives the model a safety margin while preserving the existing validator invariant.

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

## Validation and rejection policy

`run_check_agent.py` validates every generated LLM issue comment before accepting it as a candidate output.

Validation checks include:

- report title;
- required sections;
- metadata values;
- prompt ID;
- provider and model identity;
- signal count;
- allowed categories;
- severity and confidence values;
- signal ID sequence;
- required field order;
- `Location` format;
- hard 160-character `Location` fragment limit;
- no unresolved template placeholders;
- no copied explanatory prompt text;
- no forbidden task checkboxes;
- no out-of-scope source-validation claims;
- no recommendations to mutate repository or issue state.

If validation fails, `run_check_agent.py` writes an invalid artifact and exits nonzero.

The invalid artifact path uses `.invalid.md`, for example:

```text
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.invalid.md
```

`run_check_batch.py` can treat validation failures as nonfatal when this flag is used:

```text
--allow-rejected-check-outputs
```

When this flag is active:

- rejected outputs are kept as artifacts;
- rejected outputs are not sent to `issue_manager.py`;
- rejected outputs are not posted as issue comments;
- the batch can still exit successfully if no fatal automation failure occurs.

Provider failures, configuration failures, issue-manager failures, and resolver failures remain fatal unless handled by provider retry logic or by the relevant wrapper.

## Structured signal data

Machine-readable signal data is currently agent- and version-dependent.

Current status:

- `page-structure-checker` emits YAML blocks because its output is generated deterministically by Python;
- `page-hygiene-checker-v1.0.2` is Markdown-only;
- `language-style-checker-v1.0.2` is Markdown-only;
- automated resolver prompts emit strict JSON resolution plans;
- resolver plans are written under `.tmp/phase-2/resolver/`;
- machine-readable signal blocks for LLM-based check-agent comments are deferred to a later prompt version or later tooling.

The Markdown text is for humans and issue readability. Structured blocks and resolver JSON plans are infrastructure for deterministic tooling.

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

All provider/model outputs for the same page and same check agent are posted to the same open issue.

For example, if `page-hygiene-checker` runs with Groq and Gemini on `docs/stereotypes/classes/event.md`, both model reports are comments under:

```text
Check signal: page-hygiene-checker: classes/event
```

The issue manager currently searches only open issues with an exact matching title. Closed issues are not reused.

The automated resolver also requires this issue title pattern and currently selects only open issues for:

```text
page-hygiene-checker
language-style-checker
```

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

A direct `run_check_batch.py` invocation iterates over:

```text
pages × check agents × models
```

for one selected provider.

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

Common Groq example:

```bash
python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider groq \
  --model llama-3.3-70b-versatile \
  --mode generate
```

Common Gemini example:

```bash
export GEMINI_API_KEY="..."

python scripts/phase-2/run_check_batch.py \
  --page docs/stereotypes/classes/event.md \
  --agent page-hygiene-checker \
  --provider gemini \
  --model gemini-3.5-flash \
  --mode generate \
  --max-runs 1 \
  --max-completion-tokens 8000 \
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
| `--dry-run` | Generate and validate a plan without modifying files or writing to GitHub. |
| `--branch-prefix` | Branch prefix for accepted-change PRs; default `phase-2/auto-resolve`. |

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
13,43 * * * *
```

That means it is scheduled every 30 minutes, at minutes 13 and 43 UTC.

The workflow is also manually triggerable through `workflow_dispatch`.

Manual dispatch supports:

- `generate`, `dry-run`, or `post` mode;
- `groq` or `gemini` provider selection;
- comma-separated `models`;
- comma- or newline-separated `provider_model_specs`;
- comma- or newline-separated page lists;
- explicit `rotation_index`;
- explicit `max_completion_tokens`.

When `provider_model_specs` is supplied, it overrides the `provider` and `models` inputs.

Scheduled provider/model rotation:

```text
groq:llama-3.3-70b-versatile
gemini:gemini-3.5-flash
```

Effective scheduled defaults:

```text
mode: post
selection: rotate
rotation_seed: hourly
max_runs: 1
sleep_seconds: 0
agents: page-hygiene-checker,language-style-checker
provider/model rotation: groq:llama-3.3-70b-versatile, gemini:gemini-3.5-flash
pages: all canonical class and relation stereotype pages, excluding index.md
```

The workflow first rotates over provider/model specs, then delegates page/agent/model selection to `run_check_batch.py` with rotating selection.

The scheduled run therefore gradually rotates over page, agent, provider, and model combinations. It does not run the full matrix in one execution.

If a selected LLM output fails validation:

- the generated invalid output is saved as `.invalid.md`;
- `issue_manager.py` is not called for that output;
- artifacts are still uploaded;
- the workflow remains nonfatal for that rejection because it passes `--allow-rejected-check-outputs`;
- provider, configuration, and issue-manager failures remain fatal unless handled by retry logic.

### Automated resolver execution

The automated resolver runs periodically through:

```text
.github/workflows/phase-2-signal-resolver.yml
```

Workflow display name:

```text
Phase 2 automated signal resolver
```

It runs on this schedule:

```text
17 */4 * * *
```

That means it is scheduled every four hours at minute 17 UTC.

The workflow is also manually triggerable through `workflow_dispatch`.

Effective scheduled defaults:

```text
provider: gemini
model: gemini-3.5-flash
issue: oldest eligible open page-hygiene-checker or language-style-checker signal issue
dry_run: false
```

Manual dispatch can:

- resolve one explicit issue;
- select `gemini` or `groq`;
- select a provider model;
- run in dry-run mode.

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

- earlier successful GitHub Actions execution for `gemini-2.5-flash`; the current scheduled workflow selects `gemini-3.5-flash`;
- valid generated issue-comment structure after adding reduced-thinking configuration and increasing Gemini completion tokens;
- transient Gemini provider failures with `503 UNAVAILABLE`;
- validation rejections caused by overly long `Location` fragments before the prompt target was tightened from 160 characters to 140 characters.

Later operational updates added:

- automated signal issue resolution on a four-hour schedule;
- accepted resolver edits converted into pull requests;
- issue comments and issue closure for accepted and rejected automated resolver outcomes;
- PR branch update by rebase before auto-merge enablement;
- squash auto-merge after required checks pass;
- structured resolver log entries in the `Generation and Review Log` table;
- deterministic page-structure validation of the `Generation and Review Log` table.

These observations are not guarantees of future provider behavior. The committed workflows and scripts should be treated as authoritative for current automation behavior.

## Manual signal-review and issue-resolution prompt support

Phase 2 includes two manual ChatGPT prompts for reviewing and resolving check-agent signal issues:

```text
prompts/phase-2/close-page-hygiene-signal-issue-v1.0.0.md
prompts/phase-2/close-language-style-signal-issue-v1.0.0.md
```

These prompts are implemented for the two LLM-based check agents:

```text
page-hygiene-checker
language-style-checker
```

There is no current `page-structure-checker` closure prompt. The earlier plan for a third closure prompt was discarded. Page-structure signals should therefore be handled through direct maintainer review of the deterministic report, the referenced page, and the normal repository review process.

The two manual prompts help a human maintainer use ChatGPT to review one Phase 2 issue at a time. They support two stages:

1. read-only analysis and preparation;
2. optional GitHub mutation only after explicit human confirmation.

In the read-only stage, the prompts guide ChatGPT to:

1. validate the issue URL and repository;
2. read the issue body and all accessible comments;
3. verify attribution to the relevant check agent;
4. identify the reviewed page;
5. inspect the current reviewed page;
6. extract and group relevant check-agent signals;
7. classify each signal or signal group as `accept`, `reject`, or `defer`;
8. explain the decision for each signal or signal group;
9. prepare exact local edits, issue comments, branch names, commit messages, or pull-request material only when safe and in scope;
10. recommend whether the issue should remain open, receive a comment, be closed as not planned, or later be closed as completed after accepted edits have actually been applied.

The manual prompts require explicit human confirmation before any GitHub write action.

GitHub write actions include, but are not limited to:

- creating a branch;
- modifying repository files;
- creating a commit;
- opening a pull request;
- posting an issue comment;
- closing an issue;
- changing labels;
- changing assignees;
- changing milestones;
- changing issue titles.

The manual prompts remain useful as fallback tooling. The automated resolver is separate and uses strict JSON resolver prompts rather than these manual close prompts.

### Page-hygiene manual issue-resolution prompt

The page-hygiene manual issue-resolution prompt is:

```text
prompts/phase-2/close-page-hygiene-signal-issue-v1.0.0.md
```

It focuses on `page-hygiene-checker` signals.

It evaluates:

- visible reference-hygiene issues;
- Markdown-hygiene issues;
- encoding issues;
- Generation and Review Log hygiene.

It should not validate source content, infer missing source support, evaluate OntoUML correctness, or perform broad rewriting.

### Language-style manual issue-resolution prompt

The language-style manual issue-resolution prompt is:

```text
prompts/phase-2/close-language-style-signal-issue-v1.0.0.md
```

It focuses on `language-style-checker` signals in reader-facing prose.

It evaluates:

- grammar;
- spelling;
- clarity;
- professional technical style;
- project/process self-reference in reader-facing text.

It protects:

- direct quotations;
- citation locators;
- bibliographic entries;
- source titles;
- stereotype names;
- formal definitions;
- OntoUML claims;
- source interpretations;
- technical terminology when meaning could change.

## Automated resolver prompt support

Phase 2 includes two automated resolver prompts:

```text
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.1.0.md
prompts/phase-2/resolve-language-style-signal-issue-v1.1.0.md
```

These prompts are implemented for:

```text
page-hygiene-checker
language-style-checker
```

They are not manual chat prompts. They are consumed by:

```text
scripts/phase-2/resolve_signal_issue.py
```

They return strict JSON resolution plans and do not directly perform GitHub writes.

### Page-hygiene automated resolver prompt

The page-hygiene automated resolver prompt is:

```text
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.1.0.md
```

It may accept only deterministic, local, meaning-preserving editorial edits within the page-hygiene checker scope:

- visible reference hygiene;
- Markdown hygiene;
- encoding hygiene;
- Generation and Review Log hygiene.

It must reject conceptual validation, source-faithfulness validation, quote verification, citation-support assessment, cross-page consistency, broad rewrites, inferred bibliography data, and non-local changes for Phase 2 automation.

### Language-style automated resolver prompt

The language-style automated resolver prompt is:

```text
prompts/phase-2/resolve-language-style-signal-issue-v1.1.0.md
```

It may accept only deterministic, local, meaning-preserving editorial edits within the language-style checker scope:

- grammar;
- spelling;
- clarity;
- professional technical style;
- project/process self-reference in reader-facing prose.

It must reject conceptual validation, source-faithfulness validation, quote verification, citation-support assessment, cross-page consistency, citation/reference hygiene, Markdown hygiene, encoding hygiene, review-log hygiene, broad rewrites, and technical meaning changes for Phase 2 automation.

## Future work outside Phase 2

The following may be considered in later phases, but should not be required for Phase 2 completion:

- additional check agents;
- model quorum rules;
- signal deduplication across agents;
- semantic patch planning;
- source-faithfulness validation;
- heavy semantic analysis;
- cross-page consistency validation;
- OntoUML/UFO semantic validation;
- local/offline model integration;
- a stricter second workflow that closes source issues only after PR merge if issue-closure semantics are changed later.

A later pipeline may eventually be:

```text
check agents
→ signal issues
→ automated or manual resolution support
→ deterministic patching
→ verification checks
→ pull request
→ CI
→ merge
→ issue update or closure
```

The current Phase 2 implementation already includes a constrained version of this pipeline for low-risk exact local edits in LLM-based signal issues.

## Current migration status

Completed:

- Phase 2 methodology defines lightweight check-agent infrastructure;
- signal terminology is used by the current runners and issue manager;
- `page-structure-checker` exists as the deterministic Python check agent;
- `page-structure-checker` supports an explicit `<!-- skeleton-page -->` marker for intentional skeleton pages;
- `page-structure-checker` validates the `Generation and Review Log` table structure;
- `run_page_structure_batch.py` runs the deterministic page-structure checker across canonical stereotype pages;
- `.github/workflows/page-structure-check.yml` runs the page-structure checker in CI;
- the page-structure CI workflow uploads generated reports as artifacts and fails on structural signals;
- `page-hygiene-checker-v1.0.2` exists as a dedicated LLM check-agent prompt;
- `language-style-checker-v1.0.2` exists as a dedicated LLM check-agent prompt;
- `run_check_agent.py` runs the two LLM check agents through an agent-aware contract;
- `run_check_agent.py` supports Groq and Gemini provider adapters;
- `run_check_agent.py` validates generated LLM output and writes `.invalid.md` debugging files for invalid output;
- `run_check_batch.py` supports page × agent × model execution for one selected provider;
- `run_check_batch.py` supports rotating scheduled selection;
- `run_check_batch.py` can keep validation rejections nonfatal when `--allow-rejected-check-outputs` is used;
- `issue_manager.py` implements page-plus-agent issue routing;
- `issue_manager.py` implements stable comment identity;
- `issue_manager.py` updates matching existing comments instead of posting duplicates;
- `.github/workflows/check-agent-signal-collector.yml` runs scheduled rotating LLM check-agent collection;
- scheduled runs can create or update GitHub issues/comments in `post` mode;
- scheduled provider/model rotation includes `groq:llama-3.3-70b-versatile` and `gemini:gemini-3.5-flash`;
- Gemini uses `gemini-3.5-flash` as the current scheduled default;
- Gemini runs use `max_completion_tokens=8000` in the canonical workflow when no manual override is supplied;
- generated output paths are ignored by `.gitignore`;
- `close-page-hygiene-signal-issue-v1.0.0.md` exists as the manual issue-review and resolution prompt for `page-hygiene-checker` issues;
- `close-language-style-signal-issue-v1.0.0.md` exists as the manual issue-review and resolution prompt for `language-style-checker` issues;
- the earlier plan for a third `page-structure-checker` closure prompt has been discarded;
- `resolve-page-hygiene-signal-issue-v1.1.0.md` exists as the automated resolver prompt for `page-hygiene-checker` issues;
- `resolve-language-style-signal-issue-v1.1.0.md` exists as the automated resolver prompt for `language-style-checker` issues;
- `resolve_signal_issue.py` implements automated resolver orchestration;
- `.github/workflows/phase-2-signal-resolver.yml` runs scheduled and manual automated signal resolution;
- the automated resolver selects the oldest eligible open signal issue when no issue is provided;
- the automated resolver can run in dry-run mode;
- the automated resolver validates strict JSON plans;
- the automated resolver applies accepted exact local edits;
- the automated resolver writes accepted-edit provenance as a `Generation and Review Log` table row;
- the automated resolver removes legacy bullet-style automated resolver log lines for the same issue;
- the automated resolver runs the page-structure checker before creating a PR;
- the automated resolver creates PRs for accepted changes;
- the automated resolver updates PR branches by rebase;
- the automated resolver enables squash auto-merge;
- the automated resolver comments on and closes source signal issues;
- accepted automated resolver PRs for `language-style-checker` issues have been merged through the repository workflow.

Pending:

1. decide whether to keep or remove non-canonical support artifacts such as `providers/mock.py` and `.github/workflows/phase-2-check-agents.yml.bak`;
2. document any observed clean baseline with a dated run artifact rather than an undocumented local claim;
3. extend provider transient-error markers if future observed SDK diagnostics are not caught by the current marker list;
4. confirm whether the two manual issue-resolution prompts and two automated resolver prompts should remain directly under `prompts/phase-2/` or be moved into a dedicated subdirectory in a later cleanup;
5. decide whether source signal issues should remain closed after resolver completion or be closed only after PR merge through a separate `pull_request.closed` workflow;
6. update adjacent methodology pages if they still describe Phase 2 as excluding all automatic PR creation, issue closure, or auto-merge.

Deferred outside Phase 2:

- additional check agents beyond the three Phase 2 agents;
- source-faithfulness validation;
- heavy semantic analysis;
- cross-page consistency validation;
- OntoUML/UFO semantic validation;
- model quorum evaluation;
- semantic patch planning;
- local/offline model integration.

## Recommended next implementation steps

### Step 1 — Commit this methodology alignment

Update the canonical Phase 2 methodology page to reflect the current automated resolver and review-log table validation behavior.

Suggested commit message:

```bash
docs(phase-2): document automated signal resolution
```

### Step 2 — Align adjacent methodology pages

Review adjacent methodology pages for now-stale claims that Phase 2 excludes all automatic PR creation, automatic issue closure, or auto-merge.

Likely candidates:

```text
docs/methodology/generation-policy.md
docs/methodology/phases/index.md
```

Suggested commit message:

```bash
docs(methodology): align Phase 2 automation boundaries
```

### Step 3 — Clean up non-canonical Phase 2 support artifacts

Clarify, move to the archive, or remove non-canonical support artifacts if they are no longer needed.

Current candidates:

```text
.github/workflows/phase-2-check-agents.yml.bak
scripts/phase-2/providers/mock.py
```

Suggested commit message:

```bash
chore(phase-2): remove stale check-agent support artifacts
```

### Step 4 — Record a dated Phase 2 baseline

If a clean or representative run is observed or already available in GitHub Actions artifacts/issues, document it with a dated artifact or issue reference rather than relying on an undocumented local claim.

Suggested commit message:

```bash
docs(phase-2): record current check-agent baseline
```

### Step 5 — Decide issue-closure semantics

The current resolver closes the source signal issue after resolver completion. If the project later requires issue closure only after successful PR merge, add a separate workflow triggered by merged resolver PRs.

Suggested commit message if implemented later:

```bash
feat(phase-2): close resolved signal issues after merge
```

## Completion criteria

Phase 2 can be considered complete when:

- the simplified three-agent architecture is documented;
- `page-structure-checker` is implemented and runs after canonical stereotype page modifications;
- `page-structure-checker` validates the `Generation and Review Log` table structure;
- `page-hygiene-checker` is implemented as an LLM-based check agent and runs in conservative periodic batches;
- `language-style-checker` is implemented as an LLM-based check agent and runs in conservative periodic batches;
- issue routing is page-plus-agent based;
- outputs use signal terminology;
- generated comments are structured according to each agent contract and pass validation before posting;
- all provider/model outputs for the same page and agent are routed to the same issue;
- repeated runs update existing comments when the stable identity is unchanged;
- generated outputs remain uncommitted;
- small batch execution works locally;
- page-structure CI blocks structural regressions;
- conservative scheduled LLM execution works with Groq and Gemini;
- the two manual issue-review and resolution prompts for the LLM-based agents exist and are documented;
- the absence of a dedicated `page-structure-checker` closure prompt is documented as intentional;
- the two automated resolver prompts for LLM-based signal issues exist and are documented;
- the automated resolver can select eligible issues, validate strict JSON plans, apply accepted exact edits, reject unsafe or out-of-scope signals for automation, create PRs, enable squash auto-merge, and close source signal issues;
- the repository permissions and branch-protection settings allow the automated resolver workflow to complete its intended path.

## Generation and review log

- Phase 2 revised from a broader check-and-future-resolution architecture into a simplified lightweight check-agent infrastructure.
- The simplified Phase 2 target has exactly three check agents: one deterministic Python agent and two LLM-based agents.
- The deterministic Python agent is `page-structure-checker`.
- The two LLM-based agents are `page-hygiene-checker` and `language-style-checker`.
- The `page-structure-checker` runs after canonical stereotype page modifications and blocks structural regressions in CI.
- The `page-structure-checker` now validates the `Generation and Review Log` table schema.
- The two LLM-based check agents run periodically through the scheduled rotating workflow.
- The active LLM providers are `groq` and `gemini`.
- Gemini support is documented inline in this Phase 2 page rather than split into a separate provider-only methodology page.
- The current scheduled Gemini model for Phase 2 check-agent automation is `gemini-3.5-flash`.
- The scheduled provider/model rotation includes `groq:llama-3.3-70b-versatile` and `gemini:gemini-3.5-flash`.
- Gemini runs use a larger completion-token budget and reduced-thinking configuration to improve strict-format output reliability.
- The prompts target 140-character `Location` fragments while the validator hard limit remains 160 characters.
- Issue routing is one GitHub issue per page and check agent.
- Different providers and models executed by the same agent for the same page create comments in the same issue.
- Stable comment identity is implemented with page, agent, provider, model, prompt, and commit.
- Matching existing comments are updated instead of duplicated.
- Manual signal-review and issue-resolution support is documented for `page-hygiene-checker` and `language-style-checker` through two ChatGPT prompts.
- The planned `page-structure-checker` closure prompt was discarded; deterministic page-structure signals remain subject to direct maintainer review.
- Automated signal resolution is implemented for `page-hygiene-checker` and `language-style-checker` issues.
- Automated resolver prompts return strict JSON plans and classify non-accepted cases as `reject_for_phase_2_automation`.
- Accepted automated resolver edits must be exact local replacements and pass deterministic validation.
- Accepted automated resolver edits are logged as rows in the `Generation and Review Log` table.
- Automated resolver PRs are updated by rebase and configured for squash auto-merge after required checks pass.
- Automated resolver source issues are commented on and closed after resolver completion.
- Conceptual validation, source-faithfulness validation, cross-page semantic comparison, and OntoUML/UFO semantic validation remain outside Phase 2.
