# Generation Policy

This project documents OntoUML stereotypes using content generated, reviewed, or revised with large language models and supporting deterministic tooling.

## Purpose

The purpose of this policy is to make explicit how documentation in this repository is generated, reviewed, checked, and maintained.

This policy also clarifies how Phase 2 check-agent outputs relate to canonical stereotype pages, GitHub issues, and page-level generation and review logs.

## Principles

1. Documentation content may be generated, reviewed, or revised with assistance from large language models.
2. Deterministic and API-based tooling may be used to check page structure, page hygiene, and language/style quality.
3. Generated content and check-agent outputs are provisional until reviewed by a human maintainer.
4. Phase 2 check-agent outputs are **signals**, not accepted findings, edit instructions, or closure decisions.
5. Generated content should be checked against authoritative OntoUML sources whenever conceptual accuracy, source faithfulness, or claim support matters.
6. Phase 2 check agents do not perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, or OntoUML/UFO semantic validation.
7. The project is unofficial and should not be cited as the normative source for OntoUML.
8. Claims, examples, and interpretations should remain traceable to consulted sources whenever possible.

## Page structure

Each canonical stereotype page should contain the following sections:

```text
## Description
## Stereotype Profile
## Examples
## References
### Direct Citations
### Consulted Sources
## Generation and Review Log
```

This structure is checked by the Phase 2 `page-structure-checker`.

Some intentionally incomplete pages may use the explicit skeleton-page marker:

```markdown
<!-- skeleton-page -->
```

The marker indicates that empty-section signals may be suppressed for that page, but it does not remove the requirement to preserve the expected page structure.

## References policy

Each page should distinguish between direct citations and consulted sources.

### Direct Citations

Direct citations are exact quoted passages used to support specific claims in the page.

Direct citation entries should preserve enough visible locator information to make later review practical when such information is available.

### Consulted Sources

Consulted sources are documents, specifications, articles, books, or other materials studied while generating or reviewing the page.

A source may appear in the consulted sources list even when no direct quotation from it is used.

Consulted-source entries should remain clear enough to support later traceability and review.

## Generation and review log policy

Each stereotype page should include a log entry when the canonical page content is created, modified, reviewed, corrected, consolidated, or regenerated.

Each log entry should record, when applicable:

- date;
- human reviewer, tool, agent, prompt, provider, or model used;
- action performed;
- short summary of the change or review;
- main inputs used;
- related issue, pull request, or commit reference.

In the `Generation and Review Log` table, the `Agent` column is a broad provenance field. It may identify a human reviewer, LLM/model, deterministic tool, check agent, or automated process. It should not be read as meaning "Phase 2 check agent" unless the value is one of the documented check-agent slugs.

A Phase 2 check-agent run that only creates a local report, workflow artifact, GitHub issue, or GitHub issue comment does **not** by itself require a new page-level generation and review log entry.

A page-level log entry should be added when a Phase 2 signal leads to an accepted page change, a completed manual review of the page, or another substantive update to the canonical stereotype page.

## Phase 2 check-agent output policy

Phase 2 check-agent outputs are review-support artifacts.

They may appear as:

```text
.tmp/phase-2/...
issue-comment*.md
GitHub issue comments
GitHub Actions artifacts
```

These outputs are not canonical documentation pages and should not be committed as source files unless a later workflow explicitly changes that policy.

Phase 2 currently uses three check agents:

```text
page-structure-checker
page-hygiene-checker
language-style-checker
```

The `page-structure-checker` is deterministic Python tooling. It checks required headings, heading order, duplicate headings, malformed heading levels, unexpected level-2 sections, and empty required sections. It does not call an LLM, edit pages, commit changes, open pull requests, or post to GitHub by itself.

The `page-hygiene-checker` and `language-style-checker` are lightweight LLM-based check agents. Their outputs are structured Markdown issue comments containing candidate signals.

The LLM-based Phase 2 check agents are intentionally narrow in scope. They must not:

- validate quotations against original sources;
- infer source content;
- check external papers, PDFs, theses, web pages, or other source material;
- decide whether a citation substantively supports a claim;
- evaluate OntoUML/UFO conceptual correctness;
- perform cross-page consistency analysis;
- automatically modify repository files;
- automatically open pull requests;
- automatically close issues.

## Manual signal review and issue-resolution policy

Phase 2 includes manual, confirmation-gated issue-resolution prompts for the two LLM-based check agents:

```text
prompts/phase-2/close-page-hygiene-signal-issue-v1.0.0.md
prompts/phase-2/close-language-style-signal-issue-v1.0.0.md
```

There is currently no dedicated `page-structure-checker` issue-closure prompt.

Manual issue-resolution prompts are intended to help a human maintainer inspect one GitHub issue, compare candidate signals against the current canonical page, and classify each signal or signal group as:

```text
accept
reject
defer
```

These prompts do not run automatically and do not replace maintainer judgment.

Any GitHub write action, including posting an issue comment, creating a branch, committing changes, opening a pull request, or closing an issue, requires explicit human confirmation.

## Review status

The presence of generated content does not imply correctness.

A page should be treated as provisional until its claims, examples, and interpretations have been reviewed against authoritative OntoUML sources where accuracy matters.

A passing Phase 2 structural, hygiene, or language-style check does not imply conceptual correctness, source faithfulness, cross-page consistency, or authoritative validation.

Likewise, the absence of Phase 2 signals does not prove that a page is complete or correct.
