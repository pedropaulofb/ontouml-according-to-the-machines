# Phase 2 — Check Agents

← Previous: [Scope and Architecture](overview.md) | [Phase 2 index](index.md) | Next: [Automated Signal Resolver](automated-resolver.md) →

## Phase 2 check agents

### 1. Page Structure Checker

| Property | Value |
|---|---|
| Check-agent slug | `page-structure-checker` |
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
Page-structure check
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
| Check-agent slug | `page-hygiene-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Implemented in the active check-agent-aware LLM runner and scheduled workflow |
| Runner | `scripts/phase-2/run_check_agent.py` |
| Batch runner | `scripts/phase-2/run_check_batch.py` |
| Prompt | Shared `check-signal-shared-contract-v1.0.0.md` plus `page-hygiene-checker-v1.1.0.md` |
| Supported provider adapters | `sambanova`, `groq`, `gemini`, `openrouter` |
| Active scheduled providers | `sambanova`, `groq`, `gemini`, `openrouter` |
| Output | Structured Markdown signal comment |
| Applies changes | No |
| Target execution | Periodic quota-aware content-addressed queue |

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

The active shared contract plus `page-hygiene-checker-v1.1.0` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

`run_check_agent.py` validates the output against the configured page-hygiene contract. Invalid model output is written as `.invalid.md` and is not posted.

### 3. Language Style Checker

| Property | Value |
|---|---|
| Check-agent slug | `language-style-checker` |
| Type | Lightweight LLM |
| LLM required | Yes |
| Phase | 2 |
| Implementation status | Implemented in the active check-agent-aware LLM runner and scheduled workflow |
| Runner | `scripts/phase-2/run_check_agent.py` |
| Batch runner | `scripts/phase-2/run_check_batch.py` |
| Prompt | Shared `check-signal-shared-contract-v1.0.0.md` plus `language-style-checker-v1.1.0.md` |
| Supported provider adapters | `sambanova`, `groq`, `gemini`, `openrouter` |
| Active scheduled providers | `sambanova`, `groq`, `gemini`, `openrouter` |
| Output | Structured Markdown signal comment |
| Applies changes | No |
| Target execution | Periodic quota-aware content-addressed queue |

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

The active shared contract plus `language-style-checker-v1.1.0` prompt is Markdown-only. It emits one GitHub issue comment and does not emit YAML, JSON, or a separate machine-readable artifact.

`run_check_agent.py` validates the output against the configured language-style contract. Invalid model output is written as `.invalid.md` and is not posted.

---

← Previous: [Scope and Architecture](overview.md) | [Phase 2 index](index.md) | Next: [Automated Signal Resolver](automated-resolver.md) →
