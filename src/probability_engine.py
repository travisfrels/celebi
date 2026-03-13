import itertools
from collections import Counter
from enum import Enum


class SelectionStrategy(Enum):
    TOP = "top"
    BOTTOM = "bottom"


def _validate_inputs(pool_size: int, pick_count: int) -> None:
    if pool_size < 1:
        raise ValueError(f"pool_size must be at least 1, got {pool_size}")
    if pool_size > 6:
        raise ValueError(f"pool_size must be at most 6, got {pool_size}")
    if pick_count not in (1, 2, 3):
        raise ValueError(f"pick_count must be 1, 2, or 3, got {pick_count}")
    if pick_count > pool_size:
        raise ValueError(
            f"pick_count ({pick_count}) cannot exceed pool_size ({pool_size})"
        )


def _enumerate_outcomes(pool_size: int):
    return itertools.product(range(1, 7), repeat=pool_size)


def _select_dice(
    outcome: tuple[int, ...],
    pick_count: int,
    selection: SelectionStrategy,
) -> tuple[int, ...]:
    sorted_outcome = sorted(outcome)
    if selection == SelectionStrategy.TOP:
        return tuple(sorted_outcome[-pick_count:])
    return tuple(sorted_outcome[:pick_count])


def _compute_totals(
    pool_size: int,
    pick_count: int,
    selection: SelectionStrategy,
    modifier: int,
) -> Counter[int]:
    totals: Counter[int] = Counter()
    for outcome in _enumerate_outcomes(pool_size):
        selected = _select_dice(outcome, pick_count, selection)
        total = sum(selected) + modifier
        totals[total] += 1
    return totals


def calculate_probabilities(
    pool_size: int,
    pick_count: int,
    selection: SelectionStrategy,
    modifier: int = 0,
) -> dict[int, float]:
    """Return exact probability of each possible total.

    Returns a dict mapping each possible total to its probability (0.0-1.0).
    Keys are sorted ascending.
    """
    _validate_inputs(pool_size, pick_count)
    totals = _compute_totals(pool_size, pick_count, selection, modifier)
    total_outcomes = 6**pool_size
    return {
        k: v / total_outcomes for k, v in sorted(totals.items())
    }


def calculate_cumulative_probabilities(
    pool_size: int,
    pick_count: int,
    selection: SelectionStrategy,
    modifier: int = 0,
) -> dict[int, float]:
    """Return cumulative probabilities (chance of achieving each total or higher).

    Returns a dict mapping each possible total to the probability of rolling
    that total or higher. Keys are sorted ascending. The lowest key always
    maps to 1.0.
    """
    exact = calculate_probabilities(pool_size, pick_count, selection, modifier)
    cumulative: dict[int, float] = {}
    running_sum = 0.0
    for total in sorted(exact.keys(), reverse=True):
        running_sum += exact[total]
        cumulative[total] = running_sum
    return dict(sorted(cumulative.items()))
