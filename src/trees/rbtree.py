from shared_state import RotationStep


RED = "red"
BLACK = "black"


class RBNode:
    def __init__(self, value: int, color: str = RED):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


def _color(n):
    return n.color if n is not None else BLACK


def clone_tree(node, parent=None):
    if node is None:
        return None
    c = RBNode(node.value, node.color)
    c.parent = parent
    c.left = clone_tree(node.left, c)
    c.right = clone_tree(node.right, c)
    return c


def _rotate_left(root, x):
    y = x.right
    x.right = y.left
    if y.left is not None:
        y.left.parent = x

    y.parent = x.parent
    if x.parent is None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y

    y.left = x
    x.parent = y
    return root


def _rotate_right(root, y):
    x = y.left
    y.left = x.right
    if x.right is not None:
        x.right.parent = y

    x.parent = y.parent
    if y.parent is None:
        root = x
    elif y == y.parent.left:
        y.parent.left = x
    else:
        y.parent.right = x

    x.right = y
    y.parent = x
    return root


def _bst_insert(root, z):
    y = None
    x = root
    while x is not None:
        y = x
        if z.value < x.value:
            x = x.left
        elif z.value > x.value:
            x = x.right
        else:
            return root, None

    z.parent = y
    if y is None:
        root = z
    elif z.value < y.value:
        y.left = z
    else:
        y.right = z
    return root, z


def insert(root, value: int):
    steps = []
    rotation_count = 0

    z = RBNode(value, RED)
    root, inserted = _bst_insert(root, z)
    if inserted is None:
        steps.append(RotationStep(f"Value {value} already exists", snapshot_root=clone_tree(root)))
        return root, steps, 0

    steps.append(RotationStep(f"Inserted {value} (red)", snapshot_root=clone_tree(root)))

    while inserted.parent is not None and inserted.parent.color == RED:
        p = inserted.parent
        g = p.parent
        if g is None:
            break

        if p == g.left:
            u = g.right
            if _color(u) == RED:
                steps.append(RotationStep("Recolor (parent+uncle red)", snapshot_root=clone_tree(root)))
                p.color = BLACK
                u.color = BLACK
                g.color = RED
                inserted = g
                continue

            if inserted == p.right:
                steps.append(RotationStep("Left Rotation (prepare)", snapshot_root=clone_tree(root)))
                root = _rotate_left(root, p)
                rotation_count += 1
                inserted = p
                p = inserted.parent
                g = p.parent

            steps.append(RotationStep("Right Rotation", snapshot_root=clone_tree(root)))
            p.color = BLACK
            g.color = RED
            root = _rotate_right(root, g)
            rotation_count += 1

        else:
            u = g.left
            if _color(u) == RED:
                steps.append(RotationStep("Recolor (parent+uncle red)", snapshot_root=clone_tree(root)))
                p.color = BLACK
                u.color = BLACK
                g.color = RED
                inserted = g
                continue

            if inserted == p.left:
                steps.append(RotationStep("Right Rotation (prepare)", snapshot_root=clone_tree(root)))
                root = _rotate_right(root, p)
                rotation_count += 1
                inserted = p
                p = inserted.parent
                g = p.parent

            steps.append(RotationStep("Left Rotation", snapshot_root=clone_tree(root)))
            p.color = BLACK
            g.color = RED
            root = _rotate_left(root, g)
            rotation_count += 1

        break

    if root is not None:
        root.color = BLACK

    steps.append(RotationStep("Done", snapshot_root=clone_tree(root)))
    return root, steps, rotation_count


def search(root, value: int) -> bool:
    cur = root
    while cur is not None:
        if value == cur.value:
            return True
        cur = cur.left if value < cur.value else cur.right
    return False


def _minimum(x: RBNode) -> RBNode:
    cur = x
    while cur.left is not None:
        cur = cur.left
    return cur


def _transplant(root, u: RBNode, v):
    if u.parent is None:
        root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v
    if v is not None:
        v.parent = u.parent
    return root


def _delete_fixup(root, x, parent):
    steps = []
    rotation_count = 0

    def set_color(n, c):
        if n is not None:
            n.color = c

    while (x != root) and (_color(x) == BLACK):
        if parent is None:
            break

        if x == parent.left:
            w = parent.right
            if w is None:
                x = parent
                parent = x.parent
                continue

            if _color(w) == RED:
                steps.append(RotationStep("Fixup: Case 1 (sibling red)", snapshot_root=clone_tree(root)))
                set_color(w, BLACK)
                set_color(parent, RED)
                root = _rotate_left(root, parent)
                rotation_count += 1
                w = parent.right
                if w is None:
                    x = parent
                    parent = x.parent
                    continue

            if _color(w.left) == BLACK and _color(w.right) == BLACK:
                steps.append(RotationStep("Fixup: Case 2", snapshot_root=clone_tree(root)))
                set_color(w, RED)
                x = parent
                parent = x.parent
            else:
                if _color(w.right) == BLACK:
                    steps.append(RotationStep("Fixup: Case 3", snapshot_root=clone_tree(root)))
                    set_color(w.left, BLACK)
                    set_color(w, RED)
                    root = _rotate_right(root, w)
                    rotation_count += 1
                    w = parent.right
                    if w is None:
                        x = parent
                        parent = x.parent
                        continue

                steps.append(RotationStep("Fixup: Case 4", snapshot_root=clone_tree(root)))
                set_color(w, parent.color)
                set_color(parent, BLACK)
                set_color(w.right, BLACK)
                root = _rotate_left(root, parent)
                rotation_count += 1
                x = root
                parent = None
        else:
            w = parent.left
            if w is None:
                x = parent
                parent = x.parent
                continue

            if _color(w) == RED:
                steps.append(RotationStep("Fixup: Case 1 (mirror)", snapshot_root=clone_tree(root)))
                set_color(w, BLACK)
                set_color(parent, RED)
                root = _rotate_right(root, parent)
                rotation_count += 1
                w = parent.left
                if w is None:
                    x = parent
                    parent = x.parent
                    continue

            if _color(w.left) == BLACK and _color(w.right) == BLACK:
                steps.append(RotationStep("Fixup: Case 2 (mirror)", snapshot_root=clone_tree(root)))
                set_color(w, RED)
                x = parent
                parent = x.parent
            else:
                if _color(w.left) == BLACK:
                    steps.append(RotationStep("Fixup: Case 3 (mirror)", snapshot_root=clone_tree(root)))
                    set_color(w.right, BLACK)
                    set_color(w, RED)
                    root = _rotate_left(root, w)
                    rotation_count += 1
                    w = parent.left
                    if w is None:
                        x = parent
                        parent = x.parent
                        continue

                steps.append(RotationStep("Fixup: Case 4 (mirror)", snapshot_root=clone_tree(root)))
                set_color(w, parent.color)
                set_color(parent, BLACK)
                set_color(w.left, BLACK)
                root = _rotate_right(root, parent)
                rotation_count += 1
                x = root
                parent = None

    if x is not None:
        x.color = BLACK

    steps.append(RotationStep("Fixup complete", snapshot_root=clone_tree(root)))
    return root, steps, rotation_count

def delete(root, value: int):
    steps = []
    rotation_count = 0

    z = root
    while z is not None and z.value != value:
        z = z.left if value < z.value else z.right

    if z is None:
        steps.append(RotationStep(f"Delete {value} (not found)", snapshot_root=clone_tree(root)))
        return root, steps, 0

    steps.append(RotationStep(f"Delete {value}", snapshot_root=clone_tree(root)))

    y = z
    y_original_color = y.color
    x = None
    x_parent = None

    if z.left is None:
        x = z.right
        x_parent = z.parent
        root = _transplant(root, z, z.right)
    elif z.right is None:
        x = z.left
        x_parent = z.parent
        root = _transplant(root, z, z.left)
    else:
        y = _minimum(z.right)
        y_original_color = y.color
        x = y.right
        if y.parent == z:
            x_parent = y
        else:
            x_parent = y.parent
            root = _transplant(root, y, y.right)
            y.right = z.right
            y.right.parent = y

        root = _transplant(root, z, y)
        y.left = z.left
        y.left.parent = y
        y.color = z.color

    steps.append(RotationStep("After BST removal", snapshot_root=clone_tree(root)))

    if y_original_color == BLACK:
        root, fix_steps, fix_rots = _delete_fixup(root, x, x_parent)
        steps.extend(fix_steps)
        rotation_count += fix_rots

    if root is not None:
        root.color = BLACK

    steps.append(RotationStep("Done", snapshot_root=clone_tree(root)))
    return root, steps, rotation_count