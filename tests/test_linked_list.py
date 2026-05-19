import pytest
from linked_list.linked_list import LinkedList  # Adjust this import to match your folder structure

# --- Fixtures ---
@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def populated_list():
    ll = LinkedList()
    ll.add("A")
    ll.add("B")
    ll.add("C")
    return ll


# --- Tests for Initialization & State ---
def test_initialization(empty_list):
    """Ensures a newly initialized list is empty and has a length of 0."""
    assert empty_list.is_empty() is True
    assert empty_list.length == 0
    assert empty_list.head is None


# --- Tests for Adding Elements ---
def test_add_to_empty_list(empty_list):
    """Tests that adding an element to an empty list correctly sets the head."""
    empty_list.add(10)
    assert empty_list.is_empty() is False
    assert empty_list.length == 1
    assert empty_list.head.element == 10
    assert empty_list.head.next is None

def test_add_multiple_elements(empty_list):
    """Verifies that elements append to the end of the chain sequentially."""
    empty_list.add(10)
    empty_list.add(20)
    empty_list.add(30)
    
    assert empty_list.length == 3
    # Step through the nodes manually to verify structure
    node_1 = empty_list.head
    assert node_1.element == 10
    
    node_2 = node_1.next
    assert node_2.element == 20
    
    node_3 = node_2.next
    assert node_3.element == 30
    assert node_3.next is None


# --- Edge Case Tests for Removing Elements ---
def test_remove_from_empty_list(empty_list):
    """Edge Case: Removing an item from a list with 0 elements should fail gracefully."""
    empty_list.remove(5)
    assert empty_list.length == 0
    assert empty_list.head is None

def test_remove_only_element(empty_list):
    """Edge Case: Removing the sole item returns the list to a clean, empty state."""
    empty_list.add(99)
    empty_list.remove(99)
    assert empty_list.is_empty() is True
    assert empty_list.length == 0
    assert empty_list.head is None

def test_remove_head_element(populated_list):
    """Edge Case: Removing the head shifts the list tracking forward to the next node."""
    # List looks like: A -> B -> C
    populated_list.remove("A")
    
    assert populated_list.length == 2
    assert populated_list.head.element == "B"
    assert populated_list.head.next.element == "C"

def test_remove_middle_element(populated_list):
    """Tests if removing a middle element properly stitches the surrounding links."""
    # List looks like: A -> B -> C
    populated_list.remove("B")
    
    assert populated_list.length == 2
    assert populated_list.head.element == "A"
    assert populated_list.head.next.element == "C"  # Link skipped B directly to C

def test_remove_tail_element(populated_list):
    """Tests if removing the last element leaves the new tail pointing to None."""
    # List looks like: A -> B -> C
    populated_list.remove("C")
    
    assert populated_list.length == 2
    assert populated_list.head.element == "A"
    assert populated_list.head.next.element == "B"
    assert populated_list.head.next.next is None  # B is now the tail

def test_remove_non_existent_element(populated_list):
    """Edge Case: Requesting to remove an element not in the list changes nothing."""
    # List looks like: A -> B -> C
    populated_list.remove("Z")
    
    assert populated_list.length == 3
    assert populated_list.head.element == "A"
    assert populated_list.head.next.element == "B"
    assert populated_list.head.next.next.element == "C"


# --- Tests for Duplicate Values ---
def test_remove_first_duplicate_only(empty_list):
    """Edge Case: If duplicate entries exist, remove() should only drop the first occurrence."""
    empty_list.add("X")
    empty_list.add("Y")
    empty_list.add("X")
    
    empty_list.remove("X")
    
    assert empty_list.length == 2
    assert empty_list.head.element == "Y"
    assert empty_list.head.next.element == "X"  # The second 'X' is still there