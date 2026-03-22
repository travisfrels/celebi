import tkinter as tk
from tkinter import ttk

from src.dice_roller import DiceRollResult, calculate_sum, roll_pool, select_dice
from src.theme import apply_theme, detect_system_theme, get_palette
from src.probability_engine import (
    SelectionStrategy,
    calculate_probabilities,
    cumulative_from_exact,
    success_failure,
)


_DIE_SIZE = 36
_DOT_RADIUS = 3

_DOT_POSITIONS = {
    1: [(0.5, 0.5)],
    2: [(0.25, 0.25), (0.75, 0.75)],
    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
    4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
    5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
    6: [
        (0.25, 0.25), (0.75, 0.25),
        (0.25, 0.5), (0.75, 0.5),
        (0.25, 0.75), (0.75, 0.75),
    ],
}


def _draw_die_face(canvas, value, bg, fg):
    """Draw a d6 face with dot pattern on the given canvas."""
    canvas.delete("all")
    size = _DIE_SIZE
    canvas.configure(width=size, height=size)
    canvas.create_rectangle(1, 1, size - 1, size - 1, fill=bg, outline=fg, width=1)
    for px, py in _DOT_POSITIONS.get(value, []):
        cx = px * size
        cy = py * size
        canvas.create_oval(
            cx - _DOT_RADIUS, cy - _DOT_RADIUS,
            cx + _DOT_RADIUS, cy + _DOT_RADIUS,
            fill=fg, outline=fg,
        )


class ScenarioFrame(ttk.Frame):
    def __init__(self, parent, on_remove=None, palette=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._on_remove = on_remove
        self._palette = palette or {}
        self._last_roll = None
        self._die_canvases = []

        self._pool_size_var = tk.StringVar(value="2")
        self._selection_var = tk.StringVar(value="top")
        self._pick_count_var = tk.StringVar(value="2")
        self._modifier_var = tk.StringVar(value="0")
        self._threshold_var = tk.StringVar(value="7")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self._build_config()
        self._build_success_failure()
        self._build_dice_roller()
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

    def _build_dice_roller(self):
        roller_frame = ttk.LabelFrame(self, text="Dice Roller", padding=10)
        roller_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 5))
        roller_frame.columnconfigure(0, weight=1)

        self.roll_button = ttk.Button(
            roller_frame, text="Roll", command=self._do_roll
        )
        self.roll_button.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self._dice_frame = ttk.Frame(roller_frame)
        self._dice_frame.grid(row=1, column=0, sticky="w")

        self.sum_label = ttk.Label(roller_frame, text="")
        self.sum_label.grid(row=2, column=0, sticky="w", pady=(5, 0))

    def _do_roll(self):
        try:
            pool_size = int(self._pool_size_var.get())
            pick_count = int(self._pick_count_var.get())
            modifier = int(self._modifier_var.get())
        except (ValueError, tk.TclError):
            return

        selection = SelectionStrategy(self._selection_var.get())
        pool = roll_pool(pool_size)
        selected, unselected = select_dice(pool, pick_count, selection)
        total = calculate_sum(selected, modifier)

        self._last_roll = DiceRollResult(
            pool=pool,
            selected=selected,
            unselected=unselected,
            modifier=modifier,
            total=total,
        )
        self._render_dice()

    def _render_dice(self):
        for canvas in self._die_canvases:
            canvas.destroy()
        self._die_canvases = []

        if self._last_roll is None:
            self.sum_label.configure(text="")
            return

        roll = self._last_roll
        selected_set = list(roll.selected)
        bg = self._palette.get("bg", "#f0f0f0")
        fg = self._palette.get("fg", "#1a1a1a")
        muted_bg = self._palette.get("trough", "#c8c8c8")
        muted_fg = self._palette.get("border", "#a0a0a0")

        remaining_selected = list(roll.selected)
        for i, value in enumerate(roll.pool):
            is_selected = value in remaining_selected
            if is_selected:
                remaining_selected.remove(value)
                die_bg = bg
                die_fg = fg
            else:
                die_bg = muted_bg
                die_fg = muted_fg

            canvas = tk.Canvas(
                self._dice_frame,
                width=_DIE_SIZE,
                height=_DIE_SIZE,
                highlightthickness=0,
                bg=bg,
            )
            canvas.grid(row=0, column=i, padx=2)
            _draw_die_face(canvas, value, die_bg, die_fg)
            self._die_canvases.append(canvas)

        modifier_str = ""
        if roll.modifier > 0:
            modifier_str = f" + {roll.modifier}"
        elif roll.modifier < 0:
            modifier_str = f" - {abs(roll.modifier)}"
        self.sum_label.configure(text=f"Total: {roll.total}{modifier_str}")

    def _build_results(self):
        results_frame = ttk.LabelFrame(self, text="Probabilities", padding=10)
        results_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=(0, 5))
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
        self.remove_button.grid(row=4, column=0, pady=(0, 5))

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

        theme = detect_system_theme()
        apply_theme(self.root, theme)
        self._palette = get_palette(theme)

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
            self._scenario_container,
            on_remove=self._handle_remove,
            palette=self._palette,
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
