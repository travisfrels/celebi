---
name: create-adr
description: Create a local Architecture Decision Records (ADR) file. Use when the asked to create an ADR.
---

Create an ADR within a local ADR file (docs/adrs) around $ARGUMENTS.

## ADR Template

ADRs use the filename format `ADR-{SCOPE}-{TOPIC}-{DATE}.md` where:

- `{SCOPE}`: Category of the decision (see Scopes below)
- `{TOPIC}`: The concern being addressed, not the solution chosen (e.g., `PERSISTENCE` not `POSTGRESQL`)
- `{DATE}`: `YYYYMMDD`

Use the following template:

```markdown
# ADR: {Title}

## Status

{Status}

## Context

What problem or need prompted this decision? Include constraints, requirements, and the alternatives evaluated.

## Decision

One-sentence statement of what was chosen.

## Rationale

Why this alternative was selected over others. Evaluate using three criteria, in order: impact, least astonishment, idiomaticity. Include a comparison table and "Why not X?" sections for each rejected alternative.

## Consequences

**Positive:**

- Benefits of this decision.

**Negative:**

- Costs, risks, or tradeoffs accepted.

**Neutral:**

- Side effects that are neither positive nor negative.
```

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
