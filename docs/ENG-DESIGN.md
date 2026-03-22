# Engineering Design

## Overview

Celebi is a desktop probability calculator for the tabletop game Trench Crusade. Players roll pools of six-sided dice, select the highest or lowest subset, apply modifiers, and compare the total against a threshold to determine success or failure. Celebi computes exact probabilities for every possible outcome, enabling players to evaluate risk before committing to in-game actions.

## Architecture

The application follows a two-layer architecture with strict separation between computation and presentation.

```
main.py
  └── CelebiApp (orchestrator)
        └── ScenarioFrame (1–4 instances)
              └── probability_engine (stateless computation)
```

- **Presentation layer** (`src/app.py`) — Tkinter GUI. Handles user input, layout, and results display. Depends on the computation layer but contains no probability logic.
- **Computation layer** (`src/probability_engine.py`) — Pure functions using only the standard library (`itertools`, `math`, `collections`). No UI or I/O dependencies. Can be tested and used independently of the GUI.

Data flows in one direction: user input changes trigger Tk variable traces, which call the probability engine, and the results are rendered back into the UI.

## Key Components

### CelebiApp

Application orchestrator. Manages the shared Tk root window, the scenario container, and the "Add Scenario" button. Supports 1–4 concurrent `ScenarioFrame` instances with dynamic add/remove. Handles grid relayout and remove-button visibility when scenarios change.

### ScenarioFrame

Self-contained scenario panel (`ttk.Frame` subclass). Each instance owns its own state and widgets:

- **Inputs**: pool size (1–12), selection strategy (top/bottom), pick count (1–4, constrained by pool size), modifier (-20 to +20), threshold (2–24)
- **Outputs**: success/failure percentages and a probability table (exact and cumulative percentages per total)
- **Reactivity**: All input variables are traced; any change recalculates and re-renders results immediately

### probability_engine

Stateless computation module. Public API:

| Function | Purpose |
|----------|---------|
| `calculate_probabilities` | Exact probability of each possible total |
| `cumulative_from_exact` | Cumulative probabilities (total or higher) |
| `success_failure` | Success/failure split at a given threshold |
| `calculate_cumulative_probabilities` | Convenience wrapper combining the above |

Uses multiset enumeration with multinomial weighting to compute exact probabilities. Enumerates `combinations_with_replacement(range(1,7), pool_size)` and weights each multiset by its multinomial coefficient. See [ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314](adrs/ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314.md) for rationale.

### SelectionStrategy

Enum (`TOP`, `BOTTOM`) controlling whether the highest or lowest dice from the pool are selected for the total.

### theme

OS-aware theming module (`src/theme.py`). Public API:

| Function | Purpose |
|----------|---------|
| `detect_system_theme` | Read Windows `AppsUseLightTheme` registry value via `winreg`; fall back to LIGHT |
| `apply_theme` | Configure `ttk.Style` (clam base) and root window background for a given `Theme` |

Defines `Theme` enum (`LIGHT`, `DARK`) and light/dark color palettes. Called once at startup by `CelebiApp.__init__` before widget construction. Uses only stdlib (`winreg`, `tkinter.ttk`).

## Environment

- **Python**: 3.10+
- **Dependencies**: None. Tkinter ships with the Python standard library.
- **Run**: `python main.py`
- **Test**: `python -m pytest tests/ -v`

## Design Decisions

Architectural decisions are recorded as ADRs in `docs/adrs/`. See the [ADR index](adrs/CLAUDE.md) for the full list and current status.
