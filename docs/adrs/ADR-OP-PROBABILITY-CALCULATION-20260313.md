# ADR: Probability Calculation Method

## Status

Superseded by [ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314](ADR-OP-PROBABILITY-CALCULATION-MULTISET-20260314.md)

## Context

The V1.00 Trench Crusade Dice Probability Calculator needs to compute the probability of every possible outcome for a dice pool mechanic: roll N d6, pick the top or bottom K dice, sum them, and apply a modifier. The application must display exact cumulative probabilities for each possible total.

Two approaches were evaluated:

| Criterion | Exact Combinatorial | Monte Carlo Simulation |
|-----------|--------------------|-----------------------|
| Impact | High — exact results, deterministic, no sampling error | Medium — approximate results, requires many iterations for convergence |
| Least Astonishment | High — users expect a "calculator" to give exact answers | Low — simulation introduces randomness into a deterministic tool |
| Idiomaticity | High — standard approach for bounded discrete probability spaces | Medium — common for large/continuous spaces, but overkill for small discrete problems |

## Decision

Use exact combinatorial calculation via brute-force enumeration of all possible outcomes.

## Rationale

The problem space is bounded and small: d6 dice with pool sizes 1–6 produce at most 6^6 = 46,656 outcomes — trivially enumerable on modern hardware. Exact computation guarantees deterministic, precise results with no sampling error, which is the natural expectation for a tool called a "calculator."

### Why not Monte Carlo Simulation?

Monte Carlo simulation introduces sampling error that requires thousands of iterations to converge to acceptable accuracy. For a small, bounded discrete probability space, simulation adds complexity (convergence criteria, seed management, confidence intervals) without benefit. The results would be non-deterministic — running the same inputs twice could produce slightly different outputs, which violates the principle of least astonishment for a calculator tool. The project explicitly requires "exact (combinatorial), not simulation-based" calculations.

## Consequences

**Positive:**

- Results are exact — no sampling error, no convergence concerns.
- Deterministic — identical inputs always produce identical outputs.
- Fast for the bounded input space (pool sizes 1–6, ~46K max outcomes).
- Simple implementation using `itertools.product` — trivially correct by construction.

**Negative:**

- Computational cost grows as 6^N with pool size. The upper bound of pool_size=6 keeps this manageable, but extending to larger pools (e.g., pool_size=10 → ~60M outcomes) would require a different approach.
- The brute-force approach does not generalize to continuous distributions or larger dice sets without modification.

**Neutral:**

- The implementation uses Python's `itertools.product` for enumeration, which is memory-efficient (generator-based) and well-understood.
- If future versions need to support larger pool sizes, the algorithm could be replaced with dynamic programming or generating functions without changing the public API.
