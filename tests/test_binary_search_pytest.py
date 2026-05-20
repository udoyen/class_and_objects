import pytest
from binary_search.binary_search import binary_search  # Adjust import to your file layout

# --- Structural Data Fixtures ---
@pytest.fixture
def clean_odd_list():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def clean_even_list():
    return [1, 2, 3, 4, 5, 9]


# --- Parametrized Test Scenarios ---
@pytest.mark.parametrize("target, expected_path, expected_msg", [
    (3, [3], "Value found at index 2"),       # Exact middle element
    (1, [3, 1], "Value found at index 0"),    # Left extreme boundary
    (5, [3, 4, 5], "Value found at index 4"), # Right extreme boundary
])
def test_odd_length_list_searches(clean_odd_list, target, expected_path, expected_msg):
    """Verifies search paths and success strings in an odd-length list."""
    path, msg = binary_search(clean_odd_list, target)
    assert path == expected_path
    assert msg == expected_msg


@pytest.mark.parametrize("target, expected_path, expected_msg", [
    (3, [3], "Value found at index 2"),          # Left-leaning middle index
    (4, [3, 5, 4], "Value found at index 3"),    # Right-leaning middle index
    (9, [3, 5, 9], "Value found at index 5"),    # Far right item
])
def test_even_length_list_searches(clean_even_list, target, expected_path, expected_msg):
    """Verifies execution behaviors in an even-length list where mid leans left."""
    path, msg = binary_search(clean_even_list, target)
    assert path == expected_path
    assert msg == expected_msg


# --- Core Edge Case Tests ---
def test_search_in_empty_list():
    """Edge Case: Searching an empty collection must drop out immediately."""
    path, msg = binary_search([], 10)
    assert path == []
    assert msg == "Value not found"


def test_search_single_element_list_success():
    """Edge Case: Target matches the single element in the collection."""
    path, msg = binary_search([42], 42)
    assert path == [42]
    assert msg == "Value found at index 0"


def test_search_single_element_list_failure():
    """Edge Case: Target is missing from a single element collection."""
    path, msg = binary_search([42], 7)
    assert path == []
    assert msg == "Value not found"


def test_target_missing_returns_empty_path():
    """Edge Case: A missing item returns an empty path per the code's return statement."""
    # Elements evaluated before failing: 5 -> 14 -> 9 -> out of bounds
    path, msg = binary_search([1, 3, 5, 9, 14, 22], 10)
    assert path == []
    assert msg == "Value not found"


def test_duplicate_elements_returns_first_encountered_mid():
    """Edge Case: Arrays with duplicates resolve at the calculated middle index entry."""
    # Mid calculation will stop at the first duplicate index it structurally strikes
    path, msg = binary_search([2, 2, 2, 2, 2], 2)
    assert path == [2]
    assert msg == "Value found at index 2"