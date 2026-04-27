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

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Draw basic info at top
        info_lines = [
            f"Tree: {state.tree_type.value}",
            f"Status: {state.status_text}",
        ]
        
        tree = state.current_tree()
        if state.tree_type.value == "AVL":
            info_lines.append(f"Height: {tree.get_height()} | Rotations: {state.metrics.avl_rotations}")
        else:
            info_lines.append(f"Rotations: {state.metrics.rb_rotations}")

        info_text = " | ".join(info_lines)
        self.canvas.create_text(
            10, 20,
            text=info_text,
            fill="#222",
            font=("Arial", 10),
            anchor="nw"
        )

        # Draw the tree visualization
        root = state.current_root()
        if root:
            self._draw_tree(root, w // 2, 60, w // 4)
        else:
            self.canvas.create_text(
                w // 2, h // 2,
                text="Tree is empty. Insert values to begin.",
                fill="#999",
                font=("Arial", 12)
            )

    def _draw_tree(self, node, x, y, offset):
        """Recursively draw the tree nodes and edges"""
        if node is None:
            return

        # Determine node color based on tree type and highlight
        node_color = "lightblue"
        
        if state.tree_type.value == "RED_BLACK":
            # For Red-Black trees, use the node's actual color
            from red_black_tree import Color
            node_color = "#ff6b6b" if node.color == Color.RED else "#333333"
            text_color = "white"
        else:
            text_color = "black"

        # Highlight the searched/inserted/deleted node
        if state.highlight.value == node.value:
            node_color = state.highlight.color

        # Draw edges to children
        if hasattr(node, 'left') and node.left:
            self.canvas.create_line(x, y, x - offset, y + 60, fill="#ccc", width=2)
            self._draw_tree(node.left, x - offset, y + 60, offset // 2)

        if hasattr(node, 'right') and node.right:
            self.canvas.create_line(x, y, x + offset, y + 60, fill="#ccc", width=2)
            self._draw_tree(node.right, x + offset, y + 60, offset // 2)

        # Draw the node
        self.canvas.create_oval(
            x - 20, y - 20, x + 20, y + 20,
            fill=node_color, outline="black", width=2
        )
        
        # Draw the value
        self.canvas.create_text(
            x, y,
            text=str(node.value),
            fill=text_color,
            font=("Arial", 10, "bold")
        )