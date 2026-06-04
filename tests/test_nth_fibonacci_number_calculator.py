import pytest
import inspect
import ast

# Import your file as an alias (change 'fib_calc' to your actual filename)
import dynamic_programming.nth_fibonacci_number_calculator as target_file

# --- 1. Structural & Input Tests ---

def test_fibonacci_function_exists():
    """User Story 1 & 2: You should have a function named fibonacci that takes one parameter."""
    assert hasattr(target_file, "fibonacci"), "Function must be named 'fibonacci'"
    
    sig = inspect.signature(target_file.fibonacci)
    assert len(sig.parameters) == 1, "The function must accept exactly one argument."


# --- 2. Lab Required Exact Match Tests ---

@pytest.mark.parametrize("n, expected", [
    (0, 0),     # User Story 4
    (1, 1),     # User Story 5
    (2, 1),     # User Story 6
    (3, 2),     # User Story 7
    (5, 5),     # User Story 8
    (10, 55),   # User Story 9
    (15, 610),  # User Story 10
])
def test_fibonacci_values(n, expected):
    """User Stories 4-10: Tests the exact values returned."""
    assert target_file.fibonacci(n) == expected


# --- 3. Internal Code Requirement Tests (Using AST) ---

def test_internal_code_requirements():
    """User Stories 3 & 11: Checks the raw code for 'sequence = [0, 1]' and no recursion."""
    source = inspect.getsource(target_file.fibonacci)
    tree = ast.parse(source)
    
    # User Story 3: Check for `sequence = [0, 1]`
    sequence_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'sequence':
                    # Check if the assigned value is a list
                    if isinstance(node.value, ast.List):
                        # Extract the numbers from the list
                        vals = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
                        if vals == [0, 1]:
                            sequence_found = True
                            
    assert sequence_found, "You must initialize a list named 'sequence' exactly as [0, 1] inside the function."
    
    # User Story 11: Check that the function does not call itself (Recursion)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'fibonacci':
                pytest.fail("Recursion detected! You must use an iterative loop, not recursion.")