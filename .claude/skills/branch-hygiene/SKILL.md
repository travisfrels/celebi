---
name: branch-hygiene
description: Synchronize the local main branch with the remote. Use when a clean, up-to-date main is needed before creating a branch or merging.
---

Perform branch hygiene

1. Use `git checkout main` to checkout `main`.
2. Use `git fetch --prune` to fetch latest changes from the remote repository.
3. Use `git pull` to update `main` with the latest changes.
4. For each branch deleted from the remote repository:
   a. Use `git branch -D {branch-name}` to delete the branch locally.
