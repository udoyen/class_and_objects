import unittest
from merge_sort.sample_sort import merge_sort  # Adjust import to match your file name

class TestMergeSortUnittest(unittest.TestCase):

    # --- Standard Functionality Tests ---
    def test_sample_one_odd_length(self):
        sample = [38, 27, 43, 3, 9, 82, 10]
        self.assertEqual(merge_sort(sample), [3, 9, 10, 27, 38, 43, 82])

    def test_sample_two_with_duplicates(self):
        sample = [5, 2, 9, 1, 5]
        self.assertEqual(merge_sort(sample), [1, 2, 5, 5, 9])

    def test_reversed_array(self):
        self.assertEqual(merge_sort([10, 9, 8, 7, 6]), [6, 7, 8, 9, 10])

    # --- Structural Edge Cases ---
    def test_empty_array(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_item_array(self):
        self.assertEqual(merge_sort([99]), [99])

    def test_identical_elements(self):
        self.assertEqual(merge_sort([1, 1, 1]), [1, 1, 1])

    def test_negative_values(self):
        self.assertEqual(merge_sort([-3, -1, -7, 2, 0]), [-7, -3, -1, 0, 2])

    def test_immutability(self):
        """Verifies original input array state is fully preserved outside function execution."""
        original = [5, 4, 3]
        _ = merge_sort(original)
        self.assertEqual(original, [5, 4, 3])

if __name__ == "__main__":
    unittest.main()