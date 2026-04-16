import tkinter as tk
from tkinter import ttk
from shared_state import state


class TreeCanvas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(
            self,
            background="white",
            highlightthickness=1,
            highlightbackground="#ccc",
        )
        self.canvas.pack(fill="both", expand=True)

        self._last_revision = -1
        self.after(50, self._poll_and_redraw)

    def _poll_and_redraw(self):
        if state.revision != self._last_revision:
            self._last_revision = state.revision
            self.redraw()
        self.after(50, self._poll_and_redraw)

    def redraw(self):
        self.canvas.delete("all")

        w = max(self.canvas.winfo_width(), 1)
        h = max(self.canvas.winfo_height(), 1)

        lines = [
            "Balanced BST Visualizer — UI Blueprint",
            f"Active tree: {state.tree_type.value}",
            f"Status: {state.status_text}",
            "",
            f"Highlight: value={state.highlight.value} reason={state.highlight.reason} color={state.highlight.color}",
            f"Animation: in_progress={state.animation.in_progress} "
            f"step={state.animation.step_index}/{len(state.animation.steps)} "
            f"delay_ms={state.animation.delay_ms}",
        ]

        if state.animation.in_progress and state.animation.steps:
            step = state.animation.steps[state.animation.step_index]
            lines.append(f"Current step label: {step.label}")

        self.canvas.create_text(
            w // 2,
            h // 2,
            text="\n".join(lines),
            fill="#222",
            font=("Arial", 14),
            justify="center",
        )