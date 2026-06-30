# Phase 2 — Prompts and Status

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md)

## Manual signal-review and issue-resolution prompt support

Phase 2 keeps two archived manual ChatGPT prompts for reviewing and resolving check-agent signal issues:

```text
archive/phase-2/manual-closure-prompts/close-page-hygiene-signal-issue-v1.0.0.md
archive/phase-2/manual-closure-prompts/close-language-style-signal-issue-v1.0.0.md
```

These archived prompts were implemented for the two LLM-based check agents:

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
archive/phase-2/manual-closure-prompts/close-page-hygiene-signal-issue-v1.0.0.md
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
archive/phase-2/manual-closure-prompts/close-language-style-signal-issue-v1.0.0.md
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
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.1.md
prompts/phase-2/resolve-language-style-signal-issue-v1.2.1.md
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
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.1.md
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
prompts/phase-2/resolve-language-style-signal-issue-v1.2.1.md
```

The current prompt file heading is:

```text
Phase 2 automated resolver: language-style signals v1.2.1
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
- `page-hygiene-checker-v1.0.3` exists as a dedicated LLM check-agent prompt;
- `language-style-checker-v1.0.3` exists as a dedicated LLM check-agent prompt;
- `run_check_agent.py` runs the two LLM check agents through an agent-aware contract;
- `run_check_agent.py` supports Groq, Gemini, Cerebras, SambaNova, and OpenRouter provider adapters;
- `run_check_agent.py` validates generated LLM output and writes `.invalid.md` debugging files for invalid output;
- `run_check_batch.py` supports page × agent × model execution for one selected provider;
- `run_check_batch.py` supports rotating scheduled selection;
- `run_check_batch.py` can keep validation rejections nonfatal when `--allow-rejected-check-outputs` is used;
- `run_check_batch.py` can keep transient provider-side availability failures nonfatal when `--allow-provider-failures` is used while keeping actionable provider failures fatal;
- `issue_manager.py` implements page-plus-agent issue routing;
- `issue_manager.py` implements stable comment identity;
- `issue_manager.py` updates matching existing comments instead of posting duplicates;
- `.github/workflows/check-agent-signal-collector.yml` runs scheduled rotating LLM check-agent collection;
- scheduled runs can create or update GitHub issues/comments in `post` mode;
- scheduled provider/model rotation includes seven active Cerebras, SambaNova, OpenRouter, and Gemini provider/model specs, with no active Groq slot;
- Gemini uses `gemini-3.1-flash-lite` as the current scheduled signal-generation default;
- scheduled signal-generation runs use `max_completion_tokens=3000` in the canonical workflow when no manual override is supplied;
- generated output paths are ignored by `.gitignore`;
- `close-page-hygiene-signal-issue-v1.0.0.md` exists as the manual issue-review and resolution prompt for `page-hygiene-checker` issues;
- `close-language-style-signal-issue-v1.0.0.md` exists as the manual issue-review and resolution prompt for `language-style-checker` issues;
- the earlier plan for a third `page-structure-checker` closure prompt has been discarded;
- `resolve-page-hygiene-signal-issue-v1.2.1.md` exists as the automated resolver prompt for `page-hygiene-checker` issues;
- `resolve-language-style-signal-issue-v1.2.1.md` exists as the automated resolver prompt for `language-style-checker` issues;
- `resolve_signal_issue.py` implements automated resolver orchestration;
- `.github/workflows/phase-2-signal-resolver.yml` runs scheduled and manual automated signal resolution;
- the automated resolver schedule is one scheduled attempt every four hours;
- the automated resolver keeps `gemini-3.5-flash` as the primary Gemini resolver model;
- the automated resolver workflow uses `gemini-2.5-flash` as a one-shot immediate fallback model only for provider-unavailability or 503-like primary Gemini failures;
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

Update the canonical Phase 2 methodology page to reflect the current resolver schedule, primary Gemini resolver model, immediate fallback-model behavior, provider rotation, workflow naming, retry policy, and actionable-failure behavior.

Suggested commit message:

```bash
docs(phase-2): align resolver fallback methodology
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
- conservative scheduled LLM execution works with the current seven-slot rotation across Cerebras, SambaNova, OpenRouter, and Gemini;
- the two manual issue-review and resolution prompts for the LLM-based agents exist and are documented;
- the absence of a dedicated `page-structure-checker` closure prompt is documented as intentional;
- the two automated resolver prompts for LLM-based signal issues exist and are documented;
- the automated resolver can select eligible issues, validate strict JSON plans, apply accepted exact edits, reject unsafe or out-of-scope signals for automation, create PRs, enable squash auto-merge, and close source signal issues;
- the automated resolver schedule, primary Gemini model, and fallback-model behavior are documented;
- the repository permissions and branch-protection settings allow the automated resolver workflow to complete its intended path.

## Generation and review log

- Phase 2 revised from a broader check-and-future-resolution architecture into a simplified lightweight check-agent infrastructure.
- The simplified Phase 2 target has exactly three check agents: one deterministic Python agent and two LLM-based agents.
- The deterministic Python agent is `page-structure-checker`.
- The two LLM-based agents are `page-hygiene-checker` and `language-style-checker`.
- The `page-structure-checker` runs after canonical stereotype page modifications and blocks structural regressions in CI.
- The `page-structure-checker` now validates the `Generation and Review Log` table schema.
- The two LLM-based check agents run periodically through the scheduled rotating workflow.
- The supported LLM signal-generation provider adapters are `groq`, `gemini`, `cerebras`, `sambanova`, and `openrouter`.
- Gemini support is documented inline in this Phase 2 page rather than split into a separate provider-only methodology page.
- The current scheduled Gemini model for Phase 2 check-agent signal generation is `gemini-3.1-flash-lite`.
- The scheduled provider/model rotation includes seven active provider/model specs across Cerebras, SambaNova, OpenRouter, and Gemini; Groq is retained as provider support but has no active scheduled slot.
- Gemini runs use reduced-thinking configuration to improve strict-format output reliability.
- The prompts target 140-character `Location` fragments while the validator hard limit remains 160 characters.
- Issue routing is one GitHub issue per page and check agent.
- Different providers and models executed by the same agent for the same page create comments in the same issue.
- Stable comment identity is implemented with page, agent, provider, model, prompt, and commit.
- Matching existing comments are updated instead of duplicated.
- Manual signal-review and issue-resolution support is documented for `page-hygiene-checker` and `language-style-checker` through two ChatGPT prompts.
- The planned `page-structure-checker` closure prompt was discarded; deterministic page-structure signals remain subject to direct maintainer review.
- Automated signal resolution is implemented for `page-hygiene-checker` and `language-style-checker` issues.
- Automated resolver prompts return strict JSON plans and classify non-accepted cases as `reject_for_phase_2_automation`.
- The automated resolver keeps `gemini-3.5-flash` as the primary Gemini resolver model.
- The automated resolver workflow uses `gemini-2.5-flash` once as an immediate fallback model only for provider-unavailability or 503-like primary Gemini failures.
- The automated resolver schedule is one scheduled attempt every four hours.
- Accepted automated resolver edits must be exact local replacements and pass deterministic validation.
- Accepted automated resolver edits are logged as rows in the `Generation and Review Log` table.
- Automated resolver PRs are updated by rebase and configured for squash auto-merge after required checks pass.
- Automated resolver source issues are commented on and closed after resolver completion.
- Conceptual validation, source-faithfulness validation, cross-page semantic comparison, and OntoUML/UFO semantic validation remain outside Phase 2.

---

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md)
