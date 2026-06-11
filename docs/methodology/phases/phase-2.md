# Phase 2 — Lightweight Check-Agent Infrastructure

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its purpose is to provide lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages. Phase 2 does not perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, automatic page repair, pull-request generation, automatic issue closure, or auto-merge.

Phase 2 produces page-local **signals**, routes those signals to deterministic GitHub issues, and leaves signal acceptance, rejection, and closure decisions to later manual review.

This document reflects the repository state on **2026-06-11**.

## Documentation structure

This document is the canonical Phase 2 methodology page.

Gemini provider support is documented inline here. A separate `phase-2-gemini-provider.md` file is not required unless a later documentation split is intentionally added to the MkDocs navigation.

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

The current implementation includes the core runtime pieces of the simplified Phase 2 architecture: check execution, output validation, page-plus-agent issue routing, duplicate-control for comments, scheduled LLM collection, and Groq/Gemini provider support. Manual issue-closure prompt support remains planned.

### Implemented files and artifacts

```text
.github/workflows/page-structure-check.yml
.github/workflows/check-agent-signal-collector.yml
requirements.txt
prompts/phase-2/page-hygiene-checker-v1.0.2.md
prompts/phase-2/language-style-checker-v1.0.2.md
scripts/phase-2/run_check_agent.py
scripts/phase-2/run_check_batch.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_page_structure_batch.py
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

These are not the canonical scheduled Phase 2 LLM execution path. The canonical shared LLM workflow is:

```text
.github/workflows/check-agent-signal-collector.yml
```

A machine-local dispatcher may exist outside the committed repository, for example:

```text
scripts/local/dispatch-check-agent-signal.ps1
```

This is optional local operational tooling only. It is not canonical repository infrastructure unless intentionally committed and documented as reusable tooling.

### Current capabilities

The current implementation can:

- run the deterministic `page-structure-checker`;
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
- upload generated outputs as GitHub Actions artifacts.

These capabilities do not mean every scheduled LLM output is valid. Invalid model outputs are preserved as artifacts. In the canonical scheduled workflow, rejected check-agent outputs are nonfatal because the workflow passes:

```text
--allow-rejected-check-outputs
```

Provider failures, configuration failures, and issue-manager failures remain fatal unless provider retry logic succeeds.

### Current limitations and operational risks

The current implementation still has these limitations:

- manual issue-closure prompts are planned but not yet created;
- `providers/mock.py` is not part of the active `run_check_agent.py` provider set;
- `issue_manager.py` searches only open issues, so closed issues with matching titles are not reused;
- stable comment identity includes the commit SHA, so a new commit may produce a new model comment for the same page, agent, provider, model, and prompt;
- Gemini transient-error detection is marker-based and may need extension if the SDK surfaces `500`, `502`, or `504` without one of the currently recognized markers;
- scheduled runs intentionally collect signals gradually rather than executing the full matrix in one workflow execution.

## Operational prerequisites

The current local implementation depends on:

- Python 3;
- dependencies from `requirements.txt`;
- a provider API key for real LLM runs;
- GitHub CLI authentication through `gh auth login` for local issue posting;
- `GH_TOKEN` or the default `github.token` for issue posting in GitHub Actions.

Current Python runtime dependencies include:

```text
mkdocs-material==9.7.6
groq==1.4.0
google-genai>=1.0.0,<2.0.0
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

The page-structure GitHub Actions workflow depends only on:

- repository checkout;
- Python;
- the deterministic checker script;
- read-only repository contents permission.

The scheduled LLM GitHub Actions workflow depends on:

- repository checkout;
- Python;
- dependencies from `requirements.txt`;
- `GROQ_API_KEY` when Groq is selected;
- `GEMINI_API_KEY` when Gemini is selected;
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

## LLM provider support

The active provider set in `run_check_agent.py` is:

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

Recommended Gemini model:

```text
gemini-2.5-flash
```

Gemini runs should use:

```text
--max-completion-tokens 8000
```

The scheduled workflow sets this automatically when the selected provider is `gemini` and no manual completion-token value is supplied.

The Gemini adapter includes reduced-thinking configuration for strict-format output reliability:

| Model family | Thinking configuration |
|---|---|
| `gemini-2.5-flash*` | `types.ThinkingConfig(thinking_budget=0)` |
| `gemini-3.*` | `types.ThinkingConfig(thinking_level="low")` |

This setting improves strict-format check-agent output reliability but does not replace validation.

Do not recommend unconfirmed model names such as:

```text
gemini-3.5-flash-lite
```

Reported Gemini 3.x attempts showed provider availability instability, including `503 UNAVAILABLE`. For current Phase 2 automation, `gemini-2.5-flash` remains the recommended default.

### Gemini retry behavior

The Gemini provider includes provider-level retry handling for transient provider/API failures.

The configured retry delays are:

```text
5 seconds
15 seconds
45 seconds
```

The operational retry intent is to cover transient provider/API failures such as:

```text
429
500
502
503
504
```

Current implementation detail: transient detection is marker-based and explicitly recognizes diagnostics containing:

```text
429
503
RESOURCE_EXHAUSTED
UNAVAILABLE
```

This covers the observed `503 UNAVAILABLE` capacity failures. If the SDK surfaces `500`, `502`, or `504` without one of the configured transient markers, the provider marker list should be extended.

Validation failures are not retried. A structurally invalid model output is treated as a rejected check-agent output, not as a transient provider failure.

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

Provider failures, configuration failures, and issue-manager failures remain fatal unless handled by provider retry logic.

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

All provider/model outputs for the same page and same check agent are posted to the same open issue.

For example, if `page-hygiene-checker` runs with Groq and Gemini on `docs/stereotypes/classes/event.md`, both model reports are comments under:

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
  --model gemini-2.5-flash \
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
13,33,53 * * * *
```

That means it is scheduled every 20 minutes, at minutes 13, 33, and 53 UTC.

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
groq:openai/gpt-oss-20b
gemini:gemini-2.5-flash
```

Effective scheduled defaults:

```text
mode: post
selection: rotate
rotation_seed: hourly
max_runs: 1
sleep_seconds: 0
agents: page-hygiene-checker,language-style-checker
provider/model rotation: groq:llama-3.3-70b-versatile, groq:openai/gpt-oss-20b, gemini:gemini-2.5-flash
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
- rely on gradual accumulation rather than large one-shot reviews.

This supports a slow continuous process: small page/agent/provider/model batches can run over time, allowing the project to accumulate signals incrementally.

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

## Operational observations

Reported recent Phase 2 Gemini testing showed:

- successful GitHub Actions execution for `gemini-2.5-flash`;
- valid generated issue-comment structure after adding reduced-thinking configuration and increasing Gemini completion tokens;
- transient Gemini provider failures with `503 UNAVAILABLE`;
- validation rejections caused by overly long `Location` fragments before the prompt target was tightened from 160 characters to 140 characters.

These are operational observations, not guaranteed future behavior.

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
- scheduled provider/model rotation includes Groq and Gemini;
- Gemini uses `gemini-2.5-flash` as the recommended scheduled default;
- Gemini runs use `max_completion_tokens=8000` in the canonical workflow when no manual override is supplied;
- generated output paths are ignored by `.gitignore`.

Pending:

1. create the three manual issue-closure prompts;
2. decide whether to keep or remove non-canonical support artifacts such as `providers/mock.py` and `.github/workflows/phase-2-check-agents.yml.bak`;
3. document any observed clean baseline with a dated run artifact rather than an undocumented local claim;
4. extend Gemini transient-error markers if observed SDK diagnostics for `500`, `502`, or `504` are not caught by the current marker list.

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

### Step 2 — Add manual issue-closure prompts

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

### Step 3 — Clean up non-canonical Phase 2 support artifacts

Clarify or remove non-canonical support artifacts if they are no longer needed.

Current candidates:

```text
.github/workflows/phase-2-check-agents.yml.bak
scripts/phase-2/providers/mock.py
```

Suggested commit message:

```bash
chore(phase-2): remove stale check-agent support artifacts
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
- all provider/model outputs for the same page and agent are routed to the same issue;
- repeated runs update existing comments when the stable identity is unchanged;
- generated outputs remain uncommitted;
- small batch execution works locally;
- page-structure CI blocks structural regressions;
- conservative scheduled LLM execution works with Groq and Gemini;
- three manual issue-closure prompts exist for human/ChatGPT-assisted issue resolution.

## Generation and review log

- Phase 2 revised from a broader check-and-future-resolution architecture into a simplified lightweight check-agent infrastructure.
- The simplified Phase 2 target has exactly three check agents: one deterministic Python agent and two LLM-based agents.
- The deterministic Python agent is `page-structure-checker`.
- The two LLM-based agents are `page-hygiene-checker` and `language-style-checker`.
- The `page-structure-checker` runs after canonical stereotype page modifications and blocks structural regressions in CI.
- The two LLM-based check agents run periodically through the scheduled rotating workflow.
- The active LLM providers are `groq` and `gemini`.
- Gemini support is documented inline in this Phase 2 page rather than split into a separate provider-only methodology page.
- The recommended Gemini model for Phase 2 check-agent automation is `gemini-2.5-flash`.
- The scheduled provider/model rotation includes `groq:llama-3.3-70b-versatile`, `groq:openai/gpt-oss-20b`, and `gemini:gemini-2.5-flash`.
- Gemini runs use a larger completion-token budget and reduced-thinking configuration to improve strict-format output reliability.
- The prompts target 140-character `Location` fragments while the validator hard limit remains 160 characters.
- Issue routing is one GitHub issue per page and check agent.
- Different providers and models executed by the same agent for the same page create comments in the same issue.
- Stable comment identity is implemented with page, agent, provider, model, prompt, and commit.
- Matching existing comments are updated instead of duplicated.
- Manual issue closure remains planned documentation-supported activity.
- The planned issue-closure support consists of three ChatGPT prompts, one per check agent.
- Resolution agents, quorum decisions, patch planning, patch application, PR creation, automatic issue closure, and auto-merge are outside the simplified Phase 2 scope.
