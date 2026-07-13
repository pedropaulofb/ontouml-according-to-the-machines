# Phase 2 — Lightweight Check-Agent and Automated Signal-Resolution Infrastructure

Phase 2 is the second documented project phase of **OntoUML According to the Machines**.

Its purpose is to provide lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages, plus a tightly bounded automated resolver for selected Phase 2 signal issues.

Phase 2 still does **not** perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, OntoUML/UFO semantic validation, or conceptual adequacy assessment. Phase 2 signals remain candidate observations until they are reviewed or resolved within the documented workflow.

This document includes a historical repository-state snapshot verified from committed repository files on **2026-06-28**, at commit:

```text
fed1de9630ee6f09c93262971a3fd14b53aa34fb
```

That commit aligned the scheduled check-agent signal-collector documentation with the then-current provider/model rotation, the cron-offset rotation index calculation, the active LLM check-agent prompt versions, OpenRouter signal-generation support, and the separation between scheduled provider-failure classification and automated resolver fallback behavior. The current active scheduled signal-generation rotation is now a seven-slot rotation without Groq; Groq provider support remains available for explicit future or manual use.

This index page is the entry point for the split Phase 2 methodology documentation. The original single-page Phase 2 document was split into topical pages to improve readability, navigation, and maintenance while preserving the original content in the linked subpages.

## Phase 2 pages

| Page | Purpose |
|---|---|
| [Scope and architecture](overview.md) | Purpose, boundaries, architecture, implementation status, risks, prerequisites, generated-output policy, and excluded checks. |
| [Check agents](check-agents.md) | Detailed reference for `page-structure-checker`, `page-hygiene-checker`, and `language-style-checker`. |
| [Exact-replacement safety](exact-replacement-safety.md) | Authoritative current behavior for deterministic signal-publication checks, resolver revalidation, atomic-group demotion, and automatic-rejection issue records. |
| [Automated resolver](automated-resolver.md) | Automated signal resolver behavior, issue selection, fallback behavior, PR flow, review-log entries, and workflow details. |
| [Providers](providers.md) | LLM provider support, provider-specific notes, retry behavior, and resolver provider behavior. |
| [Signals and issues](signals-and-issues.md) | Signal terminology, signal output structure, validation/rejection policy, structured signal data, issue routing, issue bodies, and duplicate control. |
| [Execution and operations](execution-and-operations.md) | Batch execution, resolver commands, operator options, execution policy, free-model strategy, GitHub Actions policy, branch protection, and operational observations. |
| [Model run statistics](model-run-statistics.md) | Cumulative provider/model execution counters for the scheduled check-agent signal collector. |
| [Prompts and status](prompts-and-status.md) | Manual and automated prompt support, future work, migration status, next implementation steps, completion criteria, and generation/review log. |

## Preservation note

The split generally moves content without reinterpreting it. The exact-replacement safety page is a targeted current-behavior update and supersedes older general summaries only for exact-target publication, revalidation, and automatic-demotion semantics.
