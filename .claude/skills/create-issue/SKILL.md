---
name: create-issue
description: Create a GitHub issue. Use when asked to create an issue or report a defect (a.k.a. bug).
---

Create a GitHub Issue, using the GitHub (`gh`) CLI, about $ARGUMENTS

## Workflow

1. **Determine milestone**: Determine the milestone and project from context.
   - If you were called from the `create-project` skill, then use that project.
   - If you were called directly, then there is no milestone.
2. **Draft the issue** following the `## Issue Structure` and `## Style` guidelines below.
   a. **Validate acceptance criteria against ADRs**: Read the ADR index at `docs/adrs/CLAUDE.md` and identify any ADRs whose scope and topic are relevant to the issue's domain. For each relevant ADR with a status of "Accepted", read the ADR and verify that no acceptance criterion contradicts its decision or consequences. Revise any contradicting criteria to align with the ADR, noting the ADR reference in the criterion.
3. **Create the issue**: `gh issue create --title "{title}" --body "{body}"` — include `--milestone "{title}"` if a milestone was selected in step 1.

## Issue Structure:

```markdown
## Project Reference

[{project-title}]({project-file-location})

## What is wrong?

Clearly and concisely describe the problem including any details about how to observe the problem directly. Explain the impact the problem is having on the system and/or stakeholders. Quantifying with data where it is possible to reference this data. Describe any workarounds currently used to compensate for the issue.

## Why is this a problem?

Describe the root cause. Explain the technical reason the problem exists rather than simply repeating what is wrong. To make the issue actionable reference code areas and behaviors, not specific file paths or line numbers because those can change over time.

## What is correct?

Describe what the correct behavior of the system should be. Include design patterns, strategies, and objective best practices by name where relevant. Avoid being overly prescriptive because creating an implementation plan is the part working the issue (`work-issue`), not creating the issue (`create-issue`).

## Edge cases (when applicable)

Call out non-obvious or un-common scenarios to address. Explain what makes these scenarios non-obvious or un-common.

## Acceptance criteria

Checkboxes. Each one should be independently testable. Cover:

- The happy path
- Key edge cases
- Things that should NOT change
```

## Style

- Concise and direct.
  - No jargon, no filler.
- Ground claims with data and references.
- Link to external docs (language, framework, SDK, library, and API references) where they add clarity.
- The issue is self-contained.
  - Contributors have everything needed to understand the issue.
- Never include sensitive information.
