# Archived Phase 2 General Page-Reviewer Stack

This directory contains legacy Phase 2 artifacts from an earlier general page-reviewer architecture for **OntoUML According to the Machines**.

These files are archived for provenance. They are not part of the current active Phase 2 execution path.

## Status

Archived.

## Reason for archival

The current Phase 2 architecture uses lightweight check-agent infrastructure with exactly three check agents:

- `page-structure-checker`
- `page-hygiene-checker`
- `language-style-checker`

The archived artifacts belong to an older general page-reviewer stack centered on `general-page-checker` / `page-reviewer-v1.0.x`.

That older stack has been superseded by the active agent-aware check-agent stack.

## Active replacement

Use the current Phase 2 artifacts instead:

```text
.github/workflows/page-structure-check.yml
.github/workflows/phase-2-check-agents.yml
scripts/phase-2/check_agents/page_structure_checker.py
scripts/phase-2/run_check_agent.py
scripts/phase-2/run_check_batch.py
scripts/phase-2/issue_manager.py
scripts/phase-2/providers/groq.py
prompts/phase-2/page-hygiene-checker-v1.0.2.md
prompts/phase-2/language-style-checker-v1.0.2.md
```

## Archived contents

This archive bundle preserves the legacy general page-reviewer stack:

```text
configs/phase-2/review-batch.yml
scripts/phase-2/run_page_review.py
scripts/phase-2/run_review_batch.py
prompts/phase-2/stale/prompt-phase-2-page-reviewer-v1.0.0.md
prompts/phase-2/stale/prompt-phase-2-page-reviewer-v1.0.3.md
```

## Intentionally retained outside this archive

The file below was intentionally left in its original location:

```text
scripts/phase-2/providers/mock.py
```

It is not part of this archive move.

## Historical role

The archived stack supported an earlier Phase 2 model in which a general page-level reviewer inspected one canonical stereotype Markdown page and produced candidate review comments.

That approach was replaced by a more explicit check-agent architecture with narrower responsibilities, signal terminology, and page-plus-agent issue routing.

## Do not use for current automation

These files should not be used by current GitHub Actions workflows or current Phase 2 automation.

In particular:

- do not add these files back to active workflow entry points;
- do not treat `general-page-checker` as a current Phase 2 check agent;
- do not revive `Finding count`, `Finding`, or `F-001` terminology for current Phase 2 outputs;
- do not use this stack as evidence of the current Phase 2 methodology.

## Restoration policy

Restore files from this archive only if all of the following are true:

1. there is an explicit decision to inspect or reproduce the legacy general page-reviewer behavior;
2. the restored files are clearly marked as legacy or experimental;
3. current active workflows remain based on the three-agent Phase 2 architecture;
4. any restored dependency requirements are documented separately;
5. restoration does not reintroduce obsolete finding terminology into current check-agent outputs.

## Deletion policy

These archived files may be deleted later if the project decides that Git history is sufficient for preserving old runner and prompt versions.

Before deletion, run a repository-wide reference check, for example:

```bash
git grep -n "run_page_review\|run_review_batch\|review-batch.yml\|general-page-checker\|page-reviewer-v1.0"
```

Also confirm that:

- no open pull requests reference these artifacts;
- no open issues depend on them;
- no branch-protection status checks refer to the old workflow or runner names;
- the active Phase 2 workflows still pass;
- the project has an explicit policy for relying on Git history instead of in-tree archives.

## Notes

This archive is intentionally outside `docs/` so that it is not published as part of the MkDocs site.

It is intentionally grouped as one bundle because the config, scripts, and prompts belong to the same retired implementation path.
