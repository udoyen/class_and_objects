import pytest

# Import your file as an alias to avoid namespace collisions
# Adjust "selection_sort.selection_sort" to match your actual structure
from selection_sort import selection_sort_algorithm as target_file 


# --- 1. Structural Test: Function Name ---

def test_selection_sort_function_exists():
    """Explicitly checks that a function named 'selection_sort' exists."""
    assert hasattr(target_file, "selection_sort"), "Function must be named exactly 'selection_sort'"
    assert callable(target_file.selection_sort), "'selection_sort' must be a function"


# --- 2. Standard Sorting Tests ---

@pytest.mark.parametrize("unordered, expected", [
    ([64, 25, 12, 22, 11], [11, 12, 22, 25, 64]),   # Standard random
    ([10, 9, 8, 7, 6], [6, 7, 8, 9, 10]),           # Completely reversed
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),             # Already sorted
    ([3, -1, -5, 2, 0], [-5, -1, 0, 2, 3]),         # Mixed with negatives
    ([4, 2, 4, 2, 4], [2, 2, 4, 4, 4]),             # Duplicates
    ([42], [42]),                                   # Single element
    ([], []),                                       # Empty list
])
def test_sorting_accuracy(unordered, expected):
    """Verifies that the algorithm accurately sorts various configurations."""
    # We use list() to pass a fresh copy of the list so parametrize data isn't permanently mutated
    assert target_file.selection_sort(list(unordered)) == expected


# --- 3. In-Place Modification Test ---

def test_sorts_in_place_and_returns():
    """
    User Story: modify the input list in-place, and return it once it's sorted.
    This proves you aren't creating a completely new list in memory.
    """
    original_list = [5, 3, 1, 4, 2]
    original_memory_id = id(original_list)
    
    returned_list = target_file.selection_sort(original_list)
    
    # 1. Check that the returned list is the exact same object in memory
    assert id(returned_list) == original_memory_id
    # 2. Check that the original variable was actually mutated
    assert original_list == [1, 2, 3, 4, 5]


# --- 4. Advanced: "No Unnecessary Swaps" Test ---

class SpyList(list):
    """
    A custom list wrapper that tracks how many times elements are swapped/reassigned.
    This allows us to test the specific 'no unnecessary swaps' requirement.
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.assignment_count = 0

    def __setitem__(self, key, value):
        self.assignment_count += 1
        super().__setitem__(key, value)


def test_no_unnecessary_swaps():
    """
    User Story: should not perform unnecessary swaps when the smallest element 
    is already in the correct position.
    """
    # Create an already sorted list using our tracker
    already_sorted = SpyList([1, 2, 3, 4, 5])
    target_file.selection_sort(already_sorted)
    
    # If the algorithm checks 'if min_index != current_index' before swapping,
    # zero assignments should occur on an already sorted list!
    assert already_sorted.assignment_count == 0, (
        "The algorithm performed a swap on an already sorted element! "
        "Make sure you check `if min_index != i:` before swapping."
    )
    
    # Let's test a list that needs exactly ONE swap (the first and last elements)
    needs_one_swap = SpyList([5, 2, 3, 4, 1])
    target_file.selection_sort(needs_one_swap)
    
    # A single Python swap (arr[a], arr[b] = arr[b], arr[a]) triggers __setitem__ twice.
    assert needs_one_swap.assignment_count == 2, "Algorithm performed more swaps than necessary."