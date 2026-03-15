import tkinter as tk
import unittest

from src.app import CelebiApp, ScenarioFrame
from src.probability_engine import (
    SelectionStrategy,
    calculate_cumulative_probabilities,
    calculate_probabilities,
    success_failure,
)

_root = None


def setUpModule():
    global _root
    _root = tk.Tk()
    _root.withdraw()


def tearDownModule():
    global _root
    _root.destroy()
    _root = None


class TestAppBase(unittest.TestCase):
    def setUp(self):
        self.root = _root
        self.app = CelebiApp(root=self.root)
        self.root.update()

    def tearDown(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.update()

    def _scenario(self, index=0):
        return self.app.scenarios[index]

    def _get_table_data(self, scenario_index=0):
        scenario = self._scenario(scenario_index)
        rows = []
        for item_id in scenario.results_tree.get_children():
            values = scenario.results_tree.item(item_id, "values")
            rows.append((int(values[0]), values[1], values[2]))
        return rows


class TestWidgetCreation(TestAppBase):
    def test_window_title(self):
        self.assertEqual(self.root.title(), "Celebi \u2014 Trench Crusade Dice Probability Calculator")

    def test_pool_size_spinbox_exists(self):
        self.assertIsNotNone(self._scenario().pool_size_spinbox)
        self.assertEqual(float(self._scenario().pool_size_spinbox.cget("from")), 1.0)
        self.assertEqual(float(self._scenario().pool_size_spinbox.cget("to")), 12.0)

    def test_selection_radios_exist(self):
        self.assertIsNotNone(self._scenario().top_radio)
        self.assertIsNotNone(self._scenario().bottom_radio)

    def test_pick_count_spinbox_exists(self):
        self.assertIsNotNone(self._scenario().pick_count_spinbox)
        self.assertIsInstance(self._scenario().pick_count_spinbox, tk.ttk.Spinbox)

    def test_modifier_spinbox_exists(self):
        self.assertIsNotNone(self._scenario().modifier_spinbox)

    def test_threshold_spinbox_exists(self):
        self.assertIsNotNone(self._scenario().threshold_spinbox)

    def test_success_label_exists(self):
        self.assertIsNotNone(self._scenario().success_label)

    def test_failure_label_exists(self):
        self.assertIsNotNone(self._scenario().failure_label)

    def test_results_treeview_exists(self):
        self.assertIsNotNone(self._scenario().results_tree)

    def test_treeview_columns(self):
        columns = self._scenario().results_tree["columns"]
        self.assertEqual(columns, ("total", "exact_pct", "cumulative_pct"))


class TestDefaultState(TestAppBase):
    def test_default_pool_size(self):
        self.assertEqual(self._scenario()._pool_size_var.get(), "2")

    def test_default_selection(self):
        self.assertEqual(self._scenario()._selection_var.get(), "top")

    def test_default_pick_count(self):
        self.assertEqual(self._scenario()._pick_count_var.get(), "2")

    def test_default_modifier(self):
        self.assertEqual(self._scenario()._modifier_var.get(), "0")

    def test_default_threshold(self):
        self.assertEqual(self._scenario()._threshold_var.get(), "7")

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
        self._scenario()._pool_size_var.set("4")
        self.root.update()
        expected = calculate_cumulative_probabilities(
            4, 2, SelectionStrategy.TOP, 0
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_selection_change_updates_results(self):
        self._scenario()._pool_size_var.set("3")
        self.root.update()
        self._scenario()._selection_var.set("bottom")
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
        self._scenario()._pool_size_var.set("4")
        self.root.update()
        self._scenario()._pick_count_var.set("3")
        self.root.update()
        expected = calculate_cumulative_probabilities(
            4, 3, SelectionStrategy.TOP, 0
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_modifier_change_updates_results(self):
        self._scenario()._modifier_var.set("3")
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
        s = self._scenario()
        s._pool_size_var.set("4")
        self.root.update()
        s._selection_var.set("top")
        self.root.update()
        s._pick_count_var.set("2")
        self.root.update()
        s._modifier_var.set("1")
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
        self._scenario()._pool_size_var.set("2")
        self.root.update()
        self._scenario()._pick_count_var.set("2")
        self.root.update()
        rows = self._get_table_data()
        self.assertGreater(len(rows), 0)

    def test_negative_modifier(self):
        self._scenario()._modifier_var.set("-5")
        self.root.update()
        expected = calculate_cumulative_probabilities(
            2, 2, SelectionStrategy.TOP, -5
        )
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_invalid_spinbox_value_no_crash(self):
        self._scenario()._pool_size_var.set("")
        self.root.update()
        rows = self._get_table_data()
        self.assertEqual(len(rows), 0)

    def test_pick_count_constrained_when_pool_too_small(self):
        self._scenario()._pool_size_var.set("1")
        self.root.update()
        self._scenario()._pick_count_var.set("4")
        self.root.update()
        self.assertEqual(self._scenario()._pick_count_var.get(), "1")
        rows = self._get_table_data()
        self.assertGreater(len(rows), 0)

    def test_pick_count_spinbox_max_clamped_to_pool_size(self):
        self._scenario()._pool_size_var.set("3")
        self.root.update()
        self.assertEqual(float(self._scenario().pick_count_spinbox.cget("to")), 3.0)

    def test_pick_count_spinbox_max_capped_at_4(self):
        self._scenario()._pool_size_var.set("8")
        self.root.update()
        self.assertEqual(float(self._scenario().pick_count_spinbox.cget("to")), 4.0)

    def test_pick_count_resets_when_pool_shrinks(self):
        s = self._scenario()
        s._pool_size_var.set("4")
        self.root.update()
        s._pick_count_var.set("3")
        self.root.update()
        s._pool_size_var.set("2")
        self.root.update()
        self.assertEqual(s._pick_count_var.get(), "2")

    def test_pool_1_pick_1(self):
        s = self._scenario()
        s._pool_size_var.set("1")
        self.root.update()
        s._pick_count_var.set("1")
        self.root.update()
        expected = calculate_probabilities(1, 1, SelectionStrategy.TOP, 0)
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))

    def test_pool_12_pick_4(self):
        s = self._scenario()
        s._pool_size_var.set("12")
        self.root.update()
        s._pick_count_var.set("4")
        self.root.update()
        expected = calculate_probabilities(12, 4, SelectionStrategy.TOP, 0)
        rows = self._get_table_data()
        self.assertEqual(len(rows), len(expected))


class TestSuccessFailureDisplay(TestAppBase):
    def test_default_threshold_is_7(self):
        self.assertEqual(self._scenario()._threshold_var.get(), "7")

    def test_default_success_failure_matches_engine(self):
        exact = calculate_probabilities(2, 2, SelectionStrategy.TOP, 0)
        expected_fail, expected_succ = success_failure(exact, 7)
        s = self._scenario()
        self.assertIn(f"{expected_succ * 100:.1f}%", s.success_label.cget("text"))
        self.assertIn(f"{expected_fail * 100:.1f}%", s.failure_label.cget("text"))

    def test_threshold_change_updates_display(self):
        s = self._scenario()
        s._threshold_var.set("10")
        self.root.update()
        exact = calculate_probabilities(2, 2, SelectionStrategy.TOP, 0)
        expected_fail, expected_succ = success_failure(exact, 10)
        self.assertIn(f"{expected_succ * 100:.1f}%", s.success_label.cget("text"))
        self.assertIn(f"{expected_fail * 100:.1f}%", s.failure_label.cget("text"))

    def test_success_failure_updates_on_input_change(self):
        s = self._scenario()
        s._pool_size_var.set("4")
        self.root.update()
        exact = calculate_probabilities(4, 2, SelectionStrategy.TOP, 0)
        expected_fail, expected_succ = success_failure(exact, 7)
        self.assertIn(f"{expected_succ * 100:.1f}%", s.success_label.cget("text"))
        self.assertIn(f"{expected_fail * 100:.1f}%", s.failure_label.cget("text"))


class TestScenarioFrame(unittest.TestCase):
    def setUp(self):
        self.root = _root

    def tearDown(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.update()

    def test_scenario_frame_creation(self):
        frame = ScenarioFrame(self.root)
        self.assertIsInstance(frame, ScenarioFrame)

    def test_scenario_frame_has_config_widgets(self):
        frame = ScenarioFrame(self.root)
        self.assertIsNotNone(frame.pool_size_spinbox)
        self.assertIsNotNone(frame.top_radio)
        self.assertIsNotNone(frame.bottom_radio)
        self.assertIsNotNone(frame.pick_count_spinbox)
        self.assertIsNotNone(frame.modifier_spinbox)
        self.assertIsNotNone(frame.threshold_spinbox)

    def test_scenario_frame_has_results_tree(self):
        frame = ScenarioFrame(self.root)
        self.assertIsNotNone(frame.results_tree)

    def test_scenario_frame_has_success_failure_labels(self):
        frame = ScenarioFrame(self.root)
        self.assertIsNotNone(frame.success_label)
        self.assertIsNotNone(frame.failure_label)

    def test_scenario_frame_default_state(self):
        frame = ScenarioFrame(self.root)
        self.assertEqual(frame._pool_size_var.get(), "2")
        self.assertEqual(frame._selection_var.get(), "top")
        self.assertEqual(frame._pick_count_var.get(), "2")
        self.assertEqual(frame._modifier_var.get(), "0")
        self.assertEqual(frame._threshold_var.get(), "7")

    def test_scenario_frame_updates_results_on_input_change(self):
        frame = ScenarioFrame(self.root)
        frame._pool_size_var.set("4")
        self.root.update()
        rows = []
        for item_id in frame.results_tree.get_children():
            values = frame.results_tree.item(item_id, "values")
            rows.append(int(values[0]))
        expected = calculate_probabilities(4, 2, SelectionStrategy.TOP, 0)
        self.assertEqual(len(rows), len(expected))

    def test_two_scenario_frames_independent(self):
        frame1 = ScenarioFrame(self.root)
        frame2 = ScenarioFrame(self.root)
        frame1._pool_size_var.set("4")
        frame1._pick_count_var.set("3")
        self.root.update()
        self.assertEqual(frame1._pool_size_var.get(), "4")
        self.assertEqual(frame1._pick_count_var.get(), "3")
        self.assertEqual(frame2._pool_size_var.get(), "2")
        self.assertEqual(frame2._pick_count_var.get(), "2")


class TestMultiScenario(TestAppBase):
    def test_app_starts_with_one_scenario(self):
        self.assertEqual(len(self.app.scenarios), 1)

    def test_add_scenario(self):
        self.app.add_scenario()
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 2)

    def test_add_scenario_up_to_four(self):
        for _ in range(3):
            self.app.add_scenario()
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 4)

    def test_cannot_add_beyond_four(self):
        for _ in range(5):
            self.app.add_scenario()
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 4)

    def test_remove_scenario(self):
        self.app.add_scenario()
        self.root.update()
        self.app.remove_scenario(1)
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 1)

    def test_cannot_remove_last_scenario(self):
        self.app.remove_scenario(0)
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 1)

    def test_add_button_hidden_at_four(self):
        for _ in range(3):
            self.app.add_scenario()
        self.root.update()
        self.assertEqual(self.app.add_button.winfo_manager(), "")

    def test_add_button_visible_below_four(self):
        for _ in range(2):
            self.app.add_scenario()
        self.root.update()
        self.assertNotEqual(self.app.add_button.winfo_manager(), "")

    def test_remove_button_hidden_at_one(self):
        self.root.update()
        self.assertEqual(self._scenario().remove_button.winfo_manager(), "")

    def test_remove_button_visible_above_one(self):
        self.app.add_scenario()
        self.root.update()
        self.assertNotEqual(self._scenario(0).remove_button.winfo_manager(), "")
        self.assertNotEqual(self._scenario(1).remove_button.winfo_manager(), "")

    def test_scenarios_independent(self):
        self.app.add_scenario()
        self.root.update()
        self._scenario(0)._pool_size_var.set("6")
        self.root.update()
        self.assertEqual(self._scenario(0)._pool_size_var.get(), "6")
        self.assertEqual(self._scenario(1)._pool_size_var.get(), "2")


class TestMultiScenarioE2E(TestAppBase):
    def test_two_scenarios_different_configs(self):
        self.app.add_scenario()
        self.root.update()
        s0 = self._scenario(0)
        s1 = self._scenario(1)

        s0._pool_size_var.set("3")
        s0._selection_var.set("top")
        s0._pick_count_var.set("2")
        s0._modifier_var.set("0")
        self.root.update()

        s1._pool_size_var.set("4")
        s1._selection_var.set("bottom")
        s1._pick_count_var.set("2")
        s1._modifier_var.set("1")
        self.root.update()

        expected0 = calculate_probabilities(3, 2, SelectionStrategy.TOP, 0)
        expected1 = calculate_probabilities(4, 2, SelectionStrategy.BOTTOM, 1)

        rows0 = self._get_table_data(0)
        rows1 = self._get_table_data(1)

        self.assertEqual(len(rows0), len(expected0))
        self.assertEqual(len(rows1), len(expected1))

        for total, exact_str, _ in rows0:
            self.assertEqual(exact_str, f"{expected0[total] * 100:.1f}%")
        for total, exact_str, _ in rows1:
            self.assertEqual(exact_str, f"{expected1[total] * 100:.1f}%")

    def test_add_remove_add_cycle(self):
        self.app.add_scenario()
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 2)
        self.app.remove_scenario(1)
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 1)
        self.app.add_scenario()
        self.root.update()
        self.assertEqual(len(self.app.scenarios), 2)

    def test_four_scenarios_all_independent(self):
        for _ in range(3):
            self.app.add_scenario()
        self.root.update()

        configs = [
            ("2", "top", "2", "0"),
            ("4", "bottom", "2", "1"),
            ("6", "top", "3", "-2"),
            ("8", "bottom", "4", "3"),
        ]

        for i, (pool, sel, pick, mod) in enumerate(configs):
            s = self._scenario(i)
            s._pool_size_var.set(pool)
            self.root.update()
            s._selection_var.set(sel)
            s._pick_count_var.set(pick)
            s._modifier_var.set(mod)
            self.root.update()

        for i, (pool, sel, pick, mod) in enumerate(configs):
            expected = calculate_probabilities(
                int(pool), int(pick), SelectionStrategy(sel), int(mod)
            )
            rows = self._get_table_data(i)
            self.assertEqual(
                len(rows), len(expected),
                f"Scenario {i} row count mismatch",
            )

    def test_success_failure_per_scenario(self):
        self.app.add_scenario()
        self.root.update()
        s0 = self._scenario(0)
        s1 = self._scenario(1)

        s0._pool_size_var.set("3")
        self.root.update()
        s1._pool_size_var.set("6")
        self.root.update()

        exact0 = calculate_probabilities(3, 2, SelectionStrategy.TOP, 0)
        exact1 = calculate_probabilities(6, 2, SelectionStrategy.TOP, 0)
        _, succ0 = success_failure(exact0, 7)
        _, succ1 = success_failure(exact1, 7)

        self.assertIn(f"{succ0 * 100:.1f}%", s0.success_label.cget("text"))
        self.assertIn(f"{succ1 * 100:.1f}%", s1.success_label.cget("text"))

    def test_large_pool_in_multi_scenario(self):
        self.app.add_scenario()
        self.root.update()
        s0 = self._scenario(0)
        s1 = self._scenario(1)

        s0._pool_size_var.set("2")
        s0._pick_count_var.set("2")
        self.root.update()
        s1._pool_size_var.set("12")
        self.root.update()
        s1._pick_count_var.set("4")
        self.root.update()

        expected0 = calculate_probabilities(2, 2, SelectionStrategy.TOP, 0)
        expected1 = calculate_probabilities(12, 4, SelectionStrategy.TOP, 0)

        rows0 = self._get_table_data(0)
        rows1 = self._get_table_data(1)

        self.assertEqual(len(rows0), len(expected0))
        self.assertEqual(len(rows1), len(expected1))


if __name__ == "__main__":
    unittest.main()
