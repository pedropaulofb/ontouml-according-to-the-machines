# Phase 2 — Automated Signal Resolver

← Previous: [Check Agents](check-agents.md) | [Phase 2 index](index.md) | Next: [LLM Provider Support](providers.md) →

## Automated signal resolver

The automated signal resolver is implemented by:

```text
scripts/phase-2/resolve_signal_issue.py
```

Its scheduled workflow is:

```text
.github/workflows/phase-2-signal-resolver.yml
```

Its resolver prompts are:

```text
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.1.md
prompts/phase-2/resolve-language-style-signal-issue-v1.2.1.md
```

The resolver operates only on signal issues produced by these check agents:

```text
page-hygiene-checker
language-style-checker
```

It does not support `page-structure-checker`.

### Resolver issue selection

When no issue is supplied manually, the resolver selects the oldest open eligible issue for the supported check agents.

Eligibility requires the issue title to match:

```text
Check signal: <agent-slug>: <page-id>
```

with `<agent-slug>` equal to one of:

```text
page-hygiene-checker
language-style-checker
```

and `<page-id>` under:

```text
classes/<id>
relations/<id>
```

Manual workflow dispatch may provide an explicit issue number or issue URL.

### Resolver decision model

The resolver prompts return strict JSON only.

Every signal group receives one of:

```text
accept
reject_for_phase_2_automation
```

There is no `defer` decision in automated resolution. Cases that would previously have been deferred are classified as:

```text
reject_for_phase_2_automation
```

with a concrete reason.

Accepted groups must use:

```text
reason_code: in_scope_exact_edit
```

Accepted edits must include:

```text
current_text
proposed_text
rationale
```

Rejected groups must have an empty `edits` array.

The wrapper validates that accepted `current_text` values occur exactly once in the current reviewed page before applying the edit.

### Resolver provider and fallback behavior

The resolver script supports these providers:

```text
groq
gemini
```

The resolver script default provider and model are:

```text
provider: gemini
model: gemini-3.5-flash
```

The resolver script also has:

```text
--provider-max-attempts
```

with default:

```text
1
```

The scheduled resolver workflow explicitly runs each resolver model invocation with:

```text
--provider-max-attempts 1
```

This means the scheduled resolver workflow does not perform a delayed retry or backoff loop for a failed resolver provider call.

The scheduled resolver workflow uses these Gemini model defaults:

```text
primary model: gemini-3.5-flash
fallback model: gemini-2.5-flash
```

The fallback behavior is implemented in `.github/workflows/phase-2-signal-resolver.yml`, not as a general `resolve_signal_issue.py` command-line option.

The workflow-level fallback sequence is:

```text
run resolver once with the selected primary provider/model
→ if the run succeeds, exit successfully
→ if the provider is gemini, the primary model differs from the fallback model, and the provider-error artifact contains provider-unavailability or 503-like diagnostics, run the fallback Gemini model once for the same issue
→ otherwise fail the workflow normally
```

Provider-unavailability detection scans resolver error artifacts under:

```text
.tmp/phase-2/resolver
```

for marker text matching diagnostics such as:

```text
503
ServiceUnavailable
service_unavailable
provider_unavailable
status.*unavailable
temporarily unavailable
```

When the fallback path is taken, the workflow preserves the primary provider-error artifact by renaming the relevant file from:

```text
issue-<issue-number>-provider-error.txt
```

to:

```text
issue-<issue-number>-primary-provider-error.txt
```

Then it runs the fallback model once.

The fallback does **not** hide non-provider failures:

- if the primary call fails for quota, rate-limit, authentication, configuration, invalid request, output-validation, plan-validation, GitHub, or other non-provider-unavailability reasons, the workflow fails normally;
- if the primary call fails for an unrecognized provider error that does not match the workflow marker pattern, the workflow fails normally;
- if the fallback model also fails, the workflow fails normally.

Manual dispatch can override `model` and `fallback_model`. If the selected primary model is already the same as `fallback_model`, the workflow does not run a fallback attempt.

### Resolver accepted-change flow

When the plan contains accepted changes, the implemented flow is:

```text
read issue
→ read current reviewed page
→ call resolver prompt/provider
→ parse strict JSON
→ validate plan
→ apply exact local replacements
→ add Generation and Review Log table row
→ run page-structure checker on the modified page
→ create branch
→ commit changed page
→ push branch
→ open pull request
→ update PR branch by rebase
→ enable squash auto-merge
→ comment on source issue
→ close source issue as completed
→ GitHub later merges PR after required checks pass
```

The local pre-PR validation step runs:

```text
python scripts/phase-2/check_agents/page_structure_checker.py
```

against the modified page and refuses to create a PR if the report has `Signal count > 0`.

The PR branch naming pattern is:

```text
phase-2/auto-resolve-issue-<issue-number>
```

The commit message pattern is:

```text
fix(phase-2): resolve <agent> signals for issue #<issue-number>
```

The PR title pattern is:

```text
Resolve Phase 2 <agent> signals for issue #<issue-number>
```

### Resolver no-accepted-change flow

When no signal group is accepted, the resolver:

```text
read issue
→ read current reviewed page
→ call resolver prompt/provider
→ parse strict JSON
→ validate plan
→ write resolver plan artifact
→ comment on source issue
→ close source issue as not_planned
```

No branch, commit, pull request, or page edit is created.

### Resolver review-log row

Accepted automated edits create a `Generation and Review Log` table row with this structure:

```markdown
| <date> | Phase 2 | Phase 2 automated resolver | Signal resolution | <resolver-prompt-id> | <resolver-prompt-title> | GitHub issue #<issue-number> | Applied accepted <agent> signal edits through automated Phase 2 resolution; not a conceptual or source-faithfulness validation. |
```

Current resolver prompt metadata as emitted by `resolve_signal_issue.py`:

| Check agent | Prompt ID | Prompt title |
|---|---|---|
| `page-hygiene-checker` | `resolve-page-hygiene-signal-issue-v1.2.1` | `Phase 2 automated resolver: page-hygiene signals v1.2.1` |
| `language-style-checker` | `resolve-language-style-signal-issue-v1.2.1` | `Phase 2 automated resolver: language-style signals v1.2.1` |

The `resolve-language-style-signal-issue-v1.2.1.md` prompt file heading uses `v1.2.1`. The current `resolve-page-hygiene-signal-issue-v1.2.1.md` path is the active wrapper route for page-hygiene resolution, while the wrapper metadata above is authoritative for review-log rows.

Legacy bullet-style resolver log entries are removed for the same issue when the resolver applies accepted edits.

### Resolver auto-merge behavior

The resolver enables squash auto-merge with:

```text
gh pr merge <pr-url> --repo <repo> --auto --squash --delete-branch
```

This means GitHub merges the PR only after required merge requirements are met.

The resolver also updates the PR branch before enabling auto-merge with:

```text
gh pr update-branch <pr-url> --repo <repo> --rebase
```

The source issue is closed after the resolver successfully creates the PR, updates the branch, enables auto-merge, and posts its closure comment. The source issue closure records that the Phase 2 resolution step is complete. It does not by itself prove that the PR has already merged.

### Resolver dry-run mode

Manual dispatch supports `dry_run: true`.

Dry-run mode:

- selects or reads the issue;
- calls the resolver LLM;
- parses and validates the JSON plan;
- writes the resolver plan artifact;
- prints the plan;
- does not modify files;
- does not create a branch;
- does not create a pull request;
- does not comment on or close the issue.

The scheduled resolver workflow applies the same primary-model and fallback-model sequence in dry-run mode when manually dispatched with `dry_run: true`; GitHub write actions remain disabled by the resolver script after successful plan validation.

### Resolver workflow

The automated resolver workflow is:

```text
.github/workflows/phase-2-signal-resolver.yml
```

Workflow display name:

```text
Automated signal resolver
```

Schedule:

```text
5 */4 * * *
```

This means it is scheduled once every four hours, at minute 5 UTC, for six scheduled attempts per UTC day.

Manual dispatch inputs:

| Input | Purpose |
|---|---|
| `issue` | Issue number or URL. Empty means oldest eligible open issue. |
| `provider` | `gemini` or `groq`; default `gemini`. |
| `model` | Provider model; default `gemini-3.5-flash`. |
| `fallback_model` | Fallback Gemini model used once when the primary Gemini model fails with provider unavailability; default `gemini-2.5-flash`. |
| `dry_run` | Generate and validate a resolution plan without GitHub writes. |

Workflow permissions:

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

Concurrency group:

```text
phase-2-automated-signal-resolver
```

with:

```text
cancel-in-progress: false
```

The workflow uploads resolver plan artifacts from:

```text
.tmp/phase-2/resolver
```

as:

```text
phase-2-resolver-plan
```

---

← Previous: [Check Agents](check-agents.md) | [Phase 2 index](index.md) | Next: [LLM Provider Support](providers.md) →
