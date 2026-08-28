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

Phase 2 includes two agent-specific automated resolver prompts:

```text
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.2.md
prompts/phase-2/resolve-language-style-signal-issue-v1.2.2.md
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
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.2.md
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
prompts/phase-2/resolve-language-style-signal-issue-v1.2.2.md
```

The current prompt file heading is:

```text
Phase 2 automated resolver: language-style signals v1.2.2
```

It may accept only deterministic, local, meaning-preserving editorial edits within the language-style checker scope:

- grammar;
- spelling;
- clarity;
- professional technical style;
- project/process self-reference in reader-facing prose.

It must reject conceptual validation, source-faithfulness validation, quote verification, citation-support assessment, cross-page consistency, citation/reference hygiene, Markdown hygiene, encoding hygiene, review-log hygiene, broad rewrites, and technical meaning changes for Phase 2 automation.

## Automated resolver provider fallback

The two agent-specific resolver prompts remain unchanged and are used by every supported resolver provider.

The default scheduled resolver sequence is:

```text
primary: gemini:gemini-3.5-flash
primary max_completion_tokens: 8000
fallback after recognized primary provider unavailability: gemini:gemini-3.6-flash
fallback max_completion_tokens: 6000
fallback thinking: low
provider_max_attempts per resolver call: 1
```

The secondary-model fallback is workflow orchestration, not a third resolver prompt. It targets the same issue and uses the same agent-specific resolver prompt. The fallback invocation re-reads the issue snapshot and the page from the unchanged workflow checkout before building its input.

Gemini calls suppress thought output and return only the strict JSON plan. The existing parser, deterministic normalization, plan validator, exact-one-match rule, page-structure check, and GitHub mutation sequence remain unchanged and provider-independent.

The resolver still fails closed when:

- provider authentication or configuration is invalid;
- quota or rate limits prevent completion;
- an unrecognized provider failure occurs;
- a generated plan is invalid;
- exact edit targets are absent or ambiguous;
- deterministic page-structure validation fails after applying accepted edits;
- branch, pull-request, auto-merge, issue-comment, or issue-closure operations fail.

No failed or invalid output is treated as a successful resolution.

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
- a stricter second workflow that closes source issues only after PR merge if issue-closure semantics are changed later;
- a cooldown or quarantine policy if repeatedly invalid oldest issues continue to cause head-of-line blocking.

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
- `check-signal-shared-contract-v1.0.0` defines the common Markdown signal contract;
- `page-hygiene-checker-v1.1.1` defines the page-hygiene-specific instructions;
- `language-style-checker-v1.1.0` defines the language-style-specific instructions;
- `run_check_agent.py` runs the two LLM check agents through an agent-aware contract;
- `run_check_agent.py` supports SambaNova, Groq, Gemini, and OpenRouter provider adapters;
- `run_check_agent.py` validates generated LLM output and writes `.invalid.md` debugging files for invalid output;
- `run_check_batch.py` supports page × agent × model execution for one selected provider;
- the quota-aware scheduler selects content-addressed tasks by eligibility and age;
- `run_check_batch.py` can keep validation rejections nonfatal when `--allow-rejected-check-outputs` is used;
- `run_check_batch.py` can keep transient provider-side availability failures nonfatal when `--allow-provider-failures` is used while keeping actionable provider failures fatal;
- `issue_manager.py` implements page-plus-agent issue routing;
- `issue_manager.py` implements current LLM stable comment identity with page, agent, provider, model, and content-addressed `task_id`, while retaining the older prompt/commit marker only for backward compatibility;
- `issue_manager.py` updates matching existing comments instead of posting duplicates;
- `.github/workflows/check-agent-signal-collector.yml` runs scheduled quota-aware LLM check-agent collection;
- the scheduled signal-collector workflow grants `contents: write` and `issues: write`;
- scheduled runs can create or update GitHub issues/comments in `post` mode;
- serialized lease and aggregation state commits require `PHASE2_AUTOMATION_TOKEN`;
- the configured signal queue contains 25 provider-model slots across SambaNova, Groq, Gemini, and OpenRouter;
- reconciliation produces 1,950 desired tasks from 39 pages, two LLM agents, and those 25 slots;
- configured signal-generation requests use the registry's per-slot completion cap, currently 3,000 tokens for all slots;
- transient generated runner, transport, work-plan, batch, and diagnostic outputs are ignored through `.gitignore`, while canonical state, compact history, statistics, and retained audit Markdown are intentionally tracked;
- task-state schema v2 stores durable terminal-event identity without requiring per-attempt result JSON files;
- machine event history is retained in monthly NDJSON ledgers under `data/phase-2/history/`;
- publication retries use retained validated Markdown rather than separate publication-payload JSON files;
- the two archived manual issue-review and resolution prompts remain available for `page-hygiene-checker` and `language-style-checker` issues;
- the absence of a dedicated `page-structure-checker` closure prompt is documented as intentional;
- `resolve-page-hygiene-signal-issue-v1.2.2.md` exists as the automated resolver prompt for `page-hygiene-checker` issues;
- `resolve-language-style-signal-issue-v1.2.2.md` exists as the automated resolver prompt for `language-style-checker` issues;
- `resolve_signal_issue.py` implements automated resolver orchestration;
- `.github/workflows/phase-2-signal-resolver.yml` runs scheduled and manual automated signal resolution;
- the automated resolver schedule is one scheduled attempt every four hours;
- the automated resolver keeps `gemini-3.5-flash` as the primary resolver model;
- the automated resolver uses Gemini `gemini-3.6-flash` as a secondary-model fallback only for recognized primary Gemini provider unavailability;
- the Gemini fallback uses low thinking, final-only output, and a 6,000-token completion cap;
- resolver inputs include only active published task-addressed signals for the current page identity;
- content-addressed resolver-attempt state prevents unchanged terminal attempts from repeatedly calling a provider;
- the automated resolver selects the oldest eligible open signal issue when no issue is provided;
- the automated resolver can run in dry-run mode;
- the automated resolver validates strict JSON plans;
- the automated resolver derives the redundant `overall_decision` from group decisions;
- the automated resolver preserves the exact-one-match validator for accepted `current_text`;
- the automated resolver applies accepted exact local edits;
- the automated resolver writes accepted-edit provenance as a `Generation and Review Log` table row;
- the automated resolver removes legacy bullet-style automated resolver log lines for the same issue;
- the automated resolver runs the page-structure checker before creating a PR;
- the automated resolver creates PRs for accepted changes;
- the automated resolver updates PR branches by rebase;
- the automated resolver enables squash auto-merge;
- the automated resolver comments on and closes source signal issues;
- accepted automated resolver PRs for both `page-hygiene-checker` and `language-style-checker` issues have been merged through the repository workflow.

Post-cutover status:

- Stage 9 full-branch validation and cutover preparation completed on 2026-08-20.
- PR #571 merged the recalibration to `main`.
- All four signal-generation provider secrets and `PHASE2_AUTOMATION_TOKEN` were exercised by the production collector path.
- Call-free scheduler planning completed with 1,950 desired tasks and no task-state mutation.
- A bounded production `post` canary ran at most one task per provider; Gemini, Groq, and SambaNova produced valid zero-signal outputs, while OpenRouter Nemotron Ultra was classified as `provider_unavailable` and deferred without failing the workflow.
- Aggregation persisted task, quota, publication, and model-run statistics state successfully.
- Post-cutover validation passed for the provider-model registry, task state, quota state, and resolver-attempt state.
- Both scheduled Phase 2 workflows are enabled.
- No operational recovery was required during cutover.
- On 2026-08-28, the previous statistics page was archived, live model-run statistics started a new collection epoch, task state was normalized to remove legacy artifact-path references, and the legacy per-attempt result, publication-payload, and rejection JSON stores were removed from the current tree. Existing Git history was deliberately retained.

Deferred outside Phase 2:

- additional check agents beyond the three Phase 2 agents;
- source-faithfulness validation;
- heavy semantic analysis;
- cross-page consistency validation;
- OntoUML/UFO semantic validation;
- model quorum evaluation;
- semantic patch planning;
- local/offline model integration.

## Recommended next implementation step

No further Phase 2 recalibration implementation step is pending. Continue normal scheduled operation using the queue-managed collector and automated resolver. Future work remains under Deferred outside Phase 2.

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
- transient generated runner, transport, work-plan, batch, and diagnostic outputs remain uncommitted, while canonical durable state/history/statistics/audit outputs are tracked according to the Phase 2 persistence policy;
- small batch execution works locally;
- page-structure CI blocks structural regressions;
- quota-aware scheduled LLM execution operates over all 1,950 desired tasks across the 25 configured SambaNova, Groq, Gemini, and OpenRouter slots;
- the two manual issue-review and resolution prompts for the LLM-based agents exist and are documented;
- the absence of a dedicated `page-structure-checker` closure prompt is documented as intentional;
- the two agent-specific automated resolver prompts exist and are documented;
- the automated resolver can select eligible issues, validate complete plans, safely normalize redundant schema drift, preserve exact edit constraints, apply accepted exact edits, reject unsafe or out-of-scope signals, create PRs, enable squash auto-merge, and close source signal issues;
- the automated resolver schedule, primary and fallback Gemini models, completion-token settings, attempt identity, and failure behavior are documented;
- the repository permissions, branch-protection settings, `PHASE2_AUTOMATION_TOKEN`, and `GEMINI_API_KEY` allow the default automated resolver workflow to complete its intended path.

## Generation and review log

- Phase 2 revised from a broader check-and-future-resolution architecture into a simplified lightweight check-agent infrastructure.
- The simplified Phase 2 target has exactly three check agents: one deterministic Python agent and two LLM-based agents.
- The deterministic Python agent is `page-structure-checker`.
- The two LLM-based agents are `page-hygiene-checker` and `language-style-checker`.
- The `page-structure-checker` runs after canonical stereotype page modifications and blocks structural regressions in CI.
- The `page-structure-checker` validates the `Generation and Review Log` table schema.
- The two LLM-based check agents run periodically through the quota-aware scheduled workflow.
- The supported LLM signal-generation provider adapters are `sambanova`, `groq`, `gemini`, and `openrouter`.
- The content-addressed queue contains 1,950 desired tasks across 39 pages, two LLM agents, and 25 configured provider-model slots.
- The scheduler selects eligible oldest work within shared and model-specific free-quota constraints rather than rotating by time.
- Gemini runs use reduced-thinking configuration to improve strict-format output reliability.
- Issue routing is one GitHub issue per page and check agent.
- Different providers and models executed by the same agent for the same page create comments in the same issue.
- Current content-addressed LLM comment identity is implemented with page, agent, provider, model, and `task_id`; the earlier prompt-and-commit marker remains only for backward compatibility.
- Matching existing comments are updated instead of duplicated.
- Manual signal-review and issue-resolution support is documented for `page-hygiene-checker` and `language-style-checker` through two archived ChatGPT prompts.
- The planned `page-structure-checker` closure prompt was discarded; deterministic page-structure signals remain subject to direct maintainer review.
- Automated signal resolution is implemented for `page-hygiene-checker` and `language-style-checker` issues.
- The active agent-specific automated resolver prompt IDs are `resolve-page-hygiene-signal-issue-v1.2.2` and `resolve-language-style-signal-issue-v1.2.2`.
- Automated resolver prompts return strict JSON plans and classify non-accepted cases as `reject_for_phase_2_automation`.
- The automated resolver keeps `gemini-3.5-flash` as the primary resolver model.
- The automated resolver workflow uses Gemini `gemini-3.6-flash` as a one-shot secondary-model fallback only for recognized primary Gemini provider unavailability.
- The Gemini fallback uses low thinking, final-only output, and a 6,000-token completion cap.
- Content-addressed resolver-attempt state prevents unchanged terminal attempts from repeatedly calling a provider.
- The resolver deterministically derives `overall_decision` from signal-group decisions.
- The exact-one-match rule remains unchanged; ambiguous targets are never selected automatically.
- The automated resolver schedule is one scheduled attempt every four hours.
- Accepted automated resolver edits must be exact local replacements and pass deterministic validation.
- Accepted automated resolver edits are logged as rows in the `Generation and Review Log` table.
- Automated resolver PRs are updated by rebase and configured for squash auto-merge after required checks pass.
- Automated resolver source issues are commented on and closed after resolver completion.
- The 2026-08-28 storage cutover replaced legacy per-attempt/per-rejection JSON persistence with task-state v2 durable event identity, compact monthly NDJSON history, retained Markdown, and a fresh statistics collection baseline while preserving the pre-reset statistics page as historical documentation.
- Conceptual validation, source-faithfulness validation, cross-page semantic comparison, and OntoUML/UFO semantic validation remain outside Phase 2.

---

← Previous: [Execution and Operations](execution-and-operations.md) | [Phase 2 index](index.md)
