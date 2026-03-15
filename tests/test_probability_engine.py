import itertools
import unittest
from collections import Counter

from src.probability_engine import (
    SelectionStrategy,
    calculate_cumulative_probabilities,
    calculate_probabilities,
    success_failure,
)


class TestValidation(unittest.TestCase):
    def test_pool_size_zero(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(0, 2, SelectionStrategy.TOP)

    def test_pool_size_negative(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(-1, 2, SelectionStrategy.TOP)

    def test_pool_size_too_large(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(13, 2, SelectionStrategy.TOP)

    def test_pick_count_invalid(self):
        with self.assertRaises(ValueError):
            calculate_probabilities(4, 5, SelectionStrategy.TOP)

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
        for pool_size in range(1, 13):
            for pick_count in range(1, 5):
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


class TestLargePoolSizes(unittest.TestCase):
    def test_pool_size_12_pick_4_top_returns_results(self):
        probs = calculate_probabilities(12, 4, SelectionStrategy.TOP)
        self.assertAlmostEqual(sum(probs.values()), 1.0)
        self.assertTrue(all(v >= 0 for v in probs.values()))

    def test_pool_size_12_pick_4_bottom_returns_results(self):
        probs = calculate_probabilities(12, 4, SelectionStrategy.BOTTOM)
        self.assertAlmostEqual(sum(probs.values()), 1.0)

    def test_pool_size_8_pick_3_top(self):
        probs = calculate_probabilities(8, 3, SelectionStrategy.TOP)
        self.assertAlmostEqual(sum(probs.values()), 1.0)
        self.assertEqual(min(probs.keys()), 3)
        self.assertEqual(max(probs.keys()), 18)

    def test_pick_count_4_valid(self):
        probs = calculate_probabilities(4, 4, SelectionStrategy.TOP)
        self.assertAlmostEqual(sum(probs.values()), 1.0)
        self.assertEqual(min(probs.keys()), 4)
        self.assertEqual(max(probs.keys()), 24)


class TestCrossValidation(unittest.TestCase):
    """Verify multiset results match brute-force for pool_size <= 6."""

    def _brute_force_probabilities(self, pool_size, pick_count, selection):
        totals: Counter[int] = Counter()
        for outcome in itertools.product(range(1, 7), repeat=pool_size):
            sorted_outcome = sorted(outcome)
            if selection == SelectionStrategy.TOP:
                selected = sorted_outcome[-pick_count:]
            else:
                selected = sorted_outcome[:pick_count]
            totals[sum(selected)] += 1
        total_outcomes = 6**pool_size
        return {k: v / total_outcomes for k, v in sorted(totals.items())}

    def test_cross_validate_all_small_pools(self):
        for pool_size in range(1, 7):
            for pick_count in range(1, min(pool_size, 4) + 1):
                for selection in SelectionStrategy:
                    with self.subTest(
                        pool=pool_size, pick=pick_count, sel=selection
                    ):
                        engine = calculate_probabilities(
                            pool_size, pick_count, selection
                        )
                        brute = self._brute_force_probabilities(
                            pool_size, pick_count, selection
                        )
                        self.assertEqual(engine.keys(), brute.keys())
                        for k in engine:
                            self.assertAlmostEqual(engine[k], brute[k])


class TestSuccessFailure(unittest.TestCase):
    def test_default_threshold_2d6(self):
        exact = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        failure, success = success_failure(exact)
        self.assertAlmostEqual(success, 21 / 36)
        self.assertAlmostEqual(failure, 15 / 36)

    def test_custom_threshold_10(self):
        exact = calculate_probabilities(2, 2, SelectionStrategy.TOP)
        failure, success = success_failure(exact, threshold=10)
        self.assertAlmostEqual(success, 6 / 36)
        self.assertAlmostEqual(failure, 30 / 36)

    def test_threshold_below_min_total(self):
        exact = calculate_probabilities(1, 1, SelectionStrategy.TOP)
        failure, success = success_failure(exact, threshold=0)
        self.assertAlmostEqual(success, 1.0)
        self.assertAlmostEqual(failure, 0.0)

    def test_threshold_above_max_total(self):
        exact = calculate_probabilities(1, 1, SelectionStrategy.TOP)
        failure, success = success_failure(exact, threshold=20)
        self.assertAlmostEqual(success, 0.0)
        self.assertAlmostEqual(failure, 1.0)

    def test_sum_to_one(self):
        for pool_size in range(1, 7):
            for pick_count in range(1, min(pool_size, 4) + 1):
                for selection in SelectionStrategy:
                    for threshold in (1, 7, 12):
                        with self.subTest(
                            pool=pool_size,
                            pick=pick_count,
                            sel=selection,
                            threshold=threshold,
                        ):
                            exact = calculate_probabilities(
                                pool_size, pick_count, selection
                            )
                            failure, success = success_failure(exact, threshold)
                            self.assertAlmostEqual(failure + success, 1.0)


if __name__ == "__main__":
    unittest.main()
