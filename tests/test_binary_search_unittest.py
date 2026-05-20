import unittest
from binary_search.binary_search import binary_search  # Adjust import to your file layout

class TestBinarySearchUnittest(unittest.TestCase):

    def setUp(self):
        """Initializes reusable testing targets before each test method runs."""
        self.odd_list = [1, 2, 3, 4, 5]
        self.even_list = [1, 2, 3, 4, 5, 9]

    # --- Success Pathways ---
    def test_find_exact_middle_odd(self):
        path, msg = binary_search(self.odd_list, 3)
        self.assertEqual(path, [3])
        self.assertEqual(msg, "Value found at index 2")

    def test_find_left_boundary_odd(self):
        path, msg = binary_search(self.odd_list, 1)
        self.assertEqual(path, [3, 1])
        self.assertEqual(msg, "Value found at index 0")

    def test_find_right_boundary_even(self):
        path, msg = binary_search(self.even_list, 9)
        self.assertEqual(path, [3, 5, 9])
        self.assertEqual(msg, "Value found at index 5")

    # --- Edge Cases ---
    def test_empty_list(self):
        path, msg = binary_search([], 99)
        self.assertEqual(path, [])
        self.assertEqual(msg, "Value not found")

    def test_single_item_found(self):
        path, msg = binary_search([7], 7)
        self.assertEqual(path, [7])
        self.assertEqual(msg, "Value found at index 0")

    def test_single_item_not_found(self):
        path, msg = binary_search([7], 9)
        self.assertEqual(path, [])
        self.assertEqual(msg, "Value not found")

    def test_missing_item_complex_list(self):
        path, msg = binary_search([1, 3, 5, 9, 14, 22], 10)
        self.assertEqual(path, [])
        self.assertEqual(msg, "Value not found")

    def test_all_elements_identical(self):
        path, msg = binary_search([5, 5, 5, 5, 5, 5], 5)
        self.assertEqual(path, [5])
        self.assertEqual(msg, "Value found at index 2")

if __name__ == "__main__":
    unittest.main()