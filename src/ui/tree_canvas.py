import tkinter as tk
from tkinter import ttk
from shared_state import state, current_display_root


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
        self.zoom = 1.0
        self.zoom_min = 0.4
        self.zoom_max = 2.5

        self._last_revision = -1
        self.after(50, self._poll_and_redraw)

    def _poll_and_redraw(self):
        if state.revision != self._last_revision:
            self._last_revision = state.revision
            self.redraw()
        self.after(50, self._poll_and_redraw)

    def _h(self, n):
        if n is None:
            return 0
        if hasattr(n, "height"):
            return n.height
        return 1 + max(self._h(n.left), self._h(n.right))

    def redraw(self):
        self.canvas.delete("all")

        w = max(self.canvas.winfo_width(), 1)

        if state.animation.in_progress and state.animation.steps:
            step = state.animation.steps[state.animation.step_index]
            self.canvas.create_text(
                12, 12,
                anchor="nw",
                text=step.label,
                fill="#111",
                font=("Arial", 14, "bold"),
            )

        self.canvas.create_text(
            12, 36,
            anchor="nw",
            text=f"AVL height: {state.metrics.avl_height} | RB height: {state.metrics.rb_height} | "
                 f"AVL rotations: {state.metrics.avl_rotations} | RB rotations: {state.metrics.rb_rotations}",
            fill="#333",
            font=("Arial", 11),
        )

        root = current_display_root()
        if root is None:
            self.canvas.create_text(
                w // 2,
                100,
                text=f"{state.tree_type.value} tree is empty",
                fill="#222",
                font=("Arial", 16),
            )
            return

        z = self.zoom
        start_x = w // 2
        start_y = int(110 * z)
        dx = max(w * 0.25 * z, 60 * z)
        level_gap = int(90 * z)

        self._draw_node(root, start_x, start_y, dx, level_gap)

    def _node_fill(self, node):
        if node.value == state.highlight.value:
            return state.highlight.color

        if hasattr(node, "color"):
            if node.color == "red":
                return "#ffb3b3"
            return "#e6e6e6"

        return "white"

    def _draw_node(self, node, x, y, dx, level_gap):
        if node is None:
            return

        r = int(20 * self.zoom)
        fill = self._node_fill(node)

        if node.left is not None:
            x2, y2 = x - dx, y + level_gap
            self.canvas.create_line(x, y, x2, y2, fill="#666", width=2)
            self._draw_node(node.left, x2, y2, dx * 0.6, level_gap)

        if node.right is not None:
            x2, y2 = x + dx, y + level_gap
            self.canvas.create_line(x, y, x2, y2, fill="#666", width=2)
            self._draw_node(node.right, x2, y2, dx * 0.6, level_gap)

        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline="#222", width=2)
        self.canvas.create_text(x, y, text=str(node.value), fill="#111", font=("Arial", 12, "bold"))

        if hasattr(node, "height"):
            bf = self._h(node.left) - self._h(node.right)
            self.canvas.create_text(
                x, y + r + int(12 * self.zoom),
                text=f"h={node.height} bf={bf}",
                fill="#333",
                font=("Arial", 10),
            )

        if hasattr(node, "color"):
            self.canvas.create_text(
                x, y + r + int(12 * self.zoom),
                text=node.color,
                fill="#333",
                font=("Arial", 10),
            )
    
    def zoom_in(self):
        self.zoom = min(self.zoom * 1.15, self.zoom_max)
        state.touch()

    def zoom_out(self):
        self.zoom = max(self.zoom / 1.15, self.zoom_min)
        state.touch()

    def reset_zoom(self):
        self.zoom = 1.0
        state.touch()