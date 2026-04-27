"""
Test the controller integration with shared state
"""

import sys
sys.path.insert(0, 'src')

from shared_state import state, ActiveTreeType
import controller


def test_controller_avl():
    """Test AVL tree operations through controller"""
    print("Testing AVL Tree Controller Integration")
    print("=" * 50)
    
    # Verify we start with AVL selected
    print(f"Active tree type: {state.tree_type}")
    assert state.tree_type == ActiveTreeType.AVL
    
    # Test insert
    print("\n1. Testing insert operations:")
    values = [50, 25, 75, 10, 30]
    for val in values:
        controller.insert_value(val)
        print(f"   Inserted {val}: {state.status_text}")
    
    # Check tree state
    tree = state.current_tree()
    print(f"   In-order: {tree.in_order_traverse()}")
    print(f"   Height: {tree.get_height()}")
    
    # Test search
    print("\n2. Testing search operations:")
    controller.search_value(30)
    print(f"   Search 30: {state.status_text}")
    
    controller.search_value(100)
    print(f"   Search 100: {state.status_text}")
    
    # Test delete
    print("\n3. Testing delete operations:")
    controller.delete_value(25)
    print(f"   Deleted 25: {state.status_text}")
    print(f"   In-order: {tree.in_order_traverse()}")


def test_controller_rb():
    """Test Red-Black tree operations through controller"""
    print("\n\nTesting Red-Black Tree Controller Integration")
    print("=" * 50)
    
    # Switch to Red-Black tree
    print("\n1. Switching to Red-Black tree:")
    controller.set_active_tree(ActiveTreeType.RED_BLACK)
    print(f"   Active tree: {state.tree_type}")
    print(f"   Status: {state.status_text}")
    
    # Test insert
    print("\n2. Testing insert operations:")
    values = [50, 25, 75, 10, 30]
    for val in values:
        controller.insert_value(val)
        print(f"   Inserted {val}: {state.status_text}")
    
    # Check tree state
    tree = state.current_tree()
    print(f"   In-order: {tree.in_order_traverse()}")
    
    # Test search
    print("\n3. Testing search operations:")
    controller.search_value(30)
    print(f"   Search 30: {state.status_text}")
    
    # Test delete
    print("\n4. Testing delete operations:")
    controller.delete_value(50)
    print(f"   Deleted 50: {state.status_text}")
    print(f"   In-order: {tree.in_order_traverse()}")


def test_tree_switching():
    """Test switching between trees preserves data"""
    print("\n\nTesting Tree Switching")
    print("=" * 50)
    
    # Reset and start with AVL
    state.avl_tree.root = None
    state.rb_tree.root = None
    controller.set_active_tree(ActiveTreeType.AVL)
    
    # Add values to AVL
    print("\n1. Adding values to AVL:")
    avl_values = [50, 25, 75]
    for val in avl_values:
        controller.insert_value(val)
    avl_tree = state.current_tree()
    print(f"   AVL values: {avl_tree.in_order_traverse()}")
    
    # Switch to Red-Black and add different values
    print("\n2. Switching to Red-Black and adding values:")
    controller.set_active_tree(ActiveTreeType.RED_BLACK)
    rb_values = [40, 20, 60]
    for val in rb_values:
        controller.insert_value(val)
    rb_tree = state.current_tree()
    print(f"   Red-Black values: {rb_tree.in_order_traverse()}")
    
    # Switch back to AVL and verify data is preserved
    print("\n3. Switching back to AVL:")
    controller.set_active_tree(ActiveTreeType.AVL)
    avl_tree = state.current_tree()
    print(f"   AVL values (should be unchanged): {avl_tree.in_order_traverse()}")
    assert avl_tree.in_order_traverse() == [25, 50, 75], "AVL data was not preserved!"
    
    # Switch back to Red-Black and verify
    print("\n4. Switching back to Red-Black:")
    controller.set_active_tree(ActiveTreeType.RED_BLACK)
    rb_tree = state.current_tree()
    print(f"   Red-Black values (should be unchanged): {rb_tree.in_order_traverse()}")
    assert rb_tree.in_order_traverse() == [20, 40, 60], "Red-Black data was not preserved!"
    
    print("\n✓ Tree switching works correctly!")


if __name__ == "__main__":
    try:
        test_controller_avl()
        test_controller_rb()
        test_tree_switching()
        
        print("\n" + "=" * 50)
        print("All controller tests passed! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
