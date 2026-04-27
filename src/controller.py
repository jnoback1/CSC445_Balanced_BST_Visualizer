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

    tree = state.current_tree()
    tree.insert(value)
    
    # Update metrics
    if state.tree_type == ActiveTreeType.AVL:
        state.metrics.avl_rotations = tree.rotation_count
        state.metrics.avl_height = tree.get_height()
        state.touch(f"AVL: inserted {value}")
    else:
        state.metrics.rb_rotations = tree.rotation_count
        state.touch(f"Red-Black: inserted {value}")


def delete_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="delete")

    tree = state.current_tree()
    if tree.search(value):
        tree.delete(value)
        
        # Update metrics
        if state.tree_type == ActiveTreeType.AVL:
            state.metrics.avl_rotations = tree.rotation_count
            state.metrics.avl_height = tree.get_height()
            state.touch(f"AVL: deleted {value}")
        else:
            state.metrics.rb_rotations = tree.rotation_count
            state.touch(f"Red-Black: deleted {value}")
    else:
        state.touch(f"Value {value} not found")


def search_value(value: int) -> None:
    if state.animation.in_progress:
        state.touch("Wait for the animation to finish.")
        return

    set_highlight(value, reason="search")

    tree = state.current_tree()
    found = tree.search(value)
    
    if state.tree_type == ActiveTreeType.AVL:
        state.touch(f"AVL: {'found' if found else 'not found'} {value}")
    else:
        state.touch(f"Red-Black: {'found' if found else 'not found'} {value}")