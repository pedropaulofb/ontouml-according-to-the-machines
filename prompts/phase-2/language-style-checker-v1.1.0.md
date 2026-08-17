# Language-style checker contract

Prompt ID: `language-style-checker-v1.1.0`

Inspect one supplied canonical stereotype page for low-risk language and professional-style problems only.

## Scope

In scope: grammar, spelling, clarity, professional technical style, and project/process self-reference in reader-facing documentation.

Out of scope: source/citation validation; OntoUML/UFO semantics; conceptual adequacy; source faithfulness; quotations; claim support/overstatement; required/missing sections; reference, Markdown, encoding, or review-log hygiene; cross-page consistency; and any change to OntoUML meaning.

Reader-facing prose includes headings, paragraphs, list items, table cells, captions, and image alt text, except text in front matter, code, HTML comments, generation/review logs, source metadata, bibliography/references, citation/source tables, changelogs, or explicitly marked process/history sections. If an observation may instead be semantic, evidential, conceptual, structural, or hygienic, omit it.

Flag reader-facing references such as `According to Phase 1`, `In this project`, `This generated page`, `The generated documentation`, `The Phase 1 analysis`, or `According to the Machines`. Recommend neutral standalone OntoUML wording only when doing so preserves the claim, modality, caution, citation, and external-source attribution.

## Categories and priority

Use one category:

- `grammar`: agreement, tense, article, sentence construction, or other grammar.
- `spelling`: typo, misspelling, or obvious orthographic error.
- `clarity`: awkward, ambiguous, unnecessarily complex, or hard-to-parse wording.
- `professional_style`: informal, conversational, promotional, or otherwise unsuitable technical prose.
- `project_self_reference`: reader-facing reference to the project, phases, generation/review process, or machine origin.

When categories overlap, prefer: `project_self_reference`, `spelling`, `grammar`, `clarity`, `professional_style`. Use the same order for signal priority.

## Protected content and replacements

For any problem inside protected content, omit exact-replacement fields. Do not change stereotype names, definitions, technical claims/terms, modality, caution, citations, quotations, links, or source interpretation. Do not add precision or strengthen/weaken a claim.

## Severity and confidence

- Severity `low`: minor language/style issue.
- Severity `medium`: noticeably affects readability, professionalism, or standalone quality.
- Severity `high`: substantially confuses readers or makes the page read like project/process documentation.
- Confidence `low`: uncertain and likely requires human judgment.
- Confidence `medium`: plausible from the supplied page.
- Confidence `high`: clearly visible.

## Required report values

Summary judgment must be exactly one of:

- `No language-style signals were identified within the configured scope.`
- `Minor language-style signals were identified; they mainly affect readability or professional style.`
- `Language-style signals were identified that may affect standalone professional documentation quality.`
- `Language-style signals were identified, and only the highest-impact three are reported.`

Use the fourth only when more than three candidates existed and only three are reported.
Emit the selected summary as one plain sentence without a bullet marker.

The exact `### Scope` sentence is:

`Language-style check only. This run reviewed grammar, spelling, clarity, professional technical style, and project self-reference in the provided page only.`
