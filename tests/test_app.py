import tkinter as tk
import unittest

from src.app import CelebiApp
from src.probability_engine import (
    SelectionStrategy,
    calculate_cumulative_probabilities,
    calculate_probabilities,
)


class TestAppBase(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = CelebiApp(root=self.root)
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def _get_table_data(self):
        rows = []
        for item_id in self.app.results_tree.get_children():
            values = self.app.results_tree.item(item_id, "values")
            rows.append((int(values[0]), values[1], values[2]))
        return rows


class TestWidgetCreation(TestAppBase):
    def test_window_title(self):
        self.assertEqual(self.root.title(), "Celebi — Trench Crusade Dice Probability Calculator")

    def test_pool_size_spinbox_exists(self):
        self.assertIsNotNone(self.app.pool_size_spinbox)

    def test_selection_radios_exist(self):
        self.assertIsNotNone(self.app.top_radio)
        self.assertIsNotNone(self.app.bottom_radio)

    def test_pick_count_radios_exist(self):
        self.assertIsNotNone(self.app.pick2_radio)
        self.assertIsNotNone(self.app.pick3_radio)

    def test_modifier_spinbox_exists(self):
        self.assertIsNotNone(self.app.modifier_spinbox)

    def test_results_treeview_exists(self):
        self.assertIsNotNone(self.app.results_tree)

    def test_treeview_columns(self):
        columns = self.app.results_tree["columns"]
        self.assertEqual(columns, ("total", "exact_pct", "cumulative_pct"))


class TestDefaultState(TestAppBase):
    def test_default_pool_size(self):
        self.assertEqual(self.app._pool_size_var.get(), "2")

    def test_default_selection(self):
        self.assertEqual(self.app._selection_var.get(), "top")

    def test_default_pick_count(self):
        self.assertEqual(self.app._pick_count_var.get(), "2")

    def test_default_modifier(self):
        self.assertEqual(self.app._modifier_var.get(), "0")

    def test_default_results_populated(self):
        rows = self._get_table_data()
        self.assertGreater(len(rows), 0)

    def test_default_results_match_engine(self):
        expected_exact = calculate_probabilities(
            2, 2, SelectionStrategy.TOP, 0
        )
        expected_cumulative = calculate_cumulative_probabilities(
            2, 2, SelectionStrategy.TOP, 0
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected_exact))
        for total, exact_str, cumulative_str in rows:
            self.assertEqual(exact_str, f"{expected_exact[total] * 100:.1f}%")
            self.assertEqual(cumulative_str, f"{expected_cumulative[total] * 100:.1f}%")


class TestInputChanges(TestAppBase):
    def test_pool_size_change_updates_results(self):
        self.app._pool_size_var.set("4")
        self.root.update()
        expected = calculate_cumulative_probabilities(
            4, 2, SelectionStrategy.TOP, 0
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_selection_change_updates_results(self):
        self.app._pool_size_var.set("3")
        self.root.update()
        self.app._selection_var.set("bottom")
        self.root.update()
        expected_exact = calculate_probabilities(
            3, 2, SelectionStrategy.BOTTOM, 0
        )
        expected_cumulative = calculate_cumulative_probabilities(
            3, 2, SelectionStrategy.BOTTOM, 0
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected_exact))
        for total, exact_str, cumulative_str in rows:
            self.assertEqual(exact_str, f"{expected_exact[total] * 100:.1f}%")
            self.assertEqual(cumulative_str, f"{expected_cumulative[total] * 100:.1f}%")

    def test_pick_count_change_updates_results(self):
        self.app._pool_size_var.set("4")
        self.root.update()
        self.app._pick_count_var.set("3")
        self.root.update()
        expected = calculate_cumulative_probabilities(
            4, 3, SelectionStrategy.TOP, 0
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_modifier_change_updates_results(self):
        self.app._modifier_var.set("3")
        self.root.update()
        expected_exact = calculate_probabilities(
            2, 2, SelectionStrategy.TOP, 3
        )
        expected_cumulative = calculate_cumulative_probabilities(
            2, 2, SelectionStrategy.TOP, 3
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected_exact))
        for total, exact_str, cumulative_str in rows:
            self.assertEqual(exact_str, f"{expected_exact[total] * 100:.1f}%")
            self.assertEqual(cumulative_str, f"{expected_cumulative[total] * 100:.1f}%")


class TestE2E(TestAppBase):
    def test_pool4_top_pick2_modifier1(self):
        self.app._pool_size_var.set("4")
        self.root.update()
        self.app._selection_var.set("top")
        self.root.update()
        self.app._pick_count_var.set("2")
        self.root.update()
        self.app._modifier_var.set("1")
        self.root.update()

        expected_exact = calculate_probabilities(
            4, 2, SelectionStrategy.TOP, 1
        )
        expected_cumulative = calculate_cumulative_probabilities(
            4, 2, SelectionStrategy.TOP, 1
        )
        rows = self._get_table_data()

        self.assertEqual(len(rows), len(expected_exact))
        for total, exact_str, cumulative_str in rows:
            self.assertEqual(
                exact_str,
                f"{expected_exact[total] * 100:.1f}%",
                f"Exact mismatch at total {total}",
            )
            self.assertEqual(
                cumulative_str,
                f"{expected_cumulative[total] * 100:.1f}%",
                f"Cumulative mismatch at total {total}",
            )


class TestEdgeCases(TestAppBase):
    def test_pool_equals_pick(self):
        self.app._pool_size_var.set("2")
        self.root.update()
        self.app._pick_count_var.set("2")
        self.root.update()
        rows = self._get_table_data()
        self.assertGreater(len(rows), 0)

    def test_negative_modifier(self):
        self.app._modifier_var.set("-5")
        self.root.update()
        expected = calculate_cumulative_probabilities(
            2, 2, SelectionStrategy.TOP, -5
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_invalid_spinbox_value_no_crash(self):
        self.app._pool_size_var.set("")
        self.root.update()
        rows = self._get_table_data()
        self.assertEqual(len(rows), 0)

    def test_pick_count_constrained_when_pool_too_small(self):
        self.app._pool_size_var.set("2")
        self.root.update()
        self.app._pick_count_var.set("3")
        self.root.update()
        self.assertEqual(self.app._pick_count_var.get(), "2")
        rows = self._get_table_data()
        self.assertGreater(len(rows), 0)

    def test_pick3_disabled_when_pool_size_2(self):
        self.app._pool_size_var.set("2")
        self.root.update()
        self.assertIn("disabled", self.app.pick3_radio.state())

    def test_pick3_enabled_when_pool_size_3(self):
        self.app._pool_size_var.set("3")
        self.root.update()
        self.assertNotIn("disabled", self.app.pick3_radio.state())

    def test_pick_count_resets_to_2_when_pool_shrinks(self):
        self.app._pool_size_var.set("4")
        self.root.update()
        self.app._pick_count_var.set("3")
        self.root.update()
        self.app._pool_size_var.set("2")
        self.root.update()
        self.assertEqual(self.app._pick_count_var.get(), "2")


if __name__ == "__main__":
    unittest.main()
