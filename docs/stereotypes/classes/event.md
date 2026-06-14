# Event

## Description

Event is consolidated here as the class stereotype for event types: classes whose instances are events, with one source-specific modeling extension explicitly characterizing those instances as past occurrences. Across the valid inputs, events are primarily characterized as perduring individuals: they unfold in time through temporal parts and are contrasted with endurants, which are treated as wholly present whenever they are present. One source-specific contribution narrows the generic perdurant or occurrent sense by analyzing events as scene-based entities individuated by a spatiotemporal region and a focus.

The valid inputs treat events as first-class ontological entities distinct from endurants, and one formalization also distinguishes them from situations. In the OntoUML modeling extension for events as entities, Event classes are disjoint from endurant-type classes: the same class must not be stereotyped both as Event and as an endurant-type stereotype, and a class must not specialize both an event class and an endurant-type class. Instances of Event classes are necessarily classified by those classes rather than contingently classified.

Several inputs distinguish atomic and complex events. Atomic events have no event parts, while complex events are composed of other events or aggregate at least two disjoint events. The event parthood relation is presented as a strict partial order, with weak and strong supplementation supporting an extensional event mereology in which complex events are individuated by their parts.

Events are also characterized through dependence and manifestation. Atomic events are presented as manifestations of dispositions or particularized properties, and complex events may involve the manifestation of several dispositions. More generally, events are treated as ontologically dependent on objects or endurants through the properties, qualities, or dispositions whose manifestations they are. For relational events, one source-specific contribution characterizes them as manifestations of qualities constituting the focal relationship.

Temporally, events are delimited by begin and end points, and their temporal extent includes the temporal extent of their proper parts. Event classes may carry temporal attributes stereotyped `<<begin>>` and `<<end>>`; when begin and end coincide systematically, one attribute may bear both stereotypes. The inputs also connect these temporal boundaries to Allen-style temporal relations.

Dynamically, events are treated as transformations between situations. A triggering situation obtains at an event's beginning, and a situation brought about by the event obtains at its end; situations brought about by events may in turn trigger other events. The inputs also associate events with change involving endurants, including the creation, destruction, or alteration of endurants and their qualities, and with participants playing processual roles.

The inputs consistently caution against treating events as mutable endurants. Classical events cannot qualitatively change while preserving numerical identity; apparent event change is explained through variation among temporal parts or through change in an underlying endurant whose manifestations accumulate as events. Consequently, the modeling-oriented inputs treat event features as immutable and recommend read-only event features, including association ends connected to endurants through Participation or Creation associations. Object identifiers are presented as safest for historical events, once no further branching of the event's unfolding is possible.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "Events (also called perdurants) are individuals composed of temporal parts." — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 2, Section 2.
- "Events can be atomic or complex, depending on their mereological structure." — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 3, Section 3.1.
- "Events are ontologically dependent entities" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 4, Section 3.2.
- "Events are transformations from a portion of reality to another" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 7, Section 3.4.
- "The atomic events considered here are manifestations of single dispositions" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 12, Section 6.
- "We often refer to perdurants as events" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 4, footnote 4.
- "Perdurants are individuals that unfold in time accumulating temporal parts" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 4, Section 1.
- "events cannot bear modal properties" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 26, Section 3.3.
- "identifies those classes whose instances are events (past occurrences)" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.1.
- "no class may be stereotyped with both <<event>> and any of the other stereotypes" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.1.
- "any features of events are immutable (and should be marked readOnly)" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 6, Section 3.2.
- "events are also mappings from and to situations" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 24, Sect. 2.2.
- "events are manifestations of properties" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 24, Sect. 2.2.
- "we can only have OIDs referring to historical events" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 28, Sect. 3.3.
- "Events may be composed of other Events" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 6, Section 3.2.
- "AtomicEvents are manifestations of (the inverse of manifestedBy) unique Dispositions" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 6, Section 3.3.
- "All Events are triggered by a unique Situation" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 10, Section 3.6.

### Consulted Sources

- Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.. Scope: full document.
- Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.. Scope: full document.
- Guarino, N., & Guizzardi, G. (2015, May). “We need to discuss the relationship”: Revisiting relationships as modeling constructs. In International Conference on Advanced Information Systems Engineering (pp. 279-294). Cham: Springer International Publishing.. Scope: full document.
- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Guarino, N., & Guizzardi, G. (2016, November). Relationships and events: towards a general theory of reification and truthmaking. In Conference of the Italian Association for Artificial Intelligence (pp. 237-249). Cham: Springer International Publishing.. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t1024-guizzardi-2013-events-full-document.md, 2026-06-05t1024-guizzardi-2022-ufo-full-document.md, 2026-06-05t1025-guarino-guizzardi-2015-relationships-full-document.md, 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1033-guarino-guizzardi-2016-relationships-events-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-05t1701; not final expert-validated documentation. |
