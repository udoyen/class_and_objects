import pytest

# Import your file as an alias to test the file structure
from luhn_algorithm import luhn_algorithm as target_file 

# --- 1. Structural Test ---

def test_verify_card_number_function_exists():
    """Explicitly checks that the required function exists and is named correctly."""
    assert hasattr(target_file, "verify_card_number"), "Function must be named 'verify_card_number'"
    assert callable(target_file.verify_card_number), "'verify_card_number' must be a function"


# --- 2. Lab Specific User Stories ---

@pytest.mark.parametrize("card_string, expected_result", [
    # The exact test cases provided in your lab instructions
    ("453914889", "VALID!"),
    ("4111-1111-1111-1111", "VALID!"),
    ("1234 5678 9012 3456", "INVALID!"),
    ("4539a14889", False),
    ("4111-1111-1111-111x", False),
    ("1234 5678 9012 345y", False)
])
def test_lab_required_cases(card_string, expected_result):
    """Tests the exact inputs and outputs requested by the lab grading table."""
    assert target_file.verify_card_number(card_string) == expected_result


# --- 3. Robust Edge Cases (Formatting) ---

def test_handles_dashes():
    """User Story: You should handle any dashes that may be present."""
    # A valid number chopped up with excessive dashes
    assert target_file.verify_card_number("4-5-3-9-1-4-8-8-9") == "VALID!"

def test_handles_spaces():
    """User Story: You should handle any spaces that may be present."""
    # A valid number chopped up with excessive spaces
    assert target_file.verify_card_number("4 5 3 9 1 4 8 8 9") == "VALID!"

def test_handles_mixed_formatting():
    """Ensures the function can handle combinations of spaces, dashes, and numbers."""
    assert target_file.verify_card_number("4111 - 1111 - 1111 - 1111") == "VALID!"
