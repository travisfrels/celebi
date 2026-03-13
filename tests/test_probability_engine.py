import unittest

from src.probability_engine import (
    SelectionStrategy,
    calculate_cumulative_probabilities,
    calculate_probabilities,
)


class TestValidation(unittest.TestCase):
    def test_pool_size_zero(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(0, 2, SelectionStrategy.TOP)

    def test_pool_size_negative(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(-1, 2, SelectionStrategy.TOP)

    def test_pick_count_invalid(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(4, 4, SelectionStrategy.TOP)

    def test_pick_count_zero(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(2, 0, SelectionStrategy.TOP)

    def test_pick_count_exceeds_pool(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(1, 2, SelectionStrategy.TOP)

    def test_cumulative_also_validates(self):
        with self.assertRaises(ValueError):
            calculate_cumulative_probabilities(0, 2, SelectionStrategy.TOP)


class TestExactProbabilities(unittest.TestCase):
    def test_2d6_pick_2_total_7(self):
        probs = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        self.assertAlmostEqual(probs[7], 6 / 36)

    def test_2d6_pick_2_total_2(self):
        probs = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        self.assertAlmostEqual(probs[2], 1 / 36)

    def test_2d6_pick_2_total_12(self):
        probs = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        self.assertAlmostEqual(probs[12], 1 / 36)

    def test_3d6_pick_top_2_max(self):
        # Top-2 sum of 12 requires at least two 6s: C(3,2)*5 + 1 = 16 outcomes
        probs = calculate_probabilities(3, 2, SelectionStrategy.TOP)
        self.assertAlmostEqual(probs[12], 16 / 216)

    def test_3d6_pick_bottom_2_min(self):
        # Bottom-2 sum of 2 requires at least two 1s: C(3,2)*5 + 1 = 16 outcomes
        probs = calculate_probabilities(3, 2, SelectionStrategy.BOTTOM)
        self.assertAlmostEqual(probs[2], 16 / 216)

    def test_1d6_pick_1(self):
        probs = calculate_probabilities(1, 1, SelectionStrategy.TOP)
        for face in range(1, 7):
            self.assertAlmostEqual(probs[face], 1 / 6)


class TestProbabilitySumToOne(unittest.TestCase):
    def test_all_valid_combinations(self):
        for pool_size in range(1, 7):
            for pick_count in (1, 2, 3):
                if pick_count > pool_size:
                    continue
                for selection in SelectionStrategy:
                    for modifier in (-2, 0, 3):
                        with self.subTest(
                            pool=pool_size,
                            pick=pick_count,
                            sel=selection,
                            mod=modifier,
                        ):
                            probs = calculate_probabilities(
                                pool_size, pick_count, selection, modifier
                            )
                            self.assertAlmostEqual(sum(probs.values()), 1.0)


class TestCumulativeProbabilities(unittest.TestCase):
    def test_lowest_total_is_one(self):
        cumulative = calculate_cumulative_probabilities(
            3, 2, SelectionStrategy.TOP
        )
        lowest = min(cumulative.keys())
        self.assertAlmostEqual(cumulative[lowest], 1.0)

    def test_highest_total_equals_exact(self):
        exact = calculate_probabilities(3, 2, SelectionStrategy.TOP)
        cumulative = calculate_cumulative_probabilities(
            3, 2, SelectionStrategy.TOP
        )
        highest = max(cumulative.keys())
        self.assertAlmostEqual(cumulative[highest], exact[highest])

    def test_monotonically_non_increasing(self):
        cumulative = calculate_cumulative_probabilities(
            4, 3, SelectionStrategy.BOTTOM
        )
        totals = sorted(cumulative.keys())
        for i in range(1, len(totals)):
            self.assertGreaterEqual(
                cumulative[totals[i - 1]], cumulative[totals[i]]
            )

    def test_2d6_cumulative_gte_7(self):
        cumulative = calculate_cumulative_probabilities(
            2, 2, SelectionStrategy.TOP
        )
        self.assertAlmostEqual(cumulative[7], 21 / 36)


class TestModifiers(unittest.TestCase):
    def test_positive_modifier_shifts_keys(self):
        base = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        shifted = calculate_probabilities(2, 2, SelectionStrategy.TOP, modifier=3)
        for k, v in base.items():
            self.assertAlmostEqual(shifted[k + 3], v)

    def test_negative_modifier_shifts_keys(self):
        base = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        shifted = calculate_probabilities(
            2, 2, SelectionStrategy.TOP, modifier=-1
        )
        for k, v in base.items():
            self.assertAlmostEqual(shifted[k - 1], v)

    def test_zero_modifier_same_as_default(self):
        default = calculate_probabilities(3, 2, SelectionStrategy.TOP)
        explicit = calculate_probabilities(
            3, 2, SelectionStrategy.TOP, modifier=0
        )
        self.assertEqual(default, explicit)


class TestEdgeCases(unittest.TestCase):
    def test_pool_equals_pick_top_bottom_identical(self):
        top = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        bottom = calculate_probabilities(2, 2, SelectionStrategy.BOTTOM)
        for k in top:
            self.assertAlmostEqual(top[k], bottom[k])

    def test_pool_equals_pick_3(self):
        top = calculate_probabilities(3, 3, SelectionStrategy.TOP)
        bottom = calculate_probabilities(3, 3, SelectionStrategy.BOTTOM)
        for k in top:
            self.assertAlmostEqual(top[k], bottom[k])

    def test_pool_size_1_pick_1_top(self):
        probs = calculate_probabilities(1, 1, SelectionStrategy.TOP)
        self.assertEqual(len(probs), 6)

    def test_pool_size_1_pick_1_bottom(self):
        top = calculate_probabilities(1, 1, SelectionStrategy.TOP)
        bottom = calculate_probabilities(1, 1, SelectionStrategy.BOTTOM)
        self.assertEqual(top, bottom)


if __name__ == "__main__":
    unittest.main()
