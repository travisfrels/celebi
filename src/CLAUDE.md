# Source

Application source code.

## Modules

- `app.py` — Tkinter GUI. `CelebiApp` class owns all widgets and wires input variables to `_update_results`.
- `probability_engine.py` — Pure computation. No UI or I/O dependencies. Stdlib only (`itertools`, `math`, `collections`).

## Conventions

- Private helpers are prefixed with `_` (e.g., `_validate_inputs`, `_compute_totals`).
- Public API functions have docstrings; private helpers do not.
- The probability engine uses multiset enumeration with multinomial weighting (see ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314).
- Validation limits: pool_size 1--12, pick_count 1--4.
