# Prompt: Phase 1 Population — Source-Grounded Markdown Update
# Version: 1.0.0

You are helping populate the documentation pages of the project "OntoUML According to the Machines".

This execution belongs to Phase 1 — Groundwork and Initial Population.

Phase 1 is a content-only phase. Its purpose is to produce structured, source-grounded, first-pass content for OntoUML stereotype pages based on selected high-yield input sources. The resulting content is provisional and intended for later review, refinement, and normalization.

You are evaluating and transforming one supplied input source into Markdown page updates. You are not performing final expert validation.

---

## Execution metadata

Use the metadata below exactly. Do not guess missing values.

- Current date: <YYYY-MM-DD>
- Agent/model: <agent or model name/version>
- Prompt ID: prompt-phase-1-population-v1.0.0
- Prompt title: Phase 1 Population — Source-Grounded Markdown Update
- Prompt version: 1.0.0
- Prompt file path: prompts/phase-1/prompt-phase-1-population-v1.0.0.md
- Input source identifier: <bibliographic reference, filename, document title, or other stable identifier>
- Input source type: <full document | excerpt | notes | other>
- Maximum file replacements in this response: 2

If any required metadata field is missing, state which field is missing and do not generate page replacements.

---

## Valid target files

Only the following target groups are valid:

- `docs/stereotypes/classes/`
- `docs/stereotypes/relations/`

Do not invent other stereotype directories.

Use the existing repository filename convention:

- lowercase filenames;
- words separated by hyphens;
- `.md` extension.

Examples:

- `docs/stereotypes/classes/kind.md`
- `docs/stereotypes/classes/role-mixin.md`
- `docs/stereotypes/relations/mediation.md`
- `docs/stereotypes/relations/component-of.md`

---

## Core instruction

Analyze the single selected input source provided under "Input source material".

Produce complete Markdown replacement content only for OntoUML stereotype pages that are directly and substantively informed by that source.

Use only the supplied input source for this execution unless additional sources are explicitly included in the "Input source material" section.

Do not use prior knowledge, general OntoUML knowledge, external sources, inferred theory, or unstated assumptions.

If a claim cannot be directly supported by the supplied source, omit it.

---

## Scope restrictions

This task is limited to stereotype page content.

Do not propose, generate, or modify:

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
- complete stereotype profiles.

Do not provide general project-management advice.

Do not suggest changes to pages outside the affected stereotype pages.

---

## Page selection rule

Update a stereotype page only if the input source provides substantive information about that stereotype.

Substantive information includes at least one of the following:

- a definition;
- a conceptual characterization;
- an ontological explanation;
- a constraint;
- a distinction from related categories;
- a role in OntoUML or UFO theory;
- terminology that directly clarifies the stereotype.

Do not update a page if the stereotype is only mentioned in passing.

Do not update a page if the source is ambiguous, insufficient, or not directly relevant to that stereotype.

For every stereotype considered, make the selection decision explicit in the decision table.

---

## Handling uncertainty and conflicts

Avoid uncertain claims.

If the source is unclear, incomplete, or insufficient for a claim, omit the claim.

If the input source contains internal tension or conflict:

- prefer the clearest and most directly relevant passage;
- do not resolve theoretical conflicts using external knowledge;
- do not speculate beyond the source;
- if the conflict prevents a reliable Phase 1 description, skip the affected stereotype page.

---

## Output control, batching, and continuation

Always start the response with the `Execution metadata used` section.

Then produce the page selection decision table.

Then produce complete Markdown file replacements only for pages marked `Yes`.

Respect the value of `Maximum file replacements in this response`.

Before generating file replacements, perform an internal output-size preflight:

- if all approved file replacements can fit, generate them normally up to the specified maximum;
- if the number of `Yes` pages exceeds the maximum, generate only the first `<maximum>` `Yes` pages, ordered by source relevance, highest priority first;
- if a single file replacement would likely be too long to complete fully, do not start that file replacement;
- instead, list that file under `## Remaining approved files not yet generated` with the reason `single file likely too long for this response`.

Never stop in the middle of a Markdown file replacement.

If output limits are reached despite batching, stop only after a complete `----- END FILE:` delimiter. Do not leave a partial file replacement.

After producing the first batch of file replacements, do not automatically continue with remaining approved files.

If approved files remain after the generated batch:

1. list them under `## Remaining approved files not yet generated`;
2. end the response after that section;
3. wait for explicit user instruction before generating additional file replacements.

Do not ask for approval before producing the first batch.

Do not generate remaining approved files unless the user explicitly asks for the next batch or names specific files to generate.

---

## Required output format

Use exactly this output structure:

## Execution metadata used

| Field | Value |
|---|---|
| Current date | <Current date> |
| Agent/model | <Agent/model> |
| Prompt ID | prompt-phase-1-population-v1.0.0 |
| Prompt title | Phase 1 Population — Source-Grounded Markdown Update |
| Prompt version | 1.0.0 |
| Prompt file path | prompts/phase-1/prompt-phase-1-population-v1.0.0.md |
| Input source identifier | <Input source identifier> |
| Input source type | <Input source type> |
| Maximum file replacements in this response | <Maximum file replacements in this response> |

## Page selection decisions

| File path | Update? | Reason |
|---|---|---|
| docs/stereotypes/<classes-or-relations>/<filename>.md | Yes/No | <brief source-based justification> |

For every generated file replacement, use this delimiter format exactly:

----- BEGIN FILE: docs/stereotypes/<classes-or-relations>/<filename>.md -----
# <Stereotype Name>

## Description

<Phase 1 generated content.>

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

<Direct citation entries using the required bullet format, or exactly: None.>

### Consulted Sources

- <Input source identifier>

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| <Current date> | Phase 1 | <Agent/model> | Population | prompt-phase-1-population-v1.0.0 | Phase 1 Population — Source-Grounded Markdown Update | <Input source identifier> | First-pass description only; stereotype profile and examples deferred. |
----- END FILE: docs/stereotypes/<classes-or-relations>/<filename>.md -----

Repeat the file delimiter block for every generated file replacement.

If approved files remain but are not generated in this response, add:

## Remaining approved files not yet generated

| File path | Reason |
|---|---|
| docs/stereotypes/<classes-or-relations>/<filename>.md | <reason> |

If no pages should be updated, output only:

## Execution metadata used

| Field | Value |
|---|---|
| Current date | <Current date> |
| Agent/model | <Agent/model> |
| Prompt ID | prompt-phase-1-population-v1.0.0 |
| Prompt title | Phase 1 Population — Source-Grounded Markdown Update |
| Prompt version | 1.0.0 |
| Prompt file path | prompts/phase-1/prompt-phase-1-population-v1.0.0.md |
| Input source identifier | <Input source identifier> |
| Input source type | <Input source type> |
| Maximum file replacements in this response | <Maximum file replacements in this response> |

## Page selection decisions

| File path | Update? | Reason |
|---|---|---|
| None | No | The supplied source does not substantively inform any target stereotype page. |

---

## Description section requirements

The `Description` section is the main content target for Phase 1.

It must be:

- technical;
- concise;
- documentation-like;
- source-grounded;
- provisional;
- suitable for later human or agentic review.

It should explain only what the supplied source supports.

Focus on:

- what the stereotype means;
- what kind of entity, relation, or modeling construct it classifies;
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
- claims that would require other sources to verify.

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
- ensure the surrounding page content makes clear which claim the quotation supports.

Use this exact format under `Direct Citations` when quotations are used:

- "<short exact quotation>" — Source: <Input source identifier>; Locator: <page, section, heading, paragraph, or excerpt label if available>.

If no locator is available, use:

- "<short exact quotation>" — Source: <Input source identifier>.

If no direct quotation is necessary, output exactly:

None.

under `Direct Citations`.

Do not add any explanatory sentence under `Direct Citations` other than citation bullets or `None.`.

Always list the processed input source under `Consulted Sources`.

---

## Continuation behavior

If the user later asks for the next batch, continue using the same page selection decisions and the same execution metadata.

When continuing:

- do not repeat file replacements already generated;
- generate only remaining approved files requested by the user, or the next batch if no specific files are named;
- respect the same `Maximum file replacements in this response`;
- keep the same prompt ID, prompt title, prompt version, prompt file path, input source identifier, and source-grounding constraints;
- include the `Execution metadata used` section again;
- include only the remaining relevant rows in `Page selection decisions`;
- include `Remaining approved files not yet generated` again if some approved files still remain.

---

## Final self-check before answering

Before producing the final answer, verify that:

1. all required execution metadata is available;
2. the response starts with `Execution metadata used`;
3. only the supplied input source was used;
4. only valid target paths under `classes` or `relations` were used;
5. no examples were generated;
6. no diagrams were generated;
7. the `Stereotype Profile` section remains exactly `TBD in a later phase.`;
8. the `Examples` section remains exactly `TBD in a later phase.`;
9. only substantively supported pages are marked `Yes`;
10. every important claim is grounded in the supplied source;
11. the consulted source is listed;
12. direct quotations, if any, follow the required bullet format;
13. direct quotations, if any, are short and used only for key definitions or central claims;
14. the generation log uses the expanded future-proof table: Date, Phase, Agent, Action, Prompt ID, Prompt Title, Inputs, Notes;
15. the generation log uses the provided date, agent/model, prompt ID, prompt title, and input source identifier;
16. no website, navigation, formatting, deployment, automation, or repository-structure changes are proposed;
17. no file replacement is left incomplete;
18. if no files are updated, the execution metadata is still included;
19. if approved files remain ungenerated, they are listed under `Remaining approved files not yet generated`;
20. if approved files remain ungenerated, the response does not automatically continue without explicit user instruction;
21. the `Direct Citations` section contains only citation bullets or `None.`.

---

## Input source material

<Paste the selected source text, excerpt, or notes here>