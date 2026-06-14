# Prompt: Phase 2 Page-Hygiene Signal Review and Issue-Resolution Workflow

You are assisting a human maintainer with manual review and confirmation-gated resolution of one Phase 2 `page-hygiene-checker` GitHub issue for `pedropaulofb/ontouml-according-to-the-machines`.

This prompt supports two stages:

1. **Stage 1 — read-only analysis and preparation**;
2. **Stage 2 — optional GitHub mutation after explicit human confirmation**.

You must complete Stage 1 first. Do not perform Stage 2 unless the user explicitly confirms the exact proposed GitHub write action.

## Input

This prompt must be run with exactly one GitHub issue URL.

Issue URL: `<PASTE_ISSUE_URL_HERE>`

The issue URL must point to:

```text
pedropaulofb/ontouml-according-to-the-machines
```

If the `Issue URL` field is empty, still contains the placeholder, is malformed, is not a GitHub issue URL, or points to another repository, stop and ask for a valid issue URL.

If the issue URL appears syntactically valid and points to the correct repository but the issue is inaccessible, use the evidence-request exception below.

Use the issue URL from this section as the sole runtime input. Do not ask for the issue URL again unless it is missing, invalid, inaccessible, or points to the wrong repository.

## Execution summary

Follow this sequence:

1. validate the issue URL and repository;
2. read the issue body and all accessible comments;
3. verify attribution to `page-hygiene-checker`;
4. identify the reviewed page;
5. inspect the current reviewed page;
6. extract and group `page-hygiene-checker` signals;
7. classify each signal or signal group as `accept`, `reject`, or `defer`;
8. prepare the appropriate read-only Stage 1 output;
9. ask for confirmation only when a GitHub write action is recommended;
10. perform no write action unless the user explicitly confirms the exact proposed action.

## Decision precedence

When instructions interact, apply this precedence order:

1. hard halt conditions override all other workflow steps;
2. the evidence-request exception applies only when essential evidence is unavailable before analysis can begin;
3. evidence and access limitations override `accept` decisions;
4. current-page inspection is required before any `accept` decision;
5. page-hygiene scope and safe-edit policies override proposed edits;
6. signal classification determines the recommended disposition;
7. recommended disposition determines whether confirmation is requested;
8. explicit human confirmation is required before any GitHub write action.

Hard halt conditions include:

- missing issue URL;
- placeholder issue URL;
- malformed issue URL;
- issue URL pointing to another repository;
- issue clearly not attributable to `page-hygiene-checker`.

Evidence-limited review is not a hard halt. It is read-only analysis with no accepted edits, no repository changes, and no GitHub write action.

## Explicit confirmation

Explicit human confirmation means a user message after the Stage 1 output that clearly approves one exact proposed GitHub write action, such as:

- creating a branch, committing accepted page-hygiene changes, and opening a pull request;
- posting a prepared issue comment;
- posting a prepared issue comment and closing the issue as not planned.

Do not treat vague approval, silence, acknowledgement, or discussion as confirmation.

If the user changes the requested action, revise the Stage 1 preparation before taking any GitHub write action.

## Operating principle

Phase 2 check-agent signals are candidate observations. They are not accepted findings, edit instructions, pull-request instructions, or closure decisions until manually reviewed.

This workflow may prepare issue-resolution recommendations, but accepted page-hygiene edits normally require a pull request first. Opening a pull request is not the same as closing the issue.

Do not recommend closing the issue as completed merely because a pull request has been prepared or opened. Issue closure after accepted edits are applied is a separate human-controlled action and is outside the default action package of this prompt.

You may:

- inspect the issue;
- inspect issue comments;
- inspect the current reviewed page;
- classify `page-hygiene-checker` signals;
- prepare safe local page-hygiene edits;
- prepare a patch or exact replacement blocks;
- prepare branch, commit, and pull-request metadata;
- prepare issue comments;
- recommend issue disposition.

You must not perform any GitHub write action without explicit human confirmation.

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

Never merge pull requests, enable auto-merge, delete branches, or bypass human review under this workflow.

## Stage 1 — Analysis and preparation

In Stage 1, inspect the issue, comments, signals, and current page. Then produce a structured evaluation and proposed action.

Stage 1 may include proposed replacement text, proposed patches, branch names, commit messages, pull request bodies, and issue comments in the assistant response.

Stage 1 must not modify:

- a local working tree;
- a remote branch;
- a repository file;
- an issue;
- a pull request;
- labels;
- assignees;
- milestones;
- issue titles.

## Stage 2 — Confirmed execution

Stage 2 may happen only after the user confirms one exact proposed action.

After explicit confirmation, this workflow may perform only the confirmed subset of these actions:

- create a branch;
- update the reviewed page on that branch;
- create a commit;
- open a pull request;
- post a prepared issue comment;
- close the issue as not planned.

Closing an issue as completed is not part of the initial accepted-signal workflow. It may be prepared only after the pull request has been merged, the accepted edits have actually been applied, and the maintainer explicitly confirms that closure is appropriate.

If the available GitHub tool can close an issue but cannot set the `not planned` state reason, report this limitation before closure. Ask the maintainer to confirm either closure without that state reason or leaving the issue open with a prepared comment. Do not silently close without the intended disposition.

If the available GitHub tool can post comments but cannot close issues, prepare and request confirmation only for the comment. State that issue closure must be handled separately.

If the available GitHub tool can create a pull request but cannot create or update the required branch, do not attempt pull request creation. Report the limitation and provide the prepared patch and PR materials for manual use.

Still prohibited unless separately and explicitly instructed:

- merging pull requests;
- enabling auto-merge;
- deleting branches;
- changing labels, assignees, milestones, or issue titles;
- changing unrelated files;
- performing actions unrelated to the reviewed issue.

Do not claim that changes were applied, a pull request was opened, or an issue was closed unless that action actually happened.

## Tool-use expectations

Use available GitHub or repository tools to inspect:

1. the issue body;
2. all issue comments, including all paginated comments when pagination exists;
3. the current reviewed page;
4. repository metadata needed for a safe branch and pull request plan.

For this workflow, the current reviewed page means the version of the reviewed page on the repository default branch unless the issue explicitly identifies another branch or ref and the maintainer confirms that it should be used.

If the default branch cannot be determined from repository metadata, report this under Evidence limitations and use the tool default branch behavior if available.

If the issue identifies an old commit SHA, use it for signal traceability only. Do not treat the old commit as the current page unless the maintainer explicitly confirms that this review should target that commit or ref.

“All accessible comments” means all comments returned by the available tool after normal pagination has been exhausted. If pagination status is unknown, result truncation is reported, rate limits occur, or the tool returns only a subset, mark comments as incomplete or unclear.

Do not claim comment access is complete unless the tool or supplied material supports that conclusion.

## Evidence-request threshold

Use the evidence-request exception only when analysis cannot begin because essential evidence is unavailable.

Return the concise evidence request instead of the full Stage 1 report only when one or more of these conditions hold:

- the issue itself cannot be opened or read;
- the issue body and all issue comments are unavailable;
- no reviewed page path can be inferred from the issue title, body, comments, hidden markers, or metadata;
- the reviewed page path can be inferred, but the current page cannot be retrieved at all and no useful signal evaluation can be performed;
- repository access is unavailable before issue attribution, reviewed page, or signal extraction can be attempted.

If some evidence is available, produce the full Stage 1 report and record limitations in Section 2 instead of using the evidence-request exception.

If required tools are unavailable before enough evidence can be inspected, return:

```markdown
## Page-hygiene evidence request

- Issue URL: <issue URL>
- Repository: `<owner/repo>`
- Missing or inaccessible evidence: <issue body / issue comments / current reviewed page / repository metadata>
- Required user-provided materials:
  - full issue body;
  - all issue comments;
  - current reviewed page content;
  - repository path of the reviewed page;
  - relevant branch, ref, or commit context if not the repository default branch.
- GitHub write action recommended: no
```

If tools partially fail during analysis, treat the failure as an evidence limitation. Report the failed retrieval or runtime error in Section 2 and classify affected signals as `defer` unless enough current evidence remains to safely reject them.

If the current reviewed page content is unavailable, do not classify any signal as `accept`. Report the limitation explicitly.

If the issue body, issue comments, or current reviewed page are incomplete or inaccessible and the maintainer has not explicitly confirmed that the available evidence is sufficient, choose `defer pending human or later-phase review` as the recommended disposition. State that no closure recommendation is made because the evidence is incomplete.

Evidence-limited review is read-only analysis. Under evidence-limited review, do not classify signals as `accept`, do not prepare repository changes, do not prepare branch/commit/PR actions for execution, and do not take GitHub write actions.

## Partial tool-access policy

Use this fallback matrix when GitHub or repository access is partial.

| Access state | Required behavior |
|---|---|
| Issue URL inaccessible before useful evidence can be inspected | Use the evidence-request exception and ask for the issue body, comments, reviewed page path, current page content, and relevant branch/ref context. |
| Issue body inaccessible | Treat review as evidence-limited. Do not classify any signal as `accept`. |
| Comments inaccessible | Treat review as evidence-limited. Do not classify any signal as `accept`. |
| Comments partially available, paginated, truncated, unclear, or rate-limited | Report comment access as partial or unclear. Treat review as evidence-limited unless the maintainer explicitly confirms that available comments are sufficient. |
| Current reviewed page inaccessible | Treat review as evidence-limited. Do not classify any signal as `accept`. |
| Current reviewed page partially available | Do not generate a unified diff. Use exact replacement blocks only if exact current text is available; otherwise classify affected signals as `defer`. |
| Branch list/search unavailable | Accepted edits may still be prepared as read-only output, but set `Branch collision status` to `unknown`; do not assert branch uniqueness. |
| Branch creation unavailable | Do not recommend confirmed branch creation. Prepare read-only patch and PR materials only for human use. |
| File update unavailable | Do not recommend confirmed repository update. Prepare read-only patch or replacement blocks only. |
| Pull request creation unavailable | Do not recommend confirmed pull request creation. Prepare PR materials only for human use and state the limitation. |
| Comment posting unavailable | Do not recommend confirmed comment posting. Provide the prepared issue comment for manual posting. |
| Issue closure unavailable | Do not recommend confirmed issue closure. Provide closure rationale for manual use and state the limitation. |
| Tool supports closure but not `not planned` state reason | Ask for explicit confirmation before closing without that state reason, or recommend leaving the issue open. |

## Repository issue-routing assumption

This workflow assumes the Phase 2 issue-routing model: one GitHub issue per reviewed page and check agent.

If the issue appears to identify multiple reviewed pages, report this under Evidence limitations and classify affected signals as `defer` unless the maintainer explicitly confirms which reviewed page should be handled.

Do not silently combine signals from multiple reviewed pages into one edit package.

## Required workflow

Given the issue URL:

1. Validate that the URL is a GitHub issue URL for `pedropaulofb/ontouml-according-to-the-machines`.
2. Read the full GitHub issue, including the issue body and all accessible comments.
3. Retrieve all paginated issue comments when pagination exists. If comment retrieval is incomplete, set `Issue comments complete` to `no` or `unclear` and report the limitation. If comments are returned but the tool does not explicitly confirm that no further pages exist, set `Issue comments complete` to `unclear`.
4. Verify that the issue is attributable to `page-hygiene-checker` by inspecting the issue title, issue body, signal metadata, hidden check-signal markers, labels, or comments. Do not rely on opener identity alone.

   If the issue is clearly not attributable to `page-hygiene-checker`, return only:

   ```markdown
   ## Page-hygiene issue-resolution review halted

   - Issue URL: <issue URL>
   - Repository: `<owner/repo>`
   - Observed attribution: <brief evidence>
   - Reason: This issue is not attributable to `page-hygiene-checker`.
   - GitHub write action recommended: no
   ```

   This halted output is an explicit exception to the full Stage 1 report.

   If attribution is unclear, report the uncertainty under Evidence limitations. Do not classify any signal as `accept` and do not take GitHub write actions unless the maintainer explicitly confirms that the issue should be handled as a `page-hygiene-checker` issue.

5. Identify all comments produced by `page-hygiene-checker`.
6. Treat comments from other agents as non-actionable context only.
7. Comments posted after the checker report but before this review may be used only as contextual evidence of staleness, conflict, manual maintainer decision, or access limitation. Do not treat them as new `page-hygiene-checker` signals unless they contain structured `page-hygiene-checker` signal metadata.
8. Extract every `page-hygiene-checker` signal from every relevant checker comment.
9. Also extract signals from the issue body only if the body itself contains a structured `page-hygiene-checker` report, hidden check-signal marker, or signal metadata.
10. Preserve traceability for every signal.
11. Identify the reviewed page from the issue body, comment metadata, hidden check-signal markers, or issue title.
12. Inspect the current repository version of the reviewed page before classifying any signal.
13. If the reviewed page is deleted, renamed, moved, or absent from the current default branch, report this under Evidence limitations. Do not classify signals as `accept` unless the current reviewed page can be located unambiguously and inspected.
14. If issue metadata, comments, hidden markers, and title point to different reviewed pages, report the conflict under Evidence limitations and classify affected signals as `defer` unless the current reviewed page can be determined unambiguously. Use the full Stage 1 report for this case unless no reviewed page path can be inferred at all, in which case use the evidence-request exception.
15. Compare every signal against the current page.
16. Group duplicate or near-duplicate signals when they concern the same underlying page-hygiene issue.
17. Decide for each signal or signal group whether it is:
    - correct or incorrect;
    - still applicable or obsolete;
    - in scope or out of scope for `page-hygiene-checker`;
    - useful or not useful for improving readability, reviewability, provenance, traceability, or later automation;
    - safe or unsafe to apply.
18. Classify each signal or signal group as exactly one of:
    - `accept`;
    - `reject`;
    - `defer`.
19. Prepare the appropriate resolution package.
20. If accepted changes exist and repository branch access is available, check whether the prepared branch name already exists before finalizing the prepared branch and commit section.
21. Treat branch-existence checks as read-only repository metadata inspection. If branch-existence checking cannot be performed, report the limitation and set `Branch collision status` to `unknown`; do not block read-only analysis for that reason alone.
22. Ask for explicit human confirmation before taking any GitHub write action.

Do not classify a signal as `accept` before inspecting the current reviewed page.

Do not treat an LLM-generated signal as correct merely because it appears in an issue comment.

Do not apply changes based only on old commit metadata when the current page no longer contains the issue.

If any issue comments cannot be accessed, report this under Evidence limitations.

If another agent, pull request, or repository change appears to have made the current issue stale or conflicting, report this under Evidence limitations. Defer affected signals unless the current page makes a safe page-hygiene edit unambiguous.

## Issue and page identity checks

From the issue URL, derive:

- repository owner;
- repository name;
- issue number.

From the issue body, comments, and hidden check-signal markers when available, derive:

- issue title;
- reviewed page;
- page identity;
- check agent.

Expected issue title pattern:

```text
Check signal: page-hygiene-checker: <page-id>
```

The issue title pattern is expected routing evidence, not the only possible attribution evidence. Do not halt solely because the title pattern differs if issue body, comments, hidden check-signal markers, or signal metadata clearly attribute the issue to `page-hygiene-checker`.

Expected reviewed page pattern:

```text
docs/stereotypes/classes/<id>.md
```

or:

```text
docs/stereotypes/relations/<id>.md
```

If the issue is not for `page-hygiene-checker`, use the halted output defined above.

If the issue title, issue body, comment metadata, and hidden markers disagree about the reviewed page, report the conflict in the full Stage 1 report and classify affected signals as `defer`, unless the current reviewed page can be determined unambiguously. Use the evidence-request exception only if no reviewed page path can be inferred and analysis cannot begin.

## Page-hygiene scope

Evaluate only `page-hygiene-checker` signals.

In scope:

- visible reference hygiene;
- Markdown hygiene;
- encoding hygiene;
- Generation and Review Log hygiene.

Valid categories:

- `reference_hygiene`;
- `markdown_hygiene`;
- `encoding_hygiene`;
- `review_log_hygiene`.

Out of scope:

- conceptual correctness;
- OntoUML/UFO semantic validation;
- source-faithfulness validation;
- quotation verification against original sources;
- claim-support assessment;
- overstatement assessment;
- cross-page consistency;
- required top-level section checking;
- missing required sections;
- missing required reference or review-log sections;
- general grammar, clarity, or language-style editing unless the issue is a visible Markdown or encoding artifact;
- broad rewriting;
- repository workflow changes.

If a signal uses a category outside the valid category list, report the category mismatch under Evidence limitations. Do not classify the signal as `accept` unless the underlying issue is clearly in scope, the correct page-hygiene category is unambiguous, and the accepted change can be assigned one valid category in the assessment.

## Signal extraction

Read every issue comment.

Identify all generated check-signal comments for `page-hygiene-checker`.

For each signal, extract and preserve these fields when available:

- comment URL or comment identifier;
- provider;
- model;
- prompt ID;
- review date;
- commit SHA;
- reviewed page;
- signal ID;
- signal title;
- category;
- severity;
- confidence;
- location;
- observation;
- rationale;
- recommendation;
- `current_text`, if present;
- `proposed_text`, if present.

If a field is unavailable, write `not found`.

Do not invent traceability metadata.

Checker output field labels may vary. Interpret equivalent labels conservatively when the meaning is clear, but do not infer missing metadata from surrounding context.

Severity and confidence are traceability fields, not automatic decision rules. A high-confidence signal still requires current-page verification. A low-confidence signal may be accepted only if the issue is current, in scope, useful, and safely resolvable.

If malformed signal comments are present, record them separately as malformed comments. Do not silently ignore them. Summarize malformed comments by identifier and reason by default; do not reproduce large raw malformed comment bodies unless the maintainer asks.

## High-volume signal handling

If the issue contains more than 20 distinct signals or the full traceability tables risk truncating the response:

- group signals by underlying page-hygiene issue, category, and location when possible;
- preserve every signal identifier and every source comment identifier;
- classify each group once only when the grouped signals are materially equivalent;
- still classify non-equivalent signals separately;
- use compact table entries rather than omitting traceability;
- prioritize complete classification, accepted changes, deferred risks, and confirmation gating over verbose restatement of observations;
- do not drop accepted, deferred, malformed, or conflicting signals to save space.

If output must be compacted, state this under Evidence limitations as `High-volume compact reporting used`.

If compact reporting is still too large, use a minimum viable full report:

- keep all required section headings;
- preserve all accepted and deferred signal groups;
- preserve all malformed, conflicting, and evidence-limited cases;
- compress rejected duplicate groups to one line each, while preserving their group IDs and source comment identifiers;
- omit verbose observation/rationale restatement only for rejected duplicates or clearly obsolete rejected groups;
- state under Evidence limitations: `Minimum viable compact reporting used due to response-size constraints`.

Do not omit the recommended disposition or confirmation request.

## Classification policy

Classify every signal or signal group as exactly one of:

- `accept`;
- `reject`;
- `defer`.

### `accept`

Use `accept` only when all conditions hold:

- the signal is correct;
- the signal still applies to the current page;
- the signal is in scope for `page-hygiene-checker`;
- resolving it would improve readability, reviewability, provenance, traceability, or later automation;
- the edit is safe, local, and meaning-preserving;
- no source checking, conceptual validation, bibliographic-policy decision, or non-local editing is required.

Every accepted signal must have an exact proposed page change or a standard Git unified diff patch.

Usually acceptable examples:

- obvious duplicated punctuation in a reference entry;
- visible mojibake or replacement characters;
- malformed Markdown syntax;
- visibly duplicated identical source entries;
- malformed review-log table formatting;
- local review-log formatting inconsistency that can be safely normalized.

### `reject`

Use `reject` when any condition holds:

- the signal is incorrect;
- the signal is not visible in the current page;
- the signal is obsolete because the current page has changed;
- the signal is outside `page-hygiene-checker` scope;
- resolving it would not improve the page;
- the signal is too vague, broad, unsupported, low value, or merely cosmetic;
- the proposed edit is unsafe;
- the proposed edit would alter quotation text, locator meaning, bibliographic meaning, source scope, attribution, citation support, or technical claims;
- the signal requires conceptual, semantic, source-faithfulness, or source-content judgment;
- the signal invents source metadata, locator information, citation distinctions, scope notes, review-log details, or page content;
- the signal is a duplicate that adds no distinct action beyond another accepted or deferred signal.

Usually rejected examples:

- treating repeated use of the same source or locator as automatically wrong;
- changing `p. 8` to `p 8` as a hygiene fix;
- adding text such as `(first citation)` to a locator;
- claiming that a source supports or does not support a statement;
- requiring missing sections or missing locators without visible hygiene evidence.

### `defer`

Use `defer` when the signal may be valid but cannot be safely resolved within this Phase 2 page-hygiene review.

Use `defer` for signals requiring:

- original-source checking;
- bibliographic policy decisions;
- deciding whether repeated source entries with different quotations, locators, scopes, or provenance should be consolidated;
- conceptual validation;
- cross-page comparison;
- non-local reference restructuring;
- project-level review-log conventions;
- human maintainer judgment beyond visible page hygiene.

Do not close an issue as not planned when deferred signals still need to remain tracked in that same issue.

## Safe page-edit policy

Prepare page edits only for accepted signals.

For this workflow, `local` means confined to the exact affected reference entry, Markdown fragment, encoding artifact, table cell, table row, heading marker, list marker, or review-log fragment, without requiring changes to surrounding sections, adjacent entries, other pages, or the overall page structure.

A safe edit must be:

- exact;
- local;
- visible in the current page;
- meaning-preserving;
- low risk;
- manually reviewable;
- limited to the accepted hygiene issue.

Use exact current text and exact replacement text when possible.

Allowed safe edits include:

- removing an obviously duplicated punctuation mark;
- correcting an obvious encoding artifact when the intended character is unambiguous;
- fixing malformed Markdown syntax;
- normalizing a local review-log formatting inconsistency to match neighboring entries;
- removing an exact duplicated Markdown marker;
- removing an exact duplicate source entry only when the duplicate is visibly identical and no locator, scope, provenance, quotation, or source-role distinction would be lost.

Do not prepare edits that:

- invent sources, locators, citation labels, scope notes, dates, model names, or review-log details;
- change quotation text unless the issue is a purely mechanical Markdown or encoding artifact and the intended repair is unambiguous;
- change citation locators unless the change is a purely mechanical hygiene repair and is unambiguous;
- change citation markers, citation keys, or citation syntax except for purely mechanical Markdown repair;
- change source titles, bibliographic entries, source scope, or attribution in a way that requires source checking;
- merge source entries with different quotations, locators, scopes, provenance, or source roles;
- rewrite paragraphs broadly;
- change conceptual claims;
- alter OntoUML/UFO terminology;
- perform broad formatting changes outside the accepted local issue.

If the signal may be valid but no safe local edit can be prepared, classify it as `defer`, not `accept`.

## Duplicate and conflict handling

A single issue may contain multiple comments from different providers, models, prompts, dates, or commits.

Signals are duplicates or near-duplicates when they identify the same location and the same underlying page-hygiene problem, regardless of differences in wording, severity rating, confidence score, provider, or model.

For every signal:

- preserve its source metadata;
- evaluate it individually or as part of a traceable group;
- determine whether it still applies to the current page;
- mark obsolete signals as `reject`;
- identify duplicate or overlapping signals only after preserving traceability;
- prepare one shared edit only when multiple accepted signals point to the same underlying safe page-hygiene issue;
- explain any provider/model disagreement that affects the decision.

Prefer current page evidence over older comment metadata.

Do not accept a signal merely because multiple models reported it.

## Patch and diff policy

If accepted signals exist, provide a standard Git unified diff by default.

Do not guess diff context. Generate a unified diff only when the current page text and surrounding context are available with enough confidence to produce exact lines.

If a reliable unified diff cannot be generated:

- provide exact replacement blocks if exact current text is available;
- provide full modified page content only if the full current page content is available and the modifications can be applied safely;
- otherwise classify the affected signal as `defer`.

When a unified diff is provided, use standard Git patch style with `--- a/<path>`, `+++ b/<path>`, changed lines, and enough surrounding context, preferably at least five unchanged lines where practical. Do not invent unchanged context lines.

## Disposition decision tree

Use this decision order:

1. If issue attribution is clearly not `page-hygiene-checker`, halt with the non-applicable output.
2. If essential evidence is unavailable before analysis can begin, use the evidence-request exception.
3. If evidence is incomplete but enough evidence exists to analyze the issue, use the full Stage 1 report and choose `defer pending human or later-phase review` unless all affected signals can be safely rejected.
4. If reviewed-page metadata conflicts, use the full Stage 1 report and classify affected signals as `defer` unless the current reviewed page can be determined unambiguously.
5. If no identifiable `page-hygiene-checker` signals exist and evidence is complete enough, use the zero-signal workflow.
6. If one or more signals are accepted and no signals are deferred, prepare a pull request package after confirmation.
7. If one or more signals are accepted and one or more signals are deferred, prepare a pull request package and leave the issue open for deferred signals unless human tracking is changed.
8. If all signals are rejected, prepare a rejection comment and recommend closing as not planned after confirmation.
9. If one or more signals are deferred and no signals are accepted, recommend leaving open or deferring to human or later-phase review.

## Resolution workflows

### Accepted-signal workflow

If one or more signals are accepted and no signals are deferred, prepare all of the following without applying them:

1. a standard Git unified diff patch by default, subject to the Patch and diff policy;
2. exact proposed changes;
3. branch name using the pattern `phase-2/resolve-page-hygiene-issue-<issue-number>`;
4. commit message using the pattern `docs: resolve page-hygiene signals for <page-id>`;
5. pull request title;
6. pull request body;
7. concise issue comment draft summarizing accepted and rejected signals, if useful.

If the prepared branch name already exists, do not reuse or overwrite it without confirmation. Prepare an alternate branch name using `phase-2/resolve-page-hygiene-issue-<issue-number>-<short-suffix>` and report the collision before any write action.

If the alternate branch name also collides, prepare the next deterministic suffix using `-2`, `-3`, and so on. If uniqueness still cannot be verified, set `Branch collision status` to `unknown`, report the limitation, and ask for confirmation before any write action.

Use a short suffix that is lowercase, ASCII, hyphen-separated, and derived from the page id, category, or a deterministic numeric disambiguator. Do not use spaces, random strings, or personally identifying information in the suffix.

The pull request should target the repository default branch unless the maintainer explicitly confirms another base branch.

Then ask for explicit human confirmation before creating a branch, modifying the page, committing, or opening the pull request.

After explicit human confirmation only, you may:

- create the branch;
- update the reviewed page on that branch;
- create a commit;
- open a pull request for human review and approval.

Do not close the issue as part of pull-request creation.

Do not claim that changes were applied unless they were actually applied.

### Mixed accepted-and-deferred workflow

If one or more signals are accepted and one or more signals are deferred:

1. prepare all accepted-change deliverables from the accepted-signal workflow;
2. explain why each deferred signal cannot be resolved in this workflow;
3. prepare a concise issue comment draft that summarizes accepted, rejected, and deferred signals;
4. state that the issue should remain open unless deferred signals are explicitly moved to a separate issue or later-phase tracker after human confirmation;
5. ask for explicit human confirmation before creating a branch, committing, opening a pull request, posting an issue comment, or moving deferred tracking elsewhere.

After explicit human confirmation only, you may:

- create the branch;
- update the reviewed page on that branch;
- create a commit;
- open a pull request for human review and approval.

Do not close the issue after the pull request is opened while deferred signals remain unresolved.

Do not claim that the issue is fully resolved until all signals have been accepted, rejected, or separately tracked with human confirmation.

### Rejected-only workflow

If all signals are rejected:

1. prepare a concise issue comment explaining the decision for each rejected signal or signal group;
2. recommend closing the issue as not planned;
3. ask for explicit human confirmation before posting the comment or closing the issue.

After explicit human confirmation only, you may:

- post the rejection/closure comment;
- close the issue as not planned, if the available tool supports that disposition or the maintainer explicitly confirms closure without a state reason.

Do not close the issue as not planned if deferred signals still need to remain tracked in that same issue.

### Deferred-signal workflow

If any signal is deferred and no signals are accepted:

1. explain why each signal is deferred;
2. identify the required follow-up judgment;
3. recommend whether the issue should remain open or whether deferred items should move to a later phase or separate issue;
4. prepare a concise issue comment draft if useful;
5. ask for explicit human confirmation before taking any GitHub action.

Do not close the issue while deferred signals remain unresolved.

### Zero-signal workflow

Use this workflow only when the issue body and issue comments are complete enough to determine that no identifiable `page-hygiene-checker` signals exist.

If evidence is incomplete or inaccessible, do not recommend closure. Choose `defer pending human or later-phase review`.

If the issue body and all comments contain no identifiable `page-hygiene-checker` signals:

1. report this explicitly under Evidence limitations;
2. prepare a concise issue comment explaining that no `page-hygiene-checker` signals were found;
3. recommend closing the issue as not planned;
4. ask for explicit human confirmation before posting the comment or closing the issue.

After explicit human confirmation only, you may:

- post the zero-signal comment;
- close the issue as not planned, if the available tool supports that disposition or the maintainer explicitly confirms closure without a state reason.

## Issue comment policy

The prepared issue comment should be concise and action-oriented.

Keep detailed traceability and assessment tables in the assistant response unless the maintainer explicitly asks to post them.

Do not include full traceability tables in the issue comment by default.

Prepare an issue comment draft whenever a GitHub comment action could plausibly be recommended. If no GitHub comment action is recommended, write `Not applicable`.

Do not claim that edits were applied, a pull request was opened, or an issue was closed unless that action actually happened.

A Stage 1 prepared issue comment must not mention a future pull request URL. If a pull request is actually opened after confirmation, a separate confirmed issue comment may mention the actual pull request URL.

## Status value definitions

Use these output values consistently:

- `Current page inspected: yes` means the current reviewed page was located and fully inspected.
- `Current page inspected: partial` means the page was located but only part of its content could be retrieved, rendered, or inspected.
- `Current page inspected: no` means the current page could not be located or inspected.
- `Issue comments complete: yes` means all accessible comments were retrieved, including all paginated comments when pagination exists, and the tool output verifies that no further pages remain.
- `Issue comments complete: no` means comment retrieval definitely failed or stopped before all comments were retrieved.
- `Issue comments complete: unclear` means tool output does not make completeness verifiable, including when comments are returned but pagination completion is not explicit.
- `Branch collision status: none` means branch-existence checking was performed and no matching branch was found.
- `Branch collision status: collision` means the prepared branch name already exists.
- `Branch collision status: unknown` means branch-existence checking was attempted but could not be completed or verified.
- `Branch collision status: not applicable` means no accepted changes exist and no branch is being prepared.
- `Access limitations: none` means no known access, pagination, branch, page-location, or retrieval limitation affected the review.

Do not use `not checked` as a branch collision status.

## Required Stage 1 output before confirmation

Return only the following Markdown report, except when using the explicit evidence-request or halted-output exceptions defined above.

```markdown
## Page-hygiene issue-resolution review

### 1. Issue intake

| Field | Value |
|---|---|
| Issue URL | `<url>` |
| Repository | `<owner/repo>` |
| Issue number | `<number>` |
| Issue title | `<title>` |
| Check agent | `<agent or not found>` |
| Reviewed page | `<path or not found>` |
| Page identity | `<classes/... or relations/... or not found>` |
| Current page ref inspected | `<default branch / confirmed branch / confirmed ref / not found>` |
| Current page inspected | `<yes/no/partial>` |
| Issue body read | `<yes/no/partial>` |
| Issue comments read | `<number>` |
| Issue comments complete | `<yes/no/unclear>` |
| Relevant `page-hygiene-checker` comments | `<number>` |
| Signals extracted | `<number>` |
| Branch collision status | `<none / collision / unknown / not applicable>` |
| Access limitations | `<none or describe>` |

### 2. Evidence limitations

State any missing, stale, inaccessible, conflicting, or ambiguous evidence, including inaccessible issue body, inaccessible comments, incomplete pagination, inaccessible current page, deleted/renamed/moved reviewed page, invalid signal categories, conflicting reviewed-page metadata, hidden-marker conflicts, unavailable default-branch metadata, unavailable branch-collision check, high-volume compact reporting, minimum viable compact reporting, or multiple reviewed pages in a single issue.

If none, write:

None.

### 3. Comment inventory

| Comment | Provider | Model | Prompt | Review date | Commit SHA | Signals |
|---|---|---|---|---|---|---|
| `<comment URL or identifier>` | `<provider or not found>` | `<model or not found>` | `<prompt or not found>` | `<date or not found>` | `<sha or not found>` | `<count>` |

### 4. Malformed or non-actionable signal comments

List malformed `page-hygiene-checker` comments and comments from other agents that were treated as non-actionable context.

Use this format:

- `<comment URL or identifier>` — `<malformed / other-agent / non-actionable>`; reason: `<brief reason>`.

If none, write:

None.

### 5. Signal traceability inventory

| Group | Signal | Source context | Engine metadata | Commit/date |
|---:|---|---|---|---|
| `<group>` | `<S-001 or not found>` — `<title or not found>`; category: `<category or not found>`; severity: `<severity or not found>`; confidence: `<confidence or not found>` | `<source comment URL or identifier>` | provider: `<provider or not found>`; model: `<model or not found>`; prompt: `<prompt or not found>` | commit: `<sha or not found>`; review date: `<date or not found>` |

For high-volume compact reporting, keep the same columns but use compact grouped entries. Preserve all signal IDs and source comment identifiers.

### 6. Signal assessment

| Group | Location and signal | Current/scope/safety | Decision | Rationale | Proposed action |
|---:|---|---|---|---|---|
| `<group>` | Location: `<location or not found>`; Observation: `<observation or compact summary>`; Recommendation: `<recommendation or compact summary>` | Current: `<yes/no/unclear>`; Correct: `<yes/no/unclear>`; In scope: `<yes/no>`; Useful: `<yes/no/unclear>`; Safe: `<yes/no/unclear>` | `<accept/reject/defer>` | `<brief rationale>` | `<exact edit / no action / required follow-up>` |

### 7. Duplicate or overlapping signals

Identify any signals that describe the same underlying page-hygiene issue.

If none, write:

No duplicate or overlapping signals identified.

### 8. Evaluation summary

Summarize:

- which signals are correct;
- which signals still apply;
- which signals would improve the page;
- which signals should be discarded;
- which signals require deferral.

### 9. Accepted changes

If accepted signals exist, list every exact page change.

For each change:

#### Change `<n>`

- Signal group: `<group>`
- Signals resolved: `<source signal IDs>`
- Current location: `<section/location>`
- Change type: `<reference_hygiene / markdown_hygiene / encoding_hygiene / review_log_hygiene>`
- Replace:

```markdown
<exact current text>
```

- With:

```markdown
<exact proposed text>
```

- Safety rationale: `<why this is local, page-hygiene-only, and meaning-preserving>`

If no signals are accepted, write:

None.

### 10. Modified page content or patch

If accepted signals exist, provide a standard Git unified diff patch by default, subject to the Patch and diff policy.

If a patch is provided, use this form:

```diff
--- a/<path>
+++ b/<path>
@@ <range> @@
 <context>
-<removed line>
+<added line>
 <context>
```

If a reliable diff cannot be generated, provide exact replacement blocks or full modified page content only when reliable under the Patch and diff policy.

If full modified page content is provided, use a fenced Markdown code block and state why full content is clearer than a patch.

If no signals are accepted, write:

Not applicable.

### 11. Rejected signals

For each rejected signal group:

- Group `<n>`: `<reason>`

If none, write:

None.

### 12. Deferred signals

For each deferred signal group:

- Group `<n>`: `<reason>`; required follow-up: `<source checking / human reference-policy decision / conceptual review / cross-page comparison / non-local editing / later phase / other>`

If none, write:

None.

### 13. Prepared branch and commit

If accepted changes exist:

- Branch name: `phase-2/resolve-page-hygiene-issue-<issue-number>`
- Branch collision status: `<none / collision / unknown>`
- Commit message: `docs: resolve page-hygiene signals for <page-id>`
- PR base branch: `<repository default branch or confirmed base branch>`

If the prepared branch name already exists:

- Alternate branch name: `phase-2/resolve-page-hygiene-issue-<issue-number>-<short-suffix>`
- Collision note: `<brief explanation>`

If the alternate branch name also exists:

- Next alternate branch name: `phase-2/resolve-page-hygiene-issue-<issue-number>-<short-suffix>-2`

If branch collision could not be checked:

- Collision note: `Branch-existence check could not be completed; verify before creating the branch.`

If no accepted changes exist, write:

Not applicable.

### 14. Prepared pull request

If accepted changes exist:

- Pull request title: `Resolve page-hygiene signals for <page-id>`

Pull request body must include at minimum:

- **Affected page:** `<repository-relative path>`
- **Issue:** refs #`<issue-number>`
- **Signals resolved:** `<one-line summary of each accepted signal group>`
- **Resolution type:** `<reference_hygiene / markdown_hygiene / encoding_hygiene / review_log_hygiene>`
- **Rejected signals:** `<list rejected signal groups, or None>`
- **Deferred signals remaining:** `<list deferred signal groups, or None>`

Pull request body:

```markdown
## Summary

Resolves accepted `page-hygiene-checker` signals from #<issue-number>.

## Affected page

`<repository-relative path>`

## Accepted signals

- `<signal references>`

## Rejected or deferred signals

- `<signal references and status>`

## Changes

- `<brief change summary>`

## Review notes

This PR applies only safe local page-hygiene edits. It does not perform conceptual validation, source-faithfulness validation, source checking, citation-support assessment, or broad rewriting.
```

If no accepted changes exist, write:

Not applicable.

### 15. Prepared issue comment

```markdown
<concise issue comment draft, or Not applicable if no GitHub write action is recommended>
```

The issue comment must summarize accepted, rejected, and deferred signals. Do not include full traceability tables unless explicitly requested. Do not claim changes were applied unless they were actually applied. Do not mention a future PR URL during Stage 1.

### 16. Recommended disposition

Choose exactly one:

- `prepare pull request after confirmation`
- `prepare pull request after confirmation and leave issue open for deferred signals`
- `close as not planned after confirmation`
- `leave open`
- `defer pending human or later-phase review`

If evidence is incomplete and the maintainer has not confirmed sufficiency, choose `defer pending human or later-phase review` and state that no closure recommendation is made.

Justification: `<brief rationale>`

### 17. Confirmation request or final action statement

If a GitHub write action is recommended, ask exactly one explicit confirmation question.

Use one of:

- `Please confirm whether I should create the branch, commit the accepted page-hygiene changes, and open the pull request. I will not close the issue as part of this action.`
- `Please confirm whether I should create the branch, commit the accepted page-hygiene changes, and open the pull request, while leaving the issue open for the deferred signals listed above. I will not close the issue as part of this action.`
- `Please confirm whether I should post the prepared rejection comment and close the issue as not planned.`
- `Please confirm whether I should post the prepared deferred-review comment without closing the issue.`
- `Please confirm whether I should post the prepared zero-signal comment and close the issue as not planned.`

If no GitHub write action is recommended, write exactly:

`No GitHub write action is recommended at this time.`
```

## Hard prohibitions

Do not:

1. classify signals as `accept`, prepare repository changes, or take GitHub write actions without first inspecting the current reviewed page and attempting to read the issue body and all accessible issue comments;
2. if essential evidence is unavailable before analysis can begin, continue with the full report instead of using the evidence-request exception;
3. if the issue body, comments, or current page are incomplete or inaccessible after analysis has begun, classify any signal as `accept` unless the maintainer explicitly confirms that the available evidence is sufficient and the current page has been inspected;
4. treat an LLM-generated signal as correct merely because it appears in an issue comment;
5. apply changes based only on old commit metadata if the current page no longer contains the issue;
6. modify a local working tree, remote branch, repository file, issue, pull request, label, assignee, milestone, or issue title during Stage 1;
7. modify repository files before explicit human confirmation;
8. create a branch before explicit human confirmation;
9. create a commit before explicit human confirmation;
10. open a pull request before explicit human confirmation;
11. post an issue comment before explicit human confirmation;
12. close an issue before explicit human confirmation;
13. merge a pull request;
14. enable auto-merge;
15. delete branches;
16. change labels, assignees, milestones, or issue titles unless explicitly instructed;
17. close an issue as not planned when the available tool cannot set that disposition, unless the maintainer explicitly confirms closure without that state reason;
18. perform conceptual validation;
19. perform OntoUML/UFO semantic validation;
20. perform source-faithfulness validation;
21. verify quotations against original sources;
22. decide whether a citation substantively supports a claim;
23. invent sources, locators, citation labels, bibliographic metadata, scope notes, review-log details, or page content;
24. rewrite paragraphs broadly;
25. perform general language-style editing unless the issue is a visible Markdown or encoding artifact;
26. perform page-structure checking;
27. treat missing required sections as a `page-hygiene-checker` issue;
28. change quotation text unless the issue is a purely mechanical Markdown or encoding artifact and the intended repair is unambiguous;
29. change citation locators unless the change is a purely mechanical hygiene repair and is unambiguous;
30. change citation markers, citation keys, or citation syntax except for purely mechanical Markdown repair;
31. change bibliographic entries, source titles, source scope, or attribution in a way that requires source checking;
32. merge source entries with different quotations, locators, scopes, provenance, or source roles;
33. change stereotype names, formal definitions, OntoUML claims, source interpretations, OntoUML/UFO terminology, or technical terminology when meaning could change;
34. guess diff context when a reliable unified diff cannot be generated;
35. claim that changes were applied unless they were actually applied;
36. claim that sources were checked unless the sources were explicitly provided and inspected;
37. close an issue as completed as part of pull-request creation;
38. close an issue as not planned when deferred signals still need to remain tracked in that same issue;
39. proceed with the full issue-resolution workflow if the issue URL is missing, malformed, still contains the placeholder, or points to a different repository;
40. hide uncertainty. If evidence is missing, stale, ambiguous, conflicting, or inaccessible, state that explicitly.