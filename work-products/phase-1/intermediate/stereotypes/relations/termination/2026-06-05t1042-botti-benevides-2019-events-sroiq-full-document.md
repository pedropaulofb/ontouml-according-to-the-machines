# Termination

## Source-Specific Description Contribution

The source introduces `terminatedBy`, glossed as destructed by, as a relation from `Object` to `Event` (p. 12-13, Section 3.9). Together with `createdBy` and `changedBy`, this relation is left without cardinality constraints to avoid forcing infinite models and to allow eternal objects in infinite models (p. 12, Section 3.9).

For `terminatedBy`, the FOL axiom states that an object terminated by an event must be present in the situation that triggers the event, cannot be present in the situation brought about by the event, and must be related to the event through dependence: either the event itself or one of its atomic parts depends on the object (p. 13, Section 3.9, C2).

The SROIQ mapping only partially captures this constraint, retaining the implication from `terminatedBy` composed with the inverse of `triggers` to `presentIn` because the full FOL condition requires constructs not expressible in SROIQ (p. 22, Section 4.2.10, a183).

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "terminatedBy (meaning "destructed by")" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 12, Section 3.9.
- "an Object terminatedBy an Event must be presentIn" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 13, Section 3.9.
- "cannot be presentIn a Situation brought about" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 13, Section 3.9.

### Consulted Sources

- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1042; not a final documentation page; intended for later consolidation. |
