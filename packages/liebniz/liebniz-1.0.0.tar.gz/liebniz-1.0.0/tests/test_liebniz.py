import unittest
from liebnizlib.liebniz import ECCmod, chaos, compute_formula

class TestCore(unittest.TestCase):
    def test_ECCmod(self):
        self.assertEqual(ECCmod(5, 3), 1)  # Example test case

    def test_chaos(self):
        self.assertAlmostEqual(chaos(1, 2), 0.49315059, places=7)

    def test_compute_formula(self):
        # Add test cases for compute_formula
        pass