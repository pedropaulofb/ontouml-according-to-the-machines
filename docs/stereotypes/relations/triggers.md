# Triggers

## Description

Triggers represents a relation from a Situation to an Event. The Phase 1 sources characterize the relation as holding when an event occurs because a situation obtains; in the formalized accounts, the triggering situation obtains at the event's begin point and each event occurrence has a unique triggering situation.

The supplied sources also connect Triggers to dispositions. For atomic events, a situation triggers an atomic event when the situation activates a disposition manifested by that event. In this role, Triggers relates the obtaining of a situation to the manifestation of a disposition through an event occurrence, and is associated with the source relations `activates` and `manifestedBy`.

Triggers is also used in accounts of event causation. If one event brings about a situation that triggers another event, the brought-about situation mediates a direct causal relation between the two events. One source further uses this pattern in its account of historical dependence, where historical dependence may hold when one event brings about a situation that triggers another event or brings about a situation necessary for such triggering.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "a situation s triggers an e event" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 7, Section 3.4.
- "e occurs because of the obtaining of s" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 7, Section 3.4.
- "A situation that triggers an event obtains at the begin point of that event" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 7, Section 3.4.
- "there is a unique situation that triggers a particular event occurrence" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 7, Section 3.4.
- "this situation activates the disposition that is manifested by that event" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: pp. 8-9, Section 3.5.
- "Dispositions are said to be triggered by certain situations" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 4, Section 2.
- "S triggers E0 and that E causes E0" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 4, Section 2.
- "brings about the situation that triggers b" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 10, Section 3.4.
- "trigger the occurrence of other events" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 24, Sect. 2.2.
- "All Events are triggered by a unique Situation" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 10, Section 3.6.
- "the Situation obtainsIn the same TimePoint" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 10, Section 3.6.
- "triggers an AtomicEvent iff" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 7, Section 3.3.

### Consulted Sources

- Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.. Scope: full document.
- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-06 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t1024-guizzardi-2013-events-full-document.md, 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-06t0157; not final expert-validated documentation. |
