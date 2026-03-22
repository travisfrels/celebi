---
name: merge-main
description: Merge the latest main into the current working branch. Use when upstream changes need to be incorporated mid-flight.
---

Merge the latest main into the current working branch

1. Record the current branch name.
2. Perform branch hygiene using the `branch-hygiene` skill.
3. Use `git checkout {recorded-branch}` to return to the original working branch.
4. Use `git merge main` to merge main into the working branch.
