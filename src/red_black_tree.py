"""
Red-Black Tree implementation - Self-balancing binary search tree
Maintains color properties to ensure O(log n) operations
"""

from __future__ import annotations
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class Color(Enum):
    """Node color in Red-Black tree"""
    RED = "RED"
    BLACK = "BLACK"


@dataclass
class RBNode:
    """Node in a Red-Black tree"""
    value: int
    color: Color = Color.RED
    left: Optional[RBNode] = None
    right: Optional[RBNode] = None
    parent: Optional[RBNode] = None

    def uncle(self) -> Optional[RBNode]:
        """Get the node's uncle (parent's sibling)"""
        if not self.parent or not self.parent.parent:
            return None
        if self.parent == self.parent.parent.left:
            return self.parent.parent.right
        else:
            return self.parent.parent.left

    def sibling(self) -> Optional[RBNode]:
        """Get the node's sibling"""
        if not self.parent:
            return None
        if self == self.parent.left:
            return self.parent.right
        else:
            return self.parent.left


class RedBlackTree:
    """Red-Black Tree with automatic balancing"""

    def __init__(self):
        self.root: Optional[RBNode] = None
        self.rotation_count: int = 0

    def insert(self, value: int) -> None:
        """Insert a value into the Red-Black tree"""
        if self.root is None:
            self.root = RBNode(value, Color.BLACK)
            return

        # Find insertion point
        node = self._insert_bst(self.root, value)
        if node:
            self._fix_insert(node)

    def _insert_bst(self, node: RBNode, value: int) -> Optional[RBNode]:
        """Standard BST insertion, returns the newly inserted node"""
        if value == node.value:
            return None  # Duplicate

        if value < node.value:
            if node.left is None:
                node.left = RBNode(value, Color.RED, parent=node)
                return node.left
            else:
                return self._insert_bst(node.left, value)
        else:
            if node.right is None:
                node.right = RBNode(value, Color.RED, parent=node)
                return node.right
            else:
                return self._insert_bst(node.right, value)

    def _fix_insert(self, node: RBNode) -> None:
        """Fix Red-Black properties after insertion"""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                if uncle and uncle.color == Color.RED:
                    # Case 1: Uncle is red - recolor
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    # Uncle is black
                    if node == node.parent.right:
                        # Case 2: Node is right child - left rotate
                        node = node.parent
                        self._rotate_left(node)

                    # Case 3: Node is left child - right rotate and recolor
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left

                if uncle and uncle.color == Color.RED:
                    # Case 1: Uncle is red - recolor
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    # Uncle is black
                    if node == node.parent.left:
                        # Case 2: Node is left child - right rotate
                        node = node.parent
                        self._rotate_right(node)

                    # Case 3: Node is right child - left rotate and recolor
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._rotate_left(node.parent.parent)

        self.root.color = Color.BLACK

    def delete(self, value: int) -> None:
        """Delete a value from the Red-Black tree"""
        node = self._find_node(self.root, value)
        if node:
            self._delete_node(node)

    def _find_node(self, node: Optional[RBNode], value: int) -> Optional[RBNode]:
        """Find a node with the given value"""
        if node is None:
            return None
        if value == node.value:
            return node
        elif value < node.value:
            return self._find_node(node.left, value)
        else:
            return self._find_node(node.right, value)

    def _delete_node(self, node: RBNode) -> None:
        """Delete a node from the tree"""
        # If node has two children, replace with inorder successor
        if node.left and node.right:
            successor = self._find_min(node.right)
            node.value = successor.value
            node = successor

        # Node has at most one child
        child = node.right if node.right else node.left

        if node.color == Color.RED:
            # If node is red, simply remove it
            if node.parent:
                if node == node.parent.left:
                    node.parent.left = child
                else:
                    node.parent.right = child
                if child:
                    child.parent = node.parent
            else:
                self.root = child
        else:
            # Node is black
            if child:
                child.color = Color.BLACK
                if node.parent:
                    if node == node.parent.left:
                        node.parent.left = child
                    else:
                        node.parent.right = child
                    child.parent = node.parent
                else:
                    self.root = child
            else:
                # Node is black with no children
                if node.parent:
                    self._fix_delete(node)
                    if node == node.parent.left:
                        node.parent.left = None
                    else:
                        node.parent.right = None
                else:
                    self.root = None

    def _fix_delete(self, node: RBNode) -> None:
        """Fix Red-Black properties after deletion"""
        while node != self.root and self._is_black(node):
            if node == node.parent.left:
                sibling = node.parent.right

                if sibling and sibling.color == Color.RED:
                    # Case 1: Sibling is red
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._rotate_left(node.parent)
                    sibling = node.parent.right

                if (
                    sibling
                    and self._is_black(sibling.left)
                    and self._is_black(sibling.right)
                ):
                    # Case 2: Sibling and its children are black
                    if sibling:
                        sibling.color = Color.RED
                    node = node.parent
                elif sibling:
                    if self._is_black(sibling.right):
                        # Case 3: Sibling's right child is black
                        if sibling.left:
                            sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._rotate_right(sibling)
                        sibling = node.parent.right

                    # Case 4: Sibling's right child is red
                    if sibling:
                        sibling.color = node.parent.color
                        node.parent.color = Color.BLACK
                        if sibling.right:
                            sibling.right.color = Color.BLACK
                        self._rotate_left(node.parent)
                    break
            else:
                sibling = node.parent.left

                if sibling and sibling.color == Color.RED:
                    # Case 1: Sibling is red
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._rotate_right(node.parent)
                    sibling = node.parent.left

                if (
                    sibling
                    and self._is_black(sibling.right)
                    and self._is_black(sibling.left)
                ):
                    # Case 2: Sibling and its children are black
                    if sibling:
                        sibling.color = Color.RED
                    node = node.parent
                elif sibling:
                    if self._is_black(sibling.left):
                        # Case 3: Sibling's left child is black
                        if sibling.right:
                            sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self._rotate_left(sibling)
                        sibling = node.parent.left

                    # Case 4: Sibling's left child is red
                    if sibling:
                        sibling.color = node.parent.color
                        node.parent.color = Color.BLACK
                        if sibling.left:
                            sibling.left.color = Color.BLACK
                        self._rotate_right(node.parent)
                    break

    def _is_black(self, node: Optional[RBNode]) -> bool:
        """Check if a node is black (None nodes are black)"""
        return node is None or node.color == Color.BLACK

    def _find_min(self, node: RBNode) -> RBNode:
        """Find node with minimum value"""
        while node.left:
            node = node.left
        return node

    def _rotate_left(self, node: RBNode) -> None:
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
        if not right_child:
            return

        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node

        right_child.parent = node.parent
        if not node.parent:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node: RBNode) -> None:
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
        if not left_child:
            return

        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node

        left_child.parent = node.parent
        if not node.parent:
            self.root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child

        left_child.right = node
        node.parent = left_child

    def search(self, value: int) -> bool:
        """Search for a value in the tree"""
        return self._find_node(self.root, value) is not None

    def in_order_traverse(self) -> list:
        """Get in-order traversal of tree"""
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node: Optional[RBNode], result: list) -> None:
        if node:
            self._in_order(node.left, result)
            result.append(node.value)
            self._in_order(node.right, result)
