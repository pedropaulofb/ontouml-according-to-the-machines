# Creation

## Source-Specific Description Contribution

The source introduces `createdBy` as one of three relations from `Object` to `Event` used to model creation, termination, and change of objects (p. 12, Section 3.9). It explicitly imposes no cardinality constraints on these relations, in order to avoid necessitating infinite regress in object creation and to allow eternal objects in infinite models (p. 12, Section 3.9).

For `createdBy`, the FOL axiom states that an object created by an event cannot be present in the situation that triggers the event, must be present in the situation brought about by the event, and must be related to the event through dependence: either the event itself or one of its atomic parts depends on the object (p. 12-13, Section 3.9, C1).

The SROIQ mapping only partially captures this constraint, retaining the implication from `createdBy` composed with `bringsAbout` to `presentIn` because role negation and disjunction are not available in SROIQ (p. 22, Section 4.2.10, a182).

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "we introduce three relations from Objects to Events" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.
- "an Object createdBy an Event cannot be presentIn" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.
- "we impose no cardinality constraints" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.

### Consulted Sources

- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1042; not a final documentation page; intended for later consolidation. |
