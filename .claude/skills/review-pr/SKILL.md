---
name: review-pr
description: Review a GitHub pull request. Use when a GitHub pull request review is needed.
---

Review GitHub pull request $ARGUMENTS

## Gather Context

1. Fetch PR details using `gh pr view $ARGUMENTS`
2. Fetch PR comments using `gh pr view $ARGUMENTS --comments`
3. Fetch PR reviews using `gh pr view $ARGUMENTS --json reviews --jq '.reviews'`
4. Fetch PR diff using `gh pr diff $ARGUMENTS`
5. Fetch related issue using:
  - `gh issue view {related-issue}`
  - `gh issue view {related-issue} --comments`

## Review the Pull Request

1. Assess scope and correctness.
   * Does the PR do what the issue asks — no more, no less? Flag unrelated changes bundled into the PR.
   * Is the logic correct? Look for off-by-one errors, incorrect assumptions, missing conditions, and unhandled states.
   * Are there race conditions, null dereferences, or other correctness hazards?
   * When a gap is identified, check whether it is already tracked by another issue. If so, note the covering issue and whether the gap should be resolved in this PR or deferred.
2. Think critically about code quality and design.
   * Assess readability, maintainability, extensibility, and modularity.
   * Is the code clean, SOLID, DRY, and self documenting?
   * Does the code exhibit anti-patterns or code smells?
   * Is the code idiomatic for the language, frameworks, libraries, and SDKs used?
   * Are there any dead code paths or unused references, variables, or functions?
3. Assess security.
   * Are inputs validated at system boundaries (user input, external APIs)?
   * Are there injection vulnerabilities, authentication/authorization gaps, or insecure data handling?
   * Does the change introduce any OWASP Top 10 risks?
4. Assess test coverage and quality.
   * Do the tests effectively validate functionality, handle edge cases, and objectively follow best practices for testing?
   * Are there any redundant, missing, or ineffective tests?
   * Are tests each covering one-and-only-one behavior?
5. Assess documentation coverage and quality including README.md, CLAUDE.md, RUNBOOK.md, and project files.
   * Is the documentation clear, concise, comprehensive, up-to-date, and audience appropriate?
   * Does the documentation effectively communicate the purpose, intention, and usage of the code?
   * Are there stale README.md, CLAUDE.md, or RUNBOOK.md files?
   * If the change introduces or modifies an operational capability, does the runbook cover it?
   * If the change modifies environment-specific configuration or documentation, search `docs/ENG-DESIGN.md` for all references to the affected environment to ensure consistency across sections.
6. Determine if this body of work stays true to the intent of the issue, associated project document (docs/projects), and eng-design (docs/ENG-DESIGN.md).
   * If yes, then use a comment to clearly state that the pull request is acceptable and explain why.
   * If no, then use a comment explain the specific deficiencies, calling out anti-patterns by name if applicable. For each deficiency, propose a concrete alternative.

## Classify Findings

Label each finding before posting:

- **Defect** — Must be resolved before merge. Incorrect behavior, security issue, or a clear violation of project standards.
- **Observation** — Does not block merge. Worth noting for awareness or future improvement.

## Post the Pull Request Review

```bash
gh pr review $ARGUMENTS --comment --body '{Body}'
```
