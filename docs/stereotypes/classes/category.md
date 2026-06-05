# Category

## Description

Category is an OntoUML class stereotype for rigid, relationally independent non-sortals. The supplied sources characterize a Category as a rigid mixin or dispersive universal that aggregates essential properties common to instances of different Kinds or rigid sortals. Because it is non-sortal, a Category does not provide a uniform principle of identity for its instances; identity is supplied by the relevant sortal types instantiated by those individuals.

The source-specific contributions consistently distinguish Category from sortal stereotypes and from anti-rigid mixins. Profile-oriented sources state that Category must be abstract, cannot have direct instances, and cannot specialize sortals such as Kind, Subkind, Phase, or Role. They also state that a rigid Category cannot specialize anti-rigid classifiers such as RoleMixin. One contribution reports the stricter profile constraint that Category can only be subsumed by another Category or by a Mixin.

For OntoUML 2-oriented sources, Category decorates rigid non-sortals whose instances may follow different identity principles and are not necessarily constrained to a single ontological nature. One multi-level modeling source further discusses Category specialization patterns as hierarchies in which more specific Categories may partition a more general Category according to immutable intrinsic properties, supporting Category as a rigid non-sortal taxonomic abstraction over entities of multiple Kinds.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- “We use the stereotype ´categoryª to represent a rigid mixin that subsumes different kinds” — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 4, Section 4.2.4, p. 112.
- “some mixins represent properties that are essential to some of its instances and accidental to others” — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 4, Section 4.2.4, p. 113.
- “rigid mixins (categories) cannot be subsumed by anti-rigid ones” — Source: Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.; Locator: Chapter 4, Section 4.2.4, p. 113.
- “categories: rigid types that define essential properties for their instances” — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 6, Section 1.
- “Category(t) ↔Rigid(t) ∧NonSortal(t)” — Source: Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.; Locator: p. 9, Section 2.2.
- “A Category represents a rigid and relationally independent non-sortal” — Source: Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021). Types and taxonomic structures in conceptual modeling: a novel ontological theory and engineering support. Data & Knowledge Engineering, 134, 101891.; Locator: p. 4, Section 2.
- “decorates classes that represent rigid non-sortals whose instances may follow different identity principles and are not constrained to a specific ontological nature.” — Source: Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021). Types and taxonomic structures in conceptual modeling: a novel ontological theory and engineering support. Data & Knowledge Engineering, 134, 101891.; Locator: p. 9, Section 4.1.
- “Rigid mixins that represent abstractions of properties that apply necessarily to instances of different kinds are called Category universals” — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 3, Section 2.1.
- “a second-order type that specialize "Category" must have, as base type, a rigid mixin universal” — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 11, Section 5.2.1.

### Consulted Sources

- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.. Scope: Chapter 4.
- Guizzardi, G. (2005). Ontological Foundations for Structural Conceptual Models. PhD thesis, University of Twente.. Scope: Chapter 8.
- Guizzardi, G., Fonseca, C. M., Benevides, A. B., Almeida, J. P. A., Porello, D., & Sales, T. P. (2018, September). Endurant types in ontology-driven conceptual modeling: Towards OntoUML 2.0. In International conference on conceptual modeling (pp. 136-150). Cham: Springer International Publishing.. Scope: full document.
- Guizzardi, G., Botti Benevides, A., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Prince Sales, T. (2022). UFO: Unified foundational ontology. Applied ontology, 17(1), 167-210.. Scope: full document.
- Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., & Porello, D. (2021). Types and taxonomic structures in conceptual modeling: a novel ontological theory and engineering support. Data & Knowledge Engineering, 134, 101891.. Scope: full document.
- Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Consolidation | prompt-phase-1-consolidation-v1.0.0 | Phase 1 Consolidation — Direct Main Commit for One Stereotype | 2026-06-05t0921-guizzardi-2005-thesis-chapter-04.md, 2026-06-05t0930-guizzardi-2005-thesis-chapter-08.md, 2026-06-05t1024-guizzardi-2018-endurant-types-full-document.md, 2026-06-05t1024-guizzardi-2022-ufo-full-document.md, 2026-06-05t1037-guizzardi-2021-types-taxonomic-structures-full-document.md, 2026-06-05t1040-carvalho-2017-multi-level-ontology-based-conceptual-modeling-full-document.md | First consolidated stereotype page generated from Phase 1 source-specific intermediate files at 2026-06-05t1508; not final expert-validated documentation. |
