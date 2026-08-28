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
prompts/phase-2/resolve-page-hygiene-signal-issue-v1.2.2.md
prompts/phase-2/resolve-language-style-signal-issue-v1.2.2.md
```

The resolver operates only on signal issues produced by these check agents:

```text
page-hygiene-checker
language-style-checker
```

It does not support `page-structure-checker`.

### Resolver issue selection

When no issue is supplied manually, the resolver considers open eligible issues for the supported check agents in oldest-first order. It selects the first issue that has active valid signal comments and no terminal attempt for the same content-addressed resolver identity.

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

An active signal comment must carry a content-addressed task marker whose task is completed and published in `data/phase-2/task-state.json`. The task must target the issue's agent and page, and its agent-scoped content hash must match the current page. This deterministically excludes obsolete, superseded, unpublished, and untracked comments from resolver input.

The compact resolver input contains the issue number, title, agent, reviewed page, active signal provenance and bodies, and the current page content. It does not repeat the issue body, comment authors, timestamps, URLs, or inactive comments.

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

The top-level `overall_decision` is a deterministic summary of the signal-group decisions. After parsing the model response, the wrapper derives it as follows:

```text
at least one signal group has decision: accept
→ overall_decision: accepted_changes

no signal group has decision: accept
→ overall_decision: no_accepted_changes
```

If the model-provided value is missing or differs from the derived value, the wrapper normalizes `overall_decision` before full plan validation. The normalization does not change any signal-group decision, reason code, rationale, edit, or issue comment. All ordinary plan validation remains in effect, including exact-match validation for accepted edits and `{{PR_URL}}` consistency.

The wrapper derives this value only when `signal_groups` is a list of objects with recognized group-decision values. Invalid group structures or decisions are not concealed by normalization and continue to fail ordinary plan validation.

When `overall_decision` is normalized, the wrapper records the original and derived values in the workflow log and in:

```text
.tmp/phase-2/resolver/issue-<issue-number>-normalization.txt
```

The normalized plan is also preserved as:

```text
.tmp/phase-2/resolver/issue-<issue-number>-normalized-plan.json
```

### Resolver provider and fallback behavior

The resolver script supports these providers:

```text
groq
gemini
```

The resolver script default provider and model remain:

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

The scheduled resolver workflow uses these defaults:

```text
primary provider: gemini
primary model: gemini-3.5-flash
primary max_completion_tokens: 8000

fallback provider: gemini
fallback model: gemini-3.6-flash
fallback max_completion_tokens: 6000
fallback thinking: low
fallback final output: only the strict JSON plan
```

The fallback behavior is implemented in `.github/workflows/phase-2-signal-resolver.yml`, not as a general `resolve_signal_issue.py` command-line option.

The workflow-level fallback sequence is:

```text
run resolver once with the selected primary provider/model
→ if the run succeeds, exit successfully
→ if the primary provider is Gemini and its provider-error artifact contains provider-unavailability or 503-like diagnostics, run Gemini gemini-3.6-flash once for the same issue
→ otherwise fail the workflow normally
```

The fallback is model-diverse but not provider-diverse. It avoids the Groq free-tier token-per-minute ceiling for full resolver inputs, but both resolver attempts still depend on Gemini service availability.

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
server disconnected
disconnected without sending a response
```

When the fallback path is taken, the workflow preserves the primary provider-error artifact by renaming the relevant file from:

```text
issue-<issue-number>-provider-error.txt
```

to:

```text
issue-<issue-number>-primary-provider-error.txt
```

Then it runs the Gemini `gemini-3.6-flash` fallback once.

The fallback does **not** hide non-provider failures:

- if the primary call fails for quota, rate-limit, authentication, configuration, invalid request, output-validation, plan-validation, GitHub, or other non-provider-unavailability reasons, the workflow fails normally;
- if the primary call fails for an unrecognized provider error that does not match the workflow marker pattern, the workflow fails normally;
- if the configured Gemini fallback model also fails, the workflow fails normally.

Manual dispatch can override the primary `provider` and `model`. The fallback remains fixed to Gemini `gemini-3.6-flash` and is used only when the selected primary provider is `gemini` and the primary failure matches provider-unavailability diagnostics. If the selected primary already is Gemini `gemini-3.6-flash`, the workflow skips fallback rather than making a duplicate provider call.

Both default resolver routes require `GEMINI_API_KEY` in GitHub Actions; local execution may use `GEMINI_API_KEY` or `GOOGLE_API_KEY`. A manually selected Groq primary still requires `GROQ_API_KEY`.

Both default routes use the configured low-thinking policy and suppress provider thoughts from the returned plan. The existing deterministic parser, normalizers, and plan validator remain authoritative for the resolver contract and page-dependent safety checks.

### Resolver attempt identity and persistence

Each provider call has a content-addressed identity containing:

```text
issue number
agent
page content hash
normalized active-signal snapshot hash
resolver prompt hash
resolver validator version
provider and model
request configuration hash
```

Terminal outcomes are emitted under `.tmp/phase-2/resolver-attempt-events` and aggregated idempotently into:

```text
data/phase-2/resolver-attempt-state.json
```

Provider failures after a request, invalid plans, deterministic execution failures, and completed attempts block the unchanged identity from another provider call. A pre-call withholding or configuration failure is recorded as `not_called` and does not falsely consume the logical attempt. A page change, active-signal change, prompt change, validator change, provider/model change, or request-configuration change produces a new attempt identity.

If a persisted unchanged primary Gemini attempt failed for recognized provider unavailability and the Gemini `gemini-3.6-flash` identity remains eligible, a later primary run emits the same fallback signal without calling the primary model again. Invalid Gemini plans are terminal validation outcomes and do not invoke the fallback.

Resolver provider calls emit the same replayable quota events as signal-generation calls. The workflow's always-running shared state-writer step aggregates quota events, task consequences, and resolver-attempt events against the latest branch state before committing them. Resolver preflight uses those quota observations and attempt records when reserving the shared Gemini `gemini-3.5-flash` and `gemini-3.6-flash` scheduler slots.

### Resolver accepted-change flow

When the plan contains accepted changes, the implemented flow is:

```text
read issue
→ read current reviewed page
→ call resolver prompt/provider
→ parse strict JSON
→ normalize harmless schema drift and derive overall_decision
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
→ normalize harmless schema drift and derive overall_decision
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
| `page-hygiene-checker` | `resolve-page-hygiene-signal-issue-v1.2.2` | `Phase 2 automated resolver: page-hygiene signals v1.2.2` |
| `language-style-checker` | `resolve-language-style-signal-issue-v1.2.2` | `Phase 2 automated resolver: language-style signals v1.2.2` |

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
- parses the JSON plan;
- normalizes harmless schema drift and derives `overall_decision` from signal-group decisions;
- validates the JSON plan;
- writes resolver diagnostic/plan artifacts under `.tmp/phase-2/resolver`;
- prints the plan;
- does not edit the reviewed canonical page;
- does not create a resolver branch or pull request;
- does not comment on or close the source issue.

The scheduled resolver workflow applies the same primary-provider and fallback-provider sequence in dry-run mode when manually dispatched with `dry_run: true`. Because dry-run still makes a real provider call, the workflow may persist quota observations through its always-running state-writer step. `resolve_signal_issue.py --dry-run` suppresses resolver-attempt event emission, so the dry run does not add a terminal resolver-attempt record. Those quota-state updates are distinct from page, branch, pull-request, or issue mutation.

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
| `provider` | Primary workflow provider: `gemini` or `groq`; default `gemini`. The fixed fallback always uses Gemini. |
| `model` | Primary provider model; default `gemini-3.5-flash`. |
| `dry_run` | Generate and validate a resolution plan without page, branch, pull-request, or issue mutation; operational quota/attempt state may still be persisted because a real provider call occurs. |

Workflow permissions:

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

The workflow checks out the repository with `secrets.PHASE2_AUTOMATION_TOKEN` and exposes the same secret as `GH_TOKEN` and `GITHUB_TOKEN` for resolver GitHub operations, including branch-write operations.

The fixed fallback reuses `GEMINI_API_KEY`; it requires no additional provider secret beyond the configured Gemini key.

Concurrency group:

```text
phase-2-operational-state-write
```

with:

```text
cancel-in-progress: false
```

The workflow uploads resolver plan artifacts from:

```text
.tmp/phase-2/resolver
.tmp/phase-2/quota-events
.tmp/phase-2/resolver-attempt-events
```

as:

```text
phase-2-resolver-plan
```

When normalization occurs, the uploaded artifact includes `issue-<issue-number>-normalization.txt` and `issue-<issue-number>-normalized-plan.json` in addition to the usual raw, parsed, final, or error artifacts produced by the resolver path.

---

← Previous: [Check Agents](check-agents.md) | [Phase 2 index](index.md) | Next: [LLM Provider Support](providers.md) →
