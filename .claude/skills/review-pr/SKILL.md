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

## Validate Findings

Apply the [`/critique`](../critique/SKILL.md) skill to each finding before posting. The critique's verdict determines the finding's fate:

- **Defects**: Confirmed Defect, Downgrade to Observation, or Dismiss.
- **Observations**: Confirmed Observation or Dismiss.

Validation reasoning is internal. Only confirmed findings and their verdicts appear in the posted review.

## Post the Pull Request Review

Post only confirmed findings. Include the classification label (Defect or Observation) and the validation verdict for each finding so the PR author understands the reasoning.

```bash
gh pr review $ARGUMENTS --comment --body '{Body}'
```

If the review contains any confirmed defects, end the body with a **Merge Blocked** notice stating that defects must be resolved before merge.

## Record Findings in Project Document

After posting the review, record all confirmed findings in the associated project document in `docs/projects/`.

1. Identify the project doc from the PR's related issue and its milestone. If the related issue has no milestone, skip this section.
2. Add a row to the `## Defects` table for each confirmed defect: the PR, finding description, and required resolution.
3. Add a row to the `## Observations` table for each confirmed observation: the PR, finding description, and disposition.
4. Commit and push the project doc update.

## Create Issues for Out-of-Scope Findings

For each confirmed finding that should not be addressed in this PR, create a GitHub issue using the [`/create-issue`](../create-issue/SKILL.md) skill. Assign the issue to the same milestone as the PR's related issue so the finding is associated with the project whose implementation produced it.

## Defect Deferral

Defects must be resolved before merge. The PR author fixes the defects and the reviewer confirms resolution in a follow-up review.

If deferral is necessary, the reviewer must post a comment to the PR documenting:

1. The decision to defer the defect.
2. The justification for deferral.
3. Confirmation that the defect is tracked (in the project Defects table and/or as a follow-up issue).
