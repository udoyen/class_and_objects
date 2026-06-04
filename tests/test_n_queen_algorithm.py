import pytest
import inspect

# Import your file as an alias (change 'queens_solver' to your actual filename)
import graph_problems.n_queen_algorithm as target_file

# --- 1. Structural & Input Tests ---

def test_dfs_n_queens_function_exists():
    """User Story 1: You should have a function named dfs_n_queens."""
    assert hasattr(target_file, "dfs_n_queens"), "Function must be named 'dfs_n_queens'"
    
    sig = inspect.signature(target_file.dfs_n_queens)
    assert len(sig.parameters) == 1, "The dfs_n_queens function must accept exactly one argument."

def test_invalid_n_returns_empty_list():
    """User Story 2: If n is less than 1, return an empty list."""
    assert target_file.dfs_n_queens(0) == []
    assert target_file.dfs_n_queens(-5) == []


# --- 2. Lab Required Exact Match Tests ---

@pytest.mark.parametrize("n, expected_solutions", [
    (1, [[0]]),                         # User Story 4
    (2, []),                            # User Story 5
    (3, []),                            # User Story 6
    (4, [[1, 3, 0, 2], [2, 0, 3, 1]]),  # User Story 7
])
def test_exact_solution_matches(n, expected_solutions):
    """User Stories 4, 5, 6, 7: Tests the exact arrays returned for smaller boards."""
    result = target_file.dfs_n_queens(n)
    
    # User Story 3 check: Verify it's a list of lists
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0], list)
        
    # Sort both just in case the algorithm finds them in a different order
    assert sorted(result) == sorted(expected_solutions)


def test_n_equals_5():
    """User Story 8 & 9: Tests N=5 solutions and exact count."""
    expected = [
        [0, 2, 4, 1, 3], [0, 3, 1, 4, 2], [1, 3, 0, 2, 4], 
        [1, 4, 2, 0, 3], [2, 0, 3, 1, 4], [2, 4, 1, 3, 0], 
        [3, 0, 2, 4, 1], [3, 1, 4, 2, 0], [4, 1, 3, 0, 2], 
        [4, 2, 0, 3, 1]
    ]
    result = target_file.dfs_n_queens(5)
    
    assert len(result) == 10
    assert sorted(result) == sorted(expected)


def test_n_equals_8_count():
    """User Story 10: Tests the classic 8-Queens problem total count."""
    result = target_file.dfs_n_queens(8)
    assert len(result) == 92