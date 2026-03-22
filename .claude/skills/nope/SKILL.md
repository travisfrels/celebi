---
name: nope
description: Correction for prohibited behaviors. Use when Claude violates command style rules (compound commands, git -C flag).
---

Stop. A prohibited behavior was just performed. Acknowledge the violation, then review and internalize the rules below.

## Prohibited Behaviors

### 1. Compound commands are strictly prohibited

Every shell command must be issued as its own, separate Bash tool call. Do not chain commands with `&&`, `||`, `;`, or any other operator.

**Why:** The `settings.local.json` file defines permission patterns that are evaluated per Bash tool call. Compound commands cannot be matched against these patterns, which forces manual approval prompts and breaks the automated workflow.

### 2. The git `-C` flag is prohibited

Do not use `git -C {path}`. Instead, `cd` to the target directory as a separate Bash tool call, then run the git command.

**Why:** `-C` is a form of compound command indirection — it changes the working directory inline, bypassing the same permission evaluation that compound commands bypass.

## Correction

1. Identify which rule was just violated.
2. State what was done incorrectly.
3. Redo the last action correctly, issuing each command as a separate Bash tool call.
