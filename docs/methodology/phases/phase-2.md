# Phase 2 — Lightweight Check-Agent Infrastructure

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its revised purpose is to introduce lightweight, API-based and deterministic review infrastructure for existing canonical stereotype pages. Phase 2 does not perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, or page repair. It produces structured, page-local **signals** that can later be evaluated, resolved, and transformed into edits by Phase 3 automation.

Phase 2 follows a gradual automation model: small checks, small batches, conservative scheduling, and incremental accumulation of signals over time. The intended operating philosophy is _de grão em grão_: progress should come from many small, cheap, repeatable checks rather than infrequent heavyweight analyses.

## Purpose

Phase 2 has six initial goals:

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

The current implementation already provides a working local Phase 2 foundation:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_review_batch.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/mock.py
```

The current implementation can:

- run one page-level review at a time;
- call Groq models through the Groq provider adapter;
- run a deterministic mock provider for smoke testing;
- write local Markdown candidate comments;
- normalize safe Markdown/template issues;
- validate generated comments for structure and safety;
- read generated comment files;
- derive deterministic GitHub issue titles;
- create or reuse GitHub issues;
- post generated comments to GitHub issues;
- read a YAML batch configuration;
- run configured page/model batches;
- write generated outputs under `.tmp/phase-2/`.

The current implementation does **not** yet match the revised final Phase 2 architecture. In particular, it still uses a general page-reviewer prompt and page-only issue routing. The next Phase 2 work should migrate this implementation toward agent-aware check signals.

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

## Revised Phase 2 agent model

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
| Output | Structured signals |
| Applies changes | No |

The Page Structure Checker verifies the expected stereotype-page skeleton.

It should check:

- required headings;
- heading order;
- duplicate required headings;
- missing required sections;
- malformed required-section structure;
- unexpected top-level structural deviations;
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

### 2. Page Hygiene Checker

| Property | Value |
|---|---|
| Agent slug | `page-hygiene-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Output | Structured signals |
| Applies changes | No |

The Page Hygiene Checker combines reference hygiene, Markdown/encoding hygiene, and review-log hygiene.

It should check only visible page-level issues such as:

- missing or malformed `### Direct Citations` structure;
- missing or malformed `### Consulted Sources` structure;
- duplicate-looking source entries;
- visibly malformed citation locators;
- inconsistent locator formatting;
- broken Markdown tables;
- odd quotation artifacts;
- encoding noise;
- malformed headings;
- malformed review-log entries;
- missing or inconsistent Generation and Review Log metadata.

It must not:

- validate quotations against original sources;
- infer source content;
- check PDFs, papers, theses, or external sources;
- compare the page with related stereotype pages;
- decide whether a citation substantively supports a claim;
- recommend conceptual rewrites.

### 3. Language Style Checker

| Property | Value |
|---|---|
| Agent slug | `language-style-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Output | Structured signals |
| Applies changes | No |

The Language Style Checker identifies low-risk writing-quality issues.

It should check:

- grammar;
- spelling;
- awkward phrasing;
- unclear sentence structure;
- overly long sentences;
- minor style inconsistencies;
- reader-facing wording problems.

It may propose replacement wording only when the proposed wording preserves meaning and does not introduce new conceptual content.

It must not:

- change OntoUML claims;
- strengthen or weaken conceptual claims;
- add new technical precision;
- modify source interpretation;
- rewrite whole sections;
- perform semantic validation.

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
| Signal count | <number of signals, or 0 if none> |
```

Recommended signal section:

```markdown
### Signals

#### S-001 — <signal title>

- Category: `<category>`
- Severity: `<low | medium | high>`
- Confidence: `<low | medium | high>`
- Location: `<section heading or precise local reference>`
- Observation: `<what appears problematic>`
- Rationale: `<why this matters for reviewability or readability>`
- Recommendation: `<concrete next action>`
- Suggested repair: `<optional exact local repair; omit if not useful>`
```

If no signals are identified, use exactly:

```markdown
### Signals

None identified within the configured check-agent scope.
```

## Structured signal block

For automation, each signal should eventually include a machine-readable block.

Recommended format:

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

The Markdown text is for humans and issue readability. The structured block is for Phase 3 resolution agents and deterministic patch tools.

## Issue routing model

Phase 2 should use one GitHub issue per:

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

The revised batch model should eventually iterate over:

```text
pages × check agents × models
```

For deterministic Python agents, the provider/model fields can be:

```text
provider: python
model: deterministic
```

For LLM agents, the provider/model fields should identify the API provider and model.

Example conceptual configuration:

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
    prompt: page-hygiene-checker-v0.1.0
    provider: groq
    models:
      - model: openai/gpt-oss-20b
        slug: gpt-oss-20b
        max_completion_tokens: 1200

  - slug: language-style-checker
    type: llm
    prompt: language-style-checker-v0.1.0
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

1. check-agent prompts are separated;
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

### Step 1 — Update Phase 2 documentation

Update this document to define Phase 2 as lightweight check-agent infrastructure.

Commit message:

```bash
docs(phase-2): define lightweight check-agent architecture
```

### Step 2 — Rename concepts from findings to signals

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

### Step 3 — Introduce agent-aware issue routing

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

### Step 4 — Implement `page-structure-checker`

Implement the first revised check agent as Python-only.

Recommended file:

```text
scripts/phase-2/check_agents/page_structure_checker.py
```

The checker should generate a structured signal report and should not call an LLM.

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

### Step 6 — Split the current LLM prompt

Replace the general page-review prompt with two narrower prompts:

```text
prompts/phase-2/page-hygiene-checker-v0.1.0.md
prompts/phase-2/language-style-checker-v0.1.0.md
```

Commit message:

```bash
feat(phase-2): add lightweight check-agent prompts
```

### Step 7 — Update batch configuration

Move the batch config from page/model execution to page/agent/model execution.

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
- at least two lightweight LLM check agents are implemented;
- issue routing is page-plus-agent based;
- outputs use signal terminology;
- generated comments are structured and machine-readable;
- repeated runs update existing comments rather than creating duplicates;
- generated outputs remain uncommitted;
- small batch execution works locally;
- manual GitHub Actions execution works;
- conservative scheduled execution works;
- Phase 3 resolution-agent requirements are documented but not implemented in Phase 2.

## Generation and review log

- Phase 2 revised from a general page-level review pilot into lightweight check-agent infrastructure.
- Check agents are responsible for producing structured page-local signals.
- Resolution agents, quorum decisions, patch planning, patch application, PR creation, and issue closure are deferred to Phase 3.
- The final automation goal may remove the human from the loop, but must retain structured signals, quorum gates, deterministic patch application, validation, and traceable GitHub issues/PRs.
