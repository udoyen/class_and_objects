import pytest
from merge_sort.sample_sort import merge_sort  # Adjust import to match your file name

# --- Parametrizing standard arrays to test various structures ---
@pytest.mark.parametrize("unordered, expected", [
    ([38, 27, 43, 3, 9, 82, 10], [3, 9, 10, 27, 38, 43, 82]), # Standard odd length
    ([5, 2, 9, 1, 5], [1, 2, 5, 5, 9]),                     # Even-ish with duplicate
    ([4, 3, 2, 1], [1, 2, 3, 4]),                           # Completely reversed list
    ([1, 2, 3, 4], [1, 2, 3, 4]),                           # Already sorted list
])
def test_standard_sorting_scenarios(unordered, expected):
    """Verifies that merge_sort correctly sorts different list configurations."""
    assert merge_sort(unordered) == expected


# --- Core Edge Case Tests ---
def test_empty_list():
    """Edge Case: An empty list should safely return an empty list instantly."""
    assert merge_sort([]) == []


def test_single_element_list():
    """Edge Case: A single item list hits the base case and returns untouched."""
    assert merge_sort([42]) == [42]


def test_all_elements_identical():
    """Edge Case: A list where all items are identical retains structural stability."""
    assert merge_sort([7, 7, 7, 7]) == [7, 7, 7, 7]


def test_negative_and_mixed_numbers():
    """Edge Case: Verifies that negative values sort to the left of positive values."""
    mixed_list = [0, -5, 10, -22, 3, -5]
    expected_sorted = [-22, -5, -5, 0, 3, 10]
    assert merge_sort(mixed_list) == expected_sorted


def test_does_not_mutate_original_list():
    """Edge Case: Ensure the merge_sort function does not modify the original list in-place."""
    original = [3, 1, 2]
    sorted_copy = merge_sort(original)
    
    assert sorted_copy == [1, 2, 3]
    assert original == [3, 1, 2]  # Original list must remain unsorted