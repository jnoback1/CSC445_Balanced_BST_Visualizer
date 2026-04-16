from shared_state import (
    state,
    ActiveTreeType,
    set_tree_type,
    set_highlight,
)


def set_active_tree(tree_type: ActiveTreeType) -> None:
    set_tree_type(tree_type)


def insert_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="insert")

    if state.tree_type == ActiveTreeType.AVL:
        state.touch(f"AVL: insert {value} (stub)")
    else:
        state.touch(f"Red-Black: insert {value} (stub)")


def delete_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="delete")

    if state.tree_type == ActiveTreeType.AVL:
        state.touch(f"AVL: delete {value} (stub)")
    else:
        state.touch(f"Red-Black: delete {value} (stub)")


def search_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="search")

    if state.tree_type == ActiveTreeType.AVL:
        state.touch(f"AVL: search {value} (stub)")
    else:
        state.touch(f"Red-Black: search {value} (stub)")