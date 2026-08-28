# Phase 2 — Lightweight Check-Agent and Automated Signal-Resolution Infrastructure

Phase 2 is the second documented project phase of **OntoUML According to the Machines**.

Its purpose is to provide lightweight deterministic and API-based review infrastructure for existing canonical stereotype pages, plus a tightly bounded automated resolver for selected Phase 2 signal issues.

Phase 2 still does **not** perform deep content validation, source-faithfulness analysis, cross-page semantic comparison, OntoUML/UFO semantic validation, or conceptual adequacy assessment. Phase 2 signals remain candidate observations until they are reviewed or resolved within the documented workflow.

The current implementation follows the accepted [quota-aware multi-provider recalibration RFC](recalibration-rfc.md), as amended by its [2026-08-28 post-cutover amendment](recalibration-rfc.md#post-cutover-amendment-2026-08-28). It replaces time-based provider/model rotation with a content-addressed queue over 39 pages, two LLM check agents, and 25 configured provider-model slots: 1,950 desired tasks for the current configuration generation.

This index page is the entry point for the split Phase 2 methodology documentation. The original single-page Phase 2 document was split into topical pages to improve readability, navigation, and maintenance while preserving the original content in the linked subpages.

## Phase 2 pages

| Page | Purpose |
|---|---|
| [Accepted recalibration RFC](recalibration-rfc.md) | Original normative requirements and staged implementation plan, plus the accepted 2026-08-28 post-cutover amendment that supersedes selected requirements. |
| [Scope and architecture](overview.md) | Purpose, boundaries, architecture, implementation status, risks, prerequisites, generated-output policy, and excluded checks. |
| [Check agents](check-agents.md) | Detailed reference for `page-structure-checker`, `page-hygiene-checker`, and `language-style-checker`. |
| [Exact-replacement safety](exact-replacement-safety.md) | Authoritative current behavior for deterministic signal-publication checks, resolver revalidation, atomic-group demotion, and automatic-rejection issue records. |
| [Automated resolver](automated-resolver.md) | Automated signal resolver behavior, issue selection, fallback behavior, PR flow, review-log entries, and workflow details. |
| [Providers](providers.md) | LLM provider support, provider-specific notes, retry behavior, and resolver provider behavior. |
| [Signals and issues](signals-and-issues.md) | Signal terminology, signal output structure, validation/rejection policy, structured signal data, issue routing, issue bodies, and duplicate control. |
| [Execution and operations](execution-and-operations.md) | Batch execution, resolver commands, operator options, execution policy, free-model strategy, GitHub Actions policy, branch protection, and operational observations. |
| [Model run statistics](model-run-statistics.md) | Cumulative provider/model execution counters for the scheduled check-agent signal collector. |
| [Prompts and status](prompts-and-status.md) | Manual and automated prompt support, future work, migration status, next implementation steps, completion criteria, and generation/review log. |

## Authority note

The provider-model registry, task state, quota state, resolver-attempt state, statistics state, workflows, and scripts are authoritative for executable behavior. The accepted RFC **as amended by its 2026-08-28 post-cutover amendment** is authoritative for recalibration requirements. Generated model-run statistics preserve inactive and retired rows for historical continuity; those rows are not active execution slots.
