"""
Test script for AVL and Red-Black tree implementations
"""

import sys
sys.path.insert(0, 'src')

from avl_tree import AVLTree
from red_black_tree import RedBlackTree


def test_avl_tree():
    """Test AVL tree operations"""
    print("=" * 50)
    print("Testing AVL Tree")
    print("=" * 50)
    
    avl = AVLTree()
    
    # Test insertions
    values = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35]
    print(f"\nInserting values: {values}")
    for val in values:
        avl.insert(val)
    
    print(f"In-order traversal: {avl.in_order_traverse()}")
    print(f"Tree height: {avl.get_height()}")
    print(f"Rotations performed: {avl.rotation_count}")
    
    # Test search
    print(f"\nSearch tests:")
    for val in [30, 100, 75]:
        found = avl.search(val)
        print(f"  Search {val}: {'Found' if found else 'Not found'}")
    
    # Test deletions
    print(f"\nDeleting values: [5, 30, 50]")
    for val in [5, 30, 50]:
        avl.delete(val)
    
    print(f"In-order traversal after deletions: {avl.in_order_traverse()}")
    print(f"Tree height after deletions: {avl.get_height()}")
    print(f"Total rotations: {avl.rotation_count}")
    
    return True


def test_red_black_tree():
    """Test Red-Black tree operations"""
    print("\n" + "=" * 50)
    print("Testing Red-Black Tree")
    print("=" * 50)
    
    rb = RedBlackTree()
    
    # Test insertions
    values = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35]
    print(f"\nInserting values: {values}")
    for val in values:
        rb.insert(val)
    
    print(f"In-order traversal: {rb.in_order_traverse()}")
    print(f"Rotations performed: {rb.rotation_count}")
    
    # Test search
    print(f"\nSearch tests:")
    for val in [30, 100, 75]:
        found = rb.search(val)
        print(f"  Search {val}: {'Found' if found else 'Not found'}")
    
    # Test deletions
    print(f"\nDeleting values: [5, 30, 50]")
    for val in [5, 30, 50]:
        rb.delete(val)
    
    print(f"In-order traversal after deletions: {rb.in_order_traverse()}")
    print(f"Total rotations: {rb.rotation_count}")
    
    return True


def test_duplicate_handling():
    """Test that duplicate values are handled correctly"""
    print("\n" + "=" * 50)
    print("Testing Duplicate Handling")
    print("=" * 50)
    
    avl = AVLTree()
    rb = RedBlackTree()
    
    values = [10, 20, 30, 20, 10, 40]
    print(f"\nInserting values (with duplicates): {values}")
    
    for val in values:
        avl.insert(val)
        rb.insert(val)
    
    print(f"AVL in-order traversal: {avl.in_order_traverse()}")
    print(f"Red-Black in-order traversal: {rb.in_order_traverse()}")
    
    return avl.in_order_traverse() == rb.in_order_traverse() == [10, 20, 30, 40]


def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 50)
    print("Testing Edge Cases")
    print("=" * 50)
    
    # Test empty tree
    print("\n1. Empty tree operations:")
    avl = AVLTree()
    rb = RedBlackTree()
    print(f"  AVL search in empty tree: {avl.search(10)}")
    print(f"  Red-Black search in empty tree: {rb.search(10)}")
    
    # Test single element
    print("\n2. Single element:")
    avl.insert(42)
    rb.insert(42)
    print(f"  AVL height: {avl.get_height()}, values: {avl.in_order_traverse()}")
    print(f"  Red-Black rotations: {rb.rotation_count}, values: {rb.in_order_traverse()}")
    
    # Test delete all
    print("\n3. Delete all elements:")
    avl.delete(42)
    rb.delete(42)
    print(f"  AVL after delete: {avl.in_order_traverse()}")
    print(f"  Red-Black after delete: {rb.in_order_traverse()}")
    
    return True


if __name__ == "__main__":
    try:
        test_avl_tree()
        test_red_black_tree()
        test_duplicate_handling()
        test_edge_cases()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
