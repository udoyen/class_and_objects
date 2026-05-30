import pytest
import inspect

# Import your file as an alias to test the structure safely
from graph_problems import graph_converter as target_file

# --- 1. Structural & Parameter Tests ---

def test_function_exists_and_callable():
    """User Story 1: You should define a function named adjacency_list_to_matrix."""
    assert hasattr(target_file, "adjacency_list_to_matrix"), "Function must be named 'adjacency_list_to_matrix'"
    assert callable(target_file.adjacency_list_to_matrix), "'adjacency_list_to_matrix' must be a function"

def test_function_has_one_parameter():
    """User Story 2: The function should have exactly one parameter."""
    sig = inspect.signature(target_file.adjacency_list_to_matrix)
    assert len(sig.parameters) == 1, "The function must accept exactly one argument (the adjacency list)."


# --- 2. Print Output Test (Using capsys) ---

def test_function_prints_each_row(capsys):
    """User Story 5: The function should print each row of the matrix."""
    adj_list = {0: [1], 1: [0]}
    
    # Run the function to trigger the print statements
    target_file.adjacency_list_to_matrix(adj_list)
    
    # Capture the printed output
    captured = capsys.readouterr()
    printed_text = captured.out.strip()
    
    # Check if the output contains the string representation of the rows
    assert "[0, 1]" in printed_text
    assert "[1, 0]" in printed_text
    
    # Ensure there's a newline separating the rows
    assert "\n" in printed_text, "Each row must be printed on a new line."


# --- 3. Matrix Conversion Logic Tests ---

@pytest.mark.parametrize("adj_list, expected_matrix", [
    (
        # User Story 7: The main 4-node example
        {0: [1, 2], 1: [2], 2: [0, 3], 3: [2]}, 
        [
            [0, 1, 1, 0], 
            [0, 0, 1, 0], 
            [1, 0, 0, 1], 
            [0, 0, 1, 0]
        ]
    ),
    (
        # User Story 8: Simple 2-node graph
        {0: [1], 1: [0]}, 
        [
            [0, 1], 
            [1, 0]
        ]
    ),
    (
        # User Story 9: Disconnected nodes (no edges)
        {0: [], 1: [], 2: []}, 
        [
            [0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0]
        ]
    )
])
def test_adjacency_list_to_matrix_logic(adj_list, expected_matrix):
    """User Stories 3, 4, 6, 7, 8, 9: Tests accurate sizing, mapping, and returning."""
    
    result = target_file.adjacency_list_to_matrix(adj_list)
    
    # User Story 6: The function should return the adjacency matrix.
    assert isinstance(result, list), "The function must return a list of lists."
    
    # User Stories 3, 4, 7-9: Ensure the output exactly matches the expected matrix.
    assert result == expected_matrix