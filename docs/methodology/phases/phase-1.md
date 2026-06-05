# Phase 1 — Groundwork and Initial Population

Phase 1 is the first content-production phase of **OntoUML According to the Machines**.

Its purpose is to do the groundwork for the stereotype documentation by extracting source-grounded, source-specific intermediate content from selected high-yield resources. The resulting work products are expected to be useful, technically oriented, traceable, and provisional. They are not final documentation pages.

## Purpose

Phase 1 has two main goals:

1. produce source-specific intermediate content for OntoUML stereotype pages;
2. create a structured evidence base that can later be consolidated into first complete stereotype pages.

The phase prioritizes coverage of relevant source material over final completeness. It is intended to transform difficult, information-rich sources into reviewable intermediate work products for the affected stereotypes.

Phase 1 does not aim to produce final, authoritative, or fully reviewed OntoUML documentation.

## Scope

Phase 1 is limited to content work.

It may generate intermediate files when selected source material provides substantive information about one or more OntoUML stereotypes.

Phase 1 does not include:

- website formatting;
- visual identity work;
- CSS or theme changes;
- navigation redesign;
- diagram creation;
- example creation;
- complete stereotype profiles;
- deep expert validation;
- agent-based refinement;
- changes to the general site architecture;
- direct commits, branches, pull requests, or repository mutation by the population prompt.

These exclusions apply to Phase 1 and are expected to hold for later project phases unless explicitly revised.

## Execution model

Phase 1 is executed manually using regular ChatGPT.

It is not an agentic workflow. Agents are not part of the Phase 1 population method.

The Phase 1 population prompt is expected to be run multiple times, once per selected input file, source unit, chapter, section, excerpt, or note set. Each execution analyzes one supplied input source and generates source-specific intermediate files only for stereotypes that are directly and substantively informed by that source.

For example:

- execution 1 processes input source X;
- if source X contains substantive information about stereotypes A and B, intermediate files are generated for A and B;
- execution 2 processes input source Y;
- if source Y contains substantive information about stereotypes B and C, separate intermediate files are generated for B and C.

The order of population is therefore determined by the content of the selected input files, not by the current navigation order or by a predefined stereotype sequence.

## Input model

Phase 1 uses manually selected source material.

Sources should be selected because they are expected to define, explain, or substantially inform OntoUML stereotypes. Examples of suitable inputs include:

- Giancarlo Guizzardi's PhD thesis;
- main OntoUML papers;
- UFO and OntoUML papers by Guizzardi and collaborators;
- existing OntoUML documentation;
- other selected authoritative or high-yield resources.

Large or dense sources should be processed in smaller source units, such as chapters, sections, page ranges, excerpts, or note sets. The source scope must be recorded explicitly for each execution.

A complete thesis or long paper should not normally be processed as one input if it can be divided into coherent source units.

## Population prompt

The first Phase 1 prompt is the population prompt.

Its current intended prompt identity is:

| Field | Value |
|---|---|
| Prompt ID | `prompt-phase-1-population-v1.2.4` |
| Prompt title | `Phase 1 Population — Source-Grounded Intermediate File Generation` |
| Prompt path | `prompts/phase-1/prompt-phase-1-population-v1.2.4.md` |

The population prompt should require only minimal run-specific information from the user:

| Field | Meaning |
|---|---|
| Input source identifier | Bibliographic reference, filename, document title, or other stable identifier. |
| Input source type | One of `full document`, `excerpt`, `notes`, or `other`. |
| Source scope | Full document, chapter, section, page range, excerpt label, notes scope, or other precise scope statement. |

The prompt should generate technical metadata itself, including current date, current datetime, prompt ID, prompt version, prompt file path, input source short ID, and output package name.

The generated timestamp and source short ID should be computed once and reused consistently in the ZIP package name, intermediate file paths, generation logs, and final confirmation.

## Output model

Each Phase 1 population execution should generate a downloadable ZIP package containing source-specific intermediate Markdown files.

The population prompt should not output full generated Markdown contents in the chat.

The population prompt should not generate final documentation files under `docs/`.

The population prompt should not commit files, create branches, or open pull requests.

If file generation is unavailable, the prompt should report that clearly and stop. It should not provide a textual fallback containing generated file contents.

If no target stereotype is substantively informed by the supplied source, the prompt should generate no package and report that no intermediate files were generated.

## Intermediate work-product location

Intermediate files should be generated inside the ZIP package using repository-relative paths under:

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

Intermediate files should not be generated under `docs/`, `references/`, or `prompts/`.

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

## Citation and reference requirements

Phase 1 uses a strict citation expectation.

Every important claim should be grounded in the supplied input source. The goal is not only to generate content, but also to preserve enough source traceability for later consolidation and review.

Direct quotations may be used when they support key definitions or especially important claims. They should not be overused.

Each intermediate file should distinguish between:

### Direct Citations

Exact quoted passages used to support specific claims in the intermediate file. Direct citations should be short and should include a locator when available, such as page number, section number, heading, paragraph number, or excerpt label.

The expected direct citation format is:

```markdown
- "<short exact quotation>" — Source: <Input source identifier>; Locator: <page, section, heading, paragraph, or excerpt label if available>.
```

If no direct quotation is necessary, the section should contain exactly:

```text
None.
```

### Consulted Sources

The supplied input source used to generate the intermediate file, including the source scope.

If a source informs intermediate content, it should be listed as a consulted source.

## Handling uncertainty and conflicts

Phase 1 should avoid uncertain claims rather than include them.

If a claim cannot be supported from the supplied input source, it should not be added in the intermediate file.

If the input source contains internal tension or conflict, the prompt should prefer the clearest and most directly relevant passage. It should not resolve theoretical conflicts using external knowledge. If the conflict prevents a reliable source-specific contribution for a stereotype, the stereotype should be skipped for that execution.

## Relationship to final stereotype pages

Phase 1 population does not directly update the canonical stereotype pages under `docs/stereotypes/`.

Instead, it produces source-specific intermediate files. A later consolidation prompt should read the intermediate files for one stereotype and synthesize a first consolidated page under the canonical documentation structure.

The intended pipeline is:

```text
selected source unit
-> population prompt
-> source-specific intermediate files
-> consolidation prompt
-> first consolidated stereotype page
-> review and refinement in later phases
```

For consolidation, the recommended unit is one stereotype at a time. Intermediate files should be grouped by stereotype before consolidation.

## Generation and review log

Each generated intermediate file should include a Phase 1 generation log entry.

The log entry should record:

- date;
- phase;
- agent name and version;
- action performed;
- prompt ID;
- prompt title;
- input source identifier;
- source scope;
- notes clarifying that the file is source-specific, intermediate, and intended for later consolidation.

The log should make clear that the file was generated during Phase 1 and remains provisional.

## Completion criteria

Phase 1 population is complete when all selected major input sources or source units have been processed and all source-specific intermediate files have been generated for the stereotypes substantively informed by those inputs.

Some stereotypes may still have no intermediate files after Phase 1 population. A stereotype is not required to receive intermediate content if the selected Phase 1 inputs do not provide relevant content for it.

Additional success criteria are:

- generated intermediate files are source-specific;
- generated intermediate files are stored under the expected `work-products/phase-1/intermediate/stereotypes/` structure;
- each generated intermediate file lists consulted sources and source scope;
- each generated intermediate file has a generation log entry;
- generated content is clearly marked as provisional and intermediate;
- no generated population output directly modifies canonical `docs/stereotypes/` pages.

## Deferred work

The following work is deferred to later phases or later Phase 1 prompts:

- consolidation of intermediate files into canonical stereotype pages;
- examples;
- diagrams;
- complete stereotype profiles;
- terminology normalization;
- systematic cross-page consistency checks;
- expert-level validation;
- agent-assisted refinement;
- conflict analysis beyond source-local handling;
- visual or structural website improvements.

## Risks

Phase 1 carries known risks:

- hallucinated claims;
- misread source material;
- oversimplification;
- citation gaps;
- inconsistent terminology across intermediate files;
- uneven intermediate file quality;
- overconfidence in generated content;
- excessive dependence on difficult sources;
- loss of nuance from UFO or OntoUML theory;
- duplication or overlap across source-specific intermediate files;
- later consolidation bias if one source dominates the available intermediate files.

These risks are acceptable only because Phase 1 is explicitly provisional and designed to support later consolidation and review.

## Expected readers

Phase 1 intermediate content primarily serves:

- the project maintainer;
- future consolidation prompts;
- future review agents.

The content should therefore be useful for later consolidation and refinement work, not merely readable as final educational material.

## Relationship to later phases

Later phases are not specified in detail here.

Phase 1 establishes a source-grounded intermediate content base. Future phase documentation should define its own purpose, execution model, and quality expectations.
