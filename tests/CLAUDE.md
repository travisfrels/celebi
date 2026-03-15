# Tests

Unit and integration tests. Run with `python -m pytest tests/ -v`.

## Modules

- `test_probability_engine.py` — Engine unit tests. Pure logic, no UI dependencies.
- `test_app.py` — UI integration tests. Requires Tk; uses a withdrawn root window (`root.withdraw()`).

## Conventions

- Framework: `unittest.TestCase`. Runner: `pytest`.
- One test class per concern (e.g., `TestValidation`, `TestExactProbabilities`, `TestModifiers`).
- Use `self.subTest()` for parametrized coverage over input combinations.
- UI tests inherit from `TestAppBase`, which handles `setUp`/`tearDown` for the Tk root and app instance.
- Cross-validation tests compare the engine against an independent brute-force implementation to verify algorithmic correctness.
