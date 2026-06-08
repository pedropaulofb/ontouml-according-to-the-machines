# Phase 2 — Current Check-Agent Implementation

This note records the current implementation state of Phase 2 after the signal-terminology migration, the addition of the Python-based `page-structure-checker`, and the addition of the standalone `page-hygiene-checker` prompt.

## Implemented files

The current Phase 2 implementation includes:

```text
prompts/phase-2/prompt-phase-2-page-reviewer-v1.0.3.md
prompts/phase-2/page-hygiene-checker-v1.0.0.md
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/issue_manager.py
scripts/phase-2/run_review_batch.py
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/providers/__init__.py
scripts/phase-2/providers/groq.py
scripts/phase-2/providers/mock.py
```

## Completed migration items

The following Phase 2 migration items are now complete:

- the main runner, issue manager, batch runner, and mock provider use signal terminology;
- the current signal vocabulary is `Signal count`, `Signals`, and `S-001` identifiers;
- the standalone Python-based `page-structure-checker` exists;
- the standalone LLM prompt `page-hygiene-checker-v1.0.0` exists.

## Page Structure Checker

| Property | Value |
|---|---|
| Agent slug | `page-structure-checker` |
| Type | Deterministic Python |
| File | `scripts/phase-2/check_agents/page_structure_checker.py` |
| Provider metadata | `python` |
| Model metadata | `deterministic` |
| Prompt metadata | `n/a` |
| Applies changes | No |

The checker verifies the canonical stereotype-page skeleton. It checks:

- required headings;
- heading order;
- duplicate required headings;
- missing required sections;
- malformed required heading levels;
- unexpected level-2 sections;
- empty required sections where the project expects placeholder text.

It produces a Phase 2 check-signal report. It does not call an LLM and does not modify canonical pages.

## Page Hygiene Checker Prompt

| Property | Value |
|---|---|
| Agent slug | `page-hygiene-checker` |
| Type | Lightweight LLM prompt |
| Prompt | `prompts/phase-2/page-hygiene-checker-v1.0.0.md` |
| Runner integration | Pending |
| Batch integration | Pending |
| Applies changes | No |

The prompt checks only visible page-hygiene issues in Markdown content that is present. It covers:

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

The prompt explicitly excludes content correctness, source validation, required top-level section checking, grammar/style review except for visible Markdown or encoding artifacts, cross-page consistency, and repository actions.

The current prompt version is Markdown-only. It does not emit YAML, JSON, or a separate machine-readable artifact.

## Current limitations

The implementation is not yet fully agent-aware.

Current limitations:

- issue routing is still page-level, not page-plus-agent;
- repeated runs still post new comments rather than updating matching comments;
- the batch runner is still page/model oriented, not page/check-agent/model oriented;
- `page-structure-checker` is standalone and not yet part of the batch runner;
- `page-hygiene-checker-v1.0.0` is standalone and not yet wired into an agent-aware runner or batch configuration;
- `language-style-checker` is still pending;
- manual GitHub Actions execution is still pending;
- scheduled execution is still pending.

The general `run_page_review.py` runner has been migrated to check-signal validation, but it still points to the legacy general page-reviewer prompt `prompt-phase-2-page-reviewer-v1.0.3.md`. That prompt should be replaced or parameterized before relying on real LLM runs through the general runner.

## Next implementation priorities

The next implementation priorities are:

1. implement agent-aware issue routing;
2. implement stable comment identity and update-existing behavior;
3. add runner and batch support for page/check-agent/model execution;
4. create the `language-style-checker` prompt;
5. run small local agent-aware batches before issue posting;
6. add manual GitHub Actions execution after local stability;
7. add conservative scheduling only after duplicate-comment control exists.

## Recommended next commit

The next code-oriented commit should be:

```bash
feat(phase-2): route check signals by page and agent
```

That change should update `issue_manager.py` so that Phase 2 issues are keyed by:

```text
page + check agent
```

Recommended title pattern:

```text
Phase 2 check: <agent-slug>: <page-id>
```

Examples:

```text
Phase 2 check: page-structure-checker: classes/event
Phase 2 check: page-hygiene-checker: classes/event
Phase 2 check: language-style-checker: classes/event
```
