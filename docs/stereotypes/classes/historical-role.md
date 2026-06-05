# HistoricalRole

## Description

HistoricalRole is the class stereotype for a role an endurant instantiates because it participated in one or more past events of a relevant type. In the Phase 1 sources, this attribution is grounded in historical semantics: once the relevant event participation is part of fixed history, the role attribution is grounded in that past participation rather than in a current relational context.

A HistoricalRole must be related to an Event type through a Participation association. The source-specific contribution states that, for this association, the minimum cardinality at the association end attached to the Event type must be one. This expresses that each instance of the HistoricalRole must have participated in at least one event of the relevant type.

The consolidated evidence distinguishes HistoricalRole from Role in current relational contexts. Current relationship-based role playing is represented through Role, Relator, and Mediation, whereas historical role playing is represented through HistoricalRole, Event, and Participation. This distinction is tied to the immutability and accumulation of past events in the cited historical semantics.

One input source uses ProcessualRole rather than the later target label HistoricalRole. In that source, ProcessualRole classifies endurants synchronically according to how they participate in events, with the synchronic classification inferred from a diachronic, historical classification. The same source states that the `plays` relation is an instantiation relation from objects to processual roles, and that processual roles are induced by participation universals that classify events. Because the source does not itself use the HistoricalRole label, these ProcessualRole-based claims should be treated as provisional for this page pending later expert validation.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "The role an endurant instantiates in virtue of having participated in an event" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 7, Section 3.2.
- "A historical role is required to be related to an event type through a <<participation>> association" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 7, Section 3.2.
- "distinguish explicitly between role playing in the scope of a (current) relationship and role playing in (past) events" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 7, Section 3.2.
- "ProcessualRoles synchronically classify Endurants" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 10, Section 3.7.
- "a synchronic classification is inferred from a diachronic (historical) classification" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 10, Section 3.7.
- "the relation plays is an instantiation relation from Objects to ProcessualRoles" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 10, Section 3.7.

### Consulted Sources

- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-05t1711; not final expert-validated documentation. |
