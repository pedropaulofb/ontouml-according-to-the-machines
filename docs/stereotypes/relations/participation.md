# Participation

## Description

Participation is used in the sources to represent how endurants or objects are involved in events or perdurants. At the OntoUML modeling level, Participation is described as an association stereotype connecting an Event class to a class denoting an endurant type. It is the main connection between modeled events and the endurant types that participate in them.

The sources ground this connection in an underlying event account. One recurrent characterization treats a participation as the event portion that depends exclusively on a single object. In this account, `participationOf` is derived from exclusive dependence between that event portion and the object, rather than introduced as primitive. Participation can apply to atomic events that manifest dispositions and to complex events that have such atomic events as parts; participations may themselves be atomic or complex. The participation view is therefore presented as orthogonal to a purely mereological decomposition of events.

Several source-specific contributions relate Participation to manifestation. One account states that an endurant participates in a perdurant when the perdurant has a part that manifests a disposition inhering in that endurant. Another presents Participation as linking an endurant to an Event when the Event is a manifestation of the endurant's disposition or is composed of such a manifestation. A related source distinguishes participation from manifestation by treating participation as the endurant's involvement in an event and manifestation as the unfolding of particularized properties of endurants.

Participation also supports role-sensitive accounts of events. The sources indicate that the nature of an endurant's participation determines the processual role it plays in the event, and that event participation may involve different degrees or kinds of involvement. Participation is not characterized as limited to agents; one source explicitly states that the participating object may be inanimate.

Because some sources treat modeled events as past occurrences or as existentially dependent on their participants, they associate Participation with immutability constraints on the event-side facts represented in structural models. In those accounts, association ends attached to endurant types in Participation associations should be read-only, and past participations accumulate under the source's historical semantics.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "the portion of an event which depends exclusively on a single object a participation" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 5, Section 3.2.
- "participations can be atomic or complex" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 5, Section 3.2.
- "participation of and the notion of participation itself are all derived notions" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 5, Section 3.2.
- "The participation view of events is in some sense orthogonal to the mereological view" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 12, Section 6.
- "connected to their participants via an existential dependence relation" — Source: Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.; Locator: p. 13, Section 6.
- "An endurant then participates in a perdurant" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 4, Section 1.
- "if that perdurant has a part that is a manifestation of a disposition inhering in that endurant" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 4, Section 1.
- "Perdurants are always dependent on the substantials that participate in them" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 7, Section 1.1.
- "In order to model the participation of endurants in events, we use the stereotype <<participation>>" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "always relates a class stereotyped with <<event>> with a class denoting an endurant type" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "either: (i) the event is a manifestation of a disposition of the participating endurant" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.2.
- "endurant participation in events" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 24, Sect. 2.2.
- "playing certain processual roles" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 25, Sect. 2.2.
- "Objects participate not only in the AtomicEvents" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 8, Section 3.4.
- "A Participation is an Event that exclusivelyDependsOn a unique Object" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 8, Section 3.4.
- "a single (possibly inanimate) object" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 32, Section 7.2.

### Consulted Sources

- Guizzardi, G., Wagner, G., de Almeida Falbo, R., Guizzardi, R. S., & Almeida, J. P. A. (2013, November). Towards ontological foundations for the conceptual modeling of events. In International conference on conceptual modeling (pp. 327-341). Berlin, Heidelberg: Springer Berlin Heidelberg.. Scope: full document.
- Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.. Scope: full document.
- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Guarino, N., & Guizzardi, G. (2016, November). Relationships and events: towards a general theory of reification and truthmaking. In Conference of the Italian Association for Artificial Intelligence (pp. 237-249). Cham: Springer International Publishing.. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-06 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t1024-guizzardi-2013-events-full-document.md, 2026-06-05t1024-guizzardi-2022-ufo-full-document.md, 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1033-guarino-guizzardi-2016-relationships-events-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-06t0139; not final expert-validated documentation. |
