class Node:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None


def insert(root, value: int):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    return root


def search(root, value: int) -> bool:
    cur = root
    while cur is not None:
        if value == cur.value:
            return True
        cur = cur.left if value < cur.value else cur.right
    return False


def delete(root, value: int):
    if root is None:
        return None

    if value < root.value:
        root.left = delete(root.left, value)
        return root
    if value > root.value:
        root.right = delete(root.right, value)
        return root

    if root.left is None:
        return root.right
    if root.right is None:
        return root.left

    succ_parent = root
    succ = root.right
    while succ.left is not None:
        succ_parent = succ
        succ = succ.left

    root.value = succ.value

    if succ_parent.left == succ:
        succ_parent.left = succ.right
    else:
        succ_parent.right = succ.right

    return root