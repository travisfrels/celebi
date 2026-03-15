---
name: fetch-pr
description: Fetch GitHub pull request details, comments, and reviews
---

Fetch GitHub pull request $ARGUMENTS

1. Fetch PR details.
2. Fetch PR comments.
3. Fetch PR reviews.

```bash
gh pr view $ARGUMENTS
gh pr view $ARGUMENTS --comments
gh pr view $ARGUMENTS --json reviews --jq '.reviews'
gh pr diff $ARGUMENTS
```

4. Summarize

Tell the user:
- PR title, state, and branch info
- Each comment with its author and body
- Each review with its state, body, and inline comments (include the file path, line number, and comment body)
