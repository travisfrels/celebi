---
name: plan-project
description: Plan a project by investigating the problem space, drafting project definition content, and preparing for project creation. Use when starting a new project initiative.
---

Plan a project around $ARGUMENTS

1. Run the test suite to establish a clean baseline: `python -m pytest tests/ -v`. All tests must pass before proceeding. If any tests fail, report the failures to the user and stop — do not continue with project planning until the baseline is clean.
2. Read `projects/CLAUDE.md` and `projects/TEMPLATE.md`.
3. Read project documents in `projects/` noting the status of the project to identify lessons learned and in-flight work.
4. Examine the codebase for relevant files and documentation noting the behavior and constraints that each file imposes on the solution.
  - Stop when you can describe the current state in the Situation section without gaps.
5. Where the implementation space is non-obvious, consult official documentation and collect design reference URLs.
6. Present a requirements summary to the user for confirmation before drafting the research brief:
   * **Interpreted Intent**: A plain-language statement of what the project will build and the problem it solves.
   * **Key Assumptions**: Assumptions made that were not explicitly stated by the user.
   * **Scope Boundaries**: What is in scope and what is explicitly out of scope.
   * **Open Questions**: Ambiguities that need user input to resolve.

   Do not proceed to the research brief until the user confirms the requirements or provides corrections. Incorporate any corrections before continuing.
7. Draft a research brief and present it to the user for confirmation:
   * **Situation**: Current state, grounded in specific files, systems, and behaviors observed.
   * **Opportunity**: What is wrong or could be better, with root cause if applicable.
   * **Approach**: Generate viable alternatives — for each, describe what it is, how it addresses the problem, and its trade-offs. Present alternatives as columns in a markdown table with impact, least astonishment, and idiomaticity as rows at minimum. Then assess alternatives: score each against impact, least astonishment, and idiomaticity (High/Medium/Low), identify the most viable, and justify rejected alternatives. Present the recommendation with a decisions table if multiple decisions are involved.
   * **Goals**: What the project achieves.
   * **Non-Goals**: What the project explicitly does not attempt.
   * **Exit Criteria**: Verifiable conditions that define "done." For infrastructure or workflow projects, include at least one criterion that exercises the integrated system end-to-end.
   * **Issue Decomposition**: Break exit criteria into discrete, implementable issues. Each issue should have a title and a brief description of its scope. For features that affect user-facing behavior, include E2E test criteria in the feature issue's acceptance criteria rather than deferring E2E coverage to a separate terminal issue.
   * **Design References**: External documentation URLs consulted during research.
8. Iterate on user feedback until the research brief is confirmed.
9. Evaluate each decision in the Approach section against the ADR eligibility criteria in `adrs/CLAUDE.md`. For decisions that meet the criteria, create the ADR in `adrs/` following the ADR template and conventions in `adrs/CLAUDE.md`. Link the ADR in the research brief's Design References.
10. Create the project definition file and GitHub Milestone from the confirmed research brief:
    1. Create a GitHub issue to represent project creation.
    2. Create a working branch to use with the project creation GitHub issue.
    3. Create a GitHub Milestone matching the project title using `gh api repos/{owner}/{repo}/milestones -f title="V{VERSION} {Initiative Name}"`. The milestone title must match the project title exactly.
    4. Create the project file at `projects/V{VERSION}-{INITIATIVE}.md` using the template in `projects/TEMPLATE.md`. Populate template sections from the confirmed research brief. Populate the `### Design References` section from the collected design references. Include the milestone URL in the `## References` section.
    5. Create the GitHub issues for the project, each with `--milestone "{milestone title}"`. Follow the issue structure and style conventions in the `create-issue` skill definition.
