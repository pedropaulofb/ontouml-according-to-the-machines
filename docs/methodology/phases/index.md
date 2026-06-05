# Project Phases

The project is organized into content-production phases.

A phase defines a bounded period of work with a specific purpose, execution model, output expectation, and maturity target. Phases help keep broad generation, review, refinement, and later automation work separate from each other.

## Why phases are used

This project produces documentation through iterative use of generative AI. Different moments of the project require different levels of precision, review, and tooling.

Using phases makes those differences explicit:

- early work can prioritize source-grounded extraction and structured first-pass population;
- later work can prioritize consolidation, validation, normalization, consistency, and expert review;
- limitations of each period remain visible;
- generated material can be refined without pretending that all pages have the same maturity level.

## Content-only scope

Project phases concern page content and content-production methodology.

They do not define or govern:

- website formatting;
- visual identity;
- CSS styling;
- MkDocs theme behavior;
- deployment infrastructure;
- general repository maintenance unrelated to documentation content.

## Current phases

| Phase | Name | Status | Main purpose |
|---|---|---|---|
| Phase 1 | [Groundwork and Initial Population](phase-1.md) | Planned / in progress | Generate source-specific intermediate files from selected high-yield sources for later consolidation into stereotype pages. |

## Phase relationship

The phases are cumulative but not necessarily exhaustive.

Phase 1 creates a provisional source-grounded intermediate content base. Later work may consolidate, review, refine, normalize, restructure, validate, or expand that base. A later phase may also revisit content produced in an earlier phase if new source material or review decisions require it.

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
