# Phase 2 — Lightweight Check-Agent Infrastructure

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its purpose is to introduce lightweight, API-based and deterministic review infrastructure for existing canonical stereotype pages. Phase 2 does not perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, or page repair. It produces structured, page-local **signals** that can later be evaluated, resolved, and transformed into edits by Phase 3 tooling.

Phase 2 follows a gradual automation model: small checks, small batches, conservative scheduling, and incremental accumulation of signals over time. The intended operating philosophy is _de grão em grão_: progress should come from many small, cheap, repeatable checks rather than infrequent heavyweight analyses.

## Purpose

Phase 2 has six goals:

1. introduce API-based LLM execution into the project in a controlled and lightweight way;
2. introduce deterministic Python check agents where LLMs are unnecessary;
3. produce structured, page-local signals about documentation structure, hygiene, formatting, and writing quality;
4. route signals to deterministic GitHub issues scoped by page and check agent;
5. support small repeated executions over time without depending on expensive or heavyweight models;
6. prepare the repository for Phase 3 resolution, planning, patching, and verification agents.

Phase 2 prioritizes infrastructure, signal quality, traceability, and repeatability over deep content judgment.

## Core phase boundary

Phase 2 implements **check agents** only.

Check agents:

- inspect one canonical stereotype page at a time;
- produce lightweight structured signals;
- may suggest a repair or replacement when the repair is exact and local;
- must not modify canonical documentation pages;
- must not commit changes;
- must not open pull requests;
- must not decide that a signal is accepted or rejected;
- must not perform heavy semantic or source validation.

Resolution agents are deferred to Phase 3.

Resolution agents will later:

- read open check issues;
- evaluate collected signals;
- vote on whether a signal should be fixed;
- produce decision records;
- plan exact changes;
- trigger deterministic patch appliers;
- verify resulting pages;
- close or update issues according to explicit automation rules.

## Current implementation status

The current implementation provides a working local Phase 2 foundation:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
prompts/phase-2/page-hygiene-checker-v1.0.0.md
prompts/phase-2/language-style-checker-v1.0.0.md
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_review_batch.py
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/mock.py
```

The current implementation can:

- run one general page-level check at a time through `run_page_review.py`;
- use signal terminology in generated comments, validation, mock output, batch output, and issue-manager parsing;
- call Groq models through the Groq provider adapter;
- run a deterministic mock provider for smoke testing;
- run the standalone Python-based `page-structure-checker` for deterministic page-skeleton checks;
- provide dedicated LLM prompt contracts for `page-hygiene-checker-v1.0.0` and `language-style-checker-v1.0.0`;
- write local Markdown candidate signal comments;
- normalize safe Markdown/template issues;
- validate generated signal comments for structure and safety;
- read generated comment files;
- derive deterministic page-level GitHub issue titles;
- create or reuse GitHub issues;
- post generated signal comments to GitHub issues;
- read a YAML batch configuration;
- run configured page/model batches;
- write generated outputs under `.tmp/phase-2/`.

The current implementation does **not** yet match the final Phase 2 architecture. In particular:

- issue routing is still page-level, not page-plus-agent;
- repeated runs still post new comments rather than updating matching comments;
- the batch runner is still page/model oriented, not page/check-agent/model oriented;
- `page-structure-checker` exists as a standalone script but is not yet integrated into the batch runner;
- `page-hygiene-checker-v1.0.0` exists as a standalone prompt but is not yet wired into an agent-aware runner or batch configuration;
- `language-style-checker-v1.0.0` exists as a standalone prompt but is not yet wired into an agent-aware runner or batch configuration;
- manual GitHub Actions execution is still pending;
- scheduled execution is still pending.

The general `run_page_review.py` runner has been migrated to check-signal validation, but it still points to the legacy general page-reviewer prompt:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
```

That prompt is retained for compatibility and should be replaced or parameterized before relying on real agent-specific LLM runs through the general runner.

## Operational prerequisites

The current local implementation depends on:

- Python;
- `pyyaml` for the batch configuration;
- `groq` for Groq API calls;
- a `GROQ_API_KEY` environment variable for real Groq runs;
- GitHub CLI authentication through `gh auth login` for local issue posting;
- `GH_TOKEN` later when the same issue-posting workflow runs in GitHub Actions.

The Groq API key must never be committed.

## Generated output policy

Generated Phase 2 outputs are not source files and must not be committed.

Generated local outputs include paths such as:

```text
.tmp/phase-2/<page-id>/issue-comment-<provider>-<model>.md
issue-comment.md
issue-comment.invalid.md
```

The repository should continue to ignore these outputs with:

```text
.tmp/
issue-comment*.md
```

## Phase 2 agent model

Phase 2 distinguishes two top-level agent types, but only the first type is implemented during Phase 2.

```text
Check agents
└── implemented in Phase 2

Resolution agents
└── deferred to Phase 3
```

### Check agents

Check agents produce lightweight page-local signals. They do not apply changes.

Phase 2 should implement three check agents:

```text
check-agents
├── page-structure-checker
├── page-hygiene-checker
└── language-style-checker
```

### Resolution agents

Resolution agents process check-agent signals. They are deferred to Phase 3.

Potential Phase 3 resolution-agent roles include:

```text
resolution-agents
├── signal-deduplicator
├── signal-evaluator
├── change-planner
└── verification-reviewer
```

These roles may be implemented as separate agents or as stages in a single resolution pipeline.

## Phase 2 check agents

### 1. Page Structure Checker

| Property | Value |
|---|---|
| Agent slug | `page-structure-checker` |
| Type | Deterministic Python |
| LLM required | No |
| Phase | 2 |
| Implementation status | Implemented as a standalone script |
| File | `scripts/phase-2/check_agents/page_structure_checker.py` |
| Provider metadata | `python` |
| Model metadata | `deterministic` |
| Prompt metadata | `n/a` |
| Output | Structured signals |
| Applies changes | No |

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

The checker may propose an exact structural repair, such as inserting a missing heading, but it must not apply the repair. It reports `Agent: page-structure-checker`, `Provider: python`, `Model: deterministic`, and `Prompt: n/a`.

### 2. Page Hygiene Checker

| Property | Value |
|---|---|
| Agent slug | `page-hygiene-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Prompt implemented; runner integration pending |
| Prompt | `prompts/phase-2/page-hygiene-checker-v1.0.0.md` |
| Output | Structured Markdown signal comment |
| Applies changes | No |

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

The current `page-hygiene-checker-v1.0.0` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

### 3. Language Style Checker

| Property | Value |
|---|---|
| Agent slug | `language-style-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Prompt implemented; runner integration pending |
| Prompt | `prompts/phase-2/language-style-checker-v1.0.0.md` |
| Output | Structured Markdown signal comment |
| Applies changes | No |

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

The current `language-style-checker-v1.0.0` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

For no-signal runs, the prompt still requires a full comment with `Signal count` set to `0` and the exact no-signal sentence under `### Signals`.

## Explicitly excluded Phase 2 checks

Phase 2 does not currently include a Caution Language Checker.

The following are deferred to Phase 3:

- conceptual adequacy analysis;
- source-faithfulness analysis;
- comparison with original papers or PDFs;
- cross-page consistency analysis;
- OntoUML/UFO semantic validation;
- claim acceptance or rejection;
- automatic page rewriting;
- pull-request generation;
- patch application;
- issue closing based on accepted fixes.

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

For `language-style-checker-v1.0.0`, `current_text` and `proposed_text` are forbidden for issues inside protected content. When they are included, values must be double-quoted and exact, local, meaning-preserving text spans.

If no signals are identified, use exactly:

```markdown
### Signals

None identified within the configured check-agent scope.
```

## Structured signal data

Machine-readable signal data is currently agent- and version-dependent.

Current status:

- `page-structure-checker` emits YAML blocks because its output is generated deterministically by Python;
- `page-hygiene-checker-v1.0.0` is Markdown-only;
- `language-style-checker-v1.0.0` is Markdown-only;
- machine-readable signal blocks for LLM-based agents are deferred to a later prompt version or to Phase 3 tooling.

For future LLM-based check agents, structured signal data may use a block such as:

````markdown
```yaml
signal_id: S-001
agent: language-style-checker
page: docs/stereotypes/classes/event.md
category: grammar
severity: low
confidence: high
location: "## Description"
current_text: "An event are..."
proposed_text: "An event is..."
application_mode: exact_replace
risk: low
```
````

The Markdown text is for humans and issue readability. Structured blocks are for later resolution agents and deterministic patch tools.

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

## Resolution status

Resolution is deferred to Phase 3. Phase 2 signals are candidate inputs and are not accepted findings.
```

## Comment identity and duplicate control

Before repeated or scheduled execution, Phase 2 should support stable comment identity.

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

This is required before scheduled execution to prevent issue-comment noise.

## Batch execution model

The current batch runner is page/model oriented.

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

  - slug: page-hygiene-checker
    type: llm
    prompt: page-hygiene-checker-v1.0.0
    provider: groq
    models:
      - model: openai/gpt-oss-20b
        slug: gpt-oss-20b
        max_completion_tokens: 1200

  - slug: language-style-checker
    type: llm
    prompt: language-style-checker-v1.0.0
    provider: groq
    models:
      - model: openai/gpt-oss-20b
        slug: gpt-oss-20b
        max_completion_tokens: 1200

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

## Scheduling policy

Scheduled execution is not the immediate next milestone.

Scheduling should wait until:

1. all check-agent prompts or deterministic implementations required for the scheduled batch exist;
2. agent-aware issue routing is implemented;
3. stable comment identity and update-existing behavior are implemented;
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

## Phase 3 resolution model

Phase 3 should introduce resolution agents.

A resolution agent reads open check issues and evaluates the collected signals.

The resolution stage should not rely on a single model judgment. It should use a quorum rule.

Recommended vote values:

```text
must_fix
no_fix
defer
```

Recommended acceptance rule:

```text
A signal is accepted when at least 2 out of 3 evaluator votes are must_fix.
```

This single rule should apply across signal types.

Do not define different acceptance thresholds for grammar, style, hygiene, and structure at the beginning. A single rule is easier to reason about and easier to automate.

## Acceptance gate vs patch-safety gate

The quorum rule decides whether a signal should be fixed.

It does not decide whether the system may automatically patch the page.

Use two gates:

```text
Gate 1: resolution quorum
Gate 2: deterministic patch safety
```

### Gate 1 — Resolution quorum

A signal is accepted if:

- at least 2 out of 3 evaluators vote `must_fix`;
- no evaluator reports the signal as unsafe;
- the signal still refers to the current page version or can be rebased safely.

### Gate 2 — Patch safety

An accepted signal may be automatically applied only if:

- the application mode is supported by Python;
- at least two evaluators propose the same normalized replacement;
- `current_text` occurs exactly once;
- `proposed_text` is non-empty;
- the change is local;
- the change does not touch protected content types;
- the resulting Markdown passes validation.

Protected content types should initially include:

- definitions;
- conceptual claims;
- source interpretation;
- direct quotations;
- citation locators not already visible in the page.

## Patch application model

LLMs should not directly edit repository files.

Phase 3 should use deterministic Python tools for patch application.

Initial supported operations may include:

```text
exact_replace
insert_heading
normalize_whitespace
fix_markdown_table
append_review_log_entry
```

Patch tools must reject ambiguous edits.

Reject when:

- `current_text` occurs zero times;
- `current_text` occurs multiple times;
- the target page changed since the signal commit SHA and cannot be safely rebased;
- the proposed replacement is empty;
- the edit affects protected content;
- post-edit validation fails.

## Fully automatic final configuration

The final project goal may remove the human from the loop, but it should not remove control gates.

The final automated pipeline should be:

```text
check agents
→ signal issues
→ resolution agents
→ quorum decision
→ change planner
→ deterministic Python patch applier
→ verification checks
→ pull request
→ CI
→ auto-merge when eligible
→ issue update or closure
```

The preferred final automation path is automatic PR creation and auto-merge after gates pass, rather than direct commits to `main`.

Direct commits, if ever allowed, should be limited to very low-risk mechanical fixes.

## Current migration status

Completed:

- Phase 2 methodology defines lightweight check-agent infrastructure;
- signal terminology is used in the current runner, mock provider, issue manager, and batch runner;
- `page-structure-checker` exists as the first deterministic check agent;
- `page-hygiene-checker-v1.0.0` exists as the first dedicated LLM check-agent prompt;
- `language-style-checker-v1.0.0` exists as the second dedicated LLM check-agent prompt.

Pending:

1. implement agent-aware issue routing;
2. implement stable comment identity and update-existing behavior;
3. add runner and batch support for page/check-agent/model execution;
4. wire `page-hygiene-checker-v1.0.0` and `language-style-checker-v1.0.0` into agent-aware local execution;
5. run small local agent-aware batches before issue posting;
6. add manual GitHub Actions execution after local stability;
7. add conservative scheduling only after duplicate-comment control exists.

## Current deferred work

The following work is deferred from the immediate Phase 2 migration:

- GitHub Actions scheduling;
- Phase 3 resolution agents;
- quorum evaluation;
- patch planning;
- patch application;
- automatic PR creation;
- automatic issue closure;
- auto-merge;
- source-faithfulness validation;
- heavy semantic analysis;
- local/offline model integration.

## Recommended implementation steps

### Step 1 — Update Phase 2 documentation — completed

Update this document to define Phase 2 as lightweight check-agent infrastructure.

Commit message:

```bash
docs(phase-2): define lightweight check-agent architecture
```

### Step 2 — Rename concepts from findings to signals — completed

Update runner, issue-manager, prompts, and docs to use:

```text
Signal count
Signals
S-001
```

rather than:

```text
Finding count
Findings
F-001
```

Commit message:

```bash
refactor(phase-2): rename review findings to check signals
```

### Step 3 — Introduce agent-aware issue routing — next

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

### Step 4 — Implement `page-structure-checker` — completed

Implemented file:

```text
scripts/phase-2/check_agents/page_structure_checker.py
```

Commit message:

```bash
feat(phase-2): add page structure check agent
```

### Step 5 — Add stable comment identity and update-existing behavior

Modify issue posting so repeated runs update matching comments instead of always posting new comments.

Stable identity:

```text
page + agent + provider + model + prompt + commit SHA
```

Commit message:

```bash
feat(phase-2): update existing check signal comments
```

### Step 6 — Split the current LLM prompt — completed

The page-hygiene checker prompt exists:

```text
prompts/phase-2/page-hygiene-checker-v1.0.0.md
```

The language-style checker prompt exists:

```text
prompts/phase-2/language-style-checker-v1.0.0.md
```

Commit messages:

```bash
feat(phase-2): add page hygiene checker prompt
feat(phase-2): add language style checker prompt
```

### Step 7 — Update batch configuration

Move the batch config from page/model execution to page/check-agent/model execution.

Commit message:

```bash
feat(phase-2): configure agent-aware check batches
```

### Step 8 — Run small local batches

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

### Step 9 — Add manual GitHub Actions execution

After local execution is stable and duplicate comments are controlled, add manual GitHub Actions execution through `workflow_dispatch`.

Do not add schedules yet.

Commit message:

```bash
ci(phase-2): add manual check-agent workflow
```

### Step 10 — Add conservative scheduling

After manual GitHub Actions execution is stable, add a conservative schedule.

Initial schedule should run only a very small batch.

Commit message:

```bash
ci(phase-2): schedule lightweight check-agent batch
```

## Completion criteria

Phase 2 can be considered complete when:

- check-agent architecture is documented;
- at least one deterministic check agent is implemented;
- at least two lightweight LLM check-agent prompts are implemented and wired into agent-aware execution;
- issue routing is page-plus-agent based;
- outputs use signal terminology;
- generated comments are structured according to each agent contract and pass validation;
- repeated runs update existing comments rather than creating duplicates;
- generated outputs remain uncommitted;
- small batch execution works locally;
- manual GitHub Actions execution works;
- conservative scheduled execution works;
- Phase 3 resolution-agent requirements are documented but not implemented in Phase 2.

## Generation and review log

- Phase 2 revised from a general page-level review pilot into lightweight check-agent infrastructure.
- Check agents are responsible for producing structured page-local signals.
- Signal terminology has been introduced in the current runner, mock provider, issue manager, and batch runner.
- The Python-based `page-structure-checker` has been added as the first deterministic check agent.
- The LLM-based `page-hygiene-checker-v1.0.0` prompt has been added, with runner and batch integration still pending.
- The LLM-based `language-style-checker-v1.0.0` prompt has been added, with runner and batch integration still pending.
- The current general runner still points to the legacy general page-reviewer prompt and should be parameterized or replaced before real agent-specific LLM runs.
- Resolution agents, quorum decisions, patch planning, patch application, PR creation, and issue closure are deferred to Phase 3.
- The final automation goal may remove the human from the loop, but must retain structured signals, quorum gates, deterministic patch application, validation, and traceable GitHub issues/PRs.
