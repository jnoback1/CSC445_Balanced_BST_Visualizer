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