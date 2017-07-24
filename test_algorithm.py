import unittest
from algorithm import avg
from algorithm import power_management


class AlgorithmTestCase(unittest.TestCase):
    """Test for 'algorithm.py'."""

    def test_average_of_numbers_sequence(self):
        """Test for function calculating average of numbers sequence"""
        self.assertEqual(avg((1, 2, 3, 4)), -79)

    def test_power_management(self):
        """Test if powe management function is working properly"""
        self.assertEqual(power_management(), [])

if __name__ == '__main__':
    unittest.main()
