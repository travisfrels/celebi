import tkinter as tk
from tkinter import ttk

from src.probability_engine import SelectionStrategy, calculate_cumulative_probabilities


class CelebiApp:
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.root.title("Celebi \u2014 Trench Crusade Dice Roller")
        self.root.geometry("600x400")

        self._pool_size_var = tk.StringVar(value="2")
        self._selection_var = tk.StringVar(value="top")
        self._pick_count_var = tk.StringVar(value="2")
        self._modifier_var = tk.StringVar(value="0")

        self._build_ui()
        self._bind_variables()
        self._update_results()

    def _build_ui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._build_config_panel()
        self._build_results_panel()

    def _build_config_panel(self):
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        config_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        row = 0

        ttk.Label(config_frame, text="Pool Size:").grid(
            row=row, column=0, sticky="w", pady=(0, 5)
        )
        row += 1
        self.pool_size_spinbox = ttk.Spinbox(
            config_frame,
            from_=2,
            to=6,
            width=5,
            textvariable=self._pool_size_var,
        )
        self.pool_size_spinbox.grid(row=row, column=0, sticky="w", pady=(0, 10))
        row += 1

        ttk.Label(config_frame, text="Selection:").grid(
            row=row, column=0, sticky="w", pady=(0, 5)
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
        self.bottom_radio.grid(row=row, column=0, sticky="w", pady=(0, 10))
        row += 1

        ttk.Label(config_frame, text="Pick Count:").grid(
            row=row, column=0, sticky="w", pady=(0, 5)
        )
        row += 1
        self.pick2_radio = ttk.Radiobutton(
            config_frame, text="2", variable=self._pick_count_var, value="2"
        )
        self.pick2_radio.grid(row=row, column=0, sticky="w")
        row += 1
        self.pick3_radio = ttk.Radiobutton(
            config_frame, text="3", variable=self._pick_count_var, value="3"
        )
        self.pick3_radio.grid(row=row, column=0, sticky="w", pady=(0, 10))
        row += 1

        ttk.Label(config_frame, text="Modifier:").grid(
            row=row, column=0, sticky="w", pady=(0, 5)
        )
        row += 1
        self.modifier_spinbox = ttk.Spinbox(
            config_frame,
            from_=-20,
            to=20,
            width=5,
            textvariable=self._modifier_var,
        )
        self.modifier_spinbox.grid(row=row, column=0, sticky="w")

    def _build_results_panel(self):
        results_frame = ttk.LabelFrame(
            self.root, text="Cumulative Probabilities", padding=10
        )
        results_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_tree = ttk.Treeview(
            results_frame, columns=("total", "cumulative_pct"), show="headings"
        )
        self.results_tree.heading("total", text="Total")
        self.results_tree.heading("cumulative_pct", text="Cumulative %")
        self.results_tree.column("total", width=80, anchor="center")
        self.results_tree.column("cumulative_pct", width=120, anchor="center")
        self.results_tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_tree.configure(yscrollcommand=scrollbar.set)

    def _bind_variables(self):
        for var in (
            self._pool_size_var,
            self._selection_var,
            self._pick_count_var,
            self._modifier_var,
        ):
            var.trace_add("write", self._on_input_change)

    def _on_input_change(self, *_args):
        self._update_results()

    def _update_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        try:
            pool_size = int(self._pool_size_var.get())
            pick_count = int(self._pick_count_var.get())
            modifier = int(self._modifier_var.get())
        except (ValueError, tk.TclError):
            return

        selection = SelectionStrategy(self._selection_var.get())

        try:
            cumulative = calculate_cumulative_probabilities(
                pool_size, pick_count, selection, modifier
            )
        except ValueError:
            return

        for total, prob in cumulative.items():
            self.results_tree.insert(
                "", "end", values=(total, f"{prob * 100:.1f}%")
            )

    def run(self):
        self.root.mainloop()
