"""
AVL Tree implementation - Self-balancing binary search tree
Maintains balance factor (height difference) within [-1, 1] at all nodes
"""

from __future__ import annotations
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class AVLNode:
    """Node in an AVL tree"""
    value: int
    left: Optional[AVLNode] = None
    right: Optional[AVLNode] = None
    height: int = 1  # Height of the node (longest path to leaf)

    def balance_factor(self) -> int:
        """Calculate balance factor: height(left) - height(right)"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

    def update_height(self) -> None:
        """Recalculate height based on children"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)


class AVLTree:
    """AVL Tree with automatic balancing"""

    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.rotation_count: int = 0

    def insert(self, value: int) -> None:
        """Insert a value into the AVL tree"""
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: Optional[AVLNode], value: int) -> AVLNode:
        """Recursively insert and rebalance"""
        # Standard BST insertion
        if node is None:
            return AVLNode(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            # Duplicate values - do nothing
            return node

        # Update height and balance
        node.update_height()
        return self._balance(node)

    def delete(self, value: int) -> None:
        """Delete a value from the AVL tree"""
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node: Optional[AVLNode], value: int) -> Optional[AVLNode]:
        """Recursively delete and rebalance"""
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node found - delete it
            # Case 1: No children (leaf)
            if node.left is None and node.right is None:
                return None

            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: Two children - find inorder successor
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)

        # Update height and balance
        if node:
            node.update_height()
            node = self._balance(node)

        return node

    def _find_min(self, node: AVLNode) -> AVLNode:
        """Find node with minimum value"""
        while node.left:
            node = node.left
        return node

    def _balance(self, node: AVLNode) -> AVLNode:
        """Rebalance the tree at this node using rotations"""
        bf = node.balance_factor()

        # Left-heavy cases
        if bf > 1:
            # Check if left child is right-heavy (LR case)
            if node.left and node.left.balance_factor() < 0:
                node.left = self._rotate_left(node.left)
            # Left-Left case
            node = self._rotate_right(node)

        # Right-heavy cases
        elif bf < -1:
            # Check if right child is left-heavy (RL case)
            if node.right and node.right.balance_factor() > 0:
                node.right = self._rotate_right(node.right)
            # Right-Right case
            node = self._rotate_left(node)

        return node

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        r"""
        Left rotation:
            node                  right
           /    \                /    \
          A      right    ->   node    C
               /    \         /    \
              B      C       A      B
        """
        self.rotation_count += 1
        right_child = node.right
        assert right_child is not None

        # Perform rotation
        node.right = right_child.left
        right_child.left = node

        # Update heights
        node.update_height()
        right_child.update_height()

        return right_child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        r"""
        Right rotation:
              node                left
             /    \              /    \
           left    C      ->    A      node
           /    \                    /    \
          A      B                  B      C
        """
        self.rotation_count += 1
        left_child = node.left
        assert left_child is not None

        # Perform rotation
        node.left = left_child.right
        left_child.right = node

        # Update heights
        node.update_height()
        left_child.update_height()

        return left_child

    def search(self, value: int) -> bool:
        """Search for a value in the tree"""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node: Optional[AVLNode], value: int) -> bool:
        """Recursively search for a value"""
        if node is None:
            return False

        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def get_height(self) -> int:
        """Get the height of the tree"""
        return self.root.height if self.root else 0

    def in_order_traverse(self) -> list:
        """Get in-order traversal of tree"""
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node: Optional[AVLNode], result: list) -> None:
        if node:
            self._in_order(node.left, result)
            result.append(node.value)
            self._in_order(node.right, result)
