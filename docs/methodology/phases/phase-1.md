# Phase 1 — Groundwork and Initial Population

Phase 1 is the first content-production phase of **OntoUML According to the Machines**.

Its purpose is to do the groundwork for the stereotype documentation by producing a structured first population of page content from selected high-yield source material. The resulting content is expected to be useful, technically oriented, and traceable, but still provisional and subject to later refinement.

## Purpose

Phase 1 has two main goals:

1. populate currently empty stereotype pages with first-pass content;
2. create a structured content base that can be refined in later phases.

The phase prioritizes coverage of relevant page content over final completeness. It is intended to transform difficult, information-rich sources into usable documentation fragments for the affected stereotype pages.

Phase 1 does not aim to produce final, authoritative, or fully reviewed OntoUML documentation.

## Scope

Phase 1 is limited to page content.

It may modify the contents of stereotype documentation pages when selected source material provides relevant information about those stereotypes.

Phase 1 does not include:

- website formatting;
- visual identity work;
- CSS or theme changes;
- navigation redesign;
- diagram creation;
- example creation;
- deep expert validation;
- agent-based refinement;
- changes to the general site architecture.

These exclusions apply to Phase 1 and are expected to hold for later project phases unless explicitly revised.

## Execution model

Phase 1 is executed manually using regular ChatGPT.

It is not an agentic workflow. Agents are not part of the Phase 1 method.

The Phase 1 prompt is expected to be run multiple times, once per selected input file or source unit. Each execution should analyze one input and generate all necessary Markdown updates for the stereotype pages affected by that input.

For example:

- execution 1 processes input source X;
- if source X contains relevant information about stereotypes A and B, only pages A and B are updated;
- execution 2 processes input source Y;
- if source Y contains relevant information about stereotypes B and C, only pages B and C are updated.

The order of page population is therefore determined by the content of the selected input files, not by the current navigation order or by a predefined stereotype sequence.

## Input model

Phase 1 uses manually selected source material.

Sources should be selected because they are expected to define, explain, or substantially inform the content of OntoUML stereotypes. Examples of suitable inputs include:

- Giancarlo Guizzardi's PhD thesis;
- main OntoUML papers;
- UFO and OntoUML papers by Guizzardi and collaborators;
- existing OntoUML documentation;
- other selected authoritative or high-yield resources.

The selected inputs are expected to be processed as many times as necessary across separate prompt executions.

Every source used to generate page content must be reported in the affected page's references section.

## Output model

Each Phase 1 execution should produce complete Markdown replacement content for each affected stereotype page.

The output should be limited to pages for which the input source provides relevant information. Pages with no relevant information in the processed input should not be modified by that execution.

The output should be technical, concise, and documentation-like. It should support future review by humans or later refinement workflows.

## Quality target

Phase 1 content should be:

- structured and readable;
- technically oriented;
- concise where possible;
- grounded in selected source material;
- explicitly provisional;
- suitable for later systematic review.

Phase 1 prioritizes:

- population of relevant stereotype pages;
- clear structure;
- preparation for later refinement.

Phase 1 does not prioritize stylistic polish, examples, diagrams, or final conceptual completeness.

## Citation and reference requirements

Phase 1 uses a strict citation expectation.

Every important claim should be grounded in a reported source. The goal is not only to generate content, but also to preserve enough source traceability for later review.

Direct quotations may be used when they support key definitions or especially important claims. They should not be overused.

Each affected page should distinguish between:

### Direct Citations

Exact quoted passages used to support specific claims in the page.

### Consulted Sources

Sources used to generate or review the page content, even when no direct quotation is used.

If a source informs page content, it should be listed as a consulted source.

## Handling uncertainty and conflicts

Phase 1 should avoid uncertain claims rather than include them.

If a claim cannot be supported from the selected input or from another reported source, it should not be added in Phase 1.

When sources conflict, the most authoritative source should be preferred. Conflict resolution should be conservative and should not rely on unsupported speculation.

## Stereotype page structure in Phase 1

Phase 1 should preserve the current stereotype page structure while marking deferred sections explicitly.

The expected structure is:

```markdown
# <Stereotype Name>

## Description

<Phase 1 generated content.>

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

<Only direct quotations used to support key definitions, if any.>

### Consulted Sources

<Sources used for the Phase 1 content.>

## Generation and Review Log

| Date | Agent | Action | Prompt | Inputs |
|---|---|---|---|---|
| YYYY-MM-DD | <agent name/version> | Phase 1 population | <prompt title/version> | <input source(s)> |
```

The `Description` section is the main content target for Phase 1. It should contain a beginner-accessible but technically precise explanation of the stereotype based on the processed input source.

The `Stereotype Profile` section should remain `TBD in a later phase.` unless a later decision revises the Phase 1 structure.

The `Examples` section should remain `TBD in a later phase.` Examples are intentionally deferred and should not be generated in Phase 1.

## Generation and review log

Each affected page should include a Phase 1 generation log entry.

The log entry should record:

- date;
- agent name and version;
- action performed;
- prompt title and version;
- input source or sources.

The log should make clear that the page was populated during Phase 1 and remains provisional.

## Completion criteria

Phase 1 is complete when all selected major input sources have been processed and all affected stereotype pages have been updated accordingly.

Some stereotype pages may still be blank or mostly skeletal after Phase 1. A page is not required to be populated if the selected Phase 1 inputs do not provide relevant content for it.

Additional success criteria are:

- each affected page lists consulted sources;
- each affected page has a generation log entry;
- affected pages are clearly marked as provisional;
- the MkDocs site still builds successfully.

## Deferred work

The following work is deferred to later phases:

- examples;
- diagrams;
- complete stereotype profiles;
- terminology normalization;
- systematic cross-page consistency checks;
- expert-level validation;
- agent-assisted refinement;
- conflict analysis beyond preferring the most authoritative source;
- visual or structural website improvements.

## Risks

Phase 1 carries known risks:

- hallucinated claims;
- misread source material;
- oversimplification;
- citation gaps;
- inconsistent terminology;
- uneven page quality;
- overconfidence in generated content;
- excessive dependence on difficult sources;
- loss of nuance from UFO or OntoUML theory.

These risks are acceptable only because Phase 1 is explicitly provisional and designed to support later review.

## Expected readers

Phase 1 content primarily serves:

- future review agents;
- the project maintainer.

The content should therefore be useful for later refinement work, not merely readable as final educational material.

## Relationship to later phases

Later phases are not specified in detail here.

Phase 1 only establishes the initial content base. Future phase documentation should define its own purpose, execution model, and quality expectations.
