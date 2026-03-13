# ADR: GUI Framework

## Status

Accepted

## Context

The V1.00 Trench Crusade Dice Probability Calculator needed a GUI framework for a desktop application. The app displays input controls (spinboxes, radio buttons) and a results table showing cumulative probabilities. Requirements: zero external dependencies preferred, simple UI (no complex graphics or animations), Python ecosystem, desktop deployment.

Alternatives evaluated:

| Criterion | Tkinter | PyQt/PySide | Textual (TUI) | Web App |
|-----------|---------|-------------|---------------|---------|
| Impact | High — ships with Python, sufficient for V1.00 | High — polished UI, rich widget set | Medium — terminal-only, limited table/chart display | High — rich UI, broad reach |
| Least Astonishment | High — standard choice for simple Python desktop apps | Medium — heavier dependency for a simple tool | Low — non-technical users expect a window, not a terminal | Low — user explicitly requested desktop |
| Idiomaticity | High — Python's built-in GUI toolkit | Medium — common but adds third-party dependency | Medium — growing but niche for desktop apps | Low — different deployment model entirely |

## Decision

Use Tkinter as the GUI framework.

## Rationale

Tkinter is Python's built-in GUI toolkit, requiring zero external dependencies. The V1.00 scope (input controls + probability table) is well within Tkinter's capabilities. It is the idiomatic choice for simple Python desktop applications and the least surprising option for this use case.

### Why not PyQt/PySide?

PyQt/PySide provides a more polished UI and richer widget set, but adds a heavy external dependency (~50 MB) for a simple probability calculator. The licensing model (GPL for PyQt, LGPL for PySide) adds unnecessary complexity. Overkill for V1.00 scope.

### Why not Textual (TUI)?

Textual runs in the terminal rather than a windowed application. While it can render tables, the lack of a traditional GUI window would be less intuitive for non-technical users. Displaying probability charts and tables is harder in a terminal environment. Growing ecosystem but niche for desktop applications.

### Why not a Web App?

The user explicitly chose a desktop application. A web app would require a different deployment model (browser, possibly a server), adding complexity that is unnecessary for a single-user probability calculator.

## Consequences

**Positive:**

- Zero external dependencies — the app runs on any Python 3.10+ installation with no `pip install` step.
- Ships with Python's standard library, ensuring long-term availability and stability.
- Simple deployment: `python main.py` launches the app.

**Negative:**

- Limited styling and theming options compared to PyQt or web frameworks.
- Tkinter's widget set is functional but visually dated on some platforms.
- If future versions require complex visualizations (charts, graphs), Tkinter may become a constraint.

**Neutral:**

- Tkinter's event model (mainloop, trace_add) is well-documented and sufficient for reactive UI updates.
- The decision can be revisited in a future version if UI requirements outgrow Tkinter's capabilities.
