import tkinter as tk
from tkinter import ttk
from ui.controls import Controls
from ui.tree_canvas import TreeCanvas


def main():
    root = tk.Tk()
    root.title("Balanced BST Visualizer")

    try:
        ttk.Style().theme_use("clam")
    except tk.TclError:
        pass

    Controls(root).pack(side="top", fill="x")
    TreeCanvas(root).pack(side="top", fill="both", expand=True)

    root.minsize(900, 500)
    root.mainloop()


if __name__ == "__main__":
    main()