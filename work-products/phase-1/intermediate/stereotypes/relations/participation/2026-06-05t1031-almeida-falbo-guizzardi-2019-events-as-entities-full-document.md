# Participation

## Source-Specific Description Contribution

The source introduces `<<participation>>` as the association stereotype for modeling the participation of endurants in events. A `<<participation>>` association always relates a class stereotyped `<<event>>` to a class denoting an endurant type.

The semantics given by the source is that, when an endurant and an event are linked through `<<participation>>`, either the event is a manifestation of a disposition of that endurant or the event is composed of such a manifestation. This makes participation the main bridge between the proposed event extension and the endurant types already available in OntoUML.

Because the source treats modeled events as past occurrences, the event-side facts represented by participation are immutable. Association ends attached to endurants in participation associations should be marked read-only, and past participations accumulate over time under the source's historical semantics.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "In order to model the participation of endurants in events, we use the stereotype <<participation>>" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "always relates a class stereotyped with <<event>> with a class denoting an endurant type" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "either: (i) the event is a manifestation of a disposition of the participating endurant" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.

### Consulted Sources

- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1031; not a final documentation page; intended for later consolidation. |
