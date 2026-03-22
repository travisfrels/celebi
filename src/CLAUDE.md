# Source

Application source code.

## Modules

- `app.py` — Tkinter GUI. `ScenarioFrame(ttk.Frame)` owns per-scenario state and widgets. `CelebiApp` orchestrates 1–4 `ScenarioFrame` instances with add/remove management.
- `dice_roller.py` — Dice rolling logic. `roll_pool()`, `select_dice()`, `calculate_sum()`, `DiceRollResult` dataclass. Uses `random` (stdlib).
- `probability_engine.py` — Pure computation. No UI or I/O dependencies. Stdlib only (`itertools`, `math`, `collections`).
- `theme.py` — OS-aware light/dark theming. Detects Windows system theme via `winreg`, applies palettes via `ttk.Style`. Stdlib only.

## Conventions

- Private helpers are prefixed with `_` (e.g., `_validate_inputs`, `_compute_totals`).
- Public API functions have docstrings; private helpers do not.
- The probability engine uses multiset enumeration with multinomial weighting (see ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314).
- Validation limits: pool_size 1--12, pick_count 1--4.
