# Kind

## Description

Kind is a rigid sortal type used to represent the ultimate identity-supplying classification of its instances. Across the Phase 1 sources, Kind is repeatedly characterized as providing a uniform principle of identity, individuation, and persistence: an instance of a Kind is classified by that Kind necessarily, and the Kind determines the basis on which the instance can be identified as the same individual through qualitative change and across situations.

In sources focused on object universals and OntoUML profile constructs, Kind is treated as the substance-sortal or ultimate-sortal stereotype for regular objects or substantials. In that role, it anchors a sortal hierarchy: non-Kind sortals such as Subkind, Phase, and Role carry an identity principle inherited from an appropriate Kind rather than supplying one themselves. Several sources also state the corresponding uniqueness commitment: an object, endurant, or substantial must be ultimately covered by exactly one relevant identity-supplying sortal, and it must not receive incompatible ultimate identity principles.

The consolidated sources support several specialization constraints for Kind. A Kind should not specialize an anti-rigid universal such as Phase, Role, or RoleMixin. Some sources additionally state that Kind cannot specialize another sortal universal or another Kind, because that would make it both inherit and supply a principle of identity. The OntoUML 2-oriented sources express this as a constraint that Kind anchors the relevant sortal hierarchy as a unique ultimate sortal.

The scope of Kind varies across the supplied sources. Earlier or broader UFO discussions use kind-based identity for endurants beyond independent objects, including Relators, insofar as they require an identity principle through time. Later OntoUML 2 sources narrow the stereotype Kind to ultimate sortals whose instances are regular objects, while Relator, Mode, and Quality receive their own ultimate-sortal stereotypes. This page therefore treats Kind primarily as the identity-supplying ultimate sortal for regular objects in the OntoUML profile, while preserving the broader source-grounded observation that kind-based identity principles apply to endurants in the underlying theory.

Kind is also used in the sources to distinguish sortal from non-sortal classification. A non-sortal classifier that groups instances of different Kinds cannot itself supply a single identity principle; its instances must remain covered by suitable sortal specializations that inherit identity from the relevant Kind. In the event-extension source, Kind is treated as an endurant-type stereotype and is therefore disjoint from Event classification. A class should not simultaneously specialize an Event type and an endurant type such as Kind.

A multi-level modeling source adds a second-order constraint: a domain second-order type specializing Kind must have a rigid mixin base type, identified there as an instance of Category. That contribution is source-specific and should be treated as Phase 1 consolidation material rather than a complete profile rule.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "represents a substance sortal that supplies a principle of identity for its instances" — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 4, Section 4.2.1, p. 108.
- "Every object in a conceptual specification using this profile must be an instance of a Kind" — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 4, Section 4.2.1, p. 108.
- "it cannot be an instance of more than one ultimate Kind" — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 4, Section 4.2.1, p. 108.
- "ultimate substance sortals (kinds) that supply the principles of identity" — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 7, section 7.1, p. 282.
- "Customer is hence a dispersive or transsortal type (a non-sortal)" — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 7, section 7.1, p. 281.
- "If the universal A is rigid then A(x) is necessarily true" — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 7, section 7.2, p. 286.
- "provides uniform principles of individuation, identity, and persistence to its instances" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 6, Section 1.
- "every endurant necessarily instantiates a kind" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 9, Section 2.2.
- "Kinds are types that classify their entities necessarily" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 3, Section 2.
- "provide a uniform principle of identity for their instances" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 3, Section 2.
- "These classes are disjoint from any classes that model endurant types" — Source: Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing; Locator: p. 5, Section 3.1.
- "a principle of identity, individuation and persistence" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 21, Sect. 2.1.
- "a principle of identity must be supplied by a type" — Source: Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing.; Locator: p. 22, Sect. 2.1.
- "decorates classes that represent ultimate sortals whose instances are regular objects." — Source: Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021). Types and taxonomic structures in conceptual modeling: a novel ontological theory and engineering support. Data & Knowledge Engineering, 134, 101891.; Locator: p. 8, Section 4.1.
- "every endurant must instantiate a unique ultimate sortal." — Source: Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021). Types and taxonomic structures in conceptual modeling: a novel ontological theory and engineering support. Data & Knowledge Engineering, 134, 101891.; Locator: p. 9, Section 4.1.
- "A Rigid Sortal that supplies a principle of identity to its instances is termed Kind" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 3, Section 2.1.
- "an instance of Kind cannot specialize another sortal universal" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 4, Section 2.2.
- "a second-order type specializing "Kind" must have a rigid mixin sortal as base type" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 8, Section 5.1.1.

### Consulted Sources

- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente. Scope: Chapter 4.
- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente. Scope: Chapter 6.
- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente. Scope: Chapter 7.
- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente. Scope: Chapter 8.
- Guizzardi, G., Fonseca, C. M., Benevides, A. B., Almeida, J. P. A., Porello, D., & Sales, T. P. (2018, September). Endurant types in ontology-driven conceptual modeling: Towards OntoUML 2.0. In International conference on conceptual modeling (pp. 136-150). Cham: Springer International Publishing. Scope: full document.
- Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210. Scope: full document.
- Guarino, N., & Guizzardi, G. (2015, May). “We need to discuss the relationship”: Revisiting relationships as modeling constructs. In International Conference on Advanced Information Systems Engineering (pp. 279-294). Cham: Springer International Publishing. Scope: full document.
- Almeida, J. P. A., Falbo, R. A., & Guizzardi, G. (2019, October). Events as entities in ontology-driven conceptual modeling. In International Conference on Conceptual Modeling (pp. 469-483). Cham: Springer International Publishing. Scope: full document.
- Guizzardi, G., Guarino, N., & Almeida, J. P. A. (2016, September). Ontological considerations about the representation of events and endurants in business models. In International Conference on Business Process Management (pp. 20-36). Cham: Springer International Publishing. Scope: full document.
- Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021). Types and taxonomic structures in conceptual modeling: a novel ontological theory and engineering support. Data & Knowledge Engineering, 134, 101891. Scope: full document.
- Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document.
- Guizzardi, G., Almeida, J. P., Guarino, N., & Carvalho, V. A. (2015). Towards an ontological analysis of powertypes. In Proceedings of the Joint Ontology Workshops 2015 Episode 1: The Argentine Winter of Ontology co-located with the 24th International Joint Conference on Artificial Intelligence (IJCAI 2015); Buenos Aires, Argentina, July 25-27, 2015 (Vol. 1517). RWTH. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t0921-guizzardi-2005-thesis-chapter-04.md, 2026-06-05t0928-guizzardi-2005-thesis-chapter-06.md, 2026-06-05t0929-guizzardi-2005-thesis-chapter-07.md, 2026-06-05t0930-guizzardi-2005-thesis-chapter-08.md, 2026-06-05t1024-guizzardi-2018-endurant-types-full-document.md, 2026-06-05t1024-guizzardi-2022-ufo-full-document.md, 2026-06-05t1025-guarino-guizzardi-2015-relationships-full-document.md, 2026-06-05t1031-almeida-falbo-guizzardi-2019-events-as-entities-full-document.md, 2026-06-05t1037-guizzardi-2016-events-endurants-full-document.md, 2026-06-05t1037-guizzardi-2021-types-taxonomic-structures-full-document.md, 2026-06-05t1040-carvalho-2017-multi-level-ontology-based-conceptual-modeling-full-document.md, 2026-06-05t1040-guizzardi-2015-powertypes-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-05t1717; not final expert-validated documentation. |
