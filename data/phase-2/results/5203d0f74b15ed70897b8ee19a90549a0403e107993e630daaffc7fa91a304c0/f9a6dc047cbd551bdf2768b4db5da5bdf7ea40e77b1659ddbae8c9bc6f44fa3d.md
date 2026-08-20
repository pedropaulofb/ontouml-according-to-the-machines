## Check signal report: language-style-checker / gemini / gemini-3-flash-preview — 2026-08-20

### Run metadata

| Field | Value |
|---|---|
| Agent | language-style-checker |
| Provider | gemini |
| Model | gemini-3-flash-preview |
| Prompt | language-style-checker-v1.1.0 |
| Review date | 2026-08-20 |
| Reviewed page | docs/stereotypes/classes/quality.md |
| Commit SHA | 7533897fc781a0fe5f3918ea3093fea5e403ee24 |
| Signal count | 1 |

### Summary judgment

Minor language-style signals were identified; they mainly affect readability or professional style.

### Scope

Language-style check only. This run reviewed grammar, spelling, clarity, professional technical style, and project self-reference in the provided page only.

### Signals

#### S-001 — Avoid project self reference

- Category: `project_self_reference`
- Severity: `medium`
- Confidence: `high`
- Location: Section: "Description"; Fragment: "The supplied sources also distinguish simple qualities from complex qualities"
- Observation: The phrase "The supplied sources" is a project-specific reference to the input data used for generation.
- Rationale: Documentation should be standalone and avoid mentioning the process or materials used to generate the content.
- Recommendation: Use a neutral technical phrasing that focuses on the conceptual distinction.
- current_text: "The supplied sources also distinguish simple qualities from complex qualities"
- proposed_text: "Simple qualities are distinguished from complex qualities"
