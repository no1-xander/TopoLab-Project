import unittest
from topolab.core.example_validation import check_finite_topology_example

class FiniteExampleTests(unittest.TestCase):
    def test_valid_example_and_operators(self):
        r = check_finite_topology_example("a,b,c,d", "∅;X;a;d;a,d", "a,b,c")
        self.assertTrue(r["valid"])
        self.assertEqual(r["interior"], "{a}")
        self.assertEqual(r["closure"], "{a, b, c, d}")
        self.assertEqual(r["boundary"], "{b, c, d}")
        self.assertFalse(r["hausdorff"])

    def test_missing_empty_set_rejected(self):
        r = check_finite_topology_example("a,b", "X;a")
        self.assertFalse(r["valid"])
        self.assertIn("empty set", " ".join(r["errors"]).lower())

    def test_non_topology_rejected(self):
        self.assertFalse(check_finite_topology_example("a,b", "∅;X;a")["isTopology"])

    def test_subset_outside_universe_rejected(self):
        self.assertFalse(check_finite_topology_example("a,b", "∅;X", "c")["valid"])

    def test_indiscrete_space_not_hausdorff(self):
        r = check_finite_topology_example("a,b", "∅;X", "a")
        self.assertTrue(r["valid"])
        self.assertFalse(r["hausdorff"])

    def test_discrete_space_hausdorff(self):
        r = check_finite_topology_example("a,b", "∅;a;b;X")
        self.assertTrue(r["valid"])
        self.assertTrue(r["hausdorff"])

if __name__ == "__main__":
    unittest.main()
