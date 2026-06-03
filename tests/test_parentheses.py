import pytest

# Import your function
from graph_problems.parentheses import gen_parentheses 

# --- 1. Type Validation Edge Cases ---

@pytest.mark.parametrize("invalid_type", [
    3.14,       # Float
    "3",        # String
    None,       # NoneType
    [3],        # List
    {"pairs": 3}# Dictionary
])
def test_rejects_non_integers(invalid_type):
    """Verifies that passing anything other than an int returns the specific error string."""
    expected_error = 'The number of pairs should be an integer'
    assert gen_parentheses(invalid_type) == expected_error


# --- 2. Boundary Edge Cases (< 1) ---

@pytest.mark.parametrize("invalid_value", [
    0, 
    -1, 
    -99
])
def test_rejects_values_less_than_one(invalid_value):
    """Verifies that passing integers less than 1 returns the specific error string."""
    expected_error = 'The number of pairs should be at least 1'
    assert gen_parentheses(invalid_value) == expected_error


# --- 3. Standard Generation Tests ---

def test_one_pair():
    """The smallest valid input."""
    assert gen_parentheses(1) == ['()']

def test_two_pairs():
    """Testing n=2. We use sorted() to ensure the test passes regardless of the list order."""
    expected = ['(())', '()()']
    assert sorted(gen_parentheses(2)) == sorted(expected)

def test_three_pairs():
    """Testing the example n=3 case."""
    expected = ['((()))', '(()())', '(())()', '()(())', '()()()']
    assert sorted(gen_parentheses(3)) == sorted(expected)


# --- 4. Mathematical Integrity (Advanced Edge Case) ---

def test_four_pairs_catalan_number():
    """
    The number of valid parenthesis combinations is defined by the Catalan Number sequence.
    For n=4, the 4th Catalan number is 14. 
    This test ensures no duplicates are generated and the exact right amount is returned.
    """
    result = gen_parentheses(4)
    
    # 1. Check length (must be exactly 14)
    assert len(result) == 14
    
    # 2. Check uniqueness (converting to a set removes duplicates)
    assert len(set(result)) == 14
    
    # 3. Quick structural check (every string must be exactly 8 characters long)
    for combination in result:
        assert len(combination) == 8