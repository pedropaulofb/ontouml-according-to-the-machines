## Check signal report: page-hygiene-checker / gemini / gemini-2.5-flash — 2026-08-27

### Run metadata

| Field | Value |
|---|---|
| Agent | page-hygiene-checker |
| Provider | gemini |
| Model | gemini-2.5-flash |
| Prompt | page-hygiene-checker-v1.1.1 |
| Review date | 2026-08-27 |
| Reviewed page | docs/stereotypes/relations/component-of.md |
| Commit SHA | 219764795c45536f78f0bb49b5e8df96ae85a515 |
| Signal count | 1 |

### Summary judgment

Minor page-hygiene signals were identified; they mainly affect readability or reviewability.

### Scope

Page-hygiene check only. This run reviewed visible reference hygiene, Markdown hygiene, encoding hygiene, and Generation and Review Log hygiene in the provided page only.

### Signals

#### S-001 — Inconsistent formatting of source locators

- Category: `reference_hygiene`
- Severity: `low`
- Confidence: `high`
- Location: Section: "Direct Citations"; Fragment: "Locator: Chapter 5, p. 187, section 5.6."
- Observation: The formatting of locators for "Chapter" and "section" is inconsistent across direct citations.
- Rationale: Some locators use "Chapter X, p. Y, section Z" while others use "Chapter X, section Y, p. Z".
- Recommendation: Standardize the order of "Chapter", "section", and "p." in locators for consistency.
