# Instantiation

## Source-Specific Description Contribution

The source uses MLT's instance-of relation as a primitive relation between an entity and the type it falls under, indexed by possible worlds. World-indexing supports dynamic classification: an entity may instantiate a type in one world and not in another (Section 3, p. 5).

The source uses instantiation to distinguish classification orders. First-order types are instantiated by individuals; second-order types are instantiated by first-order types. UFO categories themselves are positioned using this relation: concepts in UFO's taxonomy of individuals instantiate First-Order Type, while concepts in UFO's taxonomy of universals instantiate Second-Order Type (Sections 3-4, pp. 5, 7).

For the OntoUML extension, the source applies instantiation to domain models by requiring every first-order domain type to instantiate a leaf category of UFO's taxonomy of universals. Domain second-order types are introduced as specializations of those leaf categories and have their own instances at the first-order type level (Section 4, p. 7).

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "MLT defines a primitive instance of relation" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 5, Section 3.
- "The concepts in UFO's taxonomy of individuals are instances of "1stOT" specializing "Individual"" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 7, Section 4.
- "every domain first-order type must: (i) instantiate one of the leaf ontological categories of UFO's taxonomy of universals" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 7, Section 4.

### Consulted Sources

- Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1040; not a final documentation page; intended for later consolidation. |
