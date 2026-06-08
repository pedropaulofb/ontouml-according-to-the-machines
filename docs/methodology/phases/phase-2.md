# Phase 2 — Page-Level Review Pilot

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its initial purpose is to introduce a controlled review workflow for existing canonical stereotype pages. Phase 2 starts with page-level review rather than automatic rewriting, source reprocessing, or full expert validation.

The current Phase 2 implementation produces **structured candidate review comments** from existing canonical Markdown pages. These comments are raw inputs for later human or agentic aggregation. They are not accepted project decisions and they do not directly modify the documentation pages.

## Purpose

Phase 2 has four initial goals:

1. review existing canonical stereotype pages against the project's documented structure and review expectations;
2. identify potential overstatements and claims that lack visible citation or source support within the page;
3. check citation and consulted-source hygiene;
4. collect model-specific candidate findings for later human or agentic aggregation.

The phase prioritizes controlled review, traceability, and explicit candidate findings over automatic content generation.

## Current implementation status

The current implementation is a **manual local runner**.

It can:

- review one canonical stereotype page per execution;
- use the compact Phase 2 page-review prompt `page-reviewer-v1.0.3`;
- call a real Groq model through the Groq provider adapter;
- run a deterministic mock provider for smoke testing;
- write a local Markdown issue-comment candidate;
- normalize safe Markdown/template issues;
- validate generated comments for structure and safety.

It does **not** yet:

- create GitHub issues;
- post comments to GitHub issues;
- aggregate multiple model reviews;
- rewrite canonical pages;
- open pull requests;
- commit generated outputs.

The current implementation files are:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
scripts/phase-2/run_page_review.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/mock.py
```

Generated local review outputs are ignored by Git using the `issue-comment*.md` pattern.

## Scope

The current Phase 2 pilot includes:

- page-level review of one canonical stereotype page at a time;
- manual local execution from the repository checkout;
- one reviewer-model run per execution;
- use of one LLM provider or local model per reviewer-model run;
- local generation of one structured candidate issue comment per run;
- identification of methodology-compliance issues;
- identification of potential overstatements;
- identification of claims without visible citation or consulted-source support;
- citation-locator checks;
- citation relevance checks for central claims;
- consulted-source duplication and formatting checks;
- detection of quotation encoding or formatting artifacts.

The current Phase 2 pilot does not include:

- validation against Phase 1 intermediate files;
- validation against original papers, theses, PDFs, or external source texts;
- cross-page consistency checking;
- automatic rewriting of canonical stereotype pages;
- automatic commits to canonical stereotype pages;
- automatic pull-request creation;
- example creation;
- diagram creation;
- completion of stereotype profiles;
- expert-level OntoUML validation.

These exclusions apply to the current pilot only. Later Phase 2 work may add broader review tasks if the pilot proves reliable.

## Execution model

The current Phase 2 workflow is manual and review-oriented.

A reviewer-model run receives:

1. one canonical stereotype Markdown page under `docs/stereotypes/classes/` or `docs/stereotypes/relations/`;
2. a Phase 2 page-review prompt;
3. run metadata, including provider name, model name, prompt ID, review date, reviewed page path, commit SHA, and maximum completion-token budget.

The reviewer model produces a structured Markdown comment. The runner validates and writes the comment locally.

### Current execution constraints

| Constraint | Current value |
|---|---|
| Trigger | Manual local command |
| Page count | One page per run |
| Provider adapters | `mock`, `groq` |
| Prompt | `page-reviewer-v1.0.3` |
| Output | Local Markdown candidate comment |
| Repository mutation | No canonical page edits |
| Review basis | Provided page content and Phase 2 prompt only |
| Aggregation | Deferred |
| GitHub issue posting | Deferred |

Scheduled execution, GitHub issue posting, aggregation agents, and pull-request generation are deferred until the manual local workflow is stable.

## Input model

The minimal input for the current runner is:

```text
<canonical stereotype page>.md
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
```

Example:

```text
docs/stereotypes/classes/role.md
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
```

The reviewer model must not read Phase 1 intermediate files unless a later Phase 2 workflow explicitly enables that task.

The reviewer model must not read original source papers, theses, PDFs, external documents, previous issue comments, related pages, commits, or web pages in the current pilot.

## Output model

The current output is a **local Markdown candidate issue comment**.

Candidate comments are generated files and should not be committed. Examples include:

```text
issue-comment.md
issue-comment.invalid.md
issue-comment-groq-llama-3.3-70b-versatile.md
issue-comment-groq-gpt-oss-20b.md
```

Each candidate comment identifies the provider, model, prompt version, reviewed page, repository commit SHA, review scope, finding count, and candidate findings.

The preferred future output is a GitHub issue comment. The planned issue identity should be deterministic enough to prevent duplicates. A recommended future issue title pattern is:

```text
Phase 2 page review: <group>/<stereotype-id>
```

Examples:

```text
Phase 2 page review: classes/role
Phase 2 page review: classes/kind
Phase 2 page review: relations/mediation
```

Recommended future labels include:

- `phase-2`;
- `page-review`;
- `agent-review`;
- `needs-human-review`;
- a stereotype-specific label if available.

## Current model set

The first implemented real provider is Groq.

The current manually tested Groq models are:

| Provider | Model | Typical max completion tokens | Role |
|---|---|---:|---|
| `groq` | `llama-3.3-70b-versatile` | `3000` | stronger general reviewer |
| `groq` | `openai/gpt-oss-20b` | `2400` | alternate model-family reviewer under current token limits |

The exact completion-token value is configurable per run through `--max-completion-tokens`.

Example commands:

```bash
python scripts/phase-2/run_page_review.py \
  --page docs/stereotypes/classes/role.md \
  --provider groq \
  --model llama-3.3-70b-versatile \
  --output issue-comment-groq-llama-3.3-70b-versatile.md \
  --max-completion-tokens 3000
```

```bash
python scripts/phase-2/run_page_review.py \
  --page docs/stereotypes/classes/role.md \
  --provider groq \
  --model openai/gpt-oss-20b \
  --output issue-comment-groq-gpt-oss-20b.md \
  --max-completion-tokens 2400
```

The Groq API key must be provided through the `GROQ_API_KEY` environment variable and must not be committed.

## Mock provider

The `mock` provider is a smoke-test provider, not a substantive reviewer.

It allows maintainers to test the runner without:

- Groq credentials;
- API quota;
- internet access;
- model availability.

The mock provider checks the pipeline:

```text
CLI arguments
→ prompt loading
→ page loading
→ commit SHA detection
→ provider loading
→ output generation
→ normalization
→ validation
→ file writing
```

It should not be interpreted as a model-generated review.

## Review basis

The reviewer model evaluates only what is visible from the provided page and the Phase 2 prompt.

The reviewer may state that a claim lacks visible support within the page. It must not state that a claim is unsupported by the original literature unless the workflow has actually checked the original literature.

The reviewer may state that a citation appears relevant, irrelevant, weakly connected, malformed, duplicated, or missing a locator. It must not state that a quotation is accurate in the original source unless the workflow has actually checked the source text.

## Review checks

### Methodology compliance

The reviewer should check whether the page follows the expected documentation structure, including:

- `## Description`;
- `## Stereotype Profile`;
- `## Examples`;
- `## References`;
- `### Direct Citations`;
- `### Consulted Sources`;
- `## Generation and Review Log`.

The reviewer should also check whether the page respects the current maturity expectations. In the current pilot, the reviewer should not require completed examples, diagrams, or stereotype profiles. `Stereotype Profile` and `Examples` may contain `TBD in a later phase.`

### Potential overstatements

The reviewer should identify claims that sound stronger than their visible support in the page.

Examples of potential overstatement signals include:

- absolute language where the page only provides limited support;
- profile-like rules stated as final when the page is still provisional;
- broad claims based on a narrow set of citations;
- claims that appear to collapse version-sensitive distinctions;
- claims that imply expert validation where only Phase 1 consolidation has occurred.

### Claims without visible support

The reviewer should identify important claims in the `Description` section that do not appear visibly supported by a direct citation or consulted source entry in the page.

This is a page-level traceability check. It is not a source-literature validation check.

### Citation and source-grounding quality

The reviewer should check:

- whether important claims appear connected to at least one direct citation or consulted source;
- whether direct citations include locators when locators are expected;
- whether direct citations are relevant to central claims;
- whether direct citations are used for key definitions or central conceptual claims rather than decorative support.

### Consulted-source hygiene

The reviewer should check:

- duplicated consulted-source entries;
- inconsistent formatting of the same source;
- missing source scopes;
- unclear or malformed source identifiers;
- source entries that appear unrelated to the page content.

### Encoding and formatting issues

The reviewer should check:

- quotation encoding artifacts;
- malformed quotation marks;
- broken Markdown in citation bullets;
- Markdown table problems in the generation and review log;
- other formatting issues that reduce reviewability.

## Candidate issue comment structure

Each generated candidate comment should use the compact structure defined by `page-reviewer-v1.0.3`:

```markdown
## Model review: <provider> / <model> — <review date>

### Run metadata

| Field | Value |
|---|---|
| Provider | <provider> |
| Model | <model> |
| Prompt | page-reviewer-v1.0.3 |
| Review date | <review date> |
| Reviewed page | <path> |
| Commit SHA | <sha> |
| Finding count | <number of findings, or 0 if none> |

### Summary judgment

<One concise paragraph.>

### Scope

Page-level review only. This run did not check intermediate files, original sources, related pages, previous issue comments, or external OntoUML materials.

### Findings

#### F-001 — <finding title>

- Category: <one category>
- Severity: <low, medium, or high>
- Confidence: <low, medium, or high>
- Location: <section heading or line reference if supplied>
- Observation: <problem>
- Rationale: <why it matters>
- Recommendation: <concrete action>
- Suggested wording: <optional; omit if not useful>
```

The prompt asks for at most three findings, prioritizing the highest-impact findings. The runner remains more permissive and only rejects unusually noisy output above its configured hard limit.

## Runner validation and normalization

The runner enforces structure and safety, not review quality.

It normalizes safe mechanical issues such as:

- missing backticks around allowed category, severity, or confidence values;
- placeholder-style `Suggested wording: None` lines;
- duplicate trailing `### Findings` notes after concrete findings.

It validates:

- required output sections;
- required metadata values;
- unresolved placeholders;
- task checkboxes;
- finding-count parseability;
- finding-count consistency with visible finding headings;
- sequential finding IDs;
- required finding fields;
- allowed category, severity, and confidence values;
- obvious claims that the model used out-of-scope evidence;
- obvious recommendations to commit, open pull requests, apply changes, or otherwise mutate the repository automatically.

It intentionally does not reject candidate findings merely because a later aggregation step may consider them weak, redundant, overbroad, or out of scope.

## Multi-model review pattern

The current pattern runs multiple reviewer models independently over the same page.

In this pattern:

- each model-specific reviewer evaluates the page independently;
- each reviewer produces a separate structured candidate comment;
- reviewers should not use previous model comments as input unless explicitly configured to do so;
- a later aggregation agent may read all candidate comments and propose accepted findings, rejected findings, merged findings, and issues requiring human review.

The aggregation agent is deferred from the current pilot.

## Planned GitHub issue pattern

A later `issue_manager.py` implementation should:

1. read one generated issue-comment Markdown file;
2. derive the deterministic issue title for the reviewed page;
3. find an existing open issue for that page;
4. create the issue if it does not exist;
5. post the model review as a comment.

The intended long-term pattern is:

```text
one GitHub issue per stereotype page
one comment per model run
one later aggregation comment per reviewed page or review cycle
```

This functionality is planned but not implemented in the current runner.

## Risks

The current Phase 2 pilot carries known risks:

- model reviewers may overinterpret page content;
- model reviewers may confuse visible support with actual source support;
- multiple reviewers may repeat the same weak finding;
- candidate comments may become noisy if runs are repeated too often;
- free API limits may interrupt executions;
- provider-specific model behavior may change over time;
- page-level review cannot establish authoritative OntoUML correctness.

These risks are acceptable only if the workflow remains review-oriented and avoids automatic page mutation.

## Completion criteria for the current local-runner milestone

The current local-runner milestone is complete when:

- a Phase 2 page-review prompt exists;
- a manual reviewer command can be executed for one canonical stereotype page;
- the runner can call at least one real provider adapter;
- the runner can run a mock smoke-test provider;
- the runner can write a structured local candidate comment;
- the generated comment clearly states its scope and limitations;
- the runner validates candidate comments for structure and safety;
- no canonical stereotype page is modified automatically;
- no pull request is opened automatically.

## Completion criteria for the future issue-posting milestone

The future issue-posting milestone will be complete when:

- the workflow can create or find the correct GitHub issue for the reviewed page;
- the workflow can add a structured reviewer comment to that issue;
- repeated runs avoid duplicate issues;
- the maintainer can inspect the issue and decide whether follow-up work is needed.

## Deferred work

The following work is deferred to later Phase 2 iterations or later phases:

- GitHub issue posting;
- aggregation of multiple model reviews;
- validation against Phase 1 intermediate files;
- validation against original source documents;
- cross-page consistency checking;
- automatic pull-request creation;
- controlled page rewriting;
- stereotype-profile completion;
- example generation;
- diagram generation;
- expert-level review workflows.

## Relationship to Phase 1

Phase 1 created a provisional source-grounded documentation base. Phase 2 begins by reviewing that base without assuming that the content is final.

The current Phase 2 pilot deliberately operates at page level. It checks structure, visible traceability, citation hygiene, and overstatement risk. It does not reopen the full Phase 1 extraction or consolidation process.
