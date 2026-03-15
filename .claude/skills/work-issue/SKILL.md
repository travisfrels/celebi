---
name: work-issue
description: Start working on a GitHub issue. Use when working a GitHub issue is needed.
---

Implement the GitHub issue $ARGUMENTS

## 1. Branch Hygiene

1. Use `git checkout main` to checkout `main`.
2. Use `git fetch --prune` to fetch latest changes from the remote repository.
3. Use `git pull` to update `main` with the latest changes.
4. For each branch deleted from the remote repository:
   a. Use `git branch -D {branch-name}` to delete the branch locally.

## 2. Plan the Implementation

1. Read `docs/ENG-DESIGN.md`.
2. Read the issue using `gh issue view $ARGUMENTS && gh issue view $ARGUMENTS --comments`.
3. Identify the key decision points for implementing issue $ARGUMENTS.
  - A decision point is any choice between meaningfully different implementation approaches that affects design, behavior, or maintainability.
  - For each decision point:
    a. **Generate alternatives**: A viable alternative is one that is objectively reasonable and feasibly implementable within project constraints. Where the implementation space is non-obvious, consult official documentation and cite relevant excerpts. For each alternative, describe: what it is, how it addresses the problem, and its trade-offs. Present alternatives as columns in a markdown table. Use impact, least astonishment, and idiomaticity as rows at minimum; add other relevant trade-off dimensions as needed. Do not score, rank, or advocate. Characterize only.
    b. **Assess alternatives**: Score each alternative against impact (High/Medium/Low), least astonishment (High/Medium/Low), and idiomaticity (High/Medium/Low). Present scores in a markdown table with criteria as rows and alternatives as columns. Identify the most viable alternative and justify the selection. List alternatives not chosen and justify their rejection.
    c. Present the analysis and recommendation to the user and get explicit confirmation before proceeding.
    d. If the user rejects the recommendation, refine the alternatives and re-present.
    e. After the user confirms the recommendation, evaluate the decision against the ADR eligibility criteria in `docs/adrs/CLAUDE.md`.

## 3. Implementation

1. Assign the issue using `gh issue edit $ARGUMENTS --add-assignee @me`.
2. Post a step-by-step implementation plan using `gh issue comment $ARGUMENTS --body '{Implementation_Plan}'`.
3. Checkout a working branch from `main` using `git checkout -b issue-$ARGUMENTS-{slugified_issue_title}`.
4. Push the branch to origin using `git push --set-upstream origin issue-$ARGUMENTS-{slugified_issue_title}`.
5. For each decision that meets the criteria:
  a. Create an ADR in `docs/adrs/` following the ADR template and conventions in `docs/adrs/CLAUDE.md`.
6. Set project status to "Active":
  - If the issue has a milestone, find the matching project file in `docs/projects/` and append an Active row to its status table.
    - Skip if already Active or Done, or if the issue has no milestone.
    - See `docs/projects/CLAUDE.md` for status conventions.
7. Implement the plan.
8. Use the finish-issue skill to complete the issue.
