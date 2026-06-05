# Phase 2 — Page-Level Review Pilot

Phase 2 is the second content-production phase of **OntoUML According to the Machines**.

Its initial purpose is to introduce a controlled review workflow for existing canonical stereotype pages. Phase 2 starts with page-level review rather than automatic rewriting, source reprocessing, or full expert validation.

The first Phase 2 pilot uses manually triggered reviewer agents to inspect one canonical Markdown page and record findings in GitHub issues. The output is an actionable review trail for human assessment, not a direct modification of the documentation pages.

## Purpose

Phase 2 has four initial goals:

1. review existing canonical stereotype pages against the project's documented structure and review expectations;
2. identify potential overstatements and claims that lack visible citation or source support within the page;
3. check citation and consulted-source hygiene;
4. collect model-specific review findings in GitHub issues for later human or agentic aggregation.

The phase prioritizes controlled review, traceability, and issue-based discussion over automatic content generation.

## Scope

The initial Phase 2 pilot includes:

- page-level review of one canonical stereotype page at a time;
- manual execution through a GitHub Actions workflow or equivalent local command;
- one reviewer agent per execution;
- use of one LLM provider or local model per reviewer agent;
- one GitHub issue per reviewed stereotype page;
- one structured issue comment per reviewer-agent run;
- identification of methodology-compliance issues;
- identification of potential overstatements;
- identification of claims without visible citation or consulted-source support;
- citation-locator checks;
- citation relevance checks for central claims;
- consulted-source duplication and formatting checks;
- detection of quotation encoding or formatting artifacts.

The initial Phase 2 pilot does not include:

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

These exclusions apply to the initial pilot only. Later Phase 2 work may add broader review tasks if the pilot proves reliable.

## Execution model

The initial Phase 2 workflow is manual and review-oriented.

A reviewer-agent run receives:

1. one canonical stereotype Markdown page under `docs/stereotypes/classes/` or `docs/stereotypes/relations/`;
2. a Phase 2 page-review prompt or rubric;
3. compact project rules copied from the generation policy and phase methodology where needed.

The reviewer agent produces a structured review result. The result is posted to GitHub as an issue comment.

The workflow should use one issue per canonical stereotype page. If an open issue already exists for the reviewed page, the reviewer should add a new structured comment to that issue rather than opening a duplicate issue. If no open issue exists, the workflow should create one.

### Initial execution constraints

The first implementation should use:

| Constraint | Value |
|---|---|
| Trigger | Manual execution |
| Page count | One page per run |
| Agent count | One reviewer agent per run |
| Output | GitHub issue or issue comment |
| Repository mutation | No canonical page edits |
| Review basis | Page content and Phase 2 rubric only |

Scheduled execution, multiple reviewer agents, aggregation agents, and pull-request generation are deferred until the manual workflow is stable.

## Input model

The minimal input for the first pilot is:

```text
<canonical stereotype page>.md
<Phase 2 page-review prompt or rubric>
```

Example:

```text
docs/stereotypes/classes/role.md
prompts/phase-2/page-reviewer-v0.1.0.md
```

The reviewer agent should not read Phase 1 intermediate files unless a later Phase 2 workflow explicitly enables that task.

The reviewer agent should not read original source papers, theses, PDFs, or external documents in the initial pilot.

## Output model

The preferred initial output is a GitHub issue.

Issue identity should be deterministic enough to prevent duplicates. A recommended issue title pattern is:

```text
Phase 2 page review: <group>/<stereotype-id>
```

Examples:

```text
Phase 2 page review: classes/role
Phase 2 page review: classes/kind
Phase 2 page review: relations/mediation
```

Recommended labels include:

- `phase-2`;
- `page-review`;
- `agent-review`;
- `needs-human-review`;
- a stereotype-specific label if available.

Each reviewer-agent run should post a structured comment to the issue. The comment should identify the provider, model, prompt version, reviewed page, repository commit SHA, review scope, findings, recommendations, and limitations.

## Review basis

The initial reviewer agent evaluates only what is visible from the page and the Phase 2 rubric.

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

The reviewer should also check whether the page respects the current maturity expectations. In the initial pilot, the reviewer should not require completed examples, diagrams, or stereotype profiles.

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

## Recommended issue comment structure

Each reviewer-agent comment should use a structure similar to:

```markdown
## Model review: <provider> / <model> — <date>

### Run metadata

| Field | Value |
|---|---|
| Provider | <provider> |
| Model | <model> |
| Prompt | <prompt ID and version> |
| Reviewed page | `<repository-relative path>` |
| Commit SHA | `<commit SHA>` |
| Scope | Page-level review only |

### Summary judgment

<Short summary.>

### Methodology compliance

<Findings.>

### Potential overstatements

<Findings, or `None identified.`>

### Claims without visible support

<Findings, or `None identified.`>

### Citation and source-grounding issues

<Findings, or `None identified.`>

### Consulted-source issues

<Findings, or `None identified.`>

### Encoding or formatting issues

<Findings, or `None identified.`>

### Recommended actions

- [ ] <Action item.>

### Limitations

This review did not check Phase 1 intermediate files, original source papers, external OntoUML materials, or related stereotype pages.
```

## Multi-model review pattern

Later Phase 2 work may run several reviewer agents for the same page, each using a different viable model or provider.

In that case:

- each model-specific reviewer should evaluate the page independently;
- each reviewer should add a separate structured comment to the same open issue;
- reviewers should not use previous model comments as input unless explicitly configured to do so;
- a later aggregation agent may read all comments and propose accepted findings, rejected findings, and issues requiring human review.

The aggregation agent is deferred from the initial pilot.

## Risks

The initial Phase 2 pilot carries known risks:

- model reviewers may overinterpret page content;
- model reviewers may confuse visible support with actual source support;
- multiple reviewers may repeat the same weak finding;
- issue comments may become noisy if runs are repeated too often;
- free API limits may interrupt executions;
- provider-specific model behavior may change over time;
- page-level review cannot establish authoritative OntoUML correctness.

These risks are acceptable only if the workflow remains review-oriented and avoids automatic page mutation.

## Completion criteria for the initial pilot

The initial Phase 2 pilot is complete when:

- a Phase 2 page-review prompt or rubric exists;
- a manual reviewer workflow can be executed for one canonical stereotype page;
- the workflow can create or find the correct GitHub issue for the reviewed page;
- the workflow can add a structured reviewer comment to that issue;
- the reviewer output clearly states its scope and limitations;
- no canonical stereotype page is modified automatically;
- no pull request is opened automatically;
- the maintainer can inspect the issue and decide whether follow-up work is needed.

## Deferred work

The following work is deferred to later Phase 2 iterations or later phases:

- validation against Phase 1 intermediate files;
- validation against original source documents;
- cross-page consistency checking;
- automated aggregation of multiple model reviews;
- automatic pull-request creation;
- controlled page rewriting;
- stereotype-profile completion;
- example generation;
- diagram generation;
- expert-level review workflows.

## Relationship to Phase 1

Phase 1 created a provisional source-grounded documentation base. Phase 2 begins by reviewing that base without assuming that the content is final.

The initial Phase 2 pilot deliberately operates at page level. It checks structure, visible traceability, citation hygiene, and overstatement risk. It does not reopen the full Phase 1 extraction or consolidation process.