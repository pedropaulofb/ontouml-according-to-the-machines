# Type

## Source-Specific Description Contribution

The source uses MLT to extend UFO/OntoUML so conceptual models can represent multiple classification levels rather than only first-order domain types. It distinguishes type orders: first-order types have individuals as instances, second-order types have first-order types as instances, and the scheme can extend further. Instantiation is treated as a primitive, world-indexed relation, enabling contingent classification (Section 3, p. 5).

In the UFO-MLT combination, first-order domain types instantiate a leaf category in UFO's taxonomy of universals while specializing a corresponding category in UFO's taxonomy of individuals. Domain second-order types are introduced as specializations of leaf categories in UFO's taxonomy of universals. Each such second-order type must also be related to a first-order base type by an MLT cross-level relation — categorization, complete categorization, disjoint categorization, partitioning, or power type — so that its instances are constrained as specializations of that base type (Sections 4-5, pp. 7-8).

For later consolidation, this source supports treating Type as the place for the multi-level modeling contribution: type order, instance-of, base type, and cross-level relations are the core mechanisms by which OntoUML is extended beyond a fixed set of first-order domain types.

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "Types having individuals as instances are called first-order types, types whose instances are first-order types are called second-order types" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 5, Section 3.
- "every domain second-order type has an MLT cross-level relation" — Source: Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24; Locator: p. 7, Section 4.

### Consulted Sources

- Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., & Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling. Data & Knowledge Engineering, 109, 3-24. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1040; not a final documentation page; intended for later consolidation. |
