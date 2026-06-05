# Phase 1 — Groundwork and Initial Population

Phase 1 is the first content-production phase of **OntoUML According to the Machines**.

Its purpose is to create a source-grounded first version of the stereotype documentation. Phase 1 does this in two steps:

1. generate source-specific intermediate files from selected high-yield sources;
2. consolidate those intermediate files into the first canonical stereotype pages.

The resulting canonical pages are still provisional. They are first consolidated documentation pages, not final expert-validated OntoUML documentation.

## Purpose

Phase 1 has three main goals:

1. extract source-specific contributions from selected OntoUML and UFO resources;
2. preserve source traceability through intermediate files, citations, consulted sources, and generation logs;
3. consolidate the intermediate files into first canonical stereotype pages under `docs/stereotypes/`.

The phase prioritizes source-grounded coverage and traceable first-pass synthesis over final completeness.

Phase 1 does not aim to produce final, authoritative, or fully reviewed OntoUML documentation.

## Scope

Phase 1 is limited to content work for stereotype documentation.

It includes:

- source-specific extraction into intermediate work products;
- consolidation of intermediate files into first canonical stereotype pages;
- direct updates to skeletal canonical stereotype pages during the consolidation step;
- generation and review log entries for both intermediate and consolidated artifacts.

Phase 1 does not include:

- website formatting;
- visual identity work;
- CSS or theme changes;
- navigation redesign;
- diagram creation;
- example creation;
- complete stereotype profiles;
- deep expert validation;
- agent-based refinement beyond the defined prompt executions;
- changes to the general site architecture;
- pull requests or branch-based review workflows.

These exclusions apply to Phase 1 and are expected to hold for later project phases unless explicitly revised.

## Execution model

Phase 1 is executed manually using regular ChatGPT and repository tools.

The phase uses two prompts:

1. a population prompt, run once per selected source unit;
2. a consolidation prompt, run once per stereotype.

The population prompt generates source-specific intermediate files. The consolidation prompt reads the intermediate files for one stereotype and commits the first consolidated canonical page directly to `main`, provided that the current canonical page is empty or skeletal.

This direct commit behavior is intentionally limited to Phase 1 because the target canonical pages are initially skeletal. Later phases should not assume that direct commits to `main` remain appropriate.

## Input model

Phase 1 uses manually selected source material.

Sources should be selected because they are expected to define, explain, or substantially inform OntoUML stereotypes. Examples of suitable inputs include:

- Giancarlo Guizzardi's PhD thesis;
- main OntoUML papers;
- UFO and OntoUML papers by Guizzardi and collaborators;
- existing OntoUML documentation;
- other selected authoritative or high-yield resources.

Large or dense sources should be processed in smaller source units, such as chapters, sections, page ranges, excerpts, or note sets. The source scope must be recorded explicitly for each population execution.

A complete thesis or long paper should not normally be processed as one input if it can be divided into coherent source units.

## Prompt 1 — Population

The first Phase 1 prompt is the population prompt.

| Field | Value |
|---|---|
| Prompt ID | `prompt-phase-1-population-v1.1.0` |
| Prompt title | `Phase 1 Population — Source-Grounded Intermediate File Generation` |
| Prompt path | `prompts/phase-1/prompt-phase-1-population-v1.1.0.md` |

The population prompt is run once per selected source unit.

It requires only minimal run-specific information from the user:

| Field | Meaning |
|---|---|
| Input source identifier | Bibliographic reference, filename, document title, or other stable identifier. |
| Input source type | One of `full document`, `excerpt`, `notes`, or `other`. |
| Source scope | Full document, chapter, section, page range, excerpt label, notes scope, or other precise scope statement. |

The population prompt generates technical metadata itself, including current date, current datetime, prompt ID, prompt version, prompt file path, input source short ID, and output package name.

### Population output

Each population execution generates a downloadable ZIP package containing source-specific intermediate Markdown files.

The ZIP package preserves repository-relative paths under:

```text
work-products/phase-1/intermediate/stereotypes/
```

The expected path pattern is:

```text
work-products/phase-1/intermediate/stereotypes/<classes-or-relations>/<stereotype-id>/<current-datetime>-<input-source-short-id>.md
```

Examples:

```text
work-products/phase-1/intermediate/stereotypes/classes/kind/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
work-products/phase-1/intermediate/stereotypes/classes/role-mixin/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
work-products/phase-1/intermediate/stereotypes/relations/mediation/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
```

The population prompt does not:

- generate final documentation files under `docs/`;
- commit files to the repository;
- create branches;
- open pull requests;
- generate examples;
- complete stereotype profiles.

If no target stereotype is substantively informed by the supplied source, the population prompt generates no package and reports that no intermediate files were generated.

## Intermediate file structure

Each generated intermediate file should use the following structure:

```markdown
# <Stereotype Name>

## Source-Specific Description Contribution

<Phase 1 source-specific content generated from the supplied input source.>

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

<Direct citation entries using the required bullet format, or exactly: None.>

### Consulted Sources

- <Input source identifier>. Scope: <Source scope>.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| <Current date> | Phase 1 | <agent/model> | Intermediate population | <prompt ID> | <prompt title> | <input source identifier>. Scope: <source scope>. | Source-specific intermediate file generated at <current datetime>; not a final documentation page; intended for later consolidation. |
```

The `Source-Specific Description Contribution` section is the main content target for Phase 1 population. It represents what one supplied source contributes to a later final `Description` section. It should not be treated as the final description of the stereotype.

## Prompt 2 — Consolidation

The second Phase 1 prompt is the consolidation prompt.

| Field | Value |
|---|---|
| Prompt ID | `prompt-phase-1-consolidation-v1.0.5` |
| Prompt title | `Phase 1 Consolidation — Direct Main Commit for One Stereotype` |
| Prompt path | `prompts/phase-1/prompt-phase-1-consolidation-v1.0.5.md` |

The consolidation prompt is run once per stereotype.

It receives one GitHub folder URL pointing to the intermediate files for that stereotype, for example:

```text
https://github.com/pedropaulofb/ontouml-according-to-the-machines/tree/main/work-products/phase-1/intermediate/stereotypes/classes/kind
```

From that URL, the prompt derives:

- target stereotype group;
- target stereotype ID;
- target display name;
- target canonical file path;
- commit message.

The consolidation prompt reads all Markdown files directly under the supplied intermediate folder, processes only files for the target stereotype, and generates exactly one canonical page.

### Consolidation output

The consolidation prompt commits exactly one file directly to `main`:

```text
docs/stereotypes/<classes-or-relations>/<stereotype-id>.md
```

Examples:

```text
docs/stereotypes/classes/kind.md
docs/stereotypes/classes/historical-role-mixin.md
docs/stereotypes/relations/historical-dependence.md
```

Direct commits to `main` are allowed in Phase 1 only because the canonical stereotype pages are expected to be empty or skeletal before consolidation.

Before committing, the consolidation prompt must verify that:

- the target canonical page exists;
- the target canonical page is empty or skeletal;
- the target canonical page is not already substantively populated;
- the output path is exactly the derived canonical path;
- exactly one file will be modified;
- no file outside `docs/stereotypes/classes/` or `docs/stereotypes/relations/` will be changed.

After committing, the prompt verifies that the committed file content matches the generated canonical page.

If the target page is not skeletal, the prompt must stop and report that it cannot safely overwrite the page.

## Canonical page structure after consolidation

Each consolidated canonical page should use the following structure:

```markdown
# <OntoUML VP-style display name>

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
| <Current date> | Phase 1 | <agent/model> | Consolidation | <prompt ID> | <prompt title> | <intermediate file IDs or filenames> | First consolidated stereotype page generated from Phase 1 source-specific intermediate files; not final expert-validated documentation. |
```

The consolidated page contains one new consolidation log entry only. It does not copy the generation logs from the intermediate files. Intermediate generation history remains available in the intermediate files under `work-products/phase-1/intermediate/stereotypes/`.

## Naming conventions

Repository paths and filenames use kebab-case.

Examples:

```text
docs/stereotypes/classes/historical-role-mixin.md
docs/stereotypes/relations/historical-dependence.md
```

Page headings and prose use OntoUML VP-style stereotype display names.

Examples:

```text
HistoricalRoleMixin
HistoricalDependence
RoleMixin
PhaseMixin
ComponentOf
SubQuantityOf
SubCollectionOf
```

Spaced labels such as `Historical Role Mixin` or `Historical Dependence` should not be used in generated page content, except inside exact direct quotations.

Direct quotations preserve exact source wording and should not be normalized.

## Citation and reference requirements

Phase 1 uses a strict citation expectation.

Every important claim should be grounded in the supplied input source or in a valid target intermediate file.

Population files distinguish between:

### Direct Citations

Exact quoted passages used to support specific claims. Direct citations should be short and should include a locator when available, such as page number, section number, heading, paragraph number, or excerpt label.

The expected direct citation format is:

```markdown
- "<short exact quotation>" — Source: <Input source identifier>; Locator: <page, section, heading, paragraph, or excerpt label if available>.
```

If no direct quotation is necessary, the section should contain exactly:

```text
None.
```

### Consulted Sources

The supplied input source used to generate the intermediate or consolidated content, including source scope when available.

If a source informs content, it should be listed as a consulted source.

The consolidation prompt merges consulted sources from the valid target intermediate files and preserves distinct source-scope information.

## Handling uncertainty and conflicts

Phase 1 should avoid uncertain claims rather than include them.

If a claim cannot be supported from the supplied input source or valid target intermediate files, it should not be added.

If source-specific intermediate files conflict, the consolidation prompt should not invent a resolution. It should either omit the contested claim or use cautious wording that reflects only what is safely supported.

Claims supported by only one valid target intermediate file should be worded cautiously unless that intermediate file presents the claim as a central definition, central constraint, or central characterization.

## Results of Phase 1

Phase 1 produces two levels of result:

1. source-specific intermediate files under `work-products/phase-1/intermediate/stereotypes/`;
2. first consolidated canonical stereotype pages under `docs/stereotypes/`.

The intermediate files preserve source-specific extraction and local provenance.

The consolidated pages provide the first coherent documentation pages for each stereotype.

The consolidated pages are still provisional. They are suitable as a starting point for later review, normalization, refinement, expert validation, and example/profile completion.

## Completion criteria

Phase 1 is complete when:

- the selected major source units have been processed with the population prompt;
- generated intermediate files have been committed under `work-products/phase-1/intermediate/stereotypes/`;
- the consolidation prompt has been executed once for every stereotype with available intermediate files;
- each successfully consolidated stereotype has a canonical page under `docs/stereotypes/classes/` or `docs/stereotypes/relations/`;
- each consolidated page contains a source-grounded `Description` section;
- each consolidated page keeps `Stereotype Profile` as `TBD in a later phase.`;
- each consolidated page keeps `Examples` as `TBD in a later phase.`;
- each consolidated page includes `Direct Citations`, `Consulted Sources`, and one consolidation log entry;
- no examples, diagrams, or complete stereotype profiles have been generated;
- no non-skeletal canonical page has been overwritten.

A stereotype is not required to receive a canonical consolidated page if the selected Phase 1 inputs do not provide relevant intermediate content for it.

## Deferred work

The following work is deferred to later phases:

- expert-level validation;
- systematic terminology normalization;
- systematic cross-page consistency checks;
- conflict analysis beyond conservative Phase 1 handling;
- examples;
- diagrams;
- complete stereotype profiles;
- review of direct citations and consulted sources;
- refinement of prose for clarity, pedagogy, and completeness;
- visual or structural website improvements.

## Risks

Phase 1 carries known risks:

- hallucinated claims;
- misread source material;
- oversimplification;
- citation gaps;
- inconsistent terminology across pages;
- uneven page quality;
- overconfidence in generated content;
- excessive dependence on difficult sources;
- loss of nuance from UFO or OntoUML theory;
- duplication or overlap across source-specific intermediate files;
- consolidation bias if one source dominates the available intermediate files;
- direct commits to `main` during consolidation, even though guarded by skeletal-page preflight checks.

These risks are acceptable only because Phase 1 is explicitly provisional and designed to support later review and refinement.

## Expected readers

Phase 1 content primarily serves:

- the project maintainer;
- future review agents;
- later expert or human reviewers;
- future phases of the project.

The content should therefore be useful for later consolidation, review, and refinement work, not treated as final educational material.

## Relationship to later phases

Phase 1 establishes a source-grounded initial documentation base.

Later phases should define their own purpose, execution model, quality expectations, and review criteria. They should treat Phase 1 pages as provisional first-pass outputs requiring validation and refinement.
