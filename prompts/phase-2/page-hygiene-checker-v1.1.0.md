# Page-hygiene checker contract

Prompt ID: `page-hygiene-checker-v1.1.0`

Inspect one supplied canonical stereotype page for visible page-hygiene problems only.

## Scope

In scope:

1. visible reference hygiene;
2. Markdown hygiene;
3. encoding hygiene;
4. visible Generation and Review Log hygiene.

Out of scope: content correctness; OntoUML/UFO semantics; source faithfulness; quotation verification; claim support or overstatement; grammar/style except when the problem is a visible Markdown or encoding artifact; required or missing top-level/reference/log sections; and cross-page consistency. Required top-level structure belongs to `page-structure-checker`.

Inspect `## Description` only for visible Markdown or encoding artifacts. Do not assess its claims, grammar, style, concepts, or evidence. If an observation may instead be semantic, source-validation, structural, or stylistic, omit it.

## Categories and priority

Use one category:

- `reference_hygiene`: visible issues in `### Direct Citations` or `### Consulted Sources`, including visibly repeated/near-repeated source entries; inconsistent labels for such entries; malformed source-entry structure; visibly malformed, dangling, repeated, garbled, or materially inconsistent locators; or a visible quotation/passage reference lacking enough locator information for reviewability.
- `markdown_hygiene`: broken tables, malformed lists/headings/layout, unclosed fences, inconsistent blockquotes, duplicated markers, or similar visible Markdown defects.
- `encoding_hygiene`: mojibake, replacement characters, corrupted punctuation/quotation marks/dashes, or other visible character artifacts.
- `review_log_hygiene`: malformed, duplicated-looking, unclear, or internally inconsistent visible log entries, dates, providers, models, prompts, notes, or provenance.

When categories overlap, prefer: `encoding_hygiene`, `markdown_hygiene`, `reference_hygiene`, `review_log_hygiene`.

Prioritize: traceability/reviewability impact; possible later-automation impact; repeated/systematic problems; confidence; then safe local repair potential.

Do not verify quotations, infer bibliography, add sources/locators, decide claim support, require inline citations, require locators for every consulted source, or report harmless citation-style variation. Judge log consistency only from the supplied visible log; do not impose external conventions.

## Protected content and replacements

For protected content, omit exact-replacement fields unless a repair is purely mechanical, visibly unambiguous, local, and meaning-preserving. Allowed repairs include obvious encoding-character correction, local Markdown repair without a full table row, local normalization to an existing visible log pattern, or removal of a duplicated Markdown marker. Never invent a locator, add a source, validate support, change a quotation/claim, or rewrite prose.

## Severity and confidence

- Severity `low`: limited consistency/readability/reviewability effect.
- Severity `medium`: may affect traceability, readability, or reviewability.
- Severity `high`: materially interferes with traceability, provenance, or review.
- Confidence `low`: possible but uncertain from the page.
- Confidence `medium`: plausible from visible content.
- Confidence `high`: clearly visible.

## Required report values

Summary judgment must be exactly one of:

- `No page-hygiene signals were identified within the configured scope.`
- `Minor page-hygiene signals were identified; they mainly affect readability or reviewability.`
- `Page-hygiene signals were identified that may affect traceability, provenance, or reviewability.`
- `Page-hygiene signals were identified, and only the highest-impact three are reported.`

Use the fourth only when more than three candidates existed and only three are reported.
Emit the selected summary as one plain sentence without a bullet marker.

The exact `### Scope` sentence is:

`Page-hygiene check only. This run reviewed visible reference hygiene, Markdown hygiene, encoding hygiene, and Generation and Review Log hygiene in the provided page only.`
