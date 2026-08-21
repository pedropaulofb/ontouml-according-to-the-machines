## Check signal report: language-style-checker / gemini / gemini-3-flash-preview — 2026-08-21

### Run metadata

| Field | Value |
|---|---|
| Agent | language-style-checker |
| Provider | gemini |
| Model | gemini-3-flash-preview |
| Prompt | language-style-checker-v1.1.0 |
| Review date | 2026-08-21 |
| Reviewed page | docs/stereotypes/classes/collective.md |
| Commit SHA | b789100a861dc1bc4d769782b9bfcb5767d1cc8a |
| Signal count | 1 |

### Summary judgment

Minor language-style signals were identified; they mainly affect readability or professional style.

### Scope

Language-style check only. This run reviewed grammar, spelling, clarity, professional technical style, and project self-reference in the provided page only.

### Signals

#### S-001 — Referencing supplied sources

- Category: `project_self_reference`
- Severity: `low`
- Confidence: `high`
- Location: Section: "Description"; Fragment: "The supplied sources distinguish extensional and non-extensional treatments of Collective."
- Observation: The phrase "supplied sources" refers to the project's input data rather than the subject matter itself.
- Rationale: Professional technical documentation should ideally stand alone without referring to the process of its own creation or the sources provided to the generator.
- Recommendation: Use a neutral technical phrasing that avoids referencing the project's source delivery.
- current_text: "The supplied sources distinguish"
- proposed_text: "There are"
