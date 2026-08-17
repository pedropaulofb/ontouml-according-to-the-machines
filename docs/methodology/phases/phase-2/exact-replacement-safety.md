# Phase 2 — Exact-Replacement Safety

← Previous: [Check Agents](check-agents.md) | [Phase 2 index](index.md) | Next: [Automated Signal Resolver](automated-resolver.md) →

## Purpose

Phase 2 treats exact-replacement fields as optional automation instructions. A signal may describe one problem that occurs once or multiple times, but every published or applied exact-replacement target must identify its intended occurrence unambiguously.

This page is the authoritative Phase 2 reference for exact-target publication, resolver revalidation, and automatic group demotion. Where an older general status summary describes an ambiguous exact target as a whole-run plan-validation failure, this page supersedes that description for target-specific failures. Unrelated malformed plan structure remains fail-closed.

The active signal-generation prompt is composed from a shared contract and one agent-specific contract:

```text
prompts/phase-2/check-signal-shared-contract-v1.0.0.md
prompts/phase-2/page-hygiene-checker-v1.1.0.md
prompts/phase-2/language-style-checker-v1.1.0.md
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.2.md
prompts/phase-2/resolve-language-style-signal-issue-v1.2.2.md
```

The shared contract requires exact, unique targets, permits unsafe optional replacement fields to be omitted, and defines the repeated-problem and minimum-context interpretation once for both agents. The deterministic run-input wrapper supplies only compact run metadata and the agent-scoped page content.

## Signal-creation validation

`scripts/phase-2/run_check_agent.py` validates optional `current_text` and `proposed_text` fields against the full reviewed page before a generated report is eligible for publication.

The check-agent contract is:

- one signal may represent one problem with one or multiple occurrences;
- `current_text` and `proposed_text` remain optional and must appear together;
- a published `current_text` must be an exact contiguous page fragment with exactly one match in the full reviewed page, counting overlapping exact occurrences;
- a unique `current_text` must also share the same exact page occurrence with the signal's declared `Location` fragment under the declared `Location` section, so that it identifies the occurrence described by that signal rather than matching a fabricated location fragment, a different unique page fragment, or a same-text fragment in another section;
- the run-input reminder instructs models to use only the minimum surrounding context reasonably needed to make the intended occurrence unique;
- the signal limit applies to distinct problems, not to the number of occurrences of one problem;
- repeated problems may be reported without exact-replacement fields when one pair would be ambiguous, incomplete, or misleading.

When an otherwise valid generated signal contains a well-formed exact-replacement pair whose `current_text` has zero or multiple matches, or whose unique target does not share the same grounded page occurrence as the signal's declared `Location` fragment and section, the runner removes both optional fields only when the declared fragment is also found under the declared section in the full reviewed page. This section-aware grounding check prevents a hallucinated or stale replacement target from being stripped in a way that would accidentally turn an ungrounded report into a publishable signal. A grounded report remains useful as a non-automatable observation without publishing unsafe replacement instructions.

Unsafe-target sanitization applies only when the signal's original generated `Location` fragment is grounded under its declared section. Grounding-sensitive exact-field sanitization runs before schema-level `Location` normalization, so later whitespace collapsing or shortening of an overlong fragment cannot manufacture the evidence used to remove unsafe fields. This includes recognized sentinel placeholder values (`None`, `N/A`, and `Not applicable`): the runner removes the complete optional pair from a grounded signal, but leaves the pair visible when the original declared location is ungrounded so strict validation rejects the report rather than sanitizing it into apparent validity. Other malformed or incomplete pairs and unchanged pairs also remain visible to strict validation.

For `language-style-checker`, provider input remains scoped to reader-facing content. Exact-target validation uses the full reviewed page so that a target duplicated inside an excluded section is not incorrectly treated as unique.

## Resolver revalidation

`scripts/phase-2/resolve_signal_issue.py` validates non-page-dependent plan-level and group-level resolver structure after parsing and before any automatic demotion. This schema preflight preserves fail-closed handling for invalid identities, group decisions, reason codes, non-empty group references/rationales, rejected-group shape, and non-empty issue-comment shape.

PR-placeholder consistency is validated after target revalidation. This allows the wrapper to replace stale model commentary with its deterministic automatic-rejection comment when an accepted group is demoted, while still failing closed when a valid accepted plan reaches final validation without the required `{{PR_URL}}` placeholder.

Accepted edit-array and edit-local failures are deliberately left to atomic-group revalidation. A malformed or incomplete edit therefore demotes only its affected accepted group instead of failing independent valid groups. Only after the plan-level preflight passes does the wrapper revalidate accepted edits against the current page. This second check is required even when a target was valid at signal creation because the page may have changed while the issue remained open.

One accepted signal group may contain multiple edits for multiple occurrences of the same problem. Every edit must independently identify exactly one occurrence. The resolver also rejects duplicate or overlapping accepted targets.

## Atomic-group automatic demotion

Signal groups are atomic. If any edit in an accepted group cannot be applied safely and deterministically, the wrapper converts the complete group to:

```text
reject_for_phase_2_automation
```

Examples include:

- zero exact matches in the current page;
- multiple exact matches, including overlapping occurrences;
- empty or whitespace-only values, unchanged values, or recognized sentinel placeholders such as `None`, `N/A`, and `Not applicable`;
- duplicate or overlapping targets;
- another condition that prevents deterministic application.

The wrapper clears the demoted group's `edits` array and assigns a specific reason code, normally:

```text
no_current_page_match
not_deterministic_or_local
unsafe_edit
```

Only the affected atomic group is demoted. Independent accepted groups whose edits remain valid and unambiguous are preserved and applied. Groups that already fail edit-local or within-group validation are excluded before cross-group overlap checks, so spans from a group that will not be applied cannot incorrectly demote another group. Accepted edits are then applied by their validated original-page spans, from right to left, so replacement text introduced by an earlier edit cannot redirect a later edit to the wrong occurrence.

The wrapper records automatic demotions in:

```text
.tmp/phase-2/resolver/issue-<issue-number>-automatic-rejections.json
```

The raw parsed plan remains available separately, and the normalized plan records the deterministic post-processing result.

## Issue outcome

When automatic demotions occur, the wrapper generates a deterministic issue comment that preserves the resolver safety disclaimers and, when accepted edits remain, the exact agent-specific pull-request sentence required by the established page-hygiene or language-style resolver prompt. The comment separates:

- accepted groups that remain actionable;
- automatic deterministic wrapper rejections;
- groups explicitly rejected during normal LLM resolution.

The comment also states that automatic rejection is not a judgment that a signal is false and that the resolution did not perform source-faithfulness, conceptual, cross-page semantic, or OntoUML/UFO semantic validation.

If valid accepted groups remain, the resolver applies only those groups, creates the normal pull request, and records the automatic rejections in the issue comment.

If no valid accepted group remains, the resolver:

```text
does not modify the page
→ records every group disposition in the issue
→ states that the issue is no longer automatically actionable
→ closes the issue as not planned
```

This prevents a stale or ambiguous oldest issue from repeatedly blocking later scheduled resolver runs while preserving an auditable explanation of why no automated page change was made.

## Safety boundary

Automatic demotion is deterministic wrapper behavior, not an additional LLM decision. It never invents replacement text, chooses arbitrarily among multiple matches, or partially applies an atomic group.

Plan-level and group-level structure is validated before automatic demotion so that demotion cannot conceal an unrelated schema error. Accepted edit-array and edit-local failures are treated as atomic-group failures and are demoted locally. The final validator for the enforced plan-contract conditions then runs again after demotion and independently rejects recognized sentinel placeholders if the demotion layer is bypassed or later regresses. Invalid identity metadata, group structure, decisions or reason codes, empty or malformed group references/rationales, rejected-group shape, inconsistent final issue-comment placeholders, inconsistent final `overall_decision`, and other non-local schema failures remain fail-closed errors.
