import unittest
import decimal
from napier.utilities.napierbone import generate_keys
from napier.utilities.napiermath import custom_summation
from napier.config import P, Gx, Gy

class TestNapier(unittest.TestCase):
    def test_generate_keys(self):
        private_key, public_key = generate_keys(P, Gx, Gy)
        self.assertTrue(1 <= private_key < P)
        self.assertIsInstance(public_key, tuple)
        self.assertEqual(len(public_key), 2)

    def test_custom_summation(self):
        result = custom_summation(P, 10)
        self.assertIsInstance(result, decimal.Decimal)  # Check if the result is a Decimal
        self.assertGreater(result, decimal.Decimal(0))  # Check if the result is positive

if __name__ == "__main__":
    unittest.main()
