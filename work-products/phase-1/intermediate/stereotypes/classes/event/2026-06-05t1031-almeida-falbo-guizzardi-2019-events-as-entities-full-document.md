# Event

## Source-Specific Description Contribution

The source supports `<<event>>` as the OntoUML class stereotype for event types: classes whose instances are events understood as past occurrences. In this extension, event classes are disjoint from classes that model endurant types. The same class must not be stereotyped both as `<<event>>` and as an endurant-type stereotype, and a class must not specialize both an event class and an endurant-type class.

The source adopts a historical interpretation of events. Instances of `<<event>>` classes are necessarily classified by those classes rather than contingently classified. Event features are immutable and should be marked read-only, including association ends connected to endurants through `<<participation>>` or `<<creation>>` associations.

The source also supports temporal properties for event types. Event classes may carry temporal attributes stereotyped `<<begin>>` and `<<end>>`; if the begin and end coincide systematically for a class, one attribute may bear both stereotypes. The temporal value space and corresponding datatype are application-dependent. When temporal attributes apply uniformly across event classes, they may be placed in an abstract `<<event>>` superclass. The source states that Allen-style interval relations can be derived from these temporal attributes and made available as helper OCL operations.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "identifies those classes whose instances are events (past occurrences)" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.1.
- "no class may be stereotyped with both <<event>> and any of the other stereotypes" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.1.
- "any features of events are immutable (and should be marked readOnly)" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 6, Section 3.2.

### Consulted Sources

- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1031; not a final documentation page; intended for later consolidation. |
