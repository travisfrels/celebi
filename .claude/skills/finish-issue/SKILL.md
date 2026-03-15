---
name: finish-issue
description: Finish working on a GitHub issue. Used in the context of work-issue when the issue work is complete. Creates the GitHub pull request.
---

Finish GitHub issue $ARGUMENTS

1. Use the `git` CLI to add, commit, and push any remaining changes to the working branch.
2. Use `git log -n 10 --pretty=format:"%h - %an, %ar : %s"` to sanity check repository changes.
3. Think critically about issue implementation and use `gh issue comment $ARGUMENTS --body '{Body}'` to post an implementation summary comment to the issue with the following sections:
    - **What was implemented.**
    - **Design decisions**: decisions made and the rationale behind them.
    - **Open questions**: unresolved issues that remain.
    - **Blockers**: what slowed or stopped progress, and what systemic condition caused it. None if unobstructed.
    - **Rework**: what had to be redone and why. None if not applicable.
    - **Scope changes**: what was added, dropped, or deferred from the original plan. None if unchanged.
4. Check for stale CLAUDE.md files.
5. Create a GitHub pull request using the GitHub (`gh`) CLI:
    1. Verify prerequisites: on a working branch, working tree is clean.
    2. Gather context: find the base branch, view the diffs (`git diff {base}...HEAD`), find the related issue.
    3. Analyze: do the changes address the issue? Do the commits follow the implementation plan? Was correctness verified?
    4. Create the PR:
       - Identify the issue.
       - Describe how the changes address the issue.
       - Describe how correctness was verified.
       ```bash
       gh pr create --title "{Title}" --body "{Body}"
       ```
6. Update the project doc in `docs/projects/`:
    - Add the PR URL returned by step 5 to the `### Pull Requests` section.
    - If this issue is a follow-up (not in the project's original scope), add the issue URL to the `### Follow-Up Issues` section.
    - Commit and push the project doc update.
    - Verify: grep the project doc for the PR URL. If missing, the update failed — retry before proceeding.
7. Check milestone progress:
    - If the issue title starts with `Post-Mortem:`, skip this step (the project-post-mortem skill handles project completion).
    - Retrieve the issue's milestone: `gh issue view $ARGUMENTS --json milestone`.
    - If the issue has a milestone, query progress: `gh api repos/{owner}/{repo}/milestones/{number}`.
    - If `open_issues` is 1 (this is the last open issue in the milestone):
      1. Prompt the developer to verify exit criteria in the project document before marking the project Done.
      2. Create a post-mortem issue:
         ```bash
         gh issue create \
           --title "Post-Mortem: {milestone title}" \
           --body "Perform a post-mortem analysis of the {milestone title} project.\n\n/project-post-mortem {project name}" \
           --milestone "{milestone title}"
         ```
