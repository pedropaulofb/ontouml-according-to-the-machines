# Creation

## Description

Creation connects an Event with the endurant or Object it brings into existence. The intermediate sources characterize Creation as an event-to-endurant relation, and one source describes `<<creation>>` as a special kind of Participation. In the evidence, Creation belongs to the broader event-extension account in which Event occurrences record changes affecting endurants, including Creation, Termination, property change, and Participation.

For past modeled Event occurrences, a Creation relation fixes which endurant was created by the Event. The source-specific contribution that discusses `<<creation>>` therefore applies an immutability rule to association ends attached to endurants in Creation associations: they should be read-only because the past Event cannot change which endurant it created.

A complementary source treats creation events as Events with temporal boundaries and states that the creation time of an endurant is derived from the termination time point of the creation event. Another source formalizes the related `createdBy` relation between Objects and Events: a created Object is not present in the triggering situation, is present in the situation brought about by the Event, and is connected to the Event through a dependence relation involving the Event or one of its atomic parts. That same source imposes no cardinality constraints on `createdBy`; its SROIQ mapping only partially captures the first-order constraint, preserving the implication from `createdBy` composed with `bringsAbout` to `presentIn`.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "A special kind of participation is the creation of an endurant" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "If an endurant is related to an event through an association stereotyped <<creation>>" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "including the association ends attached to endurants in participation and creation associations" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 6, Section 3.2.
- "brought into existence" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 24, Sect. 2.2.
- "Endurants are created by creation events" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 31, Sect. 3.4.
- "we introduce three relations from Objects to Events" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.
- "an Object createdBy an Event cannot be presentIn" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.
- "we impose no cardinality constraints" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.

### Consulted Sources

- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-06 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-06t0020; not final expert-validated documentation. |
