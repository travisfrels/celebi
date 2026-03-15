import tkinter as tk
from tkinter import ttk

from src.probability_engine import (
    SelectionStrategy,
    calculate_probabilities,
    cumulative_from_exact,
    success_failure,
)


class ScenarioFrame(ttk.Frame):
    def __init__(self, parent, on_remove=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._on_remove = on_remove

        self._pool_size_var = tk.StringVar(value="2")
        self._selection_var = tk.StringVar(value="top")
        self._pick_count_var = tk.StringVar(value="2")
        self._modifier_var = tk.StringVar(value="0")
        self._threshold_var = tk.StringVar(value="7")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._build_config()
        self._build_success_failure()
        self._build_results()
        self._build_remove_button()
        self._bind_variables()
        self._update_pick_count_constraint()
        self._update_results()

    def _build_config(self):
        config_frame = ttk.LabelFrame(self, text="Configuration", padding=10)
        config_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        row = 0

        ttk.Label(config_frame, text="Pool Size:").grid(
            row=row, column=0, sticky="w", pady=(0, 2)
        )
        row += 1
        self.pool_size_spinbox = ttk.Spinbox(
            config_frame,
            from_=1,
            to=12,
            width=5,
            textvariable=self._pool_size_var,
        )
        self.pool_size_spinbox.grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1

        ttk.Label(config_frame, text="Selection:").grid(
            row=row, column=0, sticky="w", pady=(0, 2)
        )
        row += 1
        self.top_radio = ttk.Radiobutton(
            config_frame, text="Top", variable=self._selection_var, value="top"
        )
        self.top_radio.grid(row=row, column=0, sticky="w")
        row += 1
        self.bottom_radio = ttk.Radiobutton(
            config_frame, text="Bottom", variable=self._selection_var, value="bottom"
        )
        self.bottom_radio.grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1

        ttk.Label(config_frame, text="Pick Count:").grid(
            row=row, column=0, sticky="w", pady=(0, 2)
        )
        row += 1
        self.pick_count_spinbox = ttk.Spinbox(
            config_frame,
            from_=1,
            to=4,
            width=5,
            textvariable=self._pick_count_var,
        )
        self.pick_count_spinbox.grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1

        ttk.Label(config_frame, text="Modifier:").grid(
            row=row, column=0, sticky="w", pady=(0, 2)
        )
        row += 1
        self.modifier_spinbox = ttk.Spinbox(
            config_frame,
            from_=-20,
            to=20,
            width=5,
            textvariable=self._modifier_var,
        )
        self.modifier_spinbox.grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1

        ttk.Label(config_frame, text="Threshold:").grid(
            row=row, column=0, sticky="w", pady=(0, 2)
        )
        row += 1
        self.threshold_spinbox = ttk.Spinbox(
            config_frame,
            from_=2,
            to=24,
            width=5,
            textvariable=self._threshold_var,
        )
        self.threshold_spinbox.grid(row=row, column=0, sticky="w")

    def _build_success_failure(self):
        sf_frame = ttk.LabelFrame(self, text="Summary", padding=10)
        sf_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.success_label = ttk.Label(sf_frame, text="Success: —")
        self.success_label.grid(row=0, column=0, sticky="w")

        self.failure_label = ttk.Label(sf_frame, text="Failure: —")
        self.failure_label.grid(row=1, column=0, sticky="w")

    def _build_results(self):
        results_frame = ttk.LabelFrame(self, text="Probabilities", padding=10)
        results_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 5))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_tree = ttk.Treeview(
            results_frame,
            columns=("total", "exact_pct", "cumulative_pct"),
            show="headings",
        )
        self.results_tree.heading("total", text="Total")
        self.results_tree.heading("exact_pct", text="Exact %")
        self.results_tree.heading("cumulative_pct", text="Cumulative %")
        self.results_tree.column("total", width=50, anchor="center")
        self.results_tree.column("exact_pct", width=70, anchor="center")
        self.results_tree.column("cumulative_pct", width=90, anchor="center")
        self.results_tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_tree.configure(yscrollcommand=scrollbar.set)

    def _build_remove_button(self):
        self.remove_button = ttk.Button(
            self, text="Remove", command=self._request_remove
        )

    def _request_remove(self):
        if self._on_remove:
            self._on_remove(self)

    def show_remove_button(self):
        self.remove_button.grid(row=3, column=0, pady=(0, 5))

    def hide_remove_button(self):
        self.remove_button.grid_remove()

    def _bind_variables(self):
        for var in (
            self._pool_size_var,
            self._selection_var,
            self._pick_count_var,
            self._modifier_var,
            self._threshold_var,
        ):
            var.trace_add("write", self._on_input_change)

    def _on_input_change(self, *_args):
        self._update_pick_count_constraint()
        self._update_results()

    def _update_pick_count_constraint(self):
        try:
            pool_size = int(self._pool_size_var.get())
        except (ValueError, tk.TclError):
            return

        max_pick = min(4, pool_size)
        self.pick_count_spinbox.configure(to=max_pick)

        try:
            pick_count = int(self._pick_count_var.get())
        except (ValueError, tk.TclError):
            return

        if pick_count > max_pick:
            self._pick_count_var.set(str(max_pick))

    def _update_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        try:
            pool_size = int(self._pool_size_var.get())
            pick_count = int(self._pick_count_var.get())
            modifier = int(self._modifier_var.get())
            threshold = int(self._threshold_var.get())
        except (ValueError, tk.TclError):
            self.success_label.configure(text="Success: —")
            self.failure_label.configure(text="Failure: —")
            return

        selection = SelectionStrategy(self._selection_var.get())

        try:
            exact = calculate_probabilities(
                pool_size, pick_count, selection, modifier
            )
            cumulative = cumulative_from_exact(exact)
        except ValueError:
            self.success_label.configure(text="Success: —")
            self.failure_label.configure(text="Failure: —")
            return

        fail_prob, succ_prob = success_failure(exact, threshold)
        self.success_label.configure(
            text=f"Success (\u2265{threshold}): {succ_prob * 100:.1f}%"
        )
        self.failure_label.configure(
            text=f"Failure (<{threshold}): {fail_prob * 100:.1f}%"
        )

        for total in sorted(exact.keys()):
            self.results_tree.insert(
                "",
                "end",
                values=(
                    total,
                    f"{exact[total] * 100:.1f}%",
                    f"{cumulative[total] * 100:.1f}%",
                ),
            )


class CelebiApp:
    MAX_SCENARIOS = 4

    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.root.title("Celebi \u2014 Trench Crusade Dice Probability Calculator")
        self.root.geometry("1200x600")
        self.root.minsize(400, 400)

        self.scenarios = []
        self._build_ui()
        self.add_scenario()

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._scenario_container = ttk.Frame(self.root)
        self._scenario_container.grid(row=0, column=0, sticky="nsew")
        self._scenario_container.rowconfigure(0, weight=1)

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=5)

        self.add_button = ttk.Button(
            button_frame, text="Add Scenario", command=self.add_scenario
        )
        self.add_button.pack()

    def add_scenario(self):
        if len(self.scenarios) >= self.MAX_SCENARIOS:
            return

        scenario = ScenarioFrame(
            self._scenario_container, on_remove=self._handle_remove
        )
        self.scenarios.append(scenario)
        self._relayout_scenarios()

    def remove_scenario(self, index):
        if len(self.scenarios) <= 1:
            return

        scenario = self.scenarios.pop(index)
        scenario.destroy()
        self._relayout_scenarios()

    def _handle_remove(self, scenario):
        if scenario in self.scenarios:
            index = self.scenarios.index(scenario)
            self.remove_scenario(index)

    def _relayout_scenarios(self):
        for i, scenario in enumerate(self.scenarios):
            self._scenario_container.columnconfigure(i, weight=1)
            scenario.grid(row=0, column=i, sticky="nsew", padx=2)

        for i in range(len(self.scenarios), self.MAX_SCENARIOS):
            self._scenario_container.columnconfigure(i, weight=0)

        if len(self.scenarios) >= self.MAX_SCENARIOS:
            self.add_button.pack_forget()
        else:
            self.add_button.pack()

        show_remove = len(self.scenarios) > 1
        for scenario in self.scenarios:
            if show_remove:
                scenario.show_remove_button()
            else:
                scenario.hide_remove_button()

    def run(self):
        self.root.mainloop()
