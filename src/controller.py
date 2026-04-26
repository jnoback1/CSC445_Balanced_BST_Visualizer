from shared_state import (
    state,
    ActiveTreeType,
    set_tree_type,
    set_highlight,
    begin_animation,
)

from trees import avl
from trees import rbtree


def set_active_tree(tree_type: ActiveTreeType) -> None:
    set_tree_type(tree_type)


def _height(node) -> int:
    if node is None:
        return 0
    return 1 + max(_height(node.left), _height(node.right))


def insert_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="insert")

    if state.tree_type == ActiveTreeType.AVL:
        new_root, steps, rot_count = avl.insert(state.avl_root, value)
        state.avl_root = new_root
        state.metrics.avl_rotations += rot_count
        state.metrics.avl_height = new_root.height if new_root is not None else 0
        if steps:
            begin_animation(steps)
        state.touch(f"AVL: inserted {value}")
    else:
        new_root, steps, rot_count = rbtree.insert(state.rb_root, value)
        state.rb_root = new_root
        state.metrics.rb_rotations += rot_count
        state.metrics.rb_height = _height(new_root)
        if steps:
            begin_animation(steps)
        state.touch(f"Red-Black: inserted {value}")


def delete_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="delete")

    if state.tree_type == ActiveTreeType.AVL:
        state.touch("AVL delete: not implemented yet")
    else:
        state.touch("Red-Black delete: not implemented yet")


def search_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="search")

    if state.tree_type == ActiveTreeType.AVL:
        found = avl.search(state.avl_root, value)
        state.touch(f"AVL: search {value} -> {'found' if found else 'not found'}")
    else:
        found = rbtree.search(state.rb_root, value)
        state.touch(f"Red-Black: search {value} -> {'found' if found else 'not found'}")