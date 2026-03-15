---
name: create-pr
description: Create a GitHub pull request. Use when a standalone pull request is needed outside the finish-issue workflow.
---

Create a GitHub pull request, using the GitHub (`gh`) CLI.

## Prerequisites Checklist

- [ ] On a working branch
- [ ] Working tree is clean

## Gather Context

1. Find the base branch
2. View the diffs
3. Find the related issue

### Checklist

- [ ] Base branch found
- [ ] Diffs reviewed
- [ ] Related issue identified

## Analyze the Changes

1. Do the changes address the issue?
2. Do the commits follow the implementation plan?
3. Was correctness verified?

### Checklist

- [ ] Changes address the issue
- [ ] Commits follow the implementation plan
- [ ] Correctness verified

## Create the Pull Request

1. Identify the issue.
2. Describe how the changes address the issue.
3. Describe how correctness was verified.

```bash
gh pr create --title "{Title}" --body "{Body}"
```
