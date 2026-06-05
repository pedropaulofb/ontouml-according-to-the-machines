# Type

## Description

Type is the OntoUML construct for representing types as entities that can be instantiated, rather than as mere extensions or sets of instances. The Phase 1 sources characterize Type through instantiation and higher-order typing: individuals can instantiate first-order types, and types can instantiate higher-order types. The available sources explicitly cover first-order and second-order types, while one multi-level treatment also describes a scheme that can extend further.

Several sources present Type in relation to universals, properties, and intensions. Chapter 6 of the 2005 thesis treats types as universals: predicative entities that can apply to multiple individuals. It also distinguishes a type from its extension, arguing that coextension, empty extensions, and membership changes are not sufficient to determine the identity or meaning of a type. The same source connects type intensions to axiomatic or elementary specifications involving features, including moment universals that may characterize the universal.

The supplied material also links Type to identity and classification constraints. One source distinguishes identity-supplying sortal universals from characterizing universals and uses that distinction to support the constraint that a concrete class in a conceptual-model ontology may represent a domain universal only when that universal carries a determinate principle of identity for its instances.

In the cited multi-level modeling treatment, Type is used to make classification levels explicit. First-order types have individuals as instances, and second-order types have first-order types as instances. In the UFO-MLT combination, domain second-order types specialize leaf categories in UFO's taxonomy of universals and are related to a first-order base type through an MLT cross-level relation, such as categorization, complete categorization, disjoint categorization, partitioning, or power type. These relations constrain the instances of the second-order type as specializations of the corresponding base type.

One powertype-focused source treats powertypes as a specific use of Type for domains whose classification scheme is itself part of the subject matter. In the UML powertype pattern discussed there, a powertype is connected to a base type through a generalization-set configuration, and its instances correspond to explicit subtypes of the base type. The source presents variable embodiments as its preferred interpretation of powertype instances, allowing them to be treated as entities with properties, modal classifications, and change without reducing their identity to membership in an extension.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "types are implicitly defined as those entities that are possibly instantiated" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 8, Section 2.1.
- "We deal here only with first-order and second-order types" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 8, Section 2.1.
- "types whose instances are also types" — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 6, Section 1.
- "Types having individuals as instances are called first-order types, types whose instances are first-order types are called second-order types" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 5, Section 3.
- "every domain second-order type has an MLT cross-level relation" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 7, Section 4.

### Consulted Sources

- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.. Scope: Chapter 6.
- Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.. Scope: full document.
- Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document.
- Guizzardi, G., Almeida, J. P., Guarino, N., & Carvalho, V. A. (2015). Towards an ontological analysis of powertypes. In Proceedings of the Joint Ontology Workshops 2015 Episode 1: The Argentine Winter of Ontology co-located with the 24th International Joint Conference on Artificial Intelligence (IJCAI 2015); Buenos Aires, Argentina, July 25-27, 2015 (Vol. 1517). RWTH.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t0928-guizzardi-2005-thesis-chapter-06.md, 2026-06-05t1024-guizzardi-2022-ufo-full-document.md, 2026-06-05t1040-carvalho-2017-multi-level-ontology-based-conceptual-modeling-full-document.md, 2026-06-05t1040-guizzardi-2015-powertypes-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-05t2032; not final expert-validated documentation. |
