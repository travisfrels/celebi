---
name: create-project
description: Create a local project file and GitHub Milestone. Use when creating a project after using the plan-project skill.
---

Create project within a local project file (docs/projects) around $ARGUMENTS.

## Workflow

1. Create a GitHub issue to represent project creation.
2. Create a working branch to use with the project creation GitHub issue.
3. Create a GitHub Milestone matching the project title using `gh api repos/{owner}/{repo}/milestones -f title="V{VERSION} {Initiative Name}"`
   * The milestone title must match the project title exactly (e.g., `V0.7 Project Workflow`).
4. Create the project file at `docs/projects/V{VERSION}-{INITIATIVE}.md` using the template in `docs/projects/TEMPLATE.md`.
   * Populate template sections from the confirmed research brief.
   * Populate the `### Design References` section from the collected design references.
   * Include the milestone URL in the `## References` section.
5. Create the GitHub issues for the project, each with `--milestone "{milestone title}"`. Follow the issue structure and style conventions in the `create-issue` skill definition.
