import unittest

from src.dice_roller import DiceRollResult, calculate_sum, roll_pool, select_dice
from src.probability_engine import SelectionStrategy


class TestRollPool(unittest.TestCase):
    def test_returns_list_of_integers(self):
        result = roll_pool(2)
        self.assertIsInstance(result, list)
        for die in result:
            self.assertIsInstance(die, int)

    def test_pool_size_matches(self):
        for size in range(1, 13):
            result = roll_pool(size)
            self.assertEqual(len(result), size)

    def test_values_in_range(self):
        for _ in range(100):
            result = roll_pool(6)
            for die in result:
                self.assertGreaterEqual(die, 1)
                self.assertLessEqual(die, 6)

    def test_pool_size_zero_raises(self):
        with self.assertRaises(ValueError):
            roll_pool(0)

    def test_pool_size_negative_raises(self):
        with self.assertRaises(ValueError):
            roll_pool(-1)


class TestSelectDice(unittest.TestCase):
    def test_top_selection(self):
        pool = [1, 3, 5, 2]
        selected, unselected = select_dice(pool, 2, SelectionStrategy.TOP)
        self.assertEqual(sorted(selected), [3, 5])
        self.assertEqual(sorted(unselected), [1, 2])

    def test_bottom_selection(self):
        pool = [1, 3, 5, 2]
        selected, unselected = select_dice(pool, 2, SelectionStrategy.BOTTOM)
        self.assertEqual(sorted(selected), [1, 2])
        self.assertEqual(sorted(unselected), [3, 5])

    def test_pick_all(self):
        pool = [4, 2, 6]
        selected, unselected = select_dice(pool, 3, SelectionStrategy.TOP)
        self.assertEqual(sorted(selected), [2, 4, 6])
        self.assertEqual(unselected, [])

    def test_pick_one_top(self):
        pool = [1, 6, 3]
        selected, unselected = select_dice(pool, 1, SelectionStrategy.TOP)
        self.assertEqual(selected, [6])
        self.assertEqual(sorted(unselected), [1, 3])

    def test_pick_one_bottom(self):
        pool = [1, 6, 3]
        selected, unselected = select_dice(pool, 1, SelectionStrategy.BOTTOM)
        self.assertEqual(selected, [1])
        self.assertEqual(sorted(unselected), [3, 6])

    def test_preserves_pool_order_in_selected(self):
        pool = [5, 1, 4, 2]
        selected, _ = select_dice(pool, 2, SelectionStrategy.TOP)
        self.assertEqual(selected, [5, 4])

    def test_preserves_pool_order_in_unselected(self):
        pool = [5, 1, 4, 2]
        _, unselected = select_dice(pool, 2, SelectionStrategy.TOP)
        self.assertEqual(unselected, [1, 2])

    def test_duplicate_values_top(self):
        pool = [3, 3, 3, 1]
        selected, unselected = select_dice(pool, 2, SelectionStrategy.TOP)
        self.assertEqual(selected, [3, 3])
        self.assertEqual(sorted(unselected), [1, 3])

    def test_pick_count_exceeds_pool_raises(self):
        with self.assertRaises(ValueError):
            select_dice([1, 2], 3, SelectionStrategy.TOP)


class TestCalculateSum(unittest.TestCase):
    def test_basic_sum(self):
        self.assertEqual(calculate_sum([3, 5], 0), 8)

    def test_sum_with_positive_modifier(self):
        self.assertEqual(calculate_sum([3, 5], 2), 10)

    def test_sum_with_negative_modifier(self):
        self.assertEqual(calculate_sum([3, 5], -1), 7)

    def test_single_die(self):
        self.assertEqual(calculate_sum([6], 0), 6)

    def test_empty_list(self):
        self.assertEqual(calculate_sum([], 0), 0)


class TestDiceRollResult(unittest.TestCase):
    def test_fields(self):
        result = DiceRollResult(
            pool=[1, 3, 5, 2],
            selected=[5, 3],
            unselected=[1, 2],
            modifier=1,
            total=10,
        )
        self.assertEqual(result.pool, [1, 3, 5, 2])
        self.assertEqual(result.selected, [5, 3])
        self.assertEqual(result.unselected, [1, 2])
        self.assertEqual(result.modifier, 1)
        self.assertEqual(result.total, 10)

    def test_is_dataclass(self):
        import dataclasses

        self.assertTrue(dataclasses.is_dataclass(DiceRollResult))


if __name__ == "__main__":
    unittest.main()
