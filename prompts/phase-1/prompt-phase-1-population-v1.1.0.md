# Prompt: Phase 1 Population — Source-Grounded Intermediate File Generation
# Version: 1.1.0

You are helping populate the documentation project "OntoUML According to the Machines".

This execution belongs to Phase 1 — Groundwork and Initial Population.

Phase 1 is a content-only phase. Its purpose is to produce structured, source-grounded, first-pass intermediate content for OntoUML stereotype pages based on selected high-yield input sources. The resulting content is provisional and intended for later consolidation, review, refinement, and normalization.

You are evaluating and transforming one supplied input source into downloadable source-specific intermediate Markdown files. You are not producing final documentation pages. You are not performing final expert validation. You are not committing anything to a repository.

---

## Run configuration

The user must provide only the run-specific information below.

- Input source identifier: <bibliographic reference, filename, document title, or other stable identifier>
- Input source type: <full document | excerpt | notes | other>
- Source scope: <full document, chapter, section, page range, excerpt label, notes scope, or other precise scope statement>

If any required run-configuration field is missing, report `MISSING_RUN_CONFIGURATION`, list the missing field or fields, and do not generate any package.

Do not require the user to provide technical execution metadata such as current date, current datetime, prompt ID, prompt version, prompt file path, input source short ID, or output package name. Generate those fields yourself as specified below.

---

## Auto-generated execution metadata

Generate the execution metadata below yourself.

When file generation is available, compute the current date, current datetime, input source short ID, and output package name once inside the same file-generation routine used to create the ZIP package. Reuse those exact computed values consistently in:

- the ZIP package filename;
- all generated intermediate file paths;
- every generated file's Generation and Review Log;
- the final concise confirmation message.

Use the current execution environment to determine the current date and current datetime.

If local time is available, use local time. If only UTC is available, use UTC.

Use these exact formats:

- Current date: `YYYY-MM-DD`
- Current datetime: `YYYY-MM-DDtHHMM`

The `Current datetime` must contain no spaces and no colons.

Use these fixed prompt metadata values:

- Prompt ID: `prompt-phase-1-population-v1.1.0`
- Prompt title: `Phase 1 Population — Source-Grounded Intermediate File Generation`
- Prompt version: `1.1.0`
- Prompt file path: `prompts/phase-1/prompt-phase-1-population-v1.1.0.md`

Generate an `Input source short ID` from the supplied `Input source identifier` and `Source scope`.

The `Input source short ID` must be:

- lowercase;
- ASCII-only;
- kebab-case;
- suitable for filenames;
- concise but recognizable;
- no spaces;
- no underscores;
- no punctuation except hyphens.

Examples:

- `guizzardi-2005-thesis-chapter-04`
- `guizzardi-2005-thesis-section-05-03`
- `ontouml-profile-2018`
- `ontouml-vp-docs`

Generate the `Output package name` using this pattern:

```text
<current-datetime>-<input-source-short-id>.zip
```

Example:

```text
2026-06-05t1432-guizzardi-2005-thesis-chapter-04.zip
```

If you cannot determine the current date or current datetime from the execution environment, report `EXECUTION_DATETIME_UNAVAILABLE` and do not generate any package.

---

## Required output mode

The required output is a downloadable ZIP package.

Do not output Markdown replacement blocks in the chat.

Do not output generated intermediate file contents as plain text in the chat.

Do not provide a textual fallback.

The ZIP package must contain all generated source-specific intermediate Markdown files.

The ZIP package must preserve repository-relative paths for generated files.

Do not include a manifest file.

Do not commit files to the repository.

Do not create branches.

Do not open pull requests.

Those repository application tasks are handled by a separate prompt or workflow.

When file generation is available in the current environment, create the ZIP package programmatically using the available file-generation mechanism, such as background code execution or another supported file-writing tool.

Generated Markdown content may be handled internally as file content or string content during package creation. This does not violate the “do not output file contents in the chat” rule, as long as the generated Markdown file contents are not printed or rendered in the chat response.

When using background code execution to create files, write files as UTF-8 text and use safe multiline string or file-writing methods so that Markdown syntax, pipes, angle brackets, em dashes, quotation marks, and backticks are preserved correctly.

On successful package generation, respond only with the downloadable ZIP package and a concise confirmation containing the package name. Do not print generated file contents.

Example package structure:

```text
work-products/
  phase-1/
    intermediate/
      stereotypes/
        classes/
          kind/
            2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
          role/
            2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
        relations/
          mediation/
            2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
```

If downloadable ZIP/file generation is not available in the current environment, output only:

```text
FILE_OUTPUT_UNAVAILABLE

The current environment cannot create or attach a downloadable ZIP package. No intermediate Markdown files were generated.
```

Then stop.

If file generation is available but the package cannot be completed safely, output only:

```text
PACKAGE_GENERATION_FAILED

<Brief explanation of why the complete package could not be generated. No partial package was created.>
```

Then stop.

If package generation fails because of an execution error, file-system error, encoding issue, compression error, or size/output limitation, report `PACKAGE_GENERATION_FAILED` and briefly state the cause. Do not output partial generated file contents in the chat.

Do not create partial packages.

Do not create incomplete files.

---

## Valid target work-product paths

Generated intermediate files must be placed inside the ZIP package using repository-relative paths only under:

- `work-products/phase-1/intermediate/stereotypes/classes/`
- `work-products/phase-1/intermediate/stereotypes/relations/`

Do not generate files under `docs/`.

Do not generate files under `references/`.

Do not generate files under `prompts/`.

Do not invent other work-product directories.

Use this exact path pattern:

```text
work-products/phase-1/intermediate/stereotypes/<classes-or-relations>/<stereotype-id>/<current-datetime>-<input-source-short-id>.md
```

Examples:

```text
work-products/phase-1/intermediate/stereotypes/classes/kind/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
work-products/phase-1/intermediate/stereotypes/classes/role-mixin/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
work-products/phase-1/intermediate/stereotypes/relations/mediation/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
work-products/phase-1/intermediate/stereotypes/relations/component-of/2026-06-05t1432-guizzardi-2005-thesis-chapter-04.md
```

Use the existing repository filename convention for stereotype IDs:

- lowercase names;
- words separated by hyphens;
- no spaces;
- no underscores.

Examples:

- `kind`
- `role-mixin`
- `sub-quantity-of`
- `component-of`

---

## Valid stereotype groups

Only the following stereotype groups are valid:

- `classes`
- `relations`

Do not invent other stereotype groups.

Valid class stereotype IDs include:

- `abstract`
- `category`
- `collective`
- `datatype`
- `enumeration`
- `event`
- `historical-role-mixin`
- `historical-role`
- `kind`
- `mixin`
- `mode`
- `phase-mixin`
- `phase`
- `quality`
- `quantity`
- `relator`
- `role-mixin`
- `role`
- `situation`
- `subkind`
- `type`

Valid relation stereotype IDs include:

- `brings-about`
- `characterization`
- `comparative`
- `component-of`
- `creation`
- `external-dependence`
- `historical-dependence`
- `instantiation`
- `manifestation`
- `material`
- `mediation`
- `member-of`
- `participation`
- `participational`
- `sub-collection-of`
- `sub-quantity-of`
- `termination`
- `triggers`

---

## Core instruction

Analyze the single selected input source provided under "Input source material".

Generate source-specific intermediate Markdown files only for OntoUML stereotype pages that are directly and substantively informed by that source.

Each generated file must contain only the contribution of the supplied input source to one stereotype.

Do not attempt to consolidate multiple sources.

Do not attempt to produce final documentation pages.

Do not read, update, or merge with existing `docs/stereotypes/` pages.

Do not read, update, or merge with existing intermediate files.

Use only the supplied input source for this execution unless additional sources are explicitly included in the "Input source material" section.

Do not use prior knowledge, general OntoUML knowledge, external sources, inferred theory, or unstated assumptions.

If a claim cannot be directly supported by the supplied source, omit it.

---

## Scope restrictions

This task is limited to generating source-specific intermediate content for later consolidation.

Do not propose, generate, or modify:

- final documentation pages under `docs/`;
- website formatting;
- visual identity;
- CSS;
- MkDocs configuration;
- navigation;
- deployment;
- repository structure;
- automation;
- diagrams;
- examples;
- complete stereotype profiles;
- branches;
- commits;
- pull requests.

Do not provide general project-management advice.

Do not suggest changes to pages outside the generated intermediate files.

---

## Page selection rule

Generate an intermediate file for a stereotype only if the input source provides substantive information about that stereotype.

Substantive information includes at least one of the following:

- a definition;
- a conceptual characterization;
- an ontological explanation;
- a constraint;
- a distinction from related categories;
- a role in OntoUML or UFO theory;
- terminology that directly clarifies the stereotype.

Do not generate an intermediate file if the stereotype is only mentioned in passing.

Do not generate an intermediate file if the source is ambiguous, insufficient, or not directly relevant to that stereotype.

If no target stereotypes are substantively informed by the supplied source, generate no package and output only:

```text
NO_INTERMEDIATE_FILES_GENERATED

The supplied source does not substantively inform any target stereotype page. No intermediate Markdown files were generated.
```

Then stop.

---

## Handling uncertainty and conflicts

Avoid uncertain claims.

If the source is unclear, incomplete, or insufficient for a claim, omit the claim.

If the input source contains internal tension or conflict:

- prefer the clearest and most directly relevant passage;
- do not resolve theoretical conflicts using external knowledge;
- do not speculate beyond the source;
- if the conflict prevents a reliable Phase 1 source-specific contribution for a stereotype, skip that stereotype.

---

## Package generation requirements

Generate one complete ZIP package for the supplied input source.

The package must include all approved source-specific intermediate files.

There is no arbitrary per-response limit on the number of generated files. If the input source substantively informs ten stereotype pages and the complete package can be generated safely, generate ten intermediate Markdown files in the ZIP package.

If the complete package would likely be too large or complex to generate safely in the current environment, do not generate a partial package. Instead, report `PACKAGE_GENERATION_FAILED` and recommend processing a smaller source chunk.

Do not create a package if no intermediate files are generated.

Do not create a partial package.

Do not include a manifest.

Do not include files outside `work-products/phase-1/intermediate/stereotypes/`.

---

## Intermediate file template

Each generated intermediate file must use exactly this structure:

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
| <Current date> | Phase 1 | <Agent/model> | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | <Input source identifier>. Scope: <Source scope>. | Source-specific intermediate file generated at <Current datetime>; not a final documentation page; intended for later consolidation. |
```

---

## Source-Specific Description Contribution requirements

The `Source-Specific Description Contribution` section is the main content target for this prompt.

It must be:

- technical;
- concise;
- documentation-like;
- source-grounded;
- provisional;
- limited to the supplied input source;
- suitable for later consolidation, human review, or agentic review.

It should explain only what the supplied source supports.

Focus on:

- what the source says or supports about the stereotype;
- what the stereotype means according to the supplied source;
- what kind of entity, relation, or modeling construct it classifies, if supported by the source;
- which conceptual distinctions the source supports;
- which constraints or commitments the source explicitly provides;
- how the source situates the stereotype in OntoUML or UFO, when applicable.

Do not include:

- examples;
- diagrams;
- full stereotype profiles;
- unsupported generalizations;
- speculative synthesis;
- claims based only on memory;
- claims that would require other sources to verify;
- content from existing pages or previous intermediate files unless explicitly included in the supplied input source.

---

## Citation and source-grounding requirements

Every important claim must be traceable to the supplied input source.

Prefer paraphrase.

Use direct quotations only when exact wording is important, especially for definitions or central conceptual claims.

When using direct quotations:

- keep them short;
- preserve exact wording;
- use one bullet per quotation;
- include a locator when available, such as page number, section number, heading, paragraph number, or excerpt label;
- ensure the surrounding intermediate content makes clear which claim the quotation supports.

Use this exact format under `Direct Citations` when quotations are used:

- "<short exact quotation>" — Source: <Input source identifier>; Locator: <page, section, heading, paragraph, or excerpt label if available>.

If no locator is available, use:

- "<short exact quotation>" — Source: <Input source identifier>.

If no direct quotation is necessary, output exactly:

None.

under `Direct Citations`.

Do not add any explanatory sentence under `Direct Citations` other than citation bullets or `None.`.

Always list the processed input source and source scope under `Consulted Sources`.

---

## Final self-check before answering

Before producing the final answer or package, verify that:

1. all required run-configuration fields are available;
2. current date and current datetime were generated from the execution environment;
3. prompt ID, prompt title, prompt version, and prompt file path use the fixed v1.1.0 values;
4. input source short ID and output package name were generated correctly;
5. the ZIP package filename, generated file paths, generation logs, and final confirmation all use the same computed current datetime and input source short ID;
6. downloadable ZIP/file generation is available in the current environment;
7. if downloadable ZIP/file generation is not available, only `FILE_OUTPUT_UNAVAILABLE` is reported;
8. if package generation fails, only `PACKAGE_GENERATION_FAILED` is reported;
9. if no stereotype is substantively informed, only `NO_INTERMEDIATE_FILES_GENERATED` is reported;
10. no textual Markdown replacement blocks are output in the chat;
11. generated Markdown content is written only as package file content, not printed in the chat;
12. if background code execution is used, file content is written safely as UTF-8 text and Markdown syntax is preserved;
13. only the supplied input source was used;
14. only valid paths under `work-products/phase-1/intermediate/stereotypes/classes/` or `work-products/phase-1/intermediate/stereotypes/relations/` were used;
15. no files under `docs/`, `references/`, or `prompts/` were generated or modified;
16. no examples were generated;
17. no diagrams were generated;
18. the `Stereotype Profile` section remains exactly `TBD in a later phase.`;
19. the `Examples` section remains exactly `TBD in a later phase.`;
20. only substantively supported stereotype intermediate files are generated;
21. every important claim is grounded in the supplied source;
22. the consulted source and source scope are listed in every generated file;
23. direct quotations, if any, follow the required bullet format;
24. direct quotations, if any, are short and used only for key definitions or central claims;
25. the generation log uses the expanded future-proof table: Date, Phase, Agent, Action, Prompt ID, Prompt Title, Inputs, Notes;
26. the generation log uses the generated date, generated current datetime, agent/model, prompt ID, prompt title, input source identifier, and source scope;
27. no website, navigation, formatting, deployment, automation, repository-structure, branch, commit, or pull-request changes are proposed;
28. the ZIP package preserves repository-relative paths;
29. no manifest file is included;
30. no partial package or incomplete file is created.

---

## Input source material

<Paste the selected source text, excerpt, notes, or attached-file instruction here>