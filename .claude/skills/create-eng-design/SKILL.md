---
name: create-eng-design
description: Create or update the engineering design document (docs/ENG-DESIGN.md). Use when engineering design changes need to be documented.
---

Create or update the engineering design document (`docs/ENG-DESIGN.md`) for $ARGUMENTS.

## Before Modifying

1. Read the existing `docs/ENG-DESIGN.md` to understand the current state of the document.
2. Read relevant ADRs in `docs/adrs/` for architectural context behind existing sections.

## Template

See [TEMPLATE.md](TEMPLATE.md) for the engineering design document structure.

## Workflow

1. Identify which sections are affected by the change.
2. Update affected sections to reflect the new or modified design.
3. Add new sections following the template structure when introducing a new concern.
4. Update the status table: set `Last Updated` to today's date.
5. Update the Glossary if new domain terms are introduced.

## Conventions

- Sections document the current state of the system, not the history of changes.
- Reference ADRs by relative link when a section's design is governed by an architectural decision (e.g., `(see [ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314](adrs/ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314.md))`).
- Subsection decisions that chose one approach over others include an **Alternatives not chosen** block explaining what was rejected and why.
- Keep the document self-contained: a reader should understand the system's design without consulting source code.
