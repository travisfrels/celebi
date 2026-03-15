# ADR: Probability Calculation Method — Multiset Enumeration

## Status

Accepted (supersedes [ADR-OP-PROBABILITY-CALCULATION-20260313](ADR-OP-PROBABILITY-CALCULATION-20260313.md))

## Context

The V1.01 project increases the maximum pool size from 6 to 12. The existing brute-force algorithm enumerates all 6^N outcomes via `itertools.product`, which is O(6^N). At pool_size=12, this produces ~2.2 billion outcomes — infeasible for interactive use. The original ADR anticipated this limitation: "extending to larger pools (e.g., pool_size=10 → ~60M outcomes) would require a different approach."

Three approaches were evaluated:

| Criterion | Multiset Enumeration | Dynamic Programming | Brute-Force (cap at 8) |
|-----------|---------------------|---------------------|------------------------|
| Impact | High — handles N=12 (6,188 multisets), exact results | High — handles N=12+, exact results | Low — caps at N=8, doesn't meet requirement |
| Least Astonishment | High — code mirrors the physical dice mechanic | Medium — state transitions are abstract | High — identical to current code |
| Idiomaticity | High — `combinations_with_replacement` + `math.factorial` from stdlib | Medium — manual state tracking, less Pythonic | High — no change |

## Decision

Replace brute-force enumeration with multiset enumeration using `itertools.combinations_with_replacement`.

## Rationale

Instead of enumerating all 6^N permutations, enumerate unique sorted outcomes (multisets of size N from {1,2,3,4,5,6}) and weight each by its multinomial coefficient (N! / product of factorials of each face count). The number of multisets is C(N+5, 5), which grows polynomially:

| Pool Size | Brute-force (6^N) | Multisets C(N+5, 5) |
|-----------|-------------------|---------------------|
| 6 | 46,656 | 462 |
| 8 | 1,679,616 | 1,287 |
| 10 | 60,466,176 | 3,003 |
| 12 | 2,176,782,336 | 6,188 |

At N=12, this is a ~350,000x reduction. Results remain exact — the same combinatorial calculation, just a smarter way to count. The public API (`calculate_probabilities`, `cumulative_from_exact`, `calculate_cumulative_probabilities`) is unchanged.

### Why not Dynamic Programming?

DP is equally performant but harder to implement correctly for the top/bottom-K selection problem. State design for order statistics requires careful validation. The multiset space at N=12 is only 6,188, so DP's advantage of avoiding enumeration entirely provides no practical benefit. The higher implementation complexity and correctness risk are not justified.

### Why not brute-force with a higher cap?

Capping at pool_size=8 (1.6M outcomes) would still be feasible, but does not meet the stated requirement of pool sizes up to 12. Even pool_size=10 (~60M outcomes) introduces noticeable latency.

## Consequences

**Positive:**

- Results remain exact — no sampling error, deterministic.
- Handles pool_size=12 in well under 1 second (~6,188 multisets).
- Polynomial growth (C(N+5,5)) provides headroom beyond N=12 if needed.
- Uses Python stdlib (`itertools.combinations_with_replacement`, `math.factorial`).
- Public API unchanged — drop-in replacement.

**Negative:**

- Slightly more complex implementation than brute-force (multinomial coefficient calculation).
- Requires cross-validation against brute-force for small N to verify correctness during development.

**Neutral:**

- The `_select_dice` function (sorting and slicing) is reused unchanged.
- The approach can be further optimized with caching if needed, but is fast enough without it.
