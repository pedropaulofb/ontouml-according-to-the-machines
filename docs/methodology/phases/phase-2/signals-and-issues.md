# Phase 2 — Signals and Issues

← Previous: [LLM Provider Support](providers.md) | [Phase 2 index](index.md) | Next: [Execution and Operations](execution-and-operations.md) →

## Signal terminology

Phase 2 outputs are **signals**, not accepted findings.

Use:

```text
Signal count
Signal
S-001
S-002
S-003
```

Avoid:

```text
Finding count
Finding
F-001
```

Rationale: a Phase 2 signal is a candidate observation. It has not yet been accepted, rejected, deduplicated, or converted into an edit plan.

Resolver decisions are not expert validation. They are automation decisions over Phase 2 signals and use this terminology:

```text
accept
reject_for_phase_2_automation
accepted_changes
no_accepted_changes
```

A signal rejected for Phase 2 automation is not necessarily false. It may be out of scope, source-dependent, obsolete, insufficiently deterministic, unsafe for automated edit application, duplicate, or otherwise unsuitable for Phase 2 automation.

## Signal output structure

Each check-agent output should be one structured Markdown comment.

Required heading:

```markdown
## Check signal report: <agent> / <provider> / <model> — <review date>
```

Required metadata table:

```markdown
### Run metadata

| Field | Value |
|---|---|
| Agent | <agent-slug> |
| Provider | <provider> |
| Model | <model> |
| Prompt | <prompt-id or n/a> |
| Review date | <review date> |
| Reviewed page | <path> |
| Commit SHA | <sha> |
| Signal count | <number of emitted signal sections, or 0 if none> |
```

For LLM-based check agents, `Signal count` must exactly match the number of emitted `#### S-...` signal sections.

Required summary section:

```markdown
### Summary judgment

<agent-specific summary sentence>
```

Required scope section:

```markdown
### Scope

<agent-specific scope statement>
```

Required signal section:

```markdown
### Signals

#### S-001 — <short plain-text signal title>

- Category: <agent-specific category>
- Severity: <low | medium | high>
- Confidence: <low | medium | high>
- Location: Section: "<nearest heading, or Document root if no heading applies>"; Fragment: "<exact affected fragment, maximum 160 characters>"
- Observation: <single-line observation>
- Rationale: <single-line rationale>
- Recommendation: <single-line recommendation>
```

For LLM-based check agents, the prompt target for `Location` fragments is stricter:

```text
maximum 140 characters
```

The validator hard acceptance limit remains:

```text
maximum 160 characters
```

The lower prompt target gives the model a safety margin while preserving the existing validator invariant.

Agent-specific contracts may allow optional exact replacement fields:

```markdown
- current_text: "<exact current text copied from the page>"
- proposed_text: "<exact local replacement text>"
```

Optional replacement fields must be emitted together or omitted together. They must not be emitted as empty values, placeholders, `None`, or `N/A`.

For no-signal runs, the prompt still requires a full comment with `Signal count` set to `0` and this exact sentence under `### Signals`:

```markdown
None identified within the configured check-agent scope.
```

## Validation and rejection policy

`run_check_agent.py` validates every generated LLM issue comment before accepting it as a candidate output.

Validation checks include:

- report title;
- required sections;
- metadata values;
- prompt ID;
- provider and model identity;
- signal count;
- allowed categories;
- severity and confidence values;
- signal ID sequence;
- required field order;
- `Location` format;
- hard 160-character `Location` fragment limit;
- no unresolved template placeholders;
- no copied explanatory prompt text;
- no forbidden task checkboxes;
- no out-of-scope source-validation claims;
- no recommendations to mutate repository or issue state.

If validation fails, `run_check_agent.py` writes an invalid artifact and exits nonzero.

The invalid artifact path uses `.invalid.md`, for example:

```text
.tmp/phase-2/<agent>/<page-id>/issue-comment-<provider>-<model>.invalid.md
```

`run_check_batch.py` can treat validation failures as nonfatal when this flag is used:

```text
--allow-rejected-check-outputs
```

When this flag is active:

- rejected outputs are kept as artifacts;
- rejected outputs are not sent to `issue_manager.py`;
- rejected outputs are not posted as issue comments;
- the batch can still exit successfully if no fatal automation failure occurs.

Transient provider-side availability failures and empty provider responses can remain nonfatal when `--allow-provider-failures` is used. Quota, rate-limit, authentication, configuration, request-shape, unknown provider, issue-manager, and resolver failures remain fatal unless handled by retry logic or by the relevant wrapper.

## Structured signal data

Machine-readable signal data is currently agent- and version-dependent.

Current status:

- `page-structure-checker` emits YAML blocks because its output is generated deterministically by Python;
- the shared signal contract plus `page-hygiene-checker-v1.1.0` is Markdown-only;
- the shared signal contract plus `language-style-checker-v1.1.0` is Markdown-only;
- automated resolver prompts emit strict JSON resolution plans;
- resolver plans are written under `.tmp/phase-2/resolver/`;
- machine-readable signal blocks for LLM-based check-agent comments are deferred to a later prompt version or later tooling.

The Markdown text is for humans and issue readability. Structured blocks and resolver JSON plans are infrastructure for deterministic tooling.

## Issue routing model

The implemented Phase 2 issue routing model is one open GitHub issue per:

```text
page + check agent
```

Implemented issue title pattern:

```text
Check signal: <agent-slug>: <page-id>
```

Examples:

```text
Check signal: page-structure-checker: classes/event
Check signal: page-hygiene-checker: classes/event
Check signal: language-style-checker: classes/event
Check signal: page-structure-checker: relations/material
```

The page identity is derived from the reviewed page path:

```text
docs/stereotypes/classes/event.md -> classes/event
docs/stereotypes/relations/material.md -> relations/material
```

All provider/model outputs for the same page and same check agent are posted to the same open issue.

For example, if `page-hygiene-checker` runs with Groq and Gemini on `docs/stereotypes/classes/event.md`, both model reports are comments under:

```text
Check signal: page-hygiene-checker: classes/event
```

The issue manager currently searches only open issues with an exact matching title. Closed issues are not reused.

The automated resolver also requires this issue title pattern and currently selects only open issues for:

```text
page-hygiene-checker
language-style-checker
```

## Issue body pattern

When creating a new issue, the issue body uses this structure:

```markdown
# Check signal: <agent-slug>: <page-id>

## Reviewed page

`<docs/stereotypes/...>.md`

## Page identity

`<group>/<stereotype-id>`

## Check agent

`<agent-slug>`

## Purpose

Collect check-agent signal comments for this page and agent.

## Resolution model

Signals are candidate observations. They are not accepted findings until reviewed.

This issue may be resolved manually or by later resolution tooling.
```

## Comment identity and duplicate control

Phase 2 supports stable comment identity.

Stable identity fields:

```text
page
agent
provider
model
prompt
commit
```

The issue manager inserts a hidden marker into the posted comment:

```markdown
<!-- check-signal-comment
page: <reviewed page>
agent: <agent>
provider: <provider>
model: <model>
prompt: <prompt>
commit: <commit SHA>
-->
```

If a comment with the same stable identity already exists in the target issue, the system updates the existing comment instead of posting a new one.

If the commit SHA changes, a new comment may be posted because the reviewed page content may have changed.

---

← Previous: [LLM Provider Support](providers.md) | [Phase 2 index](index.md) | Next: [Execution and Operations](execution-and-operations.md) →
