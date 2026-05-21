import pytest
from bisection_method.square_root_bisection import square_root_bisection  # Replace 'your_module' with your actual file name


# --- 1. Parameter and Default Value Tests ---

def test_default_parameters_exist():
    """Verifies that tolerance and max_iterations have default values and can be omitted."""
    # This should execute successfully using default values
    result = square_root_bisection(4)
    assert result is not None
    # With default tolerance, sqrt(4) should be extremely close to 2
    assert abs(result - 2) <= 0.01 


# --- 2. Exception and Early Return Tests ---

def test_negative_number_raises_value_error():
    """User Story: Raise ValueError with specific message for negative inputs."""
    with pytest.raises(ValueError) as exc_info:
        square_root_bisection(-4)
    
    assert str(exc_info.value) == "Square root of negative number is not defined in real numbers"


@pytest.mark.parametrize("input_val", [0, 1, 0.0, 1.0])
def test_boundary_zero_and_one(capsys, input_val):
    """User Story: Quick-return 0 and 1, printing the exact match string."""
    result = square_root_bisection(input_val)
    
    # Check exact return value
    assert result == input_val
    
    # Check printed message format
    captured = capsys.readouterr()
    expected_msg = f"The square root of {input_val} is {input_val}\n"
    assert captured.out == expected_msg


# --- 3. Convergence & Success Mapping Tests ---

@pytest.mark.parametrize("target, expected_root, tolerance", [
    (4, 2.0, 0.001),
    (9, 3.0, 0.01),
    (0.25, 0.5, 0.0001),  # Tests a fraction between 0 and 1
    (2, 1.4142, 0.001),   # Irrational root
])
def test_successful_convergence_printing(capsys, target, expected_root, tolerance):
    """User Story: Positive numbers print the approximate message and return the root."""
    result = square_root_bisection(target, tolerance=tolerance)
    
    # Ensure the returned value falls within the requested tolerance boundary
    assert abs(result - expected_root) <= tolerance
    
    # Check printed approximate message format
    captured = capsys.readouterr()
    assert f"The square root of {target} is approximately" in captured.out
    assert str(result) in captured.out


# --- 4. Failure to Converge Tests ---

def test_failed_to_converge(capsys):
    """User Story: Print failure message and return None if iterations run out."""
    # Forcing failure by limiting max iterations to 1 on a hard calculation
    result = square_root_bisection(2, tolerance=0.00001, max_iterations=1)
    
    # Must explicitly return None
    assert result is None
    
    # Verify the failure string output matches the max iteration constraint
    captured = capsys.readouterr()
    assert "Failed to converge within 1 iterations" in captured.out