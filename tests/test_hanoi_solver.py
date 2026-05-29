import pytest

# Import your file as an alias to test the file structure (like we did before!)
from hanoi_solver import hanoi_solver as target_file 

# --- 1. Structural & Type Tests ---

def test_hanoi_solver_function_exists():
    """User Story 1 & 2: Checks that the function exists and accepts arguments."""
    assert hasattr(target_file, "hanoi_solver"), "Function must be named 'hanoi_solver'"
    assert callable(target_file.hanoi_solver), "'hanoi_solver' must be a callable function"

def test_hanoi_solver_returns_string():
    """User Story 3: Your function should return a string."""
    # We pass n=1 to ensure the function runs and returns its data type
    result = target_file.hanoi_solver(1)
    assert isinstance(result, str), "The function must return a string type, not a list or print directly."


# --- 2. Lab Required Exact Match Tests ---

@pytest.mark.parametrize("n, expected_output", [
    (
        2, 
        "[2, 1] [] []\n[2] [1] []\n[] [1] [2]\n[] [] [2, 1]"
    ),
    (
        3, 
        "[3, 2, 1] [] []\n[3, 2] [] [1]\n[3] [2] [1]\n[3] [2, 1] []\n[] [2, 1] [3]\n[1] [2] [3]\n[1] [] [3, 2]\n[] [] [3, 2, 1]"
    ),
    (
        4, 
        "[4, 3, 2, 1] [] []\n[4, 3, 2] [1] []\n[4, 3] [1] [2]\n[4, 3] [] [2, 1]\n[4] [3] [2, 1]\n[4, 1] [3] [2]\n[4, 1] [3, 2] []\n[4] [3, 2, 1] []\n[] [3, 2, 1] [4]\n[] [3, 2] [4, 1]\n[2] [3] [4, 1]\n[2, 1] [3] [4]\n[2, 1] [] [4, 3]\n[2] [1] [4, 3]\n[] [1] [4, 3, 2]\n[] [] [4, 3, 2, 1]"
    ),
    (
        5, 
        "[5, 4, 3, 2, 1] [] []\n[5, 4, 3, 2] [] [1]\n[5, 4, 3] [2] [1]\n[5, 4, 3] [2, 1] []\n[5, 4] [2, 1] [3]\n[5, 4, 1] [2] [3]\n[5, 4, 1] [] [3, 2]\n[5, 4] [] [3, 2, 1]\n[5] [4] [3, 2, 1]\n[5] [4, 1] [3, 2]\n[5, 2] [4, 1] [3]\n[5, 2, 1] [4] [3]\n[5, 2, 1] [4, 3] []\n[5, 2] [4, 3] [1]\n[5] [4, 3, 2] [1]\n[5] [4, 3, 2, 1] []\n[] [4, 3, 2, 1] [5]\n[1] [4, 3, 2] [5]\n[1] [4, 3] [5, 2]\n[] [4, 3] [5, 2, 1]\n[3] [4] [5, 2, 1]\n[3] [4, 1] [5, 2]\n[3, 2] [4, 1] [5]\n[3, 2, 1] [4] [5]\n[3, 2, 1] [] [5, 4]\n[3, 2] [] [5, 4, 1]\n[3] [2] [5, 4, 1]\n[3] [2, 1] [5, 4]\n[] [2, 1] [5, 4, 3]\n[1] [2] [5, 4, 3]\n[1] [] [5, 4, 3, 2]\n[] [] [5, 4, 3, 2, 1]"
    )
])
def test_exact_lab_matches(n, expected_output):
    """User Story 4-7: Tests the exact string outputs required by the grading script."""
    assert target_file.hanoi_solver(n) == expected_output


# --- 3. Edge Cases & Algorithmic Rule Tests ---

def test_edge_case_single_disk():
    """Edge Case: The absolute minimum valid puzzle size (1 disk)."""
    # Should take exactly 1 move (2 lines of text)
    expected = "[1] [] []\n[] [] [1]"
    assert target_file.hanoi_solver(1) == expected

def test_edge_case_zero_disks():
    """Edge Case: Passing 0 should theoretically just return empty rods with no moves."""
    expected = "[] [] []"
    assert target_file.hanoi_solver(0) == expected

def test_mathematical_move_count():
    """
    User Story 8: 'hanoi_solver(n) should solve the tower... for any positive value'.
    The rule states it must take exactly (2^n - 1) moves.
    This test verifies the math holds up for larger numbers without hardcoding the strings!
    """
    n = 6
    result = target_file.hanoi_solver(n)
    
    # Split the returned string by newlines to count how many states were printed
    printed_states = result.strip().split('\n')
    
    # 2^n - 1 moves PLUS the 1 starting state = exactly 2^n total lines printed
    expected_lines = 2 ** n 
    
    assert len(printed_states) == expected_lines, f"A puzzle of size {n} should take exactly {expected_lines} lines of output."