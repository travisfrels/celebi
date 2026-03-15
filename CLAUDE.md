# Celebi

Trench Crusade dice probability calculator. Desktop app built with Python + Tkinter.

## Quick Reference

- **Run the app**: `python main.py`
- **Run tests**: `python -m pytest tests/ -v`
- **Python version**: 3.10+
- **Dependencies**: None (Tkinter is built into Python)

## Project Structure

```
src/
  app.py                 # Tkinter GUI (CelebiApp class)
  probability_engine.py  # Exact combinatorial probability calculations
tests/
  test_app.py            # UI tests (requires Tk)
  test_probability_engine.py  # Engine unit tests
projects/                # Project definitions and milestone tracking
adrs/                    # Architecture Decision Records
  CLAUDE.md              # ADR index and conventions
main.py                  # Entry point
```

## Documentation

- `projects/` — Project definitions. Check here for scope, status, and exit criteria before starting work.
- `adrs/` — Architecture Decision Records. Check `adrs/CLAUDE.md` for the index. Consult before making design choices that may already be settled.
- `projects/TEMPLATE.md` — Template for new project definitions.

## Skills

Custom skills are defined in `.claude/skills/`. Each skill has a `SKILL.md` with its workflow.

| Skill | Purpose |
|-------|---------|
| `plan-project` | Plan a new project initiative (research, requirements, brief) |
| `create-project` | Create project definition file, milestone, and issues |
| `work-issue` | Start working on a GitHub issue (branch, plan, implement) |
| `finish-issue` | Complete issue work (commit, PR, project doc update) |
| `create-issue` | Create a GitHub issue |
| `create-pr` | Create a standalone pull request |
| `review-pr` | Review a GitHub pull request |
| `fetch-pr` | Fetch PR details, comments, and reviews |
| `create-adr` | Create an Architecture Decision Record |
| `design` | Generate solution alternatives (used with assess-alternatives) |
| `assess-alternatives` | Score and select from alternatives |
| `critique` | Critical assessment of a statement or idea |
| `project-post-mortem` | Post-mortem analysis after project completion |

## Conventions

- **Testing**: Use `unittest`. Tests live in `tests/`. Run with `pytest`.
- **Git workflow**: Branch per issue (`issue-{number}-{description}`). PRs reference issues.
- **Commits**: Concise message, reference issue number, include `Co-Authored-By` when AI-assisted.
- **Project tracking**: GitHub Milestones group issues per project. Project docs in `projects/`.
- **ADRs**: Follow template in `adrs/CLAUDE.md`. Filename format: `ADR-{SCOPE}-{TOPIC}-{DATE}.md`.
