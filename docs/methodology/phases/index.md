# Project Phases

The project is organized into methodology phases.

A phase defines a bounded period of work with a specific purpose, execution model, output expectation, and maturity target. Phases help keep broad generation, review, refinement, check infrastructure, and later automation work separate from each other.

## Why phases are used

This project produces documentation through iterative use of generative AI. Different moments of the project require different levels of precision, review, and tooling.

Using phases makes those differences explicit:

- early work can prioritize source-grounded extraction, structured first-pass population, and controlled consolidation;
- later work can prioritize validation, normalization, consistency, expert review, examples, and profile completion;
- phase-specific tooling can be introduced without implying that it performs full content validation or autonomous remediation;
- limitations of each period remain visible;
- generated material can be refined without pretending that all pages have the same maturity level.

## Content and methodology scope

Project phases concern page content, content-production methodology, and phase-specific review or check infrastructure.

They do not define or govern:

- website formatting;
- visual identity;
- CSS styling;
- MkDocs theme behavior;
- deployment infrastructure;
- general repository maintenance unrelated to documentation content or documented phase methodology.

## Current phases

| Phase | Name | Status | Main purpose |
|---|---|---|---|
| Phase 1 | [Groundwork and Initial Population](phase-1.md) | In progress | Generate source-specific intermediate files from selected high-yield sources and consolidate them into first canonical stereotype pages. |
| Phase 2 | [Lightweight Check-Agent Infrastructure](phase-2.md) | Active / implemented infrastructure | Provide deterministic and LLM-based check-agent infrastructure that emits page-local signals, routes them to page-plus-agent GitHub issues, and supports manual confirmation-gated review of LLM signal issues. |

## Phase relationship

The phases are cumulative but not necessarily exhaustive.

Phase 1 creates a provisional source-grounded documentation base. Phase 2 adds lightweight page-local check infrastructure over that base: deterministic page-structure checks in CI, scheduled conservative LLM signal collection for page hygiene and language/style, deterministic issue routing, and manual confirmation-gated signal-review prompts. Phase 2 does not perform source-faithfulness validation, conceptual adequacy review, cross-page semantic comparison, automatic page repair, automatic PR creation, or automatic issue closure. Later work may review, refine, normalize, restructure, validate, or expand the documentation base. A later phase may also revisit content produced in an earlier phase if new source material, review decisions, or automation requirements justify it.

## Maturity expectation

A page or work product produced in an early phase should not be interpreted as final.

The maturity of a page or work product depends on:

- which phase produced or revised it;
- which sources were used;
- whether the content has been checked against authoritative OntoUML and UFO material;
- whether the page or work product has undergone systematic review;
- whether unresolved conceptual or citation issues remain.

## Phase documentation

Each phase document should specify:

- purpose;
- scope;
- execution model;
- input model;
- output model;
- citation and source-reporting requirements;
- deferred work;
- risks;
- completion criteria;
- generation or review log requirements.
