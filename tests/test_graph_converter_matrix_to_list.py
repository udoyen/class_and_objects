import pytest
import inspect

# Import your file as an alias to test the structure safely
from graph_problems import graph_converter as target_file

# --- 1. Structural & Parameter Tests ---

def test_reverse_function_exists():
    """Checks that a function named 'adjacency_matrix_to_list' exists."""
    assert hasattr(target_file, "adjacency_matrix_to_list"), "Function must be named 'adjacency_matrix_to_list'"
    assert callable(target_file.adjacency_matrix_to_list), "'adjacency_matrix_to_list' must be a function"

def test_reverse_function_has_one_parameter():
    """The function should accept exactly one argument (the matrix)."""
    sig = inspect.signature(target_file.adjacency_matrix_to_list)
    assert len(sig.parameters) == 1, "The function must accept exactly one argument."


# --- 2. Logic & Conversion Tests ---

@pytest.mark.parametrize("matrix, expected_list", [
    (
        # The main 4-node example (Reversed)
        [
            [0, 1, 1, 0], 
            [0, 0, 1, 0], 
            [1, 0, 0, 1], 
            [0, 0, 1, 0]
        ],
        {0: [1, 2], 1: [2], 2: [0, 3], 3: [2]}
    ),
    (
        # Simple 2-node graph
        [
            [0, 1], 
            [1, 0]
        ],
        {0: [1], 1: [0]}
    ),
    (
        # Disconnected nodes (no edges, completely empty matrix)
        [
            [0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0]
        ],
        {0: [], 1: [], 2: []}
    ),
    (
        # Edge Case: Completely empty graph
        [], 
        {}
    )
])
def test_adjacency_matrix_to_list_logic(matrix, expected_list):
    """Tests if the function accurately converts matrices back to dictionaries."""
    
    # Run the function
    result = target_file.adjacency_matrix_to_list(matrix)
    
    # Verify the return type is correct
    assert isinstance(result, dict), "The function must return a dictionary."
    
    # Verify the logic perfectly matches the expected adjacency list
    assert result == expected_list