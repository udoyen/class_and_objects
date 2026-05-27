import pytest
from quick_sort.quick_sort import quick_sort  # Replace 'your_module' with your actual file name
import quick_sort.quick_sort as target_file

def test_quick_sort_function_exists():
    """Explicitly checks that a function named 'quick_sort' exists in the file."""
    
    # hasattr asks: "Does 'your_module' have an attribute named 'quick_sort'?"
    assert hasattr(target_file, "quick_sort") is True, "Function must be named exactly 'quick_sort'"
    
    # Optional: Verify that the name actually belongs to a callable function
    assert callable(target_file.quick_sort) is True, "'quick_sort' must be a function"
# --- 1. Base Case Tests (Recursion Stoppers) ---

def test_empty_list():
    """If the list is empty, it should return an empty list."""
    assert quick_sort([]) == []

def test_single_element_list():
    """If the list has one element, it is already sorted."""
    assert quick_sort([42]) == [42]


# --- 2. Standard Sorting Tests ---

@pytest.mark.parametrize("unordered, expected", [
    ([3, 6, 8, 10, 1, 2, 1], [1, 1, 2, 3, 6, 8, 10]),
    ([10, 9, 8, 7, 6, 5], [5, 6, 7, 8, 9, 10]),       # Reverse sorted
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),               # Already sorted
    ([0, -5, 10, -22, 3, -5], [-22, -5, -5, 0, 3, 10]) # Mixed negative/positive
])
def test_sorting_various_configurations(unordered, expected):
    """Verifies that the algorithm correctly sorts various list configurations."""
    assert quick_sort(unordered) == expected


# --- 3. The "Equal to Pivot" Partition Requirement ---

def test_list_with_duplicates():
    """
    This specifically tests your 3-partition requirement.
    If you don't create an 'equal to pivot' sublist, lists with heavy duplicates
    often cause infinite recursion or drop elements.
    """
    assert quick_sort([5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5]
    assert quick_sort([4, 2, 4, 2, 4, 2]) == [2, 2, 2, 4, 4, 4]


# --- 4. Return Value Requirement ---

def test_returns_new_list_not_mutated():
    """
    User Story: "return a new list of these integers in sorted order"
    This ensures you aren't sorting the list in-place (like list.sort() does).
    """
    original_list = [5, 2, 9, 1, 5, 6]
    # Create a copy to compare against later
    original_copy = original_list.copy() 
    
    sorted_list = quick_sort(original_list)
    
    # 1. The new list should be sorted
    assert sorted_list == [1, 2, 5, 5, 6, 9]
    
    # 2. The original list must remain completely untouched
    assert original_list == original_copy
    
    # 3. They must be two completely different objects in memory
    assert sorted_list is not original_list