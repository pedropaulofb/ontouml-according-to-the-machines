# Participation

## Source-Specific Description Contribution

The source treats participation as the way objects are involved in events, including both atomic events that manifest their dispositions and complex events that have such atomic events as parts (p. 8, Section 3.4). `AtomicEvent` depends on a unique `Object`; `exclusivelyDependsOn` generalizes `dependsOn` to complex events, and both relations coincide for atomic events in the FOL theory (p. 8-9, Section 3.4, P1-P3).

A `Participation` is defined as an `Event` that exclusively depends on a unique `Object` (p. 8-9, Section 3.4, P4; p. 19, axioms a141-a142). This partitions events according to the ways a specific object contributes to the manifestation of atomic proper and non-proper event parts (p. 8, Section 3.4). The `participationOf` relation from `Participation` to `Object` is defined by `exclusivelyDependsOn` in the FOL theory (p. 9, Section 3.4, P5; p. 19-20, axiom a143).

In the comparison section, the source clarifies that UFO-B participation is not restricted to agents: an event is an `ufo-b:Participation` if it exclusively depends on a single, possibly inanimate, object (p. 32, Section 7.2).

## Stereotype Profile

TBD in a later phase.

## Examples

TBD in a later phase.

## References

### Direct Citations

- "Objects participate not only in the AtomicEvents" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 8, Section 3.4.
- "A Participation is an Event that exclusivelyDependsOn a unique Object" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 8, Section 3.4.
- "a single (possibly inanimate) object" — Source: Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.; Locator: p. 32, Section 7.2.

### Consulted Sources

- Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document.

## Generation and Review Log

| Date | Phase | Agent | Action | Prompt ID | Prompt Title | Inputs | Notes |
|---|---|---|---|---|---|---|---|
| 2026-06-05 | Phase 1 | GPT-5.5 Thinking | Intermediate population | prompt-phase-1-population-v1.1.0 | Phase 1 Population — Source-Grounded Intermediate File Generation | Botti Benevides, A., Bourguet, J. R., Guizzardi, G., Peñaloza, R., & Almeida, J. P. A. (2019). Representing a reference foundational ontology of events in SROIQ. Applied Ontology, 14(3), 293-334.. Scope: full document. | Source-specific intermediate file generated at 2026-06-05t1042; not a final documentation page; intended for later consolidation. |
