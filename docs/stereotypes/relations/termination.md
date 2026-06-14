# Termination

## Description

Termination is used to represent the event-related endpoint of an endurant's active life. The sources treat this endpoint as distinct from an unrestricted deletion mechanism: under historical semantics, termination is modeled as a change of phase rather than removal from the universe of discourse, because events and their dependent endurants accumulate.

One source characterizes `<<termination>>` as an association from an Event type to a Phase. The target Phase is instantiated by the terminated endurant when it assumes a historical nature; in that state, the endurant has immutable properties comparable to those of past events. A complementary source frames termination as the counterpart of Creation in the life cycle of an endurant, where an endurant may go out of existence by becoming causally inactive and entering inactive or final phases after its relevant manifestations have accumulated.

The supplied sources also relate termination to explicit event-dependence constraints. In one formalization, `terminatedBy` is a relation from `Object` to `Event`, glossed as "destructed by". An object terminated by an event must be present in the situation that triggers the event, absent from the situation brought about by the event, and connected to the event through dependence, either because the event itself or one of its atomic parts depends on the object. The same source notes that the SROIQ mapping captures only part of this condition and leaves `terminatedBy`, together with `createdBy` and `changedBy`, without cardinality constraints to avoid forcing infinite models and to allow eternal objects in infinite models.

Taken together, the sources support Termination as a constrained event-related transition into historical or inactive status, with consequences for presence, causal activity, manifestation, and immutability.

## Stereotype Profile

To be determined.

## Examples

To be determined.

## References

### Direct Citations

- "The termination of an endurant in the profile is represented with the introduction of the <<termination>> stereotype" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 6, Section 3.2.
- "termination of an endurant should be considered a change in phase rather than "removal"" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 6, Section 3.2.
- "which relates an event type to a class stereotyped <<phase>>" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 6, Section 3.2.
- "go out of existence" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 24, Sect. 2.2.
- "created in and terminated in" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 34, Sect. 3.5.
- "terminatedBy (meaning "destructed by")" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.
- "an Object terminatedBy an Event must be presentIn" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 13, Section 3.9.
- "cannot be presentIn a Situation brought about" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 13, Section 3.9.

### Consulted Sources

- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-06 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-06t0153; not final expert-validated documentation. |
