# Phase 2 — Page Hygiene Checker

This note records the Phase 2 documentation adjustments introduced by the dedicated `page-hygiene-checker` prompt.

## Prompt

The Page Hygiene Checker prompt is:

```text
prompts/phase-2/page-hygiene-checker-v1.0.0.md
```

The prompt defines a standalone lightweight LLM check agent for Phase 2. It replaces the earlier general page-reviewer scope for hygiene-specific runs, but it does not by itself complete the remaining Phase 2 migration work.

## Agent role

The `page-hygiene-checker` inspects exactly one canonical stereotype Markdown page and produces one structured Markdown GitHub issue comment with candidate hygiene signals.

Its output is a Phase 2 signal report. Signals are provisional observations. They are not accepted findings, resolution decisions, or instructions to modify the page.

## Scope

The agent checks only visible page-hygiene issues in Markdown content that is present.

It covers:

- visible reference hygiene;
- Markdown hygiene;
- encoding hygiene;
- Generation and Review Log hygiene.

It does not check missing required top-level sections or missing required reference/log sections. Those checks belong to `page-structure-checker`.

## Categories

The prompt uses exactly four signal categories:

```text
reference_hygiene
markdown_hygiene
encoding_hygiene
review_log_hygiene
```

Category precedence is:

```text
encoding_hygiene
markdown_hygiene
reference_hygiene
review_log_hygiene
```

The precedence rule exists because encoding and Markdown defects can explain apparent reference or review-log defects.

## Explicit exclusions

The agent must not:

- validate quotations against original sources;
- infer source content;
- inspect PDFs, papers, theses, or external sources;
- compare the page with related stereotype pages;
- decide whether a citation substantively supports a claim;
- evaluate conceptual correctness;
- perform OntoUML/UFO semantic validation;
- check grammar or writing style except where a visible Markdown or encoding artifact is the issue;
- require inline citations in `## Description`;
- require locators for every consulted source;
- report missing required top-level sections;
- report missing required reference/log sections;
- recommend conceptual rewrites;
- recommend repository actions or workflow changes.

## Output contract

The prompt is Markdown-only for version `v1.0.0`.

It emits one GitHub issue comment and does not emit JSON, YAML, or a separate machine-readable artifact.

The output uses:

```text
Signal count
Signals
S-001
S-002
S-003
```

The no-signal output remains:

```markdown
### Signals

None identified within the configured check-agent scope.
```

## Parser constraints

The prompt intentionally hardens the Markdown comment for downstream parsing.

It requires:

- fixed signal field order;
- concise single-line signal field values;
- no nested bullets inside signal fields;
- no raw newlines inside signal field values;
- no `<br>` inside signal field values;
- no fenced code blocks inside signal fields;
- `Signal count` equality with the number of `S-xxx` signal headings;
- exact replacement text only in `Suggested repair`;
- general action text in `Recommendation`.

## Machine-readable signal data

Machine-readable signal blocks are deferred to a later prompt version or to Phase 3 tooling.

For the current prompt, the Markdown issue comment is the only output artifact.

## Remaining migration work

The existence of `page-hygiene-checker-v1.0.0` means one dedicated LLM check-agent prompt now exists.

The remaining Phase 2 migration work still includes:

- agent-aware runner configuration;
- agent-aware issue routing;
- stable comment identity and update-existing behavior;
- deterministic implementation of `page-structure-checker` if not already wired into the runner;
- creation of the `language-style-checker` prompt;
- agent-aware batch configuration;
- small local batches before issue posting;
- manual GitHub Actions execution after local stability.

## Relationship to the main Phase 2 methodology

The main Phase 2 methodology should treat `page-hygiene-checker-v1.0.0` as the current dedicated hygiene-check prompt.

Where older text describes the hygiene checker as checking missing required reference/log sections, interpret that as superseded by this prompt-specific boundary: missing required sections belong to `page-structure-checker`; `page-hygiene-checker` checks malformed or inconsistent visible content that is present.

Where older text suggests machine-readable signal blocks during Phase 2, interpret that as deferred for this prompt version. The current hygiene checker emits a Markdown-only issue comment.
