# Tests

Unit and integration tests. Run with `python -m pytest tests/ -v`.

## Modules

- `test_probability_engine.py` — Engine unit tests. Pure logic, no UI dependencies.
- `test_app.py` — UI integration tests. Requires Tk; uses a withdrawn root window (`root.withdraw()`). Includes dice roller widget, behavior, and E2E tests.
- `test_dice_roller.py` — Dice roller unit tests. Pure logic, no UI dependencies. Tests `roll_pool`, `select_dice`, `calculate_sum`, `DiceRollResult`.
- `test_theme.py` — Theme detection and application tests. Mocks `winreg` for detection; verifies `ttk.Style` configuration for all widget types.

## Conventions

- Framework: `unittest.TestCase`. Runner: `pytest`.
- One test class per concern (e.g., `TestValidation`, `TestExactProbabilities`, `TestModifiers`).
- Use `self.subTest()` for parametrized coverage over input combinations.
- UI tests share a single module-level `tk.Tk()` root (`setUpModule`/`tearDownModule`). `TestAppBase` creates a fresh `CelebiApp` per test and destroys child widgets in `tearDown`.
- Cross-validation tests compare the engine against an independent brute-force implementation to verify algorithmic correctness.
