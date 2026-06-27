# Phase 2 — Lightweight Check-Agent and Automated Signal-Resolution Infrastructure

Phase 2 is the second documented project phase of **OntoUML According to the Machines**.

Its purpose is to provide lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages, plus a tightly bounded automated resolver for selected Phase 2 signal issues.

Phase 2 still does **not** perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, OntoUML/UFO semantic validation, or conceptual adequacy assessment. Phase 2 signals remain candidate observations until they are reviewed or resolved within the documented workflow.

This document reflects the repository state verified from committed repository files on **2026-06-26**, with the current repository commit:

```text
42d20ecf93dd1a366711f0a7f78018365e0a9fb8
```

That commit keeps `gemini-3.5-flash` as the primary automated Gemini resolver model, uses `gemini-2.5-flash` as an immediate fallback model only for provider-unavailability or 503-like primary Gemini failures, adds explicit resolver execution logging, and keeps scheduled automated resolver execution at one scheduled attempt every four hours.

This index page is the entry point for the split Phase 2 methodology documentation. The original single-page Phase 2 document was split into topical pages to improve readability, navigation, and maintenance while preserving the original content in the linked subpages.

## Phase 2 pages

| Page | Purpose |
|---|---|
| [Scope and architecture](overview.md) | Purpose, boundaries, architecture, implementation status, risks, prerequisites, generated-output policy, and excluded checks. |
| [Check agents](check-agents.md) | Detailed reference for `page-structure-checker`, `page-hygiene-checker`, and `language-style-checker`. |
| [Automated resolver](automated-resolver.md) | Automated signal resolver behavior, issue selection, fallback behavior, PR flow, review-log entries, and workflow details. |
| [Providers](providers.md) | LLM provider support, provider-specific notes, retry behavior, and resolver provider behavior. |
| [Signals and issues](signals-and-issues.md) | Signal terminology, signal output structure, validation/rejection policy, structured signal data, issue routing, issue bodies, and duplicate control. |
| [Execution and operations](execution-and-operations.md) | Batch execution, resolver commands, operator options, execution policy, free-model strategy, GitHub Actions policy, branch protection, and operational observations. |
| [Prompts and status](prompts-and-status.md) | Manual and automated prompt support, future work, migration status, next implementation steps, completion criteria, and generation/review log. |

## Preservation note

The split moves content; it does not reinterpret it. Any stale or internally inconsistent claims in the original document should be corrected in a separate documentation update.
