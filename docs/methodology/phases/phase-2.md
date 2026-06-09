# Phase 2 — Lightweight Check-Agent Infrastructure

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its purpose is to introduce lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages. Phase 2 does not perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, automatic page repair, pull-request generation, or automatic issue closure.

Phase 2 produces page-local **signals**, routes those signals to deterministic GitHub issues, and provides manual ChatGPT-assisted prompts for closing those issues later.

Phase 2 follows a gradual automation model: small checks, small batches, conservative execution, and incremental accumulation of signals over time. The intended operating philosophy is _de grão em grão_: progress should come from many small, cheap, repeatable checks rather than infrequent heavyweight analyses.

## Purpose

Phase 2 has six goals:

1. implement three lightweight check agents for canonical stereotype pages;
2. run the deterministic Python check agent on page modifications;
3. run the two LLM-based check agents periodically in conservative batches;
4. produce structured, page-local signals about page structure, page hygiene, formatting, and writing quality;
5. route check-agent outputs to deterministic GitHub issues scoped by page and check agent;
6. provide manual ChatGPT prompts that help a human evaluate, resolve, and close Phase 2 signal issues.

Phase 2 prioritizes infrastructure, signal quality, traceability, repeatability, and controlled issue routing over deep content judgment.

## Simplified Phase 2 boundary

Phase 2 implements:

```text
check agents
→ check-agent execution
→ issue routing
→ manual issue-closure prompt support
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

- reads check-agent reports;
- derives the reviewed page identity;
- derives the check-agent identity;
- creates or reuses one GitHub issue per page and check agent;
- posts model-specific check-agent reports as comments in that issue;
- should update matching comments instead of creating duplicate comments once stable comment identity is implemented.

Manual issue-closure prompts:

- are planned Phase 2 documentation artifacts;
- are intended for use with ChatGPT by a human maintainer;
- help evaluate the signals in one issue;
- help decide whether the issue should be closed as completed, closed as not planned, or left open;
- do not run automatically;
- do not replace human judgment.

## Target Phase 2 architecture

Phase 2 should contain exactly three check agents:

```text
check-agents
├── page-structure-checker
├── page-hygiene-checker
└── language-style-checker
```

The target execution model is:

```text
page-structure-checker
└── deterministic Python
└── runs after canonical stereotype page modifications
└── blocks structural regressions in CI

page-hygiene-checker
└── LLM-based
└── runs periodically in conservative batches
└── reports page-hygiene signals

language-style-checker
└── LLM-based
└── runs periodically in conservative batches
└── reports language/style signals
```

The target issue-routing model is:

```text
one GitHub issue per page + check agent
```

Different models executed by the same agent for the same page must post comments in the same issue.

Examples:

```text
Phase 2 check: page-structure-checker: classes/event
Phase 2 check: page-hygiene-checker: classes/event
Phase 2 check: language-style-checker: classes/event
```

If `page-hygiene-checker` runs with multiple LLM models on `classes/event`, all those model outputs belong in:

```text
Phase 2 check: page-hygiene-checker: classes/event
```

## Current implementation status

The current implementation provides a working local and CI-based Phase 2 foundation, but it does not yet fully implement the simplified target architecture.

### Implemented files and artifacts

```text
.github/workflows/page-structure-check.yml
prompts/phase-2/page-hygiene-checker-v1.0.2.md
prompts/phase-2/language-style-checker-v1.0.2.md
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_review_batch.py
scripts/phase-2/run_page_structure_batch.py
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/mock.py
```

Legacy compatibility artifacts also exist or are referenced by the current runner:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
```

The legacy general page-reviewer prompt is not part of the simplified target architecture. It should be replaced or parameterized before relying on real agent-specific LLM runs.

### Current capabilities

The current implementation can:

- run one general page-level LLM check at a time through `run_page_review.py`;
- use signal terminology in generated comments, validation, mock output, batch output, and issue-manager parsing;
- call Groq models through the Groq provider adapter;
- run a deterministic mock provider for smoke testing;
- run the standalone Python-based `page-structure-checker` for deterministic page-skeleton checks;
- provide dedicated LLM prompt contracts for `page-hygiene-checker-v1.0.2` and `language-style-checker-v1.0.2`;
- write local Markdown candidate signal comments;
- normalize safe Markdown/template issues;
- validate generated signal comments for structure and safety;
- read generated comment files;
- derive deterministic page-level GitHub issue titles;
- create or reuse GitHub issues through local `issue_manager.py`;
- post generated signal comments to GitHub issues through local `issue_manager.py`;
- read a YAML batch configuration for the existing page/model-oriented runner;
- run configured page/model batches through the existing batch runner;
- run `page-structure-checker` across all canonical stereotype pages through `run_page_structure_batch.py`;
- exclude stereotype `index.md` pages from page-structure batch execution;
- mark intentional skeleton pages with `<!-- skeleton-page -->`;
- suppress empty-section signals for explicitly marked skeleton pages;
- run page-structure checks in GitHub Actions on changed canonical stereotype pages;
- upload page-structure check reports as GitHub Actions artifacts;
- fail CI when page-structure signals are reported.

### Current clean baseline

The latest local execution of `run_page_structure_batch.py` over all canonical stereotype pages reported:

```text
Pages processed: 39
Checker failures: 0
Pages with structural signals: 0
Issue-manager runs: 0
Issue-manager failures: 0
```

This means the deterministic page-structure checker currently has a clean baseline across all canonical stereotype pages.

### Current limitations

The current implementation does **not** yet match the simplified target architecture. In particular:

- issue routing is still page-level, not page-plus-agent;
- repeated local issue-posting runs still post new comments rather than updating matching comments;
- `run_review_batch.py` is still page/model oriented, not page/check-agent/model oriented;
- `page-structure-checker` is implemented and has a dedicated local batch runner, but it is not integrated into a unified agent-aware runner;
- `page-hygiene-checker-v1.0.2` exists as a standalone prompt but is not yet wired into an agent-aware runner or batch configuration;
- `language-style-checker-v1.0.2` exists as a standalone prompt but is not yet wired into an agent-aware runner or batch configuration;
- GitHub Actions currently run the deterministic page-structure checker only;
- GitHub Actions do not create or update GitHub issues;
- scheduled LLM execution is still pending;
- automatic issue creation and comment updates from scheduled runs are still pending;
- the three manual issue-closure prompts are planned but have not yet been created.

## Operational prerequisites

The current local implementation depends on:

- Python;
- `pyyaml` for the batch configuration;
- `groq` for Groq API calls;
- a `GROQ_API_KEY` environment variable for real Groq runs;
- GitHub CLI authentication through `gh auth login` for local issue posting;
- `GH_TOKEN` later if issue-posting workflows run in GitHub Actions.

The Groq API key must never be committed.

The current page-structure GitHub Actions workflow depends only on:

- repository checkout;
- Python;
- the deterministic checker script;
- read-only repository contents permission.

It does not require secrets, issue permissions, or write permissions.

Scheduled LLM workflows will require:

- a model-provider API key, such as `GROQ_API_KEY`;
- issue write permissions if the workflow creates issues or comments;
- duplicate-control logic before routine posting is enabled.

## Generated output policy

Generated Phase 2 outputs are not source files and must not be committed.

Generated local outputs include paths such as:

```text
.tmp/phase-2/<page-id>/issue-comment-<provider>-<model>.md
.tmp/phase-2/page-structure-checker/<page-id>/issue-comment-page-structure-checker.md
issue-comment.md
issue-comment.invalid.md
```

The repository should continue to ignore these outputs with:

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
| Implementation status | Implemented as a standalone script, local batch runner, and CI workflow |
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

Current intentionally marked skeleton page:

```text
docs/stereotypes/classes/historical-role-mixin.md
```

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

The `--post` mode should be used conservatively until `issue_manager.py` supports page-plus-agent routing and stable comment updates.

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

A negative-control pull request should be used to verify that the branch rule blocks merges when the workflow fails.

### 2. Page Hygiene Checker

| Property | Value |
|---|---|
| Agent slug | `page-hygiene-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Prompt implemented; runner integration pending |
| Prompt | `prompts/phase-2/page-hygiene-checker-v1.0.2.md` |
| Output | Structured Markdown signal comment |
| Applies changes | No |
| Target execution | Periodic conservative batches |

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

The current `page-hygiene-checker-v1.0.2` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

### 3. Language Style Checker

| Property | Value |
|---|---|
| Agent slug | `language-style-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Prompt implemented; runner integration pending |
| Prompt | `prompts/phase-2/language-style-checker-v1.0.2.md` |
| Output | Structured Markdown signal comment |
| Applies changes | No |
| Target execution | Periodic conservative batches |

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

The checker must not flag project/process references when they occur outside reader-facing prose, including:

- YAML or TOML front matter;
- code blocks;
- HTML comments;
- generation logs;
- review logs;
- source metadata;
- bibliography or reference sections;
- citation/source tables;
- changelog sections;
- explicitly marked process/history sections.

It must protect:

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

It must not:

- validate source support;
- validate citation correctness;
- evaluate OntoUML correctness;
- evaluate conceptual adequacy;
- compare pages;
- change OntoUML claims;
- strengthen or weaken conceptual claims;
- add new technical precision;
- remove necessary caution;
- modify source interpretation;
- rewrite whole sections;
- recommend repository operations.

The current `language-style-checker-v1.0.2` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

For no-signal runs, the prompt still requires a full comment with `Signal count` set to `0` and the exact no-signal sentence under `### Signals`.

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

Recommended heading:

```markdown
## Check signal report: <agent> / <provider> / <model> — <review date>
```

Recommended metadata table:

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

For LLM-based check agents, `Signal count` should exactly match the number of emitted `#### S-...` signal sections.

Recommended summary section:

```markdown
### Summary judgment

<agent-specific summary sentence>
```

Recommended scope section:

```markdown
### Scope

<agent-specific scope statement>
```

Recommended signal section:

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

For `language-style-checker-v1.0.2`, `current_text` and `proposed_text` are forbidden for issues inside protected content. When they are included, values must be double-quoted and exact, local, meaning-preserving text spans.

If no signals are identified, use exactly:

```markdown
### Signals

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

The target Phase 2 issue routing model is one GitHub issue per:

```text
page + check agent
```

Recommended issue title pattern:

```text
Phase 2 check: <agent-slug>: <page-id>
```

Examples:

```text
Phase 2 check: page-structure-checker: classes/event
Phase 2 check: page-hygiene-checker: classes/event
Phase 2 check: language-style-checker: classes/event
Phase 2 check: page-structure-checker: relations/material
```

The page identity is derived from the reviewed page path:

```text
docs/stereotypes/classes/event.md -> classes/event
docs/stereotypes/relations/material.md -> relations/material
```

All model outputs for the same page and same check agent should be posted to the same issue.

For example, if `page-hygiene-checker` runs with two models on `docs/stereotypes/classes/event.md`, both model reports should be comments under:

```text
Phase 2 check: page-hygiene-checker: classes/event
```

Current status: `issue_manager.py` still uses the older page-level issue title pattern:

```text
Phase 2 page review: <group>/<stereotype-id>
```

Changing issue routing to page-plus-agent is the next major implementation step.

## Issue body pattern

Recommended issue body:

```markdown
# Phase 2 check: <agent-slug>: <page-id>

## Reviewed page

`<docs/stereotypes/...>.md`

## Page identity

`<group>/<stereotype-id>`

## Check agent

`<agent-slug>`

## Purpose

Collect Phase 2 check-agent signals for this page and agent.

## Resolution model

This issue is resolved manually with the aid of the corresponding Phase 2 issue-closure prompt.

Signals are candidate observations. They are not accepted findings until reviewed.
```

## Comment identity and duplicate control

Before repeated or scheduled issue posting, Phase 2 should support stable comment identity.

Recommended stable identity:

```text
page
agent
provider
model
prompt
commit SHA
```

If a comment with the same stable identity already exists, the system should update the existing comment instead of posting a new one.

If the commit SHA changes, a new comment may be posted because the page content may have changed.

This is required before scheduled LLM execution or automated issue posting to prevent issue-comment noise.

The current page-structure CI workflow intentionally avoids GitHub issue/comment creation until this duplicate-control layer exists.

## Batch execution model

The current general batch runner is page/model oriented.

The new `run_page_structure_batch.py` runner is agent-specific and supports one deterministic check agent:

```text
page-structure-checker
```

The target batch model should iterate over:

```text
pages × check agents × models
```

For deterministic Python agents, the provider/model fields can be:

```text
provider: python
model: deterministic
```

For LLM agents, the provider/model fields should identify the API provider and model.

Example target configuration:

```yaml
repo: pedropaulofb/ontouml-according-to-the-machines
output_dir: .tmp/phase-2
delay_seconds: 60
continue_on_error: true
post_mode: after_agent
post_empty: false

agents:
  - slug: page-structure-checker
    type: python
    provider: python
    model: deterministic
    execution: on_page_modification

  - slug: page-hygiene-checker
    type: llm
    prompt: page-hygiene-checker-v1.0.2
    provider: groq
    execution: scheduled
    models:
      - model: openai/gpt-oss-20b
        slug: gpt-oss-20b
        max_completion_tokens: 3000

  - slug: language-style-checker
    type: llm
    prompt: language-style-checker-v1.0.2
    provider: groq
    execution: scheduled
    models:
      - model: openai/gpt-oss-20b
        slug: gpt-oss-20b
        max_completion_tokens: 3000

pages:
  - docs/stereotypes/classes/event.md
```

The concrete schema may evolve, but the conceptual shift should be from:

```text
page × model
```

to:

```text
page × check agent × model
```

## Execution policy

### Page-structure execution

The deterministic `page-structure-checker` should run when canonical stereotype pages are modified.

This check should remain CI-oriented and blocking:

- it should run on relevant pull requests;
- it should run on relevant pushes to `main`;
- it should be manually triggerable;
- it should upload reports as artifacts;
- it should fail when structural signals are reported;
- it should not create GitHub issues from CI until issue routing and duplicate control are stable.

### LLM-agent execution

The two LLM-based agents should run periodically in conservative batches:

```text
page-hygiene-checker
language-style-checker
```

Initial scheduled execution should be deliberately small:

```text
one or a few pages
one LLM check agent
one lightweight model
large interval between runs
```

After the issue manager supports page-plus-agent routing and duplicate-control updates, scheduled runs may post results to GitHub issues.

LLM scheduled execution should avoid:

- reviewing all pages too frequently;
- using expensive models by default;
- creating issues for zero-signal runs unless there is a specific reason;
- posting duplicate comments for the same page, agent, provider, model, prompt, and commit SHA.

## Free-model and slow-automation strategy

Phase 2 should be designed to work within free or low-cost model quotas.

The intended strategy is:

- keep prompts compact;
- cap outputs to a small number of signals;
- run few pages per batch;
- use lightweight models more often;
- use deterministic Python whenever possible;
- spread execution over time;
- avoid heavyweight models in Phase 2;
- rely on gradual accumulation rather than large one-shot reviews.

This supports a slow continuous process: small page batches can run with delays between pages or agents, allowing the project to accumulate signals incrementally.

## GitHub Actions and branch protection policy

The current page-structure GitHub Actions workflow is CI-only.

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

After branch protection is configured, a negative-control pull request should be created to verify that:

- the workflow fails when a canonical stereotype page has a structural defect;
- the failing required status check blocks merging;
- the report artifact is uploaded and inspectable.

## Scheduling policy

Scheduled execution applies to the two LLM-based check agents:

```text
page-hygiene-checker
language-style-checker
```

Scheduled execution is not the first implementation step. It should wait until:

1. agent-aware issue routing is implemented;
2. stable comment identity and update-existing behavior are implemented;
3. both LLM prompts are wired into agent-aware execution;
4. duplicate issue-comment posting is controlled;
5. lightweight model quotas are understood;
6. generated signals are consistently structured.

Once those gates are satisfied, the initial schedule should be conservative.

Recommended starting point:

```text
one page
one LLM check agent
one lightweight model
large delay between runs
```

Later, scheduling may expand page by page.

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
- signal terminology is used in the current runner, mock provider, issue manager, and batch runner;
- `page-structure-checker` exists as the deterministic Python check agent;
- `page-structure-checker` supports an explicit `<!-- skeleton-page -->` marker for intentional skeleton pages;
- `run_page_structure_batch.py` runs the deterministic page-structure checker across all canonical stereotype pages;
- the repository has a clean page-structure baseline across 39 canonical stereotype pages;
- `.github/workflows/page-structure-check.yml` runs the page-structure checker in CI;
- the CI workflow uploads generated reports as artifacts and fails on structural signals;
- `page-hygiene-checker-v1.0.2` exists as the first dedicated LLM check-agent prompt;
- `language-style-checker-v1.0.2` exists as the second dedicated LLM check-agent prompt.

Pending:

1. verify branch protection with a negative-control pull request;
2. implement agent-aware issue routing;
3. implement stable comment identity and update-existing behavior;
4. add runner and batch support for page/check-agent/model execution;
5. wire `page-hygiene-checker-v1.0.2` into agent-aware local execution;
6. wire `language-style-checker-v1.0.2` into agent-aware local execution;
7. run small local agent-aware batches before issue posting;
8. enable issue creation/update based on check-agent results;
9. add conservative scheduled execution for the two LLM-based agents;
10. add the three manual issue-closure prompts.

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

## Recommended implementation steps

### Step 1 — Keep the current page-structure checker and CI workflow

The current deterministic checker and workflow already match the simplified Phase 2 model.

Keep:

```text
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/run_page_structure_batch.py
.github/workflows/page-structure-check.yml
```

The workflow should continue to run after canonical stereotype page modifications and should continue to fail on structural signals.

### Step 2 — Verify branch protection and blocking behavior

Create a negative-control pull request that deliberately introduces a structural defect and verify that:

- the page-structure workflow fails;
- the required status check blocks merging;
- the artifact contains the generated signal report.

Commit message for the temporary test branch may be:

```bash
test: trigger page-structure check failure
```

The test branch should be reverted or closed after validation.

### Step 3 — Implement agent-aware issue routing

Change deterministic issue titles from page-only routing to page-plus-agent routing.

From:

```text
Phase 2 page review: classes/event
```

To:

```text
Phase 2 check: page-structure-checker: classes/event
Phase 2 check: page-hygiene-checker: classes/event
Phase 2 check: language-style-checker: classes/event
```

Commit message:

```bash
feat(phase-2): route check signals by page and agent
```

### Step 4 — Add stable comment identity and update-existing behavior

Modify issue posting so repeated runs update matching comments instead of always posting new comments.

Stable identity:

```text
page + agent + provider + model + prompt + commit SHA
```

Commit message:

```bash
feat(phase-2): update existing check signal comments
```

### Step 5 — Wire LLM check-agent prompts into execution

The page-hygiene checker prompt exists:

```text
prompts/phase-2/page-hygiene-checker-v1.0.2.md
```

The language-style checker prompt exists:

```text
prompts/phase-2/language-style-checker-v1.0.2.md
```

Next, wire both prompts into agent-aware local execution.

Commit messages:

```bash
feat(phase-2): run page hygiene checker as agent
feat(phase-2): run language style checker as agent
```

### Step 6 — Update batch configuration

Move the batch config from page/model execution to page/check-agent/model execution.

Commit message:

```bash
feat(phase-2): configure agent-aware check batches
```

### Step 7 — Run small local agent-aware batches

Begin with:

```text
one page
page-structure-checker
no posting
```

Then:

```text
one page
page-hygiene-checker
one lightweight model
no posting
```

Then:

```text
one page
language-style-checker
one lightweight model
no posting
```

Only then enable issue posting.

### Step 8 — Enable issue creation and comment updates

Once local execution is stable, enable the issue manager to create or reuse page-plus-agent issues and post or update check-agent comments.

The issue manager should:

- create one issue per page and agent;
- reuse existing open issues with the same title;
- skip zero-signal reports unless explicitly configured to post them;
- update an existing matching comment when the stable identity already exists;
- post a new comment when the stable identity is new.

### Step 9 — Add conservative scheduled execution for LLM agents

After duplicate control exists, add scheduled execution for:

```text
page-hygiene-checker
language-style-checker
```

Initial schedule should run only a very small batch.

Commit message:

```bash
ci(phase-2): schedule lightweight check-agent batch
```

### Step 10 — Add manual issue-closure prompts

Add three prompt files:

```text
prompts/phase-2/issue-closure/close-page-structure-signal-issue.md
prompts/phase-2/issue-closure/close-page-hygiene-signal-issue.md
prompts/phase-2/issue-closure/close-language-style-signal-issue.md
```

Commit message:

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
- generated comments are structured according to each agent contract and pass validation;
- all model outputs for the same page and agent are routed to the same issue;
- repeated runs update existing comments rather than creating duplicates;
- generated outputs remain uncommitted;
- small batch execution works locally;
- page-structure CI blocks structural regressions;
- conservative scheduled LLM execution works after duplicate-comment control exists;
- three manual issue-closure prompts exist for human/ChatGPT-assisted issue resolution.

## Generation and review log

- Phase 2 revised from a broader check-and-future-resolution architecture into a simplified lightweight check-agent infrastructure.
- The simplified Phase 2 target has exactly three check agents: one deterministic Python agent and two LLM-based agents.
- The deterministic Python agent is `page-structure-checker`.
- The two LLM-based agents are `page-hygiene-checker` and `language-style-checker`.
- The `page-structure-checker` should run after canonical stereotype page modifications and block structural regressions in CI.
- The two LLM-based check agents should run periodically in conservative batches.
- Issue routing should be one GitHub issue per page and check agent.
- Different models executed by the same agent for the same page should create comments in the same issue.
- Manual issue closure has been added to the Phase 2 target as a new documentation-supported activity.
- The planned issue-closure support consists of three ChatGPT prompts, one per check agent.
- The manual issue-closure prompts are planned but not created in this document update.
- Resolution agents, quorum decisions, patch planning, patch application, PR creation, automatic issue closure, and auto-merge are outside the simplified Phase 2 scope.
