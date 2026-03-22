import random
from dataclasses import dataclass

from src.probability_engine import SelectionStrategy


@dataclass
class DiceRollResult:
    pool: list[int]
    selected: list[int]
    unselected: list[int]
    modifier: int
    total: int


def roll_pool(pool_size: int) -> list[int]:
    """Roll a pool of d6 dice and return the individual results."""
    if pool_size < 1:
        raise ValueError(f"pool_size must be at least 1, got {pool_size}")
    return [random.randint(1, 6) for _ in range(pool_size)]


def select_dice(
    pool: list[int],
    pick_count: int,
    selection: SelectionStrategy,
) -> tuple[list[int], list[int]]:
    """Select dice from the pool by strategy, preserving original order.

    Returns (selected, unselected) where both lists preserve the order
    the dice appeared in the pool.
    """
    if pick_count > len(pool):
        raise ValueError(
            f"pick_count ({pick_count}) cannot exceed pool size ({len(pool)})"
        )

    indexed = list(enumerate(pool))
    sorted_by_value = sorted(indexed, key=lambda x: x[1])

    if selection == SelectionStrategy.TOP:
        chosen_indices = {i for i, _ in sorted_by_value[-pick_count:]}
    else:
        chosen_indices = {i for i, _ in sorted_by_value[:pick_count]}

    selected = [v for i, v in enumerate(pool) if i in chosen_indices]
    unselected = [v for i, v in enumerate(pool) if i not in chosen_indices]
    return selected, unselected


def calculate_sum(selected: list[int], modifier: int) -> int:
    """Calculate the total of selected dice plus modifier."""
    return sum(selected) + modifier
