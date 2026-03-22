---
name: create-adr
description: Create a local Architecture Decision Records (ADR) file. Use when asked to create an ADR.
---

Create an ADR within a local ADR file (docs/adrs) around $ARGUMENTS.

## Conventions

ADRs use the filename format `ADR-{SCOPE}-{TOPIC}-{DATE}.md` where:

- `{SCOPE}`: Category of the decision (see Scopes below)
- `{TOPIC}`: The concern being addressed, not the solution chosen (e.g., `PERSISTENCE` not `POSTGRESQL`)
- `{DATE}`: `YYYYMMDD`

See [TEMPLATE.md](TEMPLATE.md) for the ADR template.

ADRs that include subsystem design decisions should add a **Design** section between Rationale and Consequences, with "Alternatives not chosen" noted inline for each subsystem decision.

## Scopes

- **OP**: Operational — runtime infrastructure the application depends on (databases, caching, monitoring)
- **DEV**: Development — tooling and infrastructure for the development process (git hosting, CI/CD, task management)

## Status Values

- **Proposed**: Under discussion, not yet accepted
- **Accepted**: Decision is in effect
- **Superseded**: Replaced by a later ADR; note which one

## After Creating the ADR

Add a row to the `## Index` table in `docs/adrs/CLAUDE.md` with the new ADR's filename (as a relative link), title, scope, and status.
