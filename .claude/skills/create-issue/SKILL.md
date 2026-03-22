---
name: create-issue
description: Create a GitHub issue. Use when asked to create an issue or report a defect (a.k.a. bug).
---

Create a GitHub Issue, using the GitHub (`gh`) CLI, about $ARGUMENTS

## Workflow

1. **Determine milestone**: Determine the milestone and project from context.
   - If you were called from the `create-project` skill, then use that project.
   - If you were called from the `review-pr` skill, then use the milestone from the PR's related issue.
   - If the issue reports a defect in an existing implementation, trace the defective code to its originating project:
     1. Use `git blame` on the defective code to find the commit that introduced it.
     2. Find the issue referenced in the commit message.
     3. Use `gh issue view {issue} --json milestone` to get that issue's milestone.
     4. If any step fails to produce a milestone, there is no milestone.
   - Otherwise, there is no milestone.
2. **Draft the issue** following the `## Issue Structure` and `## Style` guidelines below.
   a. **Validate acceptance criteria against ADRs**: Read the ADR index at `docs/adrs/CLAUDE.md` and identify any ADRs whose scope and topic are relevant to the issue's domain. For each relevant ADR with a status of "Accepted", read the ADR and verify that no acceptance criterion contradicts its decision or consequences. Revise any contradicting criteria to align with the ADR, noting the ADR reference in the criterion.
3. **Create the issue**: `gh issue create --title "{title}" --body "{body}"` — include `--milestone "{title}"` if a milestone was selected in step 1.

## Issue Structure

See [TEMPLATE.md](TEMPLATE.md) for the issue structure template.

## Style

- Concise and direct.
  - No jargon, no filler.
- Ground claims with data and references.
- Link to external docs (language, framework, SDK, library, and API references) where they add clarity.
- The issue is self-contained.
  - Contributors have everything needed to understand the issue.
- Never include sensitive information.
