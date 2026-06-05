# Historical Role

## Source-Specific Description Contribution

The source supports `<<historicalRole>>` as the class stereotype for a role that an endurant instantiates in virtue of past participation in an event of a particular type. A historical role is tied to the historical semantics introduced by past events: once the relevant event participation is part of the fixed history, the role attribution is grounded in that past participation.

A `<<historicalRole>>` class must be related to an event type through a `<<participation>>` association. For such an association, the minimum cardinality at the association end attached to the event type must be one, expressing that an instance of the historical role must have participated in at least one event of the relevant type.

The source uses `<<historicalRole>>` to distinguish role playing in past events from role playing in current relationships. A current relationship role is represented through `<<role>>`, `<<relator>>`, and `<<mediation>>`; a historical role is represented through `<<historicalRole>>`, `<<event>>`, and `<<participation>>`. The distinction is grounded in the immutability and accumulation of past events under the source's historical semantics.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "The role an endurant instantiates in virtue of having participated in an event" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 7, Section 3.2.
- "A historical role is required to be related to an event type through a <<participation>> association" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 7, Section 3.2.
- "distinguish explicitly between role playing in the scope of a (current) relationship and role playing in (past) events" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 7, Section 3.2.

### Consulted Sources

- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1031; not a final documentation page; intended for later consolidation. |
