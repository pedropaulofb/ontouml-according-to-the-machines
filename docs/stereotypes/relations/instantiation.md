# Instantiation

## Description

Instantiation is a classification relation connecting an instance-bearing entity to a type or universal it falls under. In the supplied sources, this relation is commonly used between individuals and universals or types, and in multi-level settings it is also used between lower-order and higher-order types. The relation is symbolized as `::` in some formalizations.

Instantiation is constrained differently from related relations. One source presents its first argument as an individual and its second argument as a universal, distinguishing it from set membership and inherence. The extension of a universal is the set of its instances, but the universal itself is not identified with that extension and must be treated intensionally. The same source also distinguishes Instantiation from exemplification: Instantiation relates an individual directly to a universal, while exemplification of a moment universal is mediated by a particular moment inhering in an individual.

Several sources use Instantiation to support modal and dynamic classification. One account distinguishes necessary Instantiation, where an individual instantiates a Kind in every possible situation in which it exists, from contingent Instantiation, where an individual may enter or leave a type's extension without losing its identity. This distinction is used to characterize Kind as necessarily instantiated and Phase, Role, and RoleMixin as contingent classifications of endurants. Another source indexes instantiation by possible worlds, allowing an entity to instantiate a type in one world and not in another.

In multi-level modeling, Instantiation is used to distinguish classification orders. First-order types are instantiated by individuals, while second-order types are instantiated by first-order types; higher-order types may therefore have types as their instances. In the OntoUML extension discussed by one source, every first-order domain type must instantiate a leaf category in UFO's taxonomy of universals, while domain second-order types specialize those leaf categories and have first-order types as instances.

One powertype-oriented source keeps Instantiation central but coordinates it with `isClassifiedBy`. In that account, each subtype of a base type is associated with a unique powertype instance, and an ordinary individual instantiates the subtype exactly when it is classified by that associated powertype instance. The same source rejects a higher-order-universal interpretation of powertype instances because it does not provide the required modal behavior for those instances.

A SROIQ-oriented event formalization reifies universals and individuals and uses an atemporal `instantiates` relation between them. In that formalization, individuals instantiate at least one universal, and specific universal categories constrain their possible instances: `QualityUniversal` is instantiated by qualities, `ObjectUniversal` by objects, `EventUniversal` by events, and `ParticipationUniversal` by participations. The same source states that events instantiate event universals rigidly across their occurrence or existence.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "being connected by the instantiation relation" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 7, Section 2.
- "symbolized as “::”" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 7, Section 2.
- "types whose instances are themselves types" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 32, Section 3.5.
- "instantiates that kind necessarily" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 22, Sect. 2.1.
- "contingent types" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 22, Sect. 2.1.
- "MLT defines a primitive instance of relation" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 5, Section 3.
- "The concepts in UFO's taxonomy of individuals are instances of "1stOT" specializing "Individual"" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 7, Section 4.
- "every domain first-order type must: (i) instantiate one of the leaf ontological categories of UFO's taxonomy of universals" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 7, Section 4.
- "an atemporal instantiation relation" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 5, Section 3.1.
- "Individuals instantiate at least one Universal." — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 5, Section 3.1.
- "Events instantiate EventUniversals rigidly" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 5, Section 3.1.

### Consulted Sources

- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente. Scope: Chapter 6.
- Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing. Scope: full document.
- Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document.
- Guizzardi, G., Almeida, J. P., Guarino, N., & Carvalho, V. A. (2015). Towards an ontological analysis of powertypes. In Proceedings of the Joint Ontology Workshops 2015 Episode 1: The Argentine Winter of Ontology co-located with the 24th International Joint Conference on Artificial Intelligence (IJCAI 2015); Buenos Aires, Argentina, July 25-27, 2015 (Vol. 1517). RWTH. Scope: full document.
- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-06 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t0928-guizzardi-2005-thesis-chapter-06.md, 2026-06-05t1024-guizzardi-2022-ufo-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1040-carvalho-2017-multi-level-ontology-based-conceptual-modeling-full-document.md, 2026-06-05t1040-guizzardi-2015-powertypes-full-document.md, 2026-06-05t1042-botti-benevides-2019-events-sroiq-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-06t0056; not final expert-validated documentation. |
