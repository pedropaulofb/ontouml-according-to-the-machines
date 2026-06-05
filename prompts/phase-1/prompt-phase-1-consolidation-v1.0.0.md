# Prompt: Phase 1 Consolidation — Direct Main Commit for One Stereotype
# Version: 1.0.0

You are helping consolidate Phase 1 intermediate work products for the documentation project "OntoUML According to the Machines".

This execution belongs to Phase 1 — Groundwork and Initial Population.

This prompt is a direct-repository-mutation variant. Use it only when autonomous direct commits to `main` are explicitly intended and accepted for the current run. For reviewable artifact generation without repository mutation, use a ZIP-package consolidation prompt instead.

Your task is to read all committed Phase 1 source-specific intermediate files for exactly one OntoUML stereotype, generate the first consolidated canonical Markdown page for that stereotype, commit that page directly to the repository's `main` branch, and verify that the committed file matches the generated page.

This direct commit is allowed only because the target canonical stereotype pages are currently empty or skeletal Phase 1 pages.

You are not performing final expert validation. You are not generating examples. You are not completing the stereotype profile. You are not creating branches. You are not opening pull requests.

---

## Run configuration

The user must provide only the run-specific information below.

- Target intermediate folder URL: <GitHub tree URL pointing to one stereotype's intermediate folder on main>

Example:

```text
https://github.com/pedropaulofb/ontouml-according-to-the-machines/tree/main/work-products/phase-1/intermediate/stereotypes/classes/kind
```

If the required run-configuration field is missing, report `MISSING_RUN_CONFIGURATION`, list the missing field, and do not generate or commit anything.

Do not require the user to provide technical execution metadata such as current date, current datetime, prompt ID, prompt version, prompt file path, target stereotype group, target stereotype ID, target display name, target canonical file path, or commit message. Derive or generate those fields yourself as specified below.

---

## Repository and branch constraints

The target repository must be:

```text
pedropaulofb/ontouml-according-to-the-machines
```

The only branch that may be read from and updated is:

```text
main
```

Do not create branches.

Do not open pull requests.

Do not merge anything.

Do not update any repository other than `pedropaulofb/ontouml-according-to-the-machines`.

Do not modify more than one file.

Do not modify files outside:

```text
docs/stereotypes/classes/
docs/stereotypes/relations/
```

Resolve and compare repository-relative paths using POSIX path semantics. Before any write operation, the normalized target path must exactly equal the derived target canonical file path.

If repository read access or a required repository-read tool is unavailable, report `REPOSITORY_READ_UNAVAILABLE` and do not generate or commit anything.

If repository write access or a required repository-write tool is unavailable, report `REPOSITORY_WRITE_UNAVAILABLE` and do not commit anything.

---

## URL parsing and target derivation

Parse the supplied `Target intermediate folder URL`.

Before validation, normalize the URL by removing:

- trailing slashes;
- query parameters;
- URL fragments.

The normalized URL must match this structure:

```text
https://github.com/pedropaulofb/ontouml-according-to-the-machines/tree/main/work-products/phase-1/intermediate/stereotypes/<target-stereotype-group>/<target-stereotype-id>
```

where:

- the Git ref must be exactly `main`;
- `<target-stereotype-group>` is either `classes` or `relations`;
- `<target-stereotype-id>` is a valid stereotype ID from the controlled mapping.

URLs pointing to any ref other than `main` are invalid.

Reject URLs whose decoded path contains encoded slashes, encoded backslashes, dot segments, control characters, or any character sequence that would alter the normalized repository-relative path.

Derive:

- target stereotype group;
- target stereotype ID;
- target display name;
- target canonical file path;
- commit message.

The target canonical file path must be:

```text
docs/stereotypes/<target-stereotype-group>/<target-stereotype-id>.md
```

Example:

```text
docs/stereotypes/classes/kind.md
```

If the URL does not match the required structure, report `INVALID_TARGET_INTERMEDIATE_FOLDER_URL` and do not generate or commit anything.

If the configured target stereotype group and target stereotype ID do not match the controlled mapping, report `INVALID_TARGET_STEREOTYPE` and do not generate or commit anything.

---

## Auto-generated execution metadata

Generate the execution metadata below yourself.

Use Europe/Amsterdam local time for the current date and current datetime.

If Europe/Amsterdam time is unavailable in the execution environment, use UTC. If UTC is used:

- state `UTC used for timestamp` in the generated page's Generation and Review Log notes;
- state `(UTC used)` in the final concise confirmation.

Use these exact formats:

- Current date: `YYYY-MM-DD`
- Current datetime: `YYYY-MM-DDtHHMM`

The `Current datetime` must contain no spaces and no colons.

Use these fixed prompt metadata values:

- Prompt ID: `prompt-phase-1-consolidation-v1.0.0`
- Prompt title: `Phase 1 Consolidation — Direct Main Commit for One Stereotype`
- Prompt version: `1.0.0`
- Prompt file path: `prompts/phase-1/prompt-phase-1-consolidation-v1.0.0.md`

Use the executing agent/model name in the generated page's Generation and Review Log. If the executing agent/model name is unavailable, write exactly:

```text
Unspecified generation agent
```

When committing, use this commit message pattern:

```text
docs(stereotypes): consolidate <Target display name> page
```

Example:

```text
docs(stereotypes): consolidate Kind page
```

If you cannot determine the current date or current datetime from the execution environment, report `EXECUTION_DATETIME_UNAVAILABLE` and do not generate or commit anything.

---

## Controlled stereotype mapping

Use this mapping to validate the target stereotype and derive the target display name.

Do not invent stereotype IDs.

Do not invent display names.

### Class stereotypes

| Target stereotype ID | Target display name |
|---|---|
| `abstract` | `Abstract` |
| `category` | `Category` |
| `collective` | `Collective` |
| `datatype` | `Datatype` |
| `enumeration` | `Enumeration` |
| `event` | `Event` |
| `historical-role-mixin` | `HistoricalRoleMixin` |
| `historical-role` | `HistoricalRole` |
| `kind` | `Kind` |
| `mixin` | `Mixin` |
| `mode` | `Mode` |
| `phase-mixin` | `PhaseMixin` |
| `phase` | `Phase` |
| `quality` | `Quality` |
| `quantity` | `Quantity` |
| `relator` | `Relator` |
| `role-mixin` | `RoleMixin` |
| `role` | `Role` |
| `situation` | `Situation` |
| `subkind` | `Subkind` |
| `type` | `Type` |

### Relation stereotypes

| Target stereotype ID | Target display name |
|---|---|
| `brings-about` | `BringsAbout` |
| `characterization` | `Characterization` |
| `comparative` | `Comparative` |
| `component-of` | `ComponentOf` |
| `creation` | `Creation` |
| `external-dependence` | `ExternalDependence` |
| `historical-dependence` | `HistoricalDependence` |
| `instantiation` | `Instantiation` |
| `manifestation` | `Manifestation` |
| `material` | `Material` |
| `mediation` | `Mediation` |
| `member-of` | `MemberOf` |
| `participation` | `Participation` |
| `participational` | `Participational` |
| `sub-collection-of` | `SubCollectionOf` |
| `sub-quantity-of` | `SubQuantityOf` |
| `termination` | `Termination` |
| `triggers` | `Triggers` |

---

## Naming convention

Use the controlled target display name in headings and prose.

When referring in prose to any stereotype present in the controlled mapping, use the mapped display name. Do not create spaced labels for any mapped stereotype outside exact direct quotations.

If an intermediate file uses a spaced stereotype name outside a direct quotation, normalize it to the mapped display name only when the intended mapped stereotype is unambiguous and the phrase is being used as a stereotype name, not as ordinary prose.

Examples:

- HistoricalRoleMixin
- HistoricalDependence
- RoleMixin
- PhaseMixin
- ComponentOf
- SubQuantityOf
- SubCollectionOf

Repository paths and filenames must remain kebab-case.

Example:

- File path: `docs/stereotypes/classes/historical-role-mixin.md`
- Display name: `HistoricalRoleMixin`

Do not normalize stereotype names inside direct quotations. Direct quotations must preserve exact source wording.

---

## Input file retrieval

Use the supplied GitHub folder URL to retrieve all `.md` files directly under the target intermediate folder.

Expected source folder pattern:

```text
work-products/phase-1/intermediate/stereotypes/<target-stereotype-group>/<target-stereotype-id>/
```

Use repository contents or tree APIs when available.

Use repository search only if it can establish a complete, enumerable set of direct child Markdown files under the expected folder.

If no available method can establish a complete enumerable set of direct child Markdown files, report `SOURCE_FILE_ENUMERATION_INCOMPLETE` and do not generate or commit anything.

Only process Markdown files directly inside that folder.

Process valid target intermediate files in lexicographic order by repository-relative path. Use the same order for the Generation and Review Log Inputs column.

Ignore:

- subfolders;
- non-Markdown files;
- hidden files;
- auxiliary files;
- files outside the target intermediate folder.

For this prompt, hidden files are files whose basename starts with `.`.

If the target intermediate folder cannot be read, report `TARGET_INTERMEDIATE_FOLDER_UNAVAILABLE` and do not generate or commit anything.

If the target intermediate folder contains no Markdown files directly under it, report `NO_TARGET_INTERMEDIATE_FILES` and do not generate or commit anything.

Each valid supplied intermediate file is expected to contain:

- `## Source-Specific Description Contribution`
- `## References`
- `### Direct Citations`
- `### Consulted Sources`
- `## Generation and Review Log`

A target intermediate file is malformed if it is empty, corrupted, unreadable, or missing `## Source-Specific Description Contribution`.

A target intermediate file that has `## Source-Specific Description Contribution` but is missing one or more reference or generation-log sections may still be consolidated, but the missing sections must be mentioned in the generated page's Generation and Review Log notes.

If a file path says it belongs to the target stereotype but the file's explicit target metadata, title, main heading, or Generation and Review Log identifies a different mapped stereotype as the subject, treat it as malformed and ignore it.

Do not treat incidental mentions of other stereotypes as wrong-stereotype identification.

If all Markdown files in the target folder are empty, corrupted, unreadable, malformed, or missing required description contribution content, report `NO_VALID_TARGET_INTERMEDIATE_FILES` and do not generate or commit anything.

---

## Current canonical page preflight

Before generating or committing, read the current target canonical page on `main`.

The target canonical page is:

```text
docs/stereotypes/<target-stereotype-group>/<target-stereotype-id>.md
```

Commit directly to `main` only if the current target canonical page is empty or skeletal.

A page is considered skeletal only if it contains no substantive content beyond:

- optional front matter that is itself non-substantive;
- optional HTML comments;
- the page title;
- expected section headings;
- empty sections;
- `TBD in a later phase.`;
- empty references;
- an empty, absent, or single-row system baseline initialization generation log.

Optional front matter may be treated as skeletal only if it contains no substantive documentation content, no prior-consolidation metadata, no review status indicating completed content work, and no redirect, alias, navigation, permalink, or other routing information that would be lost by overwrite.

If the significance of front matter is unclear, report `TARGET_PAGE_SKELETON_STATUS_UNDETERMINED` and do not generate or commit anything.

A baseline initialization generation log is a single row whose action or notes indicate only scaffold creation, placeholder initialization, baseline setup, or page initialization, and do not indicate source consolidation, expert review, substantive authoring, or prior documentation content work.

If the current canonical page contains any non-placeholder sentence under `## Description`, treat it as not skeletal.

A page is not skeletal if it contains substantive prose, examples, completed stereotype profile content, meaningful references, previous consolidation content, meaningful front matter, or any non-baseline generation log indicating substantive prior content work.

If the target canonical page does not exist, report `TARGET_PAGE_MISSING` and do not generate or commit anything.

If the target canonical page is not skeletal, report `TARGET_PAGE_NOT_SKELETAL` and do not generate or commit anything.

If the current target canonical page can be read but skeletal status cannot be determined confidently, report `TARGET_PAGE_SKELETON_STATUS_UNDETERMINED` and do not generate or commit anything.

Do not use the current canonical page as evidence for consolidation. It is checked only to determine whether direct overwrite is safe.

---

## Core task

Generate one consolidated canonical Markdown page for the target stereotype.

The generated canonical page must be written as UTF-8 text with LF line endings and a final newline.

The page must synthesize the supplied `Source-Specific Description Contribution` sections into one coherent `## Description` section.

The consolidation should:

- preserve source-grounded claims;
- remove duplicate claims;
- merge complementary claims;
- preserve important conceptual distinctions and constraints;
- avoid unsupported generalization;
- avoid overconfident language;
- avoid merely concatenating intermediate descriptions;
- produce a first consolidated page, not a final authoritative page.

Include a synthesized description claim only if it is supported by at least one valid target intermediate file and is not contradicted by another valid target intermediate file.

When a claim is supported by only one valid target intermediate file, use cautious wording unless the source-specific contribution presents the claim as a central definition, central constraint, or central characterization.

If support is weak or isolated, use cautious wording or omit the claim.

Do not infer definitions, hierarchy placement, constraints, modeling guidance, anti-patterns, or distinctions unless they are explicitly supported by the supplied valid target intermediate files.

If intermediate files conflict, do not invent a resolution. Either omit the contested claim or use cautious wording that reflects only what is safely supported by the supplied valid target intermediate files.

Do not use external knowledge.

Do not use prior OntoUML knowledge unless it is explicitly present in the supplied valid target intermediate files.

---

## Internal evidence pass

Before generating the canonical page, perform an internal evidence pass.

Identify:

1. claims repeated across multiple valid target intermediate files;
2. claims supported by only one valid target intermediate file;
3. complementary claims that can be safely combined;
4. claims that appear to conflict;
5. claims that are too weak, vague, or unsupported for inclusion;
6. direct citations that should be preserved;
7. consulted sources that should be carried into the final page;
8. malformed target files that were ignored;
9. incomplete target files that were used but had missing reference or log sections;
10. duplicate copies or regenerated variants of the same source-specific contribution.

If two or more valid target intermediate files appear to be duplicate copies or regenerated variants of the same source-specific contribution, do not treat them as independent support for repeated claims.

Mention the duplicate-handling decision in the Generation and Review Log notes if it affects consolidation.

Keep internal traceability from each included `Description` claim to the valid target intermediate file or files supporting it. Use this traceability to prevent unsupported claims. Do not output the traceability map in the generated page or chat.

Use this internal evidence pass to generate the final page.

Do not output the internal evidence pass in the chat.

If consolidation fails because the evidence is too inconsistent, too sparse, or too ambiguous, report `CONSOLIDATION_FAILED` with a brief explanation and do not commit anything.

---

## Canonical page template

The generated canonical page must use exactly this structure:

```markdown
# <Target display name>

## Description

<Consolidated Phase 1 description synthesized from the supplied valid target intermediate files.>

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

<Consolidated direct citation bullets from the supplied valid target intermediate files, or exactly: None.>

### Consulted Sources

<Consolidated consulted source bullets from the supplied valid target intermediate files, or exactly: None.>

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| <Current date> | Phase 1 | <Agent/model or Unspecified generation agent> | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | <comma-separated and space-separated list of consolidated short intermediate file IDs or filenames, excluding full paths> | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at <Current datetime>; not final expert-validated documentation. <Mention ignored malformed target files if any. Mention incomplete but used target files if any. Mention duplicate-handling decisions if any. Mention UTC used for timestamp if applicable.> |
```

---

## Description requirements

The `Description` section must:

- be based only on supplied valid target intermediate files;
- use the controlled target display name and OntoUML VP-style stereotype names;
- be coherent as a standalone documentation page;
- be technical, concise, and documentation-like;
- synthesize rather than concatenate;
- preserve important source-grounded distinctions;
- avoid examples;
- avoid diagrams;
- avoid complete stereotype profile content;
- avoid claims not grounded in the supplied valid target intermediate files;
- avoid claims based only on prior knowledge or external knowledge;
- preserve uncertainty where the intermediate files do not support stronger claims.

The generated description should be suitable as a first consolidated Phase 1 page, not as final authoritative OntoUML documentation.

---

## References requirements

Merge direct citations from all supplied valid target intermediate files.

Preserve exact quotation wording.

Do not normalize stereotype names inside direct quotations.

When preserving direct citations, ensure citation bullets remain valid Markdown even when quotation text contains pipes, backticks, angle brackets, quotation marks, brackets, code fences, or other Markdown-significant characters.

Preserve exact quoted wording while using safe surrounding Markdown syntax.

Prefer plain list bullets with quotation text delimited by quotation marks when safe.

If a direct quotation contains Markdown syntax that cannot be represented safely as a citation bullet while preserving exact wording, omit that direct citation unless it is central to the consolidated page.

If the omitted citation is central, report `CONSOLIDATION_FAILED` rather than generating a page with broken Markdown or altered quotation wording.

When removing duplicate direct quotations, deduplicate by quotation text while preserving all distinct source attributions associated with that quotation where such attribution is available.

Use direct citations only where useful for key definitions or central claims.

When omitting a direct citation because it is not useful for a key definition or central claim, do not use that omission to weaken traceability of claims in the `Description`.

If no direct citations are available, write exactly:

```text
None.
```

under `Direct Citations`.

Do not add any explanatory sentence under `Direct Citations` other than citation bullets or `None.`.

Merge consulted sources from all supplied valid target intermediate files.

Remove duplicate consulted sources only when source identity and source scope are equivalent.

Do not merge consulted-source entries if merging would remove distinct source-scope information.

Preserve source scope information when available.

If no consulted sources are available from valid target intermediate files, write exactly:

```text
None.
```

under `Consulted Sources`.

Do not include consulted sources from malformed target files that were ignored.

---

## Generation log requirements

The generated page must include one consolidation log row.

The log row must record:

- current date;
- Phase 1;
- agent/model, or `Unspecified generation agent` if unavailable;
- action: `Consolidation`;
- prompt ID;
- prompt title;
- a comma-separated and space-separated list of consolidated short intermediate file IDs or filenames, excluding full paths;
- a note stating that the page is a first consolidated stereotype page generated from Phase 1 source-specific intermediate files and is not final expert-validated documentation.

Use only short file IDs or filenames in the Inputs column, not full repository-relative paths.

Separate Inputs items with a comma followed by a space.

If a source filename or generated short file ID contains a comma, vertical bar, newline, or other table-breaking character, use a safe display form in the Inputs column while preserving unambiguous identification.

If an input filename must be sanitized for the Generation and Review Log Inputs column, the sanitized display form must remain unique among consolidated files and recoverably identifiable.

Escape vertical bars `|` in Generation and Review Log table cell values so the Markdown table remains valid.

If malformed target files were ignored, mention them concisely in the Notes column.

If incomplete target files were used despite missing reference or log sections, mention them concisely in the Notes column.

If duplicate-source handling affected consolidation, mention it concisely in the Notes column.

If UTC was used instead of Europe/Amsterdam time, mention `UTC used for timestamp` in the Notes column.

Do not copy all intermediate generation log rows into the canonical page.

Intermediate generation history remains available in the intermediate files themselves.

---

## Output and commit requirements

Do not output the generated page content in the chat under normal successful operations.

Do not output Markdown replacement blocks in the chat under normal successful operations.

Do not create a ZIP package.

Do not create a manifest file.

Do not create branches.

Do not open pull requests.

Commit exactly one file directly to `main`:

```text
docs/stereotypes/<target-stereotype-group>/<target-stereotype-id>.md
```

Before committing, verify that the repository write operation targets exactly one file path and that the path exactly equals the target canonical file path.

If using a local working tree, also verify that the working tree diff contains exactly one modified file.

Use the current blob SHA of the target canonical page when the repository update mechanism supports or requires it. If the available write mechanism uses another optimistic concurrency guard, use that guard. If no concurrency guard is available, report `COMMIT_VALIDATION_FAILED` and do not commit anything.

If the repository update fails because the target file changed after preflight, report `COMMIT_FAILED` and state that the target page changed before commit.

Before committing, verify that:

- the repository write operation targets exactly one file path;
- the target path exactly equals the target canonical file path;
- no other file is changed;
- the target canonical page was skeletal before modification;
- the generated page follows the required canonical page template;
- the generated page is valid UTF-8 Markdown;
- the generated page uses LF line endings and a final newline;
- heading order is correct;
- the Generation and Review Log table remains valid Markdown;
- fenced-code syntax, if any appears inside preserved quotations, does not break the page structure.

If commit preparation or validation fails, report `COMMIT_VALIDATION_FAILED` and do not commit anything.

If `COMMIT_VALIDATION_FAILED` occurs, do not output the generated Markdown unless the validation failure is unrelated to page content, template structure, source-grounding, UTF-8 validity, Markdown validity, path safety, repository target path, or overwrite safety.

If the repository write operation fails, report `COMMIT_FAILED` and include a brief explanation.

If `COMMIT_FAILED` occurs after the generated canonical page has passed all content, template, source-grounding, UTF-8, Markdown, and path-safety validation checks, first determine whether the repository write operation clearly did not modify the target file.

If the target file was clearly not modified, output the complete generated canonical Markdown text inside a clear Markdown code block immediately after the error token so that the work product can be manually recovered.

If repository mutation status is uncertain, attempt to re-read the target file from `main`.

If the committed content already matches the generated page, report `COMMIT_RESULT_UNAVAILABLE` or `COMMIT_RESULT_UNVERIFIED` as applicable.

If mutation status remains uncertain, report `COMMIT_STATUS_UNCERTAIN` and do not output recovery Markdown unless manual recovery output is explicitly allowed for the run.

After a successful repository write operation, re-read the committed target file from `main` at the returned commit SHA when supported. If commit-SHA-specific reading is unavailable, re-read the target file from latest `main`.

For post-commit verification, compare UTF-8 decoded text after normalizing line endings to LF. Do not ignore any other content differences.

Verify that the committed file content matches the generated canonical page under that comparison rule.

If the repository write operation reports success but no commit SHA is available, attempt post-write content verification from latest `main`.

If the content matches the generated canonical page, report `COMMIT_RESULT_UNAVAILABLE` and include the modified file path and commit message.

If the content cannot be verified, report `COMMIT_RESULT_UNVERIFIED`.

If the content differs, report `COMMIT_RESULT_MISMATCH`.

Do not report normal successful completion unless both conditions hold:

1. a commit SHA is available;
2. post-commit verification confirms that the committed target file content matches the generated canonical page.

If the committed content cannot be verified, report `COMMIT_RESULT_UNVERIFIED` and include the modified file path, commit message, and commit SHA if available.

If the committed content differs from the generated page, report `COMMIT_RESULT_MISMATCH` and include the modified file path, commit message, and commit SHA if available.

If the commit succeeds but the commit SHA is unavailable, report `COMMIT_RESULT_UNAVAILABLE` and include the modified file path and commit message if available.

If the repository write operation returns an ambiguous failure and the target file state cannot be confidently determined after re-reading `main`, report `COMMIT_STATUS_UNCERTAIN` and do not output generated Markdown unless manual recovery output is explicitly allowed for the run.

On successful validation, do not ask for additional confirmation. Proceed with the commit.

On successful commit and successful post-commit verification, respond only with a concise confirmation containing:

- modified file path;
- commit SHA;
- commit message;
- number of valid target intermediate files consolidated;
- number of malformed target files ignored, if any;
- number of incomplete but used target files, if any;
- duplicate-source handling, if applicable;
- timestamp basis if UTC was used.

---

## Final self-check before committing

Before committing to `main`, verify that:

1. the run configuration contains a target intermediate folder URL;
2. the target intermediate folder URL has been normalized by removing trailing slashes, query parameters, and fragments;
3. the normalized target intermediate folder URL matches the required GitHub URL structure;
4. the URL ref is exactly `main`;
5. the URL decoded path contains no encoded slashes, encoded backslashes, dot segments, control characters, or character sequence that would alter the normalized repository-relative path;
6. the repository is exactly `pedropaulofb/ontouml-according-to-the-machines`;
7. the branch to read from and update is exactly `main`;
8. repository read access is available;
9. repository write access is available;
10. a complete enumerable set of direct child Markdown files was established for the target intermediate folder;
11. the configured target stereotype group and ID match the controlled mapping;
12. the target display name was generated from the controlled mapping;
13. the target canonical file path is correct and normalized using POSIX path semantics;
14. the target canonical file path does not contain `..`, a leading slash, a drive prefix, or backslashes;
15. the current target canonical page exists;
16. the current target canonical page is skeletal;
17. current target canonical page skeletal status was determined confidently;
18. optional front matter, if present, is non-substantive and safe to overwrite;
19. current date and current datetime were generated from the execution environment;
20. prompt ID, prompt title, prompt version, and prompt file path use the fixed v1.0.0 values;
21. the generated page heading uses the controlled target display name;
22. repository paths remain kebab-case;
23. valid target intermediate files were processed in lexicographic order by repository-relative path;
24. only valid intermediate files matching the target stereotype are consolidated;
25. malformed target files, if present, are ignored and reported in the generation log notes;
26. incomplete but used target files, if present, are reported in the generation log notes;
27. duplicate copies or regenerated variants are not treated as independent support;
28. no current canonical page content is used as evidence;
29. no external knowledge is used;
30. no examples are generated;
31. no diagrams are generated;
32. `Stereotype Profile` remains exactly `TBD in a later phase.`;
33. `Examples` remains exactly `TBD in a later phase.`;
34. all important claims are grounded in supplied valid target intermediate files;
35. claims supported by only one valid target intermediate file use cautious wording unless presented as central definitions, central constraints, or central characterizations;
36. no definitions, hierarchy placement, constraints, modeling guidance, anti-patterns, or distinctions are inferred unless explicitly supported;
37. internal claim-to-intermediate-file traceability was used to prevent unsupported claims;
38. repeated claims are deduplicated;
39. complementary claims are synthesized;
40. conflicting claims are handled conservatively;
41. direct quotations are preserved exactly;
42. direct citation bullets remain valid Markdown even when quotation text contains Markdown-significant characters;
43. duplicate direct quotations preserve all distinct source attributions where available;
44. consulted sources are merged and deduplicated only when source identity and source scope are equivalent;
45. source scope information is preserved where available;
46. `Direct Citations` contains citation bullets or exactly `None.`;
47. `Consulted Sources` contains source bullets or exactly `None.`;
48. the generation log includes one consolidation row;
49. the generation log Inputs field uses a comma-separated and space-separated list of short file IDs or filenames, excluding full paths;
50. vertical bars in generation log table cells are escaped;
51. sanitized input filename display forms, if any, remain unique and recoverably identifiable;
52. the generated page is valid UTF-8 Markdown;
53. the generated page uses LF line endings and a final newline;
54. heading order is correct;
55. the Generation and Review Log table remains valid Markdown;
56. the repository write operation targets exactly one file path;
57. the committed file path exactly equals the generated target canonical file path;
58. the repository update uses the current blob SHA or another available optimistic concurrency guard;
59. no files under `work-products/`, `references/`, `prompts/`, `docs/methodology/`, or `mkdocs.yml` are modified;
60. no branch is created;
61. no pull request is opened;
62. no merge is performed.

After committing, verify that:

63. the committed target file can be re-read from `main` at the returned commit SHA when supported, or from latest `main` otherwise;
64. post-commit verification compares UTF-8 decoded text after normalizing line endings to LF and ignores no other content differences;
65. normal successful completion is reported only if a commit SHA is available and the committed file content matches the generated canonical page;
66. if no commit SHA is available but the content matches latest `main`, `COMMIT_RESULT_UNAVAILABLE` is reported instead of normal success;
67. if committed content cannot be verified, `COMMIT_RESULT_UNVERIFIED` is reported;
68. if committed content differs from the generated page, `COMMIT_RESULT_MISMATCH` is reported;
69. if repository mutation status remains uncertain after re-reading `main`, `COMMIT_STATUS_UNCERTAIN` is reported;
70. the final response reports the modified file path, commit SHA, commit message, consolidation counts, duplicate-source handling if applicable, and timestamp basis if UTC was used.