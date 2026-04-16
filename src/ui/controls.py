import tkinter as tk
from tkinter import ttk
import controller
from shared_state import state, ActiveTreeType


class Controls(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)

        self.value_var = tk.StringVar()
        self.tree_var = tk.StringVar(value=state.tree_type.value)

        ttk.Label(self, text="Value:").grid(row=0, column=0, sticky="w")

        self.entry = ttk.Entry(self, textvariable=self.value_var, width=12)
        self.entry.grid(row=0, column=1, padx=(6, 10), sticky="w")
        self.entry.bind("<Return>", lambda _e: self.on_insert())

        self.btn_insert = ttk.Button(self, text="Insert", command=self.on_insert)
        self.btn_delete = ttk.Button(self, text="Delete", command=self.on_delete)
        self.btn_search = ttk.Button(self, text="Search", command=self.on_search)

        self.btn_insert.grid(row=0, column=2, padx=4)
        self.btn_delete.grid(row=0, column=3, padx=4)
        self.btn_search.grid(row=0, column=4, padx=4)

        toggle = ttk.Frame(self)
        toggle.grid(row=0, column=5, padx=(16, 0), sticky="e")

        ttk.Label(toggle, text="Tree:").pack(side="left", padx=(0, 6))

        ttk.Radiobutton(
            toggle,
            text="AVL",
            value=ActiveTreeType.AVL.value,
            variable=self.tree_var,
            command=self.on_toggle_tree,
        ).pack(side="left")

        ttk.Radiobutton(
            toggle,
            text="Red-Black",
            value=ActiveTreeType.RED_BLACK.value,
            variable=self.tree_var,
            command=self.on_toggle_tree,
        ).pack(side="left", padx=(8, 0))

        self.status = ttk.Label(self, text="", foreground="#333")
        self.status.grid(row=1, column=0, columnspan=6, pady=(8, 0), sticky="w")

        self.grid_columnconfigure(5, weight=1)

        self._last_revision = -1
        self.after(50, self._poll_state)

        self.entry.focus_set()

    def _poll_state(self):
        if state.revision != self._last_revision:
            self._last_revision = state.revision
            self.status.config(text=state.status_text)

            disabled = state.animation.in_progress
            new_state = "disabled" if disabled else "normal"
            for btn in (self.btn_insert, self.btn_delete, self.btn_search):
                btn.config(state=new_state)
            self.entry.config(state=new_state)

            self.tree_var.set(state.tree_type.value)

        self.after(50, self._poll_state)

    def _get_int_from_entry(self):
        raw = self.value_var.get().strip()
        if raw == "":
            state.touch("Enter an integer value.")
            return None
        try:
            return int(raw)
        except ValueError:
            state.touch(f"Invalid integer: {raw}")
            return None

    def on_toggle_tree(self):
        controller.set_active_tree(ActiveTreeType(self.tree_var.get()))

    def on_insert(self):
        value = self._get_int_from_entry()
        if value is None:
            return
        controller.insert_value(value)

    def on_delete(self):
        value = self._get_int_from_entry()
        if value is None:
            return
        controller.delete_value(value)

    def on_search(self):
        value = self._get_int_from_entry()
        if value is None:
            return
        controller.search_value(value)