from shared_state import RotationStep


class AVLNode:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def _h(n):
    return n.height if n is not None else 0


def _update(n):
    n.height = 1 + max(_h(n.left), _h(n.right))


def _bf(n):
    return _h(n.left) - _h(n.right)


def clone_tree(node):
    if node is None:
        return None
    c = AVLNode(node.value)
    c.height = node.height
    c.left = clone_tree(node.left)
    c.right = clone_tree(node.right)
    return c


def _rotate_right(y):
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    _update(y)
    _update(x)
    return x


def _rotate_left(x):
    y = x.right
    t2 = y.left
    y.left = x
    x.right = t2
    _update(x)
    _update(y)
    return y


def insert(root, value: int):
    steps = []
    rotation_count = 0

    def rec(node):
        nonlocal rotation_count
        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = rec(node.left)
        elif value > node.value:
            node.right = rec(node.right)
        else:
            return node

        _update(node)
        balance = _bf(node)

        if balance > 1 and value < node.left.value:
            rotation_count += 1
            steps.append(RotationStep("Right Rotation (LL)", snapshot_root=clone_tree(node)))
            node = _rotate_right(node)
            steps.append(RotationStep("After Right Rotation (LL)", snapshot_root=clone_tree(node)))
            return node

        if balance < -1 and value > node.right.value:
            rotation_count += 1
            steps.append(RotationStep("Left Rotation (RR)", snapshot_root=clone_tree(node)))
            node = _rotate_left(node)
            steps.append(RotationStep("After Left Rotation (RR)", snapshot_root=clone_tree(node)))
            return node

        if balance > 1 and value > node.left.value:
            rotation_count += 1
            steps.append(RotationStep("Left Rotation (LR step 1)", snapshot_root=clone_tree(node)))
            node.left = _rotate_left(node.left)
            steps.append(RotationStep("After LR step 1", snapshot_root=clone_tree(node)))
            rotation_count += 1
            steps.append(RotationStep("Right Rotation (LR step 2)", snapshot_root=clone_tree(node)))
            node = _rotate_right(node)
            steps.append(RotationStep("After LR step 2", snapshot_root=clone_tree(node)))
            return node

        if balance < -1 and value < node.right.value:
            rotation_count += 1
            steps.append(RotationStep("Right Rotation (RL step 1)", snapshot_root=clone_tree(node)))
            node.right = _rotate_right(node.right)
            steps.append(RotationStep("After RL step 1", snapshot_root=clone_tree(node)))
            rotation_count += 1
            steps.append(RotationStep("Left Rotation (RL step 2)", snapshot_root=clone_tree(node)))
            node = _rotate_left(node)
            steps.append(RotationStep("After RL step 2", snapshot_root=clone_tree(node)))
            return node

        return node

    new_root = rec(root)
    steps.insert(0, RotationStep(f"Inserted {value}", snapshot_root=clone_tree(new_root)))
    steps.append(RotationStep("Done", snapshot_root=clone_tree(new_root)))
    return new_root, steps, rotation_count


def search(root, value: int) -> bool:
    cur = root
    while cur is not None:
        if value == cur.value:
            return True
        cur = cur.left if value < cur.value else cur.right
    return False


def delete(root, value: int):
    steps = []
    rotation_count = 0

    def _min_value_node(n: AVLNode) -> AVLNode:
        cur = n
        while cur.left is not None:
            cur = cur.left
        return cur

    def _delete_exact(node, exact_value: int):
        if node is None:
            return None
        if exact_value < node.value:
            node.left = _delete_exact(node.left, exact_value)
        elif exact_value > node.value:
            node.right = _delete_exact(node.right, exact_value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = _min_value_node(node.right)
            node.value = succ.value
            node.right = _delete_exact(node.right, succ.value)

        if node is None:
            return None

        _update(node)
        balance = _bf(node)

        if balance > 1:
            if _bf(node.left) >= 0:
                return _rotate_right(node)
            node.left = _rotate_left(node.left)
            return _rotate_right(node)

        if balance < -1:
            if _bf(node.right) <= 0:
                return _rotate_left(node)
            node.right = _rotate_right(node.right)
            return _rotate_left(node)

        return node

    def rec(node):
        nonlocal rotation_count
        if node is None:
            return None

        if value < node.value:
            node.left = rec(node.left)
        elif value > node.value:
            node.right = rec(node.right)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = _min_value_node(node.right)
            node.value = succ.value
            node.right = _delete_exact(node.right, succ.value)

        if node is None:
            return None

        _update(node)
        balance = _bf(node)

        if balance > 1:
            left_bf = _bf(node.left)
            if left_bf >= 0:
                rotation_count += 1
                steps.append(RotationStep("Right Rotation (LL)", snapshot_root=clone_tree(node)))
                node = _rotate_right(node)
                steps.append(RotationStep("After Right Rotation (LL)", snapshot_root=clone_tree(node)))
                return node
            rotation_count += 1
            steps.append(RotationStep("Left Rotation (LR step 1)", snapshot_root=clone_tree(node)))
            node.left = _rotate_left(node.left)
            steps.append(RotationStep("After LR step 1", snapshot_root=clone_tree(node)))
            rotation_count += 1
            steps.append(RotationStep("Right Rotation (LR step 2)", snapshot_root=clone_tree(node)))
            node = _rotate_right(node)
            steps.append(RotationStep("After LR step 2", snapshot_root=clone_tree(node)))
            return node

        if balance < -1:
            right_bf = _bf(node.right)
            if right_bf <= 0:
                rotation_count += 1
                steps.append(RotationStep("Left Rotation (RR)", snapshot_root=clone_tree(node)))
                node = _rotate_left(node)
                steps.append(RotationStep("After Left Rotation (RR)", snapshot_root=clone_tree(node)))
                return node
            rotation_count += 1
            steps.append(RotationStep("Right Rotation (RL step 1)", snapshot_root=clone_tree(node)))
            node.right = _rotate_right(node.right)
            steps.append(RotationStep("After RL step 1", snapshot_root=clone_tree(node)))
            rotation_count += 1
            steps.append(RotationStep("Left Rotation (RL step 2)", snapshot_root=clone_tree(node)))
            node = _rotate_left(node)
            steps.append(RotationStep("After RL step 2", snapshot_root=clone_tree(node)))
            return node

        return node

    new_root = rec(root)
    steps.insert(0, RotationStep(f"Delete {value}", snapshot_root=clone_tree(new_root)))
    steps.append(RotationStep("Done", snapshot_root=clone_tree(new_root)))
    return new_root, steps, rotation_count